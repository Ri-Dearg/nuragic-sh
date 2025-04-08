"""Test stripe webhooks with spoof data."""

import hashlib
import hmac
from time import time

from django.conf import settings
from django.shortcuts import reverse
from django.test import TestCase

from .stripe_spoof import PAYMENT_INTENT_FAILED


class TestWebhook(TestCase):
    """Tests for webhook endpoints.

    Args:
        TestCase (class): django TestCase.

    """

    def _stripe_sig(self, payload: str) -> str:
        """Spoof stripe API signature.

        Args:
            payload (str): the raw JSON content.

        Returns:
            str: A spoofed signature.

        """
        timestamp = int(time())
        wh_secret = settings.STRIPE_WH_SECRET

        # Construct the signed_payload
        signed_payload = f'{timestamp}.{payload}'

        # Create the v1 signature
        v1_signature = hmac.new(
            bytes(wh_secret, 'utf-8'),
            msg=bytes(signed_payload, 'utf-8'),
            digestmod=hashlib.sha256,
        ).hexdigest()

        # Create the v0
        v0_signature = hmac.new(
            bytes(wh_secret, 'utf-8'),
            msg=bytes(signed_payload, 'utf-8'),
            digestmod=hashlib.sha1,
        ).hexdigest()

        # Construct the signature header
        return f't={timestamp},v1={v1_signature},v0={v0_signature}'

    def test_payment_intent_failed(self) -> None:
        """Test a failed payment webhook response."""
        api_response = PAYMENT_INTENT_FAILED

        stripe_sig = self._stripe_sig(api_response)
        response = self.client.post(
            reverse('checkout:webhook'),
            api_response,
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE=stripe_sig,
        )
        self.assertEqual(response.status_code, 200)
