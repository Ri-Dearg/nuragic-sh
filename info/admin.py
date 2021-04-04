"""Admin registry for the Info module."""
from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline

from .models import Category, Page, Review, SplashImage


class PageInlineAdmin(TranslationStackedInline):
    """Inline for viewing all Pages in a category in both langauges."""
    model = Page
    fields = ('category', 'product', 'product_button_text', 'title',
              'summary', 'button_text', 'desc_title1', 'description1',
              'desc_title2', 'description2', 'title_image_tw_header',
              'image_fb_link', 'bot_image_tw_header', 'order', 'theme',
              'date_added')


class CategoryAdmin(admin.ModelAdmin):
    """Displays the Page arrayfield as a list."""
    inlines = [PageInlineAdmin]
    fields = ('title', 'menu_word', 'description', 'button_text',
              'image_fb_link', 'display', 'date_added')


class CategoryTrans(CategoryAdmin, TranslationAdmin):
    """Allows translation in the admin."""


class PageAdmin(admin.ModelAdmin, DynamicArrayMixin):
    """Displays the Page arrayfield as a list."""
    ordering = ['category']
    fields = ('category', 'product', 'product_button_text', 'title',
              'summary', 'button_text', 'desc_title1', 'description1',
              'desc_title2', 'description2', 'title_image_tw_header',
              'image_fb_link', 'bot_image_tw_header', 'order', 'theme',
              'date_added')


class PageTrans(PageAdmin, TranslationAdmin):
    """Allows translation in the admin."""


class SplashImageAdmin(admin.ModelAdmin):
    """Displays order based on its associated Page."""
    ordering = ['page', 'product']
    fields = ('page', 'product', 'title', 'description', 'image_tw_header',
              'image_fb_link', 'info_display', 'shop_display', 'date_added')


class SplashImageTrans(SplashImageAdmin, TranslationAdmin):
    """Allows translation in the admin."""


admin.site.register(SplashImage, SplashImageTrans)
admin.site.register(Category, CategoryTrans)
admin.site.register(Page, PageTrans)
admin.site.register(Review, TranslationAdmin)
