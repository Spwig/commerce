from rest_framework import serializers
from .cart import POSCartItemSerializer


class POSOrderItemSerializer(serializers.Serializer):
    """Order line item for POS display."""
    id = serializers.IntegerField()
    product_name = serializers.CharField()
    variant_name = serializers.CharField(allow_null=True, allow_blank=True)
    sku = serializers.CharField()
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    line_total = serializers.DecimalField(max_digits=10, decimal_places=2)


class POSPaymentDetailSerializer(serializers.Serializer):
    """Payment detail in order context."""
    method = serializers.CharField()
    method_display = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    amount_tendered = serializers.DecimalField(
        max_digits=10, decimal_places=2, allow_null=True
    )
    change_given = serializers.DecimalField(
        max_digits=10, decimal_places=2, allow_null=True
    )
    card_last_four = serializers.CharField(allow_blank=True)


class POSOrderSerializer(serializers.Serializer):
    """Full order for POS display."""
    id = serializers.IntegerField()
    order_number = serializers.CharField()
    status = serializers.CharField()
    channel = serializers.CharField()
    items = POSOrderItemSerializer(many=True)
    payments = POSPaymentDetailSerializer(many=True, required=False)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    discount_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField()
    customer_name = serializers.CharField(allow_null=True, allow_blank=True)
    customer_email = serializers.CharField(allow_null=True, allow_blank=True)
    cashier_name = serializers.CharField(allow_null=True, allow_blank=True)
    terminal_name = serializers.CharField(allow_null=True, allow_blank=True)
    created_at = serializers.DateTimeField()


class POSOrderListSerializer(serializers.Serializer):
    """Lightweight order for POS order list."""
    id = serializers.IntegerField()
    order_number = serializers.CharField()
    status = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField()
    item_count = serializers.IntegerField()
    customer_name = serializers.CharField(allow_null=True, allow_blank=True)
    cashier_name = serializers.CharField(allow_null=True, allow_blank=True)
    created_at = serializers.DateTimeField()


class POSReceiptSerializer(serializers.Serializer):
    """Receipt data for printing."""
    order_number = serializers.CharField()
    store_name = serializers.CharField()
    store_address = serializers.CharField(allow_blank=True)
    store_phone = serializers.CharField(allow_blank=True)
    terminal_name = serializers.CharField()
    cashier_name = serializers.CharField()
    items = POSOrderItemSerializer(many=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    discount_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField()
    payments = POSPaymentDetailSerializer(many=True)
    change_given = serializers.DecimalField(
        max_digits=10, decimal_places=2, allow_null=True
    )
    date = serializers.DateTimeField()
    footer_text = serializers.CharField(allow_blank=True)
