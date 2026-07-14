"""
Admin API Bulk Order Views

Bulk order status update and fulfillment endpoints for the merchant mobile app.
"""

import logging
import secrets

from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from admin_api.permissions import category_permission
from admin_api.serializers.auth import BulkOperationResponseSerializer, ErrorResponseSerializer
from admin_api.serializers.bulk_operations import (
    BulkOrderFulfillSerializer,
    BulkOrderStatusSerializer,
)
from admin_api.services.audit_service import AuditService
from admin_api.throttling import AdminSensitiveOperationThrottle
from core.api.api_descriptions import AUTH_REQUIRED, PERMISSION_DENIED, RATE_LIMIT_EXCEEDED
from orders.models import Order

logger = logging.getLogger(__name__)


def generate_error_reference():
    """Generate a unique error reference for debugging."""
    return f"ERR-{secrets.token_hex(3).upper()}"


# Valid order status transitions: from_status -> [allowed_to_statuses]
VALID_ORDER_STATUS_TRANSITIONS = {
    "pending": ["processing", "cancelled"],
    "processing": ["shipped", "cancelled"],
    "shipped": ["delivered", "cancelled"],
    "delivered": ["refunded"],
    "cancelled": ["pending"],
    "refunded": [],
}


@extend_schema(
    tags=["Admin - Bulk Operations"],
    summary=_("Bulk update order statuses"),
    description=_("""
    Update the status of multiple orders in a single request.

    **Rate Limit:** 30 requests per minute (sensitive operation)

    Maximum 100 orders per request. Each order is processed independently;
    individual failures do not affect other orders in the batch.

    **Valid status transitions:**
    - pending -> processing, cancelled
    - processing -> shipped, cancelled
    - shipped -> delivered, cancelled
    - delivered -> refunded
    - cancelled -> pending
    """),
    request=BulkOrderStatusSerializer,
    responses={
        200: BulkOperationResponseSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["POST"])
@permission_classes([category_permission("orders", "full")])
@throttle_classes([AdminSensitiveOperationThrottle])
def bulk_order_status(request):
    """
    Bulk update order statuses with validation of status transitions.
    """
    serializer = BulkOrderStatusSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid bulk status update request."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    order_numbers = serializer.validated_data["order_numbers"]
    new_status = serializer.validated_data["status"]

    succeeded = 0
    failed = 0
    results = []

    for order_number in order_numbers:
        try:
            with transaction.atomic():
                order = Order.objects.select_for_update().get(order_number=order_number)
                old_status = order.status

                # Validate status transition
                allowed_transitions = VALID_ORDER_STATUS_TRANSITIONS.get(old_status, [])
                if new_status not in allowed_transitions:
                    results.append(
                        {
                            "order_number": order_number,
                            "success": False,
                            "error": _('Invalid transition from "%(old)s" to "%(new)s".')
                            % {"old": old_status, "new": new_status},
                        }
                    )
                    failed += 1
                    continue

                order.status = new_status

                # Set delivered_at timestamp when marking as delivered
                if new_status == "delivered" and not order.delivered_at:
                    order.delivered_at = timezone.now()

                order.save(update_fields=["status", "delivered_at", "updated_at"])

                AuditService.log_order_status_change(
                    user=request.user,
                    order=order,
                    old_status=old_status,
                    new_status=new_status,
                    request=request,
                )

                results.append(
                    {
                        "order_number": order_number,
                        "success": True,
                        "old_status": old_status,
                        "new_status": new_status,
                    }
                )
                succeeded += 1

        except Order.DoesNotExist:
            results.append(
                {"order_number": order_number, "success": False, "error": _("Order not found.")}
            )
            failed += 1
        except Exception as e:
            logger.error(f"Bulk order status update failed for {order_number}: {e}", exc_info=True)
            results.append({"order_number": order_number, "success": False, "error": str(e)})
            failed += 1

    AuditService.log_bulk_operation(
        user=request.user,
        action="order.bulk_status_update",
        resource_type="order",
        created_count=succeeded,
        error_count=failed,
        request=request,
    )

    return Response(
        {
            "success": succeeded > 0,
            "data": {
                "total": len(order_numbers),
                "succeeded": succeeded,
                "failed": failed,
                "results": results,
            },
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin - Bulk Operations"],
    summary=_("Bulk fulfill orders"),
    description=_("""
    Fulfill multiple orders in a single request by updating their status to 'shipped'
    and optionally setting tracking information.

    **Rate Limit:** 30 requests per minute (sensitive operation)

    Maximum 100 orders per request. Each order is processed independently;
    individual failures do not affect other orders in the batch.

    For each order:
    - Status is updated to 'shipped'
    - Tracking number is set on the order (if provided)
    - shipped_at timestamp is recorded in order metadata
    """),
    request=BulkOrderFulfillSerializer,
    responses={
        200: BulkOperationResponseSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["POST"])
@permission_classes([category_permission("orders", "full")])
@throttle_classes([AdminSensitiveOperationThrottle])
def bulk_order_fulfill(request):
    """
    Bulk fulfill orders with optional tracking information.
    """
    serializer = BulkOrderFulfillSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid bulk fulfillment request."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    orders_data = serializer.validated_data["orders"]
    serializer.validated_data.get("notify_customers", True)

    succeeded = 0
    failed = 0
    results = []

    for order_data in orders_data:
        order_number = order_data["order_number"]
        tracking_number = order_data.get("tracking_number", "")
        tracking_url = order_data.get("tracking_url", "")
        carrier_name = order_data.get("carrier", "")

        try:
            with transaction.atomic():
                order = Order.objects.select_for_update().get(order_number=order_number)
                old_status = order.status

                # Only allow fulfillment from pending or processing
                if old_status not in ("pending", "processing"):
                    results.append(
                        {
                            "order_number": order_number,
                            "success": False,
                            "error": _(
                                'Cannot fulfill order with status "%(status)s". '
                                'Order must be "pending" or "processing".'
                            )
                            % {"status": old_status},
                        }
                    )
                    failed += 1
                    continue

                # Update order status and tracking
                order.status = "shipped"
                if tracking_number:
                    order.tracking_number = tracking_number

                # Store fulfillment metadata
                now = timezone.now()
                fulfillment_info = {
                    "shipped_at": now.isoformat(),
                    "fulfilled_by": request.user.get_full_name() or request.user.username,
                }
                if tracking_url:
                    fulfillment_info["tracking_url"] = tracking_url
                if carrier_name:
                    fulfillment_info["carrier"] = carrier_name

                # Merge into order metadata
                metadata = order.metadata or {}
                metadata["fulfillment"] = fulfillment_info
                order.metadata = metadata

                update_fields = ["status", "tracking_number", "metadata", "updated_at"]
                order.save(update_fields=update_fields)

                AuditService.log_order_status_change(
                    user=request.user,
                    order=order,
                    old_status=old_status,
                    new_status="shipped",
                    tracking_number=tracking_number,
                    request=request,
                )

                result_entry = {
                    "order_number": order_number,
                    "success": True,
                    "old_status": old_status,
                    "new_status": "shipped",
                    "tracking_number": tracking_number or None,
                    "shipped_at": now.isoformat(),
                }
                results.append(result_entry)
                succeeded += 1

        except Order.DoesNotExist:
            results.append(
                {"order_number": order_number, "success": False, "error": _("Order not found.")}
            )
            failed += 1
        except Exception as e:
            logger.error(f"Bulk order fulfillment failed for {order_number}: {e}", exc_info=True)
            results.append({"order_number": order_number, "success": False, "error": str(e)})
            failed += 1

    AuditService.log_bulk_operation(
        user=request.user,
        action="order.bulk_fulfill",
        resource_type="order",
        created_count=succeeded,
        error_count=failed,
        request=request,
    )

    return Response(
        {
            "success": succeeded > 0,
            "data": {
                "total": len(orders_data),
                "succeeded": succeeded,
                "failed": failed,
                "results": results,
            },
        },
        status=status.HTTP_200_OK,
    )
