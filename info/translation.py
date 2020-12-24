from modeltranslation.translator import TranslationOptions, register

from .models import Category, DetailInfo, HomeCarousel, Review


@register(HomeCarousel)
class HomeCarouselTranslation(TranslationOptions):
    fields = ('name', 'description')
    required_languages = ('en', 'it',)


@register(Category)
class CategoryTranslation(TranslationOptions):
    fields = ('title', 'menu_word', 'description', 'button_text')
    required_languages = ('en', 'it',)


@register(DetailInfo)
class DetailInfoTranslation(TranslationOptions):
    fields = ('title', 'summary', 'desc_title1',
              'description1', 'desc_title2', 'description2')
    required_languages = {'default': (
        'title', 'summary', 'desc_title1', 'description1',)}


@ register(Review)
class ReviewTranslation(TranslationOptions):
    fields = ('text',)
    required_languages = ('en', 'it',)
