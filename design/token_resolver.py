"""Token Resolution System

Implements 4-level priority cascade for design tokens:
1. Brand Builder (priority 1) - Merchant customizations (highest priority)
2. Theme (priority 2) - Active theme tokens
3. Component (priority 3) - Component-specific tokens
4. Default (priority 4) - System defaults (lowest priority)

Lower priority number = higher precedence in cascade.

The TokenResolver provides efficient, tier-aware token resolution with caching
to ensure fast CSS variable generation for the frontend.

Example Usage:
    >>> from design.token_resolver import get_token_resolver
    >>> from design.theme_models import Theme
    >>>
    >>> # Get resolver for Tier A checkout page
    >>> theme = Theme.objects.get(is_active=True)
    >>> resolver = get_token_resolver(page_tier='A', theme=theme)
    >>>
    >>> # Resolve single token
    >>> primary_color = resolver.resolve_token('primary-color')
    >>> print(primary_color.value)  # Uses highest priority available
    '#FF5733'
    >>>
    >>> # Get all resolved tokens as CSS variables
    >>> css_vars = resolver.get_css_variables()
    >>> # Returns: ":root { --primary-color: #FF5733; ... }"
"""

from typing import Dict, Optional, List
from django.core.cache import cache
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
import logging

from .models import DesignToken, PageTier
from .theme_models import Theme

logger = logging.getLogger(__name__)


