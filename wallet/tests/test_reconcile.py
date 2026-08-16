"""
Invariant I5: available_balance == signed ledger sum over {completed, reversed}.

The reconciler ships BEFORE the wallet becomes a payment tender: it is the net
under P2.5's money movement. These tests pin the sum's exact semantics, because
every plausible variation is wrong in a way that hides real drift:

* Excluding REVERSED originals double-subtracts (the compensating reversal row
  would then swing the sum negative).
* Counting PENDING rows books money that has not moved.
* Guessing a sign for TYPE_ADJUSTMENT rows (no writer exists, convention
  undefined) is how reconciliation tools corrupt the very ledgers they check.
"""

from decimal import Decimal

import pytest
from django.core.management import call_command
from djmoney.money import Money

from tests.factories import UserFactory
from wallet.models import CustomerWallet, WalletTransaction
from wallet.services import WalletService

pytestmark = [pytest.mark.django_db, pytest.mark.wallet, pytest.mark.r2]


def _wallet(user=None):
    return WalletService.get_or_create_wallet(user or UserFactory())


def _run(*args):
    """Run the command; return (exit_ok, so tests read naturally)."""
    try:
        call_command("reconcile_wallet_balances", *args)
        return True
    except SystemExit:
        return False


class TestCleanLedgersReconcile:
    def test_credits_debits_and_a_reversal_pair_net_to_the_stored_balance(self):
        wallet = _wallet()
        WalletService.credit(wallet.customer, Decimal("50.00"), "USD", "manual", "t")
        WalletService.debit(wallet.customer, Decimal("20.00"), "USD", "manual", "t")
        credit2 = WalletService.credit(wallet.customer, Decimal("10.00"), "USD", "manual", "t")
        WalletService.reverse_transaction(credit2, reason="t")

        assert _run() is True

        wallet.refresh_from_db()
        # 50 - 20 + 10 - 10: the reversed original still counts; its
        # compensating reversal row nets it out.
        assert wallet.available_balance.amount == Decimal("30.00")

    def test_an_empty_wallet_is_clean(self):
        _wallet()
        assert _run() is True


class TestDriftIsDetectedAndRepaired:
    def test_a_corrupted_balance_exits_nonzero(self):
        wallet = _wallet()
        WalletService.credit(wallet.customer, Decimal("50.00"), "USD", "manual", "t")

        # Corrupt the stored balance behind the ledger's back.
        CustomerWallet.objects.filter(pk=wallet.pk).update(available_balance=Decimal("999.00"))

        assert _run() is False, "Drift must exit non-zero — it is the alarm."

    def test_fix_restamps_from_the_ledger_and_is_idempotent(self):
        wallet = _wallet()
        WalletService.credit(wallet.customer, Decimal("50.00"), "USD", "manual", "t")
        CustomerWallet.objects.filter(pk=wallet.pk).update(available_balance=Decimal("999.00"))

        assert _run("--fix") is True
        wallet.refresh_from_db()
        assert wallet.available_balance.amount == Decimal("50.00")

        # Second run: nothing left to fix.
        assert _run() is True


class TestHumanTerritoryIsNeverAutoFixed:
    def test_an_adjustment_row_is_reported_not_guessed(self):
        wallet = _wallet()
        WalletService.credit(wallet.customer, Decimal("50.00"), "USD", "manual", "t")
        WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type=WalletTransaction.TYPE_ADJUSTMENT,
            amount=Money(Decimal("5.00"), "USD"),
            balance_after=wallet.available_balance,
            status=WalletTransaction.STATUS_COMPLETED,
            source="manual",
            description="hand-made row with no defined sign",
        )

        assert _run() is False, "Adjustment rows need a human, not a guess."

        # --fix must refuse too: the balance stays whatever it was.
        wallet.refresh_from_db()
        before = wallet.available_balance.amount
        _run("--fix")
        wallet.refresh_from_db()
        assert wallet.available_balance.amount == before

    def test_pending_rows_are_outside_the_sum(self):
        wallet = _wallet()
        WalletService.credit(wallet.customer, Decimal("50.00"), "USD", "manual", "t")
        WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type=WalletTransaction.TYPE_DEBIT,
            amount=Money(Decimal("40.00"), "USD"),
            balance_after=wallet.available_balance,
            status=WalletTransaction.STATUS_PENDING,
            source="manual",
            description="not yet moved",
        )

        # Stored balance reflects only completed movement; pending must not
        # count, or the reconciler reports phantom drift.
        assert _run() is True


