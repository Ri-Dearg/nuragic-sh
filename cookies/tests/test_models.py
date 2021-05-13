"""Tests the Policy Model"""
from django.contrib.staticfiles.storage import staticfiles_storage
from django.shortcuts import reverse
from django.test import TestCase

from cookies.models import CookieRecord
from policies.tests.test_models import (valid_cookie_policy,
                                        valid_privacy_policy)
from users.tests.test_views import test_user


class TestCookiesModels(TestCase):
    """Tests for Cookies models."""

    def setUp(self):
        valid_cookie_policy.save()
        valid_privacy_policy.save()

        self.client.force_login(test_user)
        self.client.post(
            reverse('cookies:consent'
                    ), {'cookie-consent': 'opt-in',
                        'script-url': staticfiles_storage.url(
                            'js/custom/trackers.js')},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def test_cookie_str(self):
        """Tests the string method on the CookieRecord."""
        record = CookieRecord.objects.latest('date')
        self.assertEqual(
            str(record),
            (f'{record.ip_address}, {record.date}, {record.consent}'))
