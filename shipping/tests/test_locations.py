"""
Tests for Location model and pickup functionality.

Tests cover:
- Location model creation and fields
- Operating hours validation
- Distance calculations (Haversine formula)
- Pickup availability checks
- Delivery range calculations
- Time slot generation
"""

from datetime import datetime, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from djmoney.money import Money

from cart.models import ShippingMethod
from orders.models import Order
from shipping.models import Location, ShippingZone

User = get_user_model()


class LocationModelTest(TestCase):
    """Test Location model creation and basic functionality."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.zone = ShippingZone.objects.create(name="USA", countries=["US"])

    def test_create_location_basic(self):
        """Test creating a basic location."""
        location = Location.objects.create(
            name="Downtown Store",
            code="STORE-001",
            location_type="store",
            address1="123 Main St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="US",
            created_by=self.user,
        )

        self.assertEqual(location.name, "Downtown Store")
        self.assertEqual(location.code, "STORE-001")
        self.assertEqual(location.location_type, "store")
        self.assertTrue(location.is_active)
        self.assertTrue(location.accepts_pickup)
        self.assertFalse(location.accepts_delivery_dispatch)

    def test_location_str_representation(self):
        """Test location string representation."""
        location = Location.objects.create(
            name="Main Warehouse",
            code="WH-001",
            address1="456 Industrial Pkwy",
            city="Los Angeles",
            state="CA",
            postal_code="90001",
            country="US",
        )

        self.assertEqual(str(location), "Main Warehouse (WH-001)")

    def test_location_full_address_property(self):
        """Test full_address property returns formatted address."""
        location = Location.objects.create(
            name="Store",
            code="ST-001",
            address1="123 Main St",
            address2="Suite 100",
            city="Chicago",
            state="IL",
            postal_code="60601",
            country="US",
        )

        expected = "123 Main St, Suite 100, Chicago, IL 60601, US"
        self.assertEqual(location.full_address, expected)

    def test_location_full_address_without_address2(self):
        """Test full_address property without address2."""
        location = Location.objects.create(
            name="Store",
            code="ST-002",
            address1="789 Oak Ave",
            city="Boston",
            state="MA",
            postal_code="02101",
            country="US",
        )

        expected = "789 Oak Ave, Boston, MA 02101, US"
        self.assertEqual(location.full_address, expected)

    def test_location_coordinates_property_with_values(self):
        """Test coordinates property returns tuple when set."""
        location = Location.objects.create(
            name="Store",
            code="ST-003",
            address1="123 Main St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="US",
            latitude=Decimal("40.7128"),
            longitude=Decimal("-74.0060"),
        )

        coords = location.coordinates
        self.assertIsNotNone(coords)
        self.assertEqual(coords[0], 40.7128)
        self.assertEqual(coords[1], -74.0060)

    def test_location_coordinates_property_without_values(self):
        """Test coordinates property returns None when not set."""
        location = Location.objects.create(
            name="Store",
            code="ST-004",
            address1="123 Main St",
            city="Denver",
            state="CO",
            postal_code="80201",
            country="US",
        )

        self.assertIsNone(location.coordinates)

    def test_location_with_zones(self):
        """Test location can be associated with shipping zones."""
        location = Location.objects.create(
            name="Regional Hub",
            code="HUB-001",
            address1="100 Commerce Dr",
            city="Dallas",
            state="TX",
            postal_code="75201",
            country="US",
        )

        location.zones.add(self.zone)

        self.assertEqual(location.zones.count(), 1)
        self.assertIn(self.zone, location.zones.all())


class LocationOperatingHoursTest(TestCase):
    """Test Location operating hours functionality."""

    def setUp(self):
        self.location = Location.objects.create(
            name="Test Store",
            code="TS-001",
            address1="123 Test St",
            city="Test City",
            state="TS",
            postal_code="12345",
            country="US",
            operating_hours={
                "monday": {"open": "09:00", "close": "17:00", "closed": False},
                "tuesday": {"open": "09:00", "close": "17:00", "closed": False},
                "wednesday": {"open": "09:00", "close": "17:00", "closed": False},
                "thursday": {"open": "09:00", "close": "17:00", "closed": False},
                "friday": {"open": "09:00", "close": "17:00", "closed": False},
                "saturday": {"open": "10:00", "close": "15:00", "closed": False},
                "sunday": {"closed": True},
            },
        )

    def test_is_open_at_during_hours(self):
        """Test is_open_at returns True during operating hours."""
        # Monday at 12:00 PM
        dt = timezone.make_aware(datetime(2025, 11, 10, 12, 0))  # Monday
        self.assertTrue(self.location.is_open_at(dt))

    def test_is_open_at_before_opening(self):
        """Test is_open_at returns False before opening."""
        # Monday at 8:00 AM (opens at 9:00 AM)
        dt = timezone.make_aware(datetime(2025, 11, 10, 8, 0))
        self.assertFalse(self.location.is_open_at(dt))

    def test_is_open_at_after_closing(self):
        """Test is_open_at returns False after closing."""
        # Monday at 6:00 PM (closes at 5:00 PM)
        dt = timezone.make_aware(datetime(2025, 11, 10, 18, 0))
        self.assertFalse(self.location.is_open_at(dt))

    def test_is_open_at_closed_day(self):
        """Test is_open_at returns False on closed days."""
        # Sunday (closed)
        dt = timezone.make_aware(datetime(2025, 11, 9, 12, 0))  # Sunday
        self.assertFalse(self.location.is_open_at(dt))

    def test_is_open_at_inactive_location(self):
        """Test is_open_at returns False for inactive location."""
        self.location.is_active = False
        self.location.save()

        dt = timezone.make_aware(datetime(2025, 11, 10, 12, 0))
        self.assertFalse(self.location.is_open_at(dt))

    def test_is_open_at_no_hours_specified(self):
        """Test is_open_at returns True when no hours specified (always open)."""
        location = Location.objects.create(
            name="24/7 Store",
            code="247-001",
            address1="123 Always St",
            city="Open City",
            state="OC",
            postal_code="24700",
            country="US",
            operating_hours={},
        )

        dt = timezone.now()
        self.assertTrue(location.is_open_at(dt))


class LocationDistanceCalculationTest(TestCase):
    """Test Location distance calculation methods."""

    def setUp(self):
        # New York City coordinates
        self.nyc_location = Location.objects.create(
            name="NYC Store",
            code="NYC-001",
            address1="123 Broadway",
            city="New York",
            state="NY",
            postal_code="10001",
            country="US",
            latitude=Decimal("40.7128"),
            longitude=Decimal("-74.0060"),
        )

    def test_calculate_distance_to_nearby_point(self):
        """Test calculating distance to nearby point."""
        # Brooklyn coordinates (approximately 6-8km from NYC)
        brooklyn_lat = Decimal("40.6782")
        brooklyn_lon = Decimal("-73.9442")

        distance = self.nyc_location.calculate_distance_to(brooklyn_lat, brooklyn_lon)

        self.assertIsNotNone(distance)
        # Distance should be approximately 6-8 km
        self.assertGreater(distance, 5)
        self.assertLess(distance, 10)

    def test_calculate_distance_to_far_point(self):
        """Test calculating distance to far point."""
        # Los Angeles coordinates (approximately 3940km from NYC)
        la_lat = Decimal("34.0522")
        la_lon = Decimal("-118.2437")

        distance = self.nyc_location.calculate_distance_to(la_lat, la_lon)

        self.assertIsNotNone(distance)
        # Distance should be approximately 3900-4000 km
        self.assertGreater(distance, 3800)
        self.assertLess(distance, 4100)

    def test_calculate_distance_without_coordinates(self):
        """Test calculate_distance returns None when location has no coordinates."""
        location = Location.objects.create(
            name="No Coords Store",
            code="NC-001",
            address1="123 Unknown St",
            city="Unknown",
            state="UK",
            postal_code="00000",
            country="US",
        )

        distance = location.calculate_distance_to(Decimal("40.7128"), Decimal("-74.0060"))
        self.assertIsNone(distance)

    def test_calculate_distance_to_same_point(self):
        """Test calculating distance to same coordinates (should be ~0)."""
        distance = self.nyc_location.calculate_distance_to(Decimal("40.7128"), Decimal("-74.0060"))

        self.assertIsNotNone(distance)
        # Distance to same point should be very close to 0
        self.assertLess(distance, 1)


class LocationDeliveryRangeTest(TestCase):
    """Test Location delivery range checking."""

    def setUp(self):
        self.location = Location.objects.create(
            name="Distribution Center",
            code="DC-001",
            address1="100 Warehouse Rd",
            city="Chicago",
            state="IL",
            postal_code="60601",
            country="US",
            latitude=Decimal("41.8781"),
            longitude=Decimal("-87.6298"),
            accepts_delivery_dispatch=True,
            delivery_radius=Decimal("50.00"),  # 50 km radius
        )

    def test_is_within_delivery_range_inside_radius(self):
        """Test point within delivery radius."""
        # Point approximately 30km from Chicago
        nearby_lat = Decimal("41.9742")
        nearby_lon = Decimal("-87.9073")

        in_range, distance = self.location.is_within_delivery_range(nearby_lat, nearby_lon)

        self.assertTrue(in_range)
        self.assertIsNotNone(distance)
        self.assertLess(distance, 50)

    def test_is_within_delivery_range_outside_radius(self):
        """Test point outside delivery radius."""
        # Milwaukee, WI (approximately 150km from Chicago)
        milwaukee_lat = Decimal("43.0389")
        milwaukee_lon = Decimal("-87.9065")

        in_range, distance = self.location.is_within_delivery_range(milwaukee_lat, milwaukee_lon)

        self.assertFalse(in_range)
        self.assertIsNotNone(distance)
        self.assertGreater(distance, 50)

    def test_is_within_delivery_range_no_radius_limit(self):
        """Test delivery range with no radius limit (unlimited)."""
        self.location.delivery_radius = None
        self.location.save()

        # Any point should be in range
        in_range, distance = self.location.is_within_delivery_range(
            Decimal("40.7128"), Decimal("-74.0060")
        )

        self.assertTrue(in_range)
        self.assertIsNone(distance)

    def test_is_within_delivery_range_not_accepting_delivery(self):
        """Test delivery range when location doesn't accept delivery."""
        self.location.accepts_delivery_dispatch = False
        self.location.save()

        in_range, distance = self.location.is_within_delivery_range(
            Decimal("41.9742"), Decimal("-87.9073")
        )

        self.assertFalse(in_range)
        self.assertIsNone(distance)

    def test_is_within_delivery_range_no_coordinates(self):
        """Test delivery range when location has no coordinates."""
        location = Location.objects.create(
            name="No Coords DC",
            code="NC-DC-001",
            address1="123 Unknown",
            city="Unknown",
            state="UK",
            postal_code="00000",
            country="US",
            accepts_delivery_dispatch=True,
            delivery_radius=Decimal("50.00"),
        )

        in_range, distance = location.is_within_delivery_range(
            Decimal("40.7128"), Decimal("-74.0060")
        )

        self.assertFalse(in_range)
        self.assertIsNone(distance)


