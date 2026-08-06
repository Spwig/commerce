"""
Payment Providers Context Processors

Provides express checkout information to all templates.
"""

import logging
from typing import Any

from core.license import get_license_manager
from payment_providers.models import PaymentProviderAccount
from payment_providers.services.payment_method_filter import PaymentMethodFilter

logger = logging.getLogger(__name__)


# Mapping of payment method slugs to express checkout button configuration
EXPRESS_CHECKOUT_METHODS = {
    "apple_pay": {
        "slug": "apple_pay",
        "name": "Apple Pay",
        "icon": "fab fa-apple-pay",
        "button_class": "express-checkout__btn--apple",
        "requires_js_check": True,  # Requires ApplePaySession check
        "js_check": "apple-pay",  # Key in mini-cart.js FEATURE_CHECKS registry
    },
    "google_pay": {
        "slug": "google_pay",
        "name": "Google Pay",
        "icon": "fab fa-google-pay",
        "button_class": "express-checkout__btn--google",
        "requires_js_check": False,
    },
    "paypal": {
        "slug": "paypal",
        "name": "PayPal",
        "icon": "fab fa-paypal",
        "button_class": "express-checkout__btn--paypal",
        "requires_js_check": False,
    },
    "klarna": {
        "slug": "klarna",
        "name": "Klarna",
        "icon": "fas fa-credit-card",  # No FA icon for Klarna
        "button_class": "express-checkout__btn--klarna",
        "requires_js_check": False,
    },
    "afterpay": {
        "slug": "afterpay",
        "name": "Afterpay",
        "icon": "fas fa-credit-card",
        "button_class": "express-checkout__btn--afterpay",
        "requires_js_check": False,
    },
    "shop_pay": {
        "slug": "shop_pay",
        "name": "Shop Pay",
        "icon": "fas fa-shopping-bag",
        "button_class": "express-checkout__btn--shop",
        "requires_js_check": False,
    },
}


def get_available_express_methods(
    country_code: str | None = None, currency: str | None = None
) -> list[dict[str, Any]]:
    """
    Get list of express checkout methods available to the visitor.

    When the visitor's country and currency are known, only methods the
    merchant enabled for that country — through a provider account that is
    actually eligible for that country/currency — are surfaced. When the
    country is unknown, only globally-enabled (``_global``) methods are
    exposed, since country-specific overrides can't be honoured yet.

    Args:
        country_code: ISO 3166-1 alpha-2 country code, or None when unknown
        currency: ISO 4217 currency code, or None when unknown

    Returns:
        List of express checkout method configurations
    """
    express_methods = []
    seen_methods = set()  # Avoid duplicates across providers

    try:
        if country_code and currency:
            # Country known: restrict to providers eligible for this
            # country/currency and to the methods enabled for it. The
            # ships-to gate is a cart concern we can't evaluate here.
            providers = PaymentMethodFilter.get_available_providers_for_checkout(
                customer_country=country_code,
                currency=currency,
                require_ships_to=False,
            )
            # get_available_providers_for_checkout only filters is_active, so
            # keep the connected-account requirement the global path enforces —
            # never surface methods from a disconnected account.
            provider_methods = []
            for provider in providers:
                if provider.connection_status != "connected":
                    continue
                # Intersect enabled with available for this country: enabled
                # falls back to _global when a country has no override, so a
                # globally-enabled method can leak into a country where the
                # provider doesn't actually offer it. Only surface methods the
                # provider both enables and makes available here.
                available = set(provider.get_available_methods_for_country(country_code))
                enabled = provider.get_enabled_methods_for_country(country_code)
                provider_methods.append((provider, [m for m in enabled if m in available]))
        else:
            # Country unknown: only methods enabled for all countries
            # (_global) apply regardless of where the visitor is.
            active_providers = PaymentProviderAccount.objects.filter(
                is_active=True, connection_status="connected"
            ).select_related("component")
            provider_methods = [
                (
                    provider,
                    provider.get_enabled_methods_for_country(PaymentProviderAccount.GLOBAL_KEY),
                )
                for provider in active_providers
            ]

        for provider, enabled_methods in provider_methods:
            # Filter for express checkout methods only
            for method_slug in enabled_methods:
                if method_slug in EXPRESS_CHECKOUT_METHODS and method_slug not in seen_methods:
                    method_config = EXPRESS_CHECKOUT_METHODS[method_slug].copy()
                    method_config["provider_slug"] = provider.component.slug
                    method_config["provider_id"] = str(provider.id)
                    express_methods.append(method_config)
                    seen_methods.add(method_slug)

    except Exception as e:
        logger.error(f"Error getting express checkout methods: {e}")

    return express_methods


def payment_providers(request) -> dict[str, Any]:
    """
    Context processor that provides payment provider information to templates.

    Provides:
        - payments_enabled: Whether payments are enabled (False in trial mode)
        - has_payment_providers: Whether any payment providers are configured
        - express_checkout_methods: List of available express checkout methods
        - show_payment_setup_prompt: Whether to show setup prompt (staff only, no providers)
    """
    # Check license status
    license_manager = get_license_manager()
    payments_enabled = license_manager.has_feature("payment_processing")
    is_licensed = license_manager.is_valid()

    # Check for configured providers
    has_payment_providers = PaymentProviderAccount.objects.filter(is_active=True).exists()

    # Get express checkout methods (only if licensed and providers exist)
    express_checkout_methods = []
    if payments_enabled and has_payment_providers:
        # Resolve the visitor's country (GeoIP) and currency so the methods
        # shown belong to a provider eligible for that country/currency.
        geo_location = getattr(request, "geo_location", None)
        country_code = geo_location.get("country_code") if geo_location else None
        currency = getattr(request, "currency", None)
        express_checkout_methods = get_available_express_methods(country_code, currency)

    # Show setup prompt to staff if no providers configured
    is_staff = getattr(request.user, "is_staff", False)
    show_payment_setup_prompt = is_staff and not has_payment_providers and payments_enabled

    # Show trial mode banner to staff
    show_trial_mode_banner = is_staff and not is_licensed

    return {
        "payments_enabled": payments_enabled,
        "is_licensed": is_licensed,
        "has_payment_providers": has_payment_providers,
        "express_checkout_methods": express_checkout_methods,
        "show_payment_setup_prompt": show_payment_setup_prompt,
        "show_trial_mode_banner": show_trial_mode_banner,
    }
