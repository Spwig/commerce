"""
Inventory Intelligence Serializers for Admin API

Serializers for inventory dashboard, velocity, movements, reorder
suggestions, and inventory settings endpoints.
"""

from rest_framework import serializers

# ──────────────────────────────────────────────
# Dashboard
# ──────────────────────────────────────────────


class VelocityProductSerializer(serializers.Serializer):
    """Top velocity product in dashboard."""

    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    sku = serializers.CharField()
    units_sold_30d = serializers.IntegerField()
    daily_average = serializers.DecimalField(max_digits=10, decimal_places=2)


class RecentStockoutSerializer(serializers.Serializer):
    """Recent stockout entry in dashboard."""

    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    sku = serializers.CharField()
    stockout_date = serializers.DateTimeField()


class InventoryDashboardSerializer(serializers.Serializer):
    """Complete inventory dashboard response."""

    total_products = serializers.IntegerField()
    total_variants = serializers.IntegerField()
    total_stock_value = serializers.DecimalField(max_digits=14, decimal_places=2)
    currency = serializers.CharField()
    in_stock_count = serializers.IntegerField()
    low_stock_count = serializers.IntegerField()
    out_of_stock_count = serializers.IntegerField()
    overstock_count = serializers.IntegerField()
    stockouts_last_30_days = serializers.IntegerField()
    top_velocity_products = VelocityProductSerializer(many=True)
    recent_stockouts = RecentStockoutSerializer(many=True)


# ──────────────────────────────────────────────
# Low Stock Products
# ──────────────────────────────────────────────


class StockItemBreakdownSerializer(serializers.Serializer):
    """Per-warehouse stock breakdown."""

    warehouse_id = serializers.IntegerField()
    warehouse_name = serializers.CharField()
    on_hand = serializers.IntegerField()
    allocated = serializers.IntegerField()


class LowStockProductDetailSerializer(serializers.Serializer):
    """Enhanced low stock product with velocity and restock data."""

    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    sku = serializers.CharField()
    image_url = serializers.CharField(allow_null=True)
    category_name = serializers.CharField(allow_null=True)
    available_stock = serializers.IntegerField()
    low_stock_threshold = serializers.IntegerField()
    severity = serializers.ChoiceField(choices=["critical", "warning"])
    velocity_7d = serializers.DecimalField(max_digits=10, decimal_places=2)
    velocity_30d = serializers.DecimalField(max_digits=10, decimal_places=2)
    days_of_supply_remaining = serializers.DecimalField(
        max_digits=10, decimal_places=1, allow_null=True
    )
    last_restock_date = serializers.DateTimeField(allow_null=True)
    last_restock_quantity = serializers.IntegerField(allow_null=True)
    stock_items = StockItemBreakdownSerializer(many=True)


class PaginationSerializer(serializers.Serializer):
    """Pagination metadata."""

    page = serializers.IntegerField()
    page_size = serializers.IntegerField()
    total_count = serializers.IntegerField()
    total_pages = serializers.IntegerField()


class LowStockProductListSerializer(serializers.Serializer):
    """Low stock products list response with pagination."""

    products = LowStockProductDetailSerializer(many=True)
    pagination = PaginationSerializer()


# ──────────────────────────────────────────────
# Velocity
# ──────────────────────────────────────────────


class VelocityAveragesSerializer(serializers.Serializer):
    """Velocity averages for different time windows."""

    daily_average_7d = serializers.DecimalField(max_digits=10, decimal_places=2)
    daily_average_30d = serializers.DecimalField(max_digits=10, decimal_places=2)
    daily_average_90d = serializers.DecimalField(max_digits=10, decimal_places=2)


class DailySalesPointSerializer(serializers.Serializer):
    """Single day data point for velocity chart."""

    date = serializers.DateField()
    units_sold = serializers.IntegerField()
    stock_level = serializers.IntegerField()


class VelocityResponseSerializer(serializers.Serializer):
    """Stock velocity response for a product."""

    product_id = serializers.IntegerField()
    variant_id = serializers.IntegerField(allow_null=True)
    current_stock = serializers.IntegerField()
    low_stock_threshold = serializers.IntegerField()
    velocity = VelocityAveragesSerializer()
    trend = serializers.ChoiceField(choices=["increasing", "decreasing", "stable"])
    trend_percentage = serializers.FloatField()
    days_of_supply_remaining = serializers.DecimalField(
        max_digits=10, decimal_places=1, allow_null=True
    )
    projected_stockout_date = serializers.DateField(allow_null=True)
    daily_sales = DailySalesPointSerializer(many=True)


