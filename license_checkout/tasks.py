"""
Hosted Subscription Billing Tasks

Celery tasks for recurring billing of hosted subscriptions.
Adapts the fallback billing pattern from subscriptions/tasks.py
for Spwig's own hosted subscription billing via Airwallex consents.

Schedule (configured in core/settings.py, HQ only):
- process_due_billing: every hour
- process_grace_periods: daily at 03:00
- process_terminations: daily at 04:00
- send_termination_warnings: daily at 05:00
"""

import logging
from datetime import timedelta as td
from celery import shared_task
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


def _require_hq():
    """Defense-in-depth: ensure hosted billing tasks only run on HQ."""
    if not getattr(settings, 'SPWIG_IS_HQ', False):
        logger.warning('Hosted billing task invoked on non-HQ instance — skipping')
        return False
    return True


@shared_task(name='hosted.process_due_billing', ignore_result=True)
def process_due_billing():
    """
    Process hosted subscriptions due for billing.
    Runs every hour via Celery Beat.

    For each due subscription:
    - Charges the Airwallex payment consent
    - On success: advances billing period, sends receipt
    - On failure: marks past_due, schedules retry, sends failure email
    """
    if not _require_hq():
        return
    from dateutil.relativedelta import relativedelta
    from license_checkout.models import HostedSubscription, HostedBillingLog
    from djmoney.money import Money

    now = timezone.now()

    # Use select_for_update(skip_locked=True) to prevent double-charging
    # if overlapping task runs occur. Wrapped in transaction.atomic().
    from django.db import transaction

    success_count = 0
    failed_count = 0

    # Process each subscription one at a time with its own atomic lock.
    # This prevents double-charging if overlapping task runs occur.
    due_ids = list(
        HostedSubscription.objects.filter(
            status__in=[
                HostedSubscription.Status.ACTIVE,
                HostedSubscription.Status.PAST_DUE,
            ],
            next_billing_date__lte=now,
        ).exclude(
            grace_period_end_date__isnull=False,
        ).exclude(
            cancellation_type__in=[
                HostedSubscription.CancellationType.END_OF_PERIOD,
                HostedSubscription.CancellationType.IMMEDIATE,
            ],
        ).values_list('id', flat=True)
    )

    total = len(due_ids)
    if total == 0:
        return {'total': 0, 'successful': 0, 'failed': 0}

    logger.info('Found %d hosted subscriptions due for billing', total)

    for sub_id in due_ids:
        try:
            # Lock this specific subscription for the duration of billing
            with transaction.atomic():
                subscription = HostedSubscription.objects.select_for_update(
                    skip_locked=True,
                ).select_related(
                    'hosted_plan', 'payment_provider_account',
                ).filter(
                    id=sub_id,
                    next_billing_date__lte=now,  # Re-check: still due?
                ).first()

                if not subscription:
                    continue  # Already processed by another worker or no longer due

                amount = subscription.billing_amount
                cycle = subscription.billing_cycle_count + 1

                # Idempotency: skip if already being processed
                if HostedBillingLog.objects.filter(
                    subscription=subscription,
                    cycle_number=cycle,
                    status=HostedBillingLog.Status.PROCESSING,
                ).exists():
                    logger.info('Skipping %s cycle %d — already processing', subscription.store_slug, cycle)
                    continue

                # Create billing log inside the lock
                billing_log = HostedBillingLog.objects.create(
                    subscription=subscription,
                    cycle_number=cycle,
                    billing_date=now,
                    amount=Money(amount, 'EUR'),
                    status=HostedBillingLog.Status.PROCESSING,
                )

            # Charge via Airwallex consent
            charge_success = _charge_subscription(subscription, amount, billing_log)

            if charge_success:
                # Advance billing period
                if subscription.billing_interval == HostedSubscription.BillingInterval.ANNUAL:
                    new_period_end = subscription.current_period_end + relativedelta(years=1)
                else:
                    new_period_end = subscription.current_period_end + relativedelta(months=1)

                subscription.current_period_start = subscription.current_period_end
                subscription.current_period_end = new_period_end
                subscription.next_billing_date = new_period_end
                subscription.billing_cycle_count = cycle
                subscription.last_billing_date = now
                subscription.last_billing_status = 'successful'
                subscription.status = HostedSubscription.Status.ACTIVE
                subscription.retry_count = 0
                subscription.save(update_fields=[
                    'current_period_start', 'current_period_end',
                    'next_billing_date', 'billing_cycle_count',
                    'last_billing_date', 'last_billing_status',
                    'status', 'retry_count', 'updated_at',
                ])

                billing_log.status = HostedBillingLog.Status.SUCCESSFUL
                billing_log.save(update_fields=['status'])

                # Send receipt email
                _send_billing_email(subscription, 'hosted_payment_receipt', {
                    'store_name': subscription.store_name,
                    'plan_name': subscription.hosted_plan.name,
                    'amount': str(amount),
                    'currency': 'EUR',
                    'period_start': subscription.current_period_start.strftime('%d %B %Y'),
                    'period_end': subscription.current_period_end.strftime('%d %B %Y'),
                    'next_billing_date': subscription.next_billing_date.strftime('%d %B %Y'),
                    'admin_url': f'https://{subscription.store_slug}.myspwig.com/en/admin/',
                })

                success_count += 1
                logger.info(
                    'Billing successful for %s (cycle %d, EUR %s)',
                    subscription.store_slug, cycle, amount,
                )
            else:
                # Mark past_due and schedule retry
                subscription.status = HostedSubscription.Status.PAST_DUE
                subscription.last_billing_date = now
                subscription.last_billing_status = 'failed'
                subscription.retry_count += 1
                subscription.save(update_fields=[
                    'status', 'last_billing_date', 'last_billing_status',
                    'retry_count', 'updated_at',
                ])

                billing_log.status = HostedBillingLog.Status.RETRYING
                billing_log.retry_count = subscription.retry_count
                # Exponential backoff: 2h, 4h, 8h
                backoff_hours = 2 ** subscription.retry_count
                billing_log.next_retry_date = now + td(hours=backoff_hours)
                billing_log.save(update_fields=[
                    'status', 'retry_count', 'next_retry_date',
                ])

                if subscription.retry_count <= 3:
                    retry_hosted_billing.apply_async(
                        args=[str(billing_log.id)],
                        countdown=backoff_hours * 3600,
                    )

                # Send payment failed email
                _send_billing_email(subscription, 'hosted_payment_failed', {
                    'store_name': subscription.store_name,
                    'plan_name': subscription.hosted_plan.name,
                    'amount': str(amount),
                    'currency': 'EUR',
                    'retry_info': f'We will retry in {backoff_hours} hours',
                })

                # Notify update server
                _notify_status_change(subscription, 'past_due')

                failed_count += 1
                logger.warning(
                    'Billing failed for %s (cycle %d, retry %d)',
                    subscription.store_slug, cycle, subscription.retry_count,
                )

        except Exception as e:
            logger.exception(
                'Error processing billing for %s: %s',
                subscription.store_slug, e,
            )
            failed_count += 1

    logger.info(
        'Hosted billing complete: %d successful, %d failed out of %d',
        success_count, failed_count, total,
    )
    return {'total': total, 'successful': success_count, 'failed': failed_count}


