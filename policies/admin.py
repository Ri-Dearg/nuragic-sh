"""Registers models to the admin page."""
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Policy

admin.site.register(Policy, TranslationAdmin)
