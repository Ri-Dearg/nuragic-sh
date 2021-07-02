"""Tests the Policy Model"""
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase

from cookies.models import CookieRecord
from policies.tests.test_models import (valid_cookie_policy,
                                        valid_privacy_policy, valid_returns,
                                        valid_terms)
from users.tests.test_views import create_user


class TestCookiesModels(TestCase):
    """Tests for Cookies models."""

    def setUp(self):
        create_user()
        valid_cookie_policy.save()
        valid_privacy_policy.save()
        valid_returns.save()
        valid_terms.save()

        test_user = get_user_model().objects.latest('date_joined')
        self.client.force_login(test_user)
        self.client.post(
            reverse('cookies:consent'
                    ), {'cookie-consent': 'opt-in'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def test_cookie_str(self):
        """Tests the string method on the CookieRecord."""
        record = CookieRecord.objects.latest('date')
        self.assertEqual(
            str(record),
            (f'{record.ip_address}, {record.date}, {record.consent}'))
