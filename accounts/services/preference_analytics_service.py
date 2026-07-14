"""
Preference Analytics Service

Provides analytics and metrics for communication preferences including:
- Opt-in rates and trends
- Verification rates
- App preference breakdowns
- Conversion funnels
"""

import logging
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone

logger = logging.getLogger(__name__)
User = get_user_model()


class PreferenceAnalyticsService:
    """
    Service for generating preference analytics and metrics.

    Mirrors the pattern from payment_providers/services/analytics_service.py.
    """

    @classmethod
    def get_date_range_for_period(
        cls, period: str, start_date: datetime | None = None, end_date: datetime | None = None
    ) -> tuple[datetime, datetime]:
        """
        Get date range for a given period.

        Args:
            period: 'today', 'last_7_days', 'last_30_days', 'this_month',
                   'last_quarter', 'this_year', 'custom'
            start_date: Start date for 'custom' period
            end_date: End date for 'custom' period

        Returns:
            Tuple of (start_datetime, end_datetime)
        """
        now = timezone.now()

        if period == "today":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now

        elif period == "last_7_days":
            start = now - timedelta(days=7)
            end = now

        elif period == "last_30_days":
            start = now - timedelta(days=30)
            end = now

        elif period == "this_month":
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end = now

        elif period == "last_quarter":
            # Get current quarter
            current_quarter = (now.month - 1) // 3 + 1
            # Previous quarter
            prev_quarter = current_quarter - 1 if current_quarter > 1 else 4
            prev_year = now.year if current_quarter > 1 else now.year - 1
            # Start of previous quarter
            start_month = (prev_quarter - 1) * 3 + 1
            start = datetime(prev_year, start_month, 1, tzinfo=now.tzinfo)
            # End of previous quarter
            end_month = start_month + 2
            if end_month == 12:
                end = datetime(prev_year, 12, 31, 23, 59, 59, tzinfo=now.tzinfo)
            else:
                end = datetime(prev_year, end_month + 1, 1, tzinfo=now.tzinfo) - timedelta(
                    seconds=1
                )

        elif period == "this_year":
            start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end = now

        elif period == "custom":
            if not start_date or not end_date:
                raise ValueError("start_date and end_date required for custom period")
            start = start_date
            end = end_date

        else:
            raise ValueError(f"Invalid period: {period}")

        return (start, end)

    @classmethod
    def get_action_cards(cls) -> dict:
        """
        Get action card metrics for dashboard.

        Returns:
            Dict with counts for:
            - Unverified users
            - Recent unsubscribes
            - Pending verifications
            - Total active subscribers
        """
        from accounts.models import CommunicationPreference, PreferenceChangeLog

        # Unverified users (email marketing enabled but not verified)
        unverified_count = CommunicationPreference.objects.filter(
            email_marketing=True, email_verified=False
        ).count()

        # Recent unsubscribes (last 7 days)
        week_ago = timezone.now() - timedelta(days=7)
        recent_unsubscribes = PreferenceChangeLog.objects.filter(
            action="unsubscribe_all", timestamp__gte=week_ago
        ).count()

        # Pending verifications (code sent but not verified).
        # sms_verification_code is CharField(default=""), never NULL —
        # use ~Q("") instead of __isnull=False so we count actual pending
        # SMS verifications rather than every preference row.
        pending_verifications = CommunicationPreference.objects.filter(
            ~Q(sms_verification_code="") | Q(email_verified=False, email_marketing=True)
        ).count()

        # Total active subscribers (email marketing enabled and verified)
        active_subscribers = CommunicationPreference.objects.filter(
            email_marketing=True, email_verified=True
        ).count()

        return {
            "unverified_users": unverified_count,
            "recent_unsubscribes": recent_unsubscribes,
            "pending_verifications": pending_verifications,
            "total_subscribers": active_subscribers,
        }

    @classmethod
    def get_opt_in_metrics(
        cls, start_date: datetime, end_date: datetime, compare: bool = False
    ) -> dict:
        """
        Get opt-in metrics for a period.

        Args:
            start_date: Start of period
            end_date: End of period
            compare: If True, include comparison with previous period

        Returns:
            Dict with:
            - total_users
            - marketing_opted_in (count and percentage)
            - email_verified (count and percentage)
            - sms_opted_in (count and percentage)
            - previous_period (if compare=True)
            - changes (if compare=True)
        """
        from accounts.models import CommunicationPreference

        # Current period metrics
        total_users = User.objects.filter(date_joined__lte=end_date).count()

        prefs = CommunicationPreference.objects.filter(created_at__lte=end_date)

        marketing_count = prefs.filter(email_marketing=True).count()
        verified_count = prefs.filter(email_verified=True).count()
        sms_count = prefs.filter(sms_marketing=True).count()

        metrics = {
            "total_users": total_users,
            "marketing_opted_in": {
                "count": marketing_count,
                "percentage": (marketing_count / total_users * 100) if total_users > 0 else 0,
            },
            "email_verified": {
                "count": verified_count,
                "percentage": (verified_count / total_users * 100) if total_users > 0 else 0,
            },
            "sms_opted_in": {
                "count": sms_count,
                "percentage": (sms_count / total_users * 100) if total_users > 0 else 0,
            },
        }

        # Comparison with previous period
        if compare:
            duration = end_date - start_date
            prev_end = start_date
            prev_end - duration

            prev_total = User.objects.filter(date_joined__lte=prev_end).count()
            prev_prefs = CommunicationPreference.objects.filter(created_at__lte=prev_end)

            prev_marketing = prev_prefs.filter(email_marketing=True).count()
            prev_verified = prev_prefs.filter(email_verified=True).count()
            prev_sms = prev_prefs.filter(sms_marketing=True).count()

            metrics["previous_period"] = {
                "total_users": prev_total,
                "marketing_opted_in": prev_marketing,
                "email_verified": prev_verified,
                "sms_opted_in": prev_sms,
            }

            metrics["changes"] = {
                "total_users": cls._calculate_change(total_users, prev_total),
                "marketing_opted_in": cls._calculate_change(marketing_count, prev_marketing),
                "email_verified": cls._calculate_change(verified_count, prev_verified),
                "sms_opted_in": cls._calculate_change(sms_count, prev_sms),
            }

        return metrics

    @classmethod
    def get_app_preference_breakdown(cls) -> dict:
        """
        Get breakdown of app preferences for pie chart.

        Returns:
            Dict with app names and enabled counts
        """
        from accounts.models import CommunicationPreference

        prefs = CommunicationPreference.objects.all()

        breakdown = {
            "blog": 0,
            "loyalty": 0,
            "referrals": 0,
            "affiliate": 0,
        }

        for pref in prefs:
            for app in breakdown:
                if pref.app_preferences.get(app, {}).get("enabled", False):
                    breakdown[app] += 1

        return breakdown

    @classmethod
    def get_opt_in_over_time(
        cls, start_date: datetime, end_date: datetime, period: str = "daily"
    ) -> list[dict]:
        """
        Get opt-in trend data for line chart.

        Args:
            start_date: Start of period
            end_date: End of period
            period: 'daily', 'weekly', or 'monthly'

        Returns:
            List of dicts with date and opt-in counts
        """
        from accounts.models import PreferenceChangeLog

        # Determine grouping based on duration
        duration = (end_date - start_date).days

        if duration <= 7 or period == "daily":
            # Group by day
            date_format = "%Y-%m-%d"
            delta = timedelta(days=1)
        elif duration <= 60 or period == "weekly":
            # Group by week
            date_format = "%Y-W%W"
            delta = timedelta(weeks=1)
        else:
            # Group by month
            date_format = "%Y-%m"
            delta = timedelta(days=30)

        # Get opt-in events (email_marketing enabled)
        logs = PreferenceChangeLog.objects.filter(
            timestamp__gte=start_date,
            timestamp__lte=end_date,
            action__contains="email_marketing",
            new_value__email_marketing=True,
        ).values("timestamp")

        # Group by period
        data = {}
        current = start_date
        while current <= end_date:
            key = current.strftime(date_format)
            data[key] = 0
            current += delta

        for log in logs:
            key = log["timestamp"].strftime(date_format)
            if key in data:
                data[key] += 1

        # Format for chart
        result = [{"date": date, "count": count} for date, count in sorted(data.items())]

        return result

    @classmethod
    def get_verification_funnel(cls) -> dict:
        """
        Get verification funnel data.

        Returns:
            Dict with conversion rates at each step:
            - Signup -> Opted In -> Verified -> Active
        """
        from accounts.models import CommunicationPreference

        total_users = User.objects.count()

        if total_users == 0:
            return {
                "signup": 0,
                "opted_in": 0,
                "verified": 0,
                "active": 0,
                "conversion_rates": {
                    "signup_to_opted_in": 0,
                    "opted_in_to_verified": 0,
                    "verified_to_active": 0,
                },
            }

        opted_in = CommunicationPreference.objects.filter(email_marketing=True).count()
        verified = CommunicationPreference.objects.filter(
            email_marketing=True, email_verified=True
        ).count()
        active = verified  # Active = verified and opted in

        return {
            "signup": total_users,
            "opted_in": opted_in,
            "verified": verified,
            "active": active,
            "conversion_rates": {
                "signup_to_opted_in": (opted_in / total_users * 100) if total_users > 0 else 0,
                "opted_in_to_verified": (verified / opted_in * 100) if opted_in > 0 else 0,
                "verified_to_active": 100.0 if verified > 0 else 0,  # Same as verified
            },
        }

    @classmethod
    def _calculate_change(cls, current: int, previous: int) -> float:
        """
        Calculate percentage change between two values.

        Args:
            current: Current value
            previous: Previous value

        Returns:
            Percentage change (positive or negative)
        """
        if previous == 0:
            return 100.0 if current > 0 else 0.0

        return ((current - previous) / previous) * 100.0
