"""
Tests for shipping app models
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from djmoney.money import Money

from component_updates.models import ComponentRegistry
from orders.models import Order
from shipping.models import (
    CarrierPreset,
    ProviderAccount,
    Shipment,
    TrackingEvent,
    WebhookLog,
)

User = get_user_model()


class CarrierPresetModelTest(TestCase):
    """Test CarrierPreset model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_create_carrier_preset(self):
        """Test creating a carrier preset"""
        carrier = CarrierPreset.objects.create(
            name="Test Carrier",
            slug="test-carrier",
            tracking_url_template="https://test.com/track/{tracking_number}",
            description="Test carrier description",
            is_active=True,
            is_system=False,
            created_by=self.user,
        )

        self.assertEqual(carrier.name, "Test Carrier")
        self.assertEqual(carrier.slug, "test-carrier")
        self.assertTrue(carrier.is_active)
        self.assertFalse(carrier.is_system)
        self.assertFalse(carrier.is_default)

    def test_carrier_preset_str(self):
        """Test __str__ method"""
        carrier = CarrierPreset.objects.create(
            name="Test String Carrier",
            slug="test-string-carrier",
        )
        self.assertEqual(str(carrier), "Test String Carrier")

    def test_only_one_default_carrier(self):
        """Test that only one carrier can be default"""
        carrier1 = CarrierPreset.objects.create(
            name="Carrier 1",
            slug="carrier-1",
            is_default=True,
        )
        carrier2 = CarrierPreset.objects.create(
            name="Carrier 2",
            slug="carrier-2",
            is_default=True,
        )

        # Refresh from DB
        carrier1.refresh_from_db()
        carrier2.refresh_from_db()

        # Only carrier2 should be default now
        self.assertFalse(carrier1.is_default)
        self.assertTrue(carrier2.is_default)

    def test_system_carrier_preset_is_system_flag(self):
        """Test that carriers can be marked as system carriers"""
        # No data migration currently seeds system carriers, so we validate
        # the is_system flag behaves correctly on directly-created presets.
        system_preset = CarrierPreset.objects.create(
            slug="test-system-carrier",
            name="Test System Carrier",
            tracking_url_template="https://example.com/track?id={tracking_number}",
            is_system=True,
        )
        self.assertTrue(system_preset.is_system)

        user_preset = CarrierPreset.objects.create(
            slug="test-user-carrier",
            name="Test User Carrier",
            tracking_url_template="https://example.com/track?id={tracking_number}",
            is_system=False,
        )
        self.assertFalse(user_preset.is_system)


class ProviderAccountModelTest(TestCase):
    """Test ProviderAccount model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        # Create a test component (shipping provider)
        self.component = ComponentRegistry.objects.create(
            component_type="shipping_provider",
            slug="test-provider",
            name="Test Provider",
            current_version="1.0.0",
        )

    def test_create_provider_account(self):
        """Test creating a provider account"""
        provider = ProviderAccount.objects.create(
            component=self.component,
            user=self.user,
            display_name="My Test Provider",
            credentials_encrypted={"api_key": "encrypted_value"},
            settings={"region": "us-west"},
            is_active=True,
        )

        self.assertEqual(provider.display_name, "My Test Provider")
        self.assertEqual(provider.user, self.user)
        self.assertEqual(provider.component, self.component)
        self.assertTrue(provider.is_active)
        self.assertEqual(provider.connection_status, "unknown")

    def test_provider_account_str(self):
        """Test __str__ method"""
        provider = ProviderAccount.objects.create(
            component=self.component,
            user=self.user,
            display_name="My Easyship",
        )
        self.assertIn("testuser", str(provider))
        self.assertIn("My Easyship", str(provider))

    def test_only_one_default_provider_per_user(self):
        """Test that only one provider can be default per user"""
        component2 = ComponentRegistry.objects.create(
            component_type="shipping_provider",
            slug="another-provider",
            name="Another Provider",
            current_version="1.0.0",
        )

        provider1 = ProviderAccount.objects.create(
            component=self.component,
            user=self.user,
            is_default=True,
        )
        provider2 = ProviderAccount.objects.create(
            component=component2,
            user=self.user,
            is_default=True,
        )

        # Refresh from DB
        provider1.refresh_from_db()
        provider2.refresh_from_db()

        # Only provider2 should be default now
        self.assertFalse(provider1.is_default)
        self.assertTrue(provider2.is_default)


class ShipmentModelTest(TestCase):
    """Test Shipment model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        # Create a test order with all required fields
        self.order = Order.objects.create(
            user=self.user,
            order_number="TEST-001",
            email="customer@example.com",
            status="processing",
            shipping_name="Test Customer",
            shipping_address1="123 Test St",
            shipping_city="Test City",
            shipping_postal_code="12345",
            shipping_country="US",
            subtotal=Money("100.00", "USD"),
            total_amount=Money("100.00", "USD"),
        )

        # Create a carrier preset
        self.carrier = CarrierPreset.objects.create(
            name="Test Carrier",
            slug="test-carrier",
            tracking_url_template="https://test.com/track/{tracking_number}",
        )

    def test_create_manual_shipment(self):
        """Test creating a manual shipment"""
        shipment = Shipment.objects.create(
            order=self.order,
            user=self.user,
            carrier_preset=self.carrier,
            origin_country="US",
            dest_country="CA",
            packages=[{"weight_g": 1000, "length_cm": 10, "width_cm": 10, "height_cm": 10}],
            tracking_id="1234567890",
            status="in_transit",
        )

        self.assertEqual(shipment.order, self.order)
        self.assertEqual(shipment.carrier_preset, self.carrier)
        self.assertEqual(shipment.tracking_id, "1234567890")
        self.assertEqual(shipment.status, "in_transit")
        self.assertTrue(shipment.is_manual)
        self.assertFalse(shipment.is_api)

    def test_shipment_str(self):
        """Test __str__ method"""
        shipment = Shipment.objects.create(
            order=self.order,
            user=self.user,
            carrier_preset=self.carrier,
            origin_country="US",
            dest_country="CA",
        )
        self.assertIn(self.order.order_number, str(shipment))
        self.assertIn(self.carrier.name, str(shipment))

    def test_get_tracking_url(self):
        """Test tracking URL generation"""
        shipment = Shipment.objects.create(
            order=self.order,
            user=self.user,
            carrier_preset=self.carrier,
            origin_country="US",
            dest_country="CA",
            tracking_id="ABC123",
        )

        tracking_url = shipment.get_tracking_url()
        self.assertEqual(tracking_url, "https://test.com/track/ABC123")

    def test_get_tracking_url_no_tracking_id(self):
        """Test tracking URL returns None without tracking ID"""
        shipment = Shipment.objects.create(
            order=self.order,
            user=self.user,
            carrier_preset=self.carrier,
            origin_country="US",
            dest_country="CA",
        )

        tracking_url = shipment.get_tracking_url()
        self.assertIsNone(tracking_url)

    def test_shipment_money_fields(self):
        """Test MoneyField usage for costs"""
        shipment = Shipment.objects.create(
            order=self.order,
            user=self.user,
            carrier_preset=self.carrier,
            origin_country="US",
            dest_country="CA",
            shipping_cost=Money("15.99", "USD"),
            carrier_cost=Money("12.50", "USD"),
        )

        self.assertEqual(str(shipment.shipping_cost.amount), "15.99")
        self.assertEqual(str(shipment.shipping_cost.currency), "USD")
        self.assertEqual(str(shipment.carrier_cost.amount), "12.50")


