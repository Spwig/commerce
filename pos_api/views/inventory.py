"""
POS Inventory API views.

Stock level queries, stock adjustments, and movement history for the
terminal's warehouse. All endpoints require staff authentication and
a valid POS license.
"""

import math

from django.db import transaction
from django.db.models import Prefetch, Q
from django.utils.translation import gettext_lazy as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from admin_api.authentication import MobileTokenAuthentication
from core.api.api_descriptions import (
    AUTH_REQUIRED,
    POS_LICENSE_REQUIRED,
    PRODUCT_NOT_FOUND,
)
from pos_api.permissions import IsStaffUser, check_pos_permission
from pos_api.serializers.inventory import (
    POSCrossLocationStockSerializer,
    POSStockAdjustmentSerializer,
    POSStockItemSerializer,
    POSStockMovementSerializer,
)
from pos_api.views.utils import get_warehouse_id

# Product types that have physical inventory
_INVENTORY_TYPES = ("simple", "variable", "customizable")


def _get_product_image(product):
    """Get the primary image thumbnail URL for a product."""
    primary_images = getattr(product, "_primary_images", None)
    if primary_images:
        img = primary_images[0]
        if img.media_asset:
            return img.media_asset.get_thumbnail("medium")
    try:
        img = product.images.select_related("media_asset").filter(is_primary=True).first()
        if not img:
            img = product.images.select_related("media_asset").first()
        if img and img.media_asset:
            return img.media_asset.get_thumbnail("medium")
    except Exception:
        pass
    return None


def _haversine_km(lat1, lon1, lat2, lon2):
    """Calculate distance in km between two coordinate points."""
    R = 6371
    dlat = math.radians(float(lat2) - float(lat1))
    dlon = math.radians(float(lon2) - float(lon1))
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(float(lat1)))
        * math.cos(math.radians(float(lat2)))
        * math.sin(dlon / 2) ** 2
    )
    return R * 2 * math.asin(math.sqrt(a))


