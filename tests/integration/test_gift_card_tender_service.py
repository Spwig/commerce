"""
GiftCardTenderService — gift card as a payment tender.

A gift card is money the customer already handed over, so it settles like a
payment method rather than reducing the bill like a discount. The lifecycle
mirrors a card payment and is recorded as ``PaymentTransaction`` rows:

    authorize -> capture -> (void | refund)

Two properties carry most of the risk and get the most attention below:

1. **Authorize does not debit.** A hold reserves value without moving it, so an
   abandoned checkout costs the customer nothing. If authorize debited, every
   abandoned basket would quietly eat a balance.
2. **Capture is idempotent.** Payment webhooks retry. A second
   ``capture_for_order`` for the same order must not debit the card twice —
   this is the single assertion most likely to be worth real money.

Plan: docs/.claude_code/plans/wondrous-moseying-wolf.md (R2, P2.1; D5 for the
single-currency rule)
"""

from datetime import timedelta
from decimal import Decimal

import pytest
from django.utils import timezone
from djmoney.money import Money

from catalog.models import GiftCard, GiftCardTransaction
from catalog.services.gift_card_tender_service import (
    GiftCardTenderError,
    GiftCardTenderService,
    InsufficientGiftCardBalance,
)
from payment_providers.models import PaymentTransaction
from tests.factories import CartFactory, OrderFactory, ProductFactory, UserFactory

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
    pytest.mark.r2,
    pytest.mark.gift_card_tender,
]


# ============================================================
# Helpers
# ============================================================


@pytest.fixture
def gift_card_product(db):
    return ProductFactory(product_type="gift_card", status="published")


def _card(gift_card_product, value="100.00", currency="USD", **kwargs):
    """
    A gift card holding a known balance.

    ``GiftCard.save`` copies ``initial_value`` into ``current_balance`` on
    creation, so passing the two separately is only needed for a partially
    spent card.
    """
    defaults = {
        "product": gift_card_product,
        "initial_value": Money(Decimal(value), currency),
        "recipient_email": "recipient@test.spwig.com",
        "is_active": True,
    }
    defaults.update(kwargs)
    return GiftCard.objects.create(**defaults)


def _checkout_session(user=None):
    """
    A checkout session. ``CheckoutSession`` requires ``cart`` and ``expires_at``,
    and ``cart`` is a OneToOne — one session per cart.

    User carts are used deliberately: anonymous carts carry a partial unique
    constraint on ``session_key``, so two anonymous carts in one test collide.
    """
    from cart.models import CheckoutSession

    cart = CartFactory(user=user or UserFactory())
    return CheckoutSession.objects.create(cart=cart, expires_at=timezone.now() + timedelta(hours=1))


def _reread(card):
    return GiftCard.objects.get(pk=card.pk)


def _redemptions(card):
    return GiftCardTransaction.objects.filter(gift_card=card, transaction_type="redemption")


# ============================================================
# authorize — a hold reserves without debiting
# ============================================================


class TestAuthorizeDoesNotDebit:
    def test_a_hold_leaves_the_settled_balance_alone(self, gift_card_product):
        card = _card(gift_card_product, "100.00")
        session = _checkout_session()

        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )

        assert _reread(card).current_balance == Money(Decimal("100.00"), "USD"), (
            "Authorize debited the card. An abandoned checkout would then eat "
            "the customer's balance with no purchase to show for it."
        )

    def test_a_hold_reduces_the_available_balance(self, gift_card_product):
        card = _card(gift_card_product, "100.00")
        session = _checkout_session()

        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )

        card = _reread(card)
        assert card.held_amount == Money(Decimal("40.00"), "USD")
        assert card.available_balance == Money(Decimal("60.00"), "USD")

    def test_no_ledger_row_is_written_for_a_hold(self, gift_card_product):
        """
        ``GiftCardTransaction`` is the record of money *moving*. Writing one at
        authorize time would make the ledger stop reconciling to the balance.
        """
        card = _card(gift_card_product, "100.00")
        session = _checkout_session()

        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )

        assert GiftCardTransaction.objects.filter(gift_card=card).count() == 0

    def test_the_hold_row_records_the_tender(self, gift_card_product):
        card = _card(gift_card_product, "100.00")
        session = _checkout_session()

        hold = GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )

        assert hold.tender_type == PaymentTransaction.TENDER_GIFT_CARD
        assert hold.transaction_type == "authorize"
        assert hold.status == "authorized"
        assert hold.gift_card_id == card.pk
        assert hold.checkout_session_id == session.pk
        assert hold.order_id is None
        assert hold.amount == Money(Decimal("40.00"), "USD")
        assert hold.provider_account_id is None, (
            "A gift card tender settles against an internal balance, so it has "
            "no payment provider behind it."
        )

    def test_omitting_the_amount_holds_the_whole_available_balance(self, gift_card_product):
        card = _card(gift_card_product, "100.00")
        session = _checkout_session()

        hold = GiftCardTenderService.authorize_for_session(session, card.code)

        assert hold.amount == Money(Decimal("100.00"), "USD")
        assert _reread(card).available_balance == Money(Decimal("0.00"), "USD")