# ──────────────────────────────────────────────
# Stock Movements
# ──────────────────────────────────────────────


class StockMovementSerializer(serializers.Serializer):
    """Stock movement entry."""

    id = serializers.IntegerField()
    movement_type = serializers.CharField()
    movement_type_display = serializers.CharField()
    quantity = serializers.IntegerField()
    previous_quantity = serializers.IntegerField()
    new_quantity = serializers.IntegerField()
    reason = serializers.CharField(allow_blank=True)
    warehouse_id = serializers.IntegerField()
    warehouse_name = serializers.CharField()
    variant_id = serializers.IntegerField(allow_null=True)
    variant_sku = serializers.CharField(allow_null=True)
    order_number = serializers.CharField(allow_null=True)
    user_name = serializers.CharField(allow_null=True)
    created_at = serializers.DateTimeField()


class StockMovementListSerializer(serializers.Serializer):
    """Stock movements list response with pagination."""

    movements = StockMovementSerializer(many=True)
    pagination = PaginationSerializer()


# ──────────────────────────────────────────────
# Reorder Suggestions
# ──────────────────────────────────────────────


class ReorderSuggestionSerializer(serializers.Serializer):
    """Single reorder suggestion."""

    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    sku = serializers.CharField()
    image_url = serializers.CharField(allow_null=True)
    category_name = serializers.CharField(allow_null=True)
    current_stock = serializers.IntegerField()
    velocity_30d = serializers.DecimalField(max_digits=10, decimal_places=2)
    days_of_supply_remaining = serializers.DecimalField(max_digits=10, decimal_places=1)
    projected_stockout_date = serializers.DateField()
    suggested_reorder_quantity = serializers.IntegerField()
    urgency = serializers.ChoiceField(choices=["immediate", "soon", "upcoming"])


class ReorderSettingsSerializer(serializers.Serializer):
    """Reorder calculation settings included in response."""

    lead_days = serializers.IntegerField()
    safety_multiplier = serializers.FloatField()


class ReorderSuggestionListSerializer(serializers.Serializer):
    """Reorder suggestions list response with pagination."""

    suggestions = ReorderSuggestionSerializer(many=True)
    settings = ReorderSettingsSerializer()
    pagination = PaginationSerializer()


# ──────────────────────────────────────────────
# Inventory Settings
# ──────────────────────────────────────────────


class InventorySettingsSerializer(serializers.Serializer):
    """Inventory settings from SiteSettings."""

    default_low_stock_threshold = serializers.IntegerField(
        min_value=0, help_text="Default threshold for low stock alerts"
    )
    low_stock_alerts_enabled = serializers.BooleanField(
        help_text="Whether low stock alert notifications are enabled"
    )
    low_stock_alert_frequency = serializers.ChoiceField(
        choices=["realtime", "daily", "weekly"], help_text="How often low stock alerts are sent"
    )
    track_inventory_by_default = serializers.BooleanField(
        help_text="Default value for new products' track_inventory field"
    )
    allow_backorders_by_default = serializers.BooleanField(
        help_text="Default value for new products' allow_backorders field"
    )
    default_reorder_lead_days = serializers.IntegerField(
        min_value=1, help_text="Default supplier lead time in days for reorder calculations"
    )
    safety_stock_multiplier = serializers.FloatField(
        min_value=0.1, help_text="Safety stock multiplier for reorder quantity formula"
    )
    velocity_calculation_window_days = serializers.IntegerField(
        min_value=7, help_text="Number of days used for velocity calculations"
    )


class InventorySettingsUpdateSerializer(serializers.Serializer):
    """Partial update serializer for inventory settings (all fields optional)."""

    default_low_stock_threshold = serializers.IntegerField(min_value=0, required=False)
    low_stock_alerts_enabled = serializers.BooleanField(required=False)
    low_stock_alert_frequency = serializers.ChoiceField(
        choices=["realtime", "daily", "weekly"], required=False
    )
    track_inventory_by_default = serializers.BooleanField(required=False)
    allow_backorders_by_default = serializers.BooleanField(required=False)
    default_reorder_lead_days = serializers.IntegerField(min_value=1, required=False)
    safety_stock_multiplier = serializers.FloatField(min_value=0.1, required=False)
    velocity_calculation_window_days = serializers.IntegerField(min_value=7, required=False)
