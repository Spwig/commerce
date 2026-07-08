"""
Cryptlex License Provider Adapter

Integrates with Cryptlex license management platform.
API Documentation: https://docs.cryptlex.com/

Cryptlex provides:
- License key generation and validation
- Device/machine activation tracking
- Floating licenses
- Node-locked licenses
- Trial licenses
- Offline validation
- License meter attributes for usage tracking
"""

import logging
from typing import Dict, Tuple
from catalog.providers.base import BaseLicenseProviderAdapter

logger = logging.getLogger(__name__)


class CryptlexAdapter(BaseLicenseProviderAdapter):
    """
    Adapter for Cryptlex license management platform.

    Cryptlex uses a product-based licensing system with powerful
    policy engine supporting various licensing models.
    """

    provider_key = 'cryptlex'
    provider_name = 'Cryptlex'

    @property
    def capabilities(self) -> Dict:
        """Return capability set for Cryptlex"""
        return {
            'create_license': True,
            'validate_license': True,
            'activate_device': True,
            'deactivate_device': True,
            'suspend_license': True,
            'revoke_license': True,
            'webhooks': True,
            'floating_licenses': True,
            'node_locked_licenses': True,
            'trial_licenses': True,
            'offline_validation': True,
            'usage_tracking': True,
            'analytics': True,
        }

    @property
    def credential_schema(self) -> Dict:
        """Define required credentials for Cryptlex"""
        return {
            'access_token': {
                'type': 'string',
                'title': 'Access Token',
                'required': True,
                'secret': True,
                'help_text': 'Personal access token from Cryptlex dashboard',
            },
            'product_id': {
                'type': 'string',
                'title': 'Default Product ID',
                'required': True,
                'help_text': 'Default product ID in Cryptlex',
            },
            'account_id': {
                'type': 'string',
                'title': 'Account ID',
                'required': True,
                'help_text': 'Your Cryptlex account ID',
            },
        }

    def _get_base_url(self) -> str:
        """Get base URL for Cryptlex API"""
        return 'https://api.cryptlex.com/v3'

    def _get_auth_headers(self) -> Dict:
        """Get authentication headers for Cryptlex API"""
        access_token = self.config.get('access_token', self.api_key)
        return {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }

    def _get_product_id(self, product) -> str:
        """
        Get Cryptlex product ID for a Spwig product.

        Merchants can map products in provider_config.
        """
        product_mapping = self.config.get('product_mapping', {})
        product_id = product_mapping.get(str(product.id))

        if not product_id:
            # Use default product ID
            product_id = self.config.get('product_id')

        return product_id

    def create_license(self, license_key, product, order) -> Tuple[bool, str, Dict]:
        """
        Create license in Cryptlex.

        Args:
            license_key: LicenseKey model instance
            product: Product model instance
            order: Order model instance

        Returns:
            Tuple of (success: bool, external_id: str, response_data: dict)
        """
        product_id = self._get_product_id(product)

        if not product_id:
            error_msg = f"No Cryptlex product mapping found for product {product.id}"
            logger.error(error_msg)
            return False, '', {'error': error_msg}

        endpoint = '/licenses'

        data = {
            'key': license_key.key,
            'productId': product_id,
            'allowedActivations': license_key.max_activations,
            'expiresAt': license_key.expires_at.isoformat() if license_key.expires_at else None,
            'type': 'perpetual' if license_key.is_lifetime else 'trial',
            'metadata': [
                {'key': 'order_id', 'value': str(order.id)},
                {'key': 'order_number', 'value': order.order_number},
                {'key': 'customer_email', 'value': order.user.email},
                {'key': 'product_sku', 'value': product.sku},
                {'key': 'source', 'value': 'spwig'},
            ]
        }

        # Override base URL for Cryptlex
        original_endpoint = self.api_endpoint
        self.api_endpoint = self._get_base_url()

        success, response = self._make_request('POST', endpoint, data, headers=self._get_auth_headers())

        # Restore original endpoint
        self.api_endpoint = original_endpoint

        if success:
            external_id = response.get('id', '')
            logger.info(f"Successfully created license {license_key.key} in Cryptlex (ID: {external_id})")
            return True, external_id, response

        error = response.get('message', 'Unknown error')
        logger.error(f"Failed to create license in Cryptlex: {error}")
        return False, '', response

    def validate_license(self, key: str) -> Tuple[bool, Dict]:
        """
        Validate license with Cryptlex.

        Note: Cryptlex validation is typically done via SDK on client side.
        This is a simple key lookup for server-side validation.

        Args:
            key: License key string

        Returns:
            Tuple of (is_valid: bool, validation_data: dict)
        """
        # Cryptlex uses key as identifier
        endpoint = f'/licenses/{key}'

        # Override base URL for Cryptlex
        original_endpoint = self.api_endpoint
        self.api_endpoint = self._get_base_url()

        success, response = self._make_request('GET', endpoint, headers=self._get_auth_headers())

        # Restore original endpoint
        self.api_endpoint = original_endpoint

        if success:
            # Check if license is valid (not revoked, not expired)
            is_valid = (
                not response.get('revoked', False) and
                response.get('suspended', False) is False
            )

            if is_valid:
                logger.info(f"License {key} validated successfully in Cryptlex")
                return True, response
            else:
                logger.warning(f"License {key} is invalid in Cryptlex")
                return False, response

        logger.error(f"Failed to validate license in Cryptlex")
        return False, response

    def activate_device(self, license_key, device_fingerprint: str, device_info: Dict) -> Tuple[bool, str, Dict]:
        """
        Activate a device in Cryptlex.

        Args:
            license_key: LicenseKey model instance
            device_fingerprint: Unique device identifier
            device_info: Dictionary of device information

        Returns:
            Tuple of (success: bool, activation_id: str, response_data: dict)
        """
        # First, get the Cryptlex license ID
        from catalog.models import ExternalLicenseSync

        try:
            sync = ExternalLicenseSync.objects.get(
                license_key=license_key,
                provider=self.provider,
                sync_status='success'
            )
            cryptlex_license_id = sync.external_id
        except ExternalLicenseSync.DoesNotExist:
            logger.error(f"No Cryptlex sync found for license {license_key.key}")
            return False, '', {'error': 'License not synced to Cryptlex'}

        endpoint = '/activations'

        data = {
            'licenseId': cryptlex_license_id,
            'fingerprint': device_fingerprint,
            'metadata': [
                {'key': 'device_name', 'value': device_info.get('device_name', '')},
                {'key': 'platform', 'value': device_info.get('platform', '')},
            ]
        }

        # Override base URL for Cryptlex
        original_endpoint = self.api_endpoint
        self.api_endpoint = self._get_base_url()

        success, response = self._make_request('POST', endpoint, data, headers=self._get_auth_headers())

        # Restore original endpoint
        self.api_endpoint = original_endpoint

        if success:
            activation_id = response.get('id', '')
            logger.info(f"Successfully activated device {device_fingerprint} in Cryptlex (ID: {activation_id})")
            return True, activation_id, response

        error = response.get('message', 'Unknown error')
        logger.error(f"Failed to activate device in Cryptlex: {error}")
        return False, '', response

    def deactivate_device(self, license_key, device_fingerprint: str) -> Tuple[bool, Dict]:
        """
        Deactivate a device in Cryptlex.

        In Cryptlex, this deletes the activation.

        Args:
            license_key: LicenseKey model instance
            device_fingerprint: Unique device identifier

        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        # We need to find the activation ID by fingerprint
        # For now, we'll assume the fingerprint can be used as ID
        # In a real implementation, we'd store the activation ID during activation
        endpoint = f'/activations/{device_fingerprint}'

        # Override base URL for Cryptlex
        original_endpoint = self.api_endpoint
        self.api_endpoint = self._get_base_url()

        success, response = self._make_request('DELETE', endpoint, headers=self._get_auth_headers())

        # Restore original endpoint
        self.api_endpoint = original_endpoint

        if success:
            logger.info(f"Successfully deactivated device {device_fingerprint} in Cryptlex")
            return True, response

        error = response.get('message', 'Unknown error')
        logger.error(f"Failed to deactivate device in Cryptlex: {error}")
        return False, response

    def suspend_license(self, license_key) -> Tuple[bool, Dict]:
        """
        Suspend a license in Cryptlex.

        Args:
            license_key: LicenseKey model instance

        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        from catalog.models import ExternalLicenseSync

        try:
            sync = ExternalLicenseSync.objects.get(
                license_key=license_key,
                provider=self.provider,
                sync_status='success'
            )
            cryptlex_license_id = sync.external_id
        except ExternalLicenseSync.DoesNotExist:
            return False, {'error': 'License not synced to Cryptlex'}

        endpoint = f'/licenses/{cryptlex_license_id}'

        data = {
            'suspended': True
        }

        # Override base URL for Cryptlex
        original_endpoint = self.api_endpoint
        self.api_endpoint = self._get_base_url()

        success, response = self._make_request('PATCH', endpoint, data, headers=self._get_auth_headers())

        # Restore original endpoint
        self.api_endpoint = original_endpoint

        if success:
            logger.info(f"Successfully suspended license {license_key.key} in Cryptlex")
            return True, response

        error = response.get('message', 'Unknown error')
        logger.error(f"Failed to suspend license in Cryptlex: {error}")
        return False, response

    def revoke_license(self, license_key) -> Tuple[bool, Dict]:
        """
        Revoke a license in Cryptlex.

        Args:
            license_key: LicenseKey model instance

        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        from catalog.models import ExternalLicenseSync

        try:
            sync = ExternalLicenseSync.objects.get(
                license_key=license_key,
                provider=self.provider,
                sync_status='success'
            )
            cryptlex_license_id = sync.external_id
        except ExternalLicenseSync.DoesNotExist:
            return False, {'error': 'License not synced to Cryptlex'}

        endpoint = f'/licenses/{cryptlex_license_id}'

        data = {
            'revoked': True
        }

        # Override base URL for Cryptlex
        original_endpoint = self.api_endpoint
        self.api_endpoint = self._get_base_url()

        success, response = self._make_request('PATCH', endpoint, data, headers=self._get_auth_headers())

        # Restore original endpoint
        self.api_endpoint = original_endpoint

        if success:
            logger.info(f"Successfully revoked license {license_key.key} in Cryptlex")
            return True, response

        error = response.get('message', 'Unknown error')
        logger.error(f"Failed to revoke license in Cryptlex: {error}")
        return False, response

    def get_license_info(self, external_id: str) -> Tuple[bool, Dict]:
        """
        Retrieve license information from Cryptlex.

        Args:
            external_id: Cryptlex license ID

        Returns:
            Tuple of (success: bool, license_data: dict)
        """
        endpoint = f'/licenses/{external_id}'

        # Override base URL for Cryptlex
        original_endpoint = self.api_endpoint
        self.api_endpoint = self._get_base_url()

        success, response = self._make_request('GET', endpoint, headers=self._get_auth_headers())

        # Restore original endpoint
        self.api_endpoint = original_endpoint

        if success:
            logger.info(f"Successfully retrieved license info for {external_id} from Cryptlex")
            return True, response

        error = response.get('message', 'Unknown error')
        logger.error(f"Failed to retrieve license info from Cryptlex: {error}")
        return False, response

    def test_connection(self) -> Dict:
        """
        Test connection to Cryptlex API.

        Returns:
            Dict with 'success' (bool) and 'error' (str) or 'message' (str)
        """
        try:
            # Validate credentials first
            is_valid, error_msg = self.validate_credentials()
            if not is_valid:
                return {'success': False, 'error': error_msg}

            # Try to get account info
            account_id = self.config.get('account_id')
            if not account_id:
                return {'success': False, 'error': 'Missing account_id in configuration'}

            endpoint = f'/accounts/{account_id}'

            # Override base URL for Cryptlex
            original_endpoint = self.api_endpoint
            self.api_endpoint = self._get_base_url()

            success, response = self._make_request('GET', endpoint, headers=self._get_auth_headers())

            # Restore original endpoint
            self.api_endpoint = original_endpoint

            if success:
                account_name = response.get('name', 'Unknown')
                return {
                    'success': True,
                    'message': f'Connected to Cryptlex (Account: {account_name})'
                }
            else:
                error = response.get('message', 'Unknown error')
                return {'success': False, 'error': f'Connection failed: {error}'}

        except Exception as e:
            logger.exception(f"Connection test failed for Cryptlex")
            return {'success': False, 'error': str(e)}
