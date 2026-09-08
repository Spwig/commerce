"""
Cart Recommendation Service - Intelligent product suggestions for empty cart state

Provides personalized recommendations based on:
- Recently viewed products (session or user-based)
- Related products (same category/brand)
- On-sale items
- Trending/bestselling products
- Featured products as fallback
"""

from typing import Any

from django.db.models import F, Q, Sum
from django.urls import reverse

from cart.models import RecentlyViewed
from catalog.models import Product, StockItem


class CartRecommendationService:
    """
    Service for generating intelligent empty cart recommendations.

    Supports both authenticated and anonymous users via session-based
    recently viewed tracking.
    """

    @staticmethod
    def _in_stock_product_ids():
        """
        Return a subquery of product IDs that currently have available stock.

        Aggregates every StockItem row for a product — simple products keep
        stock in product-level rows (variant_id is null) while variable
        products keep it in variant-level rows, so both are included — and
        keeps only products where total on_hand exceeds total allocated.
        """
        return (
            StockItem.objects.values("product_id")
            .annotate(total_available=Sum(F("on_hand") - F("allocated")))
            .filter(total_available__gt=0)
            .values("product_id")
        )

    @staticmethod
    def _in_stock_q(prefix: str = "") -> Q:
        """
        Return a Q matching in-stock products, optionally across a relation.

        Products with track_inventory=False are always in stock; tracked
        products need at least one StockItem row with positive availability.
        ``prefix`` (e.g. ``"product__"``) lets the same guard apply from a
        related model such as RecentlyViewed.
        """
        in_stock_ids = CartRecommendationService._in_stock_product_ids()
        return Q(**{f"{prefix}track_inventory": False}) | Q(
            **{f"{prefix}track_inventory": True, f"{prefix}pk__in": in_stock_ids}
        )

    @staticmethod
    def _filter_in_stock(queryset):
        """
        Filter a Product queryset to only include products that are in stock.
        """
        return queryset.filter(CartRecommendationService._in_stock_q())

    @staticmethod
    def get_empty_cart_recommendations(request, limit: int = 6) -> dict[str, Any]:
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
        used_product_ids: set[int] = set()

        # 1. Recently viewed products (max 2)
        recently_viewed = []
        remaining_slots = limit - len(used_product_ids)
        if remaining_slots > 0:
            recently_viewed = CartRecommendationService._get_recently_viewed_products(
                request, limit=min(2, remaining_slots), exclude_ids=used_product_ids
            )
        if recently_viewed:
            sections.append(
                {
                    "type": "recently_viewed",
                    "label": "Continue Shopping",
                    "products": recently_viewed,
                }
            )
            used_product_ids.update(p["id"] for p in recently_viewed)

        # 2. Related to recently viewed (same category, max 2)
        remaining_slots = limit - len(used_product_ids)
        if recently_viewed and remaining_slots > 0:
            # Get categories from recently viewed
            recently_viewed_ids = [p["id"] for p in recently_viewed]
            related = CartRecommendationService._get_related_to_viewed(
                viewed_product_ids=recently_viewed_ids,
                exclude_ids=used_product_ids,
                limit=min(2, remaining_slots),
            )
            if related:
                sections.append(
                    {"type": "related", "label": "You Might Also Like", "products": related}
                )
                used_product_ids.update(p["id"] for p in related)

        # 3. On-sale products (max 2)
        remaining_slots = limit - len(used_product_ids)
        if remaining_slots > 0:
            on_sale = CartRecommendationService._get_on_sale_products(
                exclude_ids=used_product_ids, limit=min(2, remaining_slots)
            )
            if on_sale:
                sections.append({"type": "on_sale", "label": "On Sale Now", "products": on_sale})
                used_product_ids.update(p["id"] for p in on_sale)

        # 4. Trending/Popular products (fill remaining)
        remaining_slots = limit - len(used_product_ids)
        if remaining_slots > 0:
            trending = CartRecommendationService._get_trending_products(
                exclude_ids=used_product_ids, limit=remaining_slots
            )
            if trending:
                sections.append(
                    {"type": "trending", "label": "Popular Right Now", "products": trending}
                )
                used_product_ids.update(p["id"] for p in trending)

        # 5. Fallback: Featured products if we still need more
        remaining_slots = limit - len(used_product_ids)
        if remaining_slots > 0:
            featured = CartRecommendationService._get_featured_products(
                exclude_ids=used_product_ids, limit=remaining_slots
            )
            if featured:
                # Merge into trending section if exists, otherwise create new
                trending_section = next((s for s in sections if s["type"] == "trending"), None)
                if trending_section:
                    trending_section["products"].extend(featured)
                else:
                    sections.append(
                        {"type": "featured", "label": "Recommended For You", "products": featured}
                    )

        # Count total products
        total_count = sum(len(s["products"]) for s in sections)

        return {"sections": sections, "total_count": total_count}

    @staticmethod
    def _get_recently_viewed_products(
        request, limit: int = 2, exclude_ids: set[int] | None = None
    ) -> list[dict[str, Any]]:
        """
        Get recently viewed products from RecentlyViewed model.

        Works for both authenticated users and anonymous sessions.
        """
        exclude_ids = exclude_ids or set()

        if request.user.is_authenticated:
            queryset = RecentlyViewed.objects.filter(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                return []
            queryset = RecentlyViewed.objects.filter(session_key=session_key)

        # Apply publication, exclusion, and stock filters in the queryset so
        # slicing happens over eligible rows only, then order by recency.
        queryset = (
            queryset.filter(product__status="published")
            .exclude(product_id__in=exclude_ids)
            .filter(CartRecommendationService._in_stock_q(prefix="product__"))
            .select_related("product", "product__category")
            .prefetch_related("product__images__media_asset")
            .order_by("-viewed_at")
        )

        # A product can have multiple RecentlyViewed rows (e.g. differing
        # session_key), so deduplicate before filling recommendation slots.
        products = []
        seen_ids: set[int] = set()
        for rv in queryset:
            product = rv.product
            if product.id in seen_ids:
                continue
            seen_ids.add(product.id)
            products.append(CartRecommendationService._format_product(product))
            if len(products) >= limit:
                break

        return products

    @staticmethod
    def _get_related_to_viewed(
        viewed_product_ids: list[int], exclude_ids: set[int] | None = None, limit: int = 2
    ) -> list[dict[str, Any]]:
        """
        Get products related to recently viewed (same category or brand).
        """
        exclude_ids = exclude_ids or set()
        exclude_ids = exclude_ids.union(set(viewed_product_ids))

        # Get categories from viewed products
        viewed_products = Product.objects.filter(id__in=viewed_product_ids).values_list(
            "category_id", flat=True
        )

        category_ids = list(set(viewed_products))
        if not category_ids:
            return []

        # Get related products from same categories (in stock only)
        related = (
            Product.objects.filter(category_id__in=category_ids, status="published")
            .exclude(id__in=exclude_ids)
            .select_related("category")
            .prefetch_related("images__media_asset")
        )
        related = CartRecommendationService._filter_in_stock(related)
        related = related.order_by("-views_count")[:limit]

        return [CartRecommendationService._format_product(p) for p in related]

    @staticmethod
    def _get_on_sale_products(
        exclude_ids: set[int] | None = None, limit: int = 2
    ) -> list[dict[str, Any]]:
        """
        Get products currently on sale.
        """
        from django.utils import timezone

        exclude_ids = exclude_ids or set()
        now = timezone.now()

        # Products with active sales (in stock only)
        on_sale = (
            Product.objects.filter(
                status="published",
                sale_type__in=["percentage_off", "amount_off", "fixed_price"],
                sale_value__isnull=False,
                sale_value__gt=0,
            )
            .filter(Q(sale_start_date__isnull=True) | Q(sale_start_date__lte=now))
            .filter(Q(sale_end_date__isnull=True) | Q(sale_end_date__gte=now))
            .exclude(id__in=exclude_ids)
            .select_related("category")
            .prefetch_related("images__media_asset")
        )
        on_sale = CartRecommendationService._filter_in_stock(on_sale)
        on_sale = on_sale.order_by("-views_count")[:limit]

        return [CartRecommendationService._format_product(p, show_sale=True) for p in on_sale]

    @staticmethod
    def _get_trending_products(
        exclude_ids: set[int] | None = None, limit: int = 2
    ) -> list[dict[str, Any]]:
        """
        Get trending products by view count (in stock only).
        """
        exclude_ids = exclude_ids or set()

        trending = (
            Product.objects.filter(status="published")
            .exclude(id__in=exclude_ids)
            .select_related("category")
            .prefetch_related("images__media_asset")
        )
        trending = CartRecommendationService._filter_in_stock(trending)
        trending = trending.order_by("-views_count", "-sales_count")[:limit]

        return [CartRecommendationService._format_product(p) for p in trending]

    @staticmethod
    def _get_featured_products(
        exclude_ids: set[int] | None = None, limit: int = 2
    ) -> list[dict[str, Any]]:
        """
        Get featured products as fallback (in stock only).
        """
        exclude_ids = exclude_ids or set()

        featured = (
            Product.objects.filter(status="published", is_featured=True)
            .exclude(id__in=exclude_ids)
            .select_related("category")
            .prefetch_related("images__media_asset")
        )
        featured = CartRecommendationService._filter_in_stock(featured)
        featured = featured.order_by("-created_at")[:limit]

        # If not enough featured, get newest in-stock products
        if featured.count() < limit:
            newest = (
                Product.objects.filter(status="published")
                .exclude(id__in=exclude_ids.union(set(featured.values_list("id", flat=True))))
                .select_related("category")
                .prefetch_related("images__media_asset")
            )
            newest = CartRecommendationService._filter_in_stock(newest)
            newest = newest.order_by("-created_at")[: limit - featured.count()]

            return [
                CartRecommendationService._format_product(p) for p in list(featured) + list(newest)
            ]

        return [CartRecommendationService._format_product(p) for p in featured]

    @staticmethod
    def _get_primary_asset(product: Product):
        """
        Return the primary media asset from the product's prefetched images.

        Mirrors Product.primary_image but reads the prefetched ``images``
        collection instead of issuing fresh reverse-relation queries, so
        formatting a recommendation list stays free of N+1 image lookups.
        """
        images = list(product.images.all())
        if not images:
            return None
        primary = next((img for img in images if img.is_primary), None)
        if primary and primary.media_asset:
            return primary.media_asset
        first_image = images[0]
        return first_image.media_asset or None

    @staticmethod
    def _format_product(product: Product, show_sale: bool = False) -> dict[str, Any]:
        """
        Format a product for the recommendation response.
        """
        # Get product URL
        try:
            url = reverse("page_builder:product_detail", kwargs={"product_slug": product.slug})
        except Exception:
            url = f"/products/{product.slug}/"

        # Get image URL from the prefetched images (see _get_primary_asset),
        # resolving the primary asset once to avoid extra per-product queries.
        image_url = None
        image_sources = None
        primary_asset = CartRecommendationService._get_primary_asset(product)
        if primary_asset:
            image_url = primary_asset.get_display_url()
            if hasattr(primary_asset, "get_picture_sources"):
                image_sources = primary_asset.get_picture_sources()

        # Get prices
        price = product.price
        if hasattr(price, "amount"):
            price_amount = float(price.amount)
            currency = str(price.currency)
        else:
            price_amount = float(price)
            from core.utils import get_default_currency

            currency = get_default_currency()

        # Check if on sale
        is_on_sale = getattr(product, "is_on_sale", False)
        sale_price = None
        if is_on_sale:
            calculated_sale = product.calculate_sale_price()
            if calculated_sale:
                sale_price = float(calculated_sale)

        from cart.mini_cart_api import _format_price

        return {
            "id": product.id,
            "name": product.name,
            "slug": product.slug,
            "url": url,
            "image_url": image_url,
            "image_sources": image_sources,
            "price": price_amount,
            "price_formatted": _format_price(price_amount, currency),
            "on_sale": is_on_sale,
            "sale_price": sale_price,
            "sale_price_formatted": _format_price(sale_price, currency) if sale_price else None,
            "category": product.category.name if product.category else None,
        }
