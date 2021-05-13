"""Tests App Config."""
from django.apps import apps
from django.test import TestCase

from cookies.apps import CookiesConfig


class TestProductsConfig(TestCase):
    """Tests the Info app config."""

    def test_app(self):
        """Tests App name"""
        self.assertEqual('cookies', CookiesConfig.name)
        self.assertEqual('cookies',
                         apps.get_app_config('cookies').name)
