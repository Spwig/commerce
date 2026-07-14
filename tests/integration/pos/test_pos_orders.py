"""
POS Orders API integration tests.

Tests for order listing, detail, receipt, refund, and void endpoints
served at /api/pos/orders/.
"""

from decimal import Decimal

import pytest
from django.utils import timezone

from tests.factories import (
    OrderFactory,
    OrderItemFactory,
    ProductFactory,
    StockItemFactory,
    UserFactory,
)
from tests.helpers import assert_pos_error, assert_pos_success

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.pos]

ORDERS_URL = "/api/pos/orders/"
CASHIERS_URL = "/api/pos/orders/cashiers/"


def _detail_url(order_id):
    return f"/api/pos/orders/{order_id}/"


def _receipt_url(order_id):
    return f"/api/pos/orders/{order_id}/receipt/"


def _refund_url(order_id):
    return f"/api/pos/orders/{order_id}/refund/"


def _void_url(order_id):
    return f"/api/pos/orders/{order_id}/void/"


def _create_pos_order(pos_terminal, cashier, site_settings, **kwargs):
    """Helper to create a POS order with sensible defaults."""
    defaults = {
        "channel": "pos",
        "pos_terminal": pos_terminal,
        "cashier": cashier,
        "status": "processing",
        "payment_status": "paid",
        "subtotal": Decimal("25.00"),
        "subtotal_currency": "USD",
        "total_amount": Decimal("25.00"),
        "total_amount_currency": "USD",
        "tax_amount": Decimal("0.00"),
        "tax_amount_currency": "USD",
        "discount_amount": Decimal("0.00"),
        "discount_amount_currency": "USD",
    }
    defaults.update(kwargs)
    return OrderFactory(**defaults)


def _create_pos_payment(order, shift, **kwargs):
    """Helper to create a POSPayment record linked to order and shift."""
    from pos_app.models import POSPayment

    defaults = {
        "order": order,
        "shift": shift,
        "method": "cash",
        "amount": order.total_amount.amount
        if hasattr(order.total_amount, "amount")
        else order.total_amount,
    }
    defaults.update(kwargs)
    return POSPayment.objects.create(**defaults)


# ============================================================
# Order List
# ============================================================


