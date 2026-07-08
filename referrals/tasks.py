"""
Referral Program Celery Tasks

Background tasks for reward expiry, attribution management, and stats aggregation.
"""

from celery import shared_task
from django.utils import timezone
from django.db.models import Q, Sum, Count
from core.celery_utils import BackgroundDBTask
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task(name='referrals.send_reward_expiry_reminders', ignore_result=True)
def send_reward_expiry_reminders():
    """
    Send email reminders for rewards expiring soon.

    Sends reminder emails 7 days before reward expiration.
    Runs daily at 10 AM via Celery Beat.

    Returns:
        dict: Summary of emails sent
    """
    from .models import ReferralReward, ReferralProgram
    from .services.email_notifications import send_reward_expiring_email

    logger.info("Starting reward expiry reminder task")

    # Check if program is active
    try:
        program = ReferralProgram.get_program()
        if not program or not program.is_active():
            return {'sent': 0, 'message': 'Referral program not active'}
    except Exception:
        return {'sent': 0, 'message': 'Referral program not configured'}

    # Find rewards expiring in 7 days
    seven_days_from_now = timezone.now() + timedelta(days=7)
    target_date = seven_days_from_now.date()

    rewards = ReferralReward.objects.filter(
        status='issued',
        expires_at__date=target_date,
        expires_at__isnull=False
    ).select_related('customer')

    sent = 0
    failed = 0

    for reward in rewards:
        try:
            success = send_reward_expiring_email(reward, days_until_expiration=7)
            if success:
                sent += 1
                logger.info(f"Sent expiry reminder for reward {reward.id} to {reward.customer.email}")
            else:
                failed += 1
                logger.warning(f"Failed to send expiry reminder for reward {reward.id}")
        except Exception as e:
            failed += 1
            logger.error(f"Error sending expiry reminder for reward {reward.id}: {e}", exc_info=True)

    logger.info(f"Expiry reminders complete: {sent} sent, {failed} failed")
    return {
        'sent': sent,
        'failed': failed,
        'total_expiring': rewards.count()
    }


@shared_task(name='referrals.expire_old_rewards', base=BackgroundDBTask, ignore_result=True)
def expire_old_rewards():
    """
    Mark expired rewards as expired and update stats.

    Runs daily at 1 AM via Celery Beat.

    Returns:
        dict: Summary of rewards expired
    """
    from .models import ReferralReward

    logger.info("Starting reward expiry cleanup task")

    now = timezone.now()

    # Find expired rewards that are still marked as issued
    expired_rewards = ReferralReward.objects.filter(
        status='issued',
        expires_at__lt=now,
        expires_at__isnull=False
    )

    count = expired_rewards.count()

    if count == 0:
        return {'expired': 0, 'message': 'No rewards to expire'}

    # Mark as expired
    expired_rewards.update(status='expired')

    logger.info(f"Marked {count} rewards as expired")
    return {
        'expired': count,
        'message': f'Marked {count} rewards as expired'
    }


@shared_task(name='referrals.expire_old_attributions', base=BackgroundDBTask, ignore_result=True)
def expire_old_attributions():
    """
    Mark pending attributions as expired if they exceed the review period.

    Default review period: 30 days from creation.
    Runs daily at 2 AM via Celery Beat.

    Returns:
        dict: Summary of attributions expired
    """
    from .models import ReferralAttribution, ReferralProgram

    logger.info("Starting attribution expiry task")

    # Get program settings
    try:
        program = ReferralProgram.get_program()
        if not program:
            return {'expired': 0, 'message': 'Referral program not configured'}
    except Exception:
        return {'expired': 0, 'message': 'Referral program not configured'}

    # Get review period from fraud policy (default 30 days)
    review_period_days = program.fraud_policy.get('attribution_review_period_days', 30)
    cutoff_date = timezone.now() - timedelta(days=review_period_days)

    # Find pending attributions older than review period
    expired_attributions = ReferralAttribution.objects.filter(
        status='pending',
        created_at__lt=cutoff_date
    )

    count = expired_attributions.count()

    if count == 0:
        return {'expired': 0, 'message': 'No attributions to expire'}

    # Mark as expired
    for attribution in expired_attributions:
        attribution.reject(
            reason='other',
            notes=f'Automatically expired after {review_period_days} days pending review'
        )

    logger.info(f"Expired {count} pending attributions")
    return {
        'expired': count,
        'review_period_days': review_period_days,
        'message': f'Expired {count} attributions older than {review_period_days} days'
    }


