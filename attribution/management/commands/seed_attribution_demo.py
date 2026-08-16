"""Seed realistic revenue-attribution demo data on a test/demo store.

Creates real customers, multi-touch touch streams, and orders, then runs them
through the **actual resolver** — so the dashboard shows genuine engine output,
exactly what a live store (or the demo fleet's order-generating cron) produces
as orders complete. Channels are biased the way real journeys are (discovery
channels tend to be first-touch, closers last-touch), so flipping the
attribution model visibly reshuffles credit.

Everything is clearly marked and removable:
  ./manage.py seed_attribution_demo            # clears prior demo data, seeds fresh
  ./manage.py seed_attribution_demo --orders 120 --days 60
  ./manage.py seed_attribution_demo --clear    # remove all demo data, seed nothing

Safe on a shared dev DB: orders are bulk-created (no order-completion signals
fire — no demo emails, no stock changes); only Attribution is produced, via the
real resolve_order.
"""

import random
import uuid
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from attribution.models import Attribution, Campaign, TouchPoint
from attribution.services.resolution import resolve_order

User = get_user_model()

# Markers so demo data is always identifiable + removable.
USER_PREFIX = "attrdemo_"
EMAIL_DOMAIN = "demo.spwig.test"
ORDER_PREFIX = "ATTRDEMO-"
VISITOR_PREFIX = "attrdemo:"
CAMPAIGN_PREFIX = "attrdemo-"

DISCOVERY = ["organic_search", "paid_social", "organic_social"]
MID = ["paid_search", "affiliate", "referral"]
CLOSERS = ["email", "campaign", "direct"]

DEMO_CAMPAIGNS = [
    ("attrdemo-spring-refresh", "Spring Refresh"),
    ("attrdemo-influencer-maya", "Influencer · Maya K."),
    ("attrdemo-back-in-stock", "Back in Stock"),
    ("attrdemo-newsletter-aug", "August Newsletter"),
]


class Command(BaseCommand):
    help = "Seed realistic revenue-attribution demo data (resolved through the real engine)."

    def add_arguments(self, parser):
        parser.add_argument("--orders", type=int, default=80, help="Number of demo orders.")
        parser.add_argument(
            "--days", type=int, default=45, help="Spread orders over this many days."
        )
        parser.add_argument("--clear", action="store_true", help="Remove all demo data and exit.")
        parser.add_argument("--seed", type=int, default=20260813, help="RNG seed (reproducible).")

    def handle(self, *args, **opts):
        cleared = self._clear()
        if opts["clear"]:
            self.stdout.write(self.style.SUCCESS(f"Cleared demo data ({cleared})."))
            return

        rng = random.Random(opts["seed"])
        base_currency = self._base_currency()
        campaigns = self._ensure_campaigns()
        n_orders = opts["orders"]
        days = opts["days"]
        now = timezone.now()

        created_orders = 0
        with transaction.atomic():
            for i in range(n_orders):
                user = User.objects.create_user(
                    username=f"{USER_PREFIX}{i}_{uuid.uuid4().hex[:6]}",
                    email=f"attrdemo+{i}@{EMAIL_DOMAIN}",
                    password="demo-not-a-login",
                    first_name="Demo",
                    last_name=f"Buyer {i}",
                )
                order_dt = now - timedelta(days=rng.uniform(0, days), hours=rng.uniform(0, 23))
                self._make_touches(user, order_dt, campaigns, rng)

                total = Decimal(str(rng.choice([29, 39, 49, 59, 79, 89, 120, 150, 220, 340])))
                refunded = (
                    (total * Decimal("0.4")).quantize(Decimal("0.01"))
                    if rng.random() < 0.08
                    else Decimal("0.00")
                )
                order = self._make_order(user, order_dt, total, refunded, base_currency)
                resolve_order(order)
                created_orders += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {created_orders} demo orders over {days} days "
                f"({base_currency}). Open /admin/insights/attribution/."
            )
        )

    # ---- helpers ----

    def _base_currency(self):
        try:
            from core.models import SiteSettings

            return SiteSettings.get_settings().default_currency or "USD"
        except Exception:
            return "USD"

    def _ensure_campaigns(self):
        out = []
        for slug, name in DEMO_CAMPAIGNS:
            c, _ = Campaign.objects.get_or_create(slug=slug, defaults={"name": name})
            out.append(c)
        return out

    def _make_touches(self, user, order_dt, campaigns, rng):
        """A biased multi-touch journey, backdated before the order."""
        # ~15% of orders are pure direct (no recorded touch).
        if rng.random() < 0.15:
            return
        n = rng.choice([1, 2, 2, 3, 3, 4])
        chans = []
        for p in range(n):
            if p == 0:
                pool = DISCOVERY if rng.random() < 0.8 else MID
            elif p == n - 1:
                pool = CLOSERS if rng.random() < 0.78 else MID
            else:
                pool = rng.choice([DISCOVERY, MID, CLOSERS])
            c = rng.choice(pool)
            if chans and chans[-1] == c:
                c = rng.choice(pool)
            chans.append(c)

        # spread touches across up to ~18 days before the order, oldest first
        span = min(18.0, max(1.0, (n - 1) * 4.0))
        offsets = sorted((rng.uniform(0.05, span) for _ in range(n)), reverse=True)
        for c, off in zip(chans, offsets, strict=True):
            campaign_ref = None
            if c in ("email", "campaign") and rng.random() < 0.6:
                campaign_ref = rng.choice(campaigns)
            tp = TouchPoint.objects.create(
                visitor_key=f"{VISITOR_PREFIX}{uuid.uuid4().hex}",
                customer=user,
                channel=c,
                medium=c,
                campaign_ref=campaign_ref,
                consent_state="granted",
            )
            TouchPoint.objects.filter(pk=tp.pk).update(occurred_at=order_dt - timedelta(days=off))

    def _make_order(self, user, order_dt, total, refunded, currency):
        from orders.models import Order

        order = Order(
            user=user,
            order_number=f"{ORDER_PREFIX}{uuid.uuid4().hex[:12].upper()}",
            email=user.email,
            status="completed",
            payment_status="paid",
            channel="web",
            subtotal=total,
            subtotal_currency=currency,
            total_amount=total,
            total_amount_currency=currency,
            amount_refunded=refunded,
            amount_refunded_currency=currency,
            created_at=order_dt,
        )
        # bulk_create skips post_save side-effects (emails/stock); we only want
        # the attribution, produced by resolve_order below.
        Order.objects.bulk_create([order])
        return order

    def _clear(self):
        from orders.models import Order

        orders = Order.objects.filter(order_number__startswith=ORDER_PREFIX)
        n_orders = orders.count()
        orders.delete()  # cascades Attribution
        n_touch = TouchPoint.objects.filter(visitor_key__startswith=VISITOR_PREFIX).delete()[0]
        Campaign.objects.filter(slug__startswith=CAMPAIGN_PREFIX).delete()
        n_users = User.objects.filter(username__startswith=USER_PREFIX).delete()[0]
        # Any orphaned demo attribution (defensive; should already be cascaded).
        Attribution.objects.filter(order__isnull=True, channel="").delete()
        return f"{n_orders} orders, {n_touch} touches, {n_users} users"
