from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        'action',
        'actor',
        'document',
        'target_user',
        'timestamp'
    )

    list_filter = ('action', 'timestamp')

    search_fields = (
        'actor__username',
        'document__title',
        'target_user__username'
    )

    readonly_fields = (
        'actor',
        'document',
        'target_user',
        'action',
        'details',
        'timestamp'
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False