@shared_task(name='hosted.retry_billing', ignore_result=True)
def retry_hosted_billing(billing_log_id):
    """
    Retry a failed billing charge with exponential backoff.

    After max retries (3): enters 7-day grace period.
    """
    if not _require_hq():
        return
    from dateutil.relativedelta import relativedelta
    from license_checkout.models import HostedBillingLog, HostedSubscription

    from django.db import transaction

    try:
        log = HostedBillingLog.objects.select_related(
            'subscription', 'subscription__hosted_plan',
        ).get(id=billing_log_id)
    except HostedBillingLog.DoesNotExist:
        logger.error('retry_hosted_billing: log %s not found', billing_log_id)
        return

    # Lock the log and subscription, verify state is still valid, flip to PROCESSING
    with transaction.atomic():
        log = HostedBillingLog.objects.select_for_update().select_related(
            'subscription', 'subscription__hosted_plan',
        ).get(id=billing_log_id)

        if log.status != HostedBillingLog.Status.PENDING_RETRY:
            logger.info(
                'Skipping retry for log %s — status is %s (expected PENDING_RETRY)',
                billing_log_id, log.status,
            )
            return

        log.status = HostedBillingLog.Status.PROCESSING
        log.save(update_fields=['status'])

    subscription = log.subscription

    if subscription.status not in (
        HostedSubscription.Status.PAST_DUE,
        HostedSubscription.Status.ACTIVE,
    ):
        logger.info('Skipping retry for %s — status is %s', subscription.store_slug, subscription.status)
        return

    success = _charge_subscription(subscription, log.amount.amount, log)

    if success:
        log.status = HostedBillingLog.Status.SUCCESSFUL
        log.save(update_fields=['status'])

        # Advance billing period (same logic as process_due_billing success path)
        now = timezone.now()
        if subscription.billing_interval == HostedSubscription.BillingInterval.ANNUAL:
            new_period_end = subscription.current_period_end + relativedelta(years=1)
        else:
            new_period_end = subscription.current_period_end + relativedelta(months=1)

        subscription.current_period_start = subscription.current_period_end
        subscription.current_period_end = new_period_end
        subscription.next_billing_date = new_period_end
        subscription.billing_cycle_count = log.cycle_number
        subscription.status = HostedSubscription.Status.ACTIVE
        subscription.retry_count = 0
        subscription.last_billing_date = now
        subscription.last_billing_status = 'successful'
        subscription.grace_period_end_date = None  # Clear any grace period
        subscription.save(update_fields=[
            'current_period_start', 'current_period_end',
            'next_billing_date', 'billing_cycle_count',
            'status', 'retry_count', 'last_billing_date',
            'last_billing_status', 'grace_period_end_date', 'updated_at',
        ])

        # Send recovery email
        _send_billing_email(subscription, 'hosted_payment_recovered', {
            'store_name': subscription.store_name,
            'plan_name': subscription.hosted_plan.name,
            'amount': str(log.amount.amount),
            'currency': 'EUR',
            'admin_url': f'https://{subscription.store_slug}.myspwig.com/en/admin/',
        })

        # Notify update server: back to active
        _notify_status_change(subscription, 'active')

        logger.info('Billing retry successful for %s', subscription.store_slug)
    else:
        log.retry_count += 1

        if log.retry_count >= log.max_retries:
            # Max retries exhausted — enter grace period
            log.status = HostedBillingLog.Status.FAILED
            log.save(update_fields=['status', 'retry_count'])

            subscription.grace_period_end_date = timezone.now() + td(days=7)
            subscription.save(update_fields=['grace_period_end_date', 'updated_at'])

            _send_billing_email(subscription, 'hosted_suspension_warning', {
                'store_name': subscription.store_name,
                'plan_name': subscription.hosted_plan.name,
                'grace_end_date': subscription.grace_period_end_date.strftime('%d %B %Y'),
            })

            logger.warning(
                'Max retries reached for %s — entering 7-day grace period',
                subscription.store_slug,
            )
        else:
            # More retries available — schedule next attempt
            log.status = HostedBillingLog.Status.RETRYING
            backoff_hours = 2 ** (log.retry_count + 1)
            log.next_retry_date = timezone.now() + td(hours=backoff_hours)
            log.save(update_fields=['status', 'retry_count', 'next_retry_date'])

            retry_hosted_billing.apply_async(
                args=[str(log.id)],
                countdown=backoff_hours * 3600,
            )


