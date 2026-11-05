
from django.db import models
from django.contrib.auth.models import User


class AuditLog(models.Model):

    ACTION_CHOICES = [
        ('UPLOAD', 'Document Uploaded'),
        ('DOWNLOAD', 'Document Downloaded'),
        ('SHARE', 'Document Shared'),
        ('REVOKE', 'Access Revoked'),
        ('EDIT', 'Document Edited'),
    ]

    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_actions'
    )

    document = models.ForeignKey(
        'documents.Document',
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs'
    )

    target_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='received_audit_actions'
    )

    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES
    )

    details = models.TextField(blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.actor} - {self.timestamp}"
