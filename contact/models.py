"""Models for the info module."""

from django.shortcuts import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from django.db import models

from django_better_admin_arrayfield.models.fields import ArrayField

from config import settings


class Newsletter(models.Model):
    """Model for the creation of different newsletter lists."""
    name = models.CharField(max_length=60, blank=False, null=False)
    email_list = ArrayField(models.EmailField(
        null=False, blank=False), default=list)

    def save(self, *args, **kwargs):
        email_history = EmailHistory.objects.values_list(
            'email_address', flat=True)
        history_list = list(email_history)
        history_list.sort()

        news_list = self.email_list
        news_list.sort()

        news_list_unique = [item for item in news_list
                            if item not in history_list]
        if len(news_list_unique) > 0:
            history_objs = [EmailHistory(email_address=item, newsletter=True)
                            for item in news_list_unique]
            EmailHistory.objects.bulk_create(history_objs)

        history_unique = [item for item in history_list
                          if item not in news_list]
        if len(history_unique) > 0:
            history_objs = EmailHistory.objects.filter(
                email_address__in=history_unique)
            for item in history_objs:
                item.newsletter = False
            EmailHistory.objects.bulk_update(history_objs, ['newsletter'])

        super().save(*args, **kwargs)

    class Meta:
        """Orders by alphabetical order."""
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class EmailHistory(models.Model):
    """Created a contact history detail for every email address."""
    email_address = models.EmailField(blank=False, null=False)
    newsletter = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        newsletter = Newsletter.objects.get(name='basic')
        newsletter_list = newsletter.email_list
        if self.email_address in newsletter_list:
            self.newsletter = True
        newsletter_list = sorted(newsletter_list)

        super().save(*args, **kwargs)

    class Meta:
        """Orders by alphabetical order."""
        ordering = ['email_address']
        verbose_name = 'Email Histories'

    def __str__(self):
        return f'{self.email_address}'


class Email(models.Model):
    """The model used to save emails in the DB."""
    email = models.EmailField(blank=False, null=False)
    name = models.CharField(max_length=60, blank=False, null=False)
    subject = models.CharField(max_length=254, blank=False, null=False)
    message = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    email_history = models.ForeignKey(EmailHistory,
                                      null=True,
                                      on_delete=models.SET_NULL)

    def get_absolute_url(self):
        """Returns users to the contact page on successful creation."""
        return reverse('contact:email-form')

    def save(self, *args, **kwargs):
        """Saves the email to the database and sends it to the admin."""
        email = self.email
        name = self.name
        subject = self.subject
        message = self.message

        # Fills in the email templates and then send the email.
        contact_subject = render_to_string(
            'contact/emails/contact_subject.txt',
            {'subject': subject})
        contact_body = render_to_string(
            'contact/emails/contact_body.txt',
            {'name': name, 'email': email, 'message': message})
        send_mail(contact_subject,
                  contact_body,
                  email,
                  [settings.DEFAULT_FROM_EMAIL])

        # Sends a thank you email to the person who sent the email
        thanks_subject = render_to_string(
            'contact/emails/thanks_subject.txt',
            {'subject': subject})
        thanks_body = render_to_string(
            'contact/emails/thanks_body.txt',
            {'name': name})
        send_mail(thanks_subject,
                  thanks_body,
                  settings.DEFAULT_FROM_EMAIL,
                  [email])

        history = EmailHistory.objects.get_or_create(email_address=self.email)
        self.email_history = history[0]

        super().save(*args, **kwargs)

    class Meta:
        """Orders by the most recent created by default."""
        ordering = ['-date']

    def __str__(self):
        return f'{self.email}, {self.subject}'
