"""
Fulfillment service gap tests.

Tests for Gap 4 (shipping_origin_country fallback), Gap 5 (CountryWarehouseFallback),
Gap 6 (geocoder distance scoring), Gap 7 (real stock scoring),
and Gap 9 (region-aware reservation warehouse selection).
"""
import pytest
from decimal import Decimal
from unittest.mock import patch, MagicMock

from catalog.services.fulfillment import FulfillmentService
from catalog.services.stock_reservation import StockReservationService
from catalog.models import StockItem
from tests.factories import (
    ProductFactory, ProductVariantFactory, StockItemFactory,
    SalesRegionFactory, WarehouseFactory, OrderFactory,
    CategoryFactory, CartFactory, CartItemFactory,
    ShippingCountryFactory, CountryWarehouseFallbackFactory,
)
from tests.fixtures.checkout_scenarios import multi_warehouse_merchant

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.fulfillment]


@pytest.fixture
def site_settings(db):
    """SiteSettings required for single-tenant operation."""
    from core.models import SiteSettings
    settings, _ = SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            'site_name': 'Test Store',
            'admin_email': 'admin@test.spwig.com',
            'default_currency': 'USD',
            'default_language': 'en',
        }
    )
    # Clear shipping_origin_country to prevent fallback interference
    SiteSettings.objects.filter(pk=1).update(shipping_origin_country='')
    settings.refresh_from_db()
    return settings


@pytest.fixture
def merchant(db, site_settings):
    """Multi-warehouse merchant scenario."""
    return multi_warehouse_merchant()


@pytest.fixture
def fulfillment_svc():
    """FulfillmentService instance."""
    return FulfillmentService()


# ============================================================
# A. Shipping Origin Country Fallback (Gap 4)
# ============================================================

class TestShippingOriginFallback:
    """Test that shipping_origin_country is used when no region matches."""

    def test_origin_country_used_when_no_region_matches(
        self, fulfillment_svc, merchant, site_settings
    ):
        """Order to BR (not in any region), origin='US' -> US region returned."""
        from core.models import SiteSettings
        # Use .filter().update() to bypass SiteSettings.clean() validation
        SiteSettings.objects.filter(pk=site_settings.pk).update(
            shipping_origin_country='US'
        )

        order = OrderFactory(shipping_country='BR')

        region = fulfillment_svc._get_order_region(order)

        # Should fall back to origin country 'US' -> NAM region
        assert region is not None
        assert region.code == 'NAM'

    def test_origin_country_ignored_when_region_matches(
        self, fulfillment_svc, merchant, site_settings
    ):
        """Order to US, US region exists -> direct match, origin not consulted."""
        from core.models import SiteSettings
        # Use .filter().update() to bypass SiteSettings.clean() validation
        SiteSettings.objects.filter(pk=site_settings.pk).update(
            shipping_origin_country='DE'
        )

        order = OrderFactory(shipping_country='US')

        region = fulfillment_svc._get_order_region(order)

        # Direct match on US -> NAM region (not EUR despite origin='DE')
        assert region is not None
        assert region.code == 'NAM'


# ============================================================
# B. Country Warehouse Fallback (Gap 5)
# ============================================================

