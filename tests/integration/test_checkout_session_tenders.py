"""
CheckoutSession.tendered_amount and .amount_due — and what the gateway is asked for.

These two properties are the whole tender rail's arithmetic. Everything else
(holds, capture, settlement, zero-due checkout) reads one of them, and until
this module existed neither had a single test anywhere in ``tests/``.

The gap was not academic. It hid a double-charge: ``create_payment_intent``
asked the gateway for ``checkout_session.total_amount`` — the gross figure —
while gift card holds sat on the session. The customer was billed the full
total by card AND had their gift card debited on settlement.

The distinction the tests below pin down:

* ``total_amount``  — what the order costs. A tender must NEVER reduce it, or
  the gift card starts behaving like a discount again (reducing the tax base,
  showing up as a "saving") which is exactly what P2.2 removed.
* ``amount_due``    — what is left to charge a payment provider. This is the
  figure a gateway gets, and it can legitimately be zero.

Plan: docs/.claude_code/plans/wondrous-moseying-wolf.md (R2, P2.2)
"""

from datetime import timedelta
from decimal import Decimal

import pytest
from django.utils import timezone
from djmoney.money import Money

from catalog.models import GiftCard
from catalog.services.gift_card_tender_service import GiftCardTenderService
from payment_providers.models import PaymentTransaction
from tests.factories import CartFactory, OrderFactory, ProductFactory, UserFactory

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
    pytest.mark.r2,
    pytest.mark.gift_card_tender,
]


@pytest.fixture
def gift_card_product(db):
    return ProductFactory(product_type="gift_card", status="published")


def _card(gift_card_product, value="100.00", currency="USD", **kwargs):
    defaults = {
        "product": gift_card_product,
        "initial_value": Money(Decimal(value), currency),
        "recipient_email": "recipient@test.spwig.com",
        "is_active": True,
    }
    defaults.update(kwargs)
    return GiftCard.objects.create(**defaults)


def _session(total="100.00", currency="USD"):
    """A checkout session with a known total, independent of cart contents."""
    from cart.models import CheckoutSession

    session = CheckoutSession.objects.create(
        cart=CartFactory(user=UserFactory()),
        expires_at=timezone.now() + timedelta(hours=1),
    )
    # Set directly: these tests are about the tender arithmetic on top of a
    # total, not about how the total itself is derived from the cart.
    session.total_amount = Money(Decimal(total), currency)
    session.save(update_fields=["total_amount"])
    return session


def _reread_card(card):
    return GiftCard.objects.get(pk=card.pk)


class TestTenderedAmount:
    def test_no_tenders_is_zero(self):
        session = _session("100.00")
        assert session.tendered_amount == Money(Decimal("0.00"), "USD")

    def test_a_live_hold_counts(self, gift_card_product):
        session = _session("100.00")
        card = _card(gift_card_product, "40.00")
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )
        assert session.tendered_amount == Money(Decimal("40.00"), "USD")

    def test_two_holds_sum(self, gift_card_product):
        session = _session("100.00")
        first = _card(gift_card_product, "40.00")
        second = _card(gift_card_product, "25.00", code="GC-SECOND-SUM")
        GiftCardTenderService.authorize_for_session(
            session, first.code, amount=Money(Decimal("40.00"), "USD")
        )
        GiftCardTenderService.authorize_for_session(
            session, second.code, amount=Money(Decimal("25.00"), "USD")
        )
        assert session.tendered_amount == Money(Decimal("65.00"), "USD")

    def test_a_voided_hold_stops_counting(self, gift_card_product):
        """Otherwise a removed tender keeps suppressing what the gateway is asked for."""
        session = _session("100.00")
        card = _card(gift_card_product, "40.00")
        hold = GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )
        hold.status = "voided"
        hold.save(update_fields=["status"])

        assert session.tendered_amount == Money(Decimal("0.00"), "USD")


class TestAmountDue:
    def test_no_tenders_means_the_whole_total_is_due(self):
        session = _session("100.00")
        assert session.amount_due == Money(Decimal("100.00"), "USD")

    def test_a_partial_tender_leaves_the_remainder_due(self, gift_card_product):
        session = _session("100.00")
        card = _card(gift_card_product, "40.00")
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )
        assert session.amount_due == Money(Decimal("60.00"), "USD")

    def test_full_cover_leaves_nothing_due(self, gift_card_product):
        session = _session("100.00")
        card = _card(gift_card_product, "100.00")
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("100.00"), "USD")
        )
        assert session.amount_due == Money(Decimal("0.00"), "USD")

    def test_over_tender_floors_at_zero_never_negative(self, gift_card_product):
        """A negative charge request would be rejected or, worse, refund money."""
        session = _session("50.00")
        card = _card(gift_card_product, "200.00")
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("120.00"), "USD")
        )
        assert session.amount_due == Money(Decimal("0.00"), "USD")

    def test_a_tender_never_reduces_total_amount(self, gift_card_product):
        """
        The invariant that separates a tender from a discount.

        If a hold moved `total_amount`, the gift card would once again reduce
        the tax base and show up as a customer "saving" — the exact defect
        P2.2 removed by deleting cart.AppliedGiftCard.
        """
        session = _session("100.00")
        card = _card(gift_card_product, "40.00")
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )
        assert session.total_amount == Money(Decimal("100.00"), "USD")


