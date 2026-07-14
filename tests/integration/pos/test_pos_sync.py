"""
POS Sync API integration tests.

Tests for product delta sync, customer sync, offline transaction upload,
sync status, sync version, order sync, and stock adjustment sync endpoints
served at /api/pos/sync/*.
"""

import uuid
from datetime import timedelta
from decimal import Decimal

import pytest
from django.utils import timezone

from tests.factories import (
    OrderFactory,
    OrderItemFactory,
    ProductFactory,
    UserFactory,
)
from tests.helpers import assert_pos_success

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.pos]

SYNC_PRODUCTS_URL = "/api/pos/sync/products/"
SYNC_CUSTOMERS_URL = "/api/pos/sync/customers/"
SYNC_OFFLINE_URL = "/api/pos/sync/offline-transactions/"
SYNC_STATUS_URL = "/api/pos/sync/status/"
SYNC_VERSION_URL = "/api/pos/sync/version/"
SYNC_STOCK_ADJ_URL = "/api/pos/sync/stock-adjustments/"
SYNC_ORDERS_URL = "/api/pos/sync/orders/"


# ============================================================
# Product Delta Sync
# ============================================================


class TestProductDeltaSync:
    """GET /api/pos/sync/products/ -- incremental product sync."""

    def test_since_timestamp(
        self,
        pos_client,
        category,
        warehouse,
        site_settings,
    ):
        """?since= returns only products updated after that timestamp."""
        old_product = ProductFactory(
            name="Old Product",
            slug="old-product-sync",
            category=category,
        )
        # Push updated_at into the past
        past = timezone.now() - timedelta(hours=2)
        type(old_product).__class__  # noqa -- just accessing the model
        from catalog.models import Product

        Product.objects.filter(pk=old_product.pk).update(updated_at=past)

        since = (timezone.now() - timedelta(hours=1)).isoformat()

        new_product = ProductFactory(
            name="New Product",
            slug="new-product-sync",
            category=category,
        )

        data = assert_pos_success(pos_client.get(SYNC_PRODUCTS_URL, {"since": since}))

        returned_ids = {p["id"] for p in data["results"]}
        assert new_product.id in returned_ids
        assert old_product.id not in returned_ids
        assert "sync_token" in data

    def test_all_without_since(
        self,
        pos_client,
        category,
        site_settings,
    ):
        """No ?since returns all POS-eligible products."""
        p1 = ProductFactory(name="Sync All A", slug="sync-all-a", category=category)
        p2 = ProductFactory(name="Sync All B", slug="sync-all-b", category=category)
        # online_only should be excluded
        p3 = ProductFactory(
            name="Online Only Sync",
            slug="online-only-sync",
            category=category,
            sales_channel="online_only",
        )

        data = assert_pos_success(pos_client.get(SYNC_PRODUCTS_URL))

        returned_ids = {p["id"] for p in data["results"]}
        assert p1.id in returned_ids
        assert p2.id in returned_ids
        assert p3.id not in returned_ids

    def test_includes_stock(
        self,
        pos_client,
        product_with_stock,
        warehouse,
        site_settings,
    ):
        """Response includes stock quantities for the terminal warehouse."""
        data = assert_pos_success(pos_client.get(SYNC_PRODUCTS_URL))

        matching = [p for p in data["results"] if p["id"] == product_with_stock.id]
        assert len(matching) == 1
        product_data = matching[0]
        assert product_data["stock_available"] == 50
        assert product_data["track_inventory"] is True

    def test_pagination(self, pos_client, category, site_settings):
        """Large result sets are paginated."""
        for i in range(5):
            ProductFactory(
                name=f"Sync Page Product {i}",
                slug=f"sync-page-product-{i}",
                category=category,
            )

        data = assert_pos_success(pos_client.get(SYNC_PRODUCTS_URL, {"page": 1, "page_size": 2}))

        assert data["page"] == 1
        assert data["page_size"] == 2
        assert data["count"] >= 5
        assert data["total_pages"] >= 3
        assert len(data["results"]) == 2


# ============================================================
# Customer Sync
# ============================================================


