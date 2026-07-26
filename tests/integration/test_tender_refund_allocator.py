"""
Splitting a refund across the tenders that actually paid for an order.

Refunds did not work at all before this. ``RefundService.validate_refund_amount``
called Python's builtin ``sum("amount")`` on a string — a TypeError on every
invocation — and every filter used ``status="succeeded"``, which is not in
``PaymentTransaction.STATUS_CHOICES``, so it matched zero rows.

That breakage was protective, which is what makes this area dangerous. POS
passes gross ``order.total_amount`` into a charge row that has held only
``amount_due`` since the P2.2 double-charge fix, so simply repairing the status
vocabulary turns a dead rail into a live over-refund: a 120 order paid
40 card + 80 gateway would refund 120 through the gateway and the merchant eats
the difference, looking exactly like a working refund.

Hence the canonical fixture used throughout: **120 = 80 gateway + 40 gift card**,
refunded 30 / 30 / 60. Every test asserts PER LEG, never just the total — a test
that only checks "120 came back" passes the over-refund.

Plan: docs/.claude_code/plans/wondrous-moseying-wolf.md (R2, P2.4)
"""

from decimal import Decimal

import pytest
from djmoney.money import Money

from catalog.models import GiftCard
from orders.services.tender_refund_allocator import (
    RefundAllocationError,
    TenderRefundAllocator,
)
from payment_providers.models import PaymentTransaction
from tests.factories import OrderFactory, ProductFactory

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
    pytest.mark.r2,
]

USD = "USD"


def _money(v):
    return Money(Decimal(str(v)), USD)


@pytest.fixture
def gift_card_product(db):
    return ProductFactory(product_type="gift_card", status="published")


def _card(gift_card_product, value="40.00"):
    return GiftCard.objects.create(
        product=gift_card_product,
        initial_value=_money(value),
        recipient_email="recipient@test.spwig.com",
        is_active=True,
    )


def _split_tender_order(gift_card_product, gateway="80.00", card="40.00"):
    """120 order: 80 taken by the gateway, 40 captured from a gift card."""
    order = OrderFactory(
        payment_status="paid",
        total_amount=Decimal("120.00"),
        total_amount_currency=USD,
        amount_paid=Decimal("120.00"),
        amount_paid_currency=USD,
    )
    gateway_row = PaymentTransaction.objects.create(
        transaction_id="chg-gateway-1",
        order=order,
        tender_type=PaymentTransaction.TENDER_GATEWAY,
        transaction_type="charge",
        status="completed",
        amount=_money(gateway),
        settlement_amount=_money(gateway),
        provider_account=None,
    )
    card_obj = _card(gift_card_product, value=card)
    card_row = PaymentTransaction.objects.create(
        transaction_id="cap-giftcard-1",
        order=order,
        tender_type=PaymentTransaction.TENDER_GIFT_CARD,
        transaction_type="capture",
        status="completed",
        gift_card=card_obj,
        amount=_money(card),
        settlement_amount=_money(card),
        provider_account=None,
    )
    # The capture spent the card down.
    card_obj.current_balance = _money("0.00")
    card_obj.save(update_fields=["current_balance"])
    return order, gateway_row, card_row, card_obj


class TestOrdering:
    def test_gift_card_is_refunded_before_the_gateway(self, gift_card_product):
        """
        Refunding cash the merchant never collected is the worse failure, and
        internal-first closes buy-with-stolen-card -> spend -> refund-elsewhere.
        """
        order, gateway_row, card_row, _card_obj = _split_tender_order(gift_card_product)

        legs = TenderRefundAllocator.plan(order, _money("30.00"))

        assert len(legs) == 1
        assert legs[0]["capture"].pk == card_row.pk
        assert legs[0]["amount"] == _money("30.00")

    def test_tender_class_beats_recency(self, gift_card_product):
        """
        POS writes its gift card leg BEFORE the card leg, so reading
        reverse-chronological as primary would silently invert the
        anti-laundering default there while web orders kept behaving — an
        invisible bug on exactly the surface where it matters most.
        """
        assert TenderRefundAllocator.get_tender_priority(
            "gift_card"
        ) < TenderRefundAllocator.get_tender_priority("gateway")

    def test_an_unknown_tender_refunds_last(self):
        assert TenderRefundAllocator.get_tender_priority(
            "something_new"
        ) > TenderRefundAllocator.get_tender_priority("gateway")


