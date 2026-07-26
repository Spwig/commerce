"""
Rewards service for referral program.

Handles reward creation, issuance, redemption, revocation, and expiry.
"""

import logging
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from core.utils import get_default_currency
from core.utils.codes import generate_unique_code

logger = logging.getLogger(__name__)


def _validated_kind(kind, recipient_type):
    """
    Reject a reward kind that ``issue_reward`` cannot dispatch on.

    ``issue_reward`` falls through to ``success = False`` for an unrecognised
    kind, and ``create_and_issue_rewards`` only logs that as a generic failure —
    so a typo or a stale config value in ``program.reward_config`` silently
    produced rewards that were never issued. Failing at creation makes the
    misconfiguration visible at the point it can be fixed.

    Raises:
        ValueError: If ``kind`` is not one of ReferralReward.KIND_CHOICES.
    """
    from ..models import ReferralReward

    valid = {choice for choice, _label in ReferralReward.KIND_CHOICES}
    if kind not in valid:
        raise ValueError(
            f"Invalid {recipient_type} reward kind {kind!r} in program reward_config. "
            f"Expected one of {sorted(valid)}."
        )
    return kind


def create_rewards(attribution):
    """
    Create rewards for both referrer and referee.

    Args:
        attribution (ReferralAttribution): Approved attribution instance

    Returns:
        tuple: (referrer_reward: ReferralReward, referee_reward: ReferralReward or None)
    """
    from ..models import ReferralReward

    program = attribution.program
    reward_config = program.reward_config

    # Calculate expiry date
    expiry_days = reward_config.get("expiry_days", 90)
    expires_at = timezone.now() + timedelta(days=expiry_days) if expiry_days else None

    referrer_reward = None
    referee_reward = None

    # Create referrer reward
    if "referrer" in reward_config:
        referrer_config = reward_config["referrer"]

        referrer_reward = ReferralReward.objects.create(
            program=program,
            attribution=attribution,
            referrer_identity=attribution.referrer_identity,
            customer=attribution.referrer_identity.customer,
            recipient_type="referrer",
            kind=_validated_kind(referrer_config.get("kind", "credit"), "referrer"),
            amount=referrer_config.get("amount", 10),
            amount_currency=referrer_config.get("currency", get_default_currency()),
            percentage=referrer_config.get("percentage"),
            description=referrer_config.get("description", "Referral reward"),
            status="pending",
            expires_at=expires_at,
        )

    # Create referee reward (if double-sided)
    if reward_config.get("double_sided", False) and "referee" in reward_config:
        referee_config = reward_config["referee"]

        referee_reward = ReferralReward.objects.create(
            program=program,
            attribution=attribution,
            referrer_identity=attribution.referrer_identity,  # Link to referrer for tracking
            customer=attribution.referee_customer,
            recipient_type="referee",
            # Default "credit", matching the referrer branch above. This was
            # "discount", which is not in ReferralReward.KIND_CHOICES — any
            # referee config without an explicit kind produced a reward that
            # fell through the issue_reward dispatcher and was never issued,
            # logged only as a generic failure.
            kind=_validated_kind(referee_config.get("kind", "credit"), "referee"),
            amount=referee_config.get("amount", 10),
            amount_currency=referee_config.get("currency", get_default_currency()),
            percentage=referee_config.get("percentage"),
            description=referee_config.get("description", "Welcome reward"),
            status="pending",
            expires_at=expires_at,
        )

    return referrer_reward, referee_reward


@transaction.atomic
def issue_reward(reward):
    """
    Issue a reward to customer (create wallet credit or coupon).

    Args:
        reward (ReferralReward): Reward to issue

    Returns:
        bool: True if successful
    """
    if reward.status != "pending":
        return False

    # Issue based on reward kind
    if reward.kind == "credit":
        success = create_wallet_credit(reward)
    elif reward.kind == "coupon":
        success = create_coupon_code(reward)
    elif reward.kind == "percent":
        success = create_percentage_coupon(reward)
    elif reward.kind == "perk":
        # Perks are issued differently (manual or automated based on type)
        success = True
    else:
        success = False

    if success:
        # Mark reward as issued
        reward.issue()

        # Update referrer identity stats
        if reward.recipient_type == "referrer" and reward.referrer_identity:
            reward.referrer_identity.increment_conversions(reward.amount.amount)

        # Send notification email
        send_reward_issued_email(reward)

    return success


