"""Journey orchestrator — enroll subscribers on events, walk their flowchart.

A lifecycle event (via signals) calls ``trigger_event(event, subscriber)``, which
enrolls the subscriber into every active journey bound to that event, subject to
segment / once-per-subscriber / cooldown eligibility. A beat then processes due
enrollments by walking the journey's ``JourneyNode`` graph: it fires the current
node (send an email, evaluate a branch), routes the enrollment down the matching
edge, pausing at ``wait_delay`` nodes and completing at an ``exit`` node (or any
node with no outgoing edge).

Modeled on loyalty's campaign orchestrator, but keyed on ``Subscriber`` and
sending builder-designed campaigns via ``send_campaign_to_subscriber`` (consent
is enforced there, per send).
"""

import logging
from datetime import timedelta

from django.db import transaction
from django.db.models import F
from django.utils import timezone

logger = logging.getLogger("email_marketing")

# Safety cap: how many nodes one enrollment may traverse in a single tick before
# we stop and log. Guards against an accidental cycle in the graph.
MAX_HOPS_PER_TICK = 100


def _in_segment(segment, subscriber) -> bool:
    try:
        return segment.resolve_queryset().filter(pk=subscriber.pk).exists()
    except Exception:  # noqa: BLE001 — a bad segment must not block enrollment
        logger.warning("Segment %s membership check failed", getattr(segment, "pk", None))
        return False


def _entry_node(journey):
    """The journey's root node (the ``entry`` node, or any node with no in-edge)."""
    from email_marketing.models import JourneyNode

    entry = journey.nodes.filter(node_type=JourneyNode.TYPE_ENTRY).first()
    if entry:
        return entry
    # Fall back to a node nothing points at (a graph with no explicit entry).
    return journey.nodes.filter(in_edges__isnull=True).first()


def enroll_subscriber(journey, subscriber, now=None, *, context=None, trigger_ref=""):
    """Enroll a subscriber into a journey if eligible; return the enrollment or None.

    ``context`` (event payload, e.g. ``{"cart_id": 123}``) and ``trigger_ref`` (a stable
    per-instance key like ``"cart:123"``) are stored on the enrollment: the context is
    read at send time so a step email can render the actual cart/product, and the
    trigger_ref lets a converting cart / fulfilled order cancel the right enrollment.
    """
    from email_marketing.models import Journey, JourneyEnrollment

    now = now or timezone.now()
    if journey.status != Journey.STATUS_ACTIVE:
        return None
    # Never start a journey for an unsubscribed/bounced subscriber. (Per-send
    # consent is re-checked too, so mid-journey opt-outs also stop delivery.)
    if subscriber.status != subscriber.STATUS_ACTIVE:
        return None

    entry = _entry_node(journey)
    if entry is None:
        return None

    if journey.target_segment_id and not _in_segment(journey.target_segment, subscriber):
        return None

    existing = JourneyEnrollment.objects.filter(journey=journey, subscriber=subscriber)
    # Never run two active enrollments of the same journey for one subscriber. For a
    # time-based trigger (e.g. cart-abandonment scanned every tick) this is also what
    # dedupes re-enrollment of the same still-idle cart.
    if existing.filter(status=JourneyEnrollment.STATUS_ACTIVE).exists():
        return None
    if journey.once_per_subscriber and existing.exists():
        return None
    if journey.cooldown_days:
        cutoff = now - timedelta(days=journey.cooldown_days)
        if existing.filter(started_at__gte=cutoff).exists():
            return None

    enrollment = JourneyEnrollment.objects.create(
        journey=journey,
        subscriber=subscriber,
        current_node=entry,
        next_step_at=now,
        status=JourneyEnrollment.STATUS_ACTIVE,
        context=context or {},
        trigger_ref=trigger_ref or "",
    )
    Journey.objects.filter(pk=journey.pk).update(enrolled_count=F("enrolled_count") + 1)
    logger.info("Enrolled subscriber %s in journey %s", subscriber.pk, journey.pk)
    return enrollment


