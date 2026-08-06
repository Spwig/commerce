"""
Tier-1 transaction-integrity invariants (digital single-item flow).

Drives the real ``PaymentOrchestrationService`` order-creation and settlement
seams (the PSP boundary is stubbed deterministically, exactly as the rest of
the integration suite does — the fake ``test_gateway`` is itself deterministic)
and asserts the resulting transaction footprint. Covers plan invariants:

  #1  successful payment -> exactly one correct order
  #2  failed payment    -> no paid order
  #3  amount charged    == authoritative server-computed amount
  #6  duplicate settlement -> no duplicate side effects (idempotent)

Inventory (#4 no double deduction) needs a stock-tracking physical product and
is covered in ``test_inventory_integrity`` so this module stays on the clean
no-shipping digital path.
"""

from decimal import Decimal
from unittest import mock

import pytest

from commerce_footprint import (
    assert_charged_equals,
    assert_exactly_one_order,
    assert_no_duplicate_reference_keys,
    assert_no_paid_order,
    assert_same_side_effects,
)
from commerce_footprint.footprint import Amount
from commerce_footprint.orm_backend import footprint_for_order
from payment_providers.services.payment_orchestration_service import (
    PaymentOrchestrationService,
)
from tests.factories import CartFactory, CartItemFactory, PaymentProviderAccountFactory
from tests.pricing_oracle import CartSpec, LineSpec, recompute_expected_total

pytestmark = [pytest.mark.django_db, pytest.mark.invariant, pytest.mark.checkout]

# Stub only the PSP boundary; every order/settlement/DB path runs for real.
REGISTRY = "payment_providers.services.payment_orchestration_service.ProviderRegistry.get_provider"
GET_PROVIDER = "payment_providers.models.PaymentProviderAccount.get_provider_instance"

# The price the *test* chose — the independent oracle is built from this, never
# read back from Spwig.
DIGITAL_PRICE = Decimal("9.99")


def _stub_provider(provider_intent_id="pi_integrity_1"):
    provider = mock.MagicMock()
    provider.create_payment_intent_for_checkout.return_value = {
        "success": True,
        "provider_intent_id": provider_intent_id,
        "status": "requires_payment_method",
    }
    return provider


@pytest.fixture
def priced_digital_product(db, category):
    """A digital product at a price this test owns (independent of fixtures)."""
    from tests.factories import ProductFactory

    return ProductFactory(
        name="Integrity Download",
        slug="integrity-download",
        category=category,
        price=DIGITAL_PRICE,
        digital=True,
    )


@pytest.fixture
def ready_digital_session(customer_user, priced_digital_product, site_settings, warehouse):
    """A digital (no-shipping) session ready to raise a payment intent."""
    from cart.services.checkout_service import CheckoutService

    cart = CartFactory(user=customer_user)
    CartItemFactory(cart=cart, product=priced_digital_product, quantity=1)
    session = CheckoutService.get_or_create_session(cart)
    session.recalculate_totals()
    CheckoutService.set_billing_address(
        session,
        same_as_shipping=False,
        address_data={
            "address_type": "billing",
            "name": "Ivy Invariant",
            "address1": "1 Ledger Way",
            "city": "Beverly Hills",
            "state": "CA",
            "country": "US",
            "postal_code": "90210",
        },
    )
    provider = PaymentProviderAccountFactory()
    session.payment_provider = provider
    session.save(update_fields=["payment_provider"])
    return session, provider


def _create_intent(session, provider):
    with (
        mock.patch(REGISTRY, return_value=mock.MagicMock()),
        mock.patch(GET_PROVIDER, return_value=_stub_provider()),
    ):
        ok, intent, msg = PaymentOrchestrationService.create_payment_intent(
            session, provider, "https://example.test/return", "https://example.test/cancel"
        )
    assert ok, f"intent creation failed: {msg}"
    return intent


def _expected_total() -> Amount:
    """Independent oracle: a single digital line, no shipping, no tax."""
    return recompute_expected_total(
        CartSpec(lines=(LineSpec(DIGITAL_PRICE, 1),), tax_rate=Decimal("0"))
    ).total


def test_successful_payment_creates_exactly_one_correct_order(ready_digital_session):
    """Invariants #1 + #3: one order, charged == independently-computed total."""
    session, provider = ready_digital_session
    intent = _create_intent(session, provider)

    ok, msg = PaymentOrchestrationService.handle_payment_success(intent, {"status": "succeeded"})
    assert ok, msg

    intent.refresh_from_db()
    fp = footprint_for_order(intent.order)

    order = assert_exactly_one_order(fp)
    assert order.payment_status == "paid", order.payment_status
    assert_charged_equals(fp, _expected_total())
    assert_no_duplicate_reference_keys(fp)


def test_duplicate_settlement_is_idempotent(ready_digital_session):
    """Invariant #6: replaying settlement creates no second order/charge/email."""
    session, provider = ready_digital_session
    intent = _create_intent(session, provider)

    PaymentOrchestrationService.handle_payment_success(intent, {"status": "succeeded"})
    intent.refresh_from_db()
    before = footprint_for_order(intent.order)

    # Replay the exact same settlement — the guard must make it a no-op.
    PaymentOrchestrationService.handle_payment_success(intent, {"status": "succeeded"})
    intent.refresh_from_db()
    after = footprint_for_order(intent.order)

    assert_same_side_effects(before, after)


def test_failed_payment_creates_no_paid_order(ready_digital_session):
    """Invariant #2: a failed settlement never yields a paid order or capture."""
    session, provider = ready_digital_session
    intent = _create_intent(session, provider)

    PaymentOrchestrationService.handle_payment_failure(
        intent, error_code="card_declined", error_message="Card declined"
    )
    intent.refresh_from_db()
    fp = footprint_for_order(intent.order)

    assert_no_paid_order(fp)
