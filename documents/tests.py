
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Document, DocumentPermission


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
