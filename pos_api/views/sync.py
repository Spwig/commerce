"""
POS Sync API views.

Data synchronization endpoints for offline POS support.
Includes product delta sync, customer sync, offline transaction upload,
and sync status.
All endpoints require staff authentication and a valid POS license.
"""

import logging
from decimal import Decimal

from django.db import transaction
from django.db.models import Prefetch
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.translation import gettext_lazy as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from admin_api.authentication import MobileTokenAuthentication
from core.api.api_descriptions import AUTH_REQUIRED, INVALID_REQUEST, POS_LICENSE_REQUIRED
from pos_api.permissions import IsStaffUser

logger = logging.getLogger(__name__)

# POS API version info - increment data_schema_version when IndexedDB structure changes
POS_API_VERSION = "1.0.0"
POS_DATA_SCHEMA_VERSION = 1

from pos_api.serializers.product import POSProductListSerializer
from pos_api.serializers.sync import (
    POSOfflineStockAdjustmentUploadSerializer,
    POSOfflineUploadSerializer,
    POSOrderSyncSerializer,
    POSSyncStatusSerializer,
)
from pos_api.views.catalog import _get_terminal_context, _serialize_product


def _get_pos_order_language():
    """Get language for POS orders (uses site default since POS is merchant-facing)."""
    try:
        from core.models import SiteSettings

        return SiteSettings.get_settings().default_language or "en"
    except Exception:
        return "en"


