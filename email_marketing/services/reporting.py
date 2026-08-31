"""Per-campaign delivery & engagement reporting.

Aggregates a campaign's ``CampaignSend`` rows (and, for an A/B parent, its variant
children) into delivery/engagement counts and rates in a single query. Bounce and
complaint data is rolled up from ``EmailEvent`` onto ``CampaignSend`` by
``signals._engagement_receiver``; opens/clicks come from the tracking pixel + click
rollup. Rates follow email-industry convention:

- delivered  = accepted by the provider and not later bounced (status SENT, not bounced)
- attempted  = delivery attempts that reached the provider (SENT + FAILED)
- open/click rates over DELIVERED; bounce rate over ATTEMPTED; complaint over DELIVERED

so a rate can never exceed 100% or go negative regardless of the sync-reject vs
async-bounce status path.
"""

from datetime import timedelta

from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from django.utils import timezone


def _rate(numerator, denominator):
    return round(100 * numerator / denominator, 1) if denominator else 0.0


def daily_counts(qs, date_field, since, days):
    """(labels, counts): a zero-filled per-day count over a trailing window.

    Buckets ``qs`` by ``TruncDate(date_field)`` from ``since`` for ``days`` days and
    densifies gaps to 0 so every day in the window has a bar. Shared by the dashboard
    trends and the per-campaign time-series.
    """
    rows = (
        qs.filter(**{f"{date_field}__gte": since})
        .annotate(day=TruncDate(date_field))
        .values("day")
        .annotate(n=Count("id"))
    )
    by_day = {r["day"]: r["n"] for r in rows if r["day"]}
    start = since.date()
    labels, counts = [], []
    for i in range(days):
        d = start + timedelta(days=i)
        labels.append(d.strftime("%d %b"))
        counts.append(by_day.get(d, 0))
    return labels, counts


def _scope_ids(campaign):
    """This campaign plus its direct children (one level, via ``Campaign.parent``).

    ``parent`` is the shared "spawned-from" link: an A/B parent's buckets are variant
    child campaigns (plus the winner-send holdout child), and a recurring template's
    occurrences are children too. So a report on an A/B parent covers the whole test,
    and a report on a recurring template covers all its occurrences (lifetime). A
    plain broadcast has no children and reports on itself alone.

    Limitation: only one level is walked. A recurring template whose *occurrences*
    are themselves A/B tests would not roll up the occurrences' variant grandchildren.
    """
    from email_marketing.models import Campaign

    ids = [campaign.id]
    ids += list(Campaign.objects.filter(parent_id=campaign.id).values_list("id", flat=True))
    return ids


def campaign_report(campaign):
    """Delivery + engagement metrics for one campaign (counts + rates).

    Returns a flat dict suitable for a template or JSON payload.
    """
    from email_marketing.models import CampaignSend

    # Engagement is measured on DELIVERED mail: scope opened/clicked to the same
    # population as the rate denominator so a numerator can never exceed it (an open
    # on a send that later bounced, or one recorded against a non-SENT row, would
    # otherwise push open_rate past 100%).
    delivered_q = Q(status=CampaignSend.STATUS_SENT, bounced=False)

    # Aggregate aliases are suffixed ``_n`` so they don't shadow the model field
    # names referenced in each filter (Django would otherwise read e.g. ``bounced``
    # as the aggregate, not the column).
    agg = CampaignSend.objects.filter(campaign_id__in=_scope_ids(campaign)).aggregate(
        recipients_n=Count("id"),
        sent_n=Count("id", filter=Q(status=CampaignSend.STATUS_SENT)),
        failed_n=Count("id", filter=Q(status=CampaignSend.STATUS_FAILED)),
        skipped_n=Count("id", filter=Q(status=CampaignSend.STATUS_SKIPPED)),
        skipped_suppressed_n=Count(
            "id", filter=Q(status=CampaignSend.STATUS_SKIPPED, skip_reason="suppressed")
        ),
        delivered_n=Count("id", filter=delivered_q),
        opened_n=Count("id", filter=delivered_q & Q(opened=True)),
        clicked_n=Count("id", filter=delivered_q & Q(clicked=True)),
        bounced_n=Count("id", filter=Q(bounced=True)),
        hard_bounced_n=Count("id", filter=Q(bounced=True, bounce_type="hard")),
        soft_bounced_n=Count("id", filter=Q(bounced=True, bounce_type="soft")),
        complained_n=Count("id", filter=Q(complained=True)),
    )
    sent = agg["sent_n"]
    failed = agg["failed_n"]
    delivered = agg["delivered_n"]
    attempted = sent + failed
    opened = agg["opened_n"]
    bounced = agg["bounced_n"]
    complained = agg["complained_n"]
    return {
        "recipients": agg["recipients_n"],
        "sent": sent,
        "failed": failed,
        "skipped": agg["skipped_n"],
        "skipped_suppressed": agg["skipped_suppressed_n"],
        "delivered": delivered,
        "attempted": attempted,
        "opened": opened,
        "clicked": agg["clicked_n"],
        "bounced": bounced,
        "hard_bounced": agg["hard_bounced_n"],
        "soft_bounced": agg["soft_bounced_n"],
        "complained": complained,
        "delivery_rate": _rate(delivered, attempted),
        "open_rate": _rate(opened, delivered),
        "click_rate": _rate(agg["clicked_n"], delivered),
        "click_to_open_rate": _rate(agg["clicked_n"], opened),
        "bounce_rate": _rate(bounced, attempted),
        "complaint_rate": _rate(complained, delivered),
    }