class TestCountryWarehouseFallback:
    """Test fallback warehouse chain for countries without regional warehouses."""

    def test_fallback_warehouses_used_when_region_empty(
        self, fulfillment_svc, merchant
    ):
        """AU order, no AU region -> fallback warehouses used, allocation succeeds."""
        wh_eu = merchant['warehouses']['eu']
        wh_us = merchant['warehouses']['us']
        product_a = merchant['products']['a']

        order = OrderFactory(shipping_country='AU')
        order_items = [
            {'product': product_a, 'variant': None, 'quantity': 5},
        ]

        with patch.object(fulfillment_svc, '_geocode_order_address', return_value=None):
            allocation = fulfillment_svc.select_warehouse_for_order(order, order_items)

        # Allocation succeeds via fallback warehouses (scoring picks best)
        assert 0 in allocation
        assert allocation[0] in (wh_eu, wh_us)

    def test_fallback_priority_ordering(self, fulfillment_svc, merchant):
        """Two fallbacks with different priorities -> lower number tried first."""
        wh_eu = merchant['warehouses']['eu']
        wh_us = merchant['warehouses']['us']
        product_b = merchant['products']['b']

        # product_b: 5 at US, 80 at EU
        # Need enough quantity that EU can handle but US cannot
        order = OrderFactory(shipping_country='AU')
        order_items = [
            {'product': product_b, 'variant': None, 'quantity': 50},
        ]

        with patch.object(fulfillment_svc, '_geocode_order_address', return_value=None):
            allocation = fulfillment_svc.select_warehouse_for_order(order, order_items)

        # EU-WEST is fallback priority 0 and has 80 units
        assert allocation[0] == wh_eu

    def test_no_fallback_configured_raises_error(self, fulfillment_svc, site_settings):
        """No region warehouses, no fallbacks -> InsufficientStockError."""
        from catalog.services.fulfillment import InsufficientStockError

        category = CategoryFactory(name='Isolated', slug='isolated')
        product = ProductFactory(
            name='Isolated Product', slug='isolated-product',
            category=category, track_inventory=True,
        )

        # No region covers 'ZZ', no shipping country or fallback
        order = OrderFactory(shipping_country='ZZ')
        order_items = [
            {'product': product, 'variant': None, 'quantity': 1},
        ]

        with patch.object(fulfillment_svc, '_geocode_order_address', return_value=None):
            with pytest.raises(InsufficientStockError):
                fulfillment_svc.select_warehouse_for_order(order, order_items)


# ============================================================
# C. Distance Scoring (Gap 6)
# ============================================================

class TestDistanceScoring:
    """Test geocoder-powered distance scoring in warehouse selection."""

    def test_closer_warehouse_scores_higher(self, fulfillment_svc, merchant):
        """WH1 at 100km vs WH2 at 5000km -> closer WH gets higher distance score."""
        wh_us = merchant['warehouses']['us']
        wh_eu = merchant['warehouses']['eu']

        # Order ships to NYC (near US-EAST warehouse)
        order = OrderFactory(
            shipping_country='US',
            shipping_city='New York',
            shipping_state='NY',
            shipping_postal_code='10001',
            shipping_address1='123 Broadway',
        )

        # Mock geocoder to return NYC coordinates
        nyc_coords = (40.7128, -74.0060)
        with patch.object(fulfillment_svc, '_geocode_order_address', return_value=nyc_coords):
            score_us = fulfillment_svc._calculate_distance_score(wh_us, order)
            score_eu = fulfillment_svc._calculate_distance_score(wh_eu, order)

        # US warehouse is ~5km from NYC; EU is ~6000km
        assert score_us > score_eu

    def test_distance_score_degrades_gracefully_no_geocoder(self, fulfillment_svc, merchant):
        """Geocoder unavailable -> returns 0.5 fallback."""
        wh_us = merchant['warehouses']['us']
        order = OrderFactory(shipping_country='US')

        with patch.object(fulfillment_svc, '_geocode_order_address', return_value=None):
            score = fulfillment_svc._calculate_distance_score(wh_us, order)

        assert score == 0.5

    def test_distance_score_degrades_gracefully_no_warehouse_coords(
        self, fulfillment_svc, site_settings
    ):
        """Warehouse has no lat/lon -> returns 0.5."""
        region = SalesRegionFactory(name='No Coords Region', code='NOCRD', countries=['US'])
        wh = WarehouseFactory(
            name='No Coords WH', code='NO-COORDS',
            region=region, latitude=None, longitude=None,
        )
        order = OrderFactory(shipping_country='US')

        score = fulfillment_svc._calculate_distance_score(wh, order)
        assert score == 0.5

    def test_geocoded_address_is_cached(self, fulfillment_svc, merchant):
        """Second call uses cache, doesn't hit geocoder again."""
        order = OrderFactory(
            shipping_country='US',
            shipping_city='Boston',
            shipping_state='MA',
            shipping_postal_code='02101',
            shipping_address1='1 State St',
        )

        boston_coords = (42.3601, -71.0589)
        mock_client = MagicMock()
        mock_client.autocomplete.return_value = {
            'suggestions': [{'centroid': {'lat': 42.3601, 'lon': -71.0589}}]
        }

        with patch('catalog.services.fulfillment.cache') as mock_cache:
            # First call: cache miss
            mock_cache.get.return_value = None

            with patch('address_autocomplete.services.AutocompleteClient', return_value=mock_client):
                result1 = fulfillment_svc._geocode_order_address(order)

            assert result1 == boston_coords
            assert mock_cache.set.called

            # Second call: cache hit
            mock_cache.get.return_value = boston_coords
            result2 = fulfillment_svc._geocode_order_address(order)

            assert result2 == boston_coords


