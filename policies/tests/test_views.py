"""Tests the Policy View"""
from django.shortcuts import reverse
from django.test import TestCase

from policies.models import Policy

from .test_models import make_policies


class TestPoliciesModels(TestCase):
    """Tests for Products models."""

    def setUp(self):
        make_policies()

    def test_policy_detail_view(self):
        """Checks that the url produces the correct template."""
        policy = Policy.objects.latest('date_created')
        response = self.client.get(
            reverse('policies:policy-detail',
                    kwargs={'slug': policy.slug, 'pk': policy.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'policies/policy_detail.html')

        response = self.client.get(policy.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'policies/policy_detail.html')