class TestAuthorizeLimits:
    def test_holding_more_than_the_balance_is_refused(self, gift_card_product):
        card = _card(gift_card_product, "50.00")
        session = _checkout_session()

        with pytest.raises(InsufficientGiftCardBalance):
            GiftCardTenderService.authorize_for_session(
                session, card.code, amount=Money(Decimal("50.01"), "USD")
            )

        assert _reread(card).held_amount == Money(Decimal("0.00"), "USD")

    def test_a_second_hold_is_limited_by_what_the_first_left_available(self, gift_card_product):
        """
        The regression that makes holds worth having: validating against
        ``current_balance`` instead of ``available_balance`` lets two concurrent
        checkouts each pass, and the card is promised twice.
        """
        card = _card(gift_card_product, "100.00")
        first_session = _checkout_session()
        second_session = _checkout_session()

        GiftCardTenderService.authorize_for_session(
            first_session, card.code, amount=Money(Decimal("70.00"), "USD")
        )

        with pytest.raises(InsufficientGiftCardBalance):
            GiftCardTenderService.authorize_for_session(
                second_session, card.code, amount=Money(Decimal("40.00"), "USD")
            )

        card = _reread(card)
        assert card.held_amount == Money(Decimal("70.00"), "USD"), (
            "The refused hold was recorded anyway."
        )
        assert card.available_balance == Money(Decimal("30.00"), "USD")

    def test_a_second_hold_within_the_remainder_is_allowed(self, gift_card_product):
        """Negative control: the refusal above is about the amount, not the count."""
        card = _card(gift_card_product, "100.00")

        GiftCardTenderService.authorize_for_session(
            _checkout_session(), card.code, amount=Money(Decimal("70.00"), "USD")
        )
        GiftCardTenderService.authorize_for_session(
            _checkout_session(), card.code, amount=Money(Decimal("30.00"), "USD")
        )

        card = _reread(card)
        assert card.held_amount == Money(Decimal("100.00"), "USD")
        assert card.available_balance == Money(Decimal("0.00"), "USD")

    def test_a_card_with_no_available_balance_is_refused(self, gift_card_product):
        card = _card(gift_card_product, "50.00")
        GiftCardTenderService.authorize_for_session(
            _checkout_session(), card.code, amount=Money(Decimal("50.00"), "USD")
        )

        with pytest.raises(InsufficientGiftCardBalance):
            GiftCardTenderService.authorize_for_session(_checkout_session(), card.code)

    def test_an_unknown_code_is_refused(self, gift_card_product):
        with pytest.raises(GiftCardTenderError):
            GiftCardTenderService.authorize_for_session(_checkout_session(), "GC-NOPE-NOPE-NOPE")

    def test_an_inactive_card_is_refused(self, gift_card_product):
        card = _card(gift_card_product, "100.00", is_active=False)

        with pytest.raises(GiftCardTenderError):
            GiftCardTenderService.authorize_for_session(_checkout_session(), card.code)

    def test_an_expired_card_is_refused(self, gift_card_product):
        card = _card(gift_card_product, "100.00")
        GiftCard.objects.filter(pk=card.pk).update(expires_at=timezone.now() - timedelta(days=1))

        with pytest.raises(GiftCardTenderError):
            GiftCardTenderService.authorize_for_session(_checkout_session(), card.code)


