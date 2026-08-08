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
from payment_providers.models import PaymentProviderAccount, PaymentTransaction
from payment_providers.services.refund_service import RefundService
from tests.factories import OrderFactory, PaymentProviderAccountFactory

pytestmark = [pytest.mark.django_db, pytest.mark.invariant, pytest.mark.voucher_gift_card]

USD = "USD"
CHARGE_TOTAL = Decimal("120.00")

# RefundService builds its provider client via
# PaymentProviderAccount.get_provider_instance() — the same path every live
# payment flow uses (it decrypts credentials, runs the sandbox guard, and
# constructs the provider with `credentials=`). Stub THAT so no real PSP is
# contacted but the real refund bookkeeping runs. The provider contract is
# `refund(...)`; stubbing a fictional `create_refund` (as this suite used to)
# is exactly what let the create_refund/credentials bug sail through CI.
PROVIDER_FACTORY = "payment_providers.models.PaymentProviderAccount.get_provider_instance"


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


def _stub_provider():
    """Patch PaymentProviderAccount.get_provider_instance -> a provider whose
    real ``refund(...)`` reports success (no PSP contacted)."""
    provider_instance = mock.MagicMock()
    provider_instance.refund.return_value = {
        "success": True,
        "provider_refund_id": "re_stub_1",
    }
    return mock.patch(PROVIDER_FACTORY, return_value=provider_instance)


def test_full_refund_reconciles(paid_order_with_charge):
    """A full refund returns exactly the captured amount; order -> refunded."""
    order, charge = paid_order_with_charge

    with _stub_provider():
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

    with _stub_provider():
        ok, _txn, msg = RefundService.create_refund(charge, refund_amount=Decimal("30.00"))
    assert ok, msg

    fp = footprint_for_order(order)
    assert_refund_reconciles(fp)
    assert total_refunded(fp).close_to(Amount(Decimal("30.00"), USD))
    assert fp.orders[0].payment_status == "partially_refunded"


def test_multiple_partial_refunds_reconcile(paid_order_with_charge):
    """Two partial refunds sum correctly and never over-count."""
    order, charge = paid_order_with_charge

    with _stub_provider():
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

    with _stub_provider():
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

    with _stub_provider():
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

    with _stub_provider():
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

    with _stub_provider():
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


def test_refund_uses_provider_refund_contract_with_idempotency_key(paid_order_with_charge):
    """Regression for the platform-wide gateway-refund bug.

    RefundService must (1) build the provider via ``get_provider_instance()`` —
    NOT by handing the account model to ``provider_class(...)``, which raised
    TypeError inside ``_select_credentials`` — and (2) call the real
    ``refund(...)`` contract (no provider defines ``create_refund``), passing a
    Decimal amount and ``refund_id`` in the metadata so the PSP can derive a
    stable idempotency key and a retried refund cannot pay out twice.

    The old suite hid all of this: it stubbed a fictional ``create_refund`` on a
    MagicMock, which auto-vivifies any attribute and accepts any constructor
    args, so neither the wrong method name nor the wrong constructor arg failed.
    """
    order, charge = paid_order_with_charge

    provider_instance = mock.MagicMock()
    provider_instance.refund.return_value = {
        "success": True,
        "provider_refund_id": "re_stub_idem",
    }
    with mock.patch.object(
        PaymentProviderAccount, "get_provider_instance", return_value=provider_instance
    ):
        ok, refund_txn, msg = RefundService.create_refund(charge, refund_amount=Decimal("40.00"))

    assert ok, msg
    # The fictional method must never be called; the real contract must be.
    provider_instance.create_refund.assert_not_called()
    provider_instance.refund.assert_called_once()

    _args, kwargs = provider_instance.refund.call_args
    # Decimal, not float — float risks money-precision drift converting to minor units.
    assert kwargs["amount"] == Decimal("40.00")
    assert isinstance(kwargs["amount"], Decimal)
    # refund_id is the stored refund row's id, so a PSP-side retry de-dupes.
    assert kwargs["metadata"]["refund_id"] == refund_txn.transaction_id


# --- Provider contract-drift guard --------------------------------------------
#
# Providers are pluggable/marketplace-distributed, so their real refund()
# signatures can drift from the base contract. These use REAL classes (not
# MagicMock, which accepts any kwarg and would hide the drift) so
# inspect.signature sees the true parameter list.


class _ConformingProvider:
    """refund() honours the base contract (accepts metadata)."""

    def __init__(self):
        self.calls = []

    def refund(self, transaction_id, amount=None, reason=None, metadata=None):
        self.calls.append(
            {
                "transaction_id": transaction_id,
                "amount": amount,
                "reason": reason,
                "metadata": metadata,
            }
        )
        return {"success": True, "provider_refund_id": "re_conforming"}


class _NoMetadataProvider:
    """Airwallex-shaped drift: refund() omits metadata (and has no **kwargs)."""

    def __init__(self):
        self.calls = []

    def refund(self, transaction_id, amount=None, reason=None):
        self.calls.append({"transaction_id": transaction_id, "amount": amount, "reason": reason})
        return {"success": True, "provider_refund_id": "re_no_metadata"}


