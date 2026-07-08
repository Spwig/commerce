"""
Context providers for page builder elements.

Provides dynamic data from Django models to page builder elements based on their configuration.
Elements can specify a `context_provider` in their config.json to use these providers.

Author: Page Builder System
"""

import logging
from typing import Dict, Any, Optional, List
from django.db.models import QuerySet, Avg, Count
from django.utils import timezone

from core.translation_utils import (
    get_primary_language, translate_instance, translate_menu_items,
    translate_storefront_context,
)

logger = logging.getLogger(__name__)

# Provider registry - maps element types to their context provider functions
ELEMENT_CONTEXT_PROVIDERS = {}


def register_provider(element_type: str):
    """
    Decorator to register a context provider for an element type.

    Usage:
        @register_provider('blog_post_grid')
        def blog_post_grid_context(content: dict, request=None) -> dict:
            ...
    """
    def decorator(func):
        ELEMENT_CONTEXT_PROVIDERS[element_type] = func
        return func
    return decorator


def _apply_display_translations(context: Dict[str, Any], request) -> None:
    """
    Apply translations to model instances in the context dict in-place.

    Called by the dispatcher after each context provider returns.  Delegates
    to the shared ``translate_storefront_context`` for Product, Category,
    BlogPost, etc., then handles MenuItem translation separately (menu items
    use a recursive pattern and only appear in element contexts).
    """
    translate_storefront_context(context, request)

    # Menu items use a separate recursive mechanism
    if not request or not hasattr(request, 'LANGUAGE_CODE'):
        return
    lang = request.LANGUAGE_CODE
    primary = get_primary_language()
    if lang == primary:
        return
    menu_items = context.get('menu_items')
    if menu_items and isinstance(menu_items, list):
        translate_menu_items(menu_items, lang)


def get_element_context(element_type: str, content: Dict[str, Any], request=None) -> Dict[str, Any]:
    """
    Get dynamic context for an element based on its configuration.

    Args:
        element_type: The element type (e.g., 'blog_post_grid')
        content: The element's content/configuration dict
        request: Optional Django request object for context-aware queries

    Returns:
        Dict containing context data for the element template
    """
    provider = ELEMENT_CONTEXT_PROVIDERS.get(element_type)
    if provider:
        try:
            result = provider(content, request)
            _apply_display_translations(result, request)
            return result
        except Exception as e:
            logger.warning(f"Context provider error for {element_type}: {e}")
            return {}
    return {}


# =============================================================================
# Blog Context Providers
# =============================================================================

@register_provider('blog_post_grid')
def blog_post_grid_context(content: Dict, request=None) -> Dict:
    """Provide blog posts for the grid element."""
    if content.get('data_source') != 'dynamic':
        return {}

    from blog.models import BlogPost

    source = content.get('source', 'recent')
    max_posts = content.get('max_posts', 6)

    queryset = BlogPost.objects.filter(
        status='published',
        published_at__lte=timezone.now()
    ).select_related('category', 'featured_image', 'created_by')

    if source == 'featured':
        queryset = queryset.filter(is_featured=True)
    elif source == 'pinned':
        queryset = queryset.filter(is_pinned=True)
    elif source == 'category':
        category_slug = content.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
    elif source == 'tag':
        tag_slug = content.get('tag_slug')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

    # Order by pinned first, then by date
    queryset = queryset.order_by('-is_pinned', '-published_at')

    return {'posts': list(queryset[:max_posts])}


@register_provider('blog_post_carousel')
def blog_post_carousel_context(content: Dict, request=None) -> Dict:
    """Provide blog posts for the carousel element."""
    # Reuse the grid context provider with adjusted defaults
    if content.get('data_source') != 'dynamic':
        return {}

    adjusted_content = content.copy()
    adjusted_content.setdefault('max_posts', 8)

    return blog_post_grid_context(adjusted_content, request)


@register_provider('featured_blog_banner')
def featured_blog_banner_context(content: Dict, request=None) -> Dict:
    """Provide a single featured blog post for the banner element."""
    if content.get('data_source') != 'dynamic':
        return {}

    from blog.models import BlogPost

    source = content.get('source', 'latest_featured')
    post_slug = content.get('post_slug')

    queryset = BlogPost.objects.filter(
        status='published',
        published_at__lte=timezone.now()
    ).select_related('category', 'featured_image', 'created_by')

    if post_slug:
        # Specific post requested
        post = queryset.filter(slug=post_slug).first()
    elif source == 'latest_featured':
        post = queryset.filter(is_featured=True).order_by('-published_at').first()
    elif source == 'latest_pinned':
        post = queryset.filter(is_pinned=True).order_by('-published_at').first()
    else:  # latest
        post = queryset.order_by('-published_at').first()

    return {'post': post}


