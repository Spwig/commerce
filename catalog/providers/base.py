"""
Base adapter class for external license providers.

This module defines the interface that all provider adapters must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class BaseLicenseProviderAdapter(ABC):
    """
    Abstract base class for external license provider adapters.

    All provider-specific adapters (Keygen, License Spring, etc.) must inherit
    from this class and implement all abstract methods.
    """

    # Provider metadata (must be set by subclasses)
    provider_key = None  # Unique identifier (e.g., 'keygen', 'licensespring')
    provider_name = None  # Human-readable name (e.g., 'Keygen.sh')

    def __init__(self, provider):
        """
        Initialize adapter with provider configuration.

        Args:
            provider: LicenseProvider model instance or None (for schema access only)
        """
        self.provider = provider

        # Allow None provider for cases where we only need schema/metadata
        # (e.g., during wizard setup before provider is created)
        if provider is not None:
            self.api_endpoint = provider.api_endpoint
            self.api_key = provider.api_key
            self.api_secret = provider.api_secret
            self.config = provider.provider_config
        else:
            self.api_endpoint = None
            self.api_key = None
            self.api_secret = None
            self.config = {}

    @property
    @abstractmethod
    def capabilities(self) -> Dict:
        """
        Return dictionary of provider capabilities.

        Returns:
            Dict with boolean values for each capability:
            {
                'create_license': True,
                'validate_license': True,
                'activate_device': True,
                'deactivate_device': True,
                'suspend_license': True,
                'revoke_license': True,
                'webhooks': True,
                'offline_validation': False,
                'floating_licenses': False,
                ...
            }
        """
        pass

    @property
    @abstractmethod
    def credential_schema(self) -> Dict:
        """
        Return schema defining required credentials for this provider.

        Returns:
            Dict defining credential fields:
            {
                'field_name': {
                    'type': 'string|select|json|url',
                    'title': 'Field Label',
                    'required': True|False,
                    'secret': True|False,  # Mask in UI
                    'help_text': 'Help text',
                    'choices': [(value, label), ...],  # For select type
                    'default': 'default value',
                }
            }
        """
        pass

    @abstractmethod
    def create_license(self, license_key, product, order) -> Tuple[bool, str, Dict]:
        """
        Create a license in the external provider system.

        Args:
            license_key: LicenseKey model instance
            product: Product model instance
            order: Order model instance

        Returns:
            Tuple of (success: bool, external_id: str, response_data: dict)
        """
        pass

    @abstractmethod
    def validate_license(self, key: str) -> Tuple[bool, Dict]:
        """
        Validate a license key with the external provider.

        Args:
            key: License key string to validate

        Returns:
            Tuple of (is_valid: bool, validation_data: dict)
        """
        pass

    @abstractmethod
    def activate_device(self, license_key, device_fingerprint: str, device_info: Dict) -> Tuple[bool, str, Dict]:
        """
        Register a device activation with the external provider.

        Args:
            license_key: LicenseKey model instance
            device_fingerprint: Unique device identifier
            device_info: Dictionary of device information

        Returns:
            Tuple of (success: bool, activation_id: str, response_data: dict)
        """
        pass

    @abstractmethod
    def deactivate_device(self, license_key, device_fingerprint: str) -> Tuple[bool, Dict]:
        """
        Deactivate a device with the external provider.

        Args:
            license_key: LicenseKey model instance
            device_fingerprint: Unique device identifier

        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        pass

    @abstractmethod
    def suspend_license(self, license_key) -> Tuple[bool, Dict]:
        """
        Suspend a license in the external provider.

        Args:
            license_key: LicenseKey model instance

        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        pass

    @abstractmethod
    def revoke_license(self, license_key) -> Tuple[bool, Dict]:
        """
        Revoke a license in the external provider.

        Args:
            license_key: LicenseKey model instance

        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        pass

    @abstractmethod
    def get_license_info(self, external_id: str) -> Tuple[bool, Dict]:
        """
        Retrieve license information from external provider.

        Args:
            external_id: External license ID

        Returns:
            Tuple of (success: bool, license_data: dict)
        """
        pass

    @abstractmethod
    def _get_auth_headers(self) -> Dict:
        """
        Get authentication headers for API requests.

        This must be implemented by subclasses to provide provider-specific
        authentication (Bearer token, API key, Basic auth, etc.)

        Returns:
            Dict of HTTP headers for authentication
        """
        pass

    def handle_webhook(self, event_type: str, payload: Dict) -> Tuple[bool, Optional[str]]:
        """
        Process webhook event from external provider.

        This method can be overridden by subclasses for provider-specific webhook handling.

        Args:
            event_type: Type of webhook event
            payload: Webhook payload data

        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        logger.info(f"Received webhook event: {event_type} from {self.provider.name}")
        # Default implementation - subclasses should override
        return True, None

    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """
        Verify webhook signature.

        Default implementation uses HMAC-SHA256. Subclasses can override
        for provider-specific signature verification.

        Args:
            payload: Raw webhook payload bytes
            signature: Signature from webhook headers

        Returns:
            bool: True if signature is valid
        """
        import hmac
        import hashlib

        if not self.provider.webhook_secret:
            logger.warning(f"No webhook secret configured for {self.provider.name}")
            return False

        expected = hmac.new(
            self.provider.webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected, signature)

    def test_connection(self) -> Dict:
        """
        Test connection to provider API.

        Default implementation tries to make a basic API call.
        Subclasses can override for provider-specific health checks.

        Returns:
            Dict with 'success' (bool) and 'error' (str) or 'message' (str)
        """
        try:
            # Validate credentials first
            is_valid, error_msg = self.validate_credentials()
            if not is_valid:
                return {'success': False, 'error': error_msg}

            # Try a basic API call with auth headers
            headers = self._get_auth_headers()

            # Most providers have a health or account endpoint
            # This is a generic attempt - subclasses should override with specific endpoint
            success, response = self._make_request('GET', '/', headers=headers)

            if success:
                return {'success': True, 'message': 'Connection successful'}
            else:
                error = response.get('error', 'Unknown error')
                return {'success': False, 'error': f'Connection failed: {error}'}

        except Exception as e:
            logger.exception(f"Connection test failed for {self.provider.name}")
            return {'success': False, 'error': str(e)}

    def validate_credentials(self) -> Tuple[bool, Optional[str]]:
        """
        Validate credential format and values.

        Returns:
            Tuple of (is_valid: bool, error_message: Optional[str])
        """
        schema = self.credential_schema

        for field_name, field_config in schema.items():
            if field_config.get('required', False):
                value = self.config.get(field_name)

                # For standard fields, check the provider attributes too
                if field_name == 'api_key' and not value:
                    value = self.api_key
                if field_name == 'api_secret' and not value:
                    value = self.api_secret
                if field_name == 'api_endpoint' and not value:
                    value = self.api_endpoint

                if not value:
                    title = field_config.get('title', field_name)
                    return False, f"Missing required field: {title}"

        return True, None

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None,
                     headers: Optional[Dict] = None) -> Tuple[bool, Dict]:
        """
        Helper method for making HTTP requests to provider API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            data: Request payload (for POST/PUT)
            headers: Additional HTTP headers

        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        import requests

        url = f"{self.api_endpoint.rstrip('/')}/{endpoint.lstrip('/')}"

        # Build headers with authentication
        request_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        if headers:
            request_headers.update(headers)

        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                headers=request_headers,
                timeout=30
            )

            response.raise_for_status()

            return True, response.json() if response.content else {}

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return False, {'error': str(e)}
