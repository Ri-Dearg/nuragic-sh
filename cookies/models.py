"""Model to register cookie consent records."""
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.storage import staticfiles_storage
from django.db import models
from django.template.loader import render_to_string

from policies.models import Policy


class CookieRecord(models.Model):
    """Records data about cookie consent with related documents."""
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.SET_NULL,
                             related_name='cookierecord',
                             blank=True,
                             null=True,
                             editable=False)
    ip_address = models.CharField(max_length=120,
                                  default='',
                                  blank=False,
                                  editable=False)
    date = models.DateTimeField(auto_now_add=True,
                                editable=False)
    consent = models.BooleanField(blank=False,
                                  editable=False)
    cookie_policy = models.ForeignKey(Policy,
                                      on_delete=models.CASCADE,
                                      related_name='cookie_policy',
                                      blank=False,
                                      editable=False)
    privacy_policy = models.ForeignKey(Policy,
                                       on_delete=models.CASCADE,
                                       related_name='privacy_policy',
                                       blank=False,
                                       editable=False)
    current_dialogue = models.TextField(default='',
                                        blank=False,
                                        editable=False)
    current_javascript = models.TextField(default='',
                                          blank=False,
                                          editable=False)

    def save(self, *args, **kwargs):
        """Selects current documents and saves them to the record."""
        self.cookie_policy = Policy.objects.get(active_cookie=True)
        self.privacy_policy = Policy.objects.get(active_privacy=True)
        self.current_dialogue = render_to_string(
            'cookies/includes/cookie_dialogue.html')

        with staticfiles_storage.open('js/custom/cookie.js', 'r') as js_file:
            self.current_javascript = js_file.read()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.ip_address}, {self.date}, {self.consent}'
