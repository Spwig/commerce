"""
Savings Service - Track and calculate customer savings
"""
from django.db.models import Sum, Count, Avg, Q, F
from django.utils import timezone
from typing import Dict, Any, List, Optional
from decimal import Decimal
from datetime import timedelta

from orders.models import Order


def _to_decimal(value):
    """Safely extract Decimal from MoneyField aggregation results."""
    if value is None:
        return Decimal('0.00')
    if hasattr(value, 'amount'):
        return value.amount
    return Decimal(str(value))


class SavingsService:
    """Service for calculating and tracking customer savings"""

    @staticmethod
    def calculate_total_savings(user) -> Dict[str, Any]:
        """
        Calculate total savings for customer

        Args:
            user: User instance

        Returns:
            Dict with savings breakdown
        """
        # Get all completed orders with discounts
        orders = Order.objects.filter(
            user=user,
            status__in=['processing', 'shipped', 'delivered']
        )

        # Calculate total savings from order-level discount_amount
        total_saved = _to_decimal(
            orders.aggregate(total=Sum('discount_amount'))['total']
        )

        # Count orders with savings
        orders_with_savings = orders.filter(
            discount_amount__gt=0
        ).count()

        total_orders = orders.count()

        # Calculate average savings per order
        if orders_with_savings > 0:
            avg_savings = total_saved / orders_with_savings
        else:
            avg_savings = Decimal('0.00')

        # Breakdown by type
        voucher_savings = Decimal('0.00')
        loyalty_savings = Decimal('0.00')

        # Get loyalty-generated voucher IDs so we can separate them
        loyalty_voucher_ids = set()
        try:
            from loyalty.models import LoyaltyRedemption
            loyalty_voucher_ids = set(
                LoyaltyRedemption.objects.filter(
                    member__customer=user,
                    order__in=orders,
                    voucher_code__isnull=False,
                    status__in=['confirmed', 'fulfilled']
                ).values_list('voucher_code_id', flat=True)
            )
        except Exception:
            pass

        # Voucher savings (excluding loyalty-generated vouchers)
        try:
            from vouchers.models import AppliedVoucher
            voucher_qs = AppliedVoucher.objects.filter(
                order__in=orders,
                order__isnull=False
            )
            if loyalty_voucher_ids:
                # Loyalty savings from loyalty-generated vouchers
                loyalty_savings = _to_decimal(
                    AppliedVoucher.objects.filter(
                        order__in=orders,
                        voucher_id__in=loyalty_voucher_ids
                    ).aggregate(total=Sum('discount_amount'))['total']
                )
                voucher_qs = voucher_qs.exclude(voucher_id__in=loyalty_voucher_ids)

            voucher_savings = _to_decimal(
                voucher_qs.aggregate(total=Sum('discount_amount'))['total']
            )
        except Exception:
            pass

        # Sale savings = total discount minus what we can attribute to vouchers/loyalty
        sale_savings = max(
            total_saved - voucher_savings - loyalty_savings,
            Decimal('0.00')
        )

        return {
            'total_saved': total_saved,
            'total_orders_with_savings': orders_with_savings,
            'average_savings_per_order': avg_savings,
            'voucher_savings': voucher_savings,
            'sale_savings': sale_savings,
            'loyalty_savings': loyalty_savings,
        }

    @staticmethod
    def _classify_order_discount(order) -> str:
        """
        Determine the primary discount type for an order.
        Uses prefetched data when available.
        """
        sources = []

        # Check for applied vouchers
        try:
            if order.applied_vouchers.all():
                sources.append('voucher')
        except Exception:
            pass

        # Check for gift card discount
        try:
            if order.gift_card_discount and order.gift_card_discount.amount > 0:
                sources.append('gift_card')
        except Exception:
            pass

        # Check for loyalty redemptions
        try:
            if order.loyalty_redemptions.all():
                sources.append('loyalty')
        except Exception:
            pass

        # Check for item-level sale discounts
        try:
            for item in order.items.all():
                if item.discount_type != 'none' and item.discount_value > 0:
                    sources.append('sale')
                    break
        except Exception:
            pass

        if not sources:
            return 'none'
        elif len(sources) == 1:
            return sources[0]
        else:
            return 'mixed'

    @staticmethod
    def get_savings_history(user, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent savings history

        Args:
            user: User instance
            limit: Number of recent savings to return

        Returns:
            List of recent savings
        """
        # Get recent orders with discounts, prefetch related for classification
        orders = Order.objects.filter(
            user=user,
            discount_amount__gt=0,
            status__in=['processing', 'shipped', 'delivered']
        ).prefetch_related(
            'applied_vouchers', 'loyalty_redemptions', 'items'
        ).order_by('-created_at')[:limit]

        recent_savings = []

        for order in orders:
            original_total = _to_decimal(order.total_amount) + _to_decimal(order.discount_amount)
            discount_amt = _to_decimal(order.discount_amount)
            savings_pct = (discount_amt / original_total * 100) if original_total > 0 else Decimal('0')

            recent_savings.append({
                'order_number': order.order_number,
                'order_date': order.created_at,
                'savings_amount': str(order.discount_amount),
                'order_total': str(order.total_amount),
                'original_total': str(original_total),
                'savings_percentage': float(savings_pct),
                'discount_type': SavingsService._classify_order_discount(order),
            })

        return recent_savings

    @staticmethod
    def get_monthly_savings(user, months: int = 12) -> List[Dict[str, Any]]:
        """
        Get monthly savings for the past N months

        Args:
            user: User instance
            months: Number of months to look back

        Returns:
            List of monthly savings data
        """
        # Calculate date range
        end_date = timezone.now()
        start_date = end_date - timedelta(days=months * 30)

        # Get orders in date range
        orders = Order.objects.filter(
            user=user,
            created_at__gte=start_date,
            created_at__lte=end_date,
            status__in=['processing', 'shipped', 'delivered']
        )

        # Group by month
        monthly_data = {}

        for order in orders:
            month_key = order.created_at.strftime('%Y-%m')

            if month_key not in monthly_data:
                monthly_data[month_key] = {
                    'month': month_key,
                    'total_savings': Decimal('0.00'),
                    'orders_count': 0,
                    'orders_with_savings': 0,
                }

            monthly_data[month_key]['orders_count'] += 1

            discount_dec = _to_decimal(order.discount_amount)
            if discount_dec > 0:
                monthly_data[month_key]['total_savings'] += discount_dec
                monthly_data[month_key]['orders_with_savings'] += 1

        # Convert to list and sort
        monthly_savings = sorted(
            [
                {
                    'month': data['month'],
                    'total_savings': str(data['total_savings']),
                    'orders_count': data['orders_count'],
                    'orders_with_savings': data['orders_with_savings'],
                    'savings_rate': float(
                        data['orders_with_savings'] / data['orders_count'] * 100
                    ) if data['orders_count'] > 0 else 0,
                }
                for data in monthly_data.values()
            ],
            key=lambda x: x['month']
        )

        return monthly_savings

    @staticmethod
    def get_best_savings_month(user) -> Dict[str, Any]:
        """
        Find the month with the highest savings

        Args:
            user: User instance

        Returns:
            Dict with best savings month data
        """
        monthly_savings = SavingsService.get_monthly_savings(user, months=12)

        if not monthly_savings:
            return {
                'month': None,
                'total_savings': '0.00',
                'orders_count': 0,
            }

        # Find month with highest savings
        best_month = max(
            monthly_savings,
            key=lambda x: Decimal(x['total_savings'])
        )

        return {
            'month': best_month['month'],
            'total_savings': best_month['total_savings'],
            'orders_count': best_month['orders_count'],
        }

    @staticmethod
    def get_savings_summary(user) -> Dict[str, Any]:
        """
        Get complete savings summary for customer

        Args:
            user: User instance

        Returns:
            Dict with comprehensive savings data
        """
        # Get total savings
        savings_breakdown = SavingsService.calculate_total_savings(user)

        # Get recent savings
        recent_savings = SavingsService.get_savings_history(user, limit=5)

        # Get monthly trends
        monthly_savings = SavingsService.get_monthly_savings(user, months=12)

        # Get best month
        best_month = SavingsService.get_best_savings_month(user)

        return {
            'total_saved': savings_breakdown['total_saved'],
            'total_orders_with_savings': savings_breakdown['total_orders_with_savings'],
            'average_savings_per_order': savings_breakdown['average_savings_per_order'],
            'voucher_savings': savings_breakdown['voucher_savings'],
            'sale_savings': savings_breakdown['sale_savings'],
            'loyalty_savings': savings_breakdown['loyalty_savings'],
            'recent_savings': recent_savings,
            'monthly_savings': monthly_savings,
            'best_savings_month': best_month,
        }

    @staticmethod
    def calculate_potential_savings(user) -> Dict[str, Any]:
        """
        Calculate potential future savings based on available offers

        Args:
            user: User instance

        Returns:
            Dict with potential savings opportunities
        """
        now = timezone.now()

        # 1. Find active, applicable vouchers
        available_vouchers = 0
        potential_voucher_savings = Decimal('0.00')
        try:
            from vouchers.models import VoucherCode
            active_vouchers = VoucherCode.objects.filter(
                is_active=True,
                discount_type__in=['percentage', 'fixed'],
            ).filter(
                Q(start_date__lte=now) | Q(start_date__isnull=True),
            ).filter(
                Q(end_date__gte=now) | Q(end_date__isnull=True),
            ).filter(
                Q(max_uses_total__isnull=True) | Q(current_uses__lt=F('max_uses_total')),
            )

            # Exclude first-time-only vouchers if user already has orders
            has_orders = Order.objects.filter(
                user=user, status='delivered'
            ).exists()
            if has_orders:
                active_vouchers = active_vouchers.exclude(
                    first_time_customers_only=True
                )

            available_vouchers = active_vouchers.count()

            # Estimate potential savings (cap iteration)
            for v in active_vouchers[:10]:
                if v.discount_type == 'fixed':
                    potential_voucher_savings += v.discount_value
                elif v.discount_type == 'percentage' and v.max_discount_amount:
                    potential_voucher_savings += _to_decimal(v.max_discount_amount)
        except Exception:
            pass

        # 2. Check wishlist items currently on sale
        wishlist_items_on_sale = 0
        potential_sale_savings = Decimal('0.00')
        try:
            from cart.models import Wishlist, WishlistItem
            wishlist = Wishlist.objects.filter(user=user).first()
            if wishlist:
                on_sale_items = WishlistItem.objects.filter(
                    wishlist=wishlist,
                    product__sale_type__in=['fixed_price', 'amount_off', 'percentage_off'],
                ).filter(
                    Q(product__sale_start_date__lte=now) | Q(product__sale_start_date__isnull=True),
                ).filter(
                    Q(product__sale_end_date__gte=now) | Q(product__sale_end_date__isnull=True),
                ).select_related('product')

                for wi in on_sale_items:
                    wishlist_items_on_sale += 1
                    sale_price = wi.product.calculate_sale_price()
                    if sale_price is not None:
                        saving = _to_decimal(wi.product.price) - _to_decimal(sale_price)
                        if saving > 0:
                            potential_sale_savings += saving
        except Exception:
            pass

        # 3. Check loyalty tier upgrade benefits
        loyalty_tier_upgrade_benefit = None
        try:
            from loyalty.models import LoyaltyMember
            member = LoyaltyMember.objects.filter(
                customer=user, is_active=True
            ).select_related('current_tier').first()

            if member:
                next_tier = member.get_next_tier()
                if next_tier:
                    loyalty_tier_upgrade_benefit = {
                        'next_tier_name': next_tier.name,
                        'points_multiplier': float(next_tier.points_multiplier),
                    }
        except Exception:
            pass

        return {
            'available_vouchers': available_vouchers,
            'potential_voucher_savings': potential_voucher_savings,
            'wishlist_items_on_sale': wishlist_items_on_sale,
            'potential_sale_savings': potential_sale_savings,
            'loyalty_tier_upgrade_benefit': loyalty_tier_upgrade_benefit,
        }

    @staticmethod
    def get_savings_comparison(user) -> Dict[str, Any]:
        """
        Compare customer's savings to average customer

        Args:
            user: User instance

        Returns:
            Dict with comparison data
        """
        # Get user's savings
        user_savings = SavingsService.calculate_total_savings(user)

        # Calculate platform-wide average savings
        platform_stats = Order.objects.filter(
            status__in=['processing', 'shipped', 'delivered'],
            discount_amount__gt=0
        ).aggregate(
            avg_discount=Avg('discount_amount'),
            total_orders=Count('id'),
            total_customers=Count('user', distinct=True)
        )

        avg_savings = _to_decimal(platform_stats['avg_discount'])
        total_customers = platform_stats['total_customers'] or 0
        if total_customers > 0:
            avg_orders_with_savings = platform_stats['total_orders'] // total_customers
        else:
            avg_orders_with_savings = 0

        # Calculate comparison
        user_total = _to_decimal(user_savings['total_saved'])
        user_orders = user_savings['total_orders_with_savings']

        if user_total > avg_savings:
            comparison = 'above_average'
            difference = user_total - avg_savings
        elif user_total < avg_savings:
            comparison = 'below_average'
            difference = avg_savings - user_total
        else:
            comparison = 'average'
            difference = Decimal('0.00')

        # Calculate actual percentile
        percentile = 0
        if user_total > 0:
            completed_statuses = ['processing', 'shipped', 'delivered']
            customers_below = Order.objects.filter(
                status__in=completed_statuses,
                discount_amount__gt=0
            ).values('user').annotate(
                total_discount=Sum('discount_amount')
            ).filter(
                total_discount__lt=user_total
            ).count()

            total_savers = Order.objects.filter(
                status__in=completed_statuses,
                discount_amount__gt=0
            ).values('user').distinct().count()

            if total_savers > 0:
                percentile = int((customers_below / total_savers) * 100)

        return {
            'user_total_savings': user_total,
            'user_orders_with_savings': user_orders,
            'platform_average_savings': avg_savings,
            'platform_average_orders': avg_orders_with_savings,
            'comparison': comparison,
            'difference': difference,
            'percentile': percentile,
        }
