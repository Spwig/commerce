"""Segment resolution — turn saved rules into a Subscriber queryset.

Dynamic segments compile their rule tree into ORM filters (joining
``customers.CustomerMetrics`` for spend/order rules) so membership is resolved
with a single query rather than a per-user Python loop. Static segments return
their explicit membership.

Rule tree shape::

    {
        "match": "all",            # "all" (AND) or "any" (OR)
        "conditions": [
            {"field": "has_orders",   "op": "is_true"},
            {"field": "total_spent",  "op": "gte", "value": 100},
            {"field": "joined_after", "op": "gte", "value": "2026-01-01"},
            {"field": "language",     "op": "eq",  "value": "en"},
        ],
    }
"""

import logging
from decimal import Decimal, InvalidOperation

from django.db.models import Q
from django.utils import timezone

logger = logging.getLogger("email_marketing")

# Map a rule field to the ORM lookup path it filters on. Everything reachable
# from ``Subscriber.user`` (customer metrics, loyalty, affiliate) joins through
# that FK, so these cohorts resolve as one query alongside the subscriber's own
# fields — no materialised membership.
_FIELD_LOOKUPS = {
    "total_spent": "user__customer_metrics__total_spent",
    "total_orders": "user__customer_metrics__completed_orders",
    "lifetime_value": "user__customer_metrics__lifetime_value",
    "average_order_value": "user__customer_metrics__average_order_value",
    "days_since_last_purchase": "user__customer_metrics__days_since_last_purchase",
    "loyalty_points": "user__loyalty_member__balance__available_points",
    "loyalty_tier": "user__loyalty_member__current_tier__slug",
    "language": "language_code",
    "joined_after": "created_at",
    "source": "source",
    "has_tag": "tags__slug",
}

# Operators a rule may use. Deliberately excludes regex/iregex (ReDoS) and any
# lookup that isn't needed, so a crafted rule blob can't build a pathological or
# invalid ORM lookup.
_ALLOWED_OPS = {"eq", "gte", "lte", "gt", "lt", "in", "icontains"}
# Cap membership lists so an "in" rule can't be used to build a huge query.
_MAX_IN_VALUES = 500

# Rule fields whose value is a numeric threshold: coerced to Decimal, and a bare
# threshold (no operator) means ">=" by convention.
_NUMERIC_FIELDS = {
    "total_spent",
    "total_orders",
    "lifetime_value",
    "average_order_value",
    "days_since_last_purchase",
    "loyalty_points",
}

# Human labels for the operators the rule-builder offers.
OPERATOR_LABELS = {
    "gte": "is at least",
    "lte": "is at most",
    "gt": "is more than",
    "lt": "is less than",
    "eq": "is",
    "in": "is any of",
    "is_true": "is true",
}


