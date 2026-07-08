"""
Shop Analytics Service
Provides business metrics and analytics for the Shop Dashboard
"""
from django.db.models import Sum, Count, Avg, F, Q, Value, CharField, DecimalField
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth, Coalesce
from django.utils import timezone
from django.core.cache import cache
from datetime import timedelta, datetime
from decimal import Decimal
from typing import Dict, List, Tuple, Optional
from djmoney.models.fields import MoneyField


class ShopAnalyticsService:
    """
    Service for calculating shop analytics and metrics
    All monetary values are returned as Decimal for precision
    """

    CACHE_TIMEOUT = 900  # 15 minutes

    @staticmethod
    def _base_sum(field='total_amount'):
        """Sum using base-currency field with fallback to raw amount for mixed-currency reporting."""
        return Coalesce(
            Sum(f'{field}_base', output_field=DecimalField()),
            Sum(field, output_field=DecimalField()),
            Value(0, output_field=DecimalField())
        )

    @staticmethod
    def _base_avg(field='total_amount'):
        """Avg using base-currency field with fallback to raw amount for mixed-currency reporting."""
        return Coalesce(
            Avg(f'{field}_base', output_field=DecimalField()),
            Avg(field, output_field=DecimalField()),
            Value(0, output_field=DecimalField())
        )

    @staticmethod
    def get_date_range_for_period(period: str, custom_start: Optional[datetime] = None,
                                  custom_end: Optional[datetime] = None) -> Tuple[datetime, datetime]:
        """
        Get start and end dates for a given period

        Args:
            period: One of 'today', 'yesterday', 'last_7_days', 'last_30_days',
                   'this_month', 'last_month', 'this_quarter', 'last_quarter',
                   'this_year', 'last_year', 'custom'
            custom_start: Start date for custom range
            custom_end: End date for custom range

        Returns:
            Tuple of (start_date, end_date)
        """
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        if period == 'today':
            return today_start, now

        elif period == 'yesterday':
            yesterday = today_start - timedelta(days=1)
            return yesterday, today_start

        elif period == 'last_7_days':
            start = today_start - timedelta(days=7)
            return start, now

        elif period == 'last_30_days':
            start = today_start - timedelta(days=30)
            return start, now

        elif period == 'this_month':
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            return start, now

        elif period == 'last_month':
            first_of_this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            last_day_of_last_month = first_of_this_month - timedelta(days=1)
            first_of_last_month = last_day_of_last_month.replace(day=1)
            return first_of_last_month, first_of_this_month

        elif period == 'this_quarter':
            quarter = (now.month - 1) // 3
            start = now.replace(month=quarter * 3 + 1, day=1, hour=0, minute=0, second=0, microsecond=0)
            return start, now

        elif period == 'last_quarter':
            quarter = (now.month - 1) // 3
            if quarter == 0:
                # Last quarter of previous year
                start = now.replace(year=now.year - 1, month=10, day=1, hour=0, minute=0, second=0, microsecond=0)
                end = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            else:
                start = now.replace(month=(quarter - 1) * 3 + 1, day=1, hour=0, minute=0, second=0, microsecond=0)
                end = now.replace(month=quarter * 3 + 1, day=1, hour=0, minute=0, second=0, microsecond=0)
            return start, end

        elif period == 'this_year':
            start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            return start, now

        elif period == 'last_year':
            start = now.replace(year=now.year - 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            return start, end

        elif period == 'custom':
            if custom_start and custom_end:
                return custom_start, custom_end
            raise ValueError("Custom period requires custom_start and custom_end parameters")

        else:
            raise ValueError(f"Invalid period: {period}")

    @staticmethod
    def get_previous_period(start_date: datetime, end_date: datetime) -> Tuple[datetime, datetime]:
        """
        Calculate the previous period for comparison

        Args:
            start_date: Current period start
            end_date: Current period end

        Returns:
            Tuple of (previous_start, previous_end)
        """
        duration = end_date - start_date
        previous_end = start_date
        previous_start = start_date - duration
        return previous_start, previous_end

    @staticmethod
    def calculate_percentage_change(current: Decimal, previous: Decimal) -> Optional[float]:
        """
        Calculate percentage change between two values

        Returns:
            Percentage change as float, or None if previous is 0
        """
        if previous == 0 or previous is None:
            return None
        return float(((current - previous) / previous) * 100)

    @classmethod
    def get_action_cards(cls) -> Dict:
        """
        Get action cards data (not time-filtered)
        These represent items requiring immediate attention

        Returns:
            Dict with counts for various action items
        """
        cache_key = 'shop_dashboard_action_cards'
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        from orders.models import Order
        from cart.models import Cart
        from catalog.models import Product, ProductReview
        from customers.models import AbandonedCart
        from component_updates.models import ComponentRegistry

        data = {
            'incomplete_orders': Order.objects.filter(
                Q(status='pending') | Q(status='processing')
            ).count(),

            'abandoned_carts': AbandonedCart.objects.filter(
                recovered=False
            ).count(),

            # Multi-location inventory: Count products with low stock at any warehouse
            'low_stock_products': Product.objects.filter(
                track_inventory=True,
                stock_items__on_hand__lte=F('stock_items__low_stock_threshold'),
                stock_items__on_hand__gt=F('stock_items__allocated')
            ).distinct().count(),

            # Multi-location inventory: Count products out of stock at all warehouses
            'out_of_stock_products': Product.objects.filter(
                track_inventory=True
            ).exclude(
                stock_items__on_hand__gt=F('stock_items__allocated')
            ).distinct().count(),

            'pending_reviews': ProductReview.objects.filter(
                is_approved=False
            ).count(),

            # Component updates available (not locked)
            'component_updates': ComponentRegistry.objects.filter(
                update_available=True,
                locked=False
            ).count(),
        }

        cache.set(cache_key, data, cls.CACHE_TIMEOUT)
        return data

    @classmethod
    def get_sales_performance(cls, start_date: datetime, end_date: datetime,
                             compare: bool = True) -> Dict:
        """
        Get sales performance metrics

        Args:
            start_date: Start of period
            end_date: End of period
            compare: Whether to include comparison with previous period

        Returns:
            Dict with revenue, orders, AOV, and optional comparison data
        """
        from orders.models import Order

        # Current period metrics
        current_orders = Order.objects.filter(
            created_at__gte=start_date,
            created_at__lt=end_date,
            status__in=['processing', 'shipped', 'delivered']
        )

        current_stats = current_orders.aggregate(
            total_revenue=Coalesce(Sum('total_amount_base', output_field=DecimalField()), Sum('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField())),
            order_count=Count('id'),
            avg_order_value=Coalesce(Avg('total_amount_base', output_field=DecimalField()), Avg('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )

        result = {
            'current': {
                'revenue': current_stats['total_revenue'] or Decimal('0.00'),
                'orders': current_stats['order_count'],
                'aov': current_stats['avg_order_value'] or Decimal('0.00'),
            }
        }

        if compare:
            # Previous period metrics
            prev_start, prev_end = cls.get_previous_period(start_date, end_date)

            prev_orders = Order.objects.filter(
                created_at__gte=prev_start,
                created_at__lt=prev_end,
                status__in=['processing', 'shipped', 'delivered']
            )

            prev_stats = prev_orders.aggregate(
                total_revenue=Coalesce(Sum('total_amount_base', output_field=DecimalField()), Sum('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField())),
                order_count=Count('id'),
                avg_order_value=Coalesce(Avg('total_amount_base', output_field=DecimalField()), Avg('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField()))
            )

            result['previous'] = {
                'revenue': prev_stats['total_revenue'] or Decimal('0.00'),
                'orders': prev_stats['order_count'],
                'aov': prev_stats['avg_order_value'] or Decimal('0.00'),
            }

            # Calculate percentage changes
            result['changes'] = {
                'revenue': cls.calculate_percentage_change(
                    result['current']['revenue'],
                    result['previous']['revenue']
                ),
                'orders': cls.calculate_percentage_change(
                    Decimal(result['current']['orders']),
                    Decimal(result['previous']['orders'])
                ),
                'aov': cls.calculate_percentage_change(
                    result['current']['aov'],
                    result['previous']['aov']
                ),
            }

        return result

    @classmethod
    def get_refund_metrics(cls, start_date: datetime, end_date: datetime,
                          compare: bool = True) -> Dict:
        """
        Get refund analytics metrics

        Args:
            start_date: Start of period
            end_date: End of period
            compare: Whether to include comparison with previous period

        Returns:
            Dict with refund metrics including count, amount, rate, and reasons breakdown
        """
        from orders.models import Order, Refund

        # Current period refunds
        current_refunds = Refund.objects.filter(
            created_at__gte=start_date,
            created_at__lt=end_date
        )

        # Total orders in period for refund rate calculation
        total_orders = Order.objects.filter(
            created_at__gte=start_date,
            created_at__lt=end_date
        ).count()

        current_stats = current_refunds.aggregate(
            total_amount=Coalesce(Sum('total_amount_base', output_field=DecimalField()), Sum('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField())),
            refund_count=Count('id')
        )

        # Refund rate calculation
        refund_rate = Decimal('0.00')
        if total_orders > 0:
            refund_rate = (Decimal(current_stats['refund_count']) / Decimal(total_orders)) * 100

        # Breakdown by reason
        reasons_breakdown = {}
        for reason_code, reason_label in Refund.REFUND_REASON_CHOICES:
            count = current_refunds.filter(reason=reason_code).count()
            if count > 0:
                reasons_breakdown[reason_label] = count

        # Breakdown by status
        status_breakdown = {}
        for status_code, status_label in Refund.STATUS_CHOICES:
            count = current_refunds.filter(status=status_code).count()
            if count > 0:
                status_breakdown[status_label] = count

        result = {
            'current': {
                'total_amount': current_stats['total_amount'] or Decimal('0.00'),
                'refund_count': current_stats['refund_count'],
                'refund_rate': refund_rate,
                'total_orders': total_orders,
                'reasons_breakdown': reasons_breakdown,
                'status_breakdown': status_breakdown,
            }
        }

        if compare:
            # Previous period metrics
            prev_start, prev_end = cls.get_previous_period(start_date, end_date)

            prev_refunds = Refund.objects.filter(
                created_at__gte=prev_start,
                created_at__lt=prev_end
            )

            prev_total_orders = Order.objects.filter(
                created_at__gte=prev_start,
                created_at__lt=prev_end
            ).count()

            prev_stats = prev_refunds.aggregate(
                total_amount=Coalesce(Sum('total_amount_base', output_field=DecimalField()), Sum('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField())),
                refund_count=Count('id')
            )

            prev_refund_rate = Decimal('0.00')
            if prev_total_orders > 0:
                prev_refund_rate = (Decimal(prev_stats['refund_count']) / Decimal(prev_total_orders)) * 100

            result['previous'] = {
                'total_amount': prev_stats['total_amount'] or Decimal('0.00'),
                'refund_count': prev_stats['refund_count'],
                'refund_rate': prev_refund_rate,
                'total_orders': prev_total_orders,
            }

            # Calculate percentage changes
            result['changes'] = {
                'total_amount': cls.calculate_percentage_change(
                    result['current']['total_amount'],
                    result['previous']['total_amount']
                ),
                'refund_count': cls.calculate_percentage_change(
                    Decimal(result['current']['refund_count']),
                    Decimal(result['previous']['refund_count'])
                ),
                'refund_rate': cls.calculate_percentage_change(
                    result['current']['refund_rate'],
                    result['previous']['refund_rate']
                ),
            }

        return result

    @classmethod
    def get_sales_by_source(cls, start_date: datetime, end_date: datetime,
                           compare: bool = True) -> Dict:
        """
        Get sales performance broken down by source/channel

        Args:
            start_date: Start of period
            end_date: End of period
            compare: Whether to include comparison with previous period

        Returns:
            Dict with sales metrics by source including revenue, orders, AOV, conversion rate
        """
        from orders.models import Order

        # Current period sales by source
        current_orders = Order.objects.filter(
            created_at__gte=start_date,
            created_at__lt=end_date,
            status__in=['processing', 'shipped', 'delivered']
        )

        # Group by source
        by_source = []
        for source_code, source_label in Order.SOURCE_CHOICES:
            source_orders = current_orders.filter(source=source_code)

            stats = source_orders.aggregate(
                revenue=Coalesce(Sum('total_amount_base', output_field=DecimalField()), Sum('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField())),
                order_count=Count('id'),
                aov=Coalesce(Avg('total_amount_base', output_field=DecimalField()), Avg('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField()))
            )

            if stats['order_count'] > 0:  # Only include sources with orders
                by_source.append({
                    'source': source_code,
                    'source_label': source_label,
                    'revenue': stats['revenue'] or Decimal('0.00'),
                    'orders': stats['order_count'],
                    'aov': stats['aov'] or Decimal('0.00'),
                })

        # Sort by revenue descending
        by_source.sort(key=lambda x: x['revenue'], reverse=True)

        # Calculate totals
        total_revenue = sum(s['revenue'] for s in by_source)
        total_orders = sum(s['orders'] for s in by_source)

        result = {
            'by_source': by_source,
            'total_revenue': total_revenue,
            'total_orders': total_orders,
        }

        if compare:
            # Previous period metrics
            prev_start, prev_end = cls.get_previous_period(start_date, end_date)

            prev_orders = Order.objects.filter(
                created_at__gte=prev_start,
                created_at__lt=prev_end,
                status__in=['processing', 'shipped', 'delivered']
            )

            prev_by_source = {}
            for source_code, source_label in Order.SOURCE_CHOICES:
                source_orders = prev_orders.filter(source=source_code)

                stats = source_orders.aggregate(
                    revenue=Coalesce(Sum('total_amount_base', output_field=DecimalField()), Sum('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField())),
                    order_count=Count('id')
                )

                prev_by_source[source_code] = {
                    'revenue': stats['revenue'] or Decimal('0.00'),
                    'orders': stats['order_count'],
                }

            # Add changes to each source
            for source in result['by_source']:
                source_code = source['source']
                prev = prev_by_source.get(source_code, {'revenue': Decimal('0.00'), 'orders': 0})

                source['changes'] = {
                    'revenue': cls.calculate_percentage_change(
                        source['revenue'],
                        prev['revenue']
                    ),
                    'orders': cls.calculate_percentage_change(
                        Decimal(source['orders']),
                        Decimal(prev['orders'])
                    ),
                }

        return result

    @classmethod
    def get_utm_campaign_performance(cls, start_date: datetime, end_date: datetime,
                                    compare: bool = True) -> Dict:
        """
        Get UTM campaign performance metrics

        Args:
            start_date: Start of period
            end_date: End of period
            compare: Whether to include comparison with previous period

        Returns:
            Dict with campaign performance including visitors, conversions, revenue
        """
        from geoip.models import VisitorLocation
        from orders.models import Order

        # Get visitors with UTM data (exclude bots and admin traffic)
        current_visitors = VisitorLocation.objects.filter(
            first_seen__gte=start_date,
            first_seen__lt=end_date,
            is_bot=False,
            is_admin_traffic=False
        ).exclude(
            utm_campaign=''
        )

        # Group by campaign
        campaigns = []
        campaign_groups = current_visitors.values('utm_source', 'utm_medium', 'utm_campaign').annotate(
            visitor_count=Count('id')
        )

        for group in campaign_groups:
            utm_source = group['utm_source']
            utm_medium = group['utm_medium']
            utm_campaign = group['utm_campaign']

            # Get session keys for this campaign
            session_keys = list(current_visitors.filter(
                utm_source=utm_source,
                utm_medium=utm_medium,
                utm_campaign=utm_campaign
            ).values_list('session_key', flat=True))

            # Count orders from these sessions (using session key matching)
            # Note: This is a simplified approach - in production you'd want to track
            # session_key on Order model for accurate attribution
            campaign_orders = Order.objects.filter(
                created_at__gte=start_date,
                created_at__lt=end_date,
                status__in=['processing', 'shipped', 'delivered']
            )

            order_stats = campaign_orders.aggregate(
                revenue=Coalesce(Sum('total_amount_base', output_field=DecimalField()), Sum('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField())),
                order_count=Count('id')
            )

            # Calculate conversion rate
            visitors = group['visitor_count']
            orders = order_stats['order_count']
            conversion_rate = (Decimal(orders) / Decimal(visitors) * 100) if visitors > 0 else Decimal('0.00')

            campaigns.append({
                'utm_source': utm_source,
                'utm_medium': utm_medium,
                'utm_campaign': utm_campaign,
                'visitors': visitors,
                'orders': orders,
                'revenue': order_stats['revenue'] or Decimal('0.00'),
                'conversion_rate': conversion_rate,
                'revenue_per_visitor': (order_stats['revenue'] or Decimal('0.00')) / Decimal(visitors) if visitors > 0 else Decimal('0.00')
            })

        # Sort by revenue
        campaigns.sort(key=lambda x: x['revenue'], reverse=True)

        result = {
            'campaigns': campaigns,
            'total_utm_visitors': current_visitors.count(),
            'total_campaigns': len(campaigns),
        }

        # Add comparison if requested
        if compare:
            prev_start, prev_end = cls.get_previous_period(start_date, end_date)
            prev_visitors = VisitorLocation.objects.filter(
                first_seen__gte=prev_start,
                first_seen__lt=prev_end,
                is_bot=False,
                is_admin_traffic=False
            ).exclude(
                utm_campaign=''
            )

            result['comparison'] = {
                'previous_visitors': prev_visitors.count(),
                'change_pct': cls.calculate_percentage_change(
                    Decimal(current_visitors.count()),
                    Decimal(prev_visitors.count())
                )
            }

        return result

    @classmethod
    def get_traffic_sources(cls, start_date: datetime, end_date: datetime,
                           compare: bool = True) -> Dict:
        """
        Get traffic source breakdown (UTM + referrers)

        Args:
            start_date: Start of period
            end_date: End of period
            compare: Whether to include comparison with previous period

        Returns:
            Dict with traffic source metrics
        """
        from geoip.models import VisitorLocation
        from urllib.parse import urlparse

        current_visitors = VisitorLocation.objects.filter(
            first_seen__gte=start_date,
            first_seen__lt=end_date,
            is_bot=False,
            is_admin_traffic=False
        )

        # UTM Source breakdown
        utm_sources = []
        utm_groups = current_visitors.exclude(utm_source='').values('utm_source').annotate(
            visitor_count=Count('id')
        ).order_by('-visitor_count')

        for group in utm_groups:
            utm_sources.append({
                'source': group['utm_source'],
                'visitors': group['visitor_count'],
                'percentage': (Decimal(group['visitor_count']) / Decimal(current_visitors.count()) * 100) if current_visitors.count() > 0 else Decimal('0.00')
            })

        # Referrer domain breakdown
        referrer_domains = []
        visitors_with_referrer = current_visitors.exclude(referrer_url='')

        # Group by referrer domain (simplified - extract domain from URL)
        referrer_data = {}
        for visitor in visitors_with_referrer:
            try:
                parsed = urlparse(visitor.referrer_url)
                domain = parsed.netloc or 'direct'
                referrer_data[domain] = referrer_data.get(domain, 0) + 1
            except:
                referrer_data['direct'] = referrer_data.get('direct', 0) + 1

        for domain, count in sorted(referrer_data.items(), key=lambda x: x[1], reverse=True):
            referrer_domains.append({
                'domain': domain,
                'visitors': count,
                'percentage': (Decimal(count) / Decimal(current_visitors.count()) * 100) if current_visitors.count() > 0 else Decimal('0.00')
            })

        # Calculate direct vs referred traffic
        direct_traffic = current_visitors.filter(referrer_url='', utm_source='').count()
        referred_traffic = current_visitors.count() - direct_traffic

        result = {
            'utm_sources': utm_sources[:10],  # Top 10
            'referrer_domains': referrer_domains[:10],  # Top 10
            'direct_traffic': direct_traffic,
            'referred_traffic': referred_traffic,
            'total_visitors': current_visitors.count(),
        }

        # Add comparison if requested
        if compare:
            prev_start, prev_end = cls.get_previous_period(start_date, end_date)
            prev_visitors = VisitorLocation.objects.filter(
                first_seen__gte=prev_start,
                first_seen__lt=prev_end,
                is_bot=False,
                is_admin_traffic=False
            )

            prev_direct = prev_visitors.filter(referrer_url='', utm_source='').count()

            result['comparison'] = {
                'previous_total': prev_visitors.count(),
                'previous_direct': prev_direct,
                'total_change_pct': cls.calculate_percentage_change(
                    Decimal(current_visitors.count()),
                    Decimal(prev_visitors.count())
                ),
                'direct_change_pct': cls.calculate_percentage_change(
                    Decimal(direct_traffic),
                    Decimal(prev_direct)
                )
            }

        return result

    @classmethod
    def get_traffic_by_device(cls, start_date: datetime, end_date: datetime,
                             compare: bool = True) -> Dict:
        """
        Get traffic breakdown by device type

        Args:
            start_date: Start of period
            end_date: End of period
            compare: Whether to include comparison with previous period

        Returns:
            Dict with device type metrics
        """
        from geoip.models import VisitorLocation

        current_visitors = VisitorLocation.objects.filter(
            first_seen__gte=start_date,
            first_seen__lt=end_date,
            is_bot=False,
            is_admin_traffic=False
        )

        # Device type breakdown
        device_breakdown = []
        for device_code, device_label in VisitorLocation.DEVICE_TYPE_CHOICES:
            device_visitors = current_visitors.filter(device_type=device_code)
            count = device_visitors.count()

            if count > 0:
                device_breakdown.append({
                    'device': device_code,
                    'device_label': device_label,
                    'visitors': count,
                    'percentage': (Decimal(count) / Decimal(current_visitors.count()) * 100) if current_visitors.count() > 0 else Decimal('0.00')
                })

        # Sort by visitor count
        device_breakdown.sort(key=lambda x: x['visitors'], reverse=True)

        result = {
            'device_breakdown': device_breakdown,
            'total_visitors': current_visitors.count(),
        }

        # Add comparison if requested
        if compare:
            prev_start, prev_end = cls.get_previous_period(start_date, end_date)
            prev_visitors = VisitorLocation.objects.filter(
                first_seen__gte=prev_start,
                first_seen__lt=prev_end,
                is_bot=False,
                is_admin_traffic=False
            )

            prev_breakdown = {}
            for device_code, device_label in VisitorLocation.DEVICE_TYPE_CHOICES:
                prev_breakdown[device_code] = prev_visitors.filter(device_type=device_code).count()

            result['comparison'] = {
                'previous_total': prev_visitors.count(),
                'device_changes': {},
                'total_change_pct': cls.calculate_percentage_change(
                    Decimal(current_visitors.count()),
                    Decimal(prev_visitors.count())
                )
            }

            # Calculate change for each device type
            for device in device_breakdown:
                device_code = device['device']
                prev_count = prev_breakdown.get(device_code, 0)
                result['comparison']['device_changes'][device_code] = cls.calculate_percentage_change(
                    Decimal(device['visitors']),
                    Decimal(prev_count)
                )

        return result

    @classmethod
    def get_conversion_by_device(cls, start_date: datetime, end_date: datetime,
                                 compare: bool = True) -> Dict:
        """
        Get conversion rate by device type

        Args:
            start_date: Start of period
            end_date: End of period
            compare: Whether to include comparison with previous period

        Returns:
            Dict with device conversion metrics
        """
        from geoip.models import VisitorLocation
        from orders.models import Order

        current_visitors = VisitorLocation.objects.filter(
            first_seen__gte=start_date,
            first_seen__lt=end_date,
            is_bot=False,
            is_admin_traffic=False
        )

        current_orders = Order.objects.filter(
            created_at__gte=start_date,
            created_at__lt=end_date,
            status__in=['processing', 'shipped', 'delivered']
        )

        # Device conversion breakdown
        device_conversion = []
        for device_code, device_label in VisitorLocation.DEVICE_TYPE_CHOICES:
            device_visitors = current_visitors.filter(device_type=device_code).count()

            if device_visitors > 0:
                # Note: This is a simplified approach - ideally you'd track device_type on Order
                # For now, we calculate overall conversion and assume proportional distribution
                device_orders = int(current_orders.count() * (device_visitors / current_visitors.count())) if current_visitors.count() > 0 else 0

                conversion_rate = (Decimal(device_orders) / Decimal(device_visitors) * 100) if device_visitors > 0 else Decimal('0.00')

                device_conversion.append({
                    'device': device_code,
                    'device_label': device_label,
                    'visitors': device_visitors,
                    'orders': device_orders,
                    'conversion_rate': conversion_rate,
                })

        # Sort by conversion rate
        device_conversion.sort(key=lambda x: x['conversion_rate'], reverse=True)

        result = {
            'device_conversion': device_conversion,
            'total_visitors': current_visitors.count(),
            'total_orders': current_orders.count(),
        }

        # Add comparison if requested
        if compare:
            prev_start, prev_end = cls.get_previous_period(start_date, end_date)
            prev_visitors = VisitorLocation.objects.filter(
                first_seen__gte=prev_start,
                first_seen__lt=prev_end,
                is_bot=False,
                is_admin_traffic=False
            )
            prev_orders = Order.objects.filter(
                created_at__gte=prev_start,
                created_at__lt=prev_end,
                status__in=['processing', 'shipped', 'delivered']
            )

            result['comparison'] = {
                'previous_visitors': prev_visitors.count(),
                'previous_orders': prev_orders.count(),
                'visitor_change_pct': cls.calculate_percentage_change(
                    Decimal(current_visitors.count()),
                    Decimal(prev_visitors.count())
                ),
                'order_change_pct': cls.calculate_percentage_change(
                    Decimal(current_orders.count()),
                    Decimal(prev_orders.count())
                )
            }

        return result

    @classmethod
    def get_revenue_by_device(cls, start_date: datetime, end_date: datetime,
                             compare: bool = True) -> Dict:
        """
        Get revenue breakdown by device type

        Args:
            start_date: Start of period
            end_date: End of period
            compare: Whether to include comparison with previous period

        Returns:
            Dict with device revenue metrics
        """
        from geoip.models import VisitorLocation
        from orders.models import Order

        current_visitors = VisitorLocation.objects.filter(
            first_seen__gte=start_date,
            first_seen__lt=end_date,
            is_bot=False,
            is_admin_traffic=False
        )

        current_orders = Order.objects.filter(
            created_at__gte=start_date,
            created_at__lt=end_date,
            status__in=['processing', 'shipped', 'delivered']
        )

        total_revenue = current_orders.aggregate(
            revenue=Coalesce(Sum('total_amount_base', output_field=DecimalField()), Sum('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )['revenue'] or Decimal('0.00')

        # Device revenue breakdown
        device_revenue = []
        for device_code, device_label in VisitorLocation.DEVICE_TYPE_CHOICES:
            device_visitors = current_visitors.filter(device_type=device_code).count()

            if device_visitors > 0:
                # Note: This is a simplified approach - proportional revenue distribution
                # Ideally track device_type on Order for accurate attribution
                visitor_ratio = Decimal(device_visitors) / Decimal(current_visitors.count()) if current_visitors.count() > 0 else Decimal('0.00')
                device_revenue_amount = total_revenue * visitor_ratio

                device_revenue.append({
                    'device': device_code,
                    'device_label': device_label,
                    'revenue': device_revenue_amount,
                    'visitors': device_visitors,
                    'revenue_per_visitor': device_revenue_amount / Decimal(device_visitors) if device_visitors > 0 else Decimal('0.00'),
                    'percentage': (visitor_ratio * 100),
                })

        # Sort by revenue
        device_revenue.sort(key=lambda x: x['revenue'], reverse=True)

        result = {
            'device_revenue': device_revenue,
            'total_revenue': total_revenue,
            'total_visitors': current_visitors.count(),
        }

        # Add comparison if requested
        if compare:
            prev_start, prev_end = cls.get_previous_period(start_date, end_date)
            prev_orders = Order.objects.filter(
                created_at__gte=prev_start,
                created_at__lt=prev_end,
                status__in=['processing', 'shipped', 'delivered']
            )

            prev_revenue = prev_orders.aggregate(
                revenue=Coalesce(Sum('total_amount_base', output_field=DecimalField()), Sum('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField()))
            )['revenue'] or Decimal('0.00')

            result['comparison'] = {
                'previous_revenue': prev_revenue,
                'revenue_change_pct': cls.calculate_percentage_change(
                    total_revenue,
                    prev_revenue
                )
            }

        return result

    @classmethod
    def get_profit_metrics(cls, start_date: datetime, end_date: datetime,
                          compare: bool = True) -> Dict:
        """
        Get profit margin metrics and analysis

        Args:
            start_date: Start of period
            end_date: End of period
            compare: Whether to include comparison with previous period

        Returns:
            Dict with profit metrics including revenue, COGS, refunds, profit, margin
        """
        from orders.models import Order, OrderItem, Refund
        from catalog.models import Product

        # Get current period orders
        current_orders = Order.objects.filter(
            created_at__gte=start_date,
            created_at__lt=end_date,
            status__in=['processing', 'shipped', 'delivered']
        )

        # Calculate revenue
        revenue_stats = current_orders.aggregate(
            revenue=Coalesce(Sum('total_amount_base', output_field=DecimalField()), Sum('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )
        revenue = revenue_stats['revenue'] or Decimal('0.00')

        # Get all order items for this period
        order_items = OrderItem.objects.filter(
            order__in=current_orders
        ).select_related('product')

        # Get refunds for orders in this period (not just refunds created in this period)
        # This ensures we account for refunds on orders from this period
        refunds_for_orders = Refund.objects.filter(
            order__in=current_orders,
            status='completed'
        ).select_related('order')

        # Build map of refunded items: {order_item_id: refunded_quantity}
        refunded_items = {}
        refund_amount = Decimal('0.00')

        for refund in refunds_for_orders:
            # Sum up total refund amounts
            if hasattr(refund.total_amount, 'amount'):
                refund_amount += Decimal(str(refund.total_amount.amount))
            else:
                refund_amount += Decimal(str(refund.total_amount))

            # Track refunded quantities per item
            if refund.items_json:
                for item_data in refund.items_json:
                    item_id = item_data.get('order_item_id')
                    if item_id:
                        qty = int(item_data.get('quantity', 0))
                        refunded_items[item_id] = refunded_items.get(item_id, 0) + qty

        # Calculate COGS (Cost of Goods Sold) - excluding refunded items
        cogs = Decimal('0.00')
        for item in order_items:
            if item.product and item.product.cost:
                # Get refunded quantity for this item
                refunded_qty = refunded_items.get(item.id, 0)
                # Only count cost for items that were kept (not refunded)
                kept_qty = item.quantity - refunded_qty

                if kept_qty > 0:
                    # Convert cost to decimal
                    item_cogs = Decimal(str(item.product.cost.amount)) * kept_qty
                    cogs += item_cogs

        # Store refunds for display
        refunds = refund_amount

        # Calculate profit: Revenue - COGS - Refunds
        # Revenue = Total order amounts (includes amounts that were refunded)
        # COGS = Cost only for items that were kept
        # Refunds = Money returned to customers
        profit = revenue - cogs - refunds

        # Calculate profit margin percentage
        margin_percentage = (profit / revenue * 100) if revenue > 0 else Decimal('0.00')

        # Calculate profit by product (top 10) - accounting for refunds
        profit_by_product = []
        product_profits = {}

        for item in order_items:
            if item.product and item.product.cost:
                product_id = item.product.id
                if product_id not in product_profits:
                    product_profits[product_id] = {
                        'product_name': item.product_name or item.product.name,
                        'product_id': product_id,
                        'revenue': Decimal('0.00'),
                        'cogs': Decimal('0.00'),
                        'units_sold': 0
                    }

                # Get refunded quantity for this item
                refunded_qty = refunded_items.get(item.id, 0)
                # Only count items that were kept (not refunded)
                kept_qty = item.quantity - refunded_qty

                if kept_qty > 0:
                    # Calculate revenue per unit
                    product_revenue = Decimal(str(item.total_price.amount)) if hasattr(item.total_price, 'amount') else Decimal(str(item.total_price))
                    revenue_per_unit = product_revenue / item.quantity if item.quantity > 0 else Decimal('0.00')

                    # Only count revenue and COGS for items that were kept
                    kept_revenue = revenue_per_unit * kept_qty
                    product_cogs = Decimal(str(item.product.cost.amount)) * kept_qty

                    product_profits[product_id]['revenue'] += kept_revenue
                    product_profits[product_id]['cogs'] += product_cogs
                    product_profits[product_id]['units_sold'] += kept_qty

        # Calculate profit for each product and sort
        for product_data in product_profits.values():
            product_data['profit'] = product_data['revenue'] - product_data['cogs']
            product_data['margin_pct'] = (product_data['profit'] / product_data['revenue'] * 100) if product_data['revenue'] > 0 else Decimal('0.00')
            profit_by_product.append(product_data)

        profit_by_product.sort(key=lambda x: x['profit'], reverse=True)
        profit_by_product = profit_by_product[:10]  # Top 10

        # Calculate profit by category
        # Note: This requires category info on products - simplified for now
        profit_by_category = []  # To be implemented if category structure exists

        result = {
            'current': {
                'revenue': revenue,
                'cogs': cogs,
                'refunds': refunds,
                'profit': profit,
                'margin_percentage': margin_percentage
            },
            'by_product': profit_by_product,
            'by_category': profit_by_category
        }

        # Add comparison if requested
        if compare:
            prev_start, prev_end = cls.get_previous_period(start_date, end_date)
            prev_orders = Order.objects.filter(
                created_at__gte=prev_start,
                created_at__lt=prev_end,
                status__in=['processing', 'shipped', 'delivered']
            )

            # Previous revenue
            prev_revenue_stats = prev_orders.aggregate(
                revenue=Coalesce(Sum('total_amount_base', output_field=DecimalField()), Sum('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField()))
            )
            prev_revenue = prev_revenue_stats['revenue'] or Decimal('0.00')

            # Previous items
            prev_items = OrderItem.objects.filter(order__in=prev_orders).select_related('product')

            # Get refunds for previous period orders
            prev_refunds_for_orders = Refund.objects.filter(
                order__in=prev_orders,
                status='completed'
            ).select_related('order')

            # Build map of refunded items for previous period
            prev_refunded_items = {}
            prev_refund_amount = Decimal('0.00')

            for refund in prev_refunds_for_orders:
                # Sum up total refund amounts
                if hasattr(refund.total_amount, 'amount'):
                    prev_refund_amount += Decimal(str(refund.total_amount.amount))
                else:
                    prev_refund_amount += Decimal(str(refund.total_amount))

                # Track refunded quantities per item
                if refund.items_json:
                    for item_data in refund.items_json:
                        item_id = item_data.get('order_item_id')
                        if item_id:
                            qty = int(item_data.get('quantity', 0))
                            prev_refunded_items[item_id] = prev_refunded_items.get(item_id, 0) + qty

            # Previous COGS - excluding refunded items
            prev_cogs = Decimal('0.00')
            for item in prev_items:
                if item.product and item.product.cost:
                    # Get refunded quantity for this item
                    refunded_qty = prev_refunded_items.get(item.id, 0)
                    # Only count cost for items that were kept
                    kept_qty = item.quantity - refunded_qty

                    if kept_qty > 0:
                        item_cogs = Decimal(str(item.product.cost.amount)) * kept_qty
                        prev_cogs += item_cogs

            # Store refunds for display
            prev_refunds = prev_refund_amount

            # Previous profit
            prev_profit = prev_revenue - prev_cogs - prev_refunds
            prev_margin_percentage = (prev_profit / prev_revenue * 100) if prev_revenue > 0 else Decimal('0.00')

            result['previous'] = {
                'revenue': prev_revenue,
                'cogs': prev_cogs,
                'refunds': prev_refunds,
                'profit': prev_profit,
                'margin_percentage': prev_margin_percentage
            }

            result['changes'] = {
                'revenue': cls.calculate_percentage_change(revenue, prev_revenue),
                'cogs': cls.calculate_percentage_change(cogs, prev_cogs),
                'refunds': cls.calculate_percentage_change(refunds, prev_refunds),
                'profit': cls.calculate_percentage_change(profit, prev_profit),
                'margin_percentage': prev_margin_percentage - margin_percentage if prev_revenue > 0 else Decimal('0.00')
            }

        return result

    @classmethod
    def get_abandoned_cart_metrics(cls, start_date: datetime, end_date: datetime,
                                   compare: bool = True) -> Dict:
        """
        Get abandoned cart analytics and recovery metrics

        Args:
            start_date: Start of period
            end_date: End of period
            compare: Whether to include comparison with previous period

        Returns:
            Dict with abandoned cart metrics, recovery stats, and recent carts
        """
        from customers.models import AbandonedCart
        from django.contrib.auth import get_user_model

        User = get_user_model()

        # Current period abandoned carts
        current_abandoned = AbandonedCart.objects.filter(
            abandoned_at__gte=start_date,
            abandoned_at__lt=end_date
        )

        # Calculate metrics
        total_abandoned = current_abandoned.count()
        recovered_count = current_abandoned.filter(recovered=True).count()
        unrecovered_count = total_abandoned - recovered_count

        # Calculate total potential value
        total_value_stats = current_abandoned.aggregate(
            total=Coalesce(Sum('total_value', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )
        total_potential_value = total_value_stats['total'] or Decimal('0.00')

        # Calculate recovered value
        recovered_value_stats = current_abandoned.filter(recovered=True).aggregate(
            total=Coalesce(Sum('total_value', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )
        recovered_value = recovered_value_stats['total'] or Decimal('0.00')

        # Calculate unrecovered value
        unrecovered_value = total_potential_value - recovered_value

        # Calculate recovery rate
        recovery_rate = (recovered_count / total_abandoned * 100) if total_abandoned > 0 else Decimal('0.00')

        # Calculate average cart value
        avg_cart_value = (total_potential_value / total_abandoned) if total_abandoned > 0 else Decimal('0.00')

        result = {
            'current': {
                'total_abandoned': total_abandoned,
                'recovered_count': recovered_count,
                'unrecovered_count': unrecovered_count,
                'total_potential_value': total_potential_value,
                'recovered_value': recovered_value,
                'unrecovered_value': unrecovered_value,
                'recovery_rate': recovery_rate,
                'avg_cart_value': avg_cart_value
            }
        }

        # Get recent abandoned carts (last 20 unrecovered)
        recent_carts = current_abandoned.filter(
            recovered=False
        ).select_related('user', 'cart').prefetch_related('cart__items__product')[:20]

        recent_carts_list = []
        for abandoned in recent_carts:
            try:
                user = abandoned.user
                cart_items = abandoned.cart.items.all()[:3]  # First 3 items for preview

                items_preview = [
                    {
                        'product_name': item.product.name if item.product else item.product_name,
                        'quantity': item.quantity,
                        'unit_price': float(item.unit_price.amount) if hasattr(item.unit_price, 'amount') else float(item.unit_price)
                    }
                    for item in cart_items
                ]

                recent_carts_list.append({
                    'id': abandoned.id,
                    'user_id': user.id,
                    'user_name': user.get_full_name() or user.username,
                    'user_email': user.email,
                    'abandoned_at': abandoned.abandoned_at.isoformat(),
                    'days_since_abandonment': abandoned.days_since_abandonment,
                    'total_items': abandoned.total_items,
                    'total_value': float(abandoned.total_value.amount) if hasattr(abandoned.total_value, 'amount') else float(abandoned.total_value),
                    'recovery_emails_sent': abandoned.recovery_emails_sent,
                    'estimated_reason': abandoned.get_estimated_reason_display(),
                    'items_preview': items_preview
                })
            except Exception as e:
                logger.error(f"Error processing abandoned cart {abandoned.id}: {e}")
                continue

        result['recent_carts'] = recent_carts_list

        # Add comparison if requested
        if compare:
            prev_start, prev_end = cls.get_previous_period(start_date, end_date)

            prev_abandoned = AbandonedCart.objects.filter(
                abandoned_at__gte=prev_start,
                abandoned_at__lt=prev_end
            )

            prev_total_abandoned = prev_abandoned.count()
            prev_recovered_count = prev_abandoned.filter(recovered=True).count()
            prev_unrecovered_count = prev_total_abandoned - prev_recovered_count

            prev_total_value_stats = prev_abandoned.aggregate(
                total=Coalesce(Sum('total_value', output_field=DecimalField()), Value(0, output_field=DecimalField()))
            )
            prev_total_potential_value = prev_total_value_stats['total'] or Decimal('0.00')

            prev_recovered_value_stats = prev_abandoned.filter(recovered=True).aggregate(
                total=Coalesce(Sum('total_value', output_field=DecimalField()), Value(0, output_field=DecimalField()))
            )
            prev_recovered_value = prev_recovered_value_stats['total'] or Decimal('0.00')

            prev_unrecovered_value = prev_total_potential_value - prev_recovered_value

            prev_recovery_rate = (prev_recovered_count / prev_total_abandoned * 100) if prev_total_abandoned > 0 else Decimal('0.00')

            prev_avg_cart_value = (prev_total_potential_value / prev_total_abandoned) if prev_total_abandoned > 0 else Decimal('0.00')

            result['previous'] = {
                'total_abandoned': prev_total_abandoned,
                'recovered_count': prev_recovered_count,
                'unrecovered_count': prev_unrecovered_count,
                'total_potential_value': prev_total_potential_value,
                'recovered_value': prev_recovered_value,
                'unrecovered_value': prev_unrecovered_value,
                'recovery_rate': prev_recovery_rate,
                'avg_cart_value': prev_avg_cart_value
            }

            result['changes'] = {
                'total_abandoned': cls.calculate_percentage_change(total_abandoned, prev_total_abandoned),
                'recovered_count': cls.calculate_percentage_change(recovered_count, prev_recovered_count),
                'unrecovered_count': cls.calculate_percentage_change(unrecovered_count, prev_unrecovered_count),
                'total_potential_value': cls.calculate_percentage_change(total_potential_value, prev_total_potential_value),
                'recovered_value': cls.calculate_percentage_change(recovered_value, prev_recovered_value),
                'unrecovered_value': cls.calculate_percentage_change(unrecovered_value, prev_unrecovered_value),
                'recovery_rate': prev_recovery_rate - recovery_rate if prev_total_abandoned > 0 else Decimal('0.00'),
                'avg_cart_value': cls.calculate_percentage_change(avg_cart_value, prev_avg_cart_value)
            }

        return result

    @classmethod
    def get_voucher_performance(cls, start_date: datetime, end_date: datetime,
                               compare: bool = True) -> Dict:
        """
        Get voucher performance analytics

        Args:
            start_date: Start of period
            end_date: End of period
            compare: Whether to include comparison with previous period

        Returns:
            Dict with voucher performance metrics and top performing vouchers
        """
        from vouchers.models import VoucherCode, VoucherUsage

        # Current period voucher usage
        current_usages = VoucherUsage.objects.filter(
            used_at__gte=start_date,
            used_at__lt=end_date
        ).select_related('voucher', 'order')

        # Calculate metrics
        total_uses = current_usages.count()

        # Calculate total discount given
        discount_stats = current_usages.aggregate(
            total_discount=Coalesce(Sum('discount_amount', output_field=DecimalField()), Value(0, output_field=DecimalField())),
            total_revenue=Coalesce(Sum('cart_total', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )
        total_discount = discount_stats['total_discount'] or Decimal('0.00')
        total_revenue = discount_stats['total_revenue'] or Decimal('0.00')

        # Calculate average discount
        avg_discount = (total_discount / total_uses) if total_uses > 0 else Decimal('0.00')

        # Calculate discount rate (discount / revenue)
        discount_rate = (total_discount / total_revenue * 100) if total_revenue > 0 else Decimal('0.00')

        # Count active vs total vouchers
        total_vouchers = VoucherCode.objects.count()
        active_vouchers = VoucherCode.objects.filter(is_active=True).count()

        result = {
            'current': {
                'total_uses': total_uses,
                'total_discount': total_discount,
                'total_revenue': total_revenue,
                'avg_discount': avg_discount,
                'discount_rate': discount_rate,
                'total_vouchers': total_vouchers,
                'active_vouchers': active_vouchers
            }
        }

        # Top vouchers by usage count
        top_by_usage = current_usages.values(
            'voucher__code',
            'voucher__name',
            'voucher__discount_type'
        ).annotate(
            use_count=Count('id'),
            total_discount=Coalesce(Sum('discount_amount', output_field=DecimalField()), Value(0, output_field=DecimalField())),
            total_revenue=Coalesce(Sum('cart_total', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        ).order_by('-use_count')[:10]

        top_vouchers_list = []
        for voucher_data in top_by_usage:
            discount_rate_pct = (voucher_data['total_discount'] / voucher_data['total_revenue'] * 100) if voucher_data['total_revenue'] > 0 else Decimal('0.00')
            top_vouchers_list.append({
                'code': voucher_data['voucher__code'],
                'name': voucher_data['voucher__name'],
                'discount_type': voucher_data['voucher__discount_type'],
                'use_count': voucher_data['use_count'],
                'total_discount': float(voucher_data['total_discount']),
                'total_revenue': float(voucher_data['total_revenue']),
                'discount_rate': float(discount_rate_pct)
            })

        result['top_vouchers'] = top_vouchers_list

        # Add comparison if requested
        if compare:
            prev_start, prev_end = cls.get_previous_period(start_date, end_date)

            prev_usages = VoucherUsage.objects.filter(
                used_at__gte=prev_start,
                used_at__lt=prev_end
            )

            prev_total_uses = prev_usages.count()

            prev_discount_stats = prev_usages.aggregate(
                total_discount=Coalesce(Sum('discount_amount', output_field=DecimalField()), Value(0, output_field=DecimalField())),
                total_revenue=Coalesce(Sum('cart_total', output_field=DecimalField()), Value(0, output_field=DecimalField()))
            )
            prev_total_discount = prev_discount_stats['total_discount'] or Decimal('0.00')
            prev_total_revenue = prev_discount_stats['total_revenue'] or Decimal('0.00')

            prev_avg_discount = (prev_total_discount / prev_total_uses) if prev_total_uses > 0 else Decimal('0.00')
            prev_discount_rate = (prev_total_discount / prev_total_revenue * 100) if prev_total_revenue > 0 else Decimal('0.00')

            result['previous'] = {
                'total_uses': prev_total_uses,
                'total_discount': prev_total_discount,
                'total_revenue': prev_total_revenue,
                'avg_discount': prev_avg_discount,
                'discount_rate': prev_discount_rate
            }

            result['changes'] = {
                'total_uses': cls.calculate_percentage_change(total_uses, prev_total_uses),
                'total_discount': cls.calculate_percentage_change(total_discount, prev_total_discount),
                'total_revenue': cls.calculate_percentage_change(total_revenue, prev_total_revenue),
                'avg_discount': cls.calculate_percentage_change(avg_discount, prev_avg_discount),
                'discount_rate': prev_discount_rate - discount_rate if prev_total_revenue > 0 else Decimal('0.00')
            }

        return result

    @classmethod
    def get_customer_segmentation(cls) -> Dict:
        """
        Get customer segmentation visualization data

        Returns:
            Dict with segment distribution, customer counts, and value metrics
        """
        from customers.models import CustomerSegment, CustomerMetrics
        from django.contrib.auth import get_user_model

        User = get_user_model()

        # Get all active segments
        segments = CustomerSegment.objects.filter(is_active=True).order_by('-priority', 'name')

        segment_data = []
        total_customers = 0
        total_lifetime_value = Decimal('0.00')

        # Count customers in each segment
        for segment in segments:
            # Get all customer metrics
            segment_customers = []
            segment_ltv = Decimal('0.00')
            segment_aov = Decimal('0.00')
            segment_order_count = 0

            # Iterate through all customer metrics to find matches
            all_metrics = CustomerMetrics.objects.select_related('user').all()

            for metrics in all_metrics:
                if segment.matches_user(metrics):
                    segment_customers.append(metrics.user)
                    segment_ltv += Decimal(str(metrics.lifetime_value.amount)) if metrics.lifetime_value else Decimal('0.00')
                    segment_aov += Decimal(str(metrics.average_order_value.amount)) if metrics.average_order_value else Decimal('0.00')
                    segment_order_count += metrics.completed_orders

            customer_count = len(segment_customers)
            avg_ltv = (segment_ltv / customer_count) if customer_count > 0 else Decimal('0.00')
            avg_aov = (segment_aov / customer_count) if customer_count > 0 else Decimal('0.00')

            segment_data.append({
                'name': segment.name,
                'display_name': segment.display_name,
                'description': segment.description,
                'color': segment.color,
                'customer_count': customer_count,
                'total_ltv': float(segment_ltv),
                'avg_ltv': float(avg_ltv),
                'avg_aov': float(avg_aov),
                'total_orders': segment_order_count
            })

            total_customers += customer_count
            total_lifetime_value += segment_ltv

        # Calculate percentages
        for segment in segment_data:
            segment['percentage'] = (segment['customer_count'] / total_customers * 100) if total_customers > 0 else 0.0

        result = {
            'segments': segment_data,
            'total_customers': total_customers,
            'total_lifetime_value': float(total_lifetime_value)
        }

        return result

    @classmethod
    def get_top_products(cls, start_date: datetime, end_date: datetime,
                        limit: int = 10) -> List[Dict]:
        """
        Get top selling products for the period

        Args:
            start_date: Start of period
            end_date: End of period
            limit: Number of products to return

        Returns:
            List of dicts with product info, units sold, and revenue
        """
        from orders.models import OrderItem
        from catalog.models import Product

        # Aggregate sales by product
        top_items = OrderItem.objects.filter(
            order__created_at__gte=start_date,
            order__created_at__lt=end_date,
            order__status__in=['processing', 'shipped', 'delivered']
        ).values(
            'product_id',
            'product_name'
        ).annotate(
            units_sold=Sum('quantity'),
            revenue=Coalesce(Sum('total_price_base', output_field=DecimalField()), Sum('total_price', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        ).order_by('-revenue')[:limit]

        results = []
        for item in top_items:
            # Get product details for image
            try:
                product = Product.objects.prefetch_related('images__media_asset__thumbnails').get(id=item['product_id'])
                # Get primary image or first image
                primary_image = product.images.filter(is_primary=True).first()
                if not primary_image:
                    primary_image = product.images.first()
                # Use thumbnail for better performance (300x300)
                image_url = primary_image.media_asset.get_thumbnail('small') if (primary_image and primary_image.media_asset) else None
            except Product.DoesNotExist:
                image_url = None

            results.append({
                'product_id': item['product_id'],
                'name': item['product_name'],
                'image_url': image_url,
                'units_sold': item['units_sold'],
                'revenue': item['revenue'] or Decimal('0.00'),
            })

        return results

    @classmethod
    def get_visitor_analytics(cls, start_date: datetime, end_date: datetime,
                             compare: bool = True) -> Dict:
        """
        Get visitor analytics metrics.
        Excludes bot and admin traffic from main metrics.
        Provides separate bot/admin traffic counts.

        Args:
            start_date: Start of period
            end_date: End of period
            compare: Whether to include comparison with previous period

        Returns:
            Dict with visitor metrics, bot metrics, and optional comparison data
        """
        from geoip.models import VisitorLocation
        from orders.models import Order
        from django.contrib.auth import get_user_model

        User = get_user_model()

        # All visitors in period (unfiltered, for bot metrics)
        all_visitors = VisitorLocation.objects.filter(
            first_seen__gte=start_date,
            first_seen__lt=end_date
        )

        # Real human storefront visitors only (exclude bots and admin traffic)
        current_visitors = all_visitors.filter(
            is_bot=False,
            is_admin_traffic=False
        )

        # Bot and admin traffic counts (separate metrics)
        bot_visitors = all_visitors.filter(is_bot=True)
        admin_visitors = all_visitors.filter(is_admin_traffic=True, is_bot=False)

        unique_visitors = current_visitors.count()
        total_page_views = current_visitors.aggregate(
            total=Coalesce(Sum('page_views'), Value(0))
        )['total']

        # Orders in period
        orders_in_period = Order.objects.filter(
            created_at__gte=start_date,
            created_at__lt=end_date,
            status__in=['processing', 'shipped', 'delivered']
        ).count()

        # New customers (users created in period)
        new_customers = User.objects.filter(
            date_joined__gte=start_date,
            date_joined__lt=end_date,
            is_staff=False,
            is_superuser=False
        ).exclude(
            username__startswith='guest_'
        ).count()

        # Conversion rate (based on real visitors only)
        conversion_rate = (orders_in_period / unique_visitors * 100) if unique_visitors > 0 else 0

        result = {
            'current': {
                'unique_visitors': unique_visitors,
                'page_views': total_page_views,
                'new_customers': new_customers,
                'conversion_rate': round(conversion_rate, 2),
            },
            'automated_traffic': {
                'bot_visitors': bot_visitors.count(),
                'bot_page_views': bot_visitors.aggregate(
                    total=Coalesce(Sum('page_views'), Value(0))
                )['total'],
                'admin_visitors': admin_visitors.count(),
                'admin_page_views': admin_visitors.aggregate(
                    total=Coalesce(Sum('page_views'), Value(0))
                )['total'],
            }
        }

        if compare:
            prev_start, prev_end = cls.get_previous_period(start_date, end_date)

            prev_visitors = VisitorLocation.objects.filter(
                first_seen__gte=prev_start,
                first_seen__lt=prev_end,
                is_bot=False,
                is_admin_traffic=False
            )

            prev_unique_visitors = prev_visitors.count()
            prev_page_views = prev_visitors.aggregate(
                total=Coalesce(Sum('page_views'), Value(0))
            )['total']

            prev_orders = Order.objects.filter(
                created_at__gte=prev_start,
                created_at__lt=prev_end,
                status__in=['processing', 'shipped', 'delivered']
            ).count()

            prev_new_customers = User.objects.filter(
                date_joined__gte=prev_start,
                date_joined__lt=prev_end,
                is_staff=False,
                is_superuser=False
            ).exclude(
                username__startswith='guest_'
            ).count()

            prev_conversion_rate = (prev_orders / prev_unique_visitors * 100) if prev_unique_visitors > 0 else 0

            result['previous'] = {
                'unique_visitors': prev_unique_visitors,
                'page_views': prev_page_views,
                'new_customers': prev_new_customers,
                'conversion_rate': round(prev_conversion_rate, 2),
            }

            result['changes'] = {
                'unique_visitors': cls.calculate_percentage_change(
                    Decimal(unique_visitors),
                    Decimal(prev_unique_visitors)
                ),
                'page_views': cls.calculate_percentage_change(
                    Decimal(total_page_views),
                    Decimal(prev_page_views)
                ),
                'new_customers': cls.calculate_percentage_change(
                    Decimal(new_customers),
                    Decimal(prev_new_customers)
                ),
                'conversion_rate': cls.calculate_percentage_change(
                    Decimal(str(conversion_rate)),
                    Decimal(str(prev_conversion_rate))
                ),
            }

        return result

    @classmethod
    def get_views_over_time(cls, start_date: datetime, end_date: datetime,
                           compare: bool = True) -> Dict:
        """
        Get page views over time for charting

        Args:
            start_date: Start of period
            end_date: End of period
            compare: Whether to include comparison with previous period

        Returns:
            Dict with daily page view data and optional comparison
        """
        from geoip.models import VisitorLocation

        # Current period - group by date (exclude bots and admin traffic)
        current_views = VisitorLocation.objects.filter(
            first_seen__gte=start_date,
            first_seen__lt=end_date,
            is_bot=False,
            is_admin_traffic=False
        ).annotate(
            date=TruncDate('first_seen')
        ).values('date').annotate(
            views=Sum('page_views')
        ).order_by('date')

        # Convert to dict for easy lookup
        current_dict = {item['date']: item['views'] for item in current_views}

        result = {
            'current': {
                'labels': [],
                'data': [],
            }
        }

        # Generate all dates in range
        current = start_date.date()
        end = end_date.date()
        while current < end:
            result['current']['labels'].append(current.strftime('%Y-%m-%d'))
            result['current']['data'].append(current_dict.get(current, 0))
            current += timedelta(days=1)

        if compare:
            prev_start, prev_end = cls.get_previous_period(start_date, end_date)

            prev_views = VisitorLocation.objects.filter(
                first_seen__gte=prev_start,
                first_seen__lt=prev_end,
                is_bot=False,
                is_admin_traffic=False
            ).annotate(
                date=TruncDate('first_seen')
            ).values('date').annotate(
                views=Sum('page_views')
            ).order_by('date')

            prev_dict = {item['date']: item['views'] for item in prev_views}

            result['previous'] = {
                'labels': [],
                'data': [],
            }

            current = prev_start.date()
            end = prev_end.date()
            while current < end:
                result['previous']['labels'].append(current.strftime('%Y-%m-%d'))
                result['previous']['data'].append(prev_dict.get(current, 0))
                current += timedelta(days=1)

        return result

    @classmethod
    def get_most_viewed_products(cls, start_date: datetime, end_date: datetime,
                                 limit: int = 10) -> List[Dict]:
        """
        Get most viewed products for the period

        Note: This requires tracking product views. If not implemented,
        returns empty list.

        Args:
            start_date: Start of period
            end_date: End of period
            limit: Number of products to return

        Returns:
            List of dicts with product info and view counts
        """
        from catalog.models import Product

        # Get most viewed published products
        top_products = Product.objects.filter(
            status='published'
        ).prefetch_related('images__media_asset__thumbnails').order_by('-views_count')[:limit]

        results = []
        for product in top_products:
            # Get primary image or first image
            primary_image = product.images.filter(is_primary=True).first()
            if not primary_image:
                primary_image = product.images.first()
            # Use thumbnail for better performance (300x300)
            image_url = primary_image.media_asset.get_thumbnail('small') if (primary_image and primary_image.media_asset) else None

            results.append({
                'product_id': product.id,
                'name': product.name,
                'image_url': image_url,
                'views': product.views_count,
            })

        return results

    @classmethod
    def get_visitor_geography(cls, start_date: datetime, end_date: datetime,
                             limit: int = 10, country_code: Optional[str] = None) -> List[Dict]:
        """
        Get visitor geography breakdown

        Args:
            start_date: Start of period
            end_date: End of period
            limit: Number of countries/regions to return
            country_code: If provided, return regions/cities for this country (drill-down)

        Returns:
            List of dicts with country/region codes and visitor counts
        """
        from geoip.models import VisitorLocation
        import pycountry

        base_query = VisitorLocation.objects.filter(
            first_seen__gte=start_date,
            first_seen__lt=end_date,
            is_bot=False,
            is_admin_traffic=False
        )

        # Drill-down mode: show regions/cities for specific country
        if country_code:
            geography = base_query.filter(
                resolved_country=country_code
            ).exclude(
                resolved_city=''
            ).values(
                'resolved_city',
                'resolved_region'
            ).annotate(
                visitors=Count('id')
            ).order_by('-visitors')[:limit]

            results = []
            for item in geography:
                results.append({
                    'city': item['resolved_city'],
                    'region': item['resolved_region'],
                    'visitors': item['visitors'],
                    'country_code': country_code,
                })

            return results

        # Country-level view
        geography = base_query.exclude(
            resolved_country=''
        ).values(
            'resolved_country'
        ).annotate(
            visitors=Count('id')
        ).order_by('-visitors')[:limit]

        results = []
        for item in geography:
            country_code = item['resolved_country']

            # Get country name
            try:
                country = pycountry.countries.get(alpha_2=country_code)
                country_name = country.name if country else country_code
            except (KeyError, AttributeError):
                country_name = country_code

            # Get flag emoji (Unicode flags: 🇬🇧 = Regional Indicator Symbol Letter G + B)
            flag = ''.join(chr(127397 + ord(c)) for c in country_code.upper())

            results.append({
                'country_code': country_code,
                'country_name': country_name,
                'flag': flag,
                'visitors': item['visitors'],
            })

        return results

    @classmethod
    def get_referrer_stats(cls, start_date: datetime, end_date: datetime,
                          limit: int = 10) -> List[Dict]:
        """
        Get traffic referrer statistics from VisitorLocation referrer_url data.

        Args:
            start_date: Start of period
            end_date: End of period
            limit: Number of referrers to return

        Returns:
            List of dicts with 'source' (domain) and 'visitors' (count)
        """
        from geoip.models import VisitorLocation
        from urllib.parse import urlparse

        visitors_with_referrer = VisitorLocation.objects.filter(
            first_seen__gte=start_date,
            first_seen__lte=end_date,
            is_bot=False,
            is_admin_traffic=False,
        ).exclude(referrer_url='')

        referrer_data = {}
        for visitor in visitors_with_referrer.only('referrer_url'):
            try:
                domain = urlparse(visitor.referrer_url).netloc or 'direct'
                referrer_data[domain] = referrer_data.get(domain, 0) + 1
            except Exception:
                pass

        results = [
            {'source': domain, 'visitors': count}
            for domain, count in sorted(referrer_data.items(), key=lambda x: x[1], reverse=True)
        ]
        return results[:limit]

    @staticmethod
    def determine_grouping(start_date: datetime, end_date: datetime, grouping: Optional[str] = None) -> str:
        """
        Determine appropriate time grouping based on date range

        Args:
            start_date: Start of period
            end_date: End of period
            grouping: Optional manual override ('day', 'week', 'month')

        Returns:
            Grouping type: 'day', 'week', or 'month'
        """
        if grouping and grouping in ['day', 'week', 'month']:
            return grouping

        # Auto-determine based on date range
        duration = (end_date - start_date).days

        if duration <= 31:
            return 'day'  # Up to 1 month: daily
        elif duration <= 90:
            return 'week'  # 1-3 months: weekly
        else:
            return 'month'  # 3+ months: monthly

    @classmethod
    def get_sales_over_time(cls, start_date: datetime, end_date: datetime,
                           compare: bool = True, grouping: Optional[str] = None) -> Dict:
        """
        Get sales revenue over time for charting (PRIMARY CHART)

        Args:
            start_date: Start of period
            end_date: End of period
            compare: Whether to include comparison with previous period
            grouping: Time grouping ('day', 'week', 'month', or None for auto)

        Returns:
            Dict with sales data grouped by time period
        """
        from orders.models import Order

        # Determine grouping
        actual_grouping = cls.determine_grouping(start_date, end_date, grouping)

        # Select appropriate truncation function
        if actual_grouping == 'week':
            trunc_func = TruncWeek
        elif actual_grouping == 'month':
            trunc_func = TruncMonth
        else:
            trunc_func = TruncDate

        # Current period - group by time
        current_sales = Order.objects.filter(
            created_at__gte=start_date,
            created_at__lt=end_date,
            status__in=['processing', 'shipped', 'delivered']
        ).annotate(
            period=trunc_func('created_at')
        ).values('period').annotate(
            revenue=Coalesce(Sum('total_amount_base', output_field=DecimalField()), Sum('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField())),
            orders=Count('id')
        ).order_by('period')

        # Convert to dict for easy lookup
        current_dict = {item['period']: {'revenue': item['revenue'], 'orders': item['orders']}
                       for item in current_sales}

        result = {
            'current': {
                'labels': [],
                'revenue': [],
                'orders': [],
            },
            'grouping': actual_grouping
        }

        # Generate all periods in range
        current = start_date
        while current < end_date:
            if actual_grouping == 'month':
                period_key = current.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                label = current.strftime('%b %Y')
                next_period = (current.replace(day=28) + timedelta(days=4)).replace(day=1)
            elif actual_grouping == 'week':
                # Get Monday of the week
                period_key = (current - timedelta(days=current.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
                label = period_key.strftime('%b %d')
                next_period = period_key + timedelta(days=7)
            else:  # day
                period_key = current.replace(hour=0, minute=0, second=0, microsecond=0)
                label = current.strftime('%b %d')
                next_period = current + timedelta(days=1)

            # Get data for this period
            data = current_dict.get(period_key.date() if actual_grouping == 'day' else period_key,
                                   {'revenue': Decimal('0.00'), 'orders': 0})

            result['current']['labels'].append(label)
            result['current']['revenue'].append(float(data['revenue']))
            result['current']['orders'].append(data['orders'])

            current = next_period

        if compare:
            prev_start, prev_end = cls.get_previous_period(start_date, end_date)

            prev_sales = Order.objects.filter(
                created_at__gte=prev_start,
                created_at__lt=prev_end,
                status__in=['processing', 'shipped', 'delivered']
            ).annotate(
                period=trunc_func('created_at')
            ).values('period').annotate(
                revenue=Coalesce(Sum('total_amount_base', output_field=DecimalField()), Sum('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField())),
                orders=Count('id')
            ).order_by('period')

            prev_dict = {item['period']: {'revenue': item['revenue'], 'orders': item['orders']}
                        for item in prev_sales}

            result['previous'] = {
                'labels': [],
                'revenue': [],
                'orders': [],
            }

            current = prev_start
            while current < prev_end:
                if actual_grouping == 'month':
                    period_key = current.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                    label = current.strftime('%b %Y')
                    next_period = (current.replace(day=28) + timedelta(days=4)).replace(day=1)
                elif actual_grouping == 'week':
                    period_key = (current - timedelta(days=current.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
                    label = period_key.strftime('%b %d')
                    next_period = period_key + timedelta(days=7)
                else:
                    period_key = current.replace(hour=0, minute=0, second=0, microsecond=0)
                    label = current.strftime('%b %d')
                    next_period = current + timedelta(days=1)

                data = prev_dict.get(period_key.date() if actual_grouping == 'day' else period_key,
                                    {'revenue': Decimal('0.00'), 'orders': 0})

                result['previous']['labels'].append(label)
                result['previous']['revenue'].append(float(data['revenue']))
                result['previous']['orders'].append(data['orders'])

                current = next_period

        return result

    @classmethod
    def get_views_over_time_grouped(cls, start_date: datetime, end_date: datetime,
                                    compare: bool = True, grouping: Optional[str] = None) -> Dict:
        """
        Get page views over time with automatic grouping

        Args:
            start_date: Start of period
            end_date: End of period
            compare: Whether to include comparison with previous period
            grouping: Time grouping ('day', 'week', 'month', or None for auto)

        Returns:
            Dict with page view data grouped by time period
        """
        from geoip.models import VisitorLocation

        # Determine grouping
        actual_grouping = cls.determine_grouping(start_date, end_date, grouping)

        # Select appropriate truncation function
        if actual_grouping == 'week':
            trunc_func = TruncWeek
        elif actual_grouping == 'month':
            trunc_func = TruncMonth
        else:
            trunc_func = TruncDate

        # Current period - group by time (exclude bots and admin traffic)
        current_views = VisitorLocation.objects.filter(
            first_seen__gte=start_date,
            first_seen__lt=end_date,
            is_bot=False,
            is_admin_traffic=False
        ).annotate(
            period=trunc_func('first_seen')
        ).values('period').annotate(
            views=Sum('page_views')
        ).order_by('period')

        # Convert to dict for easy lookup
        current_dict = {item['period']: item['views'] for item in current_views}

        result = {
            'current': {
                'labels': [],
                'data': [],
            },
            'grouping': actual_grouping
        }

        # Generate all periods in range
        current = start_date
        while current < end_date:
            if actual_grouping == 'month':
                period_key = current.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                label = current.strftime('%b %Y')
                next_period = (current.replace(day=28) + timedelta(days=4)).replace(day=1)
            elif actual_grouping == 'week':
                period_key = (current - timedelta(days=current.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
                label = period_key.strftime('%b %d')
                next_period = period_key + timedelta(days=7)
            else:
                period_key = current.replace(hour=0, minute=0, second=0, microsecond=0)
                label = current.strftime('%b %d')
                next_period = current + timedelta(days=1)

            result['current']['labels'].append(label)
            result['current']['data'].append(current_dict.get(
                period_key.date() if actual_grouping == 'day' else period_key, 0))

            current = next_period

        if compare:
            prev_start, prev_end = cls.get_previous_period(start_date, end_date)

            prev_views = VisitorLocation.objects.filter(
                first_seen__gte=prev_start,
                first_seen__lt=prev_end,
                is_bot=False,
                is_admin_traffic=False
            ).annotate(
                period=trunc_func('first_seen')
            ).values('period').annotate(
                views=Sum('page_views')
            ).order_by('period')

            prev_dict = {item['period']: item['views'] for item in prev_views}

            result['previous'] = {
                'labels': [],
                'data': [],
            }

            current = prev_start
            while current < prev_end:
                if actual_grouping == 'month':
                    period_key = current.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                    label = current.strftime('%b %Y')
                    next_period = (current.replace(day=28) + timedelta(days=4)).replace(day=1)
                elif actual_grouping == 'week':
                    period_key = (current - timedelta(days=current.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
                    label = period_key.strftime('%b %d')
                    next_period = period_key + timedelta(days=7)
                else:
                    period_key = current.replace(hour=0, minute=0, second=0, microsecond=0)
                    label = current.strftime('%b %d')
                    next_period = current + timedelta(days=1)

                result['previous']['labels'].append(label)
                result['previous']['data'].append(prev_dict.get(
                    period_key.date() if actual_grouping == 'day' else period_key, 0))

                current = next_period

        return result

    @classmethod
    def get_affiliate_summary(cls) -> Dict:
        """
        Get affiliate program summary metrics for dashboard integration

        Returns:
            Dict containing:
            - active_affiliates: Count of active affiliates
            - pending_commissions_amount: Total pending commissions
            - pending_commissions_count: Number of pending commissions
            - approved_commissions_amount: Total approved (unpaid) commissions
            - approved_commissions_count: Number of approved commissions
            - pending_payouts_count: Number of payouts pending/processing
            - pending_payouts_amount: Total amount in pending/processing payouts
        """
        try:
            from affiliate.models import Affiliate, Commission, Payout
        except ImportError:
            # Affiliate app not installed
            return {
                'active_affiliates': 0,
                'pending_commissions_amount': Decimal('0.00'),
                'pending_commissions_count': 0,
                'approved_commissions_amount': Decimal('0.00'),
                'approved_commissions_count': 0,
                'pending_payouts_count': 0,
                'pending_payouts_amount': Decimal('0.00'),
            }

        # Count active affiliates
        active_affiliates = Affiliate.objects.filter(status='active').count()

        # Get pending commissions (awaiting approval) - use base currency amounts
        pending_commissions = Commission.objects.filter(status='pending').aggregate(
            total=Coalesce(Sum('amount_base', output_field=DecimalField()), Sum('amount', output_field=DecimalField()), Value(0, output_field=DecimalField())),
            count=Count('id')
        )

        # Get approved commissions (approved but not yet paid) - use base currency amounts
        approved_commissions = Commission.objects.filter(status='approved').aggregate(
            total=Coalesce(Sum('amount_base', output_field=DecimalField()), Sum('amount', output_field=DecimalField()), Value(0, output_field=DecimalField())),
            count=Count('id')
        )

        # Get pending and processing payouts - use base currency amounts
        pending_payouts = Payout.objects.filter(
            status__in=['pending', 'processing']
        ).aggregate(
            total=Coalesce(Sum('amount_base', output_field=DecimalField()), Sum('amount', output_field=DecimalField()), Value(0, output_field=DecimalField())),
            count=Count('id')
        )

        return {
            'active_affiliates': active_affiliates,
            'pending_commissions_amount': pending_commissions['total'] or Decimal('0.00'),
            'pending_commissions_count': pending_commissions['count'] or 0,
            'approved_commissions_amount': approved_commissions['total'] or Decimal('0.00'),
            'approved_commissions_count': approved_commissions['count'] or 0,
            'pending_payouts_count': pending_payouts['count'] or 0,
            'pending_payouts_amount': pending_payouts['total'] or Decimal('0.00'),
        }

    @classmethod
    def get_loyalty_summary(cls, start_date: datetime, end_date: datetime) -> Dict:
        """
        Get loyalty program summary metrics for dashboard integration

        Args:
            start_date: Start of date range
            end_date: End of date range

        Returns:
            Dict containing:
            - active_members: Count of active loyalty members
            - points_issued: Total points issued in period
            - points_redeemed: Total points redeemed in period
            - redemptions_count: Number of redemptions in period
            - tier_distribution: List of tiers with member counts
        """
        try:
            from loyalty.models import LoyaltyMember, LoyaltyTransaction, LoyaltyRedemption, LoyaltyTier
        except ImportError:
            # Loyalty app not installed
            return {
                'active_members': 0,
                'points_issued': 0,
                'points_redeemed': 0,
                'redemptions_count': 0,
                'tier_distribution': [],
            }

        # Count active members
        active_members = LoyaltyMember.objects.filter(is_active=True).count()

        # Get points issued in period (earn + bonus transactions)
        points_issued = LoyaltyTransaction.objects.filter(
            created_at__gte=start_date,
            created_at__lt=end_date,
            transaction_type__in=['earn', 'bonus']
        ).aggregate(
            total=Coalesce(Sum('points', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )['total'] or 0

        # Get points redeemed in period (redeem transactions - stored as negative values)
        points_redeemed = LoyaltyTransaction.objects.filter(
            created_at__gte=start_date,
            created_at__lt=end_date,
            transaction_type='redeem'
        ).aggregate(
            total=Coalesce(Sum('points', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )['total'] or 0

        # Get redemptions count in period (confirmed + fulfilled)
        redemptions_count = LoyaltyRedemption.objects.filter(
            created_at__gte=start_date,
            created_at__lt=end_date,
            status__in=['confirmed', 'fulfilled']
        ).count()

        # Get tier distribution (all active members by tier)
        tier_distribution = []
        tiers = LoyaltyTier.objects.filter(is_active=True).order_by('rank')

        for tier in tiers:
            member_count = LoyaltyMember.objects.filter(
                is_active=True,
                current_tier=tier
            ).count()

            if member_count > 0:
                tier_distribution.append({
                    'name': tier.name,
                    'color': tier.color if hasattr(tier, 'color') else '#3498db',
                    'member_count': member_count,
                })

        # Members with no tier
        no_tier_count = LoyaltyMember.objects.filter(
            is_active=True,
            current_tier__isnull=True
        ).count()

        if no_tier_count > 0:
            tier_distribution.append({
                'name': 'No Tier',
                'color': '#95a5a6',
                'member_count': no_tier_count,
            })

        return {
            'active_members': active_members,
            'points_issued': int(points_issued),
            'points_redeemed': abs(int(points_redeemed)),  # Make positive for display
            'redemptions_count': redemptions_count,
            'tier_distribution': tier_distribution,
        }

    @classmethod
    def get_email_campaign_roi(cls, start_date: datetime, end_date: datetime, template_id=None) -> Dict:
        """
        Calculate email campaign ROI metrics with 7-day attribution window.

        Args:
            start_date: Start of analysis period
            end_date: End of analysis period
            template_id: Optional template ID to filter by specific template

        Returns:
            Dict containing:
            - overall: Overall metrics (sent, opened, clicked, conversions, revenue, rates)
            - by_template: Per-template breakdown with ROI
        """
        from email_system.models import EmailOutbox, EmailEvent
        from orders.models import Order
        from django.db.models import Count, Sum, Q, F, DecimalField, Value
        from django.db.models.functions import Coalesce

        # Base query for emails in period
        emails_query = EmailOutbox.objects.filter(
            sent_at__gte=start_date,
            sent_at__lt=end_date,
            status='sent'
        )

        if template_id:
            emails_query = emails_query.filter(template_type=template_id)

        # Overall metrics
        total_sent = emails_query.count()

        # Count unique opens (distinct email IDs with 'opened' events)
        opened_emails = EmailEvent.objects.filter(
            email__sent_at__gte=start_date,
            email__sent_at__lt=end_date,
            email__status='sent',
            event_type='opened'
        )
        if template_id:
            opened_emails = opened_emails.filter(email__template_type=template_id)
        total_opened = opened_emails.values('email').distinct().count()

        # Count unique clicks (distinct email IDs with 'clicked' events)
        clicked_emails = EmailEvent.objects.filter(
            email__sent_at__gte=start_date,
            email__sent_at__lt=end_date,
            email__status='sent',
            event_type='clicked'
        )
        if template_id:
            clicked_emails = clicked_emails.filter(email__template_type=template_id)
        total_clicked = clicked_emails.values('email').distinct().count()

        # Count conversions (orders with attributed_email in period)
        # Attribution window: order must be within 7 days of email sent
        conversions_query = Order.objects.filter(
            attributed_email__sent_at__gte=start_date,
            attributed_email__sent_at__lt=end_date,
            created_at__gte=F('attributed_email__sent_at'),
            created_at__lte=F('attributed_email__sent_at') + timedelta(days=7),
            status__in=['delivered', 'processing', 'shipped']
        )
        if template_id:
            conversions_query = conversions_query.filter(attributed_email__template_type=template_id)

        total_conversions = conversions_query.count()
        total_revenue = conversions_query.aggregate(
            revenue=Coalesce(Sum('total_amount_base', output_field=DecimalField()), Sum('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )['revenue'] or Decimal('0.00')

        # Calculate rates
        open_rate = (Decimal(total_opened) / Decimal(total_sent) * 100) if total_sent > 0 else Decimal('0.00')
        click_rate = (Decimal(total_clicked) / Decimal(total_sent) * 100) if total_sent > 0 else Decimal('0.00')
        conversion_rate = (Decimal(total_conversions) / Decimal(total_sent) * 100) if total_sent > 0 else Decimal('0.00')
        revenue_per_email = (total_revenue / Decimal(total_sent)) if total_sent > 0 else Decimal('0.00')

        overall = {
            'total_sent': total_sent,
            'total_opened': total_opened,
            'total_clicked': total_clicked,
            'total_conversions': total_conversions,
            'total_revenue': total_revenue,
            'open_rate': round(open_rate, 2),
            'click_rate': round(click_rate, 2),
            'conversion_rate': round(conversion_rate, 2),
            'revenue_per_email': round(revenue_per_email, 2)
        }

        # Per-template breakdown
        by_template = []

        if not template_id:  # Only show breakdown if not filtering by specific template
            # Get all template types that sent emails in this period
            template_types = emails_query.values_list('template_type', flat=True).distinct()

            for template_type in template_types:
                if not template_type:
                    continue

                template_emails = emails_query.filter(template_type=template_type)
                sent_count = template_emails.count()

                # Opens for this template
                opened_count = EmailEvent.objects.filter(
                    email__sent_at__gte=start_date,
                    email__sent_at__lt=end_date,
                    email__status='sent',
                    email__template_type=template_type,
                    event_type='opened'
                ).values('email').distinct().count()

                # Clicks for this template
                clicked_count = EmailEvent.objects.filter(
                    email__sent_at__gte=start_date,
                    email__sent_at__lt=end_date,
                    email__status='sent',
                    email__template_type=template_type,
                    event_type='clicked'
                ).values('email').distinct().count()

                # Conversions for this template
                template_conversions = Order.objects.filter(
                    attributed_email__sent_at__gte=start_date,
                    attributed_email__sent_at__lt=end_date,
                    attributed_email__template_type=template_type,
                    created_at__gte=F('attributed_email__sent_at'),
                    created_at__lte=F('attributed_email__sent_at') + timedelta(days=7),
                    status__in=['delivered', 'processing', 'shipped']
                )

                conversions_count = template_conversions.count()
                template_revenue = template_conversions.aggregate(
                    revenue=Coalesce(Sum('total_amount_base', output_field=DecimalField()), Sum('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField()))
                )['revenue'] or Decimal('0.00')

                # Calculate ROI (revenue per email sent)
                roi = (template_revenue / Decimal(sent_count)) if sent_count > 0 else Decimal('0.00')

                by_template.append({
                    'template_name': template_type.replace('_', ' ').title(),
                    'template_id': template_type,
                    'sent': sent_count,
                    'opened': opened_count,
                    'clicked': clicked_count,
                    'conversions': conversions_count,
                    'revenue': template_revenue,
                    'roi': round(roi, 2)
                })

            # Sort by revenue descending
            by_template.sort(key=lambda x: x['revenue'], reverse=True)

        return {
            'overall': overall,
            'by_template': by_template
        }

    @classmethod
    def get_customer_messages(cls, limit: int = 10) -> List[Dict]:
        """
        Get recent customer messages from OrderNotes for inbox display

        Args:
            limit: Maximum number of messages to return (default 10)

        Returns:
            List of dicts with message details:
            - id: OrderNote ID
            - order_number: Order number
            - order_id: Order ID for linking
            - customer_name: Customer full name or username
            - customer_email: Customer email
            - message: Note content (truncated to 100 chars)
            - message_full: Full note content
            - is_read: Whether merchant has read this
            - created_at: When message was sent
            - days_ago: Days since message was sent
        """
        from orders.models import OrderNote

        # Get customer notes (is_customer_note=True), ordered by unread first, then by recent
        customer_notes = OrderNote.objects.filter(
            is_customer_note=True
        ).select_related('order', 'author').order_by('is_read', '-created_at')[:limit]

        messages = []
        for note in customer_notes:
            # Calculate days since message
            days_ago = (timezone.now() - note.created_at).days

            # Get customer info from order or author
            customer = note.author if note.author else note.order.user
            customer_name = customer.get_full_name() if customer else note.order.shipping_name or 'Guest'
            customer_email = customer.email if customer else note.order.email or ''

            messages.append({
                'id': note.id,
                'order_number': note.order.order_number,
                'order_id': note.order.id,
                'customer_name': customer_name,
                'customer_email': customer_email,
                'message': note.note[:100] + '...' if len(note.note) > 100 else note.note,
                'message_full': note.note,
                'is_read': note.is_read,
                'created_at': note.created_at,
                'days_ago': days_ago,
            })

        return messages

    @classmethod
    def get_shipment_summary(cls, start_date: datetime, end_date: datetime) -> Dict:
        """Get shipment status summary for operational dashboard"""
        try:
            from shipping.models import Shipment
            from orders.models import Order
        except ImportError:
            return {
                'in_transit_count': 0,
                'out_for_delivery_count': 0,
                'delivered_today_count': 0,
                'exception_count': 0,
                'late_shipments': [],
                'late_shipments_count': 0,
            }

        # Get status counts for active shipments (not delivered/canceled/returned)
        in_transit_count = Shipment.objects.filter(status='in_transit').count()
        out_for_delivery_count = Shipment.objects.filter(status='out_for_delivery').count()
        exception_count = Shipment.objects.filter(status='exception').count()

        # Get deliveries completed today
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        delivered_today_count = Shipment.objects.filter(
            status='delivered',
            updated_at__gte=today_start,
            updated_at__lt=today_end
        ).count()

        # Find late shipments (past estimated_delivery_date and not delivered)
        late_shipments = []
        today = timezone.now().date()

        # Query orders with shipments that are late
        late_orders = Order.objects.filter(
            estimated_delivery_date__lt=today,
            shipments__status__in=['created', 'labeled', 'in_transit', 'out_for_delivery', 'exception']
        ).select_related('carrier').prefetch_related('shipments').distinct()

        for order in late_orders[:10]:  # Limit to 10 most recent
            # Get most recent shipment for this order
            shipment = order.shipments.filter(
                status__in=['created', 'labeled', 'in_transit', 'out_for_delivery', 'exception']
            ).first()

            if shipment:
                days_late = (today - order.estimated_delivery_date).days
                late_shipments.append({
                    'order_id': order.id,
                    'order_number': order.order_number,
                    'customer_name': order.shipping_name,
                    'carrier': order.carrier.name if order.carrier else 'Unknown',
                    'tracking_number': shipment.tracking_id or 'N/A',
                    'estimated_delivery': order.estimated_delivery_date,
                    'days_late': days_late,
                    'status': shipment.get_status_display(),
                    'status_code': shipment.status,
                })

        return {
            'in_transit_count': in_transit_count,
            'out_for_delivery_count': out_for_delivery_count,
            'delivered_today_count': delivered_today_count,
            'exception_count': exception_count,
            'late_shipments': late_shipments,
            'late_shipments_count': len(late_shipments),
        }

    @classmethod
    def get_sales_channel_performance(cls, start_date: datetime, end_date: datetime, compare: bool = False) -> Dict:
        """
        Get sales performance broken down by acquisition channel/source.

        This method analyzes revenue, order count, AOV, and conversion rates
        for each sales channel (direct, referral, email, social, etc.).

        Args:
            start_date: Start date for analysis period
            end_date: End date for analysis period
            compare: Whether to include comparison with previous period

        Returns:
            Dict containing:
            - by_channel: List of channel performance dicts with:
                - source: Channel name (direct, email, referral, etc.)
                - source_display: Human-readable name
                - revenue: Total revenue from this channel
                - orders: Number of orders
                - aov: Average order value
                - percentage: Percentage of total revenue
            - total_revenue: Sum of all channel revenue
            - total_orders: Sum of all channel orders
            - previous: Previous period data if compare=True
            - changes: Change percentages if compare=True
        """
        from orders.models import Order
        from django.db.models import Sum, Count, Avg, Q

        # Source display names mapping
        source_names = {
            'direct': 'Direct Traffic',
            'referral': 'Affiliate Referrals',
            'email': 'Email Campaigns',
            'social': 'Social Media',
            'loyalty': 'Loyalty Program',
            'organic': 'Organic Search',
            'utm_tracked': 'UTM Campaigns',
            'web': 'Web',
            'mobile': 'Mobile',
            'unknown': 'Unknown',
        }

        def get_channel_data(period_start, period_end):
            """Calculate channel performance for a period"""
            # Get orders in completed states only
            orders = Order.objects.filter(
                created_at__gte=period_start,
                created_at__lt=period_end,
                status__in=['delivered', 'processing', 'shipped']
            )

            # Calculate per-channel metrics
            channel_stats = orders.values('source').annotate(
                revenue=Coalesce(Sum('total_amount_base', output_field=DecimalField()), Sum('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField())),
                order_count=Count('id'),
                avg_order_value=Coalesce(Avg('total_amount_base', output_field=DecimalField()), Avg('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField()))
            ).order_by('-revenue')

            # Calculate total for percentage calculations
            total_revenue = sum(stat['revenue'] for stat in channel_stats if stat['revenue'])
            total_orders = sum(stat['order_count'] for stat in channel_stats)

            # Format channel data
            by_channel = []
            for stat in channel_stats:
                source = stat['source']
                revenue = stat['revenue'] or Decimal('0')
                order_count = stat['order_count']
                aov = stat['avg_order_value'] or Decimal('0')

                percentage = (revenue / total_revenue * 100) if total_revenue > 0 else Decimal('0')

                by_channel.append({
                    'source': source,
                    'source_display': source_names.get(source, source.replace('_', ' ').title()),
                    'revenue': revenue,
                    'orders': order_count,
                    'aov': aov,
                    'percentage': round(percentage, 2),
                })

            return {
                'by_channel': by_channel,
                'total_revenue': total_revenue,
                'total_orders': total_orders
            }

        # Get current period data
        current_data = get_channel_data(start_date, end_date)

        # Add comparison if requested
        if compare:
            previous_start, previous_end = cls.get_previous_period(start_date, end_date)
            previous_data = get_channel_data(previous_start, previous_end)

            # Calculate changes for each channel and add to channel data
            for current_channel in current_data['by_channel']:
                source = current_channel['source']

                # Find matching previous channel
                prev_channel = next(
                    (c for c in previous_data['by_channel'] if c['source'] == source),
                    {'revenue': Decimal('0'), 'orders': 0, 'aov': Decimal('0')}
                )

                current_channel['revenue_change'] = cls.calculate_percentage_change(
                    current_channel['revenue'],
                    prev_channel['revenue']
                )

                current_channel['order_change'] = cls.calculate_percentage_change(
                    current_channel['orders'],
                    prev_channel['orders']
                )

                current_channel['aov_change'] = cls.calculate_percentage_change(
                    current_channel['aov'],
                    prev_channel['aov']
                )

            # Overall changes
            total_revenue_change = cls.calculate_percentage_change(
                current_data['total_revenue'],
                previous_data['total_revenue']
            )

            total_orders_change = cls.calculate_percentage_change(
                current_data['total_orders'],
                previous_data['total_orders']
            )

            result = {
                'by_channel': current_data['by_channel'],
                'total_revenue': current_data['total_revenue'],
                'total_orders': current_data['total_orders'],
                'previous': {
                    'by_channel': previous_data['by_channel'],
                    'total_revenue': previous_data['total_revenue'],
                    'total_orders': previous_data['total_orders'],
                },
                'changes': {
                    'total_revenue_change': total_revenue_change,
                    'total_orders_change': total_orders_change,
                }
            }
        else:
            result = {
                'by_channel': current_data['by_channel'],
                'total_revenue': current_data['total_revenue'],
                'total_orders': current_data['total_orders'],
            }

        return result

    @classmethod
    def get_conversion_funnel(cls, start_date: datetime, end_date: datetime) -> Dict:
        """
        Get conversion funnel analytics showing drop-offs at each stage

        Funnel stages:
        1. Product Views - Sum of all product views
        2. Add to Cart - Carts created
        3. Checkout Started - CheckoutSession created
        4. Payment Initiated - CheckoutSession reached payment step
        5. Order Completed - Orders placed

        Args:
            start_date: Start of period
            end_date: End of period

        Returns:
            Dict with stages, conversion rates, and drop-offs
        """
        from catalog.models import Product
        from cart.models import Cart, CheckoutSession
        from orders.models import Order

        # Stage 1: Product Views
        # Sum views_count for all products (only counting products viewed in period)
        # Note: Product.views_count is cumulative, so we use VisitorLocation data if available
        # For now, use total views as proxy
        total_product_views = Product.objects.filter(
            status='published',
            views_count__gt=0
        ).aggregate(
            total_views=Sum('views_count')
        )['total_views'] or 0

        # Stage 2: Add to Cart (Carts created in period)
        add_to_cart_count = Cart.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date
        ).count()

        # Stage 3: Checkout Started (CheckoutSession created in period)
        checkout_started_count = CheckoutSession.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date
        ).count()

        # Stage 4: Payment Initiated (CheckoutSession reached payment step)
        payment_steps = ['payment', 'review']  # payment or review steps
        payment_initiated_count = CheckoutSession.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date,
            step_completed__in=payment_steps
        ).count()

        # Stage 5: Orders Completed
        orders_completed = Order.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date
        ).count()

        # Calculate percentages and drop-offs
        stages = []

        # Helper function to calculate percentage
        def calc_percentage(current, total):
            if total == 0:
                return 0
            return round((current / total) * 100, 2)

        # Helper function to calculate drop-off
        def calc_dropoff(current, previous):
            if previous == 0:
                return 0
            return round(((previous - current) / previous) * 100, 2)

        # Stage 1: Product Views (baseline = 100%)
        stages.append({
            'name': 'Product Views',
            'count': total_product_views,
            'percentage': 100.0,
            'drop_off': 0
        })

        # Stage 2: Add to Cart
        stages.append({
            'name': 'Add to Cart',
            'count': add_to_cart_count,
            'percentage': calc_percentage(add_to_cart_count, total_product_views),
            'drop_off': calc_dropoff(add_to_cart_count, total_product_views)
        })

        # Stage 3: Checkout Started
        stages.append({
            'name': 'Checkout Started',
            'count': checkout_started_count,
            'percentage': calc_percentage(checkout_started_count, total_product_views),
            'drop_off': calc_dropoff(checkout_started_count, add_to_cart_count)
        })

        # Stage 4: Payment Initiated
        stages.append({
            'name': 'Payment',
            'count': payment_initiated_count,
            'percentage': calc_percentage(payment_initiated_count, total_product_views),
            'drop_off': calc_dropoff(payment_initiated_count, checkout_started_count)
        })

        # Stage 5: Order Completed
        stages.append({
            'name': 'Order Complete',
            'count': orders_completed,
            'percentage': calc_percentage(orders_completed, total_product_views),
            'drop_off': calc_dropoff(orders_completed, payment_initiated_count)
        })

        # Calculate overall conversion rate (views → orders)
        overall_conversion_rate = calc_percentage(orders_completed, total_product_views)

        # Identify biggest drop-off stage
        biggest_drop_off_stage = None
        max_drop_off = 0
        for i in range(1, len(stages)):
            if stages[i]['drop_off'] > max_drop_off:
                max_drop_off = stages[i]['drop_off']
                biggest_drop_off_stage = f"{stages[i-1]['name']} → {stages[i]['name']}"

        return {
            'stages': stages,
            'overall_conversion_rate': overall_conversion_rate,
            'biggest_drop_off_stage': biggest_drop_off_stage,
            'biggest_drop_off_percentage': max_drop_off
        }

    @classmethod
    def get_traffic_source_analytics(cls, start_date: datetime, end_date: datetime) -> Dict:
        """
        Comprehensive traffic source analytics combining referrers, UTM tracking,
        device data, and conversion metrics.

        Excludes bot and admin traffic from all metrics. Bot/admin traffic is
        reported separately via get_visitor_analytics().

        Args:
            start_date: Start of period
            end_date: End of period

        Returns:
            Dict containing:
                - top_referrers: List of top referrer domains with visitors, conversions, revenue
                - utm_performance: UTM campaign breakdown with full metrics
                - traffic_by_device: Device type breakdown with conversions
                - traffic_trends: Time-series data for visualizations
                - summary_metrics: Overall totals and averages
        """
        from geoip.models import VisitorLocation
        from orders.models import Order
        from urllib.parse import urlparse
        from django.utils import timezone as django_timezone
        from datetime import datetime

        # Convert dates to timezone-aware datetimes to properly filter DateTimeFields
        if isinstance(start_date, datetime):
            start_datetime = start_date
        else:
            start_datetime = django_timezone.make_aware(datetime.combine(start_date, datetime.min.time()))

        if isinstance(end_date, datetime):
            end_datetime = end_date
        else:
            end_datetime = django_timezone.make_aware(datetime.combine(end_date, datetime.max.time()))

        # Real human storefront visitors only (exclude bots and admin traffic)
        visitors = VisitorLocation.objects.filter(
            first_seen__gte=start_datetime,
            first_seen__lte=end_datetime,
            is_bot=False,
            is_admin_traffic=False
        )

        total_visitors = visitors.count()

        # Get orders in period for revenue/conversion calculations
        orders = Order.objects.filter(
            created_at__gte=start_datetime,
            created_at__lte=end_datetime,
            status__in=['processing', 'shipped', 'delivered', 'completed']
        )

        total_orders = orders.count()
        total_revenue = orders.aggregate(
            revenue=Coalesce(Sum('total_amount_base', output_field=DecimalField()), Sum('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )['revenue'] or Decimal('0.00')

        # 1. Top Referrers Analysis
        top_referrers = []
        visitors_with_referrer = visitors.exclude(referrer_url='')

        referrer_data = {}
        for visitor in visitors_with_referrer.only('referrer_url', 'session_key'):
            try:
                parsed = urlparse(visitor.referrer_url)
                domain = parsed.netloc or 'direct'
                if domain not in referrer_data:
                    referrer_data[domain] = {
                        'visitors': 0,
                        'session_keys': []
                    }
                referrer_data[domain]['visitors'] += 1
                referrer_data[domain]['session_keys'].append(visitor.session_key)
            except Exception:
                pass

        for domain, data in referrer_data.items():
            visitors_count = data['visitors']

            conversion_rate = (Decimal(total_orders) / Decimal(total_visitors) * 100) if total_visitors > 0 else Decimal('0.00')
            estimated_conversions = int((Decimal(visitors_count) / Decimal(total_visitors)) * Decimal(total_orders)) if total_visitors > 0 else 0
            estimated_revenue = (total_revenue / Decimal(total_visitors)) * Decimal(visitors_count) if total_visitors > 0 else Decimal('0.00')

            top_referrers.append({
                'domain': domain,
                'visitors': visitors_count,
                'conversions': estimated_conversions,
                'revenue': estimated_revenue,
                'percentage': (Decimal(visitors_count) / Decimal(total_visitors) * 100) if total_visitors > 0 else Decimal('0.00'),
                'conversion_rate': conversion_rate,
            })

        top_referrers.sort(key=lambda x: x['visitors'], reverse=True)
        top_referrers = top_referrers[:10]

        # 2. UTM Campaign Performance
        utm_campaigns = []
        utm_visitors = visitors.exclude(utm_campaign='')

        campaign_groups = utm_visitors.values('utm_source', 'utm_medium', 'utm_campaign').annotate(
            visitor_count=Count('id')
        )

        for group in campaign_groups:
            visitors_count = group['visitor_count']

            conversion_rate = (Decimal(total_orders) / Decimal(total_visitors) * 100) if total_visitors > 0 else Decimal('0.00')
            estimated_orders = int((Decimal(visitors_count) / Decimal(total_visitors)) * Decimal(total_orders)) if total_visitors > 0 else 0
            estimated_revenue = (total_revenue / Decimal(total_visitors)) * Decimal(visitors_count) if total_visitors > 0 else Decimal('0.00')

            utm_campaigns.append({
                'source': group['utm_source'],
                'medium': group['utm_medium'],
                'campaign': group['utm_campaign'],
                'visitors': visitors_count,
                'percentage': (Decimal(visitors_count) / Decimal(total_visitors) * 100) if total_visitors > 0 else Decimal('0.00'),
                'conversions': estimated_orders,
                'conversion_rate': conversion_rate,
                'revenue': estimated_revenue,
                'revenue_per_visitor': estimated_revenue / Decimal(visitors_count) if visitors_count > 0 else Decimal('0.00')
            })

        utm_campaigns.sort(key=lambda x: x['revenue'], reverse=True)

        # 3. Traffic by Device Type
        device_breakdown = []
        device_groups = visitors.values('device_type').annotate(
            visitor_count=Count('id')
        )

        device_config = {
            'desktop': {'icon': 'desktop', 'color': '#3498db'},
            'mobile': {'icon': 'mobile-alt', 'color': '#2ecc71'},
            'tablet': {'icon': 'tablet-alt', 'color': '#9b59b6'},
            'unknown': {'icon': 'question-circle', 'color': '#95a5a6'},
        }

        for group in device_groups:
            device_type = group['device_type']
            visitors_count = group['visitor_count']
            config = device_config.get(device_type, device_config['unknown'])

            overall_conversion = (Decimal(total_orders) / Decimal(total_visitors) * 100) if total_visitors > 0 else Decimal('0.00')

            device_breakdown.append({
                'type': dict(VisitorLocation.DEVICE_TYPE_CHOICES).get(device_type, 'Unknown'),
                'device_code': device_type,
                'count': visitors_count,
                'percentage': (Decimal(visitors_count) / Decimal(total_visitors) * 100) if total_visitors > 0 else Decimal('0.00'),
                'conversion_rate': overall_conversion,
                'icon': config['icon'],
                'color': config['color'],
            })

        device_breakdown.sort(key=lambda x: x['count'], reverse=True)

        # 4. Traffic Sources by Type (Direct, Referral, UTM, Organic)
        direct_traffic = visitors.filter(referrer_url='', utm_source='').count()
        utm_traffic = visitors.exclude(utm_source='').count()
        referral_traffic = visitors.exclude(referrer_url='').exclude(utm_source='').count()

        # Identify organic search traffic via DB query instead of Python loop
        search_engines = ['google.com', 'bing.com', 'yahoo.com', 'duckduckgo.com', 'baidu.com']
        organic_q = Q()
        for se in search_engines:
            organic_q |= Q(referrer_url__icontains=se)
        organic_traffic = visitors_with_referrer.filter(organic_q, utm_source='').count()

        traffic_by_type = [
            {
                'type': 'Direct',
                'count': direct_traffic,
                'percentage': (Decimal(direct_traffic) / Decimal(total_visitors) * 100) if total_visitors > 0 else Decimal('0.00'),
                'color': '#3498db'
            },
            {
                'type': 'UTM Campaigns',
                'count': utm_traffic,
                'percentage': (Decimal(utm_traffic) / Decimal(total_visitors) * 100) if total_visitors > 0 else Decimal('0.00'),
                'color': '#2ecc71'
            },
            {
                'type': 'Organic Search',
                'count': organic_traffic,
                'percentage': (Decimal(organic_traffic) / Decimal(total_visitors) * 100) if total_visitors > 0 else Decimal('0.00'),
                'color': '#9b59b6'
            },
            {
                'type': 'Referral',
                'count': referral_traffic - organic_traffic,
                'percentage': (Decimal(referral_traffic - organic_traffic) / Decimal(total_visitors) * 100) if total_visitors > 0 else Decimal('0.00'),
                'color': '#e74c3c'
            },
        ]

        # 5. Traffic Trends Over Time (daily breakdown)
        from django.db.models.functions import TruncDate

        traffic_trends = list(visitors.annotate(
            date=TruncDate('first_seen')
        ).values('date').annotate(
            visitors=Count('id')
        ).order_by('date'))

        for trend in traffic_trends:
            trend['date'] = trend['date'].strftime('%Y-%m-%d')

        # 6. Summary Metrics
        overall_conversion_rate = (Decimal(total_orders) / Decimal(total_visitors) * 100) if total_visitors > 0 else Decimal('0.00')
        revenue_per_visitor = total_revenue / Decimal(total_visitors) if total_visitors > 0 else Decimal('0.00')

        return {
            'summary': {
                'total_visitors': total_visitors,
                'total_orders': total_orders,
                'total_revenue': total_revenue,
                'conversion_rate': overall_conversion_rate,
                'revenue_per_visitor': revenue_per_visitor,
                'utm_traffic_percentage': (Decimal(utm_traffic) / Decimal(total_visitors) * 100) if total_visitors > 0 else Decimal('0.00'),
                'direct_traffic_percentage': (Decimal(direct_traffic) / Decimal(total_visitors) * 100) if total_visitors > 0 else Decimal('0.00'),
            },
            'top_referrers': top_referrers,
            'utm_campaigns': utm_campaigns[:10],
            'device_breakdown': device_breakdown,
            'traffic_by_type': traffic_by_type,
            'traffic_trends': traffic_trends,
            'best_performing_campaign': utm_campaigns[0] if utm_campaigns else None,
            'best_performing_referrer': top_referrers[0] if top_referrers else None,
        }
