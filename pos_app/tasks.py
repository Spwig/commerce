"""
Celery tasks for POS app.

Handles background processing for splash screen generation and updates.
"""

import logging
import time

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def update_reader_splash_screen(self, reader_pk: str):
    """
    Generate and upload splash screen for a single reader.

    Args:
        reader_pk: UUID of the POSTerminalReader
    """
    from pos_app.models import POSTerminalReader
    from pos_app.services import splash_screen_service

    try:
        reader = POSTerminalReader.objects.select_related("provider").get(pk=reader_pk)
    except POSTerminalReader.DoesNotExist:
        logger.warning(f"Reader {reader_pk} not found, skipping splash screen update")
        return {"success": False, "error": "Reader not found"}

    # Only process Stripe Terminal readers
    if not reader.provider or reader.provider.provider_key != "stripe_terminal":
        logger.info(f"Reader {reader_pk} is not a Stripe Terminal reader, skipping")
        return {"success": False, "error": "Not a Stripe Terminal reader"}

    try:
        result = splash_screen_service.update_reader_splash(reader, force=False)
        logger.info(f"Splash screen update for reader {reader_pk}: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to update splash screen for reader {reader_pk}: {e}")
        # Retry on transient errors
        raise self.retry(exc=e)


@shared_task(bind=True)
def regenerate_all_splash_screens(self):
    """
    Regenerate splash screens for all Stripe Terminal readers that use auto-generated splash.

    Called when site logo changes. Skips readers with custom override images.
    """
    from pos_app.models import POSTerminalProvider, POSTerminalReader
    from pos_app.services import splash_screen_service

    # Find all Stripe Terminal providers
    stripe_providers = POSTerminalProvider.objects.filter(
        provider_key="stripe_terminal", is_active=True
    )

    if not stripe_providers.exists():
        logger.info("No active Stripe Terminal providers, skipping splash regeneration")
        return {"success": True, "processed": 0}

    # Find all readers that:
    # 1. Use a Stripe Terminal provider
    # 2. Don't have a custom splash override
    readers = POSTerminalReader.objects.filter(
        provider__in=stripe_providers, splash_override_image__isnull=True
    ).select_related("provider")

    processed = 0
    errors = 0

    for reader in readers:
        try:
            result = splash_screen_service.update_reader_splash(reader, force=True)
            if result.get("success"):
                processed += 1
            else:
                errors += 1
                logger.warning(f"Splash update failed for reader {reader.pk}: {result}")

            # Rate limit: 100ms delay between Stripe API calls
            time.sleep(0.1)

        except Exception as e:
            errors += 1
            logger.error(f"Error regenerating splash for reader {reader.pk}: {e}")

    logger.info(f"Splash screen regeneration complete: {processed} updated, {errors} errors")
    return {"success": True, "processed": processed, "errors": errors}


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def update_splash_screen_for_reader_override(self, reader_pk: str):
    """
    Update splash screen when a reader's override image is changed.

    This is called when the admin saves a reader with a new custom splash image.
    """
    from pos_app.models import POSTerminalReader
    from pos_app.services import splash_screen_service

    try:
        reader = POSTerminalReader.objects.select_related("provider").get(pk=reader_pk)
    except POSTerminalReader.DoesNotExist:
        logger.warning(f"Reader {reader_pk} not found")
        return {"success": False, "error": "Reader not found"}

    if not reader.provider or reader.provider.provider_key != "stripe_terminal":
        return {"success": False, "error": "Not a Stripe Terminal reader"}

    try:
        # Force regeneration since override changed
        result = splash_screen_service.update_reader_splash(reader, force=True)
        logger.info(f"Override splash update for reader {reader_pk}: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to update override splash for reader {reader_pk}: {e}")
        raise self.retry(exc=e)


# ─────────────────────────────────────────────────────────────────────────────
# Parked Cart Cleanup
# ─────────────────────────────────────────────────────────────────────────────


@shared_task(name="pos_app.cleanup_expired_parked_carts", ignore_result=True)
def cleanup_expired_parked_carts():
    """Delete parked carts that have passed their expires_at time."""
    from django.utils import timezone

    from pos_app.models import ParkedCart

    count, _ = ParkedCart.objects.filter(
        expires_at__lte=timezone.now(),
        restored_at__isnull=True,
    ).delete()
    if count:
        logger.info(f"Cleaned up {count} expired parked carts")
    return {"deleted": count}


