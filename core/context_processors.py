"""
Context processors for the shop application.
"""

import logging
from datetime import timedelta

from django.core.cache import cache
from django.utils import timezone

logger = logging.getLogger(__name__)

BADGE_CACHE_KEY = "admin_menu_badges"
BADGE_CACHE_TTL = 60  # seconds


def admin_theme(request):
    """
    Context processor to provide admin theme information.
    """
    # Get theme preference from session, cookie, or user preference
    theme = "dark"  # default theme (changed to dark)

    if request.user.is_authenticated:
        # Check if user has a theme preference stored
        user_theme = getattr(request.user, "admin_theme_preference", None)
        if user_theme:
            theme = user_theme

    # Check session for theme preference
    if "admin_theme" in request.session:
        theme = request.session["admin_theme"]

    # Check cookie for theme preference
    elif "admin_theme" in request.COOKIES:
        theme = request.COOKIES["admin_theme"]

    # Check for system preference via CSS media query support
    # This will be handled by JavaScript on the frontend

    return {
        "admin_theme": theme,
        "available_themes": ["light", "dark"],
    }


def _compute_badges():
    """
    Compute badge counts for admin menu items.
    Returns a dict of badge keys to counts/values.
    Reusable by both the context processor and the badge API endpoint.
    """
    badges = {}

    # --- Existing badges ---

    try:
        from orders.models import Order

        orders_count = Order.objects.filter(status__in=["pending", "processing"]).count()
        if orders_count > 0:
            badges["orders_new"] = orders_count
    except Exception:
        logger.debug("Badge computation failed for orders_new", exc_info=True)

    try:
        from cart.models import Cart

        abandoned_threshold = timezone.now() - timedelta(hours=24)
        carts_count = (
            Cart.objects.filter(updated_at__lt=abandoned_threshold, items__isnull=False)
            .distinct()
            .count()
        )
        if carts_count > 0:
            badges["carts_abandoned"] = carts_count
    except Exception:
        logger.debug("Badge computation failed for carts_abandoned", exc_info=True)

    try:
        from shipping.models import Shipment

        shipments_count = Shipment.objects.filter(status__in=["created", "labeled"]).count()
        if shipments_count > 0:
            badges["shipments_pending"] = shipments_count
    except Exception:
        logger.debug("Badge computation failed for shipments_pending", exc_info=True)

    try:
        from component_updates.models import ComponentRegistry

        updates_count = ComponentRegistry.objects.filter(
            update_available=True, locked=False
        ).count()
        if updates_count > 0:
            badges["design_updates"] = updates_count
            badges["component_updates"] = updates_count
    except Exception:
        logger.debug("Badge computation failed for design/component_updates", exc_info=True)

    try:
        from product_feeds.models import FeedProviderAccount

        feed_errors_count = FeedProviderAccount.objects.filter(
            is_active=True, sync_status="error"
        ).count()
        if feed_errors_count > 0:
            badges["feed_errors"] = feed_errors_count
    except Exception:
        logger.debug("Badge computation failed for feed_errors", exc_info=True)

    try:
        from management.models import SystemStatus

        status = SystemStatus.get_instance()
        if status.update_available:
            badges["platform_update"] = True
            badges["platform_update_version"] = status.available_version or ""
    except Exception:
        logger.debug("Badge computation failed for platform_update", exc_info=True)

    try:
        hotfix_result = cache.get("hotfix_check_result")
        if hotfix_result and hotfix_result.get("hotfix_available"):
            badges["hotfix_available"] = 1
    except Exception:
        logger.debug("Badge computation failed for hotfix_available", exc_info=True)

    # --- New badges ---

    try:
        from orders.models import ReturnRequest

        returns_count = ReturnRequest.objects.filter(status="pending").count()
        if returns_count > 0:
            badges["returns_pending"] = returns_count
    except Exception:
        logger.debug("Badge computation failed for returns_pending", exc_info=True)

    try:
        from admin_api.models import CustomerMessage

        unread_count = CustomerMessage.objects.filter(status="unread").count()
        if unread_count > 0:
            badges["messages_unread"] = unread_count
    except Exception:
        logger.debug("Badge computation failed for messages_unread", exc_info=True)

    try:
        from catalog.models import ProductReview

        reviews_count = ProductReview.objects.filter(is_approved=False).count()
        if reviews_count > 0:
            badges["reviews_pending"] = reviews_count
    except Exception:
        logger.debug("Badge computation failed for reviews_pending", exc_info=True)

    try:
        from email_system.models import EmailOutbox

        failed_emails = EmailOutbox.objects.filter(status__in=["failed", "bounced"]).count()
        if failed_emails > 0:
            badges["emails_failed"] = failed_emails
    except Exception:
        logger.debug("Badge computation failed for emails_failed", exc_info=True)

    try:
        from payment_providers.models import PaymentTransaction

        recent_threshold = timezone.now() - timedelta(days=7)
        failed_payments = PaymentTransaction.objects.filter(
            status="failed", created_at__gte=recent_threshold
        ).count()
        if failed_payments > 0:
            badges["payments_failed"] = failed_payments
    except Exception:
        logger.debug("Badge computation failed for payments_failed", exc_info=True)

    try:
        from form_builder.models import FormResponse

        forms_count = FormResponse.objects.filter(status="submitted").count()
        if forms_count > 0:
            badges["forms_submitted"] = forms_count
    except Exception:
        logger.debug("Badge computation failed for forms_submitted", exc_info=True)

    try:
        from django.db.models import F

        from catalog.models import StockItem

        low_stock_count = (
            StockItem.objects.filter(
                product__track_inventory=True,
                product__is_deleted=False,
                warehouse__is_active=True,
                on_hand__gt=F("allocated"),
                on_hand__lte=F("allocated") + F("product__low_stock_threshold"),
            )
            .values("product")
            .distinct()
            .count()
        )
        if low_stock_count > 0:
            badges["low_stock"] = low_stock_count
    except Exception:
        logger.debug("Badge computation failed for low_stock", exc_info=True)

    # --- Actionable badges for additional menu items ---

    try:
        from catalog.models import Booking

        bookings_count = Booking.objects.filter(status="pending_confirmation").count()
        if bookings_count > 0:
            badges["bookings_pending"] = bookings_count
    except Exception:
        logger.debug("Badge computation failed for bookings_pending", exc_info=True)

    try:
        from subscriptions.models import CustomerSubscription

        past_due_count = CustomerSubscription.objects.filter(status="past_due").count()
        if past_due_count > 0:
            badges["subscriptions_past_due"] = past_due_count
    except Exception:
        logger.debug("Badge computation failed for subscriptions_past_due", exc_info=True)

    try:
        from loyalty.models import LoyaltyRedemption

        redemptions_count = LoyaltyRedemption.objects.filter(status="pending").count()
        if redemptions_count > 0:
            badges["loyalty_redemptions_pending"] = redemptions_count
    except Exception:
        logger.debug("Badge computation failed for loyalty_redemptions_pending", exc_info=True)

    try:
        from affiliate.models import Payout

        payouts_count = Payout.objects.filter(status__in=["pending", "processing"]).count()
        if payouts_count > 0:
            badges["affiliate_payouts_pending"] = payouts_count
    except Exception:
        logger.debug("Badge computation failed for affiliate_payouts_pending", exc_info=True)

    try:
        from sms_system.models import SMSOutbox

        sms_failed_count = SMSOutbox.objects.filter(status="failed").count()
        if sms_failed_count > 0:
            badges["sms_failed"] = sms_failed_count
    except Exception:
        logger.debug("Badge computation failed for sms_failed", exc_info=True)

    try:
        from translations.models import TranslationJob

        translations_failed_count = TranslationJob.objects.filter(status="failed").count()
        if translations_failed_count > 0:
            badges["translations_failed"] = translations_failed_count
    except Exception:
        logger.debug("Badge computation failed for translations_failed", exc_info=True)

    try:
        from blog.models import BlogPost

        drafts_count = BlogPost.objects.filter(status="draft").count()
        if drafts_count > 0:
            badges["blog_drafts"] = drafts_count
    except Exception:
        logger.debug("Badge computation failed for blog_drafts", exc_info=True)

    return badges


