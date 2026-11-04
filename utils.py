from .models import AuditLog


def log_activity(
    actor,
    action,
    document=None,
    target_user=None,
    details=""
):
    AuditLog.objects.create(
        actor=actor,
        action=action,
        document=document,
        target_user=target_user,
        details=details
    )