# ─────────────────────────────────────────────────────────────────────────────
# Digital Receipt Tasks
# ─────────────────────────────────────────────────────────────────────────────


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def send_pos_receipt_email(self, order_pk: int, email: str = None, language: str = None):
    """
    Send email receipt for a POS order.

    Args:
        order_pk: Order primary key
        email: Recipient email (uses order.email if not provided)
        language: Language code for template
    """
    from orders.models import Order
    from pos_app.services.digital_receipt_service import digital_receipt_service

    try:
        order = (
            Order.objects.prefetch_related("items", "pos_payments")
            .select_related("user", "cashier", "pos_terminal", "pos_terminal__warehouse")
            .get(pk=order_pk)
        )
    except Order.DoesNotExist:
        logger.warning(f"Order {order_pk} not found, skipping receipt email")
        return {"success": False, "error": "Order not found"}

    try:
        result = digital_receipt_service.send_email_receipt(
            order=order,
            email=email,
            language=language,
        )
        logger.info(f"POS receipt email result for order {order_pk}: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to send receipt email for order {order_pk}: {e}")
        raise self.retry(exc=e)


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def send_pos_receipt_sms(self, order_pk: int, phone: str = None):
    """
    Send SMS receipt for a POS order.

    Args:
        order_pk: Order primary key
        phone: Recipient phone number (uses order.phone if not provided)
    """
    from orders.models import Order
    from pos_app.services.digital_receipt_service import digital_receipt_service

    try:
        order = Order.objects.select_related("pos_terminal").get(pk=order_pk)
    except Order.DoesNotExist:
        logger.warning(f"Order {order_pk} not found, skipping receipt SMS")
        return {"success": False, "error": "Order not found"}

    try:
        result = digital_receipt_service.send_sms_receipt(
            order=order,
            phone=phone,
        )
        logger.info(f"POS receipt SMS result for order {order_pk}: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to send receipt SMS for order {order_pk}: {e}")
        raise self.retry(exc=e)


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def send_pos_receipt_whatsapp(self, order_pk: int, phone: str = None):
    """
    Send WhatsApp receipt for a POS order.

    Args:
        order_pk: Order primary key
        phone: Recipient phone number (uses order.phone if not provided)
    """
    from orders.models import Order
    from pos_app.services.digital_receipt_service import digital_receipt_service

    try:
        order = Order.objects.select_related("pos_terminal").get(pk=order_pk)
    except Order.DoesNotExist:
        logger.warning(f"Order {order_pk} not found, skipping receipt WhatsApp")
        return {"success": False, "error": "Order not found"}

    try:
        result = digital_receipt_service.send_whatsapp_receipt(
            order=order,
            phone=phone,
        )
        logger.info(f"POS receipt WhatsApp result for order {order_pk}: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to send receipt WhatsApp for order {order_pk}: {e}")
        raise self.retry(exc=e)


# ─────────────────────────────────────────────────────────────────────────────
# POS License Validation
# ─────────────────────────────────────────────────────────────────────────────


@shared_task(bind=True, max_retries=2, default_retry_delay=300, ignore_result=True)
def validate_pos_license(self):
    """
    Periodic POS license validation against the update server.

    Runs daily via Celery Beat. Updates the local license state and sends
    warning emails when the license is nearing expiration.
    """
    from datetime import timedelta

    from django.utils import timezone

    from component_updates.models import UpdateServerConfig
    from pos_app.license import (
        POS_GRACE_PERIOD_DAYS,
        _validate_against_server,
        clear_pos_license_cache,
    )

    try:
        config = UpdateServerConfig.get_instance()

        if not config.pos_license_key:
            logger.info("No POS license key configured, skipping validation")
            return {"success": True, "status": "not_configured"}

        result = _validate_against_server(config)
        clear_pos_license_cache()

        if result is True:
            logger.info(f"POS license validated: status={config.pos_license_status}")

            # Send expiration warnings
            if config.pos_license_expires_at:
                days_until = (config.pos_license_expires_at - timezone.now()).days
                if days_until in (30, 7, 1):
                    _send_pos_expiration_warning(config, days_until)

            return {"success": True, "status": config.pos_license_status}

        elif result is False:
            logger.warning(f"POS license invalid: status={config.pos_license_status}")

            if config.pos_license_status == "grace" and config.pos_license_expires_at:
                grace_end = config.pos_license_expires_at + timedelta(days=POS_GRACE_PERIOD_DAYS)
                days_left = (grace_end - timezone.now()).days
                _send_pos_expiration_warning(config, days_left, grace=True)

            return {"success": True, "status": config.pos_license_status}

        else:
            logger.warning("Could not reach update server for POS license validation")
            return {"success": False, "status": "server_unreachable"}

    except Exception as exc:
        logger.error(f"POS license validation task failed: {exc}")
        raise self.retry(exc=exc)


def _send_pos_expiration_warning(config, days_remaining, grace=False):
    """Send POS license expiration warning email to admin."""
    try:
        from core.models import SiteSettings

        ss = SiteSettings.objects.first()
        if not ss or not ss.admin_email:
            return

        from email_system.services.email_sender import EmailSendingService

        # Mask the license key for display
        key = config.pos_license_key or ""
        license_key_masked = f"{key[:8]}****{key[-4:]}" if len(key) > 12 else key

        EmailSendingService.send_template_email(
            to_email=ss.admin_email,
            template_type="pos_license_expiration_warning",
            context={
                "days_remaining": days_remaining,
                "license_key_masked": license_key_masked,
                "expires_at": str(config.pos_license_expires_at or ""),
                "is_grace_period": grace,
                "renewal_url": "https://spwig.com/pos",
            },
            language="en",
            enable_tracking=False,
        )

    except Exception as e:
        logger.warning(f"Failed to send POS expiration warning: {e}")
