"""
Payment Providers Context Processors

Provides express checkout information to all templates.
"""
import logging
from typing import Dict, Any, List

from django.conf import settings

from core.license import get_license_manager
from payment_providers.models import PaymentProviderAccount

logger = logging.getLogger(__name__)


# Mapping of payment method slugs to express checkout button configuration
EXPRESS_CHECKOUT_METHODS = {
    'apple_pay': {
        'slug': 'apple_pay',
        'name': 'Apple Pay',
        'icon': 'fab fa-apple-pay',
        'button_class': 'express-checkout__btn--apple',
        'requires_js_check': True,  # Requires ApplePaySession check
        'js_check': 'apple-pay',  # Key in mini-cart.js FEATURE_CHECKS registry
    },
    'google_pay': {
        'slug': 'google_pay',
        'name': 'Google Pay',
        'icon': 'fab fa-google-pay',
        'button_class': 'express-checkout__btn--google',
        'requires_js_check': False,
    },
    'paypal': {
        'slug': 'paypal',
        'name': 'PayPal',
        'icon': 'fab fa-paypal',
        'button_class': 'express-checkout__btn--paypal',
        'requires_js_check': False,
    },
    'klarna': {
        'slug': 'klarna',
        'name': 'Klarna',
        'icon': 'fas fa-credit-card',  # No FA icon for Klarna
        'button_class': 'express-checkout__btn--klarna',
        'requires_js_check': False,
    },
    'afterpay': {
        'slug': 'afterpay',
        'name': 'Afterpay',
        'icon': 'fas fa-credit-card',
        'button_class': 'express-checkout__btn--afterpay',
        'requires_js_check': False,
    },
    'shop_pay': {
        'slug': 'shop_pay',
        'name': 'Shop Pay',
        'icon': 'fas fa-shopping-bag',
        'button_class': 'express-checkout__btn--shop',
        'requires_js_check': False,
    },
}


def get_available_express_methods() -> List[Dict[str, Any]]:
    """
    Get list of available express checkout methods from all active providers.

    Returns:
        List of express checkout method configurations
    """
    express_methods = []
    seen_methods = set()  # Avoid duplicates across providers

    try:
        # Get all active payment providers
        active_providers = PaymentProviderAccount.objects.filter(
            is_active=True,
            connection_status='connected'
        ).select_related('component')

        for provider in active_providers:
            # Get enabled methods from all countries (union of all)
            all_enabled_methods = set()

            for country_code, methods in provider.enabled_payment_methods.items():
                all_enabled_methods.update(methods)

            # Filter for express checkout methods only
            for method_slug in all_enabled_methods:
                if method_slug in EXPRESS_CHECKOUT_METHODS and method_slug not in seen_methods:
                    method_config = EXPRESS_CHECKOUT_METHODS[method_slug].copy()
                    method_config['provider_slug'] = provider.component.slug
                    method_config['provider_id'] = str(provider.id)
                    express_methods.append(method_config)
                    seen_methods.add(method_slug)

    except Exception as e:
        logger.error(f"Error getting express checkout methods: {e}")

    return express_methods


def payment_providers(request) -> Dict[str, Any]:
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
    payments_enabled = license_manager.has_feature('payment_processing')
    is_licensed = license_manager.is_valid()

    # Check for configured providers
    has_payment_providers = PaymentProviderAccount.objects.filter(
        is_active=True
    ).exists()

    # Get express checkout methods (only if licensed and providers exist)
    express_checkout_methods = []
    if payments_enabled and has_payment_providers:
        express_checkout_methods = get_available_express_methods()

    # Show setup prompt to staff if no providers configured
    is_staff = getattr(request.user, 'is_staff', False)
    show_payment_setup_prompt = is_staff and not has_payment_providers and payments_enabled

    # Show trial mode banner to staff
    show_trial_mode_banner = is_staff and not is_licensed

    return {
        'payments_enabled': payments_enabled,
        'is_licensed': is_licensed,
        'has_payment_providers': has_payment_providers,
        'express_checkout_methods': express_checkout_methods,
        'show_payment_setup_prompt': show_payment_setup_prompt,
        'show_trial_mode_banner': show_trial_mode_banner,
    }
