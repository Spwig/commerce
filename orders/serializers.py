"""
Serializers for Orders app
"""

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from catalog.serializers import ProductListSerializer, ProductVariantSerializer

from .models import Address, Order, OrderItem, ReturnRequest


class OrderAddressSerializer(serializers.ModelSerializer):
    """Serializer for order addresses"""

    class Meta:
        model = Address
        fields = [
            "id",
            "user",
            "address_type",
            "name",
            "company",
            "address1",
            "address2",
            "city",
            "state",
            "postal_code",
            "country",
            "phone",
            "is_default",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order items"""

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "product",
            "variant",
            "product_name",
            "variant_name",
            "sku",
            "quantity",
            "unit_price",
            "total_price",
            "customizations",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for orders"""

    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "user",
            "status",
            "tracking_number",
            "email",
            "phone",
            "shipping_name",
            "shipping_address1",
            "shipping_address2",
            "shipping_city",
            "shipping_state",
            "shipping_postal_code",
            "shipping_country",
            "billing_same_as_shipping",
            "billing_name",
            "billing_address1",
            "billing_address2",
            "billing_city",
            "billing_state",
            "billing_postal_code",
            "billing_country",
            "subtotal",
            "tax_amount",
            "shipping_cost",
            "discount_amount",
            "total_amount",
            "order_page_layout",
            "show_order_progress",
            "show_shipping_updates",
            "show_item_images",
            "notes",
            "special_instructions",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "order_number", "created_at", "updated_at"]


class OrderSummarySerializer(serializers.ModelSerializer):
    """Lightweight order serializer for lists"""

    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "status",
            "status_display",
            "total_amount",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "order_number", "created_at", "updated_at"]


class CreateAddressSerializer(serializers.Serializer):
    """Serializer for creating new addresses"""

    address_type = serializers.ChoiceField(choices=Address.ADDRESS_TYPES, default="both")
    name = serializers.CharField(max_length=200)
    company = serializers.CharField(max_length=200, required=False, allow_blank=True)
    address1 = serializers.CharField(max_length=200)
    address2 = serializers.CharField(max_length=200, required=False, allow_blank=True)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    postal_code = serializers.CharField(max_length=20)
    country = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    is_default = serializers.BooleanField(default=False)


class UpdateAddressSerializer(serializers.Serializer):
    """Serializer for updating addresses"""

    address_type = serializers.ChoiceField(choices=Address.ADDRESS_TYPES, required=False)
    name = serializers.CharField(max_length=200, required=False)
    company = serializers.CharField(max_length=200, required=False, allow_blank=True)
    address1 = serializers.CharField(max_length=200, required=False)
    address2 = serializers.CharField(max_length=200, required=False, allow_blank=True)
    city = serializers.CharField(max_length=100, required=False)
    state = serializers.CharField(max_length=100, required=False)
    postal_code = serializers.CharField(max_length=20, required=False)
    country = serializers.CharField(max_length=100, required=False)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    is_default = serializers.BooleanField(required=False)


class OrderItemDetailSerializer(serializers.ModelSerializer):
    """Detailed order item serializer with product information"""

    product = ProductListSerializer(read_only=True)
    variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "variant",
            "product_name",
            "variant_name",
            "sku",
            "quantity",
            "unit_price",
            "total_price",
            "customizations",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class OrderDetailSerializer(serializers.ModelSerializer):
    """Detailed order serializer with nested product information"""

    items = OrderItemDetailSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    can_cancel = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "user",
            "status",
            "status_display",
            "tracking_number",
            "email",
            "phone",
            "shipping_name",
            "shipping_address1",
            "shipping_address2",
            "shipping_city",
            "shipping_state",
            "shipping_postal_code",
            "shipping_country",
            "billing_same_as_shipping",
            "billing_name",
            "billing_address1",
            "billing_address2",
            "billing_city",
            "billing_state",
            "billing_postal_code",
            "billing_country",
            "subtotal",
            "tax_amount",
            "shipping_cost",
            "discount_amount",
            "total_amount",
            "order_page_layout",
            "show_order_progress",
            "show_shipping_updates",
            "show_item_images",
            "notes",
            "special_instructions",
            "items",
            "can_cancel",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "order_number", "user", "created_at", "updated_at"]

    def get_can_cancel(self, obj) -> bool:
        """Check if order can be cancelled"""
        request = self.context.get("request")
        if not request or not request.user:
            return False

        from .services import OrderService

        can_cancel, _ = OrderService.can_cancel_order(obj, request.user)
        return can_cancel


class CancelOrderSerializer(serializers.Serializer):
    """Serializer for cancelling orders"""

    reason = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
        help_text=_("Reason for cancellation (optional)"),
    )
    restore_stock = serializers.BooleanField(
        default=True, help_text=_("Restore product stock quantities")
    )


class OrderTrackingSerializer(serializers.Serializer):
    """Serializer for order tracking information"""

    order_number = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    status_display = serializers.CharField(read_only=True)
    tracking_number = serializers.CharField(read_only=True)
    estimated_delivery = serializers.CharField(read_only=True, allow_null=True)
    shipping_address = serializers.DictField(read_only=True)
    timeline = serializers.ListField(read_only=True)


