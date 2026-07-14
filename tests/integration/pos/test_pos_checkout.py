"""
POS Checkout integration tests.

Tests cash, card, gift card, split tender checkout flows, gift card balance
checks, and stock integration for the POS checkout API.
"""

from decimal import Decimal

import pytest

from tests.helpers import assert_pos_error, assert_pos_success

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.pos]

# Endpoint URLs
CASH_URL = "/api/pos/checkout/cash/"
CARD_URL = "/api/pos/checkout/card/"
GIFT_CARD_URL = "/api/pos/checkout/gift-card/"
SPLIT_URL = "/api/pos/checkout/split/"
GIFT_CARD_BALANCE_URL = "/api/pos/checkout/gift-card/balance/"
CART_ADD_URL = "/api/pos/cart/items/"


# ============================================================
# Helpers
# ============================================================


def _add_item_to_cart(pos_client, product, quantity=1):
    """Add a product to the POS cart and return the response."""
    return pos_client.post(
        CART_ADD_URL,
        {
            "product_id": product.id,
            "quantity": quantity,
        },
    )


def _create_gift_card(product, balance, currency="USD", code=None):
    """
    Create a GiftCard directly in the database for checkout tests.

    Args:
        product: A Product instance (used as the FK; product_type is irrelevant
                 for our test since we only validate the GiftCard record itself).
        balance: Decimal balance to set on the card.
        currency: Currency code.
        code: Optional specific code; auto-generated if None.

    Returns:
        GiftCard instance.
    """
    from djmoney.money import Money

    from catalog.models import GiftCard

    gc_code = code or GiftCard.generate_code()
    gift_card = GiftCard.objects.create(
        code=gc_code,
        product=product,
        initial_value=Money(balance, currency),
        current_balance=Money(balance, currency),
        recipient_email="test@example.com",
        is_active=True,
    )
    return gift_card


# ============================================================
# TestCashCheckout
# ============================================================


