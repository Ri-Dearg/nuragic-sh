"""Tests views for the Contact app."""
from django.shortcuts import reverse
from django.test import TestCase

from contact.models import Newsletter
from info.tests.test_models import make_info_models
from policies.tests.test_models import make_policies


class TestContactViews(TestCase):
    """Tests for Contact app views."""

    def setUp(self):
        """Created instances for use in tests"""
        make_policies()
        Newsletter.objects.create(name='basic')
        make_info_models()

    def test_contact_template(self):
        """Tests templates for Contact page."""
        self.client.get(reverse('contact:email-form'))
        self.assertTemplateUsed('contact_form.html')

    def test_newsletter_singup(self):
        """FETCH method for signing up to newletter checked."""
        # Signs up for newsletter in both languages.
        self.client.post(reverse('contact:newsletter'),
                         {'email_en': 'test@test.com'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.client.post(reverse('contact:newsletter'),
                         {'email_it': 'test@test.com'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                         HTTP_ACCEPT_LANGUAGE='it')

        newsletter_1 = Newsletter.objects.filter(
            name='basic').order_by('id').first()
        # Retrieves the newletter and checks that the email is present
        self.assertTrue("test@test.com" in newsletter_1.email_list_en)

        # Checks the correct message is processed if already signed up
        response = self.client.post(reverse('contact:newsletter'),
                                    {'email_en': 'test@test.com'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                    HTTP_ACCEPT_LANGUAGE='en')
        self.assertTrue(response.content,
                        {"message": "You have already signed up for the newsletter.",  # NOQA E501
                         "tag": "info"})

        # Checks for refusal in a GET request
        response = self.client.get(reverse('contact:newsletter'),
                                   {'email_en': 'test@test.com'},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)
