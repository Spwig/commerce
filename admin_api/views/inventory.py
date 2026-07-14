"""
Admin API Inventory Intelligence Views

Endpoints for inventory dashboard, low stock analysis, velocity tracking,
stock movements, reorder suggestions, and inventory settings.
"""

import secrets
from datetime import datetime

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from admin_api.permissions import category_permission
from admin_api.serializers.auth import ErrorResponseSerializer
from admin_api.serializers.inventory import (
    InventoryDashboardSerializer,
    InventorySettingsSerializer,
    InventorySettingsUpdateSerializer,
    LowStockProductListSerializer,
    ReorderSuggestionListSerializer,
    StockMovementListSerializer,
    VelocityResponseSerializer,
)
from admin_api.services.inventory_service import InventoryService
from admin_api.throttling import AdminAPIThrottle, AdminSensitiveOperationThrottle
from core.api.api_descriptions import AUTH_REQUIRED, PERMISSION_DENIED, RATE_LIMIT_EXCEEDED


def _generate_error_reference():
    """Generate a unique error reference for debugging."""
    return f"ERR-{secrets.token_hex(3).upper()}"


# ──────────────────────────────────────────────
# a) Dashboard
# ──────────────────────────────────────────────


@extend_schema(
    tags=["Admin - Inventory"],
    summary=_("Get inventory intelligence dashboard"),
    description=_("""
    Get comprehensive inventory dashboard data including stock status breakdown,
    top velocity products, and recent stockout information.

    **Rate Limit:** 300 requests per minute

    Returns:
    - Total products and variants being tracked
    - Total stock value (on_hand * price)
    - Stock status counts (in_stock, low_stock, out_of_stock, overstock)
    - Stockouts in last 30 days
    - Top 5 fastest-selling products by velocity
    - 5 most recent products to reach zero stock
    """),
    responses={
        200: InventoryDashboardSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["GET"])
@permission_classes([category_permission("catalog", "view")])
@throttle_classes([AdminAPIThrottle])
def inventory_dashboard(request):
    """
    Get inventory intelligence dashboard.
    """
    try:
        data = InventoryService.get_inventory_dashboard()
        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
    except Exception:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 500,
                    "message": _("Failed to retrieve inventory dashboard data."),
                    "reference": _generate_error_reference(),
                },
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ──────────────────────────────────────────────
# b) Low Stock Products
# ──────────────────────────────────────────────


@extend_schema(
    tags=["Admin - Inventory"],
    summary=_("Get low stock products with velocity data"),
    description=_("""
    Enhanced low stock product list with sales velocity, days of supply,
    restock history, and per-warehouse stock breakdown.

    **Rate Limit:** 300 requests per minute

    **Severity Levels:**
    - `critical`: Available stock is 0 or below
    - `warning`: Available stock is above 0 but at or below threshold
    """),
    parameters=[
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
        OpenApiParameter(
            name="ordering",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Sort field: available_stock, -available_stock, name, -name"),
            required=False,
            default="available_stock",
        ),
        OpenApiParameter(
            name="severity",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Filter by severity: critical, warning"),
            required=False,
        ),
        OpenApiParameter(
            name="category_id",
            type=int,
            location=OpenApiParameter.QUERY,
            description=_("Filter by category ID"),
            required=False,
        ),
        OpenApiParameter(
            name="warehouse_id",
            type=int,
            location=OpenApiParameter.QUERY,
            description=_("Filter by warehouse ID"),
            required=False,
        ),
    ],
    responses={
        200: LowStockProductListSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["GET"])
@permission_classes([category_permission("catalog", "view")])
@throttle_classes([AdminAPIThrottle])
def inventory_low_stock(request):
    """
    Get low stock products with velocity and restock data.
    """
    # Parse pagination parameters
    try:
        page = int(request.query_params.get("page", 1))
        page = max(1, page)
    except (ValueError, TypeError):
        page = 1

    try:
        page_size = int(request.query_params.get("page_size", 20))
        page_size = min(max(1, page_size), 100)
    except (ValueError, TypeError):
        page_size = 20

    ordering = request.query_params.get("ordering", "available_stock")
    if ordering not in ("available_stock", "-available_stock", "name", "-name"):
        ordering = "available_stock"

    severity = request.query_params.get("severity")
    if severity and severity not in ("critical", "warning"):
        severity = None

    # Optional filters
    category_id = None
    try:
        cat_param = request.query_params.get("category_id")
        if cat_param:
            category_id = int(cat_param)
    except (ValueError, TypeError):
        pass

    warehouse_id = None
    try:
        wh_param = request.query_params.get("warehouse_id")
        if wh_param:
            warehouse_id = int(wh_param)
    except (ValueError, TypeError):
        pass

    try:
        data = InventoryService.get_low_stock_products(
            page=page,
            page_size=page_size,
            ordering=ordering,
            severity=severity,
            category_id=category_id,
            warehouse_id=warehouse_id,
        )
        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
    except Exception:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 500,
                    "message": _("Failed to retrieve low stock products."),
                    "reference": _generate_error_reference(),
                },
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ──────────────────────────────────────────────
# c) Velocity
# ──────────────────────────────────────────────


