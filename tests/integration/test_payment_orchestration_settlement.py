"""
Regression coverage for today's payment-orchestration settlement fix.

``PaymentOrchestrationService.confirm_payment_intent`` used to call
``intent.mark_succeeded()`` *before* ``handle_payment_success()``. The latter
opens with a guard::

    if intent.status == "succeeded":
        return True, _("Payment already processed")

so pre-marking the intent tripped the guard and settlement was skipped
entirely: the Order stayed ``payment_status='unpaid'`` with a succeeded intent,
no ``PaymentTransaction`` row was written, and the checkout session was never
cleared — a paid customer with an unpaid order.

The fix removes the premature ``mark_succeeded`` and lets
``handle_payment_success`` mark the intent succeeded *and* settle the order
atomically in the right order.

These tests stub the provider instance (``get_provider_instance`` is patched)
so no real PSP is contacted; everything else runs against the real DB.
"""

from datetime import timedelta
from decimal import Decimal
from unittest import mock

import pytest
from django.utils import timezone
from djmoney.money import Money

from payment_providers.models import PaymentIntent, PaymentTransaction
from payment_providers.services.payment_orchestration_service import (
    PaymentOrchestrationService,
)
from tests.factories import (
    CheckoutSessionFactory,
    OrderFactory,
    PaymentProviderAccountFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.checkout]

GET_PROVIDER = "payment_providers.models.PaymentProviderAccount.get_provider_instance"


def _stub_provider(status="succeeded"):
    """A MagicMock provider whose confirm_payment_intent reports success.

    MagicMock satisfies the ``hasattr(provider, "confirm_payment_intent")``
    check in the service and returns our canned response.
    """
    provider = mock.MagicMock()
    provider.confirm_payment_intent.return_value = {
        "success": True,
        "status": status,
        "payment_method_type": "card",
        "payment_method_last4": "4242",
    }
    return provider


@pytest.fixture
def provider_account():
    return PaymentProviderAccountFactory()


@pytest.fixture
def order():
    """A fresh, unpaid order (the state create_payment_intent leaves behind)."""
    return OrderFactory(payment_status="unpaid", amount_paid=Decimal("0.00"))


@pytest.fixture
def intent(provider_account, order):
    """A non-terminal PaymentIntent linked to the order + a checkout session."""
    session = CheckoutSessionFactory()
    return PaymentIntent.objects.create(
        checkout_session=session,
        provider_account=provider_account,
        order=order,
        provider_intent_id="pi_test_settlement_123",
        amount=Money(Decimal("114.87"), "USD"),
        status="processing",
        expires_at=timezone.now() + timedelta(hours=1),
    )


class TestConfirmPaymentIntentSettles:
    def test_confirm_payment_intent_settles_order(self, intent, order):
        """The core regression: confirm_payment_intent → succeeded provider
        response settles everything. Order becomes 'paid', a completed charge
        transaction is written, and the intent is 'succeeded'."""
        session_id = intent.checkout_session_id

        with mock.patch(GET_PROVIDER, return_value=_stub_provider()):
            success, message = PaymentOrchestrationService.confirm_payment_intent(
                intent, {"confirmation_token": "tok_123"}
            )

        assert success is True, message

        intent.refresh_from_db()
        assert intent.status == "succeeded"

        order.refresh_from_db()
        assert order.payment_status == "paid"
        assert order.paid_at is not None
        assert order.amount_paid == Money(Decimal("114.87"), "USD")

        txns = PaymentTransaction.objects.filter(order=order)
        assert txns.count() == 1
        txn = txns.get()
        assert txn.status == "completed"
        assert txn.transaction_type == "charge"
        assert txn.amount == Money(Decimal("114.87"), "USD")
        assert txn.payment_method_last4 == "4242"

        # Checkout session cleared as part of settlement.
        from cart.models import CheckoutSession

        assert not CheckoutSession.objects.filter(pk=session_id).exists()

    def test_handle_payment_success_is_idempotent(self, intent, order):
        """A second settlement of the same intent is a no-op — the succeeded
        guard returns early and no duplicate transaction is written (protects
        against double processing from concurrent webhook + poll)."""
        data = {"payment_method_type": "card", "payment_method_last4": "4242"}

        ok1, _ = PaymentOrchestrationService.handle_payment_success(intent, data)
        assert ok1 is True
        order.refresh_from_db()
        assert order.payment_status == "paid"
        assert PaymentTransaction.objects.filter(order=order).count() == 1

        ok2, msg2 = PaymentOrchestrationService.handle_payment_success(intent, data)
        assert ok2 is True
        assert PaymentTransaction.objects.filter(order=order).count() == 1

    def test_pre_marking_succeeded_strands_the_order_unpaid(self, intent, order):
        """Documents the exact pre-fix failure mode and proves the guard is
        real: if the intent is marked succeeded *before* settlement runs (what
        the old confirm_payment_intent did), handle_payment_success short-
        circuits and the order is left unpaid with no transaction. The fix
        avoids this by never pre-marking — see test_confirm_payment_intent_
        settles_order, which drives the same success response and DOES settle.
        """
        intent.mark_succeeded({"status": "succeeded"})

        ok, _ = PaymentOrchestrationService.handle_payment_success(intent, {})
        assert ok is True  # "already processed"

        order.refresh_from_db()
        assert order.payment_status == "unpaid"
        assert not PaymentTransaction.objects.filter(order=order).exists()
