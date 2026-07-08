"""
Fulfillment Service for Multi-Location Inventory

This service handles warehouse selection and stock allocation for orders.
It selects the optimal warehouse(s) to fulfill an order based on:
- Customer's region/shipping address
- Product availability at each warehouse
- Warehouse fulfillment priority
- Stock buffer percentages
- Geographic proximity (via geocoder service)
"""
from typing import List, Dict, Tuple, Optional
from decimal import Decimal
from django.db.models import Q, F, Sum
from django.core.exceptions import ValidationError
from django.core.cache import cache
import logging
from math import radians, cos, sin, asin, sqrt

from catalog.models import Product, StockItem, Warehouse, SalesRegion
from orders.models import Order, OrderItem

logger = logging.getLogger(__name__)


class InsufficientStockError(Exception):
    """Raised when there's insufficient stock to fulfill an order"""
    pass


class FulfillmentService:
    """
    Service for warehouse selection and stock allocation.
    """

    def __init__(self):
        self.distance_weight = 0.3  # Weight for distance in scoring (30%)
        self.priority_weight = 0.4  # Weight for priority in scoring (40%)
        self.stock_weight = 0.3     # Weight for stock levels in scoring (30%)

    def select_warehouse_for_order(
        self,
        order: Order,
        order_items: List[Dict]
    ) -> Dict[int, Warehouse]:
        """
        Select optimal warehouse(s) to fulfill an order.

        Args:
            order: The Order instance
            order_items: List of dicts with 'product', 'variant', 'quantity' keys

        Returns:
            Dictionary mapping sequential index to Warehouse instance.
            Format: {0: warehouse_a, 1: warehouse_b, ...}
            Indices correspond to position in order_items list.

        Raises:
            InsufficientStockError: If insufficient stock to fulfill order
        """
        # Get customer's region
        region = self._get_order_region(order)

        # Get warehouses for this region
        warehouses = self._get_warehouses_for_region(region) if region else []

        # If no regional warehouses, try country-specific fallbacks
        if not warehouses:
            country_code = order.shipping_country or order.billing_country
            if country_code:
                warehouses = self._get_fallback_warehouses(country_code)

        # If still no warehouses, try highest-priority region as catch-all
        if not warehouses:
            default_region = SalesRegion.objects.filter(is_active=True).order_by('-priority').first()
            if default_region:
                logger.warning(
                    f"Order {order.id} has no region match or fallbacks, "
                    f"using default region {default_region.code}"
                )
                warehouses = self._get_warehouses_for_region(default_region)

        if not warehouses:
            region_info = region.code if region else 'unknown'
            raise InsufficientStockError(f"No active warehouses available for region {region_info}")

        # Try to fulfill from single warehouse first (preferred)
        single_warehouse = self._try_single_warehouse_fulfillment(
            order_items, warehouses, order
        )
        if single_warehouse:
            logger.info(f"Order can be fulfilled from single warehouse: {single_warehouse.code}")
            return {idx: single_warehouse for idx in range(len(order_items))}

        # Fall back to split shipment if necessary
        logger.info(f"Attempting split shipment for order {order.id}")
        allocation = self._allocate_split_shipment(order_items, warehouses, order)

        if allocation is None:
            raise InsufficientStockError("Insufficient stock across all warehouses")

        return allocation

    def check_stock_availability(
        self,
        product: Product,
        quantity: int,
        region: Optional[SalesRegion] = None,
        variant: Optional['ProductVariant'] = None
    ) -> Dict:
        """
        Check stock availability for a product in a region.

        Args:
            product: Product instance
            quantity: Quantity requested
            region: SalesRegion instance (optional)
            variant: ProductVariant instance (optional)

        Returns:
            Dictionary with availability info:
            {
                'available': bool,
                'quantity_available': int,
                'warehouses': [list of warehouse codes with stock],
                'can_backorder': bool
            }
        """
        # Products not tracking inventory are always available
        if not product.track_inventory:
            return {
                'available': True,
                'quantity_available': 999999,  # Effectively unlimited
                'warehouses': [],
                'can_backorder': False
            }

        # Get stock items — filter by variant
        stock_query = StockItem.objects.filter(
            product=product,
            warehouse__is_active=True
        )
        if variant:
            stock_query = stock_query.filter(variant=variant)
        else:
            stock_query = stock_query.filter(variant__isnull=True)

        # Filter by region if provided
        if region:
            stock_query = stock_query.filter(warehouse__region=region)

        # Calculate total available (on_hand - allocated)
        total_available = stock_query.aggregate(
            total=Sum(F('on_hand') - F('allocated'))
        )['total'] or 0

        # Get warehouses with stock
        warehouses_with_stock = stock_query.filter(
            on_hand__gt=F('allocated')
        ).values_list('warehouse__code', flat=True)

        return {
            'available': total_available >= quantity,
            'quantity_available': total_available,
            'warehouses': list(warehouses_with_stock),
            'can_backorder': product.allow_backorders
        }

    def _build_stock_filter(self, product, warehouse, variant=None):
        """Build filter kwargs for StockItem queries with proper variant handling."""
        filter_kwargs = {'product': product, 'warehouse': warehouse}
        if variant:
            filter_kwargs['variant'] = variant
        else:
            filter_kwargs['variant__isnull'] = True
        return filter_kwargs

    def allocate_stock(
        self,
        order_item: OrderItem,
        warehouse: Warehouse
    ) -> StockItem:
        """
        Allocate stock for an order item at a specific warehouse.

        Args:
            order_item: OrderItem instance
            warehouse: Warehouse to allocate from

        Returns:
            StockItem that was allocated

        Raises:
            InsufficientStockError: If insufficient stock at warehouse
        """
        product = order_item.product
        quantity = order_item.quantity

        # Products not tracking inventory don't need allocation
        if not product.track_inventory:
            logger.debug(f"Product {product.sku} doesn't track inventory, skipping allocation")
            return None

        # Get stock item — filter by variant
        filter_kwargs = self._build_stock_filter(product, warehouse, order_item.variant)
        try:
            stock_item = StockItem.objects.select_for_update().get(**filter_kwargs)
        except StockItem.DoesNotExist:
            raise InsufficientStockError(
                f"No stock item for {product.sku} at warehouse {warehouse.code}"
            )

        # Check availability (respecting buffer)
        available = stock_item.available
        if available < quantity:
            raise InsufficientStockError(
                f"Insufficient stock at {warehouse.code}: need {quantity}, have {available}"
            )

        # Allocate stock — use .filter().update() to bypass post_save signal
        StockItem.objects.filter(pk=stock_item.pk).update(
            allocated=F('allocated') + quantity
        )
        stock_item.refresh_from_db()

        logger.info(
            f"Allocated {quantity} of {product.sku} at {warehouse.code} "
            f"(on_hand: {stock_item.on_hand}, allocated: {stock_item.allocated})"
        )

        return stock_item

    def fulfill_stock(
        self,
        order_item: OrderItem,
        warehouse: Warehouse
    ) -> StockItem:
        """
        Fulfill stock for an order item (reduce on_hand and allocated).

        This should be called when the order is shipped.

        Args:
            order_item: OrderItem instance
            warehouse: Warehouse to fulfill from

        Returns:
            Updated StockItem
        """
        product = order_item.product
        quantity = order_item.quantity

        # Products not tracking inventory don't need fulfillment
        if not product.track_inventory:
            return None

        # Get stock item — filter by variant
        filter_kwargs = self._build_stock_filter(product, warehouse, order_item.variant)
        try:
            stock_item = StockItem.objects.select_for_update().get(**filter_kwargs)
        except StockItem.DoesNotExist:
            logger.error(f"No stock item for {product.sku} at {warehouse.code}")
            return None

        # Reduce on_hand and allocated — use .filter().update() to bypass post_save signal
        StockItem.objects.filter(pk=stock_item.pk).update(
            on_hand=F('on_hand') - quantity,
            allocated=F('allocated') - quantity,
        )
        stock_item.refresh_from_db()

        logger.info(
            f"Fulfilled {quantity} of {product.sku} from {warehouse.code} "
            f"(on_hand: {stock_item.on_hand}, allocated: {stock_item.allocated})"
        )

        # Check if low stock
        if stock_item.on_hand <= stock_item.low_stock_threshold:
            logger.warning(
                f"Low stock alert: {product.sku} at {warehouse.code} "
                f"has {stock_item.on_hand} units (threshold: {stock_item.low_stock_threshold})"
            )

        return stock_item

    def release_stock(
        self,
        order_item: OrderItem,
        warehouse: Warehouse
    ) -> StockItem:
        """
        Release allocated stock for an order item (e.g., on cancellation).

        Args:
            order_item: OrderItem instance
            warehouse: Warehouse to release stock from

        Returns:
            Updated StockItem
        """
        product = order_item.product
        quantity = order_item.quantity

        # Products not tracking inventory don't need release
        if not product.track_inventory:
            return None

        # Get stock item — filter by variant
        filter_kwargs = self._build_stock_filter(product, warehouse, order_item.variant)
        try:
            stock_item = StockItem.objects.select_for_update().get(**filter_kwargs)
        except StockItem.DoesNotExist:
            logger.error(f"No stock item for {product.sku} at {warehouse.code}")
            return None

        # Release allocation — use .filter().update() to bypass post_save signal
        StockItem.objects.filter(pk=stock_item.pk).update(
            allocated=F('allocated') - quantity,
        )
        stock_item.refresh_from_db()

        logger.info(
            f"Released {quantity} of {product.sku} at {warehouse.code} "
            f"(on_hand: {stock_item.on_hand}, allocated: {stock_item.allocated})"
        )

        return stock_item

    # Private helper methods

    def _get_order_region(self, order: Order) -> Optional[SalesRegion]:
        """Get the sales region for an order based on shipping address."""
        # Get country from shipping address
        country_code = order.shipping_country
        if not country_code:
            # Try billing country
            country_code = order.billing_country

        if not country_code:
            return None

        # Find region that includes this country
        regions = SalesRegion.objects.filter(is_active=True).order_by('-priority')
        for region in regions:
            if isinstance(region.countries, list) and country_code in region.countries:
                return region

        # Fallback: use shipping_origin_country from site settings to find a default region
        try:
            from core.models import SiteSettings
            site_settings = SiteSettings.objects.first()
            if site_settings and site_settings.shipping_origin_country:
                origin = site_settings.shipping_origin_country
                for region in regions:
                    if isinstance(region.countries, list) and origin in region.countries:
                        logger.info(
                            f"No region for {country_code}, falling back to origin country "
                            f"{origin} region: {region.code}"
                        )
                        return region
        except Exception:
            pass

        return None

    def _get_warehouses_for_region(self, region: SalesRegion) -> List[Warehouse]:
        """Get active warehouses for a region, ordered by fulfillment priority."""
        return list(
            Warehouse.objects.filter(
                region=region,
                is_active=True
            ).order_by('-fulfillment_priority')
        )

    def _get_fallback_warehouses(self, country_code: str) -> List[Warehouse]:
        """
        Get fallback warehouses for a country from CountryWarehouseFallback.

        Used when no regional warehouses are available.
        """
        try:
            from shipping.models import ShippingCountry, CountryWarehouseFallback
            shipping_country = ShippingCountry.objects.get(
                country_code=country_code.upper(),
                is_active=True
            )
            # First try the primary source_warehouse
            warehouses = []
            if shipping_country.source_warehouse and shipping_country.source_warehouse.is_active:
                warehouses.append(shipping_country.source_warehouse)

            # Then add fallback warehouses in priority order
            fallbacks = CountryWarehouseFallback.objects.filter(
                country=shipping_country,
                warehouse__is_active=True
            ).select_related('warehouse').order_by('priority')
            for fallback in fallbacks:
                if fallback.warehouse not in warehouses:
                    warehouses.append(fallback.warehouse)

            if warehouses:
                logger.info(
                    f"Using fallback warehouses for {country_code}: "
                    f"{[w.code for w in warehouses]}"
                )
            return warehouses
        except Exception:
            return []

    def _try_single_warehouse_fulfillment(
        self,
        order_items: List[Dict],
        warehouses: List[Warehouse],
        order: Order
    ) -> Optional[Warehouse]:
        """
        Try to fulfill entire order from a single warehouse.

        Returns the best warehouse if possible, None if split shipment needed.
        """
        candidate_warehouses = []

        for warehouse in warehouses:
            can_fulfill = True

            for item in order_items:
                product = item['product']
                variant = item.get('variant')
                quantity = item['quantity']

                # Skip non-inventory-tracked products
                if not product.track_inventory:
                    continue

                # Check if warehouse has stock — filter by variant
                filter_kwargs = self._build_stock_filter(product, warehouse, variant)
                try:
                    stock_item = StockItem.objects.get(**filter_kwargs)
                    if stock_item.available < quantity:
                        can_fulfill = False
                        break
                except StockItem.DoesNotExist:
                    can_fulfill = False
                    break

            if can_fulfill:
                # Calculate warehouse score with order items for stock scoring
                score = self._calculate_warehouse_score(warehouse, order, order_items)
                candidate_warehouses.append((warehouse, score))

        if not candidate_warehouses:
            return None

        # Return warehouse with highest score
        candidate_warehouses.sort(key=lambda x: x[1], reverse=True)
        return candidate_warehouses[0][0]

    def _allocate_split_shipment(
        self,
        order_items: List[Dict],
        warehouses: List[Warehouse],
        order: Order
    ) -> Optional[Dict[int, Warehouse]]:
        """
        Allocate items across multiple warehouses for split shipment.

        Returns mapping of sequential index to warehouse, or None if allocation fails.
        """
        allocation = {}
        # Track remaining items with their original indices
        remaining = list(enumerate(order_items))

        for warehouse in warehouses:
            newly_allocated = []

            for idx, item in remaining:
                product = item['product']
                variant = item.get('variant')
                quantity = item['quantity']

                # Non-inventory-tracked products can be allocated anywhere
                if not product.track_inventory:
                    allocation[idx] = warehouse
                    newly_allocated.append((idx, item))
                    continue

                # Check if warehouse has stock — filter by variant
                filter_kwargs = self._build_stock_filter(product, warehouse, variant)
                try:
                    stock_item = StockItem.objects.get(**filter_kwargs)
                    if stock_item.available >= quantity:
                        allocation[idx] = warehouse
                        newly_allocated.append((idx, item))
                except StockItem.DoesNotExist:
                    continue

            # Remove allocated items from remaining
            for entry in newly_allocated:
                remaining.remove(entry)

            # If all items allocated, we're done
            if not remaining:
                break

        # If there are still remaining items, allocation failed
        if remaining:
            return None

        return allocation

    def _calculate_warehouse_score(
        self,
        warehouse: Warehouse,
        order: Order,
        order_items: Optional[List[Dict]] = None
    ) -> float:
        """
        Calculate a score for a warehouse based on multiple factors.

        Higher score = better choice for fulfillment.
        """
        score = 0.0

        # Factor 1: Fulfillment priority (0-100, normalized to 0-1)
        priority_score = warehouse.fulfillment_priority / 100.0
        score += priority_score * self.priority_weight

        # Factor 2: Geographic proximity (via geocoder)
        distance_score = self._calculate_distance_score(warehouse, order)
        score += distance_score * self.distance_weight

        # Factor 3: Stock levels — actual ratio of available/needed
        stock_score = self._calculate_stock_score(warehouse, order_items)
        score += stock_score * self.stock_weight

        return score

    def _calculate_stock_score(
        self,
        warehouse: Warehouse,
        order_items: Optional[List[Dict]] = None
    ) -> float:
        """
        Calculate stock score based on actual availability vs needed quantity.

        Returns value between 0.0 and 1.0.
        Higher = more stock available relative to order needs.
        """
        if not order_items:
            return 0.5

        scores = []
        for item in order_items:
            product = item['product']
            variant = item.get('variant')
            quantity = item['quantity']

            if not product.track_inventory:
                scores.append(1.0)
                continue

            filter_kwargs = self._build_stock_filter(product, warehouse, variant)
            try:
                stock_item = StockItem.objects.get(**filter_kwargs)
                # Ratio of available to needed, capped at 1.0
                ratio = min(stock_item.available / max(quantity, 1), 1.0)
                scores.append(ratio)
            except StockItem.DoesNotExist:
                scores.append(0.0)

        return sum(scores) / len(scores) if scores else 0.5

    def _calculate_distance_score(self, warehouse: Warehouse, order: Order) -> float:
        """
        Calculate distance score using geocoder service (closer = higher score).

        Returns value between 0 and 1. Gracefully degrades to 0.5 if geocoding
        is unavailable or warehouse has no coordinates.
        """
        # Check if warehouse has coordinates
        if not all([warehouse.latitude, warehouse.longitude]):
            return 0.5

        # Try to geocode the customer's shipping address
        customer_coords = self._geocode_order_address(order)
        if not customer_coords:
            return 0.5

        customer_lat, customer_lon = customer_coords

        # Calculate distance
        distance_km = self._haversine_distance(
            float(warehouse.latitude),
            float(warehouse.longitude),
            customer_lat,
            customer_lon
        )

        # Convert distance to score: closer = higher
        # Use exponential decay: score = e^(-distance/reference_distance)
        # Reference: 1000km gives ~0.37, 100km gives ~0.90, 5000km gives ~0.007
        import math
        reference_distance = 1000.0  # km
        distance_score = math.exp(-distance_km / reference_distance)

        return min(max(distance_score, 0.0), 1.0)

    def _geocode_order_address(self, order: Order) -> Optional[Tuple[float, float]]:
        """
        Geocode an order's shipping address to (lat, lon) coordinates.

        Uses the AutocompleteClient with caching to avoid repeated lookups.
        Returns None if geocoding fails.
        """
        # Build address string from order
        address_parts = []
        for field in [order.shipping_address1, order.shipping_city,
                      order.shipping_state, order.shipping_postal_code,
                      order.shipping_country]:
            if field:
                address_parts.append(str(field))

        if not address_parts:
            return None

        address_string = ", ".join(address_parts)

        # Check cache first (long TTL since addresses don't move)
        cache_key = f"fulfillment:geocode:{hash(address_string)}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached if cached != 'NONE' else None

        try:
            from address_autocomplete.services import AutocompleteClient
            client = AutocompleteClient()
            result = client.autocomplete(
                query=address_string,
                country_bias=order.shipping_country,
                limit=1,
            )

            if result.get('suggestions'):
                centroid = result['suggestions'][0].get('centroid')
                if centroid and centroid.get('lat') and centroid.get('lon'):
                    coords = (float(centroid['lat']), float(centroid['lon']))
                    cache.set(cache_key, coords, 86400)  # Cache 24 hours
                    return coords

            # Cache negative result to avoid re-querying
            cache.set(cache_key, 'NONE', 3600)  # Cache 1 hour
            return None

        except Exception as e:
            logger.debug(f"Geocoding failed for order {order.id}: {e}")
            return None

    def _haversine_distance(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float
    ) -> float:
        """
        Calculate distance between two points on Earth using Haversine formula.

        Returns distance in kilometers.
        """
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))

        # Radius of Earth in kilometers
        r = 6371

        return c * r


# Global instance for easy access
fulfillment_service = FulfillmentService()