def campaign_revenue(campaign):
    """Attributed revenue for a campaign (+ its A/B / recurring children) with ROAS.

    Reads the multi-touch attribution engine by the campaigns' ``attribution_slug``
    values (each child is its own attribution.Campaign). Revenue is all-time
    attributed net in the store's base currency; ``revenue_per_email`` divides by
    delivered sends; ``roas`` divides by ``campaign.spend`` when set (assumed in the
    base currency — email spend is rare and single-store). Returns zeros / ``roas``
    None when nothing is attributed yet or no spend is recorded.
    """
    from decimal import Decimal

    from attribution.services import reporting as attribution_reporting
    from email_marketing.models import Campaign, CampaignSend

    ids = _scope_ids(campaign)
    slugs = list(
        Campaign.objects.filter(id__in=ids)
        .exclude(attribution_slug="")
        .values_list("attribution_slug", flat=True)
    )
    data = attribution_reporting.campaign_revenue(slugs)
    revenue = data["revenue"]

    delivered = CampaignSend.objects.filter(
        campaign_id__in=ids, status=CampaignSend.STATUS_SENT, bounced=False
    ).count()
    revenue_per_email = (
        (revenue / delivered).quantize(Decimal("0.01")) if delivered else Decimal("0.00")
    )

    # ROAS only when spend is recorded in the SAME currency as the (base-currency)
    # attributed revenue — otherwise dividing base-currency revenue by a raw foreign
    # amount yields a silently-wrong multiplier. A mismatched currency simply shows no
    # ROAS rather than a misleading one (FX conversion of spend is a future enhancement).
    roas = None
    spend = campaign.spend
    if spend is not None and spend.amount and spend.amount > 0:
        from core.models import SiteSettings

        base_ccy = SiteSettings.get_settings().default_currency or "USD"
        if str(spend.currency) == base_ccy:
            roas = (revenue / spend.amount).quantize(Decimal("0.01"))

    return {
        "revenue": revenue,
        "orders": data["orders"],
        "aov": data["aov"],
        "revenue_per_email": revenue_per_email,
        "roas": roas,
        "spend": spend,
    }


def campaign_timeseries(campaign, days=30):
    """Per-day sends / unique opens / unique clicks for the report chart.

    Returns ``{labels, sends, opens, clicks}``. Opens and clicks are counted from the
    per-recipient ``opened_at`` / ``clicked_at`` rollup timestamps, i.e. **unique per
    recipient** (first open / first click) — the standard "unique engagement over time"
    metric. Repeat opens aren't available (the open pixel is deduped to one EmailEvent
    per email in ``email_system/views/tracking.py``).

    Window: a trailing ``days``-day window ending today, starting no earlier than the
    campaign's first send. Empty series when the campaign has no sends yet. Scoped with
    ``_scope_ids`` so an A/B parent / recurring template rolls up its children.
    """
    from email_marketing.models import CampaignSend

    empty = {"labels": [], "sends": [], "opens": [], "clicks": []}
    scope = CampaignSend.objects.filter(campaign_id__in=_scope_ids(campaign))

    # Same populations as campaign_report(): the "sent" line counts only STATUS_SENT
    # rows (CampaignSend rows are created before delivery, so pending/queued/skipped/
    # failed rows must not read as sent), and opens/clicks are scoped to DELIVERED
    # (sent and not later bounced) so a series can't exceed the sent line.
    sent_qs = scope.filter(status=CampaignSend.STATUS_SENT)
    delivered_q = Q(status=CampaignSend.STATUS_SENT, bounced=False)

    first = sent_qs.order_by("created_at").values_list("created_at", flat=True).first()
    if first is None:
        return empty

    now = timezone.now()
    since = max(first, now - timedelta(days=days - 1))
    win_days = (now.date() - since.date()).days + 1

    labels, sends_c = daily_counts(sent_qs, "created_at", since, win_days)
    _, opens_c = daily_counts(scope.filter(delivered_q, opened=True), "opened_at", since, win_days)
    _, clicks_c = daily_counts(
        scope.filter(delivered_q, clicked=True), "clicked_at", since, win_days
    )
    return {"labels": labels, "sends": sends_c, "opens": opens_c, "clicks": clicks_c}


