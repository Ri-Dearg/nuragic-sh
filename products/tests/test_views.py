"""Tests views for the Product app."""

from django.shortcuts import reverse
from django.test import TestCase

from policies.tests.test_models import (valid_cookie_policy,
                                        valid_privacy_policy)
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
        valid_cookie_policy.save()
        valid_privacy_policy.save()

    def test_render_shop(self):
        """Tests templates for shop page."""
        response = self.client.get(reverse('products:product-list'))
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
        response = self.client.get(
            reverse('products:product-detail',
                    kwargs={'slug': product.slug, 'pk': product.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertTemplateUsed(response, 'products/includes/product_box.html')
        self.assertTemplateUsed(
            response, 'products/includes/related_products.html')
        self.assertTemplateUsed(
            response, 'likes/includes/likes_offcanvas.html')
        self.assertTemplateUsed(
            response, 'likes/includes/likes_menu.html')
        self.assertTemplateUsed(
            response, 'cart/includes/cart_offcanvas.html')
        self.assertTemplateUsed(
            response, 'cart/includes/cart_menu.html')
        self.assertTemplateUsed(
            response, 'likes/includes/detail_like_toggle.html')
        self.assertTemplateUsed(
            response, 'cart/includes/detail_cart_toggle.html')
        self.assertTemplateUsed(
            response, 'likes/includes/box_like_toggle.html')
        self.assertTemplateUsed(
            response, 'cart/includes/box_cart_toggle.html')
        self.assertTemplateUsed(response, 'base/base.html')
        self.assertTemplateUsed(response, 'base/includes/header.html')
        self.assertTemplateUsed(response, 'base/includes/shop_nav.html')
        self.assertTemplateUsed(response, 'base/includes/footer.html')
        self.assertTrue(
            response.context['active_category'], True)
        self.assertTrue(
            response.context['related_products'], True)
        response = self.client.get(product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_render_shopcategory_detail(self):
        """Tests templates for Category detail page."""
        shopcategory = ShopCategory.objects.filter(
            title_en='SC1').order_by('id').first()
        response = self.client.get(
            reverse('products:shop-category-detail',
                    kwargs={'slug': shopcategory.slug, 'pk': shopcategory.id}))

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
                '-popularity', '-stock'))

        response = self.client.get(shopcategory.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/shopcategory_detail.html')