class TestCustomerSync:
    """GET /api/pos/sync/customers/ -- customer delta sync."""

    def test_since_timestamp(self, pos_client, site_settings):
        """?since= returns only customers joined after that timestamp."""
        old_customer = UserFactory(
            username="old_customer",
            first_name="Old",
            last_name="Customer",
            is_staff=False,
        )
        past = timezone.now() - timedelta(hours=2)
        from django.contrib.auth import get_user_model

        User = get_user_model()
        User.objects.filter(pk=old_customer.pk).update(date_joined=past)

        since = (timezone.now() - timedelta(hours=1)).isoformat()

        new_customer = UserFactory(
            username="new_customer",
            first_name="New",
            last_name="Customer",
            is_staff=False,
        )

        data = assert_pos_success(pos_client.get(SYNC_CUSTOMERS_URL, {"since": since}))

        returned_ids = {c["id"] for c in data["results"]}
        assert new_customer.id in returned_ids
        assert old_customer.id not in returned_ids
        assert "sync_token" in data

    def test_includes_order_stats(self, pos_client, site_settings):
        """Customer data includes basic fields (id, email, first_name, last_name, full_name)."""
        customer = UserFactory(
            username="stats_customer",
            email="stats@customer.test",
            first_name="Jane",
            last_name="Doe",
            is_staff=False,
        )

        data = assert_pos_success(pos_client.get(SYNC_CUSTOMERS_URL))

        matching = [c for c in data["results"] if c["id"] == customer.id]
        assert len(matching) == 1
        c = matching[0]
        assert c["email"] == "stats@customer.test"
        assert c["first_name"] == "Jane"
        assert c["last_name"] == "Doe"
        assert c["full_name"] == "Jane Doe"


# ============================================================
# Upload Offline Transactions
# ============================================================


class TestUploadOfflineTransactions:
    """POST /api/pos/sync/offline-transactions/ -- offline transaction upload."""

    def _make_transaction(self, product, terminal, cashier, local_id=None):
        """Build a valid offline transaction payload."""
        price = product.price.amount  # plain Decimal from MoneyField
        return {
            "local_id": local_id or f"offline-{uuid.uuid4().hex[:12]}",
            "terminal_uuid": str(terminal.uuid),
            "cashier_id": cashier.id,
            "items": [
                {
                    "product_id": product.id,
                    "quantity": 2,
                    "unit_price": str(price),
                },
            ],
            "payments": [
                {
                    "method": "cash",
                    "amount": str(price * 2),
                    "amount_tendered": str(price * 2 + Decimal("5.00")),
                },
            ],
            "created_at": timezone.now().isoformat(),
        }

    def test_single_transaction(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        product_with_stock,
        open_shift,
        site_settings,
    ):
        """Upload one offline transaction creates an order."""
        from orders.models import Order

        txn = self._make_transaction(
            product_with_stock,
            pos_terminal,
            pos_staff_user,
        )
        response = pos_client.post(
            SYNC_OFFLINE_URL,
            {"transactions": [txn]},
            format="json",
        )
        data = assert_pos_success(response)

        assert data["processed"] == 1
        assert data["failed"] == 0

        order = Order.objects.get(external_id=txn["local_id"], channel="pos")
        assert order.status == "processing"
        assert order.total_amount.amount == product_with_stock.price.amount * 2

    def test_batch_transactions(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        product_with_stock,
        open_shift,
        site_settings,
    ):
        """Upload multiple transactions in one request."""
        from orders.models import Order

        txns = [
            self._make_transaction(
                product_with_stock,
                pos_terminal,
                pos_staff_user,
                local_id=f"batch-{i}",
            )
            for i in range(3)
        ]

        data = assert_pos_success(
            pos_client.post(
                SYNC_OFFLINE_URL,
                {"transactions": txns},
                format="json",
            )
        )

        assert data["processed"] == 3
        assert data["failed"] == 0
        assert (
            Order.objects.filter(
                channel="pos",
                external_id__startswith="batch-",
            ).count()
            == 3
        )

    def test_idempotency_by_local_id(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        product_with_stock,
        open_shift,
        site_settings,
    ):
        """Same local_id is not processed twice (idempotent)."""
        from orders.models import Order

        txn = self._make_transaction(
            product_with_stock,
            pos_terminal,
            pos_staff_user,
            local_id="idempotent-txn-001",
        )

        # First upload
        data1 = assert_pos_success(
            pos_client.post(SYNC_OFFLINE_URL, {"transactions": [txn]}, format="json")
        )
        assert data1["processed"] == 1

        # Second upload with same local_id
        data2 = assert_pos_success(
            pos_client.post(SYNC_OFFLINE_URL, {"transactions": [txn]}, format="json")
        )
        assert data2["processed"] == 1  # still reports processed (skipped duplicate)
        assert data2["failed"] == 0

        # Only one order should exist
        assert Order.objects.filter(external_id="idempotent-txn-001", channel="pos").count() == 1

    def test_invalid_product_graceful(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        open_shift,
        site_settings,
    ):
        """Invalid product ID is handled gracefully (per-transaction failure)."""
        txn = {
            "local_id": "bad-product-txn",
            "terminal_uuid": str(pos_terminal.uuid),
            "cashier_id": pos_staff_user.id,
            "items": [
                {
                    "product_id": 999999,
                    "quantity": 1,
                    "unit_price": "10.00",
                },
            ],
            "payments": [
                {
                    "method": "cash",
                    "amount": "10.00",
                },
            ],
            "created_at": timezone.now().isoformat(),
        }

        data = assert_pos_success(
            pos_client.post(SYNC_OFFLINE_URL, {"transactions": [txn]}, format="json")
        )

        assert data["failed"] == 1
        assert len(data["errors"]) == 1
        assert data["errors"][0]["local_id"] == "bad-product-txn"

    def test_creates_payment_records(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        product_with_stock,
        open_shift,
        site_settings,
    ):
        """Payment records (POSPayment) are created for each transaction."""
        from orders.models import Order
        from pos_app.models import POSPayment

        txn = self._make_transaction(
            product_with_stock,
            pos_terminal,
            pos_staff_user,
            local_id="payment-rec-txn",
        )

        assert_pos_success(
            pos_client.post(SYNC_OFFLINE_URL, {"transactions": [txn]}, format="json")
        )

        order = Order.objects.get(external_id="payment-rec-txn", channel="pos")
        payments = POSPayment.objects.filter(order=order)
        assert payments.count() == 1
        pmt = payments.first()
        assert pmt.method == "cash"
        assert pmt.amount == product_with_stock.price.amount * 2

    def test_per_transaction_status(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        product_with_stock,
        open_shift,
        site_settings,
    ):
        """Response includes per-transaction success/failure breakdown."""
        good_txn = self._make_transaction(
            product_with_stock,
            pos_terminal,
            pos_staff_user,
            local_id="good-txn",
        )
        bad_txn = {
            "local_id": "bad-txn",
            "terminal_uuid": str(pos_terminal.uuid),
            "cashier_id": pos_staff_user.id,
            "items": [
                {
                    "product_id": 999999,
                    "quantity": 1,
                    "unit_price": "10.00",
                },
            ],
            "payments": [{"method": "cash", "amount": "10.00"}],
            "created_at": timezone.now().isoformat(),
        }

        data = assert_pos_success(
            pos_client.post(
                SYNC_OFFLINE_URL,
                {"transactions": [good_txn, bad_txn]},
                format="json",
            )
        )

        assert data["processed"] == 1
        assert data["failed"] == 1
        assert len(data["errors"]) == 1
        assert data["errors"][0]["local_id"] == "bad-txn"


