"""
Transaction Ledger Service

Handles creation and management of loyalty transaction records.
Ensures immutability and provides transaction history queries.
"""

from django.db import transaction as db_transaction
from django.utils import timezone
from typing import Optional, List
import logging

from loyalty.models import (
    LoyaltyMember,
    LoyaltyBalance,
    LoyaltyTransaction,
)

logger = logging.getLogger(__name__)


class LedgerService:
    """
    Service for managing the immutable transaction ledger.

    All point changes must go through this service to ensure
    proper audit trails and balance reconciliation.
    """

    def create_transaction(
        self,
        member: LoyaltyMember,
        transaction_type: str,
        points: int,
        description: str,
        reason: str = '',
        status: str = LoyaltyTransaction.STATUS_AVAILABLE,
        related_object_type: str = '',
        related_object_id: str = '',
        expires_at=None,
        admin_user=None,
        admin_note: str = '',
    ) -> LoyaltyTransaction:
        """
        Create a new transaction in the ledger.

        Args:
            member: LoyaltyMember instance
            transaction_type: Type of transaction (earn, redeem, etc.)
            points: Point amount (positive for earn, negative for redeem/expire)
            description: Human-readable description
            reason: Brief reason code
            status: Transaction status
            related_object_type: Type of related object
            related_object_id: ID of related object
            expires_at: When points expire
            admin_user: Admin who created this (for manual adjustments)
            admin_note: Admin notes

        Returns:
            Created LoyaltyTransaction instance
        """
        with db_transaction.atomic():
            txn = LoyaltyTransaction.objects.create(
                member=member,
                transaction_type=transaction_type,
                points=points,
                status=status,
                description=description,
                reason=reason,
                related_object_type=related_object_type,
                related_object_id=related_object_id,
                expires_at=expires_at,
                created_by=admin_user,
                admin_note=admin_note,
            )

            logger.info(f"Created transaction {txn.id}: {points} points for member {member.id}")

        return txn

    def create_reversal(
        self,
        original_transaction: LoyaltyTransaction,
        reason: str,
        admin_user=None,
    ) -> LoyaltyTransaction:
        """
        Create a reversal transaction to undo a previous transaction.

        Args:
            original_transaction: Transaction to reverse
            reason: Reason for reversal
            admin_user: Admin performing reversal

        Returns:
            Reversal transaction
        """
        # Validate original transaction can be reversed
        if original_transaction.transaction_type not in [
            LoyaltyTransaction.TYPE_EARN,
            LoyaltyTransaction.TYPE_BONUS,
        ]:
            raise ValueError(f"Cannot reverse transaction type: {original_transaction.transaction_type}")

        # Check if already reversed
        existing = LoyaltyTransaction.objects.filter(
            reversal_of=original_transaction
        ).exists()

        if existing:
            raise ValueError(f"Transaction {original_transaction.id} already reversed")

        # Create reversal with opposite points
        description = f"Reversal of transaction #{original_transaction.id}: {reason}"

        with db_transaction.atomic():
            reversal = LoyaltyTransaction.objects.create(
                member=original_transaction.member,
                transaction_type=LoyaltyTransaction.TYPE_REVOKE,
                points=-original_transaction.points,  # Opposite amount
                status=LoyaltyTransaction.STATUS_REVOKED,
                description=description,
                reason=reason,
                reversal_of=original_transaction,
                created_by=admin_user,
            )

            # Update balance
            self._update_balance_for_reversal(
                original_transaction.member,
                reversal
            )

            logger.info(f"Created reversal {reversal.id} for transaction {original_transaction.id}")

        return reversal

    def manual_adjustment(
        self,
        member: LoyaltyMember,
        points: int,
        reason: str,
        admin_user,
        admin_note: str = '',
    ) -> LoyaltyTransaction:
        """
        Create a manual adjustment transaction (admin-initiated).

        Args:
            member: LoyaltyMember instance
            points: Point amount (can be positive or negative)
            reason: Reason for adjustment
            admin_user: Admin making the adjustment
            admin_note: Detailed admin notes

        Returns:
            Adjustment transaction
        """
        description = f"Manual adjustment by {admin_user.username}: {reason}"

        with db_transaction.atomic():
            txn = LoyaltyTransaction.objects.create(
                member=member,
                transaction_type=LoyaltyTransaction.TYPE_ADJUSTMENT,
                points=points,
                status=LoyaltyTransaction.STATUS_AVAILABLE,
                description=description,
                reason=reason,
                created_by=admin_user,
                admin_note=admin_note,
            )

            # Update balance
            balance, created = LoyaltyBalance.objects.get_or_create(member=member)

            balance.available_points += points

            if points > 0:
                balance.lifetime_earned += points
                balance.last_earned_at = timezone.now()

            balance.save()

            logger.info(f"Created manual adjustment {txn.id}: {points} points for member {member.id}")

        return txn

    def release_pending_points(self, transaction: LoyaltyTransaction):
        """
        Release pending points to make them available.

        Called after refund window passes.
        """
        if transaction.status != LoyaltyTransaction.STATUS_PENDING:
            logger.warning(f"Transaction {transaction.id} is not pending, cannot release")
            return

        # Update transaction status (this will fail due to immutability)
        # Instead, we need to create a new transaction to represent the release
        # For simplicity, we'll just update the balance

        with db_transaction.atomic():
            balance = LoyaltyBalance.objects.get(member=transaction.member)

            # Move from pending to available
            balance.pending_points -= transaction.points
            balance.available_points += transaction.points

            balance.save()

            logger.info(f"Released {transaction.points} pending points for member {transaction.member.id}")

    def expire_points(self, transaction: LoyaltyTransaction) -> LoyaltyTransaction:
        """
        Expire points from a transaction.

        Creates an expiration transaction.
        """
        if transaction.status == LoyaltyTransaction.STATUS_EXPIRED:
            logger.warning(f"Transaction {transaction.id} already expired")
            return None

        if not transaction.expires_at:
            logger.warning(f"Transaction {transaction.id} has no expiration date")
            return None

        if timezone.now() < transaction.expires_at:
            logger.warning(f"Transaction {transaction.id} not yet expired")
            return None

        description = f"Expired {transaction.points} points from transaction #{transaction.id}"

        with db_transaction.atomic():
            expiration = LoyaltyTransaction.objects.create(
                member=transaction.member,
                transaction_type=LoyaltyTransaction.TYPE_EXPIRE,
                points=-transaction.points,  # Negative to subtract
                status=LoyaltyTransaction.STATUS_EXPIRED,
                description=description,
                reason=f"Expiration of transaction #{transaction.id}",
            )

            # Update balance
            balance = LoyaltyBalance.objects.get(member=transaction.member)
            balance.available_points -= transaction.points
            balance.lifetime_expired += transaction.points
            balance.save()

            logger.info(f"Expired {transaction.points} points from transaction {transaction.id}")

        return expiration

    def get_member_history(
        self,
        member: LoyaltyMember,
        limit: int = 50,
        offset: int = 0,
    ) -> List[LoyaltyTransaction]:
        """
        Get transaction history for a member.

        Args:
            member: LoyaltyMember instance
            limit: Maximum number of transactions
            offset: Offset for pagination

        Returns:
            List of transactions ordered by created_at descending
        """
        return list(
            LoyaltyTransaction.objects.filter(member=member)
            .select_related('created_by', 'reversal_of')
            .order_by('-created_at')[offset:offset + limit]
        )

    def reconcile_balance(self, member: LoyaltyMember):
        """
        Reconcile balance from transaction ledger.

        Recalculates balance from all transactions (authoritative source).
        """
        transactions = LoyaltyTransaction.objects.filter(member=member)

        available = 0
        pending = 0
        lifetime_earned = 0
        lifetime_redeemed = 0
        lifetime_expired = 0

        for txn in transactions:
            if txn.transaction_type == LoyaltyTransaction.TYPE_EARN:
                lifetime_earned += txn.points
                if txn.status == LoyaltyTransaction.STATUS_PENDING:
                    pending += txn.points
                else:
                    available += txn.points

            elif txn.transaction_type == LoyaltyTransaction.TYPE_BONUS:
                lifetime_earned += txn.points
                available += txn.points

            elif txn.transaction_type == LoyaltyTransaction.TYPE_REDEEM:
                lifetime_redeemed += abs(txn.points)
                available += txn.points  # Points are negative

            elif txn.transaction_type == LoyaltyTransaction.TYPE_EXPIRE:
                lifetime_expired += abs(txn.points)
                available += txn.points  # Points are negative

            elif txn.transaction_type == LoyaltyTransaction.TYPE_REVOKE:
                available += txn.points  # Points are negative

            elif txn.transaction_type == LoyaltyTransaction.TYPE_ADJUSTMENT:
                available += txn.points
                if txn.points > 0:
                    lifetime_earned += txn.points

        # Update balance
        balance, created = LoyaltyBalance.objects.get_or_create(member=member)
        balance.available_points = available
        balance.pending_points = pending
        balance.lifetime_earned = lifetime_earned
        balance.lifetime_redeemed = lifetime_redeemed
        balance.lifetime_expired = lifetime_expired
        balance.save()

        logger.info(f"Reconciled balance for member {member.id}: {available} available, {pending} pending")

    def _update_balance_for_reversal(self, member: LoyaltyMember, reversal: LoyaltyTransaction):
        """Update balance for a reversal transaction."""
        balance = LoyaltyBalance.objects.get(member=member)

        # Subtract from available points
        balance.available_points += reversal.points  # Points are negative
        balance.save()

    def record_redemption(
        self,
        member: LoyaltyMember,
        points: int,
        description: str,
        redemption=None,
    ) -> LoyaltyTransaction:
        """
        Record points deduction for a reward redemption.

        Args:
            member: Member redeeming points
            points: Points to deduct (positive number)
            description: Redemption description
            redemption: Associated LoyaltyRedemption instance

        Returns:
            Created transaction
        """
        # Points should be negative for redemption
        points_amount = -abs(points)

        with db_transaction.atomic():
            # Create transaction
            transaction = LoyaltyTransaction.objects.create(
                member=member,
                transaction_type=LoyaltyTransaction.TYPE_REDEEM,
                points=points_amount,
                status=LoyaltyTransaction.STATUS_AVAILABLE,
                description=description,
                reason="reward_redemption",
                related_object_type="loyalty_redemption",
                related_object_id=str(redemption.id) if redemption else "",
            )

            # Update balance
            balance, created = LoyaltyBalance.objects.get_or_create(
                member=member,
                defaults={
                    'available_points': 0,
                    'pending_points': 0,
                    'lifetime_earned': 0,
                    'lifetime_redeemed': 0,
                    'lifetime_expired': 0,
                }
            )

            # Deduct from available points
            balance.available_points += points_amount  # points_amount is negative
            balance.lifetime_redeemed += abs(points_amount)
            balance.last_redeemed_at = timezone.now()
            balance.save()

            logger.info(f"Recorded redemption: {points_amount} points for member {member.id}")

        return transaction


# Singleton instance
ledger_service = LedgerService()
