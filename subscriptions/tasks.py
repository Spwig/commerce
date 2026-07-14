"""
Celery Tasks for Subscription Billing
Handles recurring billing for fallback providers.
"""

import logging
from datetime import timedelta

from celery import shared_task
from django.db.models import Q
from django.utils import timezone

logger = logging.getLogger(__name__)


def _emit_fallback_event(subscription, event_type, **kwargs):
    """
    Emit a synthetic SubscriptionEvent for fallback billing engine state changes.
    This provides a unified audit trail and signal emission across both provider modes.
    """
    from .event_processor import SubscriptionEventProcessor
    from .events import SubscriptionEvent

    try:
        event = SubscriptionEvent(
            event_type=event_type,
            event_id=SubscriptionEvent.generate_fallback_event_id(
                str(subscription.subscription_id), event_type.value
            ),
            source="fallback",
            provider_subscription_id=subscription.provider_subscription_id or "",
            data={
                "internal_subscription_id": str(subscription.subscription_id),
                **kwargs.pop("extra_data", {}),
            },
            **kwargs,
        )
        SubscriptionEventProcessor.process_event(event)
    except Exception as e:
        logger.warning(
            f"Failed to emit fallback event {event_type.value} "
            f"for subscription {subscription.subscription_id}: {e}"
        )


@shared_task(name="subscriptions.process_due_subscriptions", ignore_result=True)
def process_due_subscriptions():
    """
    Process all subscriptions that are due for billing.
    Runs every hour via Celery Beat.

    Only processes subscriptions using fallback providers (provider_mode='fallback').
    Native subscriptions are handled by the provider (Stripe, PayPal, etc).
    """
    from .events import SubscriptionEventType
    from .manager import SubscriptionManager
    from .models import CustomerSubscription

    now = timezone.now()

    # Find subscriptions due for billing
    # Exclude subscriptions in grace period — they are managed by dunning tasks
    due_subscriptions = (
        CustomerSubscription.objects.filter(
            provider_mode="fallback",  # Only fallback subscriptions
            status__in=["active", "trial", "past_due"],
            next_billing_date__lte=now,
            cancellation_type="none",
        )
        .exclude(
            grace_period_end_date__isnull=False,
        )
        .select_related("plan", "payment_provider_account", "payment_token")
    )

    total = due_subscriptions.count()
    logger.info(f"Found {total} subscriptions due for billing")

    success_count = 0
    failed_count = 0

    for subscription in due_subscriptions:
        try:
            # Get subscription manager for this gateway
            manager = SubscriptionManager(subscription.payment_provider_account)

            # Process billing cycle
            billing_log = manager.process_billing_cycle(subscription)

            if billing_log.status == "successful":
                success_count += 1
                _emit_fallback_event(
                    subscription,
                    SubscriptionEventType.PAYMENT_SUCCEEDED,
                    amount=billing_log.total_amount.amount if billing_log.total_amount else None,
                    currency=str(billing_log.total_amount.currency)
                    if billing_log.total_amount
                    else "",
                )
            else:
                failed_count += 1
                _emit_fallback_event(
                    subscription,
                    SubscriptionEventType.PAYMENT_FAILED,
                    error_message=billing_log.error_message or "",
                    error_code=billing_log.error_code or "",
                )

                # Schedule retry if eligible
                if billing_log.can_retry():
                    retry_billing_cycle.apply_async(
                        args=[billing_log.id],
                        countdown=3600,  # Retry in 1 hour
                    )

        except Exception as e:
            logger.exception(
                f"Error processing subscription {subscription.subscription_id}: {str(e)}"
            )
            failed_count += 1

    logger.info(
        f"Billing complete: {success_count} successful, {failed_count} failed out of {total}"
    )

    return {
        "total": total,
        "successful": success_count,
        "failed": failed_count,
    }


