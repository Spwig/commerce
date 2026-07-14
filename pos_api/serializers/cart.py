from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class POSCartItemSerializer(serializers.Serializer):
    """Cart item for POS display."""

    id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    variant_id = serializers.IntegerField(allow_null=True)
    variant_name = serializers.CharField(allow_null=True, allow_blank=True)
    sku = serializers.CharField()
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    line_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    image = serializers.URLField(required=False, allow_null=True)


class POSCartSerializer(serializers.Serializer):
    """Full cart for POS display."""

    id = serializers.IntegerField()
    items = POSCartItemSerializer(many=True)
    item_count = serializers.IntegerField()
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    discount_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField()
    voucher_code = serializers.CharField(allow_null=True, allow_blank=True)
    gift_card_applied = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)


class POSAddToCartSerializer(serializers.Serializer):
    """Add item to POS cart."""

    product_id = serializers.IntegerField()
    variant_id = serializers.IntegerField(required=False, allow_null=True)
    quantity = serializers.IntegerField(min_value=1, max_value=9999, default=1)
    barcode = serializers.CharField(required=False, allow_blank=True)
    configuration = serializers.DictField(required=False, allow_null=True)
    preset_id = serializers.IntegerField(required=False, allow_null=True)
    variant_selections = serializers.DictField(
        child=serializers.IntegerField(),
        required=False,
        allow_null=True,
        help_text=_("Bundle variant selections: {bundle_item_id: variant_id}"),
    )
    excluded_optional_items = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_null=True,
        help_text=_("List of optional BundleItem IDs to exclude"),
    )


class POSUpdateCartItemSerializer(serializers.Serializer):
    """Update cart item quantity."""

    quantity = serializers.IntegerField(min_value=0, max_value=9999)


class POSApplyDiscountSerializer(serializers.Serializer):
    """Apply voucher/discount code."""

    code = serializers.CharField(max_length=50)


class POSApplyGiftCardSerializer(serializers.Serializer):
    """Apply gift card to cart."""

    code = serializers.CharField(max_length=50)
