"""
Redemption Engine Service

Handles all redemption operations including:
- Redemption creation and validation
- Redemption code generation
- State transitions (pending -> confirmed -> fulfilled)
- Voucher/discount code generation
- Points deduction and refund
- Cancellation and expiration handling
"""

import random
import string
from decimal import Decimal
from datetime import timedelta
from django.db import transaction as db_transaction
from django.utils import timezone
from django.core.exceptions import ValidationError

from loyalty.models import (
    LoyaltyReward,
    LoyaltyRedemption,
    LoyaltyMember,
    LoyaltyTransaction,
)
from loyalty.services.ledger_service import LedgerService


class RedemptionEngine:
    """
    Service class for managing loyalty reward redemptions.

    Handles the complete redemption lifecycle with proper error handling
    and database transaction safety.
    """

    def __init__(self):
        self.ledger = LedgerService()

    def generate_redemption_code(self):
        """
        Generate a unique redemption code.

        Format: LOYALTY-XXXXX-XXXXX
        """
        while True:
            part1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            part2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            code = f"LOYALTY-{part1}-{part2}"

            # Check uniqueness
            if not LoyaltyRedemption.objects.filter(redemption_code=code).exists():
                return code

    @db_transaction.atomic
    def redeem_reward(self, member, reward, **kwargs):
        """
        Create a new redemption for a member.

        Args:
            member (LoyaltyMember): Member redeeming the reward
            reward (LoyaltyReward): Reward to redeem
            **kwargs: Optional parameters (admin_note, etc.)

        Returns:
            tuple: (LoyaltyRedemption, success: bool, message: str)

        Raises:
            ValidationError: If redemption is not allowed
        """
        # Validate eligibility
        can_redeem, reason = reward.can_member_redeem(member)
        if not can_redeem:
            raise ValidationError(reason)

        # Check quantity availability (with lock for safety)
        if reward.quantity_remaining is not None:
            reward = LoyaltyReward.objects.select_for_update().get(pk=reward.pk)
            if reward.quantity_remaining <= 0:
                raise ValidationError("Reward is out of stock")

        # Generate redemption code
        redemption_code = self.generate_redemption_code()

        # Calculate expiration
        expires_at = None
        if reward.redemption_expires_days:
            expires_at = timezone.now() + timedelta(days=reward.redemption_expires_days)

        # Create redemption record
        redemption = LoyaltyRedemption.objects.create(
            member=member,
            reward=reward,
            redemption_code=redemption_code,
            points_spent=reward.points_cost,
            status=LoyaltyRedemption.STATUS_PENDING,
            expires_at=expires_at,
            admin_note=kwargs.get('admin_note', '')
        )

        # Deduct points (creates transaction)
        try:
            points_transaction = self.ledger.record_redemption(
                member=member,
                points=reward.points_cost,
                description=f"Redeemed: {reward.name}",
                redemption=redemption
            )

            redemption.transaction = points_transaction
            redemption.save(update_fields=['transaction'])

        except Exception as e:
            # If points deduction fails, delete redemption and re-raise
            redemption.delete()
            raise ValidationError(f"Failed to deduct points: {str(e)}")

        # Update reward quantity
        if reward.quantity_remaining is not None:
            reward.quantity_remaining -= 1
            reward.save(update_fields=['quantity_remaining', 'updated_at'])

        return redemption, True, "Redemption created successfully"

    @db_transaction.atomic
    def confirm_redemption(self, redemption, **kwargs):
        """
        Confirm a pending redemption.

        This transitions the redemption from pending to confirmed state
        and generates any necessary codes/vouchers.

        Args:
            redemption (LoyaltyRedemption): Redemption to confirm
            **kwargs: Optional parameters

        Returns:
            tuple: (success: bool, message: str)
        """
        if redemption.status != LoyaltyRedemption.STATUS_PENDING:
            return False, f"Cannot confirm redemption with status: {redemption.status}"

        # Check expiration
        if redemption.is_expired():
            self.expire_redemption(redemption)
            return False, "Redemption has expired"

        # Generate voucher code for discount rewards
        if redemption.reward.reward_type == LoyaltyReward.TYPE_DISCOUNT:
            voucher = self._generate_voucher_code(redemption)
            if voucher:
                redemption.voucher_code = voucher
            else:
                return False, "Failed to generate voucher code"

        # Update status
        redemption.status = LoyaltyRedemption.STATUS_CONFIRMED
        redemption.confirmed_at = timezone.now()
        redemption.save(update_fields=['status', 'confirmed_at', 'voucher_code', 'updated_at'])

        return True, "Redemption confirmed successfully"

    @db_transaction.atomic
    def fulfill_redemption(self, redemption, **kwargs):
        """
        Mark a redemption as fulfilled.

        This is the final state indicating the reward was delivered/used.

        Args:
            redemption (LoyaltyRedemption): Redemption to fulfill
            **kwargs: Optional parameters (order, admin_note)

        Returns:
            tuple: (success: bool, message: str)
        """
        if redemption.status not in [LoyaltyRedemption.STATUS_PENDING, LoyaltyRedemption.STATUS_CONFIRMED]:
            return False, f"Cannot fulfill redemption with status: {redemption.status}"

        # Update status
        redemption.status = LoyaltyRedemption.STATUS_FULFILLED
        redemption.fulfilled_at = timezone.now()

        # Link to order if provided
        if 'order' in kwargs:
            redemption.order = kwargs['order']

        if 'admin_note' in kwargs:
            redemption.admin_note = kwargs['admin_note']

        redemption.save(update_fields=['status', 'fulfilled_at', 'order', 'admin_note', 'updated_at'])

        return True, "Redemption fulfilled successfully"

    @db_transaction.atomic
    def cancel_redemption(self, redemption, reason="", refund_points=True):
        """
        Cancel a redemption and optionally refund points.

        Args:
            redemption (LoyaltyRedemption): Redemption to cancel
            reason (str): Cancellation reason
            refund_points (bool): Whether to refund points

        Returns:
            tuple: (success: bool, message: str)
        """
        if not redemption.can_cancel():
            return False, f"Cannot cancel redemption with status: {redemption.status}"

        # Refund points if requested
        if refund_points:
            try:
                self.ledger.manual_adjustment(
                    member=redemption.member,
                    points=redemption.points_spent,
                    reason=f"Refund for cancelled redemption: {redemption.redemption_code}",
                    admin_user=None
                )
            except Exception as e:
                return False, f"Failed to refund points: {str(e)}"

        # Restore reward quantity
        if redemption.reward.quantity_remaining is not None:
            reward = LoyaltyReward.objects.select_for_update().get(pk=redemption.reward.pk)
            reward.quantity_remaining += 1
            reward.save(update_fields=['quantity_remaining', 'updated_at'])

        # Update redemption status
        redemption.status = LoyaltyRedemption.STATUS_CANCELLED
        redemption.cancelled_at = timezone.now()
        redemption.cancellation_reason = reason or "Cancelled by admin"
        redemption.save(update_fields=['status', 'cancelled_at', 'cancellation_reason', 'updated_at'])

        return True, "Redemption cancelled and points refunded" if refund_points else "Redemption cancelled"

    @db_transaction.atomic
    def expire_redemption(self, redemption):
        """
        Mark a redemption as expired.

        Args:
            redemption (LoyaltyRedemption): Redemption to expire

        Returns:
            tuple: (success: bool, message: str)
        """
        if redemption.status in [LoyaltyRedemption.STATUS_FULFILLED, LoyaltyRedemption.STATUS_CANCELLED]:
            return False, "Redemption is already in a final state"

        # Refund points for expired redemptions
        try:
            self.ledger.manual_adjustment(
                member=redemption.member,
                points=redemption.points_spent,
                reason=f"Refund for expired redemption: {redemption.redemption_code}",
                admin_user=None
            )
        except Exception as e:
            return False, f"Failed to refund points: {str(e)}"

        # Restore reward quantity
        if redemption.reward.quantity_remaining is not None:
            reward = LoyaltyReward.objects.select_for_update().get(pk=redemption.reward.pk)
            reward.quantity_remaining += 1
            reward.save(update_fields=['quantity_remaining', 'updated_at'])

        # Update status
        redemption.status = LoyaltyRedemption.STATUS_EXPIRED
        redemption.save(update_fields=['status', 'updated_at'])

        return True, "Redemption expired and points refunded"

    def process_expired_redemptions(self):
        """
        Batch process all expired redemptions.

        This should be run periodically (e.g., daily cron job).

        Returns:
            dict: Statistics about processed redemptions
        """
        now = timezone.now()

        # Find expired redemptions
        expired_redemptions = LoyaltyRedemption.objects.filter(
            status__in=[LoyaltyRedemption.STATUS_PENDING, LoyaltyRedemption.STATUS_CONFIRMED],
            expires_at__lte=now
        )

        stats = {
            'total_found': expired_redemptions.count(),
            'processed': 0,
            'failed': 0,
            'errors': []
        }

        for redemption in expired_redemptions:
            try:
                success, message = self.expire_redemption(redemption)
                if success:
                    stats['processed'] += 1
                else:
                    stats['failed'] += 1
                    stats['errors'].append(f"{redemption.redemption_code}: {message}")
            except Exception as e:
                stats['failed'] += 1
                stats['errors'].append(f"{redemption.redemption_code}: {str(e)}")

        return stats

    def _generate_voucher_code(self, redemption):
        """
        Generate a voucher code for discount redemptions.

        Args:
            redemption (LoyaltyRedemption): Redemption to generate voucher for

        Returns:
            VoucherCode or None: Generated voucher code
        """
        # This will integrate with the vouchers app
        # For now, return None (to be implemented when integrating with checkout)
        try:
            from vouchers.models import Voucher, VoucherCode

            reward = redemption.reward

            # Create or get a voucher for this reward
            voucher, created = Voucher.objects.get_or_create(
                name=f"Loyalty Reward: {reward.name}",
                defaults={
                    'code_prefix': 'LOYALTY',
                    'discount_type': reward.discount_type,
                    'discount_value': reward.discount_value,
                    'min_purchase_amount': reward.min_purchase_amount or Decimal('0.00'),
                    'usage_limit_per_customer': 1,
                    'is_active': True,
                }
            )

            # Generate unique code
            code_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            code = f"{voucher.code_prefix}-{code_suffix}"

            # Create voucher code
            voucher_code = VoucherCode.objects.create(
                voucher=voucher,
                code=code,
                usage_limit=1,
                expires_at=redemption.expires_at
            )

            return voucher_code

        except ImportError:
            # Vouchers app not available
            return None
        except Exception as e:
            # Log error
            print(f"Error generating voucher code: {e}")
            return None

    def get_available_rewards(self, member):
        """
        Get all rewards available to a specific member.

        Args:
            member (LoyaltyMember): Member to check rewards for

        Returns:
            QuerySet: Available rewards with eligibility info
        """
        rewards = LoyaltyReward.objects.filter(
            is_active=True
        ).select_related('required_tier')

        available_rewards = []

        for reward in rewards:
            can_redeem, reason = reward.can_member_redeem(member)
            reward.can_redeem = can_redeem
            reward.eligibility_reason = reason
            available_rewards.append(reward)

        return available_rewards

    def get_member_redemptions(self, member, status=None):
        """
        Get redemptions for a member with optional status filter.

        Args:
            member (LoyaltyMember): Member to get redemptions for
            status (str, optional): Filter by status

        Returns:
            QuerySet: Member's redemptions
        """
        queryset = LoyaltyRedemption.objects.filter(
            member=member
        ).select_related('reward', 'transaction', 'order', 'voucher_code')

        if status:
            queryset = queryset.filter(status=status)

        return queryset.order_by('-created_at')
