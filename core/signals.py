"""
Core Signals

Signal handlers for core functionality including:
- 2FA trusted device management
- Maintenance mode cache invalidation
- Help topic semantic search indexing
"""

import logging

from django.db.models.signals import post_delete, post_save, pre_save

logger = logging.getLogger(__name__)


# =============================================================================
# MAINTENANCE MODE CACHE INVALIDATION
# =============================================================================


def warn_on_currency_change(sender, instance, **kwargs):
    """
    Log a warning when SiteSettings.default_currency is changed.
    Existing records retain their original currency — the merchant may need
    to run: manage.py fix_currency_defaults --from-currency X --to-currency Y
    """
    if not instance.pk:
        return
    try:
        old = sender.objects.get(pk=instance.pk)
        if old.default_currency != instance.default_currency:
            logger.warning(
                "Default currency changed from %s to %s. Existing records "
                "retain their original currency. To bulk-update, run: "
                "manage.py fix_currency_defaults --from-currency %s --to-currency %s",
                old.default_currency,
                instance.default_currency,
                old.default_currency,
                instance.default_currency,
            )
    except sender.DoesNotExist:
        pass


def invalidate_maintenance_cache_on_save(sender, instance, **kwargs):
    """
    Invalidate maintenance mode cache when SiteSettings is saved.

    This ensures that changes to maintenance_mode take effect immediately
    rather than waiting for the cache to expire.
    """
    from core.middleware.maintenance import invalidate_maintenance_cache

    try:
        invalidate_maintenance_cache()
        logger.debug("Maintenance mode cache invalidated after SiteSettings save")
    except Exception as e:
        logger.error(f"Error invalidating maintenance cache: {e}")


def revoke_trusted_devices_on_password_change(sender, instance, **kwargs):
    """
    Revoke all trusted devices when a user changes their password.

    This is a security measure to ensure that if a password is compromised
    and then changed, any previously trusted devices are invalidated.
    """
    from django.contrib.auth import get_user_model

    User = get_user_model()

    # Only process for User model
    if sender != User:
        return

    # Check if this is an existing user (has pk) and password has changed
    if instance.pk:
        try:
            old_instance = User.objects.get(pk=instance.pk)
            if old_instance.password != instance.password:
                # Password has changed - revoke all trusted devices
                from core.models import TrustedDevice

                count = TrustedDevice.revoke_all_for_user(instance, reason="Password changed")
                if count:
                    logger.info(
                        f"Revoked {count} trusted device(s) for user {instance.email} "
                        f"due to password change"
                    )
        except User.DoesNotExist:
            # New user, no trusted devices to revoke
            pass
        except Exception as e:
            logger.error(f"Error revoking trusted devices on password change: {e}")


def revoke_trusted_devices_on_mfa_removed(sender, request, user, authenticator, **kwargs):
    """
    Revoke all trusted devices when MFA is disabled.

    When a user disables 2FA, their trusted devices should no longer
    bypass 2FA verification.
    """
    try:
        from core.models import TrustedDevice

        count = TrustedDevice.revoke_all_for_user(user, reason="2FA deactivated")
        if count:
            logger.info(
                f"Revoked {count} trusted device(s) for user {user.email} due to MFA removal"
            )
    except Exception as e:
        logger.error(f"Error revoking trusted devices on MFA removal: {e}")


# =============================================================================
# DOMAIN SYNC ON SITE_URL CHANGE
# =============================================================================


def sync_domain_on_site_url_change(sender, instance, **kwargs):
    """
    When SiteSettings.site_url changes, sync the domain to
    DomainConfiguration.domain and Site.domain so all three stores
    stay consistent. SiteSettings.site_url is the master.
    """
    try:
        from urllib.parse import urlparse

        parsed = urlparse(instance.site_url)
        domain = parsed.hostname or ""
    except Exception:
        return

    if not domain or domain in ("example.com", "localhost", "127.0.0.1"):
        return

    # Check if this is actually a change by comparing to the current value
    update_fields = kwargs.get("update_fields")

    # If update_fields is specified and site_url isn't in it, skip
    if update_fields is not None and "site_url" not in update_fields:
        return

    # Sync to DomainConfiguration.domain (create row if it doesn't exist yet)
    try:
        from domain_ssl.models import DomainConfiguration

        config, _ = DomainConfiguration.objects.get_or_create(pk=1)
        if config.domain != domain:
            config.domain = domain
            config.save(update_fields=["domain", "updated_at"])
            logger.info("Synced DomainConfiguration.domain to %s", domain)
    except Exception as e:
        logger.debug("Could not sync DomainConfiguration.domain: %s", e)

    # Sync to Site.domain (django.contrib.sites)
    try:
        from django.contrib.sites.models import Site

        site = Site.objects.filter(pk=1).first()
        if site and site.domain != domain:
            site.domain = domain
            site.save(update_fields=["domain"])
            logger.info("Synced Site.domain to %s", domain)
    except Exception as e:
        logger.debug("Could not sync Site.domain: %s", e)


