"""
API views for webhook management.

These endpoints allow merchants to manage their webhook endpoints
and view delivery logs.
"""

import logging

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers as drf_serializers
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WebhookDelivery, WebhookEndpoint
from .serializers import (
    WebhookDeliveryDetailSerializer,
    WebhookDeliveryListSerializer,
    WebhookEndpointCreateSerializer,
    WebhookEndpointDetailSerializer,
    WebhookEndpointListSerializer,
    WebhookEndpointUpdateSerializer,
    WebhookEventSerializer,
)
from .services import get_endpoint_stats, list_available_events

logger = logging.getLogger(__name__)


class WebhookEndpointList(APIView):
    """
    List and create webhook endpoints.
    """

    permission_classes = [IsAdminUser]

    @extend_schema(
        tags=["Webhooks"],
        summary=_("List webhook endpoints"),
        description=_("Get all configured webhook endpoints for this store."),
        responses={
            200: WebhookEndpointListSerializer(many=True),
        },
    )
    def get(self, request):
        """List all webhook endpoints."""
        endpoints = WebhookEndpoint.objects.all()
        serializer = WebhookEndpointListSerializer(endpoints, many=True)
        return Response(
            {
                "success": True,
                "data": serializer.data,
                "count": endpoints.count(),
            }
        )

    @extend_schema(
        tags=["Webhooks"],
        summary=_("Create webhook endpoint"),
        description=_("""Create a new webhook endpoint.

        The secret will be auto-generated and returned in the response.
        **Store the secret securely** - it will only be shown once.

        Example events: `order.created`, `order.shipped`, `payment.received`"""),
        request=WebhookEndpointCreateSerializer,
        responses={
            201: inline_serializer(
                name="WebhookEndpointCreatedResponse",
                fields={
                    "success": drf_serializers.BooleanField(default=True),
                    "data": WebhookEndpointDetailSerializer(),
                    "message": drf_serializers.CharField(),
                },
            ),
            400: OpenApiResponse(description=_("Validation error")),
        },
    )
    def post(self, request):
        """Create a new webhook endpoint."""
        serializer = WebhookEndpointCreateSerializer(data=request.data)
        if serializer.is_valid():
            endpoint = serializer.create(serializer.validated_data)
            response_serializer = WebhookEndpointDetailSerializer(endpoint)
            return Response(
                {
                    "success": True,
                    "data": response_serializer.data,
                    "message": "Webhook endpoint created. Store the secret securely - it will not be shown again.",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class WebhookEndpointDetail(APIView):
    """
    Retrieve, update, or delete a webhook endpoint.
    """

    permission_classes = [IsAdminUser]

    @extend_schema(
        tags=["Webhooks"],
        summary=_("Get webhook endpoint"),
        description=_("Get details of a specific webhook endpoint."),
        responses={
            200: WebhookEndpointDetailSerializer,
            404: OpenApiResponse(description=_("Endpoint not found")),
        },
    )
    def get(self, request, pk):
        """Get a webhook endpoint."""
        endpoint = get_object_or_404(WebhookEndpoint, pk=pk)
        serializer = WebhookEndpointDetailSerializer(endpoint)
        data = serializer.data
        # Don't expose secret in GET requests
        data.pop("secret", None)

        # Add stats
        stats = get_endpoint_stats(str(pk))

        return Response(
            {
                "success": True,
                "data": data,
                "stats": stats,
            }
        )

    @extend_schema(
        tags=["Webhooks"],
        summary=_("Update webhook endpoint"),
        description=_("Update an existing webhook endpoint."),
        request=WebhookEndpointUpdateSerializer,
        responses={
            200: WebhookEndpointDetailSerializer,
            400: OpenApiResponse(description=_("Validation error")),
            404: OpenApiResponse(description=_("Endpoint not found")),
        },
    )
    def patch(self, request, pk):
        """Update a webhook endpoint."""
        endpoint = get_object_or_404(WebhookEndpoint, pk=pk)
        serializer = WebhookEndpointUpdateSerializer(data=request.data)
        if serializer.is_valid():
            for field, value in serializer.validated_data.items():
                setattr(endpoint, field, value)
            endpoint.save()

            response_serializer = WebhookEndpointDetailSerializer(endpoint)
            data = response_serializer.data
            data.pop("secret", None)

            return Response(
                {
                    "success": True,
                    "data": data,
                    "message": "Webhook endpoint updated.",
                }
            )
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        tags=["Webhooks"],
        summary=_("Delete webhook endpoint"),
        description=_("Delete a webhook endpoint. All delivery logs will also be deleted."),
        responses={
            204: OpenApiResponse(description=_("Endpoint deleted")),
            404: OpenApiResponse(description=_("Endpoint not found")),
        },
    )
    def delete(self, request, pk):
        """Delete a webhook endpoint."""
        endpoint = get_object_or_404(WebhookEndpoint, pk=pk)
        endpoint.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["Webhooks"],
    summary=_("Test webhook endpoint"),
    description=_("""Send a test webhook to verify the endpoint configuration.

    This sends a `test.webhook` event with sample data to verify
    that the endpoint is reachable and properly configured."""),
    responses={
        200: inline_serializer(
            name="WebhookTestResponse",
            fields={
                "success": drf_serializers.BooleanField(),
                "status_code": drf_serializers.IntegerField(allow_null=True),
                "response_time_ms": drf_serializers.IntegerField(allow_null=True),
                "response_body": drf_serializers.CharField(allow_blank=True),
                "error": drf_serializers.CharField(allow_blank=True),
            },
        ),
        404: OpenApiResponse(description=_("Endpoint not found")),
    },
)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def test_webhook_endpoint(request, pk):
    """Send a test webhook to verify endpoint configuration."""
    endpoint = get_object_or_404(WebhookEndpoint, pk=pk)

    from .tasks import send_test_webhook

    result = send_test_webhook(str(endpoint.id))

    return Response(result)


