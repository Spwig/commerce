"""
Cart Recommendation Service - Intelligent product suggestions for empty cart state

Provides personalized recommendations based on:
- Recently viewed products (session or user-based)
- Related products (same category/brand)
- On-sale items
- Trending/bestselling products
- Featured products as fallback
"""
from typing import List, Dict, Any, Optional, Set
from django.db.models import Q, Count, Exists, OuterRef, Sum, F
from django.urls import reverse

from catalog.models import Product, StockItem
from cart.models import RecentlyViewed


class CartRecommendationService:
    """
    Service for generating intelligent empty cart recommendations.

    Supports both authenticated and anonymous users via session-based
    recently viewed tracking.
    """

    @staticmethod
    def _get_in_stock_filter():
        """
        Returns a Q filter for products that are in stock.
        Products are considered in stock if:
        - track_inventory is False (unlimited), OR
        - track_inventory is True AND has StockItem with on_hand > allocated
        """
        # Subquery to check if product has available stock
        has_available_stock = StockItem.objects.filter(
            product_id=OuterRef('pk'),
            variant_id__isnull=True  # Product-level stock (not variant-specific)
        ).annotate(
            available=F('on_hand') - F('allocated')
        ).filter(
            available__gt=0
        )

        return Q(track_inventory=False) | Q(
            track_inventory=True,
            pk__in=Exists(has_available_stock)
        )

    @staticmethod
    def _filter_in_stock(queryset):
        """
        Filter a queryset to only include products that are in stock.
        """
        # Products with track_inventory=False are always in stock
        # Products with track_inventory=True need positive stock
        has_stock_subquery = StockItem.objects.filter(
            product_id=OuterRef('pk'),
            variant_id__isnull=True
        ).values('product_id').annotate(
            total_available=Sum(F('on_hand') - F('allocated'))
        ).filter(
            total_available__gt=0
        ).values('product_id')

        return queryset.filter(
            Q(track_inventory=False) |
            Q(track_inventory=True, pk__in=has_stock_subquery)
        )

    @staticmethod
    def get_empty_cart_recommendations(request, limit: int = 6) -> Dict[str, Any]:
        """
        Get intelligent recommendations for empty cart state.

        Returns structured sections with labels for UI display.

        Args:
            request: Django request object
            limit: Total number of products across all sections

        Returns:
            {
                "sections": [
                    { "type": "recently_viewed", "label": "Continue Shopping", "products": [...] },
                    { "type": "on_sale", "label": "On Sale Now", "products": [...] },
                    { "type": "trending", "label": "Popular Right Now", "products": [...] }
                ],
                "total_count": int
            }
        """
        sections = []
        used_product_ids: Set[int] = set()

        # 1. Recently viewed products (max 2)
        recently_viewed = CartRecommendationService._get_recently_viewed_products(
            request, limit=2, exclude_ids=used_product_ids
        )
        if recently_viewed:
            sections.append({
                'type': 'recently_viewed',
                'label': 'Continue Shopping',
                'products': recently_viewed
            })
            used_product_ids.update(p['id'] for p in recently_viewed)

        # 2. Related to recently viewed (same category, max 2)
        if recently_viewed:
            # Get categories from recently viewed
            recently_viewed_ids = [p['id'] for p in recently_viewed]
            related = CartRecommendationService._get_related_to_viewed(
                viewed_product_ids=recently_viewed_ids,
                exclude_ids=used_product_ids,
                limit=2
            )
            if related:
                sections.append({
                    'type': 'related',
                    'label': 'You Might Also Like',
                    'products': related
                })
                used_product_ids.update(p['id'] for p in related)

        # 3. On-sale products (max 2)
        remaining_slots = limit - len(used_product_ids)
        if remaining_slots > 0:
            on_sale = CartRecommendationService._get_on_sale_products(
                exclude_ids=used_product_ids,
                limit=min(2, remaining_slots)
            )
            if on_sale:
                sections.append({
                    'type': 'on_sale',
                    'label': 'On Sale Now',
                    'products': on_sale
                })
                used_product_ids.update(p['id'] for p in on_sale)

        # 4. Trending/Popular products (fill remaining)
        remaining_slots = limit - len(used_product_ids)
        if remaining_slots > 0:
            trending = CartRecommendationService._get_trending_products(
                exclude_ids=used_product_ids,
                limit=remaining_slots
            )
            if trending:
                sections.append({
                    'type': 'trending',
                    'label': 'Popular Right Now',
                    'products': trending
                })
                used_product_ids.update(p['id'] for p in trending)

        # 5. Fallback: Featured products if we still need more
        remaining_slots = limit - len(used_product_ids)
        if remaining_slots > 0:
            featured = CartRecommendationService._get_featured_products(
                exclude_ids=used_product_ids,
                limit=remaining_slots
            )
            if featured:
                # Merge into trending section if exists, otherwise create new
                trending_section = next(
                    (s for s in sections if s['type'] == 'trending'), None
                )
                if trending_section:
                    trending_section['products'].extend(featured)
                else:
                    sections.append({
                        'type': 'featured',
                        'label': 'Recommended For You',
                        'products': featured
                    })

        # Count total products
        total_count = sum(len(s['products']) for s in sections)

        return {
            'sections': sections,
            'total_count': total_count
        }

    @staticmethod
    def _get_recently_viewed_products(
        request,
        limit: int = 2,
        exclude_ids: Optional[Set[int]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get recently viewed products from RecentlyViewed model.

        Works for both authenticated users and anonymous sessions.
        """
        exclude_ids = exclude_ids or set()

        if request.user.is_authenticated:
            queryset = RecentlyViewed.objects.filter(
                user=request.user
            ).select_related('product', 'product__category')
        else:
            session_key = request.session.session_key
            if not session_key:
                return []
            queryset = RecentlyViewed.objects.filter(
                session_key=session_key
            ).select_related('product', 'product__category')

        # Filter to active, in-stock products, exclude already used
        products = []
        for rv in queryset.order_by('-viewed_at')[:limit * 4]:  # Get extra in case some excluded/out-of-stock
            product = rv.product
            if product.id in exclude_ids:
                continue
            if product.status != 'published':
                continue
            # Check stock availability
            if product.track_inventory:
                # Check if product has stock
                has_stock = StockItem.objects.filter(
                    product_id=product.id,
                    variant_id__isnull=True
                ).annotate(
                    available=F('on_hand') - F('allocated')
                ).filter(
                    available__gt=0
                ).exists()
                if not has_stock:
                    continue

            products.append(CartRecommendationService._format_product(product))
            if len(products) >= limit:
                break

        return products

    @staticmethod
    def _get_related_to_viewed(
        viewed_product_ids: List[int],
        exclude_ids: Optional[Set[int]] = None,
        limit: int = 2
    ) -> List[Dict[str, Any]]:
        """
        Get products related to recently viewed (same category or brand).
        """
        exclude_ids = exclude_ids or set()
        exclude_ids = exclude_ids.union(set(viewed_product_ids))

        # Get categories from viewed products
        viewed_products = Product.objects.filter(
            id__in=viewed_product_ids
        ).values_list('category_id', flat=True)

        category_ids = list(set(viewed_products))
        if not category_ids:
            return []

        # Get related products from same categories (in stock only)
        related = Product.objects.filter(
            category_id__in=category_ids,
            status='published'
        ).exclude(
            id__in=exclude_ids
        )
        related = CartRecommendationService._filter_in_stock(related)
        related = related.order_by('-views_count')[:limit]

        return [
            CartRecommendationService._format_product(p)
            for p in related
        ]

    @staticmethod
    def _get_on_sale_products(
        exclude_ids: Optional[Set[int]] = None,
        limit: int = 2
    ) -> List[Dict[str, Any]]:
        """
        Get products currently on sale.
        """
        from django.utils import timezone

        exclude_ids = exclude_ids or set()
        now = timezone.now()

        # Products with active sales (in stock only)
        on_sale = Product.objects.filter(
            status='published',
            sale_type__in=['percentage_off', 'amount_off', 'fixed_price']
        ).filter(
            Q(sale_start_date__isnull=True) | Q(sale_start_date__lte=now)
        ).filter(
            Q(sale_end_date__isnull=True) | Q(sale_end_date__gte=now)
        ).exclude(
            id__in=exclude_ids
        )
        on_sale = CartRecommendationService._filter_in_stock(on_sale)
        on_sale = on_sale.order_by('-views_count')[:limit]

        return [
            CartRecommendationService._format_product(p, show_sale=True)
            for p in on_sale
        ]

    @staticmethod
    def _get_trending_products(
        exclude_ids: Optional[Set[int]] = None,
        limit: int = 2
    ) -> List[Dict[str, Any]]:
        """
        Get trending products by view count (in stock only).
        """
        exclude_ids = exclude_ids or set()

        trending = Product.objects.filter(
            status='published'
        ).exclude(
            id__in=exclude_ids
        )
        trending = CartRecommendationService._filter_in_stock(trending)
        trending = trending.order_by('-views_count', '-sales_count')[:limit]

        return [
            CartRecommendationService._format_product(p)
            for p in trending
        ]

    @staticmethod
    def _get_featured_products(
        exclude_ids: Optional[Set[int]] = None,
        limit: int = 2
    ) -> List[Dict[str, Any]]:
        """
        Get featured products as fallback (in stock only).
        """
        exclude_ids = exclude_ids or set()

        featured = Product.objects.filter(
            status='published',
            is_featured=True
        ).exclude(
            id__in=exclude_ids
        )
        featured = CartRecommendationService._filter_in_stock(featured)
        featured = featured.order_by('-created_at')[:limit]

        # If not enough featured, get newest in-stock products
        if featured.count() < limit:
            newest = Product.objects.filter(
                status='published'
            ).exclude(
                id__in=exclude_ids.union(set(featured.values_list('id', flat=True)))
            )
            newest = CartRecommendationService._filter_in_stock(newest)
            newest = newest.order_by('-created_at')[:limit - featured.count()]

            return [
                CartRecommendationService._format_product(p)
                for p in list(featured) + list(newest)
            ]

        return [
            CartRecommendationService._format_product(p)
            for p in featured
        ]

    @staticmethod
    def _format_product(product: Product, show_sale: bool = False) -> Dict[str, Any]:
        """
        Format a product for the recommendation response.
        """
        # Get product URL
        try:
            url = reverse('page_builder:product_detail', kwargs={'product_slug': product.slug})
        except Exception:
            url = f'/products/{product.slug}/'

        # Get image URL
        image_url = None
        if hasattr(product, 'primary_image_url') and product.primary_image_url:
            image_url = product.primary_image_url
        elif hasattr(product, 'get_primary_image'):
            image_url = product.get_primary_image()

        # Get prices
        price = product.price
        if hasattr(price, 'amount'):
            price_amount = float(price.amount)
            currency = str(price.currency)
        else:
            price_amount = float(price)
            from core.utils import get_default_currency
            currency = get_default_currency()

        # Check if on sale
        is_on_sale = getattr(product, 'is_on_sale', False)
        sale_price = None
        if is_on_sale:
            calculated_sale = product.calculate_sale_price()
            if calculated_sale:
                sale_price = float(calculated_sale)

        from cart.mini_cart_api import _format_price

        return {
            'id': product.id,
            'name': product.name,
            'slug': product.slug,
            'url': url,
            'image_url': image_url,
            'price': price_amount,
            'price_formatted': _format_price(price_amount, currency),
            'on_sale': is_on_sale,
            'sale_price': sale_price,
            'sale_price_formatted': _format_price(sale_price, currency) if sale_price else None,
            'category': product.category.name if product.category else None,
        }