def menu_badges(request):
    """
    Context processor to provide badge counts for admin menu items.
    Shows counts for items requiring merchant attention.
    Uses a 60-second cache since badge counts are global (status-based).
    """
    if not (request.user.is_authenticated and request.user.is_staff):
        return {"menu_badges": {}}

    # Try cache first
    cached = cache.get(BADGE_CACHE_KEY)
    if cached is not None:
        return {"menu_badges": cached}

    try:
        badges = _compute_badges()
    except Exception as e:
        logger.warning(f"Error computing menu badges: {e}")
        badges = {}

    cache.set(BADGE_CACHE_KEY, badges, BADGE_CACHE_TTL)
    return {"menu_badges": badges}


def spwig_hq(request):
    """
    Context processor to expose SPWIG_IS_HQ flag to templates.
    Used to conditionally show HQ-only menu items (developer portal, etc.).
    """
    from django.conf import settings as django_settings

    return {"SPWIG_IS_HQ": getattr(django_settings, "SPWIG_IS_HQ", False)}


def license_status(request):
    """
    Context processor to provide license and grace period status to admin templates.
    Used to display the license status banner in the admin header.
    """
    if not (request.user.is_authenticated and request.user.is_staff):
        return {"license_status": None}

    try:
        from core.license import get_license_manager
        from core.license_grace import get_grace_period_status

        license_manager = get_license_manager()
        grace = get_grace_period_status()
        is_valid = license_manager.is_valid()
        license_type = license_manager.get_license_type()

        # Check if this is an expired trial (sandbox mode, not locked out)
        is_expired_trial = False
        if not is_valid:
            license_data = license_manager.get_license_data()
            if license_data:
                is_expired_trial = license_data.get("license", {}).get("license_type") == "trial"

        edition = license_manager.get_edition()
        is_community = license_manager.is_community()
        return {
            "license_status": {
                "is_valid": is_valid,
                "is_sandbox": license_manager.is_sandbox(),
                "edition": edition,
                "is_community": is_community,
                "license_type": license_type,
                "hosting_type": license_manager.get_hosting_type(),
                "is_hosted": license_manager.is_spwig_hosted(),
                "is_shared_fleet": license_manager.is_shared_fleet(),
                "account_status": license_manager.get_account_status(),
                "grace_period_active": grace.is_in_grace_period,
                "warning_phase": grace.is_in_warning_phase,
                "grace_expired": grace.is_locked_out and not is_expired_trial,
                "grace_days_remaining": grace.days_remaining,
                # Community edition is always valid — no expiring-licence banner
                "show_banner": not is_valid and not is_community,
                "is_expired_trial": is_expired_trial,
                "is_account_suspended": (
                    license_manager.is_spwig_hosted()
                    and license_manager.get_account_status()
                    in ("suspended", "read_only", "cancelled")
                ),
            },
            "is_community_edition": is_community,
            "hosted_services": _hosted_services_context(is_community),
        }
    except Exception as e:
        logger.warning(f"Error computing license status: {e}")
        return {
            "license_status": None,
            "is_community_edition": False,
            "hosted_services": {"available": False},
        }


