"""Tests App Config."""
from django.apps import apps
from django.test import TestCase

from contact.apps import ContactConfig


class TestContactConfig(TestCase):
    """Tests the Contact app config."""

    def test_app(self):
        """Tests App name"""
        self.assertEqual('contact', ContactConfig.name)
        self.assertEqual('contact', apps.get_app_config('contact').name)
