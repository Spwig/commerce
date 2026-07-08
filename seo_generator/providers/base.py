"""
Base class for SEO provider components.
All SEO providers must inherit from this class.

Pattern follows exchange_rates/providers/base.py and shipping/providers/base.py architecture.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
from django.utils.translation import gettext_lazy as _


class BaseSEOProvider(ABC):
    """
    Abstract base class for SEO generation providers.

    Providers extend this class to provide standardized SEO generation services including:
    - Meta title generation (~60 chars)
    - Meta description generation (~155 chars)
    - Keyword extraction from content
    - Multi-language support (optional)

    Attributes:
        provider_key (str): Unique identifier for the provider (e.g., 'deterministic', 'openai')
        provider_name (str): Human-readable name (e.g., 'Built-in Generator', 'OpenAI GPT-4')
        capabilities (dict): Dictionary of supported features
        requires_credentials (bool): Whether provider needs API credentials
    """

    # Must be set by subclass
    provider_key: str = None       # e.g., 'deterministic'
    provider_name: str = None      # e.g., 'Built-in Generator'
    requires_credentials: bool = False  # True for external API providers

    def __init__(self, credentials: Optional[Dict[str, Any]] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize provider with optional credentials and configuration.

        Args:
            credentials: Dictionary of API credentials (only for external providers)
            config: Optional configuration dictionary

        Raises:
            ValueError: If provider_key or provider_name not set
        """
        if not self.provider_key:
            raise ValueError(_("provider_key must be set by subclass"))
        if not self.provider_name:
            raise ValueError(_("provider_name must be set by subclass"))

        self.credentials = credentials or {}
        self.config = config or {}

        # Validate credentials if provider requires them
        if self.requires_credentials:
            if not credentials:
                raise ValueError(
                    _("Provider '%(key)s' requires credentials") % {'key': self.provider_key}
                )
            self.validate_credentials(credentials)

    @property
    @abstractmethod
    def capabilities(self) -> Dict[str, bool]:
        """
        Return dictionary of provider capabilities.

        Example:
            {
                'meta_title': True,          # Can generate meta titles
                'meta_description': True,    # Can generate meta descriptions
                'keywords': True,            # Can extract keywords
                'multi_language': False,     # Supports multiple languages natively
                'bulk_generation': True,     # Can generate SEO for multiple items at once
            }

        Returns:
            Dictionary mapping capability names to boolean values
        """
        pass

    def validate_credentials(self, credentials: Dict[str, Any]) -> None:
        """
        Validate credentials against schema and business logic.

        Only called if requires_credentials is True.

        Args:
            credentials: Dictionary of credential values

        Raises:
            ValueError: If credentials are invalid or missing required fields
        """
        # Default implementation for providers without credentials
        pass

    @abstractmethod
    def generate_meta_title(self, content: Dict[str, str], language: str = 'en') -> str:
        """
        Generate SEO meta title from content.

        Args:
            content: Dictionary with content fields:
                - 'name': Primary name/title
                - 'description': Optional description text
                - 'category': Optional category name (for products)
                - 'brand': Optional brand name (for products)
            language: Target language code (default: 'en')

        Returns:
            Generated meta title string (~60 characters)

        Raises:
            GenerationError: If generation fails
        """
        pass

    @abstractmethod
    def generate_meta_description(self, content: Dict[str, str], language: str = 'en') -> str:
        """
        Generate SEO meta description from content.

        Args:
            content: Dictionary with content fields:
                - 'name': Primary name/title
                - 'description': Description text
                - 'category': Optional category name (for products)
                - 'brand': Optional brand name (for products)
            language: Target language code (default: 'en')

        Returns:
            Generated meta description string (~155 characters)

        Raises:
            GenerationError: If generation fails
        """
        pass

    @abstractmethod
    def extract_keywords(self, content: Dict[str, str], max_keywords: int = 10) -> list:
        """
        Extract relevant keywords from content.

        Args:
            content: Dictionary with content fields
            max_keywords: Maximum number of keywords to return

        Returns:
            List of keyword strings

        Raises:
            GenerationError: If extraction fails
        """
        pass

    def generate_seo(self, content: Dict[str, str], language: str = 'en') -> Dict[str, Any]:
        """
        Generate complete SEO package (title, description, keywords).

        Convenience method that calls all generation methods.

        Args:
            content: Dictionary with content fields
            language: Target language code (default: 'en')

        Returns:
            Dictionary with:
                {
                    'meta_title': str,
                    'meta_description': str,
                    'keywords': list
                }

        Raises:
            GenerationError: If generation fails
        """
        return {
            'meta_title': self.generate_meta_title(content, language),
            'meta_description': self.generate_meta_description(content, language),
            'keywords': self.extract_keywords(content)
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
            'capabilities': self.capabilities,
            'requires_credentials': self.requires_credentials,
        }


# Custom Exceptions
class GenerationError(Exception):
    """Raised when SEO generation fails"""
    pass


class ProviderNotAvailable(Exception):
    """Raised when requested provider is not available"""
    pass
