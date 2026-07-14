"""
Base class for exchange rate provider components.
All exchange rate providers must inherit from this class.

Pattern follows shipping/providers/base.py architecture.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import Any


class ExchangeRateProviderBase(ABC):
    """
    Abstract base class for exchange rate providers.

    Providers (like Open Exchange Rates, Fixer, etc.) extend this class
    to provide standardized exchange rate services including:
    - Live rate fetching
    - Historical rate lookup
    - Multi-currency support
    - Credential management

    Attributes:
        provider_key (str): Unique identifier for the provider (e.g., 'openexchangerates')
        provider_name (str): Human-readable name (e.g., 'Open Exchange Rates')
        capabilities (dict): Dictionary of supported features
        credential_schema (dict): JSON schema for required credentials
    """

    # Must be set by subclass
    provider_key: str = None  # e.g., 'openexchangerates'
    provider_name: str = None  # e.g., 'Open Exchange Rates'

    def __init__(self, credentials: dict[str, Any], config: dict[str, Any] | None = None):
        """
        Initialize provider with credentials and configuration.

        Args:
            credentials: Dictionary of decrypted API credentials
            config: Optional configuration dictionary

        Raises:
            ValueError: If credentials are invalid or missing
        """
        if not self.provider_key:
            raise ValueError("provider_key must be set by subclass")
        if not self.provider_name:
            raise ValueError("provider_name must be set by subclass")

        self.credentials = credentials
        self.config = config or {}

        # Validate credentials against schema
        self.validate_credentials(credentials)

    @property
    @abstractmethod
    def capabilities(self) -> dict[str, bool]:
        """
        Return dictionary of provider capabilities.

        Example:
            {
                'live_rates': True,         # Can fetch current rates
                'historical': True,         # Can fetch historical rates
                'crypto': False,            # Supports cryptocurrency
                'time_series': False,       # Supports time series data
                'bulk_fetch': True,         # Can fetch all rates at once
            }

        Returns:
            Dictionary mapping capability names to boolean values
        """
        pass

    @property
    @abstractmethod
    def credential_schema(self) -> dict[str, Any]:
        """
        Return JSON schema describing required credentials.

        Used to generate dynamic credential entry forms and validate inputs.

        Example:
            {
                'type': 'object',
                'properties': {
                    'api_key': {
                        'type': 'string',
                        'title': 'API Key',
                        'description': 'Your API key from provider dashboard',
                        'required': True,
                        'secret': True  # Will be encrypted and masked
                    },
                    'plan_tier': {
                        'type': 'string',
                        'title': 'Plan Tier',
                        'enum': ['free', 'developer', 'enterprise'],
                        'default': 'free',
                        'description': 'Your subscription plan'
                    }
                }
            }

        Returns:
            JSON schema dictionary
        """
        pass

    @abstractmethod
    def validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        Validate credentials against schema and business logic.

        Args:
            credentials: Dictionary of credential values

        Raises:
            ValueError: If credentials are invalid or missing required fields
        """
        pass

    @abstractmethod
    def redact_credentials(self, credentials: dict[str, Any]) -> dict[str, Any]:
        """
        Redact sensitive credential values for logging.

        Args:
            credentials: Original credentials dictionary

        Returns:
            Dictionary with sensitive values masked (e.g., 'api_***456')
        """
        pass

    @abstractmethod
    def test_connection(self) -> dict[str, Any]:
        """
        Test API connection and credential validity.

        Should make a simple API call to verify credentials work.

        Returns:
            Dictionary with test results:
            {
                'success': True,
                'message': 'Connection successful',
                'details': {
                    'account_name': 'My Account',
                    'plan_tier': 'developer',
                    'supported_currencies': 170,
                    'requests_remaining': 9543
                }
            }
        """
        pass

    @abstractmethod
    def get_rate(
        self, from_currency: str, to_currency: str, date: datetime | None = None
    ) -> Decimal:
        """
        Get exchange rate between two currencies.

        Args:
            from_currency: Source currency code (e.g., 'USD')
            to_currency: Target currency code (e.g., 'EUR')
            date: Optional date for historical rate (None = latest)

        Returns:
            Exchange rate as Decimal (e.g., 0.85 means 1 USD = 0.85 EUR)

        Raises:
            CurrencyNotSupported: If currency pair not supported
            RateFetchError: If API request fails
        """
        pass

    @abstractmethod
    def get_rates(self, base_currency: str, date: datetime | None = None) -> dict[str, Decimal]:
        """
        Get all exchange rates for a base currency.

        Args:
            base_currency: Base currency code (e.g., 'USD')
            date: Optional date for historical rates (None = latest)

        Returns:
            Dictionary of {currency_code: rate} (e.g., {'EUR': Decimal('0.85'), 'GBP': Decimal('0.73')})

        Raises:
            CurrencyNotSupported: If base currency not supported
            RateFetchError: If API request fails
        """
        pass

    @abstractmethod
    def get_supported_currencies(self) -> list[str]:
        """
        Get list of currency codes supported by this provider.

        Returns:
            List of ISO 4217 currency codes (e.g., ['USD', 'EUR', 'GBP', ...])
        """
        pass

    def supports_currency_pair(self, from_currency: str, to_currency: str) -> bool:
        """
        Check if provider supports a specific currency pair.

        Args:
            from_currency: Source currency code
            to_currency: Target currency code

        Returns:
            True if both currencies are supported, False otherwise
        """
        supported = self.get_supported_currencies()
        return from_currency in supported and to_currency in supported

    def get_provider_info(self) -> dict:
        """
        Get provider metadata for display in admin.

        Returns:
            Dictionary with provider information
        """
        return {
            "key": self.provider_key,
            "name": self.provider_name,
            "capabilities": self.capabilities,
        }


# Custom Exceptions
class CurrencyNotSupported(Exception):
    """Raised when currency is not supported by provider"""

    pass


class RateFetchError(Exception):
    """Raised when rate fetch fails (API error, network error, etc.)"""

    pass