class TestGatewayIsChargedTheNetAmount:
    """
    Regression: the gateway must be asked for `amount_due`, not `total_amount`.

    Found by adversarial review of P2.2f. `create_payment_intent` charged the
    gross total while gift card holds sat on the session, so a 100 order with a
    40 gift card billed the customer 100 on their card and then debited 40 from
    the gift card on settlement — 140 collected for a 100 order, and the
    customer silently lost 40 of stored value.

    The `amount_due` docstring had said "This — not total_amount — is the figure
    a gateway should be asked for" since P2.2. The orchestrator simply never
    read it.
    """

    def test_intent_amount_is_net_of_gift_card_holds(self, gift_card_product, monkeypatch):
        session = _session("100.00")
        card = _card(gift_card_product, "40.00")
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )

        # The orchestrator reads this property to decide what to charge. Assert
        # on it directly rather than standing up a whole provider account, so
        # the test pins the arithmetic and not the provider plumbing.
        assert session.amount_due == Money(Decimal("60.00"), "USD"), (
            "The gateway would be asked for the wrong figure."
        )

    def test_orchestrator_reads_amount_due_not_total_amount(self):
        """
        Pin the call site itself.

        A property assertion alone would not have caught the original bug —
        `amount_due` was already correct; the orchestrator ignored it. This
        reads the source so a future edit that reverts to `total_amount` fails
        here rather than in production.
        """
        import inspect

        from payment_providers.services.payment_orchestration_service import (
            PaymentOrchestrationService,
        )

        src = inspect.getsource(PaymentOrchestrationService.create_payment_intent)

        assert "checkout_session.amount_due" in src, (
            "create_payment_intent no longer reads checkout_session.amount_due. "
            "Charging checkout_session.total_amount double-bills any customer "
            "who has tendered a gift card or wallet balance."
        )
        assert "amount = checkout_session.total_amount.amount" not in src, (
            "create_payment_intent is back to charging the gross total. A 100 "
            "order with a 40 gift card would bill the card 100 and debit the "
            "gift card 40."
        )


class TestSettlementRowsMatchWhatWasCharged:
    def test_hold_settlement_amount_is_in_the_order_currency(self, gift_card_product):
        """
        `tendered_amount` raises rather than guess if a row settles in the wrong
        currency, so the writer has to get this right.
        """
        session = _session("100.00")
        card = _card(gift_card_product, "40.00")
        hold = GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )
        assert hold.settlement_amount == Money(Decimal("40.00"), "USD")
        assert hold.tender_type == PaymentTransaction.TENDER_GIFT_CARD
        assert hold.transaction_type == "authorize"
        assert hold.status == "authorized"


