"""Tests App Config."""
from django.apps import apps
from django.test import TestCase
from info.apps import InfoConfig


class TestInfoConfig(TestCase):
    """Tests the Info app config."""

    def test_app(self):
        """Tests App name"""
        self.assertEqual('info', InfoConfig.name)
        self.assertEqual('info',
                         apps.get_app_config('info').name)
