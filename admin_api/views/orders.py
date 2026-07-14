"""
Admin API Order Views

Order management endpoints for the merchant mobile app.
"""

import logging
import secrets

from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models import Prefetch, Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from admin_api.permissions import IsStaffWithWritePermission
from admin_api.serializers.auth import ErrorResponseSerializer
from admin_api.serializers.orders import (
    AdminOrderDetailSerializer,
    AdminOrderListSerializer,
    OrderCancelSerializer,
    OrderFilterSerializer,
    OrderNoteCreateSerializer,
    OrderNoteSerializer,
    OrderRefundSerializer,
    OrderStatusUpdateSerializer,
    TrackingUpdateSerializer,
)
from admin_api.services.audit_service import AuditService
from admin_api.throttling import AdminAPIThrottle, AdminSensitiveOperationThrottle
from orders.models import Order, OrderNote

logger = logging.getLogger(__name__)


def generate_error_reference():
    """Generate a unique error reference for debugging."""
    return f"ERR-{secrets.token_hex(3).upper()}"


@extend_schema(
    tags=["Admin"],
    summary=_("List orders"),
    description=_("""
    Get a paginated list of orders with filtering and sorting.

    **Rate Limit:** 300 requests per minute

    **Filtering:**
    Use either `status` for a specific status or `filter_type` for status groups.
    If `status` is provided (not 'all'), `filter_type` is ignored.

    **Filter Types (groups):**
    - all: All orders (default)
    - open: Orders with status pending or processing
    - completed: Orders with status shipped or delivered
    - refunded: Orders with status refunded or cancelled

    **Sort Options:**
    - -created_at: Newest first (default)
    - created_at: Oldest first
    - -total_amount: Highest value first
    - total_amount: Lowest value first
    - -updated_at: Recently updated first
    - updated_at: Least recently updated first
    - customer_name: Customer name A-Z
    - -customer_name: Customer name Z-A
    """),
    parameters=[
        OpenApiParameter(
            name="filter_type",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_(
                "Filter type: 'all', 'open', 'completed', 'refunded'. Ignored if 'status' is provided."
            ),
            required=False,
            default="all",
        ),
        OpenApiParameter(
            name="status",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Specific status filter"),
            required=False,
        ),
        OpenApiParameter(
            name="search",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Search by order number, email, customer name, or phone number"),
            required=False,
        ),
        OpenApiParameter(
            name="sort",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_(
                "Sort field: '-created_at', 'created_at', '-total_amount', 'total_amount', '-updated_at', 'updated_at', 'customer_name', '-customer_name'"
            ),
            required=False,
            default="-created_at",
        ),
        OpenApiParameter(
            name="date_from",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Filter orders from this date (YYYY-MM-DD)"),
            required=False,
        ),
        OpenApiParameter(
            name="date_to",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Filter orders up to this date (YYYY-MM-DD)"),
            required=False,
        ),
        OpenApiParameter(
            name="page",
            type=int,
            location=OpenApiParameter.QUERY,
            description=_("Page number"),
            required=False,
            default=1,
        ),
        OpenApiParameter(
            name="page_size",
            type=int,
            location=OpenApiParameter.QUERY,
            description=_("Items per page (max 100)"),
            required=False,
            default=20,
        ),
    ],
    responses={
        200: AdminOrderListSerializer(many=True),
        401: ErrorResponseSerializer,
    },
)
@api_view(["GET"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def order_list(request):
    """
    List orders with filtering and pagination.
    """
    # Validate filter parameters
    filter_serializer = OrderFilterSerializer(data=request.query_params)
    if not filter_serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid filter parameters."),
                    "reference": generate_error_reference(),
                    "details": filter_serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    filters = filter_serializer.validated_data
    queryset = Order.objects.select_related("user").prefetch_related("items")

    # Apply filters - specific status takes precedence over filter_type
    specific_status = filters.get("status", "all")
    if specific_status != "all":
        # Specific status filter overrides filter_type
        queryset = queryset.filter(status=specific_status)
    else:
        # Apply filter_type only when no specific status is requested
        filter_type = filters.get("filter_type", "all")
        if filter_type == "open":
            queryset = queryset.filter(status__in=["pending", "processing"])
        elif filter_type == "completed":
            queryset = queryset.filter(status__in=["shipped", "delivered"])
        elif filter_type == "refunded":
            queryset = queryset.filter(status__in=["refunded", "cancelled"])
        # 'all' - no filter

    # Apply search
    search = filters.get("search", "").strip()
    if search:
        queryset = queryset.filter(
            Q(order_number__icontains=search)
            | Q(email__icontains=search)
            | Q(shipping_name__icontains=search)
            | Q(phone__icontains=search)
            | Q(shipping_phone__icontains=search)
            | Q(billing_phone__icontains=search)
        )

    # Apply date range filter
    date_from = filters.get("date_from")
    date_to = filters.get("date_to")
    if date_from:
        queryset = queryset.filter(created_at__date__gte=date_from)
    if date_to:
        queryset = queryset.filter(created_at__date__lte=date_to)

    # Apply sorting
    sort = filters.get("sort", "-created_at")
    sort_field_map = {
        "customer_name": "shipping_name",
        "-customer_name": "-shipping_name",
    }
    queryset = queryset.order_by(sort_field_map.get(sort, sort))

    # Pagination
    page = filters.get("page", 1)
    page_size = filters.get("page_size", 20)
    start = (page - 1) * page_size
    end = start + page_size

    total_count = queryset.count()
    orders = queryset[start:end]

    serializer = AdminOrderListSerializer(orders, many=True)

    return Response(
        {
            "success": True,
            "data": {
                "orders": serializer.data,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_count": total_count,
                    "total_pages": (total_count + page_size - 1) // page_size,
                },
            },
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin"],
    summary=_("Get order details"),
    description=_("""
    Get full details of a specific order.

    **Rate Limit:** 300 requests per minute
    """),
    responses={
        200: AdminOrderDetailSerializer,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
)
@api_view(["GET"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def order_detail(request, order_number):
    """
    Get order details by order number.
    """
    try:
        order = (
            Order.objects.select_related("user", "carrier")
            .prefetch_related(
                Prefetch("items__product__images"),
                Prefetch("items__variant__images"),
            )
            .get(order_number=order_number)
        )
    except Order.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Order not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = AdminOrderDetailSerializer(order)

    return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Admin"],
    summary=_("Get order notes"),
    description=_("""
    Get all notes for an order (both merchant and customer notes).

    **Rate Limit:** 300 requests per minute
    """),
    responses={
        200: OrderNoteSerializer(many=True),
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
)
@api_view(["GET"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def order_notes(request, order_number):
    """
    Get all notes for an order.
    """
    try:
        order = Order.objects.get(order_number=order_number)
    except Order.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Order not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    notes = OrderNote.objects.filter(order=order).select_related("author").order_by("-created_at")
    serializer = OrderNoteSerializer(notes, many=True)

    return Response(
        {"success": True, "data": {"notes": serializer.data, "count": notes.count()}},
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin"],
    summary=_("Add note to order"),
    description=_("""
    Add a note to an order. Can be used to reply to customer messages.

    **Rate Limit:** 30 requests per minute (sensitive operation)

    **Fields:**
    - `note`: The note content (required)
    - `is_customer_visible`: Whether the customer can see this note (default: true)
    - `notify_customer`: Whether to send email notification to customer (default: false)

    When replying to a customer's order note, set `is_customer_visible: true` so
    the customer can see your response in their order history.
    """),
    request=OrderNoteCreateSerializer,
    responses={
        201: OrderNoteSerializer,
        400: ErrorResponseSerializer,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
)
@api_view(["POST"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def add_order_note(request, order_number):
    """
    Add a note to an order.
    """
    try:
        order = Order.objects.get(order_number=order_number)
    except Order.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Order not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = OrderNoteCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid note data."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Create the note
    note = OrderNote.objects.create(
        order=order,
        author=request.user,
        note=serializer.validated_data["note"],
        is_customer_note=serializer.validated_data.get("is_customer_visible", True),
        is_read=True,  # Merchant notes are already "read" by the merchant
    )

    # Audit log
    AuditService.log(
        user=request.user,
        action="order.note_added",
        resource_type="order",
        resource_id=order.order_number,
        new_value={
            "note_id": note.id,
            "is_customer_visible": note.is_customer_note,
            "notify_customer": serializer.validated_data.get("notify_customer", False),
        },
        request=request,
    )

    # Send email notification if requested and note is customer-visible
    if serializer.validated_data.get("notify_customer") and note.is_customer_note:
        try:
            from email_system.services.email_sender import EmailSendingService
            from email_system.utils.language import get_order_email_language

            site = Site.objects.get_current()
            site_url = f"http://{site.domain}" if settings.DEBUG else f"https://{site.domain}"

            EmailSendingService.send_template_email(
                to_email=order.email,
                template_type="order_note_notification",
                context={
                    "customer_name": order.shipping_name,
                    "order_number": order.order_number,
                    "order_url": f"{site_url}/orders/{order.order_number}/",
                    "note_content": note.note,
                    "staff_name": request.user.get_full_name() or request.user.email,
                },
                language=get_order_email_language(order),
                enable_tracking=True,
            )
        except Exception as e:
            logger.error(
                f"Failed to send order note email for {order.order_number}: {e}", exc_info=True
            )

    response_serializer = OrderNoteSerializer(note)

    return Response(
        {
            "success": True,
            "message": _("Note added successfully."),
            "data": response_serializer.data,
        },
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    tags=["Admin"],
    summary=_("Update order status"),
    description=_("""
    Update the status of an order.

    **Rate Limit:** 30 requests per minute (sensitive operation)

    **Allowed Transitions:**
    - pending → processing, cancelled
    - processing → shipped, cancelled, pending
    - shipped → delivered, processing
    - delivered → refunded
    - cancelled → pending (reopen)
    - refunded → (terminal state)

    Optionally include tracking number when marking as shipped.
    """),
    request=OrderStatusUpdateSerializer,
    responses={
        200: AdminOrderDetailSerializer,
        400: ErrorResponseSerializer,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
)
@api_view(["POST"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def update_order_status(request, order_number):
    """
    Update order status.
    """
    try:
        order = Order.objects.get(order_number=order_number)
    except Order.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Order not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = OrderStatusUpdateSerializer(data=request.data, context={"order": order})

    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid status update."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    old_status = order.status
    new_status = serializer.validated_data["status"]
    tracking_number = serializer.validated_data.get("tracking_number", "")
    notes = serializer.validated_data.get("notes", "")

    # Update order
    order.status = new_status
    if tracking_number:
        order.tracking_number = tracking_number
    if notes:
        order.notes = f"{order.notes}\n\n[{timezone.now().strftime('%Y-%m-%d %H:%M')}] Status changed to {new_status}: {notes}".strip()

    # Handle special status updates
    if new_status == "delivered" and not order.delivered_at:
        order.delivered_at = timezone.now()

    order.save()

    # Audit log
    AuditService.log_order_status_change(
        user=request.user,
        order=order,
        old_status=old_status,
        new_status=new_status,
        request=request,
        tracking_number=tracking_number,
        notes=notes,
    )

    return Response(
        {
            "success": True,
            "message": _("Order status updated successfully."),
            "data": AdminOrderDetailSerializer(order).data,
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin"],
    summary=_("Update tracking number"),
    description=_("""
    Update or add tracking number for an order.

    **Rate Limit:** 30 requests per minute (sensitive operation)
    """),
    request=TrackingUpdateSerializer,
    responses={
        200: AdminOrderDetailSerializer,
        400: ErrorResponseSerializer,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
)
@api_view(["POST"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def update_tracking(request, order_number):
    """
    Update order tracking information.
    """
    try:
        order = Order.objects.get(order_number=order_number)
    except Order.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Order not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = TrackingUpdateSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid tracking information."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    old_tracking = order.tracking_number
    new_tracking = serializer.validated_data["tracking_number"]
    carrier = serializer.validated_data.get("carrier", "")

    # Update order
    order.tracking_number = new_tracking
    order.save()

    # Audit log
    AuditService.log_tracking_update(
        user=request.user,
        order=order,
        old_tracking=old_tracking,
        new_tracking=new_tracking,
        carrier=carrier,
        request=request,
    )

    return Response(
        {
            "success": True,
            "message": _("Tracking information updated successfully."),
            "data": AdminOrderDetailSerializer(order).data,
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin"],
    summary=_("Cancel order"),
    description=_("""
    Cancel an order. This is a destructive action.

    **Rate Limit:** 30 requests per minute (sensitive operation)

    Only orders in pending or processing status can be cancelled.
    """),
    request=OrderCancelSerializer,
    responses={
        200: AdminOrderDetailSerializer,
        400: ErrorResponseSerializer,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
)
@api_view(["POST"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def cancel_order(request, order_number):
    """
    Cancel an order.
    """
    try:
        order = Order.objects.get(order_number=order_number)
    except Order.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Order not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # Check if order can be cancelled
    if order.status not in ["pending", "processing"]:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Only pending or processing orders can be cancelled."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = OrderCancelSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid request."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    old_status = order.status
    reason = serializer.validated_data.get("reason", "")

    # Update order
    order.status = "cancelled"
    if reason:
        order.notes = f"{order.notes}\n\n[{timezone.now().strftime('%Y-%m-%d %H:%M')}] Cancelled: {reason}".strip()
    order.save()

    # Audit log
    AuditService.log_order_status_change(
        user=request.user,
        order=order,
        old_status=old_status,
        new_status="cancelled",
        request=request,
        notes=reason,
    )

    # Send cancellation email if requested (defaults to True)
    if serializer.validated_data.get("notify_customer", True):
        try:
            from email_system.services.email_sender import EmailSendingService
            from email_system.utils.language import get_order_email_language

            site = Site.objects.get_current()
            site_url = f"http://{site.domain}" if settings.DEBUG else f"https://{site.domain}"

            EmailSendingService.send_template_email(
                to_email=order.email,
                template_type="order_cancelled",
                context={
                    "customer_name": order.shipping_name,
                    "order_number": order.order_number,
                    "order_url": f"{site_url}/orders/{order.order_number}/",
                    "cancellation_reason": reason,
                    "cancellation_date": timezone.now().strftime("%B %d, %Y"),
                },
                language=get_order_email_language(order),
                enable_tracking=True,
            )
        except Exception as e:
            logger.error(
                f"Failed to send cancellation email for {order.order_number}: {e}", exc_info=True
            )

    return Response(
        {
            "success": True,
            "message": _("Order cancelled successfully."),
            "data": AdminOrderDetailSerializer(order).data,
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin"],
    summary=_("Initiate refund"),
    description=_("""
    Initiate a refund for an order.

    **Rate Limit:** 30 requests per minute (sensitive operation)

    This endpoint initiates the refund process. Actual payment refund
    handling may depend on the payment provider configuration.
    """),
    request=OrderRefundSerializer,
    responses={
        200: AdminOrderDetailSerializer,
        400: ErrorResponseSerializer,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
)
@api_view(["POST"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def initiate_refund(request, order_number):
    """
    Initiate a refund for an order.
    """
    try:
        order = Order.objects.get(order_number=order_number)
    except Order.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Order not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # Check if order can be refunded
    if order.payment_status not in ["paid", "partially_refunded"]:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Only paid orders can be refunded."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = OrderRefundSerializer(data=request.data, context={"order": order})
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid refund request."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    old_status = order.status
    reason = serializer.validated_data.get("reason", "")
    refund_amount = serializer.validated_data.get("amount")

    # If no amount provided, assume full refund
    if not refund_amount:
        refund_amount = order.amount_paid.amount - order.amount_refunded.amount

    # Update order (simplified - actual refund would involve payment provider)
    order.amount_refunded.amount += refund_amount

    # Update status based on refund
    if order.amount_refunded.amount >= order.amount_paid.amount:
        order.status = "refunded"
        order.payment_status = "refunded"
    else:
        order.payment_status = "partially_refunded"

    if reason:
        order.notes = f"{order.notes}\n\n[{timezone.now().strftime('%Y-%m-%d %H:%M')}] Refund initiated ({refund_amount}): {reason}".strip()
    order.save()

    # Audit log
    AuditService.log(
        user=request.user,
        action="order.refund",
        resource_type="order",
        resource_id=order.order_number,
        old_value={
            "status": old_status,
            "amount_refunded": str(order.amount_refunded.amount - refund_amount),
        },
        new_value={
            "status": order.status,
            "amount_refunded": str(order.amount_refunded.amount),
            "refund_amount": str(refund_amount),
        },
        request=request,
    )

    return Response(
        {
            "success": True,
            "message": _("Refund initiated successfully."),
            "data": AdminOrderDetailSerializer(order).data,
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin"],
    summary=_("Get order counts by status"),
    description=_("""
    Get count of orders by status for badge display.

    **Rate Limit:** 300 requests per minute
    """),
    responses={
        200: dict,
        401: ErrorResponseSerializer,
    },
)
@api_view(["GET"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def order_counts(request):
    """
    Get order counts by status for badge display.
    """
    from django.db.models import Count

    counts = Order.objects.values("status").annotate(count=Count("id"))
    status_counts = {item["status"]: item["count"] for item in counts}

    # Calculate aggregate counts
    open_count = status_counts.get("pending", 0) + status_counts.get("processing", 0)
    completed_count = status_counts.get("shipped", 0) + status_counts.get("delivered", 0)

    return Response(
        {
            "success": True,
            "data": {
                "by_status": status_counts,
                "open": open_count,
                "completed": completed_count,
                "total": sum(status_counts.values()),
            },
        },
        status=status.HTTP_200_OK,
    )