class TestSingleCurrencyRule:
    """
    D5 (decided 2026-07-19): a gift card is spendable only against its own
    currency.

    A gift card is an unhedgeable liability with no maturity date, and
    cross-currency redemption creates FX gain/loss on every partial redemption
    plus an arbitrage surface on a stored-value instrument. Every major issuer
    (Apple, Amazon, Steam, Starbucks) region-locks for the same reasons.
    """

    def test_a_hold_in_a_different_currency_is_refused(self, gift_card_product):
        card = _card(gift_card_product, "100.00", currency="USD")
        session = _checkout_session()

        with pytest.raises(GiftCardTenderError) as exc:
            GiftCardTenderService.authorize_for_session(
                session, card.code, amount=Money(Decimal("40.00"), "EUR")
            )

        assert "currency" in str(exc.value).lower()

    def test_the_refused_hold_leaves_nothing_behind(self, gift_card_product):
        card = _card(gift_card_product, "100.00", currency="USD")
        session = _checkout_session()

        with pytest.raises(GiftCardTenderError):
            GiftCardTenderService.authorize_for_session(
                session, card.code, amount=Money(Decimal("40.00"), "EUR")
            )

        card = _reread(card)
        assert card.current_balance == Money(Decimal("100.00"), "USD")
        assert card.held_amount == Money(Decimal("0.00"), "USD")
        assert not PaymentTransaction.objects.filter(gift_card=card).exists()

    def test_the_rule_is_symmetric(self, gift_card_product):
        """A EUR card refuses USD — this is not "USD is special"."""
        card = _card(gift_card_product, "100.00", currency="EUR")

        with pytest.raises(GiftCardTenderError):
            GiftCardTenderService.authorize_for_session(
                _checkout_session(), card.code, amount=Money(Decimal("40.00"), "USD")
            )

        hold = GiftCardTenderService.authorize_for_session(
            _checkout_session(), card.code, amount=Money(Decimal("40.00"), "EUR")
        )
        assert hold.amount == Money(Decimal("40.00"), "EUR")

    def test_held_amount_refuses_to_sum_mixed_currencies(self, gift_card_product):
        """
        The model-level backstop. If a mismatched hold ever reaches the table by
        some other route, summing it would silently over- or under-state what is
        available to spend, so ``held_amount`` raises instead of guessing.
        """
        card = _card(gift_card_product, "100.00", currency="USD")
        PaymentTransaction.objects.create(
            transaction_id="gc-auth:rogue:1",
            tender_type=PaymentTransaction.TENDER_GIFT_CARD,
            transaction_type="authorize",
            status="authorized",
            gift_card=card,
            amount=Money(Decimal("40.00"), "EUR"),
        )

        with pytest.raises(ValueError):
            _ = _reread(card).held_amount


# ============================================================
# Holds stop counting once settled or released
# ============================================================


class TestHoldsStopCounting:
    def test_a_voided_hold_no_longer_counts(self, gift_card_product):
        card = _card(gift_card_product, "100.00")
        session = _checkout_session()
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )
        assert _reread(card).held_amount == Money(Decimal("40.00"), "USD")

        GiftCardTenderService.void_holds(checkout_session=session, reason="Abandoned")

        card = _reread(card)
        assert card.held_amount == Money(Decimal("0.00"), "USD")
        assert card.available_balance == Money(Decimal("100.00"), "USD")

    def test_a_captured_hold_no_longer_counts(self, gift_card_product):
        card = _card(gift_card_product, "100.00")
        session = _checkout_session()
        order = OrderFactory()
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )

        GiftCardTenderService.capture_for_order(order, checkout_session=session)

        card = _reread(card)
        assert card.held_amount == Money(Decimal("0.00"), "USD"), (
            "A settled hold still counts as reserved, so the customer sees "
            "40.00 less available than they actually have."
        )
        assert card.current_balance == Money(Decimal("60.00"), "USD")
        assert card.available_balance == Money(Decimal("60.00"), "USD")


# ============================================================
# capture
# ============================================================


