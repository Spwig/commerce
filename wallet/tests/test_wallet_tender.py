"""
The wallet as a payment tender (P2.5a).

The wallet is the SECOND internal tender on the rail gift cards proved out,
and the dangerous cases are exactly the two-rail ones:

* **Joint over-capture.** Each rail capping its debit at "order total minus my
  own captures" was correct by accident while gift cards were alone — holds
  plus the gateway charge summed to the total exactly. Two rails against a
  cart that shrank between hold and payment would each settle "the rest of the
  order". The fix (both rails subtract EVERY completed capture and charge) is
  mutation-verified by the shrunk-cart test here.
* **Holds move no money.** The whole hold lifecycle — authorize, supersede,
  void, sweep — must leave the stored balance and the ledger untouched, or a
  crashed sweeper can strand customer funds (invariant I5 and the reason the
  reconciler shipped first).

Plan: docs/.claude_code/plans/wondrous-moseying-wolf.md (R2, P2.5a)
"""

from datetime import timedelta
from decimal import Decimal

import pytest
from django.utils import timezone
from djmoney.money import Money

from payment_providers.models import PaymentTransaction
from tests.factories import CartFactory, OrderFactory, UserFactory
from wallet.models import CustomerWallet, WalletTransaction
from wallet.services import WalletService
from wallet.tender_service import (
    WalletTenderError,
    WalletTenderService,
)

pytestmark = [pytest.mark.django_db, pytest.mark.wallet, pytest.mark.r2]


def _funded_wallet(amount="100.00", user=None):
    user = user or UserFactory()
    WalletService.credit(user, Decimal(amount), "USD", "manual", "test funding")
    return CustomerWallet.objects.get(customer=user), user


def _session(user, total="80.00"):
    from cart.models import CheckoutSession

    session = CheckoutSession.objects.create(
        cart=CartFactory(user=user),
        expires_at=timezone.now() + timedelta(hours=1),
    )
    session.total_amount = Money(Decimal(total), "USD")
    session.save(update_fields=["total_amount"])
    return session


class TestAuthorize:
    def test_hold_defaults_to_min_of_spendable_and_due(self):
        wallet, user = _funded_wallet("100.00")
        session = _session(user, total="80.00")

        hold = WalletTenderService.authorize_for_session(session, user)

        assert hold.amount == Money(Decimal("80.00"), "USD")
        assert hold.tender_type == PaymentTransaction.TENDER_WALLET
        assert hold.status == "authorized"

    def test_small_balance_holds_what_it_has(self):
        wallet, user = _funded_wallet("30.00")
        session = _session(user, total="80.00")

        hold = WalletTenderService.authorize_for_session(session, user)

        assert hold.amount == Money(Decimal("30.00"), "USD")

    def test_holds_move_no_money(self):
        """The stored balance and the ledger are untouched by the whole hold lifecycle."""
        wallet, user = _funded_wallet("100.00")
        session = _session(user)
        ledger_before = WalletTransaction.objects.filter(wallet=wallet).count()

        WalletTenderService.authorize_for_session(session, user)
        WalletTenderService.void_holds(session)
        WalletTenderService.expire_stale_holds()

        wallet.refresh_from_db()
        assert wallet.available_balance.amount == Decimal("100.00")
        assert WalletTransaction.objects.filter(wallet=wallet).count() == ledger_before

    def test_a_guest_is_refused(self):
        from django.contrib.auth.models import AnonymousUser

        _wallet, user = _funded_wallet()
        session = _session(user)

        with pytest.raises(WalletTenderError, match="signed-in"):
            WalletTenderService.authorize_for_session(session, AnonymousUser())

    def test_no_wallet_is_refused_not_created(self):
        """A spend path must never get_or_create a wallet."""
        user = UserFactory()
        session = _session(user)

        with pytest.raises(WalletTenderError, match="No wallet"):
            WalletTenderService.authorize_for_session(session, user)
        assert not CustomerWallet.objects.filter(customer=user).exists()

    def test_a_frozen_wallet_is_refused(self):
        wallet, user = _funded_wallet()
        wallet.is_active = False
        wallet.save(update_fields=["is_active"])
        session = _session(user)

        with pytest.raises(WalletTenderError, match="frozen"):
            WalletTenderService.authorize_for_session(session, user)

    def test_currency_mismatch_is_refused_never_converted(self):
        """D5 applies to the wallet exactly as to gift cards."""
        wallet, user = _funded_wallet()
        session = _session(user)
        session.total_amount = Money(Decimal("80.00"), "EUR")
        session.save(update_fields=["total_amount"])

        with pytest.raises(WalletTenderError, match="order is in EUR"):
            WalletTenderService.authorize_for_session(session, user)

    def test_two_sessions_cannot_promise_the_same_balance(self):
        """The second tab sees the first tab's hold."""
        wallet, user = _funded_wallet("100.00")
        first = _session(user, total="80.00")
        second = _session(user, total="80.00")

        WalletTenderService.authorize_for_session(first, user)
        hold2 = WalletTenderService.authorize_for_session(second, user)

        # 100 - 80 held leaves 20 spendable for the second session.
        assert hold2.amount == Money(Decimal("20.00"), "USD")
        held = PaymentTransaction.objects.filter(
            wallet=wallet, transaction_type="authorize", status="authorized"
        )
        total_held = sum((h.amount.amount for h in held), Decimal("0"))
        assert total_held <= Decimal("100.00")

    def test_resubmit_supersedes_own_hold(self):
        """A re-submit must not be blocked by its own previous hold."""
        wallet, user = _funded_wallet("100.00")
        session = _session(user, total="80.00")

        WalletTenderService.authorize_for_session(session, user)
        hold2 = WalletTenderService.authorize_for_session(session, user)

        assert hold2.amount == Money(Decimal("80.00"), "USD")
        live = PaymentTransaction.objects.filter(
            wallet=wallet, transaction_type="authorize", status="authorized"
        )
        assert live.count() == 1, "The superseded hold must be voided, not stacked."


