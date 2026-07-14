"""
Token Sync Service - Handles synchronization between theme tokens and DesignToken model.

This service ensures that:
1. Theme tokens from manifest are synced to DesignToken records (source='theme')
2. Branding customizations are synced to DesignToken records (source='brand_builder')
3. Token naming follows the established --theme-{category}-{key} convention
"""

import logging

from django.db import transaction

from .models import DesignToken
from .theme_models import Theme, ThemeBranding

logger = logging.getLogger(__name__)


class TokenSyncService:
    """Service for synchronizing theme tokens with DesignToken model."""

    # Maps token.json categories to CSS variable prefixes
    # These must match the existing tokens.css naming convention
    CATEGORY_PREFIXES = {
        "colors": "theme-color",
        "typography": "theme",  # Keys already have font-, line-height- prefix
        "spacing": "theme-space",
        "borders": "theme",  # Keys already have border-, radius- prefix
        "shadows": "theme-shadow",
        "transitions": "theme-transition",
        "breakpoints": "theme-breakpoint",
        "z-index": "theme-z",
        "container": "theme-container",
        "menu": "theme-menu",
        "header": "theme-header",
        "footer": "theme-footer",
        "search": "theme-search",
        "elements": "theme-element",  # Nested: elements.button.radius -> theme-element-button-radius
        "widgets": "theme-widget",  # Nested: widgets.cart.icon-size -> theme-widget-cart-icon-size
        "animations": "theme-transition",  # Alias for transitions
    }

    # Maps categories to DesignToken.token_type
    CATEGORY_TOKEN_TYPES = {
        "colors": "color",
        "typography": "font",
        "spacing": "spacing",
        "borders": "border",
        "shadows": "shadow",
        "transitions": "animation",
        "breakpoints": "breakpoint",
        "z-index": "spacing",  # Z-index doesn't have dedicated type, use spacing
        "container": "spacing",  # Container dimensions
        "menu": "spacing",  # Menu tokens are mixed
        "header": "spacing",  # Header tokens are mixed
        "footer": "spacing",  # Footer tokens are mixed
        "search": "spacing",  # Search tokens are mixed
        "elements": "spacing",  # Element tokens are mixed
        "widgets": "spacing",  # Widget tokens are mixed (colors, spacing, etc.)
        "animations": "animation",
    }

    @classmethod
    def sync_theme_to_design_tokens(cls, theme: Theme) -> tuple[int, int, int]:
        """
        Sync theme manifest tokens to DesignToken records using bulk operations.

        Uses bulk_create/bulk_update to avoid per-token save() calls and signal
        overhead. Cache is invalidated once at the end instead of per-token.

        Args:
            theme: Theme instance to sync

        Returns:
            Tuple of (created_count, updated_count, deleted_count)
        """
        from .token_resolver import invalidate_token_cache

        if not theme or not theme.manifest:
            logger.warning(f"Theme {theme} has no manifest, skipping sync")
            return (0, 0, 0)

        tokens = theme.manifest.get("tokens", {})
        if not tokens:
            logger.warning(f"Theme {theme.name} has no tokens in manifest")
            return (0, 0, 0)

        # Flatten all categories into a single dict keyed by token name
        desired_tokens = {}
        for category, category_tokens in tokens.items():
            if not isinstance(category_tokens, dict):
                continue
            for token_data in cls._flatten_tokens(category, category_tokens):
                desired_tokens[token_data["name"]] = token_data

        # Fetch all existing theme tokens for this theme in one query
        existing_tokens = {
            t.name: t for t in DesignToken.objects.filter(source="theme", theme=theme)
        }

        to_create = []
        to_update = []
        update_fields = [
            "value",
            "token_type",
            "description",
            "priority_level",
            "is_locked",
            "is_active",
            "tier_restriction",
        ]

        for token_name, token_data in desired_tokens.items():
            if token_name in existing_tokens:
                # Update existing token
                obj = existing_tokens[token_name]
                obj.value = token_data["value"]
                obj.token_type = token_data["token_type"]
                obj.description = token_data.get("description", "")
                obj.priority_level = 2
                obj.is_locked = True
                obj.is_active = True
                obj.tier_restriction = []
                to_update.append(obj)
            else:
                # New token
                to_create.append(
                    DesignToken(
                        name=token_name,
                        source="theme",
                        theme=theme,
                        value=token_data["value"],
                        token_type=token_data["token_type"],
                        description=token_data.get("description", ""),
                        priority_level=2,
                        is_locked=True,
                        is_active=True,
                        tier_restriction=[],
                    )
                )

        with transaction.atomic():
            # Bulk create new tokens (bypasses post_save signals)
            if to_create:
                DesignToken.objects.bulk_create(to_create, batch_size=500)

            # Bulk update existing tokens (bypasses post_save signals)
            if to_update:
                DesignToken.objects.bulk_update(to_update, update_fields, batch_size=500)

            # Delete orphaned theme tokens
            orphan_names = set(existing_tokens.keys()) - set(desired_tokens.keys())
            deleted_count = 0
            if orphan_names:
                deleted_count, _ = DesignToken.objects.filter(
                    source="theme",
                    theme=theme,
                    name__in=orphan_names,
                ).delete()

        created_count = len(to_create)
        updated_count = len(to_update)

        # Invalidate cache once after all bulk operations
        invalidate_token_cache()

        logger.info(
            f"Synced theme '{theme.name}' tokens: "
            f"{created_count} created, {updated_count} updated, {deleted_count} deleted"
        )

        return (created_count, updated_count, deleted_count)

    @classmethod
    def sync_branding_to_design_tokens(cls, branding: ThemeBranding) -> tuple[int, int, int]:
        """
        Sync ThemeBranding customizations to DesignToken records.

        Args:
            branding: ThemeBranding instance to sync

        Returns:
            Tuple of (created_count, updated_count, deleted_count)
        """
        if not branding:
            return (0, 0, 0)

        created_count = 0
        updated_count = 0

        # Track token names we've processed for orphan cleanup
        processed_names = set()

        # Map ThemeBranding fields to categories
        branding_fields = {
            "colors": branding.color_tokens or {},
            "typography": branding.typography_tokens or {},
            "spacing": branding.spacing_tokens or {},
            "borders": branding.border_tokens or {},
            "shadows": branding.shadow_tokens or {},
            "transitions": branding.transition_tokens or {}
            if hasattr(branding, "transition_tokens")
            else {},
            "header": branding.header_tokens or {} if hasattr(branding, "header_tokens") else {},
            "footer": branding.footer_tokens or {} if hasattr(branding, "footer_tokens") else {},
            "menu": branding.menu_tokens or {} if hasattr(branding, "menu_tokens") else {},
            "search": branding.search_tokens or {} if hasattr(branding, "search_tokens") else {},
            "elements": branding.element_tokens or {}
            if hasattr(branding, "element_tokens")
            else {},
            "animations": branding.animation_tokens or {},
        }

        with transaction.atomic():
            for category, category_tokens in branding_fields.items():
                if not isinstance(category_tokens, dict) or not category_tokens:
                    continue

                flattened = cls._flatten_tokens(category, category_tokens)

                for token_data in flattened:
                    token_name = token_data["name"]
                    processed_names.add(token_name)

                    # Create or update DesignToken
                    # Use get_or_create + manual update to set _skip_branding_sync flag
                    try:
                        token = DesignToken.objects.get(name=token_name, source="brand_builder")
                        created = False
                        # Update fields
                        token.value = token_data["value"]
                        token.token_type = token_data["token_type"]
                        token.description = f"Brand customization: {token_name}"
                        token.priority_level = 1
                        token.is_locked = False
                        token.is_active = True
                        token.tier_restriction = []
                    except DesignToken.DoesNotExist:
                        created = True
                        token = DesignToken(
                            name=token_name,
                            source="brand_builder",
                            value=token_data["value"],
                            token_type=token_data["token_type"],
                            description=f"Brand customization: {token_name}",
                            priority_level=1,
                            is_locked=False,
                            is_active=True,
                            tier_restriction=[],
                        )

                    # Skip reverse sync since this token came from branding
                    token._skip_branding_sync = True
                    token.save()

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

            # Delete orphaned brand_builder tokens (customizations that were reset)
            deleted_count, _ = (
                DesignToken.objects.filter(
                    source="brand_builder",
                )
                .exclude(name__in=processed_names)
                .delete()
            )

        logger.info(
            f"Synced branding tokens: "
            f"{created_count} created, {updated_count} updated, {deleted_count} deleted"
        )

        return (created_count, updated_count, deleted_count)

    @classmethod
    def sync_design_token_to_branding(cls, token: DesignToken, branding: ThemeBranding) -> bool:
        """
        Sync a single DesignToken change back to ThemeBranding.

        This enables bidirectional sync when tokens are edited in the admin.

        Args:
            token: DesignToken instance that was changed
            branding: ThemeBranding instance to update

        Returns:
            True if sync was successful, False otherwise
        """
        if token.source != "brand_builder":
            # Only sync brand_builder tokens back to branding
            return False

        # Parse the token name to determine category and key
        category, key = cls._parse_token_name(token.name)
        if not category or not key:
            # This is expected for legacy tokens with non-standard names
            # They'll still work in DesignToken but won't sync back to ThemeBranding
            logger.debug(f"Could not parse token name for branding sync: {token.name}")
            return False

        # Map category to ThemeBranding field
        field_mapping = {
            "colors": "color_tokens",
            "typography": "typography_tokens",
            "spacing": "spacing_tokens",
            "borders": "border_tokens",
            "shadows": "shadow_tokens",
            "transitions": "transition_tokens",
            "header": "header_tokens",
            "footer": "footer_tokens",
            "menu": "menu_tokens",
            "search": "search_tokens",
            "elements": "element_tokens",
            "animations": "animation_tokens",
        }

        field_name = field_mapping.get(category)
        if not field_name or not hasattr(branding, field_name):
            logger.warning(f"No field mapping for category: {category}")
            return False

        # Update the field
        current_tokens = getattr(branding, field_name) or {}
        current_tokens[key] = token.value
        setattr(branding, field_name, current_tokens)

        # Save with update_fields to avoid triggering full post_save processing
        # CSS regeneration is handled by the post_save signal on ThemeBranding
        branding.save(update_fields=[field_name, "updated_at"])

        return True

    @classmethod
    def _flatten_tokens(cls, category: str, tokens: dict, prefix: str = "") -> list[dict]:
        """
        Flatten nested token structure to flat list of token dicts.

        Args:
            category: Token category (e.g., 'colors', 'elements')
            tokens: Nested token dict
            prefix: Prefix for nested keys (used for recursion)

        Returns:
            List of dicts with 'name', 'value', 'token_type', 'description'
        """
        result = []
        category_prefix = cls.CATEGORY_PREFIXES.get(category, "theme")
        token_type = cls.CATEGORY_TOKEN_TYPES.get(category, "spacing")

        for key, value in tokens.items():
            if isinstance(value, dict) and category in ("elements", "widgets"):
                # Handle nested element/widget tokens (e.g., elements.button.radius, widgets.cart.icon-size)
                nested_prefix = f"{prefix}{key}-" if prefix else f"{key}-"
                result.extend(cls._flatten_tokens(category, value, nested_prefix))
            elif isinstance(value, dict):
                # Skip non-primitive values for other categories
                continue
            else:
                # Build token name following CSS convention
                full_key = f"{prefix}{key}" if prefix else key
                token_name = f"{category_prefix}-{full_key}"

                # Infer token type from key if possible
                inferred_type = cls._infer_token_type(key, category)

                result.append(
                    {
                        "name": token_name,
                        "value": str(value),
                        "token_type": inferred_type or token_type,
                        "description": f"{category}: {full_key}",
                    }
                )

        return result

    @classmethod
    def _infer_token_type(cls, key: str, category: str) -> str | None:
        """
        Infer DesignToken.token_type from key name.

        Args:
            key: Token key
            category: Token category

        Returns:
            Inferred token_type or None
        """
        key_lower = key.lower()

        # Check for color indicators
        if any(x in key_lower for x in ["color", "bg", "background", "-light", "-dark", "-hover"]):
            return "color"

        # Check for font indicators
        if any(x in key_lower for x in ["font", "line-height", "letter-spacing", "text-transform"]):
            return "font"

        # Check for spacing indicators
        if any(
            x in key_lower for x in ["padding", "margin", "gap", "space", "height", "width", "size"]
        ):
            return "spacing"

        # Check for border indicators
        if any(x in key_lower for x in ["border", "radius", "rounded"]):
            return "border"

        # Check for shadow indicators
        if "shadow" in key_lower:
            return "shadow"

        # Check for animation indicators
        if any(x in key_lower for x in ["duration", "easing", "timing", "transition", "animation"]):
            return "animation"

        return None

    @classmethod
    def _parse_token_name(cls, token_name: str) -> tuple[str | None, str | None]:
        """
        Parse a token name to extract category and key.

        Args:
            token_name: Full token name (e.g., 'theme-color-primary')

        Returns:
            Tuple of (category, key) or (None, None) if parsing fails
        """
        # Sort prefixes by length (longest first) to avoid ambiguous matches
        # e.g., 'theme-color' should match before 'theme'
        sorted_prefixes = sorted(
            cls.CATEGORY_PREFIXES.items(), key=lambda x: len(x[1]), reverse=True
        )

        for category, prefix in sorted_prefixes:
            if token_name.startswith(f"{prefix}-"):
                key = token_name[len(prefix) + 1 :]  # +1 for the dash

                # For categories with shared 'theme' prefix, validate the key pattern
                if prefix == "theme":
                    # Typography keys start with: font-, line-height-, letter-spacing-
                    if key.startswith(("font-", "line-height-", "letter-spacing-")):
                        return ("typography", key)
                    # Border keys start with: border-, radius-
                    elif key.startswith(("border-", "radius-")):
                        return ("borders", key)
                    # If no specific pattern matches, skip to try other prefixes
                    continue

                return (category, key)

        # Handle legacy/custom token names that start with 'theme-' but don't match patterns
        # These are typically from old branding customizations
        if token_name.startswith("theme-"):
            key = token_name[6:]  # Remove 'theme-' prefix
            # Try to infer category from key content
            key_lower = key.lower()
            if any(x in key_lower for x in ["color", "bg", "background"]):
                return ("colors", key)
            elif any(x in key_lower for x in ["button", "btn"]):
                return ("borders", key)  # Button styles often go to borders
            elif any(
                x in key_lower
                for x in ["h1", "h2", "h3", "h4", "h5", "h6", "text", "font", "align"]
            ):
                return ("typography", key)

        return (None, None)

    @classmethod
    def get_all_theme_token_names(cls, theme: Theme) -> list[str]:
        """
        Get all token names that would be created from a theme manifest.

        Useful for checking what tokens exist before syncing.

        Args:
            theme: Theme instance

        Returns:
            List of token names
        """
        if not theme or not theme.manifest:
            return []

        tokens = theme.manifest.get("tokens", {})
        all_names = []

        for category, category_tokens in tokens.items():
            if not isinstance(category_tokens, dict):
                continue
            flattened = cls._flatten_tokens(category, category_tokens)
            all_names.extend([t["name"] for t in flattened])

        return all_names
