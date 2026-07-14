"""
POS Shift management and reports integration tests.

Tests shift open/close lifecycle, cash movements, daily sales reports,
and top products reporting. Verifies permission enforcement, data
calculations, and error handling across all shift-related endpoints.
"""

from decimal import Decimal

import pytest

from pos_app.models import CashMovement, POSPayment, POSShift
from tests.factories import CashMovementFactory, OrderFactory, OrderItemFactory
from tests.helpers import assert_pos_error, assert_pos_success

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.pos]

# Endpoint URLs
OPEN_SHIFT_URL = "/api/pos/shifts/open/"
CLOSE_SHIFT_URL = "/api/pos/shifts/close/"
CURRENT_SHIFT_URL = "/api/pos/shifts/current/"
CASH_MOVEMENT_URL = "/api/pos/shifts/cash-movement/"
DAILY_REPORT_URL = "/api/pos/reports/daily/"
TOP_PRODUCTS_URL = "/api/pos/reports/top-products/"


# ============================================================
# TestOpenShift
# ============================================================


class TestOpenShift:
    """Tests for POST /api/pos/shifts/open/."""

    def test_open_shift_success(self, pos_client, pos_terminal, pos_staff_user, site_settings):
        """Opens a shift with an opening cash amount and returns 201."""
        response = pos_client.post(OPEN_SHIFT_URL, {"opening_cash": "200.00"})
        data = assert_pos_success(response, http_status=201)

        assert data["message"] == "Shift opened."
        shift = POSShift.objects.get(terminal=pos_terminal, cashier=pos_staff_user)
        assert shift.is_open is True
        assert shift.opening_cash == Decimal("200.00")

    def test_open_shift_returns_data(self, pos_client, pos_terminal, site_settings):
        """Response includes shift ID, started_at, and opening_cash."""
        response = pos_client.post(OPEN_SHIFT_URL, {"opening_cash": "50.00"})
        data = assert_pos_success(response, http_status=201)

        shift_data = data["shift"]
        assert "id" in shift_data
        assert shift_data["started_at"] is not None
        assert shift_data["opening_cash"] == "50.00"
        assert shift_data["is_open"] is True
        assert shift_data["terminal_name"] == pos_terminal.name

    def test_blocks_second_shift(self, pos_client, open_shift, site_settings):
        """Cannot open a second shift when one is already open on the terminal."""
        response = pos_client.post(OPEN_SHIFT_URL, {"opening_cash": "100.00"})
        assert_pos_error(response, "SHIFT_ALREADY_OPEN", http_status=409)

    def test_blocks_different_cashier(self, pos_manager_client, open_shift, site_settings):
        """A different cashier cannot open a shift if one already exists on the terminal."""
        response = pos_manager_client.post(OPEN_SHIFT_URL, {"opening_cash": "100.00"})
        assert_pos_error(response, "SHIFT_ALREADY_OPEN", http_status=409)

    def test_opening_cash_default(self, pos_client, pos_terminal, site_settings):
        """Opening a shift with 0 cash works (default opening_cash)."""
        response = pos_client.post(OPEN_SHIFT_URL, {"opening_cash": "0.00"})
        data = assert_pos_success(response, http_status=201)

        assert data["shift"]["opening_cash"] == "0"
        shift = POSShift.objects.get(terminal=pos_terminal)
        assert shift.opening_cash == Decimal("0")


# ============================================================
# TestCloseShift
# ============================================================


