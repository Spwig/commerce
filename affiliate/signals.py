"""
Affiliate App Signals
Handles automatic commission attribution when orders are completed.
"""

import logging

from .services.email_notifications import (
    send_commission_earned_email,
    send_commission_reversed_email,
)

logger = logging.getLogger(__name__)


# NOTE: order-completion handling is no longer registered as an independent
# receiver. It is invoked (unchanged) by the unified order-completion
# orchestrator in ``attribution.orchestrator`` so all payout + reporting runs
# from one deterministic entry point. The function body is preserved verbatim
# so commission amounts are byte-for-byte identical (invariant #5).
def process_order_for_affiliate_commission(sender, instance, created, **kwargs):
    """
    Process an order for affiliate commission attribution.

    Checks if the order status is 'completed' and processes it through the
    attribution engine to create commissions. Invoked by the attribution
    orchestrator on order save.

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

        engine = AttributionEngine(order=instance)
        commissions = engine.process_order()

        if commissions:
            for commission in commissions:
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


def mark_commission_paid_on_order_refund(sender, instance, created, **kwargs):
    """
    Mark commissions as reversed when orders are refunded. Invoked by the
    attribution orchestrator on order save.

    Args:
        sender: The Order model class
        instance: The Order instance that was saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional signal arguments
    """
    from .models import Commission

    if created:
        return

    # Check if order was refunded/cancelled.
    #
    # payment_status is included because that is the only field RefundService
    # writes; gating on status alone left commission payable on money the
    # merchant had already returned.
    # Reverse commission only on a FULL refund or cancellation, not a partial.
    #
    # A partial refund reverses the WHOLE commission here (the loop flips every
    # pending/approved row to "rejected"), so a $1 refund on a $500 order wiped
    # the affiliate's entire commission. Prorating would mean writing a
    # compensating partial-reversal row — deferred with the loyalty equivalent.
    # A later full refund still reverses everything.
    refunded_statuses = ["refunded", "cancelled", "canceled", "returned"]
    refunded_payment_statuses = ["refunded"]

    if (
        instance.status not in refunded_statuses
        and instance.payment_status not in refunded_payment_statuses
    ):
        return

    # Find and reverse any approved/pending commissions for this order
    commissions = Commission.objects.filter(order=instance, status__in=["pending", "approved"])

    for commission in commissions:
        commission.status = "rejected"
        commission.save(update_fields=["status"])

        logger.info(
            f"Reversed commission {commission.id} (${commission.amount}) "
            f"for refunded order {instance.id}"
        )
        # Send commission reversed email
        send_commission_reversed_email(commission)
