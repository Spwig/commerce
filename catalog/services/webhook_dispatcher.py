"""
Webhook dispatcher for license events.

This service handles dispatching webhook events to subscribed endpoints.
"""

import hashlib
import hmac
import json
import logging
from datetime import datetime

import requests
from django.db import models as django_models
from django.utils import timezone

logger = logging.getLogger(__name__)


class LicenseWebhookEvents:
    """Constants for license webhook event types"""

    LICENSE_GENERATED = "license.generated"
    LICENSE_ACTIVATED = "license.activated"
    LICENSE_DEACTIVATED = "license.deactivated"
    LICENSE_SUSPENDED = "license.suspended"
    LICENSE_REVOKED = "license.revoked"
    LICENSE_EXPIRED = "license.expired"
    DEVICE_ACTIVATED = "device.activated"
    DEVICE_DEACTIVATED = "device.deactivated"

    ALL_EVENTS = [
        LICENSE_GENERATED,
        LICENSE_ACTIVATED,
        LICENSE_DEACTIVATED,
        LICENSE_SUSPENDED,
        LICENSE_REVOKED,
        LICENSE_EXPIRED,
        DEVICE_ACTIVATED,
        DEVICE_DEACTIVATED,
    ]


class LicenseWebhookDispatcher:
    """Dispatch webhook events to subscribed endpoints"""

    @staticmethod
    def dispatch(event_type, license_key, data=None, activation=None):
        """
        Send webhook to all subscribed endpoints for this event type.

        Args:
            event_type: Type of event (from LicenseWebhookEvents)
            license_key: LicenseKey model instance
            data: Optional additional event data
            activation: Optional LicenseActivation instance (for device events)

        Returns:
            int: Number of successful webhook deliveries
        """
        from catalog.models import WebhookSubscription

        if data is None:
            data = {}

        # Find subscriptions for this event type
        subscriptions = WebhookSubscription.objects.filter(
            is_active=True, events__contains=[event_type]
        )

        # Filter by product if subscription has product filters
        if license_key.digital_asset:
            product = license_key.digital_asset.product
            subscriptions = subscriptions.filter(
                django_models.Q(product_filter__isnull=True)
                | django_models.Q(product_filter=product)
            )

        # Filter by license type if subscription has license type filters
        subscriptions_with_filters = []
        for sub in subscriptions:
            if not sub.license_type_filter or license_key.key_type in sub.license_type_filter:
                subscriptions_with_filters.append(sub)

        # Prepare payload
        payload = {
            "event": event_type,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "license": {
                "key": license_key.key,
                "type": license_key.key_type,
                "status": license_key.status,
                "max_activations": license_key.max_activations,
                "current_activations": license_key.current_activations,
                "expires_at": license_key.expires_at.isoformat()
                if license_key.expires_at
                else None,
            },
            "data": data,
        }

        # Add device info for device events
        if activation:
            payload["device"] = {
                "fingerprint": activation.device_fingerprint,
                "name": activation.device_name,
                "info": activation.device_info,
            }

        # Add product info
        if license_key.digital_asset:
            payload["product"] = {
                "id": license_key.digital_asset.product.id,
                "name": license_key.digital_asset.product.name,
                "sku": license_key.digital_asset.product.sku,
            }

        # Add order info
        if license_key.order_item:
            payload["order"] = {
                "id": license_key.order_item.order.id,
                "number": license_key.order_item.order.order_number,
            }

        # Dispatch to all matching subscriptions
        successful_count = 0

        for subscription in subscriptions_with_filters:
            try:
                success = LicenseWebhookDispatcher._send_webhook(subscription, payload)

                if success:
                    successful_count += 1
                    subscription.successful_deliveries += 1
                else:
                    subscription.failed_deliveries += 1

                subscription.total_deliveries += 1
                subscription.last_delivery_at = timezone.now()
                subscription.save(
                    update_fields=[
                        "total_deliveries",
                        "successful_deliveries",
                        "failed_deliveries",
                        "last_delivery_at",
                    ]
                )

            except Exception as e:
                logger.exception(f"Exception dispatching webhook to {subscription.name}: {e}")
                subscription.failed_deliveries += 1
                subscription.total_deliveries += 1
                subscription.save(update_fields=["total_deliveries", "failed_deliveries"])

        return successful_count

    @staticmethod
    def _send_webhook(subscription, payload):
        """
        Send webhook to a single subscription endpoint.

        Args:
            subscription: WebhookSubscription instance
            payload: Event payload dictionary

        Returns:
            bool: Success status
        """
        # Prepare payload as JSON
        payload_json = json.dumps(payload, sort_keys=True)

        # Generate HMAC signature
        signature = hmac.new(
            subscription.secret.encode("utf-8"), payload_json.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        # Prepare headers
        headers = {
            "Content-Type": "application/json",
            "X-Spwig-Signature": f"sha256={signature}",
            "X-Spwig-Event": payload["event"],
            "X-Spwig-Delivery-ID": f"{subscription.id}-{int(datetime.utcnow().timestamp())}",
            "User-Agent": "Spwig-Webhooks/1.0",
        }

        try:
            response = requests.post(
                subscription.url, data=payload_json, headers=headers, timeout=30
            )

            # Consider 2xx status codes as success
            if 200 <= response.status_code < 300:
                logger.info(f"Webhook delivered to {subscription.name}: {response.status_code}")
                return True
            else:
                logger.error(
                    f"Webhook failed for {subscription.name}: "
                    f"HTTP {response.status_code} - {response.text[:200]}"
                )
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Webhook request failed for {subscription.name}: {e}")
            return False

    @staticmethod
    def verify_webhook_signature(payload_body, signature_header, secret):
        """
        Verify HMAC signature of incoming webhook.

        Args:
            payload_body: Raw request body (bytes or str)
            signature_header: Value of X-Spwig-Signature header
            secret: Shared webhook secret

        Returns:
            bool: True if signature is valid
        """
        if isinstance(payload_body, str):
            payload_body = payload_body.encode("utf-8")

        # Extract signature from header (format: "sha256=<signature>")
        if not signature_header.startswith("sha256="):
            return False

        provided_signature = signature_header[7:]  # Remove 'sha256=' prefix

        # Calculate expected signature
        expected_signature = hmac.new(
            secret.encode("utf-8"), payload_body, hashlib.sha256
        ).hexdigest()

        # Constant-time comparison to prevent timing attacks
        return hmac.compare_digest(provided_signature, expected_signature)
