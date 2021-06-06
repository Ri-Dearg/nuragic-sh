"""Tests views for the Jasmine app."""
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase

from policies.tests.test_models import (valid_cookie_policy,
                                        valid_privacy_policy, valid_returns,
                                        valid_terms)
from users.tests.test_views import test_user


class TestJasmineViews(TestCase):
    """Tests for Jasmine app views."""

    def setUp(self):
        valid_cookie_policy.save()
        valid_privacy_policy.save()
        valid_returns.save()
        valid_terms.save()

    def test_render_jasmine(self):
        """Tests templates for jasmine page."""
        response = self.client.get(reverse('jasmine:test'))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(test_user)
        response = self.client.get(reverse('jasmine:test'))
        self.assertEqual(response.status_code, 403)

        password = 'mypassword'
        my_admin = get_user_model().objects.create_superuser(
            'myuser',
            'myemail@test.com',
            password)
        self.client.login(username=my_admin.username, password=password)

        response = self.client.get(reverse('jasmine:test'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jasmine_testing/jasmine.html')
