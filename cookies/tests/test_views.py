"""Tests App Views."""
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase

from policies.tests.test_models import (valid_cookie_policy,
                                        valid_privacy_policy, valid_returns,
                                        valid_terms)
from users.tests.test_views import create_user


class TestCookiesViews(TestCase):
    """Tests views for the Cookies app."""

    def setUp(self):
        create_user()
        valid_cookie_policy.save()
        valid_privacy_policy.save()
        valid_returns.save()
        valid_terms.save()

    def test_cookie_acceptance(self):
        """Tests Cookie consent view."""
        response = self.client.get(
            reverse('cookies:consent'
                    ), {'cookie-consent': 'opt-in'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)

        test_user = get_user_model().objects.latest('date_joined')
        self.client.force_login(test_user)

        response = self.client.post(
            reverse('cookies:consent'
                    ), {'cookie-consent': 'decline'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(self.client.session['cookie_consent'], False)

        response = self.client.post(
            reverse('cookies:consent'
                    ), {'cookie-consent': 'opt-in'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(self.client.session['cookie_consent'], True)

        response = self.client.post(
            reverse('cookies:consent'
                    ), {'cookie-consent': 'analytics'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(self.client.session['analytics_consent'], True)
