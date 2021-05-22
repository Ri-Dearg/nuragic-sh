"""Registers models to the admin for the Products app."""
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline

from .models import Product, ShopCategory


class ProductInlineAdmin(TranslationStackedInline):
    """Inline for viewing all Products in a category in both langauges."""
    model = Product
    fields = ('category', 'title', 'description', 'price', 'delivery_cost',
              'image_4_3', 'is_unique', 'is_artisanal', 'can_preorder',
              'stock', 'date_added', 'times_purchased', 'popularity',)
    readonly_fields = ('times_purchased', 'popularity',)


class ProductAdmin(admin.ModelAdmin):
    """Displays the Products admin fields."""
    ordering = ['title']
    fields = ('category', 'title', 'description', 'price', 'delivery_cost',
              'image_4_3', 'is_unique', 'is_artisanal', 'can_preorder',
              'stock', 'date_added', 'times_purchased', 'popularity',)
    readonly_fields = ('times_purchased', 'popularity',)


class ProductTrans(ProductAdmin, TranslationAdmin):
    """Allows translation in the admin."""


class ShopCategoryAdmin(admin.ModelAdmin):
    """Displays the Products as inlines admin fields."""
    inlines = [ProductInlineAdmin]


class ShopCategoryTrans(ShopCategoryAdmin, TranslationAdmin):
    """Allows translation in the admin."""


admin.site.register(ShopCategory, ShopCategoryTrans)
admin.site.register(Product, ProductTrans)