class TestCapture:
    def test_capture_debits_the_card(self, gift_card_product):
        card = _card(gift_card_product, "100.00")
        session = _checkout_session()
        order = OrderFactory()
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )

        GiftCardTenderService.capture_for_order(order, checkout_session=session)

        assert _reread(card).current_balance == Money(Decimal("60.00"), "USD")

    def test_capture_writes_exactly_one_redemption_ledger_row(self, gift_card_product):
        card = _card(gift_card_product, "100.00")
        session = _checkout_session()
        order = OrderFactory()
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )

        GiftCardTenderService.capture_for_order(order, checkout_session=session)

        rows = list(_redemptions(card))
        assert len(rows) == 1, f"Expected one redemption row, found {len(rows)}."
        assert rows[0].amount == Money(Decimal("-40.00"), "USD"), (
            "Redemptions are negative on the ledger; a positive row would make "
            "the running total climb as the card is spent."
        )
        assert rows[0].balance_after == Money(Decimal("60.00"), "USD")
        assert rows[0].order_id == order.pk

    def test_the_capture_row_points_at_the_hold_it_settles(self, gift_card_product):
        card = _card(gift_card_product, "100.00")
        session = _checkout_session()
        order = OrderFactory()
        hold = GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )

        captures = GiftCardTenderService.capture_for_order(order, checkout_session=session)

        assert len(captures) == 1
        capture = captures[0]
        assert capture.transaction_type == "capture"
        assert capture.status == "completed"
        assert capture.parent_transaction_id == hold.pk, (
            "Without the parent link, a capture cannot be traced back to the "
            "hold it settles, and refund accounting has nothing to anchor to."
        )
        assert capture.order_id == order.pk
        assert capture.gift_card_id == card.pk
        assert capture.amount == Money(Decimal("40.00"), "USD")

    def test_the_hold_row_survives_and_is_voided(self, gift_card_product):
        """
        The ledger is append-only: the authorize row is never rewritten into the
        capture. Mutating it in place would erase the evidence that a hold was
        ever placed, which is exactly what you need when reconstructing a
        disputed checkout.
        """
        card = _card(gift_card_product, "100.00")
        session = _checkout_session()
        order = OrderFactory()
        hold = GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )

        GiftCardTenderService.capture_for_order(order, checkout_session=session)

        hold.refresh_from_db()
        assert hold.transaction_type == "authorize", (
            "The hold was mutated into the capture instead of a new row being written."
        )
        assert hold.status == "voided"
        assert hold.order_id == order.pk

        rows = PaymentTransaction.objects.filter(gift_card=card).order_by("created_at")
        assert [r.transaction_type for r in rows] == ["authorize", "capture"]

    def test_capture_with_no_holds_is_a_no_op(self, gift_card_product):
        order = OrderFactory()
        assert GiftCardTenderService.capture_for_order(order) == []

    def test_capture_settles_every_hold_on_the_session(self, gift_card_product):
        """Split tender across two cards settles as one unit."""
        first = _card(gift_card_product, "30.00")
        second = _card(gift_card_product, "50.00")
        session = _checkout_session()
        order = OrderFactory()

        GiftCardTenderService.authorize_for_session(
            session, first.code, amount=Money(Decimal("30.00"), "USD")
        )
        GiftCardTenderService.authorize_for_session(
            session, second.code, amount=Money(Decimal("20.00"), "USD")
        )

        captures = GiftCardTenderService.capture_for_order(order, checkout_session=session)

        assert len(captures) == 2
        assert _reread(first).current_balance == Money(Decimal("0.00"), "USD")
        assert _reread(second).current_balance == Money(Decimal("30.00"), "USD")


class TestCaptureIsCappedAtWhatTheOrderCosts:
    """
    A hold is sized when the customer keys the card. The cart can shrink after
    that — back button, remove an item, return to checkout — and the hold is
    still the old, larger figure.

    Found by review during P2.2f: `capture_for_order` debited `hold.amount`
    unconditionally, so a 100 hold against an order that ended up at 50 took
    the full 100 and the customer was 50 short with nothing to show for it.
    Removing `Cart.recalculate_gift_card_discounts` is what exposed this — it
    used to re-cap the old cart-discount on every mutation.
    """

    def test_capture_never_exceeds_the_order_total(self, gift_card_product):
        card = _card(gift_card_product, "200.00")
        session = _checkout_session()
        # Hold 150 while the basket is large.
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("150.00"), "USD")
        )
        # Basket shrinks: the order is only worth 50 by the time it is placed.
        order = OrderFactory(total_amount=Decimal("50.00"), total_amount_currency="USD")

        GiftCardTenderService.capture_for_order(order, checkout_session=session)

        assert _reread(card).current_balance == Money(Decimal("150.00"), "USD"), (
            "Captured more than the order cost — the customer lost the difference."
        )

    def test_the_capture_row_records_the_capped_amount(self, gift_card_product):
        card = _card(gift_card_product, "200.00")
        session = _checkout_session()
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("150.00"), "USD")
        )
        order = OrderFactory(total_amount=Decimal("50.00"), total_amount_currency="USD")

        captures = GiftCardTenderService.capture_for_order(order, checkout_session=session)

        assert len(captures) == 1
        # Both columns, or Order.amount_paid reconciliation (I2) drifts.
        assert captures[0].amount == Money(Decimal("50.00"), "USD")
        assert captures[0].settlement_amount == Money(Decimal("50.00"), "USD")

    def test_a_hold_with_nothing_left_to_cover_is_voided_not_captured(self, gift_card_product):
        """Two cards, but the first alone already covers the shrunken order."""
        first = _card(gift_card_product, "200.00")
        second = _card(gift_card_product, "200.00", code="GC-SECOND-CARD")
        session = _checkout_session()
        GiftCardTenderService.authorize_for_session(
            session, first.code, amount=Money(Decimal("60.00"), "USD")
        )
        GiftCardTenderService.authorize_for_session(
            session, second.code, amount=Money(Decimal("60.00"), "USD")
        )
        order = OrderFactory(total_amount=Decimal("50.00"), total_amount_currency="USD")

        GiftCardTenderService.capture_for_order(order, checkout_session=session)

        # 50 comes off one card; the other is left whole.
        balances = sorted(
            [_reread(first).current_balance.amount, _reread(second).current_balance.amount]
        )
        assert balances == [Decimal("150.00"), Decimal("200.00")]

        # And no hold is left dangling for the sweeper to trip over.
        assert not PaymentTransaction.objects.filter(
            checkout_session=session,
            transaction_type="authorize",
            status="authorized",
        ).exists()


