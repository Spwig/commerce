"""
Inventory Intelligence Service for Admin API

Provides advanced inventory analytics including velocity tracking,
reorder suggestions, and stock movement analysis.
"""
from decimal import Decimal
from datetime import timedelta, date
from django.db.models import (
    Sum, Count, Avg, F, Q, Value, Case, When,
    DecimalField, IntegerField, CharField,
    Min, Max, Subquery, OuterRef,
)
from django.db.models.functions import Coalesce, TruncDate, Abs
from django.utils import timezone
from core.utils import get_default_currency


class InventoryService:
    """
    Service for computing inventory intelligence data.

    All velocity calculations use StockMovement with movement_type='fulfillment'.
    Fulfillment movements have negative quantities (stock leaving warehouse),
    so we use absolute values when computing velocity.
    """

    # ──────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────

    @staticmethod
    def _get_site_settings():
        """Get SiteSettings singleton."""
        from core.models import SiteSettings
        try:
            return SiteSettings.objects.first()
        except Exception:
            return None

    @staticmethod
    def _get_image_url(product):
        """Get primary image thumbnail URL for a product."""
        try:
            primary = product.images.filter(is_primary=True).first()
            if primary and primary.media_asset:
                return primary.media_asset.get_thumbnail('medium') or primary.media_asset.get_display_url()
            first_image = product.images.first()
            if first_image and first_image.media_asset:
                return first_image.media_asset.get_thumbnail('medium') or first_image.media_asset.get_display_url()
        except Exception:
            pass
        return None

    @classmethod
    def _compute_velocity(cls, product_id, variant_id=None, days=30):
        """
        Compute average daily sales velocity for a product over a given number of days.

        Returns Decimal average daily units sold.
        """
        from catalog.models import StockMovement

        now = timezone.now()
        start_date = now - timedelta(days=days)

        filters = Q(
            stock_item__product_id=product_id,
            movement_type='fulfillment',
            created_at__gte=start_date,
        )
        if variant_id:
            filters &= Q(stock_item__variant_id=variant_id)

        total_units = StockMovement.objects.filter(filters).aggregate(
            total=Coalesce(
                Sum(Abs('quantity')),
                Value(0),
                output_field=IntegerField()
            )
        )['total']

        if days <= 0:
            return Decimal('0.00')

        return Decimal(str(total_units)) / Decimal(str(days))

    # ──────────────────────────────────────────────
    # a) Dashboard
    # ──────────────────────────────────────────────

    @classmethod
    def get_inventory_dashboard(cls):
        """
        Get inventory intelligence dashboard data.

        Returns:
            dict with total counts, stock status breakdown, velocity leaders,
            and recent stockout information.
        """
        from catalog.models import Product, StockItem, StockMovement

        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)

        # Base queryset: published products that track inventory
        tracked_products = Product.objects.filter(
            status='published',
            track_inventory=True,
        )

        total_products = tracked_products.count()
        total_variants = StockItem.objects.filter(
            product__status='published',
            product__track_inventory=True,
        ).count()

        # Total stock value: sum of on_hand * product.price.amount
        total_stock_value = StockItem.objects.filter(
            product__status='published',
            product__track_inventory=True,
        ).aggregate(
            total=Coalesce(
                Sum(
                    F('on_hand') * F('product__price'),
                    output_field=DecimalField(max_digits=14, decimal_places=2),
                ),
                Value(Decimal('0.00')),
                output_field=DecimalField(max_digits=14, decimal_places=2),
            )
        )['total']

        # Stock status counts - annotate available stock per product
        products_with_stock = tracked_products.annotate(
            _available=Coalesce(
                Sum(F('stock_items__on_hand') - F('stock_items__allocated')),
                Value(0),
                output_field=IntegerField(),
            )
        )

        out_of_stock_count = products_with_stock.filter(_available__lte=0).count()
        low_stock_count = products_with_stock.filter(
            _available__gt=0,
            _available__lte=F('low_stock_threshold'),
        ).count()
        in_stock_count = products_with_stock.filter(
            _available__gt=F('low_stock_threshold'),
        ).count()
        overstock_count = products_with_stock.filter(
            _available__gt=F('low_stock_threshold') * 5,
        ).count()

        # Stockouts in last 30 days: products whose stock hit 0 via movement
        stockouts_last_30_days = StockMovement.objects.filter(
            created_at__gte=thirty_days_ago,
            new_quantity__lte=0,
            stock_item__product__track_inventory=True,
        ).values('stock_item__product_id').distinct().count()

        # Top velocity products (5 products with highest fulfillment volume in 30 days)
        top_velocity_qs = StockMovement.objects.filter(
            movement_type='fulfillment',
            created_at__gte=thirty_days_ago,
            stock_item__product__track_inventory=True,
        ).values(
            'stock_item__product_id',
            'stock_item__product__name',
            'stock_item__product__sku',
        ).annotate(
            total_sold=Sum(Abs('quantity')),
        ).order_by('-total_sold')[:5]

        top_velocity_products = []
        for item in top_velocity_qs:
            total_sold = item['total_sold'] or 0
            daily_avg = Decimal(str(total_sold)) / Decimal('30') if total_sold else Decimal('0.00')
            top_velocity_products.append({
                'product_id': item['stock_item__product_id'],
                'product_name': item['stock_item__product__name'],
                'sku': item['stock_item__product__sku'],
                'units_sold_30d': total_sold,
                'daily_average': round(daily_avg, 2),
            })

        # Recent stockouts (5 most recent products to hit 0 stock)
        recent_stockout_qs = StockMovement.objects.filter(
            new_quantity__lte=0,
            stock_item__product__track_inventory=True,
        ).values(
            'stock_item__product_id',
            'stock_item__product__name',
            'stock_item__product__sku',
        ).annotate(
            stockout_date=Max('created_at'),
        ).order_by('-stockout_date')[:5]

        recent_stockouts = [
            {
                'product_id': item['stock_item__product_id'],
                'product_name': item['stock_item__product__name'],
                'sku': item['stock_item__product__sku'],
                'stockout_date': item['stockout_date'],
            }
            for item in recent_stockout_qs
        ]

        return {
            'total_products': total_products,
            'total_variants': total_variants,
            'total_stock_value': total_stock_value,
            'currency': get_default_currency(),
            'in_stock_count': in_stock_count,
            'low_stock_count': low_stock_count,
            'out_of_stock_count': out_of_stock_count,
            'overstock_count': overstock_count,
            'stockouts_last_30_days': stockouts_last_30_days,
            'top_velocity_products': top_velocity_products,
            'recent_stockouts': recent_stockouts,
        }

    # ──────────────────────────────────────────────
    # b) Low Stock Products (enhanced)
    # ──────────────────────────────────────────────

    @classmethod
    def get_low_stock_products(
        cls,
        page=1,
        page_size=20,
        ordering='available_stock',
        severity=None,
        category_id=None,
        warehouse_id=None,
    ):
        """
        Enhanced low stock product list with velocity and restock data.

        Args:
            page: Page number (1-indexed)
            page_size: Items per page (max 100)
            ordering: Sort field (available_stock, -available_stock, velocity, -velocity, name, -name)
            severity: Filter by 'critical' (0 stock) or 'warning' (below threshold)
            category_id: Filter by category
            warehouse_id: Filter by warehouse

        Returns:
            dict with products list and pagination info
        """
        from catalog.models import Product, StockItem, StockMovement

        now = timezone.now()
        seven_days_ago = now - timedelta(days=7)
        thirty_days_ago = now - timedelta(days=30)

        # Base queryset: published, tracking inventory
        qs = Product.objects.filter(
            status='published',
            track_inventory=True,
        ).select_related('category')

        # Optional warehouse filter: only include products with stock items in this warehouse
        if warehouse_id:
            qs = qs.filter(stock_items__warehouse_id=warehouse_id)

        # Optional category filter
        if category_id:
            qs = qs.filter(category_id=category_id)

        # Annotate available stock
        qs = qs.annotate(
            _available_stock=Coalesce(
                Sum(F('stock_items__on_hand') - F('stock_items__allocated')),
                Value(0),
                output_field=IntegerField(),
            )
        )

        # Filter to low stock products (available <= threshold)
        qs = qs.filter(_available_stock__lte=F('low_stock_threshold'))

        # Severity filter
        if severity == 'critical':
            qs = qs.filter(_available_stock__lte=0)
        elif severity == 'warning':
            qs = qs.filter(_available_stock__gt=0, _available_stock__lte=F('low_stock_threshold'))

        # Ordering
        order_map = {
            'available_stock': '_available_stock',
            '-available_stock': '-_available_stock',
            'name': 'name',
            '-name': '-name',
        }
        order_field = order_map.get(ordering, '_available_stock')
        qs = qs.order_by(order_field)

        # Pagination
        total_count = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        products = list(qs[start:end])

        # Build enriched product data
        product_ids = [p.id for p in products]

        # Compute 7-day and 30-day fulfillment volumes per product
        velocity_7d_data = dict(
            StockMovement.objects.filter(
                movement_type='fulfillment',
                created_at__gte=seven_days_ago,
                stock_item__product_id__in=product_ids,
            ).values('stock_item__product_id').annotate(
                total=Sum(Abs('quantity')),
            ).values_list('stock_item__product_id', 'total')
        )

        velocity_30d_data = dict(
            StockMovement.objects.filter(
                movement_type='fulfillment',
                created_at__gte=thirty_days_ago,
                stock_item__product_id__in=product_ids,
            ).values('stock_item__product_id').annotate(
                total=Sum(Abs('quantity')),
            ).values_list('stock_item__product_id', 'total')
        )

        # Last restock per product (adjustment movements with positive quantity)
        last_restock_qs = StockMovement.objects.filter(
            movement_type='adjustment',
            quantity__gt=0,
            stock_item__product_id__in=product_ids,
        ).values('stock_item__product_id').annotate(
            last_date=Max('created_at'),
        )
        last_restock_dates = {
            item['stock_item__product_id']: item['last_date']
            for item in last_restock_qs
        }

        # Get the actual restock quantity for each product's last restock
        last_restock_quantities = {}
        for pid, restock_date in last_restock_dates.items():
            movement = StockMovement.objects.filter(
                movement_type='adjustment',
                quantity__gt=0,
                stock_item__product_id=pid,
                created_at=restock_date,
            ).first()
            if movement:
                last_restock_quantities[pid] = movement.quantity

        # Per-warehouse breakdown for each product
        stock_items_by_product = {}
        stock_items_qs = StockItem.objects.filter(
            product_id__in=product_ids,
        ).select_related('warehouse')
        if warehouse_id:
            stock_items_qs = stock_items_qs.filter(warehouse_id=warehouse_id)

        for si in stock_items_qs:
            stock_items_by_product.setdefault(si.product_id, []).append({
                'warehouse_id': si.warehouse_id,
                'warehouse_name': si.warehouse.name,
                'on_hand': si.on_hand,
                'allocated': si.allocated,
            })

        # Build result list
        result_products = []
        for product in products:
            available = product._available_stock
            threshold = product.low_stock_threshold

            # Severity
            if available <= 0:
                sev = 'critical'
            else:
                sev = 'warning'

            # Velocity calculations
            sold_7d = velocity_7d_data.get(product.id, 0) or 0
            sold_30d = velocity_30d_data.get(product.id, 0) or 0
            vel_7d = Decimal(str(sold_7d)) / Decimal('7')
            vel_30d = Decimal(str(sold_30d)) / Decimal('30')

            # Days of supply remaining
            if vel_30d > 0 and available > 0:
                days_remaining = Decimal(str(available)) / vel_30d
            else:
                days_remaining = None

            # Image URL
            image_url = cls._get_image_url(product)

            result_products.append({
                'product_id': product.id,
                'product_name': product.name,
                'sku': product.sku,
                'image_url': image_url,
                'category_name': product.category.name if product.category else None,
                'available_stock': available,
                'low_stock_threshold': threshold,
                'severity': sev,
                'velocity_7d': round(vel_7d, 2),
                'velocity_30d': round(vel_30d, 2),
                'days_of_supply_remaining': round(days_remaining, 1) if days_remaining is not None else None,
                'last_restock_date': last_restock_dates.get(product.id),
                'last_restock_quantity': last_restock_quantities.get(product.id),
                'stock_items': stock_items_by_product.get(product.id, []),
            })

        total_pages = (total_count + page_size - 1) // page_size if total_count > 0 else 0

        return {
            'products': result_products,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total_count': total_count,
                'total_pages': total_pages,
            }
        }

    # ──────────────────────────────────────────────
    # c) Velocity
    # ──────────────────────────────────────────────

    @classmethod
    def get_velocity(cls, product_id, variant_id=None, period='30d'):
        """
        Get detailed stock velocity data for a specific product.

        Args:
            product_id: Product ID
            variant_id: Optional variant ID
            period: '7d', '30d', or '90d'

        Returns:
            dict with current stock, velocity averages, trend, and daily sales
        """
        from catalog.models import Product, StockItem, StockMovement

        now = timezone.now()
        today = now.date()

        # Resolve period to days
        period_map = {'7d': 7, '30d': 30, '90d': 90}
        num_days = period_map.get(period, 30)

        # Get product
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return None

        # Current stock
        stock_filters = Q(product_id=product_id)
        if variant_id:
            stock_filters &= Q(variant_id=variant_id)

        stock_agg = StockItem.objects.filter(stock_filters).aggregate(
            total_on_hand=Coalesce(Sum('on_hand'), Value(0), output_field=IntegerField()),
            total_allocated=Coalesce(Sum('allocated'), Value(0), output_field=IntegerField()),
        )
        current_stock = max(0, stock_agg['total_on_hand'] - stock_agg['total_allocated'])

        # Velocity averages for 7d, 30d, 90d
        vel_7d = cls._compute_velocity(product_id, variant_id, days=7)
        vel_30d = cls._compute_velocity(product_id, variant_id, days=30)
        vel_90d = cls._compute_velocity(product_id, variant_id, days=90)

        # Trend calculation: compare first half vs second half of 30-day window
        mid_point = now - timedelta(days=15)
        thirty_days_ago = now - timedelta(days=30)

        movement_filters = Q(
            stock_item__product_id=product_id,
            movement_type='fulfillment',
        )
        if variant_id:
            movement_filters &= Q(stock_item__variant_id=variant_id)

        first_half = StockMovement.objects.filter(
            movement_filters,
            created_at__gte=thirty_days_ago,
            created_at__lt=mid_point,
        ).aggregate(
            total=Coalesce(Sum(Abs('quantity')), Value(0), output_field=IntegerField())
        )['total']

        second_half = StockMovement.objects.filter(
            movement_filters,
            created_at__gte=mid_point,
        ).aggregate(
            total=Coalesce(Sum(Abs('quantity')), Value(0), output_field=IntegerField())
        )['total']

        if first_half > 0:
            trend_pct = round(((second_half - first_half) / first_half) * 100, 1)
        else:
            trend_pct = 0.0 if second_half == 0 else 100.0

        if trend_pct > 10:
            trend = 'increasing'
        elif trend_pct < -10:
            trend = 'decreasing'
        else:
            trend = 'stable'

        # Days of supply remaining
        if vel_30d > 0 and current_stock > 0:
            days_remaining = Decimal(str(current_stock)) / vel_30d
            projected_stockout = today + timedelta(days=int(days_remaining))
        else:
            days_remaining = None
            projected_stockout = None

        # Daily sales data for the requested period
        period_start = today - timedelta(days=num_days - 1)

        daily_movements = StockMovement.objects.filter(
            movement_filters,
            created_at__date__gte=period_start,
        ).annotate(
            sale_date=TruncDate('created_at'),
        ).values('sale_date').annotate(
            units_sold=Sum(Abs('quantity')),
        ).order_by('sale_date')

        daily_lookup = {
            row['sale_date']: row['units_sold'] or 0
            for row in daily_movements
        }

        # Build daily sales array with running stock level estimation
        # We work backwards from current stock to estimate historical levels
        daily_sales = []
        running_stock = current_stock
        daily_entries = []

        for i in range(num_days):
            d = period_start + timedelta(days=i)
            units = daily_lookup.get(d, 0)
            daily_entries.append({'date': d, 'units_sold': units})

        # Calculate stock levels: go forward from estimated start stock
        # Estimate start stock = current + total sold in period
        total_sold_period = sum(e['units_sold'] for e in daily_entries)
        start_stock = current_stock + total_sold_period

        running = start_stock
        for entry in daily_entries:
            running -= entry['units_sold']
            daily_sales.append({
                'date': entry['date'],
                'units_sold': entry['units_sold'],
                'stock_level': max(0, running),
            })

        return {
            'product_id': product_id,
            'variant_id': variant_id,
            'current_stock': current_stock,
            'low_stock_threshold': product.low_stock_threshold,
            'velocity': {
                'daily_average_7d': round(vel_7d, 2),
                'daily_average_30d': round(vel_30d, 2),
                'daily_average_90d': round(vel_90d, 2),
            },
            'trend': trend,
            'trend_percentage': trend_pct,
            'days_of_supply_remaining': round(days_remaining, 1) if days_remaining is not None else None,
            'projected_stockout_date': projected_stockout,
            'daily_sales': daily_sales,
        }

    # ──────────────────────────────────────────────
    # d) Stock Movements
    # ──────────────────────────────────────────────

    @classmethod
    def get_stock_movements(
        cls,
        product_id,
        variant_id=None,
        warehouse_id=None,
        movement_type=None,
        start_date=None,
        end_date=None,
        page=1,
        page_size=20,
    ):
        """
        Get paginated stock movement history for a product.

        Args:
            product_id: Required product ID
            variant_id: Optional variant filter
            warehouse_id: Optional warehouse filter
            movement_type: Optional movement type filter
            start_date: Optional start date filter
            end_date: Optional end date filter
            page: Page number
            page_size: Items per page

        Returns:
            dict with movements list and pagination
        """
        from catalog.models import StockMovement

        filters = Q(stock_item__product_id=product_id)

        if variant_id:
            filters &= Q(stock_item__variant_id=variant_id)
        if warehouse_id:
            filters &= Q(stock_item__warehouse_id=warehouse_id)
        if movement_type:
            filters &= Q(movement_type=movement_type)
        if start_date:
            filters &= Q(created_at__date__gte=start_date)
        if end_date:
            filters &= Q(created_at__date__lte=end_date)

        qs = StockMovement.objects.filter(filters).select_related(
            'stock_item__warehouse',
            'stock_item__variant',
            'order',
            'user',
        ).order_by('-created_at')

        total_count = qs.count()
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        movements = qs[start_idx:end_idx]

        movement_list = []
        for m in movements:
            movement_list.append({
                'id': m.id,
                'movement_type': m.movement_type,
                'movement_type_display': m.get_movement_type_display(),
                'quantity': m.quantity,
                'previous_quantity': m.previous_quantity,
                'new_quantity': m.new_quantity,
                'reason': m.reason,
                'warehouse_id': m.stock_item.warehouse_id,
                'warehouse_name': m.stock_item.warehouse.name,
                'variant_id': m.stock_item.variant_id,
                'variant_sku': m.stock_item.variant.sku if m.stock_item.variant else None,
                'order_number': m.order.order_number if m.order else None,
                'user_name': m.user.get_full_name() if m.user else None,
                'created_at': m.created_at,
            })

        total_pages = (total_count + page_size - 1) // page_size if total_count > 0 else 0

        return {
            'movements': movement_list,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total_count': total_count,
                'total_pages': total_pages,
            }
        }

    # ──────────────────────────────────────────────
    # e) Reorder Suggestions
    # ──────────────────────────────────────────────

    @classmethod
    def get_reorder_suggestions(
        cls,
        page=1,
        page_size=20,
        ordering='urgency',
        urgency=None,
    ):
        """
        Get products that need reordering based on velocity and supply projections.

        Suggested reorder quantity formula:
            velocity * (lead_days + safety_multiplier * lead_days) - current_stock

        Urgency levels:
            immediate: <7 days supply
            soon: 7-14 days supply
            upcoming: 14-30 days supply

        Args:
            page: Page number
            page_size: Items per page
            ordering: Sort field (urgency, -urgency, name, -name)
            urgency: Filter by urgency level

        Returns:
            dict with suggestions list and pagination
        """
        from catalog.models import Product, StockItem, StockMovement

        now = timezone.now()
        today = now.date()
        thirty_days_ago = now - timedelta(days=30)

        # Get inventory settings from SiteSettings
        site_settings = cls._get_site_settings()
        lead_days = getattr(site_settings, 'default_reorder_lead_days', 14)
        safety_multiplier = getattr(site_settings, 'safety_stock_multiplier', 1.5)

        # All tracked, published products with their available stock
        products_qs = Product.objects.filter(
            status='published',
            track_inventory=True,
        ).select_related('category').prefetch_related('images').annotate(
            _available_stock=Coalesce(
                Sum(F('stock_items__on_hand') - F('stock_items__allocated')),
                Value(0),
                output_field=IntegerField(),
            )
        )

        # Get 30-day velocity for all tracked products
        velocity_data = dict(
            StockMovement.objects.filter(
                movement_type='fulfillment',
                created_at__gte=thirty_days_ago,
                stock_item__product__status='published',
                stock_item__product__track_inventory=True,
            ).values('stock_item__product_id').annotate(
                total=Sum(Abs('quantity')),
            ).values_list('stock_item__product_id', 'total')
        )

        # Build suggestions for products with <= 30 days supply
        suggestions = []
        for product in products_qs:
            available = product._available_stock
            sold_30d = velocity_data.get(product.id, 0) or 0

            if sold_30d == 0:
                # No sales velocity - skip unless already out of stock
                if available > 0:
                    continue
                # Out of stock with no velocity - mark as immediate
                vel_daily = Decimal('0')
                days_remaining = Decimal('0')
            else:
                vel_daily = Decimal(str(sold_30d)) / Decimal('30')
                if available > 0:
                    days_remaining = Decimal(str(available)) / vel_daily
                else:
                    days_remaining = Decimal('0')

            # Determine urgency
            if days_remaining < 7:
                prod_urgency = 'immediate'
                urgency_sort = 0
            elif days_remaining < 14:
                prod_urgency = 'soon'
                urgency_sort = 1
            elif days_remaining < 30:
                prod_urgency = 'upcoming'
                urgency_sort = 2
            else:
                # More than 30 days of supply - no reorder needed
                continue

            # Filter by urgency if specified
            if urgency and prod_urgency != urgency:
                continue

            # Suggested reorder quantity
            # velocity * (lead_days + safety_multiplier * lead_days) - current_stock
            reorder_qty = vel_daily * Decimal(str(lead_days + safety_multiplier * lead_days)) - Decimal(str(available))
            reorder_qty = max(Decimal('0'), reorder_qty)
            reorder_qty = int(reorder_qty.quantize(Decimal('1')))

            # Projected stockout date
            if vel_daily > 0 and available > 0:
                projected_stockout = today + timedelta(days=int(days_remaining))
            else:
                projected_stockout = today  # Already out or will be soon

            suggestions.append({
                'product_id': product.id,
                'product_name': product.name,
                'sku': product.sku,
                'image_url': cls._get_image_url(product),
                'category_name': product.category.name if product.category else None,
                'current_stock': available,
                'velocity_30d': round(vel_daily, 2),
                'days_of_supply_remaining': round(days_remaining, 1),
                'projected_stockout_date': projected_stockout,
                'suggested_reorder_quantity': reorder_qty,
                'urgency': prod_urgency,
                '_urgency_sort': urgency_sort,
                '_days_remaining': days_remaining,
            })

        # Sort
        if ordering == 'urgency' or ordering == '-urgency':
            reverse = ordering.startswith('-')
            suggestions.sort(key=lambda x: (x['_urgency_sort'], x['_days_remaining']), reverse=reverse)
        elif ordering == 'name':
            suggestions.sort(key=lambda x: x['product_name'])
        elif ordering == '-name':
            suggestions.sort(key=lambda x: x['product_name'], reverse=True)
        else:
            # Default: most urgent first
            suggestions.sort(key=lambda x: (x['_urgency_sort'], x['_days_remaining']))

        # Clean up internal sort keys
        for s in suggestions:
            s.pop('_urgency_sort', None)
            s.pop('_days_remaining', None)

        # Pagination
        total_count = len(suggestions)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_suggestions = suggestions[start_idx:end_idx]

        total_pages = (total_count + page_size - 1) // page_size if total_count > 0 else 0

        return {
            'suggestions': page_suggestions,
            'settings': {
                'lead_days': lead_days,
                'safety_multiplier': float(safety_multiplier),
            },
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total_count': total_count,
                'total_pages': total_pages,
            }
        }
