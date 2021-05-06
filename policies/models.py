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
        """Generates a slug for the url."""
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