@shared_task(name='referrals.update_referrer_stats', base=BackgroundDBTask, ignore_result=True)
def update_referrer_stats():
    """
    Update aggregated statistics for referrer identities.

    Recalculates total conversions, rewards earned, etc.
    Runs every 6 hours via Celery Beat.

    Returns:
        dict: Summary of stats updated
    """
    from .models import ReferralIdentity, ReferralAttribution, ReferralReward
    from django.db.models import Q

    logger.info("Starting referrer stats update task")

    identities = ReferralIdentity.objects.all()
    updated = 0

    for identity in identities:
        try:
            # Count total approved attributions
            total_conversions = ReferralAttribution.objects.filter(
                referrer_identity=identity,
                status='approved'
            ).count()

            # Sum total rewards earned (only issued/redeemed rewards)
            total_rewards = ReferralReward.objects.filter(
                referrer_identity=identity,
                recipient_type='referrer',
                status__in=['issued', 'redeemed']
            ).aggregate(
                total=Sum('amount')
            )['total'] or 0

            # Update identity stats if changed
            if (identity.total_conversions != total_conversions or
                    identity.total_rewards_earned != float(total_rewards)):

                identity.total_conversions = total_conversions
                identity.total_rewards_earned = float(total_rewards)
                identity.save(update_fields=['total_conversions', 'total_rewards_earned'])

                updated += 1
                logger.debug(f"Updated stats for identity {identity.id}: {total_conversions} conversions, {total_rewards} rewards")

        except Exception as e:
            logger.error(f"Error updating stats for identity {identity.id}: {e}", exc_info=True)

    logger.info(f"Updated stats for {updated} identities")
    return {
        'updated': updated,
        'total_identities': identities.count(),
        'message': f'Updated stats for {updated}/{identities.count()} identities'
    }


@shared_task(name='referrals.fraud_check_batch_process', base=BackgroundDBTask, ignore_result=True)
def fraud_check_batch_process():
    """
    Re-evaluate high-risk pending attributions with updated fraud checks.

    Reviews attributions with risk score > 70 that have been pending for 24+ hours.
    Runs daily at 3 AM via Celery Beat.

    Returns:
        dict: Summary of attributions processed
    """
    from .models import ReferralAttribution, ReferralProgram
    from .services.validation import validate_attribution

    logger.info("Starting fraud check batch process")

    # Get program settings
    try:
        program = ReferralProgram.get_program()
        if not program or not program.is_active():
            return {'processed': 0, 'message': 'Referral program not active'}
    except Exception:
        return {'processed': 0, 'message': 'Referral program not configured'}

    # Find high-risk pending attributions (24+ hours old)
    cutoff_time = timezone.now() - timedelta(hours=24)
    high_risk_threshold = 70

    attributions = ReferralAttribution.objects.filter(
        status='pending',
        risk_score__gte=high_risk_threshold,
        created_at__lt=cutoff_time
    )[:100]  # Process 100 at a time

    processed = 0
    auto_approved = 0
    auto_rejected = 0

    for attribution in attributions:
        try:
            # Re-run validation
            is_valid, validation_data, new_risk_score = validate_attribution(attribution)

            # Update validation data and risk score
            attribution.validation_data = validation_data
            old_risk_score = attribution.risk_score
            attribution.risk_score = new_risk_score
            attribution.save(update_fields=['validation_data', 'risk_score'])

            logger.info(f"Re-evaluated attribution {attribution.id}: risk {old_risk_score} → {new_risk_score}")

            # Auto-reject if very high risk
            if not is_valid or new_risk_score >= 90:
                attribution.reject(
                    reason='fraud_risk',
                    notes=f'Automatically rejected: risk score {new_risk_score} (threshold: 90)'
                )
                auto_rejected += 1
                logger.warning(f"Auto-rejected attribution {attribution.id} due to high risk ({new_risk_score})")

            # Auto-approve if risk dropped significantly
            elif new_risk_score < program.fraud_policy.get('auto_approve_threshold', 30):
                from .services.rewards import create_rewards, issue_reward

                attribution.approve()
                auto_approved += 1
                logger.info(f"Auto-approved attribution {attribution.id} after risk decrease")

                # Create and issue rewards
                try:
                    referrer_reward, referee_reward = create_rewards(attribution)

                    if referrer_reward:
                        issue_reward(referrer_reward)
                    if referee_reward:
                        issue_reward(referee_reward)
                except Exception as e:
                    logger.error(f"Error issuing rewards for attribution {attribution.id}: {e}")

            processed += 1

        except Exception as e:
            logger.error(f"Error processing attribution {attribution.id}: {e}", exc_info=True)

    logger.info(f"Fraud check complete: {processed} processed, {auto_approved} approved, {auto_rejected} rejected")
    return {
        'processed': processed,
        'auto_approved': auto_approved,
        'auto_rejected': auto_rejected,
        'message': f'Processed {processed} high-risk attributions'
    }


