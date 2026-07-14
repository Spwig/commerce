"""
Analytics Service for Admin API

Provides analytics data for the merchant mobile app dashboard
and advanced analytics for the admin web interface.
"""

import math
from datetime import date, datetime, timedelta
from decimal import Decimal

from django.db.models import (
    Avg,
    Count,
    DecimalField,
    F,
    IntegerField,
    OuterRef,
    Q,
    Subquery,
    Sum,
    Value,
)
from django.db.models.functions import Coalesce, ExtractHour, TruncDate
from django.utils import timezone

from core.utils import get_default_currency


class AnalyticsService:
    """
    Service for computing analytics data for the admin API.

    All methods return data optimized for mobile app display,
    with proper currency handling and period comparisons.
    """

    # ------------------------------------------------------------------ #
    #  Helper: base queryset for paid, non-cancelled/refunded orders
    # ------------------------------------------------------------------ #
    @staticmethod
    def _paid_orders_qs():
        from orders.models import Order

        return Order.objects.filter(payment_status="paid").exclude(
            status__in=["cancelled", "refunded"]
        )

    @staticmethod
    def _paid_order_items_qs():
        from orders.models import OrderItem

        return OrderItem.objects.filter(order__payment_status="paid").exclude(
            order__status__in=["cancelled", "refunded"]
        )

    # ------------------------------------------------------------------ #
    #  Helper: convert date range to timezone-aware datetimes
    # ------------------------------------------------------------------ #
    @staticmethod
    def _date_to_aware_dt(d, end_of_day=False):
        """Convert a date object to a timezone-aware datetime."""
        if end_of_day:
            dt = datetime.combine(d, datetime.max.time())
        else:
            dt = datetime.combine(d, datetime.min.time())
        return timezone.make_aware(dt)

    # ------------------------------------------------------------------ #
    #  Existing: get_sales_kpi  (enhanced with optional date range)
    # ------------------------------------------------------------------ #
    @classmethod
    def get_sales_kpi(cls, period: str = "today", start_date=None, end_date=None) -> dict:
        """
        Get sales KPIs for a specified period or explicit date range.

        Args:
            period: One of 'today', '7_days', '30_days' (used when dates not provided)
            start_date: Optional datetime or date for range start
            end_date: Optional datetime or date for range end

        Returns:
            dict with total_sales, currency, order_count, average_order_value
        """
        now = timezone.now()

        if start_date and end_date:
            # Use explicit date range
            if isinstance(start_date, date) and not isinstance(start_date, datetime):
                start_date = cls._date_to_aware_dt(start_date)
            if isinstance(end_date, date) and not isinstance(end_date, datetime):
                end_date = cls._date_to_aware_dt(end_date, end_of_day=True)
        else:
            # Period-based calculation
            if period == "today":
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif period == "7_days":
                start_date = now - timedelta(days=7)
            elif period == "30_days":
                start_date = now - timedelta(days=30)
            else:
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = None

        currency = get_default_currency()

        # Query paid orders (exclude cancelled, refunded)
        orders = cls._paid_orders_qs().filter(created_at__gte=start_date)
        if end_date:
            orders = orders.filter(created_at__lte=end_date)

        # Aggregate sales data
        aggregates = orders.aggregate(
            total_sales=Coalesce(
                Sum("total_amount_base", output_field=DecimalField()),
                Sum("total_amount", output_field=DecimalField()),
                Value(Decimal("0.00"), output_field=DecimalField()),
            ),
            order_count=Count("id"),
            avg_order=Coalesce(
                Avg("total_amount_base", output_field=DecimalField()),
                Avg("total_amount", output_field=DecimalField()),
                Value(Decimal("0.00"), output_field=DecimalField()),
            ),
        )

        return {
            "total_sales": aggregates["total_sales"],
            "currency": currency,
            "order_count": aggregates["order_count"],
            "average_order_value": aggregates["avg_order"],
            "period": period,
        }

    # ------------------------------------------------------------------ #
    #  Existing: get_top_products
    # ------------------------------------------------------------------ #
    @classmethod
    def get_top_products(cls, period: str = "today", limit: int = 5) -> list:
        """
        Get top selling products for a specified period.

        Args:
            period: One of 'today', '7_days'
            limit: Maximum number of products to return

        Returns:
            List of dicts with product_id, product_name, sku, units_sold, revenue
        """
        now = timezone.now()

        if period == "today":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "7_days":
            start_date = now - timedelta(days=7)
        else:
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)

        currency = get_default_currency()

        # Query order items from paid orders
        top_products = (
            cls._paid_order_items_qs()
            .filter(
                order__created_at__gte=start_date,
            )
            .values("product_id", "product_name", "sku")
            .annotate(
                units_sold=Sum("quantity"),
                revenue=Coalesce(
                    Sum("total_price_base", output_field=DecimalField()),
                    Sum("total_price", output_field=DecimalField()),
                    Value(Decimal("0.00"), output_field=DecimalField()),
                ),
            )
            .order_by("-units_sold")[:limit]
        )

        return [
            {
                "product_id": item["product_id"],
                "product_name": item["product_name"],
                "sku": item["sku"],
                "units_sold": item["units_sold"],
                "revenue": item["revenue"] or Decimal("0.00"),
                "currency": currency,
            }
            for item in top_products
        ]

    # ------------------------------------------------------------------ #
    #  Existing: get_order_status_breakdown
    # ------------------------------------------------------------------ #
    @classmethod
    def get_order_status_breakdown(cls) -> list:
        """
        Get breakdown of orders by status.

        Returns:
            List of dicts with status, status_display, count
        """
        from orders.models import Order

        status_display_map = dict(Order.STATUS_CHOICES)

        breakdown = Order.objects.values("status").annotate(count=Count("id")).order_by("status")

        return [
            {
                "status": item["status"],
                "status_display": status_display_map.get(item["status"], item["status"].title()),
                "count": item["count"],
            }
            for item in breakdown
        ]

    # ------------------------------------------------------------------ #
    #  Existing: get_pending_orders_count
    # ------------------------------------------------------------------ #
    @classmethod
    def get_pending_orders_count(cls) -> int:
        """Get count of orders awaiting action (pending, processing)."""
        from orders.models import Order

        return Order.objects.filter(status__in=["pending", "processing"]).count()

    # ------------------------------------------------------------------ #
    #  Existing: get_low_stock_count
    # ------------------------------------------------------------------ #
    @classmethod
    def get_low_stock_count(cls, threshold: int = None) -> int:
        """
        Get count of products with low stock.

        Uses StockItem aggregation to calculate available stock
        and compares against each product's low_stock_threshold.

        Args:
            threshold: Optional override for low stock threshold.
                      If not provided, uses each product's low_stock_threshold.

        Returns:
            Count of products at or below threshold
        """
        from catalog.models import Product

        # Build queryset for published products that track inventory
        products = Product.objects.filter(status="published", track_inventory=True).annotate(
            available_stock=Coalesce(
                Sum(F("stock_items__on_hand") - F("stock_items__allocated")),
                0,
                output_field=IntegerField(),
            )
        )

        # Filter by low stock - use product's own threshold or provided threshold
        if threshold is not None:
            low_stock_products = products.filter(available_stock__lte=threshold)
        else:
            # Use each product's individual low_stock_threshold
            low_stock_products = products.filter(available_stock__lte=F("low_stock_threshold"))

        return low_stock_products.count()

    # ------------------------------------------------------------------ #
    #  Existing: get_dashboard_analytics  (enhanced with optional dates)
    # ------------------------------------------------------------------ #
    @classmethod
    def get_dashboard_analytics(cls, start_date=None, end_date=None) -> dict:
        """
        Get complete dashboard analytics data.

        Args:
            start_date: Optional date for custom range start
            end_date: Optional date for custom range end

        Returns:
            dict with all analytics data for the dashboard
        """
        if start_date and end_date:
            custom_kpi = cls.get_sales_kpi(
                period="custom", start_date=start_date, end_date=end_date
            )
            return {
                "custom_range": custom_kpi,
                "today": cls.get_sales_kpi("today"),
                "last_7_days": cls.get_sales_kpi("7_days"),
                "last_30_days": cls.get_sales_kpi("30_days"),
                "top_products_today": cls.get_top_products("today", 5),
                "top_products_7_days": cls.get_top_products("7_days", 5),
                "order_status_breakdown": cls.get_order_status_breakdown(),
                "pending_orders_count": cls.get_pending_orders_count(),
                "low_stock_count": cls.get_low_stock_count(),
            }

        return {
            "today": cls.get_sales_kpi("today"),
            "last_7_days": cls.get_sales_kpi("7_days"),
            "last_30_days": cls.get_sales_kpi("30_days"),
            "top_products_today": cls.get_top_products("today", 5),
            "top_products_7_days": cls.get_top_products("7_days", 5),
            "order_status_breakdown": cls.get_order_status_breakdown(),
            "pending_orders_count": cls.get_pending_orders_count(),
            "low_stock_count": cls.get_low_stock_count(),
        }

    # ------------------------------------------------------------------ #
    #  Existing: get_quick_stats
    # ------------------------------------------------------------------ #
    @classmethod
    def get_quick_stats(cls) -> dict:
        """
        Get quick stats for dashboard header.

        Returns:
            dict with today_sales, today_orders, pending_orders, low_stock_items
        """
        today_kpi = cls.get_sales_kpi("today")
        currency = get_default_currency()

        return {
            "today_sales": today_kpi["total_sales"],
            "today_orders": today_kpi["order_count"],
            "pending_orders": cls.get_pending_orders_count(),
            "low_stock_items": cls.get_low_stock_count(),
            "currency": currency,
        }

    # ------------------------------------------------------------------ #
    #  Existing: get_daily_stats
    # ------------------------------------------------------------------ #
    @classmethod
    def get_daily_stats(cls, period: str = "7_days") -> dict:
        """
        Get per-day breakdown of revenue and order counts.

        Args:
            period: One of '7_days', '30_days', '90_days'

        Returns:
            dict with period, currency, start_date, end_date, days list
        """
        now = timezone.now()
        today = now.date()

        if period == "90_days":
            num_days = 90
        elif period == "30_days":
            num_days = 30
        else:
            num_days = 7

        start_date = today - timedelta(days=num_days - 1)
        start_dt = cls._date_to_aware_dt(start_date)

        currency = get_default_currency()

        # Query daily aggregates for paid, non-cancelled orders
        daily_data = (
            cls._paid_orders_qs()
            .filter(
                created_at__gte=start_dt,
            )
            .annotate(order_date=TruncDate("created_at"))
            .values("order_date")
            .annotate(
                revenue=Coalesce(
                    Sum("total_amount_base", output_field=DecimalField()),
                    Sum("total_amount", output_field=DecimalField()),
                    Value(Decimal("0.00"), output_field=DecimalField()),
                ),
                order_count=Count("id"),
                avg_order=Coalesce(
                    Avg("total_amount_base", output_field=DecimalField()),
                    Avg("total_amount", output_field=DecimalField()),
                    Value(Decimal("0.00"), output_field=DecimalField()),
                ),
            )
            .order_by("order_date")
        )

        # Build lookup from DB results
        daily_lookup = {row["order_date"]: row for row in daily_data}

        # Fill in all dates (including zero-order days)
        days = []
        for i in range(num_days):
            d = start_date + timedelta(days=i)
            row = daily_lookup.get(d)
            days.append(
                {
                    "date": d,
                    "revenue": row["revenue"] if row else Decimal("0.00"),
                    "order_count": row["order_count"] if row else 0,
                    "average_order_value": row["avg_order"] if row else Decimal("0.00"),
                }
            )

        return {
            "period": period,
            "currency": currency,
            "start_date": start_date,
            "end_date": today,
            "days": days,
        }

    # ------------------------------------------------------------------ #
    #  Existing: get_sales_comparison  (enhanced with explicit dates)
    # ------------------------------------------------------------------ #
    @classmethod
    def get_sales_comparison(
        cls,
        period: str = "today",
        start_date=None,
        end_date=None,
        compare_start_date=None,
        compare_end_date=None,
    ) -> dict:
        """
        Get sales comparison with previous period.

        When explicit dates are provided they override the period-based logic.
        Also returns a daily_breakdown array for chart rendering.

        Args:
            period: 'today' compares with yesterday, '7_days' with previous 7 days
            start_date: Explicit start of current period (date or datetime)
            end_date: Explicit end of current period (date or datetime)
            compare_start_date: Explicit start of comparison period
            compare_end_date: Explicit end of comparison period

        Returns:
            dict with current_value, previous_value, change_percentage, trend,
            currency, daily_breakdown
        """
        now = timezone.now()

        if start_date and end_date:
            # Explicit date range mode
            if isinstance(start_date, date) and not isinstance(start_date, datetime):
                current_start = cls._date_to_aware_dt(start_date)
            else:
                current_start = start_date
            if isinstance(end_date, date) and not isinstance(end_date, datetime):
                current_end = cls._date_to_aware_dt(end_date, end_of_day=True)
            else:
                current_end = end_date

            if compare_start_date and compare_end_date:
                if isinstance(compare_start_date, date) and not isinstance(
                    compare_start_date, datetime
                ):
                    previous_start = cls._date_to_aware_dt(compare_start_date)
                else:
                    previous_start = compare_start_date
                if isinstance(compare_end_date, date) and not isinstance(
                    compare_end_date, datetime
                ):
                    previous_end = cls._date_to_aware_dt(compare_end_date, end_of_day=True)
                else:
                    previous_end = compare_end_date
            else:
                # Auto-calculate comparison period of same length
                delta = current_end - current_start
                previous_end = current_start - timedelta(seconds=1)
                previous_start = previous_end - delta
        else:
            # Period-based calculation (original logic)
            if period == "today":
                current_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
                current_end = now
                previous_start = current_start - timedelta(days=1)
                previous_end = current_start
            else:  # 7_days
                current_start = now - timedelta(days=7)
                current_end = now
                previous_start = current_start - timedelta(days=7)
                previous_end = current_start

        currency = get_default_currency()
        base_qs = cls._paid_orders_qs()

        # Current period sales
        current_qs = base_qs.filter(created_at__gte=current_start)
        if current_end:
            current_qs = current_qs.filter(created_at__lte=current_end)
        current_sales = current_qs.aggregate(
            total=Coalesce(
                Sum("total_amount_base", output_field=DecimalField()),
                Sum("total_amount", output_field=DecimalField()),
                Value(Decimal("0.00"), output_field=DecimalField()),
            ),
            count=Count("id"),
        )

        # Previous period sales
        previous_sales_agg = base_qs.filter(
            created_at__gte=previous_start, created_at__lt=previous_end
        ).aggregate(
            total=Coalesce(
                Sum("total_amount_base", output_field=DecimalField()),
                Sum("total_amount", output_field=DecimalField()),
                Value(Decimal("0.00"), output_field=DecimalField()),
            ),
            count=Count("id"),
        )

        current_total = current_sales["total"]
        previous_total = previous_sales_agg["total"]

        # Calculate change percentage
        if previous_total and previous_total > 0:
            change = ((current_total - previous_total) / previous_total) * 100
        else:
            change = None

        # Determine trend
        if change is None:
            trend = "stable"
        elif change > 0:
            trend = "up"
        elif change < 0:
            trend = "down"
        else:
            trend = "stable"

        # Build daily breakdown for chart rendering
        daily_breakdown = cls._build_daily_breakdown(
            current_start, current_end or now, previous_start, previous_end
        )

        return {
            "current_value": current_total,
            "previous_value": previous_total,
            "current_order_count": current_sales["count"],
            "previous_order_count": previous_sales_agg["count"],
            "change_percentage": change,
            "trend": trend,
            "currency": currency,
            "daily_breakdown": daily_breakdown,
        }

    @classmethod
    def _build_daily_breakdown(cls, current_start, current_end, previous_start, previous_end):
        """Build per-day arrays for current and previous periods."""
        base_qs = cls._paid_orders_qs()

        def _get_daily(qs_start, qs_end):
            daily = (
                base_qs.filter(
                    created_at__gte=qs_start,
                    created_at__lte=qs_end,
                )
                .annotate(order_date=TruncDate("created_at"))
                .values("order_date")
                .annotate(
                    revenue=Coalesce(
                        Sum("total_amount_base", output_field=DecimalField()),
                        Value(Decimal("0.00"), output_field=DecimalField()),
                    ),
                    order_count=Count("id"),
                )
                .order_by("order_date")
            )

            lookup = {row["order_date"]: row for row in daily}

            start_d = qs_start.date() if isinstance(qs_start, datetime) else qs_start
            end_d = qs_end.date() if isinstance(qs_end, datetime) else qs_end
            num_days = (end_d - start_d).days + 1

            result = []
            for i in range(num_days):
                d = start_d + timedelta(days=i)
                row = lookup.get(d)
                result.append(
                    {
                        "date": d,
                        "revenue": row["revenue"] if row else Decimal("0.00"),
                        "order_count": row["order_count"] if row else 0,
                    }
                )
            return result

        return {
            "current": _get_daily(current_start, current_end),
            "previous": _get_daily(previous_start, previous_end),
        }

    # ================================================================== #
    #  NEW: Product Analytics
    # ================================================================== #
    @classmethod
    def get_product_analytics(
        cls,
        start_date,
        end_date,
        category_id=None,
        brand_id=None,
        search=None,
        ordering="-revenue",
        page=1,
        page_size=20,
    ) -> dict:
        """
        Get product-level performance analytics for a date range.

        Returns:
            dict with summary, products list, and pagination
        """
        from catalog.models import Product
        from orders.models import OrderItem, Refund

        currency = get_default_currency()
        start_dt = cls._date_to_aware_dt(start_date)
        end_dt = cls._date_to_aware_dt(end_date, end_of_day=True)

        # Base queryset: order items from paid, non-cancelled orders in date range
        items_qs = cls._paid_order_items_qs().filter(
            order__created_at__gte=start_dt,
            order__created_at__lte=end_dt,
        )

        # Optional filters on the product relation
        if category_id:
            items_qs = items_qs.filter(product__category_id=category_id)
        if brand_id:
            items_qs = items_qs.filter(product__brand_id=brand_id)
        if search:
            items_qs = items_qs.filter(Q(product_name__icontains=search) | Q(sku__icontains=search))

        # Aggregate by product
        product_stats = items_qs.values(
            "product_id",
            "product_name",
            "sku",
        ).annotate(
            units_sold=Coalesce(Sum("quantity"), Value(0), output_field=IntegerField()),
            revenue=Coalesce(
                Sum("total_price_base", output_field=DecimalField()),
                Value(Decimal("0.00"), output_field=DecimalField()),
            ),
            orders_count=Count("order_id", distinct=True),
        )

        # Get refund counts per product for the period
        # Refund items_json stores order_item_id references; we count refunds
        # linked to orders that contain each product
        refund_counts = {}
        refunds_in_range = Refund.objects.filter(
            order__created_at__gte=start_dt,
            order__created_at__lte=end_dt,
            status__in=["approved", "processing", "completed"],
        ).select_related("order")
        for refund in refunds_in_range:
            for item_data in refund.items_json or []:
                oi_id = item_data.get("order_item_id")
                if oi_id:
                    try:
                        oi = OrderItem.objects.only("product_id").get(pk=oi_id)
                        refund_counts[oi.product_id] = refund_counts.get(oi.product_id, 0) + 1
                    except OrderItem.DoesNotExist:
                        pass

        # Ordering
        allowed_orderings = {
            "revenue",
            "-revenue",
            "units_sold",
            "-units_sold",
            "orders_count",
            "-orders_count",
            "product_name",
            "-product_name",
        }
        if ordering not in allowed_orderings:
            ordering = "-revenue"
        product_stats = product_stats.order_by(ordering)

        # Summary aggregates (before pagination)
        total_count = product_stats.count()
        summary_agg = items_qs.aggregate(
            total_revenue=Coalesce(
                Sum("total_price_base", output_field=DecimalField()),
                Value(Decimal("0.00"), output_field=DecimalField()),
            ),
            total_units=Coalesce(Sum("quantity"), Value(0), output_field=IntegerField()),
            total_products_sold=Count("product_id", distinct=True),
        )

        # Pagination
        total_pages = math.ceil(total_count / page_size) if total_count > 0 else 1
        offset = (page - 1) * page_size
        page_data = list(product_stats[offset : offset + page_size])

        # Enrich with image URL, category, brand, return info
        product_ids = [p["product_id"] for p in page_data]
        products_map = {}
        if product_ids:
            products_qs = (
                Product.objects.filter(id__in=product_ids)
                .select_related("category", "brand")
                .prefetch_related("images")
            )
            for p in products_qs:
                primary_img = p.images.filter(is_primary=True).first()
                products_map[p.id] = {
                    "category_name": p.category.name if p.category else "",
                    "brand_name": p.brand.name if p.brand else "",
                    "image_url": primary_img.image_url if primary_img else None,
                }

        products = []
        for item in page_data:
            pid = item["product_id"]
            extra = products_map.get(pid, {})
            units = item["units_sold"] or 0
            rev = item["revenue"] or Decimal("0.00")
            returns = refund_counts.get(pid, 0)
            return_rate = (
                (Decimal(returns) / Decimal(units) * 100) if units > 0 else Decimal("0.00")
            )
            avg_price = (rev / Decimal(units)) if units > 0 else Decimal("0.00")

            products.append(
                {
                    "product_id": pid,
                    "product_name": item["product_name"],
                    "sku": item["sku"],
                    "image_url": extra.get("image_url"),
                    "category_name": extra.get("category_name", ""),
                    "brand_name": extra.get("brand_name", ""),
                    "units_sold": units,
                    "revenue": rev,
                    "orders_count": item["orders_count"],
                    "returns_count": returns,
                    "return_rate": round(return_rate, 2),
                    "average_selling_price": round(avg_price, 2),
                }
            )

        return {
            "currency": currency,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "summary": {
                "total_revenue": summary_agg["total_revenue"],
                "total_units": summary_agg["total_units"],
                "total_products_sold": summary_agg["total_products_sold"],
            },
            "results": products,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": total_pages,
            },
        }

    # ================================================================== #
    #  NEW: Customer Analytics
    # ================================================================== #
    @classmethod
    def get_customer_analytics(
        cls,
        start_date,
        end_date,
        segment=None,
        ordering="-total_spent",
        page=1,
        page_size=20,
    ) -> dict:
        """
        Get customer analytics for a date range.

        Args:
            start_date: date object
            end_date: date object
            segment: Optional 'new', 'returning', or None for all
            ordering: Sort field for top customers list
            page: Page number
            page_size: Items per page

        Returns:
            dict with summary, geo_breakdown, ltv_distribution, top_customers, pagination
        """
        from django.contrib.auth import get_user_model

        User = get_user_model()

        currency = get_default_currency()
        start_dt = cls._date_to_aware_dt(start_date)
        end_dt = cls._date_to_aware_dt(end_date, end_of_day=True)

        base_qs = cls._paid_orders_qs()

        # Orders in date range
        range_orders = base_qs.filter(
            created_at__gte=start_dt,
            created_at__lte=end_dt,
        )

        # Customers who ordered in the range (exclude guest orders)
        range_customer_ids = set(
            range_orders.filter(user__isnull=False).values_list("user_id", flat=True).distinct()
        )

        # New customers: first-ever paid order is within date range
        # Determine each user's first order date
        first_order_subquery = (
            base_qs.filter(user_id=OuterRef("pk")).order_by("created_at").values("created_at")[:1]
        )

        users_with_first_order = User.objects.filter(id__in=range_customer_ids).annotate(
            first_order_date=Subquery(first_order_subquery)
        )

        new_customer_ids = set(
            users_with_first_order.filter(
                first_order_date__gte=start_dt,
                first_order_date__lte=end_dt,
            ).values_list("id", flat=True)
        )
        returning_customer_ids = range_customer_ids - new_customer_ids

        total_customers = len(range_customer_ids)
        new_customers = len(new_customer_ids)
        returning_customers = len(returning_customer_ids)

        # Average LTV (lifetime total spent by customers who ordered in range)
        ltv_data = (
            base_qs.filter(user_id__in=range_customer_ids)
            .values("user_id")
            .annotate(
                lifetime_spent=Coalesce(
                    Sum("total_amount_base", output_field=DecimalField()),
                    Value(Decimal("0.00"), output_field=DecimalField()),
                ),
                lifetime_orders=Count("id"),
            )
        )
        ltv_lookup = {row["user_id"]: row for row in ltv_data}

        ltv_values = [row["lifetime_spent"] for row in ltv_data]
        avg_ltv = sum(ltv_values) / Decimal(len(ltv_values)) if ltv_values else Decimal("0.00")
        order_counts = [row["lifetime_orders"] for row in ltv_data]
        avg_orders = sum(order_counts) / len(order_counts) if order_counts else 0

        # Geo breakdown from shipping_country on orders in range
        geo_data = (
            range_orders.filter(shipping_country__gt="")
            .values("shipping_country")
            .annotate(
                order_count=Count("id"),
                revenue=Coalesce(
                    Sum("total_amount_base", output_field=DecimalField()),
                    Value(Decimal("0.00"), output_field=DecimalField()),
                ),
                customer_count=Count("user_id", distinct=True),
            )
            .order_by("-revenue")
        )

        geo_breakdown = [
            {
                "country": row["shipping_country"],
                "order_count": row["order_count"],
                "revenue": row["revenue"],
                "customer_count": row["customer_count"],
            }
            for row in geo_data
        ]

        # LTV distribution buckets
        ltv_buckets = [
            {"label": "$0 - $50", "min": Decimal("0"), "max": Decimal("50"), "count": 0},
            {"label": "$50 - $100", "min": Decimal("50"), "max": Decimal("100"), "count": 0},
            {"label": "$100 - $250", "min": Decimal("100"), "max": Decimal("250"), "count": 0},
            {"label": "$250 - $500", "min": Decimal("250"), "max": Decimal("500"), "count": 0},
            {"label": "$500 - $1000", "min": Decimal("500"), "max": Decimal("1000"), "count": 0},
            {"label": "$1000+", "min": Decimal("1000"), "max": None, "count": 0},
        ]
        for ltv_val in ltv_values:
            for bucket in ltv_buckets:
                if bucket["max"] is None:
                    if ltv_val >= bucket["min"]:
                        bucket["count"] += 1
                        break
                elif bucket["min"] <= ltv_val < bucket["max"]:
                    bucket["count"] += 1
                    break
        ltv_distribution = [{"label": b["label"], "count": b["count"]} for b in ltv_buckets]

        # Top customers list with segment filtering and pagination
        # Build list from ltv_lookup, filter by segment
        if segment == "new":
            target_ids = new_customer_ids
        elif segment == "returning":
            target_ids = returning_customer_ids
        else:
            target_ids = range_customer_ids

        # Get per-range stats for top customers
        range_stats = (
            base_qs.filter(
                user_id__in=target_ids,
                created_at__gte=start_dt,
                created_at__lte=end_dt,
            )
            .values("user_id")
            .annotate(
                range_spent=Coalesce(
                    Sum("total_amount_base", output_field=DecimalField()),
                    Value(Decimal("0.00"), output_field=DecimalField()),
                ),
                range_orders=Count("id"),
            )
        )
        range_stats_lookup = {row["user_id"]: row for row in range_stats}

        # Build customer records
        customer_records = []
        users_map = {}
        if target_ids:
            for u in User.objects.filter(id__in=target_ids).only(
                "id", "first_name", "last_name", "email", "date_joined"
            ):
                users_map[u.id] = u

        for uid in target_ids:
            user = users_map.get(uid)
            if not user:
                continue
            ltv_info = ltv_lookup.get(uid, {})
            range_info = range_stats_lookup.get(uid, {})
            customer_records.append(
                {
                    "user_id": uid,
                    "name": f"{user.first_name} {user.last_name}".strip() or user.email,
                    "email": user.email,
                    "segment": "new" if uid in new_customer_ids else "returning",
                    "total_spent": ltv_info.get("lifetime_spent", Decimal("0.00")),
                    "total_orders": ltv_info.get("lifetime_orders", 0),
                    "range_spent": range_info.get("range_spent", Decimal("0.00")),
                    "range_orders": range_info.get("range_orders", 0),
                    "joined": user.date_joined.date().isoformat() if user.date_joined else None,
                }
            )

        # Sort
        allowed_orderings = {
            "total_spent",
            "-total_spent",
            "range_spent",
            "-range_spent",
            "total_orders",
            "-total_orders",
            "range_orders",
            "-range_orders",
            "name",
            "-name",
        }
        if ordering not in allowed_orderings:
            ordering = "-total_spent"
        reverse = ordering.startswith("-")
        sort_key = ordering.lstrip("-")
        customer_records.sort(
            key=lambda x: x.get(sort_key, 0) or 0,
            reverse=reverse,
        )

        # Pagination
        total_count = len(customer_records)
        total_pages = math.ceil(total_count / page_size) if total_count > 0 else 1
        offset = (page - 1) * page_size
        page_customers = customer_records[offset : offset + page_size]

        return {
            "currency": currency,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "summary": {
                "total_customers": total_customers,
                "new_customers": new_customers,
                "returning_customers": returning_customers,
                "average_ltv": round(avg_ltv, 2),
                "average_orders_per_customer": round(avg_orders, 2)
                if isinstance(avg_orders, float)
                else avg_orders,
            },
            "geo_breakdown": geo_breakdown,
            "ltv_distribution": ltv_distribution,
            "top_customers": page_customers,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": total_pages,
            },
        }

    # ================================================================== #
    #  NEW: Category Analytics
    # ================================================================== #
    @classmethod
    def get_category_analytics(cls, start_date, end_date, ordering="-revenue") -> dict:
        """
        Get revenue per category from OrderItem -> product__category.

        Args:
            start_date: date object
            end_date: date object
            ordering: Sort field ('-revenue', '-units_sold', '-orders_count', 'name')

        Returns:
            dict with currency, categories list, summary
        """
        currency = get_default_currency()
        start_dt = cls._date_to_aware_dt(start_date)
        end_dt = cls._date_to_aware_dt(end_date, end_of_day=True)

        items_qs = cls._paid_order_items_qs().filter(
            order__created_at__gte=start_dt,
            order__created_at__lte=end_dt,
        )

        category_stats = items_qs.values(
            "product__category__id",
            "product__category__name",
        ).annotate(
            revenue=Coalesce(
                Sum("total_price_base", output_field=DecimalField()),
                Value(Decimal("0.00"), output_field=DecimalField()),
            ),
            units_sold=Coalesce(Sum("quantity"), Value(0), output_field=IntegerField()),
            orders_count=Count("order_id", distinct=True),
            products_count=Count("product_id", distinct=True),
        )

        # Ordering
        order_map = {
            "-revenue": "-revenue",
            "revenue": "revenue",
            "-units_sold": "-units_sold",
            "units_sold": "units_sold",
            "-orders_count": "-orders_count",
            "orders_count": "orders_count",
            "name": "product__category__name",
            "-name": "-product__category__name",
        }
        db_ordering = order_map.get(ordering, "-revenue")
        category_stats = category_stats.order_by(db_ordering)

        # Calculate total for percentage
        total_revenue = sum((row["revenue"] or Decimal("0.00")) for row in category_stats)

        categories = []
        for row in category_stats:
            rev = row["revenue"] or Decimal("0.00")
            pct = (rev / total_revenue * 100) if total_revenue > 0 else Decimal("0.00")
            categories.append(
                {
                    "category_id": row["product__category__id"],
                    "category_name": row["product__category__name"] or "Uncategorized",
                    "revenue": rev,
                    "units_sold": row["units_sold"],
                    "orders_count": row["orders_count"],
                    "products_count": row["products_count"],
                    "revenue_percentage": round(pct, 2),
                }
            )

        summary_agg = items_qs.aggregate(
            total_revenue=Coalesce(
                Sum("total_price_base", output_field=DecimalField()),
                Value(Decimal("0.00"), output_field=DecimalField()),
            ),
            total_units=Coalesce(Sum("quantity"), Value(0), output_field=IntegerField()),
            total_categories=Count("product__category__id", distinct=True),
        )

        return {
            "currency": currency,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "summary": {
                "total_revenue": summary_agg["total_revenue"],
                "total_units": summary_agg["total_units"],
                "total_categories": summary_agg["total_categories"],
            },
            "categories": categories,
        }

    # ================================================================== #
    #  NEW: Brand Analytics
    # ================================================================== #
    @classmethod
    def get_brand_analytics(cls, start_date, end_date, ordering="-revenue") -> dict:
        """
        Get revenue per brand from OrderItem -> product__brand.

        Args:
            start_date: date object
            end_date: date object
            ordering: Sort field

        Returns:
            dict with currency, brands list, summary
        """
        currency = get_default_currency()
        start_dt = cls._date_to_aware_dt(start_date)
        end_dt = cls._date_to_aware_dt(end_date, end_of_day=True)

        items_qs = cls._paid_order_items_qs().filter(
            order__created_at__gte=start_dt,
            order__created_at__lte=end_dt,
        )

        brand_stats = items_qs.values(
            "product__brand__id",
            "product__brand__name",
        ).annotate(
            revenue=Coalesce(
                Sum("total_price_base", output_field=DecimalField()),
                Value(Decimal("0.00"), output_field=DecimalField()),
            ),
            units_sold=Coalesce(Sum("quantity"), Value(0), output_field=IntegerField()),
            orders_count=Count("order_id", distinct=True),
            products_count=Count("product_id", distinct=True),
        )

        # Ordering
        order_map = {
            "-revenue": "-revenue",
            "revenue": "revenue",
            "-units_sold": "-units_sold",
            "units_sold": "units_sold",
            "-orders_count": "-orders_count",
            "orders_count": "orders_count",
            "name": "product__brand__name",
            "-name": "-product__brand__name",
        }
        db_ordering = order_map.get(ordering, "-revenue")
        brand_stats = brand_stats.order_by(db_ordering)

        # Calculate total for percentage
        total_revenue = sum((row["revenue"] or Decimal("0.00")) for row in brand_stats)

        brands = []
        for row in brand_stats:
            rev = row["revenue"] or Decimal("0.00")
            pct = (rev / total_revenue * 100) if total_revenue > 0 else Decimal("0.00")
            brands.append(
                {
                    "brand_id": row["product__brand__id"],
                    "brand_name": row["product__brand__name"] or "No Brand",
                    "revenue": rev,
                    "units_sold": row["units_sold"],
                    "orders_count": row["orders_count"],
                    "products_count": row["products_count"],
                    "revenue_percentage": round(pct, 2),
                }
            )

        summary_agg = items_qs.aggregate(
            total_revenue=Coalesce(
                Sum("total_price_base", output_field=DecimalField()),
                Value(Decimal("0.00"), output_field=DecimalField()),
            ),
            total_units=Coalesce(Sum("quantity"), Value(0), output_field=IntegerField()),
            total_brands=Count("product__brand__id", distinct=True),
        )

        return {
            "currency": currency,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "summary": {
                "total_revenue": summary_agg["total_revenue"],
                "total_units": summary_agg["total_units"],
                "total_brands": summary_agg["total_brands"],
            },
            "brands": brands,
        }

    # ------------------------------------------------------------------ #
    #  Hourly sales breakdown for a single date
    # ------------------------------------------------------------------ #
    @classmethod
    def get_hourly_sales(cls, target_date: date) -> dict:
        """
        Get per-hour revenue and order counts for a single date.

        Uses total_amount_base (pre-converted to store default currency)
        so multi-currency orders are rolled up correctly.

        Args:
            target_date: The date to break down by hour.

        Returns:
            dict with date, currency, and hours list (0-23).
        """
        start_dt = cls._date_to_aware_dt(target_date)
        end_dt = cls._date_to_aware_dt(target_date, end_of_day=True)
        currency = get_default_currency()

        hourly_data = (
            cls._paid_orders_qs()
            .filter(
                created_at__gte=start_dt,
                created_at__lte=end_dt,
            )
            .annotate(hour=ExtractHour("created_at"))
            .values("hour")
            .annotate(
                revenue=Coalesce(
                    Sum("total_amount_base", output_field=DecimalField()),
                    Sum("total_amount", output_field=DecimalField()),
                    Value(Decimal("0.00"), output_field=DecimalField()),
                ),
                order_count=Count("id"),
            )
            .order_by("hour")
        )

        hourly_lookup = {row["hour"]: row for row in hourly_data}

        hours = []
        for h in range(24):
            row = hourly_lookup.get(h)
            hours.append(
                {
                    "hour": h,
                    "revenue": row["revenue"] if row else Decimal("0.00"),
                    "order_count": row["order_count"] if row else 0,
                }
            )

        return {
            "date": target_date,
            "currency": currency,
            "hours": hours,
        }
