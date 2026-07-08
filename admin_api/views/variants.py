"""
Admin API Variant Views

Product variant management endpoints for the merchant admin API.
"""
import secrets
from decimal import Decimal
from django.db import IntegrityError, transaction
from django.db.models import Sum, IntegerField
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _
from djmoney.money import Money
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from catalog.models import Product, ProductVariant, StockItem, Warehouse
from core.utils import get_default_currency
from admin_api.permissions import IsStaffWithWritePermission
from admin_api.throttling import AdminAPIThrottle, AdminSensitiveOperationThrottle
from admin_api.services.audit_service import AuditService
from admin_api.serializers.variants import (
    AdminVariantListSerializer,
    VariantCreateSerializer,
    VariantUpdateSerializer,
)
from admin_api.serializers.auth import ErrorResponseSerializer


def generate_error_reference():
    """Generate a unique error reference for debugging."""
    return f"ERR-{secrets.token_hex(3).upper()}"


def _get_product_or_404(product_id):
    """Get product or return None."""
    try:
        return Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return None


@extend_schema(
    tags=['Admin - Variants'],
    summary=_("List product variants"),
    description=_("""
    Get all variants for a specific product, with stock information.

    **Rate Limit:** 300 requests per minute
    """),
    responses={200: AdminVariantListSerializer(many=True), 404: ErrorResponseSerializer}
)
@api_view(['GET'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def variant_list(request, product_id):
    """Get all variants for a product."""
    product = _get_product_or_404(product_id)
    if not product:
        return Response({
            'success': False,
            'error': {
                'code': 404,
                'message': _('Product not found.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_404_NOT_FOUND)

    variants = ProductVariant.objects.filter(product=product).annotate(
        _available_stock=Coalesce(
            Sum('stock_items__on_hand') - Sum('stock_items__allocated'), 0,
            output_field=IntegerField()
        )
    ).order_by('created_at')

    serializer = AdminVariantListSerializer(variants, many=True)
    return Response({
        'success': True,
        'data': {
            'product_id': product.id,
            'product_name': product.name,
            'variants': serializer.data
        }
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Admin - Variants'],
    summary=_("Create product variant"),
    description=_("""
    Create a new variant for a product. The product must be of type 'variable'.
    If `initial_stock` is provided and the product tracks inventory, a StockItem
    is auto-created for the default warehouse.

    **Rate Limit:** 30 requests per minute (sensitive operation)
    """),
    request=VariantCreateSerializer,
    responses={201: AdminVariantListSerializer, 400: ErrorResponseSerializer, 404: ErrorResponseSerializer}
)
@api_view(['POST'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def create_variant(request, product_id):
    """Create a new variant for a product."""
    product = _get_product_or_404(product_id)
    if not product:
        return Response({
            'success': False,
            'error': {
                'code': 404,
                'message': _('Product not found.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_404_NOT_FOUND)

    if product.product_type != 'variable':
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Variants can only be added to variable products. This product is type "%(type)s".') % {'type': product.product_type},
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer = VariantCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid variant data.'),
                'reference': generate_error_reference(),
                'details': serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data

    try:
        with transaction.atomic():
            variant = ProductVariant(
                product=product,
                name=data['name'],
                sku=data['sku'],
                pricing_strategy=data.get('pricing_strategy', 'inherit'),
                weight=data.get('weight'),
                barcode=data.get('barcode', ''),
                is_active=data.get('is_active', True),
            )

            # Set price if custom pricing
            if data.get('pricing_strategy') == 'custom' and data.get('price') is not None:
                currency = data.get('currency') or get_default_currency()
                variant.price = Money(Decimal(str(data['price'])), currency)

            variant.save()

            # Set attribute values
            attr_value_ids = data.get('attribute_value_ids', [])
            if attr_value_ids:
                variant.selected_attributes.set(attr_value_ids)

            # Auto-create StockItem for default warehouse
            if product.track_inventory:
                warehouse = Warehouse.objects.filter(is_active=True).first()
                if warehouse:
                    StockItem.objects.create(
                        product=product,
                        variant=variant,
                        warehouse=warehouse,
                        on_hand=data.get('initial_stock', 0),
                        allocated=0,
                    )
    except IntegrityError:
        return Response({
            'success': False,
            'error': {
                'code': 409,
                'message': _('A variant with this SKU already exists.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_409_CONFLICT)

    AuditService.log_variant_change(
        user=request.user,
        action_suffix='create',
        variant=variant,
        new_value={'name': variant.name, 'sku': variant.sku, 'product_id': product.id},
        request=request
    )

    # Re-fetch with annotations
    variant = ProductVariant.objects.annotate(
        _available_stock=Coalesce(
            Sum('stock_items__on_hand') - Sum('stock_items__allocated'), 0,
            output_field=IntegerField()
        )
    ).get(id=variant.id)

    return Response({
        'success': True,
        'message': _('Variant created successfully.'),
        'data': AdminVariantListSerializer(variant).data
    }, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=['Admin - Variants'],
    summary=_("Update product variant"),
    description=_("""
    Partially update a variant. Only provided fields will be changed.

    **Rate Limit:** 30 requests per minute (sensitive operation)
    """),
    request=VariantUpdateSerializer,
    responses={200: AdminVariantListSerializer, 400: ErrorResponseSerializer, 404: ErrorResponseSerializer}
)
@api_view(['PATCH'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def update_variant(request, product_id, variant_id):
    """Partially update a variant."""
    product = _get_product_or_404(product_id)
    if not product:
        return Response({
            'success': False,
            'error': {
                'code': 404,
                'message': _('Product not found.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_404_NOT_FOUND)

    try:
        variant = ProductVariant.objects.get(id=variant_id, product=product)
    except ProductVariant.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 404,
                'message': _('Variant not found.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = VariantUpdateSerializer(data=request.data, context={'variant': variant})
    if not serializer.is_valid():
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid variant data.'),
                'reference': generate_error_reference(),
                'details': serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    old_values = {}
    new_values = {}

    for field in ['name', 'sku', 'pricing_strategy', 'weight', 'barcode', 'is_active']:
        if field in data:
            old_values[field] = getattr(variant, field)
            setattr(variant, field, data[field])
            new_values[field] = data[field]

    if 'price' in data:
        old_values['price'] = str(variant.price.amount) if variant.price else None
        if data['price'] is not None:
            currency = data.get('currency') or (
                str(variant.price.currency) if variant.price else get_default_currency()
            )
            variant.price = Money(Decimal(str(data['price'])), currency)
            new_values['price'] = str(data['price'])
        else:
            variant.price = None
            new_values['price'] = None

    try:
        variant.save()
    except IntegrityError:
        return Response({
            'success': False,
            'error': {
                'code': 409,
                'message': _('A variant with this SKU already exists.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_409_CONFLICT)

    # Update attribute values if provided
    if 'attribute_value_ids' in data:
        old_values['attribute_value_ids'] = list(
            variant.selected_attributes.values_list('id', flat=True)
        )
        variant.selected_attributes.set(data['attribute_value_ids'])
        new_values['attribute_value_ids'] = data['attribute_value_ids']

    AuditService.log_variant_change(
        user=request.user,
        action_suffix='update',
        variant=variant,
        old_value=old_values,
        new_value=new_values,
        request=request
    )

    # Re-fetch with annotations
    variant = ProductVariant.objects.annotate(
        _available_stock=Coalesce(
            Sum('stock_items__on_hand') - Sum('stock_items__allocated'), 0,
            output_field=IntegerField()
        )
    ).get(id=variant.id)

    return Response({
        'success': True,
        'message': _('Variant updated successfully.'),
        'data': AdminVariantListSerializer(variant).data
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Admin - Variants'],
    summary=_("Delete product variant"),
    description=_("""
    Permanently delete a variant. Associated StockItems will be cascade-deleted.

    **Rate Limit:** 30 requests per minute (sensitive operation)
    """),
    responses={200: None, 404: ErrorResponseSerializer}
)
@api_view(['DELETE'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def delete_variant(request, product_id, variant_id):
    """Delete a variant."""
    product = _get_product_or_404(product_id)
    if not product:
        return Response({
            'success': False,
            'error': {
                'code': 404,
                'message': _('Product not found.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_404_NOT_FOUND)

    try:
        variant = ProductVariant.objects.get(id=variant_id, product=product)
    except ProductVariant.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 404,
                'message': _('Variant not found.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_404_NOT_FOUND)

    variant_name = variant.name
    variant_sku = variant.sku

    AuditService.log_variant_change(
        user=request.user,
        action_suffix='delete',
        variant=variant,
        old_value={'name': variant_name, 'sku': variant_sku, 'product_id': product.id},
        request=request
    )

    variant.delete()

    return Response({
        'success': True,
        'message': _('Variant "%(name)s" (%(sku)s) deleted successfully.') % {
            'name': variant_name, 'sku': variant_sku
        },
    }, status=status.HTTP_200_OK)
