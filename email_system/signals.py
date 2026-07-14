"""
Email System Signal Handlers
Automatically sends emails when events occur
"""

import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from email_system.utils.language import get_order_email_language

logger = logging.getLogger(__name__)

# Display names for payment method types
PAYMENT_TYPE_DISPLAY = {
    "credit_card": "Credit Card",
    "debit_card": "Debit Card",
    "bank_transfer": "Bank Transfer",
    "apple_pay": "Apple Pay",
    "google_pay": "Google Pay",
    "paypal": "PayPal",
    "card": "Credit/Debit Card",
    "cash": "Cash",
}


def _get_payment_method_display(order):
    """Build human-readable payment method string from order data."""
    if not order.payment_method_type:
        return "Credit Card"
    display = PAYMENT_TYPE_DISPLAY.get(
        order.payment_method_type, order.payment_method_type.replace("_", " ").title()
    )
    if order.payment_method_last4:
        display += f" ending in {order.payment_method_last4}"
    return display


# ============================================================================
# Order Signals
# ============================================================================


@receiver(post_save, sender="orders.Order")
def send_order_confirmation_email(sender, instance, created, **kwargs):
    """
    Send order confirmation email when order is created

    Triggers: Order creation (created=True)
    Template: order_confirmation
    """
    if not created:
        return

    # Skip if order is from migration (already confirmed elsewhere)
    if instance.migration_job_id:
        logger.debug(f"Skipping order confirmation for migrated order {instance.order_number}")
        return

    # Skip license checkout orders — they use their own email templates
    # (license_purchase_confirmation) sent from license_checkout.services
    meta = instance.metadata or {}
    if meta.get("license_checkout") or meta.get("dev_license_purchase"):
        logger.debug(
            f"Skipping generic order confirmation for license order {instance.order_number}"
        )
        return

    def _send():
        try:
            from email_system.services.email_sender import EmailSendingService

            # Get site for URL building
            try:
                site = Site.objects.get_current()
                site_url = f"http://{site.domain}" if settings.DEBUG else f"https://{site.domain}"
            except Exception:
                site_url = getattr(settings, "SITE_URL", "http://localhost:8000")

            # Prepare context
            context = {
                "customer_name": instance.shipping_name,
                "customer_email": instance.email,
                "order_number": instance.order_number,
                "order_date": instance.created_at.strftime("%B %d, %Y"),
                "order_total": f"{instance.total_amount.currency} {instance.total_amount.amount}",
                "order_url": f"{site_url}/orders/{instance.order_number}/",
                "subtotal": f"{instance.subtotal.currency} {instance.subtotal.amount}",
                "shipping": f"{instance.shipping_cost.currency} {instance.shipping_cost.amount}",
                "tax": f"{instance.tax_amount.currency} {instance.tax_amount.amount}",
                "total": f"{instance.total_amount.currency} {instance.total_amount.amount}",
                "shipping_address": (
                    f"{instance.shipping_name}, "
                    f"{instance.shipping_address1}, "
                    f"{instance.shipping_city}, {instance.shipping_state} "
                    f"{instance.shipping_postal_code}, {instance.shipping_country}"
                ),
                "payment_method": _get_payment_method_display(instance),
            }

            # Get order language (captured at checkout, with user/site fallback)
            language = get_order_email_language(instance)

            # Add activation link for guest orders
            if (
                hasattr(instance, "user")
                and instance.user
                and instance.user.username.startswith("guest_")
            ):
                try:
                    from django.contrib.auth.tokens import default_token_generator
                    from django.utils.encoding import force_bytes
                    from django.utils.http import urlsafe_base64_encode

                    uid = urlsafe_base64_encode(force_bytes(instance.user.pk))
                    token = default_token_generator.make_token(instance.user)
                    activation_url = f"{site_url}/{language}/accounts/activate-guest/{uid}/{token}/"
                    context["activation_url"] = activation_url
                    context["is_guest_order"] = True
                except Exception as e:
                    logger.warning(f"Failed to generate guest activation link: {e}")

            # Send email
            EmailSendingService.send_template_email(
                to_email=instance.email,
                template_type="order_confirmation",
                context=context,
                language=language,
                enable_tracking=True,
            )

            logger.info(
                f"Sent order confirmation email for order {instance.order_number} to {instance.email}"
            )

        except Exception as e:
            logger.error(
                f"Failed to send order confirmation email for order {instance.order_number}: {e}",
                exc_info=True,
            )

    transaction.on_commit(_send)


