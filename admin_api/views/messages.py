"""
Admin API Customer Message Views

Customer message management endpoints for the merchant mobile app.

Supports two message sources:
- contact_form: CustomerMessage model (standalone contact form submissions)
- order_note: OrderNote model (customer notes attached to orders)

Both sources are unified into a single API for the mobile app.
"""

import secrets

from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from admin_api.models import CustomerMessage, MessageReadReceipt, MessageReply
from admin_api.permissions import IsStaffWithWritePermission
from admin_api.serializers.auth import ErrorResponseSerializer
from admin_api.serializers.messages import (
    MessageFilterSerializer,
    MessageReplyInputSerializer,
    MessageReplyResponseSerializer,
    MessageStatusUpdateSerializer,
    UnifiedMessageDetailSerializer,
    UnifiedMessageListSerializer,
)
from admin_api.throttling import AdminAPIThrottle
from orders.models import OrderNote


def generate_error_reference():
    """Generate a unique error reference for debugging."""
    return f"ERR-{secrets.token_hex(3).upper()}"


def _get_read_receipts_for_messages(source, object_ids):
    """
    Batch-load read receipts for a set of messages.

    Returns a dict: {object_id: [{'name': ..., 'read_at': ...}, ...]}
    """
    receipts = (
        MessageReadReceipt.objects.filter(
            source=source,
            object_id__in=object_ids,
        )
        .select_related("user")
        .order_by("read_at")
    )

    result = {}
    for receipt in receipts:
        entry = {
            "name": receipt.user.get_full_name() or receipt.user.email,
            "read_at": receipt.read_at,
        }
        result.setdefault(receipt.object_id, []).append(entry)
    return result


def _get_user_read_set(user, source, object_ids):
    """
    Returns a set of object_ids that the given user has read.
    """
    return set(
        MessageReadReceipt.objects.filter(
            source=source,
            object_id__in=object_ids,
            user=user,
        ).values_list("object_id", flat=True)
    )


def _record_read_receipt(user, source, object_id):
    """Create a read receipt for the current user (idempotent)."""
    MessageReadReceipt.objects.get_or_create(
        source=source,
        object_id=object_id,
        user=user,
    )


def _compute_last_activity_at(msg_data):
    """Compute last_activity_at from last_reply_at or created_at."""
    return msg_data.get("last_reply_at") or msg_data["created_at"]


def _transform_customer_message(msg):
    """Transform CustomerMessage to unified format."""
    preview = msg.message[:100] + "..." if len(msg.message) > 100 else msg.message
    last_activity = msg.last_reply_at or msg.created_at
    return {
        "id": msg.id,
        "source": "contact_form",
        "name": msg.name,
        "email": msg.email,
        "subject": msg.subject,
        "preview": preview,
        "status": msg.status,
        "status_display": msg.get_status_display(),
        "created_at": msg.created_at,
        # Thread info
        "reply_count": msg.reply_count,
        "last_reply_at": msg.last_reply_at,
        # Per-user read tracking (populated by view after batch loading)
        "is_read_by_me": False,
        "read_by": [],
        "last_activity_at": last_activity,
        # Deep linking fields
        "message_id": msg.id,
        "order_id": msg.order_id,
        "order_number": msg.order.order_number if msg.order else None,
    }


def _transform_customer_message_detail(msg):
    """Transform CustomerMessage to unified detail format."""
    read_by_name = None
    if msg.read_by:
        read_by_name = msg.read_by.get_full_name() or msg.read_by.email

    replied_by_name = None
    if msg.replied_by:
        replied_by_name = msg.replied_by.get_full_name() or msg.replied_by.email

    # Build replies list from prefetched data
    replies = []
    if hasattr(msg, "_prefetched_objects_cache") and "replies" in msg._prefetched_objects_cache:
        reply_qs = msg._prefetched_objects_cache["replies"]
    else:
        reply_qs = msg.replies.select_related("sender_user").all()
    for reply in reply_qs:
        replies.append(
            {
                "id": reply.id,
                "sender_type": reply.sender_type,
                "sender_name": reply.sender_name,
                "content": reply.content,
                "email_sent": reply.email_sent,
                "created_at": reply.created_at,
            }
        )

    return {
        "id": msg.id,
        "source": "contact_form",
        "name": msg.name,
        "email": msg.email,
        "phone": msg.phone or "",
        "subject": msg.subject,
        "message": msg.message,
        "message_type": msg.message_type,
        "type_display": msg.get_message_type_display(),
        "status": msg.status,
        "status_display": msg.get_status_display(),
        "read_at": msg.read_at,
        "read_by_name": read_by_name,
        "created_at": msg.created_at,
        "updated_at": msg.updated_at,
        # Legacy reply fields (backward compat)
        "reply_text": msg.reply_text or None,
        "replied_at": msg.replied_at,
        "replied_by_name": replied_by_name,
        # Thread replies
        "replies": replies,
        "reply_count": msg.reply_count,
        # Per-user read tracking (populated by caller)
        "is_read_by_me": False,
        "read_by": [],
        "last_activity_at": msg.last_reply_at or msg.created_at,
        # Deep linking fields
        "message_id": msg.id,
        "order_id": msg.order_id,
        "order_number": msg.order.order_number if msg.order else None,
    }


