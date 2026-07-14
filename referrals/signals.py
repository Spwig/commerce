"""
Referral Program Signal Handlers.

Automatically handles:
- Referral attribution when users sign up
- Order attribution and reward creation
- Email notifications for referral events
- Referrer identity stats updates
"""

import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from orders.models import Order

from .middleware import get_current_request
from .models import ReferralAttribution, ReferralIdentity, ReferralProgram, ReferralReward
from .services.email_notifications import (
    send_referral_reward_email,
)
from .services.rewards import create_and_issue_rewards
from .services.tracking import get_ref_token_from_cookie, track_order, track_signup
from .services.validation import validate_attribution

User = get_user_model()
logger = logging.getLogger(__name__)


# =====================================================================
# USER SIGNUP TRACKING
# =====================================================================


@receiver(post_save, sender=User)
def track_user_signup(sender, instance, created, **kwargs):
    """
    Track referral signup when new user is created.

    Checks for referral cookie and logs signup event.
    Does NOT create attribution yet - attribution created on first order.

    GUEST CHECKOUT SUPPORT:
    This signal automatically handles guest checkout. When a guest checks out,
    a User account is created (required for Order model), and this signal
    tracks the signup if a referral cookie is present. No special handling needed.
    """
    if not created:
        return

    # Skip if user is staff/superuser
    if instance.is_staff or instance.is_superuser:
        return

    # Check if program is active
    try:
        program = ReferralProgram.get_program()
        if not program or not program.is_active():
            return
    except Exception:
        return

    # Get request from thread-local storage
    request = get_current_request()

    if request:
        try:
            success, identity, message = track_signup(instance, request)
            if success:
                logger.info(
                    f"Tracked signup for {instance.email} via referrer {identity.customer.email}"
                )
        except Exception as e:
            logger.error(f"Error tracking signup for {instance.email}: {e}", exc_info=True)


# =====================================================================
# ORDER TRACKING & ATTRIBUTION
# =====================================================================


@receiver(post_save, sender=Order)
def handle_order_completion(sender, instance, created, **kwargs):
    """
    Handle order completion and referral attribution.

    When order status changes to 'delivered':
    1. Check for referral cookie
    2. Create ReferralAttribution if this is first order
    3. Run validation checks
    4. Auto-approve if passes validation
    5. Create and issue rewards
    """
    # Only process on status change to delivered
    if not hasattr(instance, "_previous_status"):
        # This is handled by pre_save signal below
        return

    # Check if status just changed to delivered
    if instance._previous_status != "delivered" and instance.status == "delivered":
        try:
            _process_order_attribution(instance)
        except Exception as e:
            logger.error(
                f"Error processing order attribution for {instance.order_number}: {e}",
                exc_info=True,
            )


@receiver(pre_save, sender=Order)
def track_order_status_change(sender, instance, **kwargs):
    """
    Track order status changes before save.

    Stores previous status on instance for comparison in post_save.
    """
    if instance.pk:
        try:
            previous = Order.objects.get(pk=instance.pk)
            instance._previous_status = previous.status
        except Order.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None


def _process_order_attribution(order):
    """
    Process referral attribution for completed order.

    Args:
        order (Order): Completed order instance
    """
    # Get program
    program = ReferralProgram.get_program()
    if not program or not program.is_active():
        logger.info(
            f"Referral program not active, skipping attribution for order {order.order_number}"
        )
        return

    # Check if this is user's first order
    first_order = Order.objects.filter(user=order.user).order_by("created_at").first()
    if first_order.pk != order.pk:
        logger.info(
            f"Order {order.order_number} is not first order for {order.user.email}, skipping"
        )
        return

    # Check if attribution already exists
    if hasattr(order, "referral_attribution") and order.referral_attribution:
        logger.info(f"Attribution already exists for order {order.order_number}")
        return

    # Get request from thread-local storage
    request = get_current_request()

    if not request:
        logger.debug(
            f"No request context for order {order.order_number}, cannot check referral cookie"
        )
        return

    # Get referral token from cookie
    token = get_ref_token_from_cookie(request)
    if not token:
        logger.debug(f"No referral cookie found for order {order.order_number}")
        return

    # Get referrer identity
    try:
        referrer_identity = ReferralIdentity.objects.select_related("customer").get(token=token)
    except ReferralIdentity.DoesNotExist:
        logger.warning(f"Invalid referral token {token} for order {order.order_number}")
        return

    # Check for self-referral
    if referrer_identity.customer == order.user:
        logger.warning(f"Self-referral detected for order {order.order_number}")
        return

    # Track order event
    try:
        success, identity, message = track_order(order, request)
        if success:
            logger.info(
                f"Tracked order {order.order_number} for referrer {identity.customer.email}"
            )
    except Exception as e:
        logger.error(f"Error tracking order: {e}", exc_info=True)

    # Create attribution
    try:
        attribution = ReferralAttribution.objects.create(
            program=program,
            referrer_identity=referrer_identity,
            referee_customer=order.user,
            first_order=order,
            status="pending",
        )
        logger.info(f"Created attribution for order {order.order_number}")

        # Run validation checks
        is_valid, validation_data, risk_score = validate_attribution(attribution)

        attribution.validation_data = validation_data
        attribution.risk_score = risk_score

        # Auto-approve if low risk and passes validation
        auto_approve_threshold = program.fraud_policy.get("auto_approve_threshold", 30)

        if is_valid and risk_score < auto_approve_threshold:
            attribution.status = "approved"
            attribution.approved_at = timezone.now()
            attribution.save()

            logger.info(f"Auto-approved attribution {attribution.id} with risk score {risk_score}")

            # Create and issue rewards
            create_and_issue_rewards(attribution)
        else:
            attribution.save()
            logger.info(f"Attribution {attribution.id} pending manual review (risk: {risk_score})")

    except Exception as e:
        logger.error(f"Error creating attribution: {e}", exc_info=True)


