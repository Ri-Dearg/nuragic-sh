"""Tests views for the Product app."""

from django.test import TestCase

from products.models import Product, ShopCategory
from products.tests.test_models import (valid_product_1, valid_product_2,
                                        valid_shopcategory)


class TestProductsViews(TestCase):
    """Tests for Products app views."""

    def setUp(self):
        """Sets up a model instances for tests."""
        valid_shopcategory.save()
        valid_product_1.save()
        valid_product_2.save()

    def test_render_shop(self):
        """Tests templates for shop page."""
        response = self.client.get('/shop/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_list.html')
        self.assertTemplateUsed(response, 'products/includes/product_box.html')
        self.assertTemplateUsed(response, 'base/base.html')
        self.assertTemplateUsed(response, 'base/includes/header.html')
        self.assertTemplateUsed(response, 'base/includes/shop_nav.html')
        self.assertTemplateUsed(response, 'base/includes/footer.html')
        self.assertTrue(
            response.context['all_products_active'], True)

    def test_render_product_detail(self):
        """Tests templates for shop page."""
        product = Product.objects.latest('date_added')
        response = self.client.get(f'/shop/product/{product.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertTemplateUsed(response, 'products/includes/product_box.html')
        self.assertTemplateUsed(
            response, 'products/includes/related_products.html')
        self.assertTemplateUsed(response, 'likes/includes/likes_dropdown.html')
        self.assertTemplateUsed(
            response, 'likes/includes/detail_like_toggle.html')
        self.assertTemplateUsed(
            response, 'likes/includes/box_like_toggle.html')
        self.assertTemplateUsed(response, 'base/base.html')
        self.assertTemplateUsed(response, 'base/includes/header.html')
        self.assertTemplateUsed(response, 'base/includes/shop_nav.html')
        self.assertTemplateUsed(response, 'base/includes/footer.html')
        self.assertTrue(
            response.context['active_category'], True)
        self.assertTrue(
            response.context['related_products'], True)

    def test_render_shopcategory_detail(self):
        """Tests templates for Category detail page."""
        shopcategory = ShopCategory.objects.filter(
            title='SC1').order_by('id').first()
        response = self.client.get(f'/shop/category/{shopcategory.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/shopcategory_detail.html')
        self.assertTemplateUsed(response, 'products/includes/product_box.html')
        self.assertTemplateUsed(response, 'base/base.html')
        self.assertTemplateUsed(response, 'base/includes/header.html')
        self.assertTemplateUsed(response, 'base/includes/shop_nav.html')
        self.assertTemplateUsed(response, 'base/includes/footer.html')
        self.assertTrue(
            response.context['active_category'], f'{shopcategory.id}')
        self.assertTrue(
            response.context['page_obj'], shopcategory.products.all().order_by(
                '-stock', '-popularity'))