@extend_schema(
    tags=["Admin - Inventory"],
    summary=_("Get stock velocity for a product"),
    description=_("""
    Get detailed stock velocity data for a specific product including
    daily/weekly/monthly averages, trend direction, projected stockout date,
    and per-day sales history for charting.

    **Rate Limit:** 300 requests per minute

    **Required:** `product_id` query parameter
    """),
    parameters=[
        OpenApiParameter(
            name="product_id",
            type=int,
            location=OpenApiParameter.QUERY,
            description=_("Product ID (required)"),
            required=True,
        ),
        OpenApiParameter(
            name="variant_id",
            type=int,
            location=OpenApiParameter.QUERY,
            description=_("Optional variant ID"),
            required=False,
        ),
        OpenApiParameter(
            name="period",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Period for daily sales chart: 7d, 30d, 90d"),
            required=False,
            default="30d",
        ),
    ],
    responses={
        200: VelocityResponseSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        404: ErrorResponseSerializer,
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["GET"])
@permission_classes([category_permission("catalog", "view")])
@throttle_classes([AdminAPIThrottle])
def inventory_velocity(request):
    """
    Get stock velocity for a specific product.
    """
    # product_id is required
    product_id_param = request.query_params.get("product_id")
    if not product_id_param:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("product_id query parameter is required."),
                    "reference": _generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        product_id = int(product_id_param)
    except (ValueError, TypeError):
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("product_id must be a valid integer."),
                    "reference": _generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    variant_id = None
    try:
        v_param = request.query_params.get("variant_id")
        if v_param:
            variant_id = int(v_param)
    except (ValueError, TypeError):
        pass

    period = request.query_params.get("period", "30d")
    if period not in ("7d", "30d", "90d"):
        period = "30d"

    try:
        data = InventoryService.get_velocity(
            product_id=product_id,
            variant_id=variant_id,
            period=period,
        )

        if data is None:
            return Response(
                {
                    "success": False,
                    "error": {
                        "code": 404,
                        "message": _("Product not found."),
                        "reference": _generate_error_reference(),
                    },
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
    except Exception:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 500,
                    "message": _("Failed to retrieve velocity data."),
                    "reference": _generate_error_reference(),
                },
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ──────────────────────────────────────────────
# d) Stock Movements
# ──────────────────────────────────────────────


@extend_schema(
    tags=["Admin - Inventory"],
    summary=_("Get stock movement history"),
    description=_("""
    Get paginated stock movement history for a specific product.
    Supports filtering by variant, warehouse, movement type, and date range.

    **Rate Limit:** 300 requests per minute

    **Required:** `product_id` query parameter

    **Movement Types:** adjustment, allocation, fulfillment, return, transfer, damage, recount
    """),
    parameters=[
        OpenApiParameter(
            name="product_id",
            type=int,
            location=OpenApiParameter.QUERY,
            description=_("Product ID (required)"),
            required=True,
        ),
        OpenApiParameter(
            name="variant_id",
            type=int,
            location=OpenApiParameter.QUERY,
            description=_("Filter by variant ID"),
            required=False,
        ),
        OpenApiParameter(
            name="warehouse_id",
            type=int,
            location=OpenApiParameter.QUERY,
            description=_("Filter by warehouse ID"),
            required=False,
        ),
        OpenApiParameter(
            name="movement_type",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Filter by movement type"),
            required=False,
        ),
        OpenApiParameter(
            name="start_date",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Start date filter (YYYY-MM-DD)"),
            required=False,
        ),
        OpenApiParameter(
            name="end_date",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("End date filter (YYYY-MM-DD)"),
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
        200: StockMovementListSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["GET"])
@permission_classes([category_permission("catalog", "view")])
@throttle_classes([AdminAPIThrottle])
def inventory_movements(request):
    """
    Get stock movement history for a product.
    """
    # product_id is required
    product_id_param = request.query_params.get("product_id")
    if not product_id_param:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("product_id query parameter is required."),
                    "reference": _generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        product_id = int(product_id_param)
    except (ValueError, TypeError):
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("product_id must be a valid integer."),
                    "reference": _generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Optional filters
    variant_id = None
    try:
        v_param = request.query_params.get("variant_id")
        if v_param:
            variant_id = int(v_param)
    except (ValueError, TypeError):
        pass

    warehouse_id = None
    try:
        wh_param = request.query_params.get("warehouse_id")
        if wh_param:
            warehouse_id = int(wh_param)
    except (ValueError, TypeError):
        pass

    movement_type = request.query_params.get("movement_type")
    valid_types = (
        "adjustment",
        "allocation",
        "fulfillment",
        "return",
        "transfer",
        "damage",
        "recount",
    )
    if movement_type and movement_type not in valid_types:
        movement_type = None

    # Date filters
    start_date = None
    end_date = None
    try:
        sd_param = request.query_params.get("start_date")
        if sd_param:
            start_date = datetime.strptime(sd_param, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        pass

    try:
        ed_param = request.query_params.get("end_date")
        if ed_param:
            end_date = datetime.strptime(ed_param, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        pass

    # Pagination
    try:
        page = int(request.query_params.get("page", 1))
        page = max(1, page)
    except (ValueError, TypeError):
        page = 1

    try:
        page_size = int(request.query_params.get("page_size", 20))
        page_size = min(max(1, page_size), 100)
    except (ValueError, TypeError):
        page_size = 20

    try:
        data = InventoryService.get_stock_movements(
            product_id=product_id,
            variant_id=variant_id,
            warehouse_id=warehouse_id,
            movement_type=movement_type,
            start_date=start_date,
            end_date=end_date,
            page=page,
            page_size=page_size,
        )
        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
    except Exception:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 500,
                    "message": _("Failed to retrieve stock movements."),
                    "reference": _generate_error_reference(),
                },
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ──────────────────────────────────────────────
# e) Reorder Suggestions
# ──────────────────────────────────────────────


@extend_schema(
    tags=["Admin - Inventory"],
    summary=_("Get reorder suggestions"),
    description=_("""
    Get products that need reordering based on sales velocity, lead time,
    and safety stock calculations.

    **Rate Limit:** 300 requests per minute

    **Urgency Levels:**
    - `immediate`: Less than 7 days of supply remaining
    - `soon`: 7-14 days of supply remaining
    - `upcoming`: 14-30 days of supply remaining

    **Reorder Formula:**
    `suggested_qty = velocity * (lead_days + safety_multiplier * lead_days) - current_stock`
    """),
    parameters=[
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
        OpenApiParameter(
            name="ordering",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Sort field: urgency, -urgency, name, -name"),
            required=False,
            default="urgency",
        ),
        OpenApiParameter(
            name="urgency",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Filter by urgency: immediate, soon, upcoming"),
            required=False,
        ),
    ],
    responses={
        200: ReorderSuggestionListSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["GET"])
@permission_classes([category_permission("catalog", "view")])
@throttle_classes([AdminAPIThrottle])
def inventory_reorder_suggestions(request):
    """
    Get products needing reorder based on velocity and supply analysis.
    """
    # Pagination
    try:
        page = int(request.query_params.get("page", 1))
        page = max(1, page)
    except (ValueError, TypeError):
        page = 1

    try:
        page_size = int(request.query_params.get("page_size", 20))
        page_size = min(max(1, page_size), 100)
    except (ValueError, TypeError):
        page_size = 20

    ordering = request.query_params.get("ordering", "urgency")
    if ordering not in ("urgency", "-urgency", "name", "-name"):
        ordering = "urgency"

    urgency = request.query_params.get("urgency")
    if urgency and urgency not in ("immediate", "soon", "upcoming"):
        urgency = None

    try:
        data = InventoryService.get_reorder_suggestions(
            page=page,
            page_size=page_size,
            ordering=ordering,
            urgency=urgency,
        )
        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
    except Exception:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 500,
                    "message": _("Failed to retrieve reorder suggestions."),
                    "reference": _generate_error_reference(),
                },
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ──────────────────────────────────────────────
# f) Inventory Settings - GET
# ──────────────────────────────────────────────


@extend_schema(
    tags=["Admin - Inventory"],
    summary=_("Get inventory settings"),
    description=_("""
    Get current inventory management settings from site configuration.

    **Rate Limit:** 300 requests per minute

    Returns settings for:
    - Low stock thresholds and alerts
    - Default inventory tracking preferences
    - Reorder lead time and safety stock parameters
    - Velocity calculation window
    """),
    responses={
        200: InventorySettingsSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["GET"])
@permission_classes([category_permission("catalog", "view")])
@throttle_classes([AdminAPIThrottle])
def inventory_settings_get(request):
    """
    Get inventory management settings.
    """
    from core.models import SiteSettings

    try:
        site_settings = SiteSettings.objects.first()

        # Map API field names -> actual SiteSettings field names
        data = {
            "default_low_stock_threshold": getattr(site_settings, "low_stock_threshold", 10),
            "low_stock_alerts_enabled": getattr(site_settings, "enable_low_stock_alerts", True),
            "low_stock_alert_frequency": getattr(
                site_settings, "low_stock_alert_frequency", "daily"
            ),
            "track_inventory_by_default": getattr(site_settings, "enable_inventory_tracking", True),
            "allow_backorders_by_default": getattr(
                site_settings, "allow_backorders_by_default", False
            ),
            "default_reorder_lead_days": getattr(site_settings, "default_reorder_lead_days", 14),
            "safety_stock_multiplier": getattr(site_settings, "safety_stock_multiplier", 1.5),
            "velocity_calculation_window_days": getattr(
                site_settings, "velocity_calculation_window_days", 30
            ),
        }

        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
    except Exception:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 500,
                    "message": _("Failed to retrieve inventory settings."),
                    "reference": _generate_error_reference(),
                },
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ──────────────────────────────────────────────
# g) Inventory Settings - UPDATE
# ──────────────────────────────────────────────


@extend_schema(
    tags=["Admin - Inventory"],
    summary=_("Update inventory settings"),
    description=_("""
    Update inventory management settings. Partial updates are supported;
    only provided fields will be updated.

    **Rate Limit:** 30 requests per minute (sensitive operation)

    Requires settings full access permission.
    """),
    request=InventorySettingsUpdateSerializer,
    responses={
        200: InventorySettingsSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["PATCH"])
@permission_classes([category_permission("settings", "full")])
@throttle_classes([AdminSensitiveOperationThrottle])
def inventory_settings_update(request):
    """
    Update inventory management settings.
    """
    from core.models import SiteSettings

    serializer = InventorySettingsUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid settings data."),
                    "reference": _generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        site_settings = SiteSettings.objects.first()
        if not site_settings:
            return Response(
                {
                    "success": False,
                    "error": {
                        "code": 500,
                        "message": _("Site settings not configured."),
                        "reference": _generate_error_reference(),
                    },
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Map API field names to actual SiteSettings model field names
        API_TO_MODEL_FIELD = {
            "default_low_stock_threshold": "low_stock_threshold",
            "low_stock_alerts_enabled": "enable_low_stock_alerts",
            "track_inventory_by_default": "enable_inventory_tracking",
            # These map 1:1
            "low_stock_alert_frequency": "low_stock_alert_frequency",
            "allow_backorders_by_default": "allow_backorders_by_default",
            "default_reorder_lead_days": "default_reorder_lead_days",
            "safety_stock_multiplier": "safety_stock_multiplier",
            "velocity_calculation_window_days": "velocity_calculation_window_days",
        }

        # Update only provided fields
        validated = serializer.validated_data
        updated_fields = []

        for api_field, value in validated.items():
            model_field = API_TO_MODEL_FIELD.get(api_field, api_field)
            if hasattr(site_settings, model_field):
                setattr(site_settings, model_field, value)
                updated_fields.append(model_field)

        if updated_fields:
            site_settings.save(update_fields=updated_fields)

        # Return updated settings
        data = {
            "default_low_stock_threshold": getattr(site_settings, "low_stock_threshold", 10),
            "low_stock_alerts_enabled": getattr(site_settings, "enable_low_stock_alerts", True),
            "low_stock_alert_frequency": getattr(
                site_settings, "low_stock_alert_frequency", "daily"
            ),
            "track_inventory_by_default": getattr(site_settings, "enable_inventory_tracking", True),
            "allow_backorders_by_default": getattr(
                site_settings, "allow_backorders_by_default", False
            ),
            "default_reorder_lead_days": getattr(site_settings, "default_reorder_lead_days", 14),
            "safety_stock_multiplier": getattr(site_settings, "safety_stock_multiplier", 1.5),
            "velocity_calculation_window_days": getattr(
                site_settings, "velocity_calculation_window_days", 30
            ),
        }

        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
    except Exception:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 500,
                    "message": _("Failed to update inventory settings."),
                    "reference": _generate_error_reference(),
                },
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
