"""Admin registry for the contact module."""

from django.contrib import admin

from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from .models import Email, Newsletter


class EmailAdmin(admin.ModelAdmin):
    """Prevents emails from being editable on the admin page."""
    readonly_fields = ('email', 'name', 'subject', 'date', 'message')


class NewsletterAdmin(admin.ModelAdmin, DynamicArrayMixin):
    """Displays the newsletter arrayfield as a list."""


admin.site.register(Email, EmailAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
