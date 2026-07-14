"""
Loyalty Program Celery Tasks

Background tasks for campaign execution, journey processing, and scheduled campaigns.
"""

import logging
from datetime import timedelta

from celery import shared_task
from django.db.models import Q
from django.utils import timezone

from core.celery_utils import BackgroundDBTask

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    name="loyalty.trigger_campaign",
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def trigger_campaign(self, campaign_id: int, member_id: int, context: dict):
    """
    Execute a campaign for a specific member.

    Args:
        campaign_id: LoyaltyCampaign ID
        member_id: LoyaltyMember ID
        context: Execution context dict

    Returns:
        dict: Execution result
    """
    from loyalty.models import LoyaltyCampaign, LoyaltyCampaignExecution, LoyaltyMember
    from loyalty.services.campaign_orchestrator import CampaignOrchestrator

    try:
        campaign = LoyaltyCampaign.objects.get(id=campaign_id)
        member = LoyaltyMember.objects.select_related("customer", "balance", "current_tier").get(
            id=member_id
        )
    except (LoyaltyCampaign.DoesNotExist, LoyaltyMember.DoesNotExist) as e:
        logger.error(f"Campaign or member not found: {str(e)}")
        return {"success": False, "error": str(e)}

    # Find the execution record
    execution = (
        LoyaltyCampaignExecution.objects.filter(
            campaign=campaign, member=member, status=LoyaltyCampaignExecution.STATUS_PENDING
        )
        .order_by("-triggered_at")
        .first()
    )

    if not execution:
        logger.error(
            f"No pending execution found for campaign {campaign_id} and member {member_id}"
        )
        return {"success": False, "error": "No pending execution found"}

    try:
        orchestrator = CampaignOrchestrator()
        result = orchestrator.process_campaign_actions(execution)

        logger.info(f"Campaign {campaign_id} executed for member {member_id}")
        return {"success": True, "execution_id": execution.id, "result": result}

    except Exception as e:
        logger.error(f"Campaign execution failed: {str(e)}", exc_info=True)

        # Mark execution as failed
        execution.mark_failed(str(e))
        execution.retry_count = self.request.retries
        execution.save(update_fields=["retry_count"])

        # Update campaign statistics
        campaign.total_failed += 1
        campaign.save(update_fields=["total_failed"])

        # Retry if not max retries
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=60 * (2**self.request.retries))

        return {"success": False, "error": str(e), "execution_id": execution.id}


@shared_task(
    bind=True, name="loyalty.process_campaign_action", max_retries=3, default_retry_delay=30
)
def process_campaign_action(self, execution_id: int, action_data: dict):
    """
    Process a single campaign action.

    Args:
        execution_id: LoyaltyCampaignExecution ID
        action_data: Action configuration dict

    Returns:
        dict: Action result
    """
    from loyalty.models import LoyaltyCampaignExecution
    from loyalty.services.campaign_action_executor import CampaignActionExecutor

    try:
        execution = LoyaltyCampaignExecution.objects.select_related("member", "campaign").get(
            id=execution_id
        )
    except LoyaltyCampaignExecution.DoesNotExist:
        logger.error(f"Execution {execution_id} not found")
        return {"success": False, "error": "Execution not found"}

    try:
        executor = CampaignActionExecutor()
        result = executor.execute_action(
            action=action_data, member=execution.member, context=execution.trigger_context
        )

        logger.info(f"Action {action_data['type']} completed for execution {execution_id}")
        return result

    except Exception as e:
        logger.error(f"Action processing failed: {str(e)}", exc_info=True)

        if self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=30 * (2**self.request.retries))

        return {"success": False, "error": str(e)}


