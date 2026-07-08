# -*- coding: utf-8 -*-
"""
Rate Service - Calculate shipping rates from providers.

Orchestrates rate calculation workflow:
1. Retrieve provider instance from ProviderAccount
2. Build provider-specific request from shipment data
3. Call provider get_rates() API
4. Return standardized rate list
"""
import logging
from typing import Dict, Any, List, Optional
from django.utils.translation import gettext_lazy as _

from shipping.providers.registry import ProviderRegistry
from shipping.utils.encryption import decrypt_credentials

logger = logging.getLogger(__name__)


def get_origin_address(destination_country_code: str) -> Dict[str, str]:
    """
    Resolve the best origin/warehouse address for shipping to a destination country.

    Resolution order:
    1. ShippingCountry.source_warehouse for the destination country
    2. CountryWarehouseFallback warehouses (by priority)
    3. SiteSettings business address (final fallback)

    Args:
        destination_country_code: ISO 3166-1 alpha-2 country code (e.g., 'US', 'SG')

    Returns:
        Origin address dictionary with keys: country, postal_code, state, city, address1, address2
    """
    from shipping.models import ShippingCountry, CountryWarehouseFallback

    # 1. Try primary warehouse from ShippingCountry
    try:
        shipping_country = ShippingCountry.objects.select_related('source_warehouse').filter(
            country_code=destination_country_code.upper(),
            is_active=True,
            source_warehouse__isnull=False,
        ).first()

        if shipping_country and shipping_country.source_warehouse:
            warehouse = shipping_country.source_warehouse
            logger.debug(
                "Using primary warehouse '%s' for destination %s",
                warehouse.name, destination_country_code
            )
            return _warehouse_to_address(warehouse)
    except Exception as e:
        logger.warning("Error looking up primary warehouse for %s: %s", destination_country_code, e)

    # 2. Try fallback warehouses
    try:
        shipping_country = ShippingCountry.objects.filter(
            country_code=destination_country_code.upper(),
            is_active=True,
        ).first()

        if shipping_country:
            fallback = CountryWarehouseFallback.objects.select_related('warehouse').filter(
                country=shipping_country,
            ).order_by('priority').first()

            if fallback and fallback.warehouse:
                logger.debug(
                    "Using fallback warehouse '%s' (priority %d) for destination %s",
                    fallback.warehouse.name, fallback.priority, destination_country_code
                )
                return _warehouse_to_address(fallback.warehouse)
    except Exception as e:
        logger.warning("Error looking up fallback warehouse for %s: %s", destination_country_code, e)

    # 3. Final fallback: SiteSettings business address
    try:
        from core.models import SiteSettings
        settings = SiteSettings.objects.first()
        if settings and settings.address_line_1:
            logger.debug("Using SiteSettings business address as shipping origin")
            return {
                'country': settings.shipping_origin_country or settings.country or '',
                'postal_code': settings.postal_code or '',
                'state': settings.state_province or '',
                'city': settings.city or '',
                'address1': settings.address_line_1 or '',
                'address2': settings.address_line_2 or '',
            }
    except Exception as e:
        logger.warning("Error loading SiteSettings for origin address: %s", e)

    # Absolute fallback - empty address (caller should handle this)
    logger.warning("No origin address configured for destination %s", destination_country_code)
    return {
        'country': '',
        'postal_code': '',
        'state': '',
        'city': '',
        'address1': '',
        'address2': '',
    }


def _warehouse_to_address(warehouse) -> Dict[str, str]:
    """Convert a catalog.Warehouse model instance to an address dictionary."""
    return {
        'country': warehouse.country or '',
        'postal_code': warehouse.postal_code or '',
        'state': warehouse.state_province or '',
        'city': warehouse.city or '',
        'address1': warehouse.address_line1 or '',
        'address2': warehouse.address_line2 or '',
    }


class RateService:
    """Service for calculating shipping rates from providers."""

    @staticmethod
    def get_rates(
        provider_account,
        origin: Dict[str, str],
        destination: Dict[str, str],
        parcels: List[Dict[str, Any]],
        options: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get shipping rates from a provider.

        Args:
            provider_account: ProviderAccount instance
            origin: Origin address dictionary
                {
                    'country': 'US',
                    'postal_code': '10001',
                    'state': 'NY',
                    'city': 'New York',
                    'address1': '123 Main St'
                }
            destination: Destination address dictionary (same format)
            parcels: List of parcel dictionaries
                [{
                    'length': 10,  # cm
                    'width': 10,
                    'height': 5,
                    'weight': 500,  # grams
                    'value': 100.00,  # USD
                    'currency': 'USD'
                }]
            options: Optional shipping options
                {
                    'insurance': True,
                    'signature': False,
                    'saturday_delivery': False
                }

        Returns:
            List of rate dictionaries:
            [{
                'service_code': 'fedex_ground',
                'service_name': 'FedEx Ground',
                'carrier': 'FedEx',
                'rate': Decimal('12.50'),
                'currency': 'USD',
                'delivery_days': 3,
                'delivery_date': datetime(2025, 10, 23),
                'billable_weight': 500
            }]

        Raises:
            ValueError: If provider_account is invalid or parameters missing
            ConnectionError: If provider API call fails
        """
        # Validate provider account
        if not provider_account.is_active:
            raise ValueError(_("Provider account is not active"))

        # Get provider instance
        provider_class = ProviderRegistry.get_provider(provider_account.component.slug)
        if not provider_class:
            raise ValueError(
                _("Provider '%(provider)s' not found or not registered") %
                {'provider': provider_account.component.slug}
            )

        # Decrypt credentials
        credentials = decrypt_credentials(provider_account.credentials_encrypted)

        # Initialize provider
        provider = provider_class(
            credentials=credentials,
            config=provider_account.settings
        )

        # Call provider API
        logger.info(
            f"Fetching rates from {provider.provider_name} for "
            f"{origin['country']} -> {destination['country']}"
        )

        try:
            rates = provider.get_rates(
                origin=origin,
                destination=destination,
                parcels=parcels,
                options=options or {}
            )

            logger.info(
                f"Retrieved {len(rates)} rates from {provider.provider_name}"
            )

            return rates

        except Exception as e:
            logger.error(
                f"Failed to fetch rates from {provider.provider_name}: {e}",
                exc_info=True
            )
            raise

    @staticmethod
    def get_rates_from_order(provider_account, order, parcels: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Get shipping rates for an order.

        Convenience method that extracts origin/destination from order.

        Args:
            provider_account: ProviderAccount instance
            order: Order instance
            parcels: List of parcel dictionaries

        Returns:
            List of rate dictionaries (same as get_rates())
        """
        # Build destination from order shipping address
        destination = {
            'country': order.shipping_address.get('country', ''),
            'postal_code': order.shipping_address.get('postal_code', ''),
            'state': order.shipping_address.get('state', ''),
            'city': order.shipping_address.get('city', ''),
            'address1': order.shipping_address.get('address1', ''),
            'address2': order.shipping_address.get('address2', ''),
        }

        # Resolve origin address from warehouse → fallback warehouse → SiteSettings
        origin = get_origin_address(destination['country'])

        return RateService.get_rates(
            provider_account=provider_account,
            origin=origin,
            destination=destination,
            parcels=parcels,
            options={}
        )
