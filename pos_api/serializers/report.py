from rest_framework import serializers


class POSPaymentBreakdownSerializer(serializers.Serializer):
    """Payment method breakdown in a report."""

    method = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    count = serializers.IntegerField()


class POSDailyReportSerializer(serializers.Serializer):
    """Daily sales report."""

    date = serializers.DateField()
    total_sales = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_refunds = serializers.DecimalField(max_digits=10, decimal_places=2)
    net_sales = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_transactions = serializers.IntegerField()
    average_transaction = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_breakdown = POSPaymentBreakdownSerializer(many=True)
    currency = serializers.CharField()


class POSTopProductSerializer(serializers.Serializer):
    """Top selling product in a report."""

    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    sku = serializers.CharField(allow_blank=True)
    total_quantity = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField()