class TokenResolver:
    """Resolves design tokens with tier-aware priority cascade.

    The TokenResolver implements a 4-level priority cascade system where tokens
    from higher priority sources override tokens from lower priority sources.
    This allows merchants to customize theme tokens via Brand Builder while
    maintaining fallbacks to theme, component, and system defaults.

    Priority Levels:
        1. Brand Builder - Merchant customizations (highest)
        2. Theme - Active theme tokens
        3. Component - Component-specific tokens
        4. System - System defaults (lowest)

    Tier Awareness:
        Tokens can be restricted to specific page tiers (A/B/C) for security.
        The resolver only returns tokens available in the specified tier.

    Caching:
        Resolved tokens are cached for 5 minutes to improve performance.
        Cache is automatically invalidated when tokens are updated.

    Attributes:
        page_tier: Page tier identifier ('A', 'B', or 'C')
        theme: Active theme instance
        _cache_timeout: Cache timeout in seconds (default: 300)
        _cache_key_prefix: Prefix for cache keys
    """

    CACHE_TIMEOUT = 300  # 5 minutes
    CACHE_KEY_PREFIX = 'token_resolver'

    PRIORITY_LEVELS = {
        'brand_builder': 1,
        'theme': 2,
        'component': 3,
        'system': 4,
    }

    def __init__(self, page_tier: str = None, theme: Theme = None, component = None):
        """Initialize resolver for specific context.

        Args:
            page_tier: Page tier (A/B/C) for tier restrictions. None = all tiers.
            theme: Active theme instance. None = no theme-specific tokens.
            component: ComponentStore instance for component-scoped tokens. None = no component tokens.

        Example:
            >>> theme = Theme.objects.get(is_active=True)
            >>> resolver = TokenResolver(page_tier='A', theme=theme)
            >>> # With component scoping:
            >>> component = ComponentStore.objects.get(component_type='hero_banner')
            >>> resolver = TokenResolver(page_tier='B', theme=theme, component=component)
        """
        self.page_tier = page_tier
        self.theme = theme
        self.component = component
        self._resolved_tokens = None  # Lazy-loaded cache
        logger.debug(
            f"TokenResolver initialized: tier={page_tier}, "
            f"theme={theme.name if theme else 'None'}, "
            f"component={component.component_type if component else 'None'}"
        )

    def resolve_token(self, token_name: str) -> Optional[DesignToken]:
        """Resolve token with priority cascade.

        Returns the highest priority token available for the current tier.
        Searches through all priority levels (1-4) and returns the first match.

        Args:
            token_name: Name of token to resolve (e.g., 'primary-color')

        Returns:
            DesignToken instance or None if not found

        Example:
            >>> token = resolver.resolve_token('primary-color')
            >>> if token:
            ...     print(f"Color: {token.value} from {token.get_source_display()}")
            Color: #FF5733 from Brand Builder
        """
        cache_key = self._get_cache_key(token_name)
        cached_token = cache.get(cache_key)

        if cached_token is not None:
            logger.debug(f"Cache hit for token: {token_name}")
            return cached_token

        # Build query for tier-aware token lookup
        query = Q(name=token_name, is_active=True)

        # Add tier restriction filter
        if self.page_tier:
            query &= (
                Q(tier_restriction__contains=[self.page_tier]) |
                Q(tier_restriction=[])  # Empty = all tiers
            )

        # Query all matching tokens ordered by priority
        tokens = DesignToken.objects.filter(query).select_related('theme', 'component').order_by(
            'priority_level', 'name'
        )

        # Filter theme-specific tokens if theme is specified
        if self.theme:
            # Include: brand_builder, theme (matching theme), component, system
            tokens = [
                t for t in tokens
                if t.source != 'theme' or t.theme_id == self.theme.id
            ]
        else:
            # Exclude theme tokens if no theme specified
            tokens = [t for t in tokens if t.source != 'theme']

        # Filter component-specific tokens if component is specified
        if self.component:
            # Include: brand_builder, theme, component (matching component), system
            tokens = [
                t for t in tokens
                if t.source != 'component' or t.component_id == self.component.id
            ]
        else:
            # Exclude component tokens if no component specified
            tokens = [t for t in tokens if t.source != 'component']

        # Return highest priority token (first in ordered list)
        resolved_token = tokens[0] if tokens else None

        # Cache the result
        cache.set(cache_key, resolved_token, self.CACHE_TIMEOUT)

        if resolved_token:
            logger.debug(
                f"Resolved '{token_name}' to priority {resolved_token.priority_level} "
                f"({resolved_token.get_source_display()})"
            )
        else:
            logger.debug(f"Token '{token_name}' not found in any priority level")

        return resolved_token

    def resolve_all_tokens(self, token_type: str = None) -> Dict[str, DesignToken]:
        """Resolve all tokens for current context.

        Returns a dictionary of token_name: DesignToken for all available tokens,
        with priority cascade applied. Optionally filter by token type.

        Args:
            token_type: Optional token type filter ('color', 'font', 'spacing', etc.)

        Returns:
            Dict mapping token names to resolved DesignToken instances

        Example:
            >>> color_tokens = resolver.resolve_all_tokens(token_type='color')
            >>> for name, token in color_tokens.items():
            ...     print(f"{name}: {token.value}")
            primary-color: #FF5733
            secondary-color: #3B82F6
        """
        cache_key = self._get_cache_key_all(token_type)
        cached_tokens = cache.get(cache_key)

        if cached_tokens is not None:
            logger.debug(f"Cache hit for all tokens (type={token_type})")
            return cached_tokens

        # Build query
        query = Q(is_active=True)

        # Add tier restriction
        if self.page_tier:
            query &= (
                Q(tier_restriction__contains=[self.page_tier]) |
                Q(tier_restriction=[])
            )

        # Add token type filter
        if token_type:
            query &= Q(token_type=token_type)

        # Get all matching tokens ordered by priority
        all_tokens = DesignToken.objects.filter(query).select_related('theme', 'component').order_by(
            'priority_level', 'name'
        )

        # Filter theme tokens
        if self.theme:
            all_tokens = [
                t for t in all_tokens
                if t.source != 'theme' or t.theme_id == self.theme.id
            ]
        else:
            all_tokens = [t for t in all_tokens if t.source != 'theme']

        # Filter component tokens
        if self.component:
            all_tokens = [
                t for t in all_tokens
                if t.source != 'component' or t.component_id == self.component.id
            ]
        else:
            all_tokens = [t for t in all_tokens if t.source != 'component']

        # Resolve cascades: for each token name, keep only highest priority
        resolved = {}
        for token in all_tokens:
            if token.name not in resolved:
                resolved[token.name] = token

        # Cache the result
        cache.set(cache_key, resolved, self.CACHE_TIMEOUT)

        logger.debug(
            f"Resolved {len(resolved)} tokens "
            f"(tier={self.page_tier}, type={token_type})"
        )

        return resolved

    def get_css_variables(self, token_type: str = None) -> str:
        """Generate CSS custom properties from resolved tokens.

        Creates a CSS string with :root { } declaration containing all
        resolved tokens as CSS custom properties (--token-name: value).

        Args:
            token_type: Optional token type filter

        Returns:
            CSS string ready for injection into page

        Example:
            >>> css = resolver.get_css_variables(token_type='color')
            >>> print(css)
            :root {
                --primary-color: #FF5733;
                --secondary-color: #3B82F6;
            }
        """
        tokens = self.resolve_all_tokens(token_type=token_type)

        if not tokens:
            return ""

        css_lines = [":root {"]

        for token_name, token in sorted(tokens.items()):
            # Generate CSS custom property name
            css_var = f"--{token_name.replace('_', '-')}"
            css_lines.append(f"    {css_var}: {token.value};")

        css_lines.append("}")

        css_output = "\n".join(css_lines)

        logger.debug(
            f"Generated CSS with {len(tokens)} variables "
            f"(tier={self.page_tier}, type={token_type})"
        )

        return css_output

    def get_cascade_for_token(self, token_name: str) -> List[DesignToken]:
        """Get full cascade of tokens for debugging/preview.

        Returns all tokens with the given name across all priority levels,
        ordered by priority. Useful for showing merchants how cascade works.

        Args:
            token_name: Token name to get cascade for

        Returns:
            List of DesignToken instances ordered by priority (highest first)

        Example:
            >>> cascade = resolver.get_cascade_for_token('primary-color')
            >>> for token in cascade:
            ...     print(f"{token.priority_level}: {token.value} ({token.source})")
            1: #FF5733 (brand_builder)
            2: #3B82F6 (theme)
            4: #1E40AF (system)
        """
        query = Q(name=token_name, is_active=True)

        if self.page_tier:
            query &= (
                Q(tier_restriction__contains=[self.page_tier]) |
                Q(tier_restriction=[])
            )

        cascade = DesignToken.objects.filter(query).select_related('theme', 'component').order_by(
            'priority_level'
        )

        # Filter theme tokens
        if self.theme:
            cascade = [
                t for t in cascade
                if t.source != 'theme' or t.theme_id == self.theme.id
            ]
        else:
            cascade = [t for t in cascade if t.source != 'theme']

        # Filter component tokens
        if self.component:
            cascade = [
                t for t in cascade
                if t.source != 'component' or t.component_id == self.component.id
            ]
        else:
            cascade = [t for t in cascade if t.source != 'component']

        return list(cascade)

    def clear_cache(self):
        """Clear all cached tokens for this resolver context.

        Useful when tokens are updated and cache needs to be invalidated.

        Example:
            >>> resolver.clear_cache()
        """
        # Clear specific token caches (would need to know all token names)
        # For now, clear the all-tokens cache
        for token_type in ['color', 'font', 'spacing', 'border', 'shadow', 'animation', 'breakpoint', None]:
            cache_key = self._get_cache_key_all(token_type)
            cache.delete(cache_key)

        logger.debug(f"Cache cleared for resolver (tier={self.page_tier})")

    def _get_cache_key(self, token_name: str) -> str:
        """Generate cache key for single token resolution."""
        theme_id = self.theme.id if self.theme else 'none'
        component_id = self.component.id if self.component else 'none'
        tier = self.page_tier or 'all'
        return f"{self.CACHE_KEY_PREFIX}:{tier}:{theme_id}:{component_id}:{token_name}"

    def _get_cache_key_all(self, token_type: str = None) -> str:
        """Generate cache key for all tokens resolution."""
        theme_id = self.theme.id if self.theme else 'none'
        component_id = self.component.id if self.component else 'none'
        tier = self.page_tier or 'all'
        token_type_str = token_type or 'all'
        return f"{self.CACHE_KEY_PREFIX}:all:{tier}:{theme_id}:{component_id}:{token_type_str}"