@extend_schema(
    summary=_("Sync products since timestamp"),
    description=_(
        "Returns products that have been created or updated since the given timestamp. "
        "Used for incremental product sync to the POS terminal's local database. "
        "Returns a sync_token for the next sync request. "
        "Requires staff authentication and valid POS license."
    ),
    parameters=[
        OpenApiParameter(
            "since",
            OpenApiTypes.DATETIME,
            description=_("ISO timestamp to fetch changes since. Omit for full sync."),
        ),
        OpenApiParameter("page", OpenApiTypes.INT, description=_("Page number (default: 1)")),
        OpenApiParameter(
            "page_size", OpenApiTypes.INT, description=_("Items per page (default: 100, max: 200)")
        ),
    ],
    responses={
        200: POSProductListSerializer(many=True),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Sync"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def product_delta_sync(request):
    """Sync products that changed since a given timestamp."""
    from catalog.models import Product, ProductImage, ProductVariant

    warehouse_id, currency = _get_terminal_context(request)

    since_str = request.query_params.get("since")
    since = None
    if since_str:
        since = parse_datetime(since_str)

    products = (
        Product.objects.filter(
            status="published",
            sales_channel__in=["all", "pos_only"],
            is_deleted=False,  # Exclude soft-deleted products from POS sync
        )
        .select_related("category", "brand")
        .prefetch_related(
            Prefetch(
                "images",
                queryset=ProductImage.objects.select_related("media_asset").order_by(
                    "-is_primary", "position"
                ),
            ),
            Prefetch(
                "variants",
                queryset=ProductVariant.objects.filter(is_active=True).prefetch_related(
                    "selected_attributes__attribute"
                ),
            ),
        )
    )

    if since:
        products = products.filter(updated_at__gte=since)

    products = products.order_by("updated_at")

    # Pagination
    page = int(request.query_params.get("page", 1))
    page_size = min(int(request.query_params.get("page_size", 100)), 200)
    start = (page - 1) * page_size
    end = start + page_size

    total = products.count()
    products_page = products[start:end]

    results = [_serialize_product(p, warehouse_id, currency) for p in products_page]

    return Response(
        {
            "success": True,
            "results": results,
            "count": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
            "sync_token": timezone.now().isoformat(),
        }
    )


@extend_schema(
    summary=_("Sync customers since timestamp"),
    description=_(
        "Returns customers that have been created or have placed orders since "
        "the given timestamp. Used for offline customer lookup. "
        "Requires staff authentication and valid POS license."
    ),
    parameters=[
        OpenApiParameter(
            "since",
            OpenApiTypes.DATETIME,
            description=_("ISO timestamp to fetch changes since. Omit for full sync."),
        ),
        OpenApiParameter("page", OpenApiTypes.INT, description=_("Page number (default: 1)")),
        OpenApiParameter(
            "page_size", OpenApiTypes.INT, description=_("Items per page (default: 100, max: 200)")
        ),
    ],
    responses={
        200: OpenApiResponse(description=_("Customer sync data")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Sync"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def customer_sync(request):
    """Sync customer data since a given timestamp."""
    from django.contrib.auth import get_user_model

    User = get_user_model()

    since_str = request.query_params.get("since")
    since = None
    if since_str:
        since = parse_datetime(since_str)

    users = User.objects.filter(is_active=True, is_staff=False)
    if since:
        users = users.filter(date_joined__gte=since)

    users = users.order_by("date_joined")

    # Pagination
    page = int(request.query_params.get("page", 1))
    page_size = min(int(request.query_params.get("page_size", 100)), 200)
    start = (page - 1) * page_size
    end = start + page_size

    total = users.count()
    users_page = users[start:end]

    results = []
    for u in users_page:
        results.append(
            {
                "id": u.id,
                "email": u.email or "",
                "first_name": u.first_name,
                "last_name": u.last_name,
                "full_name": u.get_full_name(),
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
            "sync_token": timezone.now().isoformat(),
        }
    )


@extend_schema(
    summary=_("Upload offline transactions"),
    description=_(
        "Batch upload transactions that were processed while the terminal was "
        "offline. Each transaction creates an Order with items and payments. "
        "Uses local_id for idempotency -- duplicate uploads are detected and skipped. "
        "Requires staff authentication and valid POS license."
    ),
    request=POSOfflineUploadSerializer,
    responses={
        200: OpenApiResponse(description=_("Upload results with success/failure per transaction")),
        400: OpenApiResponse(description=INVALID_REQUEST),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Sync"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def upload_offline_transactions(request):
    """Upload offline transactions for processing."""
    from djmoney.money import Money

    from catalog.models import Product, ProductVariant
    from orders.models import Order, OrderItem
    from pos_app.models import POSPayment, POSShift, POSTerminal

    serializer = POSOfflineUploadSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    transactions = serializer.validated_data["transactions"]

    processed = 0
    failed = 0
    errors = []

    for txn in transactions:
        local_id = txn["local_id"]

        # Idempotency check
        if Order.objects.filter(external_id=local_id, channel="pos").exists():
            processed += 1
            continue

        try:
            with transaction.atomic():
                # Resolve terminal and its currency
                terminal = POSTerminal.objects.get(uuid=txn["terminal_uuid"], is_active=True)
                currency = terminal.effective_currency

                # Find or create shift context
                shift = POSShift.objects.filter(
                    terminal=terminal,
                    cashier_id=txn["cashier_id"],
                    ended_at__isnull=True,
                ).first()

                # Calculate totals
                order_total = Decimal("0")
                order_items_data = []
                for item_data in txn["items"]:
                    unit_price = Decimal(str(item_data["unit_price"]))
                    line_total = unit_price * item_data["quantity"]
                    order_total += line_total

                    # Use all_objects to allow orders for soft-deleted products (offline txns)
                    product = Product.all_objects.get(id=item_data["product_id"])
                    variant = None
                    if item_data.get("variant_id"):
                        variant = ProductVariant.objects.get(id=item_data["variant_id"])

                    order_items_data.append(
                        {
                            "product": product,
                            "variant": variant,
                            "product_name": str(product.name),
                            "variant_name": variant.name if variant else "",
                            "sku": (variant.sku if variant and variant.sku else product.sku) or "",
                            "quantity": item_data["quantity"],
                            "unit_price": unit_price,
                            "total_price": line_total,
                        }
                    )

                # Get user — validate cashier_id matches authenticated user
                from django.contrib.auth import get_user_model

                User = get_user_model()
                cashier_id = txn["cashier_id"]
                if cashier_id != request.user.id:
                    logger.warning(
                        f"Offline sync cashier_id mismatch: payload has {cashier_id}, "
                        f"authenticated user is {request.user.id}"
                    )
                cashier = User.objects.get(id=cashier_id)
                order_user = cashier
                if txn.get("customer_id"):
                    try:
                        order_user = User.objects.get(id=txn["customer_id"])
                    except User.DoesNotExist:
                        pass

                # Create order
                from core.license import is_sandbox_mode

                order = Order(
                    user=order_user,
                    email=order_user.email or cashier.email,
                    external_id=local_id,
                    status="processing",
                    channel="pos",
                    pos_terminal=terminal,
                    cashier=cashier,
                    subtotal=Money(order_total, currency),
                    tax_amount=Money(0, currency),
                    shipping_cost=Money(0, currency),
                    discount_amount=Money(0, currency),
                    total_amount=Money(order_total, currency),
                    payment_status="paid",
                    paid_at=txn.get("created_at", timezone.now()),
                    amount_paid=Money(order_total, currency),
                    shipping_name=order_user.get_full_name() or "Walk-in Customer",
                    shipping_address1="In-store purchase (offline)",
                    shipping_city="",
                    shipping_state="",
                    shipping_postal_code="",
                    shipping_country="",
                    is_test_order=is_sandbox_mode(),
                    language=_get_pos_order_language(),
                )
                order.save()

                # Create order items
                for oi_data in order_items_data:
                    OrderItem.objects.create(
                        order=order,
                        product=oi_data["product"],
                        variant=oi_data["variant"],
                        product_name=oi_data["product_name"],
                        variant_name=oi_data["variant_name"],
                        sku=oi_data["sku"],
                        quantity=oi_data["quantity"],
                        unit_price=Money(oi_data["unit_price"], currency),
                        total_price=Money(oi_data["total_price"], currency),
                    )

                # Create payments
                for pmt in txn["payments"]:
                    pmt_kwargs = {
                        "order": order,
                        "shift": shift,
                        "method": pmt["method"],
                        "amount": Decimal(str(pmt["amount"])),
                    }
                    if pmt["method"] == "cash" and pmt.get("amount_tendered"):
                        pmt_kwargs["amount_tendered"] = Decimal(str(pmt["amount_tendered"]))
                    if pmt.get("card_last_four"):
                        pmt_kwargs["card_last_four"] = pmt["card_last_four"]
                    if pmt.get("card_reference"):
                        pmt_kwargs["card_reference"] = pmt["card_reference"]
                    if pmt.get("gift_card_code"):
                        pmt_kwargs["gift_card_code"] = pmt["gift_card_code"]

                    POSPayment.objects.create(**pmt_kwargs)

                # Update shift totals if shift exists
                if shift:
                    shift.total_sales = (shift.total_sales or Decimal("0")) + order_total
                    shift.total_transactions = (shift.total_transactions or 0) + 1
                    shift.save(update_fields=["total_sales", "total_transactions"])

                processed += 1

        except Exception as e:
            failed += 1
            errors.append({"local_id": local_id, "error": str(e)})

    return Response(
        {
            "success": True,
            "processed": processed,
            "failed": failed,
            "errors": errors,
        }
    )


@extend_schema(
    summary=_("Get sync status"),
    description=_(
        "Returns the current server time and database counts for sync planning. "
        "Requires staff authentication and valid POS license."
    ),
    responses={
        200: POSSyncStatusSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Sync"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def sync_status(request):
    """Get sync status with server time and counts."""
    from django.contrib.auth import get_user_model

    from catalog.models import Product

    User = get_user_model()

    total_products = Product.objects.filter(
        status="published",
        sales_channel__in=["all", "pos_only"],
        is_deleted=False,  # Exclude soft-deleted products from POS sync
    ).count()

    total_customers = User.objects.filter(
        is_active=True,
        is_staff=False,
    ).count()

    return Response(
        {
            "success": True,
            "server_time": timezone.now().isoformat(),
            "total_products": total_products,
            "total_customers": total_customers,
        }
    )


@extend_schema(
    summary=_("Get sync version info"),
    description=_(
        "Returns API version and data schema version for client compatibility checks. "
        "Clients should clear and resync when schema version increases."
    ),
    responses={
        200: OpenApiResponse(description=_("Version information")),
    },
    tags=["POS - Sync"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def sync_version(request):
    """Return version info for sync compatibility."""
    return Response(
        {
            "success": True,
            "api_version": POS_API_VERSION,
            "data_schema_version": POS_DATA_SCHEMA_VERSION,
            "server_time": timezone.now().isoformat(),
        }
    )


@extend_schema(
    summary=_("Upload offline stock adjustments"),
    description=_(
        "Batch upload stock adjustments that were queued while the terminal was "
        "offline. Each adjustment uses an idempotency key to prevent duplicates. "
        "Requires staff authentication, valid POS license, and stock adjustment permission."
    ),
    request=POSOfflineStockAdjustmentUploadSerializer,
    responses={
        200: OpenApiResponse(description=_("Upload results with success/failure per adjustment")),
        400: OpenApiResponse(description=INVALID_REQUEST),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=_("POS license or permission required")),
    },
    tags=["POS - Sync"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def upload_offline_stock_adjustments(request):
    """Upload offline stock adjustments for processing."""
    from django.db.models import F

    from catalog.models import Product, ProductVariant, StockItem, StockMovement
    from pos_api.permissions import check_pos_permission
    from pos_app.models import POSTerminal

    err = check_pos_permission(request, "pos_stock_adjustment")
    if err:
        return err

    serializer = POSOfflineStockAdjustmentUploadSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    adjustments = serializer.validated_data["adjustments"]

    # Resolve terminal warehouse
    terminal_uuid = request.headers.get("X-Terminal-UUID")
    warehouse_id = None
    if terminal_uuid:
        try:
            terminal = POSTerminal.objects.select_related("warehouse").get(
                uuid=terminal_uuid, is_active=True
            )
            warehouse_id = terminal.warehouse_id
        except POSTerminal.DoesNotExist:
            pass

    TYPE_MAP = {
        "receive": "adjustment",
        "damage": "damage",
        "recount": "recount",
        "return": "return",
    }

    processed = 0
    skipped = 0
    failed = 0
    errors = []

    for adj in adjustments:
        idem_key = adj["idempotency_key"]

        # Idempotency check
        if StockMovement.objects.filter(reference_key=idem_key).exists():
            skipped += 1
            processed += 1
            continue

        try:
            with transaction.atomic():
                # Use all_objects to allow adjustments for soft-deleted products (offline adjustments)
                product = Product.all_objects.get(id=adj["product_id"])
                variant = None
                if adj.get("variant_id"):
                    variant = ProductVariant.objects.get(id=adj["variant_id"], product=product)

                stock_filter = {"product": product, "variant": variant}
                if warehouse_id:
                    stock_filter["warehouse_id"] = warehouse_id

                stock_item = StockItem.objects.select_for_update().filter(**stock_filter).first()

                adj_type = adj["adjustment_type"]
                qty = adj["quantity"]

                if adj_type == "receive" and not stock_item:
                    from catalog.models import Warehouse

                    wh = (
                        Warehouse.objects.get(id=warehouse_id)
                        if warehouse_id
                        else Warehouse.objects.first()
                    )
                    stock_item = StockItem.objects.create(
                        product=product,
                        variant=variant,
                        warehouse=wh,
                        on_hand=0,
                        allocated=0,
                        low_stock_threshold=5,
                    )

                if not stock_item:
                    raise ValueError(f"No stock item found for product {adj['product_id']}")

                old_on_hand = stock_item.on_hand

                if adj_type in ("receive", "return"):
                    delta = qty
                elif adj_type == "damage":
                    delta = -min(qty, old_on_hand)
                elif adj_type == "recount":
                    delta = qty - old_on_hand
                else:
                    delta = 0

                if delta != 0:
                    StockItem.objects.filter(pk=stock_item.pk).update(on_hand=F("on_hand") + delta)

                StockMovement.objects.create(
                    stock_item=stock_item,
                    movement_type=TYPE_MAP.get(adj_type, "adjustment"),
                    quantity=delta,
                    previous_quantity=old_on_hand,
                    new_quantity=old_on_hand + delta,
                    reason=adj.get("reason", ""),
                    user=request.user,
                    reference_key=idem_key,
                )

                processed += 1

        except Exception as e:
            failed += 1
            errors.append({"idempotency_key": idem_key, "error": str(e)})

    return Response(
        {
            "success": True,
            "processed": processed,
            "skipped": skipped,
            "failed": failed,
            "errors": errors,
        }
    )


def _serialize_sync_order(order, currency):
    """Build a lightweight order dict for offline sync cache."""
    items = []
    for item in order.items.all():
        items.append(
            {
                "id": item.id,
                "product_id": item.product_id,
                "product_name": item.product_name,
                "variant_name": item.variant_name or "",
                "sku": item.sku or "",
                "quantity": item.quantity,
                "unit_price": str(item.unit_price.amount),
                "line_total": str(item.total_price.amount),
            }
        )

    payments = []
    for p in order.pos_payments.all():
        payments.append(
            {
                "method": p.method,
                "method_display": p.get_method_display(),
                "amount": str(p.amount.amount) if hasattr(p.amount, "amount") else str(p.amount),
                "amount_tendered": str(p.amount_tendered.amount)
                if p.amount_tendered and hasattr(p.amount_tendered, "amount")
                else None,
                "change_given": str(p.change_given.amount)
                if p.change_given and hasattr(p.change_given, "amount")
                else None,
                "card_last_four": p.card_last_four or "",
            }
        )

    # For web orders, include web payment info
    if order.channel == "web":
        from payment_providers.models import PaymentTransaction

        txns = PaymentTransaction.objects.filter(
            order=order, transaction_type="charge", status="succeeded"
        ).select_related("provider_account__component")
        for t in txns:
            payments.append(
                {
                    "method": "card",
                    "method_display": t.provider_account.display_name or "Card",
                    "amount": str(t.amount.amount)
                    if hasattr(t.amount, "amount")
                    else str(t.amount),
                    "amount_tendered": None,
                    "change_given": None,
                    "card_last_four": t.payment_method_last4 or "",
                }
            )

    payment_methods = list({p["method_display"] for p in payments})

    return {
        "id": order.id,
        "order_number": order.order_number,
        "status": order.status,
        "channel": order.channel,
        "items": items,
        "payments": payments,
        "subtotal": str(order.subtotal.amount),
        "tax_amount": str(order.tax_amount.amount),
        "discount_amount": str(order.discount_amount.amount),
        "total": str(order.total_amount.amount),
        "currency": currency,
        "customer_name": order.user.get_full_name() if order.user else None,
        "customer_email": order.email or None,
        "cashier_name": order.cashier.get_full_name() if order.cashier else None,
        "terminal_name": order.pos_terminal.name if order.pos_terminal else None,
        "item_count": len(items),
        "payment_methods": payment_methods,
        "created_at": order.created_at.isoformat(),
        "updated_at": order.updated_at.isoformat(),
    }


@extend_schema(
    summary=_("Sync orders for offline cache"),
    description=_(
        "Returns orders for offline caching on the POS terminal. "
        "POS orders are prioritised over web orders up to the terminal's sync limit. "
        "Supports delta sync via the 'since' parameter. "
        "Requires staff authentication and valid POS license."
    ),
    parameters=[
        OpenApiParameter(
            "since",
            OpenApiTypes.DATETIME,
            description=_("ISO timestamp for delta sync. Omit for full sync."),
        ),
        OpenApiParameter("page", OpenApiTypes.INT, description=_("Page number (default: 1)")),
        OpenApiParameter(
            "page_size", OpenApiTypes.INT, description=_("Items per page (default: 100, max: 200)")
        ),
    ],
    responses={
        200: POSOrderSyncSerializer(many=True),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Sync"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def order_sync(request):
    """Sync orders for offline cache with POS-priority ordering."""
    from datetime import timedelta

    from orders.models import Order
    from pos_app.models import POSTerminal

    # Resolve terminal config
    terminal_uuid = request.headers.get("X-Terminal-UUID")
    sync_days = 14
    sync_limit = 500
    if terminal_uuid:
        try:
            terminal = POSTerminal.objects.get(uuid=terminal_uuid, is_active=True)
            sync_days = terminal.order_sync_days
            sync_limit = terminal.order_sync_limit
        except POSTerminal.DoesNotExist:
            pass

    since_str = request.query_params.get("since")
    since = parse_datetime(since_str) if since_str else None
    cutoff = timezone.now() - timedelta(days=sync_days)

    page = int(request.query_params.get("page", 1))
    page_size = min(int(request.query_params.get("page_size", 100)), 200)

    base_qs = (
        Order.objects.filter(
            created_at__gte=cutoff,
            status__in=["processing", "completed", "refunded", "partially_refunded"],
        )
        .select_related(
            "user",
            "cashier",
            "pos_terminal",
        )
        .prefetch_related(
            "items",
            "pos_payments",
        )
    )

    if since:
        # Delta sync: return all changed orders regardless of channel
        orders = base_qs.filter(updated_at__gt=since).order_by("-updated_at")
        total = orders.count()
    else:
        # Full sync: POS orders first, then web orders fill remaining slots
        pos_orders = base_qs.filter(channel="pos").order_by("-created_at")
        pos_count = pos_orders.count()

        remaining = max(0, sync_limit - pos_count)
        web_orders = (
            base_qs.filter(channel="web").order_by("-created_at")[:remaining]
            if remaining > 0
            else Order.objects.none()
        )
        web_orders.count()

        # Build combined ordered ID list for pagination
        pos_ids = list(pos_orders.values_list("id", flat=True))
        web_ids = list(web_orders.values_list("id", flat=True))
        all_ids = pos_ids + web_ids
        total = len(all_ids)

        # Paginate the ID list, then fetch in that order
        start = (page - 1) * page_size
        end = start + page_size
        page_ids = all_ids[start:end]

        # Preserve priority ordering
        id_order = {oid: idx for idx, oid in enumerate(page_ids)}
        orders = list(base_qs.filter(id__in=page_ids))
        orders.sort(key=lambda o: id_order.get(o.id, 0))

        results = [_serialize_sync_order(o, str(o.total_amount.currency)) for o in orders]

        return Response(
            {
                "success": True,
                "results": results,
                "count": total,
                "page": page,
                "page_size": page_size,
                "total_pages": max(1, (total + page_size - 1) // page_size),
                "sync_token": timezone.now().isoformat(),
                "config": {
                    "sync_days": sync_days,
                    "sync_limit": sync_limit,
                },
            }
        )

    # Delta sync pagination
    start = (page - 1) * page_size
    end = start + page_size
    orders_page = orders[start:end]

    results = [_serialize_sync_order(o, str(o.total_amount.currency)) for o in orders_page]

    return Response(
        {
            "success": True,
            "results": results,
            "count": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(1, (total + page_size - 1) // page_size),
            "sync_token": timezone.now().isoformat(),
            "config": {
                "sync_days": sync_days,
                "sync_limit": sync_limit,
            },
        }
    )