class TestTheCanonicalSplit:
    """120 = 80 gateway + 40 card, refunded 30 / 30 / 60."""

    def test_first_thirty_comes_entirely_off_the_card(self, gift_card_product):
        order, _gw, card_row, _c = _split_tender_order(gift_card_product)

        legs = TenderRefundAllocator.plan(order, _money("30.00"))

        assert [(leg["tender_type"], leg["amount"]) for leg in legs] == [
            ("gift_card", _money("30.00"))
        ]
        assert legs[0]["capture"].pk == card_row.pk

    def test_a_refund_spanning_both_tenders_splits_correctly(self, gift_card_product):
        """60 refund: the card can only fund 40, so 20 falls to the gateway."""
        order, gateway_row, card_row, _c = _split_tender_order(gift_card_product)

        legs = TenderRefundAllocator.plan(order, _money("60.00"))

        assert [(leg["tender_type"], leg["amount"]) for leg in legs] == [
            ("gift_card", _money("40.00")),
            ("gateway", _money("20.00")),
        ]
        assert sum((leg["amount"] for leg in legs), _money("0")) == _money("60.00")

    def test_the_full_120_exhausts_both_and_no_more(self, gift_card_product):
        order, _gw, _cr, _c = _split_tender_order(gift_card_product)

        legs = TenderRefundAllocator.plan(order, _money("120.00"))

        assert sum((leg["amount"] for leg in legs), _money("0")) == _money("120.00")
        by_tender = {leg["tender_type"]: leg["amount"] for leg in legs}
        assert by_tender == {"gift_card": _money("40.00"), "gateway": _money("80.00")}


class TestCapacityIsPerCaptureRow:
    """
    Invariant I3: sum(refunds) <= sum(captures), PER ROW.

    Capping on Order.amount_paid instead would let gift card value be refunded
    out through the gateway — cash the merchant never collected for it.
    """

    def test_refunding_more_than_was_captured_is_refused(self, gift_card_product):
        order, _gw, _cr, _c = _split_tender_order(gift_card_product)

        with pytest.raises(RefundAllocationError, match="only"):
            TenderRefundAllocator.plan(order, _money("150.00"))

    def test_prior_refunds_reduce_the_capacity_of_their_own_row(self, gift_card_product):
        order, _gw, card_row, card_obj = _split_tender_order(gift_card_product)
        PaymentTransaction.objects.create(
            transaction_id="gc-ref:cap-giftcard-1:1",
            order=order,
            gift_card=card_obj,
            parent_transaction=card_row,
            tender_type=PaymentTransaction.TENDER_GIFT_CARD,
            transaction_type="refund",
            status="completed",
            amount=_money("30.00"),
            settlement_amount=_money("30.00"),
            provider_account=None,
        )

        assert TenderRefundAllocator.refundable_on(card_row) == _money("10.00")

        legs = TenderRefundAllocator.plan(order, _money("30.00"))
        by_tender = {leg["tender_type"]: leg["amount"] for leg in legs}
        assert by_tender == {"gift_card": _money("10.00"), "gateway": _money("20.00")}

    def test_pending_refunds_also_consume_capacity(self, gift_card_product):
        """
        Otherwise two concurrent refunds are each told the same room is free
        and the row is over-refunded.
        """
        order, _gw, card_row, card_obj = _split_tender_order(gift_card_product)
        PaymentTransaction.objects.create(
            transaction_id="gc-ref:cap-giftcard-1:pending",
            order=order,
            gift_card=card_obj,
            parent_transaction=card_row,
            tender_type=PaymentTransaction.TENDER_GIFT_CARD,
            transaction_type="refund",
            status="pending",
            amount=_money("40.00"),
            settlement_amount=_money("40.00"),
            provider_account=None,
        )

        assert TenderRefundAllocator.refundable_on(card_row) == _money("0.00")

    def test_authorize_rows_are_never_refundable(self, gift_card_product):
        """
        A hold is a reservation, and since P2.2f caps captures at what the order
        owed, a hold can exceed what was actually taken. Refunding against it
        returns money that never moved.
        """
        order, _gw, _cr, card_obj = _split_tender_order(gift_card_product)
        PaymentTransaction.objects.create(
            transaction_id="gc-auth:stray",
            order=order,
            gift_card=card_obj,
            tender_type=PaymentTransaction.TENDER_GIFT_CARD,
            transaction_type="authorize",
            status="authorized",
            amount=_money("500.00"),
            settlement_amount=_money("500.00"),
            provider_account=None,
        )

        captures = TenderRefundAllocator.captures_for(order)
        assert all(c.transaction_type in ("capture", "charge") for c in captures)
        with pytest.raises(RefundAllocationError):
            TenderRefundAllocator.plan(order, _money("150.00"))


