"""A/B testing engine — bucket the audience, send variants, decide a winner.

A variant is a child ``Campaign`` carrying its own subject *and* content, so this
engine is dimension-agnostic: a subject test, a content test, or both run through
exactly the same path. The audience is split deterministically so a test group and
its holdout are exact complements and re-runs are stable.

Flow: ``start_ab_test`` sends each variant to an even slice of a ``sample_percent``
sample and arms ``decide_at``; a beat later calls ``decide_ab_test``, which reads
engagement off each variant's ``CampaignSend`` rows, picks the winner, and (if
``auto_send_winner``) sends it to the held-out remainder.
"""

import hashlib
import logging
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

logger = logging.getLogger("email_marketing")

# The test group must be large enough to put at least this many recipients in
# every arm, or the result is noise — refuse to start below it.
MIN_PER_VARIANT = 1

# A test runs at most this many arms (A–D). The UI offers up to 4; beyond that the
# audience split gets too thin, and an unbounded arm count would spawn one child
# Campaign per arm from a single request.
MAX_VARIANTS = 4


def create_ab_test(
    container,
    *,
    test_type,
    variant_subjects=None,
    num_variants=2,
    sample_percent=20,
    winner_metric=None,
    test_window_hours=4,
    auto_send_winner=True,
):
    """Create a draft A/B test on a container campaign and seed its variants.

    Each variant is a child ``Campaign`` (``parent`` = container). A subject test's
    variants share the container's rendered content and differ only in subject; a
    content test's variants each get a clone of the container's blocks to edit.
    Re-running on a container that already has a *draft* test replaces it; a
    running/complete test is left alone.
    """
    from email_marketing.models import ABTest, ABVariant, Campaign

    existing = ABTest.objects.filter(campaign=container).first()
    if existing is not None:
        if existing.status != ABTest.STATUS_DRAFT:
            return {"error": "test_already_running"}
        # Replace a draft in place — drop its variant child campaigns too.
        Campaign.objects.filter(ab_variant__ab_test=existing).delete()
        existing.delete()

    if winner_metric is None:
        winner_metric = (
            ABTest.METRIC_OPENS if test_type == ABTest.TYPE_SUBJECT else ABTest.METRIC_CLICKS
        )

    if test_type == ABTest.TYPE_SUBJECT:
        # Cap the arms to MAX_VARIANTS: the UI offers up to 4, and an unbounded
        # subject list would spawn one child Campaign per entry from one request.
        subjects = [s.strip() for s in (variant_subjects or []) if s.strip()][:MAX_VARIANTS]
        if len(subjects) < 2:
            return {"error": "need_two_subjects"}
        labels_subjects = list(enumerate(subjects))
    else:
        count = max(2, min(int(num_variants or 2), MAX_VARIANTS))
        labels_subjects = [(i, container.subject) for i in range(count)]

    with transaction.atomic():
        test = ABTest.objects.create(
            campaign=container,
            test_type=test_type,
            winner_metric=winner_metric,
            sample_percent=sample_percent,
            test_window_hours=test_window_hours,
            auto_send_winner=auto_send_winner,
            status=ABTest.STATUS_DRAFT,
        )
        for i, subject in labels_subjects:
            label = chr(ord("A") + i)
            variant_campaign = _make_variant_campaign(container, test_type, label, subject)
            ABVariant.objects.create(ab_test=test, label=label, campaign=variant_campaign)

    return {"ab_test_id": str(test.id), "variants": len(labels_subjects)}


