"""Tests app file for the users module."""
from django.apps import apps
from django.test import TestCase

from users.apps import UsersConfig


class TestUsersConfig(TestCase):
    """Tests the Django app config."""

    def test_app(self):
        """Tests user appname."""
        self.assertEqual('users', UsersConfig.name)
        self.assertEqual('users', apps.get_app_config('users').name)
