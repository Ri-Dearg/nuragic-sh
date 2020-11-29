"""Admin registry for the contact module."""

from django.contrib import admin

from .models import Email


class EmailAdmin(admin.ModelAdmin):
    """Prevents emails from being editable on the admin page."""
    readonly_fields = ('email', 'name', 'subject', 'date', 'message')


admin.site.register(Email, EmailAdmin)