class TestCapture:
    def _paid_order(self, user, total="80.00"):
        return OrderFactory(
            user=user,
            payment_status="paid",
            total_amount=Decimal(total),
            total_amount_currency="USD",
        )

    def _attach(self, hold, order):
        hold.order = order
        hold.save(update_fields=["order"])

    def test_capture_debits_wallet_and_writes_the_ledger(self):
        wallet, user = _funded_wallet("100.00")
        session = _session(user, total="80.00")
        hold = WalletTenderService.authorize_for_session(session, user)
        order = self._paid_order(user)
        self._attach(hold, order)

        captures = WalletTenderService.capture_for_order(order)

        assert len(captures) == 1
        wallet.refresh_from_db()
        assert wallet.available_balance.amount == Decimal("20.00")
        # The ledger row exists and cross-references the capture id (I5).
        assert WalletTransaction.objects.filter(
            wallet=wallet,
            transaction_type=WalletTransaction.TYPE_DEBIT,
            reference_id=captures[0].transaction_id,
        ).exists()
        hold.refresh_from_db()
        assert hold.status == "voided"

    def test_capture_is_idempotent(self):
        """A retried settlement signal debits once."""
        wallet, user = _funded_wallet("100.00")
        session = _session(user, total="80.00")
        hold = WalletTenderService.authorize_for_session(session, user)
        order = self._paid_order(user)
        self._attach(hold, order)

        WalletTenderService.capture_for_order(order)
        WalletTenderService.capture_for_order(order)

        wallet.refresh_from_db()
        assert wallet.available_balance.amount == Decimal("20.00"), (
            "A second capture pass debited the wallet again."
        )
        assert (
            WalletTransaction.objects.filter(
                wallet=wallet, transaction_type=WalletTransaction.TYPE_DEBIT
            ).count()
            == 1
        )

    def test_shrunk_cart_is_not_jointly_over_captured(self):
        """
        THE two-rail regression this phase exists to prevent.

        Order ends up at 60. A 50 gift card hold and a 50 wallet hold both
        exist (placed when the cart was bigger). Each rail capping at "total
        minus MY OWN captures" would take 50 + 50 = 100 from a 60 order.
        With the all-tender subtraction: gift card takes 50, wallet takes the
        remaining 10, and 40 of the wallet hold is released untouched.
        """
        from catalog.models import GiftCard
        from catalog.services.gift_card_tender_service import GiftCardTenderService
        from tests.factories import ProductFactory

        wallet, user = _funded_wallet("50.00")
        session = _session(user, total="100.00")

        product = ProductFactory(product_type="gift_card", status="published")
        card = GiftCard.objects.create(
            product=product,
            initial_value=Money(Decimal("50.00"), "USD"),
            recipient_email="r@test.spwig.com",
            is_active=True,
        )
        gc_hold = GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("50.00"), "USD")
        )
        w_hold = WalletTenderService.authorize_for_session(
            session, user, amount=Money(Decimal("50.00"), "USD")
        )

        # The cart shrank: the order is only 60 now.
        order = self._paid_order(user, total="60.00")
        for hold in (gc_hold, w_hold):
            self._attach(hold, order)

        gc_captures = GiftCardTenderService.capture_for_order(order)
        w_captures = WalletTenderService.capture_for_order(order)

        gc_total = sum((c.amount.amount for c in gc_captures), Decimal("0"))
        w_total = sum((c.amount.amount for c in w_captures), Decimal("0"))

        assert gc_total + w_total == Decimal("60.00"), (
            f"Jointly captured {gc_total + w_total} from a 60.00 order."
        )
        wallet.refresh_from_db()
        card.refresh_from_db()
        assert card.current_balance.amount == Decimal("0.00")  # card went first
        assert wallet.available_balance.amount == Decimal("40.00")  # only 10 taken

    def test_gift_card_rail_also_counts_foreign_captures(self):
        """
        The mirror of the shrunk-cart test, aimed at the GIFT CARD rail.

        In the shrunk-cart scenario the gift card captures FIRST, so its own
        subtraction never binds — the wallet side does the guarding. Here a
        completed gateway charge already covers most of the order before the
        gift card settles, so the GC rail's all-tender subtraction is the only
        thing standing between the customer and an over-capture. Mutating the
        GC service back to own-type-only fails THIS test, not the other one.
        """
        from catalog.models import GiftCard
        from catalog.services.gift_card_tender_service import GiftCardTenderService
        from tests.factories import ProductFactory

        _wallet, user = _funded_wallet("10.00")
        session = _session(user, total="60.00")
        product = ProductFactory(product_type="gift_card", status="published")
        card = GiftCard.objects.create(
            product=product,
            initial_value=Money(Decimal("50.00"), "USD"),
            recipient_email="r@test.spwig.com",
            is_active=True,
        )
        gc_hold = GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("50.00"), "USD")
        )
        order = self._paid_order(user, total="60.00")
        self._attach(gc_hold, order)
        # The gateway already charged 55 of the 60.
        PaymentTransaction.objects.create(
            transaction_id="chg-gateway-first",
            order=order,
            tender_type=PaymentTransaction.TENDER_GATEWAY,
            transaction_type="charge",
            status="completed",
            amount=Money(Decimal("55.00"), "USD"),
            settlement_amount=Money(Decimal("55.00"), "USD"),
            provider_account=None,
        )

        captures = GiftCardTenderService.capture_for_order(order)

        taken = sum((c.amount.amount for c in captures), Decimal("0"))
        assert taken == Decimal("5.00"), (
            f"Gift card took {taken} when only 5.00 of the order remained unfunded."
        )
        card.refresh_from_db()
        assert card.current_balance.amount == Decimal("45.00")

    def test_fully_funded_order_releases_the_hold_without_debiting(self):
        wallet, user = _funded_wallet("50.00")
        session = _session(user, total="80.00")
        hold = WalletTenderService.authorize_for_session(
            session, user, amount=Money(Decimal("50.00"), "USD")
        )
        order = self._paid_order(user, total="80.00")
        self._attach(hold, order)
        # Something else already funded the whole order.
        PaymentTransaction.objects.create(
            transaction_id="chg-covering",
            order=order,
            tender_type=PaymentTransaction.TENDER_GATEWAY,
            transaction_type="charge",
            status="completed",
            amount=Money(Decimal("80.00"), "USD"),
            settlement_amount=Money(Decimal("80.00"), "USD"),
            provider_account=None,
        )

        captures = WalletTenderService.capture_for_order(order)

        assert captures == []
        wallet.refresh_from_db()
        assert wallet.available_balance.amount == Decimal("50.00")
        hold.refresh_from_db()
        assert hold.status == "voided"


