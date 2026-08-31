"""Celery tasks for the Campaign Studio.

* ``drain_campaign_outbox`` — the batch-send worker. Claims queued campaign
  sends (throttled) and delivers them via the email_system send service. This is
  the keystone piece: nothing else drains campaign outbox rows.
* ``process_scheduled_campaigns`` — dispatches campaigns whose scheduled time
  has arrived.
* ``refresh_segments`` — rebuilds cached segment member counts.
* ``send_campaign_task`` — async entry point to enqueue a single campaign.

Send throughput is deliberately conservative: Community merchants send on their
own gateway, so the per-tick cap defaults low and can be tuned via
``settings.CAMPAIGN_SEND_RATE_PER_MINUTE``.
"""

import logging

from celery import shared_task
from django.conf import settings
from django.db import transaction
from django.utils import timezone

logger = logging.getLogger("email_marketing")

DEFAULT_SEND_RATE_PER_MINUTE = 60


def _per_tick_cap() -> int:
    """Max campaign emails to send per drainer tick (beat runs every 60s)."""
    rate = getattr(settings, "CAMPAIGN_SEND_RATE_PER_MINUTE", DEFAULT_SEND_RATE_PER_MINUTE)
    try:
        return max(1, int(rate))
    except (TypeError, ValueError):
        return DEFAULT_SEND_RATE_PER_MINUTE