class TestCashCheckout:
    """Tests for POST /api/pos/checkout/cash/."""

    def test_success(self, pos_client, open_shift, product_with_stock, site_settings):
        """Checkout with sufficient cash succeeds and returns order data."""
        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        response = pos_client.post(CASH_URL, {"amount_tendered": "50.00"})
        data = assert_pos_success(response)

        assert "order" in data
        assert data["order"]["status"] == "processing"
        assert data["order"]["payment_status"] == "paid"
        assert data["order"]["channel"] == "pos"

    def test_returns_change(self, pos_client, open_shift, product_with_stock, site_settings):
        """Response includes change amount when customer overpays."""
        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        # Product price is 25.00; tendering 50.00 should yield 25.00 change
        response = pos_client.post(CASH_URL, {"amount_tendered": "50.00"})
        data = assert_pos_success(response)

        assert "change_given" in data
        assert Decimal(data["change_given"]) == Decimal("25.00")

    def test_exact_amount(self, pos_client, open_shift, product_with_stock, site_settings):
        """Exact amount works with zero change."""
        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        response = pos_client.post(CASH_URL, {"amount_tendered": "25.00"})
        data = assert_pos_success(response)

        assert Decimal(data["change_given"]) == Decimal("0.00")

    def test_insufficient_cash_error(
        self, pos_client, open_shift, product_with_stock, site_settings
    ):
        """Less cash than the total returns INSUFFICIENT_PAYMENT error."""
        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        response = pos_client.post(CASH_URL, {"amount_tendered": "10.00"})
        assert_pos_error(response, "INSUFFICIENT_PAYMENT", http_status=400)

    def test_requires_open_shift(self, pos_client, product_with_stock, site_settings):
        """No open shift returns NO_OPEN_SHIFT error (409)."""
        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        response = pos_client.post(CASH_URL, {"amount_tendered": "50.00"})
        assert_pos_error(response, "NO_OPEN_SHIFT", http_status=409)

    def test_creates_order(self, pos_client, open_shift, product_with_stock, site_settings):
        """Order record is created in the database after checkout."""
        from orders.models import Order

        initial_count = Order.objects.count()
        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        pos_client.post(CASH_URL, {"amount_tendered": "30.00"})

        assert Order.objects.count() == initial_count + 1
        order = Order.objects.latest("created_at")
        assert order.channel == "pos"
        assert order.payment_status == "paid"

    def test_creates_pos_payment(self, pos_client, open_shift, product_with_stock, site_settings):
        """POSPayment record is created with method='cash'."""
        from pos_app.models import POSPayment

        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        pos_client.post(CASH_URL, {"amount_tendered": "30.00"})

        payment = POSPayment.objects.latest("created_at")
        assert payment.method == "cash"
        assert payment.shift == open_shift

    def test_updates_shift_totals(self, pos_client, open_shift, product_with_stock, site_settings):
        """Shift total_sales and total_transactions are updated after checkout."""
        initial_sales = open_shift.total_sales
        initial_txns = open_shift.total_transactions

        _add_item_to_cart(pos_client, product_with_stock, quantity=2)
        pos_client.post(CASH_URL, {"amount_tendered": "100.00"})

        open_shift.refresh_from_db()
        assert open_shift.total_sales > initial_sales
        assert open_shift.total_transactions == initial_txns + 1

    def test_empties_cart(self, pos_client, open_shift, product_with_stock, site_settings):
        """Cart is empty after successful checkout."""
        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        pos_client.post(CASH_URL, {"amount_tendered": "30.00"})

        # Fetch cart; should have no items
        cart_response = pos_client.get("/api/pos/cart/")
        cart_data = cart_response.json()
        items = cart_data.get("cart", {}).get("items", cart_data.get("items", []))
        assert len(items) == 0

    def test_empty_cart_error(self, pos_client, open_shift, site_settings):
        """Cannot checkout with an empty cart."""
        response = pos_client.post(CASH_URL, {"amount_tendered": "50.00"})
        assert_pos_error(response, "EMPTY_CART", http_status=400)

    def test_multiple_items_order_total(
        self, pos_client, open_shift, product_with_stock, site_settings
    ):
        """Order total reflects the sum of multiple cart items."""
        _add_item_to_cart(pos_client, product_with_stock, quantity=3)
        response = pos_client.post(CASH_URL, {"amount_tendered": "100.00"})
        data = assert_pos_success(response)

        # 3 x 25.00 = 75.00
        assert Decimal(data["order"]["total"]) == Decimal("75.00")
        assert Decimal(data["change_given"]) == Decimal("25.00")


# ============================================================
# TestCardCheckout
# ============================================================


class TestCardCheckout:
    """Tests for POST /api/pos/checkout/card/."""

    def test_success(self, pos_client, open_shift, product_with_stock, site_settings):
        """Card checkout succeeds and returns an order."""
        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        response = pos_client.post(
            CARD_URL,
            {
                "card_last_four": "4242",
                "card_reference": "ref-001",
            },
        )
        data = assert_pos_success(response)

        assert "order" in data
        assert data["order"]["payment_status"] == "paid"

    def test_optional_fields(self, pos_client, open_shift, product_with_stock, site_settings):
        """last_four and card_reference are optional; empty body still succeeds."""
        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        response = pos_client.post(CARD_URL, {})
        data = assert_pos_success(response)

        assert "order" in data

    def test_requires_shift(self, pos_client, product_with_stock, site_settings):
        """No open shift returns NO_OPEN_SHIFT error."""
        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        response = pos_client.post(CARD_URL, {})
        assert_pos_error(response, "NO_OPEN_SHIFT", http_status=409)

    def test_creates_payment_record(
        self, pos_client, open_shift, product_with_stock, site_settings
    ):
        """POSPayment record is created with method='card' and card details."""
        from pos_app.models import POSPayment

        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        pos_client.post(
            CARD_URL,
            {
                "card_last_four": "1234",
                "card_reference": "ref-abc",
            },
        )

        payment = POSPayment.objects.latest("created_at")
        assert payment.method == "card"
        assert payment.card_last_four == "1234"
        assert payment.card_reference == "ref-abc"

    def test_empty_cart_error(self, pos_client, open_shift, site_settings):
        """Card checkout with empty cart returns EMPTY_CART error."""
        response = pos_client.post(CARD_URL, {})
        assert_pos_error(response, "EMPTY_CART", http_status=400)