class TestRefusals:
    def test_an_order_with_no_captures_cannot_be_refunded(self):
        order = OrderFactory(payment_status="paid")

        with pytest.raises(RefundAllocationError, match="no completed captures"):
            TenderRefundAllocator.plan(order, _money("10.00"))

    def test_a_zero_or_negative_refund_is_refused(self, gift_card_product):
        order, _gw, _cr, _c = _split_tender_order(gift_card_product)

        with pytest.raises(RefundAllocationError):
            TenderRefundAllocator.plan(order, _money("0.00"))


class TestNoRounding:
    @pytest.mark.parametrize("amount", ["10.00", "40.00", "60.00", "120.00", "0.01"])
    def test_legs_sum_exactly_to_the_request(self, gift_card_product, amount):
        order, _gw, _cr, _c = _split_tender_order(gift_card_product)

        legs = TenderRefundAllocator.plan(order, _money(amount))

        assert sum((leg["amount"] for leg in legs), _money("0")) == _money(amount)


class TestRefundExecuteIsTheFunnel:
    """
    Every refund path must move money through the allocator.

    Before P2.4 none of the merchant-facing paths did. ``Refund.complete()`` set
    a status and saved. The mobile admin API incremented
    ``order.amount_refunded`` under a comment conceding it was "simplified -
    actual refund would involve payment provider". So a merchant could refund
    from the admin or the phone, see "refunded" in both places, and the customer
    would receive nothing — with no error anywhere.
    """

    def test_execute_moves_money_and_completes(self, gift_card_product):
        from orders.models import Refund

        order, _gw, card_row, card_obj = _split_tender_order(gift_card_product)
        refund = Refund.objects.create(
            order=order,
            refund_type="partial",
            reason="customer_request",
            status="processing",
            total_amount=_money("30.00"),
        )

        refund.execute()

        refund.refresh_from_db()
        assert refund.status == "completed"
        # Gift card first: the whole 30 comes off the card, none off the gateway.
        card_obj.refresh_from_db()
        assert card_obj.current_balance == _money("30.00")
        assert (
            PaymentTransaction.objects.filter(
                parent_transaction=card_row, transaction_type="refund"
            ).count()
            == 1
        )

    def test_execute_is_idempotent(self, gift_card_product):
        """A retried request must not pay the customer twice."""
        from orders.models import Refund

        order, _gw, _cr, card_obj = _split_tender_order(gift_card_product)
        refund = Refund.objects.create(
            order=order,
            refund_type="partial",
            reason="customer_request",
            status="processing",
            total_amount=_money("30.00"),
        )

        refund.execute()
        refund.execute()

        card_obj.refresh_from_db()
        assert card_obj.current_balance == _money("30.00"), "The refund paid out twice."

    def test_an_unfundable_refund_fails_rather_than_half_completing(self, gift_card_product):
        from orders.models import Refund
        from orders.services.tender_refund_allocator import RefundAllocationError

        order, _gw, _cr, _c = _split_tender_order(gift_card_product)
        refund = Refund.objects.create(
            order=order,
            refund_type="full",
            reason="customer_request",
            status="processing",
            total_amount=_money("500.00"),
        )

        with pytest.raises(RefundAllocationError):
            refund.execute()

        refund.refresh_from_db()
        assert refund.status == "failed"
        assert not PaymentTransaction.objects.filter(
            order=order, transaction_type="refund"
        ).exists()

    def test_amount_refunded_is_derived_from_the_ledger(self, gift_card_product):
        """Not incremented — a field that drifts the moment anything bypasses it."""
        from orders.models import Refund

        order, _gw, _cr, _c = _split_tender_order(gift_card_product)
        Refund.objects.create(
            order=order,
            refund_type="partial",
            reason="customer_request",
            status="processing",
            total_amount=_money("40.00"),
        ).execute()

        order.refresh_from_db()
        assert order.amount_refunded == _money("40.00")
        assert order.payment_status == "partially_refunded"


