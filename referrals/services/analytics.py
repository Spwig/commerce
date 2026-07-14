"""
Referral Program Analytics Service

Provides aggregated statistics and metrics for dashboard widgets.
"""

from datetime import timedelta
from decimal import Decimal

from django.db.models import Avg, Count, Q, Sum
from django.utils import timezone

from ..models import (
    ReferralAttribution,
    ReferralEvent,
    ReferralIdentity,
    ReferralProgram,
    ReferralReward,
)


def get_referral_dashboard_stats(start_date=None, end_date=None):
    """
    Get comprehensive referral program statistics for dashboard widget.

    Args:
        start_date (datetime, optional): Start of date range
        end_date (datetime, optional): End of date range

    Returns:
        dict: Dashboard statistics including:
            - pending_attributions: Count of attributions awaiting review
            - pending_rewards: Count of rewards awaiting issuance
            - high_risk_attributions: Count of attributions with high risk scores
            - total_referrers: Active referrers count
            - total_conversions: Successful referral conversions
            - total_rewards_issued: Monetary value of issued rewards
            - conversion_rate: Click-to-conversion percentage
            - avg_risk_score: Average risk score of pending attributions
            - top_referrers: List of top 5 referrers by conversions
            - recent_activity: Recent referral events
    """
    # Get active program
    program = ReferralProgram.get_program()

    if not program:
        return _empty_stats()

    # Set default date range if not provided (last 30 days)
    if not end_date:
        end_date = timezone.now()
    if not start_date:
        start_date = end_date - timedelta(days=30)

    # Filter querysets by date range
    attributions_qs = ReferralAttribution.objects.filter(created_at__range=(start_date, end_date))
    rewards_qs = ReferralReward.objects.filter(created_at__range=(start_date, end_date))
    events_qs = ReferralEvent.objects.filter(created_at__range=(start_date, end_date))

    # Action cards - items requiring attention
    pending_attributions = ReferralAttribution.objects.filter(status="pending").count()

    pending_rewards = ReferralReward.objects.filter(status="pending").count()

    high_risk_attributions = ReferralAttribution.objects.filter(
        status="pending", risk_score__gte=70
    ).count()

    expiring_rewards = ReferralReward.objects.filter(
        status="issued",
        expires_at__isnull=False,
        expires_at__lte=timezone.now() + timedelta(days=7),
        expires_at__gte=timezone.now(),
    ).count()

    # Overall metrics
    total_referrers = (
        ReferralIdentity.objects.filter(referrals_made__created_at__range=(start_date, end_date))
        .distinct()
        .count()
    )

    total_conversions = attributions_qs.filter(status="approved").count()

    total_rewards_value = rewards_qs.filter(status__in=["issued", "redeemed"]).aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0.00")

    # Conversion rate (clicks to conversions)
    total_clicks = events_qs.filter(event_type="click").count()
    conversion_rate = 0
    if total_clicks > 0:
        conversion_rate = round((total_conversions / total_clicks) * 100, 2)

    # Average risk score of pending attributions
    avg_risk_score = (
        ReferralAttribution.objects.filter(status="pending").aggregate(avg=Avg("risk_score"))["avg"]
        or 0
    )

    # Top 5 referrers by approved conversions (in date range)
    top_referrers = list(
        ReferralIdentity.objects.filter(
            referrals_made__created_at__range=(start_date, end_date),
            referrals_made__status="approved",
        )
        .annotate(
            conversions=Count(
                "referrals_made",
                filter=Q(
                    referrals_made__status="approved",
                    referrals_made__created_at__range=(start_date, end_date),
                ),
            ),
            total_rewards=Sum(
                "referrals_made__rewards__amount",
                filter=Q(
                    referrals_made__rewards__status__in=["issued", "redeemed"],
                    referrals_made__created_at__range=(start_date, end_date),
                ),
            ),
        )
        .filter(conversions__gt=0)
        .order_by("-conversions")[:5]
        .values(
            "id",
            "customer__first_name",
            "customer__last_name",
            "customer__email",
            "conversions",
            "total_rewards",
        )
    )

    # Recent activity (last 10 events in date range)
    recent_activity = list(
        events_qs.select_related("referrer_identity__customer")
        .order_by("-created_at")[:10]
        .values(
            "event_type",
            "created_at",
            "referrer_identity__customer__email",
            "referrer_identity__customer__first_name",
            "referrer_identity__customer__last_name",
        )
    )

    # Referral funnel metrics
    funnel_clicks = events_qs.filter(event_type="click").count()
    funnel_signups = events_qs.filter(event_type="signup").count()
    funnel_orders = events_qs.filter(event_type="order").count()
    funnel_conversions = total_conversions

    return {
        # Action cards
        "pending_attributions": pending_attributions,
        "pending_rewards": pending_rewards,
        "high_risk_attributions": high_risk_attributions,
        "expiring_rewards": expiring_rewards,
        # Overall metrics
        "total_referrers": total_referrers,
        "total_conversions": total_conversions,
        "total_rewards_value": float(total_rewards_value),
        "conversion_rate": conversion_rate,
        "avg_risk_score": round(avg_risk_score, 1),
        # Top performers
        "top_referrers": top_referrers,
        # Recent activity
        "recent_activity": recent_activity,
        # Funnel metrics
        "funnel": {
            "clicks": funnel_clicks,
            "signups": funnel_signups,
            "orders": funnel_orders,
            "conversions": funnel_conversions,
        },
        # Program info
        "program_active": program.is_active() if program else False,
        "program_name": program.name if program else None,
    }


