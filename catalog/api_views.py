"""
DRF API Views for Catalog
Provides customer-facing endpoints for products, categories, brands, collections, and reviews
Includes multi-language support via django-modeltranslation and Accept-Language header
"""
from rest_framework import viewsets, status, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from core.api.authentication import HeadlessAPIMixin
from django.db.models import Q, Avg, Count, Prefetch
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language, activate, gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse, OpenApiParameter
from core.api.api_descriptions import PRODUCT_NOT_FOUND

from core.utils import get_default_currency
from .models import (
    Category,
    Brand,
    Product,
    ProductImage,
    ProductVariant,
    ProductReview,
    Collection,
    Warehouse,
    StockItem,
    ProductAttribute,
    AttributeValue,
    ProductAttributeAssignment,
    StockDisplaySettings,
    StockNotification,
    ConfigurationSlot,
    ConfigurationSlotOption,
    CompatibilityRule,
    ConfigurationPreset,
)
from .serializers import (
    CategoryListSerializer,
    CategoryDetailSerializer,
    BrandSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ProductReviewSerializer,
    CollectionSerializer,
    WarehouseSerializer,
    StockAvailabilitySerializer,
    ProductAttributeSerializer,
    AttributeValueSerializer,
    ProductVariantSerializer,
    ConfigurationSlotSerializer,
    CompatibilityRuleSerializer,
    ConfigurationPresetSerializer,
    ConfiguratorDataSerializer,
    ConfigurationSelectionSerializer,
    ConfiguratorValidationResponseSerializer,
    ConfiguratorPriceResponseSerializer,
)
from .filters import ProductFilter