@shared_task(name='referrals.cleanup_old_events', base=BackgroundDBTask, ignore_result=True)
def cleanup_old_events():
    """
    Clean up old referral events to prevent database bloat.

    Deletes event logs older than 90 days (configurable).
    Runs weekly on Sunday at 4 AM via Celery Beat.

    Returns:
        dict: Summary of events deleted
    """
    from .models import ReferralEvent, ReferralProgram

    logger.info("Starting old events cleanup task")

    # Get retention period from settings (default 90 days)
    try:
        program = ReferralProgram.get_program()
        retention_days = program.settings.get('event_retention_days', 90) if program else 90
    except Exception:
        retention_days = 90

    cutoff_date = timezone.now() - timedelta(days=retention_days)

    # Delete old events (keep click, signup, order events for analytics)
    # Only delete view/other low-priority events
    old_events = ReferralEvent.objects.filter(
        created_at__lt=cutoff_date,
        event_type__in=['view', 'share']  # Keep important events like click, signup, order
    )

    count = old_events.count()

    if count == 0:
        return {'deleted': 0, 'message': 'No events to clean up'}

    deleted = old_events.delete()[0]

    logger.info(f"Deleted {deleted} old events (older than {retention_days} days)")
    return {
        'deleted': deleted,
        'retention_days': retention_days,
        'message': f'Deleted {deleted} events older than {retention_days} days'
    }


@shared_task(
    bind=True,
    name='referrals.process_attribution',
    max_retries=3,
    default_retry_delay=300,  # 5 minutes
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=1800,  # 30 minutes
    retry_jitter=True
)
def process_attribution(self, attribution_id: int):
    """
    Process a specific attribution asynchronously.

    Useful for manual admin actions or delayed processing.

    Args:
        attribution_id: ReferralAttribution ID

    Returns:
        dict: Processing result
    """
    from .models import ReferralAttribution
    from .services.validation import validate_attribution
    from .services.rewards import create_rewards, issue_reward

    try:
        attribution = ReferralAttribution.objects.get(id=attribution_id)
    except ReferralAttribution.DoesNotExist:
        logger.error(f"Attribution {attribution_id} not found")
        return {'success': False, 'error': 'Attribution not found'}

    try:
        # Run validation
        is_valid, validation_data, risk_score = validate_attribution(attribution)

        attribution.validation_data = validation_data
        attribution.risk_score = risk_score
        attribution.save(update_fields=['validation_data', 'risk_score'])

        if is_valid and attribution.status == 'approved':
            # Create and issue rewards
            referrer_reward, referee_reward = create_rewards(attribution)

            if referrer_reward:
                success = issue_reward(referrer_reward)
                if not success:
                    logger.error(f"Failed to issue referrer reward for attribution {attribution_id}")

            if referee_reward:
                success = issue_reward(referee_reward)
                if not success:
                    logger.error(f"Failed to issue referee reward for attribution {attribution_id}")

            logger.info(f"Processed attribution {attribution_id} successfully")
            return {
                'success': True,
                'attribution_id': attribution_id,
                'risk_score': risk_score
            }
        else:
            logger.info(f"Attribution {attribution_id} validation failed or not approved")
            return {
                'success': False,
                'attribution_id': attribution_id,
                'error': 'Validation failed or not approved',
                'risk_score': risk_score
            }

    except Exception as e:
        logger.error(f"Error processing attribution {attribution_id}: {e}", exc_info=True)

        # Retry if not max retries
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=300 * (2 ** self.request.retries))

        return {
            'success': False,
            'attribution_id': attribution_id,
            'error': str(e)
        }
