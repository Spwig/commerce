"""Idempotency of `create_payment_intent` under double-submit.

`PaymentOrchestrationService.create_payment_intent` now takes a
`select_for_update()` lock on the checkout-session row before deciding whether
to create an order. Without it, a double-clicked "Pay" (two requests in flight)
could both find no existing intent and each raise a separate order + provider
intent — a double charge and double stock allocation.

With the lock, the second call finds the first call's live intent and reuses
its order (same total), creating only a *new intent* against the *same order*.
These tests drive two sequential `create_payment_intent` calls against a ready
digital session and assert exactly one order is created.

The provider is stubbed (both the registry lookup and the provider instance) so
no real PSP is contacted; the order + reuse logic runs against the real DB.
"""

from decimal import Decimal
from unittest import mock

import pytest

from payment_providers.services.payment_orchestration_service import (
    PaymentOrchestrationService,
)
from tests.factories import (
    CartFactory,
    CartItemFactory,
    PaymentProviderAccountFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.checkout, pytest.mark.integration]

REGISTRY = "payment_providers.services.payment_orchestration_service.ProviderRegistry.get_provider"
GET_PROVIDER = "payment_providers.models.PaymentProviderAccount.get_provider_instance"


def _stub_provider(provider_intent_id="pi_stub"):
    provider = mock.MagicMock()
    provider.create_payment_intent_for_checkout.return_value = {
        "success": True,
        "provider_intent_id": provider_intent_id,
        "status": "requires_payment_method",
    }
    return provider


@pytest.fixture
def ready_digital_session(customer_user, digital_product, site_settings, warehouse):
    """A digital (no-shipping) session ready to raise a payment intent:
    complete billing address + a payment provider selected."""
    from cart.services.checkout_service import CheckoutService

    cart = CartFactory(user=customer_user)
    CartItemFactory(cart=cart, product=digital_product, quantity=1)
    session = CheckoutService.get_or_create_session(cart)
    session.recalculate_totals()
    CheckoutService.set_billing_address(
        session,
        same_as_shipping=False,
        address_data={
            "address_type": "billing",
            "name": "Dana Digital",
            "address1": "500 Market St",
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


def test_repeat_intent_creation_reuses_single_order(ready_digital_session):
    session, provider = ready_digital_session
    from orders.models import Order
    from payment_providers.models import PaymentIntent

    orders_before = Order.objects.count()

    with (
        mock.patch(REGISTRY, return_value=mock.MagicMock()),
        mock.patch(GET_PROVIDER, return_value=_stub_provider()),
    ):
        ok1, intent1, msg1 = PaymentOrchestrationService.create_payment_intent(
            session, provider, "http://return", "http://cancel"
        )
        ok2, intent2, msg2 = PaymentOrchestrationService.create_payment_intent(
            session, provider, "http://return", "http://cancel"
        )

    assert ok1, msg1
    assert ok2, msg2

    # Exactly ONE order created across the two calls — not one per submit.
    assert Order.objects.count() == orders_before + 1, (
        "A repeat intent creation raised a second order — the session lock / "
        "existing-order reuse regressed (double-order, double stock)."
    )

    # Both intents point at the same reused order.
    assert intent1.order_id is not None
    assert intent1.order_id == intent2.order_id

    # Two distinct intent rows, both bound to this session and its one order.
    session_intents = PaymentIntent.objects.filter(checkout_session=session)
    assert session_intents.count() == 2
    assert set(session_intents.values_list("order_id", flat=True)) == {intent1.order_id}


def test_reused_order_charges_the_same_amount(ready_digital_session):
    """The reused order's intents charge the session's amount_due, not a
    doubled figure — the reuse path must not re-price on retry."""
    session, provider = ready_digital_session
    expected_due = session.amount_due.amount

    with (
        mock.patch(REGISTRY, return_value=mock.MagicMock()),
        mock.patch(GET_PROVIDER, return_value=_stub_provider()),
    ):
        _, intent1, _ = PaymentOrchestrationService.create_payment_intent(
            session, provider, "http://return", "http://cancel"
        )
        _, intent2, _ = PaymentOrchestrationService.create_payment_intent(
            session, provider, "http://return", "http://cancel"
        )

    assert expected_due > Decimal("0")
    assert intent1.amount.amount == expected_due
    assert intent2.amount.amount == expected_due
