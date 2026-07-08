"""
Custom API License Provider Adapter

Generic adapter for merchants with their own license servers.

This adapter provides a flexible way to integrate with custom REST APIs
that follow standard HTTP patterns. Merchants can configure:
- API base URL
- Authentication method (Bearer, API Key, Basic Auth, Custom Headers)
- Endpoint mappings
- Custom request/response handling

This is ideal for merchants who:
- Already have a license server
- Want full control over their licensing infrastructure
- Need to integrate with proprietary systems
"""

import base64
import logging
from typing import Dict, Tuple, Optional
from catalog.providers.base import BaseLicenseProviderAdapter

logger = logging.getLogger(__name__)


class CustomAPIAdapter(BaseLicenseProviderAdapter):
    """
    Generic adapter for custom license server APIs.

    Supports configurable authentication and endpoint mapping.
    """

    provider_key = 'custom'
    provider_name = 'Custom API'

    @property
    def capabilities(self) -> Dict:
        """
        Return capabilities for custom API.

        Note: Actual capabilities depend on the custom server implementation.
        We assume all features are available - merchants can disable sync
        options for unsupported features.
        """
        return {
            'create_license': True,
            'validate_license': True,
            'activate_device': True,
            'deactivate_device': True,
            'suspend_license': True,
            'revoke_license': True,
            'webhooks': True,
            'offline_validation': False,  # Depends on implementation
            'analytics': False,  # Depends on implementation
        }

    @property
    def credential_schema(self) -> Dict:
        """Define configuration schema for custom API"""
        return {
            'api_endpoint': {
                'type': 'url',
                'title': 'API Base URL',
                'required': True,
                'help_text': 'Base URL of your license API (e.g., https://licenses.example.com/api)',
            },
            'auth_type': {
                'type': 'select',
                'title': 'Authentication Type',
                'choices': [
                    ('bearer', 'Bearer Token'),
                    ('api_key', 'API Key Header'),
                    ('basic', 'Basic Auth'),
                    ('custom', 'Custom Headers'),
                ],
                'default': 'bearer',
                'required': True,
                'help_text': 'How to authenticate with your API',
            },
            'auth_token': {
                'type': 'string',
                'title': 'Authentication Token/Key',
                'required': True,
                'secret': True,
                'help_text': 'API token, key, or username (for Basic Auth)',
            },
            'auth_secret': {
                'type': 'string',
                'title': 'Auth Secret (Optional)',
                'required': False,
                'secret': True,
                'help_text': 'Password for Basic Auth or secondary key',
            },
            'custom_headers': {
                'type': 'json',
                'title': 'Custom Headers (Optional)',
                'required': False,
                'help_text': 'Additional headers to send with each request (JSON object)',
                'default': {},
            },
            'endpoint_mapping': {
                'type': 'json',
                'title': 'Endpoint Mapping',
                'required': False,
                'help_text': 'Map operations to your API endpoints (use {key}, {id} placeholders)',
                'default': {
                    'create': '/licenses',
                    'validate': '/licenses/{key}/validate',
                    'activate': '/licenses/{key}/activate',
                    'deactivate': '/licenses/{key}/deactivate',
                    'suspend': '/licenses/{key}/suspend',
                    'revoke': '/licenses/{key}/revoke',
                    'get_info': '/licenses/{id}',
                }
            },
            'response_format': {
                'type': 'select',
                'title': 'Response Format',
                'choices': [
                    ('json', 'JSON'),
                    ('xml', 'XML'),
                ],
                'default': 'json',
                'help_text': 'Expected response format from your API',
            },
        }

    def _get_auth_headers(self) -> Dict:
        """
        Build authentication headers based on configured auth_type.

        Returns:
            Dict of HTTP headers for authentication
        """
        auth_type = self.config.get('auth_type', 'bearer')
        auth_token = self.config.get('auth_token', self.api_key)
        auth_secret = self.config.get('auth_secret', self.api_secret)

        headers = {}

        if auth_type == 'bearer':
            headers['Authorization'] = f'Bearer {auth_token}'

        elif auth_type == 'api_key':
            headers['X-API-Key'] = auth_token

        elif auth_type == 'basic':
            if auth_secret:
                credentials = base64.b64encode(f"{auth_token}:{auth_secret}".encode()).decode()
            else:
                credentials = base64.b64encode(f"{auth_token}:".encode()).decode()
            headers['Authorization'] = f'Basic {credentials}'

        elif auth_type == 'custom':
            # Use custom headers from config
            custom_headers = self.config.get('custom_headers', {})
            headers.update(custom_headers)

        return headers

    def _get_endpoint(self, operation: str, **kwargs) -> str:
        """
        Get endpoint for an operation with placeholder substitution.

        Args:
            operation: Operation name (create, validate, activate, etc.)
            **kwargs: Values to substitute in placeholders (key, id, etc.)

        Returns:
            str: Endpoint path with placeholders replaced
        """
        endpoint_mapping = self.config.get('endpoint_mapping', {})
        endpoint = endpoint_mapping.get(operation, '')

        if not endpoint:
            # Use default endpoints
            defaults = {
                'create': '/licenses',
                'validate': '/licenses/{key}/validate',
                'activate': '/licenses/{key}/activate',
                'deactivate': '/licenses/{key}/deactivate',
                'suspend': '/licenses/{key}/suspend',
                'revoke': '/licenses/{key}/revoke',
                'get_info': '/licenses/{id}',
            }
            endpoint = defaults.get(operation, '/')

        # Substitute placeholders
        for key, value in kwargs.items():
            placeholder = f'{{{key}}}'
            if placeholder in endpoint:
                endpoint = endpoint.replace(placeholder, str(value))

        return endpoint

    def _build_license_payload(self, license_key, product, order) -> Dict:
        """
        Build standard license payload for custom API.

        This is the recommended format that custom APIs should accept.
        Merchants can customize this in their server implementation.

        Args:
            license_key: LicenseKey model instance
            product: Product model instance
            order: Order model instance

        Returns:
            Dict: Standard license payload
        """
        return {
            'license_key': license_key.key,
            'product': {
                'id': str(product.id),
                'name': product.name,
                'sku': product.sku,
            },
            'key_type': license_key.key_type,
            'max_activations': license_key.max_activations,
            'is_lifetime': license_key.is_lifetime,
            'expires_at': license_key.expires_at.isoformat() if license_key.expires_at else None,
            'order': {
                'id': str(order.id),
                'number': order.order_number,
                'customer_email': order.user.email,
                'customer_name': f"{order.user.first_name} {order.user.last_name}".strip(),
            },
            'metadata': {
                'source': 'spwig',
            }
        }

    def create_license(self, license_key, product, order) -> Tuple[bool, str, Dict]:
        """
        Create license in custom API.

        Args:
            license_key: LicenseKey model instance
            product: Product model instance
            order: Order model instance

        Returns:
            Tuple of (success: bool, external_id: str, response_data: dict)
        """
        endpoint = self._get_endpoint('create')
        data = self._build_license_payload(license_key, product, order)

        success, response = self._make_request('POST', endpoint, data, headers=self._get_auth_headers())

        if success:
            # Try to extract external ID from response
            # Common patterns: 'id', 'license_id', 'external_id'
            external_id = response.get('id') or response.get('license_id') or response.get('external_id') or license_key.key
            logger.info(f"Successfully created license {license_key.key} in custom API (ID: {external_id})")
            return True, str(external_id), response

        error = response.get('error', 'Unknown error')
        logger.error(f"Failed to create license in custom API: {error}")
        return False, '', response

    def validate_license(self, key: str) -> Tuple[bool, Dict]:
        """
        Validate license with custom API.

        Args:
            key: License key string

        Returns:
            Tuple of (is_valid: bool, validation_data: dict)
        """
        endpoint = self._get_endpoint('validate', key=key)

        success, response = self._make_request('GET', endpoint, headers=self._get_auth_headers())

        if success:
            # Check for common validity indicators
            is_valid = response.get('valid', response.get('is_valid', False))
            if is_valid:
                logger.info(f"License {key} validated successfully in custom API")
                return True, response
            else:
                logger.warning(f"License {key} is invalid per custom API")
                return False, response

        logger.error(f"Failed to validate license in custom API")
        return False, response

    def activate_device(self, license_key, device_fingerprint: str, device_info: Dict) -> Tuple[bool, str, Dict]:
        """
        Activate a device with custom API.

        Args:
            license_key: LicenseKey model instance
            device_fingerprint: Unique device identifier
            device_info: Dictionary of device information

        Returns:
            Tuple of (success: bool, activation_id: str, response_data: dict)
        """
        endpoint = self._get_endpoint('activate', key=license_key.key)

        data = {
            'device_fingerprint': device_fingerprint,
            'device_name': device_info.get('device_name', ''),
            'device_info': device_info,
        }

        success, response = self._make_request('POST', endpoint, data, headers=self._get_auth_headers())

        if success:
            # Try to extract activation ID
            activation_id = response.get('activation_id') or response.get('id') or device_fingerprint
            logger.info(f"Successfully activated device {device_fingerprint} for license {license_key.key}")
            return True, str(activation_id), response

        error = response.get('error', 'Unknown error')
        logger.error(f"Failed to activate device in custom API: {error}")
        return False, '', response

    def deactivate_device(self, license_key, device_fingerprint: str) -> Tuple[bool, Dict]:
        """
        Deactivate a device with custom API.

        Args:
            license_key: LicenseKey model instance
            device_fingerprint: Unique device identifier

        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        endpoint = self._get_endpoint('deactivate', key=license_key.key)

        data = {
            'device_fingerprint': device_fingerprint,
        }

        success, response = self._make_request('POST', endpoint, data, headers=self._get_auth_headers())

        if success:
            logger.info(f"Successfully deactivated device {device_fingerprint} for license {license_key.key}")
            return True, response

        error = response.get('error', 'Unknown error')
        logger.error(f"Failed to deactivate device in custom API: {error}")
        return False, response

    def suspend_license(self, license_key) -> Tuple[bool, Dict]:
        """
        Suspend a license in custom API.

        Args:
            license_key: LicenseKey model instance

        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        endpoint = self._get_endpoint('suspend', key=license_key.key)

        success, response = self._make_request('PUT', endpoint, headers=self._get_auth_headers())

        if success:
            logger.info(f"Successfully suspended license {license_key.key}")
            return True, response

        error = response.get('error', 'Unknown error')
        logger.error(f"Failed to suspend license in custom API: {error}")
        return False, response

    def revoke_license(self, license_key) -> Tuple[bool, Dict]:
        """
        Revoke a license in custom API.

        Args:
            license_key: LicenseKey model instance

        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        endpoint = self._get_endpoint('revoke', key=license_key.key)

        success, response = self._make_request('PUT', endpoint, headers=self._get_auth_headers())

        if success:
            logger.info(f"Successfully revoked license {license_key.key}")
            return True, response

        error = response.get('error', 'Unknown error')
        logger.error(f"Failed to revoke license in custom API: {error}")
        return False, response

    def get_license_info(self, external_id: str) -> Tuple[bool, Dict]:
        """
        Retrieve license information from custom API.

        Args:
            external_id: External license ID

        Returns:
            Tuple of (success: bool, license_data: dict)
        """
        endpoint = self._get_endpoint('get_info', id=external_id)

        success, response = self._make_request('GET', endpoint, headers=self._get_auth_headers())

        if success:
            logger.info(f"Successfully retrieved license info for {external_id}")
            return True, response

        error = response.get('error', 'Unknown error')
        logger.error(f"Failed to retrieve license info from custom API: {error}")
        return False, response

    def test_connection(self) -> Dict:
        """
        Test connection to custom API.

        Tries to make a basic request to validate connectivity and authentication.

        Returns:
            Dict with 'success' (bool) and 'error' (str) or 'message' (str)
        """
        try:
            # Validate credentials first
            is_valid, error_msg = self.validate_credentials()
            if not is_valid:
                return {'success': False, 'error': error_msg}

            # Try to make a basic request
            # Most APIs have a health or status endpoint
            test_endpoint = self.config.get('test_endpoint', '/')

            success, response = self._make_request('GET', test_endpoint, headers=self._get_auth_headers())

            if success:
                return {
                    'success': True,
                    'message': f'Connected to custom API at {self.api_endpoint}'
                }
            else:
                error = response.get('error', 'Unknown error')
                return {'success': False, 'error': f'Connection failed: {error}'}

        except Exception as e:
            logger.exception(f"Connection test failed for custom API")
            return {'success': False, 'error': str(e)}