@register_provider('related_posts')
def related_posts_context(content: Dict, request=None) -> Dict:
    """Provide related blog posts based on category/tags."""
    if content.get('data_source') != 'dynamic':
        return {}

    from blog.models import BlogPost

    max_posts = content.get('max_posts', 3)
    relation_type = content.get('relation_type', 'auto')
    current_post_source = content.get('current_post_source', 'context')

    # Get the current post
    current_post = None

    if current_post_source == 'slug':
        post_slug = content.get('post_slug')
        if post_slug:
            current_post = BlogPost.objects.filter(slug=post_slug).first()
    elif request:
        # Try to get from request context (set by blog detail view)
        current_post = getattr(request, 'current_blog_post', None)

    if not current_post:
        return {'posts': []}

    # Build related posts query
    queryset = BlogPost.objects.filter(
        status='published',
        published_at__lte=timezone.now()
    ).exclude(
        pk=current_post.pk
    ).select_related('category', 'featured_image')

    if relation_type == 'category' and current_post.category:
        queryset = queryset.filter(category=current_post.category)
    elif relation_type == 'tags':
        tags = current_post.tags.all()
        if tags:
            queryset = queryset.filter(tags__in=tags).distinct()
    else:  # auto - category + tags
        from django.db.models import Q
        q = Q()
        if current_post.category:
            q |= Q(category=current_post.category)
        tags = current_post.tags.all()
        if tags:
            q |= Q(tags__in=tags)
        if q:
            queryset = queryset.filter(q).distinct()

    queryset = queryset.order_by('-published_at')

    return {'posts': list(queryset[:max_posts])}


# =============================================================================
# Product/Review Context Providers
# =============================================================================

@register_provider('reviews_display')
def reviews_display_context(content: Dict, request=None) -> Dict:
    """Provide product reviews for the reviews display element."""
    if content.get('data_source') != 'dynamic':
        return {}

    from catalog.models import ProductReview

    source = content.get('source_type', content.get('source', 'recent'))
    max_reviews = content.get('max_reviews', 6)

    queryset = ProductReview.objects.filter(
        is_approved=True
    ).select_related('product', 'user')

    # Apply minimum rating filter
    min_rating = content.get('min_rating')
    if min_rating:
        try:
            queryset = queryset.filter(rating__gte=int(min_rating))
        except (ValueError, TypeError):
            pass

    # Apply verified-only filter
    if content.get('show_verified_only'):
        queryset = queryset.filter(is_verified_purchase=True)

    if source == 'product':
        product_id = content.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
    elif source == 'featured':
        # Featured = highest rated verified reviews
        queryset = queryset.filter(is_verified_purchase=True).order_by('-rating', '-created_at')
    elif source == 'highest_rated':
        queryset = queryset.order_by('-rating', '-created_at')

    if source not in ('highest_rated', 'featured'):
        queryset = queryset.order_by('-created_at')

    reviews = list(queryset[:max_reviews])

    # Calculate summary stats
    stats = None
    if queryset.exists():
        agg = queryset.aggregate(
            average_rating=Avg('rating'),
            total_reviews=Count('id')
        )
        # Build rating breakdown (5 stars down to 1) - single query
        # Clear ordering to avoid it being included in GROUP BY
        rating_breakdown = {r: 0 for r in range(5, 0, -1)}
        for entry in queryset.order_by().values('rating').annotate(count=Count('id')):
            rating_breakdown[entry['rating']] = entry['count']
        stats = {
            'average_rating': round(agg['average_rating'], 1) if agg['average_rating'] else 0,
            'total_reviews': agg['total_reviews'] or 0,
            'rating_breakdown': rating_breakdown,
        }

    return {
        'reviews': reviews,
        'stats': stats,
    }


