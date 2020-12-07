from modeltranslation.translator import register, TranslationOptions
from .models import HomeCarousel


@register(HomeCarousel)
class HomeCarouselTranslation(TranslationOptions):
    fields = ('name', 'description')
    required_languages = ('en', 'it',)
