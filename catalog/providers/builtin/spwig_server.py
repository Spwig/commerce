"""
Spwig Built-in License Server Adapter

This adapter integrates with Spwig's own hosted license management server.
This is the recommended provider for merchants who want a fully managed
license server without setting up external services.

API Endpoint: https://licenses.spwig.com/api/v1/
"""

import logging
from typing import Dict, Tuple
from catalog.providers.base import BaseLicenseProviderAdapter

logger = logging.getLogger(__name__)


class SpwigLicenseServerAdapter(BaseLicenseProviderAdapter):
    """
    Adapter for Spwig's own license server.

    Features:
    - Hosted by Spwig
    - No additional API keys needed (uses merchant's Spwig account)
    - Automatic sync
    - Built-in reporting and analytics
    - Full offline validation support
    - Device management
    """

    provider_key = 'spwig_server'
    provider_name = 'Spwig Built-in License Server'

    @property
    def capabilities(self) -> Dict:
        """Return full capability set for Spwig Built-in License Server"""
        return {
            'create_license': True,
            'validate_license': True,
            'activate_device': True,
            'deactivate_device': True,
            'suspend_license': True,
            'revoke_license': True,
            'webhooks': True,
            'offline_validation': True,
            'analytics': True,
            'device_management': True,
            'floating_licenses': True,
            'usage_tracking': True,
            'trial_licenses': True,
        }

    @property
    def credential_schema(self) -> Dict:
        """Define required credentials for Spwig Built-in License Server"""
        return {
            'account_id': {
                'type': 'string',
                'title': 'Spwig License Account ID',
                'required': True,
                'help_text': 'Your Spwig Built-in License Server account ID (found in dashboard)',
            },
            'api_key': {
                'type': 'string',
                'title': 'API Key',
                'required': True,
                'secret': True,
                'help_text': 'API key from Spwig Built-in License Server dashboard',
            }
        }

    def _get_auth_headers(self) -> Dict:
        """Get authentication headers for Spwig Built-in License Server"""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'X-Account-ID': self.config.get('account_id', ''),
        }

    def create_license(self, license_key, product, order) -> Tuple[bool, str, Dict]:
        """
        Create license in Spwig Built-in License Server.

        Args:
            license_key: LicenseKey model instance
            product: Product model instance
            order: Order model instance

        Returns:
            Tuple of (success: bool, external_id: str, response_data: dict)
        """
        endpoint = '/licenses/'

        data = {
            'key': license_key.key,
            'product': {
                'id': product.id,
                'name': product.name,
                'sku': product.sku,
            },
            'key_type': license_key.key_type,
            'max_activations': license_key.max_activations,
            'is_lifetime': license_key.is_lifetime,
            'expires_at': license_key.expires_at.isoformat() if license_key.expires_at else None,
            'order': {
                'id': order.id,
                'number': order.order_number,
                'customer_email': order.user.email,
                'customer_name': f"{order.user.first_name} {order.user.last_name}".strip(),
            },
            'metadata': {
                'source': 'spwig_shop',
                'shop_url': self.provider.provider_config.get('shop_url', ''),
            }
        }

        success, response = self._make_request('POST', endpoint, data, headers=self._get_auth_headers())

        if success:
            external_id = response.get('id', '')
            logger.info(f"Successfully created license {license_key.key} in Spwig Built-in License Server (ID: {external_id})")
            return True, external_id, response

        error = response.get('error', 'Unknown error')
        logger.error(f"Failed to create license in Spwig Built-in License Server: {error}")
        return False, '', response

    def validate_license(self, key: str) -> Tuple[bool, Dict]:
        """
        Validate license with Spwig Built-in License Server.

        Args:
            key: License key string

        Returns:
            Tuple of (is_valid: bool, validation_data: dict)
        """
        endpoint = f'/licenses/{key}/validate/'

        success, response = self._make_request('GET', endpoint, headers=self._get_auth_headers())

        if success and response.get('valid'):
            logger.info(f"License {key} validated successfully")
            return True, response

        logger.warning(f"License {key} validation failed: {response.get('message', 'Invalid')}")
        return False, response

    def activate_device(self, license_key, device_fingerprint: str, device_info: Dict) -> Tuple[bool, str, Dict]:
        """
        Activate a device with Spwig Built-in License Server.

        Args:
            license_key: LicenseKey model instance
            device_fingerprint: Unique device identifier
            device_info: Dictionary of device information

        Returns:
            Tuple of (success: bool, activation_id: str, response_data: dict)
        """
        endpoint = f'/licenses/{license_key.key}/activate/'

        data = {
            'device_fingerprint': device_fingerprint,
            'device_name': device_info.get('device_name', ''),
            'device_info': device_info,
        }

        success, response = self._make_request('POST', endpoint, data, headers=self._get_auth_headers())

        if success:
            activation_id = response.get('activation_id', '')
            logger.info(f"Successfully activated device {device_fingerprint} for license {license_key.key}")
            return True, activation_id, response

        error = response.get('error', 'Unknown error')
        logger.error(f"Failed to activate device: {error}")
        return False, '', response

    def deactivate_device(self, license_key, device_fingerprint: str) -> Tuple[bool, Dict]:
        """
        Deactivate a device with Spwig Built-in License Server.

        Args:
            license_key: LicenseKey model instance
            device_fingerprint: Unique device identifier

        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        endpoint = f'/licenses/{license_key.key}/deactivate/'

        data = {
            'device_fingerprint': device_fingerprint,
        }

        success, response = self._make_request('POST', endpoint, data, headers=self._get_auth_headers())

        if success:
            logger.info(f"Successfully deactivated device {device_fingerprint} for license {license_key.key}")
            return True, response

        error = response.get('error', 'Unknown error')
        logger.error(f"Failed to deactivate device: {error}")
        return False, response

    def suspend_license(self, license_key) -> Tuple[bool, Dict]:
        """
        Suspend a license in Spwig Built-in License Server.

        Args:
            license_key: LicenseKey model instance

        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        endpoint = f'/licenses/{license_key.key}/suspend/'

        success, response = self._make_request('PUT', endpoint, headers=self._get_auth_headers())

        if success:
            logger.info(f"Successfully suspended license {license_key.key}")
            return True, response

        error = response.get('error', 'Unknown error')
        logger.error(f"Failed to suspend license: {error}")
        return False, response

    def revoke_license(self, license_key) -> Tuple[bool, Dict]:
        """
        Revoke a license in Spwig Built-in License Server.

        Args:
            license_key: LicenseKey model instance

        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        endpoint = f'/licenses/{license_key.key}/revoke/'

        success, response = self._make_request('PUT', endpoint, headers=self._get_auth_headers())

        if success:
            logger.info(f"Successfully revoked license {license_key.key}")
            return True, response

        error = response.get('error', 'Unknown error')
        logger.error(f"Failed to revoke license: {error}")
        return False, response

    def get_license_info(self, external_id: str) -> Tuple[bool, Dict]:
        """
        Retrieve license information from Spwig Built-in License Server.

        Args:
            external_id: External license ID

        Returns:
            Tuple of (success: bool, license_data: dict)
        """
        endpoint = f'/licenses/{external_id}/'

        success, response = self._make_request('GET', endpoint, headers=self._get_auth_headers())

        if success:
            logger.info(f"Successfully retrieved license info for {external_id}")
            return True, response

        error = response.get('error', 'Unknown error')
        logger.error(f"Failed to retrieve license info: {error}")
        return False, response

    def handle_webhook(self, event_type: str, payload: Dict) -> Tuple[bool, str]:
        """
        Process webhook event from Spwig Built-in License Server.

        Supported events:
        - license.activated: Device activation
        - license.deactivated: Device deactivation
        - license.suspended: License suspended
        - license.revoked: License revoked
        - license.expired: License expired

        Args:
            event_type: Type of webhook event
            payload: Webhook payload data

        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        from catalog.models import LicenseKey, LicenseActivation

        logger.info(f"Processing Spwig Built-in License Server webhook: {event_type}")

        try:
            license_key_str = payload.get('license_key')
            if not license_key_str:
                return False, "Missing license_key in payload"

            # Find the license key
            try:
                license_key = LicenseKey.objects.get(key=license_key_str)
            except LicenseKey.DoesNotExist:
                logger.warning(f"License key {license_key_str} not found")
                return False, f"License key not found: {license_key_str}"

            # Handle different event types
            if event_type == 'license.activated':
                # Record device activation
                device_fingerprint = payload.get('device_fingerprint')
                if device_fingerprint:
                    LicenseActivation.objects.update_or_create(
                        license_key=license_key,
                        device_fingerprint=device_fingerprint,
                        defaults={
                            'device_name': payload.get('device_name', ''),
                            'device_info': payload.get('device_info', {}),
                            'is_active': True,
                        }
                    )
                    logger.info(f"Recorded activation for {license_key_str}")

            elif event_type == 'license.deactivated':
                # Mark device as deactivated
                device_fingerprint = payload.get('device_fingerprint')
                if device_fingerprint:
                    LicenseActivation.objects.filter(
                        license_key=license_key,
                        device_fingerprint=device_fingerprint
                    ).update(is_active=False)
                    logger.info(f"Recorded deactivation for {license_key_str}")

            elif event_type == 'license.suspended':
                # Update license status if needed
                logger.info(f"License {license_key_str} suspended via webhook")

            elif event_type == 'license.revoked':
                # Update license status if needed
                logger.info(f"License {license_key_str} revoked via webhook")

            elif event_type == 'license.expired':
                # Handle expiration
                logger.info(f"License {license_key_str} expired via webhook")

            return True, None

        except Exception as e:
            logger.exception(f"Error processing Spwig Built-in License Server webhook: {e}")
            return False, str(e)

    def test_connection(self) -> Dict:
        """
        Test connection to Spwig Built-in License Server.

        Returns:
            Dict with 'success' (bool) and 'error' (str) or 'message' (str)
        """
        try:
            # Validate credentials first
            is_valid, error_msg = self.validate_credentials()
            if not is_valid:
                return {'success': False, 'error': error_msg}

            # Try to access the account endpoint
            endpoint = '/account/'
            success, response = self._make_request('GET', endpoint, headers=self._get_auth_headers())

            if success:
                account_name = response.get('name', 'Unknown')
                return {
                    'success': True,
                    'message': f'Connected to Spwig Built-in License Server (Account: {account_name})'
                }
            else:
                error = response.get('error', 'Unknown error')
                return {'success': False, 'error': f'Connection failed: {error}'}

        except Exception as e:
            logger.exception(f"Connection test failed for Spwig Built-in License Server")
            return {'success': False, 'error': str(e)}
