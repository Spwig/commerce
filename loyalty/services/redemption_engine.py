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

import logging
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import transaction as db_transaction
from django.utils import timezone

from core.utils.codes import generate_unique_code
from loyalty.models import (
    LoyaltyRedemption,
    LoyaltyReward,
)
from loyalty.services.ledger_service import LedgerService

logger = logging.getLogger(__name__)


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

        Uses the shared secrets-backed generator: this code is a bearer
        credential, and the previous ``random.choices`` implementation was
        predictable from observed output.
        """
        return generate_unique_code(
            exists=lambda code: LoyaltyRedemption.objects.filter(redemption_code=code).exists(),
            length=5,
            groups=2,
            prefix="LOYALTY",
        )

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
            admin_note=kwargs.get("admin_note", ""),
        )

        # Deduct points (creates transaction)
        try:
            points_transaction = self.ledger.record_redemption(
                member=member,
                points=reward.points_cost,
                description=f"Redeemed: {reward.name}",
                redemption=redemption,
            )

            redemption.transaction = points_transaction
            redemption.save(update_fields=["transaction"])

        except Exception as e:
            # If points deduction fails, delete redemption and re-raise
            redemption.delete()
            raise ValidationError(f"Failed to deduct points: {str(e)}")

        # Update reward quantity
        if reward.quantity_remaining is not None:
            reward.quantity_remaining -= 1
            reward.save(update_fields=["quantity_remaining", "updated_at"])

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
        # Lock and re-read before the status check. cancel_redemption and
        # expire_redemption already do this; confirm did not, so two racing
        # confirms could both read PENDING and both issue. The database
        # constraint on (source='loyalty', reference_id) is the backstop for
        # the fixed-value path, but the lock stops the race for every path.
        redemption = LoyaltyRedemption.objects.select_for_update().get(pk=redemption.pk)

        if redemption.status != LoyaltyRedemption.STATUS_PENDING:
            return False, f"Cannot confirm redemption with status: {redemption.status}"

        # Check expiration
        if redemption.is_expired():
            self.expire_redemption(redemption)
            return False, "Redemption has expired"

        # Discount rewards: D2 routing, live as of P2.5c.
        #   fixed      -> wallet credit (the wallet is the store-credit ledger,
        #                 and is spendable at checkout as of P2.5a/b — minting
        #                 before that existed would have been "points deducted,
        #                 unspendable number displayed").
        #   percentage -> a real single-use VoucherCode issued to the member.
        # Any issuance failure falls through to the R1 refund-and-cancel path,
        # which is idempotent and already surfaces the double-failure case.
        if redemption.reward.reward_type == LoyaltyReward.TYPE_DISCOUNT:
            issued, issue_message = self._issue_discount_reward(redemption)
            if issued:
                redemption.status = LoyaltyRedemption.STATUS_CONFIRMED
                redemption.confirmed_at = timezone.now()
                redemption.save(
                    update_fields=[
                        "status",
                        "confirmed_at",
                        "voucher_code",
                        "updated_at",
                    ]
                )
                return True, issue_message

            refunded, refund_message = self._refund_points(
                redemption,
                reason=(f"Discount reward could not be issued: {redemption.redemption_code}"),
            )
            if not refunded:
                logger.error(
                    f"Redemption {redemption.redemption_code} could not be issued AND "
                    f"its points could not be refunded: {refund_message}. "
                    f"Member {redemption.member_id} is owed "
                    f"{redemption.points_spent} points."
                )
                return False, (
                    "Your reward could not be issued, and refunding your "
                    "points failed. Support has been notified."
                )

            redemption.status = LoyaltyRedemption.STATUS_CANCELLED
            redemption.cancelled_at = timezone.now()
            redemption.cancellation_reason = f"Issuance failed: {issue_message}"[:255]
            redemption.save(
                update_fields=[
                    "status",
                    "cancelled_at",
                    "cancellation_reason",
                    "updated_at",
                ]
            )

            if redemption.reward.quantity_remaining is not None:
                reward = LoyaltyReward.objects.select_for_update().get(pk=redemption.reward.pk)
                reward.quantity_remaining += 1
                reward.save(update_fields=["quantity_remaining", "updated_at"])

            return False, (
                "Your reward could not be issued. Your points have been returned to your balance."
            )

        # Update status
        redemption.status = LoyaltyRedemption.STATUS_CONFIRMED
        redemption.confirmed_at = timezone.now()
        redemption.save(update_fields=["status", "confirmed_at", "voucher_code", "updated_at"])

        return True, "Redemption confirmed successfully"

    def _issue_discount_reward(self, redemption):
        """
        Issue what a discount redemption actually promises (D2).

        Returns (success, message). Never raises — a failure message feeds the
        caller's refund-and-cancel path, so the member always ends up with
        either the reward or their points, never neither.
        """
        reward = redemption.reward

        if reward.discount_type == LoyaltyReward.DISCOUNT_TYPE_FIXED:
            return self._issue_wallet_credit(redemption)
        if reward.discount_type == LoyaltyReward.DISCOUNT_TYPE_PERCENTAGE:
            return self._issue_percentage_voucher(redemption)

        return False, f"Unknown discount type: {reward.discount_type!r}"

    def _issue_wallet_credit(self, redemption):
        """
        Fixed-value reward -> wallet credit, exactly once per redemption.

        Idempotency is the partial UniqueConstraint on
        (source='loyalty', reference_id=redemption.uuid) — an existing row
        means a previous confirm already paid, so this reports success without
        crediting again rather than treating the collision as failure: the
        member HAS their money.
        """
        from core.utils import get_default_currency
        from wallet.models import WalletTransaction
        from wallet.services import WalletService

        reward = redemption.reward
        if not reward.discount_value or reward.discount_value <= 0:
            return False, "Reward has no discount value configured"

        already = WalletTransaction.objects.filter(
            source=WalletTransaction.SOURCE_LOYALTY,
            reference_id=str(redemption.uuid),
        ).exists()
        if already:
            logger.info(
                f"Redemption {redemption.redemption_code} already credited a "
                f"wallet; treating confirm as already done"
            )
            return True, "Reward already credited to your wallet"

        try:
            WalletService.credit(
                redemption.member.customer,
                reward.discount_value,
                get_default_currency(),
                WalletTransaction.SOURCE_LOYALTY,
                f"Loyalty reward: {reward.name}",
                reference_id=str(redemption.uuid),
            )
        except Exception as exc:  # frozen wallet, currency mismatch, race loser
            logger.warning(
                f"Wallet credit failed for redemption {redemption.redemption_code}: {exc}"
            )
            return False, str(exc)

        return True, "Reward credited to your wallet"

    def _issue_percentage_voucher(self, redemption):
        """
        Percentage reward -> a real single-use VoucherCode, issued to the
        member so nobody else holding the string can spend it.

        Mirrors referrals.create_percentage_coupon. LoyaltyReward has no
        max_discount_amount field, so the voucher is UNCAPPED — a deliberate
        product decision (forcing a cap would change merchant-facing reward
        config mid-release); the warning below is the audit trail for it.
        """
        from djmoney.money import Money

        from core.utils import get_default_currency
        from core.utils.codes import generate_unique_code
        from vouchers.models import VoucherCode

        reward = redemption.reward
        if not reward.discount_value or reward.discount_value <= 0:
            return False, "Reward has no discount percentage configured"

        if redemption.voucher_code_id:
            return True, "Reward voucher already issued"

        currency = get_default_currency()
        logger.warning(
            f"Minting UNCAPPED {reward.discount_value}% voucher for redemption "
            f"{redemption.redemption_code}: LoyaltyReward has no maximum "
            f"discount amount, so the value is bounded only by the order it "
            f"is spent on."
        )

        try:
            voucher = VoucherCode.objects.create(
                code=generate_unique_code(
                    lambda c: VoucherCode.objects.filter(code=c).exists(),
                    prefix="LOYAL",
                ),
                name=f"Loyalty Reward - {reward.name}"[:100],
                description=f"Redeemed with {redemption.points_spent} points",
                discount_type="percentage",
                discount_value=reward.discount_value,
                min_order_value=Money(0, currency),
                max_uses_total=1,
                max_uses_per_customer=1,
                issued_to=redemption.member.customer,
                is_active=True,
            )
        except Exception as exc:
            logger.warning(
                f"Voucher mint failed for redemption {redemption.redemption_code}: {exc}"
            )
            return False, str(exc)

        redemption.voucher_code = voucher
        return True, "Reward voucher issued"

    def _revoke_discount_reward(self, redemption):
        """
        Reverse the monetary benefit a discount redemption already issued, so
        the member cannot keep it after the points that bought it are refunded.

        The inverse of :meth:`_issue_discount_reward`:
          fixed      -> reverse the loyalty wallet credit.
          percentage -> deactivate the issued single-use voucher.

        Returns (success, message). A redemption that never issued anything (a
        pending redemption, a non-discount reward) is a no-op success. A
        benefit that has already been consumed cannot be revoked and returns
        failure, so the caller must abort rather than refund the points on top
        of a spent benefit.
        """
        reward = redemption.reward
        if reward.reward_type != LoyaltyReward.TYPE_DISCOUNT:
            return True, "No discount benefit to revoke"

        if reward.discount_type == LoyaltyReward.DISCOUNT_TYPE_FIXED:
            return self._revoke_wallet_credit(redemption)
        if reward.discount_type == LoyaltyReward.DISCOUNT_TYPE_PERCENTAGE:
            return self._revoke_percentage_voucher(redemption)

        return True, "No discount benefit to revoke"

    def _revoke_wallet_credit(self, redemption):
        """
        Reverse the loyalty wallet credit issued for a fixed-value redemption.

        Matches on (source='loyalty', reference_id=redemption.uuid) — the same
        key :meth:`_issue_wallet_credit` writes under. No live credit (a
        pending redemption, or one already reversed) is a no-op success; a
        credit already spent makes reverse_transaction raise, which surfaces as
        failure so the caller does not refund on top of spent store credit.
        """
        from wallet.models import WalletTransaction
        from wallet.services import WalletService

        credit = (
            WalletTransaction.objects.filter(
                source=WalletTransaction.SOURCE_LOYALTY,
                reference_id=str(redemption.uuid),
                transaction_type=WalletTransaction.TYPE_CREDIT,
            )
            .exclude(status=WalletTransaction.STATUS_REVERSED)
            .first()
        )
        if credit is None:
            return True, "No wallet credit to revoke"

        try:
            WalletService.reverse_transaction(
                credit,
                reason=f"Reversal for redemption {redemption.redemption_code}",
            )
        except Exception as exc:  # already spent, frozen wallet, race loser
            logger.warning(
                f"Could not reverse wallet credit for redemption "
                f"{redemption.redemption_code}: {exc}"
            )
            return False, f"Wallet credit could not be reversed: {exc}"

        return True, "Wallet credit reversed"

    def _revoke_percentage_voucher(self, redemption):
        """
        Deactivate the single-use voucher issued for a percentage redemption.

        No voucher (a pending redemption) is a no-op success. A voucher that
        has already been used cannot be clawed back, so it returns failure and
        the caller must not refund the points.
        """
        from vouchers.models import VoucherCode

        if not redemption.voucher_code_id:
            return True, "No voucher to revoke"

        voucher = VoucherCode.objects.select_for_update().get(pk=redemption.voucher_code_id)
        if voucher.current_uses > 0:
            return False, "Issued voucher has already been used and cannot be revoked"

        if voucher.is_active:
            voucher.is_active = False
            voucher.save(update_fields=["is_active", "updated_at"])

        return True, "Voucher deactivated"

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
        # Lock and re-read before the status check. cancel_redemption and
        # expire_redemption lock and finalize the row; without this lock a
        # concurrent cancel/expire could finalize (refund points, restore
        # stock) after this instance was loaded but before save(), and this
        # method would overwrite that final status with fulfilled.
        redemption = LoyaltyRedemption.objects.select_for_update().get(pk=redemption.pk)

        if redemption.status not in [
            LoyaltyRedemption.STATUS_PENDING,
            LoyaltyRedemption.STATUS_CONFIRMED,
        ]:
            return False, f"Cannot fulfill redemption with status: {redemption.status}"

        # A discount reward's benefit (wallet credit or voucher) is only issued
        # by confirm_redemption's _issue_discount_reward path. Fulfilling a
        # still-pending discount would mark it final with the member's points
        # spent but nothing issued, so confirm (and issue) first and only
        # proceed once issuance has succeeded.
        if (
            redemption.reward.reward_type == LoyaltyReward.TYPE_DISCOUNT
            and redemption.status == LoyaltyRedemption.STATUS_PENDING
        ):
            confirmed, confirm_message = self.confirm_redemption(redemption)
            if not confirmed:
                return False, confirm_message
            redemption.refresh_from_db()

        # Update status
        redemption.status = LoyaltyRedemption.STATUS_FULFILLED
        redemption.fulfilled_at = timezone.now()

        # Link to order if provided
        if "order" in kwargs:
            redemption.order = kwargs["order"]

        if "admin_note" in kwargs:
            redemption.admin_note = kwargs["admin_note"]

        redemption.save(
            update_fields=["status", "fulfilled_at", "order", "admin_note", "updated_at"]
        )

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
        # Lock and re-read before deciding, so two concurrent cancels cannot
        # both pass the guard and both refund/restock. See expire_redemption.
        redemption = LoyaltyRedemption.objects.select_for_update().get(pk=redemption.pk)

        if not redemption.can_cancel():
            return False, f"Cannot cancel redemption with status: {redemption.status}"

        # Revoke any already-issued discount benefit before returning the points
        # that bought it, so the member cannot keep both. Fail the cancellation
        # if the benefit cannot be revoked (e.g. a voucher already spent).
        revoked, revoke_message = self._revoke_discount_reward(redemption)
        if not revoked:
            return False, revoke_message

        # Refund points if requested
        if refund_points:
            refunded, refund_message = self._refund_points(
                redemption,
                reason=f"Refund for cancelled redemption: {redemption.redemption_code}",
            )
            if not refunded:
                # The revocation above already reversed the wallet credit /
                # deactivated the voucher. A plain return commits that inside
                # this atomic block, leaving the benefit revoked but the points
                # unrefunded and the redemption uncancelled. Roll the whole
                # cancellation back so revocation and refund stay all-or-nothing.
                db_transaction.set_rollback(True)
                return False, refund_message

        # Restore reward quantity
        if redemption.reward.quantity_remaining is not None:
            reward = LoyaltyReward.objects.select_for_update().get(pk=redemption.reward.pk)
            reward.quantity_remaining += 1
            reward.save(update_fields=["quantity_remaining", "updated_at"])

        # Update redemption status
        redemption.status = LoyaltyRedemption.STATUS_CANCELLED
        redemption.cancelled_at = timezone.now()
        redemption.cancellation_reason = reason or "Cancelled by admin"
        redemption.save(
            update_fields=["status", "cancelled_at", "cancellation_reason", "updated_at"]
        )

        return (
            True,
            "Redemption cancelled and points refunded" if refund_points else "Redemption cancelled",
        )

    @db_transaction.atomic
    def expire_redemption(self, redemption):
        """
        Mark a redemption as expired.

        Args:
            redemption (LoyaltyRedemption): Redemption to expire

        Returns:
            tuple: (success: bool, message: str)
        """
        # Lock and re-read before deciding: two concurrent expiries (a sweep
        # racing an admin action, or a retried task) would otherwise both pass
        # the status check.
        redemption = LoyaltyRedemption.objects.select_for_update().get(pk=redemption.pk)

        # STATUS_EXPIRED belongs in this list. Without it the method was
        # re-entrant: a second call re-ran the body, _refund_points reported
        # success on the already-refunded ledger row, and
        # `quantity_remaining += 1` ran again — minting a unit of reward stock
        # on every repeat call.
        if redemption.status in [
            LoyaltyRedemption.STATUS_FULFILLED,
            LoyaltyRedemption.STATUS_CANCELLED,
            LoyaltyRedemption.STATUS_EXPIRED,
        ]:
            return False, "Redemption is already in a final state"

        # Revoke any already-issued discount benefit before refunding the points
        # that bought it: a confirmed fixed reward holds a spendable wallet
        # credit and a confirmed percentage reward holds an active voucher, so
        # refunding without revoking would leave the member with both.
        revoked, revoke_message = self._revoke_discount_reward(redemption)
        if not revoked:
            return False, revoke_message

        # Refund points for expired redemptions
        refunded, refund_message = self._refund_points(
            redemption,
            reason=f"Refund for expired redemption: {redemption.redemption_code}",
        )
        if not refunded:
            # The revocation above already reversed the wallet credit /
            # deactivated the voucher. A plain return commits that inside this
            # atomic block, leaving the member with the benefit revoked but the
            # points not returned and the redemption unexpired. Roll the whole
            # expiry back so revocation and refund stay all-or-nothing.
            db_transaction.set_rollback(True)
            return False, refund_message

        # Restore reward quantity
        if redemption.reward.quantity_remaining is not None:
            reward = LoyaltyReward.objects.select_for_update().get(pk=redemption.reward.pk)
            reward.quantity_remaining += 1
            reward.save(update_fields=["quantity_remaining", "updated_at"])

        # Update status
        redemption.status = LoyaltyRedemption.STATUS_EXPIRED
        redemption.save(update_fields=["status", "updated_at"])

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
            expires_at__lte=now,
        )

        stats = {
            "total_found": expired_redemptions.count(),
            "processed": 0,
            "failed": 0,
            "errors": [],
        }

        for redemption in expired_redemptions:
            try:
                success, message = self.expire_redemption(redemption)
                if success:
                    stats["processed"] += 1
                else:
                    stats["failed"] += 1
                    stats["errors"].append(f"{redemption.redemption_code}: {message}")
            except Exception as e:
                stats["failed"] += 1
                stats["errors"].append(f"{redemption.redemption_code}: {str(e)}")

        return stats

    def _refund_points(self, redemption, reason):
        """
        Return the points a redemption spent.

        Prefers :meth:`LedgerService.refund_redemption`, which links the refund
        to the original redemption row and leaves ``lifetime_earned`` alone.
        That matters: ``lifetime_earned`` drives ``TieringService`` and
        ``SegmentEvaluator``, so refunding through ``manual_adjustment`` (as this
        code used to) can promote a member's tier as a side effect of a failed
        or cancelled redemption.

        Falls back to ``manual_adjustment`` only when the redemption has no
        linked transaction — which should not happen for anything created by
        :meth:`redeem_reward`, but is possible for legacy rows. The fallback
        carries the tier-inflation caveat above, so it is logged.

        Returns:
            tuple: (success: bool, message: str)
        """
        txn = redemption.transaction

        if txn is not None:
            try:
                self.ledger.refund_redemption(
                    redemption_transaction=txn,
                    reason=reason,
                )
                return True, "Points refunded"
            except ValueError as e:
                # Already refunded is not a failure: the points are back, which
                # is the outcome the caller wants. Anything else is.
                if "already refunded" in str(e):
                    logger.warning(
                        f"Redemption {redemption.redemption_code} was already refunded; "
                        f"treating as success"
                    )
                    return True, "Points already refunded"
                return False, f"Failed to refund points: {e}"

        logger.error(
            f"Redemption {redemption.redemption_code} has no linked transaction; "
            f"refunding via manual_adjustment, which will inflate lifetime_earned "
            f"and may affect tier assignment for this member."
        )
        try:
            self.ledger.manual_adjustment(
                member=redemption.member,
                points=redemption.points_spent,
                reason=reason,
                admin_user=None,
            )
            return True, "Points refunded"
        except Exception as e:
            return False, f"Failed to refund points: {e}"

    def get_available_rewards(self, member):
        """
        Get all rewards available to a specific member.

        Args:
            member (LoyaltyMember): Member to check rewards for

        Returns:
            QuerySet: Available rewards with eligibility info
        """
        rewards = LoyaltyReward.objects.filter(is_active=True).select_related("required_tier")

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
        queryset = LoyaltyRedemption.objects.filter(member=member).select_related(
            "reward", "transaction", "order", "voucher_code"
        )

        if status:
            queryset = queryset.filter(status=status)

        return queryset.order_by("-created_at")
