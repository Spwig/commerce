"""
Django Signals for Admin API

Automatically triggers push notifications for important events.
"""

import logging

from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_save, sender="orders.Order")
def send_new_order_notification(sender, instance, created, **kwargs):
    """
    Send push notification when a new order is created.

    Only sends notification if:
    - Order is newly created
    - Payment status is 'paid' (completed checkout)
    """
    if created and instance.payment_status == "paid":

        def _queue_new_order_notification():
            try:
                from admin_api.tasks import send_new_order_push_notification

                send_new_order_push_notification.delay(instance.id)
                logger.info(f"Queued new order notification for order {instance.order_number}")
            except Exception as e:
                logger.error(f"Failed to queue new order notification: {e}")

        transaction.on_commit(_queue_new_order_notification)


@receiver(pre_save, sender="orders.Order")
def record_order_paid_transition(sender, instance, **kwargs):
    """
    Record when an existing order transitions from unpaid to paid.

    The transition is only flagged here; the notification is enqueued from
    post_save once the change is committed, so a failed save or rolled-back
    transaction never produces a spurious paid-order notification.
    """
    instance._became_paid = False
    if instance.pk:
        try:
            from orders.models import Order

            old_instance = Order.objects.filter(pk=instance.pk).first()
            if (
                old_instance
                and old_instance.payment_status != "paid"
                and instance.payment_status == "paid"
            ):
                instance._became_paid = True
        except Exception as e:
            logger.error(f"Failed to record order paid transition: {e}")


@receiver(post_save, sender="orders.Order")
def send_order_paid_notification(sender, instance, created, **kwargs):
    """
    Send push notification when an existing order becomes paid.

    Handles case where order was created pending and later marked as paid.
    """
    if created or not getattr(instance, "_became_paid", False):
        return

    def _queue_order_paid_notification():
        try:
            from admin_api.tasks import send_new_order_push_notification

            send_new_order_push_notification.delay(instance.id)
            logger.info(f"Queued order paid notification for order {instance.order_number}")
        except Exception as e:
            logger.error(f"Failed to queue order paid notification: {e}")

    transaction.on_commit(_queue_order_paid_notification)


@receiver(post_save, sender="catalog.StockItem")
def check_low_stock_notification(sender, instance, **kwargs):
    """
    Send push notification when stock drops below threshold.

    Only sends if:
    - Product tracks inventory
    - Stock is at or below low_stock_threshold
    - Stock just dropped to this level (not already low)
    """
    try:
        product = instance.product
        if not product.track_inventory:
            return

        # Calculate available stock
        from django.db.models import IntegerField, Sum
        from django.db.models.functions import Coalesce

        from catalog.models import StockItem

        available = StockItem.objects.filter(product=product).aggregate(
            available=Coalesce(Sum("on_hand"), 0, output_field=IntegerField())
            - Coalesce(Sum("allocated"), 0, output_field=IntegerField())
        )["available"]

        if available is None:
            return

        from django.core.cache import cache

        # Persistent state flag: True once we've alerted while low, cleared on
        # recovery. This detects the above-threshold-to-low transition and
        # avoids both re-alerting a product that stays low and suppressing a
        # product that recovers then drops low again.
        cache_key = f"low_stock_notified_{product.id}"

        if available <= product.low_stock_threshold:
            # Only notify on the transition into low stock.
            if not cache.get(cache_key):
                from admin_api.tasks import send_low_stock_push_notification

                send_low_stock_push_notification.delay(product.id, available)
                cache.set(cache_key, True, None)
                logger.info(f"Queued low stock notification for product {product.sku}")
        else:
            # Stock recovered above threshold: clear state so the next drop
            # into low stock triggers a fresh notification.
            cache.delete(cache_key)

    except Exception as e:
        logger.error(f"Failed to check/queue low stock notification: {e}")


@receiver(post_save, sender="admin_api.CustomerMessage")
def send_new_message_notification(sender, instance, created, **kwargs):
    """
    Send push notification when a new customer message is received (contact form).
    """
    if created:
        try:
            from admin_api.tasks import send_customer_message_push_notification

            send_customer_message_push_notification.delay(instance.id, source="contact_form")
            logger.info(f"Queued contact form notification for message {instance.id}")
        except Exception as e:
            logger.error(f"Failed to queue contact form notification: {e}")


@receiver(post_save, sender="orders.OrderNote")
def send_order_note_notification(sender, instance, created, **kwargs):
    """
    Send push notification when a customer adds a note to an order.

    Only triggers for customer notes (is_customer_note=True), not staff notes.
    """
    if created and instance.is_customer_note:
        try:
            from admin_api.tasks import send_customer_message_push_notification

            send_customer_message_push_notification.delay(instance.id, source="order_note")
            logger.info(
                f"Queued order note notification for note {instance.id} on order {instance.order.order_number}"
            )
        except Exception as e:
            logger.error(f"Failed to queue order note notification: {e}")


def trigger_payment_alert(order, alert_type: str, details: str = ""):
    """
    Manually trigger a payment alert notification.

    Call this from payment provider integration when issues are detected.

    Args:
        order: Order instance
        alert_type: 'failed', 'fraud_risk', etc.
        details: Additional context
    """
    try:
        from admin_api.tasks import send_payment_alert_push_notification

        send_payment_alert_push_notification.delay(order.id, alert_type, details)
        logger.info(f"Queued payment alert notification for order {order.order_number}")
    except Exception as e:
        logger.error(f"Failed to queue payment alert notification: {e}")
