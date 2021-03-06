"""Fields to be translated by django-modeltranslation."""
from modeltranslation.translator import TranslationOptions, register

from .models import Product, ShopCategory


@register(ShopCategory)
class ShopCategoryTranslation(TranslationOptions):
    """Fields that need translation options."""

    fields = ('title', 'slug',)
    required_languages = ('en', 'it',)


@register(Product)
class ProductTranslation(TranslationOptions):
    """Fields that need translation options."""

    fields = ('title', 'description', 'slug',)
    required_languages = ('en', 'it',)
