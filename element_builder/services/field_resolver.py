"""
Field Resolver Service

Resolves field values from model instances based on ElementBinding configuration.
Handles computed properties, MediaAsset thumbnails, and standard fields.
"""
from django.db.models import Model
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


# Computed field resolvers for each model type
# Each resolver function takes (instance) and returns a value
COMPUTED_FIELDS = {
    'catalog.Product': {
        'primary_image': lambda p: _get_product_primary_image(p),
        'price': lambda p: _format_price(p.get_effective_price() if hasattr(p, 'get_effective_price') else p.price),
        'compare_at_price': lambda p: _format_price(p.compare_at_price) if p.compare_at_price else '',
        'discount_percentage': lambda p: _get_discount_percentage(p),
        'savings_amount': lambda p: _get_savings_amount(p),
        'is_on_sale': lambda p: 'Yes' if (p.compare_at_price and p.compare_at_price > (p.get_effective_price() if hasattr(p, 'get_effective_price') else p.price)) else 'No',
        'stock_status': lambda p: _get_stock_status(p),
        'is_in_stock': lambda p: 'Yes' if _is_in_stock(p) else 'No',
        'available_stock': lambda p: str(_get_available_stock(p)),
        'category_name': lambda p: p.category.name if p.category else '',
        'brand_name': lambda p: p.brand.name if p.brand else '',
        'url': lambda p: p.get_absolute_url() if hasattr(p, 'get_absolute_url') else '',
    },
    'catalog.Category': {
        'product_count': lambda c: str(c.products.filter(status='published').count() if hasattr(c, 'products') else 0),
        'full_path': lambda c: _get_category_full_path(c),
        'parent_name': lambda c: c.parent.name if c.parent else '',
        'url': lambda c: c.get_absolute_url() if hasattr(c, 'get_absolute_url') else '',
    },
    'catalog.Brand': {
        'product_count': lambda b: str(b.products.filter(status='published').count() if hasattr(b, 'products') else 0),
        'url': lambda b: b.get_absolute_url() if hasattr(b, 'get_absolute_url') else '',
    },
    'blog.BlogPost': {
        'author_name': lambda p: _get_author_name(p),
        'author_avatar': lambda p: _get_author_avatar(p),
        'category_name': lambda p: p.category.name if p.category else '',
        'tags_list': lambda p: ', '.join(t.name for t in p.tags.all()) if hasattr(p, 'tags') else '',
        'url': lambda p: p.get_absolute_url() if hasattr(p, 'get_absolute_url') else '',
    },
}


def resolve_field_value(instance: Model, field_name: str, thumbnail_preset: str = '') -> str:
    """
    Resolve the value of a field from a model instance.

    Args:
        instance: The model instance to get the value from
        field_name: The field/property name to resolve
        thumbnail_preset: (optional) For image fields, the thumbnail size

    Returns:
        The resolved value as a string (or URL for images)
    """
    if not instance or not field_name:
        return ''

    # Get the model key (e.g., 'catalog.Product')
    model_key = f"{instance._meta.app_label}.{instance._meta.model_name}".replace(
        instance._meta.model_name,
        instance._meta.object_name
    )

    # Check if this is a computed field
    computed_resolvers = COMPUTED_FIELDS.get(model_key, {})
    if field_name in computed_resolvers:
        try:
            value = computed_resolvers[field_name](instance)
            # Handle image returns
            if value and thumbnail_preset and hasattr(value, 'get_thumbnail'):
                return value.get_thumbnail(thumbnail_preset)
            if value and hasattr(value, 'url'):
                return value.url
            return str(value) if value else ''
        except Exception as e:
            logger.warning(f"Error resolving computed field '{field_name}' on {model_key}: {e}")
            return ''

    # Check if the field/property exists on the instance
    if not hasattr(instance, field_name):
        return ''

    try:
        value = getattr(instance, field_name)

        # Handle callable (property/method)
        if callable(value):
            value = value()

        # Handle None
        if value is None:
            return ''

        # Handle MediaAsset FK with thumbnail
        if thumbnail_preset and value:
            # Check if it's a MediaAsset or has get_thumbnail method
            if hasattr(value, 'get_thumbnail'):
                return value.get_thumbnail(thumbnail_preset)

            # For ProductImage, check media_asset attribute
            if hasattr(value, 'media_asset') and hasattr(value.media_asset, 'get_thumbnail'):
                return value.media_asset.get_thumbnail(thumbnail_preset)

        # Handle ImageField (returns URL)
        if hasattr(value, 'url'):
            return value.url

        # Handle boolean fields
        if isinstance(value, bool):
            return 'Yes' if value else 'No'

        # Handle Decimal (prices)
        if isinstance(value, Decimal):
            return _format_price(value)

        # Handle datetime
        if hasattr(value, 'strftime'):
            return value.strftime('%B %d, %Y')

        # Convert to string
        return str(value)

    except Exception as e:
        logger.warning(f"Error resolving field '{field_name}' on {instance}: {e}")
        return ''