class TestOrderList:
    """GET /api/pos/orders/ -- paginated POS order listing."""

    def test_list_pos_orders(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        open_shift,
        site_settings,
    ):
        """Returns POS channel orders for the current terminal and today's date."""
        order = _create_pos_order(pos_terminal, pos_staff_user, site_settings)
        _create_pos_payment(order, open_shift)

        data = assert_pos_success(pos_client.get(ORDERS_URL))

        assert data["count"] >= 1
        order_ids = [r["id"] for r in data["results"]]
        assert order.id in order_ids
        result = next(r for r in data["results"] if r["id"] == order.id)
        assert result["order_number"] == order.order_number
        assert result["channel"] == "pos"

    def test_filter_by_status(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        open_shift,
        site_settings,
    ):
        """?status= filters orders by their status field."""
        processing = _create_pos_order(
            pos_terminal,
            pos_staff_user,
            site_settings,
            status="processing",
        )
        _create_pos_payment(processing, open_shift)

        delivered = _create_pos_order(
            pos_terminal,
            pos_staff_user,
            site_settings,
            status="delivered",
        )
        _create_pos_payment(delivered, open_shift)

        data = assert_pos_success(pos_client.get(ORDERS_URL, {"status": "processing"}))

        result_ids = [r["id"] for r in data["results"]]
        assert processing.id in result_ids
        assert delivered.id not in result_ids

    def test_filter_by_cashier(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        open_shift,
        site_settings,
    ):
        """?cashier_id= filters orders by the cashier who processed them."""
        other_cashier = UserFactory(
            username="other_cashier",
            is_staff=True,
            first_name="Other",
            last_name="Cashier",
        )
        my_order = _create_pos_order(
            pos_terminal,
            pos_staff_user,
            site_settings,
        )
        _create_pos_payment(my_order, open_shift)

        other_order = _create_pos_order(
            pos_terminal,
            other_cashier,
            site_settings,
        )
        _create_pos_payment(other_order, open_shift)

        data = assert_pos_success(pos_client.get(ORDERS_URL, {"cashier_id": pos_staff_user.id}))

        result_ids = [r["id"] for r in data["results"]]
        assert my_order.id in result_ids
        assert other_order.id not in result_ids

    def test_filter_by_date(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        open_shift,
        site_settings,
    ):
        """?date_from= and ?date_to= restrict orders to a date range."""
        from datetime import timedelta

        today = timezone.now()
        old_order = _create_pos_order(
            pos_terminal,
            pos_staff_user,
            site_settings,
        )
        # Backdate the order to 7 days ago
        from orders.models import Order

        Order.objects.filter(pk=old_order.pk).update(
            created_at=today - timedelta(days=7),
        )
        _create_pos_payment(old_order, open_shift)

        today_order = _create_pos_order(
            pos_terminal,
            pos_staff_user,
            site_settings,
        )
        _create_pos_payment(today_order, open_shift)

        # Query only today -- old order should be excluded
        today_str = today.strftime("%Y-%m-%d")
        data = assert_pos_success(
            pos_client.get(
                ORDERS_URL,
                {
                    "date_from": today_str,
                    "date_to": today_str,
                },
            )
        )

        result_ids = [r["id"] for r in data["results"]]
        assert today_order.id in result_ids
        assert old_order.id not in result_ids

    def test_search_by_order_number(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        open_shift,
        site_settings,
    ):
        """?search= finds orders by partial order number match across all dates."""
        order = _create_pos_order(
            pos_terminal,
            pos_staff_user,
            site_settings,
            order_number="SRCH-99887766",
        )
        _create_pos_payment(order, open_shift)

        data = assert_pos_success(pos_client.get(ORDERS_URL, {"search": "SRCH-9988"}))

        result_ids = [r["id"] for r in data["results"]]
        assert order.id in result_ids

    def test_pagination(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        open_shift,
        site_settings,
    ):
        """Response includes pagination metadata."""
        for _i in range(3):
            o = _create_pos_order(pos_terminal, pos_staff_user, site_settings)
            _create_pos_payment(o, open_shift)

        data = assert_pos_success(pos_client.get(ORDERS_URL, {"page": 1, "page_size": 2}))

        assert "count" in data
        assert "page" in data
        assert "page_size" in data
        assert "total_pages" in data
        assert data["page"] == 1
        assert data["page_size"] == 2
        assert len(data["results"]) == 2
        assert data["count"] >= 3


# ============================================================
# Order Detail
# ============================================================


class TestOrderDetail:
    """GET /api/pos/orders/<id>/ -- full order detail."""

    def test_full_detail(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        open_shift,
        site_settings,
        product_with_stock,
    ):
        """Returns complete order data including items."""
        order = _create_pos_order(pos_terminal, pos_staff_user, site_settings)
        OrderItemFactory(
            order=order,
            product=product_with_stock,
            product_name=product_with_stock.name,
            sku=product_with_stock.sku,
            quantity=2,
            unit_price=Decimal("25.00"),
            total_price=Decimal("50.00"),
        )
        _create_pos_payment(order, open_shift)

        data = assert_pos_success(pos_client.get(_detail_url(order.id)))

        assert "order" in data
        o = data["order"]
        assert o["id"] == order.id
        assert o["order_number"] == order.order_number
        assert o["status"] == "processing"
        assert len(o["items"]) == 1
        assert o["items"][0]["product_name"] == product_with_stock.name
        assert o["items"][0]["quantity"] == 2

    def test_not_found(self, pos_client, site_settings):
        """404 for a non-existent order ID."""
        assert_pos_error(
            pos_client.get(_detail_url(999999)),
            "NOT_FOUND",
            http_status=404,
        )


# ============================================================
# Order Receipt
# ============================================================


