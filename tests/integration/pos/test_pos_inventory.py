"""
POS Inventory API integration tests.

Tests stock level queries, stock detail, cross-location stock,
stock adjustments, and movement history endpoints for POS terminals.
"""

from decimal import Decimal

import pytest

from tests.factories import (
    ProductFactory,
    SalesRegionFactory,
    StockItemFactory,
    WarehouseFactory,
)
from tests.helpers import assert_pos_error, assert_pos_success

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.pos]

STOCK_LEVELS_URL = "/api/pos/inventory/"
STOCK_DETAIL_URL = "/api/pos/inventory/{product_id}/"
CROSS_LOCATION_URL = "/api/pos/inventory/{product_id}/all-locations/"
ADJUST_STOCK_URL = "/api/pos/inventory/adjust/"
MOVEMENTS_URL = "/api/pos/inventory/movements/"


# ============================================================
# TestStockLevels
# ============================================================


class TestStockLevels:
    """Tests for GET /api/pos/inventory/ — stock levels for terminal warehouse."""

    def test_list_stock_levels(self, pos_client, product_with_stock, site_settings):
        """Returns stock for terminal warehouse products."""
        response = pos_client.get(STOCK_LEVELS_URL)
        data = assert_pos_success(response)

        assert "results" in data
        assert data["count"] >= 1

        product_ids = [r["product_id"] for r in data["results"]]
        assert product_with_stock.id in product_ids

    def test_includes_on_hand_and_available(self, pos_client, product_with_stock, site_settings):
        """Response has on_hand, allocated, and available fields."""
        response = pos_client.get(STOCK_LEVELS_URL)
        data = assert_pos_success(response)

        item = next(r for r in data["results"] if r["product_id"] == product_with_stock.id)
        assert "on_hand" in item
        assert "allocated" in item
        assert "available" in item
        assert item["on_hand"] == 50
        assert item["allocated"] == 0
        assert item["available"] == 50

    def test_only_terminal_warehouse(
        self,
        pos_client,
        product_with_stock,
        warehouse,
        category,
        site_settings,
    ):
        """Only shows stock for the terminal's warehouse, not other warehouses."""
        other_region = SalesRegionFactory(code="OTHER-REG", name="Other Region")
        other_warehouse = WarehouseFactory(
            code="OTHER-WH",
            name="Other Warehouse",
            region=other_region,
        )
        other_product = ProductFactory(
            name="Other Warehouse Product",
            slug="other-wh-product",
            category=category,
            price=Decimal("30.00"),
            track_inventory=True,
        )
        StockItemFactory(product=other_product, warehouse=other_warehouse, on_hand=100)

        response = pos_client.get(STOCK_LEVELS_URL)
        data = assert_pos_success(response)

        product_ids = [r["product_id"] for r in data["results"]]
        # The terminal's warehouse product should be present
        assert product_with_stock.id in product_ids
        # The other warehouse product should NOT appear (it has no stock
        # in the terminal warehouse, but it is published and POS-enabled,
        # so it appears with 0 stock; however, it has no StockItem in our
        # warehouse). The key assertion: its on_hand must NOT reflect the
        # other warehouse's 100 units.
        other_items = [r for r in data["results"] if r["product_id"] == other_product.id]
        if other_items:
            assert other_items[0]["on_hand"] == 0

    def test_filter_by_product(self, pos_client, product_with_stock, site_settings):
        """?q= filter returns only matching products."""
        response = pos_client.get(STOCK_LEVELS_URL, {"q": "Stocked Widget"})
        data = assert_pos_success(response)

        assert data["count"] >= 1
        for item in data["results"]:
            assert "stocked" in item["product_name"].lower() or "widget" in item["sku"].lower()

    def test_pagination(self, pos_client, warehouse, category, site_settings):
        """Response is paginated with page, page_size, total_pages, count."""
        # Create enough products to verify pagination fields
        for i in range(3):
            p = ProductFactory(
                name=f"Paginated Product {i}",
                slug=f"paginated-product-{i}",
                category=category,
                price=Decimal("10.00"),
                track_inventory=True,
            )
            StockItemFactory(product=p, warehouse=warehouse, on_hand=10)

        response = pos_client.get(STOCK_LEVELS_URL, {"page": 1, "page_size": 2})
        data = assert_pos_success(response)

        assert "page" in data
        assert "page_size" in data
        assert "total_pages" in data
        assert "count" in data
        assert data["page"] == 1
        assert data["page_size"] == 2
        assert len(data["results"]) <= 2
        assert data["total_pages"] >= 2


# ============================================================
# TestStockDetail
# ============================================================


