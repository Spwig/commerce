"""
Smart Defaults Service

Provides rule-based recommendations for optimal communication frequency
based on customer engagement heuristics (no ML infrastructure).
"""

import logging
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Max, Sum
from django.utils import timezone

logger = logging.getLogger(__name__)
User = get_user_model()


class SmartDefaultsService:
    """
    Service for suggesting optimal preference defaults based on engagement.

    Uses rule-based heuristics (no machine learning) to analyze:
    - Order frequency
    - Recency
    - Customer tier (total spent)
    - Email engagement (not unsubscribed)
    """

    # Engagement scoring weights (total = 100 points)
    WEIGHT_ORDER_FREQUENCY = 40
    WEIGHT_RECENCY = 30
    WEIGHT_CUSTOMER_TIER = 20
    WEIGHT_EMAIL_ENGAGEMENT = 10

    @classmethod
    def calculate_engagement_score(cls, user) -> dict:
        """
        Calculate engagement score (0-100) for a user.

        Args:
            user: User instance

        Returns:
            Dict with score and breakdown
        """
        from orders.models import Order

        score = 0
        breakdown = {}

        # 1. Order Frequency (40 points max)
        ninety_days_ago = timezone.now() - timedelta(days=90)
        order_count_90d = Order.objects.filter(
            user=user,
            created_at__gte=ninety_days_ago,
            status__in=["completed", "processing", "shipped"],
        ).count()

        if order_count_90d >= 3:  # ≥1 order/month
            frequency_score = cls.WEIGHT_ORDER_FREQUENCY
        elif order_count_90d >= 1:  # ≥1 order/quarter
            frequency_score = cls.WEIGHT_ORDER_FREQUENCY * 0.5
        else:
            frequency_score = cls.WEIGHT_ORDER_FREQUENCY * 0.25

        score += frequency_score
        breakdown["order_frequency"] = {
            "score": frequency_score,
            "orders_90d": order_count_90d,
        }

        # 2. Recency (30 points max)
        last_order = Order.objects.filter(
            user=user, status__in=["completed", "processing", "shipped"]
        ).aggregate(Max("created_at"))["created_at__max"]

        if last_order:
            days_since = (timezone.now() - last_order).days

            if days_since <= 30:
                recency_score = cls.WEIGHT_RECENCY
            elif days_since <= 90:
                recency_score = cls.WEIGHT_RECENCY * 0.67
            elif days_since <= 180:
                recency_score = cls.WEIGHT_RECENCY * 0.33
            else:
                recency_score = cls.WEIGHT_RECENCY * 0.17

            breakdown["recency"] = {
                "score": recency_score,
                "days_since_last_order": days_since,
            }
        else:
            recency_score = 0
            breakdown["recency"] = {
                "score": 0,
                "days_since_last_order": None,
            }

        score += recency_score

        # 3. Customer Tier (20 points max)
        total_spent_agg = Order.objects.filter(user=user, status="completed").aggregate(
            Sum("total_amount")
        )["total_amount__sum"]
        # Aggregate returns Money when rows exist, None when empty. Unwrap to
        # Decimal so plain-number comparisons and float() work.
        total_spent = (
            total_spent_agg.amount if hasattr(total_spent_agg, "amount") else (total_spent_agg or 0)
        )

        if total_spent >= 1000:  # VIP
            tier_score = cls.WEIGHT_CUSTOMER_TIER
            tier = "VIP"
        elif total_spent >= 500:  # High value
            tier_score = cls.WEIGHT_CUSTOMER_TIER * 0.75
            tier = "High Value"
        elif total_spent >= 100:  # Regular
            tier_score = cls.WEIGHT_CUSTOMER_TIER * 0.5
            tier = "Regular"
        else:
            tier_score = cls.WEIGHT_CUSTOMER_TIER * 0.25
            tier = "New"

        score += tier_score
        breakdown["customer_tier"] = {
            "score": tier_score,
            "tier": tier,
            "total_spent": float(total_spent),
        }

        # 4. Email Engagement (10 points max)
        # Check if user is receiving emails without unsubscribing
        from accounts.models import CommunicationPreference

        try:
            prefs = CommunicationPreference.objects.get(user=user)
            if prefs.email_marketing and prefs.email_verified:
                engagement_score = cls.WEIGHT_EMAIL_ENGAGEMENT
            else:
                engagement_score = 0

            breakdown["email_engagement"] = {
                "score": engagement_score,
                "opted_in": prefs.email_marketing,
                "verified": prefs.email_verified,
            }
        except CommunicationPreference.DoesNotExist:
            engagement_score = 0
            breakdown["email_engagement"] = {
                "score": 0,
                "opted_in": False,
                "verified": False,
            }

        score += engagement_score

        return {
            "total_score": round(score, 2),
            "breakdown": breakdown,
        }

    @classmethod
    def get_recommended_frequency(cls, user) -> dict:
        """
        Get recommended communication frequency based on engagement.

        Args:
            user: User instance

        Returns:
            Dict with frequency and reasoning
        """
        engagement = cls.calculate_engagement_score(user)
        score = engagement["total_score"]

        if score >= 80:
            frequency = "immediate"
            reasoning = "High engagement - active customer with frequent orders"
        elif score >= 50:
            frequency = "weekly"
            reasoning = "Moderate engagement - regular customer, weekly digest recommended"
        else:
            frequency = "monthly"
            reasoning = "Lower engagement - reduce frequency to avoid fatigue"

        return {
            "frequency": frequency,
            "reasoning": reasoning,
            "engagement_score": score,
            "breakdown": engagement["breakdown"],
        }

    @classmethod
    def get_app_recommendations(cls, user) -> dict:
        """
        Get recommendations for app-specific preferences.

        Args:
            user: User instance

        Returns:
            Dict with app recommendations
        """
        from orders.models import Order

        recommendations = {}

        # Get order stats
        total_orders = Order.objects.filter(user=user, status="completed").count()

        total_spent_agg = Order.objects.filter(user=user, status="completed").aggregate(
            Sum("total_amount")
        )["total_amount__sum"]
        total_spent = (
            total_spent_agg.amount if hasattr(total_spent_agg, "amount") else (total_spent_agg or 0)
        )

        # Blog: Recommend if ≥2 orders (engaged customer)
        recommendations["blog"] = {
            "recommended": total_orders >= 2,
            "reason": "Engaged customer - would likely appreciate blog content"
            if total_orders >= 2
            else "Build more order history first",
        }

        # Loyalty: Recommend if ≥$100 spent
        recommendations["loyalty"] = {
            "recommended": total_spent >= 100,
            "reason": f"Spent ${total_spent:.2f} - loyalty rewards would add value"
            if total_spent >= 100
            else f"Spend threshold not met (${total_spent:.2f} < $100)",
        }

        # Referrals: Always recommend (win-win program)
        recommendations["referrals"] = {
            "recommended": True,
            "reason": "Win-win program - earn rewards by referring friends",
        }

        # Affiliate: Recommend if ≥$500 spent AND ≥5 orders (strong advocate)
        recommendations["affiliate"] = {
            "recommended": total_spent >= 500 and total_orders >= 5,
            "reason": "Strong customer advocate - good affiliate candidate"
            if (total_spent >= 500 and total_orders >= 5)
            else "Not enough engagement for affiliate program yet",
        }

        return recommendations

    @classmethod
    def get_recommendations_for_preference_center(cls, user) -> dict:
        """
        Get complete recommendations for preference center display.

        Args:
            user: User instance

        Returns:
            Dict with all recommendations
        """
        frequency_rec = cls.get_recommended_frequency(user)
        app_recs = cls.get_app_recommendations(user)

        return {
            "frequency": frequency_rec,
            "apps": app_recs,
            "show_suggestions": True,  # Can be toggled per user preference
        }
