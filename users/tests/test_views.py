"""Tests views for custom authorization functions."""
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase

from contact.models import Newsletter
from users.tests.test_adapter import generate_string

user_model = get_user_model()
user_model.objects.get_or_create(
    username=generate_string(),
    email=f'{generate_string()}@{generate_string()}.com',
    password=generate_string())

test_user = user_model.objects.latest('date_joined')


class TestUserViews(TestCase):
    """Tests views for the Users app."""

    def test_custom_forms_rendering(self):
        """Tests the correct use of custom forms."""
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/base.html')
        self.assertTemplateUsed(response, 'base/includes/header.html')
        self.assertTemplateUsed(response, 'base/includes/info_nav.html')
        self.assertTemplateUsed(response, 'base/includes/footer.html')

        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/base.html')
        self.assertTemplateUsed(response, 'base/includes/header.html')
        self.assertTemplateUsed(response, 'base/includes/info_nav.html')
        self.assertTemplateUsed(response, 'base/includes/footer.html')

        response = self.client.get('/accounts/password/reset/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/base.html')
        self.assertTemplateUsed(response, 'base/includes/header.html')
        self.assertTemplateUsed(response, 'base/includes/info_nav.html')
        self.assertTemplateUsed(response, 'base/includes/footer.html')

        response = self.client.get(
            '/accounts/password/reset/key/2-set-password/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/base.html')
        self.assertTemplateUsed(response, 'base/includes/header.html')
        self.assertTemplateUsed(response, 'base/includes/info_nav.html')
        self.assertTemplateUsed(response, 'base/includes/footer.html')

    def test_user_profile_context(self):
        """Tests the all the correct context appear on the user's settings
        page. That's their shipping and billing info, emails, and custom info
        change forms"""

        # Retrieves the most recently created user, logs them in
        # and goes to their profile.
        self.client.force_login(test_user)

        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse('users:user-detail',
                    kwargs={'pk': test_user.id,
                            'username': {test_user.username}}))

        # Confirms context for all required page items as stated in the above.
        self.assertTrue(response.context['user_profile_detail'])
        self.assertTrue(response.context['add_email_form'])
        self.assertTrue(response.context['change_password_form'])
        self.assertTrue(response.context['user'])
        self.assertTrue(response.context['profile'])

    def test_custom_email_view(self):
        """Confirms a custom view is used for changing email."""
        # Retrieves the most recently created user and logs them in
        self.client.force_login(test_user)

        # Confirms a custom template is used
        self.client.get(reverse('users:user-email'))
        self.assertTemplateUsed('users/user_detail.html')

    def test_custom_password_view(self):
        """Confirms a custom view is used for changing password."""
        # Retrieves the most recently created user and logs them in
        self.client.force_login(test_user)

        # Confirms a custom template is used
        self.client.get(reverse('users:user-change-password'))
        self.assertTemplateUsed('users/user_detail.html')

    def test_custom_update_shipping(self):
        """Confirms a custom view is used for changing email."""
        # Retrieves the most recently created user and logs them in
        self.client.force_login(test_user)

        # Posts a valid form to update the info
        self.client.post('/accounts/shipping-billing/?next=/',
                         {'shipping_full_name': 'Test Name',
                          'shipping_phone_number_0': '+93',
                          'shipping_phone_number_1': '1',
                          'shipping_street_address_1': '',
                          'shipping_street_address_2': '',
                          'shipping_town_or_city': '',
                          'shipping_county': '',
                          'shipping_postcode': '424242',
                          'shipping_country': 'IE',
                          'billing_full_name': '',
                          'billing_phone_number_0': '+93',
                          'billing_phone_number_1': '1',
                          'billing_street_address_1': '',
                          'billing_street_address_2': '',
                          'billing_town_or_city': '',
                          'billing_county': '',
                          'billing_postcode': '',
                          'billing_country': 'IE'})
        updated_user = user_model.objects.latest('date_joined')

        # Confirms the name has been updated
        self.assertEqual(updated_user.userprofile.shipping_full_name,
                         'Test Name')

        # Posts an ivalid form to update the info
        self.client.post('/accounts/shipping-billing/?next=/',
                         {'shipping_postcode': '123456789012345678901'})

        self.assertEqual(updated_user.userprofile.shipping_phone_number,
                         '+93.1')

    def test_update_newsletter(self):
        """Tests different methods of updating the email lists."""
        # Retrieves the most recently created user and logs them in
        self.client.force_login(test_user)
        response = self.client.post('/accounts/newsletter/?next=/',
                                    {'save': '',
                                     'newsletter': 'en',
                                     'email': test_user.email})
        newsletter_1 = Newsletter.objects.filter(
            name='basic').order_by('id').first()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(test_user.email in newsletter_1.email_list_en)

        self.client.post('/accounts/newsletter/?next=/',
                         {'save': '',
                          'newsletter': 'en',
                          'email': test_user.email})

        self.assertTrue(newsletter_1.email_list_en == [test_user.email])

        self.client.post('/accounts/newsletter/?next=/',
                         {'save': '',
                          'newsletter': 'it',
                          'email': test_user.email})

        newsletter_update = Newsletter.objects.get(pk=newsletter_1.id)

        self.assertTrue(test_user.email in newsletter_update.email_list_it)
        self.assertTrue(test_user.email not in newsletter_update.email_list_en)

        self.client.get('/accounts/newsletter/?next=/',
                        {'save': '',
                         'newsletter': 'en',
                         'email': test_user.email})

        newsletter_update = Newsletter.objects.get(pk=newsletter_1.id)
        self.assertTrue(test_user.email in newsletter_update.email_list_it)
        self.assertTrue(test_user.email not in newsletter_update.email_list_en)

        self.client.post('/accounts/newsletter/?next=/',
                         {'unsub': '',
                          'email': test_user.email})

        newsletter_update = Newsletter.objects.get(pk=newsletter_1.id)
        self.assertTrue(test_user.email not in newsletter_update.email_list_it)
        self.assertTrue(test_user.email not in newsletter_update.email_list_en)

        self.client.post('/accounts/newsletter/?next=/',
                         {'save': '',
                          'newsletter': 'en',
                          'email': test_user.email})
        self.client.post('/accounts/newsletter/?next=/',
                         {'unsub': '',
                          'email': test_user.email})

        newsletter_update = Newsletter.objects.get(pk=newsletter_1.id)
        self.assertTrue(test_user.email not in newsletter_update.email_list_it)
        self.assertTrue(test_user.email not in newsletter_update.email_list_en)