@shared_task(name="loyalty.process_scheduled_campaigns", ignore_result=True)
def process_scheduled_campaigns():
    """
    Process scheduled campaigns that are due to run.

    This task runs every minute via Celery Beat.

    Returns:
        dict: Processing summary
    """
    from loyalty.models import LoyaltyCampaign
    from loyalty.services.campaign_orchestrator import CampaignOrchestrator

    now = timezone.now()

    # Find scheduled campaigns that are active and due
    campaigns = LoyaltyCampaign.objects.filter(
        campaign_type=LoyaltyCampaign.TYPE_SCHEDULED,
        is_active=True,
        status=LoyaltyCampaign.STATUS_ACTIVE,
        start_date__lte=now,
    ).filter(Q(end_date__isnull=True) | Q(end_date__gte=now))

    processed = 0
    skipped = 0

    for campaign in campaigns:
        # Check if campaign should run now based on schedule
        if not _should_run_scheduled_campaign(campaign, now):
            skipped += 1
            continue

        # Get target members
        members = _get_campaign_target_members(campaign)

        # Trigger campaign for each member
        orchestrator = CampaignOrchestrator()
        for member in members:
            try:
                orchestrator.execute_campaign(
                    campaign=campaign,
                    member=member,
                    context={"scheduled": True, "scheduled_at": now.isoformat()},
                )
                processed += 1
            except Exception as e:
                logger.error(
                    f"Failed to trigger scheduled campaign {campaign.id} for member {member.id}: {str(e)}"
                )

    logger.info(f"Processed {processed} scheduled campaigns, skipped {skipped}")
    return {"processed": processed, "skipped": skipped}


@shared_task(name="loyalty.process_campaign_journey_steps", ignore_result=True)
def process_campaign_journey_steps():
    """
    Process pending journey steps that are due.

    This task runs every 5 minutes via Celery Beat.

    Returns:
        dict: Processing summary
    """
    from loyalty.models import LoyaltyCampaignExecution
    from loyalty.services.campaign_orchestrator import CampaignOrchestrator

    now = timezone.now()

    # Find executions with pending journey steps
    executions = LoyaltyCampaignExecution.objects.filter(
        status=LoyaltyCampaignExecution.STATUS_PROCESSING,
        next_step_at__lte=now,
        next_step_at__isnull=False,
    ).select_related("campaign", "member")[:100]  # Process 100 at a time

    if not executions:
        logger.debug("No pending journey steps to process")
        return None

    processed = 0
    failed = 0

    orchestrator = CampaignOrchestrator()

    for execution in executions:
        try:
            result = orchestrator.process_journey_step(execution.id, execution.current_step)
            if result.get("success"):
                processed += 1
            else:
                failed += 1
                logger.warning(
                    f"Journey step failed for execution {execution.id}: {result.get('error')}"
                )
        except Exception as e:
            logger.error(f"Failed to process journey step for execution {execution.id}: {str(e)}")
            failed += 1

    logger.info(f"Processed {processed} journey steps, failed {failed}")
    return {"processed": processed, "failed": failed}


@shared_task(name="loyalty.trigger_birthday_campaigns", ignore_result=True)
def trigger_birthday_campaigns():
    """
    Trigger birthday campaigns for members with birthdays today.

    This task runs daily at 9 AM via Celery Beat.

    Returns:
        dict: Processing summary
    """
    from django.db.models import Q

    from loyalty.models import LoyaltyCampaign, LoyaltyMember
    from loyalty.services.campaign_orchestrator import CampaignOrchestrator

    today = timezone.now().date()

    # Find birthday campaigns
    campaigns = LoyaltyCampaign.objects.filter(
        trigger_event=LoyaltyCampaign.EVENT_BIRTHDAY,
        is_active=True,
        status=LoyaltyCampaign.STATUS_ACTIVE,
    )

    if not campaigns.exists():
        return {"processed": 0, "message": "No birthday campaigns configured"}

    # Find members with birthdays today
    members = LoyaltyMember.objects.filter(
        Q(customer__date_of_birth__month=today.month) & Q(customer__date_of_birth__day=today.day),
        is_active=True,
    ).select_related("customer", "balance", "current_tier")

    processed = 0
    orchestrator = CampaignOrchestrator()

    for member in members:
        context = {"birthday": True, "birthday_date": today.isoformat()}

        result = orchestrator.trigger_event(
            event=LoyaltyCampaign.EVENT_BIRTHDAY, member=member, context=context
        )

        processed += result.get("triggered", 0)

    logger.info(f"Triggered birthday campaigns for {processed} members")
    return {"processed": processed, "members_with_birthdays": members.count()}