def _make_variant_campaign(container, test_type, label, subject):
    """Create one variant child campaign, seeding its content by test type."""
    import copy

    from email_marketing.models import ABTest, Campaign, CampaignBlock
    from email_marketing.services.block_serializer import save_campaign_html

    # Truncate to the model's own limits — objects.create() skips full_clean(), so
    # a very long container name or submitted subject would otherwise raise a raw
    # DataError mid-transaction instead of being stored cleanly.
    name_max = Campaign._meta.get_field("name").max_length
    subject_max = Campaign._meta.get_field("subject").max_length
    variant = Campaign.objects.create(
        site=container.site,
        parent=container,
        campaign_type=Campaign.TYPE_BROADCAST,
        name=f"{container.name} — variant {label}"[:name_max],
        subject=(subject or "")[:subject_max],
        preview_text=container.preview_text,
        message_type=container.message_type,
        from_account=container.from_account,
        status=Campaign.STATUS_DRAFT,
        # Subject test: share the container's already-rendered content.
        html_content=(container.html_content if test_type == ABTest.TYPE_SUBJECT else ""),
        created_by=container.created_by,
    )
    if test_type == ABTest.TYPE_CONTENT:
        # Clone the container's blocks so the merchant edits this arm's own design.
        for block in container.blocks.all():
            CampaignBlock.objects.create(
                campaign=variant,
                block_type=block.block_type,
                content=copy.deepcopy(block.content),
                order=block.order,
            )
        save_campaign_html(variant)
    return variant


def cancel_ab_test(test):
    """Mark a draft/testing test cancelled (no winner send)."""
    from email_marketing.models import ABTest

    if test.status in (ABTest.STATUS_COMPLETE, ABTest.STATUS_CANCELLED):
        return {"error": "already_final"}
    test.status = ABTest.STATUS_CANCELLED
    test.save(update_fields=["status", "updated_at"])
    return {"cancelled": True}


def _bucket_value(test_id, subscriber_id) -> float:
    """A stable float in [0, 1) for a (test, subscriber) pair.

    Deterministic (sha256, no RNG) so bucketing is reproducible and the holdout is
    the exact complement of the test group.
    """
    digest = hashlib.sha256(f"{test_id}:{subscriber_id}".encode()).hexdigest()
    return int(digest[:12], 16) / float(1 << 48)


def assign_bucket(test, subscriber, num_variants):
    """Variant index [0..num_variants-1] for a test subscriber, or None (holdout)."""
    value = _bucket_value(test.id, subscriber.pk)
    fraction = test.sample_percent / 100.0
    if value >= fraction:
        return None  # holdout — receives the winner later
    # Even split of the [0, fraction) test band across the variants.
    idx = int((value / fraction) * num_variants)
    return min(idx, num_variants - 1)


def _audience(test):
    from email_marketing.services.campaigns import _recipient_queryset

    return _recipient_queryset(test.campaign)


def _partition(test, variants):
    """Split the current audience into per-variant buckets + a holdout list."""
    buckets = {i: [] for i in range(len(variants))}
    holdout = []
    for sub in _audience(test).iterator():
        idx = assign_bucket(test, sub, len(variants))
        if idx is None:
            holdout.append(sub)
        else:
            buckets[idx].append(sub)
    return buckets, holdout


def start_ab_test(test, now=None) -> dict:
    """Send each variant to its bucket and arm the decision time."""
    from email_marketing.models import ABTest
    from email_marketing.services.campaigns import send_campaign

    now = now or timezone.now()
    if test.status != ABTest.STATUS_DRAFT:
        return {"error": "invalid_status", "status": test.status}

    variants = list(test.variants.select_related("campaign").order_by("label"))
    if len(variants) < 2:
        return {"error": "need_two_variants"}

    buckets, holdout = _partition(test, variants)
    if any(len(buckets[i]) < MIN_PER_VARIANT for i in buckets):
        return {"error": "audience_too_small"}

    # All variant sends succeed or none do: if any enqueue errors (no sending
    # account, a variant already claimed), roll the whole start back so the test
    # never enters "testing" with a variant that has no traffic to measure.
    try:
        with transaction.atomic():
            for i, variant in enumerate(variants):
                result = send_campaign(
                    variant.campaign, recipients=buckets[i], variant_label=variant.label
                )
                if result.get("error"):
                    raise _StartAborted(result["error"])
                variant.recipients = len(buckets[i])
                variant.save(update_fields=["recipients", "updated_at"])
            test.status = ABTest.STATUS_TESTING
            test.started_at = now
            test.decide_at = now + timedelta(hours=test.test_window_hours)
            test.save(update_fields=["status", "started_at", "decide_at", "updated_at"])
    except _StartAborted as exc:
        logger.error("A/B test %s could not start: %s", test.id, exc.code)
        return {"error": exc.code}

    logger.info(
        "A/B test %s started: %d variants, %d holdout", test.id, len(variants), len(holdout)
    )
    return {"variants": len(variants), "holdout": len(holdout)}