@shared_task(name="subscriptions.retry_billing_cycle")
def retry_billing_cycle(billing_log_id: int):
    """
    Retry a failed billing cycle.

    Args:
        billing_log_id: BillingCycleLog ID to retry
    """
    from .events import SubscriptionEventType
    from .manager import SubscriptionManager
    from .models import BillingCycleLog

    try:
        billing_log = BillingCycleLog.objects.select_related(
            "subscription__payment_provider_account",
            "subscription__payment_token",
            "subscription__plan",
        ).get(id=billing_log_id)

        if not billing_log.can_retry():
            logger.warning(f"Billing log {billing_log_id} cannot be retried")
            return {"status": "not_eligible"}

        subscription = billing_log.subscription

        # Get subscription manager
        manager = SubscriptionManager(subscription.payment_provider_account)

        # Update retry count and status
        billing_log.retry_count += 1
        billing_log.status = "retrying"
        billing_log.save()

        logger.info(
            f"Retrying billing for subscription {subscription.subscription_id} "
            f"(attempt {billing_log.retry_count}/{billing_log.max_retries})"
        )

        # Attempt charge
        charge_result = manager.provider.charge_payment_token(
            token_id=subscription.payment_token.gateway_token_id,
            amount=billing_log.total_amount.amount,
            currency=str(billing_log.total_amount.currency),
            description=f"Subscription billing (retry) - {subscription.plan.name}",
            metadata={
                "subscription_id": str(subscription.subscription_id),
                "cycle_number": billing_log.cycle_number,
                "retry": billing_log.retry_count,
            },
        )

        if charge_result["status"] == "succeeded":
            # Success! Update billing log and subscription
            billing_log.status = "successful"
            billing_log.provider_response = charge_result
            billing_log.save()

            subscription.billing_cycle_count = billing_log.cycle_number
            subscription.last_billing_date = timezone.now()
            subscription.last_billing_status = "successful"
            subscription.status = "active"

            # Calculate next billing date
            subscription.current_period_start = subscription.current_period_end
            subscription.current_period_end = manager._calculate_next_billing_date(
                subscription.current_period_end,
                subscription.pricing_tier,  # Updated to use pricing_tier instead of plan
            )
            subscription.next_billing_date = subscription.current_period_end

            subscription.save()

            _emit_fallback_event(
                subscription,
                SubscriptionEventType.PAYMENT_SUCCEEDED,
                amount=billing_log.total_amount.amount if billing_log.total_amount else None,
                currency=str(billing_log.total_amount.currency) if billing_log.total_amount else "",
                extra_data={"retry_count": billing_log.retry_count},
            )

            logger.info(
                f"Successfully retried billing for subscription {subscription.subscription_id}"
            )

            return {"status": "successful", "retry_count": billing_log.retry_count}

        else:
            # Still failed
            billing_log.status = "failed"
            billing_log.error_message = charge_result.get("error_message", "")
            billing_log.error_code = charge_result.get("error_code", "")
            billing_log.provider_response = charge_result
            billing_log.save()

            # Check if we should retry again
            if billing_log.can_retry():
                # Schedule another retry with exponential backoff
                retry_hours = 2**billing_log.retry_count  # 2, 4, 8 hours
                retry_billing_cycle.apply_async(args=[billing_log.id], countdown=retry_hours * 3600)

                billing_log.next_retry_date = timezone.now() + timedelta(hours=retry_hours)
                billing_log.save()

                logger.info(
                    f"Scheduled next retry for subscription {subscription.subscription_id} "
                    f"in {retry_hours} hours"
                )
            else:
                # Max retries reached — enter grace period or cancel
                grace_days = subscription.plan.grace_period_days

                if grace_days > 0 and not subscription.grace_period_end_date:
                    # Enter grace period — customer keeps access
                    subscription.grace_period_end_date = timezone.now() + timedelta(days=grace_days)
                    subscription.save(update_fields=["grace_period_end_date"])

                    logger.info(
                        f"Subscription {subscription.subscription_id} entering "
                        f"{grace_days}-day grace period "
                        f"(ends {subscription.grace_period_end_date})"
                    )
                else:
                    # No grace period (grace_period_days=0) — cancel immediately
                    subscription.status = "canceled"
                    subscription.canceled_at = timezone.now()
                    subscription.cancellation_reason = (
                        f"Automatic cancellation: Payment failed after "
                        f"{billing_log.max_retries} retries"
                    )
                    subscription.grace_period_end_date = None
                    subscription.save()

                    _emit_fallback_event(
                        subscription,
                        SubscriptionEventType.CANCELED,
                        extra_data={
                            "reason": "max_retries_exhausted",
                            "retry_count": billing_log.retry_count,
                        },
                    )

            return {
                "status": "failed",
                "retry_count": billing_log.retry_count,
                "will_retry": billing_log.can_retry(),
            }

    except Exception as e:
        logger.exception(f"Error retrying billing log {billing_log_id}: {str(e)}")
        return {"status": "error", "error": str(e)}


