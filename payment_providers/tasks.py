"""
Payment Provider Background Tasks

Celery tasks for payment provider operations.
"""

import logging

from celery import shared_task
from django.core.cache import cache
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(name="payment_providers.notify_merchant_sdk_failure")
def notify_merchant_sdk_failure(
    provider_key, error_type="sdk_load_failure", page_url="", user_agent=""
):
    """
    Send notification email to merchant when a payment SDK fails to load.

    Rate limiting is handled by the calling view (cache-based, 1 per provider per hour).
    This task only runs when the rate limit allows it.
    """
    try:
        from django.conf import settings
        from django.contrib.sites.models import Site

        from core.models import SiteSettings
        from email_system.services.email_sender import EmailSendingService

        # Get merchant admin email
        try:
            site_settings = SiteSettings.objects.first()
            admin_email = site_settings.admin_email if site_settings else None
        except Exception:
            admin_email = None

        if not admin_email:
            logger.warning("Cannot send SDK failure notification - no admin email configured")
            return {"status": "skipped", "reason": "no_admin_email"}

        # Get provider display name
        provider_name = provider_key.replace("_", " ").title()
        try:
            from payment_providers.models import PaymentProviderAccount

            account = (
                PaymentProviderAccount.objects.filter(is_active=True)
                .select_related("component")
                .first()
            )
            if account and account.component and account.component.slug == provider_key:
                provider_name = account.display_name or account.component.name or provider_name
        except Exception:
            pass

        # Get failure count from cache
        cache_key = f"payment_sdk_failure:{provider_key}"
        failure_count = cache.get(cache_key, 1)

        # Build admin URL
        try:
            site = Site.objects.get_current()
            site_url = f"https://{site.domain}" if not settings.DEBUG else f"http://{site.domain}"
        except Exception:
            site_url = "http://localhost:8000"

        from core.translation_utils import get_primary_language

        admin_lang = get_primary_language()
        admin_url = f"{site_url}/{admin_lang}/admin/payment_providers/paymentprovideraccount/"

        context = {
            "provider_name": provider_name,
            "error_type": error_type,
            "timestamp": timezone.now().strftime("%B %d, %Y at %H:%M UTC"),
            "failure_count": failure_count,
            "admin_url": admin_url,
            "page_url": page_url,
        }

        EmailSendingService.send_template_email(
            to_email=admin_email,
            template_type="admin_payment_sdk_failure",
            context=context,
            language=admin_lang,
            enable_tracking=False,
        )

        logger.info(f"Sent SDK failure notification for provider '{provider_key}' to {admin_email}")
        return {"status": "sent", "provider": provider_key}

    except Exception as e:
        logger.error(f"Failed to send SDK failure notification: {e}", exc_info=True)
        return {"status": "error", "error": str(e)}