def campaign_link_clicks(campaign, limit=20):
    """The most-clicked links in a campaign — the link-level click map.

    Returns ``[{url, clicks, unique_clickers, ctr}]`` ordered by total clicks desc,
    top ``limit``. The clicked destination URL is only recorded on the click
    ``EmailEvent`` (``event_data["url"]`` — see ``email_system/views/tracking.py``);
    it is discarded at the CampaignSend rollup, so this queries EmailEvent directly,
    joining event → outbox → campaign_send → campaign. Scoped via ``_scope_ids``.

    ``ctr`` is unique clickers over DELIVERED (the same denominator as the report's
    click rate). ``clicks`` counts distinct events (the reverse ``campaign_send`` join
    can't inflate it). The ``event_data`` JSON key isn't indexed, so this is a bounded
    scan capped at ``limit`` — fine for a single-store install; a rollup column / GIN
    index is the optimisation if send volume ever demands it.
    """
    from email_marketing.models import CampaignSend
    from email_system.models import EmailEvent

    scope = _scope_ids(campaign)
    delivered = CampaignSend.objects.filter(
        campaign_id__in=scope, status=CampaignSend.STATUS_SENT, bounced=False
    ).count()

    # Restrict to clicks on DELIVERED sends (sent, not later bounced) — the same
    # population as campaign_report's click rate — so the table can't show clicks
    # excluded from the headline metrics, and CTR can't exceed 100%.
    rows = (
        EmailEvent.objects.filter(
            event_type="clicked",
            email__campaign_send__campaign_id__in=scope,
            email__campaign_send__status=CampaignSend.STATUS_SENT,
            email__campaign_send__bounced=False,
        )
        .exclude(event_data__url__isnull=True)
        .exclude(event_data__url="")
        .values("event_data__url")
        .annotate(
            clicks=Count("id", distinct=True),
            # Distinct delivered SENDS (not subscribers): the denominator is per-send,
            # so a recurring rollup where one subscriber clicks across occurrences
            # counts each occurrence — keeping CTR on the same basis as click_rate.
            unique_clickers=Count("email__campaign_send", distinct=True),
        )
        .order_by("-clicks")[:limit]
    )
    return [
        {
            "url": r["event_data__url"],
            "clicks": r["clicks"],
            "unique_clickers": r["unique_clickers"],
            "ctr": _rate(r["unique_clickers"], delivered),
        }
        for r in rows
    ]


# ---------------------------------------------------------------------------
# Journey-level reporting (revenue + enrollment funnel).
#
# A journey has no CampaignSend rows and its A/B arms live in node config (not
# Campaign.parent), so the campaign helpers/_scope_ids don't apply. Revenue is
# gathered from the attribution slugs of the campaigns its send nodes reference.
# ---------------------------------------------------------------------------


def _is_uuid(value):
    import uuid

    try:
        uuid.UUID(str(value))
        return True
    except (ValueError, TypeError, AttributeError):
        return False


