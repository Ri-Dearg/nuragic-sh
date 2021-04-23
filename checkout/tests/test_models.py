from django.test import TestCase

from checkout.models import Order
from products.models import Product
from products.tests.test_models import valid_product_1, valid_product_2

from .test_views import valid_order_dict


class TestCheckoutModels(TestCase):
    """Tests the models for the checkout app."""

    def setUp(self):
        Product.objects.bulk_create([
            valid_product_1,
            valid_product_2])

    def test_order_and_lineitem_string(self):
        """Tests the string method for the models."""
        # Adds an item to the cart before sending an order
        product = Product.objects.filter(
            title='P1').last()
        p_id = product.id

        self.client.post('/shop/cart/ajax/toggle/',
                         {'item-id': p_id, 'quantity': '1'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.client.post('/shop/checkout/payment/', valid_order_dict)

        # Retrieves the new order
        new_order = Order.objects.latest('date')
        order_lineitem = new_order.lineitems.get(product=p_id)

        # CHecks that the string method for the order and its items is correct.
        self.assertEqual(str(new_order), new_order.order_number)
        self.assertEqual(str(order_lineitem),
                         f'{order_lineitem.product.title} on order {new_order.order_number}')  # noqa E501
