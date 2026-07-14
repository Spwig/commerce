"""
POS Catalog API integration tests.

Tests for product list/detail/barcode lookup and category list endpoints
served at /api/pos/products/ and /api/pos/categories/.
"""

from decimal import Decimal

import pytest

from catalog.models import ProductVariant
from tests.factories import (
    CategoryFactory,
    ProductFactory,
    StockItemFactory,
)
from tests.helpers import assert_pos_error, assert_pos_success

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.pos]

PRODUCTS_URL = "/api/pos/products/"
CATEGORIES_URL = "/api/pos/categories/"


def _product_detail_url(product_id):
    return f"/api/pos/products/{product_id}/"


def _barcode_url(barcode):
    return f"/api/pos/products/barcode/{barcode}/"


# ============================================================
# Product List
# ============================================================


class TestProductList:
    """GET /api/pos/products/ — paginated product list for POS."""

    def test_list_returns_published_products(
        self,
        pos_client,
        product_with_stock,
        site_settings,
    ):
        """Only published products with sales_channel 'all' or 'pos_only' are returned."""
        # product_with_stock is published + sales_channel='all' (default)
        pos_only = ProductFactory(
            name="POS Only Item",
            slug="pos-only-item",
            sales_channel="pos_only",
        )
        # online-only should be excluded
        ProductFactory(
            name="Online Only Item",
            slug="online-only-item",
            sales_channel="online_only",
        )

        data = assert_pos_success(pos_client.get(PRODUCTS_URL))

        returned_ids = {p["id"] for p in data["results"]}
        assert product_with_stock.id in returned_ids
        assert pos_only.id in returned_ids

    def test_excludes_draft_products(
        self,
        pos_client,
        product_with_stock,
        site_settings,
    ):
        """Draft and inactive products are not returned in the list."""
        draft = ProductFactory(
            name="Draft Product",
            slug="draft-product",
            status="draft",
        )

        data = assert_pos_success(pos_client.get(PRODUCTS_URL))

        returned_ids = {p["id"] for p in data["results"]}
        assert draft.id not in returned_ids
        # The published product should still appear
        assert product_with_stock.id in returned_ids

    def test_search_by_name(
        self,
        pos_client,
        site_settings,
    ):
        """?q= filters by product name (case-insensitive)."""
        target = ProductFactory(name="Organic Honey Jar", slug="organic-honey-jar")
        other = ProductFactory(name="Steel Mug", slug="steel-mug")

        data = assert_pos_success(pos_client.get(PRODUCTS_URL, {"q": "honey"}))

        returned_ids = {p["id"] for p in data["results"]}
        assert target.id in returned_ids
        assert other.id not in returned_ids

    def test_search_by_sku(
        self,
        pos_client,
        site_settings,
    ):
        """?q= filters by SKU."""
        target = ProductFactory(
            name="SKU Search Target",
            slug="sku-search-target",
            sku="UNIQUE-SKU-999",
        )
        ProductFactory(name="Other Item", slug="other-item-sku-test")

        data = assert_pos_success(pos_client.get(PRODUCTS_URL, {"q": "UNIQUE-SKU-999"}))

        returned_ids = {p["id"] for p in data["results"]}
        assert target.id in returned_ids

    def test_search_by_barcode(
        self,
        pos_client,
        product_with_barcode,
        site_settings,
    ):
        """?q= filters by barcode."""
        data = assert_pos_success(pos_client.get(PRODUCTS_URL, {"q": "1234567890123"}))

        returned_ids = {p["id"] for p in data["results"]}
        assert product_with_barcode.id in returned_ids

    def test_filter_by_category(
        self,
        pos_client,
        category,
        product_with_stock,
        site_settings,
    ):
        """?category= filters by category ID."""
        other_category = CategoryFactory(name="Other Category", slug="other-category")
        other_product = ProductFactory(
            name="Other Category Product",
            slug="other-category-product",
            category=other_category,
        )

        data = assert_pos_success(pos_client.get(PRODUCTS_URL, {"category": category.id}))

        returned_ids = {p["id"] for p in data["results"]}
        assert product_with_stock.id in returned_ids
        assert other_product.id not in returned_ids

    def test_pagination(self, pos_client, site_settings):
        """Response includes pagination info (count, page, page_size, total_pages)."""
        # Create enough products to verify pagination metadata
        for i in range(3):
            ProductFactory(
                name=f"Page Test Product {i}",
                slug=f"page-test-product-{i}",
            )

        data = assert_pos_success(pos_client.get(PRODUCTS_URL, {"page": 1, "page_size": 2}))

        assert "count" in data
        assert "page" in data
        assert "page_size" in data
        assert "total_pages" in data
        assert data["page"] == 1
        assert data["page_size"] == 2
        assert data["count"] >= 3
        assert data["total_pages"] >= 2
        assert len(data["results"]) == 2

    def test_includes_stock_for_terminal_warehouse(
        self,
        pos_client,
        product_with_stock,
        warehouse,
        site_settings,
    ):
        """Stock quantity is shown for the terminal's warehouse."""
        data = assert_pos_success(pos_client.get(PRODUCTS_URL))

        matching = [p for p in data["results"] if p["id"] == product_with_stock.id]
        assert len(matching) == 1
        product_data = matching[0]
        assert product_data["stock_available"] == 50
        assert product_data["track_inventory"] is True


# ============================================================
# Product Detail
# ============================================================


