"""Fields to be translated by django-modeltranslation."""
from modeltranslation.translator import TranslationOptions, register

from .models import Product, ShopCategory


@register(ShopCategory)
class ShopCategoryTranslation(TranslationOptions):
    fields = ('title',)
    required_languages = ('en', 'it',)


@register(Product)
class ProductTranslation(TranslationOptions):
    fields = ('title', 'description',)
    required_languages = ('en', 'it',)