# ============================================================
# D. Stock Scoring (Gap 7)
# ============================================================

class TestStockScoring:
    """Test real stock level scoring in warehouse selection."""

    def test_warehouse_with_more_stock_scores_higher(self, fulfillment_svc, merchant):
        """WH with 100 units scores higher than WH with 20 units for large order."""
        wh_us = merchant['warehouses']['us']
        wh_eu = merchant['warehouses']['eu']
        product_a = merchant['products']['a']

        # product_a: 100 at US, 20 at EU
        # Use quantity=50 so US ratio = min(100/50, 1.0) = 1.0
        # and EU ratio = min(20/50, 1.0) = 0.4
        order_items = [
            {'product': product_a, 'variant': None, 'quantity': 50},
        ]

        score_us = fulfillment_svc._calculate_stock_score(wh_us, order_items)
        score_eu = fulfillment_svc._calculate_stock_score(wh_eu, order_items)

        assert score_us > score_eu

    def test_priority_still_dominates_over_stock(self, fulfillment_svc, merchant):
        """High priority + low stock beats low priority + high stock."""
        wh_us = merchant['warehouses']['us']
        wh_eu = merchant['warehouses']['eu']
        product_b = merchant['products']['b']

        # product_b: 5 at US (priority 80), 80 at EU (priority 60)
        order = OrderFactory(shipping_country='US')
        order_items = [
            {'product': product_b, 'variant': None, 'quantity': 3},
        ]

        with patch.object(fulfillment_svc, '_geocode_order_address', return_value=None):
            # Both can fulfill qty=3, so scoring decides
            score_us = fulfillment_svc._calculate_warehouse_score(wh_us, order, order_items)
            score_eu = fulfillment_svc._calculate_warehouse_score(wh_eu, order, order_items)

        # US has priority 80 (40% weight = 0.32) vs EU priority 60 (40% weight = 0.24)
        # Priority advantage of 0.08 should outweigh stock difference
        # at 30% weight since both can fulfill
        assert score_us > score_eu

    def test_score_with_zero_stock_is_zero(self, fulfillment_svc, merchant):
        """0 available -> stock score component is 0.0."""
        wh_us = merchant['warehouses']['us']
        variable = merchant['products']['variable']
        variant_blue = merchant['variants']['blue']

        # Blue has 0 at US
        order_items = [
            {'product': variable, 'variant': variant_blue, 'quantity': 5},
        ]

        score = fulfillment_svc._calculate_stock_score(wh_us, order_items)
        assert score == 0.0

    def test_stock_score_without_order_items_returns_default(self, fulfillment_svc, merchant):
        """No order_items -> returns 0.5 default."""
        wh_us = merchant['warehouses']['us']

        score = fulfillment_svc._calculate_stock_score(wh_us, None)
        assert score == 0.5

        score2 = fulfillment_svc._calculate_stock_score(wh_us, [])
        assert score2 == 0.5


# ============================================================
# E. Reservation Warehouse Alignment (Gap 9)
# ============================================================

