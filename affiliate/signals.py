"""
Affiliate App Signals
Handles automatic commission attribution when orders are completed.
"""

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .services.email_notifications import (
    send_commission_earned_email,
    send_commission_reversed_email,
)

logger = logging.getLogger(__name__)


@receiver(post_save, sender="orders.Order")
def process_order_for_affiliate_commission(sender, instance, created, **kwargs):
    """
    Signal handler that processes orders for affiliate commission attribution.

    Triggered when an Order is saved. Checks if the order status is 'completed'
    and processes it through the attribution engine to create commissions.

    Args:
        sender: The Order model class
        instance: The Order instance that was saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional signal arguments
    """
    from .attribution import AttributionEngine
    from .models import Commission

    # Only process orders that are marked as completed
    # Adjust status value based on your Order model's status choices
    if not hasattr(instance, "status"):
        logger.warning(f"Order {instance.id} has no status attribute")
        return

    # Check if order is completed (adjust status value as needed for your Order model)
    # Common status values: 'completed', 'complete', 'delivered', 'fulfilled'
    completed_statuses = ["completed", "complete", "delivered", "fulfilled"]

    if instance.status not in completed_statuses:
        # Order is not completed yet, don't create commission
        return

    # Check if we've already processed this order for commissions
    existing_commission = Commission.objects.filter(order=instance).exists()
    if existing_commission:
        logger.debug(f"Order {instance.id} already has commission attribution")
        return

    # Get user from order (adjust based on your Order model structure)
    user = getattr(instance, "user", None) or getattr(instance, "customer", None)

    if not user:
        logger.debug(f"Order {instance.id} has no associated user, skipping affiliate attribution")
        return

    try:
        # Process order through attribution engine
        logger.info(f"Processing order {instance.id} for affiliate commission attribution")

        engine = AttributionEngine(order=instance, user=user)
        commission = engine.process_order()

        if commission:
            logger.info(
                f"Created commission {commission.id} for order {instance.id}: "
                f"${commission.amount} for affiliate {commission.affiliate.affiliate_code}"
            )
            # Send commission earned email
            send_commission_earned_email(commission)
        else:
            logger.debug(f"No affiliate attribution found for order {instance.id}")

    except Exception as e:
        logger.error(
            f"Error processing affiliate commission for order {instance.id}: {str(e)}",
            exc_info=True,
        )


@receiver(post_save, sender="orders.Order")
def mark_commission_paid_on_order_refund(sender, instance, created, **kwargs):
    """
    Signal handler that marks commissions as reversed when orders are refunded.

    Args:
        sender: The Order model class
        instance: The Order instance that was saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional signal arguments
    """
    from .models import Commission

    if created:
        return

    # Check if order was refunded/cancelled (adjust status values as needed)
    refunded_statuses = ["refunded", "cancelled", "canceled", "returned"]

    if instance.status not in refunded_statuses:
        return

    # Find and reverse any approved/pending commissions for this order
    commissions = Commission.objects.filter(order=instance, status__in=["pending", "approved"])

    for commission in commissions:
        commission.status = "reversed"
        commission.save(update_fields=["status", "updated_at"])

        logger.info(
            f"Reversed commission {commission.id} (${commission.amount}) "
            f"for refunded order {instance.id}"
        )
        # Send commission reversed email
        send_commission_reversed_email(commission)
