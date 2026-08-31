"""Recurring-campaign engine.

A recurring Campaign is a *template*: it never sends itself. At each scheduled
``next_run_at`` the beat spawns a broadcast *occurrence* — a snapshot of the
template's freshly-rendered content — and sends it. Before spawning, a freshness
gate resolves the template's delta-aware blocks against the last-send watermark;
the merchant's ``freshness_policy`` decides what happens when there's nothing new:

* ``skip``          — don't send this occurrence; advance to the next run.
* ``send_partial``  — send anyway (empty dynamic blocks just render nothing).
* ``hold``          — postpone and retry daily until fresh, up to ``hold_days``.

Occurrences are self-contained sends (rendered ``html_content`` + subject +
segment); they don't copy the template's block rows.
"""

import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django.utils import timezone

logger = logging.getLogger("email_marketing")

# How often a held schedule re-checks for fresh content.
_HOLD_RETRY = timedelta(days=1)


def _tz(name: str) -> ZoneInfo:
    try:
        return ZoneInfo(name or "UTC")
    except (ZoneInfoNotFoundError, ValueError):
        return ZoneInfo("UTC")


def _add_months(dt: datetime, months: int) -> datetime:
    """Add whole months, clamping the day to the target month's length."""
    import calendar

    month_index = dt.month - 1 + months
    year = dt.year + month_index // 12
    month = month_index % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)


def compute_next_run(schedule, after=None) -> datetime:
    """Return the next fire time (UTC-aware) strictly after ``after`` (now)."""
    tz = _tz(schedule.timezone)
    ref = (after or timezone.now()).astimezone(tz)
    t = schedule.send_time
    interval = max(1, schedule.interval or 1)

    candidate = ref.replace(hour=t.hour, minute=t.minute, second=0, microsecond=0)

    if schedule.cadence == schedule.CADENCE_DAILY:
        while candidate <= ref:
            candidate += timedelta(days=interval)

    elif schedule.cadence == schedule.CADENCE_WEEKLY:
        target = schedule.weekday if schedule.weekday is not None else ref.weekday()
        days_ahead = (target - candidate.weekday()) % 7
        candidate += timedelta(days=days_ahead)
        while candidate <= ref:
            candidate += timedelta(weeks=interval)

    else:  # monthly
        target_day = schedule.day_of_month or ref.day
        import calendar

        dom = min(target_day, calendar.monthrange(candidate.year, candidate.month)[1])
        candidate = candidate.replace(day=dom)
        while candidate <= ref:
            candidate = _add_months(candidate, interval)

    return candidate.astimezone(ZoneInfo("UTC"))


# Blocks whose "since last send" mode makes them delta-aware, mapped to the
# content flag that turns it on and the context key that carries their results.
_DELTA_AWARE = {
    "blog_posts": ("source", "since_last_send", "posts"),
    "product_grid": ("mode", "new_since_send", "products"),
}


def has_fresh_content(campaign, since) -> bool:
    """Whether the campaign's delta-aware blocks have anything new since ``since``.

    A Blog Posts block set to "New since last send", or a Product Grid set to
    "New since last send", is delta-aware. If a campaign has such blocks and none
    yields content, it's not fresh. A campaign with no delta-aware blocks is
    always considered fresh (there's nothing to gate on).
    """
    from email_marketing.block_context import get_block_context
    from email_marketing.block_registry import get_block, sanitize_content

    delta_aware = 0
    for block in campaign.blocks.all():
        spec = _DELTA_AWARE.get(block.block_type)
        if not spec:
            continue
        cfg = get_block(block.block_type)
        if not cfg:
            continue
        flag_key, flag_value, result_key = spec
        content = sanitize_content(cfg, block.content or {})
        if content.get(flag_key) == flag_value:
            delta_aware += 1
            ctx = get_block_context(block.block_type, content, {"since": since})
            if ctx.get(result_key):
                return True
    return delta_aware == 0


def spawn_occurrence(template, schedule=None):
    """Render the template now and create+send a broadcast occurrence.

    When the schedule has a per-occurrence A/B configured, the occurrence runs a
    subject-line A/B (split the audience, test, auto-send the winner) instead of a
    plain send — falling back to a plain send if the audience is too small to
    split, so the recurring campaign still goes out. Returns the occurrence
    Campaign, or None if the send could not start.
    """
    from email_marketing.models import Campaign, CampaignSchedule
    from email_marketing.services.block_serializer import serialize_campaign

    if schedule is None:
        schedule = CampaignSchedule.objects.filter(campaign=template).first()

    # Serialise the TEMPLATE's blocks now — its ``last_content_sent_at`` is the
    # "since" watermark, so a since-last-send block only renders new posts.
    mjml = serialize_campaign(template)

    occurrence = Campaign.objects.create(
        site=template.site,
        parent=template,
        campaign_type=Campaign.TYPE_BROADCAST,
        name=f"{template.name} — {timezone.now():%Y-%m-%d}",
        subject=template.subject,
        preview_text=template.preview_text,
        message_type=template.message_type,
        segment=template.segment,
        from_account=template.from_account,
        html_content=mjml,
        status=Campaign.STATUS_DRAFT,
        created_by=template.created_by,
    )

    if schedule is not None and schedule.ab_enabled:
        return _spawn_ab_occurrence(occurrence, schedule)
    return _plain_send(occurrence)


