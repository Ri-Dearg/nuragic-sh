"""Tests views for the Info app."""

from django.shortcuts import reverse
from django.test import TestCase

from info.models import Category, Page
from policies.tests.test_models import make_policies

from .test_models import make_info_models


class TestInfoViews(TestCase):
    """Tests for Info app views."""

    def setUp(self):
        """Sets up a model instances for tests."""
        make_policies()
        make_info_models()

    def test_render_home(self):
        """Tests templates for index page."""
        response = self.client.get(reverse('info:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info/index.html')
        self.assertTemplateUsed(response, 'base/base.html')
        self.assertTemplateUsed(response, 'base/includes/header.html')
        self.assertTemplateUsed(response, 'base/includes/footer.html')

    def test_render_category_detail(self):
        """Tests templates for Category detail page."""
        category = Category.objects.latest('date_added')
        response = self.client.get(
            reverse('info:category-detail',
                    kwargs={'slug': category.slug, 'pk': category.id}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info/category_detail.html')
        self.assertTemplateUsed(response, 'info/includes/category_info.html')
        self.assertTemplateUsed(response, 'base/base.html')
        self.assertTemplateUsed(response, 'base/includes/header.html')
        self.assertTemplateUsed(response, 'base/includes/footer.html')
        self.assertTrue(response.context['active_category'], f'{category.id}')
        self.assertTrue(response.context['active_all'], f'{category.id}')

        response = self.client.get(category.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info/category_detail.html')

    def test_render_page_detail(self):
        """Tests templates for Page detail page."""
        page = Page.objects.latest('date_added')
        response = self.client.get(
            reverse('info:page-detail',
                    kwargs={'slug': page.slug, 'pk': page.id}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info/page_detail.html')
        self.assertTemplateUsed(response, 'base/base.html')
        self.assertTemplateUsed(response, 'base/includes/header.html')
        self.assertTemplateUsed(response, 'base/includes/footer.html')
        self.assertTrue(
            response.context['active_category'], f'{page.id}')
        self.assertTrue(response.context['active_page'], f'{page.id}')

        response = self.client.get(page.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info/page_detail.html')