class TestCloseShift:
    """Tests for POST /api/pos/shifts/close/."""

    def test_close_shift_success(self, pos_manager_client, manager_open_shift, site_settings):
        """Closing a shift with a closing cash amount returns 200."""
        response = pos_manager_client.post(CLOSE_SHIFT_URL, {"closing_cash": "150.00"})
        data = assert_pos_success(response, http_status=200)

        assert data["message"] == "Shift closed."
        manager_open_shift.refresh_from_db()
        assert manager_open_shift.is_open is False
        assert manager_open_shift.closing_cash == Decimal("150.00")

    def test_calculates_expected_cash(self, pos_manager_client, manager_open_shift, site_settings):
        """Response includes expected_cash calculated from opening cash and transactions."""
        response = pos_manager_client.post(CLOSE_SHIFT_URL, {"closing_cash": "100.00"})
        data = assert_pos_success(response)

        shift_data = data["shift"]
        assert "expected_cash" in shift_data
        # With no transactions, expected cash equals opening cash
        assert Decimal(shift_data["expected_cash"]) == Decimal("100.00")

    def test_calculates_variance(self, pos_manager_client, manager_open_shift, site_settings):
        """Cash difference is correctly calculated (closing - expected)."""
        # Add a cash-in movement to affect expected cash
        CashMovementFactory(
            shift=manager_open_shift,
            movement_type="in",
            amount=Decimal("50.00"),
            reason="Float top-up",
            performed_by=manager_open_shift.cashier,
        )
        # Close with exact expected amount: opening(100) + cash_in(50) = 150
        response = pos_manager_client.post(CLOSE_SHIFT_URL, {"closing_cash": "140.00"})
        data = assert_pos_success(response)

        shift_data = data["shift"]
        expected = Decimal(shift_data["expected_cash"])
        closing = Decimal(shift_data["closing_cash"])
        variance = Decimal(shift_data["cash_difference"])
        assert variance == closing - expected

    def test_includes_summary(self, pos_manager_client, manager_open_shift, site_settings):
        """Close shift response has total_sales and total_transactions."""
        response = pos_manager_client.post(CLOSE_SHIFT_URL, {"closing_cash": "100.00"})
        data = assert_pos_success(response)

        shift_data = data["shift"]
        assert "total_sales" in shift_data
        assert "total_transactions" in shift_data
        assert "net_sales" in shift_data

    def test_no_open_shift_error(
        self, pos_manager_client, pos_terminal, pos_manager_user, site_settings
    ):
        """Error when there is no shift to close."""
        response = pos_manager_client.post(CLOSE_SHIFT_URL, {"closing_cash": "100.00"})
        assert_pos_error(response, "NO_OPEN_SHIFT", http_status=409)

    def test_requires_close_shift_permission(self, pos_client, open_shift, site_settings):
        """Cashier without pos_close_shift permission gets 403."""
        response = pos_client.post(CLOSE_SHIFT_URL, {"closing_cash": "100.00"})
        assert_pos_error(response, "PERMISSION_DENIED", http_status=403)


# ============================================================
# TestCurrentShiftSummary
# ============================================================


class TestCurrentShiftSummary:
    """Tests for GET /api/pos/shifts/current/."""

    def test_returns_summary(self, pos_client, open_shift, site_settings):
        """Returns the current open shift details."""
        response = pos_client.get(CURRENT_SHIFT_URL)
        data = assert_pos_success(response)

        shift_data = data["shift"]
        assert shift_data["id"] == open_shift.id
        assert shift_data["is_open"] is True
        assert shift_data["opening_cash"] == "100.00"

    def test_no_shift_error(self, pos_client, pos_terminal, site_settings):
        """Returns null shift when no shift is open."""
        response = pos_client.get(CURRENT_SHIFT_URL)
        data = assert_pos_success(response)

        assert data["shift"] is None

    def test_includes_payment_breakdown(self, pos_client, open_shift, site_settings):
        """Summary includes payment method breakdown fields."""
        response = pos_client.get(CURRENT_SHIFT_URL)
        data = assert_pos_success(response)

        shift_data = data["shift"]
        assert "cash_total" in shift_data
        assert "card_total" in shift_data
        assert "gift_card_total" in shift_data


# ============================================================
# TestCashMovement
# ============================================================


class TestCashMovement:
    """Tests for POST /api/pos/shifts/cash-movement/."""

    def test_cash_in(self, pos_manager_client, manager_open_shift, site_settings):
        """Record a cash-in movement."""
        response = pos_manager_client.post(
            CASH_MOVEMENT_URL,
            {
                "movement_type": "in",
                "amount": "50.00",
                "reason": "Float top-up",
            },
        )
        data = assert_pos_success(response, http_status=201)

        assert data["movement"]["movement_type"] == "in"
        assert data["movement"]["amount"] == "50.00"
        assert data["movement"]["reason"] == "Float top-up"

    def test_cash_out(self, pos_manager_client, manager_open_shift, site_settings):
        """Record a cash-out movement."""
        response = pos_manager_client.post(
            CASH_MOVEMENT_URL,
            {
                "movement_type": "out",
                "amount": "30.00",
                "reason": "Bank deposit",
            },
        )
        data = assert_pos_success(response, http_status=201)

        assert data["movement"]["movement_type"] == "out"
        assert data["movement"]["amount"] == "30.00"

    def test_positive_amount_required(self, pos_manager_client, manager_open_shift, site_settings):
        """Amount must be positive (min_value=0.01 in serializer)."""
        response = pos_manager_client.post(
            CASH_MOVEMENT_URL,
            {
                "movement_type": "in",
                "amount": "0.00",
                "reason": "Zero test",
            },
        )
        assert response.status_code == 400

    def test_reason_required(self, pos_manager_client, manager_open_shift, site_settings):
        """Reason field is required."""
        response = pos_manager_client.post(
            CASH_MOVEMENT_URL,
            {
                "movement_type": "in",
                "amount": "10.00",
            },
        )
        assert response.status_code == 400

    def test_creates_record(self, pos_manager_client, manager_open_shift, site_settings):
        """CashMovement object is created in the database."""
        assert CashMovement.objects.count() == 0
        response = pos_manager_client.post(
            CASH_MOVEMENT_URL,
            {
                "movement_type": "in",
                "amount": "75.00",
                "reason": "Change float",
            },
        )
        assert_pos_success(response, http_status=201)

        assert CashMovement.objects.count() == 1
        movement = CashMovement.objects.first()
        assert movement.shift == manager_open_shift
        assert movement.movement_type == "in"
        assert movement.amount == Decimal("75.00")
        assert movement.reason == "Change float"