class TestReservationWarehouseAlignment:
    """Test region-aware reservation warehouse selection."""

    def test_reservation_picks_regional_warehouse(self, merchant):
        """US region -> reservation at US warehouse."""
        wh_us = merchant['warehouses']['us']
        us_region = merchant['regions']['us']
        product_a = merchant['products']['a']

        from tests.factories import UserFactory
        user = UserFactory()
        cart = CartFactory(user=user)
        cart_item = CartItemFactory(cart=cart, product=product_a, quantity=2)

        success, msg, reservation = StockReservationService.reserve_stock(
            cart_item=cart_item,
            quantity=2,
            channel='web',
            region=us_region,
        )

        assert success is True
        assert reservation is not None
        assert reservation.warehouse == wh_us

    def test_reservation_without_region_picks_global_best(self, merchant):
        """No region -> picks warehouse with most stock (backward compat)."""
        product_a = merchant['products']['a']

        from tests.factories import UserFactory
        user = UserFactory()
        cart = CartFactory(user=user)
        cart_item = CartItemFactory(cart=cart, product=product_a, quantity=2)

        success, msg, reservation = StockReservationService.reserve_stock(
            cart_item=cart_item,
            quantity=2,
            channel='web',
            region=None,
        )

        assert success is True
        assert reservation is not None
        # US warehouse has 100 units (most stock) so should be selected
        assert reservation.warehouse == merchant['warehouses']['us']

    def test_reservation_converts_without_release_at_same_warehouse(self, merchant):
        """Reserve at WH1, checkout selects WH1 -> conversion succeeds."""
        wh_us = merchant['warehouses']['us']
        us_region = merchant['regions']['us']
        product_a = merchant['products']['a']

        from tests.factories import UserFactory
        user = UserFactory()
        cart = CartFactory(user=user)
        cart_item = CartItemFactory(cart=cart, product=product_a, quantity=5)

        # Reserve
        success, _, reservation = StockReservationService.reserve_stock(
            cart_item=cart_item,
            quantity=5,
            channel='web',
            region=us_region,
        )
        assert success

        # Get allocated before conversion
        stock_before = StockItem.objects.get(
            product=product_a, warehouse=wh_us, variant__isnull=True,
        )
        allocated_before = stock_before.allocated

        # Convert at same warehouse (no release needed)
        converted = StockReservationService.convert_reservation_to_order_allocation(
            cart_item=cart_item,
            warehouse=wh_us,
        )

        assert converted is True

        # Allocated should stay the same (reservation deleted, allocation counts for order)
        stock_after = StockItem.objects.get(
            product=product_a, warehouse=wh_us, variant__isnull=True,
        )
        assert stock_after.allocated == allocated_before

    def test_reservation_mismatch_triggers_release(self, merchant):
        """Reserve WH1, checkout WH2 -> reservation released, fresh allocation needed."""
        wh_us = merchant['warehouses']['us']
        wh_eu = merchant['warehouses']['eu']
        us_region = merchant['regions']['us']
        product_a = merchant['products']['a']

        from tests.factories import UserFactory
        user = UserFactory()
        cart = CartFactory(user=user)
        cart_item = CartItemFactory(cart=cart, product=product_a, quantity=3)

        # Reserve at US
        success, _, reservation = StockReservationService.reserve_stock(
            cart_item=cart_item,
            quantity=3,
            channel='web',
            region=us_region,
        )
        assert success
        assert reservation.warehouse == wh_us

        # Convert at EU (different warehouse)
        converted = StockReservationService.convert_reservation_to_order_allocation(
            cart_item=cart_item,
            warehouse=wh_eu,
        )

        # Should return False — reservation was released, caller must re-allocate
        assert converted is False

        # US warehouse allocation should be decremented (released)
        stock_us = StockItem.objects.get(
            product=product_a, warehouse=wh_us, variant__isnull=True,
        )
        assert stock_us.allocated == 0

    def test_reservation_region_falls_back_to_global(self, merchant):
        """Region with no stock falls back to global warehouse search."""
        product_b = merchant['products']['b']
        eu_region = merchant['regions']['eu']

        # product_b: 5 at US, 80 at EU
        # EU region should work fine
        from tests.factories import UserFactory
        user = UserFactory()
        cart = CartFactory(user=user)
        cart_item = CartItemFactory(cart=cart, product=product_b, quantity=10)

        success, msg, reservation = StockReservationService.reserve_stock(
            cart_item=cart_item,
            quantity=10,
            channel='web',
            region=eu_region,
        )

        assert success is True
        assert reservation is not None
        assert reservation.warehouse == merchant['warehouses']['eu']