@receiver(pre_save, sender="orders.Order")
def track_order_status_changes(sender, instance, **kwargs):
    """
    Track original status before save for comparison in post_save

    Stores _original_status attribute on instance
    """
    if instance.pk:
        try:
            original = sender.objects.get(pk=instance.pk)
            instance._original_status = original.status
            instance._original_tracking = original.tracking_number
        except sender.DoesNotExist:
            instance._original_status = None
            instance._original_tracking = None
    else:
        instance._original_status = None
        instance._original_tracking = None


@receiver(post_save, sender="orders.Order")
def send_order_status_emails(sender, instance, created, **kwargs):
    """
    Send emails when order status changes

    Triggers:
    - Status changed to 'shipped' → shipping_confirmation
    - Status changed to 'delivered' → delivery_confirmation
    - Status changed to 'refunded' → refund_notification
    """
    if created:
        return  # Handled by order confirmation signal

    # Check if status changed
    if not hasattr(instance, "_original_status"):
        return

    original_status = instance._original_status
    new_status = instance.status

    if original_status == new_status:
        # Check if tracking number was added
        if hasattr(instance, "_original_tracking"):
            if not instance._original_tracking and instance.tracking_number:
                # Tracking number just added, send shipping notification
                transaction.on_commit(lambda: _send_shipping_confirmation(instance))
        return

    def _send():
        try:
            # Shipped status - send shipping confirmation
            if new_status == "shipped":
                _send_shipping_confirmation(instance)

            # Delivered status - send delivery confirmation
            elif new_status == "delivered":
                _send_delivery_confirmation(instance)

            # Refunded status - send refund notification
            elif new_status == "refunded":
                _send_refund_notification(instance)

        except Exception as e:
            logger.error(
                f"Failed to send order status email for {instance.order_number}: {e}", exc_info=True
            )

    transaction.on_commit(_send)


def _send_shipping_confirmation(order):
    """Send shipping confirmation email"""
    from email_system.services.email_sender import EmailSendingService

    # Get site for URL building
    try:
        site = Site.objects.get_current()
        site_url = f"http://{site.domain}" if settings.DEBUG else f"https://{site.domain}"
    except Exception:
        site_url = getattr(settings, "SITE_URL", "http://localhost:8000")

    context = {
        "customer_name": order.shipping_name,
        "order_number": order.order_number,
        "order_url": f"{site_url}/orders/{order.order_number}/",
        "tracking_number": order.tracking_number or "Not available",
        "tracking_url": f"{site_url}/orders/{order.order_number}/tracking/",
        "carrier": order.carrier.name if order.carrier_id else "Carrier",
        "estimated_delivery": order.estimated_delivery_date.strftime("%B %d, %Y")
        if order.estimated_delivery_date
        else "Soon",
        "shipped_date": order.updated_at.strftime("%B %d, %Y"),
        "shipping_address": (
            f"{order.shipping_name}, "
            f"{order.shipping_address1}, "
            f"{order.shipping_city}, {order.shipping_state} "
            f"{order.shipping_postal_code}"
        ),
    }

    # Get order language (captured at checkout, with user/site fallback)
    language = get_order_email_language(order)

    EmailSendingService.send_template_email(
        to_email=order.email,
        template_type="shipping_confirmation",
        context=context,
        language=language,
        enable_tracking=True,
    )

    logger.info(f"Sent shipping confirmation for order {order.order_number}")


