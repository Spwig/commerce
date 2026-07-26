"""
P2.1b — GiftCard model hardening and the tender check constraints.

The tender rail is only as safe as the primitive underneath it.
``GiftCardTenderService`` calls ``GiftCard.redeem`` and ``adjust_balance``, so
those two have to hold the line on their own:

* **Row locking.** Both are read-modify-writes on money. Without
  ``select_for_update`` two concurrent redemptions read the same pre-deduction
  balance and the second write overwrites the first — the same value is spent
  twice and the card ends up holding money that is already gone.
* **No negative balances.** ``adjust_balance`` accepts negative amounts, so an
  over-large debit is a live path to a card that owes the merchant money.
* **Ledger atomicity.** The ``GiftCardTransaction`` row is written *inside* the
  same transaction as the deduction. Outside it, a failure would leave a
  debited balance with no ledger entry, and summing the ledger would stop
  reconciling — the invariant that makes stored value auditable.
* **PROTECT.** The ledger records movements of real customer money. Deleting a
  card must not take its financial history with it.

Plus the two ``PaymentTransaction`` check constraints, which are money
invariants rather than tidiness: a gift card tender with no card FK is
unattributable money, and a card FK on a non-gift-card tender corrupts the
available-balance sum.

Plan: docs/.claude_code/plans/wondrous-moseying-wolf.md (R2, P2.1b)
"""

import threading
from decimal import Decimal
from unittest import mock

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, connection, transaction
from django.db.models import ProtectedError
from djmoney.money import Money

from catalog.models import GiftCard, GiftCardTransaction
from payment_providers.models import PaymentTransaction
from tests.factories import OrderFactory, ProductFactory

pytestmark = [
    pytest.mark.integration,
    pytest.mark.r2,
    pytest.mark.gift_card_tender,
]


def _card(product, value="100.00", currency="USD", **kwargs):
    defaults = {
        "product": product,
        "initial_value": Money(Decimal(value), currency),
        "recipient_email": "recipient@test.spwig.com",
        "is_active": True,
    }
    defaults.update(kwargs)
    return GiftCard.objects.create(**defaults)


def _reread(card):
    return GiftCard.objects.get(pk=card.pk)


def _ledger_total(card):
    return sum(
        (t.amount.amount for t in GiftCardTransaction.objects.filter(gift_card=card)),
        Decimal("0"),
    )


# ============================================================
# redeem / adjust_balance under concurrency
# ============================================================