@shared_task(name="email_marketing.drain_campaign_outbox")
def drain_campaign_outbox():
    """Send a throttled batch of queued campaign emails.

    Claims up to the per-tick cap of CampaignSend rows whose outbox is still
    queued (skip-locked so concurrent workers don't collide), delivers each via
    EmailSendingService.send_email, then finalises any campaigns that have no
    more work outstanding.
    """
    from datetime import timedelta

    from email_marketing.models import CampaignSend
    from email_system.models import EmailOutbox
    from email_system.services.email_sender import EmailSendingService

    # Reaper: a worker that died between claiming a batch (-> SENDING) and processing
    # it strands those rows. Nothing else recovers them (the pending sweep excludes
    # campaign rows). A row is only "stuck" once its SENDING claim is older than the
    # timeout — and the claim below stamps updated_at, so this can't reclaim an
    # in-flight send.
    stuck_secs = int(getattr(settings, "EMAIL_CAMPAIGN_STUCK_SECONDS", 600))
    reap_cap = int(getattr(settings, "EMAIL_CAMPAIGN_REAP_BATCH", 500))
    # Cap the batch (a mass worker-death mid-blast could otherwise materialise every
    # stuck id into a huge IN() clause); the rest are reaped on later ticks.
    stuck_ids = list(
        CampaignSend.objects.filter(
            status=CampaignSend.STATUS_SENDING,
            updated_at__lt=timezone.now() - timedelta(seconds=stuck_secs),
        ).values_list("id", flat=True)[:reap_cap]
    )
    reaped_campaigns = set()
    if stuck_ids:
        now = timezone.now()
        # Repair each stuck send by its CURRENT outbox status (classified at UPDATE
        # time, not from a stale pre-split, so a send that completed meanwhile isn't
        # mis-repaired). Every UPDATE re-asserts status=SENDING so a row another worker
        # just finished is never clobbered back — no double-send. Ordered exclusive by
        # outbox status; the outbox-sending revert runs before the queued requeue.
        stuck = CampaignSend.objects.filter(id__in=stuck_ids, status=CampaignSend.STATUS_SENDING)
        reaped_campaigns = set(stuck.values_list("campaign_id", flat=True))
        # (a) outbox already sent → the send happened; mark it sent (no re-send, no orphan).
        n_sent = stuck.filter(outbox__status="sent").update(
            status=CampaignSend.STATUS_SENT, updated_at=now
        )
        # (b) outbox failed/bounced → the send genuinely failed.
        n_failed = stuck.filter(outbox__status__in=("failed", "bounced")).update(
            status=CampaignSend.STATUS_FAILED, updated_at=now
        )
        # (c) outbox still sending → worker died mid-send; revert it to queued...
        EmailOutbox.objects.filter(campaign_send__id__in=stuck_ids, status="sending").update(
            status="queued", updated_at=now
        )
        # ...then requeue every remaining stuck send whose outbox is now queued.
        n_requeue = stuck.filter(outbox__status="queued").update(
            status=CampaignSend.STATUS_QUEUED, updated_at=now
        )
        if n_sent or n_failed or n_requeue:
            logger.warning(
                "Campaign drainer: reaped stuck send(s) — %d sent, %d failed, %d requeued",
                n_sent,
                n_failed,
                n_requeue,
            )

    cap = _per_tick_cap()

    # Claim a batch under a short lock, then release before doing slow sends. Stamp
    # updated_at so the reaper measures "stuck" from claim time, not row creation —
    # otherwise an old-but-just-claimed row could be reclaimed while it's sending.
    with transaction.atomic():
        claim_ids = list(
            CampaignSend.objects.filter(
                status=CampaignSend.STATUS_QUEUED,
                outbox__status="queued",
            )
            .select_for_update(skip_locked=True)
            .order_by("outbox__priority", "outbox__queued_at")
            .values_list("id", flat=True)[:cap]
        )
        if claim_ids:
            CampaignSend.objects.filter(id__in=claim_ids).update(
                status=CampaignSend.STATUS_SENDING, updated_at=timezone.now()
            )

    if not claim_ids and not reaped_campaigns:
        return {"sent": 0, "failed": 0}

    sent = failed = deferred = 0
    # Reaped-sent campaigns must be finalised too (their last outstanding send just
    # flipped to SENT).
    touched_campaigns = set(reaped_campaigns)

    for cs in CampaignSend.objects.filter(id__in=claim_ids).select_related("campaign", "outbox"):
        touched_campaigns.add(cs.campaign_id)
        if not cs.outbox_id:
            cs.status = CampaignSend.STATUS_FAILED
            cs.save(update_fields=["status", "updated_at"])
            failed += 1
            continue

        errored = False
        try:
            ok = EmailSendingService.send_email(str(cs.outbox_id))
        except Exception as exc:  # noqa: BLE001 — record and continue the batch
            logger.error("Campaign send %s failed: %s", cs.id, exc)
            ok = False
            errored = True

        if ok:
            cs.status = CampaignSend.STATUS_SENT
            sent += 1
        elif errored:
            # An unexpected exception is a real failure, not a budget defer: send_email
            # DEFERS by returning False and leaving the outbox queued, so it never
            # raises for a throttle. Mark this send (and its still-unsent outbox) failed
            # so retry_failed_emails re-sends it with backoff and a retry cap, rather
            # than requeuing it forever (the reaper only reclaims SENDING rows).
            cs.outbox.refresh_from_db(fields=["status"])
            if cs.outbox.status == "sent":  # threw after the provider accepted it
                cs.status = CampaignSend.STATUS_SENT
                sent += 1
            else:
                EmailOutbox.objects.filter(id=cs.outbox_id).exclude(status="sent").update(
                    status="failed", updated_at=timezone.now()
                )
                cs.status = CampaignSend.STATUS_FAILED
                failed += 1
        else:
            # send_email may DEFER a marketing row (SMTP budget exhausted): it leaves
            # the outbox queued/held rather than failed. Distinguish that from a real
            # failure so a deferred campaign send retries next tick instead of dying.
            cs.outbox.refresh_from_db(fields=["status"])
            if cs.outbox.status in ("failed", "bounced"):
                cs.status = CampaignSend.STATUS_FAILED
                failed += 1
            else:  # queued (budget defer) / held / logged (paused) → retry later
                cs.status = CampaignSend.STATUS_QUEUED
                deferred += 1
        cs.save(update_fields=["status", "updated_at"])

    _finalise_campaigns(touched_campaigns)

    if deferred and not sent:
        # Every attempted send was throttled — marketing is fully starved this tick
        # (transactional is consuming the account budget). Surface it so a stalled
        # campaign queue is visible rather than silently stuck.
        logger.warning(
            "Campaign drainer: all %d send(s) deferred by SMTP budget — marketing starved",
            deferred,
        )
    elif sent or failed or deferred:
        logger.info(
            "Campaign drainer: %d sent, %d failed, %d deferred (budget)", sent, failed, deferred
        )
    return {"sent": sent, "failed": failed, "deferred": deferred}


