"""Starter audiences — ready-made segments from the store's own app data.

Merchants shouldn't hand-build rule trees for audiences the platform already
knows. This offers one-click "starter" segments sourced from existing app
intelligence — the shop's named customer value buckets
(``customers.CustomerSegment``), the loyalty programme (membership / tier), and
the affiliate roster — expressed with the ordinary dynamic-segment rule
vocabulary (see ``services.segmentation``). They are plain dynamic segments, so
they stay live and self-updating; the merchant owns and can edit them after
seeding.

Only starters the store actually has data for are offered, so a shop with no
loyalty programme is never seeded a "loyalty members" audience.
"""

import logging

logger = logging.getLogger("email_marketing")


# --- backing-data probes (lazy imports: these apps are siblings, not deps) ----


def _present_buckets(names):
    """Return the subset of ``names`` that are active CustomerSegment buckets."""
    from customers.models import CustomerSegment

    return list(
        CustomerSegment.objects.filter(name__in=names, is_active=True)
        .order_by("-priority", "name")
        .values_list("name", flat=True)
    )


def _has_customer_metrics():
    from customers.models import CustomerMetrics

    return CustomerMetrics.objects.exists()


def _has_loyalty_members():
    from loyalty.models import LoyaltyMember

    return LoyaltyMember.objects.exists()


def _top_tier_slugs(limit=1):
    from loyalty.models import LoyaltyTier

    return list(
        LoyaltyTier.objects.filter(is_active=True)
        .order_by("rank")  # lower rank = higher tier
        .values_list("slug", flat=True)[:limit]
    )


def _has_affiliates():
    # Match the is_affiliate rule, which targets status="active". Affiliates
    # default to "pending", so a store with only pending/suspended applications
    # shouldn't be offered an "Affiliates" starter that would match nobody.
    from affiliate.models import Affiliate

    return Affiliate.objects.filter(status="active").exists()


# --- rule helpers -------------------------------------------------------------


def _rules(*conditions, match="all"):
    return {"match": match, "conditions": list(conditions)}


def _cond(field, op, value):
    return {"field": field, "op": op, "value": value}


# --- catalogue ----------------------------------------------------------------

# Named value buckets to offer, in display order: (slug, name, description, bucket names).
_BUCKET_STARTERS = [
    (
        "vip-customers",
        "VIP customers",
        "Your highest-value customers, from the shop's VIP segment.",
        ["vip"],
    ),
    (
        "high-value-customers",
        "High-value customers",
        "Top spenders — the shop's VIP and high-value segments.",
        ["vip", "high_value"],
    ),
    (
        "repeat-buyers",
        "Repeat buyers",
        "Customers who order regularly — the frequent-buyer and regular segments.",
        ["frequent_buyer", "regular"],
    ),
    (
        "new-customers",
        "New customers",
        "Customers the shop has classed as new.",
        ["new"],
    ),
]


def available_starters():
    """Starter audiences the store currently has data for, with concrete rules.

    Each entry is ``{slug, name, description, rules}``. Bucket starters reference
    only the buckets that actually exist, and each starter appears only when its
    source data is present — so nothing is offered that would resolve to nobody
    by construction.
    """
    starters = []

    # Shop value buckets (customers.CustomerSegment).
    for slug, name, description, bucket_names in _BUCKET_STARTERS:
        present = _present_buckets(bucket_names)
        if present:
            starters.append(
                {
                    "slug": slug,
                    "name": name,
                    "description": description,
                    "rules": _rules(_cond("customer_segment", "in", present)),
                }
            )

    # Recency (raw RFM). Pair with has_orders so a never-purchased account (whose
    # days-since sentinel is 0) is never swept in.
    if _has_customer_metrics():
        starters.append(
            {
                "slug": "lapsing-customers",
                "name": "Lapsing customers",
                "description": "Customers who have ordered before but not in the last 90 days.",
                "rules": _rules(
                    _cond("days_since_last_purchase", "gte", 90),
                    {"field": "has_orders", "op": "is_true"},
                ),
            }
        )

    # Loyalty.
    if _has_loyalty_members():
        starters.append(
            {
                "slug": "loyalty-members",
                "name": "Loyalty members",
                "description": "Everyone active in your loyalty programme.",
                "rules": _rules({"field": "is_loyalty_member", "op": "is_true"}),
            }
        )
        top = _top_tier_slugs()
        if top:
            starters.append(
                {
                    "slug": "top-tier-loyalty",
                    "name": "Top loyalty tier",
                    "description": "Members in your highest loyalty tier.",
                    "rules": _rules(_cond("loyalty_tier", "in", top)),
                }
            )

    # Affiliates.
    if _has_affiliates():
        starters.append(
            {
                "slug": "affiliates",
                "name": "Affiliates",
                "description": "Your active affiliate partners.",
                "rules": _rules({"field": "is_affiliate", "op": "is_true"}),
            }
        )

    return starters


def seed_starter_segments(site):
    """Create ready-made dynamic audiences from the store's own customer, loyalty
    and affiliate data.

    Idempotent: a starter whose slug already exists for the site (including one
    the merchant has since edited or removed) is left untouched, so re-running
    never duplicates or resurrects segments. Returns the created and skipped
    starter names.
    """
    from django.db import IntegrityError, transaction

    from email_marketing.models import Segment

    # Check every row (incl. soft-deleted) so a previously-removed starter isn't
    # recreated and can't collide with the (site, slug) unique constraint.
    existing = set(Segment.all_objects.filter(site=site).values_list("slug", flat=True))

    created, skipped = [], []
    for spec in available_starters():
        if spec["slug"] in existing:
            skipped.append(spec["name"])
            continue
        try:
            # Each create in its own atomic block so a lost double-submit race
            # rolls back cleanly instead of poisoning the loop's transaction.
            with transaction.atomic():
                segment = Segment.objects.create(
                    site=site,
                    name=spec["name"],
                    slug=spec["slug"],
                    description=spec["description"],
                    kind=Segment.KIND_DYNAMIC,
                    rules=spec["rules"],
                    is_active=True,
                )
        except IntegrityError:
            # A concurrent seed (double-click / two admins) already created this
            # slug — the unique constraint held; report it skipped, not a 500.
            skipped.append(spec["name"])
            continue
        segment.rebuild()
        created.append(spec["name"])

    logger.info(
        "Seeded starter audiences for site %s: %d created, %d skipped",
        site.pk,
        len(created),
        len(skipped),
    )
    return {"created": created, "skipped": skipped}