class TestGatewayLegGuardRegression:
    """
    HIGH #1 (security review): the gateway refund leg was dead.

    RefundService.create_refund had two early-return guards left on the old
    vocabulary — status != "succeeded" and transaction_type != "charge" — while
    real captures are status="completed" and transaction_type "capture" or
    "charge". So every gateway leg returned "Only successful payments can be
    refunded", the allocator raised, and the whole refund failed. No execute()
    test crossed onto the gateway leg, so it went unnoticed.

    These pin the guard directly (a full end-to-end gateway refund needs a
    provider account and a registered provider, which is out of scope here —
    the guard is where the bug lived).
    """

    def _completed_capture(self, order, tender_type, ttype="capture"):
        return PaymentTransaction.objects.create(
            transaction_id=f"cap-{tender_type}-{ttype}",
            order=order,
            tender_type=tender_type,
            transaction_type=ttype,
            status="completed",
            amount=_money("80.00"),
            settlement_amount=_money("80.00"),
            provider_account=None,
        )

    def test_a_completed_capture_gets_past_the_vocabulary_guard(self, gift_card_product):
        from payment_providers.services.refund_service import RefundService

        order = OrderFactory(payment_status="paid")
        capture = self._completed_capture(order, "gateway", "capture")

        success, _txn, message = RefundService.create_refund(
            original_transaction=capture, refund_amount=Decimal("10.00")
        )

        # It will still fail — there is no provider behind a None account — but
        # NOT with the vocabulary-guard message. That is the regression.
        assert str(message) != "Only successful payments can be refunded", (
            "A completed capture was rejected by the dead status guard."
        )
        assert str(message) != "Only charge transactions can be refunded", (
            "A capture row was rejected by the charge-only guard."
        )

    def test_a_charge_row_also_passes(self, gift_card_product):
        from payment_providers.services.refund_service import RefundService

        order = OrderFactory(payment_status="paid")
        capture = self._completed_capture(order, "gateway", "charge")

        _success, _txn, message = RefundService.create_refund(
            original_transaction=capture, refund_amount=Decimal("10.00")
        )
        assert str(message) != "Only successful payments can be refunded"

    def test_a_pending_transaction_is_still_refused(self, gift_card_product):
        from payment_providers.services.refund_service import RefundService

        order = OrderFactory(payment_status="paid")
        capture = self._completed_capture(order, "gateway", "capture")
        capture.status = "pending"
        capture.save(update_fields=["status"])

        success, _txn, message = RefundService.create_refund(
            original_transaction=capture, refund_amount=Decimal("10.00")
        )
        assert success is False
        assert str(message) == "Only successful payments can be refunded"

    def test_an_authorize_row_is_still_refused(self, gift_card_product):
        from payment_providers.services.refund_service import RefundService

        order = OrderFactory(payment_status="paid")
        auth = self._completed_capture(order, "gateway", "authorize")

        success, _txn, message = RefundService.create_refund(
            original_transaction=auth, refund_amount=Decimal("10.00")
        )
        assert success is False
        assert str(message) == "Only charge transactions can be refunded"