@shared_task(name='hosted.process_grace_periods', ignore_result=True)
def process_grace_periods():
    """
    Check for expired grace periods and suspend instances.
    Runs daily.
    """
    if not _require_hq():
        return
    from django.db import transaction
    from license_checkout.models import HostedSubscription

    now = timezone.now()

    expired_ids = list(
        HostedSubscription.objects.filter(
            status=HostedSubscription.Status.PAST_DUE,
            grace_period_end_date__lte=now,
        ).values_list('id', flat=True)
    )

    count = 0
    for sub_id in expired_ids:
        try:
            with transaction.atomic():
                subscription = HostedSubscription.objects.select_for_update(
                    skip_locked=True,
                ).select_related('hosted_plan').filter(
                    id=sub_id,
                    status=HostedSubscription.Status.PAST_DUE,
                    grace_period_end_date__lte=now,
                ).first()

                if not subscription:
                    continue  # Already processed by another worker

                subscription.status = HostedSubscription.Status.SUSPENDED
                subscription.suspended_at = now
                subscription.grace_period_end_date = None  # Clear so future billing isn't blocked
                subscription.save(update_fields=['status', 'suspended_at', 'grace_period_end_date', 'updated_at'])

            _send_billing_email(subscription, 'hosted_suspended', {
                'store_name': subscription.store_name,
                'plan_name': subscription.hosted_plan.name,
            })

            _notify_status_change(subscription, 'suspended')

            count += 1
            logger.info('Suspended %s due to expired grace period', subscription.store_slug)

        except Exception as e:
            logger.exception('Error suspending subscription %s: %s', sub_id, e)

    if count:
        logger.info('Suspended %d hosted subscriptions due to expired grace periods', count)


