"""
Bulk Operation Serializers for Admin API

Serializers for bulk order and product operations.
"""

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

# =============================================================================
# Bulk Order Serializers
# =============================================================================


class BulkOrderStatusSerializer(serializers.Serializer):
    """Serializer for bulk order status update requests."""

    order_numbers = serializers.ListField(
        child=serializers.CharField(max_length=32),
        min_length=1,
        max_length=100,
        help_text=_("List of order numbers to update (max 100)."),
    )
    status = serializers.ChoiceField(
        choices=["pending", "processing", "shipped", "delivered", "cancelled", "refunded"],
        help_text=_("New status to set for all specified orders."),
    )


class BulkOrderFulfillItemSerializer(serializers.Serializer):
    """Serializer for an individual order in a bulk fulfillment request."""

    order_number = serializers.CharField(max_length=32, help_text=_("Order number to fulfill."))
    tracking_number = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        default="",
        help_text=_("Tracking number for the shipment."),
    )
    tracking_url = serializers.URLField(
        required=False, allow_blank=True, default="", help_text=_("Tracking URL for the shipment.")
    )
    carrier = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        default="",
        help_text=_("Carrier name or identifier."),
    )


class BulkOrderFulfillSerializer(serializers.Serializer):
    """Serializer for bulk order fulfillment requests."""

    orders = serializers.ListField(
        child=BulkOrderFulfillItemSerializer(),
        min_length=1,
        max_length=100,
        help_text=_("List of orders to fulfill (max 100)."),
    )
    notify_customers = serializers.BooleanField(
        default=True, help_text=_("Whether to send shipping notification emails to customers.")
    )


# =============================================================================
# Bulk Product Serializers
# =============================================================================


class StockAdjustmentItemSerializer(serializers.Serializer):
    """Serializer for a single stock adjustment within a bulk request."""

    product_id = serializers.IntegerField(help_text=_("Product ID to adjust stock for."))
    variant_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        default=None,
        help_text=_("Variant ID (null for simple products)."),
    )
    warehouse_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        default=None,
        help_text=_("Warehouse ID (null uses default warehouse)."),
    )
    quantity = serializers.IntegerField(
        help_text=_(
            "Stock quantity: for 'set' this is the new value; for 'adjust' this is the delta (can be negative)."
        )
    )
    adjustment_type = serializers.ChoiceField(
        choices=["set", "adjust"],
        help_text=_("'set': set on_hand to quantity. 'adjust': add quantity to on_hand."),
    )


class BulkStockAdjustSerializer(serializers.Serializer):
    """Serializer for bulk stock adjustment requests."""

    adjustments = serializers.ListField(
        child=StockAdjustmentItemSerializer(),
        min_length=1,
        max_length=100,
        help_text=_("List of stock adjustments (max 100)."),
    )
    reason = serializers.CharField(max_length=500, help_text=_("Reason for the stock adjustment."))
    notes = serializers.CharField(
        max_length=2000,
        required=False,
        allow_blank=True,
        default="",
        help_text=_("Additional notes about the adjustment."),
    )


class BulkPriceUpdateSerializer(serializers.Serializer):
    """Serializer for bulk price update requests."""

    product_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        max_length=100,
        help_text=_("List of product IDs to update (max 100)."),
    )
    update_type = serializers.ChoiceField(
        choices=["absolute", "percentage"],
        help_text=_("'absolute': set price to value. 'percentage': adjust price by percentage."),
    )
    value = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text=_(
            "Price value: absolute amount or percentage change (e.g., -10 for 10%% decrease)."
        ),
    )
    apply_to = serializers.ChoiceField(
        choices=["price"], default="price", help_text=_("Which price field to update.")
    )
    round_to = serializers.IntegerField(
        required=False,
        default=2,
        min_value=0,
        max_value=4,
        help_text=_("Number of decimal places to round the result to."),
    )


class BulkAssignCategorySerializer(serializers.Serializer):
    """Serializer for bulk category assignment requests."""

    product_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        max_length=100,
        help_text=_("List of product IDs to reassign (max 100)."),
    )
    category_id = serializers.IntegerField(help_text=_("Target category ID to assign products to."))


class BulkAssignTagsSerializer(serializers.Serializer):
    """Serializer for bulk tag assignment requests."""

    product_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        max_length=100,
        help_text=_("List of product IDs to update tags for (max 100)."),
    )
    tags = serializers.ListField(
        child=serializers.SlugField(max_length=100),
        min_length=1,
        help_text=_("List of tag slugs to add/replace/remove."),
    )
    mode = serializers.ChoiceField(
        choices=["add", "replace", "remove"],
        help_text=_(
            "'add': add tags. 'replace': replace all tags. 'remove': remove specified tags."
        ),
    )


class BulkSaleUpdateSerializer(serializers.Serializer):
    """Serializer for bulk sale update requests."""

    product_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        max_length=100,
        help_text=_("List of product IDs to update (max 100)."),
    )
    sale_type = serializers.ChoiceField(
        choices=["none", "fixed_price", "amount_off", "percentage_off"],
        help_text=_(
            "'none': clear sale. 'fixed_price': set a fixed sale price. "
            "'amount_off': subtract amount from base price. "
            "'percentage_off': apply percentage discount."
        ),
    )
    sale_value = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        allow_null=True,
        default=None,
        help_text=_(
            "Sale value: fixed price, discount amount, or discount percentage. "
            "Required when sale_type is not 'none'."
        ),
    )
    sale_start_date = serializers.DateTimeField(
        required=False,
        allow_null=True,
        default=None,
        help_text=_("When the sale begins (null for immediate start)."),
    )
    sale_end_date = serializers.DateTimeField(
        required=False,
        allow_null=True,
        default=None,
        help_text=_("When the sale ends (null for no end date)."),
    )

    def validate(self, data):
        sale_type = data["sale_type"]
        sale_value = data.get("sale_value")

        if sale_type == "none":
            data["sale_value"] = None
            data["sale_start_date"] = None
            data["sale_end_date"] = None
            return data

        if sale_value is None:
            raise serializers.ValidationError(
                {"sale_value": _('sale_value is required when sale_type is not "none".')}
            )
        if sale_value < 0:
            raise serializers.ValidationError({"sale_value": _("sale_value must not be negative.")})
        if sale_type == "percentage_off" and sale_value > 100:
            raise serializers.ValidationError(
                {"sale_value": _("Percentage off cannot exceed 100.")}
            )

        start = data.get("sale_start_date")
        end = data.get("sale_end_date")
        if start and end and start >= end:
            raise serializers.ValidationError(
                {"sale_end_date": _("sale_end_date must be after sale_start_date.")}
            )

        return data


# =============================================================================
# Document Batch Serializer
# =============================================================================


class BatchDocumentsSerializer(serializers.Serializer):
    """Serializer for batch document generation requests."""

    order_numbers = serializers.ListField(
        child=serializers.CharField(max_length=32),
        min_length=1,
        max_length=50,
        help_text=_("List of order numbers to generate documents for (max 50)."),
    )
    document_types = serializers.ListField(
        child=serializers.ChoiceField(choices=["invoice", "packing_slip", "pick_list"]),
        min_length=1,
        help_text=_("Types of documents to generate for each order."),
    )
