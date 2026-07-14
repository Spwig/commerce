"""
POS Orders API views.

Order listing, detail, receipt data, refund, and void operations.
All endpoints require staff authentication and a valid POS license.
"""

from datetime import date
from decimal import Decimal

from django.db import transaction
from django.db.models import Prefetch, Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from admin_api.authentication import MobileTokenAuthentication
from core.api.api_descriptions import (
    AUTH_REQUIRED,
    NO_OPEN_SHIFT,
    ORDER_NOT_FOUND,
    POS_LICENSE_REQUIRED,
)
from pos_api.permissions import IsStaffUser, check_pos_permission
from pos_api.serializers.order import (
    POSOrderListSerializer,
    POSOrderSerializer,
    POSReceiptSerializer,
)
from pos_api.views.checkout import _serialize_order
from pos_api.views.utils import get_open_shift, get_terminal


def _get_order_thumbnails(order, request, limit=4):
    """Get absolute thumbnail URLs for order items.

    Uses prefetched items with product__images to avoid N+1 queries.
    """
    thumbnails = []
    # Use prefetch cache if available (from order_list query)
    prefetched_items = getattr(order, "_prefetched_objects_cache", {}).get("items", None)
    items = (
        list(prefetched_items)[:limit]
        if prefetched_items is not None
        else order.items.all()[:limit]
    )

    for item in items:
        if not item.product:
            continue
        # Check for prefetched images on the product
        prefetched_images = getattr(item.product, "_prefetched_objects_cache", {}).get(
            "images", None
        )
        if prefetched_images is not None:
            # Find primary image or fall back to first
            primary = next((i for i in prefetched_images if i.is_primary), None)
            if not primary and prefetched_images:
                primary = prefetched_images[0]
            if primary and primary.media_asset:
                thumb_url = primary.media_asset.get_thumbnail("product_thumbnail")
                if thumb_url:
                    thumbnails.append(request.build_absolute_uri(thumb_url))
        elif item.product.primary_image:
            # Fallback to property (will trigger query if not prefetched)
            thumb_url = item.product.primary_image.get_thumbnail("product_thumbnail")
            if thumb_url:
                thumbnails.append(request.build_absolute_uri(thumb_url))
    return thumbnails


