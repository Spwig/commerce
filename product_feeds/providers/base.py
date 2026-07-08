"""
Base class for product feed provider components.
All product feed providers must inherit from this class.

Pattern follows exchange_rates/providers/base.py architecture.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, List, Any


class FeedProviderBase(ABC):
    """
    Abstract base class for product feed providers.

    Providers (like Google Merchant Center, Facebook Catalog, etc.) extend this class
    to provide standardized feed management services including:
    - Feed generation in multiple formats
    - Feed validation
    - API push to provider
    - Connection testing

    Attributes:
        provider_key (str): Unique identifier for the provider (e.g., 'google_merchant')
        provider_name (str): Human-readable name (e.g., 'Google Merchant Center')
        supported_formats (list): List of supported feed formats ['xml', 'csv', 'json']
        capabilities (dict): Dictionary of supported features
        credential_schema (dict): JSON schema for required credentials
    """

    # Must be set by subclass
    provider_key: str = None       # e.g., 'google_merchant'
    provider_name: str = None      # e.g., 'Google Merchant Center'
    supported_formats: List[str] = ['xml']  # Default to XML

    def __init__(self, credentials: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        """
        Initialize provider with credentials and configuration.

        Args:
            credentials: Dictionary of decrypted API credentials
            config: Optional configuration dictionary including attribute mapping

        Raises:
            ValueError: If credentials are invalid or missing
        """
        if not self.provider_key:
            raise ValueError("provider_key must be set by subclass")
        if not self.provider_name:
            raise ValueError("provider_name must be set by subclass")

        self.credentials = credentials
        self.config = config or {}

        # Validate credentials against schema (only if credentials provided)
        if credentials:
            self.validate_credentials(credentials)

    @property
    @abstractmethod
    def capabilities(self) -> Dict[str, bool]:
        """
        Return dictionary of provider capabilities.

        Example:
            {
                'push_feed': True,           # Can push feed to provider API
                'fetch_feed': True,          # Provider can fetch from hosted URL
                'incremental_updates': True, # Supports delta updates
                'real_time_sync': False,     # Supports real-time product updates
                'scheduled_sync': True,      # Supports scheduled syncs
                'batch_operations': True,    # Supports batch product operations
                'validation': True,          # Provides feed validation
            }

        Returns:
            Dictionary mapping capability names to boolean values
        """
        pass

    @property
    @abstractmethod
    def credential_schema(self) -> Dict[str, Any]:
        """
        Return JSON schema describing required credentials.

        Used to generate dynamic credential entry forms and validate inputs.

        Example:
            {
                'type': 'object',
                'properties': {
                    'merchant_id': {
                        'type': 'string',
                        'title': 'Merchant ID',
                        'description': 'Your Google Merchant Center ID',
                        'required': True,
                        'secret': False
                    },
                    'api_key': {
                        'type': 'string',
                        'title': 'API Key',
                        'description': 'Service account JSON key',
                        'required': True,
                        'secret': True  # Will be encrypted and masked
                    }
                }
            }

        Returns:
            JSON schema dictionary
        """
        pass

    @property
    def attribute_mapping_schema(self) -> Dict[str, Any]:
        """
        Return schema for product attribute mapping.

        Defines how Spwig product fields map to provider-specific feed fields.

        Returns:
            Dictionary with 'required', 'recommended', 'optional' sections
        """
        return {
            'required': {},
            'recommended': {},
            'optional': {}
        }

    @abstractmethod
    def validate_credentials(self, credentials: Dict[str, Any]) -> None:
        """
        Validate credentials against schema and business logic.

        Args:
            credentials: Dictionary of credential values

        Raises:
            ValueError: If credentials are invalid or missing required fields
        """
        pass

    @abstractmethod
    def redact_credentials(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """
        Redact sensitive credential values for logging.

        Args:
            credentials: Original credentials dictionary

        Returns:
            Dictionary with sensitive values masked (e.g., 'api_***456')
        """
        pass

    @abstractmethod
    def test_connection(self) -> Dict[str, Any]:
        """
        Test API connection and credential validity.

        Should make a simple API call to verify credentials work.

        Returns:
            Dictionary with test results:
            {
                'success': True,
                'message': 'Connection successful',
                'details': {
                    'account_name': 'My Store',
                    'merchant_id': '12345',
                    'products_count': 1000
                }
            }
        """
        pass

    @abstractmethod
    def push_feed(self, feed_content: str, format: str) -> Dict[str, Any]:
        """
        Push feed content to provider API.

        Args:
            feed_content: Generated feed content string
            format: Feed format ('xml', 'csv', 'json')

        Returns:
            Dictionary with push results:
            {
                'success': True,
                'message': 'Feed uploaded successfully',
                'items_processed': 1000,
                'items_failed': 5,
                'errors': [...]
            }
        """
        pass

    @abstractmethod
    def validate_feed(self, feed_content: str, format: str) -> Dict[str, Any]:
        """
        Validate feed content against provider requirements.

        Args:
            feed_content: Generated feed content string
            format: Feed format ('xml', 'csv', 'json')

        Returns:
            Dictionary with validation results:
            {
                'valid': True,
                'errors': [],
                'warnings': ['10 products missing GTIN'],
                'products_validated': 1000
            }
        """
        pass

    def get_feed_url(self) -> Optional[str]:
        """
        Get URL where feed is hosted for provider to fetch.

        Override if provider supports fetching from URL.

        Returns:
            Feed URL or None if not supported
        """
        return None

    def supports_incremental_updates(self) -> bool:
        """
        Whether provider supports delta/incremental updates.

        Returns:
            True if incremental updates are supported
        """
        return self.capabilities.get('incremental_updates', False)

    def get_rate_limits(self) -> Dict[str, int]:
        """
        Return API rate limits for this provider.

        Returns:
            Dictionary with rate limit information
        """
        return {
            'requests_per_minute': 60,
            'requests_per_day': 10000,
            'products_per_batch': 1000
        }

    def get_provider_info(self) -> Dict:
        """
        Get provider metadata for display in admin.

        Returns:
            Dictionary with provider information
        """
        return {
            'key': self.provider_key,
            'name': self.provider_name,
            'supported_formats': self.supported_formats,
            'capabilities': self.capabilities,
        }


# Custom Exceptions
class FeedValidationError(Exception):
    """Raised when feed content fails validation"""
    pass


class FeedPushError(Exception):
    """Raised when feed push to provider fails"""
    pass


class ProviderConnectionError(Exception):
    """Raised when connection to provider fails"""
    pass


class UnsupportedFormatError(Exception):
    """Raised when requested feed format is not supported"""
    pass
