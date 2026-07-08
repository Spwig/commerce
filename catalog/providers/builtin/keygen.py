"""
Keygen.sh License Provider Adapter

Integrates with Keygen.sh license management platform.
API Documentation: https://keygen.sh/docs/api/

Keygen.sh is a popular third-party license management service that provides:
- License key generation and validation
- Device/machine activation tracking
- License policies and entitlements
- Usage tracking and analytics
- Webhook notifications
"""

import logging
from typing import Dict, Tuple
from catalog.providers.base import BaseLicenseProviderAdapter

logger = logging.getLogger(__name__)


class KeygenAdapter(BaseLicenseProviderAdapter):
    """
    Adapter for Keygen.sh license management platform.

    Keygen uses a policy-based licensing system where licenses are issued
    against specific policies that define the terms and limitations.
    """

    provider_key = 'keygen'
    provider_name = 'Keygen.sh'

    @property
    def capabilities(self) -> Dict:
        """Return capability set for Keygen.sh"""
        return {
            'create_license': True,
            'validate_license': True,
            'activate_device': True,
            'deactivate_device': True,
            'suspend_license': True,
            'revoke_license': True,
            'webhooks': True,
            'policies': True,
            'usage_tracking': True,
            'floating_licenses': True,
            'offline_validation': False,  # Requires Keygen SDK
            'analytics': True,
        }

    @property
    def credential_schema(self) -> Dict:
        """Define required credentials for Keygen.sh"""
        return {
            'account_id': {
                'type': 'string',
                'title': 'Account ID',
                'required': True,
                'help_text': 'Your Keygen account ID (found in account URL)',
            },
            'api_token': {
                'type': 'string',
                'title': 'Product Token',
                'required': True,
                'secret': True,
                'help_text': 'Product API token from Keygen dashboard (Settings → Tokens)',
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
            return 'https://api.keygen.sh/v1'
        return 'https://api.keygen.sh/v1'

    def _get_auth_headers(self) -> Dict:
        """Get authentication headers for Keygen API"""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/vnd.api+json',
        }

    def _get_policy_id(self, product) -> str:
        """
        Get Keygen policy ID for a product.

        Merchants must map Spwig products to Keygen policies in provider_config.
        Format: {'product_mapping': {<product_id>: <policy_id>}}
        """
        product_mapping = self.config.get('product_mapping', {})
        policy_id = product_mapping.get(str(product.id))

        if not policy_id:
            # Try to get default policy
            policy_id = self.config.get('default_policy_id')

        return policy_id

    def create_license(self, license_key, product, order) -> Tuple[bool, str, Dict]:
        """
        Create license in Keygen.sh.

        Args:
            license_key: LicenseKey model instance
            product: Product model instance
            order: Order model instance

        Returns:
            Tuple of (success: bool, external_id: str, response_data: dict)
        """
        account_id = self.config.get('account_id')
        policy_id = self._get_policy_id(product)

        if not policy_id:
            error_msg = f"No Keygen policy mapping found for product {product.id}"
            logger.error(error_msg)
            return False, '', {'error': error_msg}

        endpoint = f'/accounts/{account_id}/licenses'

        data = {
            'data': {
                'type': 'licenses',
                'attributes': {
                    'key': license_key.key,
                    'name': f"License for {order.user.email}",
                    'maxMachines': license_key.max_activations,
                    'expiry': license_key.expires_at.isoformat() if license_key.expires_at else None,
                    'metadata': {
                        'order_id': str(order.id),
                        'order_number': order.order_number,
                        'customer_email': order.user.email,
                        'product_sku': product.sku,
                        'source': 'spwig',
                    }
                },
                'relationships': {
                    'policy': {
                        'data': {
                            'type': 'policies',
                            'id': policy_id
                        }
                    }
                }
            }
        }

        # Override base URL for Keygen
        original_endpoint = self.api_endpoint
        self.api_endpoint = self._get_base_url()

        success, response = self._make_request('POST', endpoint, data, headers=self._get_auth_headers())

        # Restore original endpoint
        self.api_endpoint = original_endpoint

        if success and response.get('data'):
            external_id = response['data']['id']
            logger.info(f"Successfully created license {license_key.key} in Keygen (ID: {external_id})")
            return True, external_id, response

        error = response.get('errors', [{}])[0].get('detail', 'Unknown error')
        logger.error(f"Failed to create license in Keygen: {error}")
        return False, '', response

    def validate_license(self, key: str) -> Tuple[bool, Dict]:
        """
        Validate license with Keygen.sh.

        Args:
            key: License key string

        Returns:
            Tuple of (is_valid: bool, validation_data: dict)
        """
        account_id = self.config.get('account_id')
        endpoint = f'/accounts/{account_id}/licenses/actions/validate-key'

        data = {
            'meta': {
                'key': key
            }
        }

        # Override base URL for Keygen
        original_endpoint = self.api_endpoint
        self.api_endpoint = self._get_base_url()

        success, response = self._make_request('POST', endpoint, data, headers=self._get_auth_headers())

        # Restore original endpoint
        self.api_endpoint = original_endpoint

        if success and response.get('meta', {}).get('valid'):
            logger.info(f"License {key} validated successfully in Keygen")
            return True, response

        logger.warning(f"License {key} validation failed in Keygen")
        return False, response

    def activate_device(self, license_key, device_fingerprint: str, device_info: Dict) -> Tuple[bool, str, Dict]:
        """
        Activate a device (machine) in Keygen.sh.

        Args:
            license_key: LicenseKey model instance
            device_fingerprint: Unique device identifier
            device_info: Dictionary of device information

        Returns:
            Tuple of (success: bool, activation_id: str, response_data: dict)
        """
        account_id = self.config.get('account_id')

        # First, we need to get the Keygen license ID
        # This should be stored in ExternalLicenseSync
        from catalog.models import ExternalLicenseSync

        try:
            sync = ExternalLicenseSync.objects.get(
                license_key=license_key,
                provider=self.provider,
                sync_status='success'
            )
            keygen_license_id = sync.external_id
        except ExternalLicenseSync.DoesNotExist:
            logger.error(f"No Keygen sync found for license {license_key.key}")
            return False, '', {'error': 'License not synced to Keygen'}

        endpoint = f'/accounts/{account_id}/machines'

        data = {
            'data': {
                'type': 'machines',
                'attributes': {
                    'fingerprint': device_fingerprint,
                    'name': device_info.get('device_name', ''),
                    'platform': device_info.get('platform', ''),
                    'metadata': device_info,
                },
                'relationships': {
                    'license': {
                        'data': {
                            'type': 'licenses',
                            'id': keygen_license_id
                        }
                    }
                }
            }
        }

        # Override base URL for Keygen
        original_endpoint = self.api_endpoint
        self.api_endpoint = self._get_base_url()

        success, response = self._make_request('POST', endpoint, data, headers=self._get_auth_headers())

        # Restore original endpoint
        self.api_endpoint = original_endpoint

        if success and response.get('data'):
            activation_id = response['data']['id']
            logger.info(f"Successfully activated device {device_fingerprint} in Keygen (ID: {activation_id})")
            return True, activation_id, response

        error = response.get('errors', [{}])[0].get('detail', 'Unknown error')
        logger.error(f"Failed to activate device in Keygen: {error}")
        return False, '', response

    def deactivate_device(self, license_key, device_fingerprint: str) -> Tuple[bool, Dict]:
        """
        Deactivate a device in Keygen.sh.

        In Keygen, this means deleting the machine record.

        Args:
            license_key: LicenseKey model instance
            device_fingerprint: Unique device identifier

        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        account_id = self.config.get('account_id')

        # Find the machine by fingerprint
        # We would need to store the Keygen machine ID during activation
        # For now, we'll try to find it by fingerprint
        endpoint = f'/accounts/{account_id}/machines/{device_fingerprint}'

        # Override base URL for Keygen
        original_endpoint = self.api_endpoint
        self.api_endpoint = self._get_base_url()

        success, response = self._make_request('DELETE', endpoint, headers=self._get_auth_headers())

        # Restore original endpoint
        self.api_endpoint = original_endpoint

        if success:
            logger.info(f"Successfully deactivated device {device_fingerprint} in Keygen")
            return True, response

        error = response.get('errors', [{}])[0].get('detail', 'Unknown error')
        logger.error(f"Failed to deactivate device in Keygen: {error}")
        return False, response

    def suspend_license(self, license_key) -> Tuple[bool, Dict]:
        """
        Suspend a license in Keygen.sh.

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
            keygen_license_id = sync.external_id
        except ExternalLicenseSync.DoesNotExist:
            return False, {'error': 'License not synced to Keygen'}

        account_id = self.config.get('account_id')
        endpoint = f'/accounts/{account_id}/licenses/{keygen_license_id}'

        data = {
            'data': {
                'type': 'licenses',
                'attributes': {
                    'suspended': True
                }
            }
        }

        # Override base URL for Keygen
        original_endpoint = self.api_endpoint
        self.api_endpoint = self._get_base_url()

        success, response = self._make_request('PATCH', endpoint, data, headers=self._get_auth_headers())

        # Restore original endpoint
        self.api_endpoint = original_endpoint

        if success:
            logger.info(f"Successfully suspended license {license_key.key} in Keygen")
            return True, response

        error = response.get('errors', [{}])[0].get('detail', 'Unknown error')
        logger.error(f"Failed to suspend license in Keygen: {error}")
        return False, response

    def revoke_license(self, license_key) -> Tuple[bool, Dict]:
        """
        Revoke a license in Keygen.sh.

        In Keygen, this deletes the license.

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
            keygen_license_id = sync.external_id
        except ExternalLicenseSync.DoesNotExist:
            return False, {'error': 'License not synced to Keygen'}

        account_id = self.config.get('account_id')
        endpoint = f'/accounts/{account_id}/licenses/{keygen_license_id}'

        # Override base URL for Keygen
        original_endpoint = self.api_endpoint
        self.api_endpoint = self._get_base_url()

        success, response = self._make_request('DELETE', endpoint, headers=self._get_auth_headers())

        # Restore original endpoint
        self.api_endpoint = original_endpoint

        if success:
            logger.info(f"Successfully revoked license {license_key.key} in Keygen")
            return True, response

        error = response.get('errors', [{}])[0].get('detail', 'Unknown error')
        logger.error(f"Failed to revoke license in Keygen: {error}")
        return False, response

    def get_license_info(self, external_id: str) -> Tuple[bool, Dict]:
        """
        Retrieve license information from Keygen.sh.

        Args:
            external_id: Keygen license ID

        Returns:
            Tuple of (success: bool, license_data: dict)
        """
        account_id = self.config.get('account_id')
        endpoint = f'/accounts/{account_id}/licenses/{external_id}'

        # Override base URL for Keygen
        original_endpoint = self.api_endpoint
        self.api_endpoint = self._get_base_url()

        success, response = self._make_request('GET', endpoint, headers=self._get_auth_headers())

        # Restore original endpoint
        self.api_endpoint = original_endpoint

        if success and response.get('data'):
            logger.info(f"Successfully retrieved license info for {external_id} from Keygen")
            return True, response

        error = response.get('errors', [{}])[0].get('detail', 'Unknown error')
        logger.error(f"Failed to retrieve license info from Keygen: {error}")
        return False, response

    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """
        Verify Keygen webhook signature.

        Keygen uses HMAC-SHA256 with webhook secret.

        Args:
            payload: Raw webhook payload bytes
            signature: Signature from Keygen-Signature header

        Returns:
            bool: True if signature is valid
        """
        # Use parent class implementation (HMAC-SHA256)
        return super().verify_webhook_signature(payload, signature)

    def test_connection(self) -> Dict:
        """
        Test connection to Keygen.sh API.

        Returns:
            Dict with 'success' (bool) and 'error' (str) or 'message' (str)
        """
        try:
            # Validate credentials first
            is_valid, error_msg = self.validate_credentials()
            if not is_valid:
                return {'success': False, 'error': error_msg}

            account_id = self.config.get('account_id')
            endpoint = f'/accounts/{account_id}'

            # Override base URL for Keygen
            original_endpoint = self.api_endpoint
            self.api_endpoint = self._get_base_url()

            success, response = self._make_request('GET', endpoint, headers=self._get_auth_headers())

            # Restore original endpoint
            self.api_endpoint = original_endpoint

            if success and response.get('data'):
                account_name = response['data'].get('attributes', {}).get('name', 'Unknown')
                return {
                    'success': True,
                    'message': f'Connected to Keygen.sh (Account: {account_name})'
                }
            else:
                error = response.get('errors', [{}])[0].get('detail', 'Unknown error')
                return {'success': False, 'error': f'Connection failed: {error}'}

        except Exception as e:
            logger.exception(f"Connection test failed for Keygen.sh")
            return {'success': False, 'error': str(e)}