@shared_task(name="loyalty.trigger_expiring_points_campaigns", ignore_result=True)
def trigger_expiring_points_campaigns():
    """
    Trigger campaigns for members with points expiring soon.

    This task runs daily at 10 AM via Celery Beat.

    Returns:
        dict: Processing summary
    """
    from loyalty.models import LoyaltyCampaign, LoyaltyTransaction
    from loyalty.services.campaign_orchestrator import CampaignOrchestrator

    # Find campaigns for expiring points
    campaigns = LoyaltyCampaign.objects.filter(
        trigger_event=LoyaltyCampaign.EVENT_POINTS_EXPIRING,
        is_active=True,
        status=LoyaltyCampaign.STATUS_ACTIVE,
    )

    if not campaigns.exists():
        return {"processed": 0, "message": "No expiring points campaigns configured"}

    # Find transactions with points expiring in 30, 15, or 7 days
    processed = 0
    orchestrator = CampaignOrchestrator()

    for days in [30, 15, 7]:
        expiration_date = timezone.now() + timedelta(days=days)

        transactions = LoyaltyTransaction.objects.filter(
            expires_at__date=expiration_date.date(),
            transaction_type="earn",
            points_change__gt=0,
            is_active=True,
        ).select_related("member", "member__customer", "member__balance")

        for transaction in transactions:
            context = {
                "expiring_points": transaction.points_change,
                "expiration_date": transaction.expires_at.isoformat(),
                "days_until_expiration": days,
            }

            result = orchestrator.trigger_event(
                event=LoyaltyCampaign.EVENT_POINTS_EXPIRING,
                member=transaction.member,
                context=context,
            )

            processed += result.get("triggered", 0)

    logger.info(f"Triggered expiring points campaigns for {processed} members")
    return {"processed": processed}


# Helper functions


def _should_run_scheduled_campaign(campaign, now) -> bool:
    """
    Check if a scheduled campaign should run now.

    Args:
        campaign: LoyaltyCampaign instance
        now: Current datetime

    Returns:
        bool: True if campaign should run
    """
    schedule_type = campaign.schedule_type
    schedule_config = campaign.schedule_config or {}

    if schedule_type == "daily":
        # Run if hour matches
        target_hour = schedule_config.get("hour", 9)
        target_minute = schedule_config.get("minute", 0)
        return now.hour == target_hour and now.minute == target_minute

    elif schedule_type == "weekly":
        # Run if day_of_week and hour match
        target_day = schedule_config.get("day_of_week", 1)  # Monday
        target_hour = schedule_config.get("hour", 9)
        target_minute = schedule_config.get("minute", 0)
        return (
            now.weekday() == target_day and now.hour == target_hour and now.minute == target_minute
        )

    elif schedule_type == "monthly":
        # Run if day_of_month and hour match
        target_day = schedule_config.get("day_of_month", 1)
        target_hour = schedule_config.get("hour", 9)
        target_minute = schedule_config.get("minute", 0)
        return now.day == target_day and now.hour == target_hour and now.minute == target_minute

    return False


def _get_campaign_target_members(campaign):
    """
    Get members targeted by a campaign.

    Args:
        campaign: LoyaltyCampaign instance

    Returns:
        QuerySet: LoyaltyMember queryset
    """
    from loyalty.models import LoyaltyMember

    queryset = LoyaltyMember.objects.filter(is_active=True)

    # Apply targeting filters
    if not campaign.target_all_members:
        if campaign.target_segment:
            # Dynamic segment evaluation
            from loyalty.services.segmentation import SegmentEvaluator

            evaluator = SegmentEvaluator()
            queryset = evaluator.get_segment_members(campaign.target_segment)

        if campaign.target_tiers.exists():
            queryset = queryset.filter(current_tier__in=campaign.target_tiers.all())

    return queryset.select_related("customer", "balance", "current_tier")


