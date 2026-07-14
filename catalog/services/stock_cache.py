"""
Stock Cache Service

Provides caching for frequently accessed stock queries to improve performance.
Uses Django's cache framework with automatic cache invalidation on stock changes.
"""

import logging

from django.core.cache import cache
from django.db.models import Sum
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


class StockCache:
    """
    Cache manager for product stock data.

    Caches product stock totals to reduce database queries.
    Automatically invalidates cache when stock changes.
    """

    # Cache TTL (Time To Live) - 5 minutes
    CACHE_TTL = 300

    @staticmethod
    def _get_cache_key(product_id, region_id=None, warehouse_id=None):
        """
        Generate cache key for stock data.

        Args:
            product_id: Product ID
            region_id: Optional SalesRegion ID for regional stock
            warehouse_id: Optional Warehouse ID for warehouse-specific stock

        Returns:
            str: Cache key
        """
        if warehouse_id:
            return f"stock:product:{product_id}:warehouse:{warehouse_id}"
        elif region_id:
            return f"stock:product:{product_id}:region:{region_id}"
        else:
            return f"stock:product:{product_id}:total"

    @staticmethod
    def get_product_stock(product, region=None, warehouse=None):
        """
        Get cached stock for a product.

        Args:
            product: Product instance
            region: Optional SalesRegion instance
            warehouse: Optional Warehouse instance

        Returns:
            dict: Stock data with 'on_hand', 'allocated', 'available' keys
        """
        cache_key = StockCache._get_cache_key(
            product.id, region.id if region else None, warehouse.id if warehouse else None
        )

        # Try to get from cache
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            logger.debug(f"Cache hit for {cache_key}")
            return cached_data

        # Calculate and cache
        logger.debug(f"Cache miss for {cache_key}, calculating...")
        stock_data = StockCache._calculate_stock(product, region, warehouse)

        # Store in cache
        cache.set(cache_key, stock_data, StockCache.CACHE_TTL)

        return stock_data

    @staticmethod
    def _calculate_stock(product, region=None, warehouse=None):
        """
        Calculate stock totals for a product.

        Args:
            product: Product instance
            region: Optional SalesRegion instance
            warehouse: Optional Warehouse instance

        Returns:
            dict: Stock data
        """
        from catalog.models import StockItem  # Import here to avoid circular imports

        # Build queryset
        queryset = StockItem.objects.filter(product=product)

        if warehouse:
            queryset = queryset.filter(warehouse=warehouse)
        elif region:
            queryset = queryset.filter(warehouse__region=region, warehouse__is_active=True)

        # Aggregate stock
        aggregated = queryset.aggregate(
            total_on_hand=Sum("on_hand"), total_allocated=Sum("allocated")
        )

        on_hand = aggregated["total_on_hand"] or 0
        allocated = aggregated["total_allocated"] or 0
        available = on_hand - allocated

        return {"on_hand": on_hand, "allocated": allocated, "available": available}

    @staticmethod
    def invalidate_product_cache(product_id):
        """
        Invalidate all cached stock data for a product.

        Called automatically when stock changes via signals.

        Args:
            product_id: Product ID
        """
        from catalog.models import StockItem

        logger.info(f"Invalidating stock cache for product {product_id}")

        # Invalidate total stock cache
        cache.delete(StockCache._get_cache_key(product_id))

        # Invalidate regional caches
        try:
            stock_items = StockItem.objects.filter(product_id=product_id).select_related(
                "warehouse"
            )

            # Get unique regions
            regions = set()
            warehouses = set()

            for item in stock_items:
                if item.warehouse:
                    warehouses.add(item.warehouse.id)
                    if item.warehouse.region:
                        regions.add(item.warehouse.region.id)

            # Invalidate each region cache
            for region_id in regions:
                cache.delete(StockCache._get_cache_key(product_id, region_id=region_id))

            # Invalidate each warehouse cache
            for warehouse_id in warehouses:
                cache.delete(StockCache._get_cache_key(product_id, warehouse_id=warehouse_id))

        except Exception as e:
            logger.error(f"Error invalidating product cache: {e}")

    @staticmethod
    def warm_cache_for_products(product_ids, region=None):
        """
        Pre-populate cache for multiple products.

        Useful for product listing pages to avoid N+1 queries.

        Args:
            product_ids: List of product IDs
            region: Optional SalesRegion instance

        Returns:
            dict: Mapping of product_id -> stock_data
        """
        from catalog.models import Product

        logger.info(f"Warming stock cache for {len(product_ids)} products")

        result = {}

        # Fetch products in batch
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            stock_data = StockCache.get_product_stock(product, region=region)
            result[product.id] = stock_data

        return result


# Signal handlers for automatic cache invalidation


@receiver(post_save, sender="catalog.StockItem")
def invalidate_on_stock_change(sender, instance, **kwargs):
    """Invalidate cache when StockItem is created or updated"""
    StockCache.invalidate_product_cache(instance.product_id)


@receiver(post_delete, sender="catalog.StockItem")
def invalidate_on_stock_delete(sender, instance, **kwargs):
    """Invalidate cache when StockItem is deleted"""
    StockCache.invalidate_product_cache(instance.product_id)


@receiver(post_save, sender="catalog.StockMovement")
def invalidate_on_stock_movement(sender, instance, **kwargs):
    """Invalidate cache when stock movement is recorded"""
    if instance.stock_item:
        StockCache.invalidate_product_cache(instance.stock_item.product_id)
