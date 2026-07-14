"""
Admin API Bulk Product Views

Bulk product operations: stock adjustments, price updates, sale updates,
category assignment, and tag management endpoints for the merchant mobile app.
"""

import logging
import secrets
from decimal import ROUND_HALF_UP, Decimal

from django.db import transaction
from django.utils.translation import gettext_lazy as _
from djmoney.money import Money
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from admin_api.permissions import category_permission
from admin_api.serializers.auth import BulkOperationResponseSerializer, ErrorResponseSerializer
from admin_api.serializers.bulk_operations import (
    BulkAssignCategorySerializer,
    BulkAssignTagsSerializer,
    BulkPriceUpdateSerializer,
    BulkSaleUpdateSerializer,
    BulkStockAdjustSerializer,
)
from admin_api.services.audit_service import AuditService
from admin_api.throttling import AdminSensitiveOperationThrottle
from catalog.models import Product, StockItem, Warehouse
from core.api.api_descriptions import AUTH_REQUIRED, PERMISSION_DENIED, RATE_LIMIT_EXCEEDED
from core.utils import get_default_currency

logger = logging.getLogger(__name__)


def generate_error_reference():
    """Generate a unique error reference for debugging."""
    return f"ERR-{secrets.token_hex(3).upper()}"


@extend_schema(
    tags=["Admin - Bulk Operations"],
    summary=_("Bulk stock adjustment"),
    description=_("""
    Adjust stock quantities for multiple products in a single request.

    **Rate Limit:** 30 requests per minute (sensitive operation)

    Maximum 100 adjustments per request. Each adjustment is processed independently.

    **Adjustment types:**
    - set: Set on_hand to the specified quantity
    - adjust: Add quantity to on_hand (can be negative for decrements)

    Uses StockItem.adjust_stock() for 'adjust' type, creating StockMovement audit records.
    """),
    request=BulkStockAdjustSerializer,
    responses={
        200: BulkOperationResponseSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["POST"])
@permission_classes([category_permission("catalog", "full")])
@throttle_classes([AdminSensitiveOperationThrottle])
def bulk_stock_adjust(request):
    """
    Bulk adjust stock quantities for products.
    """
    serializer = BulkStockAdjustSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid bulk stock adjustment request."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    adjustments = serializer.validated_data["adjustments"]
    reason = serializer.validated_data["reason"]
    notes = serializer.validated_data.get("notes", "")

    succeeded = 0
    failed = 0
    results = []

    full_reason = reason
    if notes:
        full_reason = f"{reason} - {notes}"

    for idx, adj in enumerate(adjustments):
        product_id = adj["product_id"]
        variant_id = adj.get("variant_id")
        warehouse_id = adj.get("warehouse_id")
        quantity = adj["quantity"]
        adjustment_type = adj["adjustment_type"]

        try:
            with transaction.atomic():
                product = Product.objects.get(id=product_id)

                if not product.track_inventory:
                    results.append(
                        {
                            "index": idx,
                            "product_id": product_id,
                            "success": False,
                            "error": _("Product does not track inventory."),
                        }
                    )
                    failed += 1
                    continue

                # Resolve warehouse
                if warehouse_id:
                    warehouse = Warehouse.objects.get(id=warehouse_id)
                else:
                    warehouse = Warehouse.objects.filter(is_active=True).first()
                    if not warehouse:
                        results.append(
                            {
                                "index": idx,
                                "product_id": product_id,
                                "success": False,
                                "error": _("No active warehouse available."),
                            }
                        )
                        failed += 1
                        continue

                # Get or create stock item
                stock_item, created = StockItem.objects.get_or_create(
                    product=product,
                    warehouse=warehouse,
                    variant_id=variant_id,
                    defaults={"on_hand": 0, "allocated": 0},
                )

                old_quantity = stock_item.on_hand

                if adjustment_type == "set":
                    # Direct set: calculate delta and use adjust_stock for audit trail
                    delta = quantity - old_quantity
                    if delta != 0:
                        stock_item.adjust_stock(delta, reason=full_reason)
                    new_quantity = quantity
                else:
                    # Adjust: add quantity (can be negative)
                    stock_item.adjust_stock(quantity, reason=full_reason)
                    stock_item.refresh_from_db()
                    new_quantity = stock_item.on_hand

                AuditService.log_stock_adjustment(
                    user=request.user,
                    product=product,
                    warehouse_name=warehouse.name,
                    old_quantity=old_quantity,
                    new_quantity=new_quantity,
                    reason=full_reason,
                    request=request,
                )

                results.append(
                    {
                        "index": idx,
                        "product_id": product_id,
                        "success": True,
                        "old_quantity": old_quantity,
                        "new_quantity": new_quantity,
                        "warehouse": warehouse.name,
                    }
                )
                succeeded += 1

        except Product.DoesNotExist:
            results.append(
                {
                    "index": idx,
                    "product_id": product_id,
                    "success": False,
                    "error": _("Product not found."),
                }
            )
            failed += 1
        except Warehouse.DoesNotExist:
            results.append(
                {
                    "index": idx,
                    "product_id": product_id,
                    "success": False,
                    "error": _("Warehouse not found."),
                }
            )
            failed += 1
        except Exception as e:
            logger.error(
                f"Bulk stock adjustment failed for product {product_id}: {e}", exc_info=True
            )
            results.append(
                {"index": idx, "product_id": product_id, "success": False, "error": str(e)}
            )
            failed += 1

    AuditService.log_bulk_operation(
        user=request.user,
        action="product.bulk_stock_adjust",
        resource_type="product",
        created_count=succeeded,
        error_count=failed,
        request=request,
    )

    return Response(
        {
            "success": succeeded > 0,
            "data": {
                "total": len(adjustments),
                "succeeded": succeeded,
                "failed": failed,
                "results": results,
            },
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin - Bulk Operations"],
    summary=_("Bulk price update"),
    description=_("""
    Update prices for multiple products in a single request.

    **Rate Limit:** 30 requests per minute (sensitive operation)

    Maximum 100 products per request.

    **Update types:**
    - absolute: Set the price to the specified value
    - percentage: Adjust the current price by a percentage (e.g., -10 for 10%% decrease, 15 for 15%% increase)

    """),
    request=BulkPriceUpdateSerializer,
    responses={
        200: BulkOperationResponseSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["POST"])
@permission_classes([category_permission("catalog", "full")])
@throttle_classes([AdminSensitiveOperationThrottle])
def bulk_price_update(request):
    """
    Bulk update product prices.
    """
    serializer = BulkPriceUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid bulk price update request."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    product_ids = serializer.validated_data["product_ids"]
    update_type = serializer.validated_data["update_type"]
    value = serializer.validated_data["value"]
    round_to = serializer.validated_data.get("round_to", 2)

    succeeded = 0
    failed = 0
    results = []

    for product_id in product_ids:
        try:
            with transaction.atomic():
                product = Product.objects.select_for_update().get(id=product_id)

                current_price = product.price
                old_price_amount = current_price.amount if current_price else Decimal("0")
                currency = str(current_price.currency) if current_price else get_default_currency()

                # Calculate new price
                if update_type == "absolute":
                    new_price_amount = Decimal(str(value))
                else:
                    # Percentage adjustment
                    percentage = Decimal(str(value))
                    multiplier = (Decimal("100") + percentage) / Decimal("100")
                    new_price_amount = old_price_amount * multiplier

                # Round to specified decimal places
                quantize_str = "0." + "0" * round_to if round_to > 0 else "1"
                new_price_amount = new_price_amount.quantize(
                    Decimal(quantize_str), rounding=ROUND_HALF_UP
                )

                # Ensure price is not negative
                if new_price_amount < Decimal("0"):
                    new_price_amount = Decimal("0")

                new_price = Money(new_price_amount, currency)

                product.price = new_price
                product.save(update_fields=["price", "price_currency", "updated_at"])

                AuditService.log_product_update(
                    user=request.user,
                    product=product,
                    old_values={"price": str(old_price_amount), "currency": currency},
                    new_values={"price": str(new_price_amount), "currency": currency},
                    request=request,
                )

                results.append(
                    {
                        "product_id": product_id,
                        "success": True,
                        "old_price": str(old_price_amount),
                        "new_price": str(new_price_amount),
                        "currency": currency,
                    }
                )
                succeeded += 1

        except Product.DoesNotExist:
            results.append(
                {"product_id": product_id, "success": False, "error": _("Product not found.")}
            )
            failed += 1
        except Exception as e:
            logger.error(f"Bulk price update failed for product {product_id}: {e}", exc_info=True)
            results.append({"product_id": product_id, "success": False, "error": str(e)})
            failed += 1

    AuditService.log_bulk_operation(
        user=request.user,
        action="product.bulk_price_update",
        resource_type="product",
        created_count=succeeded,
        error_count=failed,
        request=request,
    )

    return Response(
        {
            "success": succeeded > 0,
            "data": {
                "total": len(product_ids),
                "succeeded": succeeded,
                "failed": failed,
                "results": results,
            },
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin - Bulk Operations"],
    summary=_("Bulk assign category"),
    description=_("""
    Assign multiple products to a single category.

    **Rate Limit:** 30 requests per minute (sensitive operation)

    Maximum 100 products per request.
    """),
    request=BulkAssignCategorySerializer,
    responses={
        200: BulkOperationResponseSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["POST"])
@permission_classes([category_permission("catalog", "full")])
@throttle_classes([AdminSensitiveOperationThrottle])
def bulk_assign_category(request):
    """
    Bulk assign products to a category.
    """
    from catalog.models import Category

    serializer = BulkAssignCategorySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid bulk category assignment request."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    product_ids = serializer.validated_data["product_ids"]
    category_id = serializer.validated_data["category_id"]

    # Validate category exists
    try:
        target_category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Category not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    succeeded = 0
    failed = 0
    results = []

    for product_id in product_ids:
        try:
            with transaction.atomic():
                product = Product.objects.select_for_update().get(id=product_id)
                old_category_id = product.category_id
                old_category_name = product.category.name if product.category else None

                product.category = target_category
                product.save(update_fields=["category_id", "updated_at"])

                AuditService.log_product_update(
                    user=request.user,
                    product=product,
                    old_values={"category_id": old_category_id, "category_name": old_category_name},
                    new_values={"category_id": category_id, "category_name": target_category.name},
                    request=request,
                )

                results.append(
                    {
                        "product_id": product_id,
                        "success": True,
                        "old_category": old_category_name,
                        "new_category": target_category.name,
                    }
                )
                succeeded += 1

        except Product.DoesNotExist:
            results.append(
                {"product_id": product_id, "success": False, "error": _("Product not found.")}
            )
            failed += 1
        except Exception as e:
            logger.error(
                f"Bulk category assignment failed for product {product_id}: {e}", exc_info=True
            )
            results.append({"product_id": product_id, "success": False, "error": str(e)})
            failed += 1

    AuditService.log_bulk_operation(
        user=request.user,
        action="product.bulk_assign_category",
        resource_type="product",
        created_count=succeeded,
        error_count=failed,
        request=request,
    )

    return Response(
        {
            "success": succeeded > 0,
            "data": {
                "total": len(product_ids),
                "succeeded": succeeded,
                "failed": failed,
                "results": results,
            },
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin - Bulk Operations"],
    summary=_("Bulk assign tags"),
    description=_("""
    Add, replace, or remove tags for multiple products.

    **Rate Limit:** 30 requests per minute (sensitive operation)

    Maximum 100 products per request.

    **Modes:**
    - add: Add specified tags to products (existing tags preserved)
    - replace: Replace all tags with the specified set
    - remove: Remove specified tags from products
    """),
    request=BulkAssignTagsSerializer,
    responses={
        200: BulkOperationResponseSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["POST"])
@permission_classes([category_permission("catalog", "full")])
@throttle_classes([AdminSensitiveOperationThrottle])
def bulk_assign_tags(request):
    """
    Bulk add, replace, or remove tags for products.
    """
    from catalog.models import ProductTag

    serializer = BulkAssignTagsSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid bulk tag assignment request."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    product_ids = serializer.validated_data["product_ids"]
    tag_slugs = serializer.validated_data["tags"]
    mode = serializer.validated_data["mode"]

    # Get or create ProductTag objects for all specified slugs
    tag_objects = []
    for slug in tag_slugs:
        tag, created = ProductTag.objects.get_or_create(
            slug=slug, defaults={"name": slug.replace("-", " ").title()}
        )
        tag_objects.append(tag)

    succeeded = 0
    failed = 0
    results = []

    for product_id in product_ids:
        try:
            with transaction.atomic():
                product = Product.objects.get(id=product_id)

                old_tags = list(product.tags.values_list("slug", flat=True))

                if mode == "add":
                    product.tags.add(*tag_objects)
                elif mode == "replace":
                    product.tags.set(tag_objects)
                elif mode == "remove":
                    product.tags.remove(*tag_objects)

                new_tags = list(product.tags.values_list("slug", flat=True))

                AuditService.log_product_update(
                    user=request.user,
                    product=product,
                    old_values={"tags": old_tags},
                    new_values={"tags": new_tags},
                    request=request,
                )

                results.append(
                    {
                        "product_id": product_id,
                        "success": True,
                        "old_tags": old_tags,
                        "new_tags": new_tags,
                    }
                )
                succeeded += 1

        except Product.DoesNotExist:
            results.append(
                {"product_id": product_id, "success": False, "error": _("Product not found.")}
            )
            failed += 1
        except Exception as e:
            logger.error(f"Bulk tag assignment failed for product {product_id}: {e}", exc_info=True)
            results.append({"product_id": product_id, "success": False, "error": str(e)})
            failed += 1

    AuditService.log_bulk_operation(
        user=request.user,
        action="product.bulk_assign_tags",
        resource_type="product",
        created_count=succeeded,
        error_count=failed,
        request=request,
    )

    return Response(
        {
            "success": succeeded > 0,
            "data": {
                "total": len(product_ids),
                "succeeded": succeeded,
                "failed": failed,
                "results": results,
            },
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin - Bulk Operations"],
    summary=_("Bulk sale update"),
    description=_("""
    Update sale settings for multiple products in a single request.

    **Rate Limit:** 30 requests per minute (sensitive operation)

    Maximum 100 products per request.

    **Sale types:**
    - none: Clear sale (removes all sale settings)
    - fixed_price: Set a fixed sale price
    - amount_off: Subtract a fixed amount from the base price
    - percentage_off: Apply a percentage discount off the base price

    Optionally set sale_start_date and sale_end_date to schedule the sale.
    """),
    request=BulkSaleUpdateSerializer,
    responses={
        200: BulkOperationResponseSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["POST"])
@permission_classes([category_permission("catalog", "full")])
@throttle_classes([AdminSensitiveOperationThrottle])
def bulk_sale_update(request):
    """
    Bulk update sale settings for products.
    """
    serializer = BulkSaleUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid bulk sale update request."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    product_ids = serializer.validated_data["product_ids"]
    sale_type = serializer.validated_data["sale_type"]
    sale_value = serializer.validated_data.get("sale_value")
    sale_start_date = serializer.validated_data.get("sale_start_date")
    sale_end_date = serializer.validated_data.get("sale_end_date")

    succeeded = 0
    failed = 0
    results = []

    for product_id in product_ids:
        try:
            with transaction.atomic():
                product = Product.objects.select_for_update().get(id=product_id)

                old_values = {
                    "sale_type": product.sale_type,
                    "sale_value": str(product.sale_value) if product.sale_value else None,
                    "sale_start_date": (
                        product.sale_start_date.isoformat() if product.sale_start_date else None
                    ),
                    "sale_end_date": (
                        product.sale_end_date.isoformat() if product.sale_end_date else None
                    ),
                }

                product.sale_type = sale_type
                product.sale_value = sale_value
                product.sale_start_date = sale_start_date
                product.sale_end_date = sale_end_date
                product.save(
                    update_fields=[
                        "sale_type",
                        "sale_value",
                        "sale_start_date",
                        "sale_end_date",
                        "updated_at",
                    ]
                )

                new_values = {
                    "sale_type": sale_type,
                    "sale_value": str(sale_value) if sale_value else None,
                    "sale_start_date": (sale_start_date.isoformat() if sale_start_date else None),
                    "sale_end_date": (sale_end_date.isoformat() if sale_end_date else None),
                }

                AuditService.log_product_update(
                    user=request.user,
                    product=product,
                    old_values=old_values,
                    new_values=new_values,
                    request=request,
                )

                results.append(
                    {
                        "product_id": product_id,
                        "success": True,
                        "old_sale_type": old_values["sale_type"],
                        "new_sale_type": sale_type,
                        "sale_value": str(sale_value) if sale_value else None,
                    }
                )
                succeeded += 1

        except Product.DoesNotExist:
            results.append(
                {"product_id": product_id, "success": False, "error": _("Product not found.")}
            )
            failed += 1
        except Exception as e:
            logger.error(f"Bulk sale update failed for product {product_id}: {e}", exc_info=True)
            results.append({"product_id": product_id, "success": False, "error": str(e)})
            failed += 1

    AuditService.log_bulk_operation(
        user=request.user,
        action="product.bulk_sale_update",
        resource_type="product",
        created_count=succeeded,
        error_count=failed,
        request=request,
    )

    return Response(
        {
            "success": succeeded > 0,
            "data": {
                "total": len(product_ids),
                "succeeded": succeeded,
                "failed": failed,
                "results": results,
            },
        },
        status=status.HTTP_200_OK,
    )
