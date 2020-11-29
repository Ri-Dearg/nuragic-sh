import re

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from info.models import HomeCarousel, HomeInfo, Review


class ProductTests(TestCase):
    """Tests for Product models."""

    def setUp(self):
        """Sets up a HomeCarousel model."""
        valid_carousel = HomeCarousel(name='HC1',
                                      description='description',
                                      image=SimpleUploadedFile(
                                          name='default.jpg',
                                          content=open(
                                           'media/default.jpg', 'rb').read(),
                                          content_type='image/jpeg',))
        valid_carousel.save()

        valid_info = HomeInfo(name='HI1',
                              description='description',
                              image=SimpleUploadedFile(
                                  name='default.jpg',
                                  content=open(
                                      'media/default.jpg', 'rb').read(),
                                  content_type='image/jpeg',),
                              button_text="text here",
                              order=1)
        valid_info.save()

        valid_review = Review(language='en_US',
                              reviewer_name='abacus',
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

    def test_info_image_file_is_processed_correctly(self):
        """Tests that an uploaded HomeInfo image is resized and
        processed correctly by the view."""

        # Retrieves the latest HomeInfo and saves an image to it.
        hi1 = HomeInfo.objects.latest('date_added')
        hi1.image = SimpleUploadedFile(
            name='default.jpg',
            content=open('media/default.jpg', 'rb').read(),
            content_type='image/jpeg')
        new_info = HomeInfo.objects.latest('date_added')
        new_info.save()

        # Checks that the image has been modified and named correctly
        # after being saved.
        self.assertEqual(new_info.image.height, 800)
        self.assertEqual(new_info.image.width, 1280)
        self.assertTrue(re.search('^info/default.*.jpeg$',
                                  new_info.image.name))

    def test_info_str(self):
        """Tests the string method on the HomeInfo."""
        hi1 = HomeInfo.objects.latest('date_added')
        self.assertEqual(str(hi1),
                         (f'{hi1.name}'))

    def test_review_str(self):
        """Tests the string method on the Review."""
        r1 = Review.objects.latest('date_added')
        self.assertEqual(str(r1),
                         (f'{r1.reviewer_name}'))
