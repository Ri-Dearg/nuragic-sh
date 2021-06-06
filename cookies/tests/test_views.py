"""Tests App Views."""
from django.contrib.staticfiles.storage import staticfiles_storage
from django.shortcuts import reverse
from django.test import TestCase

from policies.tests.test_models import (valid_cookie_policy,
                                        valid_privacy_policy, valid_returns,
                                        valid_terms)
from users.tests.test_views import test_user


class TestCookiesViews(TestCase):
    """Tests views for the Cookies app."""

    def setUp(self):
        valid_cookie_policy.save()
        valid_privacy_policy.save()
        valid_returns.save()
        valid_terms.save()

    def test_cookie_acceptance(self):
        """Tests Cookie consent view."""
        response = self.client.get(
            reverse('cookies:consent'
                    ), {'cookie-consent': 'opt-in',
                        'script-url': staticfiles_storage.url(
                            'js/custom/fullConsent.js')},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)

        self.client.force_login(test_user)

        response = self.client.post(
            reverse('cookies:consent'
                    ), {'cookie-consent': 'decline'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(self.client.session['cookie_consent'], False)

        response = self.client.post(
            reverse('cookies:consent'
                    ), {'cookie-consent': 'opt-in',
                        'script-url': staticfiles_storage.url(
                            'js/custom/fullConsent.js')},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(self.client.session['cookie_consent'], True)

        response = self.client.post(
            reverse('cookies:consent'
                    ), {'cookie-consent': 'analytics',
                        'script-url': staticfiles_storage.url(
                            'js/custom/gAnalytics.js')},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(self.client.session['analytics_consent'], True)
