"""Tests views for the Product app."""

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from products.models import Product, ShopCategory


class TestProductsViews(TestCase):
    """Tests for Products app views."""

    def setUp(self):
        """Sets up a model instances for tests."""
        image = SimpleUploadedFile(
            name='default.jpg',
            content=open(
                'media/default.jpg',
                'rb').read(),
            content_type='image/jpeg',)

        valid_shopcategory = ShopCategory(title_en='SC1',
                                          title_it='SC1',)
        valid_shopcategory.save()

        valid_product = Product(
            category=ShopCategory.objects.get(title='SC1'),
            title_en='P1',
            title_it='P1',
            description_en='description',
            description_it='description',
            price=0.5,
            image_4_3=image,)
        valid_product.save()

    def test_render_shop(self):
        """Tests templates for shop page."""
        response = self.client.get('/shop/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_list.html')
        self.assertTemplateUsed(response, 'products/includes/product_box.html')
        self.assertTemplateUsed(response, 'base/base.html')
        self.assertTemplateUsed(response, 'base/includes/header_shop.html')
        self.assertTemplateUsed(response, 'base/includes/footer.html')
        self.assertTrue(
            response.context['all_products_active'], True)

    def test_render_shopcategory_detail(self):
        """Tests templates for Category detail page."""
        shopcategory = ShopCategory.objects.get(title='SC1')
        response = self.client.get(f'/shop/category/{shopcategory.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/shopcategory_detail.html')
        self.assertTemplateUsed(response, 'products/includes/product_box.html')
        self.assertTemplateUsed(response, 'base/base.html')
        self.assertTemplateUsed(response, 'base/includes/header_shop.html')
        self.assertTemplateUsed(response, 'base/includes/footer.html')
        self.assertTrue(
            response.context['active_category'], f'{shopcategory.id}')
        self.assertTrue(
            response.context['page_obj'], shopcategory.products.all().order_by(
                '-stock', '-popularity'))