def apply_bindings_to_element(element, instance: Model, bindings):
    """
    Apply ElementBinding values to an element's content.

    Args:
        element: page_builder.Element instance
        instance: The model instance to get values from
        bindings: QuerySet of ElementBinding for the custom element

    Returns:
        Modified element content dict with bound values injected
    """
    # Get bindings for this specific element
    element_bindings = bindings.filter(element=element)

    if not element_bindings.exists():
        return element.content

    # Create a copy of content to modify
    content = dict(element.content) if element.content else {}

    for binding in element_bindings:
        value = resolve_field_value(
            instance,
            binding.model_field,
            binding.thumbnail_preset
        )
        if value:
            content[binding.content_field] = value

    return content


# =============================================================================
# Helper functions for computed fields
# =============================================================================

def _get_product_primary_image(product):
    """Get the primary image MediaAsset for a product."""
    # Check for primary_image property
    if hasattr(product, 'primary_image'):
        img = product.primary_image
        if img:
            return img

    # Fallback: get first product image
    if hasattr(product, 'images'):
        first_image = product.images.order_by('order').first()
        if first_image and hasattr(first_image, 'media_asset'):
            return first_image.media_asset

    return None


def _format_price(price):
    """Format a price value for display."""
    if price is None:
        return ''

    try:
        from django.conf import settings
        # Try to use the store's currency formatting
        from core.models import SiteSettings
        site_settings = SiteSettings.get_solo()
        currency_symbol = site_settings.currency_symbol or '$'
        return f"{currency_symbol}{price:.2f}"
    except Exception:
        # Fallback to simple formatting
        return f"${price:.2f}" if price else ''


def _get_discount_percentage(product):
    """Calculate the discount percentage for a product."""
    if not product.compare_at_price:
        return ''

    try:
        current_price = product.get_effective_price() if hasattr(product, 'get_effective_price') else product.price
        if not current_price or not product.compare_at_price:
            return ''

        if product.compare_at_price <= current_price:
            return ''

        discount = ((product.compare_at_price - current_price) / product.compare_at_price) * 100
        return f"{int(discount)}%"
    except Exception:
        return ''


def _get_savings_amount(product):
    """Calculate the savings amount for a product."""
    if not product.compare_at_price:
        return ''

    try:
        current_price = product.get_effective_price() if hasattr(product, 'get_effective_price') else product.price
        if not current_price or not product.compare_at_price:
            return ''

        if product.compare_at_price <= current_price:
            return ''

        savings = product.compare_at_price - current_price
        return _format_price(savings)
    except Exception:
        return ''


def _get_stock_status(product):
    """Get human-readable stock status for a product."""
    if not hasattr(product, 'track_inventory') or not product.track_inventory:
        return 'In Stock'

    stock = _get_available_stock(product)
    low_stock_threshold = getattr(product, 'low_stock_threshold', 5)

    if stock <= 0:
        return 'Out of Stock'
    elif stock <= low_stock_threshold:
        return 'Low Stock'
    else:
        return 'In Stock'


def _is_in_stock(product):
    """Check if product is in stock."""
    if not hasattr(product, 'track_inventory') or not product.track_inventory:
        return True

    return _get_available_stock(product) > 0


def _get_available_stock(product):
    """Get available stock quantity for a product."""
    # Check for stock property or method
    if hasattr(product, 'available_stock'):
        stock = product.available_stock
        return stock() if callable(stock) else (stock or 0)

    if hasattr(product, 'get_available_stock'):
        return product.get_available_stock() or 0

    # Check for total_stock
    if hasattr(product, 'total_stock'):
        return product.total_stock or 0

    # Fallback: check inventory records
    if hasattr(product, 'inventory_records'):
        return sum(inv.quantity for inv in product.inventory_records.all())

    return 0


def _get_category_full_path(category):
    """Get the full breadcrumb path for a category."""
    path_parts = [category.name]
    current = category

    while current.parent:
        current = current.parent
        path_parts.insert(0, current.name)

    return ' > '.join(path_parts)


def _get_author_name(post):
    """Get the author display name for a blog post."""
    if hasattr(post, 'author') and post.author:
        author = post.author
        if hasattr(author, 'get_full_name'):
            full_name = author.get_full_name()
            if full_name:
                return full_name
        if hasattr(author, 'username'):
            return author.username
    return ''


def _get_author_avatar(post):
    """Get the author avatar for a blog post."""
    if hasattr(post, 'author') and post.author:
        author = post.author
        # Check for profile with avatar
        if hasattr(author, 'profile') and hasattr(author.profile, 'avatar'):
            return author.profile.avatar
        # Check for avatar directly on user
        if hasattr(author, 'avatar'):
            return author.avatar
    return None
