"""
Webhook serializers for payload generation.

This module provides serializers for converting model instances
into webhook payload data.
"""

import ipaddress
import logging
import socket
from urllib.parse import urlparse

from django.db.models import Model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

logger = logging.getLogger(__name__)


def check_webhook_target_url(value):
    """Return ``value`` if it is a safe webhook target, else raise ``ValueError``.

    Framework-neutral SSRF guard shared by configuration-time validation (the
    API serializers and the admin creation wizard) and delivery-time
    re-resolution. Enforces HTTPS outside ``DEBUG`` and then resolves the
    hostname, rejecting any URL whose resolved address is loopback, private,
    link-local, multicast, reserved, or unspecified (this covers cloud-metadata
    endpoints such as ``169.254.169.254``). Delivery-time code re-runs this
    check because DNS answers can change between validation and delivery (DNS
    rebinding), and because an endpoint may have been stored before this guard
    existed.
    """
    from django.conf import settings

    # Developers routinely point webhooks at localhost while testing, so the
    # SSRF guard only applies to real (non-DEBUG) installs.
    if settings.DEBUG:
        return value

    if not value.startswith("https://"):
        raise ValueError("Webhook URLs must use HTTPS in production")

    hostname = urlparse(value).hostname
    if not hostname:
        raise ValueError("Webhook URL must include a valid host")

    try:
        addrinfo = socket.getaddrinfo(hostname, None)
    except OSError as exc:
        raise ValueError("Webhook URL host could not be resolved") from exc

    for *_meta, sockaddr in addrinfo:
        ip = ipaddress.ip_address(sockaddr[0])
        if (
            ip.is_loopback
            or ip.is_private
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
            or ip.is_unspecified
        ):
            raise ValueError("Webhook URL must not target internal or reserved addresses")

    return value


def validate_webhook_target_url(value):
    """DRF field validator wrapping :func:`check_webhook_target_url`.

    Re-raises the guard's ``ValueError`` as a DRF ``ValidationError`` so it can
    be used directly as a serializer field validator.
    """
    try:
        return check_webhook_target_url(value)
    except ValueError as exc:
        raise serializers.ValidationError(str(exc)) from exc


# =============================================================================
# Webhook Endpoint Serializers (for API)
# =============================================================================


class WebhookEndpointListSerializer(serializers.Serializer):
    """Serializer for listing webhook endpoints."""

    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    url = serializers.URLField()
    is_active = serializers.BooleanField()
    events = serializers.ListField(child=serializers.CharField())
    created_at = serializers.DateTimeField(read_only=True)
    last_triggered_at = serializers.DateTimeField(read_only=True)
    consecutive_failures = serializers.IntegerField(read_only=True)
    is_disabled_by_failures = serializers.BooleanField(read_only=True)


class WebhookEndpointDetailSerializer(serializers.Serializer):
    """Serializer for webhook endpoint details."""

    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=255)
    url = serializers.URLField(max_length=2048)
    secret = serializers.CharField(read_only=True, help_text=_("Only shown once on creation"))
    is_active = serializers.BooleanField(default=True)
    events = serializers.ListField(
        child=serializers.CharField(), help_text=_("List of event types to subscribe to")
    )
    description = serializers.CharField(required=False, allow_blank=True)
    max_retries = serializers.IntegerField(min_value=0, max_value=10, default=5)
    timeout_seconds = serializers.IntegerField(min_value=5, max_value=60, default=30)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    last_triggered_at = serializers.DateTimeField(read_only=True)
    consecutive_failures = serializers.IntegerField(read_only=True)
    is_disabled_by_failures = serializers.BooleanField(read_only=True)


class WebhookEndpointCreateSerializer(serializers.Serializer):
    """Serializer for creating a webhook endpoint."""

    name = serializers.CharField(max_length=255)
    url = serializers.URLField(max_length=2048)
    events = serializers.ListField(
        child=serializers.CharField(), help_text=_("List of event types to subscribe to")
    )
    description = serializers.CharField(required=False, allow_blank=True, default="")
    max_retries = serializers.IntegerField(min_value=0, max_value=10, default=5)
    timeout_seconds = serializers.IntegerField(min_value=5, max_value=60, default=30)
    is_active = serializers.BooleanField(default=True)

    def validate_url(self, value):
        """Validate webhook URL."""
        return validate_webhook_target_url(value)

    def validate_events(self, value):
        """Validate event types."""
        from .events import validate_events

        valid, invalid = validate_events(value)
        if invalid:
            # Allow but warn about unknown events
            logger.warning(f"Unknown webhook events: {invalid}")
        if not value:
            raise serializers.ValidationError("At least one event must be specified")
        return value

    def create(self, validated_data):
        from .models import WebhookEndpoint

        return WebhookEndpoint.objects.create(**validated_data)


