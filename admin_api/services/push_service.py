"""
Push Notification Service for Admin API

Handles sending push notifications to registered merchant devices
via the Spwig push notification service (push.spwig.com).
"""

import logging
from typing import Any

from django.conf import settings

from .push_client import PushAuthError, PushClient, PushClientError, PushRateLimitError

logger = logging.getLogger(__name__)


class PushNotificationService:
    """
    Service for sending push notifications to merchant devices.

    Uses the centralized push.spwig.com service for delivery.
    All APNs communication is handled by the push service.

    Notification Types:
    - new_order: New order placed
    - low_stock: Product stock is low
    - customer_message: New customer message received
    - payment_alert: Payment issue or fraud alert

    Usage:
        PushNotificationService.send_new_order_notification(order)
        PushNotificationService.send_low_stock_notification(product)
        PushNotificationService.send_customer_message_notification(message)
    """

    # Use sandbox for DEBUG mode (development app builds)
    USE_SANDBOX = getattr(settings, "DEBUG", False)

    @classmethod
    def is_configured(cls) -> bool:
        """Check if push notifications are properly configured."""
        try:
            client = PushClient()
            return client.is_configured()
        except Exception:
            return False

    @classmethod
    def _get_client(cls) -> PushClient:
        """Get a configured push client instance."""
        return PushClient()

    @classmethod
    def _send_notification_batch(
        cls,
        tokens: list[str],
        title: str,
        body: str,
        data: dict[str, Any] | None = None,
        sound: str = "default",
        badge: int | None = None,
    ) -> dict[str, Any]:
        """
        Send notification to a batch of device tokens.

        Args:
            tokens: List of device push tokens
            title: Notification title
            body: Notification body
            data: Custom data payload
            sound: Sound name
            badge: Badge number

        Returns:
            Dict with 'sent', 'failed', 'results' keys
        """
        if not tokens:
            return {"sent": 0, "failed": 0, "results": [], "invalid_tokens": []}

        try:
            client = cls._get_client()
            result = client.send_notification(
                tokens=tokens,
                title=title,
                body=body,
                data=data,
                sound=sound,
                badge=badge,
                sandbox=cls.USE_SANDBOX,
            )

            # Collect invalid tokens that should be removed
            invalid_tokens = [
                r["token"] for r in result.results if r.get("should_remove_token", False)
            ]

            return {
                "sent": result.sent,
                "failed": result.failed,
                "results": result.results,
                "invalid_tokens": invalid_tokens,
            }

        except PushAuthError as e:
            logger.error(f"Push authentication failed: {e}")
            return {
                "sent": 0,
                "failed": len(tokens),
                "results": [],
                "invalid_tokens": [],
                "error": str(e),
            }

        except PushRateLimitError as e:
            logger.warning(f"Push rate limit exceeded: {e}")
            return {
                "sent": 0,
                "failed": len(tokens),
                "results": [],
                "invalid_tokens": [],
                "error": str(e),
            }

        except PushClientError as e:
            logger.error(f"Push client error: {e}")
            return {
                "sent": 0,
                "failed": len(tokens),
                "results": [],
                "invalid_tokens": [],
                "error": str(e),
            }

        except Exception as e:
            logger.exception(f"Unexpected error sending notifications: {e}")
            return {
                "sent": 0,
                "failed": len(tokens),
                "results": [],
                "invalid_tokens": [],
                "error": str(e),
            }

    @classmethod
    def _remove_invalid_tokens(cls, tokens: list[str]):
        """
        Remove invalid device tokens from the database.

        Called when the push service indicates tokens are no longer valid.
        """
        if not tokens:
            return

        from admin_api.models import DeviceRegistration

        count = DeviceRegistration.objects.filter(push_token__in=tokens).delete()[0]
        if count:
            logger.info(f"Removed {count} invalid device registration(s)")

    @classmethod
    def send_notification(
        cls,
        notification_type: str,
        title: str,
        body: str,
        data: dict[str, Any] | None = None,
        exclude_user=None,
    ) -> int:
        """
        Send a notification to all relevant devices.

        Args:
            notification_type: One of 'new_order', 'low_stock', 'customer_message'
            title: Notification title
            body: Notification body
            data: Custom data payload
            exclude_user: User to exclude from notifications

        Returns:
            int: Number of notifications sent successfully
        """
        from admin_api.models import DeviceRegistration

        devices = DeviceRegistration.get_devices_for_notification(
            notification_type, exclude_user=exclude_user
        )

        if not devices.exists():
            logger.debug(f"No devices registered for {notification_type} notifications")
            return 0

        # Collect tokens by platform
        ios_tokens = []
        device_map = {}  # token -> device for updating status

        for device in devices:
            if device.platform == "ios":
                ios_tokens.append(device.push_token)
                device_map[device.push_token] = device
            elif device.platform == "android":
                # Android/FCM not yet supported by push service
                logger.debug("Android notifications not yet supported")
                continue

        if not ios_tokens:
            return 0

        # Send batch notification
        result = cls._send_notification_batch(
            tokens=ios_tokens,
            title=title,
            body=body,
            data=data,
        )

        # Update device statuses based on results
        for token_result in result.get("results", []):
            token = token_result.get("token")
            device = device_map.get(token)
            if device:
                if token_result.get("status") == "sent":
                    device.mark_notification_sent()
                else:
                    device.mark_notification_failed()

        # Remove invalid tokens
        cls._remove_invalid_tokens(result.get("invalid_tokens", []))

        sent_count = result.get("sent", 0)
        logger.info(f"Sent {sent_count}/{len(ios_tokens)} notifications for {notification_type}")

        return sent_count

    @classmethod
    def send_new_order_notification(cls, order) -> int:
        """
        Send notification for a new order.

        Args:
            order: Order instance

        Returns:
            Number of notifications sent
        """
        from django.utils.formats import localize

        title = "New Order Received"
        body = f"Order #{order.order_number} - {localize(order.total_amount.amount)} {order.total_amount.currency}"

        data = {
            "type": "new_order",
            "order_number": order.order_number,
            "order_id": order.id,
        }

        return cls.send_notification(
            notification_type="new_order",
            title=title,
            body=body,
            data=data,
        )

    @classmethod
    def send_low_stock_notification(cls, product, current_stock: int) -> int:
        """
        Send notification for low stock alert.

        Args:
            product: Product instance
            current_stock: Current stock quantity

        Returns:
            Number of notifications sent
        """
        title = "Low Stock Alert"
        body = f"{product.name} has only {current_stock} units left"

        data = {
            "type": "low_stock",
            "product_id": product.id,
            "product_name": product.name,
            "sku": product.sku,
            "current_stock": current_stock,
        }

        return cls.send_notification(
            notification_type="low_stock",
            title=title,
            body=body,
            data=data,
        )

    @classmethod
    def send_customer_message_notification(cls, message, source: str = "contact_form") -> int:
        """
        Send notification for new customer message.

        Args:
            message: CustomerMessage or OrderNote instance
            source: Message source - 'contact_form' or 'order_note'

        Returns:
            Number of notifications sent

        Deep linking:
            - source='contact_form': Use message_id to navigate to /messages/contact_form/{id}/
            - source='order_note': Use order_number to navigate to /orders/{order_number}/
        """
        if source == "contact_form":
            # CustomerMessage instance
            title = "New Customer Message"
            body = f"From {message.name}: {message.subject}"

            data = {
                "type": "customer_message",
                "source": "contact_form",
                "message_id": message.id,
                "sender_name": message.name,
                "sender_email": message.email,
                "order_id": message.order_id,
                "order_number": message.order.order_number if message.order else None,
            }
        elif source == "order_note":
            # OrderNote instance
            order = message.order
            customer_name = order.billing_name or order.shipping_name or "Customer"
            title = "New Customer Message"
            body = f"From {customer_name}: Re: Order #{order.order_number}"

            data = {
                "type": "customer_message",
                "source": "order_note",
                "message_id": message.id,
                "sender_name": customer_name,
                "sender_email": order.email,
                "order_id": order.id,
                "order_number": order.order_number,
            }
        else:
            raise ValueError(f"Invalid source: {source}")

        return cls.send_notification(
            notification_type="customer_message",
            title=title,
            body=body,
            data=data,
        )

    @classmethod
    def send_payment_alert_notification(cls, order, alert_type: str, details: str = "") -> int:
        """
        Send notification for payment alert.

        Args:
            order: Order instance
            alert_type: Type of alert (e.g., 'failed', 'fraud_risk')
            details: Additional details

        Returns:
            Number of notifications sent
        """
        from admin_api.models import DeviceRegistration

        title = "Payment Alert"

        if alert_type == "failed":
            body = f"Payment failed for order #{order.order_number}"
        elif alert_type == "fraud_risk":
            body = f"High risk payment detected for order #{order.order_number}"
        else:
            body = f"Payment issue with order #{order.order_number}"

        if details:
            body = f"{body}: {details}"

        data = {
            "type": "payment_alert",
            "alert_type": alert_type,
            "order_number": order.order_number,
            "order_id": order.id,
        }

        # Payment alerts go to all active devices regardless of preferences
        devices = DeviceRegistration.objects.filter(is_active=True)

        ios_tokens = []
        device_map = {}

        for device in devices:
            if device.platform == "ios":
                ios_tokens.append(device.push_token)
                device_map[device.push_token] = device

        if not ios_tokens:
            return 0

        result = cls._send_notification_batch(
            tokens=ios_tokens,
            title=title,
            body=body,
            data=data,
        )

        # Update device statuses
        for token_result in result.get("results", []):
            token = token_result.get("token")
            device = device_map.get(token)
            if device:
                if token_result.get("status") == "sent":
                    device.mark_notification_sent()
                else:
                    device.mark_notification_failed()

        # Remove invalid tokens
        cls._remove_invalid_tokens(result.get("invalid_tokens", []))

        return result.get("sent", 0)