def _transform_order_note(note):
    """Transform OrderNote to unified format."""
    # Get customer info from the order
    order = note.order
    customer_name = order.billing_name or order.shipping_name or "Customer"
    customer_email = order.email

    # Use order number as subject context
    subject = f"Re: Order #{order.order_number}"

    preview = note.note[:100] + "..." if len(note.note) > 100 else note.note

    # Map is_read to status
    status_value = "read" if note.is_read else "unread"
    status_display = "Read" if note.is_read else "Unread"

    return {
        "id": note.id,
        "source": "order_note",
        "name": customer_name,
        "email": customer_email,
        "subject": subject,
        "preview": preview,
        "status": status_value,
        "status_display": status_display,
        "created_at": note.created_at,
        # Thread info (order notes don't have threading)
        "reply_count": 0,
        "last_reply_at": None,
        # Per-user read tracking (populated by view after batch loading)
        "is_read_by_me": False,
        "read_by": [],
        "last_activity_at": note.created_at,
        # Deep linking fields
        "message_id": None,
        "order_id": order.id,
        "order_number": order.order_number,
    }


def _transform_order_note_detail(note):
    """Transform OrderNote to unified detail format."""
    order = note.order
    customer_name = order.billing_name or order.shipping_name or "Customer"
    customer_email = order.email
    customer_phone = order.billing_phone or order.shipping_phone or ""

    subject = f"Re: Order #{order.order_number}"

    status_value = "read" if note.is_read else "unread"
    status_display = "Read" if note.is_read else "Unread"

    return {
        "id": note.id,
        "source": "order_note",
        "name": customer_name,
        "email": customer_email,
        "phone": customer_phone,
        "subject": subject,
        "message": note.note,
        "message_type": "order",
        "type_display": "Order Related",
        "status": status_value,
        "status_display": status_display,
        "read_at": note.updated_at if note.is_read else None,
        "read_by_name": None,  # OrderNote doesn't track who read it
        "created_at": note.created_at,
        "updated_at": note.updated_at,
        # Legacy reply fields (not applicable for order notes)
        "reply_text": None,
        "replied_at": None,
        "replied_by_name": None,
        # Thread replies (order notes don't have threading)
        "replies": [],
        "reply_count": 0,
        # Per-user read tracking (populated by caller)
        "is_read_by_me": False,
        "read_by": [],
        "last_activity_at": note.created_at,
        # Deep linking fields
        "message_id": None,
        "order_id": order.id,
        "order_number": order.order_number,
    }


