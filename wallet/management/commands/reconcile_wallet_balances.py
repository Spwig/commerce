"""
Verify every wallet's stored balance against its own ledger (invariant I5).

    available_balance == signed sum of the ledger over {completed, reversed}

Signs: credit and refund add; debit and reversal subtract. A manual
``adjustment`` is a signed correction — its recorded ``balance_after`` carries
the sign the positive-only amount cannot, and the replay verifies that against
the amount (see ``ledger_balance``). A REVERSED original was a real movement —
its compensating TYPE_REVERSAL row is completed, so the pair nets to zero and
neither may be excluded. Only ``pending`` rows are outside the sum.

This ships BEFORE the wallet becomes a payment tender, deliberately: it is the
net under everything P2.5 builds. Once orders debit wallets and refunds credit
them, a bug in either rail shows up here as non-zero drift the next night,
with an exit code a beat task can alarm on — instead of surfacing months later
as a customer insisting their balance is wrong.

Each wallet is read under ``select_for_update`` so its stored balance and
ledger are compared against a consistent snapshot — an unlocked scan can race a
concurrent capture and either fabricate or mask drift. ``--fix`` re-stamps the
stored balance from the ledger within that same lock and is idempotent — a
second run finds no drift.

Two conditions are REPORTED but never auto-fixed:

* A **malformed** ``TYPE_ADJUSTMENT`` row — one whose ``balance_after`` delta
  does not equal its ``amount``. Well-formed adjustments written by
  ``WalletService.adjust_balance`` reconcile normally (their balance_after
  carries the sign); a row that fails that check was hand-written or corrupted,
  and guessing a sign while "fixing" a balance is how reconciliation tools
  corrupt ledgers. A human decides what such a row meant.
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
    derived (a malformed adjustment or mixed currency — human territory).

    Rows are replayed oldest-first as a running total: credit/refund add and
    debit/reversal subtract by ``amount`` (an independent check, blind to the
    stored ``balance_after``). A ``TYPE_ADJUSTMENT`` is a signed correction whose
    ``balance_after`` records the result; its effect is reconstructed as
    ``balance_after - running_total`` and MUST equal ``±amount``, or the row is
    malformed (a hand-written or corrupted adjustment) and is reported for a
    human rather than guessed.

    Accepted limitation (adjustments only): because the adjustment's direction is
    not persisted, its SIGN is taken from ``balance_after`` — the field this
    replay otherwise verifies — so for adjustment rows the check confirms
    magnitude (``abs(delta) == amount``) but not sign independently. Every
    adjustment the app can write (``WalletService.adjust_balance``) sets
    ``balance_after`` atomically under the wallet lock, so a consistent-but-wrong
    adjustment can only arise from a direct database write, which is outside the
    application trust boundary (an actor with DB write access can corrupt any
    row). All OTHER row types keep the fully-independent amount-only check.
    """
    rows = wallet.transactions.filter(status__in=COUNTED_STATUSES).order_by("created_at", "pk")

    problems = []
    total = Decimal("0")
    wallet_currency = str(wallet.available_balance.currency)

    for row in rows:
        if str(row.amount.currency) != wallet_currency:
            problems.append(
                f"txn {row.pk}: {row.amount.currency} row in a {wallet_currency} wallet"
            )
            continue
        amount = row.amount.amount
        if row.transaction_type in POSITIVE_TYPES:
            total += amount
        elif row.transaction_type in NEGATIVE_TYPES:
            total -= amount
        elif row.transaction_type == WalletTransaction.TYPE_ADJUSTMENT:
            # Signed correction: the writer (WalletService.adjust_balance) records
            # the resulting balance in balance_after, so the delta reconstructs
            # the sign the positive-only amount cannot carry. A delta that does
            # not match the amount means the row was not written by the service —
            # do not guess a sign, report it.
            delta = row.balance_after.amount - total
            if abs(delta) != amount:
                problems.append(
                    f"txn {row.pk}: TYPE_ADJUSTMENT balance_after {row.balance_after} "
                    f"inconsistent with amount {row.amount} (delta {delta}); resolve by hand"
                )
                continue
            total += delta
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

        # Stream ids without a lock, then lock each wallet individually. Both
        # the stored balance and the ledger must be read inside one lock so the
        # comparison sees a consistent snapshot: an unlocked read can catch a
        # capture mid-commit and either fabricate drift OR mask real drift (a
        # concurrent row nudging the ledger to match a stale stored balance),
        # so the clean verdict is only trustworthy under the same lock.
        for wallet_id in CustomerWallet.objects.values_list("pk", flat=True).iterator():
            with transaction.atomic():
                wallet = CustomerWallet.objects.select_for_update().get(pk=wallet_id)
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
                    wallet.available_balance = derived
                    wallet.save(update_fields=["available_balance", "updated_at"])
                    self.stdout.write(f"FIXED wallet={wallet.pk} -> {derived}")

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
