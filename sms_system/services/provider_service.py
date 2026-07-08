"""
SMS Provider Service.

Provides high-level operations for managing SMS providers,
including installation, configuration, and update checking.
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

from django.conf import settings

from sms_system.providers.registry import SMSProviderRegistry
from sms_system.providers.loader import SMSProviderLoader

logger = logging.getLogger(__name__)


class SMSProviderService:
    """
    Service for managing SMS providers.

    Handles provider discovery, installation, configuration,
    and interaction with the upgrade server.
    """

    COMPONENT_PATH = 'components_data/integrations/sms_provider'

    @classmethod
    def get_component_path(cls, slug: str = None) -> Path:
        """
        Get the path to SMS provider components.

        Args:
            slug: Optional provider slug to get specific provider path

        Returns:
            Path to components directory or specific provider
        """
        base_path = Path(settings.BASE_DIR) / cls.COMPONENT_PATH
        if slug:
            return base_path / slug / 'current'
        return base_path

    @classmethod
    def get_installed_providers(cls) -> List[Dict[str, Any]]:
        """
        Get list of installed SMS providers.

        Returns:
            List of provider info dictionaries
        """
        return SMSProviderRegistry.list_providers()

    @classmethod
    def get_provider_metadata(cls, provider_key: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed metadata for a provider.

        Args:
            provider_key: Provider identifier

        Returns:
            Provider metadata dictionary or None
        """
        return SMSProviderRegistry.get_provider_info(provider_key)

    @classmethod
    def get_credential_schema(cls, provider_key: str) -> Optional[Dict[str, Any]]:
        """
        Get the credential schema for a provider.

        Args:
            provider_key: Provider identifier

        Returns:
            JSON Schema for credentials
        """
        return SMSProviderRegistry.get_credential_schema(provider_key)

    @classmethod
    def get_setup_instructions(cls, provider_key: str) -> Optional[str]:
        """
        Get setup instructions HTML for a provider.

        Args:
            provider_key: Provider identifier

        Returns:
            HTML content string or None
        """
        return SMSProviderRegistry.get_setup_instructions(provider_key)

    @classmethod
    def validate_credentials(
        cls,
        provider_key: str,
        credentials: Dict[str, Any]
    ) -> tuple[bool, Optional[str]]:
        """
        Validate provider credentials.

        Args:
            provider_key: Provider identifier
            credentials: Credentials dictionary

        Returns:
            Tuple of (is_valid, error_message)
        """
        return SMSProviderRegistry.validate_credentials(provider_key, credentials)

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
            credentials: Credentials dictionary

        Returns:
            Dict with 'success' boolean and status details
        """
        return SMSProviderRegistry.test_connection(provider_key, credentials)

    @classmethod
    def fetch_available_providers(cls) -> tuple[List[Dict[str, Any]], bool]:
        """
        Fetch available providers from upgrade server.

        Returns:
            Tuple of (provider list, has_update_server flag)
        """
        try:
            from component_updates.services import UpdateManager

            update_manager = UpdateManager()
            providers = update_manager.list_available_components(
                component_type='sms_provider'
            )
            return providers, True

        except Exception as e:
            logger.error(f"Failed to fetch available providers: {e}")
            return [], False

    @classmethod
    def is_provider_installed(cls, provider_key: str) -> bool:
        """
        Check if a provider is installed.

        Args:
            provider_key: Provider identifier

        Returns:
            True if installed, False otherwise
        """
        return SMSProviderRegistry.is_provider_installed(provider_key)

    @classmethod
    def get_provider_version(cls, provider_key: str) -> Optional[str]:
        """
        Get the installed version of a provider.

        Args:
            provider_key: Provider identifier

        Returns:
            Version string or None if not installed
        """
        manifest = SMSProviderLoader.get_manifest(provider_key)
        if manifest:
            return manifest.get('version')
        return None

    @classmethod
    def get_provider_logo_url(cls, provider_key: str) -> Optional[str]:
        """
        Get the logo URL for a provider.

        Args:
            provider_key: Provider identifier

        Returns:
            Static URL to logo or None
        """
        from django.templatetags.static import static

        manifest = SMSProviderLoader.get_manifest(provider_key)
        if not manifest:
            return None

        logo_raw = manifest.get('logo')
        if not logo_raw:
            return None

        # Handle both dict and string formats
        if isinstance(logo_raw, dict):
            logo_filename = logo_raw.get('file', '')
        else:
            logo_filename = logo_raw
        if not logo_filename:
            return None

        # Find the provider's directory
        provider_path = SMSProviderLoader.get_provider_path(provider_key)
        if not provider_path:
            return None

        # Get the provider slug from the path
        slug = provider_path.parent.name

        # Build static URL
        return static(f"sms/{slug}/current/{logo_filename}")

    @classmethod
    def _get_provider_slug(cls, provider_key: str) -> Optional[str]:
        """Get the directory slug for a provider from its filesystem path."""
        path = SMSProviderLoader.get_provider_path(provider_key)
        if path:
            return path.parent.name
        return None

    @classmethod
    def _get_local_manifest(cls, slug: str) -> Dict[str, Any]:
        """Read the local manifest.json for an installed provider."""
        try:
            from component_updates.integration_paths import INTEGRATIONS_DIR
            manifest_path = INTEGRATIONS_DIR / 'sms_provider' / slug / 'current' / 'manifest.json'
            if manifest_path.exists():
                import json
                with open(manifest_path, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    @classmethod
    def get_providers_for_browse(cls, lang: str = 'en') -> Dict[str, Any]:
        """
        Get providers organized for browse view.

        Args:
            lang: Language code for manifest i18n translation.

        Returns:
            Dict with 'installed', 'available', 'has_update_server',
            'providers_json' keys.
        """
        from component_updates.models import ComponentRegistry
        from providers_common.utils import get_translated_provider_fields

        # Get installed providers from loader
        installed_raw = cls.get_installed_providers()
        installed_keys = {p['key'] for p in installed_raw}

        # ComponentRegistry lookup for version tracking
        installed_db = {
            p.slug: p.current_version
            for p in ComponentRegistry.objects.filter(component_type='sms_provider')
        }

        # Fetch from upgrade server
        available_from_server, has_update_server = cls.fetch_available_providers()

        # Build installed provider list with enriched data
        installed_providers = []
        for provider in installed_raw:
            key = provider['key']
            slug = cls._get_provider_slug(key) or key

            # Get logo URL
            logo_url = cls.get_provider_logo_url(key)

            # Translate name/description
            manifest = SMSProviderLoader.get_manifest(key) or {}
            translated = get_translated_provider_fields(manifest, lang)

            # Check for updates using proper semver comparison
            current_version = provider.get('version', '0.0.0')
            update_available = False
            latest_version = current_version

            for server_provider in available_from_server:
                if server_provider.get('provider_key') == key or server_provider.get('slug') == slug:
                    server_version = server_provider.get('current_version') or server_provider.get('version', '0.0.0')
                    latest_version = server_version
                    try:
                        from packaging import version as pkg_version
                        update_available = pkg_version.parse(server_version) > pkg_version.parse(current_version)
                    except Exception:
                        update_available = False
                    break

            provider_data = {
                'key': key,
                'slug': slug,
                'name': translated['name'] or provider.get('name', key),
                'description': translated['description'] or provider.get('description', ''),
                'version': current_version,
                'logo_url': logo_url,
                'thumbnail_url': logo_url,
                'documentation_url': provider.get('documentation_url', ''),
                'homepage_url': provider.get('homepage_url', ''),
                'capabilities': provider.get('capabilities', {}),
                'setup': provider.get('setup', {}),
                'is_installed': True,
                'update_available': update_available,
                'current_version': current_version,
                'latest_version': latest_version,
                'translations': provider.get('translations', {}),
                'default_language': provider.get('default_language', 'en'),
            }
            installed_providers.append(provider_data)

        # Build available (not installed) provider list from server data
        available_providers = []
        server_slugs_processed = set()

        for server_provider in available_from_server:
            slug = server_provider.get('slug', '')
            provider_key = server_provider.get('provider_key', '')

            # Skip if already installed
            if provider_key in installed_keys or slug in {cls._get_provider_slug(k) for k in installed_keys}:
                continue

            server_manifest = server_provider.get('manifest', {})
            capabilities = server_provider.get('capabilities') or server_manifest.get('capabilities', {})
            translated = get_translated_provider_fields(server_manifest, lang)

            provider_data = {
                'slug': slug,
                'key': provider_key or slug,
                'name': translated['name'] or server_provider.get('name', slug),
                'description': translated['description'] or server_provider.get('description', ''),
                'version': server_provider.get('current_version') or server_provider.get('version', ''),
                'thumbnail_url': server_provider.get('thumbnail_url', ''),
                'documentation_url': server_provider.get('documentation_url', '') or server_manifest.get('documentation_url', ''),
                'homepage_url': server_provider.get('homepage_url', '') or server_manifest.get('homepage_url', ''),
                'capabilities': capabilities,
                'setup': server_manifest.get('setup_wizard', server_manifest.get('setup', {})),
                'is_installed': False,
                'translations': server_manifest.get('translations', {}),
                'default_language': server_manifest.get('default_language', 'en'),
            }
            available_providers.append(provider_data)

        # Add installed providers not returned by update server (offline fallback)
        server_keys = {p.get('provider_key') for p in available_from_server}
        server_slugs = {p.get('slug') for p in available_from_server}
        for slug, db_version in installed_db.items():
            if slug in server_slugs:
                continue
            # Check if this provider is already in installed_providers
            if any(p.get('slug') == slug for p in installed_providers):
                continue
            local_manifest = cls._get_local_manifest(slug)
            if not local_manifest:
                continue
            translated = get_translated_provider_fields(local_manifest, lang)
            logo_url = None
            pk = local_manifest.get('provider_key')
            if pk:
                logo_url = cls.get_provider_logo_url(pk)
            installed_providers.append({
                'key': pk or slug,
                'slug': slug,
                'name': translated['name'] or local_manifest.get('name', slug),
                'description': translated['description'] or local_manifest.get('description', ''),
                'version': db_version or local_manifest.get('version', ''),
                'logo_url': logo_url,
                'thumbnail_url': logo_url,
                'documentation_url': local_manifest.get('documentation_url', '') or local_manifest.get('api_docs_url', ''),
                'homepage_url': local_manifest.get('homepage_url', ''),
                'capabilities': local_manifest.get('capabilities', {}),
                'setup': local_manifest.get('setup_wizard', local_manifest.get('setup', {})),
                'is_installed': True,
                'update_available': False,
                'current_version': db_version or local_manifest.get('version', ''),
                'latest_version': db_version or local_manifest.get('version', ''),
                'translations': local_manifest.get('translations', {}),
                'default_language': local_manifest.get('default_language', 'en'),
            })

        # Build providers_json for modal
        providers_json = []
        for p in installed_providers + available_providers:
            providers_json.append({
                'slug': p.get('slug', p.get('key', '')),
                'name': p.get('name', ''),
                'description': p.get('description', ''),
                'thumbnail_url': p.get('thumbnail_url') or p.get('logo_url', ''),
                'homepage_url': p.get('homepage_url', ''),
                'documentation_url': p.get('documentation_url', ''),
                'capabilities': p.get('capabilities', {}),
                'translations': dict(p.get('translations', {}), default_language=p.get('default_language', 'en')),
                'is_installed': p.get('is_installed', False),
                'current_version': p.get('current_version', p.get('version', '')),
                'latest_version': p.get('latest_version', p.get('version', '')),
                'has_update': p.get('update_available', False),
                'configure_url': '/admin/sms-system/wizard/',
            })

        return {
            'installed': installed_providers,
            'available': available_providers,
            'has_update_server': has_update_server,
            'providers_json': providers_json,
        }

    @classmethod
    def reload_providers(cls):
        """
        Reload all providers from disk.

        Call this after installing or updating a provider.
        """
        SMSProviderRegistry.reload()

    @classmethod
    def create_account_from_wizard(
        cls,
        provider_key: str,
        display_name: str,
        credentials: Dict[str, Any],
        is_default_sms: bool = False,
        is_default_whatsapp: bool = False,
    ):
        """
        Create an SMS provider account from wizard data.

        Args:
            provider_key: Provider identifier
            display_name: Account display name
            credentials: Provider credentials
            is_default_sms: Set as default for SMS
            is_default_whatsapp: Set as default for WhatsApp

        Returns:
            Created SMSProviderAccount instance

        Raises:
            ValueError: If provider not found or validation fails
        """
        from sms_system.models import SMSProviderAccount

        # Validate provider exists
        if not cls.is_provider_installed(provider_key):
            raise ValueError(f"Provider '{provider_key}' is not installed")

        # Validate credentials
        is_valid, error = cls.validate_credentials(provider_key, credentials)
        if not is_valid:
            raise ValueError(f"Invalid credentials: {error}")

        # Create account
        account = SMSProviderAccount(
            provider_key=provider_key,
            display_name=display_name,
            is_default_sms=is_default_sms,
            is_default_whatsapp=is_default_whatsapp,
        )
        account.set_credentials(credentials)
        account.save()

        # Test connection
        account.test_connection()

        return account

    @classmethod
    def build_credential_form_fields(cls, provider_key: str) -> Dict[str, Any]:
        """
        Build form field definitions from credential schema.

        Args:
            provider_key: Provider identifier

        Returns:
            Dict mapping field names to form field definitions
        """
        from django import forms

        schema = cls.get_credential_schema(provider_key)
        if not schema:
            return {}

        properties = schema.get('properties', {})
        required_fields = schema.get('required', [])

        fields = {}
        for field_name, field_schema in properties.items():
            field_type = field_schema.get('type', 'string')
            is_required = field_name in required_fields
            is_secret = field_schema.get('secret', False)

            if field_type == 'string':
                if is_secret:
                    field_class = forms.CharField
                    widget = forms.PasswordInput(attrs={
                        'class': 'vTextField',
                        'autocomplete': 'new-password'
                    })
                else:
                    field_class = forms.CharField
                    widget = forms.TextInput(attrs={'class': 'vTextField'})
            elif field_type == 'integer':
                field_class = forms.IntegerField
                widget = forms.NumberInput(attrs={'class': 'vTextField'})
            elif field_type == 'boolean':
                field_class = forms.BooleanField
                widget = forms.CheckboxInput()
            else:
                field_class = forms.CharField
                widget = forms.TextInput(attrs={'class': 'vTextField'})

            fields[field_name] = {
                'field_class': field_class,
                'widget': widget,
                'required': is_required and not is_secret,  # Secrets not required on edit
                'label': field_schema.get('title', field_name.replace('_', ' ').title()),
                'help_text': field_schema.get('description', ''),
                'initial': field_schema.get('default'),
                'order': field_schema.get('order', 999),
            }

        # Sort by order
        sorted_fields = dict(
            sorted(fields.items(), key=lambda x: x[1]['order'])
        )

        return sorted_fields