@shared_task(name="loyalty.refresh_segment_memberships", base=BackgroundDBTask, ignore_result=True)
def refresh_segment_memberships():
    """
    Refresh all dynamic segment memberships.

    Evaluates segment rules and updates member assignments.
    Runs hourly via Celery Beat.

    Returns:
        dict: Summary of segments processed and membership changes
    """
    from loyalty.services.segment_evaluator import SegmentEvaluator

    logger.info("Starting segment membership refresh")

    try:
        evaluator = SegmentEvaluator()
        result = evaluator.refresh_all_segments()

        logger.info(
            f"Segment refresh complete: {result['segments_processed']} segments, "
            f"+{result['total_added']} members, -{result['total_removed']} members"
        )

        return result

    except Exception as e:
        logger.error(f"Error refreshing segment memberships: {e}", exc_info=True)
        raise


@shared_task(name="loyalty.refresh_single_segment")
def refresh_single_segment(segment_id: int):
    """
    Refresh memberships for a single segment.

    Args:
        segment_id: ID of segment to refresh

    Returns:
        dict: Summary of membership changes
    """
    from loyalty.models import LoyaltySegment
    from loyalty.services.segment_evaluator import SegmentEvaluator

    try:
        segment = LoyaltySegment.objects.get(id=segment_id)
        evaluator = SegmentEvaluator()
        result = evaluator.refresh_segment_memberships(segment)

        logger.info(
            f"Refreshed segment {segment.name}: "
            f"+{result['added']}, -{result['removed']}, total={result['total']}"
        )

        return result

    except LoyaltySegment.DoesNotExist:
        logger.error(f"Segment {segment_id} not found")
        raise
    except Exception as e:
        logger.error(f"Error refreshing segment {segment_id}: {e}", exc_info=True)
        raise


@shared_task(
    name="loyalty.calculate_campaign_statistics", base=BackgroundDBTask, ignore_result=True
)
def calculate_campaign_statistics():
    """
    Calculate and update campaign statistics.

    Updates completion rates, conversion rates, and other metrics for campaigns.
    Runs daily at 2 AM via Celery Beat.

    Returns:
        dict: Summary of campaigns processed
    """
    from loyalty.models import LoyaltyCampaign, LoyaltyCampaignExecution

    logger.info("Starting campaign statistics calculation")

    try:
        campaigns = LoyaltyCampaign.objects.filter(is_active=True)
        processed = 0

        for campaign in campaigns:
            # Calculate execution statistics
            executions = LoyaltyCampaignExecution.objects.filter(campaign=campaign)

            total_executions = executions.count()
            if total_executions == 0:
                continue

            completed = executions.filter(status=LoyaltyCampaignExecution.STATUS_COMPLETED).count()

            failed = executions.filter(status=LoyaltyCampaignExecution.STATUS_FAILED).count()

            # Update campaign stats
            campaign.total_executions = total_executions
            campaign.successful_executions = completed
            campaign.failed_executions = failed

            # Calculate completion rate
            if total_executions > 0:
                campaign.completion_rate = (completed / total_executions) * 100
            else:
                campaign.completion_rate = 0

            campaign.save(
                update_fields=[
                    "total_executions",
                    "successful_executions",
                    "failed_executions",
                    "completion_rate",
                ]
            )

            processed += 1

        logger.info(f"Updated statistics for {processed} campaigns")

        return {"processed": processed, "message": f"Updated statistics for {processed} campaigns"}

    except Exception as e:
        logger.error(f"Error calculating campaign statistics: {e}", exc_info=True)
        raise
