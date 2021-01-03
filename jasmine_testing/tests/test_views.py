"""Tests views for the Jasmine app."""

from django.contrib.auth.models import User
from django.test import TestCase


class TestJasmineViews(TestCase):
    """Tests for Jasmine app views."""

    def test_render_jasmine(self):
        """Tests templates for jasmine page."""
        response = self.client.get('/jasmine/')
        self.assertEqual(response.status_code, 500)

        password = 'mypassword'
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com',
                                                 password)
        self.client.login(username=my_admin.username, password=password)

        response = self.client.get('/jasmine/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jasmine_testing/jasmine.html')