class _StartAborted(Exception):
    """Internal: a variant send failed, so the whole start must roll back."""

    def __init__(self, code):
        self.code = code
        super().__init__(code)


def _label_rank(label) -> int:
    return ord(label[0]) if label else 999


def decide_ab_test(test, now=None) -> dict:
    """Snapshot engagement, pick the winner, and send it to the holdout."""
    from email_marketing.models import ABTest, CampaignSend
    from email_marketing.services.ab_stats import assess

    now = now or timezone.now()
    if test.status != ABTest.STATUS_TESTING:
        return {"error": "invalid_status", "status": test.status}

    variants = list(test.variants.select_related("campaign").order_by("label"))
    for variant in variants:
        sends = CampaignSend.objects.filter(campaign=variant.campaign)
        # Delivered = the denominator (a consent-skipped recipient never had a shot).
        variant.recipients = sends.exclude(status=CampaignSend.STATUS_SKIPPED).count()
        variant.opened = sends.filter(opened=True).count()
        variant.clicked = sends.filter(clicked=True).count()
        variant.save(update_fields=["recipients", "opened", "clicked", "updated_at"])

    # Highest rate wins; tiebreak on more delivered, then the earlier label.
    winner = max(
        variants,
        key=lambda v: (v.rate(test.winner_metric), v.recipients, -_label_rank(v.label)),
    )
    # How sure are we the winner actually beat the field? Surfaced, not gated: the
    # holdout still gets the best-rate arm when auto-send is on, but the merchant
    # sees whether a small-sample split is a real result or just noise.
    stats = assess(winner, variants, test.winner_metric)
    confidence = stats["confidence"]
    reliable = stats["reliable"]

    winner_send = None
    if test.auto_send_winner:
        _, holdout = _partition(test, variants)
        if holdout:
            winner_send = _spawn_winner_send(test, winner, holdout)

    test.winner = winner
    # Only persist a confidence we'd stand behind. A near-1.0 figure from a tiny,
    # lopsided split (assess flags reliable=False) would make a completed test look
    # decisive when it isn't — store null so consumers read it as "no verdict".
    test.winner_confidence = confidence if reliable else None
    test.status = ABTest.STATUS_COMPLETE
    test.decided_at = now
    test.save(update_fields=["winner", "winner_confidence", "status", "decided_at", "updated_at"])

    logger.info(
        "A/B test %s decided: winner=%s, confidence=%.2f, reliable=%s, winner_send=%s",
        test.id,
        winner.label,
        confidence,
        reliable,
        bool(winner_send),
    )
    return {
        "winner": winner.label,
        "winner_send": bool(winner_send),
        "confidence": confidence,
        "reliable": reliable,
    }


def _spawn_winner_send(test, winner, holdout):
    """Clone the winning variant into a fresh campaign and send it to the holdout."""
    from email_marketing.models import Campaign
    from email_marketing.services.campaigns import send_campaign

    wc = winner.campaign
    winner_campaign = Campaign.objects.create(
        site=wc.site,
        parent=test.campaign,
        campaign_type=Campaign.TYPE_BROADCAST,
        name=f"{test.campaign.name} — winner ({winner.label})",
        subject=wc.subject,
        preview_text=wc.preview_text,
        message_type=wc.message_type,
        segment=test.campaign.segment,
        from_account=wc.from_account,
        html_content=wc.html_content,
        status=Campaign.STATUS_DRAFT,
        created_by=test.campaign.created_by,
    )
    result = send_campaign(winner_campaign, recipients=holdout, variant_label="winner")
    if result.get("error"):
        # The holdout wasn't queued (e.g. no sending account). Don't claim it was;
        # decide_ab_test reports winner_send=False so the merchant can resend.
        logger.error("A/B winner send for test %s failed: %s", test.id, result)
        return None
    return winner_campaign
