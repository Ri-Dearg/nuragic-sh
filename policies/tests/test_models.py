"""Tests the Policy Model"""
from django.test import TestCase

from policies.models import Policy

valid_cookie_policy = Policy(name='Cookie Policy',
                             content='Cookie policy content',
                             active_cookie=True)
valid_cookie_policy2 = Policy(name='Cookie Policy 2',
                              content='Cookie policy content 2',
                              active_cookie=True)
valid_privacy_policy = Policy(name='Privacy Policy',
                              content='Privacy Policy Content',
                              active_privacy=True)
valid_privacy_policy2 = Policy(name='Privacy Policy 2',
                               content='Privacy Policy Content 2',
                               active_privacy=True)
valid_terms = Policy(name='Terms & Conditions',
                     content='Conditional Content',
                     active_terms=True)
valid_returns = Policy(name='Retruns and Refunds',
                       content='Returns',
                       active_returns=True)
valid_general_policy = Policy(name='General Policy',
                              content='General Content')


class TestPoliciesModels(TestCase):
    """Tests for Policy models."""

    def setUp(self):
        valid_cookie_policy.save()
        valid_cookie_policy2.save()
        valid_privacy_policy.save()
        valid_privacy_policy2.save()
        valid_general_policy.save()
        valid_returns.save()
        valid_terms.save()

    def test_policy_str(self):
        """Tests the string method on the Policy."""
        policy = Policy.objects.latest('date_created')
        self.assertEqual(str(policy),
                         (f'{policy.name}: {policy.date_created}'))
