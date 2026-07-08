"""
Django Filters for Catalog API
Provides filtering capabilities for products
"""
import django_filters
from django.db.models import Q, F
from .models import Product, Category, Brand


class ProductFilter(django_filters.FilterSet):
    """
    Filter for Product queryset
    Supports filtering by category, brand, price range, stock status, rating, etc.
    """
    # Category filtering (by slug or ID)
    category = django_filters.CharFilter(method='filter_category')
    category_id = django_filters.NumberFilter(field_name='category__id')

    # Brand filtering (by slug or ID)
    brand = django_filters.CharFilter(field_name='brand__slug')
    brand_id = django_filters.NumberFilter(field_name='brand__id')

    # Price range filtering
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    price_range = django_filters.CharFilter(method='filter_price_range')

    # Stock status
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')
    low_stock = django_filters.BooleanFilter(method='filter_low_stock')

    # Product type
    product_type = django_filters.ChoiceFilter(
        field_name='product_type',
        choices=Product.PRODUCT_TYPES
    )

    # Featured products
    is_featured = django_filters.BooleanFilter(field_name='is_featured')

    # Digital products
    is_digital = django_filters.BooleanFilter(field_name='is_digital')

    # Discount filtering
    has_discount = django_filters.BooleanFilter(method='filter_has_discount')

    # Rating filtering
    min_rating = django_filters.NumberFilter(method='filter_min_rating')

    # Search query (name, description, SKU)
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Product
        fields = [
            'category',
            'category_id',
            'brand',
            'brand_id',
            'min_price',
            'max_price',
            'price_range',
            'in_stock',
            'low_stock',
            'product_type',
            'is_featured',
            'is_digital',
            'has_discount',
            'min_rating',
            'search'
        ]

    def filter_category(self, queryset, name, value):
        """
        Filter by category slug, including subcategories
        """
        try:
            category = Category.objects.get(slug=value, is_active=True)
            # Include products in this category and all subcategories
            return queryset.filter(
                Q(category=category) |
                Q(category__parent=category) |
                Q(category__parent__parent=category)  # Support 3 levels deep
            )
        except Category.DoesNotExist:
            return queryset.none()

    def filter_price_range(self, queryset, name, value):
        """
        Filter by predefined price ranges
        Format: "min-max" (e.g., "0-50", "50-100", "100-200", "200+")
        """
        if not value:
            return queryset

        if value.endswith('+'):
            # "200+" means 200 and above
            min_price = float(value.rstrip('+'))
            return queryset.filter(price__gte=min_price)

        if '-' in value:
            try:
                min_price, max_price = value.split('-')
                return queryset.filter(
                    price__gte=float(min_price),
                    price__lte=float(max_price)
                )
            except (ValueError, TypeError):
                return queryset

        return queryset

    def filter_in_stock(self, queryset, name, value):
        """
        Filter by stock status
        True = in stock, False = out of stock
        """
        if value:
            # In stock: either no inventory tracking OR has quantity > 0
            return queryset.filter(
                Q(track_inventory=False) |
                Q(track_inventory=True, quantity__gt=0)
            )
        else:
            # Out of stock: tracks inventory AND quantity = 0
            return queryset.filter(
                track_inventory=True,
                quantity=0
            )

    def filter_low_stock(self, queryset, name, value):
        """
        Filter by low stock status
        True = low stock (quantity <= low_stock_threshold)
        """
        if value:
            return queryset.filter(
                track_inventory=True,
                quantity__lte=Q(low_stock_threshold=0) | Q(quantity__lte=F('low_stock_threshold'))
            )
        return queryset

    def filter_has_discount(self, queryset, name, value):
        """
        Filter products with active discounts
        True = has discount (compare_at_price > price)
        """
        if value:
            return queryset.filter(compare_at_price__gt=F('price'))
        else:
            return queryset.filter(
                Q(compare_at_price__isnull=True) |
                Q(compare_at_price__lte=F('price'))
            )

    def filter_min_rating(self, queryset, name, value):
        """
        Filter by minimum average rating
        """
        from django.db.models import Avg
        try:
            min_rating = float(value)
            # Annotate with average rating and filter
            queryset = queryset.annotate(
                avg_rating=Avg('reviews__rating', filter=Q(reviews__is_approved=True))
            )
            return queryset.filter(avg_rating__gte=min_rating)
        except (ValueError, TypeError):
            return queryset

    def filter_search(self, queryset, name, value):
        """
        Search across multiple fields
        """
        if not value:
            return queryset

        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value) |
            Q(short_description__icontains=value) |
            Q(sku__icontains=value) |
            Q(brand__name__icontains=value) |
            Q(category__name__icontains=value)
        )
