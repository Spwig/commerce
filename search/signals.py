"""
Cache invalidation signals for the search app.

Handles automatic cache clearing when related models are updated.
"""

from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import SearchRedirect, SearchSettings, Synonym


def invalidate_search_cache(prefix="search:"):
    """
    Invalidate all search-related caches.

    Uses cache key pattern matching where supported,
    otherwise clears specific known keys.
    """
    # Try to use cache.delete_pattern if available (Redis)
    if hasattr(cache, "delete_pattern"):
        cache.delete_pattern(f"{prefix}*")
    else:
        # Fallback: clear specific known cache keys
        cache.delete("search:settings")


def invalidate_autocomplete_cache(engine_slug=None):
    """Invalidate autocomplete caches, optionally for specific engine."""
    if hasattr(cache, "delete_pattern"):
        if engine_slug:
            cache.delete_pattern(f"search:auto:{engine_slug}:*")
        else:
            cache.delete_pattern("search:auto:*")


def invalidate_results_cache(engine_slug=None):
    """Invalidate full results caches, optionally for specific engine."""
    if hasattr(cache, "delete_pattern"):
        if engine_slug:
            cache.delete_pattern(f"search:results:{engine_slug}:*")
        else:
            cache.delete_pattern("search:results:*")


@receiver(post_save, sender=SearchSettings)
def on_search_settings_save(sender, instance, **kwargs):
    """Clear settings cache when settings are updated."""
    cache.delete("search:settings")
    # Also invalidate all search caches as weights/settings may have changed
    invalidate_search_cache()


@receiver(post_save, sender=Synonym)
@receiver(post_delete, sender=Synonym)
def on_synonym_change(sender, instance, **kwargs):
    """Clear search caches when synonyms change."""
    engine_slug = instance.engine.slug if instance.engine else None
    invalidate_autocomplete_cache(engine_slug)
    invalidate_results_cache(engine_slug)


@receiver(post_save, sender=SearchRedirect)
@receiver(post_delete, sender=SearchRedirect)
def on_redirect_change(sender, instance, **kwargs):
    """Clear redirect cache when redirects change."""
    if hasattr(cache, "delete_pattern"):
        cache.delete_pattern("search:redirect:*")


# Product/Category/Brand/BlogPost signal handlers
# These will be connected in apps.py ready() after catalog/blog apps are loaded


def connect_content_signals():
    """
    Connect signals for content models (Product, Category, Brand, BlogPost).
    Called from apps.py ready() to ensure models are loaded.
    """
    try:
        from blog.models import BlogPost
        from catalog.models import Brand, Category, Product

        @receiver(post_save, sender=Product)
        @receiver(post_delete, sender=Product)
        def on_product_change(sender, instance, **kwargs):
            invalidate_autocomplete_cache()
            invalidate_results_cache()

        @receiver(post_save, sender=Category)
        @receiver(post_delete, sender=Category)
        def on_category_change(sender, instance, **kwargs):
            invalidate_autocomplete_cache()
            invalidate_results_cache()

        @receiver(post_save, sender=Brand)
        @receiver(post_delete, sender=Brand)
        def on_brand_change(sender, instance, **kwargs):
            invalidate_autocomplete_cache()
            invalidate_results_cache()

        @receiver(post_save, sender=BlogPost)
        @receiver(post_delete, sender=BlogPost)
        def on_blog_post_change(sender, instance, **kwargs):
            invalidate_autocomplete_cache()
            invalidate_results_cache()

    except ImportError:
        # Catalog or blog app not installed yet
        pass
