"""Tests views for the Jasmine app."""
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase

from policies.tests.test_models import make_policies
from users.tests.test_views import create_user


class TestJasmineViews(TestCase):
    """Tests for Jasmine app views."""

    def setUp(self):
        create_user()
        make_policies()

    def test_render_jasmine(self):
        """Tests templates for jasmine page."""
        response = self.client.get(reverse('jasmine:test'))
        self.assertEqual(response.status_code, 302)

        test_user = get_user_model().objects.latest('date_joined')
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