def _finalise_campaigns(campaign_ids):
    """Mark campaigns sent once no queued/sending work remains, and roll counts."""
    from django.db.models import Count, Q

    from email_marketing.models import Campaign, CampaignSend

    for campaign in Campaign.objects.filter(id__in=campaign_ids):
        agg = campaign.sends.aggregate(
            outstanding=Count(
                "id",
                filter=Q(
                    status__in=[
                        CampaignSend.STATUS_PENDING,
                        CampaignSend.STATUS_QUEUED,
                        CampaignSend.STATUS_SENDING,
                    ]
                ),
            ),
            sent=Count("id", filter=Q(status=CampaignSend.STATUS_SENT)),
            failed=Count("id", filter=Q(status=CampaignSend.STATUS_FAILED)),
        )
        campaign.sent_count = agg["sent"]
        campaign.failed_count = agg["failed"]
        fields = ["sent_count", "failed_count", "updated_at"]
        if agg["outstanding"] == 0 and campaign.status == campaign.STATUS_SENDING:
            campaign.status = campaign.STATUS_SENT
            now = timezone.now()
            campaign.sent_at = now
            # Advance the delta-aware watermark so a re-send (or the next
            # recurring occurrence) only includes content newer than this send.
            campaign.last_content_sent_at = now
            fields += ["status", "sent_at", "last_content_sent_at"]
        campaign.save(update_fields=fields)


@shared_task(name="email_marketing.process_scheduled_campaigns")
def process_scheduled_campaigns():
    """Enqueue campaigns whose scheduled send time has arrived."""
    from email_marketing.models import Campaign

    now = timezone.now()
    with transaction.atomic():
        due_ids = list(
            Campaign.objects.filter(
                status=Campaign.STATUS_SCHEDULED,
                scheduled_for__lte=now,
            )
            .select_for_update(skip_locked=True)
            .values_list("id", flat=True)
        )

    for campaign_id in due_ids:
        send_campaign_task.delay(str(campaign_id))

    if due_ids:
        logger.info("Dispatched %d scheduled campaign(s)", len(due_ids))
    return {"dispatched": len(due_ids)}


@shared_task(name="email_marketing.send_campaign_task")
def send_campaign_task(campaign_id: str):
    """Enqueue a single campaign's recipients (async entry to send_campaign)."""
    from email_marketing.models import Campaign
    from email_marketing.services.campaigns import send_campaign

    try:
        campaign = Campaign.objects.get(id=campaign_id)
    except Campaign.DoesNotExist:
        logger.error("send_campaign_task: campaign %s not found", campaign_id)
        return {"error": "not_found"}
    return send_campaign(campaign)


@shared_task(name="email_marketing.send_subscription_confirmation")
def send_subscription_confirmation(subscriber_id: str):
    """Send the double opt-in confirmation email for a pending storefront signup.

    Renders the merchant-editable ``newsletter_signup_confirm`` template with a
    tokenised confirmation link. No-op if the subscriber is no longer pending.
    """
    from django.contrib.sites.models import Site
    from django.urls import reverse

    from email_marketing.models import Subscriber
    from email_system.services.email_sender import EmailSendingService

    sub = Subscriber.objects.filter(pk=subscriber_id, status=Subscriber.STATUS_PENDING).first()
    if not sub or not sub.verification_token:
        return {"sent": 0, "reason": "not_pending"}

    site = Site.objects.get(pk=1)
    confirm_path = reverse("newsletter:confirm", args=[sub.verification_token])
    context = {
        "store_name": site.name,
        "confirmation_url": f"https://{site.domain}{confirm_path}",
    }
    EmailSendingService.send_template_email(
        to_email=sub.email,
        template_type="newsletter_signup_confirm",
        context=context,
        language=sub.language_code or None,
    )
    return {"sent": 1}


@shared_task(name="email_marketing.process_recurring_campaigns")
def process_recurring_campaigns():
    """Fire recurring campaign schedules whose next_run_at has arrived.

    Each due schedule spawns a broadcast occurrence (or is skipped/held per the
    merchant's freshness policy). Runs are claimed one-by-one so a slow send
    can't block the tick; next_run_at advances inside run_due_schedule.
    """
    from email_marketing.models import CampaignSchedule
    from email_marketing.services.recurrence import run_due_schedule

    now = timezone.now()
    due_ids = list(
        CampaignSchedule.objects.filter(is_active=True, next_run_at__lte=now).values_list(
            "id", flat=True
        )
    )

    outcomes = {}
    for sid in due_ids:
        with transaction.atomic():
            schedule = (
                CampaignSchedule.objects.select_for_update(skip_locked=True)
                .select_related("campaign")
                .filter(id=sid, is_active=True, next_run_at__lte=now)
                .first()
            )
            if not schedule:
                continue
            try:
                result = run_due_schedule(schedule, now)
            except Exception as exc:  # noqa: BLE001 — one bad schedule mustn't stall the rest
                logger.error("Recurring schedule %s failed: %s", sid, exc)
                result = {"outcome": "error"}
        outcomes[str(sid)] = result.get("outcome")

    if due_ids:
        logger.info("Processed %d recurring schedule(s): %s", len(due_ids), outcomes)
    return {"processed": len(due_ids), "outcomes": outcomes}