class TestRefundToWallet:
    def _captured(self, amount="40.00"):
        wallet, user = _funded_wallet("100.00")
        session = _session(user, total=amount)
        hold = WalletTenderService.authorize_for_session(session, user)
        order = OrderFactory(
            user=user,
            payment_status="paid",
            total_amount=Decimal(amount),
            total_amount_currency="USD",
        )
        hold.order = order
        hold.save(update_fields=["order"])
        (capture,) = WalletTenderService.capture_for_order(order)
        return wallet, capture

    def test_refund_credits_the_wallet(self):
        wallet, capture = self._captured("40.00")

        WalletTenderService.refund_to_wallet(
            capture, amount=Money(Decimal("15.00"), "USD"), refund_ref="r1"
        )

        wallet.refresh_from_db()
        assert wallet.available_balance.amount == Decimal("75.00")  # 100 - 40 + 15

    def test_refund_is_idempotent_before_money_moves(self):
        """The pre-lookup, not an IntegrityError afterwards, is the guard."""
        wallet, capture = self._captured("40.00")

        first = WalletTenderService.refund_to_wallet(
            capture, amount=Money(Decimal("15.00"), "USD"), refund_ref="r1"
        )
        second = WalletTenderService.refund_to_wallet(
            capture, amount=Money(Decimal("15.00"), "USD"), refund_ref="r1"
        )

        assert first.pk == second.pk
        wallet.refresh_from_db()
        assert wallet.available_balance.amount == Decimal("75.00"), (
            "A retried refund credited the wallet twice."
        )

    def test_refund_capacity_is_capped_at_the_capture(self):
        _wallet, capture = self._captured("40.00")

        with pytest.raises(WalletTenderError, match="exceed"):
            WalletTenderService.refund_to_wallet(
                capture, amount=Money(Decimal("45.00"), "USD"), refund_ref="r1"
            )

    def test_a_missing_refund_ref_is_a_programming_error(self):
        _wallet, capture = self._captured("40.00")

        with pytest.raises(WalletTenderError, match="refund_ref"):
            WalletTenderService.refund_to_wallet(capture, amount=Money(Decimal("15.00"), "USD"))

    def test_a_frozen_wallet_refuses_the_refund_loudly(self):
        wallet, capture = self._captured("40.00")
        wallet.is_active = False
        wallet.save(update_fields=["is_active"])

        with pytest.raises(WalletTenderError, match="frozen"):
            WalletTenderService.refund_to_wallet(
                capture, amount=Money(Decimal("15.00"), "USD"), refund_ref="r1"
            )
