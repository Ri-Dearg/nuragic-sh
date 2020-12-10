from modeltranslation.translator import register, TranslationOptions
from .models import HomeCarousel, HomeInfo, Review


@register(HomeCarousel)
class HomeCarouselTranslation(TranslationOptions):
    fields = ('name', 'description')
    required_languages = ('en', 'it',)


@register(HomeInfo)
class HomeInfoTranslation(TranslationOptions):
    fields = ('name', 'description', 'button_text')
    required_languages = ('en', 'it',)


@register(Review)
class ReviewTranslation(TranslationOptions):
    fields = ('text',)
    required_languages = ('en', 'it',)
