"""
Fulfillment service integration tests.

Tests for Bug 1 (warehouse allocation mapping), Bug 2 (variant stock filtering),
and Bug 3 (currency handling in shipping rules).
"""

from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest

from catalog.models import StockItem
from catalog.services.fulfillment import FulfillmentService, InsufficientStockError
from tests.factories import (
    OrderFactory,
    OrderItemFactory,
    ProductFactory,
    ShippingMethodFactory,
    ShippingZoneFactory,
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
            "site_name": "Test Store",
            "admin_email": "admin@test.spwig.com",
            "default_currency": "USD",
            "default_language": "en",
        },
    )
    # Clear shipping_origin_country to prevent fallback interference
    SiteSettings.objects.filter(pk=1).update(shipping_origin_country="")
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
# A. Warehouse Allocation (Bug 1)
# ============================================================


class TestWarehouseAllocation:
    """Test that select_warehouse_for_order returns correct index-based mapping."""

    def test_single_warehouse_returns_indexed_allocation(self, fulfillment_svc, merchant):
        """1 region, 1 WH with stock for all items -> {0: wh, 1: wh}."""
        wh_us = merchant["warehouses"]["us"]
        product_a = merchant["products"]["a"]
        product_b = merchant["products"]["b"]

        order = OrderFactory(shipping_country="US")
        order_items = [
            {"product": product_a, "variant": None, "quantity": 2},
            {"product": product_b, "variant": None, "quantity": 1},
        ]

        with patch.object(fulfillment_svc, "_geocode_order_address", return_value=None):
            allocation = fulfillment_svc.select_warehouse_for_order(order, order_items)

        assert allocation == {0: wh_us, 1: wh_us}

    def test_split_shipment_returns_indexed_allocation(self, fulfillment_svc, merchant):
        """Product A only at WH1 in quantity, product B only at WH2 -> split."""
        wh_us = merchant["warehouses"]["us"]
        wh_eu = merchant["warehouses"]["eu"]
        product_a = merchant["products"]["a"]
        product_b = merchant["products"]["b"]

        # product_a: 100 at US, 20 at EU; product_b: 5 at US, 80 at EU
        # Use AU shipping — fallback chain gives both warehouses (EU priority 0, US priority 1)
        order = OrderFactory(shipping_country="AU")
        order_items = [
            {"product": product_a, "variant": None, "quantity": 50},  # only US has enough
            {"product": product_b, "variant": None, "quantity": 50},  # only EU has enough
        ]

        with patch.object(fulfillment_svc, "_geocode_order_address", return_value=None):
            allocation = fulfillment_svc.select_warehouse_for_order(order, order_items)

        # Both indices must be present
        assert 0 in allocation
        assert 1 in allocation
        # EU-WEST is first in fallback order (priority 0), so it tries EU first
        # product_a: EU has 20 (not enough for 50) -> skipped, product_b: EU has 80 (enough) -> allocated
        # US-EAST is second (priority 1), product_a: US has 100 (enough) -> allocated
        assert allocation[0] == wh_us  # product_a fulfilled from US (100 avail)
        assert allocation[1] == wh_eu  # product_b fulfilled from EU (80 avail)

    def test_allocation_raises_insufficient_stock(self, fulfillment_svc, merchant):
        """No warehouse has enough stock -> InsufficientStockError."""
        product_a = merchant["products"]["a"]

        order = OrderFactory(shipping_country="US")
        order_items = [
            {"product": product_a, "variant": None, "quantity": 9999},
        ]

        with patch.object(fulfillment_svc, "_geocode_order_address", return_value=None):
            with pytest.raises(InsufficientStockError):
                fulfillment_svc.select_warehouse_for_order(order, order_items)

    def test_order_items_without_id_key_works(self, fulfillment_svc, merchant):
        """Dicts without 'id' key -> valid allocation (Bug 1 regression)."""
        product_a = merchant["products"]["a"]

        order = OrderFactory(shipping_country="US")
        # No 'id' key in dicts — this was the original bug
        order_items = [
            {"product": product_a, "variant": None, "quantity": 1},
        ]

        with patch.object(fulfillment_svc, "_geocode_order_address", return_value=None):
            allocation = fulfillment_svc.select_warehouse_for_order(order, order_items)

        assert 0 in allocation
        assert allocation[0] is not None

    def test_digital_product_allocated_anywhere(self, fulfillment_svc, merchant):
        """Digital products (no inventory tracking) are allocated to best warehouse."""
        digital = ProductFactory(
            name="E-Book",
            slug="e-book",
            digital=True,
            track_inventory=False,
        )
        product_a = merchant["products"]["a"]

        order = OrderFactory(shipping_country="US")
        order_items = [
            {"product": product_a, "variant": None, "quantity": 1},
            {"product": digital, "variant": None, "quantity": 1},
        ]

        with patch.object(fulfillment_svc, "_geocode_order_address", return_value=None):
            allocation = fulfillment_svc.select_warehouse_for_order(order, order_items)

        assert len(allocation) == 2
        assert 0 in allocation
        assert 1 in allocation

    def test_allocation_indices_match_order_items_list(self, fulfillment_svc, merchant):
        """Allocation keys match positions in order_items list."""
        product_a = merchant["products"]["a"]
        product_b = merchant["products"]["b"]

        order = OrderFactory(shipping_country="US")
        order_items = [
            {"product": product_a, "variant": None, "quantity": 1},
            {"product": product_b, "variant": None, "quantity": 1},
            {"product": product_a, "variant": None, "quantity": 2},
        ]

        with patch.object(fulfillment_svc, "_geocode_order_address", return_value=None):
            allocation = fulfillment_svc.select_warehouse_for_order(order, order_items)

        # All indices 0, 1, 2 must be present
        assert set(allocation.keys()) == {0, 1, 2}


