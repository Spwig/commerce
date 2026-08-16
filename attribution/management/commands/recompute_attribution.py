"""Recompute attribution for existing orders.

The whole point of the engine: because touches are retained raw, switching the
active model (or backfilling) is a re-run, not a migration. Change
``AttributionSettings.active_model`` and run this to re-attribute history under
the new model — each order gets a fresh, forward-only batch.

Examples::

    ./manage.py recompute_attribution                 # all completed orders, idempotent
    ./manage.py recompute_attribution --force         # rewrite even if unchanged
    ./manage.py recompute_attribution --since 2026-01-01
    ./manage.py recompute_attribution --order-id 1234
"""

from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from attribution.services.resolution import resolve_order

_COMPLETED = {"completed", "complete", "delivered", "fulfilled", "refunded", "returned"}


class Command(BaseCommand):
    help = "Recompute revenue attribution for existing orders under the active model."

    def add_arguments(self, parser):
        parser.add_argument("--order-id", type=int, default=None, help="Resolve a single order.")
        parser.add_argument(
            "--since", type=str, default=None, help="Only orders created on/after YYYY-MM-DD."
        )
        parser.add_argument(
            "--force", action="store_true", help="Rewrite even if the latest batch is unchanged."
        )
        parser.add_argument(
            "--limit", type=int, default=None, help="Cap the number of orders processed."
        )

    def handle(self, *args, **opts):
        from orders.models import Order

        qs = Order.objects.all().order_by("created_at")
        if opts["order_id"]:
            qs = qs.filter(pk=opts["order_id"])
        else:
            qs = qs.filter(status__in=_COMPLETED)
        if opts["since"]:
            since = timezone.make_aware(datetime.strptime(opts["since"], "%Y-%m-%d"))
            qs = qs.filter(created_at__gte=since)
        if opts["limit"]:
            qs = qs[: opts["limit"]]

        resolved = skipped = 0
        for order in qs.iterator():
            version = resolve_order(order, force=opts["force"])
            if version:
                resolved += 1
                self.stdout.write(f"order {order.pk} -> {version}")
            else:
                skipped += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. {resolved} resolved, {skipped} skipped (no eligible touches)."
            )
        )
