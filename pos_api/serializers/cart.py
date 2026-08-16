from decimal import Decimal

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

    product_id = serializers.IntegerField(required=False, allow_null=True)
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

    def validate(self, attrs):
        """Require at least one nonblank product_id or barcode."""
        product_id = attrs.get("product_id")
        barcode = (attrs.get("barcode") or "").strip()
        if product_id is None and not barcode:
            raise serializers.ValidationError(_("Either product_id or barcode is required."))
        return attrs


class POSUpdateCartItemSerializer(serializers.Serializer):
    """Update cart item quantity."""

    quantity = serializers.IntegerField(min_value=0, max_value=9999)


class POSApplyDiscountSerializer(serializers.Serializer):
    """Apply voucher/discount code."""

    code = serializers.CharField(max_length=50)


class POSManualDiscountSerializer(serializers.Serializer):
    """Validate a manual (staff/manager) discount payload.

    Shared by the item-level, cart-level, and manager-approval discount
    endpoints so malformed ``discount_value`` input (e.g. ``"abc"``) returns a
    400 instead of raising ``decimal.InvalidOperation``.
    """

    discount_type = serializers.ChoiceField(choices=("percentage", "fixed"))
    discount_value = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0.01"),
    )
    reason = serializers.CharField(required=False, allow_blank=True, default="")