@extend_schema(
    tags=["Admin"],
    summary=_("List customer messages"),
    description=_("""
    Get a paginated list of customer messages from all sources.

    **Rate Limit:** 300 requests per minute

    **Sources:**
    - `contact_form`: Messages from contact form submissions
    - `order_note`: Customer notes attached to orders

    Messages are sorted by latest activity by default (most recent reply or creation time).

    **Deep Linking:**
    - For `source='contact_form'`: Use `message_id` to navigate to message detail
    - For `source='order_note'`: Use `order_number` to navigate to order detail
    """),
    parameters=[
        OpenApiParameter(
            name="source",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Filter by source: 'all', 'contact_form', 'order_note'"),
            required=False,
            default="all",
        ),
        OpenApiParameter(
            name="status",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Filter by status: 'all', 'unread', 'read', 'replied', 'archived'"),
            required=False,
            default="all",
        ),
        OpenApiParameter(
            name="search",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Search by sender name, email, or subject"),
            required=False,
        ),
        OpenApiParameter(
            name="sort",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_(
                "Sort order: '-activity' (latest activity, default), '-created_at' (newest), 'created_at' (oldest), 'status' (group by status)"
            ),
            required=False,
            default="-activity",
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
        200: UnifiedMessageListSerializer(many=True),
        401: ErrorResponseSerializer,
    },
)
@api_view(["GET"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def message_list(request):
    """
    List customer messages from all sources with filtering and pagination.
    """
    # Validate filter parameters
    filter_serializer = MessageFilterSerializer(data=request.query_params)
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
    source_filter = filters.get("source", "all")
    message_status = filters.get("status", "all")
    search = filters.get("search", "").strip()
    sort_by = filters.get("sort", "-activity")
    page = filters.get("page", 1)
    page_size = filters.get("page_size", 20)

    unified_messages = []

    # Query CustomerMessage (contact_form source)
    if source_filter in ("all", "contact_form"):
        cm_queryset = CustomerMessage.objects.select_related("order")

        if message_status != "all":
            cm_queryset = cm_queryset.filter(status=message_status)

        if search:
            cm_queryset = cm_queryset.filter(
                Q(name__icontains=search)
                | Q(email__icontains=search)
                | Q(subject__icontains=search)
            )

        for msg in cm_queryset:
            unified_messages.append(_transform_customer_message(msg))

    # Query OrderNote (order_note source) - only customer notes
    if source_filter in ("all", "order_note"):
        on_queryset = OrderNote.objects.filter(is_customer_note=True).select_related("order")

        # Map status filter to is_read
        if message_status == "unread":
            on_queryset = on_queryset.filter(is_read=False)
        elif message_status == "read":
            on_queryset = on_queryset.filter(is_read=True)
        elif message_status in ("replied", "archived"):
            # OrderNotes don't have these statuses, exclude them
            on_queryset = on_queryset.none()

        if search:
            on_queryset = on_queryset.filter(
                Q(note__icontains=search)
                | Q(order__email__icontains=search)
                | Q(order__billing_name__icontains=search)
                | Q(order__shipping_name__icontains=search)
                | Q(order__order_number__icontains=search)
            )

        for note in on_queryset:
            unified_messages.append(_transform_order_note(note))

    # Batch-load read receipts for per-user tracking
    cm_ids = [m["id"] for m in unified_messages if m["source"] == "contact_form"]
    on_ids = [m["id"] for m in unified_messages if m["source"] == "order_note"]

    cm_receipts = _get_read_receipts_for_messages("contact_form", cm_ids) if cm_ids else {}
    on_receipts = _get_read_receipts_for_messages("order_note", on_ids) if on_ids else {}
    cm_user_read = _get_user_read_set(request.user, "contact_form", cm_ids) if cm_ids else set()
    on_user_read = _get_user_read_set(request.user, "order_note", on_ids) if on_ids else set()

    for msg in unified_messages:
        if msg["source"] == "contact_form":
            msg["is_read_by_me"] = msg["id"] in cm_user_read
            msg["read_by"] = cm_receipts.get(msg["id"], [])
        else:
            msg["is_read_by_me"] = msg["id"] in on_user_read
            msg["read_by"] = on_receipts.get(msg["id"], [])

    # Apply sorting based on sort parameter
    if sort_by == "-activity":
        unified_messages.sort(key=lambda x: x["last_activity_at"], reverse=True)
    elif sort_by == "-created_at":
        unified_messages.sort(key=lambda x: x["created_at"], reverse=True)
    elif sort_by == "created_at":
        unified_messages.sort(key=lambda x: x["created_at"], reverse=False)
    elif sort_by == "status":
        status_order = {"unread": 0, "read": 1, "replied": 2, "archived": 3}
        unified_messages.sort(
            key=lambda x: (status_order.get(x["status"], 99), -x["created_at"].timestamp())
        )

    # Pagination
    total_count = len(unified_messages)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_messages = unified_messages[start:end]

    # Serialize
    serializer = UnifiedMessageListSerializer(paginated_messages, many=True)

    return Response(
        {
            "success": True,
            "data": {
                "messages": serializer.data,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_count": total_count,
                    "total_pages": (total_count + page_size - 1) // page_size
                    if total_count > 0
                    else 0,
                },
            },
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin"],
    summary=_("Get message details"),
    description=_("""
    Get full details of a customer message.

    **Rate Limit:** 300 requests per minute

    **URL Format:** `/messages/{source}/{id}/`
    - `source`: Either 'contact_form' or 'order_note'
    - `id`: The message ID within that source

    Automatically marks the message as read if it was unread.

    **Deep Linking:**
    - For `source='contact_form'`: Returns full contact form message
    - For `source='order_note'`: Returns order note with order info for linking
    """),
    responses={
        200: UnifiedMessageDetailSerializer,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
)
@api_view(["GET"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def message_detail(request, source, message_id):
    """
    Get message details and mark as read.

    Args:
        source: 'contact_form' or 'order_note'
        message_id: ID of the message within that source
    """
    if source == "contact_form":
        try:
            from django.db.models import Prefetch

            message = (
                CustomerMessage.objects.select_related("order", "read_by", "replied_by")
                .prefetch_related(
                    Prefetch("replies", queryset=MessageReply.objects.select_related("sender_user"))
                )
                .get(id=message_id)
            )
        except CustomerMessage.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "error": {
                        "code": 404,
                        "message": _("Message not found."),
                        "reference": generate_error_reference(),
                    },
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Auto-mark as read (legacy global status)
        message.mark_as_read(request.user)

        # Record per-user read receipt
        _record_read_receipt(request.user, "contact_form", message.id)

        data = _transform_customer_message_detail(message)

    elif source == "order_note":
        try:
            note = (
                OrderNote.objects.filter(is_customer_note=True)
                .select_related("order")
                .get(id=message_id)
            )
        except OrderNote.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "error": {
                        "code": 404,
                        "message": _("Message not found."),
                        "reference": generate_error_reference(),
                    },
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Auto-mark as read (legacy global status)
        if not note.is_read:
            note.is_read = True
            note.save(update_fields=["is_read", "updated_at"])

        # Record per-user read receipt
        _record_read_receipt(request.user, "order_note", note.id)

        data = _transform_order_note_detail(note)

    else:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _('Invalid source. Must be "contact_form" or "order_note".'),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Populate per-user read tracking
    receipts = _get_read_receipts_for_messages(source, [int(message_id)])
    data["read_by"] = receipts.get(int(message_id), [])
    data["is_read_by_me"] = True  # We just recorded the receipt

    serializer = UnifiedMessageDetailSerializer(data)

    return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Admin"],
    summary=_("Update message status"),
    description=_("""
    Update the status of a customer message.

    **Rate Limit:** 300 requests per minute

    **URL Format:** `/messages/{source}/{id}/status/`
    - `source`: Either 'contact_form' or 'order_note'
    - `id`: The message ID within that source

    **Status Options:**
    - read: Mark as read
    - replied: Mark as replied (contact_form only)
    - archived: Archive the message (contact_form only)

    Note: OrderNotes only support 'read' status.
    """),
    request=MessageStatusUpdateSerializer,
    responses={
        200: UnifiedMessageDetailSerializer,
        400: ErrorResponseSerializer,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
)
@api_view(["POST"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def update_message_status(request, source, message_id):
    """
    Update message status.

    Args:
        source: 'contact_form' or 'order_note'
        message_id: ID of the message within that source
    """
    serializer = MessageStatusUpdateSerializer(data=request.data)
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

    new_status = serializer.validated_data["status"]

    if source == "contact_form":
        try:
            message = CustomerMessage.objects.select_related("order", "read_by").get(id=message_id)
        except CustomerMessage.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "error": {
                        "code": 404,
                        "message": _("Message not found."),
                        "reference": generate_error_reference(),
                    },
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if new_status == "read":
            message.mark_as_read(request.user)
            _record_read_receipt(request.user, "contact_form", message.id)
        elif new_status == "replied":
            message.mark_as_replied()
        elif new_status == "archived":
            message.archive()

        data = _transform_customer_message_detail(message)

    elif source == "order_note":
        try:
            note = (
                OrderNote.objects.filter(is_customer_note=True)
                .select_related("order")
                .get(id=message_id)
            )
        except OrderNote.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "error": {
                        "code": 404,
                        "message": _("Message not found."),
                        "reference": generate_error_reference(),
                    },
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # OrderNotes only support 'read' status
        if new_status in ("replied", "archived"):
            return Response(
                {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": _('Order notes only support "read" status.'),
                        "reference": generate_error_reference(),
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        note.is_read = True
        note.save(update_fields=["is_read", "updated_at"])
        _record_read_receipt(request.user, "order_note", note.id)

        data = _transform_order_note_detail(note)

    else:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _('Invalid source. Must be "contact_form" or "order_note".'),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Populate per-user read tracking
    receipts = _get_read_receipts_for_messages(source, [int(message_id)])
    data["read_by"] = receipts.get(int(message_id), [])
    data["is_read_by_me"] = MessageReadReceipt.objects.filter(
        source=source, object_id=int(message_id), user=request.user
    ).exists()

    return Response(
        {
            "success": True,
            "message": _("Message status updated successfully."),
            "data": UnifiedMessageDetailSerializer(data).data,
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin"],
    summary=_("Get unread message count"),
    description=_("""
    Get the count of unread customer messages for the current user.

    **Rate Limit:** 300 requests per minute

    Useful for badge display in the app. Counts are per-user — a message
    is "unread" if the current staff member has not read it yet, regardless
    of whether other staff members have.

    Returns breakdown by source:
    - `contact_form`: Unread contact form submissions for this user
    - `order_note`: Unread customer notes on orders for this user
    - `total`: Combined total
    """),
    responses={
        200: dict,
        401: ErrorResponseSerializer,
    },
)
@api_view(["GET"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def unread_count(request):
    """
    Get count of messages unread by the current user.
    """
    # All non-archived contact form message IDs
    cm_all_ids = set(
        CustomerMessage.objects.exclude(status="archived").values_list("id", flat=True)
    )
    # IDs this user has read
    cm_read_ids = set(
        MessageReadReceipt.objects.filter(
            source="contact_form",
            user=request.user,
            object_id__in=cm_all_ids,
        ).values_list("object_id", flat=True)
    )
    contact_form_unread = len(cm_all_ids - cm_read_ids)

    # All customer order note IDs
    on_all_ids = set(OrderNote.objects.filter(is_customer_note=True).values_list("id", flat=True))
    on_read_ids = set(
        MessageReadReceipt.objects.filter(
            source="order_note",
            user=request.user,
            object_id__in=on_all_ids,
        ).values_list("object_id", flat=True)
    )
    order_note_unread = len(on_all_ids - on_read_ids)

    return Response(
        {
            "success": True,
            "data": {
                "unread_count": contact_form_unread + order_note_unread,
                "by_source": {
                    "contact_form": contact_form_unread,
                    "order_note": order_note_unread,
                },
            },
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin"],
    summary=_("Get message counts by status"),
    description=_("""
    Get count of messages by status and source for badge display.

    **Rate Limit:** 300 requests per minute

    The `unread_by_me` field shows messages the current user has not read,
    regardless of the message's global status.

    Returns counts for both sources:
    - `contact_form`: Full status breakdown (unread, read, replied, archived)
    - `order_note`: Simple status (unread, read)
    """),
    responses={
        200: dict,
        401: ErrorResponseSerializer,
    },
)
@api_view(["GET"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def message_counts(request):
    """
    Get message counts by status and source, plus per-user unread.
    """
    from django.db.models import Count

    # CustomerMessage counts (global status)
    cm_counts = CustomerMessage.objects.values("status").annotate(count=Count("id"))
    cm_status_counts = {item["status"]: item["count"] for item in cm_counts}
    cm_total = sum(cm_status_counts.values())

    # OrderNote counts (global status)
    on_unread = OrderNote.objects.filter(is_customer_note=True, is_read=False).count()
    on_read = OrderNote.objects.filter(is_customer_note=True, is_read=True).count()
    on_total = on_unread + on_read

    # Per-user unread: messages this user hasn't read yet
    cm_all_ids = set(
        CustomerMessage.objects.exclude(status="archived").values_list("id", flat=True)
    )
    cm_user_read = set(
        MessageReadReceipt.objects.filter(
            source="contact_form",
            user=request.user,
            object_id__in=cm_all_ids,
        ).values_list("object_id", flat=True)
    )
    cm_unread_by_me = len(cm_all_ids - cm_user_read)

    on_all_ids = set(OrderNote.objects.filter(is_customer_note=True).values_list("id", flat=True))
    on_user_read = set(
        MessageReadReceipt.objects.filter(
            source="order_note",
            user=request.user,
            object_id__in=on_all_ids,
        ).values_list("object_id", flat=True)
    )
    on_unread_by_me = len(on_all_ids - on_user_read)

    return Response(
        {
            "success": True,
            "data": {
                "unread_by_me": cm_unread_by_me + on_unread_by_me,
                "total": cm_total + on_total,
                "by_source": {
                    "contact_form": {
                        "by_status": cm_status_counts,
                        "unread_by_me": cm_unread_by_me,
                        "total": cm_total,
                    },
                    "order_note": {
                        "by_status": {
                            "unread": on_unread,
                            "read": on_read,
                        },
                        "unread_by_me": on_unread_by_me,
                        "total": on_total,
                    },
                },
            },
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin"],
    summary=_("Reply to customer message"),
    description=_("""
    Reply to a customer message from the contact form.

    **Rate Limit:** 300 requests per minute

    **URL Format:** `/messages/contact_form/{id}/reply/`

    This endpoint:
    1. Stores the reply text against the message
    2. Updates message status to 'replied'
    3. Optionally sends an email to the customer

    Note: This endpoint only works for `contact_form` messages.
    For order notes, use the order notes reply endpoint instead.
    """),
    request=MessageReplyInputSerializer,
    responses={
        200: MessageReplyResponseSerializer,
        400: ErrorResponseSerializer,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
)
@api_view(["POST"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def reply_to_message(request, message_id):
    """
    Reply to a customer message.

    Creates a MessageReply in the thread and optionally emails the customer.
    Supports multi-turn conversations — merchants can reply multiple times.

    Args:
        message_id: ID of the CustomerMessage to reply to
    """
    serializer = MessageReplyInputSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid reply data."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        message = CustomerMessage.objects.select_related("order").get(id=message_id)
    except CustomerMessage.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Message not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    reply_text = serializer.validated_data["reply_text"]
    send_email = serializer.validated_data.get("send_email", True)
    custom_subject = serializer.validated_data.get("subject")

    email_sent = False
    email_error = None

    # Send email if requested (before creating reply, so we know the result)
    if send_email and message.email:
        try:
            from email_system.services.email_sender import EmailSendingService

            email_subject = custom_subject or f"Re: {message.subject}"

            html_body = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px;">
                <p>{reply_text.replace(chr(10), "<br>")}</p>
                <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">
                <p style="color: #666; font-size: 0.9em;">
                    <strong>Original Message:</strong><br>
                    From: {message.name} &lt;{message.email}&gt;<br>
                    Subject: {message.subject}<br>
                    Date: {message.created_at.strftime("%B %d, %Y at %I:%M %p")}
                </p>
                <blockquote style="margin: 10px 0; padding: 10px; border-left: 3px solid #e0e0e0; color: #666;">
                    {message.message.replace(chr(10), "<br>")}
                </blockquote>
            </div>
            """

            result = EmailSendingService.send_immediate(
                to_email=message.email,
                subject=email_subject,
                html_body=html_body,
                text_body=reply_text,
                template_type="message_reply",
                tags=["message_reply", f"message_{message.id}"],
            )

            email_sent = result.get("success", False)
            if not email_sent:
                email_error = result.get("message", "Failed to send email")

        except Exception as e:
            email_error = str(e)

    # Create reply in the thread (also updates legacy fields for backward compat)
    message.add_reply(
        sender_type="staff",
        content=reply_text,
        sender_user=request.user,
        email_sent=email_sent,
    )

    replied_by_name = request.user.get_full_name() or request.user.email

    response_data = {
        "id": message.id,
        "reply_text": message.reply_text,
        "replied_at": message.replied_at,
        "replied_by_name": replied_by_name,
        "email_sent": email_sent,
        "status": message.status,
        "status_display": message.get_status_display(),
    }

    if email_error:
        response_data["email_error"] = email_error

    return Response(
        {
            "success": True,
            "message": _("Reply sent successfully.")
            if email_sent
            else _("Reply saved successfully."),
            "data": MessageReplyResponseSerializer(response_data).data,
        },
        status=status.HTTP_200_OK,
    )
