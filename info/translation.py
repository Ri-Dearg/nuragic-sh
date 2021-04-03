"""Fields to be translated by django-modeltranslation."""
from modeltranslation.translator import TranslationOptions, register

from .models import Category, Page, Review, SplashImage


@register(SplashImage)
class SplashImageTranslation(TranslationOptions):
    """Fields that need translation options."""
    fields = ('title', 'description')
    required_languages = ('en', 'it',)


@register(Category)
class CategoryTranslation(TranslationOptions):
    """Fields that need translation options."""
    fields = ('title', 'menu_word', 'description', 'button_text')
    required_languages = ('en', 'it',)


@register(Page)
class PageTranslation(TranslationOptions):
    """Fields that need translation options."""
    fields = ('title', 'summary', 'button_text', 'product_button_text',
              'desc_title1', 'description1', 'desc_title2', 'description2')
    required_languages = {'default': (
        'title', 'summary', 'button_text', 'desc_title1', 'description1',)}


@ register(Review)
class ReviewTranslation(TranslationOptions):
    """Fields that need translation options."""
    fields = ('text',)
    required_languages = ('en', 'it',)