def available_rule_fields() -> list[dict]:
    """Field/operator/value schema for the segment rule-builder UI.

    The single source of truth the JS uses to render condition rows, kept in
    step with ``_condition_to_q`` so the builder can only compose rules the
    resolver understands.
    """
    from django.conf import settings

    languages = [{"value": code, "label": name} for code, name in settings.LANGUAGES]
    sources = [
        {"value": "signup", "label": "Storefront signup"},
        {"value": "import", "label": "Import"},
        {"value": "order", "label": "Order"},
        {"value": "manual", "label": "Added manually"},
        {"value": "api", "label": "API"},
    ]
    num_ops = ["gte", "lte", "gt", "lt"]
    fields = [
        {"key": "total_spent", "label": "Total spent", "type": "number", "operators": num_ops},
        {
            "key": "total_orders",
            "label": "Number of orders",
            "type": "number",
            "operators": num_ops,
        },
        {
            "key": "lifetime_value",
            "label": "Lifetime value",
            "type": "number",
            "operators": num_ops,
        },
        {
            "key": "average_order_value",
            "label": "Average order value",
            "type": "number",
            "operators": num_ops,
        },
        {
            "key": "days_since_last_purchase",
            "label": "Days since last order",
            "type": "number",
            "operators": num_ops,
        },
        {"key": "has_orders", "label": "Has ordered", "type": "boolean", "operators": ["is_true"]},
        {
            "key": "opted_into_marketing",
            "label": "Opted into marketing",
            "type": "boolean",
            "operators": ["is_true"],
        },
        {
            "key": "language",
            "label": "Language",
            "type": "select",
            "operators": ["eq", "in"],
            "options": languages,
        },
        {
            "key": "source",
            "label": "Source",
            "type": "select",
            "operators": ["eq", "in"],
            "options": sources,
        },
        {"key": "joined_after", "label": "Joined after", "type": "date", "operators": ["gte"]},
    ]

    # Offer a "has tag" condition only when the merchant has defined some tags,
    # so the rule isn't a dead control on a fresh install.
    from email_marketing.models import SubscriberTag

    tags = [
        {"value": t.slug, "label": t.name}
        for t in SubscriberTag.objects.order_by("name").only("slug", "name")
    ]
    if tags:
        fields.append(
            {
                "key": "has_tag",
                "label": "Has tag",
                "type": "select",
                "operators": ["eq", "in"],
                "options": tags,
            }
        )

    # Shop value buckets — target the merchant's own named RFM segments by name
    # (VIP / At-risk / Lapsed …). Shown only once buckets have been configured,
    # so the control isn't dead on a fresh install (same rule as "has tag").
    from customers.models import CustomerSegment

    buckets = [
        {"value": s.name, "label": s.display_name}
        for s in CustomerSegment.objects.filter(is_active=True).order_by("-priority", "name")
    ]
    if buckets:
        fields.append(
            {
                "key": "customer_segment",
                "label": "Customer segment",
                "type": "select",
                "operators": ["eq", "in"],
                "options": buckets,
            }
        )

    # Loyalty — membership / points / tier, shown only when a programme exists.
    from loyalty.models import LoyaltyMember, LoyaltyTier

    if LoyaltyMember.objects.exists():
        fields.append(
            {
                "key": "is_loyalty_member",
                "label": "Loyalty member",
                "type": "boolean",
                "operators": ["is_true"],
            }
        )
        fields.append(
            {
                "key": "loyalty_points",
                "label": "Loyalty points",
                "type": "number",
                "operators": num_ops,
            }
        )
    tiers = [
        {"value": t.slug, "label": t.name}
        for t in LoyaltyTier.objects.filter(is_active=True).order_by("rank")
    ]
    if tiers:
        fields.append(
            {
                "key": "loyalty_tier",
                "label": "Loyalty tier",
                "type": "select",
                "operators": ["eq", "in"],
                "options": tiers,
            }
        )

    # Affiliates — shown only when the store has an *active* affiliate. The
    # is_affiliate rule matches status="active", and affiliates default to
    # "pending", so exists() alone could offer a field that matches nobody.
    from affiliate.models import Affiliate

    if Affiliate.objects.filter(status="active").exists():
        fields.append(
            {
                "key": "is_affiliate",
                "label": "Affiliate",
                "type": "boolean",
                "operators": ["is_true"],
            }
        )

    return fields


def _condition_to_q(condition: dict) -> Q | None:
    """Translate a single rule condition into a Q object (or None to skip)."""
    field = condition.get("field")
    op = condition.get("op")
    value = condition.get("value")

    if field == "has_orders":
        # Only registered subscribers with at least one completed order.
        return Q(user__customer_metrics__completed_orders__gt=0)

    if field == "is_loyalty_member":
        # Active members of the loyalty programme. Anonymous leads and
        # non-members correctly never match a loyalty audience.
        return Q(user__loyalty_member__is_active=True)

    if field == "is_affiliate":
        # Subscribers who are active affiliates.
        return Q(user__affiliate_profile__status="active")

    if field == "customer_segment":
        # Target the shop's own named value buckets (VIP / At-risk / Lapsed …),
        # compiled live from the merchant's CustomerSegment thresholds.
        return _customer_segment_q(op, value)

    if field == "opted_into_marketing":
        # Registered users whose preference allows marketing, OR anonymous
        # subscribers who opted in. Consent is re-checked at send time; this is
        # only a coarse pre-filter to keep audiences honest.
        return Q(user__communication_preferences__email_marketing=True) | Q(
            user__isnull=True, marketing_opt_in=True
        )

    lookup = _FIELD_LOOKUPS.get(field)
    if not lookup:
        logger.warning("Unknown segment rule field: %s", field)
        return None

    # Whitelist the operator so a crafted rule can't build a pathological lookup.
    op = op or "eq"
    if op not in _ALLOWED_OPS:
        logger.warning("Disallowed segment rule op: %s", op)
        return None

    if op == "in":
        if not isinstance(value, (list, tuple)) or len(value) > _MAX_IN_VALUES:
            logger.warning("Invalid 'in' value for %s (len/type)", field)
            return None

    if field in _NUMERIC_FIELDS:
        try:
            value = Decimal(str(value))
        except (InvalidOperation, TypeError):
            logger.warning("Invalid numeric value for %s: %r", field, value)
            return None
        # A bare numeric threshold means ">=" by convention.
        if condition.get("op") is None:
            op = "gte"

    # "eq" maps to an exact match (Django has no "__eq" lookup).
    if op == "eq":
        return Q(**{lookup: value})
    return Q(**{f"{lookup}__{op}": value})


