"""
Order Serializers for Admin API

Serializers for order management in the merchant mobile app.
"""

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from orders.models import Order, OrderItem


class AdminOrderItemSerializer(serializers.ModelSerializer):
    """Order item serializer for order details (admin/mobile app)."""

    unit_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="unit_price.amount"
    )
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="total_price.amount"
    )
    currency = serializers.CharField(source="unit_price.currency.code", read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_id",
            "product_name",
            "variant_name",
            "sku",
            "quantity",
            "unit_price",
            "total_price",
            "currency",
            "image_url",
        ]

    def get_image_url(self, obj):
        """Get product/variant thumbnail image URL."""
        # Try variant image first (if item has a variant)
        if obj.variant:
            variant_image = obj.variant.images.filter(is_primary=True).first()
            if not variant_image:
                variant_image = obj.variant.images.first()
            if variant_image:
                return variant_image.thumbnail_small

        # Fall back to product primary image
        product_image = obj.product.images.filter(is_primary=True).first()
        if not product_image:
            product_image = obj.product.images.first()
        if product_image:
            return product_image.thumbnail_small

        return None


class AdminOrderListSerializer(serializers.ModelSerializer):
    """Compact serializer for order list view (admin/mobile app)."""

    total_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="total_amount.amount"
    )
    currency = serializers.CharField(source="total_amount.currency.code", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    payment_status_display = serializers.CharField(
        source="get_payment_status_display", read_only=True
    )
    customer_name = serializers.CharField(source="shipping_name", read_only=True)
    item_count = serializers.IntegerField(source="total_item_quantity", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "status",
            "status_display",
            "payment_status",
            "payment_status_display",
            "customer_name",
            "email",
            "total_amount",
            "currency",
            "item_count",
            "created_at",
            "updated_at",
        ]


class AdminOrderDetailSerializer(serializers.ModelSerializer):
    """Full serializer for order detail view (admin/mobile app)."""

    items = AdminOrderItemSerializer(many=True, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, source="subtotal.amount")
    tax_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="tax_amount.amount"
    )
    shipping_cost = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="shipping_cost.amount"
    )
    discount_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="discount_amount.amount"
    )
    total_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="total_amount.amount"
    )
    amount_paid = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="amount_paid.amount"
    )
    amount_refunded = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="amount_refunded.amount"
    )
    currency = serializers.CharField(source="total_amount.currency.code", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    payment_status_display = serializers.CharField(
        source="get_payment_status_display", read_only=True
    )
    item_count = serializers.IntegerField(source="total_item_quantity", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "status",
            "status_display",
            "payment_status",
            "payment_status_display",
            # Customer info
            "email",
            "phone",
            # Shipping address
            "shipping_name",
            "shipping_address1",
            "shipping_address2",
            "shipping_city",
            "shipping_state",
            "shipping_postal_code",
            "shipping_country",
            "shipping_phone",
            # Billing address
            "billing_same_as_shipping",
            "billing_name",
            "billing_address1",
            "billing_address2",
            "billing_city",
            "billing_state",
            "billing_postal_code",
            "billing_country",
            # Totals
            "subtotal",
            "tax_amount",
            "shipping_cost",
            "discount_amount",
            "total_amount",
            "amount_paid",
            "amount_refunded",
            "currency",
            # Shipping & tracking
            "tracking_number",
            "estimated_delivery_date",
            "delivered_at",
            # Notes
            "notes",
            "special_instructions",
            # Items
            "items",
            "item_count",
            # Timestamps
            "created_at",
            "updated_at",
            "paid_at",
        ]


class OrderStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating order status."""

    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)
    tracking_number = serializers.CharField(required=False, allow_blank=True, max_length=100)
    notes = serializers.CharField(required=False, allow_blank=True, max_length=1000)

    def validate_status(self, value):
        """Validate status transition is allowed."""
        order = self.context.get("order")
        if not order:
            return value

        current_status = order.status
        allowed_transitions = {
            "pending": ["processing", "cancelled"],
            "processing": ["shipped", "cancelled", "pending"],
            "shipped": ["delivered", "processing"],
            "delivered": ["refunded"],
            "cancelled": ["pending"],  # Allow reopening cancelled orders
            "refunded": [],  # Terminal state
        }

        if value not in allowed_transitions.get(current_status, []):
            raise serializers.ValidationError(
                f"Cannot transition from '{current_status}' to '{value}'."
            )

        return value


class TrackingUpdateSerializer(serializers.Serializer):
    """Serializer for updating tracking information."""

    tracking_number = serializers.CharField(max_length=100)
    carrier = serializers.CharField(required=False, allow_blank=True, max_length=100)


class OrderRefundSerializer(serializers.Serializer):
    """Serializer for initiating order refund."""

    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        help_text=_("Refund amount. If not provided, full refund is assumed."),
    )
    reason = serializers.CharField(max_length=500, required=False, allow_blank=True)

    def validate_amount(self, value):
        """Validate refund amount."""
        order = self.context.get("order")
        if not order:
            return value

        max_refundable = order.amount_paid.amount - order.amount_refunded.amount
        if value and value > max_refundable:
            raise serializers.ValidationError(f"Refund amount cannot exceed {max_refundable}.")

        return value


class OrderCancelSerializer(serializers.Serializer):
    """Serializer for cancelling an order."""

    reason = serializers.CharField(max_length=500, required=False, allow_blank=True)
    notify_customer = serializers.BooleanField(default=True)


class OrderNoteCreateSerializer(serializers.Serializer):
    """Serializer for creating an order note (merchant reply)."""

    note = serializers.CharField(max_length=2000, help_text=_("Note content"))
    is_customer_visible = serializers.BooleanField(
        default=True, help_text=_("Whether this note is visible to the customer")
    )
    notify_customer = serializers.BooleanField(
        default=False, help_text=_("Whether to send email notification to customer")
    )


class OrderNoteSerializer(serializers.Serializer):
    """Serializer for order note response."""

    id = serializers.IntegerField()
    note = serializers.CharField()
    is_customer_visible = serializers.BooleanField(source="is_customer_note")
    is_customer_note = serializers.BooleanField()
    author_name = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()

    def get_author_name(self, obj):
        if obj.author:
            return obj.author.get_full_name() or obj.author.email
        return "System"


class OrderFilterSerializer(serializers.Serializer):
    """Serializer for order list filters."""

    status = serializers.ChoiceField(
        choices=[("all", "All")] + Order.STATUS_CHOICES, required=False, default="all"
    )
    filter_type = serializers.ChoiceField(
        choices=[
            ("all", "All Orders"),
            ("open", "Open Orders"),
            ("completed", "Completed Orders"),
            ("refunded", "Refunded Orders"),
        ],
        required=False,
        default="all",
    )
    search = serializers.CharField(required=False, allow_blank=True)
    sort = serializers.ChoiceField(
        choices=[
            ("-created_at", "Newest First"),
            ("created_at", "Oldest First"),
            ("-total_amount", "Highest Value"),
            ("total_amount", "Lowest Value"),
            ("-updated_at", "Recently Updated"),
            ("updated_at", "Least Recently Updated"),
            ("customer_name", "Customer A-Z"),
            ("-customer_name", "Customer Z-A"),
        ],
        required=False,
        default="-created_at",
    )
    date_from = serializers.DateField(
        required=False, help_text=_("Filter orders created on or after this date (YYYY-MM-DD)")
    )
    date_to = serializers.DateField(
        required=False, help_text=_("Filter orders created on or before this date (YYYY-MM-DD)")
    )
    page = serializers.IntegerField(required=False, default=1, min_value=1)
    page_size = serializers.IntegerField(required=False, default=20, min_value=1, max_value=100)