@register_provider('category_showcase')
def category_showcase_context(content: Dict, request=None) -> Dict:
    """Provide categories for the category showcase element.

    Handles both dynamic and static (manual selection) modes:
    - Dynamic: queries categories by source_type (top_level, featured, children_of)
    - Static: resolves category_ids list to Category instances, preserving order
    """
    from catalog.models import Category
    from django.db.models import Q

    def _parse_category_ids(raw):
        """Parse category IDs from various formats."""
        if isinstance(raw, list):
            return [int(x) for x in raw if str(x).strip().isdigit()]
        if isinstance(raw, str):
            return [int(x.strip()) for x in raw.split(',') if x.strip().isdigit()]
        return []

    def _apply_category_filters(cats):
        """Apply merchant-configured filters to category list."""
        if content.get('hide_empty'):
            cats = [c for c in cats if getattr(c, 'product_count', 0) > 0]
        return cats

    def _base_queryset():
        return Category.objects.filter(is_active=True).select_related('image_asset').annotate(
            product_count=Count('products', filter=Q(products__status='published'))
        )

    data_source = content.get('data_source', 'dynamic')

    if data_source == 'static':
        # Static mode: resolve category_ids to Category objects
        category_ids = _parse_category_ids(content.get('category_ids', []))
        if not category_ids:
            return {'categories': []}

        queryset = _base_queryset().filter(id__in=category_ids)
        # Preserve selection order
        id_order = {cid: i for i, cid in enumerate(category_ids)}
        categories = sorted(queryset, key=lambda c: id_order.get(c.id, 999))
        return {'categories': _apply_category_filters(categories)}

    # Dynamic mode
    source_type = content.get('source_type', 'top_level')
    max_categories = int(content.get('max_categories', 6))

    queryset = _base_queryset()

    if source_type == 'top_level':
        queryset = queryset.filter(parent__isnull=True)
    elif source_type == 'featured':
        queryset = queryset.filter(is_featured=True)
    elif source_type == 'children_of':
        parent_id = content.get('parent_category_id')
        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)
        else:
            queryset = queryset.none()
    elif source_type == 'specific':
        category_ids = _parse_category_ids(content.get('category_ids', []))
        if category_ids:
            queryset = queryset.filter(id__in=category_ids)
        else:
            queryset = queryset.none()

    queryset = queryset.order_by('sort_order', 'name')
    categories = list(queryset[:max_categories])
    return {'categories': _apply_category_filters(categories)}


@register_provider('sale_products')
def sale_products_context(content: Dict, request=None) -> Dict:
    """Provide products on sale for the sale products element."""
    if content.get('data_source') != 'dynamic':
        return {}

    from catalog.models import Product, Promotion

    source = content.get('source', 'all_sale')
    max_products = content.get('max_products', 8)

    # Get products with active promotions or sale prices
    now = timezone.now()

    if source == 'promotion':
        promotion_id = content.get('promotion_id')
        if promotion_id:
            try:
                promotion = Promotion.objects.get(
                    id=promotion_id,
                    is_active=True,
                    start_date__lte=now
                )
                # Filter: end_date is null OR end_date > now
                if promotion.end_date and promotion.end_date < now:
                    return {'products': []}

                products = promotion.get_affected_products()[:max_products]
                return {'products': list(products), 'promotion': promotion}
            except Promotion.DoesNotExist:
                return {'products': []}

    # Get all products with active sale prices or promotions
    products = Product.objects.filter(
        is_active=True,
        sale_price__isnull=False
    ).select_related('featured_image').order_by('-updated_at')[:max_products]

    return {'products': list(products)}


@register_provider('promotion_banner')
def promotion_banner_context(content: Dict, request=None) -> Dict:
    """Provide promotion data for the promotion banner element."""
    if content.get('data_source') != 'dynamic':
        return {}

    from catalog.models import Promotion

    promotion_id = content.get('promotion_id')
    now = timezone.now()

    if promotion_id:
        try:
            promotion = Promotion.objects.get(
                id=promotion_id,
                is_active=True,
                start_date__lte=now
            )
            # Check end date
            if promotion.end_date and promotion.end_date < now:
                return {'promotion': None, 'expired': True}

            return {'promotion': promotion}
        except Promotion.DoesNotExist:
            pass
    else:
        # Get the most prominent active promotion
        promotion = Promotion.objects.filter(
            is_active=True,
            start_date__lte=now
        ).exclude(
            end_date__lt=now
        ).order_by('-priority', '-start_date').first()

        if promotion:
            return {'promotion': promotion}

    return {'promotion': None}


@register_provider('product_list')
def product_list_context(content: Dict, request=None) -> Dict:
    """Provide products for the product list element."""
    if content.get('data_source') != 'dynamic':
        return {}

    from catalog.models import Product, Category, Collection

    source = content.get('source', 'recent')
    max_products = content.get('max_products', 10)

    queryset = Product.objects.filter(is_active=True).select_related(
        'featured_image', 'category'
    )

    if source == 'category':
        category_id = content.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
    elif source == 'collection':
        collection_id = content.get('collection_id')
        if collection_id:
            queryset = queryset.filter(collections__id=collection_id)
    elif source == 'featured':
        queryset = queryset.filter(is_featured=True)
    elif source == 'sale':
        queryset = queryset.filter(sale_price__isnull=False)

    queryset = queryset.order_by('-created_at')

    return {'products': list(queryset[:max_products])}


