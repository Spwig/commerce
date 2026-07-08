"""
Serializers for Customer-Facing APIs
"""
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import CustomerMetrics, CustomerSegment


class CustomerDashboardSerializer(serializers.Serializer):
    """Serializer for customer dashboard summary"""
    # Customer Info
    name = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    member_since = serializers.DateTimeField(read_only=True)

    # Quick Stats
    total_orders = serializers.IntegerField(read_only=True)
    total_spent = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_saved = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    loyalty_points = serializers.IntegerField(read_only=True)

    # Loyalty Status
    segment = serializers.CharField(read_only=True)
    segment_display = serializers.CharField(read_only=True)

    # Recent Activity
    recent_orders = serializers.ListField(read_only=True)
    recently_viewed = serializers.ListField(read_only=True)

    # Recommendations
    recommended_products = serializers.ListField(read_only=True)

    # Alerts
    abandoned_carts = serializers.IntegerField(read_only=True)
    items_back_in_stock = serializers.IntegerField(read_only=True)
    items_on_sale = serializers.IntegerField(read_only=True)


class CustomerStatsSerializer(serializers.Serializer):
    """Serializer for detailed customer statistics"""
    # Order Statistics
    total_orders = serializers.IntegerField(read_only=True)
    completed_orders = serializers.IntegerField(read_only=True)
    cancelled_orders = serializers.IntegerField(read_only=True)
    average_order_value = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    # Purchase Behavior
    total_items_purchased = serializers.IntegerField(read_only=True)
    unique_products_purchased = serializers.IntegerField(read_only=True)
    average_items_per_order = serializers.FloatField(read_only=True)

    # Frequency
    days_since_first_order = serializers.IntegerField(read_only=True)
    days_since_last_order = serializers.IntegerField(read_only=True)
    average_days_between_orders = serializers.FloatField(read_only=True)
    purchase_frequency_category = serializers.CharField(read_only=True)

    # Return Behavior
    total_returns = serializers.IntegerField(read_only=True)
    return_rate = serializers.FloatField(read_only=True)

    # Engagement
    wishlist_items = serializers.IntegerField(read_only=True)
    reviews_written = serializers.IntegerField(read_only=True)
    products_viewed = serializers.IntegerField(read_only=True)


class CustomerInsightsSerializer(serializers.Serializer):
    """Serializer for customer spending insights and trends"""
    # Spending Overview
    total_lifetime_spent = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    average_monthly_spend = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    highest_month_spend = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    lowest_month_spend = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    # Spending Trends (last 12 months)
    monthly_spending = serializers.ListField(read_only=True)
    spending_trend = serializers.CharField(read_only=True)  # 'increasing', 'decreasing', 'stable'

    # Category Breakdown
    top_categories = serializers.ListField(read_only=True)
    category_spending = serializers.DictField(read_only=True)

    # Brand Preferences
    top_brands = serializers.ListField(read_only=True)
    brand_loyalty_score = serializers.FloatField(read_only=True)

    # Shopping Patterns
    peak_shopping_day = serializers.CharField(read_only=True)
    peak_shopping_hour = serializers.IntegerField(read_only=True)
    average_cart_size = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    # Discount Usage
    orders_with_discounts = serializers.IntegerField(read_only=True)
    discount_usage_rate = serializers.FloatField(read_only=True)
    favorite_discount_type = serializers.CharField(read_only=True)


class CustomerRecommendationSerializer(serializers.Serializer):
    """Serializer for product recommendations"""
    product_id = serializers.IntegerField(read_only=True)
    product_name = serializers.CharField(read_only=True)
    product_slug = serializers.CharField(read_only=True)
    product_image = serializers.CharField(read_only=True, allow_null=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    discount_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, allow_null=True)
    reason = serializers.CharField(read_only=True)  # 'frequently_bought', 'similar_to_purchased', 'trending', etc.
    confidence_score = serializers.FloatField(read_only=True)


class CustomerRecommendationsSerializer(serializers.Serializer):
    """Serializer for all customer recommendations"""
    based_on_history = serializers.ListField(
        child=CustomerRecommendationSerializer(),
        read_only=True
    )
    trending_in_categories = serializers.ListField(
        child=CustomerRecommendationSerializer(),
        read_only=True
    )
    back_in_stock = serializers.ListField(
        child=CustomerRecommendationSerializer(),
        read_only=True
    )
    on_sale = serializers.ListField(
        child=CustomerRecommendationSerializer(),
        read_only=True
    )


