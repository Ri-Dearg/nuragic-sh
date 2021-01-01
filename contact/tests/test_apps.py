"""Tests App Config."""
from contact.apps import ContactConfig
from django.apps import apps
from django.test import TestCase


class TestContactConfig(TestCase):
    """Tests the Contact app config."""

    def test_app(self):
        """Tests App name"""
        self.assertEqual('contact', ContactConfig.name)
        self.assertEqual('contact', apps.get_app_config('contact').name)