# ============================================================
# TestDailyReport
# ============================================================


class TestDailyReport:
    """Tests for GET /api/pos/reports/daily/."""

    def test_daily_summary(self, pos_manager_client, pos_terminal, site_settings):
        """Returns daily summary data with sales totals."""
        order = OrderFactory(
            channel="pos",
            pos_terminal=pos_terminal,
            total_amount=Decimal("100.00"),
            amount_refunded=Decimal("0.00"),
        )
        response = pos_manager_client.get(DAILY_REPORT_URL)
        data = assert_pos_success(response)

        report = data["report"]
        assert "total_sales" in report
        assert "total_refunds" in report
        assert "net_sales" in report
        assert "total_transactions" in report
        assert "average_transaction" in report
        assert report["total_transactions"] >= 1

    def test_payment_breakdown(self, pos_manager_client, pos_terminal, site_settings):
        """Report includes payment method totals."""
        order = OrderFactory(
            channel="pos",
            pos_terminal=pos_terminal,
            total_amount=Decimal("80.00"),
        )
        POSPayment.objects.create(
            order=order,
            method="cash",
            amount=Decimal("50.00"),
        )
        POSPayment.objects.create(
            order=order,
            method="card",
            amount=Decimal("30.00"),
        )

        response = pos_manager_client.get(DAILY_REPORT_URL)
        data = assert_pos_success(response)

        breakdown = data["report"]["payment_breakdown"]
        methods = {pb["method"] for pb in breakdown}
        assert "cash" in methods
        assert "card" in methods

    def test_date_filter(self, pos_manager_client, pos_terminal, site_settings):
        """Filter report by a specific date parameter."""
        # Create an order for today
        OrderFactory(
            channel="pos",
            pos_terminal=pos_terminal,
            total_amount=Decimal("50.00"),
        )

        # Request report for a date with no orders
        response = pos_manager_client.get(DAILY_REPORT_URL, {"date": "2020-01-01"})
        data = assert_pos_success(response)

        assert data["report"]["date"] == "2020-01-01"
        assert data["report"]["total_transactions"] == 0

    def test_requires_permission(self, pos_client, pos_terminal, site_settings):
        """Cashier without pos_view_reports permission gets 403."""
        response = pos_client.get(DAILY_REPORT_URL)
        assert_pos_error(response, "PERMISSION_DENIED", http_status=403)


# ============================================================
# TestTopProducts
# ============================================================


class TestTopProducts:
    """Tests for GET /api/pos/reports/top-products/."""

    def test_requires_permission(self, pos_client, pos_terminal, site_settings):
        """Cashier without pos_view_reports permission gets 403."""
        response = pos_client.get(TOP_PRODUCTS_URL)
        assert_pos_error(response, "PERMISSION_DENIED", http_status=403)

    def test_by_revenue(self, pos_manager_client, pos_terminal, product_with_stock, site_settings):
        """Returns products sorted by quantity sold."""
        order = OrderFactory(
            channel="pos",
            pos_terminal=pos_terminal,
            total_amount=Decimal("75.00"),
        )
        OrderItemFactory(
            order=order,
            product=product_with_stock,
            product_name=product_with_stock.name,
            quantity=3,
            unit_price=Decimal("25.00"),
            total_price=Decimal("75.00"),
        )

        response = pos_manager_client.get(TOP_PRODUCTS_URL)
        data = assert_pos_success(response)

        assert len(data["products"]) >= 1
        first = data["products"][0]
        assert first["product_name"] == product_with_stock.name

    def test_includes_qty_and_revenue(
        self, pos_manager_client, pos_terminal, product_with_stock, site_settings
    ):
        """Each product item has total_quantity and total_revenue fields."""
        order = OrderFactory(
            channel="pos",
            pos_terminal=pos_terminal,
            total_amount=Decimal("50.00"),
        )
        OrderItemFactory(
            order=order,
            product=product_with_stock,
            product_name=product_with_stock.name,
            quantity=2,
            unit_price=Decimal("25.00"),
            total_price=Decimal("50.00"),
        )

        response = pos_manager_client.get(TOP_PRODUCTS_URL)
        data = assert_pos_success(response)

        first = data["products"][0]
        assert "total_quantity" in first
        assert "total_revenue" in first
        assert first["total_quantity"] == 2
        assert Decimal(first["total_revenue"]) == Decimal("50.00")
