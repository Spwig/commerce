"""
Affiliate App Celery Tasks

Background tasks for affiliate program automation.
"""

import logging
from datetime import timedelta
from decimal import Decimal

from celery import shared_task
from django.contrib.sites.models import Site
from django.db.models import Sum
from django.utils import timezone

from core.celery_utils import BackgroundDBTask

logger = logging.getLogger(__name__)


@shared_task(
    name="affiliate.send_affiliate_monthly_reports", base=BackgroundDBTask, ignore_result=True
)
def send_affiliate_monthly_reports():
    """
    Send monthly performance reports to all active affiliates.

    Pattern: Similar to blog/tasks.py send_monthly_digest()
    Runs every hour via Celery Beat, but only sends on configured day/hour.

    Returns:
        dict: Summary of emails sent and skipped
    """
    from affiliate.models import Affiliate, AffiliateReportSettings, Commission
    from email_system.services.email_sender import EmailSendingService

    # Get settings
    settings = AffiliateReportSettings.get_settings()

    # Check if reports are enabled
    if not settings.monthly_report_enabled:
        logger.info("Monthly affiliate reports disabled in settings")
        return {"sent": 0, "skipped": 0, "reason": "disabled"}

    # Check if today is the configured send day
    today = timezone.now()
    if today.day != settings.monthly_report_day:
        logger.debug(
            f"Not send day (today: {today.day}, configured: {settings.monthly_report_day})"
        )
        return {"sent": 0, "skipped": 0, "reason": "not_send_day"}

    # Check if current hour matches configured send hour (UTC)
    if today.hour != settings.monthly_report_hour:
        logger.debug(
            f"Not send hour (now: {today.hour}, configured: {settings.monthly_report_hour})"
        )
        return {"sent": 0, "skipped": 0, "reason": "not_send_hour"}

    # Calculate previous month date range
    first_day_this_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_last_month = first_day_this_month - timedelta(days=1)
    first_day_last_month = last_day_last_month.replace(day=1)

    month_name = last_day_last_month.strftime("%B")
    year = last_day_last_month.year

    logger.info(f"Sending affiliate monthly reports for {month_name} {year}")

    # Get site
    site = Site.objects.get(pk=1)

    # Get all active affiliates
    affiliates = Affiliate.objects.filter(status="active").select_related("user")

    sent_count = 0
    skipped_count = 0

    for affiliate in affiliates:
        try:
            # Check communication preferences
            if hasattr(affiliate.user, "communication_preferences"):
                prefs = affiliate.user.communication_preferences
                if not prefs.should_send_email("affiliate_monthly_report"):
                    logger.debug(f"Skipping {affiliate.user.email} - preference disabled")
                    skipped_count += 1
                    continue

            # Aggregate commissions for last month
            commissions = Commission.objects.filter(
                affiliate=affiliate,
                created_at__gte=first_day_last_month,
                created_at__lt=first_day_this_month,
                status__in=["approved", "paid"],
            )

            total_earned = commissions.aggregate(Sum("amount"))["amount__sum"] or Decimal("0.00")
            commission_count = commissions.count()

            # Skip if no activity
            if commission_count == 0:
                logger.debug(f"Skipping {affiliate.user.email} - no commissions this month")
                skipped_count += 1
                continue

            avg_commission = (
                total_earned / commission_count if commission_count > 0 else Decimal("0.00")
            )

            # Get top N orders by commission amount
            top_orders_data = []
            top_orders = commissions.select_related("order").order_by("-amount")[
                : settings.include_top_orders_count
            ]

            for commission in top_orders:
                top_orders_data.append(
                    {
                        "order_number": commission.order.order_number,
                        "commission_amount": f"${commission.amount:.2f}",
                        "order_date": commission.order.created_at.strftime("%b %d, %Y"),
                    }
                )

            # Calculate pending balance (all approved but unpaid commissions)
            pending_balance = Commission.objects.filter(
                affiliate=affiliate, status="approved"
            ).aggregate(Sum("amount"))["amount__sum"] or Decimal("0.00")

            # Determine payment status
            from affiliate.models import Payout

            latest_payout = (
                Payout.objects.filter(affiliate=affiliate).order_by("-created_at").first()
            )

            if latest_payout:
                if latest_payout.status == "pending":
                    payment_status = "Payout Pending"
                    next_payout_date = None
                elif latest_payout.status == "processing":
                    payment_status = "Payout Processing"
                    next_payout_date = None
                elif latest_payout.status == "completed":
                    payment_status = "Last payout completed"
                    next_payout_date = None
                else:
                    payment_status = "No pending payout"
                    next_payout_date = None
            else:
                payment_status = "No payouts yet"
                next_payout_date = None

            # Build email context
            context = {
                "affiliate_name": affiliate.user.get_full_name() or affiliate.user.email,
                "month_name": month_name,
                "year": year,
                "total_earned": f"${total_earned:.2f}",
                "commission_count": commission_count,
                "avg_commission": f"${avg_commission:.2f}",
                "top_orders": top_orders_data,
                "top_orders_count": len(top_orders_data),
                "pending_balance": f"${pending_balance:.2f}",
                "payment_status": payment_status,
                "next_payout_date": next_payout_date,
                "portal_url": f"https://{site.domain}/affiliate/dashboard/",
                "shop_name": site.name,
                "support_email": f"support@{site.domain}",
            }

            # Get user's language preference
            from email_system.utils.language import get_user_email_language

            language = get_user_email_language(affiliate.user)

            # Send email via EmailSendingService (handles preference checking)
            outbox = EmailSendingService.send_template_email(
                to_email=affiliate.user.email,
                template_type="affiliate_monthly_report",
                context=context,
                language=language,
            )

            if outbox.status == "skipped":
                logger.info(
                    f"Skipped monthly report to {affiliate.user.email} - preference disabled"
                )
                skipped_count += 1
            elif outbox.status in ["pending", "queued"]:
                logger.info(f"Queued monthly report to {affiliate.user.email}")
                sent_count += 1
            else:
                logger.warning(
                    f"Failed to queue monthly report to {affiliate.user.email}: {outbox.status}"
                )
                skipped_count += 1

        except Exception as e:
            logger.error(
                f"Error sending monthly report to {affiliate.user.email}: {e}", exc_info=True
            )
            skipped_count += 1
            continue

    logger.info(f"Affiliate monthly reports complete: {sent_count} sent, {skipped_count} skipped")
    return {"sent": sent_count, "skipped": skipped_count, "month": month_name, "year": year}