class CustomerLifetimeValueSerializer(serializers.Serializer):
    """Serializer for customer lifetime value metrics"""
    # Current Value
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_orders = serializers.IntegerField(read_only=True)
    average_order_value = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    # Projected Value
    predicted_ltv = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    confidence_level = serializers.CharField(read_only=True)  # 'high', 'medium', 'low'

    # Value Tier
    value_tier = serializers.CharField(read_only=True)  # 'platinum', 'gold', 'silver', 'bronze'
    percentile = serializers.IntegerField(read_only=True)  # Top X% of customers

    # Engagement Score
    engagement_score = serializers.FloatField(read_only=True)
    churn_risk = serializers.CharField(read_only=True)  # 'low', 'medium', 'high'

    # Timeline
    customer_since = serializers.DateField(read_only=True)
    months_active = serializers.IntegerField(read_only=True)
    last_purchase_date = serializers.DateField(read_only=True)
    days_since_last_purchase = serializers.IntegerField(read_only=True)


class CustomerLoyaltyStatusSerializer(serializers.Serializer):
    """Serializer for customer loyalty status and benefits"""
    # Current Status
    segment = serializers.CharField(read_only=True)
    segment_display = serializers.CharField(read_only=True)
    segment_color = serializers.CharField(read_only=True)
    tier = serializers.CharField(read_only=True)  # 'VIP', 'Gold', 'Silver', 'Bronze'

    # Points & Rewards
    loyalty_points = serializers.IntegerField(read_only=True)
    points_to_next_tier = serializers.IntegerField(read_only=True, allow_null=True)

    # Benefits
    current_benefits = serializers.ListField(read_only=True)
    next_tier_benefits = serializers.ListField(read_only=True, allow_null=True)

    # Progress
    progress_percentage = serializers.FloatField(read_only=True)
    next_milestone = serializers.CharField(read_only=True, allow_null=True)

    # Statistics
    total_spent = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    orders_count = serializers.IntegerField(read_only=True)
    member_since = serializers.DateField(read_only=True)


class CustomerSavingsSerializer(serializers.Serializer):
    """Serializer for customer savings history"""
    # Total Savings
    total_saved = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_orders_with_savings = serializers.IntegerField(read_only=True)
    average_savings_per_order = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    # Savings Breakdown
    voucher_savings = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    sale_savings = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    loyalty_savings = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    # Recent Savings
    recent_savings = serializers.ListField(read_only=True)

    # Trends
    monthly_savings = serializers.ListField(read_only=True)
    best_savings_month = serializers.DictField(read_only=True)


class CustomerFavoriteProductSerializer(serializers.Serializer):
    """Serializer for favorite product data"""
    product_id = serializers.IntegerField(read_only=True)
    product_name = serializers.CharField(read_only=True)
    product_slug = serializers.CharField(read_only=True)
    product_image = serializers.CharField(read_only=True, allow_null=True)
    times_purchased = serializers.IntegerField(read_only=True)
    total_spent = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    last_purchased = serializers.DateField(read_only=True)
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    is_on_sale = serializers.BooleanField(read_only=True)


class CustomerFavoritesSerializer(serializers.Serializer):
    """Serializer for customer favorites"""
    # Most Purchased Products
    most_purchased = serializers.ListField(
        child=CustomerFavoriteProductSerializer(),
        read_only=True
    )

    # Favorite Categories
    favorite_categories = serializers.ListField(read_only=True)

    # Favorite Brands
    favorite_brands = serializers.ListField(read_only=True)

    # Recently Purchased
    recently_purchased = serializers.ListField(
        child=CustomerFavoriteProductSerializer(),
        read_only=True
    )

    # Wishlist Summary
    wishlist_count = serializers.IntegerField(read_only=True)
    wishlist_value = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)


class CustomerMetricsSerializer(serializers.ModelSerializer):
    """Serializer for CustomerMetrics model (admin/internal use)"""

    class Meta:
        model = CustomerMetrics
        fields = [
            'user', 'total_orders', 'completed_orders', 'cancelled_orders',
            'total_spent', 'average_order_value', 'lifetime_value',
            'total_items_purchased', 'unique_products_purchased',
            'first_order_date', 'last_order_date', 'days_since_last_order',
            'average_days_between_orders', 'total_saved', 'favorite_categories',
            'favorite_brands', 'wishlist_items_count', 'cart_abandonment_rate',
            'return_rate', 'review_count', 'last_calculated'
        ]
        read_only_fields = ['user', 'last_calculated']


