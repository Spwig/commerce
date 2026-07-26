"""
`CheckoutSessionSerializer` exposes the tender-aware charge figures.

`total_amount` is what the order costs; `amount_due` is what a gateway should
actually be asked for after gift-card / store-credit holds. A headless or agent
client that reads `total_amount` and charges that double-charges the tendered
portion — the bug 4faa2d256 fixed for the web flow. These tests prove the two
new fields are present, reflect real holds, and fail safely (never a wrong
number) when a tender row's currency is inconsistent.
"""

from decimal import Decimal
from unittest.mock import PropertyMock, patch

import pytest
from djmoney.money import Money

from cart.models import CheckoutSession
from cart.serializers import CheckoutSessionSerializer
from cart.services.checkout_service import CheckoutService
from catalog.models import GiftCard
from payment_providers.models import PaymentTransaction
from tests.factories import CartFactory, CartItemFactory, ProductFactory

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
    pytest.mark.checkout,
]

USD = "USD"


def _money(v):
    return Money(Decimal(str(v)), USD)


@pytest.fixture
def session(db, customer_user, site_settings):
    """A checkout session priced at $120 (no address → subtotal only)."""
    cart = CartFactory(user=customer_user)
    CartItemFactory(
        cart=cart,
        product=ProductFactory(name="Widget", price=Decimal("120.00")),
        quantity=1,
        unit_price=Decimal("120.00"),
    )
    s = CheckoutService.get_or_create_session(cart)
    s.recalculate_totals()
    s.refresh_from_db()
    assert s.total_amount.amount == Decimal("120.00")
    return s


class TestChargeFieldsPresent:
    def test_amount_due_and_tendered_present_with_no_tenders(self, session):
        data = CheckoutSessionSerializer(session).data

        assert "amount_due" in data
        assert "tendered_amount" in data
        # No holds → nothing tendered, so the gateway is asked for the full total.
        assert Decimal(data["tendered_amount"]) == Decimal("0")
        assert Decimal(data["amount_due"]) == Decimal("120.00")
        assert Decimal(data["amount_due"]) == Decimal(data["total"])


class TestChargeFieldsReflectHolds:
    def test_gift_card_hold_reduces_amount_due(self, session, db):
        card = GiftCard.objects.create(
            product=ProductFactory(product_type="gift_card", status="published"),
            initial_value=_money("40.00"),
            recipient_email="recipient@test.spwig.com",
            is_active=True,
        )
        # An authorized hold against this session — what tendered_amount sums.
        PaymentTransaction.objects.create(
            transaction_id="auth-gc-1",
            checkout_session=session,
            tender_type=PaymentTransaction.TENDER_GIFT_CARD,
            transaction_type="authorize",
            status="authorized",
            gift_card=card,
            amount=_money("40.00"),
            settlement_amount=_money("40.00"),
            provider_account=None,
        )

        data = CheckoutSessionSerializer(session).data

        assert Decimal(data["tendered_amount"]) == Decimal("40.00")
        assert Decimal(data["amount_due"]) == Decimal("80.00")  # 120 − 40
        # The order still *costs* 120; only the gateway ask drops.
        assert Decimal(data["total"]) == Decimal("120.00")


class TestChargeFieldsFailSafe:
    def test_currency_mismatch_returns_null_not_a_wrong_number(self, session, caplog):
        """
        `tendered_amount` raises ValueError on a currency-inconsistent tender
        row. The serializer must return null (indeterminate) and log — never a
        500, and never a plausible-but-wrong figure.
        """
        with patch.object(
            CheckoutSession,
            "tendered_amount",
            new_callable=PropertyMock,
            side_effect=ValueError("tender settles in EUR but order is USD"),
        ):
            with caplog.at_level("ERROR"):
                data = CheckoutSessionSerializer(session).data

        assert data["tendered_amount"] is None
        assert data["amount_due"] is None
        assert any("indeterminate" in r.message for r in caplog.records)

    def test_serializer_does_not_raise_on_mismatch(self, session):
        """The failure path must not propagate as a 500."""
        with patch.object(
            CheckoutSession,
            "tendered_amount",
            new_callable=PropertyMock,
            side_effect=ValueError("mismatch"),
        ):
            # Must not raise.
            data = CheckoutSessionSerializer(session).data
        assert data["amount_due"] is None
