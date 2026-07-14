"""
Tests for Shipping API
Tests REST API endpoints for shipping functionality
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from orders.models import Order
from shipping.models import CarrierPreset, Shipment, TrackingEvent

User = get_user_model()


class ShippingAPITestCase(TestCase):
    """Base test case with common setup"""

    def setUp(self):
        """Set up test data"""
        # Create users
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="testpass123"
        )
        self.staff_user = User.objects.create_user(
            username="staff", email="staff@example.com", password="testpass123", is_staff=True
        )

        # Create carrier preset (or get existing one)
        self.carrier, _ = CarrierPreset.objects.get_or_create(
            slug="dhl-express",
            defaults={
                "name": "DHL Express",
                "tracking_url_template": "https://dhl.com/track?id={tracking_number}",
                "is_active": True,
            },
        )

        # Create orders
        self.order1 = Order.objects.create(
            user=self.user1,
            order_number="ORD-001",
            subtotal=Decimal("100.00"),
            total_amount=Decimal("100.00"),
            status="processing",
        )
        self.order2 = Order.objects.create(
            user=self.user2,
            order_number="ORD-002",
            subtotal=Decimal("150.00"),
            total_amount=Decimal("150.00"),
            status="processing",
        )

        # Create shipments
        self.shipment1 = Shipment.objects.create(
            order=self.order1,
            user=self.user1,
            carrier_preset=self.carrier,
            tracking_id="TRACK001",
            status="in_transit",
            origin_country="US",
            dest_country="CA",
        )
        self.shipment2 = Shipment.objects.create(
            order=self.order2,
            user=self.user2,
            carrier_preset=self.carrier,
            tracking_id="TRACK002",
            status="delivered",
            origin_country="US",
            dest_country="GB",
        )

        # Create tracking events
        self.event1 = TrackingEvent.objects.create(
            shipment=self.shipment1,
            status="in_transit",
            location="New York, NY",
            description="Package in transit",
            occurred_at=timezone.now(),
        )

        # Create API client
        self.client = APIClient()


class CarrierAPITests(ShippingAPITestCase):
    """Tests for Carrier API endpoints"""

    def test_list_carriers_authenticated(self):
        """Test listing carriers as authenticated user"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/api/shipping/carriers/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that we got at least one carrier (our test carrier)
        self.assertGreaterEqual(len(response.data["results"]), 1)
        # Find our test carrier in the results
        carrier_names = [c["name"] for c in response.data["results"]]
        self.assertIn("DHL Express", carrier_names)

    def test_list_carriers_unauthenticated(self):
        """Test listing carriers without authentication"""
        response = self.client.get("/api/shipping/carriers/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_carrier(self):
        """Test retrieving a specific carrier"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f"/api/shipping/carriers/{self.carrier.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "DHL Express")
        self.assertEqual(response.data["slug"], "dhl-express")

    def test_search_carriers(self):
        """Test searching carriers"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/api/shipping/carriers/?search=DHL")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)


class ShipmentAPITests(ShippingAPITestCase):
    """Tests for Shipment API endpoints"""

    def test_list_user_shipments(self):
        """Test user can only see their own shipments"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/api/shipping/shipments/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["tracking_id"], "TRACK001")

    def test_list_staff_sees_all_shipments(self):
        """Test staff user can see all shipments"""
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get("/api/shipping/shipments/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_retrieve_own_shipment(self):
        """Test retrieving user's own shipment"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f"/api/shipping/shipments/{self.shipment1.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["tracking_id"], "TRACK001")
        self.assertEqual(response.data["status"], "in_transit")
        self.assertIsNotNone(response.data["tracking_url"])
        self.assertEqual(response.data["carrier_name"], "DHL Express")

    def test_cannot_retrieve_other_user_shipment(self):
        """Test user cannot retrieve another user's shipment"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f"/api/shipping/shipments/{self.shipment2.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_shipment(self):
        """Test creating a new shipment"""
        self.client.force_authenticate(user=self.user1)
        data = {
            "order": self.order1.id,
            "carrier_preset": self.carrier.id,
            "tracking_id": "TRACK003",
            "origin_country": "US",
            "dest_country": "DE",
        }
        response = self.client.post("/api/shipping/shipments/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["tracking_id"], "TRACK003")
        self.assertEqual(response.data["status"], "in_transit")

        # Verify shipment was created in database
        shipment = Shipment.objects.get(tracking_id="TRACK003")
        self.assertEqual(shipment.user, self.user1)
        self.assertEqual(shipment.order, self.order1)

    def test_create_shipment_validation(self):
        """Test shipment validation - requires carrier or provider"""
        self.client.force_authenticate(user=self.user1)
        data = {
            "order": self.order1.id,
            "origin_country": "US",
            "dest_country": "DE",
        }
        response = self.client.post("/api/shipping/shipments/", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("carrier_preset", str(response.data) + str(response.data))

    def test_filter_shipments_by_status(self):
        """Test filtering shipments by status"""
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get("/api/shipping/shipments/?status=in_transit")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["status"], "in_transit")

    def test_filter_shipments_by_order(self):
        """Test filtering shipments by order"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f"/api/shipping/shipments/?order={self.order1.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_get_shipment_tracking_events(self):
        """Test getting tracking events for a shipment"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f"/api/shipping/shipments/{self.shipment1.id}/tracking/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["status"], "in_transit")
        self.assertEqual(response.data[0]["location"], "New York, NY")

    def test_by_order_endpoint(self):
        """Test by_order custom action"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f"/api/shipping/shipments/by_order/?order_id={self.order1.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["tracking_id"], "TRACK001")

    def test_by_order_missing_param(self):
        """Test by_order without order_id parameter"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/api/shipping/shipments/by_order/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("order_id", response.data["error"])


class TrackingEventAPITests(ShippingAPITestCase):
    """Tests for TrackingEvent API endpoints"""

    def test_list_tracking_events(self):
        """Test listing tracking events for user's shipments"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/api/shipping/tracking-events/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_user_cannot_see_other_events(self):
        """Test user cannot see other user's tracking events"""
        # Create event for user2's shipment
        TrackingEvent.objects.create(
            shipment=self.shipment2,
            status="delivered",
            location="London, UK",
            description="Package delivered",
            occurred_at=timezone.now(),
        )

        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/api/shipping/tracking-events/")

        # Should only see user1's events
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["location"], "New York, NY")

    def test_filter_events_by_shipment(self):
        """Test filtering events by shipment"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f"/api/shipping/tracking-events/?shipment={self.shipment1.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)


class PermissionTests(ShippingAPITestCase):
    """Tests for API permissions"""

    def test_unauthenticated_access_denied(self):
        """Test unauthenticated users cannot access API"""
        endpoints = [
            "/api/shipping/carriers/",
            "/api/shipping/shipments/",
            "/api/shipping/tracking-events/",
            "/api/shipping/providers/",
        ]

        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
                f"Endpoint {endpoint} should require authentication",
            )

    def test_staff_can_modify_shipments(self):
        """Test staff users can update shipments"""
        self.client.force_authenticate(user=self.staff_user)

        # Update shipment status
        data = {"status": "delivered"}
        response = self.client.patch(
            f"/api/shipping/shipments/{self.shipment1.id}/", data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "delivered")

    def test_regular_user_cannot_modify_others_shipment(self):
        """Test regular users cannot modify other users' shipments"""
        self.client.force_authenticate(user=self.user2)

        data = {"status": "delivered"}
        response = self.client.patch(
            f"/api/shipping/shipments/{self.shipment1.id}/", data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
