"""Tests the Policy View"""
from django.shortcuts import reverse
from django.test import TestCase

from policies.models import Policy

from .test_models import (valid_cookie_policy, valid_general_policy,
                          valid_privacy_policy, valid_returns, valid_terms)


class TestPoliciesModels(TestCase):
    """Tests for Products models."""

    def setUp(self):
        valid_general_policy.save()
        valid_cookie_policy.save()
        valid_privacy_policy.save()
        valid_returns.save()
        valid_terms.save()

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