# ============================================================
# B. Variant Stock Filtering (Bug 2)
# ============================================================


class TestVariantStockFiltering:
    """Test that stock operations correctly filter by variant."""

    def test_check_availability_filters_by_variant(self, fulfillment_svc, merchant):
        """Variant A has stock, variant B doesn't at a given warehouse."""
        variable = merchant["products"]["variable"]
        variant_red = merchant["variants"]["red"]
        variant_blue = merchant["variants"]["blue"]
        us_region = merchant["regions"]["us"]

        # Red: 50 at US, 0 at EU; Blue: 0 at US, 40 at EU
        result_red = fulfillment_svc.check_stock_availability(
            variable,
            10,
            region=us_region,
            variant=variant_red,
        )
        result_blue = fulfillment_svc.check_stock_availability(
            variable,
            10,
            region=us_region,
            variant=variant_blue,
        )

        assert result_red["available"] is True
        assert result_red["quantity_available"] >= 10
        assert result_blue["available"] is False

    def test_check_availability_sums_null_variant(self, fulfillment_svc, merchant):
        """Simple product (null variant) returns correct availability."""
        product_a = merchant["products"]["a"]
        us_region = merchant["regions"]["us"]

        result = fulfillment_svc.check_stock_availability(
            product_a,
            5,
            region=us_region,
        )

        assert result["available"] is True
        assert result["quantity_available"] == 100  # US warehouse has 100

    def test_allocate_stock_with_variant(self, fulfillment_svc, merchant):
        """Allocate specific variant -> only that variant's StockItem modified."""
        wh_us = merchant["warehouses"]["us"]
        variable = merchant["products"]["variable"]
        variant_red = merchant["variants"]["red"]

        order = OrderFactory(shipping_country="US")
        oi = OrderItemFactory(
            order=order,
            product=variable,
            variant=variant_red,
            quantity=5,
            product_name="T-Shirt Red",
            sku="TSHIRT-RED",
        )

        stock = fulfillment_svc.allocate_stock(oi, wh_us)

        assert stock is not None
        stock.refresh_from_db()
        assert stock.allocated == 5
        assert stock.variant == variant_red

    def test_allocate_stock_no_variant_simple_product(self, fulfillment_svc, merchant):
        """Simple product allocation doesn't crash with MultipleObjectsReturned."""
        wh_us = merchant["warehouses"]["us"]
        product_a = merchant["products"]["a"]

        order = OrderFactory(shipping_country="US")
        oi = OrderItemFactory(
            order=order,
            product=product_a,
            quantity=3,
            product_name="Widget A",
            sku=product_a.sku,
        )

        stock = fulfillment_svc.allocate_stock(oi, wh_us)

        assert stock is not None
        stock.refresh_from_db()
        assert stock.allocated == 3

    def test_allocate_stock_wrong_variant_raises(self, fulfillment_svc, merchant):
        """Variant with no stock -> InsufficientStockError."""
        wh_us = merchant["warehouses"]["us"]
        variable = merchant["products"]["variable"]
        variant_blue = merchant["variants"]["blue"]

        # Blue has 0 at US warehouse
        order = OrderFactory(shipping_country="US")
        oi = OrderItemFactory(
            order=order,
            product=variable,
            variant=variant_blue,
            quantity=1,
            product_name="T-Shirt Blue",
            sku="TSHIRT-BLUE",
        )

        with pytest.raises(InsufficientStockError):
            fulfillment_svc.allocate_stock(oi, wh_us)

    def test_fulfill_stock_with_variant(self, fulfillment_svc, merchant):
        """on_hand and allocated decremented on correct variant's StockItem."""
        wh_us = merchant["warehouses"]["us"]
        variable = merchant["products"]["variable"]
        variant_red = merchant["variants"]["red"]

        # Pre-allocate
        StockItem.objects.filter(
            product=variable,
            warehouse=wh_us,
            variant=variant_red,
        ).update(allocated=10)

        order = OrderFactory(shipping_country="US")
        oi = OrderItemFactory(
            order=order,
            product=variable,
            variant=variant_red,
            quantity=10,
            product_name="T-Shirt Red",
            sku="TSHIRT-RED",
        )

        stock = fulfillment_svc.fulfill_stock(oi, wh_us)

        stock.refresh_from_db()
        assert stock.on_hand == 40  # 50 - 10
        assert stock.allocated == 0  # 10 - 10

    def test_release_stock_with_variant(self, fulfillment_svc, merchant):
        """allocated decremented on correct variant's StockItem."""
        wh_us = merchant["warehouses"]["us"]
        variable = merchant["products"]["variable"]
        variant_red = merchant["variants"]["red"]

        # Pre-allocate
        StockItem.objects.filter(
            product=variable,
            warehouse=wh_us,
            variant=variant_red,
        ).update(allocated=5)

        order = OrderFactory(shipping_country="US")
        oi = OrderItemFactory(
            order=order,
            product=variable,
            variant=variant_red,
            quantity=5,
            product_name="T-Shirt Red",
            sku="TSHIRT-RED",
        )

        stock = fulfillment_svc.release_stock(oi, wh_us)

        stock.refresh_from_db()
        assert stock.on_hand == 50  # unchanged
        assert stock.allocated == 0  # 5 - 5

    def test_single_warehouse_checks_variant_stock(self, fulfillment_svc, merchant):
        """Warehouse only selected if it has the specific variant stock."""
        wh_us = merchant["warehouses"]["us"]
        variable = merchant["products"]["variable"]
        variant_red = merchant["variants"]["red"]

        order = OrderFactory(shipping_country="US")
        order_items = [
            {"product": variable, "variant": variant_red, "quantity": 10},
        ]

        with patch.object(fulfillment_svc, "_geocode_order_address", return_value=None):
            allocation = fulfillment_svc.select_warehouse_for_order(order, order_items)

        # Red is only at US (50 units), not at EU (0 units)
        assert allocation[0] == wh_us

    def test_split_shipment_checks_variant_stock(self, fulfillment_svc, merchant):
        """Each variant routed to warehouse with its stock."""
        wh_us = merchant["warehouses"]["us"]
        wh_eu = merchant["warehouses"]["eu"]
        variable = merchant["products"]["variable"]
        variant_red = merchant["variants"]["red"]
        variant_blue = merchant["variants"]["blue"]

        # Use AU shipping — fallback chain gives both warehouses (EU priority 0, US priority 1)
        order = OrderFactory(shipping_country="AU")
        order_items = [
            {"product": variable, "variant": variant_red, "quantity": 10},
            {"product": variable, "variant": variant_blue, "quantity": 10},
        ]

        with patch.object(fulfillment_svc, "_geocode_order_address", return_value=None):
            allocation = fulfillment_svc.select_warehouse_for_order(order, order_items)

        # Red: 50 at US, 0 at EU. Blue: 0 at US, 40 at EU.
        # EU-WEST is first in fallback order: Red 0 (skip), Blue 40 (allocate)
        # US-EAST is second: Red 50 (allocate)
        assert allocation[0] == wh_us  # Red at US
        assert allocation[1] == wh_eu  # Blue at EU


