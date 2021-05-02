"""Tets that likes are correctly added to the context."""
from django.shortcuts import reverse
from django.test import TestCase

from products.models import Product
from products.tests.test_models import valid_product_1, valid_product_2
from users.tests.test_views import test_user


class TestContext(TestCase):
    """Tests the context processor orders likes correctly in the template."""

    def setUp(self):
        """Creates a user and adds likes to their account."""
        valid_product_1.save()
        valid_product_2.save()
        product_1 = Product.objects.earliest('date_added')
        product_2 = Product.objects.latest('date_added')

        test_user.userprofile.liked_products.add(*[product_1.id, product_2.id])

    def test_likes_list_creation(self):
        """Creates a list in the same manner as the context processor
        and checks that it is equal to the context."""

        # Logs in the user from the setup view
        self.client.force_login(test_user)
        response = self.client.get(reverse('info:home'))

        # Creates a fake list based on the user's likes and
        # orders it like the context does
        test_list = []
        for product in test_user.userprofile.liked_products.all().order_by(
                '-liked__datetime_added'):
            test_list.append(product)

        # Confirms the context and the test list display the same.
        self.assertEqual(response.context['likes'],
                         test_list)
        self.assertTrue(len(test_user.userprofile.liked_products.all()) == 2)