@register_provider('product_grid')
def product_grid_context(content: Dict, request=None) -> Dict:
    """
    Provide products for the product grid element.

    Handles both dynamic and static (manual selection) modes:
    - Dynamic: queries products by source_type (all, category, on_sale, featured, collection, new_arrivals)
    - Static: resolves product_ids list to Product instances, preserving order

    Also handles layout-specific processing:
    - Featured layout: splits into featured_products + remaining_products
    - Carousel layout: chunks into carousel_rows
    """
    from catalog.models import Product
    from django.db.models import Q

    data_source = content.get('data_source', 'dynamic')
    layout = content.get('layout', 'grid')

    def apply_product_filters(qs):
        """Apply merchant-configured product filters to queryset."""
        # Hide out of stock products
        if content.get('hide_out_of_stock'):
            qs = qs.with_stock_totals().filter(
                Q(track_inventory=False) | Q(total_available__gt=0) | Q(allow_backorders=True)
            )

        # Hide specific product types
        hide_types = []
        if content.get('hide_gift_cards'):
            hide_types.append('gift_card')
        if content.get('hide_digital'):
            hide_types.append('digital')
        if content.get('hide_booking'):
            hide_types.append('booking')
        if content.get('hide_bundles'):
            hide_types.append('bundle')
        if hide_types:
            qs = qs.exclude(product_type__in=hide_types)

        # Price range filters
        min_price = content.get('min_price')
        max_price = content.get('max_price')
        if min_price is not None and min_price != '' and min_price != 0:
            qs = qs.filter(price__gte=min_price)
        if max_price is not None and max_price != '' and max_price != 0:
            qs = qs.filter(price__lte=max_price)

        return qs

    if data_source == 'static':
        # Manual selection mode: resolve product IDs to instances
        product_ids = content.get('product_ids', [])
        if not product_ids:
            return {'products': []}

        # Ensure IDs are integers
        try:
            product_ids = [int(pid) for pid in product_ids]
        except (ValueError, TypeError):
            return {'products': []}

        queryset = Product.objects.filter(
            id__in=product_ids, status='published', hide_from_storefront=False
        ).exclude(
            sales_channel='pos_only'
        ).select_related('category').prefetch_related('images')

        queryset = apply_product_filters(queryset)

        # Preserve the merchant's specified order using CASE WHEN
        from django.db.models import Case, When
        preserved_order = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(product_ids)]
        )
        products = list(queryset.order_by(preserved_order))

    else:
        # Dynamic mode: query by source type
        source_type = content.get('source_type', 'all')
        max_products = int(content.get('max_products', 12))
        sort_order = content.get('sort_order', 'newest')

        queryset = Product.objects.filter(
            status='published', hide_from_storefront=False
        ).exclude(
            sales_channel='pos_only'
        ).select_related('category').prefetch_related('images')

        if source_type == 'category':
            category_id = content.get('category_id')
            if category_id:
                # Include descendant categories
                from catalog.models import Category
                try:
                    category = Category.objects.get(id=category_id, is_active=True)
                    descendant_ids = category.get_descendant_ids()
                    queryset = queryset.filter(category_id__in=descendant_ids)
                except Category.DoesNotExist:
                    return {'products': []}
            else:
                return {'products': []}
        elif source_type == 'on_sale':
            queryset = queryset.filter(sale_type__in=['fixed_price', 'amount_off', 'percentage_off'])
        elif source_type == 'featured':
            queryset = queryset.filter(is_featured=True)
        elif source_type == 'collection':
            collection_id = content.get('collection_id')
            if collection_id:
                queryset = queryset.filter(collections__id=collection_id)
            else:
                return {'products': []}
        elif source_type == 'new_arrivals':
            sort_order = 'newest'  # Force newest sort for new arrivals

        # Apply merchant product filters
        queryset = apply_product_filters(queryset)

        # Apply sort
        sort_map = {
            'newest': '-created_at',
            'price_low': 'price',
            'price_high': '-price',
            'name_az': 'name',
            'bestselling': ('-sales_count', '-views_count', '-created_at'),
        }
        order_by = sort_map.get(sort_order, '-created_at')
        if isinstance(order_by, tuple):
            queryset = queryset.order_by(*order_by)
        else:
            queryset = queryset.order_by(order_by)

        products = list(queryset[:max_products])

    # Build result dict
    result = {'products': products}

    # Layout-specific processing
    if layout == 'featured' and products:
        featured_count = int(content.get('featured_count', 1))
        result['featured_products'] = products[:featured_count]
        result['remaining_products'] = products[featured_count:]

    elif layout == 'carousel' and products:
        slides_per_view = int(content.get('slides_per_view', 4))
        # Create a single carousel row with all products
        result['carousel_rows'] = [{
            'products': products,
            'start': 1,
            'end': len(products),
            'total': len(products),
        }]

    return result


