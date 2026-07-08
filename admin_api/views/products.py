"""
Admin API Product Views

Product and stock management endpoints for the merchant mobile app.
"""
import logging
import secrets
from decimal import Decimal
from django.db import models, IntegrityError, transaction
from django.db.models import Q, Sum, F, Max, IntegerField
from django.db.models.functions import Coalesce
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from djmoney.money import Money
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from catalog.models import Product, ProductImage, StockItem, Warehouse
from core.utils import get_default_currency
from media_library.models import MediaAsset
from media_library.services import ImageProcessor
from admin_api.permissions import IsStaffWithWritePermission
from admin_api.throttling import AdminAPIThrottle, AdminSensitiveOperationThrottle
from admin_api.services.audit_service import AuditService
from admin_api.serializers.products import (
    AdminProductListSerializer,
    AdminProductDetailSerializer,
    StockAdjustmentSerializer,
    ProductStatusUpdateSerializer,
    LowStockProductSerializer,
    ProductFilterSerializer,
    ProductImageUploadSerializer,
    ProductImageUpdateSerializer,
    ProductImageReorderSerializer,
    ProductImageResponseSerializer,
    ProductCreateSerializer,
    ProductUpdateSerializer,
    BulkProductCreateSerializer,
    BulkProductUpdateSerializer,
)
from admin_api.serializers.auth import ErrorResponseSerializer

logger = logging.getLogger(__name__)


def generate_error_reference():
    """Generate a unique error reference for debugging."""
    return f"ERR-{secrets.token_hex(3).upper()}"