@shared_task(name="subscriptions.process_trial_expirations", ignore_result=True)
def process_trial_expirations():
    """
    Process subscriptions with expiring trials.
    Converts trial subscriptions to active when trial period ends.
    Runs daily via Celery Beat.
    """
    from .events import SubscriptionEventType
    from .models import CustomerSubscription

    now = timezone.now()

    # Find trials that have ended
    expired_trials = CustomerSubscription.objects.filter(
        status="trial",
        trial_end_date__lte=now,
        cancellation_type="none",
    ).select_related("plan", "payment_provider_account")

    count = expired_trials.count()
    logger.info(f"Found {count} expired trials to process")

    converted_count = 0
    failed_count = 0

    for subscription in expired_trials:
        try:
            # For native subscriptions, provider handles this automatically
            # For fallback, we need to process first billing
            if subscription.provider_mode == "fallback":
                from .manager import SubscriptionManager

                manager = SubscriptionManager(subscription.payment_provider_account)
                billing_log = manager.process_billing_cycle(subscription)

                if billing_log.status == "successful":
                    converted_count += 1
                    _emit_fallback_event(
                        subscription,
                        SubscriptionEventType.ACTIVATED,
                    )
                else:
                    failed_count += 1

                    # Schedule retry
                    if billing_log.can_retry():
                        retry_billing_cycle.apply_async(args=[billing_log.id], countdown=3600)
            else:
                # Native subscription - just update status
                subscription.status = "active"
                subscription.save()
                converted_count += 1
                _emit_fallback_event(
                    subscription,
                    SubscriptionEventType.ACTIVATED,
                )

        except Exception as e:
            logger.exception(
                f"Error processing trial expiration for {subscription.subscription_id}: {str(e)}"
            )
            failed_count += 1

    logger.info(f"Trial expiration complete: {converted_count} converted, {failed_count} failed")

    return {
        "total": count,
        "converted": converted_count,
        "failed": failed_count,
    }


@shared_task(name="subscriptions.process_subscription_expirations", ignore_result=True)
def process_subscription_expirations():
    """
    Process subscriptions scheduled to expire or cancel.
    Runs daily via Celery Beat.
    """
    from .events import SubscriptionEventType
    from .models import CustomerSubscription

    now = timezone.now()

    # Find subscriptions set to cancel at period end that have reached their end date
    expiring_subscriptions = CustomerSubscription.objects.filter(
        status__in=["active", "trial"],
        cancellation_type="end_of_period",
        current_period_end__lte=now,
    )

    count = expiring_subscriptions.count()
    logger.info(f"Found {count} subscriptions to expire")

    for subscription in expiring_subscriptions:
        try:
            subscription.status = "expired"
            subscription.canceled_at = now
            if not subscription.cancellation_reason:
                subscription.cancellation_reason = "Canceled at period end"
            subscription.save()

            _emit_fallback_event(subscription, SubscriptionEventType.EXPIRED)

            logger.info(f"Expired subscription {subscription.subscription_id}")

        except Exception as e:
            logger.exception(
                f"Error expiring subscription {subscription.subscription_id}: {str(e)}"
            )

    return {"total": count}


