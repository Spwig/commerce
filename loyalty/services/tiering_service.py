"""
Tiering Service for Loyalty Program

Handles tier calculations, promotions, demotions, and tier-specific perks.
"""

import logging
from datetime import timedelta
from decimal import Decimal

from django.db import transaction as db_transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from loyalty.models import (
    LoyaltyBadge,
    LoyaltyBalance,
    LoyaltyMember,
    LoyaltyMemberBadge,
    LoyaltyTier,
)

logger = logging.getLogger(__name__)


class TieringService:
    """
    Service for managing loyalty tier calculations and transitions.

    Responsibilities:
    - Calculate eligible tier for a member
    - Promote members to higher tiers
    - Demote members from tiers (with grace period)
    - Apply tier-specific multipliers
    - Award tier promotion badges
    """

    def __init__(self):
        """Initialize the tiering service."""
        pass

    def calculate_eligible_tier(self, member):
        """
        Calculate the highest tier a member is eligible for based on their metrics.

        Args:
            member: LoyaltyMember instance

        Returns:
            LoyaltyTier instance or None if no tier qualifies
        """
        # Get all active tiers ordered by rank (highest first)
        tiers = LoyaltyTier.objects.filter(is_active=True).order_by("rank")

        if not tiers.exists():
            return None

        # Get member metrics
        try:
            balance = member.balance
            lifetime_points = balance.lifetime_earned
        except LoyaltyBalance.DoesNotExist:
            lifetime_points = 0

        # Get actual spend and order count from order system
        try:
            from django.db.models import Sum

            from orders.models import Order

            order_qs = Order.objects.filter(
                user=member.customer,
                status__in=["processing", "completed", "shipped", "delivered"],
            )
            lifetime_spend = Decimal(
                str(order_qs.aggregate(total=Sum("total_amount_base"))["total"] or "0.00")
            )
            order_count = order_qs.count()
        except Exception as e:
            logger.warning(f"Could not fetch order data for member {member.id}: {e}")
            lifetime_spend = Decimal("0.00")
            order_count = 0

        # Find highest tier member qualifies for
        eligible_tier = None

        for tier in tiers:
            qualifies = False

            # Check if meets points threshold
            if lifetime_points >= tier.min_points_earned:
                qualifies = True

            # Check if meets spend threshold
            if lifetime_spend >= tier.min_spend:
                qualifies = True

            # Check if meets order count threshold
            if order_count >= tier.min_orders:
                qualifies = True

            # If qualifies and this is a higher tier (lower rank), set it
            if qualifies and (eligible_tier is None or tier.rank < eligible_tier.rank):
                eligible_tier = tier

        return eligible_tier

    @db_transaction.atomic
    def evaluate_and_update_tier(self, member, trigger_event=None):
        """
        Evaluate member's tier eligibility and update if needed.

        This is the main method called after points changes, purchases, etc.

        Args:
            member: LoyaltyMember instance
            trigger_event: String describing what triggered the evaluation

        Returns:
            dict with keys: 'changed', 'old_tier', 'new_tier', 'action'
        """
        current_tier = member.current_tier
        eligible_tier = self.calculate_eligible_tier(member)

        result = {
            "changed": False,
            "old_tier": current_tier,
            "new_tier": eligible_tier,
            "action": None,
        }

        # No change needed
        if current_tier == eligible_tier:
            # Clear grace period if member re-qualified
            if member.grace_period_started_at is not None:
                member.grace_period_started_at = None
                member.save(update_fields=["grace_period_started_at"])
                logger.info(f"Cleared grace period for member {member.id} (still qualifies)")
            return result

        # Promotion (moving to a better tier or getting first tier)
        if eligible_tier and (not current_tier or eligible_tier.rank < current_tier.rank):
            # Clear grace period on promotion
            if member.grace_period_started_at is not None:
                member.grace_period_started_at = None
                member.save(update_fields=["grace_period_started_at"])
            self.promote_member(member, eligible_tier, trigger_event)
            result["changed"] = True
            result["new_tier"] = eligible_tier
            result["action"] = "promotion"
            return result

        # Demotion (falling to a lower tier)
        if current_tier and (not eligible_tier or eligible_tier.rank > current_tier.rank):
            # Check grace period before demoting
            if self._is_grace_period_active(member, current_tier):
                logger.info(f"Member {member.id} in grace period for tier {current_tier.name}")
                return result

            self.demote_member(member, eligible_tier, trigger_event)
            result["changed"] = True
            result["new_tier"] = eligible_tier
            result["action"] = "demotion"
            return result

        return result

    @db_transaction.atomic
    def promote_member(self, member, new_tier, trigger_event=None):
        """
        Promote member to a new tier.

        Args:
            member: LoyaltyMember instance
            new_tier: LoyaltyTier instance
            trigger_event: String describing what triggered the promotion
        """
        old_tier = member.current_tier
        old_tier_name = old_tier.name if old_tier else "No Tier"

        # Update member's tier
        member.current_tier = new_tier
        member.save(update_fields=["current_tier", "updated_at"])

        logger.info(f"Promoted member {member.id} from {old_tier_name} to {new_tier.name}")

        # Award tier promotion badge if exists
        self._award_tier_badge(member, new_tier, "promotion")

        # Send tier promotion email notification
        try:
            from email_system.services.email_sender import EmailSendingService
            from email_system.utils.language import get_user_email_language

            benefits = self.get_tier_benefits(new_tier)
            email_context = {
                "customer_name": member.customer.get_full_name() or member.customer.username,
                "new_tier": new_tier.name,
                "old_tier": old_tier_name,
                "tier_benefits": benefits,
                "account_url": "/loyalty/account/dashboard/",
            }

            EmailSendingService.send_template_email(
                to_email=member.customer.email,
                template_type="loyalty_tier_upgrade",
                context=email_context,
                language=get_user_email_language(member.customer),
                enable_tracking=True,
            )
            logger.info(f"Sent tier promotion email to member {member.id}")
        except Exception as e:
            logger.error(f"Failed to send tier promotion email for member {member.id}: {e}")

        return True

    @db_transaction.atomic
    def demote_member(self, member, new_tier, trigger_event=None):
        """
        Demote member to a lower tier or remove tier.

        Args:
            member: LoyaltyMember instance
            new_tier: LoyaltyTier instance or None
            trigger_event: String describing what triggered the demotion
        """
        old_tier = member.current_tier
        old_tier_name = old_tier.name if old_tier else "No Tier"
        new_tier_name = new_tier.name if new_tier else "No Tier"

        # Update member's tier
        member.current_tier = new_tier
        member.save(update_fields=["current_tier", "updated_at"])

        logger.info(f"Demoted member {member.id} from {old_tier_name} to {new_tier_name}")

        # Send tier demotion email notification
        try:
            from email_system.services.email_sender import EmailSendingService
            from email_system.utils.language import get_user_email_language

            benefits = self.get_tier_benefits(old_tier) if old_tier else []
            email_context = {
                "customer_name": member.customer.get_full_name() or member.customer.username,
                "current_tier": old_tier_name,
                "next_tier": new_tier_name,
                "tier_benefits": benefits,
                "loyalty_dashboard_url": "/loyalty/account/dashboard/",
            }

            EmailSendingService.send_template_email(
                to_email=member.customer.email,
                template_type="loyalty_tier_demotion_warning",
                context=email_context,
                language=get_user_email_language(member.customer),
                enable_tracking=True,
            )
            logger.info(f"Sent tier demotion email to member {member.id}")
        except Exception as e:
            logger.error(f"Failed to send tier demotion email for member {member.id}: {e}")

        return True

    def get_tier_multiplier(self, member):
        """
        Get the current points multiplier for a member based on their tier.

        Args:
            member: LoyaltyMember instance

        Returns:
            Decimal: Points multiplier (e.g., 1.5 for 50% bonus)
        """
        if not member.current_tier:
            return Decimal("1.00")

        return member.current_tier.points_multiplier

    def apply_tier_multiplier(self, base_points, member):
        """
        Apply tier multiplier to base points.

        Args:
            base_points: int - Base points before multiplier
            member: LoyaltyMember instance

        Returns:
            int: Points after applying tier multiplier (rounded)
        """
        if not member.current_tier:
            return base_points

        multiplier = member.current_tier.points_multiplier

        if multiplier == Decimal("1.00"):
            return base_points

        # Apply multiplier and round to nearest integer
        multiplied_points = Decimal(base_points) * multiplier
        return int(multiplied_points.quantize(Decimal("1")))

    def get_next_tier(self, member):
        """
        Get the next tier a member can achieve.

        Args:
            member: LoyaltyMember instance

        Returns:
            LoyaltyTier instance or None if already at highest tier
        """
        current_tier = member.current_tier

        if not current_tier:
            # No tier yet, return lowest tier
            return LoyaltyTier.objects.filter(is_active=True).order_by("rank").first()

        # Get next tier (lower rank number = higher tier)
        return (
            LoyaltyTier.objects.filter(is_active=True, rank__lt=current_tier.rank)
            .order_by("-rank")
            .first()
        )

    def get_progress_to_next_tier(self, member):
        """
        Calculate progress percentage to next tier.

        Args:
            member: LoyaltyMember instance

        Returns:
            dict with keys: 'next_tier', 'progress_pct', 'points_needed', 'current_points'
        """
        next_tier = self.get_next_tier(member)

        if not next_tier:
            return {
                "next_tier": None,
                "progress_pct": 100,
                "points_needed": 0,
                "current_points": 0,
            }

        balance = member.balance
        current_points = balance.lifetime_earned if balance else 0
        required_points = next_tier.min_points_earned

        if required_points == 0:
            progress_pct = 100
        else:
            progress_pct = min(100, int((current_points / required_points) * 100))

        points_needed = max(0, required_points - current_points)

        return {
            "next_tier": next_tier,
            "progress_pct": progress_pct,
            "points_needed": points_needed,
            "current_points": current_points,
        }

    def get_tier_benefits(self, tier):
        """
        Get a list of benefits for a tier.

        Args:
            tier: LoyaltyTier instance

        Returns:
            list of strings describing benefits
        """
        if not tier:
            return []

        benefits = []

        # Points multiplier
        if tier.points_multiplier > Decimal("1.00"):
            bonus_pct = int((tier.points_multiplier - Decimal("1.00")) * 100)
            benefits.append(_(f"{bonus_pct}% bonus on all points earned"))

        # Free shipping
        if tier.has_free_shipping:
            benefits.append(_("Free shipping on all orders"))

        # Early access
        if tier.has_early_access:
            benefits.append(_("Early access to new products and sales"))

        return benefits

    def _is_grace_period_active(self, member, tier):
        """
        Check if member is within grace period for tier demotion.

        Args:
            member: LoyaltyMember instance
            tier: LoyaltyTier instance

        Returns:
            bool: True if in grace period, False otherwise
        """
        if not tier or tier.grace_period_days <= 0:
            return False

        now = timezone.now()

        if member.grace_period_started_at is None:
            # First time falling below threshold - start grace period
            member.grace_period_started_at = now
            member.save(update_fields=["grace_period_started_at"])
            logger.info(
                f"Started grace period for member {member.id} in tier {tier.name} "
                f"({tier.grace_period_days} days)"
            )
            return True

        # Check if grace period has expired
        grace_end = member.grace_period_started_at + timedelta(days=tier.grace_period_days)

        if now < grace_end:
            days_remaining = (grace_end - now).days
            logger.info(
                f"Member {member.id} in grace period for tier {tier.name} "
                f"({days_remaining} days remaining)"
            )
            return True

        # Grace period expired - clear tracking and allow demotion
        logger.info(f"Grace period expired for member {member.id} in tier {tier.name}")
        member.grace_period_started_at = None
        member.save(update_fields=["grace_period_started_at"])
        return False

    def _award_tier_badge(self, member, tier, badge_type="promotion"):
        """
        Award a badge for tier achievement.

        Args:
            member: LoyaltyMember instance
            tier: LoyaltyTier instance
            badge_type: 'promotion' or 'achievement'
        """
        # Look for a badge associated with this tier
        try:
            badge = LoyaltyBadge.objects.get(name=f"{tier.name} Tier", is_active=True)

            # Check if member already has this badge
            if not LoyaltyMemberBadge.objects.filter(member=member, badge=badge).exists():
                LoyaltyMemberBadge.objects.create(
                    member=member, badge=badge, earned_at=timezone.now()
                )
                logger.info(f"Awarded badge '{badge.name}' to member {member.id}")
        except LoyaltyBadge.DoesNotExist:
            # No badge for this tier, that's okay
            pass

    def batch_evaluate_all_members(self, limit=None):
        """
        Batch process to evaluate tier eligibility for all active members.

        This should be run periodically (e.g., daily) to ensure all members
        have the correct tier based on their current metrics.

        Args:
            limit: Optional limit on number of members to process

        Returns:
            dict with statistics
        """
        members = LoyaltyMember.objects.filter(is_active=True)

        if limit:
            members = members[:limit]

        stats = {
            "total_processed": 0,
            "promotions": 0,
            "demotions": 0,
            "no_change": 0,
            "errors": 0,
        }

        for member in members:
            try:
                result = self.evaluate_and_update_tier(member, trigger_event="batch_evaluation")

                stats["total_processed"] += 1

                if result["changed"]:
                    if result["action"] == "promotion":
                        stats["promotions"] += 1
                    elif result["action"] == "demotion":
                        stats["demotions"] += 1
                else:
                    stats["no_change"] += 1

            except Exception as e:
                stats["errors"] += 1
                logger.error(f"Error evaluating tier for member {member.id}: {str(e)}")

        logger.info(
            f"Batch tier evaluation complete: {stats['total_processed']} processed, "
            f"{stats['promotions']} promotions, {stats['demotions']} demotions, "
            f"{stats['errors']} errors"
        )

        return stats
