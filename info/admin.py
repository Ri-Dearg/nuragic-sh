from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from modeltranslation.admin import TranslationAdmin

from .models import Category, DetailInfo, GalleryImage, HomeCarousel, Review


class GalleryInlineAdmin(admin.StackedInline):
    model = GalleryImage


class DetailInfoAdmin(admin.ModelAdmin, DynamicArrayMixin):
    """Displays the detailinfo arrayfield as a list."""
    inlines = [GalleryInlineAdmin]


class DetailInfoTrans(DetailInfoAdmin, TranslationAdmin):
    pass


class GalleryImageAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False  # pragma: no cover


admin.site.register(HomeCarousel, TranslationAdmin)
admin.site.register(Category, TranslationAdmin)
admin.site.register(DetailInfo, DetailInfoTrans)
admin.site.register(GalleryImage, GalleryImageAdmin)
admin.site.register(Review, TranslationAdmin)
