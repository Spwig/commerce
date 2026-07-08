"""
Tests for Shipping Celery Tasks

Tests the task infrastructure, retry logic, and basic functionality.
Provider API integration will be tested when providers are implemented.
"""
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from unittest.mock import patch, MagicMock
import uuid

from shipping.models import Shipment, TrackingEvent, WebhookLog, CarrierPreset, ProviderAccount
from shipping.jobs.tasks import fetch_rates, buy_label, poll_tracking, process_webhook
from shipping.jobs.utils import (
    validate_shipment_data,
    format_rate_response,
    hash_tracking_event,
    should_poll_shipment,
    get_retry_delay,
    sanitize_webhook_payload,
    parse_tracking_status,
)
from orders.models import Order
from component_updates.models import ComponentRegistry

User = get_user_model()


class ShipmentDataValidationTests(TestCase):
    """Test shipment data validation utilities"""

    def test_valid_shipment_data(self):
        """Test validation with valid data"""
        data = {
            'origin_country': 'US',
            'dest_country': 'GB',
            'weight': '2.5',
            'weight_unit': 'kg'
        }
        is_valid, error = validate_shipment_data(data)
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_missing_required_fields(self):
        """Test validation with missing fields"""
        data = {'origin_country': 'US'}
        is_valid, error = validate_shipment_data(data)
        self.assertFalse(is_valid)
        self.assertIn('dest_country', error)

    def test_invalid_country_code(self):
        """Test validation with invalid country code"""
        data = {
            'origin_country': 'USA',  # Should be 2 chars
            'dest_country': 'GB',
        }
        is_valid, error = validate_shipment_data(data)
        self.assertFalse(is_valid)
        self.assertIn('origin_country', error)

    def test_invalid_weight(self):
        """Test validation with invalid weight"""
        data = {
            'origin_country': 'US',
            'dest_country': 'GB',
            'weight': '-5'
        }
        is_valid, error = validate_shipment_data(data)
        self.assertFalse(is_valid)
        self.assertIn('weight', error)


class TrackingEventUtilsTests(TestCase):
    """Test tracking event utilities"""

    def test_hash_tracking_event(self):
        """Test event hash generation"""
        event1 = {
            'status': 'in_transit',
            'description': 'Package in transit',
            'location': 'New York, NY',
            'occurred_at': '2025-10-20T10:00:00Z'
        }
        event2 = {
            'status': 'in_transit',
            'description': 'Package in transit',
            'location': 'New York, NY',
            'occurred_at': '2025-10-20T10:00:00Z'
        }
        event3 = {
            'status': 'delivered',
            'description': 'Package delivered',
            'location': 'London, UK',
            'occurred_at': '2025-10-21T14:00:00Z'
        }

        hash1 = hash_tracking_event(event1)
        hash2 = hash_tracking_event(event2)
        hash3 = hash_tracking_event(event3)

        # Same events should have same hash
        self.assertEqual(hash1, hash2)
        # Different events should have different hash
        self.assertNotEqual(hash1, hash3)

    def test_parse_tracking_status(self):
        """Test status parsing"""
        self.assertEqual(parse_tracking_status('Delivered', 'test'), 'delivered')
        self.assertEqual(parse_tracking_status('Out for delivery', 'test'), 'out_for_delivery')
        self.assertEqual(parse_tracking_status('IN TRANSIT', 'test'), 'in_transit')
        self.assertEqual(parse_tracking_status('Exception occurred', 'test'), 'exception')
        self.assertEqual(parse_tracking_status('Package returned', 'test'), 'returned')


class RetryLogicTests(TestCase):
    """Test retry and backoff logic"""

    def test_exponential_backoff(self):
        """Test exponential backoff calculation"""
        # With base_delay=60
        self.assertEqual(get_retry_delay(0, base_delay=60), 60)   # 60 * 2^0
        self.assertEqual(get_retry_delay(1, base_delay=60), 120)  # 60 * 2^1
        self.assertEqual(get_retry_delay(2, base_delay=60), 240)  # 60 * 2^2
        self.assertEqual(get_retry_delay(3, base_delay=60), 480)  # 60 * 2^3

    def test_max_delay_cap(self):
        """Test that delay is capped at max_delay"""
        delay = get_retry_delay(10, base_delay=60, max_delay=600)
        self.assertEqual(delay, 600)


