from rest_framework import serializers


class POSProductVariantSerializer(serializers.Serializer):
    """Lightweight variant serializer for POS product display."""

    id = serializers.IntegerField()
    sku = serializers.CharField()
    barcode = serializers.CharField(allow_blank=True)
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    attributes = serializers.DictField(required=False)
    stock_available = serializers.IntegerField(required=False)
    image = serializers.URLField(required=False, allow_null=True)


class POSProductSerializer(serializers.Serializer):
    """Full product serializer for POS product detail."""

    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.CharField()
    sku = serializers.CharField()
    barcode = serializers.CharField(allow_blank=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField()
    product_type = serializers.CharField()
    sales_channel = serializers.CharField()
    category_id = serializers.IntegerField(allow_null=True)
    category_name = serializers.CharField(allow_null=True)
    image = serializers.URLField(required=False, allow_null=True)
    images = serializers.ListField(child=serializers.URLField(), required=False)
    track_inventory = serializers.BooleanField()
    stock_available = serializers.IntegerField(required=False)
    is_low_stock = serializers.BooleanField(required=False)
    variants = POSProductVariantSerializer(many=True, required=False)
    has_variants = serializers.BooleanField()
    updated_at = serializers.DateTimeField()


class POSProductListSerializer(serializers.Serializer):
    """Lightweight product serializer for POS grid display."""

    id = serializers.IntegerField()
    name = serializers.CharField()
    sku = serializers.CharField()
    barcode = serializers.CharField(allow_blank=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField()
    product_type = serializers.CharField()
    category_id = serializers.IntegerField(allow_null=True)
    image = serializers.URLField(required=False, allow_null=True)
    stock_available = serializers.IntegerField(required=False)
    has_variants = serializers.BooleanField()


class POSCategorySerializer(serializers.Serializer):
    """Category tree serializer for POS navigation."""

    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.CharField()
    parent_id = serializers.IntegerField(allow_null=True)
    product_count = serializers.IntegerField(required=False)
    children = serializers.ListField(required=False)
