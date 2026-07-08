"""
Payment Method Filter Service

Filters available payment methods at checkout based on:
1. Customer's country (from shipping address)
2. Merchant's shipping countries
3. Provider's available payment methods
4. Merchant's enabled payment methods
5. Currency compatibility
"""
from typing import List, Dict, Optional, Any
from decimal import Decimal
import logging

from django.db.models import Q
from django.contrib.sites.models import Site

from payment_providers.models import PaymentProviderAccount
from shipping.models import ShippingCountry

logger = logging.getLogger(__name__)


class PaymentMethodFilter:
    """
    Service for filtering payment methods based on regional availability.

    This service implements multi-layered filtering to ensure only appropriate
    payment methods are shown at checkout based on customer location and
    merchant configuration.
    """

    @staticmethod
    def _normalize_country_code(country: str) -> str:
        """
        Normalize country to ISO 3166-1 alpha-2 code.
        Handles both full country names ("Australia") and ISO codes ("AU").

        Args:
            country: Country name or ISO code

        Returns:
            ISO 3166-1 alpha-2 country code (uppercase)
        """
        from django_countries import countries

        if not country:
            return ''

        # If already 2-letter code, just uppercase it
        if len(country) == 2:
            return country.upper()

        # Try to find matching country by name
        for code, name in countries:
            if name.lower() == country.lower():
                return code

        # Fallback: return uppercase (might be invalid, but let filter handle it)
        return country.upper()

    @staticmethod
    def get_available_providers_for_checkout(
        customer_country: str,
        currency: str,
        amount: Optional[Decimal] = None
    ) -> List[PaymentProviderAccount]:
        """
        Get list of payment provider accounts available for checkout.

        This applies all filtering layers:
        1. Only active providers
        2. Merchant ships to customer's country
        3. Provider supports customer's country
        4. Provider has enabled payment methods for customer's country
        5. Provider supports the transaction currency

        Args:
            customer_country: ISO 3166-1 alpha-2 country code or full country name
            currency: ISO 4217 currency code (e.g., 'USD', 'EUR')
            amount: Optional transaction amount (for future min/max filtering)

        Returns:
            List of PaymentProviderAccount objects available for checkout
        """
        # Normalize country (handles both "Australia" and "AU" formats)
        original_country = customer_country
        customer_country = PaymentMethodFilter._normalize_country_code(customer_country)
        currency = currency.upper()

        print(f"💳 Payment providers: country '{original_country}' → normalized '{customer_country}', currency={currency}")
        logger.info(
            f"Filtering payment providers for country={customer_country}, "
            f"currency={currency}, amount={amount}"
        )

        # Layer 1: Get active provider accounts
        active_providers = PaymentProviderAccount.objects.filter(
            is_active=True
        ).select_related('component')

        # Layer 2: Check if merchant ships to customer's country
        ships_to_country = ShippingCountry.objects.filter(
            site_id=1,  # Single-tenant - always site 1
            country_code=customer_country,
            is_active=True
        ).exists()

        if not ships_to_country:
            logger.warning(
                f"Merchant does not ship to {customer_country}. "
                f"No payment methods available."
            )
            return []

        # Layer 3-5: Filter providers by country support and enabled methods
        available_providers = []

        for provider in active_providers:
            # Layer 3: Check if provider has payment methods for this country
            available_methods = provider.get_available_methods_for_country(customer_country)
            if not available_methods:
                logger.debug(
                    f"Provider {provider.component.slug} has no available methods "
                    f"for {customer_country}"
                )
                continue

            # Layer 4: Check if merchant has enabled any methods for this country
            enabled_methods = provider.get_enabled_methods_for_country(customer_country)
            if not enabled_methods:
                logger.debug(
                    f"Provider {provider.component.slug} has no enabled methods "
                    f"for {customer_country}"
                )
                continue

            # Layer 5: Check currency support (via provider capabilities)
            if not PaymentMethodFilter._supports_currency(provider, currency):
                logger.debug(
                    f"Provider {provider.component.slug} does not support "
                    f"currency {currency}"
                )
                continue

            logger.info(
                f"Provider {provider.component.slug} is available with "
                f"{len(enabled_methods)} methods: {', '.join(enabled_methods)}"
            )
            available_providers.append(provider)

        logger.info(
            f"Found {len(available_providers)} available providers for "
            f"{customer_country}/{currency}"
        )

        # Sort by default first, then sort_order, then creation date
        available_providers.sort(
            key=lambda p: (not p.is_default, p.sort_order, -p.created_at.timestamp())
        )

        return available_providers

    @staticmethod
    def get_enabled_payment_methods(
        customer_country: str,
        currency: str
    ) -> Dict[str, List[str]]:
        """
        Get enabled payment methods organized by provider.

        Returns a dictionary mapping provider slugs to lists of enabled
        payment method identifiers for the customer's country.

        Args:
            customer_country: ISO 3166-1 alpha-2 country code
            currency: ISO 4217 currency code

        Returns:
            Dictionary: {provider_slug: [method1, method2, ...], ...}
        """
        available_providers = PaymentMethodFilter.get_available_providers_for_checkout(
            customer_country=customer_country,
            currency=currency
        )

        methods_by_provider = {}

        for provider in available_providers:
            enabled_methods = provider.get_enabled_methods_for_country(customer_country)
            if enabled_methods:
                methods_by_provider[provider.component.slug] = enabled_methods

        return methods_by_provider

    @staticmethod
    def is_payment_method_available(
        provider_slug: str,
        method_slug: str,
        customer_country: str,
        currency: str
    ) -> bool:
        """
        Check if a specific payment method is available for checkout.

        Args:
            provider_slug: Provider identifier (e.g., 'airwallex')
            method_slug: Payment method identifier (e.g., 'card', 'apple_pay')
            customer_country: ISO 3166-1 alpha-2 country code
            currency: ISO 4217 currency code

        Returns:
            True if method is available, False otherwise
        """
        customer_country = customer_country.upper()
        currency = currency.upper()

        try:
            # Get the provider account
            provider = PaymentProviderAccount.objects.get(
                component__slug=provider_slug,
                is_active=True
            )

            # Check merchant ships to country
            ships_to_country = ShippingCountry.objects.filter(
                site_id=1,
                country_code=customer_country,
                is_active=True
            ).exists()

            if not ships_to_country:
                return False

            # Check if method is enabled
            if not provider.is_method_enabled(customer_country, method_slug):
                return False

            # Check currency support
            if not PaymentMethodFilter._supports_currency(provider, currency):
                return False

            return True

        except PaymentProviderAccount.DoesNotExist:
            logger.warning(f"Provider {provider_slug} not found or not active")
            return False

    @staticmethod
    def get_unsupported_countries() -> List[str]:
        """
        Get list of countries where merchant has no payment methods available.

        This is useful for displaying warnings in the admin interface.

        Returns:
            List of ISO 3166-1 alpha-2 country codes
        """
        # Get all shipping countries
        shipping_countries = ShippingCountry.objects.filter(
            site_id=1,
            is_active=True
        ).values_list('country_code', flat=True)

        # Get all active providers
        active_providers = PaymentProviderAccount.objects.filter(is_active=True)

        unsupported = []

        for country_code in shipping_countries:
            has_methods = False

            for provider in active_providers:
                enabled_methods = provider.get_enabled_methods_for_country(country_code)
                if enabled_methods:
                    has_methods = True
                    break

            if not has_methods:
                unsupported.append(country_code)

        return unsupported

    @staticmethod
    def get_payment_method_coverage() -> Dict[str, Any]:
        """
        Get comprehensive payment method coverage statistics.

        Useful for admin dashboard to show which countries have payment coverage.

        Returns:
            Dictionary with coverage statistics:
            {
                'total_shipping_countries': int,
                'countries_with_methods': int,
                'countries_without_methods': int,
                'coverage_percentage': float,
                'coverage_by_country': {country_code: {provider_count, method_count}},
                'unsupported_countries': [country_codes]
            }
        """
        # Get all shipping countries
        shipping_countries = list(ShippingCountry.objects.filter(
            site_id=1,
            is_active=True
        ).values_list('country_code', flat=True))

        # Get all active providers
        active_providers = PaymentProviderAccount.objects.filter(is_active=True)

        coverage_by_country = {}
        countries_with_methods = 0

        for country_code in shipping_countries:
            provider_count = 0
            total_methods = set()

            for provider in active_providers:
                enabled_methods = provider.get_enabled_methods_for_country(country_code)
                if enabled_methods:
                    provider_count += 1
                    total_methods.update(enabled_methods)

            coverage_by_country[country_code] = {
                'provider_count': provider_count,
                'method_count': len(total_methods),
                'methods': sorted(list(total_methods))
            }

            if provider_count > 0:
                countries_with_methods += 1

        total_countries = len(shipping_countries)
        unsupported = [
            code for code, data in coverage_by_country.items()
            if data['provider_count'] == 0
        ]

        coverage_percentage = (
            (countries_with_methods / total_countries * 100)
            if total_countries > 0 else 0
        )

        return {
            'total_shipping_countries': total_countries,
            'countries_with_methods': countries_with_methods,
            'countries_without_methods': len(unsupported),
            'coverage_percentage': round(coverage_percentage, 2),
            'coverage_by_country': coverage_by_country,
            'unsupported_countries': unsupported
        }

    @staticmethod
    def _supports_currency(provider: PaymentProviderAccount, currency: str) -> bool:
        """
        Check if provider supports a specific currency.

        This checks the provider's capabilities or supported currencies list.

        Args:
            provider: PaymentProviderAccount instance
            currency: ISO 4217 currency code

        Returns:
            True if currency is supported, False otherwise
        """
        try:
            # Get provider instance
            provider_instance = provider.get_provider_instance()

            # Check if provider has get_supported_currencies method
            if hasattr(provider_instance, 'get_supported_currencies'):
                supported_currencies = provider_instance.get_supported_currencies()
                return currency.upper() in [c.upper() for c in supported_currencies]

            # Check capabilities for currency support
            if hasattr(provider_instance, 'get_capabilities'):
                capabilities = provider_instance.get_capabilities()
                supported_currencies = capabilities.get('supported_currencies', [])
                return currency.upper() in [c.upper() for c in supported_currencies]

            # If provider doesn't implement currency checking, assume supported
            logger.warning(
                f"Provider {provider.component.slug} does not implement "
                f"currency checking. Assuming {currency} is supported."
            )
            return True

        except Exception as e:
            logger.error(
                f"Error checking currency support for {provider.component.slug}: {e}"
            )
            # On error, assume not supported for safety
            return False