# =====================================================================
# ATTRIBUTION APPROVAL HANDLING
# =====================================================================


@receiver(post_save, sender=ReferralAttribution)
def handle_attribution_approval(sender, instance, created, **kwargs):
    """
    Handle manual attribution approval.

    When admin manually approves an attribution, create and issue rewards.
    Only processes manual approvals (those with reviewed_by set).
    """
    if created:
        return

    # Check if just approved
    if not hasattr(instance, "_previous_status"):
        return

    if instance._previous_status != "approved" and instance.status == "approved":
        # Only process manual approvals (reviewed_by will be set)
        # Auto-approvals are handled in _process_order_attribution
        if instance.reviewed_by:
            logger.info(
                f"Attribution {instance.id} manually approved by {instance.reviewed_by.email}"
            )
            create_and_issue_rewards(instance)
        else:
            logger.debug(f"Attribution {instance.id} auto-approved, rewards already created")


@receiver(pre_save, sender=ReferralAttribution)
def track_attribution_status_change(sender, instance, **kwargs):
    """
    Track attribution status changes before save.
    """
    if instance.pk:
        try:
            previous = ReferralAttribution.objects.get(pk=instance.pk)
            instance._previous_status = previous.status
        except ReferralAttribution.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None


# =====================================================================
# REWARD ISSUANCE NOTIFICATIONS
# =====================================================================


@receiver(post_save, sender=ReferralReward)
def handle_reward_issuance(sender, instance, created, **kwargs):
    """
    Handle reward issuance notifications.

    When reward is issued, send email notification to recipient.
    """
    if created:
        return

    # Check if just issued
    if not hasattr(instance, "_previous_status"):
        return

    if instance._previous_status != "issued" and instance.status == "issued":
        try:
            # Send reward notification email
            success = send_referral_reward_email(instance, instance.recipient_type)
            if success:
                logger.info(f"Sent reward notification email to {instance.customer.email}")
            else:
                logger.warning(
                    f"Failed to send reward notification email to {instance.customer.email}"
                )
        except Exception as e:
            logger.error(f"Error sending reward notification: {e}", exc_info=True)


@receiver(pre_save, sender=ReferralReward)
def track_reward_status_change(sender, instance, **kwargs):
    """
    Track reward status changes before save.
    """
    if instance.pk:
        try:
            previous = ReferralReward.objects.get(pk=instance.pk)
            instance._previous_status = previous.status
        except ReferralReward.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None


# =====================================================================
# ORDER CANCELLATION / REFUND HANDLING
# =====================================================================


@receiver(post_save, sender=Order)
def handle_order_cancellation(sender, instance, **kwargs):
    """
    Handle order cancellation or refund.

    If an order with attribution is cancelled/refunded, mark attribution as rejected
    and revoke any issued rewards.
    """
    if not hasattr(instance, "_previous_status"):
        return

    # Check if order was cancelled or refunded
    if instance.status in ["cancelled", "refunded"] and instance._previous_status not in [
        "cancelled",
        "refunded",
    ]:
        try:
            # Check if this order has an attribution
            if hasattr(instance, "referral_attribution") and instance.referral_attribution:
                attribution = instance.referral_attribution

                # Don't process if already rejected
                if attribution.status == "rejected":
                    return

                logger.info(
                    f"Order {instance.order_number} cancelled/refunded, rejecting attribution {attribution.id}"
                )

                # Reject attribution
                reason = "order_cancelled" if instance.status == "cancelled" else "order_refunded"
                attribution.reject(
                    reason=reason, notes=f"Order {instance.order_number} was {instance.status}"
                )

                # Revoke any issued rewards
                from .services.rewards import revoke_reward

                rewards = ReferralReward.objects.filter(attribution=attribution, status="issued")
                for reward in rewards:
                    success = revoke_reward(reward, reason=f"Order {instance.status}")
                    if success:
                        logger.info(f"Revoked reward {reward.id} due to order {instance.status}")
                    else:
                        logger.error(f"Failed to revoke reward {reward.id}")

        except Exception as e:
            logger.error(f"Error handling order cancellation: {e}", exc_info=True)