def _send_delivery_confirmation(order):
    """Send delivery confirmation email"""
    from email_system.services.email_sender import EmailSendingService

    # Get site for URL building
    try:
        site = Site.objects.get_current()
        site_url = f"http://{site.domain}" if settings.DEBUG else f"https://{site.domain}"
    except Exception:
        site_url = getattr(settings, "SITE_URL", "http://localhost:8000")

    context = {
        "customer_name": order.shipping_name,
        "order_number": order.order_number,
        "order_url": f"{site_url}/orders/{order.order_number}/",
        "delivery_date": order.updated_at.strftime("%B %d, %Y"),
        "delivered_to": (
            f"{order.shipping_address1}, "
            f"{order.shipping_city}, {order.shipping_state} "
            f"{order.shipping_postal_code}"
        ),
        "signature_required": False,
    }

    # Get order language (captured at checkout, with user/site fallback)
    language = get_order_email_language(order)

    EmailSendingService.send_template_email(
        to_email=order.email,
        template_type="delivery_confirmation",
        context=context,
        language=language,
        enable_tracking=True,
    )

    logger.info(f"Sent delivery confirmation for order {order.order_number}")


def _send_refund_notification(order):
    """Send refund notification email"""
    from email_system.services.email_sender import EmailSendingService

    # Get site for URL building
    try:
        site = Site.objects.get_current()
        site_url = f"http://{site.domain}" if settings.DEBUG else f"https://{site.domain}"
    except Exception:
        site_url = getattr(settings, "SITE_URL", "http://localhost:8000")

    # Get the latest refund for this order (if exists)
    refund = order.refunds.order_by("-created_at").first()

    # Build refund-specific values from Refund model when available
    if refund:
        refund_amount = f"{refund.total_amount.currency} {refund.total_amount.amount}"
        refund_method = refund.refund_method_display or _get_payment_method_display(order)
        refund_reason = refund.get_reason_display() if refund.reason else "Refund requested"
    else:
        refund_amount = f"{order.total_amount.currency} {order.total_amount.amount}"
        refund_method = _get_payment_method_display(order)
        refund_reason = "Refund requested"

    context = {
        "customer_name": order.shipping_name,
        "order_number": order.order_number,
        "order_url": f"{site_url}/orders/{order.order_number}/",
        "refund_amount": refund_amount,
        "refund_method": refund_method,
        "refund_date": order.updated_at.strftime("%B %d, %Y"),
        "refund_reason": refund_reason,
        "processing_days": "5-7 business days",
    }

    # Get order language (captured at checkout, with user/site fallback)
    language = get_order_email_language(order)

    EmailSendingService.send_template_email(
        to_email=order.email,
        template_type="refund_notification",
        context=context,
        language=language,
        enable_tracking=True,
    )

    logger.info(f"Sent refund notification for order {order.order_number}")


# ============================================================================
# Auth Signals (Password Reset, Email Verification)
# ============================================================================

# Note: Django's built-in password reset already sends emails
# We can override these by customizing the password reset views
# to use our template system. This would be done in the accounts app.

# For now, document that auth emails can be integrated by:
# 1. Overriding password_reset_form in accounts/forms.py
# 2. Using EmailSendingService.send_template_email()
# 3. With template_type='password_reset' or 'email_verification'


# ============================================================================
# Site Settings Signals - Auto-Translation
# ============================================================================


@receiver(post_save, sender="core.SiteSettings")
def auto_translate_email_templates_on_language_change(sender, instance, created, **kwargs):
    """
    Automatically create email template translations when site default language changes
    to a non-admin language.

    Triggers when:
    - Admin saves SiteSettings with a default_language
    - Language is NOT one of the 9 admin languages

    What it does:
    - Creates translation jobs for all 12 email templates
    - Dispatches jobs to Celery for async processing
    - Translations are customer-facing (EmailTemplateTranslation model)

    Admin languages (templates already exist):
    - en, es, fr, de, pt, zh-hans, ja, ar, ru

    Custom languages (auto-translate on demand):
    - Any other ISO language code (it, ko, hi, th, etc.)
    """
    # Get admin language codes from settings
    ADMIN_LANGUAGES = [lang[0] for lang in settings.LANGUAGES]

    site_language = instance.default_language

    # Check if this is a non-admin language
    if site_language not in ADMIN_LANGUAGES:
        logger.info(
            f"Site default language set to non-admin language: {site_language}. "
            f"Triggering auto-translation for email templates."
        )

        # Import here to avoid circular imports
        from email_system.services.site_language_translation_service import (
            SiteLanguageTranslationService,
        )

        # Trigger auto-translation (async via Celery)
        translation_service = SiteLanguageTranslationService()
        result = translation_service.auto_translate_for_site_language(
            target_language=site_language, triggered_by="site_settings_change"
        )

        if result["success"]:
            logger.info(
                f"Auto-translation initiated for {site_language}: "
                f"{result['jobs_created']} translation jobs created"
            )
        else:
            logger.warning(
                f"Auto-translation failed for {site_language}: {result.get('message', 'Unknown error')}"
            )
    else:
        logger.debug(
            f"Site language {site_language} is an admin language. "
            f"Using existing base templates, no auto-translation needed."
        )


