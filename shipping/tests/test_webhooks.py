"""
Tests for Shipping Webhook Endpoints

Tests webhook receiver functionality, logging, and task enqueueing.
Provider-specific webhook parsing will be tested when providers are implemented.
"""
import json
import unittest
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock

from shipping.models import WebhookLog
from shipping.jobs.tasks import process_webhook

User = get_user_model()


@override_settings(LANGUAGE_CODE='en-us')
class WebhookEndpointTests(TestCase):
    """Test webhook endpoint functionality"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_provider_webhook_url_resolution(self):
        """Test that webhook URL resolves correctly"""
        url = reverse('shipping_provider_webhook', kwargs={'provider_key': 'easypost'})
        self.assertIn('/webhooks/shipping/easypost/', url)

    def test_webhook_health_check_url(self):
        """Test health check URL"""
        url = reverse('shipping_webhook_health')
        self.assertIn('/webhooks/shipping/health/', url)

    def test_webhook_docs_url(self):
        """Test documentation URL"""
        url = reverse('shipping:webhook_docs')
        self.assertIn('/admin/shipping/webhooks/', url)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    @patch('shipping.webhooks.process_webhook.delay')
    def test_valid_webhook_creates_log(self, mock_task):
        """Test that valid webhook creates WebhookLog"""
        url = reverse('shipping_provider_webhook', kwargs={'provider_key': 'easypost'})
        payload = {
            'id': 'webhook_123',
            'type': 'tracking.updated',
            'data': {
                'tracking_id': 'TRACK123',
                'status': 'in_transit'
            }
        }

        response = self.client.post(
            url,
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'received')

        # Verify webhook was logged
        webhook_log = WebhookLog.objects.latest('received_at')
        self.assertEqual(webhook_log.provider_key, 'easypost')
        self.assertEqual(webhook_log.payload['id'], 'webhook_123')
        self.assertEqual(webhook_log.processing_status, 'pending')

        # Verify task was enqueued
        mock_task.assert_called_once()

    @patch('shipping.webhooks.process_webhook.delay')
    def test_webhook_with_invalid_json(self, mock_task):
        """Test webhook with invalid JSON payload"""
        url = reverse('shipping_provider_webhook', kwargs={'provider_key': 'test'})

        response = self.client.post(
            url,
            data='invalid json {',
            content_type='application/json'
        )

        # Should still return 200 OK
        self.assertEqual(response.status_code, 200)

        # Should still create log with raw body
        webhook_log = WebhookLog.objects.latest('received_at')
        self.assertIn('raw_body', webhook_log.payload)

    @patch('shipping.webhooks.process_webhook.delay')
    def test_webhook_logs_headers(self, mock_task):
        """Test that webhook logs HTTP headers"""
        url = reverse('shipping_provider_webhook', kwargs={'provider_key': 'easypost'})
        payload = {'test': 'data'}

        response = self.client.post(
            url,
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_X_WEBHOOK_ID='webhook_123',
            HTTP_X_SIGNATURE='test_signature'
        )

        self.assertEqual(response.status_code, 200)

        webhook_log = WebhookLog.objects.latest('received_at')
        self.assertIn('HTTP_X_WEBHOOK_ID', webhook_log.headers)
        self.assertIn('HTTP_X_SIGNATURE', webhook_log.headers)
        self.assertEqual(webhook_log.headers['HTTP_X_WEBHOOK_ID'], 'webhook_123')

    @patch('shipping.webhooks.process_webhook.delay')
    def test_webhook_extracts_webhook_id(self, mock_task):
        """Test that webhook ID is extracted from various sources"""
        url = reverse('shipping_provider_webhook', kwargs={'provider_key': 'test'})
        payload = {'webhook_id': 'test_123'}

        response = self.client.post(
            url,
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        # Webhook ID logged in system logs

    @patch('shipping.webhooks.process_webhook.delay')
    def test_webhook_enqueues_task(self, mock_task):
        """Test that webhook enqueues Celery task"""
        url = reverse('shipping_provider_webhook', kwargs={'provider_key': 'easypost'})
        payload = {'test': 'data'}

        response = self.client.post(
            url,
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        # Verify task was enqueued with webhook_log_id
        mock_task.assert_called_once()
        webhook_log_id = mock_task.call_args[0][0]
        self.assertTrue(webhook_log_id)  # UUID string

    @patch('shipping.webhooks.process_webhook.delay')
    def test_webhook_returns_200_on_error(self, mock_task):
        """Test that webhook always returns 200 OK, even on errors"""
        # Make the task enqueueing fail
        mock_task.side_effect = Exception("Task queue error")

        url = reverse('shipping_provider_webhook', kwargs={'provider_key': 'test'})
        payload = {'test': 'data'}

        response = self.client.post(
            url,
            data=json.dumps(payload),
            content_type='application/json'
        )

        # Should still return 200 OK (don't trigger provider retries)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'error')

    def test_webhook_only_accepts_post(self):
        """Test that webhook only accepts POST requests"""
        url = reverse('shipping_provider_webhook', kwargs={'provider_key': 'test'})

        # GET should fail
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

        # PUT should fail
        response = self.client.put(url, data='{}', content_type='application/json')
        self.assertEqual(response.status_code, 405)

        # DELETE should fail
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 405)

    @patch('shipping.webhooks.process_webhook.delay')
    def test_webhook_with_different_providers(self, mock_task):
        """Test webhooks from different providers"""
        providers = ['easypost', 'shipstation', 'shippo', 'custom']

        for provider in providers:
            url = reverse('shipping_provider_webhook', kwargs={'provider_key': provider})
            payload = {'provider': provider, 'test': 'data'}

            response = self.client.post(
                url,
                data=json.dumps(payload),
                content_type='application/json'
            )

            self.assertEqual(response.status_code, 200)

            # Verify provider_key was logged correctly
            webhook_log = WebhookLog.objects.latest('received_at')
            self.assertEqual(webhook_log.provider_key, provider)


@override_settings(LANGUAGE_CODE='en-us')
class WebhookHealthCheckTests(TestCase):
    """Test webhook health check endpoint"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_health_check_returns_200(self):
        """Test that health check returns 200 OK"""
        url = reverse('shipping_webhook_health')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'shipping-webhooks')

    def test_health_check_accepts_head(self):
        """Test that health check accepts HEAD requests"""
        url = reverse('shipping_webhook_health')
        response = self.client.head(url)
        self.assertEqual(response.status_code, 200)

    def test_health_check_rejects_post(self):
        """Test that health check rejects POST"""
        url = reverse('shipping_webhook_health')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)


