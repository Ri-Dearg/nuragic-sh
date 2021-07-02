"""Tests redirection for the custom allauth adapter."""
from django.test import TestCase

from policies.tests.test_models import (valid_cookie_policy,
                                        valid_privacy_policy, valid_returns,
                                        valid_terms)

from .test_models import generate_string


class TestAdapter(TestCase):
    """A custom adapter was created, subclassing django-allauth's for a custom
    redirect. This tests the correct redirect."""

    def setUp(self):
        valid_cookie_policy.save()
        valid_privacy_policy.save()
        valid_returns.save()
        valid_terms.save()

    def test_redirect(self):
        """Tests that the adapter redirects correctly."""
        # Generates fake credentials
        email = generate_string() + '@' + generate_string() + '.com'
        password = generate_string()

        # Creates a fake user
        new_user = {'username': generate_string(),
                    'email1': email,
                    'email2': email,
                    'password1': password,
                    'password2': password
                    }

        # Signs the user up with a redirect in the URL
        response = self.client.post('/accounts/signup/?next=/products/1/',
                                    new_user, follow=True)

        # Declares next as the query string
        next_page = response.request['QUERY_STRING']

        # Confirms the redirect is correct
        self.assertEqual('next=/products/1/', next_page)
        self.assertEqual(response.status_code, 200)
