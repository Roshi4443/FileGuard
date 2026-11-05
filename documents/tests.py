
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Document, DocumentPermission
from .forms import DocumentUploadForm


class DocumentSecurityTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            password='TestPassword123'
        )

        self.recipient = User.objects.create_user(
            username='recipient',
            password='TestPassword123'
        )

        self.unauthorized_user = User.objects.create_user(
            username='unauthorized',
            password='TestPassword123'
        )

        uploaded_file = SimpleUploadedFile(
            'test.txt',
            b'This is a test document.',
            content_type='text/plain'
        )

        self.document = Document.objects.create(
            owner=self.owner,
            title='Test Document',
            file=uploaded_file
        )

    def test_owner_can_download_document(self):
        self.client.login(
            username='owner',
            password='TestPassword123'
        )

        response = self.client.get(
            reverse('download_document', args=[self.document.id])
        )

        self.assertEqual(response.status_code, 200)

    def test_unauthorized_user_cannot_download(self):
        self.client.login(
            username='unauthorized',
            password='TestPassword123'
        )

        response = self.client.get(
            reverse('download_document', args=[self.document.id])
        )

        self.assertEqual(response.status_code, 302)

    def test_shared_user_can_download(self):
        DocumentPermission.objects.create(
            document=self.document,
            user=self.recipient,
            permission='READ',
            granted_by=self.owner
        )

        self.client.login(
            username='recipient',
            password='TestPassword123'
        )

        response = self.client.get(
            reverse('download_document', args=[self.document.id])
        )

        self.assertEqual(response.status_code, 200)

    def test_revoked_user_cannot_download(self):
        permission = DocumentPermission.objects.create(
            document=self.document,
            user=self.recipient,
            permission='READ',
            granted_by=self.owner
        )

        permission.delete()

        self.client.login(
            username='recipient',
            password='TestPassword123'
        )

        response = self.client.get(
            reverse('download_document', args=[self.document.id])
        )

        self.assertEqual(response.status_code, 302)

    def test_only_owner_can_share_document(self):
        self.client.login(
            username='unauthorized',
            password='TestPassword123'
        )

        response = self.client.get(
            reverse('share_document', args=[self.document.id])
        )

        self.assertEqual(response.status_code, 404)

    def test_audit_log_created_after_upload(self):
        from audit.models import AuditLog

        self.client.login(
            username='owner',
            password='TestPassword123'
        )

        uploaded_file = SimpleUploadedFile(
            'new_test.txt',
            b'New test document.',
            content_type='text/plain'
        )

        response = self.client.post(
            reverse('upload_document'),
            {
                'title': 'New Test Document',
                'file': uploaded_file
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            AuditLog.objects.filter(
                actor=self.owner,
                action='UPLOAD'
            ).exists()
        )

    def test_only_owner_can_revoke_permission(self):
        permission = DocumentPermission.objects.create(
            document=self.document,
            user=self.recipient,
            permission='READ',
            granted_by=self.owner
        )

        self.client.login(
            username='unauthorized',
            password='TestPassword123'
        )

        response = self.client.post(
            reverse(
                'revoke_permission',
                args=[self.document.id, permission.id]
            )
        )

        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            DocumentPermission.objects.filter(
                id=permission.id
            ).exists()
        )

    def test_edit_permission_user_can_download(self):
        DocumentPermission.objects.create(
            document=self.document,
            user=self.recipient,
            permission='EDIT',
            granted_by=self.owner
        )

        self.client.login(
            username='recipient',
            password='TestPassword123'
        )

        response = self.client.get(
            reverse('download_document', args=[self.document.id])
        )

        self.assertEqual(response.status_code, 200)


class DocumentUploadValidationTests(TestCase):

    def test_valid_text_file_is_accepted(self):
        uploaded_file = SimpleUploadedFile(
            'valid.txt',
            b'Valid UTF-8 document.',
            content_type='text/plain'
        )

        form = DocumentUploadForm(
            data={'title': 'Valid Document'},
            files={'file': uploaded_file}
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_unsupported_file_extension_is_rejected(self):
        uploaded_file = SimpleUploadedFile(
            'malicious.exe',
            b'Test content',
            content_type='application/octet-stream'
        )

        form = DocumentUploadForm(
            data={'title': 'Invalid Document'},
            files={'file': uploaded_file}
        )

        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors)

    def test_fake_pdf_file_is_rejected(self):
        uploaded_file = SimpleUploadedFile(
            'fake.pdf',
            b'This is not a real PDF file.',
            content_type='application/pdf'
        )

        form = DocumentUploadForm(
            data={'title': 'Fake PDF'},
            files={'file': uploaded_file}
        )

        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors)

    def test_empty_file_is_rejected(self):
        uploaded_file = SimpleUploadedFile(
            'empty.txt',
            b'',
            content_type='text/plain'
        )

        form = DocumentUploadForm(
            data={'title': 'Empty Document'},
            files={'file': uploaded_file}
        )

        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors)

    def test_file_over_10mb_is_rejected(self):
        uploaded_file = SimpleUploadedFile(
            'large.txt',
            b'A' * (10 * 1024 * 1024 + 1),
            content_type='text/plain'
        )

        form = DocumentUploadForm(
            data={'title': 'Large Document'},
            files={'file': uploaded_file}
        )

        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors)


class DocumentEditPermissionTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username='edit_owner',
            password='TestPassword123'
        )

        self.editor = User.objects.create_user(
            username='editor',
            password='TestPassword123'
        )

        self.reader = User.objects.create_user(
            username='reader',
            password='TestPassword123'
        )

        self.unauthorized = User.objects.create_user(
            username='edit_unauthorized',
            password='TestPassword123'
        )

        uploaded_file = SimpleUploadedFile(
            'original.txt',
            b'Original document content.',
            content_type='text/plain'
        )

        self.document = Document.objects.create(
            owner=self.owner,
            title='Original Document',
            file=uploaded_file
        )

    def test_owner_can_edit_document(self):
        self.client.login(
            username='edit_owner',
            password='TestPassword123'
        )

        response = self.client.post(
            reverse('edit_document', args=[self.document.id]),
            {
                'title': 'Updated by Owner'
            }
        )

        self.assertEqual(response.status_code, 302)

        self.document.refresh_from_db()

        self.assertEqual(
            self.document.title,
            'Updated by Owner'
        )

    def test_edit_permission_user_can_edit_document(self):
        DocumentPermission.objects.create(
            document=self.document,
            user=self.editor,
            permission='EDIT',
            granted_by=self.owner
        )

        self.client.login(
            username='editor',
            password='TestPassword123'
        )

        response = self.client.post(
            reverse('edit_document', args=[self.document.id]),
            {
                'title': 'Updated by Editor'
            }
        )

        self.assertEqual(response.status_code, 302)

        self.document.refresh_from_db()

        self.assertEqual(
            self.document.title,
            'Updated by Editor'
        )

    def test_read_permission_user_cannot_edit_document(self):
        DocumentPermission.objects.create(
            document=self.document,
            user=self.reader,
            permission='READ',
            granted_by=self.owner
        )

        self.client.login(
            username='reader',
            password='TestPassword123'
        )

        response = self.client.get(
            reverse('edit_document', args=[self.document.id])
        )

        self.assertEqual(response.status_code, 302)

        self.document.refresh_from_db()

        self.assertEqual(
            self.document.title,
            'Original Document'
        )

    def test_unauthorized_user_cannot_edit_document(self):
        self.client.login(
            username='edit_unauthorized',
            password='TestPassword123'
        )

        response = self.client.get(
            reverse('edit_document', args=[self.document.id])
        )

        self.assertEqual(response.status_code, 302)

        self.document.refresh_from_db()

        self.assertEqual(
            self.document.title,
            'Original Document'
        )

    def test_edit_creates_audit_log(self):
        from audit.models import AuditLog

        self.client.login(
            username='edit_owner',
            password='TestPassword123'
        )

        response = self.client.post(
            reverse('edit_document', args=[self.document.id]),
            {
                'title': 'Audit Test Document'
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            AuditLog.objects.filter(
                actor=self.owner,
                document=self.document,
                action='EDIT'
            ).exists()
        )

    def test_edit_permission_user_can_replace_file(self):
        DocumentPermission.objects.create(
            document=self.document,
            user=self.editor,
            permission='EDIT',
            granted_by=self.owner
        )

        self.client.login(
            username='editor',
            password='TestPassword123'
        )

        replacement_file = SimpleUploadedFile(
            'replacement.txt',
            b'Replacement document content.',
            content_type='text/plain'
        )

        response = self.client.post(
            reverse('edit_document', args=[self.document.id]),
            {
                'title': 'Replaced Document',
                'file': replacement_file
            }
        )

        self.assertEqual(response.status_code, 302)

        self.document.refresh_from_db()

        self.assertEqual(
            self.document.title,
            'Replaced Document'
        )

        with self.document.file.open('rb') as saved_file:
            saved_content = saved_file.read()

        self.assertEqual(
            saved_content,
            b'Replacement document content.'
        )