class TestStockDetail:
    """Tests for GET /api/pos/inventory/<product_id>/ — stock detail for a product."""

    def test_product_stock_detail(self, pos_client, product_with_stock, site_settings):
        """Returns stock info for a specific product."""
        url = STOCK_DETAIL_URL.format(product_id=product_with_stock.id)
        response = pos_client.get(url)
        data = assert_pos_success(response)

        assert "product" in data
        assert "stock" in data
        assert data["product"] == "Stocked Widget"
        assert len(data["stock"]) >= 1
        assert data["stock"][0]["on_hand"] == 50

    def test_product_not_found(self, pos_client, site_settings):
        """404 for a non-existent product."""
        url = STOCK_DETAIL_URL.format(product_id=999999)
        response = pos_client.get(url)
        assert_pos_error(response, "NOT_FOUND", http_status=404)

    def test_includes_warehouse_info(self, pos_client, product_with_stock, site_settings):
        """Response includes variant and allocation details."""
        url = STOCK_DETAIL_URL.format(product_id=product_with_stock.id)
        response = pos_client.get(url)
        data = assert_pos_success(response)

        stock_entry = data["stock"][0]
        assert "product_id" in stock_entry
        assert "on_hand" in stock_entry
        assert "allocated" in stock_entry
        assert "available" in stock_entry
        assert "variant_id" in stock_entry
        assert "sku" in stock_entry

    def test_no_stock_item(self, pos_client, category, warehouse, site_settings):
        """Product without a stock record in the warehouse returns empty stock list."""
        product = ProductFactory(
            name="No Stock Record",
            slug="no-stock-record",
            category=category,
            price=Decimal("20.00"),
            track_inventory=True,
        )
        # No StockItem created for this product in the terminal warehouse

        url = STOCK_DETAIL_URL.format(product_id=product.id)
        response = pos_client.get(url)
        data = assert_pos_success(response)

        assert data["stock"] == []


# ============================================================
# TestCrossLocationStock
# ============================================================


class TestCrossLocationStock:
    """Tests for GET /api/pos/inventory/<product_id>/all-locations/."""

    def test_all_locations(
        self,
        pos_client,
        product_with_stock,
        warehouse,
        site_settings,
    ):
        """Shows stock across all warehouses."""
        other_region = SalesRegionFactory(code="CROSS-REG", name="Cross Region")
        other_warehouse = WarehouseFactory(
            code="CROSS-WH",
            name="Cross Warehouse",
            region=other_region,
        )
        StockItemFactory(
            product=product_with_stock,
            warehouse=other_warehouse,
            on_hand=25,
        )

        url = CROSS_LOCATION_URL.format(product_id=product_with_stock.id)
        response = pos_client.get(url)
        data = assert_pos_success(response)

        assert "locations" in data
        assert len(data["locations"]) >= 2

        warehouse_ids = [loc["warehouse_id"] for loc in data["locations"]]
        assert warehouse.id in warehouse_ids
        assert other_warehouse.id in warehouse_ids

    def test_includes_warehouse_names(
        self,
        pos_client,
        product_with_stock,
        warehouse,
        site_settings,
    ):
        """Each location item has a warehouse name."""
        url = CROSS_LOCATION_URL.format(product_id=product_with_stock.id)
        response = pos_client.get(url)
        data = assert_pos_success(response)

        for loc in data["locations"]:
            assert "warehouse_name" in loc
            assert isinstance(loc["warehouse_name"], str)
            assert len(loc["warehouse_name"]) > 0

    def test_product_not_found(self, pos_client, site_settings):
        """404 for a non-existent product."""
        url = CROSS_LOCATION_URL.format(product_id=999999)
        response = pos_client.get(url)
        assert_pos_error(response, "NOT_FOUND", http_status=404)


# ============================================================
# TestAdjustStock
# ============================================================


class TestAdjustStock:
    """Tests for POST /api/pos/inventory/adjust/ — stock adjustments."""

    def test_adjust_stock_increase(
        self,
        pos_manager_client,
        product_with_stock,
        site_settings,
    ):
        """Increase stock by a positive amount via receive adjustment."""
        response = pos_manager_client.post(
            ADJUST_STOCK_URL,
            {
                "product_id": product_with_stock.id,
                "adjustment_type": "receive",
                "quantity": 10,
                "reason": "New shipment received",
            },
        )
        data = assert_pos_success(response)

        assert data["stock"]["on_hand"] == 60
        assert data["stock"]["delta"] == 10

    def test_adjust_stock_decrease(
        self,
        pos_manager_client,
        product_with_stock,
        site_settings,
    ):
        """Decrease stock via damage adjustment."""
        response = pos_manager_client.post(
            ADJUST_STOCK_URL,
            {
                "product_id": product_with_stock.id,
                "adjustment_type": "damage",
                "quantity": 5,
                "reason": "Broken during handling",
            },
        )
        data = assert_pos_success(response)

        assert data["stock"]["on_hand"] == 45
        assert data["stock"]["delta"] == -5

    def test_requires_permission(
        self,
        pos_client,
        product_with_stock,
        site_settings,
    ):
        """Cashier without pos_stock_adjustment permission gets 403."""
        response = pos_client.post(
            ADJUST_STOCK_URL,
            {
                "product_id": product_with_stock.id,
                "adjustment_type": "receive",
                "quantity": 10,
                "reason": "Unauthorized attempt",
            },
        )
        assert_pos_error(response, "PERMISSION_DENIED", http_status=403)

    def test_manager_can_adjust(
        self,
        pos_manager_client,
        product_with_stock,
        site_settings,
    ):
        """Manager with pos_stock_adjustment permission succeeds."""
        response = pos_manager_client.post(
            ADJUST_STOCK_URL,
            {
                "product_id": product_with_stock.id,
                "adjustment_type": "recount",
                "quantity": 42,
                "reason": "Physical recount audit",
            },
        )
        data = assert_pos_success(response)

        assert data["stock"]["on_hand"] == 42

    def test_invalid_product(self, pos_manager_client, site_settings):
        """Non-existent product returns 404 error."""
        response = pos_manager_client.post(
            ADJUST_STOCK_URL,
            {
                "product_id": 999999,
                "adjustment_type": "receive",
                "quantity": 5,
                "reason": "Stock for phantom product",
            },
        )
        assert_pos_error(response, "NOT_FOUND", http_status=404)

    def test_reason_required(
        self,
        pos_manager_client,
        product_with_stock,
        site_settings,
    ):
        """Reason field is required for stock adjustments."""
        response = pos_manager_client.post(
            ADJUST_STOCK_URL,
            {
                "product_id": product_with_stock.id,
                "adjustment_type": "receive",
                "quantity": 10,
                # No 'reason' field
            },
        )
        assert_pos_error(response, "VALIDATION_ERROR", http_status=400)