@extend_schema(
    tags=["Webhooks"],
    summary=_("Rotate webhook secret"),
    description=_("""Generate a new secret for a webhook endpoint.

    The new secret will be returned in the response. **Store it securely** -
    it will not be shown again. You will need to update your webhook
    receiver to use the new secret."""),
    responses={
        200: inline_serializer(
            name="WebhookSecretRotateResponse",
            fields={
                "success": drf_serializers.BooleanField(default=True),
                "secret": drf_serializers.CharField(help_text="The new secret"),
                "message": drf_serializers.CharField(),
            },
        ),
        404: OpenApiResponse(description=_("Endpoint not found")),
    },
)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def rotate_webhook_secret(request, pk):
    """Generate a new secret for a webhook endpoint."""
    endpoint = get_object_or_404(WebhookEndpoint, pk=pk)
    new_secret = endpoint.rotate_secret()

    logger.info(f"Rotated secret for webhook endpoint {pk}")

    return Response(
        {
            "success": True,
            "secret": new_secret,
            "message": "Secret rotated. Store the new secret securely - it will not be shown again.",
        }
    )


@extend_schema(
    tags=["Webhooks"],
    summary=_("Reset endpoint failures"),
    description=_("""Reset the failure count for a webhook endpoint.

    This re-enables an endpoint that was auto-disabled due to
    consecutive failures."""),
    responses={
        200: inline_serializer(
            name="WebhookResetResponse",
            fields={
                "success": drf_serializers.BooleanField(default=True),
                "message": drf_serializers.CharField(),
            },
        ),
        404: OpenApiResponse(description=_("Endpoint not found")),
    },
)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def reset_endpoint_failures(request, pk):
    """Reset failure count for a webhook endpoint."""
    endpoint = get_object_or_404(WebhookEndpoint, pk=pk)
    endpoint.reset_failures()

    logger.info(f"Reset failures for webhook endpoint {pk}")

    return Response(
        {
            "success": True,
            "message": "Endpoint failures reset. The endpoint is now active.",
        }
    )


