"""
Enforce one reversal per LoyaltyTransaction.

`LedgerService.refund_redemption` guarded against double-refunds with an
`.exists()` check outside any lock, which under READ COMMITTED lets two
concurrent refunds both observe "not refunded" and both credit the balance.
This constraint is the real control; the application check is now just a
friendlier error.

Because the old code could race, an install may already contain duplicate
reversals. Adding the constraint against such data fails the migration — and a
failed migration blocks startup (docker-entrypoint.sh) and the upgrader's
`migrate --check` health gate. So duplicates are detected and reported first,
with the numbers needed to correct the balances by hand.
"""

from django.conf import settings
from django.db import migrations, models


def check_for_duplicate_reversals(apps, schema_editor):
    """
    Fail loudly, with detail, if pre-existing duplicate reversals exist.

    Deliberately does NOT auto-delete. Each duplicate represents points that
    were credited to a real member; silently removing the ledger row would
    leave the cached balance overstated with no record of why. A human needs to
    decide, then re-run.
    """
    LoyaltyTransaction = apps.get_model("loyalty", "LoyaltyTransaction")

    duplicates = (
        LoyaltyTransaction.objects.filter(reversal_of__isnull=False)
        .values("reversal_of")
        .annotate(n=models.Count("id"))
        .filter(n__gt=1)
        .order_by("-n")
    )

    offenders = list(duplicates[:20])
    if not offenders:
        return

    total = duplicates.count()
    detail = ", ".join(f"txn {row['reversal_of']} x{row['n']}" for row in offenders)
    raise RuntimeError(
        f"Cannot add uniq_reversal_per_transaction: {total} transaction(s) already "
        f"have more than one reversal, which means a double-refund race has "
        f"occurred on this install.\n\n"
        f"Affected (first {len(offenders)}): {detail}\n\n"
        f"Each extra reversal credited points that were never spent. Reconcile "
        f"the affected members with LedgerService.reconcile_balance(member) "
        f"after removing the surplus reversal rows, then re-run this migration."
    )


def noop_reverse(apps, schema_editor):
    """Nothing to undo — the check writes no data."""


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty', '0004_loyaltymember_grace_period_started_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(check_for_duplicate_reversals, noop_reverse),
        migrations.AddConstraint(
            model_name='loyaltytransaction',
            constraint=models.UniqueConstraint(condition=models.Q(('reversal_of__isnull', False)), fields=('reversal_of',), name='uniq_reversal_per_transaction'),
        ),
    ]
