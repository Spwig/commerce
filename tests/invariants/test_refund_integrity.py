"""
Tier-1 refund-integrity invariants (plan invariant #8: refunds reconcile).

Drives the REAL ``RefundService.create_refund`` (the PSP boundary stubbed to
report success) against a paid order with a completed gateway charge, and
asserts the transaction footprint reconciles:

  - a full refund returns exactly the captured amount and moves the order to
    ``refunded``;
  - a partial refund returns only its part and moves the order to
    ``partially_refunded``;
  - multiple partial refunds sum correctly and never over-count;
  - a refund exceeding the remaining capacity is REFUSED — no refund row is
    written and ``amount_refunded`` is unchanged (invariant #8's teeth: you
    cannot refund more than was captured).

``assert_refund_reconciles`` checks the load-bearing identity: the order's
recorded ``amount_refunded`` equals the sum of completed refund transactions.
"""

from decimal import Decimal
from unittest import mock

import pytest
from djmoney.money import Money

from commerce_footprint import (
    assert_refund_reconciles,
    total_captured,
    total_refunded,
)
from commerce_footprint.footprint import Amount
from commerce_footprint.orm_backend import footprint_for_order
from payment_providers.models import PaymentTransaction
from payment_providers.services.refund_service import RefundService
from tests.factories import OrderFactory, PaymentProviderAccountFactory

pytestmark = [pytest.mark.django_db, pytest.mark.invariant, pytest.mark.voucher_gift_card]

USD = "USD"
CHARGE_TOTAL = Decimal("120.00")

# RefundService resolves the provider via this symbol; stub it so no real PSP
# is contacted but the real refund bookkeeping runs.
REGISTRY = "payment_providers.services.refund_service.ProviderRegistry.get_provider"


def _money(v):
    return Money(Decimal(str(v)), USD)


@pytest.fixture
def paid_order_with_charge(db, site_settings):
    """A $120 paid order with one completed gateway charge to refund against."""
    order = OrderFactory(
        payment_status="paid",
        status="processing",
        total_amount=CHARGE_TOTAL,
        total_amount_currency=USD,
        amount_paid=CHARGE_TOTAL,
        amount_paid_currency=USD,
    )
    charge = PaymentTransaction.objects.create(
        transaction_id="chg-gateway-refund-1",
        order=order,
        provider_account=PaymentProviderAccountFactory(),
        tender_type=PaymentTransaction.TENDER_GATEWAY,
        transaction_type="charge",
        status="completed",
        amount=_money(CHARGE_TOTAL),
        settlement_amount=_money(CHARGE_TOTAL),
        provider_transaction_id="ch_stub_refund_1",
    )
    return order, charge


def _stub_registry():
    """Patch ProviderRegistry.get_provider -> a provider class whose instance
    reports a successful refund."""
    provider_instance = mock.MagicMock()
    provider_instance.create_refund.return_value = {
        "success": True,
        "provider_refund_id": "re_stub_1",
    }
    provider_class = mock.MagicMock(return_value=provider_instance)
    return mock.patch(REGISTRY, return_value=provider_class)


def test_full_refund_reconciles(paid_order_with_charge):
    """A full refund returns exactly the captured amount; order -> refunded."""
    order, charge = paid_order_with_charge

    with _stub_registry():
        ok, refund_txn, msg = RefundService.create_refund(charge, refund_amount=None)
    assert ok, msg
    assert refund_txn is not None

    fp = footprint_for_order(order)
    assert_refund_reconciles(fp)
    assert total_refunded(fp).close_to(Amount(CHARGE_TOTAL, USD))
    assert total_captured(fp).close_to(Amount(CHARGE_TOTAL, USD))
    assert fp.orders[0].payment_status == "refunded"


def test_partial_refund_reconciles(paid_order_with_charge):
    """A partial refund returns only its part; order -> partially_refunded."""
    order, charge = paid_order_with_charge

    with _stub_registry():
        ok, _txn, msg = RefundService.create_refund(charge, refund_amount=Decimal("30.00"))
    assert ok, msg

    fp = footprint_for_order(order)
    assert_refund_reconciles(fp)
    assert total_refunded(fp).close_to(Amount(Decimal("30.00"), USD))
    assert fp.orders[0].payment_status == "partially_refunded"


