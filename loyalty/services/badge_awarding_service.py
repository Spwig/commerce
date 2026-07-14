"""
Badge Awarding Service

Automatically checks badge criteria and awards badges to loyalty members
when they meet achievement requirements.
"""

import logging
from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone

logger = logging.getLogger(__name__)


class BadgeAwardingService:
    """
    Service for automatically awarding badges based on criteria.

    This service checks if members meet badge criteria and awards badges
    accordingly. It handles various criteria types like order counts,
    spending totals, review counts, and more.
    """

    def __init__(self):
        """Initialize the badge awarding service."""
        pass

    def check_and_award_badges(self, member, criteria_types: list[str] | None = None) -> list:
        """
        Check all eligible badges for a member and award any they've earned.

        Args:
            member: LoyaltyMember instance
            criteria_types: Optional list of criteria types to check. If None, checks all.

        Returns:
            List of newly awarded badge IDs
        """
        from loyalty.models import LoyaltyBadge, LoyaltyMemberBadge

        # Get all auto-award badges that are active
        badges = LoyaltyBadge.objects.filter(is_active=True, auto_award=True)

        # Filter by criteria types if specified
        if criteria_types:
            badges = badges.filter(criteria_type__in=criteria_types)

        # Get badges member already has
        earned_badge_ids = set(
            LoyaltyMemberBadge.objects.filter(member=member).values_list("badge_id", flat=True)
        )

        # Filter out already earned badges
        badges = badges.exclude(id__in=earned_badge_ids)

        newly_awarded = []

        for badge in badges:
            if self._check_badge_criteria(member, badge):
                awarded_badge = self._award_badge(member, badge)
                if awarded_badge:
                    newly_awarded.append(badge.id)
                    logger.info(f"Auto-awarded badge '{badge.name}' to member {member.id}")

        return newly_awarded

    def _check_badge_criteria(self, member, badge) -> bool:
        """
        Check if member meets the criteria for a specific badge.

        Args:
            member: LoyaltyMember instance
            badge: LoyaltyBadge instance

        Returns:
            bool: True if criteria is met
        """
        criteria_type = badge.criteria_type
        criteria_value = badge.criteria_value

        # Map criteria types to check methods
        criteria_checks = {
            "program_join": self._check_program_join,
            "first_purchase": self._check_first_purchase,
            "order_count": self._check_order_count,
            "total_spend": self._check_total_spend,
            "review_count": self._check_review_count,
            "social_share": self._check_social_share,
            "monthly_streak": self._check_monthly_streak,
            "referrals": self._check_referrals,
            "birthday_purchase": self._check_birthday_purchase,
            "wishlist_items": self._check_wishlist_items,
            "early_morning_orders": self._check_early_morning_orders,
            "late_night_orders": self._check_late_night_orders,
            "weekend_orders": self._check_weekend_orders,
            "quick_return": self._check_quick_return,
            "single_order_value": self._check_single_order_value,
            "items_per_order": self._check_items_per_order,
            "orders_per_month": self._check_orders_per_month,
        }

        check_method = criteria_checks.get(criteria_type)
        if not check_method:
            logger.warning(f"Unknown criteria type: {criteria_type} for badge {badge.id}")
            return False

        return check_method(member, criteria_value)

    def _check_program_join(self, member, criteria_value) -> bool:
        """Check if member has joined the program."""
        return member.enrolled_at is not None

    def _check_first_purchase(self, member, criteria_value) -> bool:
        """Check if member has made their first purchase."""
        from orders.models import Order

        order_count = Order.objects.filter(
            user=member.customer, status__in=["processing", "completed", "shipped"]
        ).count()

        return order_count >= 1

    def _check_order_count(self, member, criteria_value) -> bool:
        """Check if member has reached a specific order count."""
        from orders.models import Order

        order_count = Order.objects.filter(
            user=member.customer, status__in=["processing", "completed", "shipped"]
        ).count()

        return order_count >= criteria_value

    def _check_total_spend(self, member, criteria_value) -> bool:
        """Check if member has reached a total spend amount."""
        from orders.models import Order

        total_spend = Order.objects.filter(
            user=member.customer, status__in=["processing", "completed", "shipped"]
        ).aggregate(total=Sum("total_amount"))["total"] or Decimal("0")

        return total_spend >= Decimal(str(criteria_value))

    def _check_review_count(self, member, criteria_value) -> bool:
        """Check if member has submitted enough reviews."""
        from catalog.models import ProductReview

        review_count = ProductReview.objects.filter(user=member.customer, is_approved=True).count()

        return review_count >= criteria_value

    def _check_social_share(self, member, criteria_value) -> bool:
        """Check if member has shared on social media enough times."""
        try:
            from social_sharing.models import SocialShare

            share_count = SocialShare.objects.filter(user=member.customer).count()

            return share_count >= criteria_value

        except ImportError:
            logger.debug("Social sharing module not available")
            return False
        except Exception as e:
            logger.error(f"Error checking social share criteria: {e}", exc_info=True)
            return False

    def _check_monthly_streak(self, member, criteria_value) -> bool:
        """Check if member has maintained a monthly purchase streak."""
        from django.db.models import Count
        from django.db.models.functions import TruncMonth

        from orders.models import Order

        # Get orders grouped by month
        monthly_orders = (
            Order.objects.filter(
                user=member.customer, status__in=["processing", "completed", "shipped"]
            )
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("-month")
        )

        if not monthly_orders:
            return False

        # Check for consecutive months
        current_streak = 0
        expected_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        for entry in monthly_orders:
            if (
                entry["month"].year == expected_month.year
                and entry["month"].month == expected_month.month
            ):
                current_streak += 1
                # Move to previous month
                if expected_month.month == 1:
                    expected_month = expected_month.replace(year=expected_month.year - 1, month=12)
                else:
                    expected_month = expected_month.replace(month=expected_month.month - 1)
            else:
                break

        return current_streak >= criteria_value

    def _check_referrals(self, member, criteria_value) -> bool:
        """Check if member has made enough referrals."""
        try:
            from referrals.models import Referral

            referral_count = Referral.objects.filter(
                referrer=member.customer,
                status="converted",
            ).count()

            return referral_count >= criteria_value

        except ImportError:
            logger.debug("Referral module not available")
            return False
        except Exception as e:
            logger.error(f"Error checking referral criteria: {e}", exc_info=True)
            return False

    def _check_birthday_purchase(self, member, criteria_value) -> bool:
        """Check if member made a purchase on their birthday."""
        from orders.models import Order

        # Get customer's birthday
        customer = member.customer
        if not hasattr(customer, "date_of_birth") or not customer.date_of_birth:
            return False

        birthday_month = customer.date_of_birth.month
        birthday_day = customer.date_of_birth.day

        # Check for orders on birthday
        birthday_orders = Order.objects.filter(
            user=member.customer,
            status__in=["processing", "completed", "shipped"],
            created_at__month=birthday_month,
            created_at__day=birthday_day,
        ).count()

        return birthday_orders >= criteria_value

    def _check_wishlist_items(self, member, criteria_value) -> bool:
        """Check if member has added enough items to wishlist."""
        from cart.models import Wishlist

        try:
            wishlist = Wishlist.objects.get(user=member.customer)
            item_count = wishlist.items.count()
            return item_count >= criteria_value
        except Wishlist.DoesNotExist:
            return False

    def _check_early_morning_orders(self, member, criteria_value) -> bool:
        """Check if member has placed enough orders before 9 AM."""
        from orders.models import Order

        early_morning_count = Order.objects.filter(
            user=member.customer,
            status__in=["processing", "completed", "shipped"],
            created_at__hour__lt=9,
        ).count()

        return early_morning_count >= criteria_value

    def _check_late_night_orders(self, member, criteria_value) -> bool:
        """Check if member has placed enough orders after 9 PM."""
        from orders.models import Order

        late_night_count = Order.objects.filter(
            user=member.customer,
            status__in=["processing", "completed", "shipped"],
            created_at__hour__gte=21,
        ).count()

        return late_night_count >= criteria_value

    def _check_weekend_orders(self, member, criteria_value) -> bool:
        """Check if member has placed enough orders on weekends."""
        from orders.models import Order

        # Django week_day: 1=Sunday, 2=Monday, ..., 7=Saturday
        weekend_count = Order.objects.filter(
            user=member.customer,
            status__in=["processing", "completed", "shipped"],
            created_at__week_day__in=[1, 7],  # Sunday=1, Saturday=7
        ).count()

        return weekend_count >= criteria_value

    def _check_quick_return(self, member, criteria_value) -> bool:
        """Check if member made a purchase within 24 hours of previous purchase."""
        from datetime import timedelta

        from orders.models import Order

        # Get all completed orders sorted by date
        orders = (
            Order.objects.filter(
                user=member.customer, status__in=["processing", "completed", "shipped"]
            )
            .order_by("created_at")
            .values_list("created_at", flat=True)
        )

        if orders.count() < 2:
            return False

        # Check consecutive orders for 24-hour gap
        quick_returns = 0
        for i in range(1, len(orders)):
            time_diff = orders[i] - orders[i - 1]
            if time_diff <= timedelta(hours=24):
                quick_returns += 1
                if quick_returns >= criteria_value:
                    return True

        return False

    def _check_single_order_value(self, member, criteria_value) -> bool:
        """Check if member has placed a single order meeting or exceeding the value."""
        from orders.models import Order

        high_value_orders = Order.objects.filter(
            user=member.customer,
            status__in=["processing", "completed", "shipped"],
            total_amount__gte=Decimal(str(criteria_value)),
        ).exists()

        return high_value_orders

    def _check_items_per_order(self, member, criteria_value) -> bool:
        """Check if member has placed an order with the specified number of items."""
        from orders.models import Order

        # Check if any order has enough items
        orders = Order.objects.filter(
            user=member.customer, status__in=["processing", "completed", "shipped"]
        ).prefetch_related("items")

        for order in orders:
            total_quantity = sum(item.quantity for item in order.items.all())
            if total_quantity >= criteria_value:
                return True

        return False

    def _check_orders_per_month(self, member, criteria_value) -> bool:
        """Check if member has placed the specified number of orders in any single month."""
        from django.db.models import Count
        from django.db.models.functions import TruncMonth

        from orders.models import Order

        # Group orders by month and count them
        monthly_orders = (
            Order.objects.filter(
                user=member.customer, status__in=["processing", "completed", "shipped"]
            )
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        if not monthly_orders:
            return False

        # Check if any month meets the criteria
        max_orders_in_month = monthly_orders[0]["count"]
        return max_orders_in_month >= criteria_value

    def _award_badge(self, member, badge):
        """
        Award a badge to a member.

        Args:
            member: LoyaltyMember instance
            badge: LoyaltyBadge instance

        Returns:
            LoyaltyMemberBadge instance or None if already awarded
        """
        from loyalty.models import LoyaltyMemberBadge

        # Double-check member doesn't already have this badge
        if LoyaltyMemberBadge.objects.filter(member=member, badge=badge).exists():
            logger.debug(f"Member {member.id} already has badge {badge.id}")
            return None

        # Create transaction for points reward if applicable
        transaction = None
        if badge.points_reward > 0:
            from loyalty.services.points_engine import PointsEngine

            engine = PointsEngine()
            try:
                transaction = engine.award_bonus_points(
                    member=member,
                    points=badge.points_reward,
                    description=f"Badge earned: {badge.name}",
                )
            except Exception as e:
                logger.error(f"Failed to award points for badge {badge.id}: {e}")

        # Award the badge
        member_badge = LoyaltyMemberBadge.objects.create(
            member=member, badge=badge, transaction=transaction, earned_at=timezone.now()
        )

        logger.info(f"Awarded badge '{badge.name}' (ID: {badge.id}) to member {member.id}")

        return member_badge