# =============================================================================
# Loyalty/Voucher Context Providers
# =============================================================================

@register_provider('loyalty_banner')
def loyalty_banner_context(content: Dict, request=None) -> Dict:
    """Provide loyalty program data for the banner element."""
    from loyalty.models import LoyaltyProgram, LoyaltyTier, LoyaltyMember

    # Get active loyalty program
    program = LoyaltyProgram.objects.filter(is_active=True).first()
    if not program:
        return {'program': None}

    tiers = list(LoyaltyTier.objects.filter(
        program=program,
        is_active=True
    ).order_by('points_required'))

    # Get member info if user is authenticated
    member = None
    if request and request.user.is_authenticated:
        member = LoyaltyMember.objects.filter(
            program=program,
            user=request.user
        ).first()

    return {
        'program': program,
        'tiers': tiers,
        'member': member
    }


@register_provider('voucher_code_display')
def voucher_code_display_context(content: Dict, request=None) -> Dict:
    """Provide voucher codes for display element."""
    if content.get('data_source') != 'dynamic':
        return {}

    from vouchers.models import VoucherCode

    now = timezone.now()
    max_vouchers = content.get('max_vouchers', 3)

    # Get public, active voucher codes
    vouchers = VoucherCode.objects.filter(
        is_active=True,
        is_public=True,
        valid_from__lte=now
    ).exclude(
        valid_until__lt=now
    ).order_by('-created_at')[:max_vouchers]

    return {'vouchers': list(vouchers)}


@register_provider('gift_card_promo')
def gift_card_promo_context(content: Dict, request=None) -> Dict:
    """Provide gift card product data for the promo element."""
    if content.get('data_source') != 'dynamic':
        return {}

    from catalog.models import Product

    # Get active gift card products
    gift_cards = Product.objects.filter(
        is_active=True,
        product_type='gift_card'
    ).select_related('featured_image').order_by('base_price')

    return {'gift_cards': list(gift_cards)}


# =============================================================================
# Navigation/Layout Context Providers
# =============================================================================

@register_provider('navigation_menu')
def navigation_menu_context(content: Dict, request=None) -> Dict:
    """
    Provide menu data for the navigation menu element.

    Fetches the specified menu with all its items in hierarchical structure.
    Supports visibility rules based on device and user authentication status.
    """
    from design.header_footer_models import Menu

    menu_id = content.get('menu_id')
    if not menu_id:
        return {'menu': None, 'menu_items': []}

    try:
        menu = Menu.objects.prefetch_related(
            'items__page_reference',
            'items__category_reference',
            'items__children'
        ).get(pk=menu_id, is_active=True)

        # Get hierarchical items (only top-level, children nested)
        menu_items = menu.get_items()

        # Apply visibility filtering if request available
        if request:
            menu_items = _filter_menu_items_by_visibility(menu_items, request)

        return {
            'menu': menu,
            'menu_items': menu_items,
            'menu_global_style': menu.global_style or {},
            'menu_mobile_config': menu.mobile_config or {},
        }
    except Menu.DoesNotExist:
        return {'menu': None, 'menu_items': []}


def _filter_menu_items_by_visibility(items: List, request) -> List:
    """
    Filter menu items based on visibility rules.

    Supports:
    - device: Filter by device type (desktop, tablet, mobile)
    - user_status: Filter by logged_in or logged_out
    """
    filtered = []
    user_authenticated = request.user.is_authenticated if hasattr(request, 'user') else False

    for item in items:
        visibility_rules = getattr(item, 'visibility_rules', None) or []

        # If no rules, item is always visible
        if not visibility_rules:
            # Recursively filter children
            if hasattr(item, 'children_list') and item.children_list:
                item.children_list = _filter_menu_items_by_visibility(item.children_list, request)
            filtered.append(item)
            continue

        # Check each rule
        visible = True
        for rule in visibility_rules:
            rule_type = rule.get('type')
            rule_value = rule.get('value')

            if rule_type == 'user_status':
                if rule_value == 'logged_in' and not user_authenticated:
                    visible = False
                    break
                elif rule_value == 'logged_out' and user_authenticated:
                    visible = False
                    break
            # Device filtering is handled client-side via CSS/JS

        if visible:
            # Recursively filter children
            if hasattr(item, 'children_list') and item.children_list:
                item.children_list = _filter_menu_items_by_visibility(item.children_list, request)
            filtered.append(item)

    return filtered