class TestCaptureIsIdempotent:
    """
    Payment webhooks retry. Every assertion here models the same event
    arriving twice.
    """

    def test_capturing_twice_does_not_debit_twice(self, gift_card_product):
        card = _card(gift_card_product, "100.00")
        session = _checkout_session()
        order = OrderFactory()
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )

        GiftCardTenderService.capture_for_order(order, checkout_session=session)
        balance_after_first = _reread(card).current_balance

        GiftCardTenderService.capture_for_order(order, checkout_session=session)

        assert balance_after_first == Money(Decimal("60.00"), "USD")
        assert _reread(card).current_balance == Money(Decimal("60.00"), "USD"), (
            "A retried payment webhook debited the card a second time. The "
            "customer paid 40.00 and lost 80.00 of stored value."
        )

    def test_capturing_twice_writes_one_redemption_row(self, gift_card_product):
        card = _card(gift_card_product, "100.00")
        session = _checkout_session()
        order = OrderFactory()
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )

        GiftCardTenderService.capture_for_order(order, checkout_session=session)
        GiftCardTenderService.capture_for_order(order, checkout_session=session)

        assert _redemptions(card).count() == 1

    def test_capturing_twice_creates_one_capture_transaction(self, gift_card_product):
        card = _card(gift_card_product, "100.00")
        session = _checkout_session()
        order = OrderFactory()
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )

        GiftCardTenderService.capture_for_order(order, checkout_session=session)
        GiftCardTenderService.capture_for_order(order, checkout_session=session)

        assert (
            PaymentTransaction.objects.filter(gift_card=card, transaction_type="capture").count()
            == 1
        )

    def test_capture_by_order_alone_is_also_idempotent(self, gift_card_product):
        """
        The retry usually arrives without the session — a webhook knows the
        order, not the in-progress checkout. Capture must be idempotent through
        that path too, and the hold carries the order after the first capture.
        """
        card = _card(gift_card_product, "100.00")
        session = _checkout_session()
        order = OrderFactory()
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )

        GiftCardTenderService.capture_for_order(order, checkout_session=session)
        GiftCardTenderService.capture_for_order(order)

        assert _reread(card).current_balance == Money(Decimal("60.00"), "USD")
        assert _redemptions(card).count() == 1


# ============================================================
# void
# ============================================================


