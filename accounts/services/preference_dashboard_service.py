"""
Service for preference-related dashboard metrics.

Provides action cards and metrics for the shop admin dashboard to give
merchants visibility into communication preference health and engagement.
"""

from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from accounts.models import CommunicationPreference, PreferenceChangeLog


class PreferenceDashboardService:
    """Service for preference-related dashboard metrics."""

    @staticmethod
    def get_action_cards():
        """
        Get action card data for dashboard.

        Returns:
            list: Action card dictionaries with title, count, icon, color, url, description
        """
        try:
            # Unverified users (marketing enabled but not verified)
            unverified_count = CommunicationPreference.objects.filter(
                email_marketing=True,
                email_verified=False
            ).count()

            return [{
                'title': 'Unverified Users',
                'count': unverified_count,
                'icon': 'fa-user-clock',
                'color': 'warning',
                'url': '/admin/accounts/communicationpreference/?email_verified__exact=0&email_marketing__exact=1',
                'description': 'Users opted into marketing but email not verified'
            }]
        except Exception as e:
            # Return empty list on error to avoid breaking dashboard
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error generating preference action cards: {e}", exc_info=True)
            return []

    @staticmethod
    def get_metrics():
        """
        Get metric cards for dashboard.

        Returns:
            list: Metric dictionaries with label, value, icon, color, trend, description
        """
        try:
            total_users = CommunicationPreference.objects.count()

            if total_users == 0:
                # No users yet - return zeros to avoid division by zero
                return [
                    {
                        'label': 'Email Verification Rate',
                        'value': '0.0%',
                        'icon': 'fa-envelope-circle-check',
                        'color': 'info',
                        'trend': None
                    },
                    {
                        'label': 'SMS Verification Rate',
                        'value': '0.0%',
                        'icon': 'fa-mobile-screen',
                        'color': 'info',
                        'trend': None
                    },
                    {
                        'label': 'Recent Preference Changes',
                        'value': '0',
                        'icon': 'fa-history',
                        'color': 'info',
                        'description': 'Last 7 days'
                    }
                ]

            # Email verification rate
            email_verified_count = CommunicationPreference.objects.filter(
                email_verified=True
            ).count()
            email_verification_rate = (email_verified_count / total_users * 100)

            # SMS verification rate
            sms_verified_count = CommunicationPreference.objects.filter(
                sms_verified=True
            ).count()
            sms_verification_rate = (sms_verified_count / total_users * 100)

            # Recent changes (last 7 days)
            seven_days_ago = timezone.now() - timedelta(days=7)
            recent_changes_count = PreferenceChangeLog.objects.filter(
                timestamp__gte=seven_days_ago
            ).count()

            return [
                {
                    'label': 'Email Verification Rate',
                    'value': f'{email_verification_rate:.1f}%',
                    'icon': 'fa-envelope-circle-check',
                    'color': 'success' if email_verification_rate >= 70 else 'warning',
                    'trend': None  # Could add trend calculation later
                },
                {
                    'label': 'SMS Verification Rate',
                    'value': f'{sms_verification_rate:.1f}%',
                    'icon': 'fa-mobile-screen',
                    'color': 'success' if sms_verification_rate >= 50 else 'info',
                    'trend': None
                },
                {
                    'label': 'Recent Preference Changes',
                    'value': str(recent_changes_count),
                    'icon': 'fa-history',
                    'color': 'info',
                    'description': 'Last 7 days'
                }
            ]
        except Exception as e:
            # Return empty list on error to avoid breaking dashboard
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error generating preference metrics: {e}", exc_info=True)
            return []