class TestOrderReceipt:
    """GET /api/pos/orders/<id>/receipt/ -- receipt data for printing."""

    def _make_receipt_order(
        self,
        pos_terminal,
        pos_staff_user,
        open_shift,
        site_settings,
    ):
        """Create a POS order with an item and a cash payment."""
        order = _create_pos_order(
            pos_terminal,
            pos_staff_user,
            site_settings,
            total_amount=Decimal("30.00"),
            subtotal=Decimal("30.00"),
        )
        OrderItemFactory(
            order=order,
            product_name="Widget A",
            quantity=2,
            unit_price=Decimal("15.00"),
            total_price=Decimal("30.00"),
        )
        _create_pos_payment(
            order,
            open_shift,
            method="cash",
            amount=Decimal("30.00"),
            amount_tendered=Decimal("50.00"),
            change_given=Decimal("20.00"),
        )
        return order

    def test_receipt_data(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        open_shift,
        site_settings,
    ):
        """Returns receipt-formatted data with items and totals."""
        order = self._make_receipt_order(
            pos_terminal,
            pos_staff_user,
            open_shift,
            site_settings,
        )

        data = assert_pos_success(pos_client.get(_receipt_url(order.id)))

        assert "receipt" in data
        r = data["receipt"]
        assert r["order_number"] == order.order_number
        assert len(r["items"]) == 1
        assert r["items"][0]["product_name"] == "Widget A"
        assert r["items"][0]["quantity"] == 2
        assert Decimal(r["total"]) == Decimal("30.00")

    def test_includes_store_info(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        open_shift,
        site_settings,
    ):
        """Receipt includes store name from SiteSettings."""
        order = self._make_receipt_order(
            pos_terminal,
            pos_staff_user,
            open_shift,
            site_settings,
        )

        data = assert_pos_success(pos_client.get(_receipt_url(order.id)))
        r = data["receipt"]

        # store_name comes from SiteSettings or ReceiptTemplate
        assert r["store_name"]
        assert r["terminal_name"] == pos_terminal.name
        assert r["cashier_name"]

    def test_includes_payment_details(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        open_shift,
        site_settings,
    ):
        """Receipt shows payment method, amount tendered, and change."""
        order = self._make_receipt_order(
            pos_terminal,
            pos_staff_user,
            open_shift,
            site_settings,
        )

        data = assert_pos_success(pos_client.get(_receipt_url(order.id)))
        r = data["receipt"]

        assert len(r["payments"]) >= 1
        payment = r["payments"][0]
        assert payment["method"] == "cash"
        assert Decimal(payment["amount"]) == Decimal("30.00")
        assert Decimal(payment["amount_tendered"]) == Decimal("50.00")
        assert Decimal(payment["change_given"]) == Decimal("20.00")


# ============================================================
# Refund Order
# ============================================================


