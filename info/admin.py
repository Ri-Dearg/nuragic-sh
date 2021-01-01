from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline

from .models import Category, GalleryImage, Page, Review, SplashImage


class PageInlineAdmin(TranslationStackedInline):
    model = Page


class GalleryInlineAdmin(admin.StackedInline):
    model = GalleryImage


class CategoryAdmin(admin.ModelAdmin):
    """Displays the Page arrayfield as a list."""
    inlines = [PageInlineAdmin]


class CategoryTrans(CategoryAdmin, TranslationAdmin):
    pass


class PageAdmin(admin.ModelAdmin, DynamicArrayMixin):
    """Displays the Page arrayfield as a list."""
    inlines = [GalleryInlineAdmin]


class PageTrans(PageAdmin, TranslationAdmin):
    pass


class GalleryImageAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False  # pragma: no cover


admin.site.register(SplashImage, TranslationAdmin)
admin.site.register(Category, CategoryTrans)
admin.site.register(Page, PageTrans)
admin.site.register(GalleryImage, GalleryImageAdmin)
admin.site.register(Review, TranslationAdmin)