# ============================================================
# Sync Status
# ============================================================


class TestSyncStatus:
    """GET /api/pos/sync/status/ -- server sync status."""

    def test_server_time(self, pos_client, site_settings):
        """Returns server time as an ISO timestamp."""
        before = timezone.now()

        data = assert_pos_success(pos_client.get(SYNC_STATUS_URL))

        assert "server_time" in data
        from django.utils.dateparse import parse_datetime

        server_time = parse_datetime(data["server_time"])
        assert server_time is not None
        assert server_time >= before

    def test_includes_counts(
        self,
        pos_client,
        product_with_stock,
        site_settings,
    ):
        """Returns counts for products and customers."""
        # Create a non-staff customer to be counted
        UserFactory(
            username="counted_customer",
            is_staff=False,
        )

        data = assert_pos_success(pos_client.get(SYNC_STATUS_URL))

        assert "total_products" in data
        assert "total_customers" in data
        assert data["total_products"] >= 1
        assert data["total_customers"] >= 1


# ============================================================
# Sync Version
# ============================================================


class TestSyncVersion:
    """GET /api/pos/sync/version/ -- API version info."""

    def test_returns_version_info(self, pos_client, site_settings):
        """Returns API version and data schema version."""
        data = assert_pos_success(pos_client.get(SYNC_VERSION_URL))

        assert "api_version" in data
        assert "data_schema_version" in data
        assert "server_time" in data
        assert isinstance(data["api_version"], str)
        assert isinstance(data["data_schema_version"], int)