@pytest.mark.django_db(transaction=True)
class TestConcurrentRedemption:
    """
    Real threads on real connections. ``django_db(transaction=True)`` is
    required: the ordinary fixture wraps the test in a transaction the worker
    connections cannot see, so every worker would find an empty database.
    """

    @staticmethod
    def _race(target, worker_count):
        results = []
        results_lock = threading.Lock()
        barrier = threading.Barrier(worker_count, timeout=20)

        def worker(index):
            try:
                barrier.wait()
                try:
                    outcome = ("ok", target(index))
                except Exception as exc:  # noqa: BLE001 — classified by the caller
                    outcome = ("error", exc)
                with results_lock:
                    results.append(outcome)
            finally:
                # A leaked connection holds the row lock open and the next test
                # blocks instead of failing with anything readable.
                connection.close()

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(worker_count)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=30)

        assert not any(t.is_alive() for t in threads), (
            "A worker thread did not finish — most likely deadlocked on a row lock."
        )
        return results

    @pytest.fixture
    def product(self):
        return ProductFactory(product_type="gift_card", status="published")

    def test_only_one_of_two_racing_redemptions_succeeds(self, product):
        card = _card(product, "50.00")

        def redeem(index):
            return GiftCard.objects.get(pk=card.pk).redeem(
                amount=Money(Decimal("30.00"), "USD"), notes=f"Race {index}"
            )

        results = self._race(redeem, worker_count=2)
        successes = [r for kind, r in results if kind == "ok"]
        failures = [r for kind, r in results if kind == "error"]

        assert len(successes) == 1, (
            f"{len(successes)} redemptions of 30.00 succeeded against a 50.00 "
            "card. The same stored value was spent twice."
        )
        assert isinstance(failures[0], ValidationError), (
            f"The losing redemption failed with {type(failures[0]).__name__}: {failures[0]}."
        )

    def test_the_final_balance_is_correct_after_a_race(self, product):
        card = _card(product, "50.00")

        def redeem(index):
            return GiftCard.objects.get(pk=card.pk).redeem(
                amount=Money(Decimal("30.00"), "USD"), notes=f"Race {index}"
            )

        self._race(redeem, worker_count=2)

        assert _reread(card).current_balance == Money(Decimal("20.00"), "USD")

    def test_the_ledger_reconciles_after_a_race(self, product):
        """
        The failure mode this catches is a refused redemption that still wrote
        its ledger row — the balance and the ledger then disagree forever.
        """
        card = _card(product, "50.00")

        def redeem(index):
            return GiftCard.objects.get(pk=card.pk).redeem(
                amount=Money(Decimal("30.00"), "USD"), notes=f"Race {index}"
            )

        self._race(redeem, worker_count=2)

        card = _reread(card)
        assert GiftCardTransaction.objects.filter(gift_card=card).count() == 1
        assert card.initial_value.amount + _ledger_total(card) == card.current_balance.amount

    def test_concurrent_adjustments_all_land(self, product):
        """
        Negative control for the lock in ``adjust_balance``: credits never fail
        on sufficiency, so five concurrent +10.00 adjustments must sum exactly.
        A lost update shows up as a balance below 150.00.
        """
        card = _card(product, "100.00")

        def adjust(index):
            return GiftCard.objects.get(pk=card.pk).adjust_balance(
                Money(Decimal("10.00"), "USD"), reason=f"Concurrent top-up {index}"
            )

        results = self._race(adjust, worker_count=5)
        errors = [r for kind, r in results if kind == "error"]
        assert not errors, f"Adjustments failed unexpectedly: {errors}"

        assert _reread(card).current_balance == Money(Decimal("150.00"), "USD")

    def test_a_redemption_racing_an_adjustment_does_not_lose_a_write(self, product):
        """
        An admin adjustment landing at the same moment as a customer redemption
        is the realistic version of this race, and the one where a lost write
        looks like a support ticket rather than a test failure.
        """
        card = _card(product, "100.00")

        def movement(index):
            fresh = GiftCard.objects.get(pk=card.pk)
            if index == 0:
                return fresh.redeem(amount=Money(Decimal("30.00"), "USD"), notes="Spend")
            return fresh.adjust_balance(Money(Decimal("20.00"), "USD"), reason="Top-up")

        results = self._race(movement, worker_count=2)
        errors = [r for kind, r in results if kind == "error"]
        assert not errors, f"Movements failed unexpectedly: {errors}"

        card = _reread(card)
        assert card.current_balance == Money(Decimal("90.00"), "USD"), (
            f"Balance is {card.current_balance}, expected 90.00 (100 - 30 + 20). "
            "One of the two writes was lost."
        )
        assert card.initial_value.amount + _ledger_total(card) == card.current_balance.amount


# ============================================================
# adjust_balance guards
# ============================================================


@pytest.mark.django_db
class TestAdjustBalanceRefusesNegative:
    @pytest.fixture
    def product(self):
        return ProductFactory(product_type="gift_card", status="published")

    def test_an_adjustment_below_zero_is_refused(self, product):
        card = _card(product, "50.00")

        with pytest.raises(ValidationError):
            card.adjust_balance(Money(Decimal("-50.01"), "USD"), reason="Over-debit")

        assert _reread(card).current_balance == Money(Decimal("50.00"), "USD")

    def test_the_refused_adjustment_writes_no_ledger_row(self, product):
        card = _card(product, "50.00")

        with pytest.raises(ValidationError):
            card.adjust_balance(Money(Decimal("-50.01"), "USD"), reason="Over-debit")

        assert GiftCardTransaction.objects.filter(gift_card=card).count() == 0

    def test_an_adjustment_to_exactly_zero_is_allowed(self, product):
        """Boundary: the guard is < 0, not <= 0."""
        card = _card(product, "50.00")

        card.adjust_balance(Money(Decimal("-50.00"), "USD"), reason="Zero it out")

        assert _reread(card).current_balance == Money(Decimal("0.00"), "USD")

    def test_a_negative_adjustment_within_the_balance_is_allowed(self, product):
        card = _card(product, "50.00")

        card.adjust_balance(Money(Decimal("-20.00"), "USD"), reason="Correction")

        assert _reread(card).current_balance == Money(Decimal("30.00"), "USD")


# ============================================================
# Ledger atomicity
# ============================================================