def _empty_stats():
    """Return empty stats when no program exists."""
    return {
        "pending_attributions": 0,
        "pending_rewards": 0,
        "high_risk_attributions": 0,
        "expiring_rewards": 0,
        "total_referrers": 0,
        "total_conversions": 0,
        "total_rewards_value": 0.0,
        "conversion_rate": 0,
        "avg_risk_score": 0,
        "top_referrers": [],
        "recent_activity": [],
        "funnel": {
            "clicks": 0,
            "signups": 0,
            "orders": 0,
            "conversions": 0,
        },
        "program_active": False,
        "program_name": None,
    }


def get_referral_performance_over_time(start_date, end_date, grouping="day"):
    """
    Get referral performance metrics over time for charts.

    Args:
        start_date (datetime): Start of date range
        end_date (datetime): End of date range
        grouping (str): Time grouping ('day', 'week', 'month')

    Returns:
        dict: Time series data with:
            - labels: Time period labels
            - clicks: Click counts per period
            - signups: Signup counts per period
            - conversions: Conversion counts per period
            - rewards_value: Total reward value per period
    """
    from django.db.models.functions import TruncDay, TruncMonth, TruncWeek

    # Determine truncation function
    if grouping == "week":
        trunc_func = TruncWeek
    elif grouping == "month":
        trunc_func = TruncMonth
    else:  # day
        trunc_func = TruncDay

    # Get click events grouped by time
    clicks_data = list(
        ReferralEvent.objects.filter(event_type="click", created_at__range=(start_date, end_date))
        .annotate(period=trunc_func("created_at"))
        .values("period")
        .annotate(count=Count("id"))
        .order_by("period")
    )

    # Get signup events grouped by time
    signups_data = list(
        ReferralEvent.objects.filter(event_type="signup", created_at__range=(start_date, end_date))
        .annotate(period=trunc_func("created_at"))
        .values("period")
        .annotate(count=Count("id"))
        .order_by("period")
    )

    # Get approved conversions grouped by time
    conversions_data = list(
        ReferralAttribution.objects.filter(
            status="approved", created_at__range=(start_date, end_date)
        )
        .annotate(period=trunc_func("created_at"))
        .values("period")
        .annotate(count=Count("id"))
        .order_by("period")
    )

    # Get rewards value grouped by time
    rewards_data = list(
        ReferralReward.objects.filter(
            status__in=["issued", "redeemed"], created_at__range=(start_date, end_date)
        )
        .annotate(period=trunc_func("created_at"))
        .values("period")
        .annotate(total=Sum("amount"))
        .order_by("period")
    )

    # Merge all data into unified time series
    # Create a set of all periods
    all_periods = set()
    for item in clicks_data:
        all_periods.add(item["period"])
    for item in signups_data:
        all_periods.add(item["period"])
    for item in conversions_data:
        all_periods.add(item["period"])
    for item in rewards_data:
        all_periods.add(item["period"])

    all_periods = sorted(all_periods)

    # Build lookup dicts
    clicks_dict = {item["period"]: item["count"] for item in clicks_data}
    signups_dict = {item["period"]: item["count"] for item in signups_data}
    conversions_dict = {item["period"]: item["count"] for item in conversions_data}
    rewards_dict = {item["period"]: float(item["total"]) for item in rewards_data}

    # Build final arrays
    labels = []
    clicks = []
    signups = []
    conversions = []
    rewards_value = []

    for period in all_periods:
        # Format label based on grouping
        if grouping == "month":
            labels.append(period.strftime("%b %Y"))
        elif grouping == "week":
            labels.append(period.strftime("%Y-W%W"))
        else:  # day
            labels.append(period.strftime("%b %d"))

        clicks.append(clicks_dict.get(period, 0))
        signups.append(signups_dict.get(period, 0))
        conversions.append(conversions_dict.get(period, 0))
        rewards_value.append(rewards_dict.get(period, 0.0))

    return {
        "labels": labels,
        "clicks": clicks,
        "signups": signups,
        "conversions": conversions,
        "rewards_value": rewards_value,
        "grouping": grouping,
    }