class WebhookUtilsTests(TestCase):
    """Test webhook utilities"""

    def test_sanitize_webhook_payload(self):
        """Test webhook payload sanitization"""
        payload = {
            'tracking_id': '1234567890',
            'api_key': 'secret_key_123',
            'status': 'delivered',
            'nested': {
                'password': 'secret_pass',
                'data': 'safe_value'
            }
        }

        sanitized = sanitize_webhook_payload(payload, 'test')

        self.assertEqual(sanitized['tracking_id'], '1234567890')
        self.assertEqual(sanitized['api_key'], '*** REDACTED ***')
        self.assertEqual(sanitized['status'], 'delivered')
        self.assertEqual(sanitized['nested']['password'], '*** REDACTED ***')
        self.assertEqual(sanitized['nested']['data'], 'safe_value')


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class FetchRatesTaskTests(TestCase):
    """Test fetch_rates Celery task"""

    def test_fetch_rates_task_structure(self):
        """Test that fetch_rates task is properly configured"""
        self.assertEqual(fetch_rates.name, 'shipping.fetch_rates')
        self.assertEqual(fetch_rates.max_retries, 3)
        self.assertTrue(fetch_rates.autoretry_for)

    def test_fetch_rates_basic_execution(self):
        """Test basic fetch_rates execution (skeleton)"""
        shipment_data = {
            'origin_country': 'US',
            'dest_country': 'GB',
            'weight': '2.5'
        }

        result = fetch_rates.delay(shipment_data).get()

        self.assertTrue(result['success'])
        self.assertIn('rates', result)
        self.assertIn('errors', result)
        self.assertIn('fetched_at', result)


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class BuyLabelTaskTests(TestCase):
    """Test buy_label Celery task"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.carrier = CarrierPreset.objects.get_or_create(
            slug='test-carrier',
            defaults={'name': 'Test Carrier'}
        )[0]
        self.order = Order.objects.create(
            user=self.user,
            order_number='TEST-001',
            subtotal=Decimal('100.00'),
            total_amount=Decimal('100.00'),
            status='processing'
        )
        self.shipment = Shipment.objects.create(
            order=self.order,
            user=self.user,
            carrier_preset=self.carrier,
            origin_country='US',
            dest_country='GB',
            status='created'
        )

    def test_buy_label_task_structure(self):
        """Test that buy_label task is properly configured"""
        self.assertEqual(buy_label.name, 'shipping.buy_label')
        self.assertEqual(buy_label.max_retries, 3)

    def test_buy_label_with_valid_shipment(self):
        """Test buy_label with valid shipment"""
        result = buy_label.delay(str(self.shipment.id)).get()

        self.assertFalse(result['success'])  # Skeleton returns False
        self.assertEqual(result['shipment_id'], str(self.shipment.id))
        self.assertIn('error', result)
        self.assertIn('skeleton', result['error'].lower())

    def test_buy_label_with_invalid_shipment(self):
        """Test buy_label with non-existent shipment"""
        fake_id = str(uuid.uuid4())
        result = buy_label.delay(fake_id).get()

        self.assertFalse(result['success'])
        self.assertIn('not found', result['error'].lower())


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class PollTrackingTaskTests(TestCase):
    """Test poll_tracking Celery task"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(username='testuser', password='testpass123')

        # Create component registry for provider
        self.component = ComponentRegistry.objects.create(
            component_type='shipping_provider',
            slug='test-provider',
            name='Test Provider',
            current_version='1.0.0',
        )

        # Create provider account
        self.provider = ProviderAccount.objects.create(
            user=self.user,
            component=self.component,
            credentials_encrypted={'api_key': 'test'},
            is_active=True
        )

        self.order = Order.objects.create(
            user=self.user,
            order_number='TEST-002',
            subtotal=Decimal('100.00'),
            total_amount=Decimal('100.00'),
            status='processing'
        )

        self.shipment = Shipment.objects.create(
            order=self.order,
            user=self.user,
            provider_account=self.provider,
            tracking_id='TRACK123',
            origin_country='US',
            dest_country='GB',
            status='in_transit'
        )

    def test_poll_tracking_task_structure(self):
        """Test that poll_tracking task is properly configured"""
        self.assertEqual(poll_tracking.name, 'shipping.poll_tracking')
        self.assertEqual(poll_tracking.max_retries, 3)

    def test_poll_tracking_single_shipment(self):
        """Test polling a single shipment"""
        result = poll_tracking.delay(str(self.shipment.id)).get()

        self.assertIn('shipments_polled', result)
        self.assertIn('shipments_updated', result)
        self.assertIn('new_events', result)
        self.assertIn('errors', result)

    def test_poll_tracking_batch(self):
        """Test batch polling"""
        result = poll_tracking.delay(batch_size=100).get()

        self.assertIn('shipments_polled', result)
        self.assertTrue(result['success'])

    def test_should_poll_shipment_logic(self):
        """Test should_poll_shipment utility"""
        # Should poll: in_transit with provider and tracking
        self.assertTrue(should_poll_shipment(self.shipment))

        # Should not poll: delivered
        self.shipment.status = 'delivered'
        self.assertFalse(should_poll_shipment(self.shipment))

        # Should not poll: no provider (manual)
        self.shipment.status = 'in_transit'
        self.shipment.provider_account = None
        self.assertFalse(should_poll_shipment(self.shipment))


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class ProcessWebhookTaskTests(TestCase):
    """Test process_webhook Celery task"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(username='testuser', password='testpass123')

        self.component = ComponentRegistry.objects.create(
            component_type='shipping_provider',
            slug='test-provider',
            name='Test Provider',
            current_version='1.0.0',
        )

        self.provider = ProviderAccount.objects.create(
            user=self.user,
            component=self.component,
            credentials_encrypted={'api_key': 'test'},
            is_active=True
        )

        self.webhook_log = WebhookLog.objects.create(
            provider_key='test-provider',
            endpoint='/webhooks/test-provider',
            payload={'tracking_id': 'TRACK123'},
            headers={'Content-Type': 'application/json'},
            processing_status='pending'
        )

    def test_process_webhook_task_structure(self):
        """Test that process_webhook task is properly configured"""
        self.assertEqual(process_webhook.name, 'shipping.process_webhook')
        self.assertEqual(process_webhook.max_retries, 5)

    def test_process_webhook_with_valid_log(self):
        """Test processing valid webhook log"""
        result = process_webhook.delay(str(self.webhook_log.id)).get()

        self.assertFalse(result['success'])  # Skeleton returns False
        self.assertEqual(result['webhook_log_id'], str(self.webhook_log.id))

        # Verify webhook log status was updated
        self.webhook_log.refresh_from_db()
        self.assertEqual(self.webhook_log.processing_status, 'pending')  # Skeleton sets to pending

    def test_process_webhook_with_invalid_log(self):
        """Test processing non-existent webhook log"""
        fake_id = str(uuid.uuid4())
        result = process_webhook.delay(fake_id).get()

        self.assertFalse(result['success'])
        self.assertIn('not found', result['error'].lower())


class TaskRegistrationTests(TestCase):
    """Test that all tasks are properly registered"""

    def test_all_tasks_have_names(self):
        """Test that all tasks have correct names"""
        self.assertEqual(fetch_rates.name, 'shipping.fetch_rates')
        self.assertEqual(buy_label.name, 'shipping.buy_label')
        self.assertEqual(poll_tracking.name, 'shipping.poll_tracking')
        self.assertEqual(process_webhook.name, 'shipping.process_webhook')

    def test_all_tasks_have_retry_config(self):
        """Test that all tasks have retry configuration"""
        tasks = [fetch_rates, buy_label, poll_tracking, process_webhook]

        for task in tasks:
            self.assertIsNotNone(task.max_retries)
            self.assertGreater(task.max_retries, 0)
            self.assertTrue(task.autoretry_for)

    def test_tasks_are_importable(self):
        """Test that tasks can be imported from jobs package"""
        from shipping.jobs import (
            fetch_rates as fr,
            buy_label as bl,
            poll_tracking as pt,
            process_webhook as pw
        )

        self.assertEqual(fr.name, 'shipping.fetch_rates')
        self.assertEqual(bl.name, 'shipping.buy_label')
        self.assertEqual(pt.name, 'shipping.poll_tracking')
        self.assertEqual(pw.name, 'shipping.process_webhook')