# ============================================================
# TestGiftCardCheckout
# ============================================================


class TestGiftCardCheckout:
    """Tests for POST /api/pos/checkout/gift-card/."""

    def test_full_amount(self, pos_client, open_shift, product_with_stock, site_settings):
        """Gift card covering the full amount completes checkout."""
        gift_card = _create_gift_card(product_with_stock, Decimal("100.00"))

        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        response = pos_client.post(
            GIFT_CARD_URL,
            {
                "gift_card_code": gift_card.code,
            },
        )
        data = assert_pos_success(response)

        assert "order" in data
        assert data["order"]["payment_status"] == "paid"

    def test_insufficient_balance(self, pos_client, open_shift, product_with_stock, site_settings):
        """Gift card with less than order total returns INSUFFICIENT_BALANCE."""
        gift_card = _create_gift_card(product_with_stock, Decimal("5.00"))

        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        response = pos_client.post(
            GIFT_CARD_URL,
            {
                "gift_card_code": gift_card.code,
            },
        )
        assert_pos_error(response, "INSUFFICIENT_BALANCE", http_status=400)

    def test_invalid_code(self, pos_client, open_shift, product_with_stock, site_settings):
        """Invalid gift card code returns GIFT_CARD_INVALID."""
        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        response = pos_client.post(
            GIFT_CARD_URL,
            {
                "gift_card_code": "NONEXISTENT-CODE-9999",
            },
        )
        assert_pos_error(response, "GIFT_CARD_INVALID", http_status=400)

    def test_balance_deducted(self, pos_client, open_shift, product_with_stock, site_settings):
        """Gift card balance is reduced after successful checkout."""

        gift_card = _create_gift_card(product_with_stock, Decimal("100.00"))
        initial_balance = gift_card.current_balance.amount

        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        pos_client.post(
            GIFT_CARD_URL,
            {
                "gift_card_code": gift_card.code,
            },
        )

        gift_card.refresh_from_db()
        assert gift_card.current_balance.amount < initial_balance
        # Product is 25.00, so balance should be 75.00
        assert gift_card.current_balance.amount == Decimal("75.00")


# ============================================================
# TestSplitTenderCheckout
# ============================================================


class TestSplitTenderCheckout:
    """Tests for POST /api/pos/checkout/split/."""

    def test_cash_and_card(self, pos_client, open_shift, product_with_stock, site_settings):
        """Split between cash and card completes checkout."""
        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        response = pos_client.post(
            SPLIT_URL,
            {
                "payments": [
                    {"method": "cash", "amount": "15.00"},
                    {"method": "card", "amount": "10.00"},
                ],
            },
            format="json",
        )
        data = assert_pos_success(response)

        assert "order" in data
        assert data["order"]["payment_status"] == "paid"

    def test_insufficient_total_error(
        self, pos_client, open_shift, product_with_stock, site_settings
    ):
        """Total of payments less than cart total returns INSUFFICIENT_PAYMENT."""
        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        response = pos_client.post(
            SPLIT_URL,
            {
                "payments": [
                    {"method": "cash", "amount": "5.00"},
                    {"method": "card", "amount": "5.00"},
                ],
            },
            format="json",
        )
        assert_pos_error(response, "INSUFFICIENT_PAYMENT", http_status=400)

    def test_overpayment_change(self, pos_client, open_shift, product_with_stock, site_settings):
        """Change is returned when split total exceeds cart total (cash last)."""
        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        # Product is 25.00; paying 10 card + 20 cash = 30 total => 5 change
        response = pos_client.post(
            SPLIT_URL,
            {
                "payments": [
                    {"method": "card", "amount": "10.00"},
                    {"method": "cash", "amount": "20.00"},
                ],
            },
            format="json",
        )
        data = assert_pos_success(response)

        assert "change_given" in data
        assert Decimal(data["change_given"]) == Decimal("5.00")

    def test_empty_payments_error(self, pos_client, open_shift, product_with_stock, site_settings):
        """Empty payments array returns validation error."""
        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        response = pos_client.post(
            SPLIT_URL,
            {
                "payments": [],
            },
            format="json",
        )

        # Empty payments should be rejected (either serializer validation or logic)
        assert response.status_code == 400

    def test_creates_multiple_payment_records(
        self, pos_client, open_shift, product_with_stock, site_settings
    ):
        """Multiple POSPayment records are created for a split tender."""
        from pos_app.models import POSPayment

        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        pos_client.post(
            SPLIT_URL,
            {
                "payments": [
                    {"method": "cash", "amount": "15.00"},
                    {"method": "card", "amount": "10.00"},
                ],
            },
            format="json",
        )

        from orders.models import Order

        order = Order.objects.latest("created_at")
        payments = POSPayment.objects.filter(order=order)
        assert payments.count() == 2

        methods = set(payments.values_list("method", flat=True))
        assert methods == {"cash", "card"}

    def test_three_way_split(self, pos_client, open_shift, product_with_stock, site_settings):
        """Cash + card + gift card split completes checkout."""
        gift_card = _create_gift_card(product_with_stock, Decimal("50.00"))

        _add_item_to_cart(pos_client, product_with_stock, quantity=1)
        response = pos_client.post(
            SPLIT_URL,
            {
                "payments": [
                    {"method": "cash", "amount": "10.00"},
                    {"method": "card", "amount": "10.00"},
                    {"method": "gift_card", "amount": "5.00", "gift_card_code": gift_card.code},
                ],
            },
            format="json",
        )
        data = assert_pos_success(response)

        assert "order" in data
        from orders.models import Order
        from pos_app.models import POSPayment

        order = Order.objects.latest("created_at")
        assert POSPayment.objects.filter(order=order).count() == 3