class TestVoidHolds:
    def test_voiding_releases_without_debiting(self, gift_card_product):
        card = _card(gift_card_product, "100.00")
        session = _checkout_session()
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )

        released = GiftCardTenderService.void_holds(
            checkout_session=session, reason="Customer abandoned"
        )

        assert released == 1
        card = _reread(card)
        assert card.current_balance == Money(Decimal("100.00"), "USD")
        assert card.available_balance == Money(Decimal("100.00"), "USD")
        assert GiftCardTransaction.objects.filter(gift_card=card).count() == 0, (
            "Voiding wrote a ledger row for money that never moved."
        )

    def test_voiding_releases_every_hold_on_the_session(self, gift_card_product):
        first = _card(gift_card_product, "30.00")
        second = _card(gift_card_product, "50.00")
        session = _checkout_session()
        GiftCardTenderService.authorize_for_session(
            session, first.code, amount=Money(Decimal("30.00"), "USD")
        )
        GiftCardTenderService.authorize_for_session(
            session, second.code, amount=Money(Decimal("20.00"), "USD")
        )

        assert GiftCardTenderService.void_holds(checkout_session=session) == 2

    def test_voiding_does_not_touch_another_sessions_holds(self, gift_card_product):
        card = _card(gift_card_product, "100.00")
        mine = _checkout_session()
        theirs = _checkout_session()
        GiftCardTenderService.authorize_for_session(
            mine, card.code, amount=Money(Decimal("30.00"), "USD")
        )
        GiftCardTenderService.authorize_for_session(
            theirs, card.code, amount=Money(Decimal("20.00"), "USD")
        )

        GiftCardTenderService.void_holds(checkout_session=mine)

        assert _reread(card).held_amount == Money(Decimal("20.00"), "USD")

    def test_voiding_a_captured_hold_does_nothing(self, gift_card_product):
        card = _card(gift_card_product, "100.00")
        session = _checkout_session()
        order = OrderFactory()
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )
        GiftCardTenderService.capture_for_order(order, checkout_session=session)

        assert GiftCardTenderService.void_holds(checkout_session=session) == 0
        assert _reread(card).current_balance == Money(Decimal("60.00"), "USD")

    def test_void_holds_requires_a_target(self):
        with pytest.raises(ValueError):
            GiftCardTenderService.void_holds()


# ============================================================
# expire_stale_holds
# ============================================================


def _age_hold(hold, minutes):
    """
    Backdate a hold. ``created_at`` is ``auto_now_add``, so it can only be moved
    with a queryset update.
    """
    PaymentTransaction.objects.filter(pk=hold.pk).update(
        created_at=timezone.now() - timedelta(minutes=minutes)
    )


class TestExpireStaleHolds:
    def test_a_stale_hold_is_voided(self, gift_card_product):
        """
        Without the sweep, a customer who keys a code and walks away has their
        balance reserved indefinitely — the card looks empty to them while no
        money has actually moved.
        """
        card = _card(gift_card_product, "100.00")
        hold = GiftCardTenderService.authorize_for_session(
            _checkout_session(), card.code, amount=Money(Decimal("40.00"), "USD")
        )
        _age_hold(hold, GiftCardTenderService.HOLD_MINUTES + 5)

        assert GiftCardTenderService.expire_stale_holds() == 1

        hold.refresh_from_db()
        assert hold.status == "voided"
        card = _reread(card)
        assert card.available_balance == Money(Decimal("100.00"), "USD")
        assert card.current_balance == Money(Decimal("100.00"), "USD")

    def test_a_fresh_hold_is_left_alone(self, gift_card_product):
        card = _card(gift_card_product, "100.00")
        hold = GiftCardTenderService.authorize_for_session(
            _checkout_session(), card.code, amount=Money(Decimal("40.00"), "USD")
        )

        assert GiftCardTenderService.expire_stale_holds() == 0

        hold.refresh_from_db()
        assert hold.status == "authorized"
        assert _reread(card).held_amount == Money(Decimal("40.00"), "USD")

    def test_a_hold_just_inside_the_window_is_left_alone(self, gift_card_product):
        """Boundary: the sweep must not reap a checkout still in a provider redirect."""
        card = _card(gift_card_product, "100.00")
        hold = GiftCardTenderService.authorize_for_session(
            _checkout_session(), card.code, amount=Money(Decimal("40.00"), "USD")
        )
        _age_hold(hold, GiftCardTenderService.HOLD_MINUTES - 2)

        assert GiftCardTenderService.expire_stale_holds() == 0
        hold.refresh_from_db()
        assert hold.status == "authorized"

    def test_a_stale_hold_attached_to_an_order_is_left_alone(self, gift_card_product):
        """
        An order-attached hold belongs to a checkout that got far enough to
        create an order. Sweeping it would release value that is about to be —
        or has been — settled.
        """
        card = _card(gift_card_product, "100.00")
        order = OrderFactory()
        hold = GiftCardTenderService.authorize_for_session(
            _checkout_session(), card.code, amount=Money(Decimal("40.00"), "USD")
        )
        PaymentTransaction.objects.filter(pk=hold.pk).update(
            created_at=timezone.now() - timedelta(minutes=GiftCardTenderService.HOLD_MINUTES + 5),
            order=order,
        )

        assert GiftCardTenderService.expire_stale_holds() == 0

        hold.refresh_from_db()
        assert hold.status == "authorized"

    def test_the_sweep_is_selective(self, gift_card_product):
        """One stale, one fresh, one stale-but-ordered — only the first goes."""
        card = _card(gift_card_product, "300.00")
        order = OrderFactory()

        stale = GiftCardTenderService.authorize_for_session(
            _checkout_session(), card.code, amount=Money(Decimal("40.00"), "USD")
        )
        fresh = GiftCardTenderService.authorize_for_session(
            _checkout_session(), card.code, amount=Money(Decimal("50.00"), "USD")
        )
        ordered = GiftCardTenderService.authorize_for_session(
            _checkout_session(), card.code, amount=Money(Decimal("60.00"), "USD")
        )
        _age_hold(stale, GiftCardTenderService.HOLD_MINUTES + 5)
        PaymentTransaction.objects.filter(pk=ordered.pk).update(
            created_at=timezone.now() - timedelta(minutes=GiftCardTenderService.HOLD_MINUTES + 5),
            order=order,
        )

        assert GiftCardTenderService.expire_stale_holds() == 1

        stale.refresh_from_db()
        fresh.refresh_from_db()
        ordered.refresh_from_db()
        assert stale.status == "voided"
        assert fresh.status == "authorized"
        assert ordered.status == "authorized"
        assert _reread(card).held_amount == Money(Decimal("110.00"), "USD")