class TestRefundOrder:
    """POST /api/pos/orders/<id>/refund/ -- full and partial refunds."""

    def _make_refundable_order(
        self,
        pos_terminal,
        cashier,
        shift,
        site_settings,
        total=Decimal("50.00"),
    ):
        """Create a completed POS order ready for refunding."""
        order = _create_pos_order(
            pos_terminal,
            cashier,
            site_settings,
            status="processing",
            payment_status="paid",
            total_amount=total,
            subtotal=total,
        )
        item = OrderItemFactory(
            order=order,
            quantity=2,
            unit_price=Decimal("25.00"),
            total_price=Decimal("50.00"),
        )
        _create_pos_payment(order, shift, amount=total)
        return order, item

    def test_full_refund(
        self,
        pos_manager_client,
        pos_terminal,
        pos_manager_user,
        manager_open_shift,
        site_settings,
    ):
        """Full refund sets order status to refunded and records the amount."""
        order, _ = self._make_refundable_order(
            pos_terminal,
            pos_manager_user,
            manager_open_shift,
            site_settings,
        )

        resp = pos_manager_client.post(
            _refund_url(order.id),
            {"refund_type": "full", "reason": "customer_request"},
            format="json",
        )
        data = assert_pos_success(resp)

        assert Decimal(data["refund_amount"]) == Decimal("50.00")
        assert data["order"]["status"] == "refunded"
        assert data["order"]["payment_status"] == "refunded"

    def test_partial_refund(
        self,
        pos_manager_client,
        pos_terminal,
        pos_manager_user,
        manager_open_shift,
        site_settings,
    ):
        """Partial refund for specific items updates the order correctly."""
        order, item = self._make_refundable_order(
            pos_terminal,
            pos_manager_user,
            manager_open_shift,
            site_settings,
        )

        resp = pos_manager_client.post(
            _refund_url(order.id),
            {
                "refund_type": "partial",
                "reason": "damaged",
                "items": [{"order_item_id": item.id, "quantity": 1}],
            },
            format="json",
        )
        data = assert_pos_success(resp)

        # Partial refund of 1 item at $25 out of $50 total
        assert Decimal(data["refund_amount"]) == Decimal("25.00")
        assert data["order"]["payment_status"] == "partially_refunded"

    def test_return_to_stock(
        self,
        pos_manager_client,
        pos_terminal,
        pos_manager_user,
        manager_open_shift,
        site_settings,
        warehouse,
        category,
    ):
        """return_to_stock=true restores inventory in the warehouse."""
        product = ProductFactory(
            name="Returnable Widget",
            slug="returnable-widget",
            category=category,
            price=Decimal("25.00"),
            track_inventory=True,
        )
        stock = StockItemFactory(
            product=product,
            warehouse=warehouse,
            on_hand=10,
        )

        order = _create_pos_order(
            pos_terminal,
            pos_manager_user,
            site_settings,
            total_amount=Decimal("50.00"),
            subtotal=Decimal("50.00"),
        )
        item = OrderItemFactory(
            order=order,
            product=product,
            product_name=product.name,
            sku=product.sku,
            quantity=2,
            unit_price=Decimal("25.00"),
            total_price=Decimal("50.00"),
        )
        _create_pos_payment(order, manager_open_shift, amount=Decimal("50.00"))

        resp = pos_manager_client.post(
            _refund_url(order.id),
            {
                "refund_type": "full",
                "reason": "customer_request",
                "return_to_stock": True,
            },
            format="json",
        )
        assert_pos_success(resp)

        stock.refresh_from_db()
        assert stock.on_hand == 12  # 10 original + 2 returned

    def test_requires_permission(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        open_shift,
        site_settings,
    ):
        """Cashier without pos_refund permission gets 403."""
        order, _ = self._make_refundable_order(
            pos_terminal,
            pos_staff_user,
            open_shift,
            site_settings,
        )

        resp = pos_client.post(
            _refund_url(order.id),
            {"refund_type": "full", "reason": "customer_request"},
            format="json",
        )
        assert_pos_error(resp, "PERMISSION_DENIED", http_status=403)

    def test_already_refunded_error(
        self,
        pos_manager_client,
        pos_terminal,
        pos_manager_user,
        manager_open_shift,
        site_settings,
    ):
        """Cannot refund an order that is already fully refunded."""
        order, _ = self._make_refundable_order(
            pos_terminal,
            pos_manager_user,
            manager_open_shift,
            site_settings,
        )
        # Mark as already refunded
        from orders.models import Order

        Order.objects.filter(pk=order.pk).update(status="refunded")

        resp = pos_manager_client.post(
            _refund_url(order.id),
            {"refund_type": "full", "reason": "customer_request"},
            format="json",
        )
        assert_pos_error(resp, "ALREADY_REFUNDED", http_status=400)


# ============================================================
# Void Order
# ============================================================


