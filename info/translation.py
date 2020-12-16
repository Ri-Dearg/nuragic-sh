from modeltranslation.translator import register, TranslationOptions
from .models import HomeCarousel, Category, DetailInfo, Review


@register(HomeCarousel)
class HomeCarouselTranslation(TranslationOptions):
    fields = ('name', 'description')
    required_languages = ('en', 'it',)


@register(Category)
class CategoryTranslation(TranslationOptions):
    fields = ('name', 'description', 'button_text')
    required_languages = ('en', 'it',)


@register(DetailInfo)
class DetailInfoTranslation(TranslationOptions):
    fields = ('title', 'summary', 'description1', 'description2')
    required_languages = {'default': ('title', 'summary', 'description1',)}


@ register(Review)
class ReviewTranslation(TranslationOptions):
    fields = ('text',)
    required_languages = ('en', 'it',)
