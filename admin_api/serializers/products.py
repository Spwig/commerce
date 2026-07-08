"""
Product Serializers for Admin API

Serializers for product and stock management in the merchant mobile app.
"""
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from catalog.models import Product, ProductImage, StockItem, Warehouse, Category, Brand


class AdminProductImageSerializer(serializers.ModelSerializer):
    """Serializer for product images with thumbnail and full URLs (admin/mobile app)."""
    thumbnail_url = serializers.SerializerMethodField()
    full_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = [
            'id',
            'thumbnail_url',
            'full_url',
            'alt_text',
            'is_primary',
            'position',
        ]

    def get_thumbnail_url(self, obj):
        """Get medium thumbnail URL."""
        if obj.media_asset:
            return obj.media_asset.get_thumbnail('medium') or obj.media_asset.get_display_url()
        return None

    def get_full_url(self, obj):
        """Get full-size image URL."""
        if obj.media_asset:
            return obj.media_asset.get_display_url()
        return None


class AdminStockItemSerializer(serializers.ModelSerializer):
    """Stock item serializer for warehouse-level stock (admin/mobile app)."""
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)

    class Meta:
        model = StockItem
        fields = [
            'id',
            'warehouse_id',
            'warehouse_name',
            'on_hand',
            'allocated',
        ]


