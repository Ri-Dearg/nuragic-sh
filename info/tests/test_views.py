"""Tests views for the Info app."""

from django.test import TestCase

from info.models import Category, Page

from .test_models import valid_category, valid_page


class TestInfoViews(TestCase):
    """Tests for Info app views."""

    def setUp(self):
        """Sets up a model instances for tests."""

        valid_category.save()

        valid_page.save()

    def test_render_home(self):
        """Tests templates for index page."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info/index.html')
        self.assertTemplateUsed(response, 'base/base.html')
        self.assertTemplateUsed(response, 'base/includes/header.html')
        self.assertTemplateUsed(response, 'base/includes/footer.html')

    def test_render_category_detail(self):
        """Tests templates for Category detail page."""
        category = Category.objects.latest('date_added')
        response = self.client.get(f'/category/{category.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info/category_detail.html')
        self.assertTemplateUsed(response, 'info/includes/category_info.html')
        self.assertTemplateUsed(response, 'base/base.html')
        self.assertTemplateUsed(response, 'base/includes/header.html')
        self.assertTemplateUsed(response, 'base/includes/footer.html')
        self.assertTrue(response.context['active_category'], f'{category.id}')
        self.assertTrue(response.context['active_all'], f'{category.id}')

    def test_render_page_detail(self):
        """Tests templates for Page detail page."""
        page = Page.objects.latest('date_added')
        response = self.client.get(f'/page/{page.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info/page_detail.html')
        self.assertTemplateUsed(response, 'base/base.html')
        self.assertTemplateUsed(response, 'base/includes/header.html')
        self.assertTemplateUsed(response, 'base/includes/footer.html')
        self.assertTrue(
            response.context['active_category'], f'{page.id}')
        self.assertTrue(response.context['active_page'], f'{page.id}')