@shared_task(name="subscriptions.process_auto_resume", ignore_result=True)
def process_auto_resume():
    """
    Process subscriptions scheduled for automatic resume.
    Runs daily via Celery Beat.
    """
    from .events import SubscriptionEventType
    from .manager import SubscriptionManager
    from .models import CustomerSubscription

    now = timezone.now()

    # Find paused subscriptions with auto-resume date
    resume_subscriptions = CustomerSubscription.objects.filter(
        status="paused",
        auto_resume_date__lte=now,
    ).select_related("payment_provider_account")

    count = resume_subscriptions.count()
    logger.info(f"Found {count} subscriptions to auto-resume")

    success_count = 0
    failed_count = 0

    for subscription in resume_subscriptions:
        try:
            manager = SubscriptionManager(subscription.payment_provider_account)
            manager.resume_subscription(subscription)

            _emit_fallback_event(subscription, SubscriptionEventType.RESUMED)

            success_count += 1
            logger.info(f"Auto-resumed subscription {subscription.subscription_id}")

        except Exception as e:
            logger.exception(
                f"Error auto-resuming subscription {subscription.subscription_id}: {str(e)}"
            )
            failed_count += 1

    logger.info(f"Auto-resume complete: {success_count} successful, {failed_count} failed")

    return {
        "total": count,
        "successful": success_count,
        "failed": failed_count,
    }


@shared_task(name="subscriptions.cleanup_old_billing_logs", ignore_result=True)
def cleanup_old_billing_logs(days_to_keep: int = 365):
    """
    Clean up old billing logs to prevent database bloat.
    Keeps logs for specified number of days (default: 365).
    Runs weekly via Celery Beat.

    Args:
        days_to_keep: Number of days of logs to retain
    """
    from .models import BillingCycleLog

    cutoff_date = timezone.now() - timedelta(days=days_to_keep)

    # Delete old logs (keep only successful ones for audit)
    deleted_count = BillingCycleLog.objects.filter(
        billing_date__lt=cutoff_date,
        status__in=["failed", "retrying"],  # Don't delete successful logs
    ).delete()[0]

    logger.info(f"Cleaned up {deleted_count} old billing logs older than {days_to_keep} days")

    return {"deleted_count": deleted_count}


@shared_task(name="subscriptions.retry_skipped_webhook_events", ignore_result=True)
def retry_skipped_webhook_events():
    """
    Retry subscription webhook events that were skipped because
    the subscription wasn't found yet (race condition handling).
    Runs every 5 minutes via Celery Beat.
    """
    from .event_processor import SubscriptionEventProcessor

    processed = SubscriptionEventProcessor.retry_skipped_events(max_retries=5)
    return {"processed": processed}


# ============================================================================
# Proactive Notification Tasks (P2)
# ============================================================================


def _emit_reminder_event(subscription, event_type):
    """
    Emit a reminder event with a date-based deterministic event ID.
    The idempotency check in SubscriptionEventProcessor prevents duplicate
    emails when the task runs daily.
    """
    from .event_processor import SubscriptionEventProcessor
    from .events import SubscriptionEvent

    today = timezone.now().strftime("%Y-%m-%d")
    event_id = f"reminder_{subscription.subscription_id}_{event_type.value}_{today}"

    try:
        event = SubscriptionEvent(
            event_type=event_type,
            event_id=event_id,
            source="fallback",
            provider_subscription_id=subscription.provider_subscription_id or "",
            data={
                "internal_subscription_id": str(subscription.subscription_id),
                "reminder_date": today,
            },
        )
        SubscriptionEventProcessor.process_event(event)
    except Exception as e:
        logger.warning(
            f"Failed to emit reminder event {event_type.value} "
            f"for subscription {subscription.subscription_id}: {e}"
        )


@shared_task(name="subscriptions.send_trial_ending_reminders", ignore_result=True)
def send_trial_ending_reminders():
    """
    Send reminder emails to customers whose trial period ends within 3 days.
    Runs daily at 9 AM via Celery Beat.

    Uses date-based event IDs for idempotency — running this task multiple
    times on the same day won't send duplicate emails.
    """
    from .events import SubscriptionEventType
    from .models import CustomerSubscription

    now = timezone.now()
    three_days = now + timedelta(days=3)

    trials_ending = CustomerSubscription.objects.filter(
        status="trial",
        trial_end_date__range=(now, three_days),
        cancellation_type="none",
    ).select_related("plan", "pricing_tier", "payment_token", "user")

    count = trials_ending.count()
    logger.info(f"Found {count} trials ending within 3 days")

    sent = 0
    for subscription in trials_ending:
        _emit_reminder_event(subscription, SubscriptionEventType.TRIAL_ENDING)
        sent += 1

    logger.info(f"Processed {sent} trial ending reminders")
    return {"total": count, "processed": sent}


