"""
Fixer.io Provider
https://fixer.io/

API Documentation: https://fixer.io/documentation
"""

import logging
from datetime import datetime
from decimal import Decimal

import requests
from django.utils.translation import gettext_lazy as _

from exchange_rates.providers.base import (
    CurrencyNotSupported,
    ExchangeRateProviderBase,
    RateFetchError,
)

logger = logging.getLogger(__name__)


class FixerProvider(ExchangeRateProviderBase):
    """
    Exchange rate provider for Fixer.io (European Central Bank data).

    Free tier: 100 requests/month
    Paid tier: From $10/month
    """

    # Provider Metadata
    provider_name = "Fixer.io"
    provider_code = "fixer"
    provider_version = "1.0.0"
    provider_author = "Spwig"
    provider_url = "https://fixer.io/"

    # Features
    supports_historical_rates = False  # Paid only
    supports_crypto = False  # Not supported
    supports_time_series = False  # Paid only

    # Rate limiting
    free_tier_requests = 100  # Per month
    paid_tier_requests = 1000  # Basic plan

    # Required credentials
    required_credentials = ["access_key"]

    # API Configuration
    API_BASE_URL = "http://data.fixer.io/api"  # Free tier uses HTTP, paid uses HTTPS

    def get_rate(
        self, from_currency: str, to_currency: str, date: datetime | None = None
    ) -> Decimal:
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
        if date and not self.supports_historical_rates:
            logger.warning("Historical rates require paid plan, using latest rates")
            date = None

        # Fixer.io free tier only supports EUR as base currency
        # We need to calculate cross rates if from_currency is not EUR

        # Get rates with EUR as base
        rates = self.get_rates("EUR", date)

        if from_currency not in rates and from_currency != "EUR":
            raise CurrencyNotSupported(f"Currency {from_currency} not supported")

        if to_currency not in rates and to_currency != "EUR":
            raise CurrencyNotSupported(f"Currency {to_currency} not supported")

        # Calculate cross rate
        if from_currency == "EUR":
            return rates[to_currency]
        elif to_currency == "EUR":
            return Decimal("1") / rates[from_currency]
        else:
            # Convert from -> EUR -> to
            return rates[to_currency] / rates[from_currency]

    def get_rates(self, base_currency: str, date: datetime | None = None) -> dict[str, Decimal]:
        """
        Get all exchange rates for a base currency.

        Note: Free tier only supports EUR as base. For other bases, we return
        calculated cross rates.

        Args:
            base_currency: Base currency code (e.g., 'EUR')
            date: Optional date for historical rates (requires paid plan)

        Returns:
            Dictionary of {currency_code: rate}

        Raises:
            CurrencyNotSupported: If base currency not supported
            RateFetchError: If API request fails
        """
        if not self.credentials.get("access_key"):
            raise RateFetchError("Missing access_key credential")

        # Endpoint selection
        if date:
            if not self.supports_historical_rates:
                logger.warning("Historical rates require paid plan, using latest rates")
                endpoint = "latest"
            else:
                date_str = date.strftime("%Y-%m-%d")
                endpoint = date_str
        else:
            endpoint = "latest"

        url = f"{self.API_BASE_URL}/{endpoint}"

        params = {
            "access_key": self.credentials["access_key"],
        }

        # Free tier only supports EUR as base, paid tier allows base parameter
        # We'll try to set base but it may be ignored on free tier
        if base_currency != "EUR":
            params["base"] = base_currency

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data.get("success", False):
                error = data.get("error", {})
                error_code = error.get("code", "unknown")
                error_msg = error.get("info", "Unknown error")
                raise RateFetchError(f"API error ({error_code}): {error_msg}")

            # Fixer returns rates with EUR as base (or requested base on paid tier)
            actual_base = data.get("base", "EUR")
            rates_data = data.get("rates", {})

            # Convert rates to Decimal
            rates = {code: Decimal(str(rate)) for code, rate in rates_data.items()}

            # If requested base doesn't match actual base, calculate cross rates
            if actual_base != base_currency:
                if base_currency not in rates:
                    raise CurrencyNotSupported(f"Currency {base_currency} not supported")

                base_rate = rates[base_currency]
                cross_rates = {}

                for code, rate in rates.items():
                    cross_rates[code] = rate / base_rate

                # Add actual base currency (EUR)
                cross_rates[actual_base] = Decimal("1") / base_rate

                return cross_rates
            else:
                # Add base currency itself
                rates[actual_base] = Decimal("1")
                return rates

        except requests.exceptions.Timeout:
            raise RateFetchError("Request timed out")
        except requests.exceptions.ConnectionError:
            raise RateFetchError("Connection error")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise RateFetchError("Invalid access_key")
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
            url = f"{self.API_BASE_URL}/latest"
            params = {"access_key": self.credentials.get("access_key", "")}

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                if data.get("success", False):
                    return (True, "Credentials valid. Using ECB data source.")
                else:
                    error = data.get("error", {})
                    error_msg = error.get("info", "Unknown error")
                    return (False, f"API error: {error_msg}")
            elif response.status_code == 401:
                return (False, "Invalid access_key")
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

    def get_supported_currencies(self) -> list[str]:
        """
        Get list of currency codes supported by this provider.

        Returns:
            List of ISO 4217 currency codes
        """
        # Fixer.io supports 170+ currencies
        # We can fetch from the symbols endpoint
        try:
            url = f"{self.API_BASE_URL}/symbols"
            params = {"access_key": self.credentials.get("access_key", "")}

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data.get("success", False):
                    symbols = data.get("symbols", {})
                    return list(symbols.keys())

        except Exception as e:
            logger.warning(f"Failed to fetch currency list from API: {e}")

        # Fallback to common currencies if API fails
        return [
            "EUR",
            "USD",
            "GBP",
            "JPY",
            "AUD",
            "CAD",
            "CHF",
            "CNY",
            "SEK",
            "NZD",
            "MXN",
            "SGD",
            "HKD",
            "NOK",
            "KRW",
            "TRY",
            "RUB",
            "INR",
            "BRL",
            "ZAR",
            "DKK",
            "PLN",
            "TWD",
            "THB",
            "MYR",
            "IDR",
            "HUF",
            "CZK",
            "ILS",
            "CLP",
            "PHP",
            "AED",
            "COP",
            "SAR",
            "RON",
            "BGN",
            "ARS",
            "VND",
            "UAH",
            "BDT",
            "ISK",
            "HRK",
            "EGP",
            "PKR",
            "LKR",
            "MAD",
            "NGN",
            "KES",
            "GHS",
            "UGX",
        ]

    @classmethod
    def get_setup_instructions(cls) -> str:
        """
        Get HTML instructions for setting up this provider.

        Returns:
            HTML string with setup instructions
        """
        return _("""
        <h3>Fixer.io Setup</h3>
        <ol>
            <li>Sign up at <a href="https://fixer.io/product" target="_blank">fixer.io/product</a></li>
            <li>Get your Access Key from the <a href="https://fixer.io/dashboard" target="_blank">dashboard</a></li>
            <li>Enter your Access Key in the credentials field</li>
        </ol>
        <p><strong>Free Tier:</strong> 100 requests/month (sufficient for ~3 daily updates)</p>
        <p><strong>Paid Plans:</strong> From $10/month for 1,000 requests</p>
        <p><strong>Data Source:</strong> European Central Bank (ECB)</p>
        <p><strong>Note:</strong> Free tier only provides EUR as base currency. Historical rates and custom base currencies require paid plans.</p>
        <p><strong>Best For:</strong> EU-based stores requiring ECB compliance</p>
        """)
