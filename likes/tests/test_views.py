"""Tests views for the like module."""
from django.shortcuts import reverse
from django.test import TestCase

from policies.tests.test_models import (valid_cookie_policy,
                                        valid_privacy_policy)
from products.models import Product
from products.tests.test_models import valid_product_1, valid_product_2
from users.tests.test_views import test_user


class TestLikesViews(TestCase):
    """Tests views for the Likes app."""

    def setUp(self):
        valid_product_1.save()
        valid_product_2.save()
        valid_cookie_policy.save()
        valid_privacy_policy.save()

    def test_correct_template_used_and_context(self):
        """Checks that the correct template is used after adding likes."""
        # Adds a liked product to session and retrieves the page
        product_1 = Product.objects.earliest('date_added')
        product_2 = Product.objects.latest('date_added')

        self.client.post(reverse('likes:likes-toggle'),
                         {'item-id': f'{product_1.id}'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.client.post(reverse('likes:likes-toggle'),
                         {'item-id': f'{product_2.id}'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = self.client.get(reverse('likes:likes-list'))
        session = self.client.session.get('likes')

        # Confirms correct likes in the session, and the correct template
        self.assertEqual(response.status_code, 200)
        self.assertEqual(session, [f'{product_1.id}', f'{product_2.id}'])
        self.assertTemplateUsed(response, 'likes/likes_list.html')

        # Logs in the user
        self.client.force_login(test_user)

        # Confirms that the session likes have been transferred to the user
        # and are correctly displayed in the context.
        response = self.client.get(reverse('likes:likes-list'))
        self.assertEqual(response.context['products'],
                         list(test_user.userprofile.liked_products.order_by(
                             '-liked__datetime_added')))

    def test_confirm_add_to_likes(self):
        """Tests that items are successfully added
        when a user is both logged in and anonymous"""

        product_1 = Product.objects.earliest('date_added')
        product_2 = Product.objects.latest('date_added')

        # Adds a liked product
        self.client.post(reverse('likes:likes-toggle'),
                         {'item-id': f'{product_1.id}'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Confirms likes are in the session
        session = self.client.session
        self.assertEqual(session['likes'], [f'{product_1.id}'])

        # Logs in the user
        self.client.force_login(test_user)

        # Adds likes while logged in and confirms that two liked
        # products are in the account.
        self.client.post(reverse('likes:likes-toggle'),
                         {'item-id': f'{product_2.id}'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTrue(len(test_user.userprofile.liked_products.all()) == 2)

    def test_error_on_incorrect_item_added(self):
        """Confirms that an error shows when adding an invalid item."""
        # Adds a liked product
        self.client.post(reverse('likes:likes-toggle'), {'item-id': 0},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Confirms an error message shows
        self.assertRaises(Exception, msg='Error adding item: 0')

    def test_forbidden_on_get(self):
        """Confirms that a 403 error when not using POST."""
        # Adds a liked product
        response = self.client.get(reverse('likes:likes-toggle'),
                                   {'item-id': '1'},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Confirms an error message shows
        self.assertEqual(response.status_code, 403)

    def test_successfully_remove_from_likes(self):
        """Checks that the like toggle removes liked products
        for both anonymous and logged in users."""

        product_1 = Product.objects.earliest('date_added')
        product_2 = Product.objects.latest('date_added')

        # Adds a liked product
        self.client.post(reverse('likes:likes-toggle'),
                         {'item-id': f'{product_1.id}'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Confirms the product is in the session
        session = self.client.session
        self.assertEqual(session['likes'], [f'{product_1.id}'])

        # Removes a liked product
        self.client.post(reverse('likes:likes-toggle'),
                         {'item-id': f'{product_1.id}'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Confirms the product is removed from the session
        session = self.client.session
        self.assertEqual(session['likes'], [])

        # Logs in a user
        self.client.force_login(test_user)

        # Adds a liked product
        self.client.post(reverse('likes:likes-toggle'),
                         {'item-id': f'{product_2.id}'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Removes a liked product
        self.client.post(reverse('likes:likes-toggle'),
                         {'item-id': f'{product_2.id}'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Confirms the product is removed from the users likes
        self.assertTrue(len(test_user.userprofile.liked_products.all()) == 0)

    def test_error_on_incorrect_item_removed(self):
        """Confirms an error occurs on trying to remove an invalid item"""
        product_1 = Product.objects.earliest('date_added')

        # Adds a liked product
        self.client.post(reverse('likes:likes-toggle'),
                         {'item-id': f'{product_1.id}'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Confirms the product is in the session
        session = self.client.session
        self.assertEqual(session['likes'], [f'{product_1.id}'])

        # Toggles an invalid item and confirms an error message
        self.client.post(reverse('likes:likes-toggle'), {'item-id': 0})
        self.assertRaises(Exception, msg='Error removing item: 0')

    def test_update_like_view(self):
        """Tests numerous functions relating to updating the likes update view,
        mainly to ensure that the context information is correct."""
        product_2 = Product.objects.latest('date_added')

        # Tests the template is updated when the view is called
        self.client.get(reverse('likes:likes-offcanvas'))
        self.assertTemplateUsed('likes/includes/likes_offcanvas.html')

        # Adds a liked product
        self.client.post(reverse('likes:likes-toggle'),
                         {'item-id': f'{product_2.id}'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # Updates the template and context
        self.client.get(reverse('likes:likes-offcanvas'))
        self.assertTemplateUsed('likes/includes/likes_offcanvas.html')

        # Logs a user in and updates the context
        self.client.force_login(test_user)
        self.client.get(reverse('likes:likes-offcanvas'))

        # Confirms the session context
        session = self.client.session
        self.assertEqual(session['likes'], [f'{product_2.id}'])
