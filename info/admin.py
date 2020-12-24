from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from modeltranslation.admin import TranslationAdmin

from .models import Category, DetailInfo, GalleryImage, HomeCarousel, Review


class DetailInfoInlineAdmin(admin.StackedInline):
    model = DetailInfo


class GalleryInlineAdmin(admin.StackedInline):
    model = GalleryImage


class CategoryAdmin(admin.ModelAdmin):
    """Displays the detailinfo arrayfield as a list."""
    inlines = [DetailInfoInlineAdmin]


class CategoryTrans(CategoryAdmin, TranslationAdmin):
    pass


class DetailInfoAdmin(admin.ModelAdmin, DynamicArrayMixin):
    """Displays the detailinfo arrayfield as a list."""
    inlines = [GalleryInlineAdmin]


class DetailInfoTrans(DetailInfoAdmin, TranslationAdmin):
    pass


class GalleryImageAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False  # pragma: no cover


admin.site.register(HomeCarousel, TranslationAdmin)
admin.site.register(Category, CategoryTrans)
admin.site.register(DetailInfo, DetailInfoTrans)
admin.site.register(GalleryImage, GalleryImageAdmin)
admin.site.register(Review, TranslationAdmin)