def trigger_event(event, subscriber, now=None, *, context=None, trigger_ref=""):
    """Enroll ``subscriber`` into all active journeys bound to ``event``.

    ``context``/``trigger_ref`` are the event payload + per-instance key (see
    ``enroll_subscriber``), carried onto each enrollment created for this event.
    """
    from email_marketing.models import Journey

    now = now or timezone.now()
    journeys = Journey.objects.filter(
        site=subscriber.site, status=Journey.STATUS_ACTIVE, trigger_event=event
    ).prefetch_related("nodes")
    enrolled = 0
    for journey in journeys:
        try:
            if enroll_subscriber(
                journey, subscriber, now, context=context, trigger_ref=trigger_ref
            ):
                enrolled += 1
        except Exception as exc:  # noqa: BLE001 — one journey mustn't break the event
            logger.error("Enrolling journey %s failed: %s", journey.pk, exc)
    return enrolled


def cancel_enrollments(site, trigger_ref, reason=""):
    """Exit any ACTIVE enrollments matching a trigger_ref (e.g. a cart that converted).

    Returns the number cancelled. Scoped to the site's journeys. Safe/idempotent —
    only ACTIVE rows are touched.
    """
    from email_marketing.models import JourneyEnrollment

    if not trigger_ref:
        return 0
    n = JourneyEnrollment.objects.filter(
        journey__site=site,
        trigger_ref=trigger_ref,
        status=JourneyEnrollment.STATUS_ACTIVE,
    ).update(
        status=JourneyEnrollment.STATUS_CANCELLED,
        completed_at=timezone.now(),
        updated_at=timezone.now(),
    )
    if n:
        logger.info("Cancelled %d enrollment(s) for trigger_ref=%s (%s)", n, trigger_ref, reason)
    return n


def back_in_stock_journey_active(site=None) -> bool:
    """True if a back-in-stock journey is live (so the catalog notifier can defer to it)."""
    from django.contrib.sites.models import Site

    from email_marketing.models import Journey

    site = site or Site.objects.get(pk=1)
    return Journey.objects.filter(
        site=site,
        status=Journey.STATUS_ACTIVE,
        trigger_event=Journey.TRIGGER_BACK_IN_STOCK,
    ).exists()


def enroll_back_in_stock(email, *, product, variant=None, user=None) -> bool:
    """Route a back-in-stock requester into an active back-in-stock journey.

    Returns True ONLY when the recipient was enrolled AND the journey can actually
    reach them — the journey then owns the notification and the caller must NOT also
    send its own one-off email (no double-send). Returns False when there is no
    active journey, no email, enrollment failed, or the recipient is suppressed /
    not marketing-emailable: the caller then sends its own transactional
    notification, so an explicitly-requested back-in-stock alert is never silently
    dropped.

    The consent check here is deliberate: a back-in-stock alert is an *explicit*
    per-product request, but the journey send path treats it as marketing and skips
    a non-opted-in subscriber (e.g. a guest who never opted into marketing). If we
    took ownership for such a recipient, the journey would silently drop the alert
    and the caller — believing the journey handled it — would send nothing. So we
    only defer to the journey for recipients it will genuinely email; everyone else
    keeps the guaranteed one-off alert (the pre-existing behaviour). is_emailable()
    uses the default marketing message type as a representative gate.

    The trigger_ref (``stock:<product>:<variant>:<subscriber>``) dedups per
    product/variant/recipient so a flapping restock can't re-enroll the same person
    while a run is still active.
    """
    from email_marketing.models import Journey
    from email_marketing.services import suppression
    from email_marketing.signals import _get_or_create_subscriber

    if not email or product is None:
        return False
    try:
        sub = _get_or_create_subscriber(email, user=user, source="back_in_stock")
        if sub is None:
            return False
        # Only take ownership if the journey will actually reach them (see docstring).
        if suppression.is_suppressed(sub.site, sub.email) or not sub.is_emailable():
            return False
        variant_id = variant.id if variant is not None else None
        ref = f"stock:{product.id}:{variant_id or 0}:{sub.id}"
        return (
            trigger_event(
                Journey.TRIGGER_BACK_IN_STOCK,
                sub,
                context={"product_id": product.id, "variant_id": variant_id},
                trigger_ref=ref,
            )
            > 0
        )
    except Exception as exc:  # noqa: BLE001 — never break the stock notifier
        logger.error("Back-in-stock journey enroll failed for %s: %s", email, exc)
        return False


