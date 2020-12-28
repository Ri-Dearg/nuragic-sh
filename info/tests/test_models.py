import re

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from info.models import Category, GalleryImage, HomeCarousel, Page, Review


class InfoTests(TestCase):
    """Tests for Product models."""

    def setUp(self):
        """Sets up a HomeCarousel model."""
        image = SimpleUploadedFile(
            name='default.jpg',
            content=open(
                'media/default.jpg',
                 'rb').read(),
            content_type='image/jpeg',)
        valid_carousel = HomeCarousel(name_en='HC1',
                                      name_it='HC1',
                                      description_en='description',
                                      description_it='description',
                                      image=image)
        valid_carousel.save()

        valid_category = Category(title_en='HI1',
                                  title_it='HI1',
                                  menu_word_en='HCMW1',
                                  menu_word_it='HCMW1',
                                  description_en='description',
                                  description_it='description',
                                  image=image,
                                  button_text="text here",
                                  order=1)
        valid_category.save()

        valid_page = Page(
            category=Category.objects.latest('date_added'),
            title_en='HI1',
            title_it='HI1',
            summary_en='HCMW1',
            summary_it='HCMW1',
            desc_title1_en='heading',
            desc_title1_it='heading',
            description1_en='description',
            description1_it='description',
            title_image=image,
            desc_image=image,
            theme='brown',
            order=1)
        valid_page.save()

        valid_review = Review(reviewer_name='abacus',
                              text='this is a review')

        valid_review.save()

    def test_carousel_image_file_is_processed_correctly(self):
        """Tests that an uploaded HomeCarousel image is resized and
        processed correctly by the view."""

        # Retrieves the latest HomeCarousel and saves an image to it.
        hc1 = HomeCarousel.objects.latest('date_added')
        hc1.image = SimpleUploadedFile(
            name='default.jpg',
            content=open('media/default.jpg', 'rb').read(),
            content_type='image/jpeg')
        new_info = HomeCarousel.objects.latest('date_added')
        new_info.save()

        # Checks that the image has been modified and named correctly
        # after being saved.
        self.assertEqual(new_info.image.height, 720)
        self.assertEqual(new_info.image.width, 1920)
        self.assertTrue(re.search('^carousel/default.*.jpeg$',
                                  new_info.image.name))

    def test_carousel_str(self):
        """Tests the string method on the HomeCarousel."""
        hc1 = HomeCarousel.objects.latest('date_added')
        self.assertEqual(str(hc1),
                         (f'{hc1.name}'))

    def test_category_image_file_is_processed_correctly(self):
        """Tests that an uploaded Category image is resized and
        processed correctly by the view."""

        # Retrieves the latest Category and saves an image to it.
        hi1 = Category.objects.latest('date_added')
        hi1.image = SimpleUploadedFile(
            name='default.jpg',
            content=open('media/default.jpg', 'rb').read(),
            content_type='image/jpeg')
        new_info = Category.objects.latest('date_added')
        new_info.save()

        # Checks that the image has been modified and named correctly
        # after being saved.
        self.assertEqual(new_info.image.height, 628)
        self.assertEqual(new_info.image.width, 1200)
        self.assertTrue(re.search('^info/category/default.*.jpeg$',
                                  new_info.image.name))

    def test_category_str(self):
        """Tests the string method on the Category."""
        hi1 = Category.objects.latest('date_added')
        self.assertEqual(str(hi1),
                         (f'{hi1.menu_word}'))

    def test_page_image_processing(self):
        d1 = Page.objects.latest('date_added')

        image = SimpleUploadedFile(
            name='default.jpg',
            content=open(
                'media/default.jpg',
                 'rb').read(),
            content_type='image/jpeg',)

        d1.desc_image = image
        d1.bot_image = image
        d1.save()
        self.assertEqual(str(d1),
                         (f'{d1.title}'))

    def test_galleryimage_str(self):
        """Tests the string method on the GalleryImage."""
        d1 = Page.objects.latest('date_added')

        image = SimpleUploadedFile(
            name='default.jpg',
            content=open(
                'media/default.jpg',
                 'rb').read(),
            content_type='image/jpeg',)

        g1 = GalleryImage(page=d1, image=image)
        self.assertEqual(str(g1),
                         (f'{g1.page}, {g1.image}'))

    def test_review_str(self):
        """Tests the string method on the Review."""
        r1 = Review.objects.latest('date_added')
        self.assertEqual(str(r1),
                         (f'{r1.reviewer_name}'))
