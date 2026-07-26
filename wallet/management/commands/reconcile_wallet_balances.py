"""
Verify every wallet's stored balance against its own ledger (invariant I5).

    available_balance == signed sum of the ledger over {completed, reversed}

Signs: credit and refund add; debit and reversal subtract. A REVERSED original
was a real movement — its compensating TYPE_REVERSAL row is completed, so the
pair nets to zero and neither may be excluded. Only ``pending`` rows are
outside the sum.

This ships BEFORE the wallet becomes a payment tender, deliberately: it is the
net under everything P2.5 builds. Once orders debit wallets and refunds credit
them, a bug in either rail shows up here as non-zero drift the next night,
with an exit code a beat task can alarm on — instead of surfacing months later
as a customer insisting their balance is wrong.

Read-only by default. ``--fix`` re-stamps the stored balance from the ledger,
under ``select_for_update``, and is idempotent — a second run finds no drift.

Two conditions are REPORTED but never auto-fixed:

* ``TYPE_ADJUSTMENT`` rows. No writer for them exists anywhere in the
  codebase and their sign convention is undefined — guessing a sign while
  "fixing" a balance is how reconciliation tools corrupt ledgers. A human
  decides what an adjustment meant.
* Mixed-currency history (ledger rows in a different currency than the
  wallet). The P2.1 currency guard prevents new ones; any survivor predates it
  and the correct rate is a business decision, not a code default.
"""

from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from wallet.models import CustomerWallet, WalletTransaction

POSITIVE_TYPES = (WalletTransaction.TYPE_CREDIT, WalletTransaction.TYPE_REFUND)
NEGATIVE_TYPES = (WalletTransaction.TYPE_DEBIT, WalletTransaction.TYPE_REVERSAL)
COUNTED_STATUSES = (
    WalletTransaction.STATUS_COMPLETED,
    WalletTransaction.STATUS_REVERSED,
)


def ledger_balance(wallet):
    """
    The balance the ledger says this wallet holds, or None if it cannot be
    derived (adjustment rows / mixed currency — human territory).
    """
    rows = wallet.transactions.filter(status__in=COUNTED_STATUSES)

    problems = []
    total = Decimal("0")
    wallet_currency = str(wallet.available_balance.currency)

    for row in rows:
        if str(row.amount.currency) != wallet_currency:
            problems.append(
                f"txn {row.pk}: {row.amount.currency} row in a {wallet_currency} wallet"
            )
            continue
        if row.transaction_type == WalletTransaction.TYPE_ADJUSTMENT:
            problems.append(
                f"txn {row.pk}: TYPE_ADJUSTMENT ({row.amount}) — sign convention "
                f"undefined, no writer exists; resolve by hand"
            )
            continue
        if row.transaction_type in POSITIVE_TYPES:
            total += row.amount.amount
        elif row.transaction_type in NEGATIVE_TYPES:
            total -= row.amount.amount
        else:
            problems.append(f"txn {row.pk}: unknown type {row.transaction_type!r}")

    return (None, problems) if problems else (total, [])


class Command(BaseCommand):
    help = "Verify (and with --fix, repair) wallet balances against their ledgers (I5)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--fix",
            action="store_true",
            help="Re-stamp drifted balances from the ledger. Never touches "
            "wallets with adjustment rows or mixed-currency history.",
        )

    def handle(self, *args, **options):
        fix = options["fix"]
        drifted, unfixable, clean = [], [], 0

        for wallet in CustomerWallet.objects.iterator():
            derived, problems = ledger_balance(wallet)

            if problems:
                unfixable.append((wallet, problems))
                continue

            stored = wallet.available_balance.amount
            if derived == stored:
                clean += 1
                continue

            drifted.append((wallet, stored, derived))
            self.stderr.write(
                f"DRIFT wallet={wallet.pk} customer={wallet.customer_id} "
                f"stored={stored} ledger={derived} delta={stored - derived}"
            )

            if fix:
                with transaction.atomic():
                    locked = CustomerWallet.objects.select_for_update().get(pk=wallet.pk)
                    # Re-derive under the lock — a capture may have landed
                    # between the scan and the fix.
                    fresh, fresh_problems = ledger_balance(locked)
                    if fresh_problems or fresh is None:
                        unfixable.append((locked, fresh_problems))
                        continue
                    locked.available_balance = fresh
                    locked.save(update_fields=["available_balance", "updated_at"])
                    self.stdout.write(f"FIXED wallet={locked.pk} -> {fresh}")

        for wallet, problems in unfixable:
            for problem in problems:
                self.stderr.write(f"UNFIXABLE wallet={wallet.pk}: {problem}")

        self.stdout.write(
            f"{clean} clean, {len(drifted)} drifted"
            f"{' (fixed)' if fix and drifted else ''}, {len(unfixable)} need a human"
        )

        if (drifted and not fix) or unfixable:
            # Non-zero exit is the alarm the nightly beat task relies on.
            raise SystemExit(1)