class TestProductDetail:
    """GET /api/pos/products/<id>/ — full product details."""

    def test_simple_product_detail(
        self,
        pos_client,
        product_with_stock,
        site_settings,
    ):
        """Returns full product info for a simple product."""
        data = assert_pos_success(pos_client.get(_product_detail_url(product_with_stock.id)))

        product = data["product"]
        assert product["id"] == product_with_stock.id
        assert product["name"] == "Stocked Widget"
        assert product["sku"] == product_with_stock.sku
        assert product["product_type"] == "simple"
        assert "price" in product
        assert "currency" in product

    def test_product_not_found(self, pos_client, site_settings):
        """404 for a non-existent product ID."""
        assert_pos_error(
            pos_client.get(_product_detail_url(999999)),
            error_code="NOT_FOUND",
            http_status=404,
        )

    def test_draft_product_not_found(self, pos_client, site_settings):
        """Draft product returns 404 — not visible through POS."""
        draft = ProductFactory(
            name="Hidden Draft",
            slug="hidden-draft",
            status="draft",
        )

        assert_pos_error(
            pos_client.get(_product_detail_url(draft.id)),
            error_code="NOT_FOUND",
            http_status=404,
        )

    def test_includes_variants(
        self,
        pos_client,
        category,
        warehouse,
        site_settings,
    ):
        """Variable product returns variant info with the detail response."""
        variable = ProductFactory(
            name="Variable Tee",
            slug="variable-tee",
            category=category,
            product_type="variable",
            price=Decimal("30.00"),
            track_inventory=True,
        )
        variant = ProductVariant.objects.create(
            product=variable,
            name="Large / Red",
            sku="VTEE-LG-RED",
            barcode="9999888877776",
            is_active=True,
        )
        StockItemFactory(
            product=variable,
            variant=variant,
            warehouse=warehouse,
            on_hand=20,
        )

        data = assert_pos_success(pos_client.get(_product_detail_url(variable.id)))

        product = data["product"]
        assert product["has_variants"] is True
        assert "variants" in product
        assert len(product["variants"]) == 1

        v = product["variants"][0]
        assert v["id"] == variant.id
        assert v["sku"] == "VTEE-LG-RED"
        assert v["stock_available"] == 20


# ============================================================
# Barcode Lookup
# ============================================================


class TestBarcodeLookup:
    """GET /api/pos/products/barcode/<barcode>/ — barcode scan."""

    def test_lookup_by_product_barcode(
        self,
        pos_client,
        product_with_barcode,
        site_settings,
    ):
        """Finds a product by its barcode field."""
        data = assert_pos_success(pos_client.get(_barcode_url("1234567890123")))

        assert data["product"]["id"] == product_with_barcode.id
        assert data["variant_id"] is None

    def test_lookup_by_sku_fallback(
        self,
        pos_client,
        site_settings,
    ):
        """If no barcode match, falls back to SKU lookup."""
        product = ProductFactory(
            name="SKU Fallback Product",
            slug="sku-fallback-product",
            sku="FALLBACK-SKU-42",
            barcode="",  # no barcode
        )

        data = assert_pos_success(pos_client.get(_barcode_url("FALLBACK-SKU-42")))

        assert data["product"]["id"] == product.id

    def test_barcode_not_found(self, pos_client, site_settings):
        """Returns 404 for an unknown barcode."""
        assert_pos_error(
            pos_client.get(_barcode_url("0000000000000")),
            error_code="NOT_FOUND",
            http_status=404,
        )

    def test_returns_product_data(
        self,
        pos_client,
        product_with_barcode,
        site_settings,
    ):
        """Response includes full product details (name, price, sku, etc.)."""
        data = assert_pos_success(pos_client.get(_barcode_url("1234567890123")))

        product = data["product"]
        assert product["name"] == "Barcode Widget"
        assert product["sku"] == product_with_barcode.sku
        assert "price" in product
        assert "currency" in product
        assert product["barcode"] == "1234567890123"


# ============================================================
# Category List
# ============================================================


class TestCategoryList:
    """GET /api/pos/categories/ — category navigation list."""

    def test_returns_active_categories(
        self,
        pos_client,
        category,
        site_settings,
    ):
        """Lists active categories."""
        data = assert_pos_success(pos_client.get(CATEGORIES_URL))

        returned_ids = {c["id"] for c in data["categories"]}
        assert category.id in returned_ids

    def test_excludes_inactive_categories(
        self,
        pos_client,
        category,
        site_settings,
    ):
        """Inactive categories are not listed."""
        inactive = CategoryFactory(
            name="Inactive Category",
            slug="inactive-category",
            is_active=False,
        )

        data = assert_pos_success(pos_client.get(CATEGORIES_URL))

        returned_ids = {c["id"] for c in data["categories"]}
        assert category.id in returned_ids
        assert inactive.id not in returned_ids

    def test_includes_parent_id(
        self,
        pos_client,
        category,
        site_settings,
    ):
        """Category response includes parent_id for tree building."""
        child = CategoryFactory(
            name="Child Category",
            slug="child-category",
            parent=category,
        )

        data = assert_pos_success(pos_client.get(CATEGORIES_URL))

        child_data = next((c for c in data["categories"] if c["id"] == child.id), None)
        assert child_data is not None
        assert child_data["parent_id"] == category.id

        parent_data = next((c for c in data["categories"] if c["id"] == category.id), None)
        assert parent_data is not None
        assert parent_data["parent_id"] is None
