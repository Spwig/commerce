"""
Regression guards for provider pluggability.

A new payment provider must work with ZERO edits to core. These tests lock in
the two generic seams that replaced per-provider ``slug ==`` branches:

- handler_config comes from the provider's own response (get_handler_config).
- the webhook signature header comes from the component manifest
  (_get_webhook_signature -> _manifest_signature_header).

If someone reintroduces slug hardcoding, or breaks the generic path, these fail.
"""

from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from payment_providers.api_serializers import PaymentIntentResponseSerializer
from payment_providers.views import handlers


class GenericHandlerConfigTests(SimpleTestCase):
    def test_provider_returned_handler_config_is_passed_through(self):
        # A provider the serializer has never heard of, whose response carries a
        # handler_config, must have it returned verbatim — no slug branch.
        obj = MagicMock()
        obj.provider_response = {"handler_config": {"key_id": "pk_x", "order_id": "o_1"}}
        obj.provider_account.component.get_manifest.return_value = {
            "frontend": {"checkout_handler": "handler.js"}
        }
        result = PaymentIntentResponseSerializer().get_handler_config(obj)
        self.assertEqual(result, {"key_id": "pk_x", "order_id": "o_1"})

    def test_no_frontend_manifest_returns_none(self):
        obj = MagicMock()
        obj.provider_response = {"handler_config": {"x": 1}}
        obj.provider_account.component.get_manifest.return_value = {}  # no "frontend"
        self.assertIsNone(PaymentIntentResponseSerializer().get_handler_config(obj))


class WebhookSignatureResolutionTests(SimpleTestCase):
    def test_uses_manifest_declared_header(self):
        # The pluggable path: header name comes from the component manifest.
        headers = {"X-Newprovider-Signature": "sig123"}
        with patch.object(
            handlers, "_manifest_signature_header", return_value="X-Newprovider-Signature"
        ):
            self.assertEqual(handlers._get_webhook_signature(headers, "newprovider"), "sig123")

    def test_falls_back_to_common_header_without_manifest(self):
        headers = {"X-Signature": "sig456"}
        with patch.object(handlers, "_manifest_signature_header", return_value=None):
            self.assertEqual(handlers._get_webhook_signature(headers, "unknown"), "sig456")

    def test_no_hardcoded_provider_map(self):
        # There is no longer a hardcoded slug->header map. A provider whose
        # header is neither declared in its manifest nor a common name is not
        # rescued by core — proving the per-provider coupling is gone.
        headers = {"Stripe-Signature": "whsec"}
        with patch.object(handlers, "_manifest_signature_header", return_value=None):
            self.assertEqual(handlers._get_webhook_signature(headers, "stripe"), "")

    def test_missing_signature_returns_empty(self):
        with patch.object(handlers, "_manifest_signature_header", return_value=None):
            self.assertEqual(handlers._get_webhook_signature({}, "whatever"), "")