@shared_task(name="subscriptions.send_renewal_reminders", ignore_result=True)
def send_renewal_reminders():
    """
    Send reminder emails to customers whose subscription renews within 3 days.
    Runs daily at 9:15 AM via Celery Beat.

    Uses date-based event IDs for idempotency.
    """
    from .events import SubscriptionEventType
    from .models import CustomerSubscription

    now = timezone.now()
    three_days = now + timedelta(days=3)

    renewals_upcoming = CustomerSubscription.objects.filter(
        status="active",
        next_billing_date__range=(now, three_days),
        cancellation_type="none",
    ).select_related("plan", "pricing_tier", "payment_token", "user")

    count = renewals_upcoming.count()
    logger.info(f"Found {count} subscriptions renewing within 3 days")

    sent = 0
    for subscription in renewals_upcoming:
        _emit_reminder_event(subscription, SubscriptionEventType.RENEWAL_UPCOMING)
        sent += 1

    logger.info(f"Processed {sent} renewal reminders")
    return {"total": count, "processed": sent}


@shared_task(name="subscriptions.send_payment_method_expiry_warnings", ignore_result=True)
def send_payment_method_expiry_warnings():
    """
    Send warning emails to customers whose payment method expires within 30 days.
    Runs daily at 9:30 AM via Celery Beat.

    Deduplicates by checking EmailOutbox for recent sends of the same template
    to the same user (within the last 7 days).
    """
    from .email_notifications import send_payment_method_expiry_email
    from .models import CustomerSubscription

    now = timezone.now()

    # Calculate which month/year combos expire within 30 days
    current_month = now.month
    current_year = now.year
    future = now + timedelta(days=30)
    future_month = future.month
    future_year = future.year

    # Build expiry filter: card expires between current month and 30 days ahead
    expiry_filter = Q(
        payment_token__card_exp_year=current_year,
        payment_token__card_exp_month__gte=current_month,
        payment_token__card_exp_month__lte=(future_month if future_year == current_year else 12),
    )
    if future_year > current_year:
        # Cross-year boundary (e.g. December → January)
        expiry_filter |= Q(
            payment_token__card_exp_year=future_year,
            payment_token__card_exp_month__lte=future_month,
        )

    # Find active subscriptions with card payment tokens expiring soon
    expiring_subs = (
        CustomerSubscription.objects.filter(
            status__in=["active", "trial"],
            cancellation_type="none",
            payment_token__payment_method_type="card",
            payment_token__is_active=True,
        )
        .filter(expiry_filter)
        .select_related("plan", "pricing_tier", "payment_token", "user")
        .distinct()
    )

    count = expiring_subs.count()
    logger.info(f"Found {count} subscriptions with expiring payment methods")

    # Check for recent sends to avoid spamming
    sent = 0
    skipped = 0

    from datetime import date

    for subscription in expiring_subs:
        # Verify the card is actually expiring (double-check)
        if (
            not subscription.payment_token.card_exp_month
            or not subscription.payment_token.card_exp_year
        ):
            continue

        token = subscription.payment_token
        try:
            # Card expires at end of its expiration month
            if token.card_exp_month == 12:
                exp_end = date(token.card_exp_year + 1, 1, 1)
            else:
                exp_end = date(token.card_exp_year, token.card_exp_month + 1, 1)
        except (ValueError, OverflowError):
            continue

        if exp_end <= now.date() or exp_end > (now + timedelta(days=30)).date():
            continue

        # Check if we already sent this email recently (within 7 days)
        try:
            from email_system.models import EmailOutbox

            recent_send = EmailOutbox.objects.filter(
                to_email=subscription.user.email,
                template_type="subscription_payment_method_expiring",
                created_at__gte=now - timedelta(days=7),
                status__in=["queued", "sending", "sent"],
            ).exists()

            if recent_send:
                skipped += 1
                continue
        except Exception:
            pass  # If check fails, send anyway

        send_payment_method_expiry_email(subscription)
        sent += 1

    logger.info(
        f"Payment method expiry warnings: {sent} sent, {skipped} skipped (already notified)"
    )
    return {"total": count, "sent": sent, "skipped": skipped}


# ============================================================================
# Dunning & Grace Period Tasks (P3)
# ============================================================================

