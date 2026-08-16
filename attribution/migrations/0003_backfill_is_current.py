"""Backfill ``is_current`` so exactly one batch per order is current.

Migration 0002 added ``is_current`` with ``default=True``, which on a store
that already had more than one attribution batch per order (from a model switch
or a refund re-resolution) would mark every historical batch current — and the
reporting layer, which reads ``is_current=True``, would then double-count those
orders. A no-op ``resolve_order`` returns early and never repairs the flags, so
this must be fixed in data. Idempotent and a no-op on a fresh store.
"""

from django.db import migrations


def mark_latest_batch_current(apps, schema_editor):
    Attribution = apps.get_model("attribution", "Attribution")

    order_ids = Attribution.objects.order_by().values_list("order_id", flat=True).distinct()
    for order_id in order_ids.iterator():
        latest = (
            Attribution.objects.filter(order_id=order_id).order_by("-created_at", "-id").first()
        )
        if latest is None:
            continue
        # Newest batch current, everything older not.
        Attribution.objects.filter(order_id=order_id).exclude(
            model_version=latest.model_version
        ).update(is_current=False)
        Attribution.objects.filter(
            order_id=order_id, model_version=latest.model_version
        ).update(is_current=True)


def noop(apps, schema_editor):
    # Irreversible in a meaningful sense; leave flags as-is on reverse.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("attribution", "0002_attribution_is_current_and_more"),
    ]

    operations = [
        migrations.RunPython(mark_latest_batch_current, noop),
    ]