def _journey_node_campaign_ids(node):
    """Campaign ids one send node references: its campaign + content-A/B arms.

    A content A/B node's arms are separate campaigns (``variant_campaign_ids``); a
    subject A/B node has a single ``campaign_id`` (its ``ab_variant_values`` are
    subject strings, not ids), so only ``content`` tests contribute extra ids.

    Node config is a JSONField a staffer (or an import) can hand-shape, so ids are
    validated as UUIDs and non-parseable values dropped — a malformed config yields a
    campaign-less step rather than a 500 when the value reaches ``filter(id__in=…)``.
    """
    cfg = node.config or {}
    ids = []
    if cfg.get("campaign_id"):
        ids.append(cfg["campaign_id"])
    if cfg.get("ab_test_type") == "content":
        ids.extend(v for v in (cfg.get("variant_campaign_ids") or []) if v)
    return list(dict.fromkeys(cid for cid in ids if _is_uuid(cid)))  # de-dup, valid ids only


def _slugs_for_campaign_ids(ids):
    from email_marketing.models import Campaign

    if not ids:
        return []
    return list(
        Campaign.objects.filter(id__in=ids)
        .exclude(attribution_slug="")
        .values_list("attribution_slug", flat=True)
    )


def journey_funnel(journey):
    """Enrollment funnel counts for a journey: enrolled / active / completed / cancelled."""
    from email_marketing.models import JourneyEnrollment

    agg = JourneyEnrollment.objects.filter(journey=journey).aggregate(
        enrolled=Count("id"),
        active=Count("id", filter=Q(status=JourneyEnrollment.STATUS_ACTIVE)),
        completed=Count("id", filter=Q(status=JourneyEnrollment.STATUS_COMPLETED)),
        cancelled=Count("id", filter=Q(status=JourneyEnrollment.STATUS_CANCELLED)),
    )
    return {k: (agg[k] or 0) for k in ("enrolled", "active", "completed", "cancelled")}


def journey_revenue(journey):
    """Attributed revenue for a journey: total + per send-step, with per-enrollee.

    Journey-driven clicks attribute to each step-campaign's slug (stamped at send).
    The journey total sums attributed revenue across ALL its send-node campaign slugs;
    ``steps`` breaks it down per send node so a merchant sees which step earns. No ROAS
    (an ongoing automation has no single spend) — ``revenue_per_enrollee`` is the
    efficiency metric. Each step's ``engagement`` (sent / opened / clicked) is rolled up
    from JourneyStepSend, now recorded for every send, so it's available for A/B and
    plain steps alike (zero until sends occur).
    """
    from decimal import Decimal

    from attribution.services import reporting as attribution_reporting
    from email_marketing.models import Campaign, JourneyNode, JourneyStepSend

    send_nodes = list(
        journey.nodes.filter(node_type=JourneyNode.TYPE_SEND_EMAIL).order_by("pos_y", "created_at")
    )
    # Batch the step-campaign names in one query for labels. Keys are normalised to
    # str because node config stores campaign ids as strings (values_list gives UUIDs).
    all_ids = [cid for node in send_nodes for cid in _journey_node_campaign_ids(node)]
    names = {
        str(k): v for k, v in Campaign.objects.filter(id__in=all_ids).values_list("id", "name")
    }

    steps = []
    all_slugs = []
    for node in send_nodes:
        ids = _journey_node_campaign_ids(node)
        slugs = _slugs_for_campaign_ids(ids)
        all_slugs.extend(slugs)
        rev = attribution_reporting.campaign_revenue(slugs)
        primary = (node.config or {}).get("campaign_id") or (ids[0] if ids else None)
        # Per-step engagement rolls up from JourneyStepSend (recorded for every send),
        # so it's available for plain and A/B steps alike.
        engagement = JourneyStepSend.objects.filter(node=node).aggregate(
            sent=Count("id"),
            opened=Count("id", filter=Q(opened=True)),
            clicked=Count("id", filter=Q(clicked=True)),
        )
        steps.append(
            {
                "node_id": str(node.id),
                # None when the step's campaign has no name yet; the template shows a
                # translated "Email step" fallback (service stays i18n-free like campaign_report).
                "label": names.get(primary) or "",
                "revenue": rev["revenue"],
                "orders": rev["orders"],
                "ab": node.is_ab_send,
                "engagement": engagement,
            }
        )

    total = attribution_reporting.campaign_revenue(list(dict.fromkeys(all_slugs)))
    enrolled = journey_funnel(journey)["enrolled"]
    per_enrollee = (
        (total["revenue"] / enrolled).quantize(Decimal("0.01")) if enrolled else Decimal("0.00")
    )
    return {
        "revenue": total["revenue"],
        "orders": total["orders"],
        "aov": total["aov"],
        "revenue_per_enrollee": per_enrollee,
        "steps": steps,
    }
