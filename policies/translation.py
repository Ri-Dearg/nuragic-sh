"""Fields to be translated by django-modeltranslation."""
from modeltranslation.translator import TranslationOptions, register

from .models import Policy


@register(Policy)
class PolicyTranslation(TranslationOptions):
    """Fields that need translation options."""
    fields = ('name', 'content', 'slug',)
    required_languages = ('en', 'it',)