class WebhookEndpointUpdateSerializer(serializers.Serializer):
    """Serializer for updating a webhook endpoint."""

    name = serializers.CharField(max_length=255, required=False)
    url = serializers.URLField(max_length=2048, required=False)
    events = serializers.ListField(child=serializers.CharField(), required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    max_retries = serializers.IntegerField(min_value=0, max_value=10, required=False)
    timeout_seconds = serializers.IntegerField(min_value=5, max_value=60, required=False)
    is_active = serializers.BooleanField(required=False)

    def validate_url(self, value):
        return validate_webhook_target_url(value)

    def validate_events(self, value):
        from .events import validate_events

        if value is not None:
            valid, invalid = validate_events(value)
            if invalid:
                logger.warning(f"Unknown webhook events: {invalid}")
            if not value:
                raise serializers.ValidationError("At least one event must be specified")
        return value


class WebhookDeliveryListSerializer(serializers.Serializer):
    """Serializer for listing webhook deliveries."""

    id = serializers.UUIDField(read_only=True)
    endpoint_id = serializers.UUIDField(source="endpoint.id")
    endpoint_name = serializers.CharField(source="endpoint.name")
    event_type = serializers.CharField()
    status = serializers.CharField()
    response_status_code = serializers.IntegerField()
    response_time_ms = serializers.IntegerField()
    attempt_count = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    delivered_at = serializers.DateTimeField()


class WebhookDeliveryDetailSerializer(serializers.Serializer):
    """Serializer for webhook delivery details."""

    id = serializers.UUIDField(read_only=True)
    endpoint_id = serializers.UUIDField(source="endpoint.id")
    endpoint_name = serializers.CharField(source="endpoint.name")
    event_type = serializers.CharField()
    payload = serializers.JSONField()
    status = serializers.CharField()
    response_status_code = serializers.IntegerField()
    response_body = serializers.CharField()
    response_headers = serializers.JSONField()
    response_time_ms = serializers.IntegerField()
    error_message = serializers.CharField()
    attempt_count = serializers.IntegerField()
    next_retry_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()
    delivered_at = serializers.DateTimeField()


class WebhookEventSerializer(serializers.Serializer):
    """Serializer for webhook event type information."""

    event = serializers.CharField()
    description = serializers.CharField()
    category = serializers.CharField()


# =============================================================================
# Payload Serializers (for webhook event data)
# =============================================================================


class OrderWebhookPayloadSerializer(serializers.Serializer):
    """Serializer for order webhook payloads."""

    id = serializers.IntegerField()
    order_number = serializers.CharField()
    status = serializers.CharField()
    total = serializers.DecimalField(max_digits=12, decimal_places=2, source="total_amount.amount")
    currency = serializers.CharField(source="total_amount.currency")
    customer_email = serializers.EmailField(source="email", allow_null=True)
    customer_id = serializers.IntegerField(source="user.id", allow_null=True)
    items_count = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def get_items_count(self, obj):
        return obj.items.count() if hasattr(obj, "items") else 0


class ProductWebhookPayloadSerializer(serializers.Serializer):
    """Serializer for product webhook payloads."""

    id = serializers.IntegerField()
    sku = serializers.CharField()
    name = serializers.CharField()
    slug = serializers.CharField()
    status = serializers.CharField()
    price = serializers.DecimalField(
        max_digits=12, decimal_places=2, source="price.amount", allow_null=True
    )
    currency = serializers.CharField(source="price.currency")
    sale_price = serializers.SerializerMethodField()
    stock_quantity = serializers.IntegerField(source="total_stock", allow_null=True)
    is_published = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def get_sale_price(self, obj):
        """Current sale price amount, or null when the product is not on sale."""
        return obj.calculate_sale_price()

    def get_is_published(self, obj):
        """Whether the product is publicly published."""
        return obj.status == "published"


class CustomerWebhookPayloadSerializer(serializers.Serializer):
    """Serializer for customer webhook payloads."""

    id = serializers.IntegerField()
    email = serializers.EmailField(source="user.email")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    created_at = serializers.DateTimeField(source="user.date_joined")


class ShipmentWebhookPayloadSerializer(serializers.Serializer):
    """Serializer for shipment webhook payloads."""

    id = serializers.IntegerField()
    order_id = serializers.IntegerField(source="order.id")
    order_number = serializers.CharField(source="order.order_number")
    tracking_number = serializers.CharField()
    carrier = serializers.CharField(source="carrier_name", allow_null=True)
    status = serializers.CharField()
    shipped_at = serializers.DateTimeField(allow_null=True)
    delivered_at = serializers.DateTimeField(allow_null=True)
    created_at = serializers.DateTimeField()


class InventoryWebhookPayloadSerializer(serializers.Serializer):
    """Serializer for inventory webhook payloads."""

    product_id = serializers.IntegerField()
    product_sku = serializers.CharField()
    product_name = serializers.CharField()
    previous_stock = serializers.IntegerField()
    current_stock = serializers.IntegerField()
    low_stock_threshold = serializers.IntegerField(allow_null=True)


class SubscriptionWebhookPayloadSerializer(serializers.Serializer):
    """Serializer for subscription webhook payloads."""

    id = serializers.IntegerField()
    customer_id = serializers.IntegerField(source="customer.id")
    customer_email = serializers.EmailField(source="customer.email")
    plan_name = serializers.CharField(source="plan.name")
    status = serializers.CharField()
    current_period_start = serializers.DateTimeField()
    current_period_end = serializers.DateTimeField()
    created_at = serializers.DateTimeField()


class RefundWebhookPayloadSerializer(serializers.Serializer):
    """Serializer for refund webhook payloads."""

    id = serializers.IntegerField()
    order_id = serializers.IntegerField(source="order.id")
    order_number = serializers.CharField(source="order.order_number")
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    currency = serializers.CharField()
    reason = serializers.CharField(allow_blank=True)
    status = serializers.CharField()
    created_at = serializers.DateTimeField()


class TranslationJobWebhookPayloadSerializer(serializers.Serializer):
    """Serializer for translation job webhook payloads."""

    id = serializers.IntegerField()
    job_type = serializers.CharField()
    status = serializers.CharField()
    content_type = serializers.CharField(allow_null=True)
    source_language = serializers.CharField()
    target_languages = serializers.ListField(child=serializers.CharField())
    progress = serializers.IntegerField()
    total_characters = serializers.IntegerField()
    translated_characters = serializers.IntegerField()
    error_message = serializers.CharField(allow_blank=True)
    created_at = serializers.DateTimeField()
    completed_at = serializers.DateTimeField(allow_null=True)


# =============================================================================
# Payload Generation
# =============================================================================

# Mapping of event prefixes to serializer classes
EVENT_SERIALIZERS = {
    "order": OrderWebhookPayloadSerializer,
    "product": ProductWebhookPayloadSerializer,
    "customer": CustomerWebhookPayloadSerializer,
    "shipment": ShipmentWebhookPayloadSerializer,
    "inventory": InventoryWebhookPayloadSerializer,
    "subscription": SubscriptionWebhookPayloadSerializer,
    "refund": RefundWebhookPayloadSerializer,
    "translation": TranslationJobWebhookPayloadSerializer,
}


def get_serializer_for_event(event_type: str):
    """
    Get the appropriate serializer class for an event type.

    Args:
        event_type: The webhook event type (e.g., 'order.created')

    Returns:
        Serializer class or None
    """
    prefix = event_type.split(".")[0] if "." in event_type else event_type
    return EVENT_SERIALIZERS.get(prefix)


def get_payload_for_event(event_type: str, instance: Model) -> dict:
    """
    Generate a webhook payload for an event and model instance.

    Args:
        event_type: The webhook event type
        instance: The model instance to serialize

    Returns:
        Dictionary of serialized data
    """
    serializer_class = get_serializer_for_event(event_type)

    if serializer_class is not None:
        # A serializer was selected for a known event: serialize with it and let
        # any failure propagate so the delivery fails visibly rather than being
        # queued with a silently incomplete generic payload.
        serializer = serializer_class(instance)
        return serializer.data

    # No event-specific serializer registered — fall back to generic data.
    return _generic_serialize(instance)


def _generic_serialize(instance: Model) -> dict:
    """
    Generic model serialization for webhook payloads.

    Args:
        instance: Model instance to serialize

    Returns:
        Dictionary with basic model data
    """
    data = {
        "id": instance.pk,
        "model": f"{instance._meta.app_label}.{instance._meta.model_name}",
    }

    # Add common fields if they exist
    for field in ["created_at", "updated_at", "status", "name", "email"]:
        if hasattr(instance, field):
            value = getattr(instance, field)
            if hasattr(value, "isoformat"):
                value = value.isoformat()
            data[field] = value

    return data