# ============================================================
# refund
# ============================================================


class TestRefundToCard:
    @pytest.fixture
    def captured(self, gift_card_product):
        """A card with 100.00, of which 40.00 has been captured against an order."""
        card = _card(gift_card_product, "100.00")
        session = _checkout_session()
        order = OrderFactory()
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )
        capture = GiftCardTenderService.capture_for_order(order, checkout_session=session)[0]
        return card, capture

    def test_a_full_refund_credits_the_card(self, captured):
        card, capture = captured
        assert _reread(card).current_balance == Money(Decimal("60.00"), "USD")

        GiftCardTenderService.refund_to_card(capture, reason="Returned")

        assert _reread(card).current_balance == Money(Decimal("100.00"), "USD")

    def test_a_refund_writes_an_adjustment_ledger_row(self, captured):
        card, capture = captured

        GiftCardTenderService.refund_to_card(capture, reason="Returned")

        rows = GiftCardTransaction.objects.filter(gift_card=card, transaction_type="adjustment")
        assert rows.count() == 1
        assert rows.first().amount == Money(Decimal("40.00"), "USD")
        assert rows.first().balance_after == Money(Decimal("100.00"), "USD")

    def test_the_refund_row_points_at_the_capture(self, captured):
        _, capture = captured

        refund = GiftCardTenderService.refund_to_card(capture)

        assert refund.transaction_type == "refund"
        assert refund.status == "completed"
        assert refund.parent_transaction_id == capture.pk
        assert refund.tender_type == PaymentTransaction.TENDER_GIFT_CARD

    def test_a_partial_refund_credits_only_that_much(self, captured):
        card, capture = captured

        GiftCardTenderService.refund_to_card(capture, amount=Money(Decimal("15.00"), "USD"))

        assert _reread(card).current_balance == Money(Decimal("75.00"), "USD")

    def test_refunding_more_than_was_captured_is_refused(self, captured):
        card, capture = captured

        with pytest.raises(GiftCardTenderError):
            GiftCardTenderService.refund_to_card(capture, amount=Money(Decimal("40.01"), "USD"))

        assert _reread(card).current_balance == Money(Decimal("60.00"), "USD"), (
            "The over-refund was refused but the card was credited anyway."
        )

    def test_cumulative_refunds_cannot_exceed_the_capture(self, captured):
        """
        The interesting case: each refund is individually valid, and only the
        running total is not. Checking a single refund against the capture in
        isolation lets a card be refilled indefinitely by repeating a
        refund — minting stored value out of nothing.
        """
        card, capture = captured

        GiftCardTenderService.refund_to_card(capture, amount=Money(Decimal("25.00"), "USD"))
        GiftCardTenderService.refund_to_card(capture, amount=Money(Decimal("10.00"), "USD"))

        with pytest.raises(GiftCardTenderError):
            GiftCardTenderService.refund_to_card(capture, amount=Money(Decimal("10.00"), "USD"))

        assert _reread(card).current_balance == Money(Decimal("95.00"), "USD"), (
            "35.00 of a 40.00 capture was refunded; the card should hold 60.00 + 35.00."
        )

    def test_refunds_up_to_exactly_the_captured_amount_are_allowed(self, captured):
        """Boundary: the guard is > not >=, so the last penny is refundable."""
        card, capture = captured

        GiftCardTenderService.refund_to_card(capture, amount=Money(Decimal("25.00"), "USD"))
        GiftCardTenderService.refund_to_card(capture, amount=Money(Decimal("15.00"), "USD"))

        assert _reread(card).current_balance == Money(Decimal("100.00"), "USD")

    def test_a_refund_in_a_different_currency_is_refused(self, captured):
        card, capture = captured

        with pytest.raises(GiftCardTenderError):
            GiftCardTenderService.refund_to_card(capture, amount=Money(Decimal("10.00"), "EUR"))

        assert _reread(card).current_balance == Money(Decimal("60.00"), "USD")

    def test_a_hold_cannot_be_refunded(self, gift_card_product):
        """Nothing was debited at authorize time, so there is nothing to return."""
        card = _card(gift_card_product, "100.00")
        hold = GiftCardTenderService.authorize_for_session(
            _checkout_session(), card.code, amount=Money(Decimal("40.00"), "USD")
        )

        with pytest.raises(GiftCardTenderError):
            GiftCardTenderService.refund_to_card(hold)

        assert _reread(card).current_balance == Money(Decimal("100.00"), "USD")