@pytest.mark.django_db
class TestLedgerIsWrittenInsideTheDeduction:
    @pytest.fixture
    def product(self):
        return ProductFactory(product_type="gift_card", status="published")

    def test_a_failed_ledger_write_rolls_back_the_deduction(self, product):
        """
        If the ledger row were written outside the transaction that deducts the
        balance, this failure would leave the card debited with no record of
        why — the balance and the ledger would disagree permanently and there
        would be nothing to reconcile against.
        """
        card = _card(product, "100.00")

        with mock.patch(
            "catalog.models.GiftCardTransaction.objects.create",
            side_effect=RuntimeError("ledger unavailable"),
        ):
            with pytest.raises(RuntimeError):
                card.redeem(amount=Money(Decimal("40.00"), "USD"), notes="Boom")

        assert _reread(card).current_balance == Money(Decimal("100.00"), "USD"), (
            "The balance was deducted even though the ledger row failed to "
            "write. Stored value moved with no audit trail."
        )

    def test_a_failed_ledger_write_during_an_adjustment_rolls_back_too(self, product):
        card = _card(product, "100.00")

        with mock.patch(
            "catalog.models.GiftCardTransaction.objects.create",
            side_effect=RuntimeError("ledger unavailable"),
        ):
            with pytest.raises(RuntimeError):
                card.adjust_balance(Money(Decimal("-40.00"), "USD"), reason="Boom")

        assert _reread(card).current_balance == Money(Decimal("100.00"), "USD")

    def test_a_successful_redemption_writes_both(self, product):
        """Negative control: the rollback above is caused by the failure, not by the mock."""
        card = _card(product, "100.00")

        card.redeem(amount=Money(Decimal("40.00"), "USD"), notes="Real")

        card = _reread(card)
        assert card.current_balance == Money(Decimal("60.00"), "USD")
        assert GiftCardTransaction.objects.filter(gift_card=card).count() == 1


# ============================================================
# PROTECT on the ledger FK
# ============================================================


@pytest.mark.django_db
class TestGiftCardTransactionProtectsTheCard:
    @pytest.fixture
    def product(self):
        return ProductFactory(product_type="gift_card", status="published")

    def test_a_card_with_ledger_rows_cannot_be_deleted(self, product):
        """
        This was CASCADE. Deleting a card silently took its financial history
        with it — including cards that still held customer value.
        """
        card = _card(product, "100.00")
        card.redeem(amount=Money(Decimal("40.00"), "USD"), notes="Spent")

        with pytest.raises(ProtectedError):
            card.delete()

        assert GiftCard.objects.filter(pk=card.pk).exists()
        assert GiftCardTransaction.objects.filter(gift_card=card).count() == 1

    def test_a_card_with_no_ledger_rows_can_still_be_deleted(self, product):
        """Negative control: PROTECT is about the history, not about cards generally."""
        card = _card(product, "100.00")
        card_pk = card.pk

        card.delete()

        assert not GiftCard.objects.filter(pk=card_pk).exists()

    def test_the_ledger_survives_after_the_protected_delete_attempt(self, product):
        card = _card(product, "100.00")
        card.redeem(amount=Money(Decimal("40.00"), "USD"), notes="Spent")

        with pytest.raises(ProtectedError):
            card.delete()

        row = GiftCardTransaction.objects.get(gift_card=card)
        assert row.amount == Money(Decimal("-40.00"), "USD")
        assert row.balance_after == Money(Decimal("60.00"), "USD")

    def test_a_card_backing_a_tender_row_cannot_be_deleted(self, product):
        """``PaymentTransaction.gift_card`` is PROTECT for the same reason."""
        card = _card(product, "100.00")
        PaymentTransaction.objects.create(
            transaction_id="gc-auth:protect-test:1",
            tender_type=PaymentTransaction.TENDER_GIFT_CARD,
            transaction_type="authorize",
            status="authorized",
            gift_card=card,
            amount=Money(Decimal("40.00"), "USD"),
        )

        with pytest.raises(ProtectedError):
            card.delete()


# ============================================================
# PaymentTransaction tender check constraints
# ============================================================


