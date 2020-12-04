"""Admin registry for the contact module."""

from django.contrib import admin

from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from .models import Email, Newsletter, EmailHistory


class EmailInline(admin.StackedInline):
    model = Email
    readonly_fields = ('email', 'name', 'subject', 'date', 'message',
                       'email_history')


class EmailHistoryAdmin(admin.ModelAdmin):
    """Prevents emails from being editable on the admin page."""
    readonly_fields = ('email_address', 'newsletter')
    inlines = [EmailInline]


class EmailAdmin(admin.ModelAdmin):
    """Prevents emails from being editable on the admin page."""
    readonly_fields = ('email', 'name', 'subject', 'date', 'message',
                       'email_history')


class NewsletterAdmin(admin.ModelAdmin, DynamicArrayMixin):
    """Displays the newsletter arrayfield as a list."""


admin.site.register(Email, EmailAdmin)
admin.site.register(EmailHistory, EmailHistoryAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