class LocationPickupAvailabilityTest(TestCase):
    """Test Location pickup availability checking."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.location = Location.objects.create(
            name="Pickup Store",
            code="PS-001",
            address1="123 Pickup St",
            city="Denver",
            state="CO",
            postal_code="80201",
            country="US",
            accepts_pickup=True,
            max_daily_pickups=10,
            pickup_preparation_time=60,  # 60 minutes
            operating_hours={
                "monday": {"open": "09:00", "close": "17:00", "closed": False},
                "tuesday": {"open": "09:00", "close": "17:00", "closed": False},
                "wednesday": {"open": "09:00", "close": "17:00", "closed": False},
                "thursday": {"open": "09:00", "close": "17:00", "closed": False},
                "friday": {"open": "09:00", "close": "17:00", "closed": False},
                "saturday": {"closed": True},
                "sunday": {"closed": True},
            },
        )

    def test_can_accept_pickup_available(self):
        """Test can_accept_pickup returns True when available."""
        # Monday at 10:00 AM
        pickup_time = timezone.make_aware(datetime(2025, 11, 10, 10, 0))

        can_accept, reason = self.location.can_accept_pickup(pickup_time)

        self.assertTrue(can_accept)
        self.assertIn("available", reason.lower())

    def test_can_accept_pickup_inactive_location(self):
        """Test can_accept_pickup returns False for inactive location."""
        self.location.is_active = False
        self.location.save()

        can_accept, reason = self.location.can_accept_pickup()

        self.assertFalse(can_accept)
        self.assertIn("not active", reason.lower())

    def test_can_accept_pickup_not_accepting_pickups(self):
        """Test can_accept_pickup returns False when not accepting pickups."""
        self.location.accepts_pickup = False
        self.location.save()

        can_accept, reason = self.location.can_accept_pickup()

        self.assertFalse(can_accept)
        self.assertIn("does not accept", reason.lower())

    def test_can_accept_pickup_at_capacity(self):
        """Test can_accept_pickup returns False when at daily capacity."""
        # Create 10 orders for today (reaching max_daily_pickups)
        today = timezone.now().date()
        pickup_datetime = timezone.make_aware(
            datetime.combine(today, datetime.min.time().replace(hour=10))
        )

        for i in range(10):
            Order.objects.create(
                order_number=f"TEST-{i:04d}",
                user=self.user,
                email="test@example.com",
                shipping_name="Test User",
                shipping_address1="123 Test St",
                shipping_city="Test City",
                shipping_state="TS",
                shipping_postal_code="12345",
                shipping_country="US",
                subtotal=Money("100.00", "USD"),
                total_amount=Money("100.00", "USD"),
                pickup_location=self.location,
                pickup_date=pickup_datetime,
            )

        can_accept, reason = self.location.can_accept_pickup(pickup_datetime)

        self.assertFalse(can_accept)
        self.assertIn("capacity", reason.lower())

    def test_can_accept_pickup_closed_day(self):
        """Test can_accept_pickup returns False on closed day."""
        # Saturday (closed)
        saturday = timezone.make_aware(datetime(2025, 11, 8, 10, 0))

        can_accept, reason = self.location.can_accept_pickup(saturday)

        self.assertFalse(can_accept)
        self.assertIn("closed", reason.lower())


class LocationTimeSlotTest(TestCase):
    """Test Location time slot generation."""

    def setUp(self):
        self.location = Location.objects.create(
            name="Slot Store",
            code="SS-001",
            address1="123 Slot St",
            city="Seattle",
            state="WA",
            postal_code="98101",
            country="US",
            accepts_pickup=True,
            operating_hours={
                "monday": {"open": "09:00", "close": "17:00", "closed": False},
                "saturday": {"closed": True},
            },
        )

    def test_get_available_pickup_slots_open_day(self):
        """Test generating time slots for open day."""
        # Monday
        monday = datetime(2025, 11, 10).date()

        slots = self.location.get_available_pickup_slots(monday)

        self.assertGreater(len(slots), 0)
        # 9:00-17:00 with 30-minute slots = 16 slots
        self.assertEqual(len(slots), 16)

        # Check first slot
        self.assertEqual(slots[0]["start"], "09:00")
        self.assertEqual(slots[0]["end"], "09:30")
        self.assertTrue(slots[0]["available"])

        # Check last slot
        self.assertEqual(slots[-1]["start"], "16:30")
        self.assertEqual(slots[-1]["end"], "17:00")

    def test_get_available_pickup_slots_closed_day(self):
        """Test generating time slots for closed day."""
        # Saturday (closed)
        saturday = datetime(2025, 11, 8).date()

        slots = self.location.get_available_pickup_slots(saturday)

        self.assertEqual(len(slots), 0)

    def test_get_available_pickup_slots_inactive_location(self):
        """Test time slots for inactive location."""
        self.location.is_active = False
        self.location.save()

        monday = datetime(2025, 11, 10).date()
        slots = self.location.get_available_pickup_slots(monday)

        self.assertEqual(len(slots), 0)

    def test_get_available_pickup_slots_not_accepting_pickups(self):
        """Test time slots when not accepting pickups."""
        self.location.accepts_pickup = False
        self.location.save()

        monday = datetime(2025, 11, 10).date()
        slots = self.location.get_available_pickup_slots(monday)

        self.assertEqual(len(slots), 0)


class LocationShippingMethodIntegrationTest(TestCase):
    """Test Location integration with ShippingMethod."""

    def setUp(self):
        self.location1 = Location.objects.create(
            name="Store 1",
            code="ST-001",
            address1="123 First St",
            city="Boston",
            state="MA",
            postal_code="02101",
            country="US",
            accepts_pickup=True,
        )

        self.location2 = Location.objects.create(
            name="Store 2",
            code="ST-002",
            address1="456 Second Ave",
            city="Boston",
            state="MA",
            postal_code="02102",
            country="US",
            accepts_pickup=True,
        )

        self.shipping_method = ShippingMethod.objects.create(
            name="Store Pickup",
            description="Pick up at store location",
            method_type="local_pickup",
            flat_rate_cost=Money("0.00", "USD"),
            is_active=True,
        )

    def test_shipping_method_pickup_locations_relationship(self):
        """Test ShippingMethod can be linked to multiple locations."""
        self.shipping_method.pickup_locations.add(self.location1, self.location2)

        self.assertEqual(self.shipping_method.pickup_locations.count(), 2)
        self.assertIn(self.location1, self.shipping_method.pickup_locations.all())
        self.assertIn(self.location2, self.shipping_method.pickup_locations.all())

    def test_location_pickup_methods_reverse_relationship(self):
        """Test Location reverse relationship to ShippingMethod."""
        self.shipping_method.pickup_locations.add(self.location1)

        self.assertEqual(self.location1.pickup_methods.count(), 1)
        self.assertIn(self.shipping_method, self.location1.pickup_methods.all())

    def test_multiple_shipping_methods_same_location(self):
        """Test multiple shipping methods can use same location."""
        method2 = ShippingMethod.objects.create(
            name="Express Pickup",
            description="Express pickup service",
            method_type="local_pickup",
            flat_rate_cost=Money("5.00", "USD"),
            is_active=True,
        )

        self.shipping_method.pickup_locations.add(self.location1)
        method2.pickup_locations.add(self.location1)

        self.assertEqual(self.location1.pickup_methods.count(), 2)


class LocationOrderIntegrationTest(TestCase):
    """Test Location integration with Order model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.location = Location.objects.create(
            name="Pickup Location",
            code="PL-001",
            address1="123 Pickup St",
            city="Portland",
            state="OR",
            postal_code="97201",
            country="US",
            accepts_pickup=True,
        )

    def test_order_with_pickup_location(self):
        """Test creating order with pickup location."""
        pickup_date = timezone.now() + timedelta(days=1)

        order = Order.objects.create(
            order_number="TEST-001",
            user=self.user,
            email="test@example.com",
            shipping_name="Test User",
            shipping_address1="123 Test St",
            shipping_city="Test City",
            shipping_state="TS",
            shipping_postal_code="12345",
            shipping_country="US",
            subtotal=Money("100.00", "USD"),
            total_amount=Money("100.00", "USD"),
            pickup_location=self.location,
            pickup_date=pickup_date,
        )

        self.assertEqual(order.pickup_location, self.location)
        self.assertEqual(order.pickup_date, pickup_date)

    def test_location_pickup_orders_relationship(self):
        """Test Location reverse relationship to Orders."""
        order1 = Order.objects.create(
            order_number="TEST-002",
            user=self.user,
            email="test@example.com",
            shipping_name="Test User",
            shipping_address1="123 Test St",
            shipping_city="Test City",
            shipping_state="TS",
            shipping_postal_code="12345",
            shipping_country="US",
            subtotal=Money("100.00", "USD"),
            total_amount=Money("100.00", "USD"),
            pickup_location=self.location,
        )

        order2 = Order.objects.create(
            order_number="TEST-003",
            user=self.user,
            email="test@example.com",
            shipping_name="Test User",
            shipping_address1="123 Test St",
            shipping_city="Test City",
            shipping_state="TS",
            shipping_postal_code="12345",
            shipping_country="US",
            subtotal=Money("100.00", "USD"),
            total_amount=Money("100.00", "USD"),
            pickup_location=self.location,
        )

        self.assertEqual(self.location.pickup_orders.count(), 2)
        self.assertIn(order1, self.location.pickup_orders.all())
        self.assertIn(order2, self.location.pickup_orders.all())

    def test_order_without_pickup_location(self):
        """Test creating regular order without pickup location."""
        order = Order.objects.create(
            order_number="TEST-004",
            user=self.user,
            email="test@example.com",
            shipping_name="Test User",
            shipping_address1="123 Test St",
            shipping_city="Test City",
            shipping_state="TS",
            shipping_postal_code="12345",
            shipping_country="US",
            subtotal=Money("100.00", "USD"),
            total_amount=Money("100.00", "USD"),
        )

        self.assertIsNone(order.pickup_location)
        self.assertIsNone(order.pickup_date)
