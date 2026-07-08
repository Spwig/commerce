"""
Open Exchange Rates Provider
https://openexchangerates.org/

API Documentation: https://docs.openexchangerates.org/
"""

import requests
import logging
from typing import Dict, Optional, List
from decimal import Decimal
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from exchange_rates.providers.base import (
    ExchangeRateProviderBase,
    CurrencyNotSupported,
    RateFetchError
)

logger = logging.getLogger(__name__)


class OpenExchangeRatesProvider(ExchangeRateProviderBase):
    """
    Exchange rate provider for Open Exchange Rates.

    Free tier: 1,000 requests/month
    Paid tier: From $12/month
    """

    # Provider Metadata
    provider_name = "Open Exchange Rates"
    provider_code = "openexchangerates"
    provider_version = "1.0.0"
    provider_author = "Spwig"
    provider_url = "https://openexchangerates.org/"

    # Features
    supports_historical_rates = False  # Paid only
    supports_crypto = False  # Paid only
    supports_time_series = False  # Paid only

    # Rate limiting
    free_tier_requests = 1000  # Per month
    paid_tier_requests = 0  # Unlimited on paid plans

    # Required credentials
    required_credentials = ['app_id']

    # API Configuration
    API_BASE_URL = "https://openexchangerates.org/api"

    def get_rate(self, from_currency: str, to_currency: str, date: Optional[datetime] = None) -> Decimal:
        """
        Get exchange rate between two currencies.

        Args:
            from_currency: Source currency code (e.g., 'USD')
            to_currency: Target currency code (e.g., 'EUR')
            date: Optional date for historical rate (requires paid plan)

        Returns:
            Exchange rate as Decimal

        Raises:
            CurrencyNotSupported: If currency pair not supported
            RateFetchError: If API request fails
        """
        # Open Exchange Rates only supports USD as base currency on free tier
        # We need to calculate cross rates if from_currency is not USD

        if date and not self.supports_historical_rates:
            logger.warning("Historical rates require paid plan, using latest rates")
            date = None

        # Get rates with USD as base
        rates = self.get_rates('USD', date)

        if from_currency not in rates and from_currency != 'USD':
            raise CurrencyNotSupported(f"Currency {from_currency} not supported")

        if to_currency not in rates and to_currency != 'USD':
            raise CurrencyNotSupported(f"Currency {to_currency} not supported")

        # Calculate cross rate
        if from_currency == 'USD':
            return rates[to_currency]
        elif to_currency == 'USD':
            return Decimal('1') / rates[from_currency]
        else:
            # Convert from -> USD -> to
            return rates[to_currency] / rates[from_currency]

    def get_rates(self, base_currency: str, date: Optional[datetime] = None) -> Dict[str, Decimal]:
        """
        Get all exchange rates for a base currency.

        Note: Free tier only supports USD as base. For other bases, we return
        calculated cross rates.

        Args:
            base_currency: Base currency code (e.g., 'USD')
            date: Optional date for historical rates (requires paid plan)

        Returns:
            Dictionary of {currency_code: rate}

        Raises:
            CurrencyNotSupported: If base currency not supported
            RateFetchError: If API request fails
        """
        if not self.credentials.get('app_id'):
            raise RateFetchError("Missing app_id credential")

        # Endpoint selection
        if date:
            if not self.supports_historical_rates:
                logger.warning("Historical rates require paid plan, using latest rates")
                endpoint = "latest.json"
            else:
                date_str = date.strftime('%Y-%m-%d')
                endpoint = f"historical/{date_str}.json"
        else:
            endpoint = "latest.json"

        url = f"{self.API_BASE_URL}/{endpoint}"

        params = {
            'app_id': self.credentials['app_id'],
            'show_alternative': 'false'  # Don't include alternative/digital currencies on free tier
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if 'error' in data:
                raise RateFetchError(f"API error: {data.get('message', 'Unknown error')}")

            # OXR returns rates with USD as base
            usd_rates = data.get('rates', {})

            # Convert to requested base currency
            if base_currency == 'USD':
                # Direct rates
                return {code: Decimal(str(rate)) for code, rate in usd_rates.items()}
            else:
                # Calculate cross rates
                if base_currency not in usd_rates:
                    raise CurrencyNotSupported(f"Currency {base_currency} not supported")

                base_rate = Decimal(str(usd_rates[base_currency]))
                cross_rates = {}

                for code, rate in usd_rates.items():
                    cross_rates[code] = Decimal(str(rate)) / base_rate

                # Add USD itself
                cross_rates['USD'] = Decimal('1') / base_rate

                return cross_rates

        except requests.exceptions.Timeout:
            raise RateFetchError("Request timed out")
        except requests.exceptions.ConnectionError:
            raise RateFetchError("Connection error")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise RateFetchError("Invalid app_id")
            elif e.response.status_code == 429:
                raise RateFetchError("Rate limit exceeded")
            else:
                raise RateFetchError(f"HTTP error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Unexpected error fetching rates: {e}")
            raise RateFetchError(f"Unexpected error: {str(e)}")

    def validate_credentials(self) -> tuple[bool, str]:
        """
        Validate provider credentials by making a test API call.

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Test with usage endpoint (doesn't count against quota)
            url = f"{self.API_BASE_URL}/usage.json"
            params = {'app_id': self.credentials.get('app_id', '')}

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                usage = data.get('data', {})
                limit = usage.get('plan', {}).get('quota', 'unlimited')
                used = usage.get('usage', {}).get('requests', 0)

                return (True, f"Credentials valid. Usage: {used}/{limit} requests")
            elif response.status_code == 401:
                return (False, "Invalid app_id")
            elif response.status_code == 429:
                return (False, "Rate limit exceeded")
            else:
                return (False, f"API returned status {response.status_code}")

        except requests.exceptions.Timeout:
            return (False, "Connection timed out")
        except requests.exceptions.ConnectionError:
            return (False, "Could not connect to API")
        except Exception as e:
            return (False, f"Error: {str(e)}")

    def get_supported_currencies(self) -> List[str]:
        """
        Get list of currency codes supported by this provider.

        Returns:
            List of ISO 4217 currency codes
        """
        # OXR supports 170+ currencies
        # Rather than hardcode, we fetch from the currencies endpoint
        try:
            url = f"{self.API_BASE_URL}/currencies.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            currencies = response.json()
            return list(currencies.keys())

        except Exception as e:
            logger.warning(f"Failed to fetch currency list from API: {e}")
            # Fallback to common currencies if API fails
            return [
                'USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY', 'SEK', 'NZD',
                'MXN', 'SGD', 'HKD', 'NOK', 'KRW', 'TRY', 'RUB', 'INR', 'BRL', 'ZAR',
                'DKK', 'PLN', 'TWD', 'THB', 'MYR', 'IDR', 'HUF', 'CZK', 'ILS', 'CLP',
                'PHP', 'AED', 'COP', 'SAR', 'RON', 'BGN', 'ARS', 'VND', 'UAH', 'BDT'
            ]

    @classmethod
    def get_setup_instructions(cls) -> str:
        """
        Get HTML instructions for setting up this provider.

        Returns:
            HTML string with setup instructions
        """
        return _("""
        <h3>Open Exchange Rates Setup</h3>
        <ol>
            <li>Sign up at <a href="https://openexchangerates.org/signup" target="_blank">openexchangerates.org/signup</a></li>
            <li>Get your App ID from the <a href="https://openexchangerates.org/account/app-ids" target="_blank">dashboard</a></li>
            <li>Enter your App ID in the credentials field</li>
        </ol>
        <p><strong>Free Tier:</strong> 1,000 requests/month (sufficient for ~30 daily updates)</p>
        <p><strong>Paid Plans:</strong> From $12/month for unlimited requests and hourly updates</p>
        <p><strong>Note:</strong> Free tier only provides USD as base currency and daily updates. Historical rates and cryptocurrency support require paid plans.</p>
        """)
