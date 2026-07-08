"""
Customer Service - Core analytics and insights logic
"""
from django.db.models import QuerySet, Count, Sum, Avg, F, Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from typing import Dict, Any, Optional, List, Tuple
from decimal import Decimal
from datetime import datetime, timedelta
import calendar

from ..models import (
    CustomerMetrics, CustomerSegment, AbandonedCart,
    LTVSettings, CustomerCohort
)
from orders.models import Order
from cart.models import Cart, Wishlist
from catalog.models import Product, ProductReview


def _to_decimal(value):
    """Safely extract Decimal from MoneyField values."""
    if value is None:
        return Decimal('0.00')
    if hasattr(value, 'amount'):
        return value.amount
    return Decimal(str(value))


class CustomerService:
    """Service for customer analytics and insights"""

    @staticmethod
    def get_dashboard_summary(user) -> Dict[str, Any]:
        """
        Get dashboard summary for customer

        Args:
            user: User instance

        Returns:
            Dict with dashboard data
        """
        # Get or create customer metrics
        metrics, _ = CustomerMetrics.objects.get_or_create(user=user)

        # Get customer segment
        segment = CustomerSegment.determine_segment_for_user(user)

        # Get recent orders (last 5)
        recent_orders = Order.objects.filter(
            user=user
        ).order_by('-created_at')[:5].values(
            'id', 'order_number', 'status', 'total_amount', 'created_at'
        )

        # Get recently viewed products (last 5)
        from cart.models import RecentlyViewed
        recently_viewed = RecentlyViewed.objects.filter(
            user=user
        ).order_by('-viewed_at')[:5].select_related('product')

        recently_viewed_data = [{
            'id': rv.product.id,
            'name': rv.product.name,
            'slug': rv.product.slug,
            'price': str(rv.product.price),
            'image': rv.product.primary_image_url
        } for rv in recently_viewed]

        # Get recommendations (simple - top 5 products from favorite categories)
        from .recommendation_service import RecommendationService
        recommendations = RecommendationService.get_quick_recommendations(user, limit=5)

        # Check for alerts
        abandoned_carts_count = AbandonedCart.objects.filter(
            user=user,
            recovered=False
        ).count()

        # Get wishlist items
        wishlist = Wishlist.objects.filter(user=user).first()
        wishlist_items = wishlist.items.count() if wishlist else 0

        # Calculate total saved from orders
        total_saved = Order.objects.filter(
            user=user,
            status__in=['processing', 'shipped', 'delivered'],
            discount_amount__gt=0
        ).aggregate(total=Sum('discount_amount'))['total'] or Decimal('0.00')

        # Back-in-stock: pending stock notifications where product is now in stock
        items_back_in_stock = 0
        try:
            from catalog.models import StockNotification
            for notif in StockNotification.objects.filter(
                email=user.email, notified_at__isnull=True
            ).select_related('product'):
                if notif.product.is_in_stock:
                    items_back_in_stock += 1
        except Exception:
            pass

        # On-sale: wishlist items where the product is currently on sale
        items_on_sale = 0
        if wishlist:
            now = timezone.now()
            from cart.models import WishlistItem
            items_on_sale = WishlistItem.objects.filter(
                wishlist=wishlist,
                product__sale_type__in=['fixed_price', 'amount_off', 'percentage_off'],
            ).filter(
                Q(product__sale_start_date__lte=now) | Q(product__sale_start_date__isnull=True),
            ).filter(
                Q(product__sale_end_date__gte=now) | Q(product__sale_end_date__isnull=True),
            ).count()

        return {
            'name': user.get_full_name() or user.username,
            'email': user.email,
            'member_since': user.date_joined,
            'total_orders': metrics.total_orders,
            'total_spent': metrics.total_spent,
            'total_saved': total_saved,
            'loyalty_points': int((metrics.total_spent.amount if hasattr(metrics.total_spent, 'amount') else metrics.total_spent) / 10),  # Simple: 1 point per $10
            'segment': segment.name if segment else 'regular',
            'segment_display': segment.get_name_display() if segment else 'Regular Customer',
            'recent_orders': list(recent_orders),
            'recently_viewed': recently_viewed_data,
            'recommended_products': recommendations,
            'abandoned_carts': abandoned_carts_count,
            'items_back_in_stock': items_back_in_stock,
            'items_on_sale': items_on_sale,
        }

    @staticmethod
    def get_order_statistics(user) -> Dict[str, Any]:
        """
        Get detailed order statistics for customer

        Args:
            user: User instance

        Returns:
            Dict with order statistics
        """
        metrics, _ = CustomerMetrics.objects.get_or_create(user=user)

        # Get order counts by status
        orders = Order.objects.filter(user=user)
        completed_orders = orders.filter(status='delivered').count()
        cancelled_orders = orders.filter(status='cancelled').count()

        # Calculate purchase frequency category
        if metrics.purchase_frequency:
            if metrics.purchase_frequency < 30:
                frequency = 'Very Frequent'
            elif metrics.purchase_frequency < 60:
                frequency = 'Frequent'
            elif metrics.purchase_frequency < 90:
                frequency = 'Occasional'
            else:
                frequency = 'Rare'
        else:
            frequency = 'New Customer'

        # Get wishlist count
        wishlist = Wishlist.objects.filter(user=user).first()
        wishlist_count = wishlist.items.count() if wishlist else 0

        # Get review count
        review_count = ProductReview.objects.filter(user=user).count()

        # Get products viewed (from recently viewed)
        from cart.models import RecentlyViewed
        products_viewed = RecentlyViewed.objects.filter(user=user).count()

        # Compute item-level stats from OrderItem
        from orders.models import OrderItem
        item_stats = OrderItem.objects.filter(
            order__user=user,
            order__status='delivered'
        ).aggregate(
            total_items=Sum('quantity'),
            unique_products=Count('product', distinct=True)
        )
        total_items_purchased = item_stats['total_items'] or 0
        unique_products_purchased = item_stats['unique_products'] or 0

        # Count returns (non-cancelled)
        total_returns = 0
        try:
            from orders.models import ReturnRequest
            total_returns = ReturnRequest.objects.filter(
                user=user
            ).exclude(status='cancelled').count()
        except Exception:
            pass

        # first_purchase_date is a DateTimeField
        first_purchase_date = metrics.first_purchase_date
        if first_purchase_date:
            days_since_first = (timezone.now() - first_purchase_date).days
            first_date = first_purchase_date.date()
        else:
            days_since_first = 0
            first_date = None

        return {
            'total_orders': metrics.total_orders,
            'completed_orders': completed_orders,
            'cancelled_orders': cancelled_orders,
            'average_order_value': metrics.average_order_value,
            'total_items_purchased': total_items_purchased,
            'unique_products_purchased': unique_products_purchased,
            'average_items_per_order': (
                float(total_items_purchased / metrics.total_orders)
                if metrics.total_orders > 0 else 0
            ),
            'days_since_first_order': days_since_first,
            'days_since_last_order': metrics.days_since_last_purchase or 0,
            'average_days_between_orders': float(metrics.purchase_frequency or 0),
            'purchase_frequency_category': frequency,
            'total_returns': total_returns,
            'return_rate': float(metrics.refund_rate),
            'wishlist_items': wishlist_count,
            'reviews_written': review_count,
            'products_viewed': products_viewed,
        }

    @staticmethod
    def _get_favorite_discount_type(user) -> str:
        """Determine the most-used discount type from order history."""
        discount_counts = {}
        try:
            from vouchers.models import AppliedVoucher
            voucher_count = AppliedVoucher.objects.filter(
                order__user=user, order__isnull=False
            ).count()
            if voucher_count > 0:
                discount_counts['voucher'] = voucher_count
        except Exception:
            pass

        gift_card_count = Order.objects.filter(
            user=user, gift_card_discount__gt=0
        ).count()
        if gift_card_count > 0:
            discount_counts['gift_card'] = gift_card_count

        try:
            from orders.models import OrderItem
            sale_count = OrderItem.objects.filter(
                order__user=user,
                discount_value__gt=0
            ).exclude(discount_type='none').values('order').distinct().count()
            if sale_count > 0:
                discount_counts['sale'] = sale_count
        except Exception:
            pass

        try:
            from loyalty.models import LoyaltyRedemption
            loyalty_count = LoyaltyRedemption.objects.filter(
                member__customer=user,
                order__isnull=False,
                status__in=['confirmed', 'fulfilled']
            ).count()
            if loyalty_count > 0:
                discount_counts['loyalty'] = loyalty_count
        except Exception:
            pass

        if discount_counts:
            return max(discount_counts, key=discount_counts.get)
        return 'none'

    @staticmethod
    def get_spending_insights(user) -> Dict[str, Any]:
        """
        Get spending insights and trends for customer

        Args:
            user: User instance

        Returns:
            Dict with spending insights
        """
        metrics, _ = CustomerMetrics.objects.get_or_create(user=user)

        # Get orders from last 12 months
        twelve_months_ago = timezone.now() - timedelta(days=365)
        orders = Order.objects.filter(
            user=user,
            created_at__gte=twelve_months_ago,
            status__in=['processing', 'shipped', 'delivered']
        )

        # Calculate monthly spending
        monthly_data = {}
        for order in orders:
            month_key = order.created_at.strftime('%Y-%m')
            if month_key not in monthly_data:
                monthly_data[month_key] = Decimal('0.00')
            monthly_data[month_key] += _to_decimal(order.total_amount)

        # Format monthly spending for chart
        monthly_spending = [
            {
                'month': month,
                'amount': str(amount)
            }
            for month, amount in sorted(monthly_data.items())
        ]

        # Determine spending trend
        if len(monthly_spending) >= 3:
            recent_avg = sum(Decimal(m['amount']) for m in monthly_spending[-3:]) / 3
            earlier_avg = sum(Decimal(m['amount']) for m in monthly_spending[:3]) / 3

            if recent_avg > earlier_avg * Decimal('1.1'):
                trend = 'increasing'
            elif recent_avg < earlier_avg * Decimal('0.9'):
                trend = 'decreasing'
            else:
                trend = 'stable'
        else:
            trend = 'insufficient_data'

        # Calculate average monthly spend
        if monthly_data:
            avg_monthly = sum(monthly_data.values()) / len(monthly_data)
            highest_month = max(monthly_data.values())
            lowest_month = min(monthly_data.values())
        else:
            avg_monthly = Decimal('0.00')
            highest_month = Decimal('0.00')
            lowest_month = Decimal('0.00')

        # Get top categories
        top_categories = []
        if metrics.favorite_category:
            top_categories = [metrics.favorite_category]

        # Get category spending (from order items)
        from orders.models import OrderItem
        category_spending = {}
        order_items = OrderItem.objects.filter(
            order__user=user,
            order__status__in=['processing', 'shipped', 'delivered']
        ).select_related('product')

        for item in order_items:
            if item.product and item.product.category:
                cat_name = item.product.category.name
                if cat_name not in category_spending:
                    category_spending[cat_name] = Decimal('0.00')
                category_spending[cat_name] += _to_decimal(item.total_price)

        # Convert to string for JSON serialization
        category_spending_str = {k: str(v) for k, v in category_spending.items()}

        # Get top brands from order history
        from orders.models import OrderItem
        brand_counts = {}
        brand_items = OrderItem.objects.filter(
            order__user=user,
            order__status__in=['processing', 'shipped', 'delivered'],
            product__brand__isnull=False
        ).select_related('product__brand')
        for item in brand_items:
            if item.product and item.product.brand:
                bname = item.product.brand.name
                brand_counts[bname] = brand_counts.get(bname, 0) + item.quantity
        top_brands = sorted(brand_counts, key=brand_counts.get, reverse=True)[:5]

        # Calculate brand loyalty score (0-100)
        if top_brands and metrics.total_orders > 0:
            top_brand_orders = OrderItem.objects.filter(
                order__user=user,
                product__brand__name=top_brands[0]
            ).values('order').distinct().count()

            loyalty_score = (top_brand_orders / metrics.total_orders * 100)
        else:
            loyalty_score = 0

        # Shopping patterns
        orders_with_time = Order.objects.filter(user=user).values_list('created_at', flat=True)
        if orders_with_time:
            # Peak shopping day
            day_counts = {}
            for dt in orders_with_time:
                day = calendar.day_name[dt.weekday()]
                day_counts[day] = day_counts.get(day, 0) + 1
            peak_day = max(day_counts.items(), key=lambda x: x[1])[0] if day_counts else 'N/A'

            # Peak shopping hour
            hour_counts = {}
            for dt in orders_with_time:
                hour = dt.hour
                hour_counts[hour] = hour_counts.get(hour, 0) + 1
            peak_hour = max(hour_counts.items(), key=lambda x: x[1])[0] if hour_counts else 0
        else:
            peak_day = 'N/A'
            peak_hour = 0

        # Discount usage
        orders_with_discounts = Order.objects.filter(
            user=user,
            discount_amount__gt=0
        ).count()

        discount_rate = (orders_with_discounts / metrics.total_orders * 100) if metrics.total_orders > 0 else 0

        return {
            'total_lifetime_spent': metrics.total_spent,
            'average_monthly_spend': avg_monthly,
            'highest_month_spend': highest_month,
            'lowest_month_spend': lowest_month,
            'monthly_spending': monthly_spending,
            'spending_trend': trend,
            'top_categories': top_categories,
            'category_spending': category_spending_str,
            'top_brands': top_brands,
            'brand_loyalty_score': float(loyalty_score),
            'peak_shopping_day': peak_day,
            'peak_shopping_hour': peak_hour,
            'average_cart_size': metrics.average_order_value,
            'orders_with_discounts': orders_with_discounts,
            'discount_usage_rate': float(discount_rate),
            'favorite_discount_type': CustomerService._get_favorite_discount_type(user)
        }

    @staticmethod
    def get_lifetime_value(user) -> Dict[str, Any]:
        """
        Get customer lifetime value metrics using configured calculation method

        This method retrieves the LTV that was previously calculated by the
        CustomerMetrics.calculate_for_user() method, which uses the configured
        calculation method (simple/cohort/probabilistic) from LTVSettings.

        Args:
            user: User instance

        Returns:
            Dict with LTV data including:
                - total_revenue: Historical spend
                - lifetime_value: Calculated LTV from CustomerMetrics
                - predicted_ltv: Future value projection
                - calculation_method: Method used (simple/cohort/probabilistic)
                - confidence: Confidence score (0-100)
                - confidence_level: high/medium/low classification
                - value_tier: platinum/gold/silver/bronze
                - engagement_score: Customer engagement (0-100)
                - churn_risk: high/medium/low
                - Additional probabilistic fields if available
        """
        metrics, _ = CustomerMetrics.objects.get_or_create(user=user)
        settings = LTVSettings.get_settings()

        # Get the calculated LTV value from metrics
        # This was calculated by CustomerMetrics.calculate_for_user()
        ltv_val = metrics.lifetime_value
        total_val = metrics.total_spent
        calculated_ltv = float(ltv_val.amount if hasattr(ltv_val, 'amount') else ltv_val) if ltv_val else float(total_val.amount if hasattr(total_val, 'amount') else total_val)

        # Get calculation method used
        calculation_method = metrics.ltv_calculation_method or settings.calculation_method

        # Get confidence score
        if metrics.ltv_confidence_score is not None:
            # Use the confidence from probabilistic calculation (0-100)
            confidence_score = float(metrics.ltv_confidence_score)
            if confidence_score >= 80:
                confidence_level = 'high'
            elif confidence_score >= 50:
                confidence_level = 'medium'
            else:
                confidence_level = 'low'
        else:
            # Simple/cohort method - base confidence on order history
            if metrics.total_orders >= 10:
                confidence_level = 'high'
                confidence_score = 85.0
            elif metrics.total_orders >= 5:
                confidence_level = 'medium'
                confidence_score = 65.0
            else:
                confidence_level = 'low'
                confidence_score = 35.0

        # Calculate simple future projection for comparison
        # (This is different from calculated_ltv which uses the configured method)
        if metrics.purchase_frequency and metrics.average_order_value:
            days_in_2_years = 730
            projected_orders = days_in_2_years / max(metrics.purchase_frequency, 1)
            simple_projected_ltv = metrics.total_spent + (projected_orders * metrics.average_order_value)
        else:
            simple_projected_ltv = metrics.total_spent

        # Determine value tier
        total_spent = float(metrics.total_spent.amount if hasattr(metrics.total_spent, 'amount') else metrics.total_spent)
        if total_spent >= 10000:
            value_tier = 'platinum'
        elif total_spent >= 5000:
            value_tier = 'gold'
        elif total_spent >= 1000:
            value_tier = 'silver'
        else:
            value_tier = 'bronze'

        # Calculate percentile (simplified - would need all customer data for accuracy)
        if value_tier == 'platinum':
            percentile = 99
        elif value_tier == 'gold':
            percentile = 90
        elif value_tier == 'silver':
            percentile = 70
        else:
            percentile = 50

        # Calculate engagement score (0-100)
        engagement_factors = []

        # Recent activity (40 points)
        if metrics.days_since_last_purchase:
            if metrics.days_since_last_purchase < 30:
                engagement_factors.append(40)
            elif metrics.days_since_last_purchase < 60:
                engagement_factors.append(30)
            elif metrics.days_since_last_purchase < 90:
                engagement_factors.append(20)
            else:
                engagement_factors.append(10)

        # Order frequency (30 points)
        if metrics.total_orders >= 10:
            engagement_factors.append(30)
        elif metrics.total_orders >= 5:
            engagement_factors.append(20)
        elif metrics.total_orders >= 2:
            engagement_factors.append(10)

        # Reviews and engagement (30 points)
        review_count = ProductReview.objects.filter(user=user).count()
        wishlist = Wishlist.objects.filter(user=user).first()
        wishlist_count = wishlist.items.count() if wishlist else 0

        if review_count >= 5 or wishlist_count >= 10:
            engagement_factors.append(30)
        elif review_count >= 2 or wishlist_count >= 5:
            engagement_factors.append(20)
        elif review_count >= 1 or wishlist_count >= 1:
            engagement_factors.append(10)

        engagement_score = sum(engagement_factors)

        # Determine churn risk
        if metrics.days_since_last_purchase:
            if metrics.days_since_last_purchase > 180:
                churn_risk = 'high'
            elif metrics.days_since_last_purchase > 90:
                churn_risk = 'medium'
            else:
                churn_risk = 'low'
        else:
            churn_risk = 'unknown'

        # Calculate months active
        if metrics.first_purchase_date:
            months_active = ((timezone.now() - metrics.first_purchase_date).days // 30)
        else:
            months_active = 0

        # Build response
        result = {
            # Core metrics
            'total_revenue': metrics.total_spent,
            'total_orders': metrics.total_orders,
            'average_order_value': metrics.average_order_value,

            # LTV calculations
            'lifetime_value': calculated_ltv,  # From configured method
            'predicted_ltv': simple_projected_ltv,  # Simple projection for comparison
            'calculation_method': calculation_method,
            'ltv_last_calculated': metrics.ltv_last_calculated,

            # Confidence metrics
            'confidence_score': confidence_score,
            'confidence_level': confidence_level,

            # Value tier and percentile
            'value_tier': value_tier,
            'percentile': percentile,

            # Engagement and risk
            'engagement_score': float(engagement_score),
            'churn_risk': churn_risk,

            # Customer history
            'customer_since': (metrics.first_purchase_date.date() if metrics.first_purchase_date else user.date_joined.date()),
            'months_active': months_active,
            'last_purchase_date': metrics.last_purchase_date,
            'days_since_last_purchase': metrics.days_since_last_purchase or 0,

            # Cohort data if available
            'cohort_month': metrics.cohort_month.strftime('%Y-%m') if metrics.cohort_month else None,
        }

        # Add probabilistic-specific fields if available
        if calculation_method == 'probabilistic':
            result.update({
                'probability_alive': float(metrics.probability_alive) if metrics.probability_alive else None,
                'predicted_purchases_12m': float(metrics.predicted_purchases_12m) if metrics.predicted_purchases_12m else None,
                'predicted_purchases_24m': float(metrics.predicted_purchases_24m) if metrics.predicted_purchases_24m else None,
            })

        return result

    @staticmethod
    def get_loyalty_status(user) -> Dict[str, Any]:
        """
        Get customer loyalty status and benefits

        Args:
            user: User instance

        Returns:
            Dict with loyalty data
        """
        metrics, _ = CustomerMetrics.objects.get_or_create(user=user)
        segment = CustomerSegment.determine_segment_for_user(user)

        # Calculate loyalty points (1 point per $10 spent)
        spent_amount = metrics.total_spent.amount if hasattr(metrics.total_spent, 'amount') else metrics.total_spent
        loyalty_points = int(spent_amount / 10)

        # Define tier thresholds
        tiers = {
            'VIP': {'points': 500, 'color': '#9333ea'},
            'Gold': {'points': 200, 'color': '#eab308'},
            'Silver': {'points': 100, 'color': '#94a3b8'},
            'Bronze': {'points': 0, 'color': '#cd7f32'},
        }

        # Determine current tier
        current_tier = 'Bronze'
        for tier, data in tiers.items():
            if loyalty_points >= data['points']:
                current_tier = tier
                break

        # Calculate points to next tier
        tier_order = ['Bronze', 'Silver', 'Gold', 'VIP']
        current_index = tier_order.index(current_tier)

        if current_index < len(tier_order) - 1:
            next_tier = tier_order[current_index + 1]
            points_needed = tiers[next_tier]['points']
            points_to_next = points_needed - loyalty_points
            progress = (loyalty_points / points_needed * 100) if points_needed > 0 else 100
        else:
            next_tier = None
            points_to_next = None
            progress = 100.0

        # Define benefits by tier
        benefits_map = {
            'VIP': [
                'Free shipping on all orders',
                '20% off all purchases',
                'Priority customer support',
                'Early access to sales',
                'Exclusive products',
                'Birthday gift'
            ],
            'Gold': [
                'Free shipping on orders over $50',
                '15% off all purchases',
                'Priority shipping',
                'Early access to sales'
            ],
            'Silver': [
                'Free shipping on orders over $100',
                '10% off all purchases',
                'Special member pricing'
            ],
            'Bronze': [
                '5% off first purchase',
                'Member-only deals'
            ]
        }

        current_benefits = benefits_map.get(current_tier, [])
        next_tier_benefits = benefits_map.get(next_tier, []) if next_tier else None

        # Determine next milestone
        if next_tier:
            next_milestone = f"Spend ${points_to_next * 10} more to reach {next_tier} tier"
        else:
            next_milestone = None

        return {
            'segment': segment.name if segment else 'regular',
            'segment_display': segment.get_name_display() if segment else 'Regular Customer',
            'segment_color': segment.color if segment else '#6b7280',
            'tier': current_tier,
            'loyalty_points': loyalty_points,
            'points_to_next_tier': points_to_next,
            'current_benefits': current_benefits,
            'next_tier_benefits': next_tier_benefits,
            'progress_percentage': float(progress),
            'next_milestone': next_milestone,
            'total_spent': metrics.total_spent,
            'orders_count': metrics.total_orders,
            'member_since': (metrics.first_purchase_date.date() if metrics.first_purchase_date else user.date_joined.date()),
        }

    @staticmethod
    def get_revenue_by_segment() -> Dict[str, Any]:
        """
        Get revenue breakdown by customer segment.
        Returns: dict with segment data for chart and analysis
        """
        from django.contrib.auth import get_user_model
        from core.models import SiteSettings

        User = get_user_model()

        # Get default currency
        from core.utils import get_default_currency
        default_currency = get_default_currency()

        # Get active segments from database
        active_segments = CustomerSegment.objects.filter(is_active=True).exclude(name='guest')

        # Build segment data by iterating through users
        segment_totals = {}  # {segment_name: {'revenue': Decimal, 'count': int, 'display_name': str, 'color': str}}

        # Initialize with configured segments
        for segment in active_segments:
            segment_totals[segment.name] = {
                'revenue': Decimal('0'),
                'count': 0,
                'display_name': segment.display_name,
                'color': segment.color,
            }

        # Add "unsegmented" for customers without a segment
        segment_totals['unsegmented'] = {
            'revenue': Decimal('0'),
            'count': 0,
            'display_name': 'Other',
            'color': '#6b7280',
        }

        # Iterate through non-guest users with metrics
        users_with_metrics = User.objects.filter(
            is_active=True,
            customer_metrics__isnull=False
        ).exclude(username__startswith='guest_').select_related('customer_metrics')

        for user in users_with_metrics:
            try:
                metrics = user.customer_metrics
                user_segment = CustomerSegment.determine_segment_for_user(user)

                if user_segment and user_segment.name in segment_totals:
                    segment_key = user_segment.name
                else:
                    segment_key = 'unsegmented'

                segment_totals[segment_key]['revenue'] += metrics.total_spent.amount
                segment_totals[segment_key]['count'] += 1
            except Exception:
                continue

        # Convert to list format
        segments_data = []
        total_revenue = Decimal('0')
        total_customers = 0

        for segment_name, data in segment_totals.items():
            if data['count'] > 0:  # Only include segments with customers
                segments_data.append({
                    'segment': segment_name,
                    'name': data['display_name'],
                    'color': data['color'],
                    'customer_count': data['count'],
                    'revenue': float(data['revenue']),
                })
                total_revenue += data['revenue']
                total_customers += data['count']

        # Calculate percentages
        for segment in segments_data:
            segment['percentage'] = round(
                (segment['revenue'] / float(total_revenue) * 100) if total_revenue > 0 else 0, 1
            )
            segment['customer_percentage'] = round(
                (segment['customer_count'] / total_customers * 100) if total_customers > 0 else 0, 1
            )

        # Sort by revenue descending
        segments_data.sort(key=lambda x: x['revenue'], reverse=True)

        return {
            'segments': segments_data,
            'total_revenue': float(total_revenue),
            'total_customers': total_customers,
            'currency': default_currency,
        }

    @staticmethod
    def get_segment_insights() -> List[Dict[str, Any]]:
        """
        Analyze segment data and generate actionable insights.
        Returns: list of insight dicts with type, title, description, and priority
        """
        insights = []
        segment_data = CustomerService.get_revenue_by_segment()

        if not segment_data['segments'] or segment_data['total_customers'] == 0:
            return [{
                'type': 'info',
                'icon': 'fa-info-circle',
                'title': 'No Segment Data Yet',
                'description': 'Customer segments will appear once customers make purchases.',
                'priority': 1
            }]

        segments = {s['segment']: s for s in segment_data['segments']}

        # Check VIP concentration
        vip = segments.get('vip', {})
        if vip.get('percentage', 0) > 0:
            vip_rev_pct = vip['percentage']
            vip_cust_pct = vip['customer_percentage']

            if vip_rev_pct > 40 and vip_cust_pct < 20:
                insights.append({
                    'type': 'success',
                    'icon': 'fa-crown',
                    'title': 'Strong VIP Revenue Concentration',
                    'description': f'VIP customers are {vip_cust_pct:.0f}% of your base but generate '
                                   f'{vip_rev_pct:.0f}% of revenue. Consider a VIP loyalty program '
                                   f'to retain these high-value customers.',
                    'priority': 2
                })
            elif vip_rev_pct > 0:
                insights.append({
                    'type': 'info',
                    'icon': 'fa-gem',
                    'title': 'VIP Customer Value',
                    'description': f'Your {vip["customer_count"]} VIP customers contribute '
                                   f'${vip["revenue"]:,.0f} ({vip_rev_pct:.0f}% of revenue).',
                    'priority': 3
                })

        # Check at-risk segment
        at_risk = segments.get('at_risk', {})
        if at_risk.get('customer_count', 0) > 0:
            at_risk_revenue = at_risk['revenue']
            at_risk_count = at_risk['customer_count']

            if at_risk_count > 5:
                insights.append({
                    'type': 'warning',
                    'icon': 'fa-exclamation-triangle',
                    'title': f'{at_risk_count} At-Risk Customers',
                    'description': f'These customers represent ${at_risk_revenue:,.0f} in potential '
                                   f'lost revenue. Consider a win-back email campaign or special offer.',
                    'priority': 1
                })

        # Check churned segment
        churned = segments.get('churned', {})
        if churned.get('customer_count', 0) > 0:
            churned_count = churned['customer_count']
            churned_pct = churned['customer_percentage']

            if churned_pct > 30:
                insights.append({
                    'type': 'warning',
                    'icon': 'fa-user-slash',
                    'title': 'High Churn Rate',
                    'description': f'{churned_pct:.0f}% of customers have churned ({churned_count} customers). '
                                   f'Focus on improving early customer experience and engagement.',
                    'priority': 1
                })

        # Check new customer conversion
        new = segments.get('new', {})
        active = segments.get('active', {})
        if new.get('customer_count', 0) > 0 and segment_data['total_customers'] > 10:
            new_count = new['customer_count']
            active_count = active.get('customer_count', 0)
            loyal_count = segments.get('loyal', {}).get('customer_count', 0)
            vip_count = segments.get('vip', {}).get('customer_count', 0)

            converted = active_count + loyal_count + vip_count
            conversion_rate = (converted / (new_count + converted) * 100) if (new_count + converted) > 0 else 0

            if conversion_rate < 30:
                insights.append({
                    'type': 'info',
                    'icon': 'fa-user-plus',
                    'title': 'New Customer Conversion Opportunity',
                    'description': f'Only {conversion_rate:.0f}% of customers progress past "New" status. '
                                   f'Improve post-purchase follow-ups and second-purchase incentives.',
                    'priority': 2
                })

        # Overall health assessment
        healthy_segments = ['vip', 'loyal', 'active']
        healthy_revenue = sum(
            segments.get(s, {}).get('revenue', 0) for s in healthy_segments
        )
        healthy_pct = (healthy_revenue / segment_data['total_revenue'] * 100) if segment_data['total_revenue'] > 0 else 0

        if healthy_pct >= 70:
            insights.append({
                'type': 'success',
                'icon': 'fa-thumbs-up',
                'title': 'Healthy Customer Base',
                'description': f'{healthy_pct:.0f}% of revenue comes from VIP, Loyal, and Active customers. '
                               f'Your customer base is well-engaged!',
                'priority': 3
            })

        # Sort by priority
        insights.sort(key=lambda x: x['priority'])

        return insights

    @staticmethod
    def get_churn_risk_distribution() -> Dict[str, Any]:
        """
        Get distribution of customers by churn risk (probability_alive).
        Returns: dict with risk buckets for chart
        """
        from django.db.models import Count, Avg

        # Define risk buckets
        risk_buckets = {
            'healthy': {'min': 0.7, 'max': 1.0, 'label': 'Healthy', 'color': '#10b981', 'count': 0, 'revenue': 0},
            'moderate': {'min': 0.4, 'max': 0.7, 'label': 'Moderate Risk', 'color': '#f59e0b', 'count': 0, 'revenue': 0},
            'at_risk': {'min': 0.2, 'max': 0.4, 'label': 'At Risk', 'color': '#ef4444', 'count': 0, 'revenue': 0},
            'critical': {'min': 0.0, 'max': 0.2, 'label': 'Critical', 'color': '#dc2626', 'count': 0, 'revenue': 0},
        }

        metrics = CustomerMetrics.objects.exclude(
            user__username__startswith='guest_'
        ).filter(probability_alive__isnull=False)

        for metric in metrics:
            prob = metric.probability_alive
            revenue = float(metric.total_spent.amount)

            for key, bucket in risk_buckets.items():
                if bucket['min'] <= prob < bucket['max'] or (bucket['max'] == 1.0 and prob == 1.0):
                    bucket['count'] += 1
                    bucket['revenue'] += revenue
                    break

        total_customers = sum(b['count'] for b in risk_buckets.values())
        buckets_data = []

        for key, bucket in risk_buckets.items():
            percentage = (bucket['count'] / total_customers * 100) if total_customers > 0 else 0
            buckets_data.append({
                'key': key,
                'label': bucket['label'],
                'count': bucket['count'],
                'percentage': round(percentage, 1),
                'revenue': bucket['revenue'],
                'color': bucket['color'],
            })

        return {
            'buckets': buckets_data,
            'total_customers': total_customers,
        }

    @staticmethod
    def get_churn_risk_insights() -> List[Dict[str, Any]]:
        """
        Analyze churn risk distribution and generate insights.
        """
        insights = []
        data = CustomerService.get_churn_risk_distribution()

        if data['total_customers'] == 0:
            return [{
                'type': 'info',
                'icon': 'fas fa-info-circle',
                'title': 'No Churn Data Yet',
                'description': 'Churn risk data will appear as customer activity is analyzed.',
                'priority': 1
            }]

        buckets = {b['key']: b for b in data['buckets']}

        # Check critical and at-risk combined
        critical = buckets.get('critical', {})
        at_risk = buckets.get('at_risk', {})
        risk_count = critical.get('count', 0) + at_risk.get('count', 0)
        risk_pct = critical.get('percentage', 0) + at_risk.get('percentage', 0)
        risk_revenue = critical.get('revenue', 0) + at_risk.get('revenue', 0)

        if risk_pct > 30:
            insights.append({
                'type': 'danger',
                'icon': 'fas fa-exclamation-circle',
                'title': f'{risk_pct:.0f}% of Customers at Risk',
                'description': f'{risk_count} customers representing ${risk_revenue:,.0f} in past revenue '
                               f'are at risk of churning. Launch a win-back campaign immediately.',
                'priority': 1
            })
        elif risk_pct > 15:
            insights.append({
                'type': 'warning',
                'icon': 'fas fa-exclamation-triangle',
                'title': f'{risk_count} Customers Need Attention',
                'description': f'{risk_pct:.0f}% of your customer base shows churn risk. '
                               f'Consider personalized re-engagement emails.',
                'priority': 2
            })

        # Check healthy percentage
        healthy = buckets.get('healthy', {})
        if healthy.get('percentage', 0) > 60:
            insights.append({
                'type': 'success',
                'icon': 'fas fa-heart',
                'title': 'Healthy Customer Base',
                'description': f'{healthy["percentage"]:.0f}% of customers are healthy and engaged. '
                               f'Keep up the great customer experience!',
                'priority': 3
            })

        insights.sort(key=lambda x: x['priority'])
        return insights

    @staticmethod
    def get_purchase_frequency_distribution() -> Dict[str, Any]:
        """
        Get histogram data for purchase frequency.
        Returns: dict with frequency buckets for chart
        """
        # Define frequency buckets (purchases per month)
        buckets = [
            {'min': 0, 'max': 0.1, 'label': 'Rare (<1/10mo)', 'count': 0},
            {'min': 0.1, 'max': 0.25, 'label': 'Occasional (1/4mo)', 'count': 0},
            {'min': 0.25, 'max': 0.5, 'label': 'Regular (1/2mo)', 'count': 0},
            {'min': 0.5, 'max': 1.0, 'label': 'Frequent (1/mo)', 'count': 0},
            {'min': 1.0, 'max': 2.0, 'label': 'Very Frequent (1-2/mo)', 'count': 0},
            {'min': 2.0, 'max': float('inf'), 'label': 'Power Buyer (2+/mo)', 'count': 0},
        ]

        metrics = CustomerMetrics.objects.exclude(
            user__username__startswith='guest_'
        ).filter(purchase_frequency__gt=0)

        for metric in metrics:
            freq = metric.purchase_frequency
            for bucket in buckets:
                if bucket['min'] <= freq < bucket['max']:
                    bucket['count'] += 1
                    break

        total = sum(b['count'] for b in buckets)
        colors = ['#ef4444', '#f59e0b', '#eab308', '#84cc16', '#10b981', '#059669']

        histogram_data = []
        for i, bucket in enumerate(buckets):
            percentage = (bucket['count'] / total * 100) if total > 0 else 0
            histogram_data.append({
                'label': bucket['label'],
                'count': bucket['count'],
                'percentage': round(percentage, 1),
                'color': colors[i],
            })

        return {
            'histogram': histogram_data,
            'total_customers': total,
        }

    @staticmethod
    def get_frequency_insights() -> List[Dict[str, Any]]:
        """
        Analyze purchase frequency and generate insights.
        """
        insights = []
        data = CustomerService.get_purchase_frequency_distribution()

        if data['total_customers'] == 0:
            return [{
                'type': 'info',
                'icon': 'fas fa-info-circle',
                'title': 'No Frequency Data Yet',
                'description': 'Purchase frequency data will appear once customers make repeat purchases.',
                'priority': 1
            }]

        histogram = data['histogram']

        # Calculate high-frequency vs low-frequency
        low_freq = sum(h['count'] for h in histogram[:2])  # Rare + Occasional
        high_freq = sum(h['count'] for h in histogram[4:])  # Very Frequent + Power Buyer
        total = data['total_customers']

        low_pct = (low_freq / total * 100) if total > 0 else 0
        high_pct = (high_freq / total * 100) if total > 0 else 0

        if high_pct > 20:
            insights.append({
                'type': 'success',
                'icon': 'fas fa-bolt',
                'title': f'{high_pct:.0f}% Power Buyers',
                'description': f'{high_freq} customers purchase frequently. Consider a loyalty rewards '
                               f'program to maintain their engagement.',
                'priority': 2
            })

        if low_pct > 50:
            insights.append({
                'type': 'warning',
                'icon': 'fas fa-clock',
                'title': 'Most Customers Buy Infrequently',
                'description': f'{low_pct:.0f}% of customers purchase rarely. Implement subscription '
                               f'options or reminder emails to increase purchase frequency.',
                'priority': 1
            })

        insights.sort(key=lambda x: x['priority'])
        return insights

    @staticmethod
    def get_predicted_vs_actual() -> Dict[str, Any]:
        """
        Compare predicted purchases vs actual for forecast accuracy.
        Returns: dict with prediction accuracy data
        """
        from django.utils import timezone
        from dateutil.relativedelta import relativedelta

        # Get customers with predictions made at least 12 months ago
        twelve_months_ago = timezone.now() - relativedelta(months=12)

        metrics = CustomerMetrics.objects.exclude(
            user__username__startswith='guest_'
        ).filter(
            ltv_last_calculated__lte=twelve_months_ago,
            predicted_purchases_12m__gt=0
        )

        comparison_data = []
        for metric in metrics[:50]:  # Limit for performance
            # Calculate actual purchases in the 12 months after prediction
            # This is simplified - in production you'd query actual orders
            actual = metric.completed_orders  # Simplified assumption

            comparison_data.append({
                'predicted': metric.predicted_purchases_12m,
                'actual': actual,
            })

        # Calculate accuracy metrics
        if comparison_data:
            total_predicted = sum(d['predicted'] for d in comparison_data)
            total_actual = sum(d['actual'] for d in comparison_data)

            if total_predicted > 0:
                accuracy = min(100, (total_actual / total_predicted) * 100)
            else:
                accuracy = 0

            # Bucket comparison
            under_predicted = sum(1 for d in comparison_data if d['actual'] > d['predicted'] * 1.2)
            over_predicted = sum(1 for d in comparison_data if d['actual'] < d['predicted'] * 0.8)
            accurate = len(comparison_data) - under_predicted - over_predicted
        else:
            accuracy = 0
            under_predicted = 0
            over_predicted = 0
            accurate = 0

        return {
            'accuracy_percentage': round(accuracy, 1),
            'sample_size': len(comparison_data),
            'under_predicted': under_predicted,
            'over_predicted': over_predicted,
            'accurate': accurate,
            'comparison_data': comparison_data[:20],  # For scatter plot
        }

    @staticmethod
    def get_prediction_insights() -> List[Dict[str, Any]]:
        """
        Analyze prediction accuracy and generate insights.
        """
        insights = []
        data = CustomerService.get_predicted_vs_actual()

        if data['sample_size'] == 0:
            return [{
                'type': 'info',
                'icon': 'fas fa-info-circle',
                'title': 'Predictions Need Time',
                'description': 'Prediction accuracy can be measured after 12 months of data collection.',
                'priority': 1
            }]

        accuracy = data['accuracy_percentage']

        if accuracy >= 80:
            insights.append({
                'type': 'success',
                'icon': 'fas fa-bullseye',
                'title': f'{accuracy:.0f}% Prediction Accuracy',
                'description': f'Your purchase predictions are highly accurate. '
                               f'You can confidently use these for inventory and marketing planning.',
                'priority': 2
            })
        elif accuracy >= 50:
            insights.append({
                'type': 'info',
                'icon': 'fas fa-chart-line',
                'title': f'{accuracy:.0f}% Prediction Accuracy',
                'description': f'Predictions are moderately accurate. Consider enriching customer '
                               f'data or adjusting prediction models.',
                'priority': 2
            })
        else:
            insights.append({
                'type': 'warning',
                'icon': 'fas fa-exclamation-triangle',
                'title': 'Low Prediction Accuracy',
                'description': f'Predictions are {accuracy:.0f}% accurate. Review your customer '
                               f'segmentation and ensure data quality.',
                'priority': 1
            })

        insights.sort(key=lambda x: x['priority'])
        return insights
