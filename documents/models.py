from django.db import models
from django.contrib.auth.models import User
from .storage import PrivateDocumentStorage
import uuid
import os


def secure_upload_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return f"private_documents/{uuid.uuid4()}{extension}"


class Document(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="documents"
    )
    title = models.CharField(max_length=255)
    file = models.FileField(
    upload_to=secure_upload_path,
    storage=PrivateDocumentStorage()
)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class DocumentPermission(models.Model):

    PERMISSION_CHOICES = [
        ('READ', 'Read'),
        ('EDIT', 'Edit'),
    ]

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='permissions'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='document_permissions'
    )

    permission = models.CharField(
        max_length=10,
        choices=PERMISSION_CHOICES,
        default='READ'
    )

    granted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='granted_permissions'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['document', 'user'],
                name='unique_document_user_permission'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.document.title} - {self.permission}"