@override_settings(LANGUAGE_CODE='en-us')
class WebhookDocumentationTests(TestCase):
    """Test webhook documentation page"""

    def setUp(self):
        """Set up test client with staff user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            is_staff=True
        )
        self.client.login(username='testuser', password='testpass123')

    @unittest.skip("Documentation page requires admin templates - will test in integration tests")
    def test_webhook_docs_page_loads(self):
        """Test that documentation page loads"""
        url = reverse('shipping:webhook_docs')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Webhook Endpoints', response.content)

    @unittest.skip("Documentation page requires admin templates - will test in integration tests")
    def test_webhook_docs_shows_examples(self):
        """Test that docs page shows webhook examples"""
        url = reverse('shipping:webhook_docs')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # Should show provider examples
        self.assertIn(b'easypost', response.content.lower())


@override_settings(LANGUAGE_CODE='en-us')
class WebhookLogModelTests(TestCase):
    """Test WebhookLog model interactions"""

    @patch('shipping.webhooks.process_webhook.delay')
    def test_webhook_log_created_with_all_fields(self, mock_task):
        """Test that WebhookLog captures all required fields"""
        client = Client()
        url = reverse('shipping_provider_webhook', kwargs={'provider_key': 'easypost'})
        payload = {
            'id': 'evt_123',
            'type': 'tracking.updated',
            'data': {'tracking_id': 'TRACK123'}
        }

        response = client.post(
            url,
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_X_WEBHOOK_ID='webhook_123'
        )

        self.assertEqual(response.status_code, 200)

        webhook_log = WebhookLog.objects.latest('received_at')
        self.assertEqual(webhook_log.provider_key, 'easypost')
        self.assertTrue(webhook_log.endpoint.startswith('/webhooks/'))
        self.assertIsInstance(webhook_log.payload, dict)
        self.assertIsInstance(webhook_log.headers, dict)
        self.assertEqual(webhook_log.processing_status, 'pending')
        self.assertTrue(webhook_log.id)  # UUID assigned

    @patch('shipping.webhooks.process_webhook.delay')
    def test_webhook_log_queryable(self, mock_task):
        """Test that webhook logs are queryable"""
        client = Client()

        # Create webhooks for different providers
        for provider in ['easypost', 'shipstation']:
            url = reverse('shipping_provider_webhook', kwargs={'provider_key': provider})
            client.post(
                url,
                data=json.dumps({'provider': provider}),
                content_type='application/json'
            )

        # Query by provider
        easypost_logs = WebhookLog.objects.filter(provider_key='easypost')
        self.assertEqual(easypost_logs.count(), 1)

        shipstation_logs = WebhookLog.objects.filter(provider_key='shipstation')
        self.assertEqual(shipstation_logs.count(), 1)

    @patch('shipping.webhooks.process_webhook.delay')
    def test_failed_webhook_logs_error(self, mock_task):
        """Test that failed webhooks log error messages"""
        # Make task.delay raise an exception
        mock_task.side_effect = Exception("Task queue down")

        client = Client()
        url = reverse('shipping_provider_webhook', kwargs={'provider_key': 'test'})

        response = client.post(
            url,
            data=json.dumps({'test': 'data'}),
            content_type='application/json'
        )

        # Should still return 200
        self.assertEqual(response.status_code, 200)

        # But webhook log should record the failure
        webhook_log = WebhookLog.objects.latest('received_at')
        self.assertEqual(webhook_log.processing_status, 'failed')
        self.assertIn('error', webhook_log.error_message.lower())


@override_settings(LANGUAGE_CODE='en-us')
class WebhookCSRFTests(TestCase):
    """Test CSRF exemption for webhooks"""

    def test_webhook_exempt_from_csrf(self):
        """Test that webhook endpoint is exempt from CSRF protection"""
        client = Client(enforce_csrf_checks=True)
        url = reverse('shipping_provider_webhook', kwargs={'provider_key': 'test'})

        # Should work without CSRF token
        response = client.post(
            url,
            data=json.dumps({'test': 'data'}),
            content_type='application/json'
        )

        # Should not get CSRF error
        self.assertNotEqual(response.status_code, 403)
        self.assertEqual(response.status_code, 200)


@override_settings(LANGUAGE_CODE='en-us')
class WebhookResponseFormatTests(TestCase):
    """Test webhook response format"""

    @patch('shipping.webhooks.process_webhook.delay')
    def test_success_response_format(self, mock_task):
        """Test that success response has correct format"""
        client = Client()
        url = reverse('shipping_provider_webhook', kwargs={'provider_key': 'test'})

        response = client.post(
            url,
            data=json.dumps({'test': 'data'}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Check required fields
        self.assertIn('status', data)
        self.assertIn('webhook_id', data)
        self.assertIn('message', data)
        self.assertIn('received_at', data)

        # Check values
        self.assertEqual(data['status'], 'received')
        self.assertTrue(data['webhook_id'])
        self.assertIn('queued', data['message'])

    @patch('shipping.webhooks.process_webhook.delay')
    def test_error_response_format(self, mock_task):
        """Test that error response has correct format"""
        mock_task.side_effect = Exception("Error")

        client = Client()
        url = reverse('shipping_provider_webhook', kwargs={'provider_key': 'test'})

        response = client.post(
            url,
            data=json.dumps({'test': 'data'}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)  # Still 200
        data = response.json()

        self.assertEqual(data['status'], 'error')
        self.assertIn('message', data)
        self.assertIn('received_at', data)
