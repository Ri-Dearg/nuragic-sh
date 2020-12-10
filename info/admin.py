from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from .models import HomeCarousel, HomeInfo, Review


admin.site.register(HomeCarousel, TranslationAdmin)
admin.site.register(HomeInfo, TranslationAdmin)
admin.site.register(Review, TranslationAdmin)
