"""Tests App Config."""
from django.apps import apps
from django.test import TestCase

from policies.apps import PoliciesConfig


class TestProductsConfig(TestCase):
    """Tests the Info app config."""

    def test_app(self):
        """Tests App name"""
        self.assertEqual('policies', PoliciesConfig.name)
        self.assertEqual('policies',
                         apps.get_app_config('policies').name)