class TestVoidOrder:
    """POST /api/pos/orders/<id>/void/ -- void an order from the current shift."""

    def _make_voidable_order(
        self,
        pos_terminal,
        cashier,
        shift,
        site_settings,
        total=Decimal("40.00"),
    ):
        """Create a POS order with payment on the given shift."""
        order = _create_pos_order(
            pos_terminal,
            cashier,
            site_settings,
            status="processing",
            payment_status="paid",
            total_amount=total,
            subtotal=total,
        )
        OrderItemFactory(
            order=order,
            quantity=2,
            unit_price=Decimal("20.00"),
            total_price=Decimal("40.00"),
        )
        _create_pos_payment(order, shift, amount=total)
        return order

    def test_void_order(
        self,
        pos_manager_client,
        pos_terminal,
        pos_manager_user,
        manager_open_shift,
        site_settings,
    ):
        """Voiding sets order status to cancelled and payment_status to refunded."""
        order = self._make_voidable_order(
            pos_terminal,
            pos_manager_user,
            manager_open_shift,
            site_settings,
        )

        resp = pos_manager_client.post(_void_url(order.id), format="json")
        data = assert_pos_success(resp)

        assert data["order"]["status"] == "cancelled"
        assert data["order"]["payment_status"] == "refunded"

    def test_reverses_shift_totals(
        self,
        pos_manager_client,
        pos_terminal,
        pos_manager_user,
        manager_open_shift,
        site_settings,
    ):
        """Shift total_sales decreases and total_refunds increases after void."""
        order_total = Decimal("40.00")
        # Pre-set shift totals as if a sale was recorded
        manager_open_shift.total_sales = order_total
        manager_open_shift.total_transactions = 1
        manager_open_shift.total_refunds = Decimal("0.00")
        manager_open_shift.save(
            update_fields=["total_sales", "total_transactions", "total_refunds"]
        )

        order = self._make_voidable_order(
            pos_terminal,
            pos_manager_user,
            manager_open_shift,
            site_settings,
            total=order_total,
        )

        pos_manager_client.post(_void_url(order.id), format="json")

        manager_open_shift.refresh_from_db()
        assert manager_open_shift.total_sales == Decimal("0.00")
        assert manager_open_shift.total_transactions == 0
        assert manager_open_shift.total_refunds == order_total

    def test_returns_stock(
        self,
        pos_manager_client,
        pos_terminal,
        pos_manager_user,
        manager_open_shift,
        site_settings,
        warehouse,
        category,
    ):
        """Voiding returns stock to the terminal's warehouse."""
        product = ProductFactory(
            name="Voidable Widget",
            slug="voidable-widget",
            category=category,
            price=Decimal("20.00"),
            track_inventory=True,
        )
        stock = StockItemFactory(
            product=product,
            warehouse=warehouse,
            on_hand=8,
        )

        order = _create_pos_order(
            pos_terminal,
            pos_manager_user,
            site_settings,
            total_amount=Decimal("40.00"),
            subtotal=Decimal("40.00"),
        )
        OrderItemFactory(
            order=order,
            product=product,
            product_name=product.name,
            sku=product.sku,
            quantity=2,
            unit_price=Decimal("20.00"),
            total_price=Decimal("40.00"),
        )
        _create_pos_payment(order, manager_open_shift, amount=Decimal("40.00"))

        pos_manager_client.post(_void_url(order.id), format="json")

        stock.refresh_from_db()
        assert stock.on_hand == 10  # 8 original + 2 returned

    def test_requires_permission(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        open_shift,
        site_settings,
    ):
        """Cashier without pos_void permission gets 403."""
        order = self._make_voidable_order(
            pos_terminal,
            pos_staff_user,
            open_shift,
            site_settings,
        )

        resp = pos_client.post(_void_url(order.id), format="json")
        assert_pos_error(resp, "PERMISSION_DENIED", http_status=403)

    def test_already_voided_error(
        self,
        pos_manager_client,
        pos_terminal,
        pos_manager_user,
        manager_open_shift,
        site_settings,
    ):
        """Cannot void an order that is already cancelled/voided."""
        order = self._make_voidable_order(
            pos_terminal,
            pos_manager_user,
            manager_open_shift,
            site_settings,
        )
        # Mark as already voided
        from orders.models import Order

        Order.objects.filter(pk=order.pk).update(status="cancelled")

        resp = pos_manager_client.post(_void_url(order.id), format="json")
        assert_pos_error(resp, "ALREADY_VOIDED", http_status=400)

    def test_different_shift_error(
        self,
        pos_manager_client,
        pos_terminal,
        pos_manager_user,
        manager_open_shift,
        site_settings,
    ):
        """Cannot void an order from a closed/different shift."""
        from tests.factories import POSShiftFactory

        # Create order on a different (closed) shift
        old_shift = POSShiftFactory(
            terminal=pos_terminal,
            cashier=pos_manager_user,
            opening_cash=Decimal("100.00"),
            closed=True,
        )

        order = _create_pos_order(
            pos_terminal,
            pos_manager_user,
            site_settings,
            status="processing",
        )
        _create_pos_payment(order, old_shift, amount=Decimal("25.00"))

        resp = pos_manager_client.post(_void_url(order.id), format="json")
        assert_pos_error(resp, "NOT_CURRENT_SHIFT", http_status=400)
