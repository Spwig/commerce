"""
Signals for POS app.

Handles automatic splash screen generation when readers are added
or when the site logo changes.
"""

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_save, sender="pos_app.POSTerminalReader")
def on_reader_saved(sender, instance, created, **kwargs):
    """
    Generate splash screen for new Stripe Terminal readers.

    Triggered when:
    - A new reader is created
    - A reader's splash_override_image is changed
    """
    # Only process Stripe Terminal readers
    if not instance.provider or instance.provider.provider_key != "stripe_terminal":
        return

    # Skip if this is just a status update or other minor change
    update_fields = kwargs.get("update_fields")
    if update_fields:
        # If specific fields were updated, only trigger for splash-related fields
        splash_fields = {"splash_override_image", "splash_override_image_id"}
        if not splash_fields.intersection(set(update_fields)):
            return

    # For new readers or explicit saves, queue splash screen generation
    if created:
        logger.info(f"New Stripe reader created: {instance.pk}, queuing splash screen generation")
        _queue_splash_update(instance.pk)


@receiver(post_save, sender="core.SiteSettings")
def on_site_settings_saved(sender, instance, **kwargs):
    """
    Regenerate splash screens when site logo changes.

    Only affects readers that use the auto-generated splash (no override).
    """
    # Check if logo field changed
    # Note: This requires tracking the old value, which we'll handle in the task
    # For now, we'll queue regeneration on any SiteSettings save
    # The task will be smart about skipping if nothing changed

    update_fields = kwargs.get("update_fields")

    # Only trigger if site_logo might have changed
    if update_fields and "site_logo" not in update_fields and "site_logo_id" not in update_fields:
        return

    logger.info("SiteSettings saved, queuing splash screen regeneration check")
    _queue_splash_regeneration()


def _queue_splash_update(reader_pk):
    """Queue a single reader splash screen update."""
    try:
        from pos_app.tasks import update_reader_splash_screen

        update_reader_splash_screen.delay(str(reader_pk))
    except Exception as e:
        logger.warning(f"Could not queue splash screen update: {e}")


def _queue_splash_regeneration():
    """Queue regeneration of all auto-generated splash screens."""
    try:
        from pos_app.tasks import regenerate_all_splash_screens

        regenerate_all_splash_screens.delay()
    except Exception as e:
        logger.warning(f"Could not queue splash screen regeneration: {e}")