@shared_task(name="email_marketing.process_journey_steps")
def process_journey_steps():
    """Send due triggered-journey step emails and advance their enrollments."""
    from email_marketing.services.journeys import process_due_enrollments

    return {"processed": process_due_enrollments()}


@shared_task(name="email_marketing.process_due_ab_tests")
def process_due_ab_tests():
    """Decide A/B tests whose test window has elapsed (pick + send the winner)."""
    from email_marketing.models import ABTest
    from email_marketing.services.ab_testing import decide_ab_test

    now = timezone.now()
    due_ids = list(
        ABTest.objects.filter(status=ABTest.STATUS_TESTING, decide_at__lte=now).values_list(
            "id", flat=True
        )
    )

    decided = 0
    for tid in due_ids:
        with transaction.atomic():
            test = (
                ABTest.objects.select_for_update(skip_locked=True)
                .select_related("campaign")
                .filter(id=tid, status=ABTest.STATUS_TESTING, decide_at__lte=now)
                .first()
            )
            if not test:
                continue
            try:
                decide_ab_test(test, now)
                decided += 1
            except Exception as exc:  # noqa: BLE001 — one bad test mustn't stall the rest
                logger.error("A/B test %s decision failed: %s", tid, exc)

    if decided:
        logger.info("Decided %d A/B test(s)", decided)
    return {"decided": decided}


@shared_task(name="email_marketing.process_journey_ab_winners")
def process_journey_ab_winners():
    """Lock in the winning variant on any journey A/B step that has a clear winner."""
    from email_marketing.services.journeys import lock_due_journey_winners

    return lock_due_journey_winners()


@shared_task(name="email_marketing.refresh_segments")
def refresh_segments():
    """Rebuild cached member counts for all active dynamic segments."""
    from email_marketing.models import Segment

    count = 0
    for segment in Segment.objects.filter(is_active=True, kind=Segment.KIND_DYNAMIC):
        segment.rebuild()
        count += 1
    return {"segments_rebuilt": count}


@shared_task(name="email_marketing.poll_hosted_gateway_bounces")
def poll_hosted_gateway_bounces():
    """Pull delayed bounces/complaints from the Spwig mail gateway into list hygiene.

    A no-op on Community / self-hosted installs (no hosted account or gateway API);
    on a hosted install it feeds the gateway's async bounce log into the same
    suppression seam as the SMTP-reject and webhook paths.
    """
    from email_marketing.services import gateway_bounces

    try:
        return gateway_bounces.ingest_hosted_gateway_bounces()
    except Exception:  # noqa: BLE001 — beat task: never let a poll failure crash the worker
        logger.warning("Hosted gateway bounce poll failed", exc_info=True)
        return {"error": True}