@extend_schema_view(
    list=extend_schema(tags=['Catalog'], summary=_("List all categories")),
    retrieve=extend_schema(tags=['Catalog'], summary=_("Get category details")),
    tree=extend_schema(tags=['Catalog'], summary=_("Get categories as tree structure")),
    products=extend_schema(tags=['Catalog'], summary=_("Get products in category"))
)
class CategoryViewSet(HeadlessAPIMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for categories

    list: Get all categories (tree structure preserved via parent field)
    retrieve: Get single category with subcategories and products

    Supports multi-language via Accept-Language header

    Categories are a small, finite dataset (typically < 100 items) so we
    allow page_size up to 200. Headless frontends need the full tree in
    one request to build navigation menus and collection pages.
    """
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    class CategoryPagination(PageNumberPagination):
        page_size = 100
        page_size_query_param = 'page_size'
        max_page_size = 200

    pagination_class = CategoryPagination

    def get_queryset(self):
        """Get categories with optimized queries.

        Includes active categories AND any inactive parents that have active
        children, so the hierarchy tree is never broken by orphaned nodes.
        """
        # Include active categories + inactive structural parents
        # (parents that have at least one active child)
        structural_parent_ids = Category.objects.filter(
            is_active=False,
            children__is_active=True,
        ).values_list('id', flat=True)

        queryset = Category.objects.filter(
            Q(is_active=True) | Q(id__in=structural_parent_ids)
        )

        # Prefetch children for tree structure
        queryset = queryset.prefetch_related(
            Prefetch('children', queryset=Category.objects.filter(is_active=True))
        )

        # Prefetch products for counts
        queryset = queryset.prefetch_related(
            Prefetch('products', queryset=Product.objects.filter(status='published'))
        )

        return queryset.order_by('sort_order', 'name')

    def get_serializer_class(self):
        """Use detailed serializer for retrieve, list serializer for list"""
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return CategoryListSerializer

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """
        Get categories as a tree structure (only root categories with nested children)
        """
        root_categories = self.get_queryset().filter(parent__isnull=True)
        serializer = CategoryDetailSerializer(root_categories, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def products(self, request, slug=None):
        """
        Get products in a specific category
        Supports filtering, sorting, pagination
        Region-aware: only shows products visible and in-stock in visitor's region
        """
        category = self.get_object()

        # Get products in this category and subcategories
        products = Product.objects.filter(
            Q(category=category) | Q(category__parent=category),
            status='published',
            is_deleted=False
        ).select_related('category', 'brand').prefetch_related('images')

        # Apply region filtering
        region = self._get_request_region()
        if region:
            products = self._filter_by_region(products, region)

        # Apply filters
        filterset = ProductFilter(request.query_params, queryset=products)
        if filterset.is_valid():
            products = filterset.qs

        # Sorting
        sort = request.query_params.get('sort', '-created_at')
        allowed_sorts = ['price', '-price', 'name', '-name', 'created_at', '-created_at', 'sales_count', '-sales_count']
        if sort in allowed_sorts:
            products = products.order_by(sort)

        # Paginate
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

    def _get_request_region(self):
        """Get the sales region from the request"""
        if hasattr(self.request, 'sales_region'):
            try:
                return self.request.sales_region if self.request.sales_region else None
            except Exception:
                pass
        return None

    def _filter_by_region(self, queryset, region):
        """Filter products by region visibility and stock availability"""
        from .models import ProductRegionVisibility

        # Get products with no visibility rules (visible everywhere)
        products_without_rules = queryset.exclude(
            id__in=ProductRegionVisibility.objects.values_list('product_id', flat=True)
        )

        # Get products with explicit visibility=True for this region
        products_with_visibility = queryset.filter(
            region_visibility__region=region,
            region_visibility__is_visible=True
        )

        # Combine both querysets
        visible_products = products_without_rules | products_with_visibility

        # Filter to only products with stock in this region
        products_with_stock = visible_products.filter(
            Q(track_inventory=False) |
            Q(
                stock_items__warehouse__region=region,
                stock_items__warehouse__is_active=True,
                stock_items__on_hand__gt=0
            )
        ).distinct()

        return products_with_stock


@extend_schema_view(
    list=extend_schema(tags=['Catalog'], summary=_("List all brands")),
    retrieve=extend_schema(tags=['Catalog'], summary=_("Get brand details")),
    products=extend_schema(tags=['Catalog'], summary=_("Get brand products"))
)
class BrandViewSet(HeadlessAPIMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for brands

    list: Get all brands
    retrieve: Get single brand with products

    Supports multi-language via Accept-Language header
    """
    queryset = Brand.objects.filter(is_active=True).order_by('name')
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    @action(detail=True, methods=['get'])
    def products(self, request, slug=None):
        """
        Get products for a specific brand
        Supports filtering, sorting, pagination
        Region-aware: only shows products visible and in-stock in visitor's region
        """
        brand = self.get_object()

        products = Product.objects.filter(
            brand=brand,
            status='published',
            is_deleted=False
        ).select_related('category', 'brand').prefetch_related('images')

        # Apply region filtering
        region = self._get_request_region()
        if region:
            products = self._filter_by_region(products, region)

        # Apply filters
        filterset = ProductFilter(request.query_params, queryset=products)
        if filterset.is_valid():
            products = filterset.qs

        # Sorting
        sort = request.query_params.get('sort', '-created_at')
        allowed_sorts = ['price', '-price', 'name', '-name', 'created_at', '-created_at', 'sales_count', '-sales_count']
        if sort in allowed_sorts:
            products = products.order_by(sort)

        # Paginate
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

    def _get_request_region(self):
        """Get the sales region from the request"""
        if hasattr(self.request, 'sales_region'):
            try:
                return self.request.sales_region if self.request.sales_region else None
            except Exception:
                pass
        return None

    def _filter_by_region(self, queryset, region):
        """Filter products by region visibility and stock availability"""
        from .models import ProductRegionVisibility

        # Get products with no visibility rules (visible everywhere)
        products_without_rules = queryset.exclude(
            id__in=ProductRegionVisibility.objects.values_list('product_id', flat=True)
        )

        # Get products with explicit visibility=True for this region
        products_with_visibility = queryset.filter(
            region_visibility__region=region,
            region_visibility__is_visible=True
        )

        # Combine both querysets
        visible_products = products_without_rules | products_with_visibility

        # Filter to only products with stock in this region
        products_with_stock = visible_products.filter(
            Q(track_inventory=False) |
            Q(
                stock_items__warehouse__region=region,
                stock_items__warehouse__is_active=True,
                stock_items__on_hand__gt=0
            )
        ).distinct()

        return products_with_stock


@extend_schema_view(
    list=extend_schema(tags=['Catalog'], summary=_("List all product attributes")),
    retrieve=extend_schema(tags=['Catalog'], summary=_("Get attribute details with values"))
)
class ProductAttributeViewSet(HeadlessAPIMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for product attributes

    list: Get all product attributes with their values
    retrieve: Get single attribute with all available values

    Supports multi-language via Accept-Language header
    """
    queryset = ProductAttribute.objects.all().prefetch_related('values').order_by('sort_order', 'name')
    serializer_class = ProductAttributeSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


@extend_schema_view(
    list=extend_schema(tags=['Catalog'], summary=_("List all products")),
    retrieve=extend_schema(tags=['Catalog'], summary=_("Get product details")),
    track_view=extend_schema(tags=['Catalog'], summary=_("Track product view")),
    featured=extend_schema(tags=['Catalog'], summary=_("Get featured products")),
    search=extend_schema(tags=['Catalog'], summary=_("Search products")),
    recently_viewed=extend_schema(tags=['Catalog'], summary=_("Get recently viewed products")),
    get_variant_by_attributes=extend_schema(tags=['Catalog'], summary=_("Find variant by attribute selection")),
    customization_options=extend_schema(tags=['Catalog'], summary=_("Get product customization options")),
    validate_customizations=extend_schema(tags=['Catalog'], summary=_("Validate customization values")),
    configurator=extend_schema(tags=['Catalog'], summary=_("Get configurator data")),
    configurator_validate=extend_schema(tags=['Catalog'], summary=_("Validate configuration")),
    configurator_price=extend_schema(tags=['Catalog'], summary=_("Calculate configuration price")),
    configurator_presets=extend_schema(tags=['Catalog'], summary=_("Get configuration presets")),
)
class ProductViewSet(HeadlessAPIMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for products

    list: Get all products with filtering, search, sorting
    retrieve: Get single product with full details
    search: Full-text search across products
    featured: Get featured products
    track_view: Track product views
    recently_viewed: Get recently viewed products

    Supports multi-language via Accept-Language header
    """
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'short_description', 'sku']
    ordering_fields = ['price', 'name', 'created_at', 'sales_count', 'views_count']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Get products with optimized queries, filtered by region visibility.

        Automatically excludes soft-deleted products via Product.objects manager.
        Explicit is_deleted=False filter added for safety.
        """
        queryset = Product.objects.filter(
            status='published',
            hide_from_storefront=False,
            is_deleted=False,  # Explicit filter for soft-deleted products
        ).exclude(sales_channel='pos_only')

        # Filter by region visibility
        region = self._get_request_region()
        if region:
            queryset = self._filter_by_region(queryset, region)

        # Select related for foreign keys
        queryset = queryset.select_related('category', 'brand')

        # Prefetch related for many-to-many and reverse foreign keys
        queryset = queryset.prefetch_related(
            Prefetch('images', queryset=ProductImage.objects.filter(show_in_listing=True)),
            Prefetch('variants', queryset=ProductVariant.objects.filter(is_active=True)),
            'reviews',
            'stock_items',  # Prefetch stock items for availability checks
            'stock_items__warehouse',  # Prefetch warehouses
            'region_visibility',  # Prefetch region visibility rules
            'customization_options'  # Prefetch customization options
        )

        return queryset

    def _get_request_region(self):
        """Get the sales region from the request"""
        if hasattr(self.request, 'sales_region'):
            try:
                return self.request.sales_region if self.request.sales_region else None
            except Exception:
                pass
        return None

    def _filter_by_region(self, queryset, region):
        """
        Filter products by region visibility and stock availability.
        Delegates to ProductQuerySet.available_in_region() for centralized logic.
        """
        return queryset.available_in_region(region)

    def get_serializer_class(self):
        """Use detailed serializer for retrieve, list serializer for list"""
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Get single product and track view
        """
        instance = self.get_object()

        # Track view (increment views_count)
        instance.views_count += 1
        instance.save(update_fields=['views_count'])

        # Store in recently viewed (session)
        if 'recently_viewed' not in request.session:
            request.session['recently_viewed'] = []

        recently_viewed = request.session['recently_viewed']
        product_id = instance.id

        # Remove if already exists (to move to front)
        if product_id in recently_viewed:
            recently_viewed.remove(product_id)

        # Add to front
        recently_viewed.insert(0, product_id)

        # Keep only last 20
        request.session['recently_viewed'] = recently_viewed[:20]

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Get featured products
        """
        products = self.get_queryset().filter(is_featured=True)[:12]
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Full-text search across products
        Query params:
        - q: search query (required)
        - category: filter by category slug
        - brand: filter by brand slug
        - min_price: minimum price
        - max_price: maximum price
        - in_stock: filter by stock status (true/false)
        """
        query = request.query_params.get('q', '').strip()

        if not query:
            return Response({
                'error': 'Search query is required',
                'results': []
            }, status=status.HTTP_400_BAD_REQUEST)

        # Base search
        products = self.get_queryset().filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(short_description__icontains=query) |
            Q(sku__icontains=query) |
            Q(category__name__icontains=query) |
            Q(brand__name__icontains=query)
        )

        # Apply additional filters
        category_slug = request.query_params.get('category')
        if category_slug:
            products = products.filter(category__slug=category_slug)

        brand_slug = request.query_params.get('brand')
        if brand_slug:
            products = products.filter(brand__slug=brand_slug)

        min_price = request.query_params.get('min_price')
        if min_price:
            products = products.filter(price__gte=min_price)

        max_price = request.query_params.get('max_price')
        if max_price:
            products = products.filter(price__lte=max_price)

        in_stock = request.query_params.get('in_stock')
        if in_stock and in_stock.lower() == 'true':
            products = products.filter(
                Q(track_inventory=False) |
                Q(track_inventory=True, quantity__gt=0)
            )

        # Sorting
        sort = request.query_params.get('sort', '-created_at')
        allowed_sorts = ['price', '-price', 'name', '-name', 'created_at', '-created_at', 'sales_count', '-sales_count']
        if sort in allowed_sorts:
            products = products.order_by(sort)

        # Paginate
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response({
            'query': query,
            'count': products.count(),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'])
    def recently_viewed(self, request):
        """
        Get recently viewed products from session
        """
        recently_viewed_ids = request.session.get('recently_viewed', [])

        if not recently_viewed_ids:
            return Response([])

        # Get products maintaining order
        products = Product.objects.filter(
            id__in=recently_viewed_ids,
            status='published',
            is_deleted=False
        ).select_related('category', 'brand').prefetch_related('images')

        # Sort by recently_viewed order
        products_dict = {p.id: p for p in products}
        ordered_products = [products_dict[pid] for pid in recently_viewed_ids if pid in products_dict]

        serializer = ProductListSerializer(ordered_products, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def track_view(self, request, slug=None):
        """
        Explicitly track a product view (alternative to automatic tracking in retrieve)
        """
        product = self.get_object()
        product.views_count += 1
        product.save(update_fields=['views_count'])

        return Response({
            'success': True,
            'views_count': product.views_count
        })

    @action(detail=True, methods=['post'])
    def get_variant_by_attributes(self, request, slug=None):
        """
        Find the matching product variant based on selected attribute values.

        Request body should contain a mapping of attribute slugs to value slugs:
        {
            "size": "large",
            "color": "red"
        }

        Returns the matching variant with stock information, or 404 if no match found.
        """
        product = self.get_object()

        # Get selected attributes from request body
        selected_attrs = request.data

        if not selected_attrs:
            return Response(
                {'error': 'No attributes provided. Please provide attribute selections.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get attribute IDs from slugs
        attribute_slugs = list(selected_attrs.keys())
        attributes = ProductAttribute.objects.filter(slug__in=attribute_slugs)
        attribute_map = {attr.slug: attr.id for attr in attributes}

        # Get value IDs from slugs
        value_slugs = list(selected_attrs.values())
        values = AttributeValue.objects.filter(slug__in=value_slugs)
        value_map = {val.slug: val.id for val in values}

        # Build the expected set of attribute value IDs
        try:
            expected_value_ids = set()
            for attr_slug, val_slug in selected_attrs.items():
                if attr_slug not in attribute_map:
                    return Response(
                        {'error': f'Unknown attribute: {attr_slug}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if val_slug not in value_map:
                    return Response(
                        {'error': f'Unknown value: {val_slug}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                expected_value_ids.add(value_map[val_slug])
        except Exception as e:
            return Response(
                {'error': f'Invalid attribute selection: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Find variants with exact attribute match
        variants = product.variants.filter(is_active=True).prefetch_related('selected_attributes')

        matching_variant = None
        for variant in variants:
            variant_value_ids = set(variant.selected_attributes.values_list('id', flat=True))
            if variant_value_ids == expected_value_ids:
                matching_variant = variant
                break

        if not matching_variant:
            return Response(
                {'error': 'No variant found matching the selected attributes'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize the variant
        serializer = ProductVariantSerializer(matching_variant, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def customization_options(self, request, slug=None):
        """
        Get all customization options for a product.
        Returns options sorted by sort_order with validation rules and pricing.
        """
        product = self.get_object()

        # Check if product allows customization
        if not product.allow_customization:
            return Response({
                'allow_customization': False,
                'options': []
            })

        # Get all customization options for this product
        options = product.customization_options.all().order_by('sort_order')

        from .serializers import CustomizationOptionSerializer
        serializer = CustomizationOptionSerializer(options, many=True, context={'request': request})

        return Response({
            'allow_customization': True,
            'options': serializer.data
        })

    @action(detail=True, methods=['post'])
    def validate_customizations(self, request, slug=None):
        """
        Validate customization values before adding to cart.

        Request body should contain customizations in the format:
        {
            "customizations": {
                "option_id": "value",
                "option_id": "value"
            }
        }

        Returns validation result with calculated prices.
        """
        product = self.get_object()

        # Check if product allows customization
        if not product.allow_customization:
            return Response({
                'valid': False,
                'errors': ['This product does not support customization']
            }, status=status.HTTP_400_BAD_REQUEST)

        customizations = request.data.get('customizations', {})

        # Use CartService validation logic
        from cart.services.cart_service import CartService

        is_valid, error_msg, validated_customizations = CartService._validate_customizations(
            product=product,
            customizations=customizations
        )

        if not is_valid:
            return Response({
                'valid': False,
                'errors': [error_msg]
            }, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total customization price
        from djmoney.money import Money
        from decimal import Decimal

        total_customization_price = Decimal('0.00')
        for option_id, customization_data in validated_customizations.items():
            total_customization_price += Decimal(customization_data['calculated_price'])

        return Response({
            'valid': True,
            'validated_customizations': validated_customizations,
            'total_customization_price': {
                'amount': str(total_customization_price),
                'currency': product.price.currency.code
            },
            'total_product_price': {
                'amount': str(product.price.amount + total_customization_price),
                'currency': product.price.currency.code
            }
        })

    # ========================================================================
    # Enhanced Product Discovery Endpoints (Headless Frontend APIs)
    # ========================================================================

    @extend_schema(
        tags=['Catalog'],
        summary=_("Get trending products"),
        description=_("Get products sorted by views in the last 7 days."),
        parameters=[
            OpenApiParameter('limit', int, description=_('Number of products (default: 12, max: 50)')),
        ]
    )
    @action(detail=False, methods=['get'])
    def trending(self, request):
        """
        Get trending products based on recent views.

        Returns products with highest views_count, filtered by recent activity.
        """
        limit = min(int(request.query_params.get('limit', 12)), 50)

        # Get products ordered by views (proxy for trending)
        products = self.get_queryset().order_by('-views_count')[:limit]

        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data
        })

    @extend_schema(
        tags=['Catalog'],
        summary=_("Get bestseller products"),
        description=_("Get top-selling products based on sales count."),
        parameters=[
            OpenApiParameter('limit', int, description=_('Number of products (default: 12, max: 50)')),
            OpenApiParameter('period', str, description=_('Time period: all, month, week (default: all)')),
        ]
    )
    @action(detail=False, methods=['get'])
    def bestsellers(self, request):
        """
        Get bestselling products based on sales count.
        """
        limit = min(int(request.query_params.get('limit', 12)), 50)

        # Get products ordered by sales count
        products = self.get_queryset().order_by('-sales_count')[:limit]

        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data
        })

    @extend_schema(
        tags=['Catalog'],
        summary=_("Get new arrival products"),
        description=_("Get recently added products."),
        parameters=[
            OpenApiParameter('limit', int, description=_('Number of products (default: 12, max: 50)')),
            OpenApiParameter('days', int, description=_('Products added in last N days (default: 30)')),
        ]
    )
    @action(detail=False, methods=['get'], url_path='new-arrivals')
    def new_arrivals(self, request):
        """
        Get recently added products.
        """
        from django.utils import timezone
        from datetime import timedelta

        limit = min(int(request.query_params.get('limit', 12)), 50)
        days = min(int(request.query_params.get('days', 30)), 90)

        cutoff_date = timezone.now() - timedelta(days=days)

        products = self.get_queryset().filter(
            created_at__gte=cutoff_date
        ).order_by('-created_at')[:limit]

        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data
        })

    @extend_schema(
        tags=['Catalog'],
        summary=_("Get products on sale"),
        description=_("Get products currently on sale (sale_price < regular price)."),
        parameters=[
            OpenApiParameter('limit', int, description=_('Number of products (default: 24, max: 100)')),
        ]
    )
    @action(detail=False, methods=['get'], url_path='on-sale')
    def on_sale(self, request):
        """
        Get products currently on sale.

        Returns products where sale_price is set and lower than regular price.
        """
        limit = min(int(request.query_params.get('limit', 24)), 100)

        # Filter products that have a sale price
        products = self.get_queryset().filter(
            sale_price__isnull=False
        ).exclude(
            sale_price=0
        ).order_by('-created_at')[:limit]

        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response({
            'success': True,
            'count': products.count() if hasattr(products, 'count') else len(products),
            'data': serializer.data
        })

    @extend_schema(
        tags=['Catalog'],
        summary=_("Get clearance products"),
        description=_("Get products marked as clearance items."),
        parameters=[
            OpenApiParameter('limit', int, description=_('Number of products (default: 24, max: 100)')),
        ]
    )
    @action(detail=False, methods=['get'])
    def clearance(self, request):
        """
        Get clearance products.

        Returns products marked as clearance or with significant discounts.
        """
        limit = min(int(request.query_params.get('limit', 24)), 100)

        # Look for clearance tagged products or deeply discounted items
        products = self.get_queryset().filter(
            Q(tags__name__icontains='clearance') |
            Q(tags__name__icontains='sale') |
            Q(sale_price__isnull=False)
        ).distinct().order_by('sale_price')[:limit]

        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data
        })

    @extend_schema(
        tags=['Catalog'],
        summary=_("Get bundle products"),
        description=_("Get products that are bundles (contain multiple items)."),
        parameters=[
            OpenApiParameter('limit', int, description=_('Number of products (default: 12, max: 50)')),
        ]
    )
    @action(detail=False, methods=['get'])
    def bundles(self, request):
        """
        Get bundle products.
        """
        limit = min(int(request.query_params.get('limit', 12)), 50)

        products = self.get_queryset().filter(
            product_type='bundle'
        ).order_by('-created_at')[:limit]

        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data
        })

    @extend_schema(
        tags=['Catalog'],
        summary=_("Get digital products"),
        description=_("Get downloadable/digital products."),
        parameters=[
            OpenApiParameter('limit', int, description=_('Number of products (default: 12, max: 50)')),
        ]
    )
    @action(detail=False, methods=['get'], url_path='digital')
    def digital_products(self, request):
        """
        Get digital products.
        """
        limit = min(int(request.query_params.get('limit', 12)), 50)

        products = self.get_queryset().filter(
            product_type='digital'
        ).order_by('-created_at')[:limit]

        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data
        })

    @extend_schema(
        tags=['Catalog'],
        summary=_("Get gift cards"),
        description=_("Get available gift card products."),
        parameters=[
            OpenApiParameter('limit', int, description=_('Number of products (default: 12, max: 50)')),
        ]
    )
    @action(detail=False, methods=['get'], url_path='gift-cards')
    def gift_card_products(self, request):
        """
        Get gift card products.
        """
        limit = min(int(request.query_params.get('limit', 12)), 50)

        products = self.get_queryset().filter(
            product_type='gift_card'
        ).order_by('-created_at')[:limit]

        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data
        })

    @extend_schema(
        tags=['Catalog'],
        summary=_("Get related products"),
        description=_("Get products related to a specific product (same category, brand, or attributes)."),
        parameters=[
            OpenApiParameter('limit', int, description=_('Number of products (default: 8, max: 20)')),
        ]
    )
    @action(detail=True, methods=['get'])
    def related(self, request, slug=None):
        """
        Get related products.

        Returns products in the same category or brand, excluding the current product.
        """
        product = self.get_object()
        limit = min(int(request.query_params.get('limit', 8)), 20)

        # Find related products by category and brand
        related = self.get_queryset().filter(
            Q(category=product.category) | Q(brand=product.brand)
        ).exclude(id=product.id).distinct()[:limit]

        serializer = ProductListSerializer(related, many=True, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data
        })

    @extend_schema(
        tags=['Catalog'],
        summary=_("Get similar products"),
        description=_("Get products with similar attributes (size, color, price range)."),
        parameters=[
            OpenApiParameter('limit', int, description=_('Number of products (default: 8, max: 20)')),
        ]
    )
    @action(detail=True, methods=['get'])
    def similar(self, request, slug=None):
        """
        Get similar products based on attributes.

        Returns products with similar characteristics.
        """
        product = self.get_object()
        limit = min(int(request.query_params.get('limit', 8)), 20)

        # Find similar products by price range (within 20% of current product price)
        price_min = product.price.amount * Decimal('0.8')
        price_max = product.price.amount * Decimal('1.2')

        similar = self.get_queryset().filter(
            category=product.category,
            price__gte=price_min,
            price__lte=price_max
        ).exclude(id=product.id)[:limit]

        serializer = ProductListSerializer(similar, many=True, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data
        })

    @extend_schema(
        tags=['Catalog'],
        summary=_("Get frequently bought together"),
        description=_("Get products frequently purchased together with this product."),
        parameters=[
            OpenApiParameter('limit', int, description=_('Number of products (default: 4, max: 10)')),
        ]
    )
    @action(detail=True, methods=['get'], url_path='frequently-bought-together')
    def frequently_bought_together(self, request, slug=None):
        """
        Get products frequently bought together.

        Analyzes order history to find products commonly purchased together.
        Falls back to related products if no purchase data available.
        """
        from orders.models import Order, OrderItem

        product = self.get_object()
        limit = min(int(request.query_params.get('limit', 4)), 10)

        # Find orders containing this product
        order_ids = OrderItem.objects.filter(
            product=product
        ).values_list('order_id', flat=True)

        # Find other products in those orders
        co_purchased = OrderItem.objects.filter(
            order_id__in=order_ids
        ).exclude(
            product=product
        ).values('product').annotate(
            frequency=Count('product')
        ).order_by('-frequency')[:limit]

        product_ids = [item['product'] for item in co_purchased]

        if product_ids:
            products = Product.objects.filter(
                id__in=product_ids,
                status='published'
            ).select_related('category', 'brand').prefetch_related('images')
        else:
            # Fallback to related products if no purchase history
            products = self.get_queryset().filter(
                category=product.category
            ).exclude(id=product.id)[:limit]

        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data
        })

    @extend_schema(
        tags=['Catalog'],
        summary=_("Get upsell products"),
        description=_("Get higher-priced alternatives or upgrades for this product."),
        parameters=[
            OpenApiParameter('limit', int, description=_('Number of products (default: 4, max: 10)')),
        ]
    )
    @action(detail=True, methods=['get'])
    def upsells(self, request, slug=None):
        """
        Get upsell products.

        Returns higher-priced products in the same category as upgrade options.
        """
        product = self.get_object()
        limit = min(int(request.query_params.get('limit', 4)), 10)

        # Find higher-priced products in same category
        upsells = self.get_queryset().filter(
            category=product.category,
            price__gt=product.price
        ).exclude(id=product.id).order_by('price')[:limit]

        serializer = ProductListSerializer(upsells, many=True, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data
        })

    @extend_schema(
        tags=['Catalog'],
        summary=_("Get cross-sell products"),
        description=_("Get complementary products that go well with this product."),
        parameters=[
            OpenApiParameter('limit', int, description=_('Number of products (default: 4, max: 10)')),
        ]
    )
    @action(detail=True, methods=['get'], url_path='cross-sells')
    def cross_sells(self, request, slug=None):
        """
        Get cross-sell products.

        Returns products from different categories that complement this product.
        """
        product = self.get_object()
        limit = min(int(request.query_params.get('limit', 4)), 10)

        # Find products from different categories (potential accessories/complements)
        cross_sells = self.get_queryset().exclude(
            category=product.category
        ).exclude(id=product.id).order_by('-sales_count')[:limit]

        serializer = ProductListSerializer(cross_sells, many=True, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data
        })

    # ── Configurator Actions ──────────────────────────────────────────────

    @extend_schema(
        tags=['Catalog'],
        summary=_("Get full configurator data"),
        description=_(
            "Returns the complete configurator payload for a configurable product, "
            "including all slots with their options, compatibility rules, presets, "
            "and pricing strategy. Used by the frontend configurator wizard to "
            "render the step-by-step configuration interface."
        ),
        responses={
            200: ConfiguratorDataSerializer,
            404: OpenApiResponse(description=_("Product not found or not configurable")),
        },
    )
    @action(detail=True, methods=['get'], url_path='configurator')
    def configurator(self, request, slug=None):
        """Get full configurator data for a configurable product."""
        product = self.get_object()

        if product.product_type != 'configurable':
            return Response(
                {'error': 'This product is not configurable.'},
                status=status.HTTP_404_NOT_FOUND
            )

        slots = product.configuration_slots.prefetch_related(
            'options__option_product__images__media_asset',
            'options__option_variant',
            'options__option_product__stock_items',
        ).order_by('sort_order')

        rules = CompatibilityRule.objects.filter(
            configurable_product=product
        ).prefetch_related('compatible_options')

        presets = ConfigurationPreset.objects.filter(
            product=product
        ).select_related('image_asset').order_by('sort_order')

        base_price = product.configurator_base_price or product.price
        currency = base_price.currency if hasattr(base_price, 'currency') else get_default_currency()

        data = {
            'product_id': product.pk,
            'product_name': product.name,
            'product_slug': product.slug,
            'pricing_strategy': product.configurator_pricing_strategy,
            'base_price': str(base_price.amount) if base_price else None,
            'currency': str(currency),
            'slots': ConfigurationSlotSerializer(slots, many=True, context={'request': request}).data,
            'rules': CompatibilityRuleSerializer(rules, many=True).data,
            'presets': ConfigurationPresetSerializer(presets, many=True, context={'request': request}).data,
        }

        return Response({'success': True, 'data': data})

    @extend_schema(
        tags=['Catalog'],
        summary=_("Validate a configuration"),
        description=_(
            "Validates a complete or partial configuration against slot requirements "
            "and compatibility rules. Returns validity status, any errors, and the "
            "calculated total price if valid."
        ),
        request=ConfigurationSelectionSerializer,
        responses={
            200: ConfiguratorValidationResponseSerializer,
            400: OpenApiResponse(description=_("Invalid request body")),
            404: OpenApiResponse(description=_("Product not found or not configurable")),
        },
    )
    @action(detail=True, methods=['post'], url_path='configurator/validate')
    def configurator_validate(self, request, slug=None):
        """Validate configuration selections and return price."""
        product = self.get_object()

        if product.product_type != 'configurable':
            return Response(
                {'error': 'This product is not configurable.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ConfigurationSelectionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        configuration = serializer.validated_data['configuration']
        # Convert string keys to int
        config_int = {int(k): v for k, v in configuration.items()}

        from cart.services.cart_service import CartService

        is_valid, error_msg, resolved_options = CartService._validate_configuration(
            product, config_int
        )

        if not is_valid:
            return Response({
                'valid': False,
                'errors': [str(error_msg)],
            })

        price = CartService._calculate_configurable_price(product, resolved_options)

        # Build price breakdown by slot
        from decimal import Decimal
        slot_subtotals = {}
        for option, variant in resolved_options:
            slot_id = str(option.slot_id)
            if product.configurator_pricing_strategy == 'base_plus_adjustments':
                adj = option.price_adjustment
                amount = adj.amount if adj and hasattr(adj, 'amount') else Decimal('0.00')
            else:
                if variant:
                    p = variant.get_price()
                else:
                    p = option.option_product.price
                amount = (p.amount if p and hasattr(p, 'amount') else Decimal('0.00')) * option.quantity

            slot_subtotals[slot_id] = str(
                Decimal(slot_subtotals.get(slot_id, '0.00')) + amount
            )

        return Response({
            'valid': True,
            'errors': [],
            'total_price': str(price.amount),
            'currency': str(price.currency),
            'price_breakdown': slot_subtotals,
        })

    @extend_schema(
        tags=['Catalog'],
        summary=_("Calculate configuration price"),
        description=_(
            "Calculate the total price for a partial or complete configuration. "
            "Does not validate compatibility — use the validate endpoint for full validation."
        ),
        request=ConfigurationSelectionSerializer,
        responses={
            200: ConfiguratorPriceResponseSerializer,
            400: OpenApiResponse(description=_("Invalid request body")),
            404: OpenApiResponse(description=_("Product not found or not configurable")),
        },
    )
    @action(detail=True, methods=['post'], url_path='configurator/price')
    def configurator_price(self, request, slug=None):
        """Quick price calculation for a configuration."""
        product = self.get_object()

        if product.product_type != 'configurable':
            return Response(
                {'error': 'This product is not configurable.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ConfigurationSelectionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        configuration = serializer.validated_data['configuration']

        # Resolve options without full validation
        from decimal import Decimal
        resolved_options = []
        slot_subtotals = {}

        for slot_id_str, option_ids in configuration.items():
            slot_total = Decimal('0.00')
            for option_id in option_ids:
                try:
                    option = ConfigurationSlotOption.objects.select_related(
                        'option_product', 'option_variant'
                    ).get(pk=option_id)
                    resolved_options.append((option, option.option_variant))

                    if product.configurator_pricing_strategy == 'base_plus_adjustments':
                        adj = option.price_adjustment
                        slot_total += adj.amount if adj and hasattr(adj, 'amount') else Decimal('0.00')
                    else:
                        if option.option_variant:
                            p = option.option_variant.get_price()
                        else:
                            p = option.option_product.price
                        slot_total += (p.amount if p and hasattr(p, 'amount') else Decimal('0.00')) * option.quantity
                except ConfigurationSlotOption.DoesNotExist:
                    continue

            slot_subtotals[slot_id_str] = str(slot_total)

        from cart.services.cart_service import CartService
        price = CartService._calculate_configurable_price(product, resolved_options)

        return Response({
            'total_price': str(price.amount),
            'currency': str(price.currency),
            'pricing_strategy': product.configurator_pricing_strategy,
            'slot_subtotals': slot_subtotals,
        })

    @extend_schema(
        tags=['Catalog'],
        summary=_("Get configuration presets"),
        description=_(
            "Returns pre-built configuration presets with calculated prices. "
            "Presets provide starting configurations customers can use and then customize."
        ),
        responses={
            200: ConfigurationPresetSerializer(many=True),
            404: OpenApiResponse(description=_("Product not found or not configurable")),
        },
    )
    @action(detail=True, methods=['get'], url_path='configurator/presets')
    def configurator_presets(self, request, slug=None):
        """Get presets for a configurable product."""
        product = self.get_object()

        if product.product_type != 'configurable':
            return Response(
                {'error': 'This product is not configurable.'},
                status=status.HTTP_404_NOT_FOUND
            )

        presets = ConfigurationPreset.objects.filter(
            product=product
        ).select_related('image_asset').order_by('sort_order')

        serializer = ConfigurationPresetSerializer(presets, many=True, context={'request': request})
        return Response({'success': True, 'data': serializer.data})


@extend_schema_view(
    list=extend_schema(tags=['Catalog'], summary=_("List all collections")),
    retrieve=extend_schema(tags=['Catalog'], summary=_("Get collection details")),
    products=extend_schema(tags=['Catalog'], summary=_("Get products in collection"))
)
class CollectionViewSet(HeadlessAPIMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for collections

    list: Get all collections
    retrieve: Get single collection with products

    Supports multi-language via Accept-Language header
    """
    queryset = Collection.objects.filter(is_active=True).order_by('sort_order', 'name')
    serializer_class = CollectionSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_serializer_context(self):
        """Include products in detail view only"""
        context = super().get_serializer_context()
        context['include_products'] = self.action == 'retrieve'
        return context

    @action(detail=True, methods=['get'])
    def products(self, request, slug=None):
        """
        Get products in a specific collection
        Supports filtering, sorting, pagination
        """
        collection = self.get_object()

        # Get collection products
        if collection.collection_type == 'manual':
            products = collection.products.filter(status='published', hide_from_storefront=False)
        else:
            # For automatic collections, apply criteria
            # This is a basic implementation - can be enhanced
            products = collection.products.filter(status='published', hide_from_storefront=False)

        products = products.select_related('category', 'brand').prefetch_related('images')

        # Apply filters
        filterset = ProductFilter(request.query_params, queryset=products)
        if filterset.is_valid():
            products = filterset.qs

        # Sorting
        sort = request.query_params.get('sort', '-created_at')
        allowed_sorts = ['price', '-price', 'name', '-name', 'created_at', '-created_at', 'sales_count', '-sales_count']
        if sort in allowed_sorts:
            products = products.order_by(sort)

        # Paginate
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(tags=['Reviews'], summary=_("List all reviews")),
    retrieve=extend_schema(tags=['Reviews'], summary=_("Get review details")),
    create=extend_schema(tags=['Reviews'], summary=_("Create a review")),
    update=extend_schema(tags=['Reviews'], summary=_("Update a review")),
    partial_update=extend_schema(tags=['Reviews'], summary=_("Partially update a review")),
    destroy=extend_schema(tags=['Reviews'], summary=_("Delete a review")),
    mark_helpful=extend_schema(tags=['Reviews'], summary=_("Mark review as helpful"))
)
class ProductReviewViewSet(HeadlessAPIMixin, viewsets.ModelViewSet):
    """
    API endpoint for product reviews

    list: Get all reviews (filtered by product if provided)
    retrieve: Get single review
    create: Create a review (authenticated users only)
    update/partial_update: Update own review
    destroy: Delete own review

    Admin can approve/reject reviews via admin interface
    """
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'rating', 'is_verified_purchase']
    ordering_fields = ['created_at', 'helpful_count', 'rating']
    ordering = ['-created_at']

    def get_queryset(self):
        """Get reviews with optimized queries"""
        queryset = ProductReview.objects.select_related('user', 'product')

        # Only show approved reviews to non-staff
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_approved=True)

        # Filter by product if provided
        product_id = self.request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)

        product_slug = self.request.query_params.get('product_slug')
        if product_slug:
            queryset = queryset.filter(product__slug=product_slug)

        return queryset

    def perform_create(self, serializer):
        """Create review with current user"""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Only allow users to update their own reviews"""
        if serializer.instance.user != self.request.user and not self.request.user.is_staff:
            return Response(
                {'error': 'You can only edit your own reviews'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    def perform_destroy(self, instance):
        """Only allow users to delete their own reviews"""
        if instance.user != self.request.user and not self.request.user.is_staff:
            return Response(
                {'error': 'You can only delete your own reviews'},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()

    @action(detail=True, methods=['post'])
    def mark_helpful(self, request, pk=None):
        """
        Mark a review as helpful (increment helpful_count)
        """
        review = self.get_object()

        # Check if user already marked this review as helpful (session-based)
        helpful_reviews = request.session.get('helpful_reviews', [])

        if review.id in helpful_reviews:
            return Response(
                {'error': 'You have already marked this review as helpful'},
                status=status.HTTP_400_BAD_REQUEST
            )

        review.helpful_count += 1
        review.save(update_fields=['helpful_count'])

        # Store in session
        helpful_reviews.append(review.id)
        request.session['helpful_reviews'] = helpful_reviews

        return Response({
            'success': True,
            'helpful_count': review.helpful_count
        })


@extend_schema(
    tags=['Catalog'],
    summary=_("Get catalog statistics"),
    description=_("Retrieve catalog-wide statistics including total products, featured products, products in stock, category count, brand count, and collection count. Useful for dashboard displays and analytics."),
    responses={
        200: OpenApiResponse(
            description=_("Catalog statistics"),
            response={
                "products": {
                    "total": 150,
                    "featured": 20,
                    "in_stock": 130
                },
                "categories": 15,
                "brands": 25,
                "collections": 8
            }
        )
    }
)
@extend_schema(
    tags=['Catalog'],
    summary=_("Get product recommendations"),
    description=_("""
    Returns product recommendations for upselling opportunities such as mini-cart empty state,
    checkout page suggestions, or related products sections.

    **Priority Logic:**
    1. Featured products are returned first
    2. If fewer featured products than requested limit, fills with latest published products

    **Use Cases:**
    - Mini-cart empty state: Show popular items to encourage purchases
    - Checkout cross-sells: Display complementary products
    - Homepage recommendations: Highlight featured inventory
    """),
    parameters=[
        OpenApiParameter(
            name='limit',
            type=int,
            location=OpenApiParameter.QUERY,
            description=_('Maximum number of products to return (1-10, default: 4)'),
            required=False
        )
    ],
    responses={
        200: OpenApiResponse(
            description=_("List of recommended products"),
            response={
                "type": "object",
                "properties": {
                    "products": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 123},
                                "name": {"type": "string", "example": "Premium Diffuser"},
                                "url": {"type": "string", "example": "/en/product/premium-diffuser/"},
                                "image_url": {"type": "string", "nullable": True, "example": "/media/products/diffuser.jpg"},
                                "price": {"type": "string", "example": "29.99"},
                                "price_formatted": {"type": "string", "example": "$29.99"}
                            }
                        }
                    }
                }
            }
        )
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def product_recommendations(request):
    """
    Get product recommendations for mini-cart empty state.
    Returns popular/featured products for upselling.
    """
    from django.urls import reverse

    limit = int(request.query_params.get('limit', 4))
    limit = min(limit, 10)  # Cap at 10

    # Get featured products first, then fall back to latest
    products = Product.objects.filter(
        status='published',
        is_featured=True,
        is_deleted=False
    ).select_related('category').prefetch_related('images__media_asset')[:limit]

    if products.count() < limit:
        # Fill with latest products
        featured_ids = list(products.values_list('id', flat=True))
        additional = Product.objects.filter(
            status='published'
        ).exclude(
            id__in=featured_ids
        ).select_related('category').prefetch_related('images__media_asset').order_by('-created_at')[:limit - len(featured_ids)]
        products = list(products) + list(additional)

    result = []
    for product in products:
        # Get image URL
        image_url = None
        if hasattr(product, 'primary_image_url'):
            image_url = product.primary_image_url

        # Get price
        price = product.price
        if hasattr(price, 'amount'):
            price = price.amount

        result.append({
            'id': product.id,
            'name': product.name,
            'url': reverse('page_builder:product_detail', kwargs={'product_slug': product.slug}),
            'image_url': image_url,
            'price': str(price),
            'price_formatted': f"${price:.2f}" if price else "$0.00",
        })

    return Response({'products': result})


@extend_schema(
    tags=['Catalog'],
    summary=_("Get catalog statistics"),
    description=_("Retrieve catalog statistics including product counts, category counts, etc."),
)
@api_view(['GET'])
@permission_classes([AllowAny])
def catalog_stats(request):
    """
    Get catalog statistics
    Returns counts for products, categories, brands, collections
    """
    stats = {
        'products': {
            'total': Product.objects.filter(status='published').count(),
            'featured': Product.objects.filter(status='published', is_featured=True).count(),
            'in_stock': Product.objects.filter(
                status='published'
            ).filter(
                Q(track_inventory=False) |
                Q(track_inventory=True, quantity__gt=0)
            ).count(),
        },
        'categories': Category.objects.filter(is_active=True).count(),
        'brands': Brand.objects.filter(is_active=True).count(),
        'collections': Collection.objects.filter(is_active=True).count(),
    }

    return Response(stats)


@extend_schema(
    tags=['Catalog'],
    summary=_("Get available filter options"),
    description=_("Retrieve all available filter options for product filtering including categories, brands, price ranges, and product types. Used to populate filter UI components."),
    responses={
        200: OpenApiResponse(
            description=_("Available filter options"),
            response={
                "categories": [{"id": 1, "name": "Electronics", "slug": "electronics"}],
                "brands": [{"id": 1, "name": "Apple", "slug": "apple"}],
                "price_range": {"min_price": 9.99, "max_price": 999.99},
                "product_types": ["physical", "digital"]
            }
        )
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def available_filters(request):
    """
    Get available filter options for products
    Returns categories, brands, price ranges, etc.
    """
    # Get all active categories
    categories = Category.objects.filter(is_active=True).values('id', 'name', 'slug')

    # Get all active brands
    brands = Brand.objects.filter(is_active=True).values('id', 'name', 'slug')

    # Get price range
    from django.db.models import Min, Max
    price_range = Product.objects.filter(status='published').aggregate(
        min_price=Min('price'),
        max_price=Max('price')
    )

    # Get available product types
    product_types = Product.objects.filter(
        status='published'
    ).values_list('product_type', flat=True).distinct()

    return Response({
        'categories': list(categories),
        'brands': list(brands),
        'price_range': {
            'min': float(price_range['min_price']) if price_range['min_price'] else 0,
            'max': float(price_range['max_price']) if price_range['max_price'] else 0,
        },
        'product_types': list(product_types),
    })


@extend_schema(
    tags=['Catalog'],
    summary=_("Check stock at specific warehouses"),
    description=_("Check real-time stock availability for a product at specific warehouse locations. Optionally calculate distance from customer location. Returns on-hand, allocated, and available quantities per warehouse."),
    parameters=[
        OpenApiParameter(
            name="warehouse_codes",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Comma-separated list of warehouse codes to check (e.g., 'MAIN-WH,WC-WH')"),
            required=False
        ),
        OpenApiParameter(
            name="postal_code",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Customer's postal code for distance calculation"),
            required=False
        ),
    ],
    responses={
        200: StockAvailabilitySerializer(many=True),
        404: OpenApiResponse(description=PRODUCT_NOT_FOUND),
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def check_warehouse_stock(request, product_slug):
    """
    Check stock availability for a product at specific warehouses.

    Query parameters:
    - warehouse_codes: Comma-separated list of warehouse codes to check
    - postal_code: Customer's postal code for distance calculation (optional)

    Returns:
    - List of warehouses with stock availability
    - Distance from customer location (if postal_code provided)
    """
    product = get_object_or_404(Product, slug=product_slug, status='published')

    # Get warehouse codes from query params
    warehouse_codes = request.query_params.get('warehouse_codes', '').split(',')
    warehouse_codes = [code.strip() for code in warehouse_codes if code.strip()]

    # Build queryset
    warehouses_query = Warehouse.objects.filter(is_active=True)

    if warehouse_codes:
        warehouses_query = warehouses_query.filter(code__in=warehouse_codes)

    # Get stock items for this product at these warehouses
    stock_items = StockItem.objects.filter(
        product=product,
        warehouse__in=warehouses_query
    ).select_related('warehouse')

    # Build response
    availability = []
    for stock_item in stock_items:
        availability.append({
            'warehouse': WarehouseSerializer(stock_item.warehouse).data,
            'on_hand': stock_item.on_hand,
            'allocated': stock_item.allocated,
            'available': stock_item.available,
            'low_stock_threshold': stock_item.low_stock_threshold or product.low_stock_threshold,
            'is_in_stock': stock_item.available > 0,
            'is_low_stock': stock_item.available <= (stock_item.low_stock_threshold or product.low_stock_threshold) if stock_item.low_stock_threshold or product.low_stock_threshold else False
        })

    return Response({
        'product': {
            'name': product.name,
            'slug': product.slug,
            'sku': product.sku
        },
        'availability': availability
    })


@extend_schema(
    tags=['Catalog'],
    summary=_("List all pickup locations"),
    description=_("Get all warehouse locations that support customer pickup (buy online, pick up in store). Optionally filter by product availability and calculate distances from customer location."),
    parameters=[
        OpenApiParameter(
            name="product_slug",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Filter to only locations with stock of this product"),
            required=False
        ),
        OpenApiParameter(
            name="latitude",
            type=float,
            location=OpenApiParameter.QUERY,
            description=_("Customer latitude for distance calculation"),
            required=False
        ),
        OpenApiParameter(
            name="longitude",
            type=float,
            location=OpenApiParameter.QUERY,
            description=_("Customer longitude for distance calculation"),
            required=False
        ),
    ],
    responses={
        200: WarehouseSerializer(many=True),
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def pickup_locations(request):
    """
    Get all warehouses that support customer pickup.

    Query parameters:
    - product_slug: Filter to only locations with stock of this product (optional)
    - latitude: Customer latitude for distance calculation (optional)
    - longitude: Customer longitude for distance calculation (optional)

    Returns:
    - List of pickup locations with stock availability (if product_slug provided)
    """
    # Get warehouses that support pickup (have shipping_location)
    warehouses = Warehouse.objects.filter(
        is_active=True,
        shipping_location__isnull=False
    ).select_related('shipping_location')

    # If product_slug provided, filter to locations with stock
    product_slug = request.query_params.get('product_slug')
    if product_slug:
        product = get_object_or_404(Product, slug=product_slug, status='published')

        # Get stock items at pickup locations
        stock_items = StockItem.objects.filter(
            product=product,
            warehouse__in=warehouses,
            on_hand__gt=0
        ).select_related('warehouse')

        locations = []
        for stock_item in stock_items:
            locations.append({
                'warehouse': WarehouseSerializer(stock_item.warehouse).data,
                'available_quantity': stock_item.available,
                'is_in_stock': stock_item.available > 0
            })

        return Response({
            'product': {
                'name': product.name,
                'slug': product.slug
            },
            'locations': locations
        })

    # No product filter - return all pickup locations
    locations = [
        {
            'warehouse': WarehouseSerializer(wh).data
        }
        for wh in warehouses
    ]

    return Response({'locations': locations})


@extend_schema(
    tags=['Gift Cards'],
    summary=_("Check gift card balance"),
    description=_("Check the balance of a gift card without requiring authentication. Public endpoint."),
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'code': {
                    'type': 'string',
                    'description': 'Gift card code (e.g., GC-XXXX-XXXX-XXXX)',
                    'example': 'GC-A2B4-C6D8-E9F1'
                }
            },
            'required': ['code']
        }
    },
    responses={
        200: OpenApiResponse(
            description=_('Gift card found'),
            response={
                'type': 'object',
                'properties': {
                    'code': {'type': 'string'},
                    'current_balance': {
                        'type': 'object',
                        'properties': {
                            'amount': {'type': 'string'},
                            'currency': {'type': 'string'}
                        }
                    },
                    'initial_value': {
                        'type': 'object',
                        'properties': {
                            'amount': {'type': 'string'},
                            'currency': {'type': 'string'}
                        }
                    },
                    'is_active': {'type': 'boolean'},
                    'is_expired': {'type': 'boolean'},
                    'is_valid': {'type': 'boolean'},
                    'expires_at': {'type': 'string', 'nullable': True},
                    'redemption_percentage': {'type': 'number'}
                }
            }
        ),
        404: OpenApiResponse(description=_('Gift card not found')),
        400: OpenApiResponse(description=_('Invalid request (missing code)'))
    }
)
@api_view(['POST'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def check_gift_card_balance(request):
    """
    Check gift card balance without authentication.

    This is a public endpoint that allows customers to check their
    gift card balance by providing the gift card code.

    Rate limiting should be implemented at the server level to prevent abuse.
    """
    from .services.gift_card_service import GiftCardService

    code = request.data.get('code', '').strip()

    if not code:
        return Response(
            {'error': 'Gift card code is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check balance using service
    balance_info = GiftCardService.check_balance(code)

    if balance_info is None:
        return Response(
            {'error': 'Gift card not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response(balance_info, status=status.HTTP_200_OK)


# ========================================================================
# Product Availability API (Frontend Stock Display)
# ========================================================================


@extend_schema(
    tags=['Catalog'],
    summary=_('Get product availability'),
    description=_('''
    Returns comprehensive stock availability and fulfillment information for a product.

    **Features:**
    - Stock status (in_stock, low_stock, out_of_stock, preorder, backorder)
    - Warehouse location display (if enabled)
    - Notify Me availability (if product is out of stock)
    - Pre-order information with release dates
    - Backorder availability
    - Respects cascading settings: Product > Category > Site-wide

    **Use cases:**
    - Product page stock display
    - Cart validation
    - Stock status badges
    '''),
    parameters=[
        OpenApiParameter(
            name='country',
            type=str,
            location=OpenApiParameter.QUERY,
            description=_('ISO 3166-1 alpha-2 country code (e.g., US, GB, AU) for regional stock'),
            required=False
        ),
        OpenApiParameter(
            name='variant_id',
            type=int,
            location=OpenApiParameter.QUERY,
            description=_('Specific variant ID to check availability for'),
            required=False
        ),
    ],
    responses={
        200: OpenApiResponse(
            description=_('Product availability data'),
            response={
                'type': 'object',
                'properties': {
                    'available': {'type': 'boolean'},
                    'stock_status': {
                        'type': 'string',
                        'enum': ['in_stock', 'low_stock', 'out_of_stock', 'preorder', 'backorder']
                    },
                    'quantity': {'type': 'integer', 'nullable': True},
                    'display_message': {'type': 'string'},
                    'ships_from': {
                        'type': 'object',
                        'nullable': True,
                        'properties': {
                            'display_name': {'type': 'string'},
                            'warehouse_code': {'type': 'string'}
                        }
                    },
                    'notify_available': {'type': 'boolean'},
                    'backorder_available': {'type': 'boolean'},
                    'preorder': {
                        'type': 'object',
                        'properties': {
                            'available': {'type': 'boolean'},
                            'release_date': {'type': 'string', 'nullable': True},
                            'message': {'type': 'string', 'nullable': True}
                        }
                    }
                }
            }
        ),
        404: OpenApiResponse(description=PRODUCT_NOT_FOUND),
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def product_availability(request, product_slug):
    """
    Get product availability information for frontend display.

    Respects StockDisplaySettings and cascading override settings.
    """
    from shipping.models import ShippingCountry, CountryWarehouseFallback

    # Get product
    product = get_object_or_404(Product, slug=product_slug, status='published')

    # Get variant if specified
    variant = None
    variant_id = request.query_params.get('variant_id')
    if variant_id:
        variant = get_object_or_404(ProductVariant, id=variant_id, product=product, is_active=True)

    # Get display settings
    settings = StockDisplaySettings.get_settings()

    # Get country from query params or GeoIP
    country_code = request.query_params.get('country')
    if not country_code and hasattr(request, 'country_code'):
        country_code = request.country_code

    # Calculate stock status
    total_available = 0
    if not product.track_inventory:
        # Not tracking inventory - always available
        stock_status = 'in_stock'
        quantity = None
        available = True
    else:
        # Get available stock (aggregated across warehouses)
        stock_items = StockItem.objects.filter(product=product, warehouse__is_active=True)
        if variant:
            stock_items = stock_items.filter(variant=variant)

        # If country specified, try to get regional stock first
        warehouse = None
        if country_code:
            try:
                shipping_country = ShippingCountry.objects.get(
                    country_code=country_code.upper(),
                    is_active=True
                )
                if shipping_country.source_warehouse:
                    warehouse = shipping_country.source_warehouse
                    stock_items = stock_items.filter(warehouse=warehouse)
            except ShippingCountry.DoesNotExist:
                pass

        # Calculate totals
        total_available = sum(item.available for item in stock_items)
        quantity = total_available if settings.show_exact_quantity else None

        # Determine status
        if total_available > 0:
            if total_available <= settings.low_stock_threshold and settings.show_low_stock_warning:
                stock_status = 'low_stock'
            else:
                stock_status = 'in_stock'
            available = True
        elif product.is_preorder:
            stock_status = 'preorder'
            available = True
        elif product.get_effective_allow_backorders():
            stock_status = 'backorder'
            available = True
        else:
            stock_status = 'out_of_stock'
            available = False

    # Get display message
    if stock_status == 'in_stock':
        display_message = 'In Stock'
    elif stock_status == 'low_stock':
        if settings.show_exact_quantity:
            display_message = f'Only {total_available} left'
        else:
            display_message = 'Low Stock'
    elif stock_status == 'preorder':
        display_message = product.preorder_message or 'Pre-Order'
    elif stock_status == 'backorder':
        display_message = settings.backorder_message
    else:
        display_message = settings.out_of_stock_message

    # Get warehouse display info
    ships_from = None
    if settings.show_ships_from and warehouse:
        warehouse_display_name = warehouse.get_display_name()
        if warehouse_display_name:
            ships_from = {
                'display_name': warehouse_display_name,
                'warehouse_code': warehouse.code
            }

    # Determine available actions
    out_of_stock_action = product.get_effective_out_of_stock_action()
    notify_available = out_of_stock_action == 'notify_me' and stock_status == 'out_of_stock'
    backorder_available = out_of_stock_action == 'allow_backorder' and stock_status == 'out_of_stock'

    # Pre-order info
    preorder_info = {
        'available': product.is_preorder,
        'release_date': product.preorder_release_date.isoformat() if product.preorder_release_date else None,
        'message': product.preorder_message or None
    }

    # Build low stock info
    is_low_stock = stock_status == 'low_stock'
    low_stock_qty = total_available if is_low_stock and product.track_inventory else None

    return Response({
        # Core status
        'available': available,
        'in_stock': available and stock_status in ('in_stock', 'low_stock'),
        'stock_status': stock_status,
        'quantity': quantity,
        'display_message': display_message,
        # Low stock
        'show_low_stock_warning': is_low_stock,
        'low_stock_quantity': low_stock_qty,
        'show_exact_quantity': settings.show_exact_quantity if product.track_inventory else False,
        # Shipping info
        'show_ships_from': settings.show_ships_from if product.track_inventory else False,
        'ships_from': ships_from.get('display_name') if ships_from else None,
        'show_estimated_delivery': bool(settings.show_estimated_delivery) if product.track_inventory else False,
        'estimated_delivery': None,
        # Out of stock actions
        'show_notify_me': notify_available,
        'allow_backorders': backorder_available,
        'backorder_message': settings.backorder_message if backorder_available else None,
        'out_of_stock_message': settings.out_of_stock_message,
        'out_of_stock_action': out_of_stock_action,
        # Pre-order
        'is_preorder': product.is_preorder,
        'preorder_message': product.preorder_message or None,
        'preorder_release_date': product.preorder_release_date.isoformat() if product.preorder_release_date else None,
        'preorder': preorder_info,
    })


@extend_schema(
    tags=['Catalog'],
    summary=_('Subscribe to stock notification'),
    description=_('''
    Subscribe to receive an email notification when a product comes back in stock.

    **Rate limiting:** This endpoint should be rate-limited to prevent abuse.
    '''),
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'email': {
                    'type': 'string',
                    'format': 'email',
                    'description': 'Email address to notify'
                },
                'variant_id': {
                    'type': 'integer',
                    'description': 'Optional variant ID to subscribe to',
                    'nullable': True
                }
            },
            'required': ['email']
        }
    },
    responses={
        201: OpenApiResponse(description=_('Successfully subscribed')),
        400: OpenApiResponse(description=_('Invalid email or already subscribed')),
        404: OpenApiResponse(description=PRODUCT_NOT_FOUND),
    }
)
@api_view(['POST'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def stock_notification_subscribe(request, product_slug):
    """
    Subscribe to back-in-stock notification for a product.
    """
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError

    product = get_object_or_404(Product, slug=product_slug, status='published')

    email = request.data.get('email', '').strip().lower()
    variant_id = request.data.get('variant_id')

    # Validate email
    if not email:
        return Response(
            {'error': 'Email address is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        validate_email(email)
    except ValidationError:
        return Response(
            {'error': 'Invalid email address'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Get variant if specified
    variant = None
    if variant_id:
        variant = get_object_or_404(ProductVariant, id=variant_id, product=product, is_active=True)

    # Check if already subscribed
    existing = StockNotification.objects.filter(
        email=email,
        product=product,
        variant=variant,
        notified_at__isnull=True  # Not yet notified
    ).exists()

    if existing:
        return Response(
            {'message': 'You are already subscribed to notifications for this product'},
            status=status.HTTP_200_OK
        )

    # Create notification subscription
    StockNotification.objects.create(
        email=email,
        product=product,
        variant=variant
    )

    return Response(
        {'message': 'You will be notified when this product is back in stock'},
        status=status.HTTP_201_CREATED
    )


# ─── Product Attribute Assignment Management (Admin Only) ──────────────────────


@extend_schema(
    tags=['Catalog'],
    summary=_("List product attribute assignments"),
    description=_("Returns all attributes assigned to a product with their allowed values and full value sets. **Admin only.**"),
    responses={200: OpenApiResponse(description=_("List of attribute assignments with values"))},
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_product_attributes(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    assignments = (
        ProductAttributeAssignment.objects
        .filter(product=product)
        .select_related('attribute')
        .prefetch_related('allowed_values', 'attribute__values')
        .order_by('sort_order', 'attribute__name')
    )

    result = []
    for assignment in assignments:
        allowed_ids = set(assignment.allowed_values.values_list('id', flat=True))
        all_values = assignment.attribute.values.all().order_by('sort_order', 'value')

        result.append({
            'id': assignment.id,
            'attribute': {
                'id': assignment.attribute.id,
                'name': assignment.attribute.name,
                'slug': assignment.attribute.slug,
                'type': assignment.attribute.type,
            },
            'sort_order': assignment.sort_order,
            'values': [
                {
                    'id': v.id,
                    'value': v.value,
                    'slug': v.slug,
                    'color_hex': v.color_hex,
                    'enabled': v.id in allowed_ids,
                }
                for v in all_values
            ],
        })

    return Response({'success': True, 'assignments': result})


@extend_schema(
    tags=['Catalog'],
    summary=_("Search available attributes"),
    description=_("Returns attributes not yet assigned to the product, filtered by optional search query. **Admin only.**"),
    parameters=[
        OpenApiParameter('q', str, description=_('Search query to filter attribute names')),
    ],
    responses={200: OpenApiResponse(description=_("List of available attributes"))},
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def search_available_attributes(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    assigned_ids = product.attribute_assignments.values_list('attribute_id', flat=True)
    qs = ProductAttribute.objects.exclude(id__in=assigned_ids)

    q = request.query_params.get('q', '').strip()
    if q:
        qs = qs.filter(name__icontains=q)

    qs = qs.annotate(value_count=Count('values')).order_by('name')[:50]

    return Response({
        'success': True,
        'attributes': [
            {
                'id': attr.id,
                'name': attr.name,
                'slug': attr.slug,
                'type': attr.type,
                'value_count': attr.value_count,
            }
            for attr in qs
        ],
    })


@extend_schema(
    tags=['Catalog'],
    summary=_("Add attribute to product"),
    description=_("Creates a new attribute assignment for the product. All attribute values are enabled by default. **Admin only.**"),
    request={'application/json': {'type': 'object', 'properties': {'attribute_id': {'type': 'integer'}}, 'required': ['attribute_id']}},
    responses={
        201: OpenApiResponse(description=_("Attribute assigned successfully")),
        400: OpenApiResponse(description=_("Invalid request or attribute already assigned")),
        404: OpenApiResponse(description=_("Product or attribute not found")),
    },
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_product_attribute(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    attribute_id = request.data.get('attribute_id')
    if not attribute_id:
        return Response({'success': False, 'error': 'attribute_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    attribute = get_object_or_404(ProductAttribute, pk=attribute_id)

    if ProductAttributeAssignment.objects.filter(product=product, attribute=attribute).exists():
        return Response({'success': False, 'error': 'Attribute already assigned to this product'}, status=status.HTTP_400_BAD_REQUEST)

    max_sort = ProductAttributeAssignment.objects.filter(product=product).count()
    assignment = ProductAttributeAssignment.objects.create(
        product=product,
        attribute=attribute,
        sort_order=max_sort,
    )
    # Default: enable all values
    assignment.allowed_values.set(attribute.values.all())

    return Response({
        'success': True,
        'assignment_id': assignment.id,
        'message': f'Attribute "{attribute.name}" added with all values enabled',
    }, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=['Catalog'],
    summary=_("Remove attribute from product"),
    description=_("Deletes an attribute assignment. Returns count of variants that used this attribute. **Admin only.**"),
    responses={
        200: OpenApiResponse(description=_("Attribute removed successfully")),
        404: OpenApiResponse(description=_("Assignment not found")),
    },
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def remove_product_attribute(request, product_id, assignment_id):
    assignment = get_object_or_404(
        ProductAttributeAssignment, pk=assignment_id, product_id=product_id
    )
    attr_name = assignment.attribute.name
    # Count variants that reference values of this attribute
    value_ids = assignment.attribute.values.values_list('id', flat=True)
    affected_variants = ProductVariant.objects.filter(
        product_id=product_id,
        selected_attributes__id__in=value_ids,
    ).distinct().count()

    assignment.delete()

    return Response({
        'success': True,
        'message': f'Attribute "{attr_name}" removed',
        'affected_variants': affected_variants,
    })


@extend_schema(
    tags=['Catalog'],
    summary=_("Update allowed attribute values"),
    description=_("Replaces the set of allowed values for an attribute assignment. **Admin only.**"),
    request={'application/json': {'type': 'object', 'properties': {'allowed_value_ids': {'type': 'array', 'items': {'type': 'integer'}}}, 'required': ['allowed_value_ids']}},
    responses={
        200: OpenApiResponse(description=_("Values updated successfully")),
        400: OpenApiResponse(description=_("Invalid request")),
        404: OpenApiResponse(description=_("Assignment not found")),
    },
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def update_attribute_values(request, product_id, assignment_id):
    assignment = get_object_or_404(
        ProductAttributeAssignment, pk=assignment_id, product_id=product_id
    )
    allowed_value_ids = request.data.get('allowed_value_ids')
    if allowed_value_ids is None:
        return Response({'success': False, 'error': 'allowed_value_ids is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Validate all IDs belong to this attribute
    valid_ids = set(assignment.attribute.values.values_list('id', flat=True))
    requested_ids = set(allowed_value_ids)
    invalid = requested_ids - valid_ids
    if invalid:
        return Response({'success': False, 'error': f'Invalid value IDs for this attribute: {list(invalid)}'}, status=status.HTTP_400_BAD_REQUEST)

    assignment.allowed_values.set(requested_ids)

    return Response({
        'success': True,
        'enabled_count': len(requested_ids),
        'total_count': len(valid_ids),
    })