class AdminProductListSerializer(serializers.ModelSerializer):
    """Compact serializer for product list view — stock-focused (admin/mobile app)."""
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source='price.amount')
    currency = serializers.CharField(source='price.currency.code', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    available_stock = serializers.IntegerField(read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'sku',
            'status',
            'status_display',
            'product_type',
            'price',
            'currency',
            'track_inventory',
            'available_stock',
            'low_stock_threshold',
            'is_low_stock',
            'allow_backorders',
            'image_url',
        ]

    def get_image_url(self, obj):
        """Get primary image thumbnail URL for list views."""
        primary = obj.images.filter(is_primary=True).first()
        if primary and primary.media_asset:
            return primary.media_asset.get_thumbnail('medium') or primary.media_asset.get_display_url()
        first_image = obj.images.first()
        if first_image and first_image.media_asset:
            return first_image.media_asset.get_thumbnail('medium') or first_image.media_asset.get_display_url()
        return None


class AdminProductDetailSerializer(serializers.ModelSerializer):
    """Full serializer for product detail view (admin/mobile app)."""
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source='price.amount')
    compare_at_price = serializers.DecimalField(
        max_digits=10, decimal_places=2,
        source='compare_at_price.amount',
        allow_null=True
    )
    currency = serializers.CharField(source='price.currency.code', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    product_type_display = serializers.CharField(source='get_product_type_display', read_only=True)
    available_stock = serializers.IntegerField(read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    stock_items = AdminStockItemSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    images = AdminProductImageSerializer(many=True, read_only=True)
    short_description = serializers.SerializerMethodField()
    full_description = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'sku',
            'status',
            'status_display',
            'product_type',
            'product_type_display',
            # Descriptions
            'short_description',
            'full_description',
            # Pricing
            'price',
            'compare_at_price',
            'currency',
            # Categorization
            'category_id',
            'category_name',
            'brand_name',
            # Inventory
            'track_inventory',
            'available_stock',
            'low_stock_threshold',
            'is_low_stock',
            'is_in_stock',
            'allow_backorders',
            'stock_items',
            # Images
            'image_url',  # Primary image (full size) for backwards compatibility
            'images',     # All images with thumbnail_url and full_url
            # Timestamps
            'created_at',
            'updated_at',
        ]

    def get_brand_name(self, obj):
        return obj.brand.name if obj.brand else None

    def get_image_url(self, obj):
        """Get primary image URL from media_asset (medium thumbnail)."""
        primary = obj.images.filter(is_primary=True).first()
        if primary and primary.media_asset:
            return primary.media_asset.get_thumbnail('medium') or primary.media_asset.get_display_url()
        first_image = obj.images.first()
        if first_image and first_image.media_asset:
            return first_image.media_asset.get_thumbnail('medium') or first_image.media_asset.get_display_url()
        return None

    def get_short_description(self, obj):
        """Get short description as plain text."""
        if obj.short_description:
            from django.utils.html import strip_tags
            return strip_tags(obj.short_description).strip()
        return None

    def get_full_description(self, obj):
        """Get full description as HTML."""
        return obj.full_description or None


class StockAdjustmentSerializer(serializers.Serializer):
    """Serializer for adjusting stock quantity."""
    quantity = serializers.IntegerField(min_value=0)
    warehouse_id = serializers.IntegerField(required=False)
    reason = serializers.CharField(max_length=500, required=False, allow_blank=True)

    def validate_warehouse_id(self, value):
        """Validate warehouse exists and is active."""
        if value:
            try:
                warehouse = Warehouse.objects.get(id=value, is_active=True)
            except Warehouse.DoesNotExist:
                raise serializers.ValidationError("Warehouse not found or inactive.")
        return value


class ProductStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating product status."""
    status = serializers.ChoiceField(choices=Product.STATUS_CHOICES)

    def validate_status(self, value):
        """Validate status transition."""
        product = self.context.get('product')
        if not product:
            return value

        # All transitions are allowed for simplicity
        # Add restrictions here if needed
        return value


class LowStockProductSerializer(serializers.ModelSerializer):
    """Serializer for low stock products list."""
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source='price.amount')
    currency = serializers.CharField(source='price.currency.code', read_only=True)
    available_stock = serializers.IntegerField(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'sku',
            'price',
            'currency',
            'available_stock',
            'low_stock_threshold',
            'image_url',
        ]

    def get_image_url(self, obj):
        """Get primary image thumbnail URL for low stock list."""
        primary = obj.images.filter(is_primary=True).first()
        if primary and primary.media_asset:
            return primary.media_asset.get_thumbnail('medium') or primary.media_asset.get_display_url()
        first_image = obj.images.first()
        if first_image and first_image.media_asset:
            return first_image.media_asset.get_thumbnail('medium') or first_image.media_asset.get_display_url()
        return None


class ProductFilterSerializer(serializers.Serializer):
    """Serializer for product list filters."""
    status = serializers.ChoiceField(
        choices=[('all', 'All')] + Product.STATUS_CHOICES,
        required=False,
        default='all'
    )
    stock_status = serializers.ChoiceField(
        choices=[
            ('all', 'All'),
            ('in_stock', 'In Stock'),
            ('low_stock', 'Low Stock'),
            ('out_of_stock', 'Out of Stock'),
        ],
        required=False,
        default='all'
    )
    search = serializers.CharField(required=False, allow_blank=True)
    low_stock_only = serializers.BooleanField(required=False, default=False)
    category_id = serializers.IntegerField(
        required=False,
        help_text=_('Filter by category ID')
    )
    brand_id = serializers.IntegerField(
        required=False,
        help_text=_('Filter by brand ID')
    )
    sort = serializers.ChoiceField(
        choices=[
            ('name', 'Name A-Z'),
            ('-name', 'Name Z-A'),
            ('-created_at', 'Newest First'),
            ('created_at', 'Oldest First'),
            ('available_stock', 'Lowest Stock'),
            ('-available_stock', 'Highest Stock'),
            ('price', 'Price Low to High'),
            ('-price', 'Price High to Low'),
            ('-updated_at', 'Recently Updated'),
            ('updated_at', 'Least Recently Updated'),
        ],
        required=False,
        default='name'
    )
    # Support both 'sort' and 'ordering' parameter names
    ordering = serializers.ChoiceField(
        choices=[
            ('name', 'Name A-Z'),
            ('-name', 'Name Z-A'),
            ('-created_at', 'Newest First'),
            ('created_at', 'Oldest First'),
            ('stock_quantity', 'Lowest Stock'),
            ('-stock_quantity', 'Highest Stock'),
            ('price', 'Price Low to High'),
            ('-price', 'Price High to Low'),
            ('-updated_at', 'Recently Updated'),
            ('updated_at', 'Least Recently Updated'),
        ],
        required=False,
        default=None
    )
    page = serializers.IntegerField(required=False, default=1, min_value=1)
    page_size = serializers.IntegerField(required=False, default=20, min_value=1, max_value=100)


class ProductImageUploadSerializer(serializers.Serializer):
    """Serializer for uploading a product image."""
    image = serializers.ImageField(
        help_text=_('Image file to upload (JPEG, PNG, GIF, WebP supported)')
    )
    alt_text = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        help_text=_('Alt text for accessibility')
    )
    is_primary = serializers.BooleanField(
        default=False,
        help_text=_('Set as primary/featured image')
    )
    position = serializers.IntegerField(
        required=False,
        min_value=0,
        help_text=_('Display position (0 = first). Auto-assigned if not provided.')
    )


class ProductImageUpdateSerializer(serializers.Serializer):
    """Serializer for updating product image metadata."""
    alt_text = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        help_text=_('Alt text for accessibility')
    )


class ProductImageReorderSerializer(serializers.Serializer):
    """Serializer for reordering product images."""
    image_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text=_('Ordered list of image IDs (first = position 0)')
    )


class ProductImageResponseSerializer(serializers.ModelSerializer):
    """Response serializer for product image operations."""
    thumbnail_url = serializers.SerializerMethodField()
    full_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = [
            'id',
            'thumbnail_url',
            'full_url',
            'alt_text',
            'is_primary',
            'position',
        ]

    def get_thumbnail_url(self, obj):
        if obj.media_asset:
            return obj.media_asset.get_thumbnail('medium') or obj.media_asset.get_display_url()
        return None

    def get_full_url(self, obj):
        if obj.media_asset:
            return obj.media_asset.get_display_url()
        return None


# --- Write Serializers ---

class ProductCreateSerializer(serializers.Serializer):
    """Serializer for creating a new product."""
    # Required
    name = serializers.CharField(max_length=255)
    sku = serializers.CharField(max_length=100)
    category_id = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    # Optional with defaults
    product_type = serializers.ChoiceField(
        choices=[c[0] for c in Product.PRODUCT_TYPES], default='simple'
    )
    status = serializers.ChoiceField(
        choices=[c[0] for c in Product.STATUS_CHOICES], default='draft'
    )
    currency = serializers.CharField(max_length=3, required=False, allow_blank=True)
    brand_id = serializers.IntegerField(required=False, allow_null=True)

    # Descriptions
    short_description = serializers.CharField(required=False, allow_blank=True, default='')
    full_description = serializers.CharField(required=False, allow_blank=True, default='')

    # Inventory
    track_inventory = serializers.BooleanField(default=True)
    low_stock_threshold = serializers.IntegerField(default=5, min_value=0)
    allow_backorders = serializers.BooleanField(default=False)
    initial_stock = serializers.IntegerField(default=0, min_value=0)

    # Physical
    weight = serializers.DecimalField(
        max_digits=10, decimal_places=3, required=False, allow_null=True
    )
    length = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    width = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    height = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )

    # SEO
    meta_title = serializers.CharField(max_length=255, required=False, allow_blank=True, default='')
    meta_description = serializers.CharField(max_length=160, required=False, allow_blank=True, default='')

    # Features & specs
    features = serializers.JSONField(required=False, default=dict)
    specifications = serializers.JSONField(required=False, default=dict)

    # Flags
    is_featured = serializers.BooleanField(default=False)

    # Sale
    sale_type = serializers.ChoiceField(
        choices=[c[0] for c in Product.SALE_TYPE_CHOICES], required=False, default='none'
    )
    sale_value = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )

    # Import tracking
    external_id = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')

    # Pre-generated translations (used by catalog_gen pipeline)
    translations = serializers.JSONField(required=False, default=dict)

    def validate_sku(self, value):
        if Product.objects.filter(sku=value).exists():
            raise serializers.ValidationError(_("A product with this SKU already exists."))
        return value

    def validate_category_id(self, value):
        try:
            Category.objects.get(id=value, is_active=True)
        except Category.DoesNotExist:
            raise serializers.ValidationError(_("Category not found or inactive."))
        return value

    def validate_brand_id(self, value):
        if value is not None:
            try:
                Brand.objects.get(id=value)
            except Brand.DoesNotExist:
                raise serializers.ValidationError(_("Brand not found."))
        return value


class ProductUpdateSerializer(serializers.Serializer):
    """Serializer for partial update of a product."""
    name = serializers.CharField(max_length=255, required=False)
    sku = serializers.CharField(max_length=100, required=False)
    category_id = serializers.IntegerField(required=False)
    brand_id = serializers.IntegerField(required=False, allow_null=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    currency = serializers.CharField(max_length=3, required=False, allow_blank=True)
    product_type = serializers.ChoiceField(
        choices=[c[0] for c in Product.PRODUCT_TYPES], required=False
    )
    status = serializers.ChoiceField(
        choices=[c[0] for c in Product.STATUS_CHOICES], required=False
    )
    short_description = serializers.CharField(required=False, allow_blank=True)
    full_description = serializers.CharField(required=False, allow_blank=True)
    track_inventory = serializers.BooleanField(required=False)
    low_stock_threshold = serializers.IntegerField(min_value=0, required=False)
    allow_backorders = serializers.BooleanField(required=False)
    weight = serializers.DecimalField(
        max_digits=10, decimal_places=3, required=False, allow_null=True
    )
    length = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    width = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    height = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    meta_title = serializers.CharField(max_length=255, required=False, allow_blank=True)
    meta_description = serializers.CharField(max_length=160, required=False, allow_blank=True)
    features = serializers.JSONField(required=False)
    specifications = serializers.JSONField(required=False)
    is_featured = serializers.BooleanField(required=False)
    sale_type = serializers.ChoiceField(
        choices=[c[0] for c in Product.SALE_TYPE_CHOICES], required=False
    )
    sale_value = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )

    def validate_sku(self, value):
        product = self.context.get('product')
        qs = Product.objects.filter(sku=value)
        if product:
            qs = qs.exclude(id=product.id)
        if qs.exists():
            raise serializers.ValidationError(_("A product with this SKU already exists."))
        return value

    def validate_category_id(self, value):
        try:
            Category.objects.get(id=value, is_active=True)
        except Category.DoesNotExist:
            raise serializers.ValidationError(_("Category not found or inactive."))
        return value

    def validate_brand_id(self, value):
        if value is not None:
            try:
                Brand.objects.get(id=value)
            except Brand.DoesNotExist:
                raise serializers.ValidationError(_("Brand not found."))
        return value


class BulkProductCreateSerializer(serializers.Serializer):
    """Wrapper serializer for bulk product creation."""
    products = ProductCreateSerializer(many=True)

    def validate_products(self, value):
        if len(value) > 100:
            raise serializers.ValidationError(_("Maximum 100 products per bulk request."))
        if len(value) == 0:
            raise serializers.ValidationError(_("At least one product is required."))
        return value


class BulkProductUpdateSerializer(serializers.Serializer):
    """Wrapper serializer for bulk product updates."""
    products = serializers.ListField(child=serializers.DictField())

    def validate_products(self, value):
        if len(value) > 100:
            raise serializers.ValidationError(_("Maximum 100 products per bulk request."))
        if len(value) == 0:
            raise serializers.ValidationError(_("At least one product is required."))
        for item in value:
            if 'id' not in item:
                raise serializers.ValidationError(
                    _("Each product must have an 'id' field.")
                )
        return value
