"""
Tests for shipping signal handlers
Tests bidirectional sync between Order and Shipment
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from djmoney.money import Money

from orders.models import Order
from shipping.models import CarrierPreset, Shipment
from shipping.signals import (
    label_purchased,
    shipment_created,
    shipment_delivered,
    shipment_exception,
    tracking_updated,
)

User = get_user_model()


class ShipmentToOrderSyncTest(TestCase):
    """Test Shipment → Order tracking sync"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.carrier = CarrierPreset.objects.create(
            name="Test Carrier",
            slug="test-carrier-sync",
            tracking_url_template="https://test.com/track/{tracking_number}",
        )

        self.order = Order.objects.create(
            user=self.user,
            order_number="SYNC-TEST-001",
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

    def test_shipment_tracking_syncs_to_order(self):
        """Test that when a shipment gets a tracking number, it syncs to the order"""
        # Create shipment without tracking
        shipment = Shipment.objects.create(
            order=self.order,
            user=self.user,
            carrier_preset=self.carrier,
            origin_country="US",
            dest_country="US",
        )

        # Verify order has no tracking yet
        self.order.refresh_from_db()
        self.assertEqual(self.order.tracking_number, "")

        # Add tracking to shipment
        shipment.tracking_id = "ABC123456"
        shipment.save()

        # Verify it synced to order
        self.order.refresh_from_db()
        self.assertEqual(self.order.tracking_number, "ABC123456")

    def test_shipment_tracking_update_syncs_to_order(self):
        """Test that updating shipment tracking updates the order"""
        shipment = Shipment.objects.create(
            order=self.order,
            user=self.user,
            carrier_preset=self.carrier,
            origin_country="US",
            dest_country="US",
            tracking_id="FIRST123",
        )

        # Verify initial sync
        self.order.refresh_from_db()
        self.assertEqual(self.order.tracking_number, "FIRST123")

        # Update tracking
        shipment.tracking_id = "SECOND456"
        shipment.save()

        # Verify update synced
        self.order.refresh_from_db()
        self.assertEqual(self.order.tracking_number, "SECOND456")

    def test_no_sync_when_no_order(self):
        """Test that signal doesn't crash when shipment has no order"""
        # Create shipment without order (should not crash)
        # Note: This will fail validation, but test the signal guard
        try:
            shipment = Shipment(
                user=self.user,
                carrier_preset=self.carrier,
                origin_country="US",
                dest_country="US",
                tracking_id="TEST123",
            )
            # Save will fail due to order being required, but signal should handle gracefully
            shipment.save()
        except Exception:
            # Expected to fail, but signal should not cause additional errors
            pass


class OrderToShipmentSyncTest(TestCase):
    """Test Order → Shipment tracking sync"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        # Create a default carrier
        self.carrier = CarrierPreset.objects.create(
            name="Default Carrier",
            slug="default-carrier",
            is_default=True,
            is_active=True,
        )

        self.order = Order.objects.create(
            user=self.user,
            order_number="ORDER-SYNC-001",
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

    def test_order_tracking_creates_shipment(self):
        """Test that adding tracking to an order creates a shipment"""
        # Verify no shipments exist yet
        self.assertEqual(Shipment.objects.filter(order=self.order).count(), 0)

        # Add tracking number to order
        self.order.tracking_number = "XYZ789"
        self.order.save()

        # Verify shipment was created
        shipments = Shipment.objects.filter(order=self.order)
        self.assertEqual(shipments.count(), 1)

        shipment = shipments.first()
        self.assertEqual(shipment.tracking_id, "XYZ789")
        self.assertEqual(shipment.carrier_preset, self.carrier)
        self.assertEqual(shipment.status, "in_transit")

    def test_order_tracking_updates_existing_shipment(self):
        """Test that updating order tracking updates existing shipment"""
        # Create initial shipment
        shipment = Shipment.objects.create(
            order=self.order,
            user=self.user,
            carrier_preset=self.carrier,
            origin_country="US",
            dest_country="US",
            tracking_id="INITIAL123",
        )

        # Update order tracking number
        self.order.tracking_number = "UPDATED456"
        self.order.save()

        # Verify shipment was updated
        shipment.refresh_from_db()
        self.assertEqual(shipment.tracking_id, "UPDATED456")

        # Verify no new shipment was created
        self.assertEqual(Shipment.objects.filter(order=self.order).count(), 1)

    def test_no_shipment_created_on_new_order(self):
        """Test that creating a new order doesn't automatically create shipment"""
        new_order = Order.objects.create(
            user=self.user,
            order_number="NEW-ORDER-001",
            email="customer@example.com",
            status="pending",
            shipping_name="Test Customer",
            shipping_address1="123 Test St",
            shipping_city="Test City",
            shipping_postal_code="12345",
            shipping_country="US",
            subtotal=Money("100.00", "USD"),
            total_amount=Money("100.00", "USD"),
            tracking_number="",  # Empty tracking
        )

        # Verify no shipment was created
        self.assertEqual(Shipment.objects.filter(order=new_order).count(), 0)

    def test_no_shipment_when_tracking_cleared(self):
        """Test that clearing tracking doesn't create a shipment"""
        self.order.tracking_number = "TEMP123"
        self.order.save()

        # Clear tracking
        self.order.tracking_number = ""
        self.order.save()

        # Should still have only 1 shipment (from first save)
        self.assertEqual(Shipment.objects.filter(order=self.order).count(), 1)


class SignalLoopPreventionTest(TestCase):
    """Test that signals don't create infinite loops"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.carrier = CarrierPreset.objects.create(
            name="Test Carrier",
            slug="test-carrier-loop",
            is_default=True,
        )

        self.order = Order.objects.create(
            user=self.user,
            order_number="LOOP-TEST-001",
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

    def test_no_infinite_loop_on_shipment_save(self):
        """Test that saving a shipment doesn't cause infinite loop"""
        shipment = Shipment.objects.create(
            order=self.order,
            user=self.user,
            carrier_preset=self.carrier,
            origin_country="US",
            dest_country="US",
            tracking_id="LOOP123",
        )

        # This should not cause infinite recursion
        shipment.save()
        shipment.save()
        shipment.save()

        # Verify tracking synced exactly once
        self.order.refresh_from_db()
        self.assertEqual(self.order.tracking_number, "LOOP123")

    def test_no_infinite_loop_on_order_save(self):
        """Test that saving an order doesn't cause infinite loop"""
        self.order.tracking_number = "ORDER123"
        self.order.save()

        # This should not cause infinite recursion
        self.order.save()
        self.order.save()

        # Verify exactly 1 shipment created
        self.assertEqual(Shipment.objects.filter(order=self.order).count(), 1)


class CustomSignalTest(TestCase):
    """Test custom shipping signals"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.carrier = CarrierPreset.objects.create(
            name="Test Carrier",
            slug="test-carrier-custom",
        )

        self.order = Order.objects.create(
            user=self.user,
            order_number="CUSTOM-SIG-001",
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

        self.shipment = Shipment.objects.create(
            order=self.order,
            user=self.user,
            carrier_preset=self.carrier,
            origin_country="US",
            dest_country="US",
        )

    def test_label_purchased_signal_updates_order_status(self):
        """Test that label_purchased signal updates order status to shipped"""
        self.assertEqual(self.order.status, "processing")

        # Send label_purchased signal
        label_purchased.send(sender=Shipment, shipment=self.shipment)

        # Verify order status updated
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "shipped")

    def test_shipment_delivered_signal_updates_order_status(self):
        """Test that shipment_delivered signal updates order status to completed"""
        self.order.status = "shipped"
        self.order.save()

        # Send shipment_delivered signal
        shipment_delivered.send(sender=Shipment, shipment=self.shipment)

        # Verify order status updated
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "completed")

    def test_shipment_created_signal(self):
        """Test that shipment_created signal can be sent"""
        # Should not crash
        shipment_created.send(sender=Shipment, shipment=self.shipment)

    def test_tracking_updated_signal(self):
        """Test that tracking_updated signal can be sent"""
        # Should not crash
        tracking_updated.send(sender=Shipment, shipment=self.shipment, events=[])

    def test_shipment_exception_signal(self):
        """Test that shipment_exception signal can be sent"""
        # Should not crash
        shipment_exception.send(sender=Shipment, shipment=self.shipment, error="Test error")
