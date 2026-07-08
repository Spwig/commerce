from rest_framework import serializers


class POSOfflineTransactionItemSerializer(serializers.Serializer):
    """Single item in an offline transaction."""
    product_id = serializers.IntegerField()
    variant_id = serializers.IntegerField(required=False, allow_null=True)
    quantity = serializers.IntegerField(min_value=1, max_value=9999)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)


class POSOfflinePaymentSerializer(serializers.Serializer):
    """Payment in an offline transaction."""
    method = serializers.ChoiceField(choices=['cash', 'card', 'gift_card'])
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    amount_tendered = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    card_last_four = serializers.CharField(required=False, allow_blank=True)
    card_reference = serializers.CharField(required=False, allow_blank=True)
    gift_card_code = serializers.CharField(required=False, allow_blank=True)


class POSOfflineTransactionSerializer(serializers.Serializer):
    """Single offline transaction for batch upload."""
    local_id = serializers.CharField(max_length=100)
    terminal_uuid = serializers.UUIDField()
    cashier_id = serializers.IntegerField()
    items = POSOfflineTransactionItemSerializer(many=True)
    payments = POSOfflinePaymentSerializer(many=True)
    customer_id = serializers.IntegerField(required=False, allow_null=True)
    created_at = serializers.DateTimeField()


class POSOfflineUploadSerializer(serializers.Serializer):
    """Batch offline transaction upload."""
    transactions = POSOfflineTransactionSerializer(many=True)


class POSOfflineStockAdjustmentItemSerializer(serializers.Serializer):
    """Single offline stock adjustment."""
    idempotency_key = serializers.CharField(max_length=64)
    product_id = serializers.IntegerField()
    variant_id = serializers.IntegerField(required=False, allow_null=True)
    adjustment_type = serializers.ChoiceField(
        choices=['receive', 'damage', 'recount', 'return']
    )
    quantity = serializers.IntegerField(min_value=0)
    reason = serializers.CharField(min_length=1)
    created_at = serializers.DateTimeField(required=False)


class POSOfflineStockAdjustmentUploadSerializer(serializers.Serializer):
    """Batch offline stock adjustment upload."""
    adjustments = POSOfflineStockAdjustmentItemSerializer(many=True)


class POSOrderSyncItemSerializer(serializers.Serializer):
    """Order line item for offline sync."""
    id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    variant_name = serializers.CharField(allow_null=True, allow_blank=True)
    sku = serializers.CharField(allow_blank=True)
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    line_total = serializers.DecimalField(max_digits=10, decimal_places=2)


class POSOrderSyncPaymentSerializer(serializers.Serializer):
    """Payment detail for offline sync."""
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


class POSOrderSyncSerializer(serializers.Serializer):
    """Full order for offline sync cache."""
    id = serializers.IntegerField()
    order_number = serializers.CharField()
    status = serializers.CharField()
    channel = serializers.CharField()
    items = POSOrderSyncItemSerializer(many=True)
    payments = POSOrderSyncPaymentSerializer(many=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField()
    customer_name = serializers.CharField(allow_null=True, allow_blank=True)
    customer_email = serializers.CharField(allow_null=True, allow_blank=True)
    cashier_name = serializers.CharField(allow_null=True, allow_blank=True)
    terminal_name = serializers.CharField(allow_null=True, allow_blank=True)
    item_count = serializers.IntegerField()
    payment_methods = serializers.ListField(child=serializers.CharField())
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class POSSyncStatusSerializer(serializers.Serializer):
    """Sync status response."""
    server_time = serializers.DateTimeField()
    total_products = serializers.IntegerField()
    total_customers = serializers.IntegerField()