class TestWellFormedAdjustmentsReconcile:
    """Adjustments written by the service carry their sign in balance_after and
    now reconcile — only rows that fail that consistency check need a human."""

    def _staff(self):
        return UserFactory(staff=True)

    def test_an_increase_adjustment_reconciles_clean(self):
        wallet = _wallet()
        WalletService.credit(wallet.customer, Decimal("50.00"), "USD", "manual", "t")
        WalletService.adjust_balance(
            wallet.customer,
            Decimal("5.00"),
            "increase",
            "USD",
            "correction",
            created_by=self._staff(),
        )
        assert _run() is True
        wallet.refresh_from_db()
        assert wallet.available_balance.amount == Decimal("55.00")

    def test_a_decrease_adjustment_reconciles_clean(self):
        wallet = _wallet()
        WalletService.credit(wallet.customer, Decimal("50.00"), "USD", "manual", "t")
        WalletService.adjust_balance(
            wallet.customer,
            Decimal("12.00"),
            "decrease",
            "USD",
            "clawback",
            created_by=self._staff(),
        )
        assert _run() is True
        wallet.refresh_from_db()
        assert wallet.available_balance.amount == Decimal("38.00")

    def test_adjustments_interleaved_with_credits_debits_reconcile(self):
        wallet = _wallet()
        WalletService.credit(wallet.customer, Decimal("100.00"), "USD", "manual", "t")
        WalletService.adjust_balance(
            wallet.customer, Decimal("10.00"), "decrease", "USD", "a", created_by=self._staff()
        )
        WalletService.debit(wallet.customer, Decimal("20.00"), "USD", "order", "t")
        WalletService.adjust_balance(
            wallet.customer, Decimal("5.00"), "increase", "USD", "a", created_by=self._staff()
        )
        # 100 - 10 - 20 + 5
        assert _run() is True
        wallet.refresh_from_db()
        assert wallet.available_balance.amount == Decimal("75.00")

    def test_refund_typed_rows_count_as_positive(self):
        wallet = _wallet()
        WalletService.record_refund_transaction(wallet.customer, Decimal("30.00"), "USD", "refund")
        assert _run() is True
        wallet.refresh_from_db()
        assert wallet.available_balance.amount == Decimal("30.00")

    def test_drift_on_a_wallet_with_an_adjustment_is_now_fixable(self):
        wallet = _wallet()
        WalletService.credit(wallet.customer, Decimal("50.00"), "USD", "manual", "t")
        WalletService.adjust_balance(
            wallet.customer, Decimal("5.00"), "increase", "USD", "c", created_by=self._staff()
        )
        # Corrupt the stored balance behind the ledger's back.
        CustomerWallet.objects.filter(pk=wallet.pk).update(available_balance=Decimal("999.00"))

        assert _run("--fix") is True
        wallet.refresh_from_db()
        assert wallet.available_balance.amount == Decimal("55.00")

    def test_a_malformed_adjustment_is_still_reported_and_not_fixed(self):
        # balance_after that contradicts the amount was not written by the
        # service — the reconciler must not guess its sign.
        wallet = _wallet()
        WalletService.credit(wallet.customer, Decimal("50.00"), "USD", "manual", "t")
        WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type=WalletTransaction.TYPE_ADJUSTMENT,
            amount=Money(Decimal("5.00"), "USD"),
            balance_after=Money(Decimal("50.00"), "USD"),  # delta 0 ≠ amount 5
            status=WalletTransaction.STATUS_COMPLETED,
            source="manual",
            description="hand-made, inconsistent",
        )
        assert _run() is False
        wallet.refresh_from_db()
        before = wallet.available_balance.amount
        _run("--fix")
        wallet.refresh_from_db()
        assert wallet.available_balance.amount == before
