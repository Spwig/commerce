"""
Email System Celery Tasks

Async tasks for scheduled email processing and other email system operations.
"""

import logging

from celery import shared_task
from django.db import transaction
from django.utils import timezone

logger = logging.getLogger("email_system")


@shared_task
def process_scheduled_emails():
    """Process pending scheduled emails that are due for sending.

    Runs every 5 minutes via Celery Beat (HQ only). Picks up ScheduledEmail
    records where status='pending' and scheduled_for <= now, then sends each
    via EmailSendingService.send_template_email().
    """
    from email_system.models import ScheduledEmail
    from email_system.services.email_sender import EmailSendingService

    now = timezone.now()

    # Collect IDs under a lock so concurrent workers don't pick the same rows,
    # then process outside the transaction to avoid long-held locks.
    with transaction.atomic():
        pending_ids = list(
            ScheduledEmail.objects.filter(
                status="pending",
                scheduled_for__lte=now,
            )
            .select_for_update(skip_locked=True)
            .values_list("id", flat=True)
        )
        if pending_ids:
            ScheduledEmail.objects.filter(id__in=pending_ids).update(
                status="sent",  # Claim them; failures get corrected below
            )

    sent = 0
    failed = 0

    for scheduled in ScheduledEmail.objects.filter(id__in=pending_ids):
        try:
            outbox = EmailSendingService.send_template_email(
                to_email=scheduled.recipient_email,
                template_type=scheduled.template_type,
                context=scheduled.context_json,
                dispatch=False,  # we send inline below; don't also on-commit-dispatch
            )
            if outbox and outbox.status == "queued":
                EmailSendingService.send_email(str(outbox.id))

            scheduled.sent_at = timezone.now()
            scheduled.save(update_fields=["status", "sent_at"])
            sent += 1

        except Exception as e:
            logger.error(
                "Failed to send scheduled email %d (%s → %s): %s",
                scheduled.id,
                scheduled.template_type,
                scheduled.recipient_email,
                e,
            )
            scheduled.status = "failed"
            scheduled.error_message = str(e)[:1000]
            scheduled.save(update_fields=["status", "error_message"])
            failed += 1

    if sent or failed:
        logger.info(
            "Processed scheduled emails: %d sent, %d failed",
            sent,
            failed,
        )


@shared_task(name="email_system.send_outbox_email")
def send_outbox_email(outbox_id):
    """Deliver a single queued EmailOutbox row (the transactional fast lane).

    Dispatched on-commit by send_template_email and by the pending sweep. Delivery
    goes through EmailSendingService.send_email, whose atomic claim makes this safe
    to call more than once for the same row (a duplicate dispatch is a no-op).
    """
    from email_system.services.email_sender import EmailSendingService

    return EmailSendingService.send_email(str(outbox_id))


@shared_task(name="email_system.retry_failed_emails")
def retry_failed_emails():
    """Retry failed sends whose backoff has elapsed (transactional included).

    Without this, a transient SMTP failure permanently loses a transactional email.
    The backoff gate in EmailSendingService.retry_failed_emails keeps it from
    hammering a flaky recipient, and the atomic claim makes it safe alongside the
    fast path / sweep.
    """
    from email_system.services.email_sender import EmailSendingService

    return EmailSendingService.retry_failed_emails()


@shared_task(name="email_system.drain_pending_outbox")
def drain_pending_outbox():
    """Safety-net sweep: deliver stranded queued outbox rows and reclaim stuck ones.

    Guarantees eventual delivery of any transactional / journey email whose on-commit
    dispatch was lost (worker/broker restart) and is the ONLY sender for journey-step
    emails (they create no CampaignSend, so the campaign drainer skips them).

    - Pass 1 (reclaim): a row stuck in "sending" past ``EMAIL_PENDING_SWEEP_STUCK_SECONDS``
      means the worker died mid-send; return it to "queued" (and bump retry_count so a
      poison message eventually fails instead of looping forever).
    - Pass 2 (deliver): dispatch queued rows inside the age window, EXCLUDING campaign
      rows (``campaign_send__isnull=True`` — those are the campaign drainer's job, and
      claiming them here would race it). The window's lower bound guards against a first
      run mailing the entire historical backlog of stale confirmations/reset links.
    """
    from datetime import timedelta

    from django.conf import settings
    from django.utils.dateparse import parse_datetime

    from email_system.models import EmailOutbox

    if not getattr(settings, "EMAIL_PENDING_SWEEP_ENABLED", True):
        return {"reclaimed": 0, "dispatched": 0}

    now = timezone.now()
    grace = int(getattr(settings, "EMAIL_PENDING_SWEEP_GRACE_SECONDS", 120))
    stuck = int(getattr(settings, "EMAIL_PENDING_SWEEP_STUCK_SECONDS", 600))
    max_age_hours = int(getattr(settings, "EMAIL_PENDING_SWEEP_MAX_AGE_HOURS", 24))
    batch = int(getattr(settings, "EMAIL_PENDING_SWEEP_BATCH", 200))

    # Pass 1 — reclaim orphaned "sending" rows (worker crashed between claim and send).
    reclaimed = EmailOutbox.objects.filter(
        status="sending", updated_at__lt=now - timedelta(seconds=stuck)
    )
    from django.db.models import F

    reclaimed_n = reclaimed.update(
        status="queued", retry_count=F("retry_count") + 1, updated_at=now
    )

    # Pass 2 — deliver stranded queued rows within the age window (never the historical
    # backlog). lower_bound = max(now - max_age, optional deploy floor).
    lower_bound = now - timedelta(hours=max_age_hours)
    floor_raw = getattr(settings, "EMAIL_PENDING_SWEEP_FLOOR", None)
    if floor_raw:
        floor = parse_datetime(floor_raw)
        if floor is None:
            logger.warning("EMAIL_PENDING_SWEEP_FLOOR is not a valid datetime: %r", floor_raw)
        else:
            # USE_TZ is on; a floor string without an offset parses naive and would
            # raise comparing against the aware bound — make it aware first.
            if timezone.is_naive(floor):
                floor = timezone.make_aware(floor)
            if floor > lower_bound:
                lower_bound = floor

    due_ids = list(
        EmailOutbox.objects.filter(
            status="queued",
            campaign_send__isnull=True,  # reverse rel: exclude campaign rows (drainer's job)
            queued_at__lte=now - timedelta(seconds=grace),
            queued_at__gte=lower_bound,
        )
        .order_by("priority", "queued_at", "id")
        .values_list("id", flat=True)[:batch]
    )
    # Just dispatch — send_email applies the marketing SMTP-budget gate itself, so a
    # journey (marketing) row with no headroom defers back to queued and is retried on
    # a later tick; transactional rows always go. (Ordering sends transactional first.)
    for oid in due_ids:
        send_outbox_email.delay(str(oid))

    if reclaimed_n or due_ids:
        logger.info(
            "Pending-outbox sweep: reclaimed %d stuck, dispatched %d",
            reclaimed_n,
            len(due_ids),
        )
    return {"reclaimed": reclaimed_n, "dispatched": len(due_ids)}