class WebhookDeliveryList(APIView):
    """
    List webhook deliveries.
    """

    permission_classes = [IsAdminUser]

    @extend_schema(
        tags=["Webhooks"],
        summary=_("List webhook deliveries"),
        description=_("Get webhook delivery logs with optional filtering."),
        parameters=[
            OpenApiParameter(name="endpoint", type=str, description=_("Filter by endpoint UUID")),
            OpenApiParameter(
                name="event_type",
                type=str,
                description=_("Filter by event type (e.g., order.created)"),
            ),
            OpenApiParameter(
                name="status",
                type=str,
                enum=["pending", "success", "failed", "retrying"],
                description=_("Filter by delivery status"),
            ),
            OpenApiParameter(
                name="limit",
                type=int,
                description=_("Number of results to return (default 50, max 200)"),
            ),
        ],
        responses={
            200: WebhookDeliveryListSerializer(many=True),
        },
    )
    def get(self, request):
        """List webhook deliveries."""
        deliveries = WebhookDelivery.objects.select_related("endpoint").all()

        # Apply filters
        endpoint = request.query_params.get("endpoint")
        if endpoint:
            deliveries = deliveries.filter(endpoint_id=endpoint)

        event_type = request.query_params.get("event_type")
        if event_type:
            deliveries = deliveries.filter(event_type=event_type)

        status_filter = request.query_params.get("status")
        if status_filter:
            deliveries = deliveries.filter(status=status_filter)

        # Limit results
        limit = min(int(request.query_params.get("limit", 50)), 200)
        deliveries = deliveries[:limit]

        serializer = WebhookDeliveryListSerializer(deliveries, many=True)
        return Response(
            {
                "success": True,
                "data": serializer.data,
                "count": len(serializer.data),
            }
        )


class WebhookDeliveryDetail(APIView):
    """
    Retrieve a webhook delivery.
    """

    permission_classes = [IsAdminUser]

    @extend_schema(
        tags=["Webhooks"],
        summary=_("Get webhook delivery"),
        description=_("Get details of a specific webhook delivery including the full payload."),
        responses={
            200: WebhookDeliveryDetailSerializer,
            404: OpenApiResponse(description=_("Delivery not found")),
        },
    )
    def get(self, request, pk):
        """Get a webhook delivery."""
        delivery = get_object_or_404(WebhookDelivery.objects.select_related("endpoint"), pk=pk)
        serializer = WebhookDeliveryDetailSerializer(delivery)
        return Response(
            {
                "success": True,
                "data": serializer.data,
            }
        )


