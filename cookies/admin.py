"""Registers models to the admin page."""
from django.contrib import admin

from .models import CookieRecord


class CookieRecordAdmin(admin.ModelAdmin):
    """Prevents editing records in the admin. Makes fields viewable."""
    readonly_fields = ('user', 'ip_address', 'date', 'consent',
                       'cookie_policy', 'privacy_policy',
                       'current_dialogue', 'current_javascript')

    def has_delete_permission(self, request, obj=None):  # pragma: no cover
        return False


admin.site.register(CookieRecord, CookieRecordAdmin)