DUNNING_RETRY_INTERVAL_HOURS = 48  # Retry charge every 2 days during grace period


@shared_task(name="subscriptions.process_dunning_retries", ignore_result=True)
def process_dunning_retries():
    """
    Retry billing for subscriptions in grace period.
    Runs every 6 hours via Celery Beat.

    During the grace period, we attempt to charge every ~2 days.
    Charges directly via the provider (not through manager.process_billing_cycle)
    to avoid BillingCycleLog unique_together constraint violations.
    On success, updates the existing failed billing log to 'successful'.
    """
    from .events import SubscriptionEventType
    from .manager import SubscriptionManager
    from .models import CustomerSubscription

    now = timezone.now()

    # Find subscriptions in active grace period (fallback mode only)
    grace_subscriptions = CustomerSubscription.objects.filter(
        provider_mode="fallback",
        status="past_due",
        grace_period_end_date__isnull=False,
        grace_period_end_date__gt=now,
    ).select_related("plan", "payment_provider_account", "payment_token", "pricing_tier")

    total = grace_subscriptions.count()
    logger.info(f"Found {total} subscriptions in grace period for dunning retry")

    success_count = 0
    skipped_count = 0
    failed_count = 0

    for subscription in grace_subscriptions:
        try:
            # Get the latest failed billing log for this subscription
            last_log = (
                subscription.billing_logs.filter(status="failed").order_by("-billing_date").first()
            )

            if not last_log:
                skipped_count += 1
                continue

            # Check if enough time has passed since last billing attempt
            if last_log.billing_date:
                hours_since_last = (now - last_log.billing_date).total_seconds() / 3600
                if hours_since_last < DUNNING_RETRY_INTERVAL_HOURS:
                    skipped_count += 1
                    continue

            # Direct charge via provider (avoids creating a new BillingCycleLog)
            manager = SubscriptionManager(subscription.payment_provider_account)
            charge_result = manager.provider.charge_payment_token(
                token_id=subscription.payment_token.gateway_token_id,
                amount=last_log.total_amount.amount,
                currency=str(last_log.total_amount.currency),
                description=(f"Subscription billing (dunning retry) - {subscription.plan.name}"),
                metadata={
                    "subscription_id": str(subscription.subscription_id),
                    "cycle_number": last_log.cycle_number,
                    "dunning_retry": True,
                },
            )

            if charge_result["status"] == "succeeded":
                # Payment recovered — update existing billing log
                last_log.status = "successful"
                last_log.provider_response = charge_result
                last_log.billing_date = now
                last_log.save(
                    update_fields=[
                        "status",
                        "provider_response",
                        "billing_date",
                    ]
                )

                # Update subscription — clear grace period, restore active
                cycle_number = last_log.cycle_number
                subscription.status = "active"
                subscription.billing_cycle_count = cycle_number
                subscription.last_billing_date = now
                subscription.last_billing_status = "successful"
                subscription.grace_period_end_date = None

                # Advance billing period
                subscription.current_period_start = subscription.current_period_end
                subscription.current_period_end = manager._calculate_next_billing_date(
                    subscription.current_period_end,
                    subscription.pricing_tier,
                )
                subscription.next_billing_date = subscription.current_period_end
                subscription.save()

                success_count += 1
                _emit_fallback_event(
                    subscription,
                    SubscriptionEventType.PAYMENT_SUCCEEDED,
                    amount=last_log.total_amount.amount,
                    currency=str(last_log.total_amount.currency),
                    extra_data={"recovered_from_grace_period": True},
                )
                logger.info(
                    f"Payment recovered for subscription "
                    f"{subscription.subscription_id} during grace period"
                )
            else:
                # Still failing — update billing log date so we respect interval
                last_log.billing_date = now
                last_log.error_message = charge_result.get("error_message", "")
                last_log.error_code = charge_result.get("error_code", "")
                last_log.provider_response = charge_result
                last_log.save(
                    update_fields=[
                        "billing_date",
                        "error_message",
                        "error_code",
                        "provider_response",
                    ]
                )

                failed_count += 1
                _emit_fallback_event(
                    subscription,
                    SubscriptionEventType.PAYMENT_FAILED,
                    error_message=last_log.error_message or "",
                    error_code=last_log.error_code or "",
                )

        except Exception as e:
            logger.exception(
                f"Error processing dunning retry for {subscription.subscription_id}: {e}"
            )
            failed_count += 1

    logger.info(
        f"Dunning retries complete: {success_count} recovered, "
        f"{failed_count} failed, {skipped_count} skipped (too soon)"
    )
    return {
        "total": total,
        "recovered": success_count,
        "failed": failed_count,
        "skipped": skipped_count,
    }