def _complete(enrollment, now, extra_fields=None):
    from email_marketing.models import Journey, JourneyEnrollment

    enrollment.status = JourneyEnrollment.STATUS_COMPLETED
    enrollment.completed_at = now
    fields = ["status", "completed_at", "updated_at", *(extra_fields or [])]
    enrollment.save(update_fields=fields)
    Journey.objects.filter(pk=enrollment.journey_id).update(
        completed_count=F("completed_count") + 1
    )


def _next_node(node, subscriber):
    """The node an enrollment leaves ``node`` for, evaluating a branch if needed."""
    from email_marketing.models import JourneyEdge, JourneyNode

    edges = list(node.out_edges.select_related("to_node"))
    if not edges:
        return None

    if node.node_type == JourneyNode.TYPE_BRANCH:
        took = _evaluate_branch(node, subscriber)
        label = JourneyEdge.BRANCH_YES if took else JourneyEdge.BRANCH_NO
        for edge in edges:
            if edge.branch == label:
                return edge.to_node
        return None  # no edge for the taken side → the path ends here

    # Linear node: follow the first (default) outgoing edge.
    return edges[0].to_node


def _evaluate_branch(node, subscriber) -> bool:
    """Evaluate a branch node's condition against the subscriber (True → Yes edge)."""
    from email_marketing.models import JourneyNode, Segment

    condition = node.config.get("condition")
    if condition == JourneyNode.CONDITION_IN_SEGMENT:
        segment_id = node.config.get("segment_id")
        if not segment_id:
            return False
        segment = Segment.objects.filter(pk=segment_id).first()
        return bool(segment and _in_segment(segment, subscriber))
    # Unknown / unconfigured condition → take the No path (fail-closed).
    logger.warning("Branch node %s has unknown condition %r", node.pk, condition)
    return False


def _route_to(enrollment, node, now):
    """Move an enrollment to ``node``. Returns True to keep walking this tick.

    Arriving at a ``wait_delay`` node schedules the pause and stops (returns
    False); any other node is due immediately (returns True) so the caller keeps
    firing nodes until it hits a wait, an exit, or the end of the graph.
    """
    from email_marketing.models import JourneyEnrollment, JourneyNode

    if node is None:
        _complete(enrollment, now)
        return False

    if node.node_type == JourneyNode.TYPE_EXIT:
        enrollment.current_node = node
        _complete(enrollment, now, extra_fields=["current_node"])
        return False

    if node.node_type == JourneyNode.TYPE_WAIT_DELAY:
        due = now + node.delay()
        enrollment.current_node = node
        enrollment.next_step_at = due
        enrollment.status = JourneyEnrollment.STATUS_ACTIVE
        enrollment.save(update_fields=["current_node", "next_step_at", "updated_at"])
        # A zero-length wait is due immediately — pass straight through this tick
        # rather than burning a beat, matching the old linear step timing.
        return due <= now

    enrollment.current_node = node
    enrollment.next_step_at = now
    enrollment.save(update_fields=["current_node", "next_step_at", "updated_at"])
    return True