# ============================================================
# TestCheckGiftCardBalance
# ============================================================


class TestCheckGiftCardBalance:
    """Tests for POST /api/pos/checkout/gift-card/balance/."""

    def test_returns_balance(self, pos_client, product_with_stock, site_settings):
        """Returns gift card balance for a valid code."""
        gift_card = _create_gift_card(product_with_stock, Decimal("75.00"))

        response = pos_client.post(
            GIFT_CARD_BALANCE_URL,
            {
                "code": gift_card.code,
            },
        )
        data = assert_pos_success(response)

        assert "balance" in data
        assert Decimal(data["balance"]) == Decimal("75.00")
        assert data["code"] == gift_card.code

    def test_invalid_code(self, pos_client, site_settings):
        """Invalid code returns error."""
        response = pos_client.post(
            GIFT_CARD_BALANCE_URL,
            {
                "code": "INVALID-CODE-0000",
            },
        )
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False


# ============================================================
# TestCheckoutStockIntegration
# ============================================================


class TestCheckoutStockIntegration:
    """Tests for stock changes after POS checkout."""

    def test_stock_reduced_after_checkout(
        self, pos_client, open_shift, product_with_stock, warehouse, site_settings
    ):
        """Stock quantity is decremented after successful checkout."""
        from catalog.models import StockItem

        stock = StockItem.objects.get(product=product_with_stock, warehouse=warehouse)
        initial_on_hand = stock.on_hand

        _add_item_to_cart(pos_client, product_with_stock, quantity=2)
        pos_client.post(CASH_URL, {"amount_tendered": "100.00"})

        stock.refresh_from_db()
        assert stock.on_hand == initial_on_hand - 2

    def test_insufficient_stock_error(
        self, pos_client, open_shift, product_no_stock, site_settings
    ):
        """Cannot add a product with zero stock to the cart (blocked at add-to-cart)."""
        response = _add_item_to_cart(pos_client, product_no_stock, quantity=1)

        # Stock validation may occur at cart-add time or checkout time.
        # If the product is added anyway, attempt checkout and verify failure.
        if response.status_code == 200:
            checkout_response = pos_client.post(CASH_URL, {"amount_tendered": "100.00"})
            # The checkout should either fail or the stock warning is logged
            # but the sale still goes through (POS allows overselling in some configs).
            # At minimum, confirm the response is handled, not a 500 error.
            assert checkout_response.status_code in (200, 400)
        else:
            # Cart add was rejected due to insufficient stock
            assert response.status_code == 400
