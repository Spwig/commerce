from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class POSStockItemSerializer(serializers.Serializer):
    """Stock level for a product in a warehouse."""

    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    sku = serializers.CharField(allow_blank=True)
    variant_id = serializers.IntegerField(allow_null=True)
    variant_name = serializers.CharField(allow_null=True, allow_blank=True)
    on_hand = serializers.IntegerField()
    allocated = serializers.IntegerField()
    available = serializers.IntegerField()
    low_stock_threshold = serializers.IntegerField()
    is_low_stock = serializers.BooleanField()
    image = serializers.CharField(allow_null=True, allow_blank=True)
    has_stock_item = serializers.BooleanField()
    product_type = serializers.CharField()


class POSCrossLocationStockSerializer(serializers.Serializer):
    """Stock at a single warehouse location with contact details."""

    warehouse_id = serializers.IntegerField()
    warehouse_name = serializers.CharField()
    is_current = serializers.BooleanField()
    on_hand = serializers.IntegerField()
    allocated = serializers.IntegerField()
    available = serializers.IntegerField()
    contact_name = serializers.CharField(allow_blank=True)
    contact_phone = serializers.CharField(allow_blank=True)
    contact_email = serializers.CharField(allow_blank=True)
    address = serializers.CharField(allow_blank=True)
    city = serializers.CharField(allow_blank=True)
    country = serializers.CharField(allow_blank=True)
    region_name = serializers.CharField(allow_blank=True)
    same_region = serializers.BooleanField()
    distance_km = serializers.FloatField(allow_null=True)


class POSStockAdjustmentSerializer(serializers.Serializer):
    """Request body for stock adjustment operations."""

    product_id = serializers.IntegerField(help_text=_("ID of the product to adjust stock for."))
    variant_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text=_("ID of the variant (required for variable products)."),
    )
    adjustment_type = serializers.ChoiceField(
        choices=["receive", "damage", "recount", "return"],
        help_text=_(
            "Type of adjustment: "
            '"receive" adds stock (e.g. new shipment), '
            '"damage" removes stock (e.g. broken item), '
            '"recount" sets absolute on_hand count, '
            '"return" adds stock back (e.g. customer return).'
        ),
    )
    quantity = serializers.IntegerField(
        min_value=0,
        help_text=_(
            "For receive/return: units to add. "
            "For damage: units to remove. "
            "For recount: new absolute on_hand count."
        ),
    )
    reason = serializers.CharField(
        min_length=1, help_text=_("Required explanation for this adjustment (audit trail).")
    )
    idempotency_key = serializers.CharField(
        required=False, max_length=64, help_text=_("Optional UUID for offline deduplication.")
    )


class POSStockMovementSerializer(serializers.Serializer):
    """A single stock movement record for audit trail display."""

    id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    sku = serializers.CharField(allow_blank=True)
    variant_id = serializers.IntegerField(allow_null=True)
    variant_name = serializers.CharField(allow_null=True, allow_blank=True)
    movement_type = serializers.CharField()
    quantity = serializers.IntegerField(help_text=_("Signed quantity delta."))
    previous_quantity = serializers.IntegerField()
    new_quantity = serializers.IntegerField()
    reason = serializers.CharField(allow_blank=True)
    user_name = serializers.CharField(allow_blank=True)
    created_at = serializers.DateTimeField()
