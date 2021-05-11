"""Defines models for the policy app."""
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.text import slugify
from tinymce.models import HTMLField


class Policy(models.Model):
    """Simple text field for creating site policies."""
    name = models.CharField(max_length=100, default='')
    content = HTMLField()
    date_created = models.DateTimeField(default=timezone.now)
    active_cookie = models.BooleanField(default=False)
    active_privacy = models.BooleanField(default=False)
    display = models.BooleanField(default=True)
    slug = models.SlugField(
        default='a', editable=False, max_length=100, null=False)

    def get_absolute_url(self):
        """Adds slug to url for page redirection."""
        kwargs = {'slug': self.slug,
                  'pk': self.id
                  }
        return reverse('policy:policy-detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        """Generates a slug for the url.
        Sets active policy settings for use with cookie records."""
        if self.active_cookie is True:
            cookie_policy = Policy.objects.filter(
                active_cookie=True).exclude(pk=self.id)
            for item in cookie_policy:
                item.active_cookie = False
                item.save()

        if self.active_privacy is True:
            privacy_policy = Policy.objects.filter(
                active_privacy=True).exclude(pk=self.id)
            for item in privacy_policy:
                item.active_privacy = False
                item.save()

        slug_value_en = self.name_en
        self.slug_en = slugify(slug_value_en, allow_unicode=True)

        slug_value_it = self.name_it
        self.slug_it = slugify(slug_value_it, allow_unicode=True)

        super().save(*args, **kwargs)

    class Meta:
        """Plural name."""
        verbose_name_plural = 'policies'

    def __str__(self):
        return f'{self.name}: {self.date_created}'
