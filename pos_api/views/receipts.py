"""
POS Digital Receipt API Views.

Endpoints for sending digital receipts via email, SMS, or WhatsApp.
"""

import logging

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from admin_api.authentication import MobileTokenAuthentication
from core.api.api_descriptions import (
    AUTH_REQUIRED,
    INVALID_REQUEST,
    ORDER_NOT_FOUND,
    POS_LICENSE_REQUIRED,
)
from pos_api.permissions import IsStaffUser

logger = logging.getLogger(__name__)


@extend_schema(
    summary=_("Send digital receipt"),
    description=_(
        "Send a digital receipt to the customer via email, SMS, or WhatsApp. "
        "The receipt is sent asynchronously via Celery task. "
        "Requires staff authentication and valid POS license."
    ),
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "method": {
                    "type": "string",
                    "enum": ["email", "sms", "whatsapp"],
                    "description": "Delivery method",
                },
                "destination": {
                    "type": "string",
                    "description": "Email address or phone number",
                },
                "language": {
                    "type": "string",
                    "description": "Language code for template (optional)",
                },
            },
            "required": ["method", "destination"],
        },
    },
    responses={
        200: OpenApiResponse(
            description=_("Receipt queued for sending"),
            examples=[
                OpenApiExample(
                    "Success",
                    value={
                        "success": True,
                        "method": "email",
                        "destination": "customer@example.com",
                        "task_id": "abc123",
                    },
                ),
            ],
        ),
        400: OpenApiResponse(description=INVALID_REQUEST),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        404: OpenApiResponse(description=ORDER_NOT_FOUND),
    },
    tags=["POS - Orders"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def send_digital_receipt(request, order_id):
    """
    Send digital receipt for a POS order.

    Body:
        method: 'email' | 'sms' | 'whatsapp'
        destination: email address or phone number
        language: optional language code
    """
    from orders.models import Order
    from pos_app import tasks

    # Get order
    try:
        order = Order.objects.get(id=order_id, channel="pos")
    except Order.DoesNotExist:
        return Response(
            {"success": False, "error": {"code": "NOT_FOUND", "message": "Order not found."}},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Parse request
    method = request.data.get("method", "").lower()
    destination = request.data.get("destination", "").strip()
    language = request.data.get("language")

    # Validate method
    if method not in ("email", "sms", "whatsapp"):
        return Response(
            {
                "success": False,
                "error": {
                    "code": "INVALID_METHOD",
                    "message": "Method must be email, sms, or whatsapp",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Validate destination
    if not destination:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "MISSING_DESTINATION",
                    "message": "Email address or phone number is required",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Basic email validation
    if method == "email" and "@" not in destination:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "INVALID_EMAIL",
                    "message": "Please provide a valid email address",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Queue the appropriate task
    try:
        if method == "email":
            task = tasks.send_pos_receipt_email.delay(
                order_pk=order.pk,
                email=destination,
                language=language,
            )
        elif method == "sms":
            task = tasks.send_pos_receipt_sms.delay(
                order_pk=order.pk,
                phone=destination,
            )
        elif method == "whatsapp":
            task = tasks.send_pos_receipt_whatsapp.delay(
                order_pk=order.pk,
                phone=destination,
            )

        # Mask PII in log output
        if "@" in destination:
            parts = destination.split("@", 1)
            masked = f"{parts[0][:2]}***@{parts[1]}"
        elif len(destination) > 4:
            masked = f"{destination[:3]}***{destination[-2:]}"
        else:
            masked = "***"
        logger.info(
            f"Queued {method} receipt for order {order.order_number} to {masked}, task_id={task.id}"
        )

        return Response(
            {
                "success": True,
                "method": method,
                "destination": destination,
                "task_id": task.id,
            }
        )

    except Exception as e:
        logger.error(f"Failed to queue receipt task: {e}", exc_info=True)
        return Response(
            {
                "success": False,
                "error": {
                    "code": "QUEUE_ERROR",
                    "message": "Failed to queue receipt. Please try again.",
                },
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@extend_schema(
    summary=_("Get receipt sending status"),
    description=_(
        "Check which digital receipts have been sent for an order. "
        "Returns timestamps for email and SMS/WhatsApp deliveries."
    ),
    responses={
        200: OpenApiResponse(
            description=_("Receipt status"),
            examples=[
                OpenApiExample(
                    "Receipt sent",
                    value={
                        "success": True,
                        "order_number": "ORD-12345",
                        "email_sent_at": "2026-02-06T10:30:00Z",
                        "sms_sent_at": None,
                        "email": "customer@example.com",
                        "phone": None,
                        "receipt_url": "https://shop.example.com/receipt/abc123/",
                    },
                ),
            ],
        ),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        404: OpenApiResponse(description=ORDER_NOT_FOUND),
    },
    tags=["POS - Orders"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def receipt_status(request, order_id):
    """Get digital receipt status for an order."""
    from orders.models import Order
    from pos_app.services.digital_receipt_service import digital_receipt_service

    try:
        order = Order.objects.get(id=order_id, channel="pos")
    except Order.DoesNotExist:
        return Response(
            {"success": False, "error": {"code": "NOT_FOUND", "message": "Order not found."}},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Get receipt URL if token exists
    receipt_url = None
    if order.receipt_token:
        receipt_url = digital_receipt_service.get_receipt_url(order, request)

    return Response(
        {
            "success": True,
            "order_number": order.order_number,
            "email_sent_at": order.receipt_email_sent_at.isoformat()
            if order.receipt_email_sent_at
            else None,
            "sms_sent_at": order.receipt_sms_sent_at.isoformat()
            if order.receipt_sms_sent_at
            else None,
            "email": order.email,
            "phone": order.phone,
            "receipt_url": receipt_url,
        }
    )