def create_and_issue_rewards(attribution):
    """
    Create and issue rewards for an approved attribution.

    Idempotent — skips if rewards already exist for this attribution.

    Args:
        attribution (ReferralAttribution): Approved attribution
    """
    from ..models import ReferralReward

    try:
        existing = ReferralReward.objects.filter(attribution=attribution).exists()
        if existing:
            logger.debug(f"Rewards already exist for attribution {attribution.id}, skipping")
            return

        referrer_reward, referee_reward = create_rewards(attribution)

        if referrer_reward:
            success = issue_reward(referrer_reward)
            if success:
                logger.info(
                    f"Issued referrer reward {referrer_reward.id} to {referrer_reward.customer.email}"
                )
            else:
                logger.error(f"Failed to issue referrer reward {referrer_reward.id}")

        if referee_reward:
            success = issue_reward(referee_reward)
            if success:
                logger.info(
                    f"Issued referee reward {referee_reward.id} to {referee_reward.customer.email}"
                )
            else:
                logger.error(f"Failed to issue referee reward {referee_reward.id}")

        # Send successful referral email to referrer
        if attribution.referrer_identity:
            try:
                from .email_notifications import send_referral_successful_email

                send_referral_successful_email(attribution)
            except Exception as e:
                logger.error(f"Error sending referral successful email: {e}", exc_info=True)

    except Exception as e:
        logger.error(
            f"Error creating/issuing rewards for attribution {attribution.id}: {e}", exc_info=True
        )


def redeem_reward(reward):
    """
    Mark reward as redeemed.

    Args:
        reward (ReferralReward): Reward to redeem

    Returns:
        bool: True if successful
    """
    if reward.status != "issued":
        return False

    reward.redeem()
    return True


@transaction.atomic
def revoke_reward(reward, reason=""):
    """
    Revoke a reward (reverse wallet credit or disable coupon).

    Args:
        reward (ReferralReward): Reward to revoke
        reason (str): Reason for revocation

    Returns:
        bool: True if successful
    """
    if reward.status not in ["pending", "issued"]:
        return False

    # Reverse integration based on reward kind
    if reward.kind == "credit" and reward.wallet_transaction_id:
        reverse_wallet_credit(reward)
    elif reward.kind in ["coupon", "percent"] and reward.voucher_code_id:
        disable_coupon_code(reward)

    # Mark reward as revoked
    reward.revoke(reason)

    # Send notification email
    send_reward_revoked_email(reward, reason)

    return True


def expire_old_rewards():
    """
    Batch job to expire unredeemed rewards past expiry date.

    Returns:
        int: Number of rewards expired
    """
    from ..models import ReferralReward

    # Find expired rewards
    expired_rewards = ReferralReward.objects.filter(status="issued", expires_at__lte=timezone.now())

    count = 0
    for reward in expired_rewards:
        # Reverse any wallet credits or coupons
        if reward.kind == "credit" and reward.wallet_transaction_id:
            reverse_wallet_credit(reward)
        elif reward.kind in ["coupon", "percent"] and reward.voucher_code_id:
            disable_coupon_code(reward)

        # Mark as expired
        reward.expire()
        count += 1

        # Send expiry notification
        send_reward_expired_email(reward)

    return count


def create_wallet_credit(reward):
    """
    Create wallet credit for customer.

    Args:
        reward (ReferralReward): Reward instance

    Returns:
        bool: True if successful
    """
    from wallet.services import WalletService

    txn = WalletService.credit(
        user=reward.customer,
        amount=reward.amount.amount,
        currency=str(reward.amount.currency),
        source="referral",
        description=f"Referral reward: {reward.description}",
        reference_id=str(reward.id),
    )

    reward.wallet_transaction_id = txn.id
    reward.save(update_fields=["wallet_transaction_id"])
    return True


def _generate_referral_voucher_code():
    """
    Generate a unique referral voucher code.

    Uses the shared secrets-backed generator. The previous implementation used
    ``random.choices`` (predictable from observed output) and had no uniqueness
    check at all, relying on the database to raise IntegrityError on collision.
    """
    from vouchers.models import VoucherCode

    return generate_unique_code(
        exists=lambda code: VoucherCode.objects.filter(code=code).exists(),
        length=8,
        prefix="REF",
        separator="",
    )


