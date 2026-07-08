"""
Recommendation Service - Product recommendation engine
"""
from django.db.models import Count, Sum, Q, F
from django.utils import timezone
from typing import List, Dict, Any, Optional
from datetime import timedelta
from decimal import Decimal

from catalog.models import Product, Category
from orders.models import OrderItem
from cart.models import Wishlist, RecentlyViewed
from ..models import CustomerMetrics


def _in_stock_q():
    """DB-level approximation of Product.is_in_stock property."""
    return (
        Q(track_inventory=False) |
        Q(allow_backorders=True) |
        Q(stock_items__on_hand__gt=F('stock_items__allocated'))
    )


class RecommendationService:
    """Service for generating product recommendations"""

    @staticmethod
    def get_quick_recommendations(user, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get quick product recommendations for dashboard

        Args:
            user: User instance
            limit: Number of recommendations

        Returns:
            List of product dicts
        """
        recommendations = []

        # Get customer metrics
        try:
            metrics = CustomerMetrics.objects.get(user=user)
            favorite_categories = [metrics.favorite_category] if metrics.favorite_category else []
        except CustomerMetrics.DoesNotExist:
            favorite_categories = []

        if favorite_categories:
            # Get published, in-stock products from favorite categories
            products = Product.objects.filter(status='published').filter(
                category__name__in=favorite_categories,
            ).filter(
                _in_stock_q()
            ).distinct().order_by('-created_at')[:limit]

            for product in products:
                recommendations.append({
                    'id': product.id,
                    'name': product.name,
                    'slug': product.slug,
                    'price': str(product.price),
                    'image': product.primary_image_url,
                    'reason': 'From your favorite categories'
                })

        # If we don't have enough, add trending products
        if len(recommendations) < limit:
            trending = Product.objects.filter(status='published').filter(
                _in_stock_q()
            ).distinct().order_by('-views_count')[:limit - len(recommendations)]

            for product in trending:
                recommendations.append({
                    'id': product.id,
                    'name': product.name,
                    'slug': product.slug,
                    'price': str(product.price),
                    'image': product.primary_image_url,
                    'reason': 'Trending now'
                })

        return recommendations

    @staticmethod
    def get_purchase_recommendations(user) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get comprehensive purchase recommendations

        Args:
            user: User instance

        Returns:
            Dict with different recommendation categories
        """
        # Initialize recommendations
        based_on_history = []
        trending_in_categories = []
        back_in_stock = []
        on_sale = []

        # Get customer's purchase history
        purchased_products = OrderItem.objects.filter(
            order__user=user,
            order__status__in=['processing', 'shipped', 'delivered']
        ).values_list('product_id', flat=True).distinct()

        # Get customer metrics for category preferences
        try:
            metrics = CustomerMetrics.objects.get(user=user)
            favorite_categories = [metrics.favorite_category] if metrics.favorite_category else []
        except CustomerMetrics.DoesNotExist:
            favorite_categories = []

        # 1. Recommendations based on purchase history
        if purchased_products:
            # Get categories from purchased products
            purchased_categories = Product.objects.filter(
                id__in=purchased_products
            ).values_list('category_id', flat=True).distinct()

            # Find similar products in same categories (not already purchased)
            similar_products = Product.objects.filter(status='published').filter(
                category_id__in=purchased_categories,
            ).filter(
                _in_stock_q()
            ).exclude(
                id__in=purchased_products
            ).distinct().order_by('-views_count', '-created_at')[:10]

            for product in similar_products:
                based_on_history.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'product_slug': product.slug,
                    'product_image': product.primary_image_url,
                    'price': product.price,
                    'discount_price': product.effective_price if product.is_on_sale else None,
                    'reason': 'frequently_bought',
                    'confidence_score': 0.8
                })

        # 2. Trending in favorite categories
        if favorite_categories:
            # Get top products from favorite categories (last 30 days)
            thirty_days_ago = timezone.now() - timedelta(days=30)

            trending_products = Product.objects.filter(status='published').filter(
                category__name__in=favorite_categories,
                created_at__gte=thirty_days_ago
            ).filter(
                _in_stock_q()
            ).exclude(
                id__in=purchased_products
            ).distinct().order_by('-views_count')[:10]

            for product in trending_products:
                trending_in_categories.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'product_slug': product.slug,
                    'product_image': product.primary_image_url,
                    'price': product.price,
                    'discount_price': product.effective_price if product.is_on_sale else None,
                    'reason': 'trending',
                    'confidence_score': 0.7
                })

        # 3. Back in stock (from wishlist)
        try:
            wishlist = Wishlist.objects.get(user=user)
            wishlist_products = wishlist.items.filter(
                product__status='published',
                product__is_deleted=False,
            ).filter(
                Q(product__track_inventory=False) |
                Q(product__allow_backorders=True) |
                Q(product__stock_items__on_hand__gt=F('product__stock_items__allocated'))
            ).select_related('product').distinct()[:10]

            for item in wishlist_products:
                back_in_stock.append({
                    'product_id': item.product.id,
                    'product_name': item.product.name,
                    'product_slug': item.product.slug,
                    'product_image': item.product.primary_image_url,
                    'price': item.product.price,
                    'discount_price': item.product.effective_price if item.product.is_on_sale else None,
                    'reason': 'back_in_stock',
                    'confidence_score': 0.9
                })
        except Wishlist.DoesNotExist:
            pass

        # 4. On sale products (from favorite categories or previously viewed)
        now = timezone.now()
        sale_filter = Q(
            sale_type__in=['fixed_price', 'amount_off', 'percentage_off'],
            status='published',
            is_deleted=False,
        ) & (
            Q(sale_start_date__lte=now) | Q(sale_start_date__isnull=True)
        ) & (
            Q(sale_end_date__gte=now) | Q(sale_end_date__isnull=True)
        )

        if favorite_categories:
            sale_filter &= Q(category__name__in=favorite_categories)

        sale_products = Product.objects.filter(
            sale_filter
        ).filter(
            _in_stock_q()
        ).exclude(
            id__in=purchased_products
        ).distinct().order_by('-created_at')[:10]

        for product in sale_products:
            sale_price = product.calculate_sale_price()
            if sale_price is not None and product.price.amount > 0:
                discount_amount = product.price.amount - sale_price
                discount_pct = (discount_amount / product.price.amount * 100)
            else:
                discount_pct = Decimal('0')

            on_sale.append({
                'product_id': product.id,
                'product_name': product.name,
                'product_slug': product.slug,
                'product_image': product.primary_image_url,
                'price': product.price,
                'discount_price': product.effective_price,
                'reason': f'on_sale_{int(discount_pct)}%_off',
                'confidence_score': 0.6
            })

        return {
            'based_on_history': based_on_history,
            'trending_in_categories': trending_in_categories,
            'back_in_stock': back_in_stock,
            'on_sale': on_sale,
        }

    @staticmethod
    def get_favorite_products(user, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get customer's favorite/most purchased products

        Args:
            user: User instance
            limit: Number of products to return

        Returns:
            List of favorite products with purchase stats
        """
        # Get most purchased products
        product_purchases = OrderItem.objects.filter(
            order__user=user,
            order__status__in=['processing', 'shipped', 'delivered']
        ).values('product').annotate(
            times_purchased=Count('id'),
            total_spent=Sum('total_price'),
            last_purchased=F('order__created_at')
        ).order_by('-times_purchased')[:limit]

        favorite_products = []

        for item in product_purchases:
            try:
                product = Product.objects.get(id=item['product'])
                favorite_products.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'product_slug': product.slug,
                    'product_image': product.primary_image_url,
                    'times_purchased': item['times_purchased'],
                    'total_spent': item['total_spent'],
                    'last_purchased': item['last_purchased'],
                    'current_price': product.price,
                    'is_on_sale': product.is_on_sale,
                })
            except Product.DoesNotExist:
                continue

        return favorite_products

    @staticmethod
    def get_favorite_categories(user, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get customer's favorite categories

        Args:
            user: User instance
            limit: Number of categories to return

        Returns:
            List of favorite categories with stats
        """
        # Get categories from order items
        category_purchases = OrderItem.objects.filter(
            order__user=user,
            order__status__in=['processing', 'shipped', 'delivered'],
            product__category__isnull=False
        ).values(
            'product__category__id',
            'product__category__name',
            'product__category__slug'
        ).annotate(
            order_count=Count('order', distinct=True),
            items_purchased=Count('id'),
            total_spent=Sum('total_price')
        ).order_by('-total_spent')[:limit]

        favorite_categories = []

        for item in category_purchases:
            favorite_categories.append({
                'category_id': item['product__category__id'],
                'category_name': item['product__category__name'],
                'category_slug': item['product__category__slug'],
                'order_count': item['order_count'],
                'items_purchased': item['items_purchased'],
                'total_spent': str(item['total_spent']),
            })

        return favorite_categories

    @staticmethod
    def get_favorite_brands(user, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get customer's favorite brands

        Args:
            user: User instance
            limit: Number of brands to return

        Returns:
            List of favorite brands with stats
        """
        # Get brands from order items
        brand_purchases = OrderItem.objects.filter(
            order__user=user,
            order__status__in=['processing', 'shipped', 'delivered'],
            product__brand__isnull=False
        ).values(
            'product__brand__id',
            'product__brand__name',
            'product__brand__slug'
        ).annotate(
            order_count=Count('order', distinct=True),
            items_purchased=Count('id'),
            total_spent=Sum('total_price')
        ).order_by('-total_spent')[:limit]

        favorite_brands = []

        for item in brand_purchases:
            favorite_brands.append({
                'brand_id': item['product__brand__id'],
                'brand_name': item['product__brand__name'],
                'brand_slug': item['product__brand__slug'],
                'order_count': item['order_count'],
                'items_purchased': item['items_purchased'],
                'total_spent': str(item['total_spent']),
            })

        return favorite_brands

    @staticmethod
    def get_recently_purchased(user, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recently purchased products

        Args:
            user: User instance
            limit: Number of products to return

        Returns:
            List of recently purchased products
        """
        # Get recent order items
        recent_items = OrderItem.objects.filter(
            order__user=user,
            order__status__in=['processing', 'shipped', 'delivered']
        ).select_related('product').order_by('-order__created_at')[:limit]

        recently_purchased = []
        seen_products = set()

        for item in recent_items:
            # Avoid duplicates
            if item.product_id in seen_products:
                continue

            seen_products.add(item.product_id)

            if item.product:
                recently_purchased.append({
                    'product_id': item.product.id,
                    'product_name': item.product.name,
                    'product_slug': item.product.slug,
                    'product_image': item.product.primary_image_url,
                    'times_purchased': 1,  # Would need aggregation for accurate count
                    'total_spent': item.total_price,
                    'last_purchased': item.order.created_at,
                    'current_price': item.product.price,
                    'is_on_sale': item.product.is_on_sale,
                })

        return recently_purchased
