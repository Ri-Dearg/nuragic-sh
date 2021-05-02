"""Tests Checkout App Name."""
from django.apps import apps
from django.test import TestCase

from checkout.apps import CheckoutConfig


class TestCheckoutConfig(TestCase):
    """Tests the Django app config."""

    def test_app(self):
        """Asserts app name is correct"""
        self.assertEqual('checkout', CheckoutConfig.name)
        self.assertEqual('checkout', apps.get_app_config('checkout').name)