def _bucket_criteria_q(seg) -> Q | None:
    """Compile one CustomerSegment's thresholds into subscriber filters.

    Follows ``customers.CustomerSegment.matches_user`` (>= min / <= max on spend,
    orders and recency). One deliberate divergence: spend bounds compare the raw
    amount (``Money.amount``) in a single ORM query, whereas ``matches_user``
    FX-converts the threshold into each customer's currency in Python. The two
    therefore agree exactly for single-currency stores; on a multi-currency store
    a bucket's spend bound is applied without conversion — the same limitation the
    plain ``total_spent`` rule already has. Returns None when the bucket defines no
    criteria (the caller treats that as "no match", never "match everyone").
    """
    clauses = Q()
    added = False
    if seg.min_total_spent:
        clauses &= Q(user__customer_metrics__total_spent__gte=seg.min_total_spent.amount)
        added = True
    if seg.max_total_spent:
        clauses &= Q(user__customer_metrics__total_spent__lte=seg.max_total_spent.amount)
        added = True
    if seg.min_orders:
        clauses &= Q(user__customer_metrics__completed_orders__gte=seg.min_orders)
        added = True
    if seg.max_orders:
        clauses &= Q(user__customer_metrics__completed_orders__lte=seg.max_orders)
        added = True
    if seg.min_days_since_last_purchase:
        clauses &= Q(
            user__customer_metrics__days_since_last_purchase__gte=seg.min_days_since_last_purchase
        )
        added = True
    if seg.max_days_since_last_purchase:
        clauses &= Q(
            user__customer_metrics__days_since_last_purchase__lte=seg.max_days_since_last_purchase
        )
        added = True
    return clauses if added else None


def _customer_segment_q(op, value) -> Q:
    """Translate a ``customer_segment`` rule into a Subscriber filter.

    Accepts a bucket name ("vip") or, with ``in``, a list of names, and ORs the
    compiled criteria of each matching active ``CustomerSegment``.

    Fails **closed**: if the rule names a bucket that has been deleted,
    deactivated, or carries no criteria, this returns an always-false predicate
    (match nobody) rather than dropping the condition. Dropping it would let a
    stale "VIP customers" segment fall back to the whole active base and blast
    every subscriber — the opposite of intent — so an unresolvable bucket matches
    no one.
    """
    # Always-false predicate: OR-identity (drops out of an "any" match) and
    # AND-annihilator (collapses an "all" match to nobody).
    no_match = Q(pk__in=[])

    op = op or "eq"
    if op == "in":
        names = list(value) if isinstance(value, (list, tuple)) else []
    elif op == "eq":
        names = [value]
    else:
        logger.warning("Disallowed op for customer_segment: %s", op)
        return no_match

    names = [n for n in names if isinstance(n, str)][:_MAX_IN_VALUES]
    if not names:
        logger.warning("No valid customer_segment names in rule")
        return no_match

    from customers.models import CustomerSegment

    combined = Q()
    matched = False
    for seg in CustomerSegment.objects.filter(name__in=names, is_active=True):
        bucket_q = _bucket_criteria_q(seg)
        if bucket_q is not None:
            combined |= bucket_q
            matched = True
    if not matched:
        logger.warning("No active CustomerSegment with criteria matched: %s", names)
        return no_match
    return combined


def resolve_segment(segment):
    """Return the active Subscriber queryset a segment currently targets.

    Static segments return their explicit, active membership. Dynamic segments
    compile ``segment.rules`` into ORM filters. Both are scoped to the segment's
    site and to active subscribers.
    """
    from email_marketing.models import Subscriber

    base = Subscriber.objects.filter(site=segment.site, status=Subscriber.STATUS_ACTIVE)

    if segment.kind == segment.KIND_STATIC:
        return base.filter(segments=segment).distinct()

    rules = segment.rules or {}
    conditions = rules.get("conditions") or []
    if not conditions:
        # No rules at all = "every active subscriber" by design (e.g. an
        # "All subscribers" segment).
        return base

    q_objects = [q for c in conditions if (q := _condition_to_q(c)) is not None]
    if not q_objects:
        # Conditions WERE specified but none compiled (unknown field, stale
        # bucket, invalid value). A broken audience rule must fail closed —
        # under-send rather than silently blast the whole active base.
        return base.none()

    if rules.get("match") == "any":
        combined = Q()
        for q in q_objects:
            combined |= q
    else:
        combined = Q()
        for q in q_objects:
            combined &= q

    return base.filter(combined).distinct()


def build_segment(segment):
    """Recompute and cache a segment's member count. Returns the count."""
    count = resolve_segment(segment).count()
    segment.cached_count = count
    segment.last_built_at = timezone.now()
    segment.save(update_fields=["cached_count", "last_built_at", "updated_at"])
    logger.info("Rebuilt segment '%s' (%s): %d members", segment.name, segment.id, count)
    return count