class TestAmountPaidReconciles:
    """
    Invariant I2: ``amount_paid == sum of settlement`` over completed rows.

    Charging the gateway ``amount_due`` instead of ``total_amount`` fixed a
    double-charge, but it made the gateway leg smaller — so unless the gift
    card leg is credited too, every split-tender order reads as permanently
    part-paid. That is not cosmetic: RefundService caps refunds at
    ``amount_paid``, so an understated figure silently blocks refunding money
    the customer really handed over.
    """

    def test_capture_credits_amount_paid(
        self, gift_card_product, django_capture_on_commit_callbacks
    ):
        from orders.models import Order

        session = _session("100.00")
        card = _card(gift_card_product, "40.00")
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )

        # Gateway leg: amount_due (60) was charged and assigned by
        # handle_payment_success. Flipping to paid fires the settlement
        # receiver, which must add the 40 of gift card tender.
        order = OrderFactory(
            total_amount=Decimal("100.00"),
            total_amount_currency="USD",
            amount_paid=Decimal("60.00"),
            amount_paid_currency="USD",
            payment_status="unpaid",
        )
        PaymentTransaction.objects.filter(checkout_session=session).update(order=order)

        # The receiver defers capture with transaction.on_commit, which does
        # not fire under a non-transactional test without this.
        with django_capture_on_commit_callbacks(execute=True):
            order.payment_status = "paid"
            order.save()
        order.refresh_from_db()

        assert order.amount_paid == Money(Decimal("100.00"), "USD"), (
            "Gateway paid 60 and the gift card settled 40, so the order is "
            "fully paid. A lower figure blocks refunds of the gift card leg."
        )
        assert Order.objects.get(pk=order.pk).amount_paid.amount == Decimal("100.00")

    def test_crediting_is_idempotent_across_repeated_paid_saves(
        self, gift_card_product, django_capture_on_commit_callbacks
    ):
        """
        A retried webhook, or an admin re-save, must not inflate amount_paid.

        Note on what this actually covers: re-saving is safe mainly because
        capture_for_order finds no *authorized* holds the second time (the
        first pass voided them) and returns early. The pre-existing-capture
        filter in the receiver is a second line of defence, exercised by
        test_a_reappearing_hold_does_not_recredit_a_settled_capture below.
        """
        session = _session("100.00")
        card = _card(gift_card_product, "40.00")
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )
        order = OrderFactory(
            total_amount=Decimal("100.00"),
            total_amount_currency="USD",
            amount_paid=Decimal("60.00"),
            amount_paid_currency="USD",
            payment_status="unpaid",
        )
        PaymentTransaction.objects.filter(checkout_session=session).update(order=order)

        with django_capture_on_commit_callbacks(execute=True):
            order.payment_status = "paid"
            order.save()
        for _ in range(3):
            with django_capture_on_commit_callbacks(execute=True):
                order.refresh_from_db()
                order.save()

        order.refresh_from_db()
        assert order.amount_paid == Money(Decimal("100.00"), "USD"), (
            "amount_paid grew on re-save — the gift card leg was credited more than once."
        )
        assert _reread_card(card).current_balance == Money(Decimal("0.00"), "USD")

    def test_a_reappearing_hold_does_not_recredit_a_settled_capture(
        self, gift_card_product, django_capture_on_commit_callbacks
    ):
        """
        capture_for_order returns pre-existing capture rows alongside new ones.

        Crediting its whole return value would re-add already-settled value, so
        the receiver credits only rows that were not already present. This
        drives that filter directly: capture once, then put another authorized
        hold on the same (order, card) so the next pass returns the existing
        capture row.
        """
        session = _session("100.00")
        card = _card(gift_card_product, "40.00")
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )
        order = OrderFactory(
            total_amount=Decimal("100.00"),
            total_amount_currency="USD",
            amount_paid=Decimal("60.00"),
            amount_paid_currency="USD",
            payment_status="unpaid",
        )
        PaymentTransaction.objects.filter(checkout_session=session).update(order=order)

        with django_capture_on_commit_callbacks(execute=True):
            order.payment_status = "paid"
            order.save()
        order.refresh_from_db()
        assert order.amount_paid == Money(Decimal("100.00"), "USD")

        # A stray authorized hold for the same (order, card) — capture_for_order
        # will now find work to do, hit its existing-capture short-circuit, and
        # hand back the already-settled row.
        PaymentTransaction.objects.create(
            transaction_id="gc-auth:stray-rehold",
            tender_type=PaymentTransaction.TENDER_GIFT_CARD,
            transaction_type="authorize",
            status="authorized",
            gift_card=card,
            order=order,
            amount=Money(Decimal("40.00"), "USD"),
            settlement_amount=Money(Decimal("40.00"), "USD"),
            provider_account=None,
        )

        with django_capture_on_commit_callbacks(execute=True):
            order.refresh_from_db()
            order.save()

        order.refresh_from_db()
        assert order.amount_paid == Money(Decimal("100.00"), "USD"), (
            "The already-settled capture was credited a second time."
        )


class TestZeroDueValidation:
    """
    P2.5b: a fully-tendered checkout must not demand a payment method.

    validate_checkout used to append "Payment method is required"
    unconditionally, which forced the UI to mount a gateway widget for 0.00 —
    and create_payment_intent has no zero guard, so that widget would have
    tried to charge it.
    """

    def test_fully_tendered_session_validates_without_a_provider(self, gift_card_product):
        from cart.services.checkout_service import CheckoutService

        session = _session("100.00")
        card = _card(gift_card_product, "100.00")
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("100.00"), "USD")
        )

        is_valid, errors = CheckoutService.validate_checkout(session)

        assert "Payment method is required" not in [str(e) for e in errors], (
            "A zero-due checkout demanded a gateway."
        )

    def test_a_partially_tendered_session_still_requires_one(self, gift_card_product):
        from cart.services.checkout_service import CheckoutService

        session = _session("100.00")
        card = _card(gift_card_product, "40.00")
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )

        is_valid, errors = CheckoutService.validate_checkout(session)

        assert "Payment method is required" in [str(e) for e in errors], (
            "60.00 is still due; skipping the provider requirement here would "
            "let an unpaid order through."
        )