# =============================================================================
# HELP TOPIC SEMANTIC SEARCH INDEXING
# =============================================================================


def reindex_help_topic_on_save(sender, instance, created, **kwargs):
    """
    Trigger async reindex when a help topic is saved.

    Only triggers for published topics to avoid indexing drafts.
    Uses cache-based deduplication to prevent flooding the task queue
    when bulk operations (e.g. sync_help) save many topics at once,
    or when containers restart and re-run startup commands.
    """
    # Allow callers to suppress reindexing (e.g. bulk sync operations)
    if getattr(instance, "_skip_reindex", False):
        return

    if instance.is_published:
        try:
            from django.core.cache import cache

            from core.tasks import index_help_topic_async

            # Dedup: skip if a reindex task was already queued recently
            cache_key = f"help_reindex_queued:{instance.id}"
            if cache.get(cache_key):
                logger.debug(f"Skipping duplicate reindex for help topic: {instance.slug}")
                return

            index_help_topic_async.delay(instance.id)
            # 10 minute dedup window - long enough to cover bulk syncs
            # and container restarts, short enough for legitimate re-indexes
            cache.set(cache_key, True, timeout=600)
            logger.debug(f"Queued async reindex for help topic: {instance.slug}")
        except Exception as e:
            logger.error(f"Error queuing help topic reindex: {e}")


def cleanup_help_index_on_delete(sender, instance, **kwargs):
    """
    Log when help index is deleted (CASCADE handles cleanup automatically).
    """
    logger.info(f"Search index for help topic {instance.slug} will be deleted via CASCADE")


def connect_signals():
    """
    Connect all signal handlers.

    This should be called from core.apps.CoreConfig.ready()
    """
    from django.contrib.auth import get_user_model

    User = get_user_model()

    # Connect password change signal
    pre_save.connect(
        revoke_trusted_devices_on_password_change,
        sender=User,
        dispatch_uid="core_revoke_trusted_devices_on_password_change",
    )

    # Connect MFA removed signal (from django-allauth)
    try:
        from allauth.mfa.signals import authenticator_removed

        authenticator_removed.connect(
            revoke_trusted_devices_on_mfa_removed,
            dispatch_uid="core_revoke_trusted_devices_on_mfa_removed",
        )
        logger.debug("Connected MFA removal signal handler")
    except ImportError:
        logger.warning("allauth.mfa.signals not available, MFA removal handler not connected")

    # Connect maintenance cache invalidation signal
    from core.models import SiteSettings

    post_save.connect(
        invalidate_maintenance_cache_on_save,
        sender=SiteSettings,
        dispatch_uid="core_invalidate_maintenance_cache_on_save",
    )
    logger.debug("Connected maintenance cache invalidation signal handler")

    # Connect currency change warning signal
    pre_save.connect(
        warn_on_currency_change, sender=SiteSettings, dispatch_uid="core_warn_on_currency_change"
    )

    # Connect domain sync signal (site_url → DomainConfiguration + Site)
    post_save.connect(
        sync_domain_on_site_url_change,
        sender=SiteSettings,
        dispatch_uid="core_sync_domain_on_site_url_change",
    )
    logger.debug("Connected domain sync signal handler")

    # Connect help topic indexing signals
    from core.models import HelpTopic

    post_save.connect(
        reindex_help_topic_on_save, sender=HelpTopic, dispatch_uid="core_reindex_help_topic_on_save"
    )
    post_delete.connect(
        cleanup_help_index_on_delete,
        sender=HelpTopic,
        dispatch_uid="core_cleanup_help_index_on_delete",
    )
    logger.debug("Connected help topic semantic search signal handlers")