def advance_enrollment(enrollment, now=None):
    """Fire the current node and walk the graph until a wait, an exit, or the end."""
    from email_marketing.models import JourneyNode
    from email_marketing.services.campaigns import send_campaign_to_subscriber

    now = now or timezone.now()

    for _hop in range(MAX_HOPS_PER_TICK):
        node = enrollment.current_node
        if node is None:
            _complete(enrollment, now)
            return

        if node.node_type == JourneyNode.TYPE_EXIT:
            _complete(enrollment, now)
            return

        if node.node_type == JourneyNode.TYPE_SEND_EMAIL:
            campaign, subject_override, variant_label = _resolve_node_send(
                node, enrollment.subscriber
            )
            if campaign is not None:
                try:
                    result = send_campaign_to_subscriber(
                        campaign,
                        enrollment.subscriber,
                        subject_override,
                        event_context=enrollment.context or None,
                    )
                    # Record every send (variant "" for a plain step) so per-step
                    # opens/clicks roll up for ALL journeys, not just A/B steps.
                    _record_variant_send(node, enrollment, variant_label, result)
                except Exception as exc:  # noqa: BLE001 — a failed send must not stall the journey
                    logger.error("Journey node send failed (enrollment %s): %s", enrollment.pk, exc)

        nxt = _next_node(node, enrollment.subscriber)
        if not _route_to(enrollment, nxt, now):
            return

    # Exhausting the hop cap means the graph cycles through immediate (non-wait)
    # nodes. Cancel the enrollment so it leaves the due set — otherwise it stays
    # ``next_step_at <= now`` and every later beat reprocesses it, resending up to
    # the cap each run. (Validation blocks activating a cyclic graph; this is the
    # runtime safety net for one built another way, e.g. via import.)
    from email_marketing.models import JourneyEnrollment

    logger.error(
        "Journey enrollment %s exceeded %d hops in one tick — cyclic graph; cancelling.",
        enrollment.pk,
        MAX_HOPS_PER_TICK,
    )
    enrollment.status = JourneyEnrollment.STATUS_CANCELLED
    enrollment.save(update_fields=["status", "updated_at"])


def _node_campaign(node):
    """The Campaign a ``send_email`` node points at, or None if unset/missing."""
    from email_marketing.models import Campaign

    campaign_id = node.config.get("campaign_id")
    if not campaign_id:
        return None
    return Campaign.objects.filter(pk=campaign_id).first()


def _resolve_node_send(node, subscriber):
    """Pick the campaign, optional subject override, and variant label for a send.

    A plain node → ``(campaign, None, "")``. An A/B node with a locked-in winner →
    the winner's arm. An A/B node still running → deterministically bucket this
    enrollee to a variant (stable per ``(node, subscriber)``, no storage, so it's
    the same across ticks and re-enrollments). For a content test the arm is a
    campaign; for a subject test it's the base campaign with the arm's subject.
    """
    from email_marketing.models import Campaign
    from email_marketing.services.ab_testing import _bucket_value

    if not node.is_ab_send:
        return _node_campaign(node), None, ""

    values = node.ab_variant_values()  # campaign ids (content) or subjects (subject)
    labels = node.ab_labels()
    winner = node.ab_winner_label
    if winner in labels:
        idx = labels.index(winner)
    else:
        idx = min(int(_bucket_value(node.id, subscriber.pk) * len(values)), len(values) - 1)

    if node.config.get("ab_test_type") == "content":
        return Campaign.objects.filter(pk=values[idx]).first(), None, labels[idx]
    # Subject test: the base campaign, sent with this arm's subject line.
    return _node_campaign(node), values[idx], labels[idx]


def _record_variant_send(node, enrollment, variant_label, result):
    """Persist the per-send record so its opens/clicks can be attributed.

    Recorded for EVERY journey send — ``variant_label`` is the A/B arm ("A"/"B"/…) or
    ``""`` for a plain step — so per-step engagement rolls up for all journeys, and the
    A/B auto-optimiser (which reads only the labelled arms via ``variant_arms``) is
    unaffected by the plain-step ``""`` rows. Keyed by the queued email's ``outbox_id``,
    which the engagement rollup stamps when the pixel/click fires. Best-effort: a
    recording failure must never stall the journey; only a genuinely queued email
    (with an outbox id) is recorded.
    """
    from email_marketing.models import JourneyStepSend

    outbox_id = (result or {}).get("outbox_id")
    if not outbox_id:
        return
    try:
        JourneyStepSend.objects.create(
            node=node, enrollment=enrollment, variant=variant_label, outbox_id=outbox_id
        )
    except Exception:  # noqa: BLE001 — a tracking-record failure must not stall the journey
        logger.warning("Could not record journey variant send for node %s", node.id, exc_info=True)


