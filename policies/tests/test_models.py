"""Tests the Policy Model"""
from django.test import TestCase

from policies.models import Policy


def make_policies():
    """Makes the policies for testing."""
    Policy.objects.create(name_en='Cookie Policy',
                          name_it='Cookie Policy',
                          content='Cookie policy content',
                          active_cookie=True)
    Policy.objects.create(name_en='Cookie Policy 2',
                          name_it='Cookie Policy 2',
                          content='Cookie policy content 2',
                          active_cookie=True)
    Policy.objects.create(name_en='Privacy Policy',
                          name_it='Privacy Policy',
                          content='Privacy Policy Content',
                          active_privacy=True)
    Policy.objects.create(name_en='Privacy Policy 2',
                          name_it='Privacy Policy 2',
                          content='Privacy Policy Content 2',
                          active_privacy=True)
    Policy.objects.create(name_en='Terms & Conditions',
                          name_it='Terms & Conditions',
                          content='Conditional Content',
                          active_terms=True)
    Policy.objects.create(name_en='Returns and Refunds',
                          name_it='Retruns and Refunds',
                          content='Returns',
                          active_returns=True)
    Policy.objects.create(name_en='General Policy',
                          name_it='General Policy',
                          content='General Content')


class TestPoliciesModels(TestCase):
    """Tests for Policy models."""

    def setUp(self):
        make_policies()

    def test_policy_str(self):
        """Tests the string method on the Policy."""
        policy = Policy.objects.latest('date_created')
        self.assertEqual(str(policy),
                         (f'{policy.name}: {policy.date_created}'))