@shared_task(name="subscriptions.process_grace_period_expirations", ignore_result=True)
def process_grace_period_expirations():
    """
    Cancel subscriptions whose grace period has expired.
    Runs daily at 1:15 AM via Celery Beat.
    """
    from .events import SubscriptionEventType
    from .models import CustomerSubscription

    now = timezone.now()

    expired_grace = CustomerSubscription.objects.filter(
        status="past_due",
        grace_period_end_date__isnull=False,
        grace_period_end_date__lte=now,
    ).select_related("plan", "user")

    count = expired_grace.count()
    logger.info(f"Found {count} subscriptions with expired grace period")

    canceled_count = 0

    for subscription in expired_grace:
        try:
            grace_days = subscription.plan.grace_period_days
            subscription.status = "canceled"
            subscription.canceled_at = now
            subscription.cancellation_reason = (
                f"Automatic cancellation: Payment not recovered during "
                f"{grace_days}-day grace period"
            )
            subscription.grace_period_end_date = None
            subscription.save()

            _emit_fallback_event(
                subscription,
                SubscriptionEventType.CANCELED,
                extra_data={
                    "reason": "grace_period_expired",
                    "grace_period_days": grace_days,
                },
            )

            canceled_count += 1
            logger.info(
                f"Canceled subscription {subscription.subscription_id} (grace period expired)"
            )

        except Exception as e:
            logger.exception(
                f"Error canceling subscription "
                f"{subscription.subscription_id} after grace period: {e}"
            )

    return {"total": count, "canceled": canceled_count}


@shared_task(name="subscriptions.send_dunning_final_notices", ignore_result=True)
def send_dunning_final_notices():
    """
    Send dunning final notice emails to customers whose grace period
    expires within 2 days.
    Runs daily at 9:45 AM via Celery Beat.

    Uses EmailOutbox deduplication to prevent duplicate sends.
    """
    from .email_notifications import send_dunning_final_notice_email
    from .models import CustomerSubscription

    now = timezone.now()
    two_days = now + timedelta(days=2)

    # Find subscriptions with grace period ending within 2 days
    expiring_soon = CustomerSubscription.objects.filter(
        status="past_due",
        grace_period_end_date__isnull=False,
        grace_period_end_date__range=(now, two_days),
    ).select_related("plan", "pricing_tier", "payment_token", "user")

    count = expiring_soon.count()
    logger.info(f"Found {count} subscriptions for dunning final notice")

    sent = 0
    skipped = 0

    for subscription in expiring_soon:
        # Check for recent sends to avoid duplicates
        try:
            from email_system.models import EmailOutbox

            recent_send = EmailOutbox.objects.filter(
                to_email=subscription.user.email,
                template_type="subscription_dunning_final_notice",
                created_at__gte=now - timedelta(days=7),
                status__in=["queued", "sending", "sent"],
            ).exists()

            if recent_send:
                skipped += 1
                continue
        except Exception:
            pass  # If check fails, send anyway

        send_dunning_final_notice_email(subscription)
        sent += 1

    logger.info(f"Dunning final notices: {sent} sent, {skipped} skipped (already notified)")
    return {"total": count, "sent": sent, "skipped": skipped}


# ============================================================================
# Plan Change Tasks (P4)
# ============================================================================


