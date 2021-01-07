from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Product, ShopCategory

admin.site.register(ShopCategory, TranslationAdmin)
admin.site.register(Product, TranslationAdmin)
