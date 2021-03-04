"""Tests for the Product app Models."""
import re

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from products.models import Product, ShopCategory

image = SimpleUploadedFile(
    name='default.jpg',
    content=open(
        'media/default.jpg',
         'rb').read(),
    content_type='image/jpeg')

valid_shopcategory = ShopCategory(title_en='SC1',
                                  title_it='SC1')
valid_shopcategory.save()

valid_product_1 = Product(
    category=ShopCategory.objects.filter(
        title='SC1').order_by('id').first(),
    title_en='P1',
    title_it='P1',
    description_en='description',
    description_it='description',
    price=0.5,
    image_4_3=image)

valid_product_2 = Product(
    category=ShopCategory.objects.filter(
        title='SC1').order_by('id').first(),
    title_en='P1',
    title_it='P1',
    description_en='description',
    description_it='description',
    price=0.5,
    image_4_3=image)


class TestProductsModels(TestCase):
    """Tests for Products models."""

    def setUp(self):
        valid_product_1.save()

    def test_product_str(self):
        """Tests the string method on the Product."""
        product = Product.objects.latest('date_added')
        self.assertEqual(str(product),
                         (f'{product.title}: €{product.price}'))

    def test_shopcategory_str(self):
        """Tests the string method on the ShopCategory."""
        shopcategory = ShopCategory.objects.filter(
            title='SC1').order_by('id').first()
        self.assertEqual(str(shopcategory),
                         (shopcategory.title))

    def test_product_image_processing(self):
        """Tests that an uploaded product image is resized and
        processed correctly by the view."""
        product_1 = Product.objects.latest('date_added')

        product_1.image_4_3 = image

        new_info = Product.objects.latest('date_added')
        new_info.save()

        self.assertEqual(new_info.image_4_3.height, 1260)
        self.assertEqual(new_info.image_4_3.width, 945)
        self.assertTrue(re.search('^shop/products/default.*.jpeg$',
                                  new_info.image_4_3.name))
