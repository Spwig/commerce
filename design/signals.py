"""Django signals for design app.

Handles automatic cache invalidation when design tokens are modified,
and theme cache invalidation when active theme changes.
"""

import logging

from django.core.cache import cache
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from .models import DesignToken, GlobalDesignSettings
from .token_resolver import invalidate_token_cache

logger = logging.getLogger(__name__)


@receiver(post_save, sender=DesignToken)
def invalidate_cache_on_token_save(sender, instance, created, **kwargs):
    """Invalidate token resolver cache when token is created or updated.

    Args:
        sender: DesignToken model class
        instance: DesignToken instance that was saved
        created: True if new instance was created, False if updated
        **kwargs: Additional signal arguments
    """
    action = "created" if created else "updated"
    logger.info(f"DesignToken '{instance.name}' {action}, invalidating token caches")
    invalidate_token_cache()


@receiver(post_delete, sender=DesignToken)
def invalidate_cache_on_token_delete(sender, instance, **kwargs):
    """Invalidate token resolver cache when token is deleted.

    Args:
        sender: DesignToken model class
        instance: DesignToken instance that was deleted
        **kwargs: Additional signal arguments
    """
    logger.info(f"DesignToken '{instance.name}' deleted, invalidating token caches")
    invalidate_token_cache()


# =============================================================================
# Theme CSS Cache Invalidation
# =============================================================================


@receiver(pre_save, sender=GlobalDesignSettings)
def track_theme_change(sender, instance, **kwargs):
    """Track if active theme is changing (for cache invalidation)."""
    if instance.pk:
        try:
            old_instance = GlobalDesignSettings.objects.get(pk=instance.pk)
            instance._previous_theme_id = old_instance.active_theme_id
        except GlobalDesignSettings.DoesNotExist:
            instance._previous_theme_id = None
    else:
        instance._previous_theme_id = None


@receiver(post_save, sender=GlobalDesignSettings)
def invalidate_theme_cache_on_change(sender, instance, created, **kwargs):
    """Clear theme CSS cache when active theme changes.

    This ensures theme switches are immediate without restart.
    Uses hash-based cache keys so only stale entries need clearing.
    Also triggers theme token sync when active theme changes.
    """
    previous_theme_id = getattr(instance, "_previous_theme_id", None)
    current_theme_id = instance.active_theme_id

    # Only invalidate if theme actually changed
    if created or previous_theme_id != current_theme_id:
        logger.info(
            f"Active theme changed from {previous_theme_id} to {current_theme_id}, "
            "invalidating theme CSS caches"
        )

        # Clear theme-related cache patterns
        try:
            # Clear all theme CSS cache entries
            cache.delete_pattern("theme_css_*")
            # Clear page builder page cache — cache_page() stores full HTML
            # responses that include {% theme_css %} output with theme CSS links.
            # Without this, cached pages serve the old theme's CSS URL.
            cache.delete_pattern("views.decorators.cache.*")
        except AttributeError:
            # Some cache backends don't support delete_pattern
            # For these, we rely on hash-based cache busting
            pass

        # Clear specific cache keys (must match keys used in theme_utils.py)
        cache.delete("active_theme_instance")
        cache.delete("active_theme_css_url")

        # Invalidate template tag caches
        invalidate_token_cache()

        # Sync theme tokens to DesignToken when active theme changes
        if instance.active_theme:
            try:
                from .token_sync_service import TokenSyncService

                created_count, updated_count, deleted_count = (
                    TokenSyncService.sync_theme_to_design_tokens(instance.active_theme)
                )
                logger.info(
                    f"Theme token sync completed: {created_count} created, "
                    f"{updated_count} updated, {deleted_count} deleted"
                )
            except Exception as e:
                logger.error(f"Failed to sync theme tokens: {e}")


# =============================================================================
# ThemeBranding Token Sync
# =============================================================================


# Import ThemeBranding lazily to avoid circular imports
def _get_theme_branding():
    from .theme_models import ThemeBranding

    return ThemeBranding


@receiver(post_save)
def sync_branding_to_design_tokens(sender, instance, created, **kwargs):
    """Sync ThemeBranding customizations to DesignToken records.

    This enables the DesignToken admin to show brand customizations.
    """
    ThemeBranding = _get_theme_branding()
    if sender != ThemeBranding:
        return

    # Avoid recursive syncing
    if getattr(instance, "_skip_token_sync", False):
        return

    try:
        from .token_sync_service import TokenSyncService

        created_count, updated_count, deleted_count = (
            TokenSyncService.sync_branding_to_design_tokens(instance)
        )
        logger.info(
            f"Branding token sync completed: {created_count} created, "
            f"{updated_count} updated, {deleted_count} deleted"
        )
    except Exception as e:
        logger.error(f"Failed to sync branding tokens: {e}")