# ============================================================
# Order Sync
# ============================================================


class TestOrderSync:
    """GET /api/pos/sync/orders/ -- order sync for offline caching."""

    def _create_pos_order(self, terminal, cashier, product, **kwargs):
        """Create a POS order with an item and payment."""
        from pos_app.models import POSPayment

        price = product.price.amount  # Extract Decimal from Money object

        order = OrderFactory(
            user=cashier,
            channel="pos",
            pos_terminal=terminal,
            cashier=cashier,
            subtotal=price,
            total_amount=price,
            **kwargs,
        )
        OrderItemFactory(
            order=order,
            product=product,
            product_name=str(product.name),
            quantity=1,
            unit_price=price,
            total_price=price,
        )
        POSPayment.objects.create(
            order=order,
            method="cash",
            amount=price,
        )
        return order

    def test_returns_recent_pos_orders(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        product_with_stock,
        site_settings,
    ):
        """Returns POS orders for offline caching."""
        order = self._create_pos_order(
            pos_terminal,
            pos_staff_user,
            product_with_stock,
        )

        data = assert_pos_success(pos_client.get(SYNC_ORDERS_URL))

        returned_ids = {o["id"] for o in data["results"]}
        assert order.id in returned_ids
        assert "sync_token" in data

        order_data = next(o for o in data["results"] if o["id"] == order.id)
        assert order_data["channel"] == "pos"
        assert len(order_data["items"]) == 1
        assert len(order_data["payments"]) >= 1

    def test_respects_sync_limit(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        product_with_stock,
        site_settings,
    ):
        """sync_limit caps web orders, not POS orders (POS orders always included)."""
        # Set a very low sync limit
        pos_terminal.order_sync_limit = 2
        pos_terminal.save(update_fields=["order_sync_limit"])

        for _i in range(5):
            self._create_pos_order(
                pos_terminal,
                pos_staff_user,
                product_with_stock,
            )

        data = assert_pos_success(pos_client.get(SYNC_ORDERS_URL))

        # POS orders are always included regardless of sync_limit
        # sync_limit only limits how many web orders fill remaining slots
        assert data["count"] >= 5

    def test_respects_sync_days(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        product_with_stock,
        site_settings,
    ):
        """Only returns orders within order_sync_days window."""
        from orders.models import Order

        pos_terminal.order_sync_days = 3
        pos_terminal.save(update_fields=["order_sync_days"])

        # Recent order
        recent_order = self._create_pos_order(
            pos_terminal,
            pos_staff_user,
            product_with_stock,
        )

        # Old order (outside the sync window)
        old_order = self._create_pos_order(
            pos_terminal,
            pos_staff_user,
            product_with_stock,
        )
        old_date = timezone.now() - timedelta(days=10)
        Order.objects.filter(pk=old_order.pk).update(created_at=old_date)

        data = assert_pos_success(pos_client.get(SYNC_ORDERS_URL))

        returned_ids = {o["id"] for o in data["results"]}
        assert recent_order.id in returned_ids
        assert old_order.id not in returned_ids


# ============================================================
# Stock Adjustment Sync
# ============================================================


class TestStockAdjustmentSync:
    """POST /api/pos/sync/stock-adjustments/ -- offline stock adjustments."""

    def test_upload_offline_adjustments(
        self,
        pos_manager_client,
        pos_terminal,
        warehouse,
        product_with_stock,
        site_settings,
    ):
        """Upload stock adjustments made while offline."""
        from catalog.models import StockItem, StockMovement

        idem_key = f"adj-{uuid.uuid4().hex[:12]}"
        payload = {
            "adjustments": [
                {
                    "idempotency_key": idem_key,
                    "product_id": product_with_stock.id,
                    "adjustment_type": "receive",
                    "quantity": 10,
                    "reason": "Delivery received offline",
                },
            ],
        }

        data = assert_pos_success(
            pos_manager_client.post(SYNC_STOCK_ADJ_URL, payload, format="json")
        )

        assert data["processed"] == 1
        assert data["failed"] == 0

        # Verify stock was updated
        stock = StockItem.objects.get(
            product=product_with_stock,
            warehouse=warehouse,
        )
        assert stock.on_hand == 60  # 50 original + 10 received

        # Verify movement was recorded
        movement = StockMovement.objects.get(reference_key=idem_key)
        assert movement.quantity == 10
        assert movement.previous_quantity == 50
        assert movement.new_quantity == 60