class TestConcurrentRefundsRespectCapacity:
    """
    HIGH #2 (security review): the order lock was released after plan(), before
    the money moved, so two Refund rows on one order could each plan against the
    same capacity and both pay out.

    A single-threaded test cannot reproduce the race, but it CAN pin the
    property that makes the lock-across-execution correct: a second refund plans
    against the first's committed rows. Executed back to back, total refunded
    can never exceed the captured total.
    """

    def test_two_sequential_refunds_cannot_exceed_captured(self, gift_card_product):
        from orders.models import Refund

        order, _gw, _cr, card_obj = _split_tender_order(gift_card_product)  # 40 card capacity

        first = Refund.objects.create(
            order=order,
            refund_type="partial",
            reason="customer_request",
            status="processing",
            total_amount=_money("30.00"),
        )
        first.execute()

        # The card only has 10 left; a second 10 refund drains it exactly.
        second = Refund.objects.create(
            order=order,
            refund_type="partial",
            reason="customer_request",
            status="processing",
            total_amount=_money("10.00"),
        )
        second.execute()

        card_obj.refresh_from_db()
        assert card_obj.current_balance == _money("40.00"), (
            "The card was refunded more than the 40 it captured."
        )
        order.refresh_from_db()
        assert order.amount_refunded == _money("40.00")

    def test_execute_requires_a_refund_identity(self, gift_card_product):
        """LOW #6: the allocator must not silently take the non-idempotent counter path."""
        from orders.services.tender_refund_allocator import (
            RefundAllocationError,
            TenderRefundAllocator,
        )

        order, _gw, _cr, _c = _split_tender_order(gift_card_product)
        with pytest.raises(RefundAllocationError, match="requires a refund"):
            TenderRefundAllocator.execute(order, _money("10.00"))


class TestDeadCardRefundPolicy:
    """
    MED #4 (security review): expired and deactivated cards must be treated
    differently on refund.

    Expiry is a clock event — the customer did nothing — so a refund mints a
    fresh no-expiry replacement. Deactivation is a MERCHANT decision (chargeback
    freeze, stolen-instrument flag), so auto-minting a spendable replacement
    would hand back exactly the value the merchant froze.
    """

    def test_refund_to_an_expired_card_mints_a_replacement(self, gift_card_product):
        from datetime import timedelta

        from django.utils import timezone

        from catalog.services.gift_card_tender_service import GiftCardTenderService

        order, _gw, card_row, card_obj = _split_tender_order(gift_card_product)
        card_obj.expires_at = timezone.now() - timedelta(days=1)
        card_obj.save(update_fields=["expires_at"])

        txn = GiftCardTenderService.refund_to_card(
            card_row, amount=_money("25.00"), refund_ref="med4-expired"
        )

        replacement = txn.gift_card
        assert replacement.pk != card_obj.pk, "Expired card was credited directly."
        assert replacement.current_balance == _money("25.00")
        assert replacement.expires_at is None
        assert replacement.recipient_email == card_obj.recipient_email

    def test_refund_to_a_deactivated_card_is_refused(self, gift_card_product):
        from catalog.services.gift_card_tender_service import (
            GiftCardTenderError,
            GiftCardTenderService,
        )

        order, _gw, card_row, card_obj = _split_tender_order(gift_card_product)
        card_obj.is_active = False
        card_obj.save(update_fields=["is_active"])

        with pytest.raises(GiftCardTenderError, match="deactivated"):
            GiftCardTenderService.refund_to_card(
                card_row, amount=_money("25.00"), refund_ref="med4-frozen"
            )

        # Nothing minted, nothing credited.
        from catalog.models import GiftCard

        assert not GiftCard.objects.filter(message__contains="Replacement").exists()
        card_obj.refresh_from_db()
        assert card_obj.current_balance == _money("0.00")
