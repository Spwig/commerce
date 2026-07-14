"""
Base provider interface for translation integrations.

All translation provider implementations must inherit from TranslationProviderBase
and implement all abstract methods defined here.
"""

from abc import ABC, abstractmethod
from typing import Any


class TranslationProviderBase(ABC):
    """
    Abstract base class for all translation providers.

    Providers (like DeepL, Google Translate, Azure Translator) extend this class
    to provide standardized translation services including:
    - Text translation (single and batch)
    - Connection testing
    - Language support queries

    Attributes:
        provider_key (str): Unique identifier for the provider (e.g., 'deepl')
        provider_name (str): Human-readable name (e.g., 'DeepL')
        capabilities (dict): Dictionary of supported features
        credential_schema (dict): JSON schema for required credentials
    """

    # Must be set by subclass
    provider_key: str = None
    provider_name: str = None

    def __init__(self, credentials: dict[str, Any], config: dict[str, Any] | None = None):
        """
        Initialize provider with credentials and configuration.

        Args:
            credentials: Dictionary of decrypted API credentials
            config: Optional configuration dictionary (rate limits, timeouts, etc.)

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
                'batch_translate': True,
                'language_detection': True,
                'formality': True,
                'glossary': False,
                'html_support': True,
            }
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
                'api_key': {
                    'type': 'password',
                    'label': 'API Key',
                    'help_text': 'Your DeepL API key',
                    'required': True,
                    'placeholder': 'Enter your API key'
                }
            }
        """
        pass

    @property
    @abstractmethod
    def supported_languages(self) -> list[str]:
        """
        Return list of supported language codes.

        Returns:
            List of ISO 639-1 language codes (e.g., ['en', 'de', 'fr', 'ja'])
        """
        pass

    @abstractmethod
    def validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        Validate that required credentials are present and well-formed.

        Args:
            credentials: Dictionary of credential values

        Raises:
            ValueError: If credentials are invalid or missing required fields
        """
        pass

    @abstractmethod
    def test_connection(self) -> dict[str, Any]:
        """
        Test the API connection with the configured credentials.

        Returns:
            Dictionary with test results:
            {
                'success': True/False,
                'message': 'Connection successful!',
                'supported_languages': 31,
            }
        """
        pass

    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate a single text string.

        Args:
            text: Source text to translate
            source_lang: Source language code (e.g., 'en')
            target_lang: Target language code (e.g., 'de')

        Returns:
            Translated text string

        Raises:
            Exception: On translation failure
        """
        pass

    @abstractmethod
    def translate_batch(self, texts: list[str], source_lang: str, target_lang: str) -> list[str]:
        """
        Translate multiple text strings in a single request.

        Args:
            texts: List of source texts
            source_lang: Source language code
            target_lang: Target language code

        Returns:
            List of translated texts (same order as input)

        Raises:
            Exception: On translation failure
        """
        pass