@shared_task(name="email_marketing.detect_abandoned_carts")
def detect_abandoned_carts():
    """Enroll idle, non-empty carts into cart-abandonment journeys (time-based trigger).

    No-op unless a merchant has an active cart-abandonment journey. Scans carts whose
    last activity (Cart.updated_at, kept fresh by CartItem save/delete) is between the
    idle threshold and the max-age floor (the floor stops a first run enrolling ancient
    carts), resolves a reachable email (the user's, or the guest email captured on the
    checkout session), and fires the trigger with the cart id as context + trigger_ref
    (so the email shows the live cart and a conversion can cancel the journey). Consent
    + suppression are still enforced per send by send_campaign_to_subscriber.
    """
    from datetime import timedelta

    from django.contrib.sites.models import Site

    from cart.models import Cart
    from email_marketing.models import Journey, JourneyEnrollment
    from email_marketing.services import journeys as journeys_svc
    from email_marketing.signals import _get_or_create_subscriber

    site = Site.objects.get(pk=1)
    if not Journey.objects.filter(
        site=site, status=Journey.STATUS_ACTIVE, trigger_event=Journey.TRIGGER_CART_ABANDONED
    ).exists():
        return {"enrolled": 0, "scanned": 0}

    now = timezone.now()
    idle_before = now - timedelta(
        minutes=int(getattr(settings, "CART_ABANDONED_AFTER_MINUTES", 60))
    )
    floor = now - timedelta(days=int(getattr(settings, "CART_ABANDONED_MAX_AGE_DAYS", 7)))
    batch = int(getattr(settings, "CART_ABANDONED_BATCH", 500))

    # Exclude carts already in an active cart-abandonment journey BEFORE slicing —
    # otherwise, with more idle carts than the batch, the oldest (already-enrolled)
    # ones fill every tick's batch and newer carts never get processed. Done as a
    # correlated NOT EXISTS on the trigger_ref index (bounded — no full set of active
    # enrollments materialised), and only enrollments of an ACTIVE journey count
    # (a paused journey's stale enrollments shouldn't block a cart).
    from django.db.models import CharField, Exists, OuterRef, Q, Value
    from django.db.models.functions import Cast, Concat

    in_active_journey = JourneyEnrollment.objects.filter(
        journey__site=site,
        journey__status=Journey.STATUS_ACTIVE,
        journey__trigger_event=Journey.TRIGGER_CART_ABANDONED,
        status=JourneyEnrollment.STATUS_ACTIVE,
        trigger_ref=Concat(
            Value("cart:"), Cast(OuterRef("pk"), CharField()), output_field=CharField()
        ),
    )
    # Only carts with an email present are candidates — so an unenrollable cart (a guest
    # who never left an email) can't sit at the front of the updated_at order and
    # monopolise the batch every tick, starving newer enrollable carts. (The registered-
    # email guest guard + format validation in _cart_email are a rare residual skip.)
    has_email = Q(user__email__gt="") | Q(checkout_session__metadata__email__gt="")
    carts = (
        Cart.objects.filter(items__isnull=False, updated_at__lt=idle_before, updated_at__gte=floor)
        .filter(has_email)
        .exclude(Exists(in_active_journey))
        .select_related("user", "checkout_session")
        .distinct()
        .order_by("updated_at")[:batch]
    )
    enrolled = scanned = 0
    for cart in carts:
        scanned += 1
        email = _cart_email(cart)
        if not email:
            continue
        try:
            sub = _get_or_create_subscriber(email, user=cart.user, source="cart_abandoned")
            if sub is None:
                continue
            enrolled += journeys_svc.trigger_event(
                Journey.TRIGGER_CART_ABANDONED,
                sub,
                context={"cart_id": cart.id},
                trigger_ref=f"cart:{cart.id}",
            )
        except Exception as exc:  # noqa: BLE001 — one cart mustn't stall the scan
            logger.error("Cart-abandonment enroll failed for cart %s: %s", cart.id, exc)

    if enrolled:
        logger.info("Cart-abandonment: enrolled %d of %d idle carts", enrolled, scanned)
    return {"enrolled": enrolled, "scanned": scanned}


def _cart_email(cart):
    """A validated, reachable email for a cart, or None.

    Registered cart → the user's email. Guest cart → the email captured on the checkout
    session, BUT only if it isn't a registered account's address: an unauthenticated
    guest typing someone else's email must not trigger a cart email to that registered
    person (identity-spoofing guard). The address is format-validated either way so junk
    input never becomes a Subscriber.
    """
    from django.contrib.auth import get_user_model
    from django.core.exceptions import ValidationError
    from django.core.validators import validate_email

    if cart.user_id and getattr(cart.user, "email", ""):
        email = cart.user.email
    else:
        cs = getattr(cart, "checkout_session", None)
        meta = getattr(cs, "metadata", None)
        email = (meta.get("email") if isinstance(meta, dict) else "") or ""
        email = email.strip()
        if email and get_user_model().objects.filter(email__iexact=email).exists():
            # A guest checkout typed a registered account's address — don't act on it.
            return None
    email = (email or "").strip()
    if not email:
        return None
    try:
        validate_email(email)
    except ValidationError:
        return None
    return email