@pytest.mark.django_db
class TestTenderCheckConstraints:
    @pytest.fixture
    def product(self):
        return ProductFactory(product_type="gift_card", status="published")

    def test_a_gift_card_tender_without_a_card_is_rejected(self):
        """
        Unattributable money: a balance would be debited with no record of
        whose card it came from.
        """
        with pytest.raises(IntegrityError) as exc:
            with transaction.atomic():
                PaymentTransaction.objects.create(
                    transaction_id="gc-orphan:1",
                    tender_type=PaymentTransaction.TENDER_GIFT_CARD,
                    transaction_type="authorize",
                    status="authorized",
                    gift_card=None,
                    amount=Money(Decimal("40.00"), "USD"),
                )

        assert "pp_txn_giftcard_tender_needs_card" in str(exc.value)

    def test_a_card_on_a_non_gift_card_tender_is_rejected(self, product):
        """
        The tender type would be wrong, which corrupts the available-balance
        sum: ``held_amount`` filters on ``tender_type='gift_card'``, so a hold
        mislabelled as a gateway charge reserves nothing while the card is
        genuinely committed.
        """
        card = _card(product, "100.00")

        with pytest.raises(IntegrityError) as exc:
            with transaction.atomic():
                PaymentTransaction.objects.create(
                    transaction_id="gw-with-card:1",
                    tender_type=PaymentTransaction.TENDER_GATEWAY,
                    transaction_type="charge",
                    status="completed",
                    gift_card=card,
                    amount=Money(Decimal("40.00"), "USD"),
                )

        assert "pp_txn_card_only_on_giftcard_tender" in str(exc.value)

    def test_a_wallet_tender_with_a_card_is_also_rejected(self, product):
        """The constraint is about gift_card being set, not about 'gateway'."""
        card = _card(product, "100.00")

        with pytest.raises(IntegrityError):
            with transaction.atomic():
                PaymentTransaction.objects.create(
                    transaction_id="wallet-with-card:1",
                    tender_type=PaymentTransaction.TENDER_WALLET,
                    transaction_type="charge",
                    status="completed",
                    gift_card=card,
                    amount=Money(Decimal("40.00"), "USD"),
                )

    def test_a_valid_gift_card_tender_is_accepted(self, product):
        """Negative control: the constraints admit the shapes they are meant to."""
        card = _card(product, "100.00")

        row = PaymentTransaction.objects.create(
            transaction_id="gc-valid:1",
            tender_type=PaymentTransaction.TENDER_GIFT_CARD,
            transaction_type="authorize",
            status="authorized",
            gift_card=card,
            amount=Money(Decimal("40.00"), "USD"),
        )

        assert row.pk is not None

    def test_a_valid_gateway_tender_without_a_card_is_accepted(self):
        row = PaymentTransaction.objects.create(
            transaction_id="gw-valid:1",
            tender_type=PaymentTransaction.TENDER_GATEWAY,
            transaction_type="charge",
            status="completed",
            amount=Money(Decimal("40.00"), "USD"),
        )

        assert row.pk is not None
        assert row.gift_card_id is None

    def test_a_cash_tender_without_a_card_is_accepted(self):
        """POS tenders have no card and no provider account."""
        row = PaymentTransaction.objects.create(
            transaction_id="cash-valid:1",
            tender_type=PaymentTransaction.TENDER_CASH,
            transaction_type="charge",
            status="completed",
            amount=Money(Decimal("40.00"), "USD"),
        )

        assert row.pk is not None


# ============================================================
# redeem guards
# ============================================================


@pytest.mark.django_db
class TestRedeemGuards:
    @pytest.fixture
    def product(self):
        return ProductFactory(product_type="gift_card", status="published")

    def test_redeeming_more_than_the_balance_is_refused(self, product):
        card = _card(product, "50.00")

        with pytest.raises(ValidationError):
            card.redeem(amount=Money(Decimal("50.01"), "USD"))

        assert _reread(card).current_balance == Money(Decimal("50.00"), "USD")
        assert GiftCardTransaction.objects.filter(gift_card=card).count() == 0

    def test_redeeming_in_another_currency_is_refused(self, product):
        """D5: a card is spendable only against its own currency."""
        card = _card(product, "50.00", currency="USD")

        with pytest.raises(ValidationError):
            card.redeem(amount=Money(Decimal("10.00"), "EUR"))

        assert _reread(card).current_balance == Money(Decimal("50.00"), "USD")

    def test_redeeming_from_an_inactive_card_is_refused(self, product):
        card = _card(product, "50.00", is_active=False)

        with pytest.raises(ValidationError):
            card.redeem(amount=Money(Decimal("10.00"), "USD"))

    def test_redeem_validates_against_the_stored_balance_not_a_stale_copy(self, product):
        """
        ``redeem`` re-reads under the lock. A caller holding a stale instance
        from before someone else's redemption must not be able to spend value
        that is already gone.
        """
        card = _card(product, "50.00")
        stale = GiftCard.objects.get(pk=card.pk)

        GiftCard.objects.get(pk=card.pk).redeem(
            amount=Money(Decimal("40.00"), "USD"), notes="Someone else"
        )

        # `stale` still believes the card holds 50.00.
        assert stale.current_balance == Money(Decimal("50.00"), "USD")

        with pytest.raises(ValidationError):
            stale.redeem(amount=Money(Decimal("30.00"), "USD"), notes="Stale spend")

        assert _reread(card).current_balance == Money(Decimal("10.00"), "USD")

    def test_redeem_stamps_first_used_at_once(self, product):
        card = _card(product, "50.00")
        assert card.first_used_at is None

        card.redeem(amount=Money(Decimal("10.00"), "USD"))
        first = _reread(card).first_used_at
        assert first is not None

        card.redeem(amount=Money(Decimal("10.00"), "USD"))
        assert _reread(card).first_used_at == first, (
            "first_used_at moved on the second redemption; it records the first."
        )

    def test_redeem_records_the_order(self, product):
        card = _card(product, "50.00")
        order = OrderFactory()

        txn = card.redeem(amount=Money(Decimal("10.00"), "USD"), order=order, notes="For order")

        assert txn.order_id == order.pk