@extend_schema(
    tags=['Admin'],
    summary=_("List products"),
    description=_("""
    Get a paginated list of products with filtering and sorting.

    **Rate Limit:** 300 requests per minute

    **Stock Status Filter:**
    - all: All products (default)
    - in_stock: Products with available stock > low_stock_threshold
    - low_stock: Products with 0 < available stock <= low_stock_threshold
    - out_of_stock: Products with available stock <= 0

    **Sort Options (use 'ordering' parameter):**
    - name: Name A-Z
    - -name: Name Z-A
    - -created_at: Newest first
    - created_at: Oldest first
    - stock_quantity: Lowest stock first
    - -stock_quantity: Highest stock first
    - price: Price low to high
    - -price: Price high to low
    - -updated_at: Recently updated first
    - updated_at: Least recently updated first
    """),
    parameters=[
        OpenApiParameter(
            name='status',
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Filter by product status: 'all', 'draft', 'published', 'discontinued'"),
            required=False,
            default='all'
        ),
        OpenApiParameter(
            name='stock_status',
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Filter by stock status: 'all', 'in_stock', 'low_stock', 'out_of_stock'"),
            required=False,
            default='all'
        ),
        OpenApiParameter(
            name='search',
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Search by product name or SKU"),
            required=False
        ),
        OpenApiParameter(
            name='low_stock_only',
            type=bool,
            location=OpenApiParameter.QUERY,
            description=_("Show only low stock products (deprecated, use stock_status=low_stock)"),
            required=False,
            default=False
        ),
        OpenApiParameter(
            name='category_id',
            type=int,
            location=OpenApiParameter.QUERY,
            description=_("Filter by category ID"),
            required=False,
        ),
        OpenApiParameter(
            name='brand_id',
            type=int,
            location=OpenApiParameter.QUERY,
            description=_("Filter by brand ID"),
            required=False,
        ),
        OpenApiParameter(
            name='ordering',
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Sort field: name, -name, stock_quantity, -stock_quantity, price, -price, -created_at, created_at, -updated_at, updated_at"),
            required=False,
            default='name'
        ),
        OpenApiParameter(
            name='page',
            type=int,
            location=OpenApiParameter.QUERY,
            description=_("Page number"),
            required=False,
            default=1
        ),
        OpenApiParameter(
            name='page_size',
            type=int,
            location=OpenApiParameter.QUERY,
            description=_("Items per page (max 100)"),
            required=False,
            default=20
        ),
    ],
    responses={
        200: AdminProductListSerializer(many=True),
        401: ErrorResponseSerializer,
    }
)
@api_view(['GET'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def product_list(request):
    """
    List products with filtering and pagination.
    """
    # Validate filter parameters
    filter_serializer = ProductFilterSerializer(data=request.query_params)
    if not filter_serializer.is_valid():
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid filter parameters.'),
                'reference': generate_error_reference(),
                'details': filter_serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    filters = filter_serializer.validated_data

    # Base queryset with stock annotation
    queryset = Product.objects.select_related('category', 'brand').prefetch_related(
        'images', 'stock_items'
    ).annotate(
        _available_stock=Coalesce(
            Sum('stock_items__on_hand') - Sum('stock_items__allocated'),
            0,
            output_field=IntegerField()
        )
    )

    # Apply product status filter (draft, published, discontinued)
    product_status = filters.get('status', 'all')
    if product_status != 'all':
        queryset = queryset.filter(status=product_status)

    # Apply search
    search = filters.get('search', '').strip()
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(sku__icontains=search)
        )

    # Apply category filter
    category_id = filters.get('category_id')
    if category_id:
        queryset = queryset.filter(category_id=category_id)

    # Apply brand filter
    brand_id = filters.get('brand_id')
    if brand_id:
        queryset = queryset.filter(brand_id=brand_id)

    # Apply stock status filter (in_stock, low_stock, out_of_stock)
    stock_status = filters.get('stock_status', 'all')
    if stock_status == 'in_stock':
        # In stock: available_stock > low_stock_threshold
        queryset = queryset.filter(
            track_inventory=True,
            _available_stock__gt=F('low_stock_threshold')
        )
    elif stock_status == 'low_stock':
        # Low stock: 0 < available_stock <= low_stock_threshold
        queryset = queryset.filter(
            track_inventory=True,
            _available_stock__gt=0,
            _available_stock__lte=F('low_stock_threshold')
        )
    elif stock_status == 'out_of_stock':
        # Out of stock: available_stock <= 0
        queryset = queryset.filter(
            track_inventory=True,
            _available_stock__lte=0
        )
    # Backwards compatibility: low_stock_only parameter (deprecated)
    elif filters.get('low_stock_only', False):
        queryset = queryset.filter(
            track_inventory=True,
            _available_stock__lte=F('low_stock_threshold')
        )

    # Apply sorting - support both 'ordering' (iOS) and 'sort' (legacy) parameters
    ordering = filters.get('ordering') or filters.get('sort', 'name')
    # Map iOS parameter names to Django field names
    if ordering == 'stock_quantity':
        queryset = queryset.order_by('_available_stock')
    elif ordering == '-stock_quantity':
        queryset = queryset.order_by('-_available_stock')
    elif ordering == 'available_stock':
        queryset = queryset.order_by('_available_stock')
    elif ordering == '-available_stock':
        queryset = queryset.order_by('-_available_stock')
    elif ordering == 'price':
        queryset = queryset.order_by('price')
    elif ordering == '-price':
        queryset = queryset.order_by('-price')
    else:
        queryset = queryset.order_by(ordering)

    # Pagination
    page = filters.get('page', 1)
    page_size = filters.get('page_size', 20)
    start = (page - 1) * page_size
    end = start + page_size

    total_count = queryset.count()
    products = queryset[start:end]

    serializer = AdminProductListSerializer(products, many=True)

    return Response({
        'success': True,
        'data': {
            'products': serializer.data,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total_count': total_count,
                'total_pages': (total_count + page_size - 1) // page_size
            }
        }
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Admin'],
    summary=_("Get product details"),
    description=_("""
    Get full details of a specific product including stock levels.

    **Rate Limit:** 300 requests per minute
    """),
    responses={
        200: AdminProductDetailSerializer,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    }
)
@api_view(['GET'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def product_detail(request, product_id):
    """
    Get product details by ID.
    """
    try:
        product = Product.objects.select_related('category', 'brand').prefetch_related(
            'images', 'stock_items__warehouse'
        ).get(id=product_id)
    except Product.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 404,
                'message': _('Product not found.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = AdminProductDetailSerializer(product)

    return Response({
        'success': True,
        'data': serializer.data
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Admin'],
    summary=_("Search product by SKU"),
    description=_("""
    Search for a product by exact SKU match.

    **Rate Limit:** 300 requests per minute

    Useful for barcode scanning functionality.
    """),
    parameters=[
        OpenApiParameter(
            name='sku',
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Product SKU (exact match)"),
            required=True
        ),
    ],
    responses={
        200: AdminProductDetailSerializer,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    }
)
@api_view(['GET'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def product_by_sku(request):
    """
    Get product by SKU (for barcode scanning).
    """
    sku = request.query_params.get('sku', '').strip()
    if not sku:
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('SKU parameter is required.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Product.objects.select_related('category', 'brand').prefetch_related(
            'images', 'stock_items__warehouse'
        ).get(sku=sku)
    except Product.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 404,
                'message': _('Product not found.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = AdminProductDetailSerializer(product)

    return Response({
        'success': True,
        'data': serializer.data
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Admin'],
    summary=_("Adjust stock quantity"),
    description=_("""
    Set the stock quantity for a product.

    **Rate Limit:** 30 requests per minute (sensitive operation)

    If warehouse_id is not provided, uses the default warehouse.
    """),
    request=StockAdjustmentSerializer,
    responses={
        200: AdminProductDetailSerializer,
        400: ErrorResponseSerializer,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    }
)
@api_view(['POST'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def adjust_stock(request, product_id):
    """
    Adjust stock quantity for a product.
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 404,
                'message': _('Product not found.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_404_NOT_FOUND)

    if not product.track_inventory:
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('This product does not track inventory.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer = StockAdjustmentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid stock adjustment.'),
                'reference': generate_error_reference(),
                'details': serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    new_quantity = serializer.validated_data['quantity']
    warehouse_id = serializer.validated_data.get('warehouse_id')
    reason = serializer.validated_data.get('reason', '')

    # Get or create warehouse
    if warehouse_id:
        warehouse = Warehouse.objects.get(id=warehouse_id)
    else:
        # Get default warehouse
        warehouse = Warehouse.objects.filter(is_active=True).first()
        if not warehouse:
            return Response({
                'success': False,
                'error': {
                    'code': 400,
                    'message': _('No active warehouse available.'),
                    'reference': generate_error_reference()
                }
            }, status=status.HTTP_400_BAD_REQUEST)

    # Get or create stock item
    stock_item, created = StockItem.objects.get_or_create(
        product=product,
        warehouse=warehouse,
        variant=None,  # For simple products
        defaults={'on_hand': 0, 'allocated': 0}
    )

    old_quantity = stock_item.on_hand
    stock_item.on_hand = new_quantity
    stock_item.save()

    # Audit log
    AuditService.log_stock_adjustment(
        user=request.user,
        product=product,
        warehouse_name=warehouse.name,
        old_quantity=old_quantity,
        new_quantity=new_quantity,
        reason=reason,
        request=request
    )

    # Refresh product from DB
    product.refresh_from_db()

    return Response({
        'success': True,
        'message': _('Stock adjusted successfully.'),
        'data': AdminProductDetailSerializer(product).data
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Admin'],
    summary=_("Update product status"),
    description=_("""
    Update the status of a product (draft, published, discontinued).

    **Rate Limit:** 30 requests per minute (sensitive operation)
    """),
    request=ProductStatusUpdateSerializer,
    responses={
        200: AdminProductDetailSerializer,
        400: ErrorResponseSerializer,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    }
)
@api_view(['POST'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def update_product_status(request, product_id):
    """
    Update product status.
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 404,
                'message': _('Product not found.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductStatusUpdateSerializer(
        data=request.data,
        context={'product': product}
    )

    if not serializer.is_valid():
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid status update.'),
                'reference': generate_error_reference(),
                'details': serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    old_status = product.status
    new_status = serializer.validated_data['status']

    product.status = new_status
    product.save()

    # Audit log
    AuditService.log_product_status_change(
        user=request.user,
        product=product,
        old_status=old_status,
        new_status=new_status,
        request=request
    )

    return Response({
        'success': True,
        'message': _('Product status updated successfully.'),
        'data': AdminProductDetailSerializer(product).data
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Admin'],
    summary=_("Get low stock products"),
    description=_("""
    Get a paginated list of products with stock at or below their low stock threshold.

    **Rate Limit:** 300 requests per minute

    Products are sorted by available stock (lowest first).
    """),
    parameters=[
        OpenApiParameter(
            name='page',
            type=int,
            location=OpenApiParameter.QUERY,
            description=_("Page number"),
            required=False,
            default=1
        ),
        OpenApiParameter(
            name='page_size',
            type=int,
            location=OpenApiParameter.QUERY,
            description=_("Items per page (max 100)"),
            required=False,
            default=20
        ),
    ],
    responses={
        200: LowStockProductSerializer(many=True),
        401: ErrorResponseSerializer,
    }
)
@api_view(['GET'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def low_stock_products(request):
    """
    Get products with low stock levels with pagination.
    """
    # Parse pagination parameters
    try:
        page = int(request.query_params.get('page', 1))
        page = max(1, page)
    except (ValueError, TypeError):
        page = 1

    try:
        page_size = int(request.query_params.get('page_size', 20))
        page_size = min(max(1, page_size), 100)
    except (ValueError, TypeError):
        page_size = 20

    # Get products with low stock
    queryset = Product.objects.filter(
        track_inventory=True,
        status='published'
    ).select_related('category', 'brand').prefetch_related('images').annotate(
        _available_stock=Coalesce(
            Sum('stock_items__on_hand') - Sum('stock_items__allocated'),
            0,
            output_field=IntegerField()
        )
    ).filter(
        _available_stock__lte=F('low_stock_threshold')
    ).order_by('_available_stock')

    # Pagination
    total_count = queryset.count()
    start = (page - 1) * page_size
    end = start + page_size
    products = queryset[start:end]

    serializer = LowStockProductSerializer(products, many=True)

    return Response({
        'success': True,
        'data': {
            'products': serializer.data,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total_count': total_count,
                'total_pages': (total_count + page_size - 1) // page_size if total_count > 0 else 0
            }
        }
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Admin'],
    summary=_("Get available warehouses"),
    description=_("""
    Get a list of active warehouses for stock adjustment.

    **Rate Limit:** 300 requests per minute
    """),
    responses={
        200: dict,
        401: ErrorResponseSerializer,
    }
)
@api_view(['GET'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def warehouse_list(request):
    """
    Get list of active warehouses.
    """
    warehouses = Warehouse.objects.filter(is_active=True).values(
        'id', 'name', 'code', 'is_default'
    )

    return Response({
        'success': True,
        'data': list(warehouses)
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Admin'],
    summary=_("Get product counts by stock status"),
    description=_("""
    Get count of products by stock status for dashboard display.

    **Rate Limit:** 300 requests per minute

    Returns counts for:
    - total: All published products that track inventory
    - in_stock: Products with available stock > low_stock_threshold
    - low_stock: Products with 0 < available stock <= low_stock_threshold
    - out_of_stock: Products with no available stock
    """),
    responses={
        200: dict,
        401: ErrorResponseSerializer,
    }
)
@api_view(['GET'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def product_counts(request):
    """
    Get product counts by stock status for dashboard display.
    """
    from django.db.models import Case, When, Value, IntegerField

    # Only count published products that track inventory
    base_queryset = Product.objects.filter(
        status='published',
        track_inventory=True
    ).annotate(
        _available_stock=Coalesce(
            Sum(F('stock_items__on_hand') - F('stock_items__allocated')),
            0,
            output_field=IntegerField()
        )
    )

    total = base_queryset.count()

    # Out of stock: available_stock <= 0
    out_of_stock = base_queryset.filter(_available_stock__lte=0).count()

    # Low stock: 0 < available_stock <= low_stock_threshold
    low_stock = base_queryset.filter(
        _available_stock__gt=0,
        _available_stock__lte=F('low_stock_threshold')
    ).count()

    # In stock: available_stock > low_stock_threshold
    in_stock = base_queryset.filter(
        _available_stock__gt=F('low_stock_threshold')
    ).count()

    return Response({
        'success': True,
        'data': {
            'total': total,
            'in_stock': in_stock,
            'low_stock': low_stock,
            'out_of_stock': out_of_stock
        }
    }, status=status.HTTP_200_OK)


# ============================================================================
# Product Image Management Endpoints
# ============================================================================

@extend_schema(
    tags=['Admin'],
    summary=_("Upload product image"),
    description=_("""
    Upload a new image for a product.

    **Rate Limit:** 300 requests per minute

    The uploaded image will be:
    - Converted to WebP format for optimal delivery
    - Thumbnails generated (small: 150x150, medium: 300x300, large: 600x600)
    - Linked to the product

    **Supported formats:** JPEG, PNG, GIF, WebP
    **Max file size:** 10MB (configurable)
    """),
    request={'multipart/form-data': ProductImageUploadSerializer},
    responses={
        201: ProductImageResponseSerializer,
        400: ErrorResponseSerializer,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    }
)
@api_view(['POST'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def upload_product_image(request, product_id):
    """
    Upload a new image for a product.
    """
    from media_library.models import MediaThumbnail
    from django.conf import settings
    from PIL import Image
    import mimetypes

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 404,
                'message': _('Product not found.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductImageUploadSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid image upload.'),
                'reference': generate_error_reference(),
                'details': serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    image_file = serializer.validated_data['image']
    alt_text = serializer.validated_data.get('alt_text', '')
    is_primary = serializer.validated_data.get('is_primary', False)
    position = serializer.validated_data.get('position')

    try:
        # Extract image metadata
        image_file.seek(0)
        img = Image.open(image_file)
        width, height = img.size

        # Detect MIME type
        mime_type, _encoding = mimetypes.guess_type(image_file.name)
        if not mime_type:
            format_to_mime = {
                'JPEG': 'image/jpeg',
                'PNG': 'image/png',
                'GIF': 'image/gif',
                'WEBP': 'image/webp',
            }
            mime_type = format_to_mime.get(img.format, 'image/jpeg')

        image_file.seek(0)

        # Create MediaAsset
        media_asset = MediaAsset.objects.create(
            title=f"{product.name} - Image",
            alt_text=alt_text,
            original_file=image_file,
            mime_type=mime_type,
            file_size=image_file.size,
            width=width,
            height=height,
            uploaded_by=request.user,
        )

        # Generate WebP version
        processor = ImageProcessor()
        if mime_type != 'image/webp':
            image_file.seek(0)
            webp_content = processor.convert_to_webp(image_file)
            if webp_content:
                media_asset.webp_file.save(f"{media_asset.id}.webp", webp_content, save=True)

        # Generate thumbnails
        thumbnail_sizes = getattr(settings, 'MEDIA_LIBRARY_SETTINGS', {}).get('THUMBNAIL_SIZES', {
            'small': (150, 150),
            'medium': (300, 300),
            'large': (600, 600),
        })

        for size_name, (thumb_width, thumb_height) in thumbnail_sizes.items():
            try:
                image_file.seek(0)
                original_content, webp_content = processor.generate_thumbnail(
                    image_file, thumb_width, thumb_height
                )

                if original_content:
                    thumbnail = MediaThumbnail.objects.create(
                        media_asset=media_asset,
                        size_preset=size_name,
                        width=thumb_width,
                        height=thumb_height
                    )
                    thumbnail.file.save(f"{media_asset.id}_{size_name}.jpg", original_content, save=False)
                    if webp_content:
                        thumbnail.webp_file.save(f"{media_asset.id}_{size_name}.webp", webp_content, save=False)
                    thumbnail.save()
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Error generating thumbnail {size_name}: {e}")
                continue

        # Auto-assign position if not provided
        if position is None:
            max_position = product.images.aggregate(max_pos=Max('position'))['max_pos']
            position = (max_position or -1) + 1

        # If setting as primary, unset other primaries
        if is_primary:
            product.images.update(is_primary=False)

        # Create ProductImage linking to MediaAsset
        product_image = ProductImage.objects.create(
            product=product,
            media_asset=media_asset,
            alt_text=alt_text,
            is_primary=is_primary,
            position=position,
        )

        # Log the action
        AuditService.log(
            user=request.user,
            action='product_image.upload',
            resource_type='product_image',
            resource_id=str(product_image.id),
            new_value={
                'product_id': product_id,
                'product_name': product.name,
                'media_asset_id': str(media_asset.id),
                'is_primary': is_primary,
            },
            request=request
        )

        response_serializer = ProductImageResponseSerializer(product_image)

        return Response({
            'success': True,
            'message': _('Image uploaded successfully.'),
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Error uploading product image: {e}")
        return Response({
            'success': False,
            'error': {
                'code': 500,
                'message': _('Failed to upload image.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    tags=['Admin'],
    summary=_("Delete product image"),
    description=_("""
    Delete an image from a product.

    **Rate Limit:** 300 requests per minute

    This will remove the image association with the product.
    The underlying media asset may be retained if used elsewhere.
    """),
    responses={
        200: dict,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    }
)
@api_view(['DELETE'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def delete_product_image(request, product_id, image_id):
    """
    Delete an image from a product.
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 404,
                'message': _('Product not found.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_404_NOT_FOUND)

    try:
        product_image = ProductImage.objects.get(id=image_id, product=product)
    except ProductImage.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 404,
                'message': _('Image not found.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_404_NOT_FOUND)

    was_primary = product_image.is_primary
    media_asset = product_image.media_asset

    # Log before deletion
    AuditService.log(
        user=request.user,
        action='product_image.delete',
        resource_type='product_image',
        resource_id=str(image_id),
        old_value={
            'product_id': product_id,
            'product_name': product.name,
            'was_primary': was_primary,
        },
        request=request
    )

    # Delete the ProductImage
    product_image.delete()

    # If this was primary, set next image as primary
    if was_primary:
        next_image = product.images.order_by('position').first()
        if next_image:
            next_image.is_primary = True
            next_image.save()

    # Check if media asset is used elsewhere, if not, soft delete it
    if media_asset:
        usage_count = ProductImage.objects.filter(media_asset=media_asset).count()
        if usage_count == 0:
            media_asset.delete()  # Soft delete via SoftDeleteModel

    return Response({
        'success': True,
        'message': _('Image deleted successfully.')
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Admin'],
    summary=_("Set primary product image"),
    description=_("""
    Set an image as the primary/featured image for a product.

    **Rate Limit:** 300 requests per minute

    Only one image can be primary at a time.
    Setting a new primary will unset the previous one.
    """),
    responses={
        200: ProductImageResponseSerializer,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    }
)
@api_view(['POST'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def set_primary_image(request, product_id, image_id):
    """
    Set an image as the primary/featured image for a product.
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 404,
                'message': _('Product not found.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_404_NOT_FOUND)

    try:
        product_image = ProductImage.objects.get(id=image_id, product=product)
    except ProductImage.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 404,
                'message': _('Image not found.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_404_NOT_FOUND)

    # Unset all other primaries for this product
    product.images.update(is_primary=False)

    # Set this image as primary
    product_image.is_primary = True
    product_image.save()

    # Log the action
    AuditService.log(
        user=request.user,
        action='product_image.set_primary',
        resource_type='product_image',
        resource_id=str(image_id),
        new_value={
            'product_id': product_id,
            'product_name': product.name,
        },
        request=request
    )

    response_serializer = ProductImageResponseSerializer(product_image)

    return Response({
        'success': True,
        'message': _('Primary image updated.'),
        'data': response_serializer.data
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Admin'],
    summary=_("Reorder product images"),
    description=_("""
    Reorder the images for a product.

    **Rate Limit:** 300 requests per minute

    Provide an ordered list of image IDs. The first ID will be position 0, second will be position 1, etc.
    All image IDs must belong to the specified product.
    """),
    request=ProductImageReorderSerializer,
    responses={
        200: ProductImageResponseSerializer(many=True),
        400: ErrorResponseSerializer,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    }
)
@api_view(['POST'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def reorder_product_images(request, product_id):
    """
    Reorder images for a product.
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 404,
                'message': _('Product not found.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductImageReorderSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid reorder request.'),
                'reference': generate_error_reference(),
                'details': serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    image_ids = serializer.validated_data['image_ids']

    # Verify all IDs belong to this product
    product_image_ids = set(product.images.values_list('id', flat=True))
    provided_ids = set(image_ids)

    if not provided_ids.issubset(product_image_ids):
        invalid_ids = provided_ids - product_image_ids
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Some image IDs do not belong to this product.'),
                'reference': generate_error_reference(),
                'details': {'invalid_ids': list(invalid_ids)}
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    # Update positions
    for position, image_id in enumerate(image_ids):
        ProductImage.objects.filter(id=image_id).update(position=position)

    # Log the action
    AuditService.log(
        user=request.user,
        action='product_image.reorder',
        resource_type='product',
        resource_id=str(product_id),
        new_value={
            'product_name': product.name,
            'new_order': image_ids,
        },
        request=request
    )

    # Get updated images
    images = product.images.order_by('position')
    response_serializer = ProductImageResponseSerializer(images, many=True)

    return Response({
        'success': True,
        'message': _('Images reordered successfully.'),
        'data': response_serializer.data
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Admin'],
    summary=_("Update product image"),
    description=_("""
    Update metadata for a product image (alt text).

    **Rate Limit:** 30 requests per minute (sensitive operation)
    """),
    request=ProductImageUpdateSerializer,
    responses={
        200: ProductImageResponseSerializer,
        400: ErrorResponseSerializer,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    }
)
@api_view(['PATCH'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def update_product_image(request, product_id, image_id):
    """
    Update metadata for a product image.
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 404,
                'message': _('Product not found.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_404_NOT_FOUND)

    try:
        product_image = ProductImage.objects.get(id=image_id, product=product)
    except ProductImage.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 404,
                'message': _('Image not found.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductImageUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid update request.'),
                'reference': generate_error_reference(),
                'details': serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    # Update alt text on both ProductImage and MediaAsset
    if 'alt_text' in serializer.validated_data:
        new_alt_text = serializer.validated_data['alt_text']
        product_image.alt_text = new_alt_text
        product_image.save()

        if product_image.media_asset:
            product_image.media_asset.alt_text = new_alt_text
            product_image.media_asset.save()

    # Log the action
    AuditService.log(
        user=request.user,
        action='product_image.update',
        resource_type='product_image',
        resource_id=str(image_id),
        new_value={
            'product_id': product_id,
            'product_name': product.name,
            'updated_fields': list(serializer.validated_data.keys()),
        },
        request=request
    )

    response_serializer = ProductImageResponseSerializer(product_image)

    return Response({
        'success': True,
        'message': _('Image updated successfully.'),
        'data': response_serializer.data
    }, status=status.HTTP_200_OK)


# --- Product CRUD Endpoints ---

def _generate_unique_product_slug(name, exclude_id=None):
    """Generate a unique slug for a product, appending -2, -3, etc. if needed."""
    base_slug = slugify(name)
    if not base_slug:
        base_slug = 'product'
    slug = base_slug
    counter = 2
    while True:
        qs = Product.objects.filter(slug=slug)
        if exclude_id:
            qs = qs.exclude(id=exclude_id)
        if not qs.exists():
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1


def _create_single_product(data, user=None):
    """
    Create a single product from validated data dict. Returns the Product instance.
    Used by both single create and bulk create to avoid duplication.
    """
    currency = data.get('currency') or get_default_currency()
    slug = _generate_unique_product_slug(data['name'])

    product = Product(
        name=data['name'],
        slug=slug,
        sku=data['sku'],
        product_type=data.get('product_type', 'simple'),
        status=data.get('status', 'draft'),
        category_id=data['category_id'],
        brand_id=data.get('brand_id'),
        short_description=data.get('short_description', ''),
        full_description=data.get('full_description', ''),
        track_inventory=data.get('track_inventory', True),
        low_stock_threshold=data.get('low_stock_threshold', 5),
        allow_backorders=data.get('allow_backorders', False),
        weight=data.get('weight'),
        length=data.get('length'),
        width=data.get('width'),
        height=data.get('height'),
        meta_title=data.get('meta_title', ''),
        meta_description=data.get('meta_description', ''),
        features=data.get('features', {}),
        specifications=data.get('specifications', {}),
        is_featured=data.get('is_featured', False),
        sale_type=data.get('sale_type', 'none'),
        sale_value=data.get('sale_value'),
        external_id=data.get('external_id', ''),
    )
    product.price = Money(Decimal(str(data['price'])), currency)

    # Include pre-generated translations if provided
    if 'translations' in data and isinstance(data['translations'], dict):
        product.translations = data['translations']

    product.save()

    # Auto-create StockItem for default warehouse
    if product.track_inventory:
        warehouse = Warehouse.objects.filter(is_active=True).first()
        if warehouse:
            initial_stock = data.get('initial_stock', 0)
            StockItem.objects.create(
                product=product,
                warehouse=warehouse,
                variant=None,
                on_hand=initial_stock,
                allocated=0,
            )

    return product


@extend_schema(
    tags=['Admin - Products'],
    summary=_("Create product"),
    description=_("""
    Create a new product. Images should be uploaded separately via the image upload endpoint.
    If `track_inventory` is true (default), a StockItem is auto-created for the default warehouse
    with `initial_stock` quantity (default 0).

    **Rate Limit:** 30 requests per minute (sensitive operation)
    """),
    request=ProductCreateSerializer,
    responses={201: AdminProductDetailSerializer, 400: ErrorResponseSerializer, 409: ErrorResponseSerializer}
)
@api_view(['POST'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def create_product(request):
    """Create a new product."""
    serializer = ProductCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid product data.'),
                'reference': generate_error_reference(),
                'details': serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            product = _create_single_product(serializer.validated_data, user=request.user)
    except IntegrityError:
        return Response({
            'success': False,
            'error': {
                'code': 409,
                'message': _('A product with this SKU or slug already exists.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_409_CONFLICT)

    AuditService.log_product_create(
        user=request.user,
        product=product,
        request=request
    )

    # Re-fetch with annotations for response
    product = Product.objects.select_related('category', 'brand').prefetch_related(
        'images', 'stock_items', 'stock_items__warehouse'
    ).annotate(
        _available_stock=Coalesce(
            Sum('stock_items__on_hand') - Sum('stock_items__allocated'), 0,
            output_field=IntegerField()
        )
    ).get(id=product.id)

    return Response({
        'success': True,
        'message': _('Product created successfully.'),
        'data': AdminProductDetailSerializer(product).data
    }, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=['Admin - Products'],
    summary=_("Update product"),
    description=_("""
    Partially update a product. Only provided fields will be changed.
    If `name` is changed and no explicit `slug` is in the payload, the slug is regenerated.

    **Rate Limit:** 30 requests per minute (sensitive operation)
    """),
    request=ProductUpdateSerializer,
    responses={200: AdminProductDetailSerializer, 400: ErrorResponseSerializer, 404: ErrorResponseSerializer}
)
@api_view(['PATCH'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def update_product(request, product_id):
    """Partially update a product."""
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 404,
                'message': _('Product not found.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductUpdateSerializer(data=request.data, context={'product': product})
    if not serializer.is_valid():
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid product data.'),
                'reference': generate_error_reference(),
                'details': serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    old_values = {}
    new_values = {}
    update_fields = []

    # Simple fields
    simple_fields = [
        'name', 'sku', 'product_type', 'status', 'short_description', 'full_description',
        'track_inventory', 'low_stock_threshold', 'allow_backorders',
        'weight', 'length', 'width', 'height',
        'meta_title', 'meta_description', 'features', 'specifications',
        'is_featured', 'sale_type', 'sale_value',
    ]
    for field in simple_fields:
        if field in data:
            old_val = getattr(product, field)
            # Convert Decimal to string for JSON serialization in audit
            old_values[field] = str(old_val) if isinstance(old_val, Decimal) else old_val
            setattr(product, field, data[field])
            new_val = data[field]
            new_values[field] = str(new_val) if isinstance(new_val, Decimal) else new_val
            update_fields.append(field)

    # FK fields
    if 'category_id' in data:
        old_values['category_id'] = product.category_id
        product.category_id = data['category_id']
        new_values['category_id'] = data['category_id']
        update_fields.append('category_id')

    if 'brand_id' in data:
        old_values['brand_id'] = product.brand_id
        product.brand_id = data['brand_id']
        new_values['brand_id'] = data['brand_id']
        update_fields.append('brand_id')

    # Price (MoneyField)
    if 'price' in data:
        old_values['price'] = str(product.price.amount) if product.price else None
        old_values['currency'] = str(product.price.currency) if product.price else None
        currency = data.get('currency') or (str(product.price.currency) if product.price else get_default_currency())
        product.price = Money(Decimal(str(data['price'])), currency)
        new_values['price'] = str(data['price'])
        new_values['currency'] = currency
        update_fields.extend(['price', 'price_currency'])

    # Slug regeneration
    if 'name' in data:
        old_values['slug'] = product.slug
        product.slug = _generate_unique_product_slug(data['name'], exclude_id=product.id)
        new_values['slug'] = product.slug
        update_fields.append('slug')

    if update_fields:
        try:
            product.save(update_fields=list(set(update_fields)) + ['updated_at'])
        except IntegrityError:
            return Response({
                'success': False,
                'error': {
                    'code': 409,
                    'message': _('A product with this SKU or slug already exists.'),
                    'reference': generate_error_reference()
                }
            }, status=status.HTTP_409_CONFLICT)

        AuditService.log_product_update(
            user=request.user,
            product=product,
            old_values=old_values,
            new_values=new_values,
            request=request
        )

    # Re-fetch with annotations
    product = Product.objects.select_related('category', 'brand').prefetch_related(
        'images', 'stock_items', 'stock_items__warehouse'
    ).annotate(
        _available_stock=Coalesce(
            Sum('stock_items__on_hand') - Sum('stock_items__allocated'), 0,
            output_field=IntegerField()
        )
    ).get(id=product.id)

    return Response({
        'success': True,
        'message': _('Product updated successfully.'),
        'data': AdminProductDetailSerializer(product).data
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Admin - Products'],
    summary=_("Delete product"),
    description=_("""
    Soft-delete a product. The product will be hidden from all queries but can be restored.

    **Rate Limit:** 30 requests per minute (sensitive operation)
    """),
    responses={200: None, 404: ErrorResponseSerializer}
)
@api_view(['DELETE'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def delete_product(request, product_id):
    """Soft-delete a product."""
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 404,
                'message': _('Product not found.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_404_NOT_FOUND)

    AuditService.log_product_delete(
        user=request.user,
        product=product,
        request=request
    )

    product.delete(user=request.user)

    return Response({
        'success': True,
        'message': _('Product "%(name)s" deleted successfully.') % {'name': product.name},
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Admin - Products'],
    summary=_("Bulk create products"),
    description=_("""
    Create multiple products in a single request. Maximum 100 products per request.
    Individual failures do not rollback the entire batch.

    **Rate Limit:** 30 requests per minute (sensitive operation)
    """),
    request=BulkProductCreateSerializer,
    responses={201: None, 400: ErrorResponseSerializer}
)
@api_view(['POST'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def bulk_create_products(request):
    """Bulk create products."""
    wrapper_serializer = BulkProductCreateSerializer(data=request.data)
    if not wrapper_serializer.is_valid():
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid bulk product data.'),
                'reference': generate_error_reference(),
                'details': wrapper_serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    items = wrapper_serializer.validated_data['products']
    created_count = 0
    errors = []

    for index, item_data in enumerate(items):
        try:
            with transaction.atomic():
                _create_single_product(item_data, user=request.user)
                created_count += 1
        except Exception as e:
            errors.append({
                'index': index,
                'name': item_data.get('name', ''),
                'sku': item_data.get('sku', ''),
                'error': str(e)
            })

    AuditService.log_bulk_operation(
        user=request.user,
        action='product.bulk_create',
        resource_type='product',
        created_count=created_count,
        error_count=len(errors),
        request=request
    )

    status_code = status.HTTP_201_CREATED if created_count > 0 else status.HTTP_400_BAD_REQUEST
    return Response({
        'success': created_count > 0,
        'message': _('Created %(created)d product(s). %(errors)d failed.') % {
            'created': created_count, 'errors': len(errors)
        },
        'data': {
            'created_count': created_count,
            'error_count': len(errors),
            'errors': errors
        }
    }, status=status_code)


@extend_schema(
    tags=['Admin - Products'],
    summary=_("Bulk update products"),
    description=_("""
    Update multiple products in a single request. Maximum 100 products per request.
    Each product object must include an `id` field plus the fields to update.
    Individual failures do not rollback the entire batch.

    **Rate Limit:** 30 requests per minute (sensitive operation)
    """),
    request=BulkProductUpdateSerializer,
    responses={200: None, 400: ErrorResponseSerializer}
)
@api_view(['PATCH'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def bulk_update_products(request):
    """Bulk update products."""
    wrapper_serializer = BulkProductUpdateSerializer(data=request.data)
    if not wrapper_serializer.is_valid():
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid bulk update data.'),
                'reference': generate_error_reference(),
                'details': wrapper_serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    items = wrapper_serializer.validated_data['products']
    updated_count = 0
    errors = []

    for index, item_data in enumerate(items):
        product_id = item_data.pop('id')
        try:
            with transaction.atomic():
                product = Product.objects.get(id=product_id)
                update_serializer = ProductUpdateSerializer(
                    data=item_data, context={'product': product}
                )
                if not update_serializer.is_valid():
                    errors.append({
                        'index': index,
                        'id': product_id,
                        'error': update_serializer.errors
                    })
                    continue

                data = update_serializer.validated_data
                update_fields = []

                simple_fields = [
                    'name', 'sku', 'product_type', 'status',
                    'short_description', 'full_description',
                    'track_inventory', 'low_stock_threshold', 'allow_backorders',
                    'weight', 'length', 'width', 'height',
                    'meta_title', 'meta_description', 'features', 'specifications',
                    'is_featured', 'sale_type', 'sale_value',
                ]
                for field in simple_fields:
                    if field in data:
                        setattr(product, field, data[field])
                        update_fields.append(field)

                if 'category_id' in data:
                    product.category_id = data['category_id']
                    update_fields.append('category_id')
                if 'brand_id' in data:
                    product.brand_id = data['brand_id']
                    update_fields.append('brand_id')

                if 'price' in data:
                    currency = data.get('currency') or (
                        str(product.price.currency) if product.price else get_default_currency()
                    )
                    product.price = Money(Decimal(str(data['price'])), currency)
                    update_fields.extend(['price', 'price_currency'])

                if 'name' in data:
                    product.slug = _generate_unique_product_slug(data['name'], exclude_id=product.id)
                    update_fields.append('slug')

                if update_fields:
                    product.save(update_fields=list(set(update_fields)) + ['updated_at'])

                updated_count += 1
        except Product.DoesNotExist:
            errors.append({
                'index': index,
                'id': product_id,
                'error': 'Product not found.'
            })
        except Exception as e:
            errors.append({
                'index': index,
                'id': product_id,
                'error': str(e)
            })

    AuditService.log_bulk_operation(
        user=request.user,
        action='product.bulk_update',
        resource_type='product',
        created_count=updated_count,
        error_count=len(errors),
        request=request
    )

    status_code = status.HTTP_200_OK if updated_count > 0 else status.HTTP_400_BAD_REQUEST
    return Response({
        'success': updated_count > 0,
        'message': _('Updated %(updated)d product(s). %(errors)d failed.') % {
            'updated': updated_count, 'errors': len(errors)
        },
        'data': {
            'updated_count': updated_count,
            'error_count': len(errors),
            'errors': errors
        }
    }, status=status_code)