def _plain_send(occurrence):
    """Send an occurrence as an ordinary broadcast. Returns it, or None on error."""
    from email_marketing.services.campaigns import send_campaign

    result = send_campaign(occurrence)
    if result.get("error"):
        logger.error("Recurring occurrence %s failed to send: %s", occurrence.id, result)
        return None
    return occurrence


def _spawn_ab_occurrence(occurrence, schedule):
    """Run an occurrence as a subject-line A/B test, or fall back to a plain send.

    Reuses the broadcast A/B engine: create the test + variant campaigns on the
    occurrence, then start it (split the audience, send each subject to its slice,
    arm the decision). The A/B beat later picks the winner and sends it to the
    holdout. If the audience is too small to split, drop the test and send the
    occurrence normally so the recurring campaign still goes out.
    """
    from email_marketing.models import ABTest, Campaign
    from email_marketing.services import ab_testing

    setup = ab_testing.create_ab_test(
        occurrence,
        test_type=ABTest.TYPE_SUBJECT,
        variant_subjects=schedule.ab_subjects,
        sample_percent=schedule.ab_sample_percent,
        winner_metric=schedule.ab_winner_metric,
        test_window_hours=schedule.ab_test_window_hours,
        auto_send_winner=schedule.ab_auto_send_winner,
    )
    if setup.get("error"):
        logger.error("Recurring A/B occurrence %s setup failed: %s", occurrence.id, setup)
        return _plain_send(occurrence)

    test = ABTest.objects.get(campaign=occurrence)
    start = ab_testing.start_ab_test(test)
    if start.get("error"):
        # Can't A/B this occurrence (e.g. audience too small) — drop the unstarted
        # test + its variant campaigns and send the occurrence as a plain broadcast.
        logger.warning(
            "Recurring A/B occurrence %s falling back to a plain send: %s", occurrence.id, start
        )
        Campaign.objects.filter(ab_variant__ab_test=test).delete()
        test.delete()
        return _plain_send(occurrence)
    return occurrence


def run_due_schedule(schedule, now=None):
    """Process one due schedule: apply the freshness policy, then send or skip.

    Returns a short outcome dict. Advances ``next_run_at`` (and the template
    watermark on a real send) so the beat is idempotent per tick.
    """
    now = now or timezone.now()
    template = schedule.campaign
    since = template.last_content_sent_at
    fresh = has_fresh_content(template, since)
    policy = schedule.freshness_policy

    def _advance(sent: bool):
        schedule.last_run_at = now
        schedule.hold_until = None
        schedule.next_run_at = compute_next_run(schedule, now)
        fields = ["last_run_at", "hold_until", "next_run_at", "updated_at"]
        if sent:
            schedule.occurrences_sent = (schedule.occurrences_sent or 0) + 1
            fields.append("occurrences_sent")
        schedule.save(update_fields=fields)

    # Nothing new + skip → skip this occurrence entirely.
    if not fresh and policy == schedule.POLICY_SKIP:
        _advance(sent=False)
        logger.info("Recurring %s: skipped (no new content)", template.id)
        return {"outcome": "skipped"}

    # Nothing new + hold → postpone and retry, up to the hold window.
    if not fresh and policy == schedule.POLICY_HOLD:
        if schedule.hold_until is None:
            schedule.hold_until = now + timedelta(days=schedule.hold_days or 3)
        if now < schedule.hold_until:
            schedule.next_run_at = now + _HOLD_RETRY
            schedule.save(update_fields=["hold_until", "next_run_at", "updated_at"])
            return {"outcome": "held"}
        # Window elapsed → give up this occurrence, move to the next slot.
        _advance(sent=False)
        return {"outcome": "hold_expired"}

    # Fresh, or send_partial → send an occurrence.
    occurrence = spawn_occurrence(template, schedule)
    if occurrence is None:
        _advance(sent=False)
        return {"outcome": "send_failed"}

    # Advance the template watermark so the NEXT occurrence starts from here.
    template.last_content_sent_at = now
    template.save(update_fields=["last_content_sent_at", "updated_at"])
    _advance(sent=True)
    logger.info("Recurring %s: sent occurrence %s", template.id, occurrence.id)
    return {"outcome": "sent", "occurrence_id": str(occurrence.id)}
