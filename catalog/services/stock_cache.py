"""
Stock Cache Service

Provides caching for frequently accessed stock queries to improve performance.
Uses Django's cache framework with automatic cache invalidation on stock changes.
"""

import logging

from django.core.cache import cache
from django.db import transaction
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

        return StockCache._build_stock_data(
            aggregated["total_on_hand"], aggregated["total_allocated"]
        )

    @staticmethod
    def _build_stock_data(on_hand, allocated):
        """
        Build a stock-data dict, clamping available to zero.

        Mirrors StockItem.available so cached values never go negative when
        allocations exceed on-hand quantity.
        """
        on_hand = on_hand or 0
        allocated = allocated or 0
        return {
            "on_hand": on_hand,
            "allocated": allocated,
            "available": max(0, on_hand - allocated),
        }

    @staticmethod
    def invalidate_product_cache(product_id, extra_warehouse_ids=None, extra_region_ids=None):
        """
        Invalidate all cached stock data for a product.

        Called automatically when stock changes via signals.

        Args:
            product_id: Product ID
            extra_warehouse_ids: Warehouse IDs to invalidate even if no surviving
                StockItem references them (e.g. the warehouse of a just-deleted item).
            extra_region_ids: Region IDs to invalidate even if no surviving StockItem
                references them.
        """
        from catalog.models import StockItem

        logger.info(f"Invalidating stock cache for product {product_id}")

        # Invalidate total stock cache
        cache.delete(StockCache._get_cache_key(product_id))

        # Seed with explicitly forwarded IDs so keys for a deleted item's last
        # warehouse/region are cleared even though they're no longer discoverable.
        warehouses = set(extra_warehouse_ids or ())
        regions = set(extra_region_ids or ())

        # Discover warehouses/regions still referenced by surviving stock items
        try:
            stock_items = StockItem.objects.filter(product_id=product_id).select_related(
                "warehouse"
            )
            for item in stock_items:
                if item.warehouse_id:
                    warehouses.add(item.warehouse_id)
                    if item.warehouse.region_id:
                        regions.add(item.warehouse.region_id)
        except Exception as e:
            logger.error(f"Error invalidating product cache: {e}")

        # Invalidate each region cache
        for region_id in regions:
            cache.delete(StockCache._get_cache_key(product_id, region_id=region_id))

        # Invalidate each warehouse cache
        for warehouse_id in warehouses:
            cache.delete(StockCache._get_cache_key(product_id, warehouse_id=warehouse_id))

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
        from catalog.models import StockItem

        logger.info(f"Warming stock cache for {len(product_ids)} products")

        region_id = region.id if region else None

        # Aggregate stock for every product in a single grouped query
        queryset = StockItem.objects.filter(product_id__in=product_ids)
        if region:
            queryset = queryset.filter(warehouse__region=region, warehouse__is_active=True)

        stock_by_product = {
            row["product_id"]: StockCache._build_stock_data(
                row["total_on_hand"], row["total_allocated"]
            )
            for row in queryset.values("product_id").annotate(
                total_on_hand=Sum("on_hand"), total_allocated=Sum("allocated")
            )
        }

        # Populate every requested product, including those with zero stock
        result = {}
        cache_data = {}
        for product_id in product_ids:
            stock_data = stock_by_product.get(
                product_id, {"on_hand": 0, "allocated": 0, "available": 0}
            )
            result[product_id] = stock_data
            cache_data[StockCache._get_cache_key(product_id, region_id=region_id)] = stock_data

        cache.set_many(cache_data, StockCache.CACHE_TTL)

        return result


# Signal handlers for automatic cache invalidation


@receiver(post_save, sender="catalog.StockItem")
def invalidate_on_stock_change(sender, instance, **kwargs):
    """Invalidate cache when StockItem is created or updated"""
    product_id = instance.product_id
    transaction.on_commit(lambda: StockCache.invalidate_product_cache(product_id))


@receiver(post_delete, sender="catalog.StockItem")
def invalidate_on_stock_delete(sender, instance, **kwargs):
    """Invalidate cache when StockItem is deleted"""
    product_id = instance.product_id
    # Forward the deleted item's warehouse/region so their cache keys are cleared
    # even when this was the product's last item there and is no longer queryable.
    warehouse_id = instance.warehouse_id
    region_id = instance.warehouse.region_id if warehouse_id else None
    transaction.on_commit(
        lambda: StockCache.invalidate_product_cache(
            product_id,
            extra_warehouse_ids=[warehouse_id] if warehouse_id else None,
            extra_region_ids=[region_id] if region_id else None,
        )
    )


@receiver(post_save, sender="catalog.StockMovement")
def invalidate_on_stock_movement(sender, instance, **kwargs):
    """Invalidate cache when stock movement is recorded"""
    if instance.stock_item:
        product_id = instance.stock_item.product_id
        transaction.on_commit(lambda: StockCache.invalidate_product_cache(product_id))