class ReorderSerializer(serializers.Serializer):
    """Serializer for reorder response"""

    success = serializers.BooleanField(read_only=True)
    message = serializers.CharField(read_only=True)
    cart_id = serializers.IntegerField(read_only=True, allow_null=True)


# Phase 7: Returns & RMA Workflow Serializers


class ReturnItemSerializer(serializers.Serializer):
    """Serializer for individual items in a return request"""

    order_item_id = serializers.IntegerField(help_text=_("ID of the order item being returned"))
    quantity = serializers.IntegerField(min_value=1, help_text=_("Quantity of this item to return"))
    reason = serializers.ChoiceField(
        choices=ReturnRequest.RETURN_REASON_CHOICES,
        help_text=_("Reason for returning this specific item"),
    )
    notes = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
        help_text=_("Additional notes about this item (optional)"),
    )


class CreateReturnRequestSerializer(serializers.Serializer):
    """Serializer for creating a return request"""

    reason = serializers.ChoiceField(
        choices=ReturnRequest.RETURN_REASON_CHOICES, help_text=_("Main reason for return")
    )
    items = ReturnItemSerializer(
        many=True, help_text=_("List of items to return with quantities and reasons")
    )
    customer_notes = serializers.CharField(
        required=False, allow_blank=True, help_text=_("Additional notes from customer")
    )

    def validate_items(self, items):
        """Validate that items are provided"""
        if not items:
            raise serializers.ValidationError(_("At least one item must be selected for return"))
        return items


class ReturnRequestSerializer(serializers.ModelSerializer):
    """Serializer for return request details"""

    order_number = serializers.CharField(source="order.order_number", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    reason_display = serializers.CharField(source="get_reason_display", read_only=True)
    items_condition_display = serializers.CharField(
        source="get_items_condition_display", read_only=True, allow_null=True
    )
    refund_status = serializers.SerializerMethodField()
    suggested_refund = serializers.SerializerMethodField()

    class Meta:
        model = ReturnRequest
        fields = [
            "id",
            "order",
            "order_number",
            "user",
            "user_email",
            "reason",
            "reason_display",
            "status",
            "status_display",
            "items_json",
            "customer_notes",
            "merchant_notes",
            "return_label_generated",
            "return_tracking_number",
            "return_label_url",
            "items_condition",
            "items_condition_display",
            "restocking_fee",
            "refund_status",
            "suggested_refund",
            "requested_at",
            "approved_at",
            "received_at",
            "inspected_at",
            "completed_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "status",
            "return_label_generated",
            "return_tracking_number",
            "return_label_url",
            "merchant_notes",
            "items_condition",
            "restocking_fee",
            "requested_at",
            "approved_at",
            "received_at",
            "inspected_at",
            "completed_at",
        ]

    def get_refund_status(self, obj) -> dict | None:
        """Get refund status if refund exists"""
        if obj.refund:
            return {
                "status": obj.refund.status,
                "status_display": obj.refund.get_status_display(),
                "amount": str(obj.refund.total_amount.amount),
                "currency": obj.refund.total_amount.currency.code,
            }
        return None

    def get_suggested_refund(self, obj) -> dict:
        """Get suggested refund amount"""
        amount = obj.calculate_refund_amount()
        return {"amount": str(amount), "currency": obj.order.total_amount.currency.code}


class ReturnRequestSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for return request lists"""

    order_number = serializers.CharField(source="order.order_number", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    reason_display = serializers.CharField(source="get_reason_display", read_only=True)
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = ReturnRequest
        fields = [
            "id",
            "order_number",
            "reason",
            "reason_display",
            "status",
            "status_display",
            "items_count",
            "return_tracking_number",
            "requested_at",
        ]

    def get_items_count(self, obj) -> int:
        """Get total number of items in return"""
        return len(obj.items_json)


# ============================================================================
# Order Notes Serializers
# ============================================================================


class OrderNoteSerializer(serializers.ModelSerializer):
    """Serializer for order notes visible to customers"""

    author_name = serializers.SerializerMethodField()
    is_merchant = serializers.SerializerMethodField()

    class Meta:
        from .models import OrderNote

        model = OrderNote
        fields = ["id", "note", "author_name", "is_merchant", "created_at", "updated_at"]
        read_only_fields = fields

    def get_author_name(self, obj) -> str:
        """Get display name of note author"""
        if not obj.author:
            return _("Store")
        # Only show customer name for customer notes, otherwise just "Store"
        if obj.author == self.context.get("request", {}).user:
            return obj.author.get_full_name() or obj.author.email
        return _("Store")

    def get_is_merchant(self, obj) -> bool:
        """Check if note was created by merchant/staff"""
        if not obj.author:
            return True
        return obj.author.is_staff


class CreateOrderNoteSerializer(serializers.Serializer):
    """Serializer for creating customer notes on orders"""

    note = serializers.CharField(max_length=2000, help_text=_("Note content (max 2000 characters)"))

    def validate_note(self, value):
        """Validate note content"""
        if not value.strip():
            raise serializers.ValidationError(_("Note cannot be empty"))
        return value.strip()