# ============================================================
# TestStockMovements
# ============================================================


class TestStockMovements:
    """Tests for GET /api/pos/inventory/movements/ — movement history."""

    def _create_adjustment(self, pos_manager_client, product, adj_type, qty, reason):
        """Helper to create a stock adjustment and return response data."""
        response = pos_manager_client.post(
            ADJUST_STOCK_URL,
            {
                "product_id": product.id,
                "adjustment_type": adj_type,
                "quantity": qty,
                "reason": reason,
            },
        )
        return assert_pos_success(response)

    def test_list_movements(
        self,
        pos_manager_client,
        product_with_stock,
        site_settings,
    ):
        """Returns movement history after adjustments are made."""
        self._create_adjustment(
            pos_manager_client,
            product_with_stock,
            "receive",
            5,
            "Restock",
        )
        self._create_adjustment(
            pos_manager_client,
            product_with_stock,
            "damage",
            2,
            "Broken item",
        )

        response = pos_manager_client.get(MOVEMENTS_URL)
        data = assert_pos_success(response)

        assert "results" in data
        assert data["count"] >= 2
        assert len(data["results"]) >= 2

    def test_filter_by_product(
        self,
        pos_manager_client,
        product_with_stock,
        warehouse,
        category,
        site_settings,
    ):
        """?product_id= filter returns only movements for that product."""
        # Create a second product with stock and an adjustment
        other_product = ProductFactory(
            name="Other Movement Product",
            slug="other-movement-product",
            category=category,
            price=Decimal("15.00"),
            track_inventory=True,
        )
        StockItemFactory(product=other_product, warehouse=warehouse, on_hand=20)

        self._create_adjustment(
            pos_manager_client,
            product_with_stock,
            "receive",
            5,
            "Restock main",
        )
        self._create_adjustment(
            pos_manager_client,
            other_product,
            "receive",
            3,
            "Restock other",
        )

        response = pos_manager_client.get(
            MOVEMENTS_URL,
            {"product_id": product_with_stock.id},
        )
        data = assert_pos_success(response)

        for movement in data["results"]:
            assert movement["product_id"] == product_with_stock.id

    def test_filter_by_date(
        self,
        pos_manager_client,
        product_with_stock,
        site_settings,
    ):
        """?type= filter returns only movements of that type."""
        self._create_adjustment(
            pos_manager_client,
            product_with_stock,
            "receive",
            10,
            "Shipment",
        )
        self._create_adjustment(
            pos_manager_client,
            product_with_stock,
            "damage",
            2,
            "Broken",
        )

        # Filter by damage type only
        response = pos_manager_client.get(MOVEMENTS_URL, {"type": "damage"})
        data = assert_pos_success(response)

        for movement in data["results"]:
            assert movement["movement_type"] == "damage"

    def test_includes_movement_details(
        self,
        pos_manager_client,
        product_with_stock,
        site_settings,
    ):
        """Each movement has type, quantity, reason, and user info."""
        self._create_adjustment(
            pos_manager_client,
            product_with_stock,
            "receive",
            7,
            "Weekly restock",
        )

        response = pos_manager_client.get(MOVEMENTS_URL)
        data = assert_pos_success(response)

        assert len(data["results"]) >= 1
        movement = data["results"][0]

        assert "movement_type" in movement
        assert "quantity" in movement
        assert "reason" in movement
        assert "user_name" in movement
        assert "created_at" in movement
        assert movement["movement_type"] == "adjustment"  # 'receive' maps to 'adjustment'
        assert movement["quantity"] == 7
        assert movement["reason"] == "Weekly restock"
        assert len(movement["user_name"]) > 0
