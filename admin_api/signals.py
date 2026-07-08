"""
Django Signals for Admin API

Automatically triggers push notifications for important events.
"""
import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_save, sender='orders.Order')
def send_new_order_notification(sender, instance, created, **kwargs):
    """
    Send push notification when a new order is created.

    Only sends notification if:
    - Order is newly created
    - Payment status is 'paid' (completed checkout)
    """
    if created and instance.payment_status == 'paid':
        try:
            from admin_api.tasks import send_new_order_push_notification
            send_new_order_push_notification.delay(instance.id)
            logger.info(f"Queued new order notification for order {instance.order_number}")
        except Exception as e:
            logger.error(f"Failed to queue new order notification: {e}")


@receiver(pre_save, sender='orders.Order')
def send_order_paid_notification(sender, instance, **kwargs):
    """
    Send push notification when an existing order becomes paid.

    Handles case where order was created pending and later marked as paid.
    """
    if instance.pk:
        try:
            from orders.models import Order
            old_instance = Order.objects.filter(pk=instance.pk).first()
            if old_instance and old_instance.payment_status != 'paid' and instance.payment_status == 'paid':
                from admin_api.tasks import send_new_order_push_notification
                send_new_order_push_notification.delay(instance.id)
                logger.info(f"Queued order paid notification for order {instance.order_number}")
        except Exception as e:
            logger.error(f"Failed to queue order paid notification: {e}")


@receiver(post_save, sender='catalog.StockItem')
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
        from django.db.models import Sum
        from django.db.models.functions import Coalesce
        from catalog.models import StockItem

        from django.db.models import IntegerField
        available = StockItem.objects.filter(
            product=product
        ).aggregate(
            available=Coalesce(Sum('on_hand'), 0, output_field=IntegerField()) - Coalesce(Sum('allocated'), 0, output_field=IntegerField())
        )['available']

        # Check if at or below threshold
        if available is not None and available <= product.low_stock_threshold:
            # Check if we've already sent a notification recently (prevent spam)
            from django.core.cache import cache
            cache_key = f"low_stock_notified_{product.id}"
            if not cache.get(cache_key):
                from admin_api.tasks import send_low_stock_push_notification
                send_low_stock_push_notification.delay(product.id, available)
                # Don't notify again for 1 hour
                cache.set(cache_key, True, 3600)
                logger.info(f"Queued low stock notification for product {product.sku}")

    except Exception as e:
        logger.error(f"Failed to check/queue low stock notification: {e}")


@receiver(post_save, sender='admin_api.CustomerMessage')
def send_new_message_notification(sender, instance, created, **kwargs):
    """
    Send push notification when a new customer message is received (contact form).
    """
    if created:
        try:
            from admin_api.tasks import send_customer_message_push_notification
            send_customer_message_push_notification.delay(instance.id, source='contact_form')
            logger.info(f"Queued contact form notification for message {instance.id}")
        except Exception as e:
            logger.error(f"Failed to queue contact form notification: {e}")


@receiver(post_save, sender='orders.OrderNote')
def send_order_note_notification(sender, instance, created, **kwargs):
    """
    Send push notification when a customer adds a note to an order.

    Only triggers for customer notes (is_customer_note=True), not staff notes.
    """
    if created and instance.is_customer_note:
        try:
            from admin_api.tasks import send_customer_message_push_notification
            send_customer_message_push_notification.delay(instance.id, source='order_note')
            logger.info(f"Queued order note notification for note {instance.id} on order {instance.order.order_number}")
        except Exception as e:
            logger.error(f"Failed to queue order note notification: {e}")


def trigger_payment_alert(order, alert_type: str, details: str = ''):
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