# ============================================================================
# Admin Notification Signals
# ============================================================================


@receiver(post_save, sender="orders.Order")
def send_admin_new_order_notification(sender, instance, created, **kwargs):
    """
    Send notification to admin when new order is created

    Triggers: Order creation
    Template: admin_new_order
    """
    if not created:
        return

    # Skip migrated orders
    if instance.migration_job_id:
        return

    # Check if admin notifications are enabled
    admin_email = getattr(settings, "ADMIN_ORDER_EMAIL", None)
    if not admin_email:
        logger.debug("Admin order notifications disabled (ADMIN_ORDER_EMAIL not set)")
        return

    def _send():
        try:
            from email_system.services.email_sender import EmailSendingService

            # Get site for URL building
            try:
                site = Site.objects.get_current()
                site_url = f"http://{site.domain}" if settings.DEBUG else f"https://{site.domain}"
            except Exception:
                site_url = getattr(settings, "SITE_URL", "http://localhost:8000")

            context = {
                "order_number": instance.order_number,
                "customer_name": instance.shipping_name,
                "customer_email": instance.email,
                "order_total": f"{instance.total_amount.currency} {instance.total_amount.amount}",
                "order_date": instance.created_at.strftime("%B %d, %Y"),
                "items_count": instance.items.count(),
                "admin_url": f"{site_url}/admin/orders/order/{instance.pk}/change/",
            }

            EmailSendingService.send_template_email(
                to_email=admin_email,
                template_type="admin_new_order",
                context=context,
                language="en",
                enable_tracking=False,  # Don't track admin emails
            )

            logger.info(f"Sent admin notification for new order {instance.order_number}")

        except Exception as e:
            logger.error(
                f"Failed to send admin notification for order {instance.order_number}: {e}",
                exc_info=True,
            )

    transaction.on_commit(_send)


# ============================================================================
# Email Delivery Mode Signals
# ============================================================================


@receiver(pre_save, sender="core.SiteSettings")
def track_delivery_mode_change(sender, instance, **kwargs):
    """Track email delivery mode changes for auto-release."""
    if instance.pk:
        try:
            original = sender.objects.get(pk=instance.pk)
            instance._original_delivery_mode = original.email_delivery_mode
        except sender.DoesNotExist:
            instance._original_delivery_mode = None
    else:
        instance._original_delivery_mode = None


@receiver(post_save, sender="core.SiteSettings")
def auto_release_held_emails_on_mode_change(sender, instance, **kwargs):
    """Release held emails when delivery mode changes from paused to live."""
    original_mode = getattr(instance, "_original_delivery_mode", None)
    new_mode = instance.email_delivery_mode

    if original_mode == "paused" and new_mode == "live":

        def _release():
            try:
                from email_system.services.email_sender import EmailSendingService

                result = EmailSendingService.release_held_emails(send_now=True)
                logger.info(
                    f"Auto-released held emails on mode change: "
                    f"{result['released']} released, {result['sent']} sent, "
                    f"{result['failed']} failed"
                )
            except Exception as e:
                logger.error(f"Failed to auto-release held emails: {e}", exc_info=True)

        transaction.on_commit(_release)