@shared_task(name='hosted.process_terminations', ignore_result=True)
def process_terminations():
    """
    Terminate subscriptions past their 30-day cancellation countdown.
    Runs daily.
    """
    if not _require_hq():
        return
    from license_checkout.models import HostedSubscription

    now = timezone.now()

    due = HostedSubscription.objects.filter(
        status=HostedSubscription.Status.CANCELLED,
        termination_scheduled_at__lte=now,
    ).select_related('hosted_plan')

    count = 0
    for subscription in due:
        subscription.status = HostedSubscription.Status.TERMINATED
        subscription.save(update_fields=['status', 'updated_at'])

        _send_billing_email(subscription, 'hosted_terminated', {
            'store_name': subscription.store_name,
        })

        # Notify update server to destroy the instance
        try:
            from license_checkout.services import notify_update_server_subscription
            notify_update_server_subscription(
                event_type='subscription.terminated',
                data={'license_key': subscription.license_key},
            )
        except Exception as e:
            logger.error(
                'Failed to notify update server of termination for %s: %s',
                subscription.store_slug, e,
            )

        count += 1
        logger.info('Terminated %s — 30-day countdown expired', subscription.store_slug)

    if count:
        logger.info('Terminated %d hosted subscriptions', count)


@shared_task(name='hosted.send_termination_warnings', ignore_result=True)
def send_termination_warnings():
    """
    Send 7-day warning emails to merchants whose subscriptions
    are approaching termination. Runs daily.
    """
    if not _require_hq():
        return
    from email_system.models import EmailOutbox
    from license_checkout.models import HostedSubscription

    now = timezone.now()
    # Find subscriptions terminating in 6-8 days (so the email arrives ~7 days before)
    window_start = now + td(days=6)
    window_end = now + td(days=8)

    due = HostedSubscription.objects.filter(
        status=HostedSubscription.Status.CANCELLED,
        termination_scheduled_at__range=(window_start, window_end),
    ).select_related('hosted_plan')

    count = 0
    for subscription in due:
        # Avoid duplicate warnings: check if we already sent one recently
        already_warned = EmailOutbox.objects.filter(
            template_type='hosted_termination_warning',
            to_email=subscription.email,
            created_at__gte=now - td(days=3),
        ).exists()

        if not already_warned:
            _send_billing_email(subscription, 'hosted_termination_warning', {
                'store_name': subscription.store_name,
                'termination_date': subscription.termination_scheduled_at.strftime('%d %B %Y'),
            })
            count += 1
            logger.info(
                'Sent termination warning to %s (termination: %s)',
                subscription.store_slug, subscription.termination_scheduled_at,
            )

    if count:
        logger.info('Sent %d termination warnings', count)


