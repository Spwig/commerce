"""
DRF serializers for search API endpoints.
"""

from rest_framework import serializers

from .models import (
    SearchEngine,
    SearchSettings,
)


class SearchSettingsSerializer(serializers.ModelSerializer):
    """Serializer for public search settings."""

    class Meta:
        model = SearchSettings
        fields = [
            "is_enabled",
            "min_query_length",
            "autocomplete_enabled",
            "autocomplete_max_results",
            "autocomplete_debounce_ms",
            "show_thumbnails",
            "search_products",
            "search_categories",
            "search_brands",
            "search_blog_posts",
            "fuzzy_enabled",
            "results_per_page",
            # Autocomplete Display - Products
            "autocomplete_product_thumbnail",
            "autocomplete_product_description",
            "autocomplete_product_price",
            "autocomplete_product_sku",
            "autocomplete_product_stock_status",
            # Autocomplete Display - Blog Posts
            "autocomplete_blog_thumbnail",
            "autocomplete_blog_excerpt",
            "autocomplete_blog_excerpt_length",
            # Autocomplete Display - Categories
            "autocomplete_category_thumbnail",
            "autocomplete_category_product_count",
            # Autocomplete Display - Brands
            "autocomplete_brand_logo",
            "autocomplete_brand_product_count",
        ]


class SearchEngineSerializer(serializers.ModelSerializer):
    """Serializer for search engines."""

    class Meta:
        model = SearchEngine
        fields = [
            "id",
            "name",
            "slug",
            "is_active",
            "content_types",
        ]


class ProductResultSerializer(serializers.Serializer):
    """Serializer for product search results."""

    id = serializers.IntegerField()
    type = serializers.CharField(default="product")
    name = serializers.CharField()
    name_base = serializers.CharField(allow_null=True)
    slug = serializers.CharField()
    url = serializers.CharField()
    price = serializers.CharField()
    currency = serializers.CharField()
    thumbnail = serializers.CharField(allow_null=True)
    sku = serializers.CharField(allow_null=True)
    in_stock = serializers.BooleanField()
    is_translated = serializers.BooleanField()
    description = serializers.CharField(allow_blank=True)


class CategoryResultSerializer(serializers.Serializer):
    """Serializer for category search results."""

    id = serializers.IntegerField()
    type = serializers.CharField(default="category")
    name = serializers.CharField()
    name_base = serializers.CharField(allow_null=True)
    slug = serializers.CharField()
    url = serializers.CharField()
    thumbnail = serializers.CharField(allow_null=True)
    product_count = serializers.IntegerField()
    is_translated = serializers.BooleanField()


class BrandResultSerializer(serializers.Serializer):
    """Serializer for brand search results."""

    id = serializers.IntegerField()
    type = serializers.CharField(default="brand")
    name = serializers.CharField()
    slug = serializers.CharField()
    url = serializers.CharField()
    logo = serializers.CharField(allow_null=True)
    product_count = serializers.IntegerField()


class BlogPostResultSerializer(serializers.Serializer):
    """Serializer for blog post search results."""

    id = serializers.IntegerField()
    type = serializers.CharField(default="blog_post")
    title = serializers.CharField()
    title_base = serializers.CharField(allow_null=True)
    slug = serializers.CharField()
    url = serializers.CharField()
    thumbnail = serializers.CharField(allow_null=True)
    excerpt = serializers.CharField(allow_blank=True)
    is_translated = serializers.BooleanField()


class RedirectSerializer(serializers.Serializer):
    """Serializer for redirect info."""

    url = serializers.CharField()
    type = serializers.CharField()
    matched_term = serializers.CharField()


class AutocompleteResponseSerializer(serializers.Serializer):
    """Serializer for autocomplete API response."""

    query = serializers.CharField()
    language = serializers.CharField()
    did_you_mean = serializers.CharField(allow_null=True)
    redirect = RedirectSerializer(allow_null=True)
    products = ProductResultSerializer(many=True)
    categories = CategoryResultSerializer(many=True)
    brands = BrandResultSerializer(many=True)
    blog_posts = BlogPostResultSerializer(many=True)
    total_count = serializers.IntegerField()
    response_time_ms = serializers.IntegerField()


class FacetsSerializer(serializers.Serializer):
    """Serializer for search facets."""

    types = serializers.DictField(child=serializers.IntegerField())
    categories = serializers.ListField(child=serializers.DictField())
    brands = serializers.ListField(child=serializers.DictField())
    price_range = serializers.DictField()
    in_stock = serializers.DictField(child=serializers.IntegerField())


class SearchResultItemSerializer(serializers.Serializer):
    """Generic serializer for any search result item."""

    id = serializers.IntegerField()
    type = serializers.CharField()
    name = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    name_base = serializers.CharField(allow_null=True, required=False)
    title_base = serializers.CharField(allow_null=True, required=False)
    slug = serializers.CharField()
    url = serializers.CharField()
    price = serializers.CharField(required=False)
    currency = serializers.CharField(required=False)
    thumbnail = serializers.CharField(allow_null=True, required=False)
    logo = serializers.CharField(allow_null=True, required=False)
    sku = serializers.CharField(allow_null=True, required=False)
    in_stock = serializers.BooleanField(required=False)
    is_translated = serializers.BooleanField(required=False)
    description = serializers.CharField(allow_blank=True, required=False)
    excerpt = serializers.CharField(allow_blank=True, required=False)
    product_count = serializers.IntegerField(required=False)


class SearchResultsResponseSerializer(serializers.Serializer):
    """Serializer for full search results API response."""

    query = serializers.CharField()
    language = serializers.CharField()
    did_you_mean = serializers.CharField(allow_null=True)
    redirect = RedirectSerializer(allow_null=True)
    results = SearchResultItemSerializer(many=True)
    total_count = serializers.IntegerField()
    page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    facets = FacetsSerializer()
    applied_synonyms = serializers.ListField(child=serializers.CharField())
    response_time_ms = serializers.IntegerField()
    # ID of the SearchQuery row created for this request. Pass this to
    # POST /api/search/click/ so clicks can be attributed to the originating
    # search. Absent on redirect responses or when tracking is disabled.
    search_query_id = serializers.IntegerField(required=False, allow_null=True)


class TrendingQuerySerializer(serializers.Serializer):
    """Serializer for trending query items."""

    query = serializers.CharField()
    count = serializers.IntegerField()
    avg_results = serializers.FloatField()
    trend = serializers.CharField()


class TrendingResponseSerializer(serializers.Serializer):
    """Serializer for trending queries API response."""

    queries = TrendingQuerySerializer(many=True)
    period_days = serializers.IntegerField()


class TrackClickRequestSerializer(serializers.Serializer):
    """Serializer for click tracking request."""

    search_query_id = serializers.IntegerField()
    content_type = serializers.CharField()
    object_id = serializers.IntegerField()
    position = serializers.IntegerField(default=0)


class SuggestCorrectionsResponseSerializer(serializers.Serializer):
    """Serializer for spelling correction suggestions."""

    query = serializers.CharField()
    suggestion = serializers.CharField(allow_null=True)
    confidence = serializers.FloatField(allow_null=True)