# Singleton factory for getting resolver instances
_resolver_cache = {}


def get_token_resolver(page_tier: str = None, theme: Theme = None, component = None) -> TokenResolver:
    """Factory function to get TokenResolver instance.

    Provides a convenient way to get resolver instances. Can be extended
    to implement pooling or other optimizations in the future.

    Args:
        page_tier: Page tier (A/B/C)
        theme: Active theme instance
        component: ComponentStore instance for component-scoped tokens

    Returns:
        TokenResolver instance

    Example:
        >>> from design.token_resolver import get_token_resolver
        >>> resolver = get_token_resolver(page_tier='A', theme=my_theme)
        >>> token = resolver.resolve_token('primary-color')
        >>> # With component scoping:
        >>> component = ComponentStore.objects.get(component_type='hero_banner')
        >>> resolver = get_token_resolver(page_tier='B', theme=my_theme, component=component)
    """
    return TokenResolver(page_tier=page_tier, theme=theme, component=component)


def invalidate_token_cache():
    """Invalidate all token resolver caches.

    Should be called when tokens are created, updated, or deleted.
    Can be connected to Django signals for automatic cache invalidation.

    Example:
        >>> from design.token_resolver import invalidate_token_cache
        >>> invalidate_token_cache()
    """
    # Clear all token resolver caches
    # Use cache pattern matching if available, otherwise clear all
    try:
        cache.delete_pattern(f"{TokenResolver.CACHE_KEY_PREFIX}:*")
        logger.info("All token resolver caches invalidated using delete_pattern")
    except AttributeError:
        # Fallback for cache backends that don't support delete_pattern (e.g., LocMem)
        logger.warning(
            "Cache backend doesn't support delete_pattern. "
            "Clearing entire cache as fallback. "
            "Consider using Redis in production for better cache control."
        )
        cache.clear()
        logger.info("Entire cache cleared as fallback for token invalidation")