# =============================================================================
# Bidirectional Sync: DesignToken → ThemeBranding
# =============================================================================


@receiver(post_save, sender=DesignToken)
def sync_design_token_to_branding(sender, instance, created, **kwargs):
    """Sync DesignToken changes back to ThemeBranding.

    When a brand_builder token is edited in the admin, update ThemeBranding
    so the branding builder reflects the change.
    """
    # Only sync brand_builder tokens
    if instance.source != "brand_builder":
        return

    # Avoid recursive syncing
    if getattr(instance, "_skip_branding_sync", False):
        return

    try:
        ThemeBranding = _get_theme_branding()
        branding = ThemeBranding.objects.first()
        if not branding:
            return

        from .token_sync_service import TokenSyncService

        # Mark branding to skip token sync (avoid infinite loop)
        branding._skip_token_sync = True
        success = TokenSyncService.sync_design_token_to_branding(instance, branding)

        if success:
            logger.info(f"DesignToken '{instance.name}' synced to ThemeBranding")
    except Exception as e:
        logger.error(f"Failed to sync DesignToken to ThemeBranding: {e}")


# =============================================================================
# ThemeBranding CSS Regeneration & Cache Invalidation
# =============================================================================


@receiver(pre_save)
def track_branding_token_changes(sender, instance, **kwargs):
    """Track if branding tokens changed (for CSS regeneration)."""
    ThemeBranding = _get_theme_branding()
    if sender != ThemeBranding:
        return

    # Define token fields that affect CSS
    token_fields = [
        "color_tokens",
        "typography_tokens",
        "spacing_tokens",
        "border_tokens",
        "shadow_tokens",
        "animation_tokens",
        "transition_tokens",
        "header_tokens",
        "footer_tokens",
        "menu_tokens",
        "search_tokens",
        "element_tokens",
        "component_overrides",
        "custom_css",
    ]

    # If update_fields is specified and doesn't include token fields, skip
    update_fields = kwargs.get("update_fields")
    if update_fields is not None:
        # Check if any token field is being updated
        if not any(f in update_fields for f in token_fields):
            instance._tokens_changed = False
            return

    if instance.pk:
        try:
            old_instance = ThemeBranding.objects.get(pk=instance.pk)
            # Check if any token field changed
            instance._tokens_changed = any(
                getattr(old_instance, f, None) != getattr(instance, f, None) for f in token_fields
            )
            instance._old_css_hash = old_instance.css_hash
        except ThemeBranding.DoesNotExist:
            instance._tokens_changed = True
            instance._old_css_hash = None
    else:
        instance._tokens_changed = True
        instance._old_css_hash = None


@receiver(post_save)
def regenerate_css_and_clear_cache(sender, instance, created, **kwargs):
    """Regenerate CSS and clear caches when branding tokens change.

    This ensures that any change to branding tokens immediately:
    1. Regenerates the compiled CSS
    2. Clears all related caches
    3. Updates the css_hash for cache busting
    """
    ThemeBranding = _get_theme_branding()
    if sender != ThemeBranding:
        return

    # Skip if we're in a recursive save from generate_css()
    if getattr(instance, "_regenerating_css", False):
        return

    # Skip if this is a partial save that doesn't include token fields
    update_fields = kwargs.get("update_fields")
    if update_fields is not None:
        token_fields = [
            "color_tokens",
            "typography_tokens",
            "spacing_tokens",
            "border_tokens",
            "shadow_tokens",
            "animation_tokens",
            "transition_tokens",
            "header_tokens",
            "footer_tokens",
            "menu_tokens",
            "search_tokens",
            "element_tokens",
            "component_overrides",
            "custom_css",
        ]
        if not any(f in update_fields for f in token_fields):
            return

    # Check if tokens changed or CSS is missing
    tokens_changed = getattr(instance, "_tokens_changed", False)
    css_missing = not instance.generated_css or not instance.css_hash

    if tokens_changed or css_missing:
        try:
            # Mark as regenerating to prevent recursion
            instance._regenerating_css = True

            # Regenerate CSS
            instance.generate_css()
            logger.info(f"ThemeBranding CSS regenerated, new hash: {instance.css_hash}")

            # Clear all brand CSS caches
            old_hash = getattr(instance, "_old_css_hash", None)
            if old_hash:
                cache.delete(f"brand_css_{old_hash}")

            # Clear pattern-based caches
            try:
                cache.delete_pattern("brand_css_*")
                cache.delete_pattern("theme_*")
                cache.delete_pattern("layered_css_*")
            except AttributeError:
                # delete_pattern not available, clear specific keys
                cache.delete("brand_css")
                cache.delete("layered_css")

            logger.info("Branding caches cleared")

        except Exception as e:
            logger.error(f"Failed to regenerate CSS or clear caches: {e}")
        finally:
            instance._regenerating_css = False