@extend_schema(
    summary=_("List stock levels for warehouse"),
    description=_(
        "Returns paginated stock levels for the terminal's warehouse. "
        "Supports search by product name or SKU and filtering for low-stock or no-stock items. "
        "Requires staff authentication and valid POS license."
    ),
    parameters=[
        OpenApiParameter("q", OpenApiTypes.STR, description=_("Search by product name or SKU")),
        OpenApiParameter(
            "low_stock_only",
            OpenApiTypes.BOOL,
            description=_("Only return items at or below low stock threshold"),
        ),
        OpenApiParameter(
            "no_stock_only",
            OpenApiTypes.BOOL,
            description=_("Only return items with zero available stock"),
        ),
        OpenApiParameter("page", OpenApiTypes.INT, description=_("Page number (default: 1)")),
        OpenApiParameter(
            "page_size", OpenApiTypes.INT, description=_("Items per page (default: 50, max: 200)")
        ),
    ],
    responses={
        200: POSStockItemSerializer(many=True),
        400: OpenApiResponse(description=_("Warehouse not determined")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Inventory"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def stock_levels(request):
    """List stock levels for the terminal's warehouse.

    Queries from Product/ProductVariant as base tables (not StockItem),
    so ALL published POS-enabled physical products appear — even those
    without a StockItem record in the warehouse.
    """
    from catalog.models import Product, ProductImage, ProductVariant, StockItem

    warehouse_id = get_warehouse_id(request)
    if not warehouse_id:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "WAREHOUSE_REQUIRED",
                    "message": "Could not determine warehouse. Provide X-Terminal-UUID or warehouse_id.",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    q = request.query_params.get("q", "").strip()
    low_stock_only = request.query_params.get("low_stock_only", "").lower() in ("true", "1")
    no_stock_only = request.query_params.get("no_stock_only", "").lower() in ("true", "1")

    # --- Image prefetch for products ---
    image_prefetch = Prefetch(
        "images",
        queryset=ProductImage.objects.select_related("media_asset").filter(is_primary=True)[:1],
        to_attr="_primary_images",
    )

    # --- Query A: Simple/customizable products ---
    base_filter = Q(
        status="published",
        sales_channel__in=["all", "pos_only"],
        product_type__in=("simple", "customizable"),
    )
    simple_qs = Product.objects.filter(base_filter).prefetch_related(image_prefetch)
    if q:
        simple_qs = simple_qs.filter(Q(name__icontains=q) | Q(sku__icontains=q))

    # --- Query B: Active variants of variable products ---
    variant_qs = (
        ProductVariant.objects.filter(
            is_active=True,
            product__status="published",
            product__sales_channel__in=["all", "pos_only"],
            product__product_type="variable",
        )
        .select_related("product")
        .prefetch_related(
            Prefetch(
                "product__images",
                queryset=ProductImage.objects.select_related("media_asset").filter(is_primary=True)[
                    :1
                ],
                to_attr="_primary_images",
            ),
        )
    )
    if q:
        variant_qs = variant_qs.filter(
            Q(product__name__icontains=q)
            | Q(product__sku__icontains=q)
            | Q(sku__icontains=q)
            | Q(name__icontains=q)
        )

    # --- Bulk StockItem lookup keyed by (product_id, variant_id) ---
    simple_ids = set(simple_qs.values_list("id", flat=True))
    variant_list = list(variant_qs)
    variable_product_ids = {v.product_id for v in variant_list}
    all_product_ids = simple_ids | variable_product_ids

    stock_map = {}  # (product_id, variant_id) -> StockItem
    if all_product_ids:
        for si in StockItem.objects.filter(
            warehouse_id=warehouse_id,
            product_id__in=all_product_ids,
        ):
            stock_map[(si.product_id, si.variant_id)] = si

    # --- Build unified results ---
    results = []

    for p in simple_qs:
        si = stock_map.get((p.id, None))
        on_hand = si.on_hand if si else 0
        allocated = si.allocated if si else 0
        available = max(0, on_hand - allocated)
        threshold = (
            si.low_stock_threshold if si and si.low_stock_threshold else 0
        ) or p.low_stock_threshold
        is_low = available <= threshold
        results.append(
            {
                "product_id": p.id,
                "product_name": str(p.name),
                "sku": p.sku or "",
                "variant_id": None,
                "variant_name": None,
                "on_hand": on_hand,
                "allocated": allocated,
                "available": available,
                "low_stock_threshold": threshold,
                "is_low_stock": is_low,
                "image": _get_product_image(p),
                "has_stock_item": si is not None,
                "product_type": p.product_type,
            }
        )

    for v in variant_list:
        si = stock_map.get((v.product_id, v.id))
        on_hand = si.on_hand if si else 0
        allocated = si.allocated if si else 0
        available = max(0, on_hand - allocated)
        threshold = (
            si.low_stock_threshold if si and si.low_stock_threshold else 0
        ) or v.product.low_stock_threshold
        is_low = available <= threshold
        results.append(
            {
                "product_id": v.product_id,
                "product_name": str(v.product.name),
                "sku": v.sku or v.product.sku or "",
                "variant_id": v.id,
                "variant_name": v.name,
                "on_hand": on_hand,
                "allocated": allocated,
                "available": available,
                "low_stock_threshold": threshold,
                "is_low_stock": is_low,
                "image": _get_product_image(v.product),
                "has_stock_item": si is not None,
                "product_type": "variable",
            }
        )

    # Stock level filters (post-merge, mutually exclusive)
    if no_stock_only:
        results = [r for r in results if r["available"] <= 0]
    elif low_stock_only:
        results = [r for r in results if r["is_low_stock"]]

    # Sort: low stock first, then alphabetical
    results.sort(
        key=lambda r: (not r["is_low_stock"], r["product_name"].lower(), r["variant_name"] or "")
    )

    # Pagination
    page = int(request.query_params.get("page", 1))
    page_size = min(int(request.query_params.get("page_size", 50)), 200)
    total = len(results)
    start = (page - 1) * page_size
    end = start + page_size

    return Response(
        {
            "success": True,
            "results": results[start:end],
            "count": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        }
    )


@extend_schema(
    summary=_("Get product stock detail"),
    description=_(
        "Returns stock levels for a specific product in the terminal's warehouse, "
        "including variant-level breakdown. "
        "Requires staff authentication and valid POS license."
    ),
    responses={
        200: POSStockItemSerializer(many=True),
        400: OpenApiResponse(description=_("Warehouse not determined")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        404: OpenApiResponse(description=PRODUCT_NOT_FOUND),
    },
    tags=["POS - Inventory"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def stock_detail(request, product_id):
    """Get stock detail for a single product."""
    from catalog.models import Product, StockItem

    warehouse_id = get_warehouse_id(request)
    if not warehouse_id:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "WAREHOUSE_REQUIRED",
                    "message": "Could not determine warehouse. Provide X-Terminal-UUID or warehouse_id.",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        product = Product.objects.get(
            id=product_id,
            status="published",
            sales_channel__in=["all", "pos_only"],
        )
    except Product.DoesNotExist:
        return Response(
            {"success": False, "error": {"code": "NOT_FOUND", "message": "Product not found."}},
            status=status.HTTP_404_NOT_FOUND,
        )

    stock_items = StockItem.objects.filter(
        product=product,
        warehouse_id=warehouse_id,
    ).select_related("variant")

    results = []
    for si in stock_items:
        results.append(
            {
                "product_id": si.product_id,
                "product_name": str(product.name),
                "sku": (si.variant.sku if si.variant and si.variant.sku else product.sku) or "",
                "variant_id": si.variant_id,
                "variant_name": si.variant.name if si.variant else None,
                "on_hand": si.on_hand,
                "allocated": si.allocated,
                "available": si.available,
                "low_stock_threshold": si.low_stock_threshold,
                "is_low_stock": si.is_low_stock,
            }
        )

    return Response({"success": True, "product": str(product.name), "stock": results})


@extend_schema(
    summary=_("Check stock across all locations"),
    description=_(
        "Returns stock levels for a product across all warehouse locations. "
        "Useful for checking if an out-of-stock item is available at another location. "
        "The current terminal's warehouse is marked with is_current=true. "
        "Requires staff authentication and valid POS license."
    ),
    responses={
        200: POSCrossLocationStockSerializer(many=True),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        404: OpenApiResponse(description=PRODUCT_NOT_FOUND),
    },
    tags=["POS - Inventory"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def cross_location_stock(request, product_id):
    """Check stock for a product across all warehouse locations.

    Includes contact details, address, region, and distance from the
    current terminal's warehouse. Results are sorted: same-region first,
    then nearest, then highest availability.
    """
    from catalog.models import Product, StockItem, Warehouse

    current_warehouse_id = get_warehouse_id(request)

    try:
        product = Product.objects.get(
            id=product_id,
            status="published",
            sales_channel__in=["all", "pos_only"],
        )
    except Product.DoesNotExist:
        return Response(
            {"success": False, "error": {"code": "NOT_FOUND", "message": "Product not found."}},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Get current warehouse for region/distance comparison
    current_wh = None
    current_region_id = None
    if current_warehouse_id:
        try:
            current_wh = Warehouse.objects.select_related("region").get(id=current_warehouse_id)
            current_region_id = current_wh.region_id
        except Warehouse.DoesNotExist:
            pass

    # Get stock in all active warehouses — aggregate across variants
    stock_items = StockItem.objects.filter(
        product=product,
        warehouse__is_active=True,
    ).select_related("warehouse__region")

    # Aggregate stock per warehouse (handles both simple and variable products)
    wh_stock = {}  # warehouse_id -> {on_hand, allocated, warehouse}
    for si in stock_items:
        wid = si.warehouse_id
        if wid not in wh_stock:
            wh_stock[wid] = {"on_hand": 0, "allocated": 0, "warehouse": si.warehouse}
        wh_stock[wid]["on_hand"] += si.on_hand
        wh_stock[wid]["allocated"] += si.allocated

    # Build location list
    locations = []
    for wid, data in wh_stock.items():
        wh = data["warehouse"]
        on_hand = data["on_hand"]
        allocated = data["allocated"]
        available = max(0, on_hand - allocated)

        # Skip locations with no available stock (unless current warehouse)
        is_current = wid == current_warehouse_id
        if available <= 0 and not is_current:
            continue

        same_region = bool(current_region_id and wh.region_id == current_region_id)

        # Calculate distance
        distance_km = None
        if (
            current_wh
            and current_wh.latitude
            and current_wh.longitude
            and wh.latitude
            and wh.longitude
        ):
            distance_km = round(
                _haversine_km(
                    current_wh.latitude,
                    current_wh.longitude,
                    wh.latitude,
                    wh.longitude,
                ),
                1,
            )

        locations.append(
            {
                "warehouse_id": wh.id,
                "warehouse_name": wh.pos_display_name or wh.name,
                "is_current": is_current,
                "on_hand": on_hand,
                "allocated": allocated,
                "available": available,
                "contact_name": wh.contact_name or "",
                "contact_phone": wh.contact_phone or "",
                "contact_email": wh.contact_email or "",
                "address": wh.full_address or "",
                "city": wh.city or "",
                "country": wh.country or "",
                "region_name": wh.region.name if wh.region else "",
                "same_region": same_region,
                "distance_km": distance_km,
            }
        )

    # Sort: current first, then same region, then nearest, then highest stock
    def _sort_key(loc):
        return (
            not loc["is_current"],
            not loc["same_region"],
            loc["distance_km"] if loc["distance_km"] is not None else 999999,
            -loc["available"],
        )

    locations.sort(key=_sort_key)

    return Response(
        {
            "success": True,
            "product": str(product.name),
            "locations": locations,
        }
    )


# Movement type mapping from adjustment_type to StockMovement.movement_type
_ADJUSTMENT_TYPE_MAP = {
    "receive": "adjustment",
    "damage": "damage",
    "recount": "recount",
    "return": "return",
}


@extend_schema(
    summary=_("Adjust stock levels"),
    description=_(
        "Adjust stock for a product in the terminal's warehouse. "
        "Supports four adjustment types: "
        "'receive' (add stock from shipment), "
        "'damage' (remove damaged/lost stock), "
        "'recount' (set absolute on_hand from physical count), "
        "'return' (add stock back from customer return). "
        "Creates an immutable StockMovement audit record. "
        "Requires staff authentication, valid POS license, and "
        "pos_stock_adjustment permission."
    ),
    request=POSStockAdjustmentSerializer,
    responses={
        200: OpenApiResponse(description=_("Stock adjusted successfully")),
        400: OpenApiResponse(description=_("Validation error or warehouse not determined")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=_("Permission denied or POS license required")),
        404: OpenApiResponse(description=_("Product or stock item not found")),
    },
    tags=["POS - Inventory"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def adjust_stock(request):
    """Adjust stock for a product in the terminal's warehouse."""
    from catalog.models import Product, StockItem, StockMovement

    err = check_pos_permission(request, "pos_stock_adjustment")
    if err:
        return err

    serializer = POSStockAdjustmentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = serializer.validated_data
    product_id = data["product_id"]
    variant_id = data.get("variant_id")
    adjustment_type = data["adjustment_type"]
    quantity = data["quantity"]
    reason = data["reason"]
    idempotency_key = data.get("idempotency_key")

    warehouse_id = get_warehouse_id(request)
    if not warehouse_id:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "WAREHOUSE_REQUIRED",
                    "message": "Could not determine warehouse. Provide X-Terminal-UUID or warehouse_id.",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Idempotency check
    if idempotency_key and StockMovement.objects.filter(reference_key=idempotency_key).exists():
        return Response(
            {
                "success": True,
                "message": "Adjustment already processed (duplicate idempotency key).",
                "duplicate": True,
            }
        )

    # Validate product exists
    try:
        Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {"success": False, "error": {"code": "NOT_FOUND", "message": "Product not found."}},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Build stock item lookup
    stock_filter = {"product_id": product_id, "warehouse_id": warehouse_id}
    if variant_id:
        stock_filter["variant_id"] = variant_id
    else:
        stock_filter["variant__isnull"] = True

    with transaction.atomic():
        stock_item = StockItem.objects.select_for_update().filter(**stock_filter).first()

        # Auto-create StockItem if none exists (products without stock
        # records now appear in the inventory grid)
        if not stock_item:
            stock_item = StockItem.objects.create(
                product_id=product_id,
                warehouse_id=warehouse_id,
                variant_id=variant_id,
                on_hand=0,
                allocated=0,
            )
            # Re-lock
            stock_item = StockItem.objects.select_for_update().get(pk=stock_item.pk)

        old_on_hand = stock_item.on_hand

        # Calculate delta based on adjustment type
        if adjustment_type in ("receive", "return"):
            delta = quantity
        elif adjustment_type == "damage":
            if quantity > old_on_hand:
                return Response(
                    {
                        "success": False,
                        "error": {
                            "code": "INSUFFICIENT_STOCK",
                            "message": (
                                f"Cannot remove {quantity} units. Only {old_on_hand} on hand."
                            ),
                        },
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            delta = -quantity
        elif adjustment_type == "recount":
            delta = quantity - old_on_hand
        else:
            delta = 0

        new_on_hand = old_on_hand + delta

        # Use .filter().update() to bypass StockItem post_save signal
        StockItem.objects.filter(pk=stock_item.pk).update(on_hand=new_on_hand)

        # Create audit trail
        movement_type = _ADJUSTMENT_TYPE_MAP[adjustment_type]
        StockMovement.objects.create(
            stock_item=stock_item,
            movement_type=movement_type,
            quantity=delta,
            previous_quantity=old_on_hand,
            new_quantity=new_on_hand,
            reason=reason,
            user=request.user,
            reference_key=idempotency_key,
        )

        # Refresh to return current state
        stock_item.refresh_from_db()

    return Response(
        {
            "success": True,
            "message": "Stock adjusted successfully.",
            "stock": {
                "product_id": stock_item.product_id,
                "variant_id": stock_item.variant_id,
                "on_hand": stock_item.on_hand,
                "allocated": stock_item.allocated,
                "available": stock_item.available,
                "delta": delta,
            },
        }
    )


@extend_schema(
    summary=_("List stock movement history"),
    description=_(
        "Returns paginated stock movement records for the terminal's warehouse. "
        "Useful for auditing recent stock changes (adjustments, damage, recounts, returns). "
        "Supports filtering by product and movement type. "
        "Requires staff authentication and valid POS license."
    ),
    parameters=[
        OpenApiParameter(
            "product_id",
            OpenApiTypes.INT,
            description=_("Filter movements by product ID"),
        ),
        OpenApiParameter(
            "type",
            OpenApiTypes.STR,
            description=_("Comma-separated movement types to include (e.g. 'damage,recount')"),
        ),
        OpenApiParameter("page", OpenApiTypes.INT, description=_("Page number (default: 1)")),
        OpenApiParameter(
            "page_size", OpenApiTypes.INT, description=_("Items per page (default: 20, max: 100)")
        ),
    ],
    responses={
        200: POSStockMovementSerializer(many=True),
        400: OpenApiResponse(description=_("Warehouse not determined")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Inventory"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def stock_movements(request):
    """List stock movement history for the terminal's warehouse."""
    from catalog.models import StockMovement

    warehouse_id = get_warehouse_id(request)
    if not warehouse_id:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "WAREHOUSE_REQUIRED",
                    "message": "Could not determine warehouse. Provide X-Terminal-UUID or warehouse_id.",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    movements = (
        StockMovement.objects.filter(
            stock_item__warehouse_id=warehouse_id,
        )
        .select_related(
            "stock_item__product",
            "stock_item__variant",
            "user",
        )
        .order_by("-created_at")
    )

    # Filter by product
    product_id = request.query_params.get("product_id")
    if product_id:
        movements = movements.filter(stock_item__product_id=int(product_id))

    # Filter by movement type
    type_filter = request.query_params.get("type", "").strip()
    if type_filter:
        types = [t.strip() for t in type_filter.split(",") if t.strip()]
        if types:
            movements = movements.filter(movement_type__in=types)

    # Pagination
    page = int(request.query_params.get("page", 1))
    page_size = min(int(request.query_params.get("page_size", 20)), 100)
    start = (page - 1) * page_size
    end = start + page_size

    total = movements.count()
    page_items = movements[start:end]

    results = []
    for mv in page_items:
        si = mv.stock_item
        user_name = ""
        if mv.user:
            user_name = mv.user.get_full_name() or mv.user.email or str(mv.user)
        results.append(
            {
                "id": mv.id,
                "product_id": si.product_id,
                "product_name": str(si.product.name),
                "sku": (si.variant.sku if si.variant and si.variant.sku else si.product.sku) or "",
                "variant_id": si.variant_id,
                "variant_name": si.variant.name if si.variant else None,
                "movement_type": mv.movement_type,
                "quantity": mv.quantity,
                "previous_quantity": mv.previous_quantity,
                "new_quantity": mv.new_quantity,
                "reason": mv.reason or "",
                "user_name": user_name,
                "created_at": mv.created_at.isoformat(),
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
        }
    )
