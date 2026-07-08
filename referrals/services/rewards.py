"""
Rewards service for referral program.

Handles reward creation, issuance, redemption, revocation, and expiry.
"""
import logging
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from decimal import Decimal

from core.utils import get_default_currency

logger = logging.getLogger(__name__)


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
    expiry_days = reward_config.get('expiry_days', 90)
    expires_at = timezone.now() + timedelta(days=expiry_days) if expiry_days else None

    referrer_reward = None
    referee_reward = None

    # Create referrer reward
    if 'referrer' in reward_config:
        referrer_config = reward_config['referrer']

        referrer_reward = ReferralReward.objects.create(
            program=program,
            attribution=attribution,
            referrer_identity=attribution.referrer_identity,
            customer=attribution.referrer_identity.customer,
            recipient_type='referrer',
            kind=referrer_config.get('kind', 'credit'),
            amount=referrer_config.get('amount', 10),
            amount_currency=referrer_config.get('currency', get_default_currency()),
            percentage=referrer_config.get('percentage'),
            description=referrer_config.get('description', 'Referral reward'),
            status='pending',
            expires_at=expires_at,
        )

    # Create referee reward (if double-sided)
    if reward_config.get('double_sided', False) and 'referee' in reward_config:
        referee_config = reward_config['referee']

        referee_reward = ReferralReward.objects.create(
            program=program,
            attribution=attribution,
            referrer_identity=attribution.referrer_identity,  # Link to referrer for tracking
            customer=attribution.referee_customer,
            recipient_type='referee',
            kind=referee_config.get('kind', 'discount'),
            amount=referee_config.get('amount', 10),
            amount_currency=referee_config.get('currency', get_default_currency()),
            percentage=referee_config.get('percentage'),
            description=referee_config.get('description', 'Welcome reward'),
            status='pending',
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
    if reward.status != 'pending':
        return False

    # Issue based on reward kind
    if reward.kind == 'credit':
        success = create_wallet_credit(reward)
    elif reward.kind == 'coupon':
        success = create_coupon_code(reward)
    elif reward.kind == 'percent':
        success = create_percentage_coupon(reward)
    elif reward.kind == 'perk':
        # Perks are issued differently (manual or automated based on type)
        success = True
    else:
        success = False

    if success:
        # Mark reward as issued
        reward.issue()

        # Update referrer identity stats
        if reward.recipient_type == 'referrer' and reward.referrer_identity:
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
                logger.info(f"Issued referrer reward {referrer_reward.id} to {referrer_reward.customer.email}")
            else:
                logger.error(f"Failed to issue referrer reward {referrer_reward.id}")

        if referee_reward:
            success = issue_reward(referee_reward)
            if success:
                logger.info(f"Issued referee reward {referee_reward.id} to {referee_reward.customer.email}")
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
        logger.error(f"Error creating/issuing rewards for attribution {attribution.id}: {e}", exc_info=True)


def redeem_reward(reward):
    """
    Mark reward as redeemed.

    Args:
        reward (ReferralReward): Reward to redeem

    Returns:
        bool: True if successful
    """
    if reward.status != 'issued':
        return False

    reward.redeem()
    return True


@transaction.atomic
def revoke_reward(reward, reason=''):
    """
    Revoke a reward (reverse wallet credit or disable coupon).

    Args:
        reward (ReferralReward): Reward to revoke
        reason (str): Reason for revocation

    Returns:
        bool: True if successful
    """
    if reward.status not in ['pending', 'issued']:
        return False

    # Reverse integration based on reward kind
    if reward.kind == 'credit' and reward.wallet_transaction_id:
        reverse_wallet_credit(reward)
    elif reward.kind in ['coupon', 'percent'] and reward.voucher_code_id:
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
    expired_rewards = ReferralReward.objects.filter(
        status='issued',
        expires_at__lte=timezone.now()
    )

    count = 0
    for reward in expired_rewards:
        # Reverse any wallet credits or coupons
        if reward.kind == 'credit' and reward.wallet_transaction_id:
            reverse_wallet_credit(reward)
        elif reward.kind in ['coupon', 'percent'] and reward.voucher_code_id:
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
        source='referral',
        description=f'Referral reward: {reward.description}',
        reference_id=str(reward.id),
    )

    reward.wallet_transaction_id = txn.id
    reward.save(update_fields=['wallet_transaction_id'])
    return True


def create_coupon_code(reward):
    """
    Create coupon code for customer.

    Args:
        reward (ReferralReward): Reward instance

    Returns:
        bool: True if successful
    """
    from vouchers.models import VoucherCode
    import random
    import string

    # Generate unique coupon code
    code = f"REF{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"

    # Create voucher
    voucher = VoucherCode.objects.create(
        code=code,
        name=f"Referral Reward - {reward.customer.email}",
        description=reward.description,
        discount_type='fixed',
        discount_value=reward.amount.amount,
        minimum_spend=0,
        is_active=True,
        single_use=True,
        usage_limit=1,
    )

    # Store voucher ID reference
    reward.voucher_code_id = voucher.id
    reward.save(update_fields=['voucher_code_id'])

    return True


def create_percentage_coupon(reward):
    """
    Create percentage discount coupon for customer.

    Args:
        reward (ReferralReward): Reward instance

    Returns:
        bool: True if successful
    """
    from vouchers.models import VoucherCode
    import random
    import string

    # Generate unique coupon code
    code = f"REF{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"

    # Create voucher
    voucher = VoucherCode.objects.create(
        code=code,
        name=f"Referral Reward - {reward.customer.email}",
        description=reward.description,
        discount_type='percentage',
        discount_value=reward.percentage or 10,
        minimum_spend=0,
        maximum_discount=reward.amount.amount if reward.amount else None,
        is_active=True,
        single_use=True,
        usage_limit=1,
    )

    # Store voucher ID reference
    reward.voucher_code_id = voucher.id
    reward.save(update_fields=['voucher_code_id'])

    return True


def reverse_wallet_credit(reward):
    """
    Reverse wallet credit transaction.

    Args:
        reward (ReferralReward): Reward with wallet transaction

    Returns:
        bool: True if successful
    """
    from wallet.services import WalletService
    from wallet.models import WalletTransaction

    if reward.wallet_transaction_id:
        try:
            original = WalletTransaction.objects.get(id=reward.wallet_transaction_id)
            WalletService.reverse_transaction(
                original, reason='Referral reward revoked'
            )
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
            voucher.save(update_fields=['is_active'])
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
