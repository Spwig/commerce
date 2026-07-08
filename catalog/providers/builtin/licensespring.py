"""
License Spring Provider Adapter

Integrates with License Spring license management platform.
API Documentation: https://docs.licensespring.com/

License Spring provides:
- License key generation and validation
- Device/machine activation tracking
- Floating licenses
- Consumption tracking (usage-based licensing)
- Trial licenses
- Offline validation
"""

import logging
from typing import Dict, Tuple
from catalog.providers.base import BaseLicenseProviderAdapter

logger = logging.getLogger(__name__)


class LicenseSpringAdapter(BaseLicenseProviderAdapter):
    """
    Adapter for License Spring license management platform.

    License Spring uses a product-based licensing system with support
    for various licensing models including perpetual, subscription,
    consumption-based, and floating licenses.
    """

    provider_key = 'licensespring'
    provider_name = 'License Spring'

    @property
    def capabilities(self) -> Dict:
        """Return capability set for License Spring"""
        return {
            'create_license': True,
            'validate_license': True,
            'activate_device': True,
            'deactivate_device': True,
            'suspend_license': True,
            'revoke_license': True,
            'webhooks': True,
            'floating_licenses': True,
            'consumption_tracking': True,
            'trial_licenses': True,
            'offline_validation': True,
            'analytics': True,
        }

    @property
    def credential_schema(self) -> Dict:
        """Define required credentials for License Spring"""
        return {
            'api_key': {
                'type': 'string',
                'title': 'Management API Key',
                'required': True,
                'secret': True,
                'help_text': 'API key from License Spring management dashboard',
            },
            'shared_key': {
                'type': 'string',
                'title': 'Shared Key',
                'required': True,
                'secret': True,
                'help_text': 'Shared key for SDK license validation',
            },
            'product_code': {
                'type': 'string',
                'title': 'Default Product Code',
                'required': True,
                'help_text': 'Default product code in License Spring',
            },
            'environment': {
                'type': 'select',
                'title': 'Environment',
                'choices': [
                    ('production', 'Production'),
                    ('sandbox', 'Sandbox'),
                ],
                'default': 'production',
                'help_text': 'Use sandbox for testing',
            }
        }

    def _get_base_url(self) -> str:
        """Get base URL based on environment"""
        environment = self.config.get('environment', 'production')
        if environment == 'sandbox':
            return 'https://saas-api-sandbox.licensespring.com'
        return 'https://saas-api.licensespring.com'

    def _get_auth_headers(self) -> Dict:
        """Get authentication headers for License Spring API"""
        return {
            'Authorization': f'ApiKey {self.api_key}',
            'Content-Type': 'application/json',
        }

    def _get_product_code(self, product) -> str:
        """
        Get License Spring product code for a Spwig product.

        Merchants can map products in provider_config.
        """
        product_mapping = self.config.get('product_mapping', {})
        product_code = product_mapping.get(str(product.id))

        if not product_code:
            # Use default product code
            product_code = self.config.get('product_code')

        return product_code

    def create_license(self, license_key, product, order) -> Tuple[bool, str, Dict]:
        """
        Create license in License Spring.

        Args:
            license_key: LicenseKey model instance
            product: Product model instance
            order: Order model instance

        Returns:
            Tuple of (success: bool, external_id: str, response_data: dict)
        """
        product_code = self._get_product_code(product)

        if not product_code:
            error_msg = f"No License Spring product mapping found for product {product.id}"
            logger.error(error_msg)
            return False, '', {'error': error_msg}

        endpoint = '/api/v4/licenses'

        data = {
            'product_code': product_code,
            'license_key': license_key.key,
            'max_activations': license_key.max_activations,
            'validity_period': None if license_key.is_lifetime else (
                (license_key.expires_at - license_key.issued_at).days if license_key.expires_at else None
            ),
            'customer': {
                'email': order.user.email,
                'first_name': order.user.first_name,
                'last_name': order.user.last_name,
                'company_name': '',
            },
            'license_type': 'perpetual' if license_key.is_lifetime else 'time_limited',
            'custom_fields': {
                'order_id': str(order.id),
                'order_number': order.order_number,
                'product_sku': product.sku,
                'source': 'spwig',
            }
        }

        # Override base URL for License Spring
        original_endpoint = self.api_endpoint
        self.api_endpoint = self._get_base_url()

        success, response = self._make_request('POST', endpoint, data, headers=self._get_auth_headers())

        # Restore original endpoint
        self.api_endpoint = original_endpoint

        if success:
            external_id = response.get('id', license_key.key)
            logger.info(f"Successfully created license {license_key.key} in License Spring (ID: {external_id})")
            return True, str(external_id), response

        error = response.get('message', 'Unknown error')
        logger.error(f"Failed to create license in License Spring: {error}")
        return False, '', response

    def validate_license(self, key: str) -> Tuple[bool, Dict]:
        """
        Validate license with License Spring.

        Args:
            key: License key string

        Returns:
            Tuple of (is_valid: bool, validation_data: dict)
        """
        endpoint = f'/api/v4/licenses/{key}/check'

        # Override base URL for License Spring
        original_endpoint = self.api_endpoint
        self.api_endpoint = self._get_base_url()

        success, response = self._make_request('GET', endpoint, headers=self._get_auth_headers())

        # Restore original endpoint
        self.api_endpoint = original_endpoint

        if success and response.get('is_valid'):
            logger.info(f"License {key} validated successfully in License Spring")
            return True, response

        logger.warning(f"License {key} validation failed in License Spring")
        return False, response

    def activate_device(self, license_key, device_fingerprint: str, device_info: Dict) -> Tuple[bool, str, Dict]:
        """
        Activate a device in License Spring.

        Args:
            license_key: LicenseKey model instance
            device_fingerprint: Unique device identifier
            device_info: Dictionary of device information

        Returns:
            Tuple of (success: bool, activation_id: str, response_data: dict)
        """
        endpoint = f'/api/v4/licenses/{license_key.key}/activate'

        data = {
            'hardware_id': device_fingerprint,
            'device_name': device_info.get('device_name', ''),
            'os': device_info.get('platform', ''),
            'os_version': device_info.get('os_version', ''),
        }

        # Override base URL for License Spring
        original_endpoint = self.api_endpoint
        self.api_endpoint = self._get_base_url()

        success, response = self._make_request('POST', endpoint, data, headers=self._get_auth_headers())

        # Restore original endpoint
        self.api_endpoint = original_endpoint

        if success:
            activation_id = response.get('activation_id', device_fingerprint)
            logger.info(f"Successfully activated device {device_fingerprint} in License Spring")
            return True, str(activation_id), response

        error = response.get('message', 'Unknown error')
        logger.error(f"Failed to activate device in License Spring: {error}")
        return False, '', response

    def deactivate_device(self, license_key, device_fingerprint: str) -> Tuple[bool, Dict]:
        """
        Deactivate a device in License Spring.

        Args:
            license_key: LicenseKey model instance
            device_fingerprint: Unique device identifier

        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        endpoint = f'/api/v4/licenses/{license_key.key}/deactivate'

        data = {
            'hardware_id': device_fingerprint,
        }

        # Override base URL for License Spring
        original_endpoint = self.api_endpoint
        self.api_endpoint = self._get_base_url()

        success, response = self._make_request('POST', endpoint, data, headers=self._get_auth_headers())

        # Restore original endpoint
        self.api_endpoint = original_endpoint

        if success:
            logger.info(f"Successfully deactivated device {device_fingerprint} in License Spring")
            return True, response

        error = response.get('message', 'Unknown error')
        logger.error(f"Failed to deactivate device in License Spring: {error}")
        return False, response

    def suspend_license(self, license_key) -> Tuple[bool, Dict]:
        """
        Suspend a license in License Spring.

        Args:
            license_key: LicenseKey model instance

        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        endpoint = f'/api/v4/licenses/{license_key.key}'

        data = {
            'is_enabled': False
        }

        # Override base URL for License Spring
        original_endpoint = self.api_endpoint
        self.api_endpoint = self._get_base_url()

        success, response = self._make_request('PATCH', endpoint, data, headers=self._get_auth_headers())

        # Restore original endpoint
        self.api_endpoint = original_endpoint

        if success:
            logger.info(f"Successfully suspended license {license_key.key} in License Spring")
            return True, response

        error = response.get('message', 'Unknown error')
        logger.error(f"Failed to suspend license in License Spring: {error}")
        return False, response

    def revoke_license(self, license_key) -> Tuple[bool, Dict]:
        """
        Revoke a license in License Spring.

        In License Spring, this deletes the license.

        Args:
            license_key: LicenseKey model instance

        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        endpoint = f'/api/v4/licenses/{license_key.key}'

        # Override base URL for License Spring
        original_endpoint = self.api_endpoint
        self.api_endpoint = self._get_base_url()

        success, response = self._make_request('DELETE', endpoint, headers=self._get_auth_headers())

        # Restore original endpoint
        self.api_endpoint = original_endpoint

        if success:
            logger.info(f"Successfully revoked license {license_key.key} in License Spring")
            return True, response

        error = response.get('message', 'Unknown error')
        logger.error(f"Failed to revoke license in License Spring: {error}")
        return False, response

    def get_license_info(self, external_id: str) -> Tuple[bool, Dict]:
        """
        Retrieve license information from License Spring.

        Args:
            external_id: License Spring license ID or key

        Returns:
            Tuple of (success: bool, license_data: dict)
        """
        endpoint = f'/api/v4/licenses/{external_id}'

        # Override base URL for License Spring
        original_endpoint = self.api_endpoint
        self.api_endpoint = self._get_base_url()

        success, response = self._make_request('GET', endpoint, headers=self._get_auth_headers())

        # Restore original endpoint
        self.api_endpoint = original_endpoint

        if success:
            logger.info(f"Successfully retrieved license info for {external_id} from License Spring")
            return True, response

        error = response.get('message', 'Unknown error')
        logger.error(f"Failed to retrieve license info from License Spring: {error}")
        return False, response

    def test_connection(self) -> Dict:
        """
        Test connection to License Spring API.

        Returns:
            Dict with 'success' (bool) and 'error' (str) or 'message' (str)
        """
        try:
            # Validate credentials first
            is_valid, error_msg = self.validate_credentials()
            if not is_valid:
                return {'success': False, 'error': error_msg}

            # Try to get product info
            product_code = self.config.get('product_code')
            if not product_code:
                return {'success': False, 'error': 'Missing product_code in configuration'}

            endpoint = f'/api/v4/products/{product_code}'

            # Override base URL for License Spring
            original_endpoint = self.api_endpoint
            self.api_endpoint = self._get_base_url()

            success, response = self._make_request('GET', endpoint, headers=self._get_auth_headers())

            # Restore original endpoint
            self.api_endpoint = original_endpoint

            if success:
                product_name = response.get('product_name', 'Unknown')
                return {
                    'success': True,
                    'message': f'Connected to License Spring (Product: {product_name})'
                }
            else:
                error = response.get('message', 'Unknown error')
                return {'success': False, 'error': f'Connection failed: {error}'}

        except Exception as e:
            logger.exception(f"Connection test failed for License Spring")
            return {'success': False, 'error': str(e)}