# ============================================================
# C. Currency Handling (Bug 3)
# ============================================================


class TestCurrencyHandling:
    """Test that shipping cost calculations use correct currency."""

    def test_calculate_shipping_uses_method_currency(self, site_settings):
        """EUR flat_rate -> _resolve_currency returns 'EUR'."""
        from shipping.services.rule_service import ShippingPromotionService

        zone = ShippingZoneFactory(name="EU Zone", countries=["DE"])
        method = ShippingMethodFactory(
            name="EU Standard",
            flat_rate_cost=Decimal("9.99"),
            flat_rate_cost_currency="EUR",
            zones=[zone],
        )

        currency = ShippingPromotionService._resolve_currency(method)
        assert str(currency) == "EUR"

    def test_calculate_shipping_fallback_to_site_currency(self, site_settings):
        """No flat_rate cost -> falls back to SiteSettings.default_currency."""
        from core.models import SiteSettings
        from shipping.services.rule_service import ShippingPromotionService

        # Use .filter().update() to bypass SiteSettings.clean() validation
        SiteSettings.objects.filter(pk=site_settings.pk).update(default_currency="GBP")
        site_settings.refresh_from_db()

        method = MagicMock()
        method.flat_rate_cost = None

        currency = ShippingPromotionService._resolve_currency(method)
        assert str(currency) == "GBP"

    def test_calculate_shipping_ultimate_fallback_usd(self):
        """No method cost, no site settings -> USD fallback."""
        from shipping.services.rule_service import ShippingPromotionService

        # Mock a method with no flat_rate_cost attribute
        method = MagicMock(spec=[])

        # Patch SiteSettings.objects.first() to return None so it falls through to USD
        with patch("core.models.SiteSettings.objects") as mock_objects:
            mock_objects.first.return_value = None
            currency = ShippingPromotionService._resolve_currency(method)

        assert str(currency) == "USD"

    def test_apply_rules_to_cost_uses_correct_currency(self, site_settings):
        """Rules applied with correct currency from method."""
        from djmoney.money import Money

        from shipping.services.rule_service import ShippingPromotionService

        zone = ShippingZoneFactory(name="EU Rules Zone", countries=["DE"])
        method = ShippingMethodFactory(
            name="EU Method",
            flat_rate_cost=Decimal("15.00"),
            flat_rate_cost_currency="EUR",
            zones=[zone],
        )

        # apply_rules_to_cost wraps base_cost in Money with resolved currency
        result = ShippingPromotionService.apply_rules_to_cost(
            base_cost=Decimal("15.00"),
            shipping_method=method,
            cart=MagicMock(subtotal=Money(Decimal("100.00"), "EUR")),
            address={"country": "DE"},
        )

        # Result should be Decimal, and no crash means currency resolved correctly
        assert isinstance(result, Decimal)
        assert result >= Decimal("0")

    def test_resolve_currency_prefers_method_over_site(self, site_settings):
        """Method currency takes priority over site default."""
        from core.models import SiteSettings
        from shipping.services.rule_service import ShippingPromotionService

        # Use .filter().update() to bypass SiteSettings.clean() validation
        SiteSettings.objects.filter(pk=site_settings.pk).update(default_currency="GBP")
        site_settings.refresh_from_db()

        zone = ShippingZoneFactory(name="JPY Zone", countries=["JP"])
        method = ShippingMethodFactory(
            name="JP Method",
            flat_rate_cost=Decimal("1500"),
            flat_rate_cost_currency="JPY",
            zones=[zone],
        )

        currency = ShippingPromotionService._resolve_currency(method)
        assert str(currency) == "JPY"  # Method currency, not site GBP