class CustomerSegmentSerializer(serializers.ModelSerializer):
    """Serializer for CustomerSegment model"""
    segment_type_display = serializers.CharField(source='get_segment_type_display', read_only=True)

    class Meta:
        model = CustomerSegment
        fields = [
            'id', 'name', 'segment_type', 'segment_type_display',
            'description', 'color', 'icon', 'is_active',
            'min_orders', 'min_total_spent', 'min_lifetime_value',
            'max_days_since_order', 'priority', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


# ============================================================================
# Digital Products Serializers
# ============================================================================

class DigitalAssetSerializer(serializers.Serializer):
    """Serializer for customer digital assets"""
    id = serializers.IntegerField(read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    filename = serializers.CharField(read_only=True)
    file_size = serializers.CharField(source='get_file_size_display', read_only=True)
    file_type = serializers.CharField(read_only=True)
    version = serializers.CharField(read_only=True)
    changelog = serializers.CharField(read_only=True)

    # Access control
    download_limit = serializers.IntegerField(read_only=True)
    expiration_days = serializers.IntegerField(read_only=True)
    requires_license = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    # Metadata
    created_at = serializers.DateTimeField(read_only=True)


class DigitalDownloadSerializer(serializers.Serializer):
    """Serializer for download history"""
    id = serializers.IntegerField(read_only=True)
    asset_filename = serializers.CharField(source='digital_asset.filename', read_only=True)
    product_name = serializers.CharField(source='digital_asset.product.name', read_only=True)
    file_version = serializers.CharField(read_only=True)
    downloaded_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)
    download_duration_seconds = serializers.IntegerField(read_only=True)


class LicenseKeySerializer(serializers.Serializer):
    """Serializer for software license keys"""
    id = serializers.IntegerField(read_only=True)
    product_name = serializers.CharField(source='digital_asset.product.name', read_only=True)
    product_version = serializers.CharField(source='digital_asset.version', read_only=True)
    key = serializers.CharField(read_only=True)
    key_type = serializers.CharField(read_only=True)

    # Activation limits
    max_activations = serializers.IntegerField(read_only=True)
    current_activations = serializers.IntegerField(read_only=True)
    activations_remaining = serializers.IntegerField(read_only=True)

    # Status
    status = serializers.CharField(read_only=True)
    is_valid = serializers.BooleanField(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    is_lifetime = serializers.BooleanField(read_only=True)
    expires_at = serializers.DateTimeField(read_only=True)

    # Metadata
    issued_at = serializers.DateTimeField(read_only=True)
    first_activated_at = serializers.DateTimeField(read_only=True)
    last_activated_at = serializers.DateTimeField(read_only=True)


class LicenseActivationSerializer(serializers.Serializer):
    """Serializer for license activations"""
    id = serializers.IntegerField(read_only=True)
    device_identifier = serializers.CharField(read_only=True)
    device_name = serializers.CharField(read_only=True)
    device_info = serializers.JSONField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    activated_at = serializers.DateTimeField(read_only=True)
    deactivated_at = serializers.DateTimeField(read_only=True)
    last_seen_at = serializers.DateTimeField(read_only=True)
    ip_address = serializers.IPAddressField(read_only=True)
    location = serializers.CharField(read_only=True)


class CustomerDigitalProductSerializer(serializers.Serializer):
    """Serializer for customer's purchased digital product"""
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    order_date = serializers.DateTimeField(source='order.created_at', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)

    # Digital assets for this purchase
    digital_assets = DigitalAssetSerializer(many=True, read_only=True)

    # License keys for this purchase
    license_keys = LicenseKeySerializer(many=True, read_only=True)

    # Download history
    digital_downloads = DigitalDownloadSerializer(many=True, read_only=True)


class DownloadLinkSerializer(serializers.Serializer):
    """Serializer for download link response"""
    download_url = serializers.URLField(read_only=True)
    expires_in_seconds = serializers.IntegerField(read_only=True)
    filename = serializers.CharField(read_only=True)
    file_size = serializers.CharField(read_only=True)
    downloads_remaining = serializers.IntegerField(read_only=True)


class LicenseActivationRequestSerializer(serializers.Serializer):
    """Serializer for license activation requests"""
    device_identifier = serializers.CharField(required=True, max_length=255)
    device_name = serializers.CharField(required=False, allow_blank=True, max_length=255)
    device_info = serializers.JSONField(required=False, default=dict)