def _hosted_services_context(is_community: bool) -> dict:
    """
    Build the ``hosted_services`` block for admin templates.

    Only relevant under Community edition — paid tiers have plenty of
    headroom and don't need the tile / banner. Reads from the Django
    cache only; the refresh happens on a Celery beat schedule
    (``refresh_hosted_service_usage``). If the cache is cold (fresh
    install, cache flushed, worker not yet run) the block is treated as
    unavailable — no HTTP fetch on the request thread.
    """
    if not is_community:
        return {"available": False}
    try:
        from core.hosted_services import get_usage_snapshot

        snapshot = get_usage_snapshot()
        if snapshot is None:
            return {"available": False}
        return {
            "available": True,
            "services": [snapshot["geoip"], snapshot["geocoder"], snapshot["push"]],
            "any_over_80": snapshot.get("any_over_80", False),
            "any_over_100": snapshot.get("any_over_100", False),
            "upgrade_url": snapshot.get("upgrade_url", "https://updates.spwig.com/upgrade/"),
        }
    except Exception as e:
        logger.debug("hosted_services context skipped: %s", e)
        return {"available": False}


def read_only_status(request):
    """
    Context processor to flag read-only admin users for template use.
    Used to show the read-only banner and hide action buttons.
    """
    if not (request.user.is_authenticated and request.user.is_staff):
        return {"is_admin_read_only": False}

    if request.user.is_superuser:
        return {"is_admin_read_only": False}

    from staff_roles.services import is_effectively_read_only

    return {"is_admin_read_only": is_effectively_read_only(request.user)}


def ssl_status(request):
    """
    Context processor to flag when SSL is not configured.
    Used to display the SSL warning banner in the admin header.
    """
    if not (request.user.is_authenticated and request.user.is_staff):
        return {}

    try:
        from domain_ssl.models import DomainConfiguration

        config = DomainConfiguration.objects.filter(pk=1).values("ssl_mode", "domain").first()
        if not config:
            return {"ssl_not_configured": True}
        return {
            "ssl_not_configured": (config["ssl_mode"] == "none" and bool(config["domain"])),
        }
    except Exception:
        return {}


def site_settings(request):
    """
    Context processor to provide SiteSettings to all templates.
    Makes site_settings available globally in templates.
    """
    from .models import SiteSettings

    try:
        settings = SiteSettings.get_settings()
        lang = getattr(request, "LANGUAGE_CODE", "en")
        cookie_ctx = settings.get_cookie_consent_context(lang) if settings else None
        from .utils import get_default_country

        return {
            "site_settings": settings,
            "cookie_consent_ctx": cookie_ctx,
            "shop_default_country": get_default_country(),
        }
    except Exception as e:
        # Gracefully handle errors - return empty dict if SiteSettings not available
        import logging

        logger = logging.getLogger(__name__)
        logger.warning(f"Error loading site settings: {e}")
        return {"site_settings": None, "cookie_consent_ctx": None, "shop_default_country": "US"}