def test_multiple_partial_refunds_reconcile(paid_order_with_charge):
    """Two partial refunds sum correctly and never over-count."""
    order, charge = paid_order_with_charge

    with _stub_registry():
        ok1, _t1, m1 = RefundService.create_refund(charge, refund_amount=Decimal("30.00"))
        ok2, _t2, m2 = RefundService.create_refund(charge, refund_amount=Decimal("30.00"))
    assert ok1 and ok2, (m1, m2)

    fp = footprint_for_order(order)
    assert_refund_reconciles(fp)
    assert total_refunded(fp).close_to(Amount(Decimal("60.00"), USD))
    assert fp.orders[0].payment_status == "partially_refunded"  # 60 < 120


def test_over_refund_is_refused(paid_order_with_charge):
    """Refunding more than was captured is refused: no refund row, no change to
    amount_refunded. This is invariant #8's teeth."""
    order, charge = paid_order_with_charge

    with _stub_registry():
        ok, refund_txn, msg = RefundService.create_refund(
            charge,
            refund_amount=Decimal("130.00"),  # > 120 captured
        )
    assert not ok
    assert refund_txn is None
    assert "exceeds" in msg.lower()

    fp = footprint_for_order(order)
    # No completed refund exists, and the order never recorded a refund.
    assert total_refunded(fp) is None
    assert fp.orders[0].amount_refunded.value == Decimal("0.00")
    assert fp.orders[0].payment_status == "paid"
    assert_refund_reconciles(fp)  # 0 == 0, trivially reconciled


def test_zero_refund_is_refused(paid_order_with_charge):
    """A Decimal("0") refund must be rejected as non-positive, NOT silently
    promoted to a full refund (the `refund_amount or ...` truthiness trap)."""
    order, charge = paid_order_with_charge

    with _stub_registry():
        ok, refund_txn, msg = RefundService.create_refund(charge, refund_amount=Decimal("0.00"))
    assert not ok
    assert refund_txn is None
    assert "greater than zero" in msg.lower()

    fp = footprint_for_order(order)
    assert total_refunded(fp) is None
    assert fp.orders[0].payment_status == "paid"  # unchanged — no full refund


def test_capacity_is_exhausted_after_a_full_refund(paid_order_with_charge):
    """Once a capture is fully refunded, no further refund against it is
    allowed — the per-capture capacity gate that the row lock in create_refund
    protects. (The lock closes the *concurrent* version of this race; here we
    prove the capacity accounting itself is correct sequentially.)"""
    order, charge = paid_order_with_charge

    with _stub_registry():
        ok1, _t1, m1 = RefundService.create_refund(charge, refund_amount=None)  # full 120
        ok2, txn2, m2 = RefundService.create_refund(charge, refund_amount=Decimal("1.00"))
    assert ok1, m1
    assert not ok2  # capacity exhausted
    assert txn2 is None
    assert "exceeds" in m2.lower()

    fp = footprint_for_order(order)
    assert_refund_reconciles(fp)
    assert total_refunded(fp).close_to(Amount(CHARGE_TOTAL, USD))  # not 121


def test_pos_web_provider_refund_succeeds(paid_order_with_charge):
    """Regression for the POS web-refund route, guarding BOTH bugs found here:

    - the charge lookup used the dead ``status="succeeded"`` vocabulary and
      matched zero rows (so it always errored "No payment transaction found");
    - even once found, ``create_refund`` raised on the Money/Decimal compare.

    Drives the real ``_process_provider_refund_web`` with the production
    Decimal amount; a clean run returns ``None`` (no error) and reconciles.
    """
    from pos_api.views.orders import _process_provider_refund_web

    order, charge = paid_order_with_charge
    # The lookup keys on the provider component slug; the factory's account uses
    # the "stripe" component, so the refund_method is "provider_stripe".
    slug = charge.provider_account.component.slug

    with _stub_registry():
        error = _process_provider_refund_web(
            order,
            refund_method=f"provider_{slug}",
            refund_amount=Decimal("50.00"),
            reason="pos web refund",
            currency=USD,
        )

    assert error is None, f"POS web refund returned an error: {error}"
    fp = footprint_for_order(order)
    assert_refund_reconciles(fp)
    assert total_refunded(fp).close_to(Amount(Decimal("50.00"), USD))
