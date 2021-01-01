"""Admin registry for the Contact module."""
from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from .models import Email, EmailHistory, Newsletter


class EmailInline(admin.StackedInline):
    """Inline for viewing all emails sent in the EmailHistory model."""
    model = Email
    readonly_fields = ('email', 'name', 'subject', 'date', 'message',
                       'email_history')


class EmailHistoryAdmin(admin.ModelAdmin):
    """Prevents editing emails in the admin. Makes Emails viewable."""
    readonly_fields = ('email_address', 'newsletter_en', 'newsletter_it')
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
