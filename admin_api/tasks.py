"""
Celery Tasks for Admin API

Async tasks for push notifications and other background operations.
"""

import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_new_order_push_notification(self, order_id: int):
    """
    Send push notification for a new order.

    Args:
        order_id: ID of the order
    """
    try:
        from admin_api.services.push_service import PushNotificationService
        from orders.models import Order

        order = Order.objects.get(id=order_id)
        sent_count = PushNotificationService.send_new_order_notification(order)
        logger.info(f"Sent {sent_count} new order notifications for order {order.order_number}")

    except Order.DoesNotExist:
        logger.error(f"Order {order_id} not found for push notification")
    except Exception as e:
        logger.error(f"Failed to send new order notification: {e}")
        self.retry(exc=e)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_low_stock_push_notification(self, product_id: int, current_stock: int):
    """
    Send push notification for low stock alert.

    Args:
        product_id: ID of the product
        current_stock: Current stock quantity
    """
    try:
        from admin_api.services.push_service import PushNotificationService
        from catalog.models import Product

        product = Product.objects.get(id=product_id)
        sent_count = PushNotificationService.send_low_stock_notification(product, current_stock)
        logger.info(f"Sent {sent_count} low stock notifications for product {product.sku}")

    except Product.DoesNotExist:
        logger.error(f"Product {product_id} not found for push notification")
    except Exception as e:
        logger.error(f"Failed to send low stock notification: {e}")
        self.retry(exc=e)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_customer_message_push_notification(self, message_id: int, source: str = "contact_form"):
    """
    Send push notification for a new customer message.

    Args:
        message_id: ID of the message (CustomerMessage or OrderNote)
        source: Message source - 'contact_form' or 'order_note'
    """
    try:
        from admin_api.services.push_service import PushNotificationService

        if source == "contact_form":
            from admin_api.models import CustomerMessage

            message = CustomerMessage.objects.select_related("order").get(id=message_id)
        elif source == "order_note":
            from orders.models import OrderNote

            message = OrderNote.objects.select_related("order").get(id=message_id)
        else:
            logger.error(f"Invalid source: {source}")
            return

        sent_count = PushNotificationService.send_customer_message_notification(
            message, source=source
        )
        logger.info(f"Sent {sent_count} customer message notifications for {source} {message_id}")

    except Exception as e:
        logger.error(f"Failed to send customer message notification: {e}")
        self.retry(exc=e)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_payment_alert_push_notification(self, order_id: int, alert_type: str, details: str = ""):
    """
    Send push notification for payment alert.

    Args:
        order_id: ID of the order
        alert_type: Type of alert (e.g., 'failed', 'fraud_risk')
        details: Additional details
    """
    try:
        from admin_api.services.push_service import PushNotificationService
        from orders.models import Order

        order = Order.objects.get(id=order_id)
        sent_count = PushNotificationService.send_payment_alert_notification(
            order, alert_type, details
        )
        logger.info(f"Sent {sent_count} payment alert notifications for order {order.order_number}")

    except Order.DoesNotExist:
        logger.error(f"Order {order_id} not found for push notification")
    except Exception as e:
        logger.error(f"Failed to send payment alert notification: {e}")
        self.retry(exc=e)


@shared_task
def cleanup_expired_tokens():
    """
    Cleanup expired mobile auth tokens.

    Should be run periodically (e.g., daily via celery beat).
    """
    from admin_api.models import MobileAuthToken

    deleted_count = MobileAuthToken.cleanup_expired_tokens()
    logger.info(f"Cleaned up {deleted_count[0]} expired mobile auth tokens")


@shared_task
def cleanup_old_audit_logs(days: int = 90):
    """
    Cleanup old audit logs.

    Args:
        days: Delete logs older than this many days

    Should be run periodically (e.g., monthly via celery beat).
    """
    from admin_api.models import AdminAPIAuditLog

    deleted_count = AdminAPIAuditLog.cleanup_old_logs(days=days)
    logger.info(f"Cleaned up {deleted_count[0]} old audit logs")