def create_coupon_code(reward):
    """
    Create a fixed-amount coupon for a referral reward.

    Args:
        reward (ReferralReward): Reward instance

    Returns:
        bool: True if successful
    """
    from djmoney.money import Money

    from vouchers.models import VoucherCode

    currency = reward.amount.currency

    voucher = VoucherCode.objects.create(
        code=_generate_referral_voucher_code(),
        name=f"Referral Reward - {reward.customer.email}",
        description=reward.description,
        discount_type="fixed",
        discount_value=reward.amount.amount,
        min_order_value=Money(0, currency),
        max_uses_total=1,
        max_uses_per_customer=1,
        issued_to=reward.customer,
        end_date=reward.expires_at,
        is_active=True,
    )

    reward.voucher_code_id = voucher.id
    reward.save(update_fields=["voucher_code_id"])

    return True


def create_percentage_coupon(reward):
    """
    Create a percentage-discount coupon for a referral reward.

    Args:
        reward (ReferralReward): Reward instance

    Returns:
        bool: True if successful

    Raises:
        ValueError: If the reward carries no percentage. This used to silently
            fall back to 10%, inventing a discount the merchant never configured.
    """
    from djmoney.money import Money

    from vouchers.models import VoucherCode

    if reward.percentage is None:
        raise ValueError(
            f"Referral reward {reward.id} has kind='percent' but no percentage set. "
            f"Fix the program's reward_config rather than assuming a rate."
        )

    currency = reward.amount.currency if reward.amount else get_default_currency()

    voucher = VoucherCode.objects.create(
        code=_generate_referral_voucher_code(),
        name=f"Referral Reward - {reward.customer.email}",
        description=reward.description,
        discount_type="percentage",
        discount_value=reward.percentage,
        min_order_value=Money(0, currency),
        # Caps the percentage at the reward's cash value where one is set.
        max_discount_amount=reward.amount if reward.amount else None,
        max_uses_total=1,
        max_uses_per_customer=1,
        issued_to=reward.customer,
        end_date=reward.expires_at,
        is_active=True,
    )

    reward.voucher_code_id = voucher.id
    reward.save(update_fields=["voucher_code_id"])

    return True


def reverse_wallet_credit(reward):
    """
    Reverse wallet credit transaction.

    Args:
        reward (ReferralReward): Reward with wallet transaction

    Returns:
        bool: True if successful
    """
    from wallet.models import WalletTransaction
    from wallet.services import WalletService

    if reward.wallet_transaction_id:
        try:
            original = WalletTransaction.objects.get(id=reward.wallet_transaction_id)
            WalletService.reverse_transaction(original, reason="Referral reward revoked")
            return True
        except WalletTransaction.DoesNotExist:
            pass

    return False


def disable_coupon_code(reward):
    """
    Disable coupon code.

    Args:
        reward (ReferralReward): Reward with coupon

    Returns:
        bool: True if successful
    """
    from vouchers.models import VoucherCode

    if reward.voucher_code_id:
        try:
            voucher = VoucherCode.objects.get(id=reward.voucher_code_id)
            voucher.is_active = False
            voucher.save(update_fields=["is_active"])
            return True
        except VoucherCode.DoesNotExist:
            pass

    return False


def send_reward_issued_email(reward):
    """
    Send email notification when reward is issued.

    Note: This is intentionally a no-op. The handle_reward_issuance signal
    in referrals/signals.py already sends the email via
    email_notifications.send_referral_reward_email() when the reward
    status changes to 'issued'. Sending here would cause a duplicate.
    """
    return None


def send_reward_expiring_email(reward, days_until_expiry=7):
    """
    Send email reminder that reward is expiring soon.

    Args:
        reward (ReferralReward): Reward instance
        days_until_expiry (int): Days until expiry

    Returns:
        bool: True if sent successfully
    """
    from .email_notifications import send_reward_expiring_email as _send

    return _send(reward, days_until_expiry)


def send_reward_expired_email(reward):
    """
    Send email notification that reward has expired.

    Args:
        reward (ReferralReward): Expired reward

    Returns:
        bool: True if sent successfully
    """
    from .email_notifications import send_reward_expired_email as _send

    return _send(reward)


def send_reward_revoked_email(reward, reason):
    """
    Send email notification that reward has been revoked.

    Args:
        reward (ReferralReward): Revoked reward
        reason (str): Reason for revocation

    Returns:
        bool: True if sent successfully
    """
    from .email_notifications import send_reward_revoked_email as _send

    return _send(reward, reason)