@shared_task(name="email_marketing.detect_lapsed_customers")
def detect_lapsed_customers():
    """Enroll lapsed customers (no purchase in N days) into win-back journeys.

    No-op unless an active win-back journey exists. Scans CustomerMetrics on the indexed
    last_purchase_date between the lapse threshold and a max-age floor (so a first run
    can't blast customers who lapsed years ago), and enrols the customer's subscriber
    with trigger_ref="winback:<user_id>". Excludes anyone actively in — or recently
    enrolled in — a win-back so a customer is re-won-back at most once per dedup window.
    The dedup window tracks the *journey's* own re-entry rule: it is the larger of
    WIN_BACK_AFTER_DAYS and the journey's cooldown_days, and any once_per_subscriber
    journey excludes every prior enrolment outright. This keeps the [:batch] slots for
    genuinely re-enrollable customers — a customer whose enrolment is old enough to clear
    a fixed window but whom enroll_subscriber would still reject (cooldown/once) would
    otherwise be re-fetched every tick and crowd out freshly-lapsed customers. Consent +
    suppression are enforced per send.
    """
    from datetime import timedelta

    from django.contrib.sites.models import Site
    from django.db.models import CharField, Exists, OuterRef, Q, Value
    from django.db.models.functions import Cast, Concat

    from customers.models import CustomerMetrics
    from email_marketing.models import Journey, JourneyEnrollment
    from email_marketing.services import journeys as journeys_svc
    from email_marketing.signals import _get_or_create_subscriber

    site = Site.objects.get(pk=1)
    win_journeys = list(
        Journey.objects.filter(
            site=site,
            status=Journey.STATUS_ACTIVE,
            trigger_event=Journey.TRIGGER_WIN_BACK,
        ).values_list("once_per_subscriber", "cooldown_days")
    )
    if not win_journeys:
        return {"enrolled": 0, "scanned": 0}
    any_once = any(once for once, _ in win_journeys)
    max_cooldown = max((cd or 0) for _, cd in win_journeys)

    now = timezone.now()
    after_days = int(getattr(settings, "WIN_BACK_AFTER_DAYS", 90))
    max_age_days = int(getattr(settings, "WIN_BACK_MAX_AGE_DAYS", 365))
    batch = int(getattr(settings, "WIN_BACK_BATCH", 500))
    lapsed_before = now - timedelta(days=after_days)
    floor = now - timedelta(days=max_age_days)
    # Re-win-back no more often than the journey's own re-entry rule allows.
    dedup_before = now - timedelta(days=max(after_days, max_cooldown))

    ref = Concat(
        Value("winback:"), Cast(OuterRef("user_id"), CharField()), output_field=CharField()
    )
    recent_or_active = JourneyEnrollment.objects.filter(
        journey__site=site,
        journey__trigger_event=Journey.TRIGGER_WIN_BACK,
        trigger_ref=ref,
    )
    if not any_once:
        # No once_per_subscriber journey → only exclude active or within-cooldown enrolments;
        # older completed ones are genuinely re-enrollable. (An once_per_subscriber journey
        # rejects any re-entry, so we exclude every prior enrolment and skip this filter.)
        recent_or_active = recent_or_active.filter(
            Q(status=JourneyEnrollment.STATUS_ACTIVE) | Q(started_at__gte=dedup_before)
        )

    metrics = (
        CustomerMetrics.objects.filter(
            last_purchase_date__lt=lapsed_before,
            last_purchase_date__gte=floor,
            user__email__gt="",
        )
        .exclude(Exists(recent_or_active))
        .select_related("user")
        .order_by("last_purchase_date")[:batch]
    )
    enrolled = scanned = 0
    for m in metrics:
        scanned += 1
        try:
            sub = _get_or_create_subscriber(m.user.email, user=m.user, source="win_back")
            if sub is None:
                continue
            enrolled += journeys_svc.trigger_event(
                Journey.TRIGGER_WIN_BACK, sub, trigger_ref=f"winback:{m.user_id}"
            )
        except Exception as exc:  # noqa: BLE001 — one customer mustn't stall the scan
            logger.error("Win-back enroll failed for user %s: %s", m.user_id, exc)

    if enrolled:
        logger.info("Win-back: enrolled %d of %d lapsed customers", enrolled, scanned)
    return {"enrolled": enrolled, "scanned": scanned}