# ============================================================
# Known defect — re-submitting a code a third time
# ============================================================


class TestRepeatedAuthorizeOnTheSameSession:
    """
    Re-keying a gift card code on the same checkout replaces the hold rather
    than stacking a second one. That works for the second attempt and breaks on
    the third.

    ``_auth_txn_id`` is the idempotency key. On the second attempt the service
    finds the row under the base id, voids it, and disambiguates the new row by
    appending the *found row's* pk. On the third attempt it looks up the base id
    again and finds that same first row — now already voided, so the live second
    hold is never released — and then derives the identical suffixed id, which
    collides with the second hold's unique ``transaction_id``.
    """

    def test_a_second_submission_replaces_the_first_hold(self, gift_card_product):
        """The part that works, pinned so a fix does not regress it."""
        card = _card(gift_card_product, "100.00")
        session = _checkout_session()

        first = GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("10.00"), "USD")
        )
        second = GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("20.00"), "USD")
        )

        first.refresh_from_db()
        assert first.status == "voided"
        assert second.status == "authorized"
        assert _reread(card).held_amount == Money(Decimal("20.00"), "USD"), (
            "Both holds counted — the card is reserved twice for one checkout."
        )

    # FIXED in P2.1: authorize_for_session now voids EVERY outstanding hold
    # for the (session, card) pair and derives a genuinely unique
    # transaction_id, instead of re-finding the first hold and rebuilding
    # the second's id. Re-entry is a normal thing customers do.
    def test_a_third_submission_neither_crashes_nor_double_holds(self, gift_card_product):
        card = _card(gift_card_product, "100.00")
        session = _checkout_session()

        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("10.00"), "USD")
        )
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("20.00"), "USD")
        )
        third = GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("30.00"), "USD")
        )

        assert third.status == "authorized"
        assert _reread(card).held_amount == Money(Decimal("30.00"), "USD"), (
            "Only the most recent hold should count; the superseded ones must be voided."
        )


# ============================================================
# End-to-end lifecycle
# ============================================================


class TestLifecycleReconciles:
    def test_the_ledger_reconciles_to_the_balance_after_a_full_lifecycle(self, gift_card_product):
        """
        authorize -> capture -> partial refund. The card's balance must equal
        its initial value plus every ledger movement; if it does not, stored
        value has been created or destroyed somewhere in the chain.
        """
        card = _card(gift_card_product, "100.00")
        session = _checkout_session()
        order = OrderFactory()

        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("40.00"), "USD")
        )
        capture = GiftCardTenderService.capture_for_order(order, checkout_session=session)[0]
        GiftCardTenderService.refund_to_card(capture, amount=Money(Decimal("15.00"), "USD"))

        card = _reread(card)
        movements = sum(
            (t.amount.amount for t in GiftCardTransaction.objects.filter(gift_card=card)),
            Decimal("0"),
        )
        assert card.initial_value.amount + movements == card.current_balance.amount
        assert card.current_balance == Money(Decimal("75.00"), "USD")
        assert card.held_amount == Money(Decimal("0.00"), "USD")