@shared_task(name='hosted.escalate_suspended', ignore_result=True)
def escalate_suspended_subscriptions():
    """
    Auto-terminate subscriptions that have been suspended for 30+ days.

    Sets termination_scheduled_at = now + 30 days and moves to CANCELLED,
    entering the standard termination countdown with warning emails.
    Total time from suspension to destruction: ~60 days.
    Runs daily.
    """
    if not _require_hq():
        return
    from license_checkout.models import HostedSubscription

    now = timezone.now()
    cutoff = now - td(days=30)

    stale = HostedSubscription.objects.filter(
        status=HostedSubscription.Status.SUSPENDED,
        suspended_at__isnull=False,
        suspended_at__lte=cutoff,
    ).select_related('hosted_plan')

    count = 0
    for subscription in stale:
        subscription.status = HostedSubscription.Status.CANCELLED
        subscription.cancellation_type = HostedSubscription.CancellationType.IMMEDIATE
        subscription.cancelled_at = now
        subscription.cancellation_reason = 'Auto-cancelled: suspended for 30+ days due to unpaid billing'
        subscription.termination_scheduled_at = now + td(days=30)
        subscription.save(update_fields=[
            'status', 'cancellation_type', 'cancelled_at',
            'cancellation_reason', 'termination_scheduled_at', 'updated_at',
        ])

        _send_billing_email(subscription, 'hosted_cancellation_confirmation', {
            'store_name': subscription.store_name,
            'plan_name': subscription.hosted_plan.name,
            'access_until_date': 'N/A (account was suspended)',
            'termination_date': subscription.termination_scheduled_at.strftime('%d %B %Y'),
        })

        count += 1
        logger.info(
            'Escalated suspended subscription %s to cancellation (30-day countdown)',
            subscription.store_slug,
        )

    if count:
        logger.info('Escalated %d suspended subscriptions to termination countdown', count)


# ── Helpers ──────────────────────────────────────────────────────────────

def _charge_subscription(subscription, amount, billing_log):
    """
    Attempt to charge a subscription via Airwallex payment consent.
    Returns True on success, False on failure.
    """
    if not subscription.airwallex_consent_id:
        billing_log.error_message = 'No payment consent configured'
        billing_log.error_code = 'no_consent'
        billing_log.save(update_fields=['error_message', 'error_code'])
        logger.error('No consent ID for %s — cannot charge', subscription.store_slug)
        return False

    # Resolve payment provider — use subscription's stored provider, fall back to default
    provider_account = subscription.payment_provider_account
    if not provider_account:
        from payment_providers.models import PaymentProviderAccount
        provider_account = PaymentProviderAccount.objects.filter(
            is_active=True, connection_status='connected',
        ).first()
    if not provider_account:
        billing_log.error_message = 'No payment provider account available'
        billing_log.error_code = 'no_provider'
        billing_log.save(update_fields=['error_message', 'error_code'])
        return False

    try:
        from subscriptions.provider_base import get_provider
        provider = get_provider(provider_account)

        charge_result = provider.charge_payment_token(
            token_id=subscription.airwallex_consent_id,
            amount=amount,
            currency='EUR',
            description=f'Spwig {subscription.hosted_plan.name} — {subscription.store_name}',
            metadata={
                'store_slug': subscription.store_slug,
                'plan': subscription.hosted_plan.slug,
                'cycle': billing_log.cycle_number,
            },
        )

        if charge_result.get('success'):
            billing_log.provider_response = charge_result
            billing_log.save(update_fields=['provider_response'])
            return True
        else:
            billing_log.error_message = charge_result.get('error', 'Charge failed')
            billing_log.error_code = charge_result.get('error_code', 'charge_failed')
            billing_log.provider_response = charge_result
            billing_log.save(update_fields=['error_message', 'error_code', 'provider_response'])
            return False

    except Exception as e:
        billing_log.error_message = str(e)[:500]
        billing_log.error_code = 'exception'
        billing_log.save(update_fields=['error_message', 'error_code'])
        logger.exception('Charge exception for %s: %s', subscription.store_slug, e)
        return False


def _send_billing_email(subscription, template_type, context):
    """Send a billing-related email using the email system."""
    try:
        from email_system.services.email_sender import EmailSendingService

        context.setdefault('name', subscription.name)

        outbox = EmailSendingService.send_template_email(
            to_email=subscription.email,
            template_type=template_type,
            context=context,
        )
        if outbox and outbox.status == 'queued':
            EmailSendingService.send_email(str(outbox.id))
    except Exception as e:
        logger.error(
            'Failed to send %s email to %s: %s',
            template_type, subscription.email, e,
        )


def _notify_status_change(subscription, account_status):
    """Notify the update server of a subscription status change."""
    try:
        from license_checkout.services import notify_update_server_subscription
        notify_update_server_subscription(
            event_type='subscription.updated',
            data={
                'license_key': subscription.license_key,
                'account_status': account_status,
            },
        )
    except Exception as e:
        logger.error(
            'Failed to notify update server of %s for %s: %s',
            account_status, subscription.store_slug, e,
        )
