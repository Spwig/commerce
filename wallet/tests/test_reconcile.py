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
