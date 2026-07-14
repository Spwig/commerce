"""
Utility functions for theme management
Provides consistent access to active theme across the system
"""

import logging
from typing import Any

from django.core.cache import cache

logger = logging.getLogger(__name__)


def get_active_theme():
    """
    Get the currently active theme from GlobalDesignSettings.
    This is the single source of truth for the active theme.
    Falls back to the 'starter' theme if no active theme is set.

    Returns:
        Theme instance or None
    """
    try:
        from .models import GlobalDesignSettings
        from .theme_models import Theme

        settings = GlobalDesignSettings.get_settings()

        if settings.active_theme:
            return settings.active_theme

        # Fall back to starter theme if no active theme is set
        starter_theme = Theme.objects.filter(slug="starter", is_active=True).first()
        if starter_theme:
            return starter_theme

        # Final fallback: any active theme (prefer is_default, then alphabetical)
        any_theme = Theme.objects.filter(is_active=True).order_by("-is_default", "name").first()
        if any_theme:
            return any_theme

        return None
    except Exception as e:
        logger.error(f"Failed to get active theme: {e}", exc_info=True)
        return None


def get_active_theme_with_metadata() -> dict[str, Any] | None:
    """
    Get active theme with enhanced metadata from ComponentRegistry and ThemeVersionManager.
    Includes author information from update server and current version.

    Returns:
        Dict with theme info including author from ComponentRegistry, or None
    """
    theme = get_active_theme()

    if not theme:
        return None

    try:
        # Get version info from ThemeVersionManager
        from .theme_version_manager import ThemeVersionManager

        theme_info = ThemeVersionManager.get_active_theme()

        # Get author from ComponentRegistry (synced with update server)
        from component_updates.models import ComponentRegistry

        component = ComponentRegistry.objects.filter(
            component_type="theme", slug=theme.slug
        ).first()

        author_name = "Unknown"
        if component and component.author:
            author_name = component.author
        elif component and component.author_details:
            author_name = component.author_details.get("name", "Unknown")
        elif theme:
            author_name = theme.author

        return {
            "theme": theme,
            "slug": theme.slug,
            "name": theme_info.get("name") if theme_info else theme.name,
            "version": theme_info.get("version") if theme_info else theme.version,
            "author": author_name,
            "description": theme.description,
        }
    except Exception as e:
        logger.error(f"Failed to get theme metadata: {e}", exc_info=True)
        return {
            "theme": theme,
            "slug": theme.slug,
            "name": theme.name,
            "version": theme.version,
            "author": theme.author,
            "description": theme.description,
        }


def get_active_theme_cached():
    """
    Get active theme with 5-minute cache for performance.
    Use this in high-traffic areas like template tags.

    Returns:
        Theme instance or None
    """
    cache_key = "active_theme_instance"
    theme = cache.get(cache_key)

    if theme is None:
        theme = get_active_theme()
        if theme:
            cache.set(cache_key, theme, 300)  # 5 minutes

    return theme


def clear_active_theme_cache():
    """
    Clear the active theme cache.
    Call this when the active theme changes.
    """
    cache.delete("active_theme_instance")
    cache.delete_pattern("theme_*")