class TrackingEventModelTest(TestCase):
    """Test TrackingEvent model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.order = Order.objects.create(
            user=self.user,
            order_number="TEST-EVENT-001",
            email="customer@example.com",
            status="processing",
            shipping_name="Test Customer",
            shipping_address1="123 Test St",
            shipping_city="Test City",
            shipping_postal_code="12345",
            shipping_country="US",
            subtotal=Money("100.00", "USD"),
            total_amount=Money("100.00", "USD"),
        )

        self.carrier = CarrierPreset.objects.create(
            name="Test Carrier",
            slug="test-carrier",
        )

        self.shipment = Shipment.objects.create(
            order=self.order,
            user=self.user,
            carrier_preset=self.carrier,
            origin_country="US",
            dest_country="CA",
        )

    def test_create_tracking_event(self):
        """Test creating a tracking event"""
        event = TrackingEvent.objects.create(
            shipment=self.shipment,
            status="in_transit",
            description="Package in transit",
            location="New York, NY",
            occurred_at=timezone.now(),
            raw={"carrier_data": "raw_data_here"},
        )

        self.assertEqual(event.shipment, self.shipment)
        self.assertEqual(event.status, "in_transit")
        self.assertEqual(event.location, "New York, NY")
        self.assertIn("carrier_data", event.raw)

    def test_tracking_event_str(self):
        """Test __str__ method"""
        event = TrackingEvent.objects.create(
            shipment=self.shipment,
            status="delivered",
            occurred_at=timezone.now(),
        )
        # Should include status display and timestamp
        self.assertIn("Delivered", str(event))


class WebhookLogModelTest(TestCase):
    """Test WebhookLog model"""

    def test_create_webhook_log(self):
        """Test creating a webhook log"""
        log = WebhookLog.objects.create(
            provider_key="test-provider",
            endpoint="/webhooks/tracking",
            payload={"event": "shipment_delivered", "tracking_id": "ABC123"},
            headers={"Content-Type": "application/json"},
            status_code=200,
            processing_status="processed",
        )

        self.assertEqual(log.provider_key, "test-provider")
        self.assertEqual(log.processing_status, "processed")
        self.assertEqual(log.status_code, 200)
        self.assertIn("event", log.payload)

    def test_webhook_log_str(self):
        """Test __str__ method"""
        log = WebhookLog.objects.create(
            provider_key="easyship",
            endpoint="/webhooks/tracking",
            payload={},
            headers={},
        )
        self.assertIn("easyship", str(log))
        self.assertIn("webhook", str(log))

    def test_webhook_log_default_status(self):
        """Test default processing status is pending"""
        log = WebhookLog.objects.create(
            provider_key="test-provider",
            endpoint="/test",
            payload={},
            headers={},
        )
        self.assertEqual(log.processing_status, "pending")