def test_conforming_provider_receives_idempotency_metadata(paid_order_with_charge):
    """A provider that accepts metadata gets refund_id passed through."""
    order, charge = paid_order_with_charge
    provider = _ConformingProvider()

    with mock.patch.object(PaymentProviderAccount, "get_provider_instance", return_value=provider):
        ok, refund_txn, msg = RefundService.create_refund(charge, refund_amount=Decimal("40.00"))

    assert ok, msg
    assert provider.calls[0]["metadata"]["refund_id"] == refund_txn.transaction_id


def test_provider_without_metadata_param_still_refunds(paid_order_with_charge, caplog):
    """Regression for the Airwallex TypeError: a provider whose refund() has no
    `metadata` parameter must NOT crash the refund. The platform omits the
    kwarg (idempotency unavailable for that provider) and warns loudly, rather
    than raising TypeError that the broad except turns into a generic failure."""
    order, charge = paid_order_with_charge
    provider = _NoMetadataProvider()

    with mock.patch.object(PaymentProviderAccount, "get_provider_instance", return_value=provider):
        with caplog.at_level("WARNING"):
            ok, refund_txn, msg = RefundService.create_refund(
                charge, refund_amount=Decimal("40.00")
            )

    assert ok, msg  # refund succeeded despite the signature drift
    assert refund_txn is not None
    # metadata was NOT forced onto a signature that can't take it.
    assert "metadata" not in provider.calls[0]
    # ...and the drift is surfaced, not swallowed.
    assert any("does not accept a `metadata`" in r.message for r in caplog.records)


def test_callable_accepts_kwarg_detects_signature_shapes():
    """Unit test for the drift detector that gates metadata passing."""
    accepts = RefundService._callable_accepts_kwarg

    def with_metadata(transaction_id, amount=None, reason=None, metadata=None):
        pass

    def without_metadata(transaction_id, amount=None, reason=None):
        pass

    def with_var_kwargs(transaction_id, **kwargs):
        pass

    assert accepts(with_metadata, "metadata") is True
    assert accepts(without_metadata, "metadata") is False
    assert accepts(with_var_kwargs, "metadata") is True  # **kwargs swallows it

    # Un-introspectable callables default to True (don't strip a kwarg blindly).
    # inspect.signature raising ValueError/TypeError is the fallback path.
    with mock.patch(
        "payment_providers.services.refund_service.inspect.signature",
        side_effect=ValueError("no signature"),
    ):
        assert accepts(without_metadata, "metadata") is True


# --- Cross-invocation refund idempotency --------------------------------------


def test_refund_with_idempotency_key_is_idempotent_across_calls(paid_order_with_charge):
    """A retry with the same idempotency_key returns the SAME refund row and does
    NOT hit the PSP again. Closes the double-pay window codex flagged: PSP
    succeeds, the DB write/order update then fails, the caller retries. The
    deterministic transaction_id + pre-PSP short-circuit make the retry inert,
    and the PSP also receives the stable key so it de-dupes if our row rolled
    back after its payout."""
    order, charge = paid_order_with_charge
    provider = _ConformingProvider()

    with mock.patch.object(PaymentProviderAccount, "get_provider_instance", return_value=provider):
        ok1, txn1, _m1 = RefundService.create_refund(
            charge, refund_amount=Decimal("30.00"), idempotency_key=4242
        )
        ok2, txn2, m2 = RefundService.create_refund(
            charge, refund_amount=Decimal("30.00"), idempotency_key=4242
        )

    assert ok1 and ok2, m2
    assert txn1.pk == txn2.pk  # same row — not a second refund
    assert len(provider.calls) == 1  # PSP hit exactly once
    assert "already processed" in m2.lower()
    # Deterministic id keyed off the capture + refund identity.
    assert txn1.transaction_id == f"rfnd:{charge.transaction_id}:4242"
    # PSP got the stable key, so it de-dupes even if our row had rolled back.
    assert provider.calls[0]["metadata"]["idempotency_key"] == "4242"
    # ...and only one refund row exists for the capture.
    assert (
        PaymentTransaction.objects.filter(
            parent_transaction=charge, transaction_type="refund"
        ).count()
        == 1
    )


def test_refund_without_idempotency_key_is_not_deduped(paid_order_with_charge):
    """Without a key, two same-amount partial refunds are DISTINCT refunds (random
    ids). Legitimate identical partials must not collapse — the reason we key on a
    caller-supplied identity rather than on (capture, amount)."""
    order, charge = paid_order_with_charge
    provider = _ConformingProvider()

    with mock.patch.object(PaymentProviderAccount, "get_provider_instance", return_value=provider):
        ok1, txn1, _m1 = RefundService.create_refund(charge, refund_amount=Decimal("30.00"))
        ok2, txn2, _m2 = RefundService.create_refund(charge, refund_amount=Decimal("30.00"))

    assert ok1 and ok2
    assert txn1.pk != txn2.pk
    assert len(provider.calls) == 2