@extend_schema(
    tags=["Webhooks"],
    summary=_("Retry webhook delivery"),
    description=_("""Manually retry a failed webhook delivery.

    This queues the delivery for immediate retry, regardless of
    the scheduled retry time."""),
    responses={
        200: inline_serializer(
            name="WebhookRetryResponse",
            fields={
                "success": drf_serializers.BooleanField(default=True),
                "message": drf_serializers.CharField(),
            },
        ),
        400: OpenApiResponse(description=_("Cannot retry this delivery")),
        404: OpenApiResponse(description=_("Delivery not found")),
    },
)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def retry_webhook_delivery(request, pk):
    """Manually retry a webhook delivery."""
    delivery = get_object_or_404(WebhookDelivery, pk=pk)

    if delivery.status == WebhookDelivery.Status.SUCCESS:
        return Response(
            {
                "success": False,
                "error": "Cannot retry a successful delivery",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Queue for immediate retry
    from .tasks import deliver_webhook

    deliver_webhook.delay(str(delivery.id))

    logger.info(f"Manually retried webhook delivery {pk}")

    return Response(
        {
            "success": True,
            "message": "Delivery queued for retry.",
        }
    )


@extend_schema(
    tags=["Webhooks"],
    summary=_("List webhook event types"),
    description=_("""Get all available webhook event types.

    Returns a list of events that can be subscribed to when
    creating a webhook endpoint."""),
    responses={
        200: WebhookEventSerializer(many=True),
    },
)
@api_view(["GET"])
@permission_classes([IsAdminUser])
def list_webhook_events(request):
    """Get all available webhook event types."""
    events = list_available_events()

    return Response(
        {
            "success": True,
            "data": events,
            "count": len(events),
        }
    )


@extend_schema(
    tags=["Webhooks - Documentation"],
    summary=_("Get webhook documentation"),
    description=_("""Get comprehensive documentation for webhook integration.

    Returns all available event types, payload schemas, signature verification
    instructions, and code examples for integrating with the webhook system.

    This endpoint is publicly accessible to allow external developers to
    understand webhook payloads without authentication."""),
    responses={
        200: inline_serializer(
            name="WebhookDocumentationResponse",
            fields={
                "version": drf_serializers.CharField(help_text="API version"),
                "overview": drf_serializers.CharField(help_text="Overview markdown"),
                "signature_verification": drf_serializers.CharField(
                    help_text="Signature verification docs"
                ),
                "headers": drf_serializers.DictField(help_text="Headers sent with webhooks"),
                "retry_policy": drf_serializers.DictField(help_text="Retry behavior details"),
                "events": drf_serializers.ListField(help_text="All available events with schemas"),
            },
        ),
    },
)
@api_view(["GET"])
def get_webhook_documentation(request):
    """
    Get comprehensive webhook documentation.

    This provides all the information developers need to integrate
    with the webhook system, including:
    - All available event types with descriptions
    - Payload schemas for each event category
    - Signature verification instructions with code examples
    - Headers sent with each webhook
    - Retry and failure policies
    """
    from core.version import __version__ as PLATFORM_VERSION

    from .events import get_events_by_category
    from .openapi_webhooks import (
        WEBHOOK_SIGNATURE_DOCS,
        CustomerWebhookData,
        InventoryWebhookData,
        OrderWebhookData,
        ProductWebhookData,
        ShipmentWebhookData,
        SubscriptionWebhookData,
    )

    # Build payload schema documentation
    payload_schemas = {
        "order": {
            "description": "Payload for order-related events",
            "fields": _serializer_to_schema(OrderWebhookData()),
        },
        "product": {
            "description": "Payload for product-related events",
            "fields": _serializer_to_schema(ProductWebhookData()),
        },
        "customer": {
            "description": "Payload for customer-related events",
            "fields": _serializer_to_schema(CustomerWebhookData()),
        },
        "shipment": {
            "description": "Payload for shipment-related events",
            "fields": _serializer_to_schema(ShipmentWebhookData()),
        },
        "inventory": {
            "description": "Payload for inventory-related events",
            "fields": _serializer_to_schema(InventoryWebhookData()),
        },
        "subscription": {
            "description": "Payload for subscription-related events",
            "fields": _serializer_to_schema(SubscriptionWebhookData()),
        },
    }

    # Build events list with categories and schemas
    events_by_category = get_events_by_category()
    events_list = []
    for category, events in events_by_category.items():
        category_data = {
            "category": category,
            "events": events,
            "payload_schema": payload_schemas.get(
                category,
                {
                    "description": f"Payload for {category}-related events",
                    "fields": {},
                },
            ),
        }
        events_list.append(category_data)

    documentation = {
        "version": PLATFORM_VERSION,
        "overview": """
# Spwig Webhooks

Webhooks allow you to receive real-time HTTP notifications when events occur in your store.
This enables you to build integrations, sync data with external systems, and automate workflows.

## Getting Started

1. **Create an endpoint** - Configure a webhook endpoint in your admin dashboard
2. **Subscribe to events** - Choose which events you want to receive
3. **Implement verification** - Use HMAC-SHA256 to verify webhook authenticity
4. **Handle payloads** - Process the JSON payloads in your application

## Best Practices

- Always verify webhook signatures before processing
- Respond quickly (within 30 seconds) with a 2xx status code
- Process webhooks asynchronously if they require long operations
- Handle duplicate deliveries idempotently using the delivery ID
- Store delivery IDs to detect and skip duplicates
        """.strip(),
        "signature_verification": WEBHOOK_SIGNATURE_DOCS,
        "headers": {
            "X-Spwig-Signature": {
                "description": "HMAC-SHA256 signature for verification",
                "format": "t={timestamp},v1={signature}",
            },
            "X-Spwig-Event": {
                "description": "The event type (e.g., order.created)",
            },
            "X-Spwig-Delivery-Id": {
                "description": "Unique delivery identifier (UUID)",
            },
            "X-Spwig-Timestamp": {
                "description": "Unix timestamp when the webhook was sent",
            },
            "Content-Type": {
                "description": "Always application/json; charset=utf-8",
            },
            "User-Agent": {
                "description": "Spwig-Webhooks/1.0",
            },
        },
        "retry_policy": {
            "max_attempts": 5,
            "backoff_schedule": [
                {"attempt": 1, "delay": "immediate"},
                {"attempt": 2, "delay": "1 minute"},
                {"attempt": 3, "delay": "2 minutes"},
                {"attempt": 4, "delay": "4 minutes"},
                {"attempt": 5, "delay": "8 minutes"},
            ],
            "success_codes": "2xx",
            "timeout_seconds": 30,
            "auto_disable_after": "10 consecutive failures",
        },
        "events": events_list,
        "payload_schemas": payload_schemas,
        "example_payload": {
            "event": "order.created",
            "created_at": "2025-01-15T10:30:00Z",
            "data": {
                "id": 12345,
                "order_number": "ORD-2025-00001",
                "status": "pending",
                "total": "99.99",
                "currency": "USD",
                "customer_email": "customer@example.com",
                "customer_id": 789,
                "items_count": 3,
                "created_at": "2025-01-15T10:30:00Z",
                "updated_at": "2025-01-15T10:30:00Z",
            },
        },
    }

    return Response(documentation)


def _serializer_to_schema(serializer):
    """Convert a serializer to a simple schema dict for documentation."""
    schema = {}
    for field_name, field in serializer.fields.items():
        field_info = {
            "type": field.__class__.__name__.replace("Field", "").lower(),
            "required": field.required,
        }
        if hasattr(field, "help_text") and field.help_text:
            field_info["description"] = str(field.help_text)
        if hasattr(field, "allow_null"):
            field_info["nullable"] = field.allow_null
        schema[field_name] = field_info
    return schema


@extend_schema(
    tags=["Webhooks"],
    summary=_("Get webhook endpoint stats"),
    description=_("Get delivery statistics for a webhook endpoint."),
    responses={
        200: inline_serializer(
            name="WebhookStatsResponse",
            fields={
                "success": drf_serializers.BooleanField(default=True),
                "data": inline_serializer(
                    name="WebhookStatsData",
                    fields={
                        "endpoint_id": drf_serializers.CharField(),
                        "endpoint_name": drf_serializers.CharField(),
                        "period": drf_serializers.CharField(),
                        "total_deliveries": drf_serializers.IntegerField(),
                        "successful": drf_serializers.IntegerField(),
                        "failed": drf_serializers.IntegerField(),
                        "retrying": drf_serializers.IntegerField(),
                        "pending": drf_serializers.IntegerField(),
                        "success_rate": drf_serializers.FloatField(),
                        "avg_response_time_ms": drf_serializers.FloatField(),
                        "is_healthy": drf_serializers.BooleanField(),
                        "consecutive_failures": drf_serializers.IntegerField(),
                        "is_disabled": drf_serializers.BooleanField(),
                    },
                ),
            },
        ),
        404: OpenApiResponse(description=_("Endpoint not found")),
    },
)
@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_webhook_stats(request, pk):
    """Get delivery statistics for a webhook endpoint."""
    get_object_or_404(WebhookEndpoint, pk=pk)
    stats = get_endpoint_stats(str(pk))

    return Response(
        {
            "success": True,
            "data": stats,
        }
    )
