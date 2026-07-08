"""
SMS Provider Registry.

Central registry for discovering and accessing SMS providers.
Provides a unified interface for the provider system.
"""
import logging
from typing import Dict, List, Optional, Type, Any

from .loader import SMSProviderLoader

logger = logging.getLogger(__name__)


class SMSProviderRegistry:
    """
    Central registry for SMS providers.

    Provides a unified interface to discover, access, and manage
    SMS providers loaded from component packages.
    """

    @classmethod
    def discover_providers(cls) -> Dict[str, Type]:
        """
        Discover all available SMS providers.

        Returns:
            Dictionary of {provider_key: ProviderClass}
        """
        return SMSProviderLoader.discover_providers()

    @classmethod
    def get_provider_class(cls, provider_key: str) -> Optional[Type]:
        """
        Get a provider class by key.

        Args:
            provider_key: Provider identifier (e.g., 'twilio')

        Returns:
            Provider class or None if not found
        """
        return SMSProviderLoader.get_provider(provider_key)

    @classmethod
    def create_provider_instance(
        cls,
        provider_key: str,
        credentials: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Create an instance of a provider.

        Args:
            provider_key: Provider identifier
            credentials: Provider credentials dictionary
            config: Optional provider configuration

        Returns:
            Provider instance or None if provider not found

        Raises:
            ValueError: If provider not found
        """
        provider_class = cls.get_provider_class(provider_key)
        if not provider_class:
            raise ValueError(f"Unknown SMS provider: {provider_key}")

        return provider_class(credentials, config)

    @classmethod
    def list_providers(cls) -> List[Dict[str, Any]]:
        """
        List all available providers with metadata.

        Returns:
            List of provider info dictionaries with keys:
            - key: Provider identifier
            - name: Display name
            - description: Provider description
            - capabilities: Dict of provider capabilities
            - version: Provider version
            - logo: Logo filename
        """
        return SMSProviderLoader.list_providers()

    @classmethod
    def get_provider_info(cls, provider_key: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a provider.

        Args:
            provider_key: Provider identifier

        Returns:
            Provider info dictionary or None if not found
        """
        manifest = SMSProviderLoader.get_manifest(provider_key)
        if not manifest:
            return None

        return {
            'key': manifest.get('provider_key'),
            'name': manifest.get('name'),
            'description': manifest.get('description'),
            'version': manifest.get('version'),
            'author': manifest.get('author'),
            'capabilities': manifest.get('capabilities', {}),
            'credential_schema': manifest.get('credential_schema', {}),
            'setup_wizard': manifest.get('setup_wizard', {}),
            'logo': manifest.get('logo'),
            'homepage_url': manifest.get('homepage_url'),
            'support_url': manifest.get('support_url'),
            'api_docs_url': manifest.get('api_docs_url'),
        }

    @classmethod
    def get_credential_schema(cls, provider_key: str) -> Optional[Dict[str, Any]]:
        """
        Get the credential schema for a provider.

        Args:
            provider_key: Provider identifier

        Returns:
            JSON Schema for credentials or None
        """
        return SMSProviderLoader.get_credential_schema(provider_key)

    @classmethod
    def get_setup_instructions(cls, provider_key: str) -> Optional[str]:
        """
        Get setup instructions HTML for a provider.

        Args:
            provider_key: Provider identifier

        Returns:
            HTML content string or None
        """
        return SMSProviderLoader.get_setup_instructions(provider_key)

    @classmethod
    def get_providers_by_capability(cls, capability: str) -> List[Dict[str, Any]]:
        """
        Get providers that have a specific capability.

        Args:
            capability: Capability name (e.g., 'sms', 'whatsapp', 'mms')

        Returns:
            List of provider info dictionaries
        """
        providers = cls.list_providers()
        return [
            p for p in providers
            if p.get('capabilities', {}).get(capability, False)
        ]

    @classmethod
    def get_sms_providers(cls) -> List[Dict[str, Any]]:
        """
        Get providers that support SMS.

        Returns:
            List of SMS-capable provider info dictionaries
        """
        return cls.get_providers_by_capability('sms')

    @classmethod
    def get_whatsapp_providers(cls) -> List[Dict[str, Any]]:
        """
        Get providers that support WhatsApp.

        Returns:
            List of WhatsApp-capable provider info dictionaries
        """
        return cls.get_providers_by_capability('whatsapp')

    @classmethod
    def reload(cls):
        """
        Force reload all providers.

        Call this after installing or updating providers.
        """
        SMSProviderLoader.reload_providers()

    @classmethod
    def is_provider_installed(cls, provider_key: str) -> bool:
        """
        Check if a provider is installed.

        Args:
            provider_key: Provider identifier

        Returns:
            True if provider is installed, False otherwise
        """
        return cls.get_provider_class(provider_key) is not None

    @classmethod
    def validate_credentials(
        cls,
        provider_key: str,
        credentials: Dict[str, Any]
    ) -> tuple[bool, Optional[str]]:
        """
        Validate credentials for a provider.

        Args:
            provider_key: Provider identifier
            credentials: Credentials to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            provider = cls.create_provider_instance(provider_key, credentials)
            if hasattr(provider, 'validate_credentials'):
                return provider.validate_credentials()
            return True, None
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            logger.error(f"Error validating credentials for {provider_key}: {e}")
            return False, str(e)

    @classmethod
    def test_connection(
        cls,
        provider_key: str,
        credentials: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Test connection to a provider.

        Args:
            provider_key: Provider identifier
            credentials: Provider credentials

        Returns:
            Dict with 'success' boolean and status details
        """
        try:
            provider = cls.create_provider_instance(provider_key, credentials)
            if hasattr(provider, 'test_connection'):
                return provider.test_connection()
            return {
                'success': True,
                'message': 'Provider does not support connection testing',
            }
        except ValueError as e:
            return {
                'success': False,
                'error': str(e),
            }
        except Exception as e:
            logger.error(f"Error testing connection for {provider_key}: {e}")
            return {
                'success': False,
                'error': str(e),
            }
