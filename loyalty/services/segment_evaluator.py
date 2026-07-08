"""
Segment Evaluator Service

Evaluates dynamic segment rules and manages segment memberships.
Supports complex rule-based filtering for customer segmentation.
"""

import logging
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q, Sum, Count, Avg, Max
from typing import List, Dict, Any, Optional

from loyalty.models import (
    LoyaltySegment,
    LoyaltySegmentMembership,
    LoyaltyMember,
    LoyaltyBalance,
    LoyaltyTransaction,
    LoyaltyRedemption
)
from orders.models import Order

logger = logging.getLogger(__name__)


class SegmentEvaluator:
    """
    Evaluates segment rules and manages segment memberships.

    Supports rule types:
    - Tier-based: tier_id
    - Points-based: min_points, max_points
    - Activity-based: min_orders, max_orders, min_spend, max_spend
    - Engagement-based: last_order_days, signup_days
    - Behavioral: has_redeemed, redemption_count
    """

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def evaluate_member_for_segment(self, member: LoyaltyMember, segment: LoyaltySegment) -> bool:
        """
        Evaluate if a member qualifies for a segment.

        Args:
            member: LoyaltyMember to evaluate
            segment: LoyaltySegment with rules to check

        Returns:
            bool: True if member qualifies for segment
        """
        if not segment.is_active:
            return False

        # Manual segments don't use automatic rules
        if segment.criteria_type == 'manual':
            return False

        rules = segment.criteria_config or {}

        # Empty rules = no members qualify
        if not rules:
            self.logger.debug(f"Segment {segment.id} has no rules")
            return False

        try:
            # Tier-based rules
            if 'tier_id' in rules:
                if not member.current_tier or member.current_tier.id != rules['tier_id']:
                    return False

            # Points-based rules
            if 'min_points' in rules or 'max_points' in rules:
                balance = self._get_member_balance(member)

                if 'min_points' in rules:
                    if balance.available_points < rules['min_points']:
                        return False

                if 'max_points' in rules:
                    if balance.available_points > rules['max_points']:
                        return False

            # Lifetime points earned
            if 'min_lifetime_earned' in rules or 'max_lifetime_earned' in rules:
                balance = self._get_member_balance(member)

                if 'min_lifetime_earned' in rules:
                    if balance.lifetime_earned < rules['min_lifetime_earned']:
                        return False

                if 'max_lifetime_earned' in rules:
                    if balance.lifetime_earned > rules['max_lifetime_earned']:
                        return False

            # Order count rules
            if 'min_orders' in rules or 'max_orders' in rules:
                order_count = Order.objects.filter(
                    user=member.customer,
                    status='completed'
                ).count()

                if 'min_orders' in rules:
                    if order_count < rules['min_orders']:
                        return False

                if 'max_orders' in rules:
                    if order_count > rules['max_orders']:
                        return False

            # Total spend rules
            if 'min_spend' in rules or 'max_spend' in rules:
                total_spend = Order.objects.filter(
                    user=member.customer,
                    status='completed'
                ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')

                if 'min_spend' in rules:
                    min_spend = Decimal(str(rules['min_spend']))
                    if total_spend < min_spend:
                        return False

                if 'max_spend' in rules:
                    max_spend = Decimal(str(rules['max_spend']))
                    if total_spend > max_spend:
                        return False

            # Average order value rules
            if 'min_avg_order_value' in rules or 'max_avg_order_value' in rules:
                avg_order = Order.objects.filter(
                    user=member.customer,
                    status='completed'
                ).aggregate(avg=Avg('total_amount'))['avg'] or Decimal('0')

                if 'min_avg_order_value' in rules:
                    min_avg = Decimal(str(rules['min_avg_order_value']))
                    if avg_order < min_avg:
                        return False

                if 'max_avg_order_value' in rules:
                    max_avg = Decimal(str(rules['max_avg_order_value']))
                    if avg_order > max_avg:
                        return False

            # Last order recency
            if 'last_order_days' in rules:
                last_order = Order.objects.filter(
                    user=member.customer,
                    status='completed'
                ).order_by('-created_at').first()

                if last_order:
                    days_since = (timezone.now() - last_order.created_at).days
                    if days_since > rules['last_order_days']:
                        return False
                else:
                    # No orders = doesn't meet recency requirement
                    return False

            # Signup recency
            if 'signup_days_min' in rules or 'signup_days_max' in rules:
                days_since_signup = (timezone.now() - member.joined_at).days

                if 'signup_days_min' in rules:
                    if days_since_signup < rules['signup_days_min']:
                        return False

                if 'signup_days_max' in rules:
                    if days_since_signup > rules['signup_days_max']:
                        return False

            # Redemption-based rules
            if 'has_redeemed' in rules:
                has_redemptions = LoyaltyRedemption.objects.filter(
                    member=member
                ).exists()

                if rules['has_redeemed'] and not has_redemptions:
                    return False
                elif not rules['has_redeemed'] and has_redemptions:
                    return False

            if 'min_redemptions' in rules or 'max_redemptions' in rules:
                redemption_count = LoyaltyRedemption.objects.filter(
                    member=member
                ).count()

                if 'min_redemptions' in rules:
                    if redemption_count < rules['min_redemptions']:
                        return False

                if 'max_redemptions' in rules:
                    if redemption_count > rules['max_redemptions']:
                        return False

            # Birthday month (for birthday campaigns)
            if 'birthday_month' in rules:
                if not member.customer.date_of_birth:
                    return False

                if member.customer.date_of_birth.month != rules['birthday_month']:
                    return False

            # Email verified
            if 'email_verified' in rules:
                # Check if user's email is verified (django-allauth)
                email_verified = member.customer.emailaddress_set.filter(
                    verified=True
                ).exists() if hasattr(member.customer, 'emailaddress_set') else True

                if rules['email_verified'] != email_verified:
                    return False

            # All rules passed
            return True

        except Exception as e:
            self.logger.error(f"Error evaluating member {member.id} for segment {segment.id}: {e}")
            return False

    def _get_member_balance(self, member: LoyaltyMember) -> LoyaltyBalance:
        """Get or create balance for member"""
        balance, _ = LoyaltyBalance.objects.get_or_create(
            member=member,
            defaults={
                'available_points': 0,
                'pending_points': 0,
                'lifetime_earned': 0,
                'lifetime_redeemed': 0
            }
        )
        return balance

    def get_segment_members(self, segment: LoyaltySegment) -> List[LoyaltyMember]:
        """
        Get all members who qualify for a segment.

        Args:
            segment: LoyaltySegment to evaluate

        Returns:
            List of LoyaltyMember instances that qualify
        """
        if segment.criteria_type == 'manual':
            # Manual segments - return existing members
            return list(
                LoyaltyMember.objects.filter(
                    segment_memberships__segment=segment,
                    is_active=True
                ).distinct()
            )

        # Dynamic segments - evaluate all active members
        qualifying_members = []

        # Get all active members
        active_members = LoyaltyMember.objects.filter(is_active=True).select_related(
            'customer', 'current_tier'
        )

        for member in active_members:
            if self.evaluate_member_for_segment(member, segment):
                qualifying_members.append(member)

        self.logger.debug(
            f"Segment {segment.id} ({segment.name}): "
            f"{len(qualifying_members)} qualifying members"
        )

        return qualifying_members

    def refresh_segment_memberships(self, segment: LoyaltySegment) -> Dict[str, int]:
        """
        Refresh all memberships for a segment.
        Adds new qualifying members, removes non-qualifying members.

        Args:
            segment: LoyaltySegment to refresh

        Returns:
            Dict with added, removed, and total counts
        """
        if not segment.is_active:
            return {'added': 0, 'removed': 0, 'total': 0}

        if segment.criteria_type == 'manual':
            # Don't auto-refresh manual segments
            return {'added': 0, 'removed': 0, 'total': segment.member_count}

        qualifying_members = self.get_segment_members(segment)
        qualifying_member_ids = {m.id for m in qualifying_members}

        # Get current members
        current_memberships = LoyaltySegmentMembership.objects.filter(
            segment=segment
        ).select_related('member')

        current_member_ids = {m.member_id for m in current_memberships}

        # Add new members
        to_add = qualifying_member_ids - current_member_ids
        added_count = 0

        for member_id in to_add:
            LoyaltySegmentMembership.objects.create(
                segment=segment,
                member_id=member_id
            )
            added_count += 1

        # Remove members who no longer qualify
        to_remove = current_member_ids - qualifying_member_ids
        removed_count = 0

        for membership in current_memberships:
            if membership.member_id in to_remove:
                # Remove all non-qualifying members from dynamic segments
                membership.delete()
                removed_count += 1

        # Update segment member count
        segment.member_count = LoyaltySegmentMembership.objects.filter(
            segment=segment
        ).count()
        segment.last_calculated_at = timezone.now()
        segment.save(update_fields=['member_count', 'last_calculated_at'])

        self.logger.info(
            f"Refreshed segment {segment.id} ({segment.name}): "
            f"+{added_count}, -{removed_count}, total={segment.member_count}"
        )

        return {
            'added': added_count,
            'removed': removed_count,
            'total': segment.member_count
        }

    def refresh_all_segments(self) -> Dict[str, Any]:
        """
        Refresh memberships for all active dynamic segments.

        Returns:
            Dict with summary statistics
        """
        active_segments = LoyaltySegment.objects.filter(
            is_active=True
        ).exclude(criteria_type='manual')

        total_added = 0
        total_removed = 0
        segments_processed = 0

        for segment in active_segments:
            try:
                result = self.refresh_segment_memberships(segment)
                total_added += result['added']
                total_removed += result['removed']
                segments_processed += 1
            except Exception as e:
                self.logger.error(f"Error refreshing segment {segment.id}: {e}")

        self.logger.info(
            f"Refreshed {segments_processed} segments: "
            f"+{total_added}, -{total_removed}"
        )

        return {
            'segments_processed': segments_processed,
            'total_added': total_added,
            'total_removed': total_removed
        }

    def add_member_to_segment(
        self,
        member: LoyaltyMember,
        segment: LoyaltySegment,
        automatically: bool = False
    ) -> Optional[LoyaltySegmentMembership]:
        """
        Manually add a member to a segment.

        Args:
            member: LoyaltyMember to add
            segment: LoyaltySegment to add to
            automatically: Whether this was added automatically

        Returns:
            LoyaltySegmentMembership if created, None if already exists
        """
        membership, created = LoyaltySegmentMembership.objects.get_or_create(
            segment=segment,
            member=member
        )

        if created:
            # Update segment count
            segment.member_count = LoyaltySegmentMembership.objects.filter(
                segment=segment
            ).count()
            segment.save(update_fields=['member_count'])

            self.logger.info(
                f"Added member {member.id} to segment {segment.id} "
                f"(auto={automatically})"
            )

        return membership if created else None

    def remove_member_from_segment(
        self,
        member: LoyaltyMember,
        segment: LoyaltySegment
    ) -> bool:
        """
        Manually remove a member from a segment.

        Args:
            member: LoyaltyMember to remove
            segment: LoyaltySegment to remove from

        Returns:
            bool: True if removed, False if not found
        """
        deleted_count, _ = LoyaltySegmentMembership.objects.filter(
            segment=segment,
            member=member
        ).delete()

        if deleted_count > 0:
            # Update segment count
            segment.member_count = LoyaltySegmentMembership.objects.filter(
                segment=segment
            ).count()
            segment.save(update_fields=['member_count'])

            self.logger.info(f"Removed member {member.id} from segment {segment.id}")
            return True

        return False
