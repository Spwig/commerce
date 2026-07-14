"""
Tests for Shipping Webhook Endpoints

Tests webhook receiver functionality, logging, and task enqueueing.
Provider-specific webhook parsing will be tested when providers are implemented.
"""

import json
import unittest
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from shipping.models import WebhookLog

User = get_user_model()


@override_settings(LANGUAGE_CODE="en-us")
class WebhookEndpointTests(TestCase):
    """Test webhook endpoint functionality"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_provider_webhook_url_resolution(self):
        """Test that webhook URL resolves correctly"""
        url = reverse("shipping_provider_webhook", kwargs={"provider_key": "easypost"})
        self.assertIn("/webhooks/shipping/easypost/", url)

    def test_webhook_health_check_url(self):
        """Test health check URL"""
        url = reverse("shipping_webhook_health")
        self.assertIn("/webhooks/shipping/health/", url)

    def test_webhook_docs_url(self):
        """Test documentation URL"""
        url = reverse("shipping:webhook_docs")
        self.assertIn("/admin/shipping/webhooks/", url)

    # NOTE: The webhook endpoint now enforces provider registration and
    # signature verification. Tests below use the unregistered provider path
    # (no ProviderRegistry entry) which rejects with 400 "Unknown provider"
    # AFTER logging the WebhookLog with processing_status='failed'. This
    # verifies the logging infrastructure works regardless of the security
    # decision. See test_webhooks_signature_verification.py (if present) for
    # positive signature-verification paths using MockProvider.

    @patch("shipping.webhooks.process_webhook.delay")
    def test_webhook_unknown_provider_logs_but_rejects(self, mock_task):
        """Unregistered provider webhooks are logged then rejected with 400"""
        url = reverse("shipping_provider_webhook", kwargs={"provider_key": "easypost"})
        payload = {
            "id": "webhook_123",
            "type": "tracking.updated",
            "data": {"tracking_id": "TRACK123", "status": "in_transit"},
        }

        response = self.client.post(url, data=json.dumps(payload), content_type="application/json")

        # Unknown provider — rejected with 400
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["status"], "error")

        # But WebhookLog is still created for audit
        webhook_log = WebhookLog.objects.latest("received_at")
        self.assertEqual(webhook_log.provider_key, "easypost")
        self.assertEqual(webhook_log.payload["id"], "webhook_123")
        # Marked as failed because provider unknown
        self.assertEqual(webhook_log.processing_status, "failed")

        # Task NOT enqueued — signature verification failed
        mock_task.assert_not_called()

    @patch("shipping.webhooks.process_webhook.delay")
    def test_webhook_with_invalid_json(self, mock_task):
        """Test webhook with invalid JSON payload — payload is captured as raw_body"""
        url = reverse("shipping_provider_webhook", kwargs={"provider_key": "test"})

        response = self.client.post(url, data="invalid json {", content_type="application/json")

        # Unknown provider still returns 400
        self.assertEqual(response.status_code, 400)

        # Should still create log with raw body
        webhook_log = WebhookLog.objects.latest("received_at")
        self.assertIn("raw_body", webhook_log.payload)

    @patch("shipping.webhooks.process_webhook.delay")
    def test_webhook_logs_headers(self, mock_task):
        """Test that webhook logs HTTP headers even for unregistered providers"""
        url = reverse("shipping_provider_webhook", kwargs={"provider_key": "easypost"})
        payload = {"test": "data"}

        response = self.client.post(
            url,
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_X_WEBHOOK_ID="webhook_123",
            HTTP_X_SIGNATURE="test_signature",
        )

        # Unknown provider rejected with 400 but headers still logged
        self.assertEqual(response.status_code, 400)

        webhook_log = WebhookLog.objects.latest("received_at")
        self.assertIn("HTTP_X_WEBHOOK_ID", webhook_log.headers)
        self.assertIn("HTTP_X_SIGNATURE", webhook_log.headers)
        self.assertEqual(webhook_log.headers["HTTP_X_WEBHOOK_ID"], "webhook_123")

    @patch("shipping.webhooks.process_webhook.delay")
    def test_webhook_extracts_webhook_id(self, mock_task):
        """Test that webhook ID is extracted from various sources (logged then rejected)"""
        url = reverse("shipping_provider_webhook", kwargs={"provider_key": "test"})
        payload = {"webhook_id": "test_123"}

        response = self.client.post(url, data=json.dumps(payload), content_type="application/json")

        # Unknown provider still returns 400
        self.assertEqual(response.status_code, 400)
        # Webhook ID logged in system logs — verify the payload was captured
        webhook_log = WebhookLog.objects.latest("received_at")
        self.assertEqual(webhook_log.payload.get("webhook_id"), "test_123")

    @patch("shipping.webhooks.process_webhook.delay")
    def test_webhook_unregistered_provider_does_not_enqueue_task(self, mock_task):
        """Test that unregistered provider webhooks do NOT enqueue Celery task"""
        url = reverse("shipping_provider_webhook", kwargs={"provider_key": "easypost"})
        payload = {"test": "data"}

        response = self.client.post(url, data=json.dumps(payload), content_type="application/json")

        # Unknown provider: rejected without enqueueing
        self.assertEqual(response.status_code, 400)
        mock_task.assert_not_called()

    @patch("shipping.webhooks.process_webhook.delay")
    def test_webhook_returns_400_for_unknown_provider(self, mock_task):
        """Test that unknown provider webhook returns 400"""
        url = reverse("shipping_provider_webhook", kwargs={"provider_key": "test"})
        payload = {"test": "data"}

        response = self.client.post(url, data=json.dumps(payload), content_type="application/json")

        # New behavior: reject unknown providers explicitly
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["status"], "error")

    def test_webhook_only_accepts_post(self):
        """Test that webhook only accepts POST requests"""
        url = reverse("shipping_provider_webhook", kwargs={"provider_key": "test"})

        # GET should fail
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

        # PUT should fail
        response = self.client.put(url, data="{}", content_type="application/json")
        self.assertEqual(response.status_code, 405)

        # DELETE should fail
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 405)

    @patch("shipping.webhooks.process_webhook.delay")
    def test_webhook_with_different_providers(self, mock_task):
        """Test webhooks from different providers are all logged with provider_key"""
        providers = ["easypost", "shipstation", "shippo", "custom"]

        for provider in providers:
            url = reverse("shipping_provider_webhook", kwargs={"provider_key": provider})
            payload = {"provider": provider, "test": "data"}

            response = self.client.post(
                url, data=json.dumps(payload), content_type="application/json"
            )

            # All unknown providers return 400 but log the webhook
            self.assertEqual(response.status_code, 400)

            # Verify provider_key was logged correctly
            webhook_log = WebhookLog.objects.latest("received_at")
            self.assertEqual(webhook_log.provider_key, provider)


@override_settings(LANGUAGE_CODE="en-us")
class WebhookHealthCheckTests(TestCase):
    """Test webhook health check endpoint"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_health_check_returns_200(self):
        """Test that health check returns 200 OK"""
        url = reverse("shipping_webhook_health")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "shipping-webhooks")

    def test_health_check_accepts_head(self):
        """Test that health check accepts HEAD requests"""
        url = reverse("shipping_webhook_health")
        response = self.client.head(url)
        self.assertEqual(response.status_code, 200)

    def test_health_check_rejects_post(self):
        """Test that health check rejects POST"""
        url = reverse("shipping_webhook_health")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)


