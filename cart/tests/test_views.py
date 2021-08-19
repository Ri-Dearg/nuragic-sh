"""Tests for Cart app."""
from django.shortcuts import reverse
from django.test import TestCase

from policies.tests.test_models import make_policies
from products.models import Product
from products.tests.test_models import make_products


class TestViews(TestCase):
    """Tests views for the Cart app."""

    def setUp(self):
        make_products()
        make_policies()

    def test_error_on_incorrect_item_removed(self):
        """Checks that an error occurs in the toggle when an
        item isn't in the cart"""

        product = Product.objects.filter(
            title='P1').last()
        p_id = product.id

        # This adds the item
        self.client.post(reverse('cart:cart-toggle'),
                         {'item-id': p_id, 'quantity': '1'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        session = self.client.session

        # confirms the item is in the cart
        self.assertEqual(session['cart'], {f'{p_id}': 1})

        # Uses the toggle on a non-existant item
        self.client.post(reverse('cart:cart-toggle'),
                         {'item-id': 0, 'quantity': '0'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # confirms the error message
        self.assertRaises(Exception, msg='Error removing item: 0')

        session['cart'] = {f'{p_id}': 1, '0': 1}
        session.save()

        self.client.post(reverse('cart:cart-toggle'),
                         {'item-id': p_id, 'quantity': '1'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        session = self.client.session
        self.assertEqual(session['cart'], {})

        # Adds an item with no stock and confirms an error.
        no_stock_product = Product.objects.filter(
            title='P1').last()
        no_stock_product.stock = 0
        no_stock_product.save()
        nsp_id = no_stock_product.id

        session['cart'] = {f'{nsp_id}': 1}

        self.client.post(reverse('cart:cart-toggle'),
                         {'item-id': p_id, 'quantity': '1'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(session['cart'], {f'{p_id}': 1})

    def test_correct_template_used(self):
        """Checks that the url produces the correct template."""
        response = self.client.get(reverse('cart:cart-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart_list.html')

    def test_correct_quantity_for_unique_products(self):
        """Test unique product stock remains at 1
        even when a greater quantity is added."""
        product_is_unique = Product.objects.filter(
            title='unique').last()

        up_id = product_is_unique.id

        self.client.post(reverse('cart:cart-toggle'),
                         {'item-id': up_id, 'quantity': '10'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        session = self.client.session
        self.assertEqual(session['cart'], {f'{up_id}': 1})

    def test_ability_to_preorder(self):
        """Tests ability to preorder items when stock is at 0."""
        product_preorder = Product.objects.filter(
            title='preorder').last()

        pp_id = product_preorder.id

        self.client.post(reverse('cart:cart-toggle'),
                         {'item-id': pp_id, 'quantity': '10'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        session = self.client.session
        self.assertEqual(session['cart'], {f'{pp_id}': 10})

    def test_confirm_add_to_cart_functions(self):
        """Tests add to cart functions, such as limiting stock,
        multiple items, updating quantities."""

        # Gets a product and sets a stock limit
        not_unique_product = Product.objects.filter(
            title='P1').first()
        not_unique_product.is_unique = False
        not_unique_product.stock = 3
        not_unique_product.save()
        nup_id = not_unique_product.id

        limit_stock_product = Product.objects.filter(
            title='P1').last()
        limit_stock_product.stock = 5
        limit_stock_product.save()
        lsp_id = limit_stock_product.id

        response = self.client.get(reverse('cart:cart-toggle'),
                                   {'item-id': lsp_id, 'quantity': '1'},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)

        # Adds a normal quantity, then adds a quantity higher than the stock
        self.client.post(reverse('cart:cart-toggle'),
                         {'item-id': lsp_id, 'quantity': '1'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.client.post(reverse('cart:cart-toggle'),
                         {'item-id': lsp_id, 'quantity': '0'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.client.post(reverse('cart:cart-toggle'),
                         {'item-id': lsp_id, 'quantity': '0'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.client.post(reverse('cart:cart-toggle'),
                         {'item-id': lsp_id, 'quantity': '1'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.client.post(reverse('cart:cart-toggle'),
                         {'item-id': nup_id, 'quantity': '4'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Updates the product when adding to cart
        self.client.post(reverse('cart:cart-toggle'),
                         {'item-id': lsp_id,
                          'quantity': '10',
                          'special': 'update'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Confirms the quantity in cart is max stock.
        session = self.client.session
        self.assertEqual(session['cart'], {f'{lsp_id}': 5, f'{nup_id}': 3})

    def test_error_on_incorrect_item_added(self):
        """Adds an invalid item to the cart and confirms that an error is
        raised."""

        # Adds a non-existent item and confirms an error
        self.client.post(reverse('cart:cart-toggle'),
                         {'item-id': 0, 'quantity': '0'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertRaises(Exception, msg='Error adding item: 0')

        # Adds an item with no stock and confirms an error.
        no_stock_product = Product.objects.filter(
            title='P1').last()
        no_stock_product.stock = 0
        no_stock_product.save()
        nsp_id = no_stock_product.id

        self.client.post(reverse('cart:cart-toggle'),
                         {'item-id': nsp_id, 'quantity': '1'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        session = self.client.session
        self.client.get('/')
        self.assertEqual(session['cart'], {})

        self.assertRaises(Exception, msg='Error adding item: 0')

    def test_successfully_remove_from_cart(self):
        """Tests that the ajax toggle first adds an item and
        then removes the item from the cart."""

        product = Product.objects.filter(
            title='P1').last()
        p_id = product.id

        # This adds the item
        self.client.post(reverse('cart:cart-toggle'),
                         {'item-id': p_id, 'quantity': '1'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        session = self.client.session

        # confirms the item is in the cart
        self.assertEqual(session['cart'], {f'{p_id}': 1})

        # This removes the item
        self.client.post(reverse('cart:cart-toggle'),
                         {'item-id': p_id, 'quantity': '1'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        session = self.client.session

        # Confirms the cart is now empty
        self.assertEqual(session['cart'], {})

    def test_update_cart_view(self):
        """Tests numerous functions relating to updating the cart update view,
        mainly to ensure that the context information is correct."""

        # Tests the template is updated when the view is called
        response = self.client.get('/shop/cart/update_offcanvas/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('cart/includes/cart_offcanvas.html')