@extend_schema(
    summary=_("List POS orders"),
    description=_(
        "Returns orders with advanced filtering for date range, origin, customer, "
        "cashier, and search. Supports viewing web orders for return scenarios. "
        "Default: today's orders from this terminal only. "
        "Search mode: When 'search' is provided, date/origin/cashier filters are "
        "bypassed to find any order by number, customer name, email, or phone. "
        "Requires staff authentication and valid POS license."
    ),
    parameters=[
        OpenApiParameter(
            "date_from",
            OpenApiTypes.DATE,
            description=_(
                "Start date for range filter (ISO format, default: today). Ignored when search is provided."
            ),
        ),
        OpenApiParameter(
            "date_to",
            OpenApiTypes.DATE,
            description=_(
                "End date for range filter (ISO format, default: today). Ignored when search is provided."
            ),
        ),
        OpenApiParameter(
            "origin",
            OpenApiTypes.STR,
            enum=["this_terminal", "all_pos", "all"],
            description=_(
                "Order origin filter: this_terminal (default), all_pos, all (includes web). Ignored when search is provided."
            ),
        ),
        OpenApiParameter(
            "customer_id",
            OpenApiTypes.INT,
            description=_("Filter by customer user ID. Ignored when search is provided."),
        ),
        OpenApiParameter(
            "cashier_id",
            OpenApiTypes.INT,
            description=_("Filter by cashier staff ID. Ignored when search is provided."),
        ),
        OpenApiParameter(
            "search",
            OpenApiTypes.STR,
            description=_(
                "Search across ALL orders by order number, customer name, email, or phone. Bypasses date/origin filters."
            ),
        ),
        OpenApiParameter(
            "status",
            OpenApiTypes.STR,
            description=_("Filter by order status (applies in both modes)"),
        ),
        OpenApiParameter("page", OpenApiTypes.INT, description=_("Page number (default: 1)")),
        OpenApiParameter(
            "page_size", OpenApiTypes.INT, description=_("Items per page (default: 20, max: 100)")
        ),
    ],
    responses={
        200: POSOrderListSerializer(many=True),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Orders"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def order_list(request):
    """List POS orders with advanced filtering."""
    from orders.models import Order

    terminal, err = get_terminal(request)
    if err:
        return err

    # Check for search query - when searching, bypass date/origin filters
    # This allows finding any order by number/customer regardless of current filters
    search = request.query_params.get("search", "").strip()

    # Date range filter (defaults to today)
    today_str = str(date.today())
    date_from_str = request.query_params.get("date_from", today_str)
    date_to_str = request.query_params.get("date_to", today_str)
    try:
        filter_date_from = date.fromisoformat(date_from_str)
    except ValueError:
        filter_date_from = date.today()
    try:
        filter_date_to = date.fromisoformat(date_to_str)
    except ValueError:
        filter_date_to = date.today()

    origin = request.query_params.get("origin", "this_terminal")

    order_status = request.query_params.get("status")

    if search:
        # Search mode: search across ALL orders (bypass date/origin filters)
        # This is for finding orders by number/customer when customer walks in
        orders = Order.objects.filter(
            Q(order_number__icontains=search)
            | Q(user__first_name__icontains=search)
            | Q(user__last_name__icontains=search)
            | Q(user__email__icontains=search)
            | Q(user__profile__phone__icontains=search)
        ).order_by("-created_at")
        # Status filter applies in search mode too
        if order_status:
            if order_status == "refunded":
                orders = orders.filter(
                    Q(status="refunded") | Q(payment_status="partially_refunded")
                )
            else:
                orders = orders.filter(status=order_status)

    elif order_status in ("refunded", "cancelled"):
        # Refunded/Voided tabs: filter by REFUND date and terminal, not order date
        from django.db.models import Max

        from orders.models import Refund

        # Build refund queryset scoped to date range
        refund_qs = Refund.objects.filter(
            status="completed",
            processed_at__date__gte=filter_date_from,
            processed_at__date__lte=filter_date_to,
        )

        # Origin filter: which terminal processed the refund
        if origin == "this_terminal":
            refund_qs = refund_qs.filter(pos_terminal=terminal)
        elif origin == "all_pos":
            refund_qs = refund_qs.filter(pos_terminal__isnull=False)
        # else 'all': no terminal filter

        # Cashier filter: who processed the refund
        cashier_id = request.query_params.get("cashier_id")
        if cashier_id:
            refund_qs = refund_qs.filter(processed_by_id=cashier_id)

        # Get order IDs from matching refunds
        refund_order_ids = refund_qs.values_list("order_id", flat=True)

        # Filter orders by status and matching refund IDs
        if order_status == "refunded":
            orders = Order.objects.filter(
                id__in=refund_order_ids,
            ).filter(Q(status="refunded") | Q(payment_status="partially_refunded"))
        else:  # 'cancelled' (voided)
            orders = Order.objects.filter(
                id__in=refund_order_ids,
                status="cancelled",
            )

        # Sort by most recent refund date
        orders = (
            orders.annotate(latest_refund_at=Max("refunds__processed_at"))
            .order_by("-latest_refund_at")
            .distinct()
        )

    else:
        # All / Completed / other tabs: filter by order creation date
        if origin == "this_terminal":
            orders = Order.objects.filter(channel="pos", pos_terminal=terminal)
        elif origin == "all_pos":
            orders = Order.objects.filter(channel="pos")
        else:  # 'all' - include web orders for return scenarios
            orders = Order.objects.all()

        # Apply date range on order creation date
        orders = orders.filter(
            created_at__date__gte=filter_date_from,
            created_at__date__lte=filter_date_to,
        ).order_by("-created_at")

        # Customer filter
        customer_id = request.query_params.get("customer_id")
        if customer_id:
            orders = orders.filter(user_id=customer_id)

        # Cashier filter
        cashier_id = request.query_params.get("cashier_id")
        if cashier_id:
            orders = orders.filter(cashier_id=cashier_id)

        # Status filter for completed/other
        if order_status:
            orders = orders.filter(status=order_status)

    # Pagination
    page = int(request.query_params.get("page", 1))
    page_size = min(int(request.query_params.get("page_size", 20)), 100)
    start = (page - 1) * page_size
    end = start + page_size

    total = orders.count()

    # Prefetch for performance - primary_image is a property that uses images relation
    from catalog.models import ProductImage
    from orders.models import OrderItem

    orders_page = orders.prefetch_related(
        Prefetch(
            "items",
            queryset=OrderItem.objects.select_related("product").prefetch_related(
                Prefetch(
                    "product__images",
                    queryset=ProductImage.objects.select_related("media_asset").order_by(
                        "-is_primary", "position"
                    ),
                )
            ),
        ),
        "pos_payments",
    ).select_related("user", "cashier", "pos_terminal")[start:end]

    results = []
    for o in orders_page:
        # Get payment methods
        payment_methods = []
        for p in list(o.pos_payments.all())[:3]:
            method_info = {"method": p.method, "display": p.get_method_display()}
            if p.card_last_four:
                method_info["last_four"] = p.card_last_four
            payment_methods.append(method_info)

        results.append(
            {
                "id": o.id,
                "order_number": o.order_number,
                "status": o.status,
                "payment_status": o.payment_status,
                "channel": o.channel,
                "total": str(o.total_amount.amount),
                "currency": str(o.total_amount.currency),
                "item_count": o.total_item_quantity,
                "customer_name": o.user.get_full_name() if o.user else None,
                "customer_email": o.user.email if o.user else None,
                "cashier_name": o.cashier.get_full_name() if o.cashier else None,
                "terminal_name": o.pos_terminal.name if o.pos_terminal else None,
                "payment_methods": payment_methods,
                "item_thumbnails": _get_order_thumbnails(o, request, limit=4),
                "created_at": o.created_at.isoformat(),
            }
        )

    return Response(
        {
            "success": True,
            "results": results,
            "count": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
            "date_from": str(filter_date_from),
            "date_to": str(filter_date_to),
            "origin": origin,
        }
    )


@extend_schema(
    summary=_("Get order details"),
    description=_(
        "Returns full order details including items and payment breakdown. "
        "Supports both POS and web orders (for return scenarios). "
        "Requires staff authentication and valid POS license."
    ),
    responses={
        200: POSOrderSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        404: OpenApiResponse(description=ORDER_NOT_FOUND),
    },
    tags=["POS - Orders"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def order_detail(request, order_id):
    """Get full order details (POS or web orders for return scenarios)."""
    from orders.models import Order

    try:
        order = (
            Order.objects.prefetch_related(
                "items",
                "pos_payments",
                "refunds",
                "refunds__processed_by",
            )
            .select_related(
                "user",
                "cashier",
                "pos_terminal",
            )
            .get(id=order_id)
        )
    except Order.DoesNotExist:
        return Response(
            {"success": False, "error": {"code": "NOT_FOUND", "message": "Order not found."}},
            status=status.HTTP_404_NOT_FOUND,
        )

    return Response({"success": True, "order": _serialize_order(order)})


@extend_schema(
    summary=_("Get receipt data for printing"),
    description=_(
        "Returns receipt-formatted data for a POS order including store info, "
        "items, payments, and footer text. Designed for ESC/POS thermal printers. "
        "Requires staff authentication and valid POS license."
    ),
    responses={
        200: POSReceiptSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        404: OpenApiResponse(description=ORDER_NOT_FOUND),
    },
    tags=["POS - Orders"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def order_receipt(request, order_id):
    """Get receipt data for printing."""
    from core.models import SiteSettings
    from orders.models import Order

    try:
        order = (
            Order.objects.prefetch_related(
                "items",
                "pos_payments",
            )
            .select_related(
                "user",
                "cashier",
                "pos_terminal",
            )
            .get(id=order_id, channel="pos")
        )
    except Order.DoesNotExist:
        return Response(
            {"success": False, "error": {"code": "NOT_FOUND", "message": "Order not found."}},
            status=status.HTTP_404_NOT_FOUND,
        )

    settings = SiteSettings.objects.first()

    # Build store info
    store_name = settings.site_name if settings else "Store"
    store_address_parts = []
    if settings:
        for part in [
            getattr(settings, "address_line_1", ""),
            getattr(settings, "city", ""),
            getattr(settings, "state_province", ""),
            getattr(settings, "postal_code", ""),
            getattr(settings, "country", ""),
        ]:
            if part:
                store_address_parts.append(str(part))
    store_address = ", ".join(store_address_parts)
    store_phone = str(getattr(settings, "phone_number", "")) if settings else ""

    # Items
    items = []
    for item in order.items.all():
        items.append(
            {
                "id": item.id,
                "product_name": item.product_name,
                "variant_name": item.variant_name,
                "sku": item.sku,
                "quantity": item.quantity,
                "unit_price": str(item.unit_price.amount),
                "line_total": str(item.total_price.amount),
            }
        )

    # Payments
    payments = []
    total_change = Decimal("0")
    for p in order.pos_payments.all():
        change = Decimal("0")
        if p.change_given:
            change = (
                p.change_given.amount
                if hasattr(p.change_given, "amount")
                else Decimal(str(p.change_given))
            )
            total_change += change

        # Handle both MoneyField (.amount attr) and plain DecimalField values
        amount_val = p.amount.amount if hasattr(p.amount, "amount") else p.amount
        tendered_val = None
        if p.amount_tendered:
            tendered_val = (
                p.amount_tendered.amount
                if hasattr(p.amount_tendered, "amount")
                else p.amount_tendered
            )

        payments.append(
            {
                "method": p.method,
                "method_display": p.get_method_display(),
                "amount": str(amount_val),
                "amount_tendered": str(tendered_val) if tendered_val is not None else None,
                "change_given": str(change) if change else None,
                "card_last_four": p.card_last_four or "",
            }
        )

    # Get receipt template for the terminal's warehouse
    template_data = None
    from pos_app.models import ReceiptTemplate

    warehouse = order.pos_terminal.warehouse if order.pos_terminal else None
    template = None
    if warehouse:
        try:
            template = ReceiptTemplate.objects.select_related("logo").get(warehouse=warehouse)
        except ReceiptTemplate.DoesNotExist:
            pass
    if not template:
        try:
            template = ReceiptTemplate.objects.select_related("logo").get(warehouse__isnull=True)
        except ReceiptTemplate.DoesNotExist:
            pass

    if template:
        logo_url = ""
        if template.logo and template.logo.file:
            logo_url = request.build_absolute_uri(template.logo.file.url)
        template_data = {
            "paper_width": template.paper_width,
            "logo_url": logo_url,
            "header_text": template.get_effective_header(),
            "show_store_address": template.show_store_address,
            "address": template.get_effective_address(),
            "show_store_phone": template.show_store_phone,
            "phone": template.get_effective_phone(),
            "show_store_email": template.show_store_email,
            "email": template.get_effective_email(),
            "tax_id_label": template.tax_id_label,
            "tax_id_number": template.tax_id_number,
            "business_registration": template.business_registration,
            "show_sku": template.show_sku,
            "show_cashier": template.show_cashier,
            "show_terminal_name": template.show_terminal_name,
            "footer_text": template.footer_text,
            "return_policy": template.return_policy,
            "qr_enabled": template.qr_enabled,
            "qr_url": template.qr_url,
            "qr_label": template.qr_label,
            "show_powered_by": template.show_powered_by,
        }

    receipt = {
        "order_number": order.order_number,
        "store_name": template.get_effective_header() if template else store_name,
        "store_address": template.get_effective_address() if template else store_address,
        "store_phone": template.get_effective_phone() if template else store_phone,
        "terminal_name": order.pos_terminal.name if order.pos_terminal else "",
        "cashier_name": order.cashier.get_full_name() if order.cashier else "",
        "items": items,
        "subtotal": str(order.subtotal.amount),
        "tax_amount": str(order.tax_amount.amount),
        "discount_amount": str(order.discount_amount.amount),
        "total": str(order.total_amount.amount),
        "currency": str(order.total_amount.currency),
        "payments": payments,
        "change_given": str(total_change) if total_change else None,
        "date": order.created_at.isoformat(),
        "footer_text": template.footer_text if template else "Thank you for your purchase!",
        "template": template_data,
    }

    return Response({"success": True, "receipt": receipt})


import logging

logger = logging.getLogger(__name__)


def _process_provider_refund_pos(order, refund_amount, reason, currency):
    """Trigger a provider refund for a POS terminal_card payment. Returns error string or None."""
    from payment_providers.models import PaymentTransaction
    from payment_providers.services.refund_service import RefundService

    # Find the terminal_card payment with a provider link
    pos_payment = (
        order.pos_payments.filter(
            method="terminal_card",
        )
        .exclude(provider_payment_id="")
        .first()
    )

    if not pos_payment:
        # No provider-linked payment — record only, no provider call
        return None

    # Find the matching PaymentTransaction
    try:
        original_txn = PaymentTransaction.objects.get(
            provider_transaction_id=pos_payment.provider_payment_id,
            transaction_type="charge",
        )
    except PaymentTransaction.DoesNotExist:
        logger.warning(
            f"No PaymentTransaction found for provider_payment_id={pos_payment.provider_payment_id}"
        )
        # Payment was made on external terminal — record only
        return None

    success, refund_txn, message = RefundService.create_refund(
        original_transaction=original_txn,
        refund_amount=refund_amount,
        reason=reason,
    )
    if not success:
        return message
    return None


def _process_provider_refund_web(order, refund_method, refund_amount, reason, currency):
    """Trigger a provider refund for a web payment transaction. Returns error string or None."""
    from payment_providers.models import PaymentTransaction
    from payment_providers.services.refund_service import RefundService

    # Extract provider slug from refund_method (e.g. "provider_airwallex" → "airwallex")
    provider_slug = refund_method.replace("provider_", "", 1)

    # Find the charge transaction for this order + provider
    try:
        original_txn = PaymentTransaction.objects.select_related("provider_account__component").get(
            order=order,
            transaction_type="charge",
            status="succeeded",
            provider_account__component__slug=provider_slug,
        )
    except PaymentTransaction.DoesNotExist:
        return f"No payment transaction found for provider '{provider_slug}'."
    except PaymentTransaction.MultipleObjectsReturned:
        # Multiple charges — use the most recent
        original_txn = (
            PaymentTransaction.objects.select_related("provider_account__component")
            .filter(
                order=order,
                transaction_type="charge",
                status="succeeded",
                provider_account__component__slug=provider_slug,
            )
            .order_by("-created_at")
            .first()
        )

    success, refund_txn, message = RefundService.create_refund(
        original_transaction=original_txn,
        refund_amount=refund_amount,
        reason=reason,
    )
    if not success:
        return message
    return None


@extend_schema(
    summary=_("Process order refund"),
    description=_(
        "Process a full or partial refund for a POS order. For partial refunds, "
        "specify the items and quantities to refund. Creates a Refund record and "
        "updates the order and shift totals. "
        "Requires an open shift on the terminal. "
        "Requires staff authentication and valid POS license."
    ),
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "refund_type": {
                    "type": "string",
                    "enum": ["full", "partial"],
                    "description": "Full or partial refund",
                },
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "order_item_id": {"type": "integer"},
                            "quantity": {"type": "integer"},
                        },
                        "required": ["order_item_id", "quantity"],
                    },
                    "description": "Items to refund (for partial refunds)",
                },
                "reason": {
                    "type": "string",
                    "enum": [
                        "customer_request",
                        "damaged",
                        "wrong_item",
                        "defective",
                        "not_as_described",
                        "other",
                    ],
                    "description": "Reason for the refund",
                },
                "notes": {"type": "string", "description": "Staff notes"},
            },
            "required": ["refund_type", "reason"],
        },
    },
    responses={
        200: OpenApiResponse(description=_("Refund processed successfully")),
        400: OpenApiResponse(description=_("Invalid refund request or order already refunded")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        404: OpenApiResponse(description=ORDER_NOT_FOUND),
        409: OpenApiResponse(description=NO_OPEN_SHIFT),
    },
    tags=["POS - Orders"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def refund_order(request, order_id):
    """Process a refund for a POS order."""
    from djmoney.money import Money

    from orders.models import Order, Refund

    # Check POS refund permission
    err = check_pos_permission(request, "pos_refund")
    if err:
        return err

    terminal, err = get_terminal(request)
    if err:
        return err
    shift, err = get_open_shift(request, terminal)
    if err:
        return err

    try:
        order = Order.objects.prefetch_related("items").get(id=order_id)
    except Order.DoesNotExist:
        return Response(
            {"success": False, "error": {"code": "NOT_FOUND", "message": "Order not found."}},
            status=status.HTTP_404_NOT_FOUND,
        )

    if order.status == "refunded":
        return Response(
            {
                "success": False,
                "error": {
                    "code": "ALREADY_REFUNDED",
                    "message": "Order is already fully refunded.",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    refund_type = request.data.get("refund_type", "full")
    reason = request.data.get("reason", "customer_request")
    notes = request.data.get("notes", "")
    refund_items = request.data.get("items", [])
    refund_method = request.data.get("refund_method", "")
    refund_method_display = request.data.get("refund_method_display", "")
    return_to_stock = request.data.get("return_to_stock", False)

    currency = str(order.total_amount.currency)

    # Calculate refund amount before the atomic block (for item validation)
    if refund_type == "full":
        refund_amount = order.total_amount.amount
        items_json = []
    else:
        refund_amount = Decimal("0")
        items_json = []
        for ri in refund_items:
            try:
                order_item = order.items.get(id=ri["order_item_id"])
            except Exception:
                return Response(
                    {
                        "success": False,
                        "error": {
                            "code": "ITEM_NOT_FOUND",
                            "message": f"Order item {ri.get('order_item_id')} not found.",
                        },
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            qty = min(ri["quantity"], order_item.quantity)
            item_refund = order_item.unit_price.amount * qty
            refund_amount += item_refund
            items_json.append(
                {
                    "order_item_id": order_item.id,
                    "quantity": qty,
                    "amount": str(item_refund),
                }
            )

    # Trigger provider refund first (before committing DB changes)
    # If provider refund fails, we abort without modifying order state
    provider_refund_error = None
    if refund_method == "terminal_card":
        provider_refund_error = _process_provider_refund_pos(order, refund_amount, reason, currency)
    elif refund_method.startswith("provider_"):
        provider_refund_error = _process_provider_refund_web(
            order, refund_method, refund_amount, reason, currency
        )

    if provider_refund_error:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "PROVIDER_REFUND_FAILED",
                    "message": provider_refund_error,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    with transaction.atomic():
        # Update order status
        if refund_type == "full":
            order.status = "refunded"
            order.payment_status = "refunded"
            order.amount_refunded = Money(refund_amount, currency)
        else:
            order.status = (
                "refunded" if refund_amount >= order.total_amount.amount else "processing"
            )
            order.payment_status = (
                "refunded" if refund_amount >= order.total_amount.amount else "partially_refunded"
            )
            prev_refunded = (
                order.amount_refunded.amount
                if hasattr(order.amount_refunded, "amount")
                else Decimal("0")
            )
            order.amount_refunded = Money(prev_refunded + refund_amount, currency)
        order.save(update_fields=["status", "payment_status", "amount_refunded"])

        # Create Refund record
        refund = Refund.objects.create(
            order=order,
            processed_by=request.user,
            pos_terminal=terminal,
            refund_type=refund_type,
            reason=reason,
            status="completed",
            refund_method=refund_method,
            refund_method_display=refund_method_display,
            total_amount=Money(refund_amount, currency),
            items_json=items_json,
            staff_notes=notes,
            processed_at=timezone.now(),
        )
        refund.compute_base_amounts()
        refund.save(
            update_fields=[
                "total_amount_base",
                "shipping_refund_amount_base",
                "tax_refund_amount_base",
            ]
        )

        # Update shift totals
        shift.total_refunds = (shift.total_refunds or Decimal("0")) + refund_amount
        shift.save(update_fields=["total_refunds"])

        # Return items to stock if requested
        if return_to_stock and terminal.warehouse_id:
            _return_refund_stock(
                order,
                refund_type,
                refund_items,
                items_json,
                terminal.warehouse_id,
                request.user,
            )

    # Re-fetch order with prefetches for serialization
    order = (
        Order.objects.prefetch_related(
            "items",
            "pos_payments",
            "refunds",
            "refunds__processed_by",
        )
        .select_related("user", "cashier", "pos_terminal")
        .get(id=order_id)
    )

    return Response(
        {
            "success": True,
            "message": f"Refund of {refund_amount} processed.",
            "refund_amount": str(refund_amount),
            "order": _serialize_order(order),
        }
    )


@extend_schema(
    summary=_("Void a POS order"),
    description=_(
        "Cancel a POS order from the current shift. Only orders placed during "
        "the current open shift can be voided. This creates a full refund and "
        "reverses all payment and inventory changes. "
        "Requires an open shift on the terminal. "
        "Requires staff authentication and valid POS license."
    ),
    responses={
        200: OpenApiResponse(description=_("Order voided successfully")),
        400: OpenApiResponse(description=_("Order cannot be voided (not from current shift)")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        404: OpenApiResponse(description=ORDER_NOT_FOUND),
        409: OpenApiResponse(description=NO_OPEN_SHIFT),
    },
    tags=["POS - Orders"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def void_order(request, order_id):
    """Void a POS order from the current shift."""
    from djmoney.money import Money

    from orders.models import Order, Refund

    # Check POS void permission
    err = check_pos_permission(request, "pos_void")
    if err:
        return err

    terminal, err = get_terminal(request)
    if err:
        return err
    shift, err = get_open_shift(request, terminal)
    if err:
        return err

    try:
        order = Order.objects.get(id=order_id, channel="pos")
    except Order.DoesNotExist:
        return Response(
            {"success": False, "error": {"code": "NOT_FOUND", "message": "Order not found."}},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Only allow voiding orders from the current shift
    order_payments = order.pos_payments.filter(shift=shift)
    if not order_payments.exists():
        return Response(
            {
                "success": False,
                "error": {
                    "code": "NOT_CURRENT_SHIFT",
                    "message": "Only orders from the current shift can be voided.",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if order.status == "cancelled":
        return Response(
            {
                "success": False,
                "error": {"code": "ALREADY_VOIDED", "message": "Order is already voided."},
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    currency = str(order.total_amount.currency)
    refund_amount = order.total_amount.amount

    with transaction.atomic():
        # Update order
        order.status = "cancelled"
        order.payment_status = "refunded"
        order.amount_refunded = Money(refund_amount, currency)
        order.save(update_fields=["status", "payment_status", "amount_refunded"])

        # Create void refund
        void_refund = Refund.objects.create(
            order=order,
            processed_by=request.user,
            pos_terminal=terminal,
            refund_type="full",
            reason="other",
            status="completed",
            total_amount=Money(refund_amount, currency),
            staff_notes="Voided at POS",
            processed_at=timezone.now(),
        )
        void_refund.compute_base_amounts()
        void_refund.save(
            update_fields=[
                "total_amount_base",
                "shipping_refund_amount_base",
                "tax_refund_amount_base",
            ]
        )

        # Reverse shift totals
        shift.total_sales = max(Decimal("0"), (shift.total_sales or Decimal("0")) - refund_amount)
        shift.total_transactions = max(0, (shift.total_transactions or 0) - 1)
        shift.total_refunds = (shift.total_refunds or Decimal("0")) + refund_amount
        shift.save(update_fields=["total_sales", "total_transactions", "total_refunds"])

        # Return stock
        _return_pos_stock(order, terminal.warehouse_id)

    return Response(
        {
            "success": True,
            "message": "Order voided.",
            "order": _serialize_order(order),
        }
    )


def _return_pos_stock(order, warehouse_id):
    """Return stock to warehouse for voided/refunded orders.

    Uses atomic F() update to prevent lost updates under concurrency
    (two simultaneous refunds could otherwise both read the same on_hand
    and the last .save() would win, losing one increment).
    """
    from django.db.models import F

    from catalog.models import StockItem

    for item in order.items.all():
        if not item.product.track_inventory:
            continue
        StockItem.objects.filter(
            product=item.product,
            variant=item.variant,
            warehouse_id=warehouse_id,
        ).update(on_hand=F("on_hand") + item.quantity)


def _return_refund_stock(order, refund_type, refund_items, items_json, warehouse_id, user):
    """Return refunded items to stock with audit trail.

    Uses .filter().update() to bypass StockItem post_save signal,
    and creates StockMovement records for each item returned.
    """
    from catalog.models import StockItem, StockMovement

    # Determine which items and quantities to return
    if refund_type == "full":
        items_to_return = [
            (item.product, item.variant, item.quantity)
            for item in order.items.all()
            if item.product.track_inventory
        ]
    else:
        # Partial refund: use items_json (already validated)
        items_to_return = []
        for ij in items_json:
            try:
                order_item = order.items.get(id=ij["order_item_id"])
            except Exception:
                continue
            if order_item.product.track_inventory:
                items_to_return.append((order_item.product, order_item.variant, ij["quantity"]))

    for product, variant, qty in items_to_return:
        try:
            stock = StockItem.objects.get(
                product=product,
                variant=variant,
                warehouse_id=warehouse_id,
            )
        except StockItem.DoesNotExist:
            continue

        old_on_hand = stock.on_hand
        new_on_hand = old_on_hand + qty

        # Use .filter().update() to bypass post_save signal
        StockItem.objects.filter(pk=stock.pk).update(on_hand=new_on_hand)

        StockMovement.objects.create(
            stock_item=stock,
            movement_type="return",
            quantity=qty,
            previous_quantity=old_on_hand,
            new_quantity=new_on_hand,
            reason=f"Refund return for order #{order.order_number}",
            order=order,
            user=user,
        )


@extend_schema(
    summary=_("List POS cashiers"),
    description=_(
        "Returns list of staff members who have processed POS orders. "
        "Used to populate the cashier filter dropdown. "
        "Requires staff authentication and valid POS license."
    ),
    responses={
        200: OpenApiResponse(
            description=_("List of cashiers"),
            examples=[
                OpenApiExample(
                    "Success",
                    value={
                        "success": True,
                        "cashiers": [
                            {"id": 1, "first_name": "Jane", "last_name": "Doe"},
                            {"id": 2, "first_name": "John", "last_name": "Smith"},
                        ],
                    },
                )
            ],
        ),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Orders"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def cashier_list(request):
    """List cashiers who have processed POS orders."""
    from django.contrib.auth import get_user_model

    User = get_user_model()

    terminal, err = get_terminal(request)
    if err:
        return err

    cashiers = (
        User.objects.filter(pos_orders__isnull=False)
        .distinct()
        .values("id", "first_name", "last_name")
    )

    return Response({"success": True, "cashiers": list(cashiers)})