class _VariantArm:
    """Lightweight per-variant stats for feeding ``ab_stats.assess`` (mirrors the
    ``.rate()/.recipients/.opened/.clicked/.id`` surface it reads off ABVariant)."""

    def __init__(self, label, recipients, opened, clicked):
        self.id = label
        self.label = label
        self.recipients = recipients
        self.opened = opened
        self.clicked = clicked

    def rate(self, metric) -> float:
        if not self.recipients:
            return 0.0
        wins = self.clicked if metric == "clicks" else self.opened
        return wins / self.recipients


def variant_arms(node):
    """Per-variant stat arms for a send node's A/B, aggregated from its sends."""
    from django.db.models import Count, Q

    from email_marketing.models import JourneyStepSend

    rows = (
        JourneyStepSend.objects.filter(node=node)
        .values("variant")
        .annotate(
            recipients=Count("id"),
            opened=Count("id", filter=Q(opened=True)),
            clicked=Count("id", filter=Q(clicked=True)),
        )
    )
    by_label = {r["variant"]: r for r in rows}
    arms = []
    for label in node.ab_labels():
        r = by_label.get(label) or {"recipients": 0, "opened": 0, "clicked": 0}
        arms.append(_VariantArm(label, r["recipients"], r["opened"], r["clicked"]))
    return arms


def lock_due_journey_winners(now=None):
    """Auto-optimise: lock the winning variant on any A/B send step with a
    statistically significant leader, so every future enrollee gets it.

    The minimum-sample guard is ``is_reliable`` inside ``assess`` (each arm needs
    enough events), so a low-traffic step never locks in early. In-flight enrollees
    keep the variant they were already assigned. Returns a small outcome dict.
    """
    from email_marketing.models import ABTest, Journey, JourneyNode
    from email_marketing.services.ab_stats import assess

    now = now or timezone.now()
    locked = 0
    nodes = JourneyNode.objects.filter(
        node_type=JourneyNode.TYPE_SEND_EMAIL, journey__status=Journey.STATUS_ACTIVE
    )
    for node in nodes:
        if not node.is_ab_send or node.ab_winner_label:
            continue
        arms = variant_arms(node)
        leader = max(arms, key=lambda a: a.rate(node.ab_metric))
        result = assess(leader, arms, node.ab_metric)
        if result["reliable"] and result["confidence"] >= ABTest.SIGNIFICANCE_THRESHOLD:
            node.config["ab_winner_label"] = leader.label
            node.config["ab_winner_locked_at"] = now.isoformat()
            node.save(update_fields=["config", "updated_at"])
            locked += 1
            logger.info("Journey A/B node %s locked winner=%s", node.id, leader.label)
    return {"locked": locked}


def process_due_enrollments(now=None):
    """Beat body: send due journey steps, one skip-locked enrollment at a time."""
    from email_marketing.models import JourneyEnrollment

    now = now or timezone.now()
    due_ids = list(
        JourneyEnrollment.objects.filter(
            status=JourneyEnrollment.STATUS_ACTIVE, next_step_at__lte=now
        ).values_list("id", flat=True)
    )
    processed = 0
    for eid in due_ids:
        with transaction.atomic():
            enrollment = (
                # Lock only the enrollment row (``of="self"``): ``current_node`` is
                # nullable, so select_related joins it as an outer join, and Postgres
                # refuses ``FOR UPDATE`` on the nullable side of an outer join.
                JourneyEnrollment.objects.select_for_update(skip_locked=True, of=("self",))
                .select_related("journey", "subscriber", "current_node")
                .filter(id=eid, status=JourneyEnrollment.STATUS_ACTIVE, next_step_at__lte=now)
                .first()
            )
            if not enrollment:
                continue
            advance_enrollment(enrollment, now)
            processed += 1
    if processed:
        logger.info("Processed %d due journey enrollment(s)", processed)
    return processed
