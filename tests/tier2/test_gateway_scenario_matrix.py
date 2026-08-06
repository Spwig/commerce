"""
Tier-2 gateway-scenario matrix — the platform's handling of each payment
outcome, driven through the REAL ``test_gateway`` provider (not a mock).

The deterministic fake gateway decides the outcome from the magic card number
(and, for async, from an order total ending in ``.19``). These tests drive the
real ``PaymentOrchestrationService`` create → confirm/verify flow with each and
assert the resulting order/payment state via the Footprint oracle:

  - success (4242…)        → order paid, charged == order total
  - declined (…0002)       → no paid order, no gateway capture
  - 3DS (…3220)            → requires_action, then completes on re-confirm
  - async (.19 total)      → processing, then settles on a status poll

This is the "ensure the payment path handles every provider outcome"
dimension of the plan's pairwise matrix.
"""

from decimal import Decimal
from unittest import mock

import pytest

from commerce_footprint import (
    assert_charged_equals,
    assert_exactly_one_order,
    assert_no_paid_order,
)
from commerce_footprint.footprint import Amount
from commerce_footprint.orm_backend import footprint_for_order
from payment_providers.services.payment_orchestration_service import (
    PaymentOrchestrationService,
)
from tests.factories import (
    CartFactory,
    CartItemFactory,
    ComponentRegistryFactory,
    PaymentProviderAccountFactory,
    ProductFactory,
    UserFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.tier2, pytest.mark.checkout]

CARD_SUCCESS = "4242424242424242"
CARD_DECLINED = "4000000000000002"
CARD_3DS = "4000000000003220"

RETURN_URL = "https://example.test/return"
CANCEL_URL = "https://example.test/cancel"


def _card(number, *, three_ds_completed=None):
    data = {
        "card": {"number": number, "exp_month": 12, "exp_year": 2030, "cvc": "123"},
        "cardholder_name": "Ivy Invariant",
    }
    if three_ds_completed is not None:
        data["three_ds_completed"] = three_ds_completed
    return data


@pytest.fixture
def test_gateway_account(db, test_gateway_on_disk, django_site, site_settings, warehouse):
    """A PaymentProviderAccount bound to the real on-disk test_gateway provider
    (components_data/.../test_gateway/current/), so get_provider_instance()
    loads the actual deterministic fake — no mock. ``test_gateway_on_disk`` (root
    conftest) unpacks that provider from the tracked preinstalled bundle when the
    tree doesn't have it (CI / fresh clone). Depends on ``warehouse`` so order
    creation's warehouse selection has one to pick (even digital orders route
    through it)."""
    component = ComponentRegistryFactory(slug="test_gateway", name="Test Gateway")
    return PaymentProviderAccountFactory(component=component)


def _ready_session(provider, *, price="9.99"):
    """A digital (no-shipping) checkout session with a valid billing identity —
    enough for the gateway's strict-mode create validation to pass."""
    from cart.services.checkout_service import CheckoutService

    customer = UserFactory(email="payer@example.test")
    product = ProductFactory(digital=True, price=Decimal(price))
    cart = CartFactory(user=customer)
    CartItemFactory(cart=cart, product=product, quantity=1)
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
    session.payment_provider = provider
    session.save(update_fields=["payment_provider"])
    return session


def _create_intent(session, provider):
    ok, intent, msg = PaymentOrchestrationService.create_payment_intent(
        session, provider, RETURN_URL, CANCEL_URL
    )
    assert ok, f"intent creation failed: {msg}"
    return intent


def test_successful_card_pays_the_order(test_gateway_account):
    session = _ready_session(test_gateway_account, price="9.99")
    intent = _create_intent(session, test_gateway_account)

    ok, msg = PaymentOrchestrationService.confirm_payment_intent(intent, _card(CARD_SUCCESS))
    assert ok, msg

    intent.refresh_from_db()
    fp = footprint_for_order(intent.order)
    order = assert_exactly_one_order(fp)
    assert order.payment_status == "paid"
    assert_charged_equals(fp, Amount(Decimal("9.99"), "USD"))


def test_declined_card_leaves_no_paid_order(test_gateway_account):
    session = _ready_session(test_gateway_account, price="9.99")
    intent = _create_intent(session, test_gateway_account)

    # ...0002 is a *soft* decline (retryable): the gateway reports it as
    # requires_payment_method, so confirm may return ok=True — the load-bearing
    # invariant is that no order is paid and the intent never reaches succeeded.
    PaymentOrchestrationService.confirm_payment_intent(intent, _card(CARD_DECLINED))

    intent.refresh_from_db()
    assert intent.status != "succeeded"
    assert_no_paid_order(footprint_for_order(intent.order))  # no paid order, no capture


def test_3ds_card_requires_action_then_completes(test_gateway_account):
    session = _ready_session(test_gateway_account, price="9.99")
    intent = _create_intent(session, test_gateway_account)

    # First confirm: the gateway asks for 3DS.
    ok, _msg = PaymentOrchestrationService.confirm_payment_intent(intent, _card(CARD_3DS))
    assert ok
    intent.refresh_from_db()
    assert intent.status == "requires_action"
    fp = footprint_for_order(intent.order)
    assert_no_paid_order(fp)  # not paid until the challenge is completed

    # Re-confirm after the customer completes the challenge.
    ok2, msg2 = PaymentOrchestrationService.confirm_payment_intent(
        intent, _card(CARD_3DS, three_ds_completed=True)
    )
    assert ok2, msg2
    intent.refresh_from_db()
    assert intent.status == "succeeded"
    fp2 = footprint_for_order(intent.order)
    order = assert_exactly_one_order(fp2)
    assert order.payment_status == "paid"


def test_async_capture_settles_on_status_poll(test_gateway_account):
    """An order total ending in .19 makes the gateway defer capture
    (processing → succeeded on the delayed 'webhook'). The platform must not
    treat it as paid until a status poll observes the settlement."""
    import sys

    session = _ready_session(test_gateway_account, price="9.19")  # total ends .19
    intent = _create_intent(session, test_gateway_account)

    # Collapse the simulated webhook delay. It's read at CONFIRM time to set the
    # capture-ready timestamp, so the patch must wrap the confirm (and the poll).
    mod = sys.modules[test_gateway_account.get_provider_instance().__class__.__module__]
    with mock.patch.object(mod, "PROCESSING_DELAY_SECONDS", 0):
        ok, msg = PaymentOrchestrationService.confirm_payment_intent(intent, _card(CARD_SUCCESS))
        assert ok, msg
        intent.refresh_from_db()
        assert intent.status == "processing"  # capture deferred, not yet paid
        assert_no_paid_order(footprint_for_order(intent.order))

        # A status poll observes the settled capture and pays the order.
        PaymentOrchestrationService.verify_and_sync_payment_status(intent)

    intent.refresh_from_db()
    order = assert_exactly_one_order(footprint_for_order(intent.order))
    assert order.payment_status == "paid"