@shared_task(name="subscriptions.process_scheduled_plan_changes", ignore_result=True)
def process_scheduled_plan_changes():
    """
    Apply deferred plan changes for subscriptions that have reached their renewal date.
    Runs daily at 12:15 AM via Celery Beat (before process_due_subscriptions).

    For subscriptions with a scheduled_plan_change whose current_period_end has passed,
    applies the plan change and calculates proration credit for downgrades.
    """
    from .events import SubscriptionEventType
    from .manager import SubscriptionManager
    from .models import CustomerSubscription, PlanPricingTier, SubscriptionPlan

    now = timezone.now()

    # Find subscriptions with pending plan changes that have reached period end
    pending_changes = (
        CustomerSubscription.objects.filter(
            status__in=["active", "trial"],
            current_period_end__lte=now,
            cancellation_type="none",
        )
        .exclude(
            scheduled_plan_change={},
        )
        .select_related(
            "plan",
            "pricing_tier",
            "payment_provider_account",
            "payment_token",
            "product",
            "variant",
            "user",
        )
    )

    total = pending_changes.count()
    logger.info(f"Found {total} subscriptions with scheduled plan changes to apply")

    applied_count = 0
    failed_count = 0

    for subscription in pending_changes:
        try:
            change_data = subscription.scheduled_plan_change
            if not change_data or not change_data.get("new_plan_id"):
                continue

            # Load new plan and tier
            new_plan = SubscriptionPlan.objects.get(plan_id=change_data["new_plan_id"])
            new_tier = PlanPricingTier.objects.get(tier_id=change_data["new_tier_id"])

            if not new_plan.is_active or not new_tier.is_active:
                logger.warning(
                    f"Skipping scheduled plan change for "
                    f"{subscription.subscription_id}: "
                    f"plan or tier no longer active"
                )
                # Clear the stale scheduled change
                subscription.scheduled_plan_change = {}
                subscription.save(update_fields=["scheduled_plan_change"])
                failed_count += 1
                continue

            # Store old plan info for the event
            old_plan = subscription.plan
            change_type = change_data.get("change_type", "upgrade")

            # Calculate proration credit for downgrades
            # (at renewal, credit is based on price difference for next cycle)
            proration_credit_data = None
            if change_type == "downgrade":
                try:
                    manager = SubscriptionManager(subscription.payment_provider_account)
                    proration_credit_data = manager._calculate_proration(
                        subscription, new_plan, new_tier
                    )
                    if (
                        proration_credit_data
                        and proration_credit_data["proration_amount"].amount < 0
                    ):
                        from djmoney.money import Money

                        subscription.proration_credit = Money(
                            abs(proration_credit_data["proration_amount"].amount),
                            proration_credit_data["proration_amount"].currency,
                        )
                except Exception as e:
                    logger.warning(
                        f"Could not calculate proration for {subscription.subscription_id}: {e}"
                    )

            # Apply the plan change
            subscription.plan = new_plan
            subscription.pricing_tier = new_tier
            subscription.scheduled_plan_change = {}
            subscription.save()

            # Emit event
            event_type = (
                SubscriptionEventType.PLAN_UPGRADED
                if change_type == "upgrade"
                else SubscriptionEventType.PLAN_DOWNGRADED
            )

            extra_data = {
                "old_plan_name": old_plan.name,
                "new_plan_name": new_plan.name,
                "old_plan_id": str(old_plan.plan_id),
                "new_plan_id": str(new_plan.plan_id),
                "change_type": change_type,
                "applied_at_renewal": True,
            }
            if proration_credit_data and change_type == "downgrade":
                extra_data["credit_amount"] = str(proration_credit_data["proration_amount"].amount)

            _emit_fallback_event(
                subscription,
                event_type,
                extra_data=extra_data,
            )

            applied_count += 1
            logger.info(
                f"Applied scheduled plan change for "
                f"{subscription.subscription_id}: "
                f"{old_plan.name} -> {new_plan.name}"
            )

        except (SubscriptionPlan.DoesNotExist, PlanPricingTier.DoesNotExist) as e:
            logger.error(
                f"Plan/tier not found for scheduled change on {subscription.subscription_id}: {e}"
            )
            # Clear invalid scheduled change
            subscription.scheduled_plan_change = {}
            subscription.save(update_fields=["scheduled_plan_change"])
            failed_count += 1

        except Exception as e:
            logger.exception(
                f"Error applying scheduled plan change for {subscription.subscription_id}: {e}"
            )
            failed_count += 1

    logger.info(
        f"Scheduled plan changes complete: {applied_count} applied, "
        f"{failed_count} failed out of {total}"
    )
    return {
        "total": total,
        "applied": applied_count,
        "failed": failed_count,
    }
