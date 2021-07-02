"""Tests for the Info app Models."""
import re

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from info.models import Category, Page, Review, SplashImage
from products.models import Product
from products.tests.test_models import make_products

image = SimpleUploadedFile(
    name='default.jpg',
    content=open(
        'media/default.jpg',
         'rb').read(),
    content_type='image/jpeg',)


def make_info_models():
    """Makes a category and a pages for testing."""
    Category.objects.create(title_en='HI1',
                            title_it='HI1',
                            menu_word_en='HCMW1',
                            menu_word_it='HCMW1',
                            description_en='description',
                            description_it='description',
                            image_fb_link=image,
                            image_fb_link_md=image,
                            image_fb_link_sm=image,
                            button_text="text here",
                            display=False,
                            order=12)

    Category.objects.create(title_en='about',
                            title_it='HI1',
                            menu_word_en='HCMW1',
                            menu_word_it='HCMW1',
                            description_en='description',
                            description_it='description',
                            image_fb_link=image,
                            image_fb_link_md=image,
                            image_fb_link_sm=image,
                            button_text="text here",
                            order=2)

    Page.objects.create(category=Category.objects.latest('date_added'),
                        title_en='HI1',
                        title_it='HI1',
                        summary_en='HCMW1',
                        summary_it='HCMW1',
                        desc_title1_en='heading',
                        desc_title1_it='heading',
                        description1_en='description',
                        description1_it='description',
                        title_image_tw_header=image,
                        title_image_tw_header_md=image,
                        title_image_tw_header_sm=image,
                        image_fb_link=image,
                        image_fb_link_md=image,
                        image_fb_link_sm=image,
                        theme='brown',
                        order=1)

    SplashImage.objects.create(page=Page.objects.latest('date_added'),
                               title_en='splash1',
                               title_it='splash1',
                               description_en='description',
                               description_it='description',
                               image_tw_header=image,
                               image_tw_header_md=image,
                               image_tw_header_sm=image,
                               image_fb_link=image,
                               image_fb_link_md=image,
                               image_fb_link_sm=image)

    Review.objects.create(reviewer_name='abacus',
                          text='this is a review')


class TestInfoModels(TestCase):
    """Tests for Info models."""

    def setUp(self):
        """Created instances for use in tests"""
        make_info_models()

    def test_carousel_image_file_is_processed_correctly(self):
        """Tests that an uploaded SplashImage image is resized and
        processed correctly by the view."""

        # Retrieves the latest SplashImage and saves an image to it.
        splash1 = SplashImage.objects.latest('date_added')
        splash1.image_image_tw_header = SimpleUploadedFile(
            name='default.jpg',
            content=open('media/default.jpg', 'rb').read(),
            content_type='image/jpeg')
        splash1.image_fb_link = SimpleUploadedFile(
            name='default.jpg',
            content=open('media/default.jpg', 'rb').read(),
            content_type='image/jpeg')
        new_info = SplashImage.objects.latest('date_added')
        new_info.save()

        # Checks that the image has been modified and named correctly
        # after being saved.
        self.assertEqual(new_info.image_tw_header.height, 420)
        self.assertEqual(new_info.image_tw_header.width, 1260)
        self.assertEqual(new_info.image_fb_link.height, 630)
        self.assertEqual(new_info.image_fb_link.width, 1200)
        self.assertTrue(re.search('^info/carousel/default.*.jpeg$',
                                  new_info.image_tw_header.name))
        self.assertTrue(re.search('^info/carousel/default.*.jpeg$',
                                  new_info.image_fb_link.name))

    def test_carousel_str(self):
        """Tests the string method on the SplashImage."""
        make_products()
        valid_splash_2 = SplashImage(
            product=Product.objects.latest('date_added'),
            title_en='splash1',
            title_it='splash1',
            description_en='description',
            description_it='description',
            image_tw_header=image,
            image_tw_header_md=image,
            image_tw_header_sm=image,
            image_fb_link=image,
            image_fb_link_md=image,
            image_fb_link_sm=image)
        valid_splash_2.save()

        splash2 = SplashImage.objects.earliest('date_added')
        splash1 = SplashImage.objects.latest('date_added')
        self.assertEqual(str(splash1),
                         (f'{splash1.product}: {splash1.title}'))
        self.assertEqual(str(splash2),
                         (f'{splash2.page}: {splash2.title}'))

    def test_category_image_file_is_processed_correctly(self):
        """Tests that an uploaded Category image is resized and
        processed correctly by the view."""

        # Retrieves the latest Category and saves an image to it.
        new_info = Category.objects.latest('date_added')
        new_info.image_fb_link = image
        new_info.save()

        # Checks that the image has been modified and named correctly
        # after being saved.
        self.assertEqual(new_info.image_fb_link.height, 630)
        self.assertEqual(new_info.image_fb_link.width, 1200)
        self.assertTrue(re.search('^info/category/default.*.jpeg$',
                                  new_info.image_fb_link.name))

    def test_category_str(self):
        """Tests the string method on the Category."""
        hi1 = Category.objects.latest('date_added')
        self.assertEqual(str(hi1),
                         (f'{hi1.menu_word}'))

    def test_page_image_processing(self):
        """Tests that an uploaded Page image is resized and
        processed correctly by the view. Tests str."""
        page_1 = Page.objects.latest('date_added')

        page_1.image_fb_link = image
        page_1.bot_image_tw_header = image
        page_1.save()
        self.assertEqual(str(page_1),
                         (f'{page_1.category}: {page_1.title}'))

    def test_review_str(self):
        """Tests the string method on the Review."""
        review_1 = Review.objects.latest('date_added')
        self.assertEqual(str(review_1),
                         (f'{review_1.reviewer_name}'))
