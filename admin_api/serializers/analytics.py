"""
Analytics Serializers for Admin API

Serializers for dashboard analytics and KPI data.
"""
from rest_framework import serializers


class SalesKPISerializer(serializers.Serializer):
    """Sales KPI data for a specific period."""
    total_sales = serializers.DecimalField(max_digits=12, decimal_places=2)
    currency = serializers.CharField()
    order_count = serializers.IntegerField()
    average_order_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    period = serializers.CharField()  # 'today', '7_days', '30_days'


class TopProductSerializer(serializers.Serializer):
    """Top selling product data."""
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    sku = serializers.CharField()
    units_sold = serializers.IntegerField()
    revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    currency = serializers.CharField()


class OrderStatusBreakdownSerializer(serializers.Serializer):
    """Order status breakdown."""
    status = serializers.CharField()
    status_display = serializers.CharField()
    count = serializers.IntegerField()


class DashboardAnalyticsSerializer(serializers.Serializer):
    """Complete dashboard analytics response."""
    today = SalesKPISerializer()
    last_7_days = SalesKPISerializer()
    last_30_days = SalesKPISerializer()
    top_products_today = TopProductSerializer(many=True)
    top_products_7_days = TopProductSerializer(many=True)
    order_status_breakdown = OrderStatusBreakdownSerializer(many=True)
    pending_orders_count = serializers.IntegerField()
    low_stock_count = serializers.IntegerField()


class QuickStatsSerializer(serializers.Serializer):
    """Quick stats for dashboard header."""
    today_sales = serializers.DecimalField(max_digits=12, decimal_places=2)
    today_orders = serializers.IntegerField()
    pending_orders = serializers.IntegerField()
    low_stock_items = serializers.IntegerField()
    currency = serializers.CharField()


class SalesComparisonSerializer(serializers.Serializer):
    """Sales comparison with previous period."""
    current_value = serializers.DecimalField(max_digits=12, decimal_places=2)
    previous_value = serializers.DecimalField(max_digits=12, decimal_places=2)
    change_percentage = serializers.DecimalField(max_digits=6, decimal_places=2, allow_null=True)
    trend = serializers.ChoiceField(choices=['up', 'down', 'stable'])
    currency = serializers.CharField()


class DailyStatsItemSerializer(serializers.Serializer):
    """Single day data point for chart display."""
    date = serializers.DateField()
    revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    order_count = serializers.IntegerField()
    average_order_value = serializers.DecimalField(max_digits=10, decimal_places=2)


class DailyStatsSerializer(serializers.Serializer):
    """Daily breakdown response for dashboard charts."""
    period = serializers.CharField()
    currency = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    days = DailyStatsItemSerializer(many=True)


class HourlySalesItemSerializer(serializers.Serializer):
    """Single hour data point."""
    hour = serializers.IntegerField()
    revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    order_count = serializers.IntegerField()


class HourlySalesSerializer(serializers.Serializer):
    """Hourly sales breakdown for a single date."""
    date = serializers.DateField()
    currency = serializers.CharField()
    hours = HourlySalesItemSerializer(many=True)