@override_settings(LANGUAGE_CODE="en-us")
class WebhookDocumentationTests(TestCase):
    """Test webhook documentation page"""

    def setUp(self):
        """Set up test client with staff user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@example.com", is_staff=True
        )
        self.client.login(username="testuser", password="testpass123")

    @unittest.skip("Documentation page requires admin templates - will test in integration tests")
    def test_webhook_docs_page_loads(self):
        """Test that documentation page loads"""
        url = reverse("shipping:webhook_docs")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Webhook Endpoints", response.content)

    @unittest.skip("Documentation page requires admin templates - will test in integration tests")
    def test_webhook_docs_shows_examples(self):
        """Test that docs page shows webhook examples"""
        url = reverse("shipping:webhook_docs")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # Should show provider examples
        self.assertIn(b"easypost", response.content.lower())


@override_settings(LANGUAGE_CODE="en-us")
class WebhookLogModelTests(TestCase):
    """Test WebhookLog model interactions"""

    @patch("shipping.webhooks.process_webhook.delay")
    def test_webhook_log_created_with_all_fields(self, mock_task):
        """Test that WebhookLog captures all required fields even when provider is unregistered"""
        client = Client()
        url = reverse("shipping_provider_webhook", kwargs={"provider_key": "easypost"})
        payload = {"id": "evt_123", "type": "tracking.updated", "data": {"tracking_id": "TRACK123"}}

        response = client.post(
            url,
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_X_WEBHOOK_ID="webhook_123",
        )

        # Unregistered provider: rejected with 400 but log still captured
        self.assertEqual(response.status_code, 400)

        webhook_log = WebhookLog.objects.latest("received_at")
        self.assertEqual(webhook_log.provider_key, "easypost")
        self.assertTrue(webhook_log.endpoint.startswith("/webhooks/"))
        self.assertIsInstance(webhook_log.payload, dict)
        self.assertIsInstance(webhook_log.headers, dict)
        # New behavior: unregistered provider marked failed instead of pending
        self.assertEqual(webhook_log.processing_status, "failed")
        self.assertTrue(webhook_log.id)  # UUID assigned

    @patch("shipping.webhooks.process_webhook.delay")
    def test_webhook_log_queryable(self, mock_task):
        """Test that webhook logs are queryable by provider_key"""
        client = Client()

        # Create webhooks for different providers (all unregistered — still logged)
        for provider in ["easypost", "shipstation"]:
            url = reverse("shipping_provider_webhook", kwargs={"provider_key": provider})
            client.post(
                url, data=json.dumps({"provider": provider}), content_type="application/json"
            )

        # Query by provider
        easypost_logs = WebhookLog.objects.filter(provider_key="easypost")
        self.assertEqual(easypost_logs.count(), 1)

        shipstation_logs = WebhookLog.objects.filter(provider_key="shipstation")
        self.assertEqual(shipstation_logs.count(), 1)

    @patch("shipping.webhooks.process_webhook.delay")
    def test_failed_webhook_logs_error(self, mock_task):
        """Test that unregistered-provider webhooks log a failure error message"""
        client = Client()
        url = reverse("shipping_provider_webhook", kwargs={"provider_key": "test"})

        response = client.post(
            url, data=json.dumps({"test": "data"}), content_type="application/json"
        )

        # Unknown provider — rejected with 400
        self.assertEqual(response.status_code, 400)

        # Webhook log should record the failure
        webhook_log = WebhookLog.objects.latest("received_at")
        self.assertEqual(webhook_log.processing_status, "failed")
        # error_message includes "not registered" text
        self.assertIn("not registered", webhook_log.error_message.lower())


@override_settings(LANGUAGE_CODE="en-us")
class WebhookCSRFTests(TestCase):
    """Test CSRF exemption for webhooks"""

    def test_webhook_exempt_from_csrf(self):
        """Test that webhook endpoint is exempt from CSRF protection"""
        client = Client(enforce_csrf_checks=True)
        url = reverse("shipping_provider_webhook", kwargs={"provider_key": "test"})

        # Should work without CSRF token (no 403). Unregistered provider still
        # rejects with 400, but the point is that CSRF is not enforced.
        response = client.post(
            url, data=json.dumps({"test": "data"}), content_type="application/json"
        )

        # Should not get CSRF error (403)
        self.assertNotEqual(response.status_code, 403)
        # Unknown provider — 400
        self.assertEqual(response.status_code, 400)


@override_settings(LANGUAGE_CODE="en-us")
class WebhookResponseFormatTests(TestCase):
    """Test webhook response format"""

    @patch("shipping.webhooks.process_webhook.delay")
    def test_success_response_format(self, mock_task):
        """Test that unknown-provider error response has correct format"""
        # NOTE: Previously this test asserted a 'success' path but the webhook
        # endpoint now rejects unregistered providers. We assert the error
        # envelope shape for the unregistered-provider path.
        client = Client()
        url = reverse("shipping_provider_webhook", kwargs={"provider_key": "test"})

        response = client.post(
            url, data=json.dumps({"test": "data"}), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        data = response.json()

        # Check required fields in the error envelope
        self.assertIn("status", data)
        self.assertIn("message", data)

        # Check values
        self.assertEqual(data["status"], "error")

    @patch("shipping.webhooks.process_webhook.delay")
    def test_error_response_format(self, mock_task):
        """Test that error response has correct format"""
        mock_task.side_effect = Exception("Error")

        client = Client()
        url = reverse("shipping_provider_webhook", kwargs={"provider_key": "test"})

        response = client.post(
            url, data=json.dumps({"test": "data"}), content_type="application/json"
        )

        # Unknown provider returns 400 with error envelope
        self.assertEqual(response.status_code, 400)
        data = response.json()

        self.assertEqual(data["status"], "error")
        self.assertIn("message", data)
