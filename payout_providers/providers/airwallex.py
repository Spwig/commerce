"""
Airwallex Transfers Provider

Implements the Airwallex Transfers API for sending bank payouts to affiliates.
https://www.airwallex.com/docs/payouts__create-a-transfer
"""

import hashlib
import hmac
import logging
import time
import uuid
from decimal import Decimal
from typing import Any, Dict, List, Optional

import requests

from .base import (
    BasePayoutProvider,
    BatchPayoutResult,
    PayoutMethod,
    PayoutRecipient,
    PayoutRequest,
    PayoutResult,
    PayoutStatus,
)

logger = logging.getLogger(__name__)


class AirwallexPayoutProvider(BasePayoutProvider):
    """
    Airwallex Transfers API Provider

    Supports bank transfers to 200+ countries in 60+ currencies.
    Both SWIFT and LOCAL transfer methods are supported.
    """

    DEMO_API_BASE = "https://api-demo.airwallex.com/api/v1"
    PRODUCTION_API_BASE = "https://api.airwallex.com/api/v1"

    # Airwallex transfer status mapping
    STATUS_MAP = {
        'NEW': PayoutStatus.PENDING,
        'READY_FOR_FUNDING': PayoutStatus.PENDING,
        'BATCH_FUNDING_REQUESTED': PayoutStatus.PROCESSING,
        'BATCH_CONFIRMED': PayoutStatus.PROCESSING,
        'PROCESSING': PayoutStatus.PROCESSING,
        'IN_REVIEW': PayoutStatus.PROCESSING,
        'SENT': PayoutStatus.PROCESSING,
        'COMPLETED': PayoutStatus.COMPLETED,
        'SETTLED': PayoutStatus.COMPLETED,
        'FAILED': PayoutStatus.FAILED,
        'RETURNED': PayoutStatus.RETURNED,
        'CANCELLED': PayoutStatus.CANCELLED,
        'REJECTED': PayoutStatus.FAILED,
    }

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._access_token = None
        self._token_expires_at = None

    @property
    def provider_name(self) -> str:
        return 'airwallex'

    @property
    def display_name(self) -> str:
        return 'Airwallex Transfers'

    @property
    def supported_methods(self) -> List[PayoutMethod]:
        return [
            PayoutMethod.BANK_TRANSFER,
            PayoutMethod.BANK_TRANSFER_LOCAL,
            PayoutMethod.BANK_TRANSFER_SWIFT,
        ]

    @property
    def supported_currencies(self) -> List[str]:
        return [
            'USD', 'EUR', 'GBP', 'AUD', 'CAD', 'SGD', 'HKD', 'CNY', 'JPY',
            'NZD', 'CHF', 'SEK', 'NOK', 'DKK', 'PLN', 'CZK', 'HUF', 'RON',
            'BGN', 'HRK', 'TRY', 'ZAR', 'MXN', 'BRL', 'INR', 'IDR', 'MYR',
            'PHP', 'THB', 'VND', 'KRW', 'TWD', 'ILS', 'AED', 'SAR', 'QAR',
            'KWD', 'BHD', 'OMR'
        ]

    @property
    def credential_schema(self) -> Dict[str, Any]:
        return {
            'client_id': {
                'type': 'string',
                'required': True,
                'label': 'Client ID',
                'help_text': 'Airwallex API Client ID'
            },
            'api_key': {
                'type': 'string',
                'required': True,
                'label': 'API Key',
                'sensitive': True,
                'help_text': 'Airwallex API Key'
            },
            'environment': {
                'type': 'select',
                'required': True,
                'label': 'Environment',
                'options': [
                    {'value': 'demo', 'label': 'Demo (Testing)'},
                    {'value': 'production', 'label': 'Production (Live)'}
                ],
                'default': 'demo'
            },
            'webhook_secret': {
                'type': 'string',
                'required': False,
                'label': 'Webhook Secret',
                'sensitive': True,
                'help_text': 'Secret for verifying webhook signatures'
            },
            'default_transfer_method': {
                'type': 'select',
                'required': False,
                'label': 'Default Transfer Method',
                'options': [
                    {'value': 'LOCAL', 'label': 'Local (Faster, lower fees)'},
                    {'value': 'SWIFT', 'label': 'SWIFT (International)'}
                ],
                'default': 'LOCAL'
            }
        }

    @property
    def _api_base(self) -> str:
        """Get API base URL based on environment"""
        env = self.config.get('environment', 'demo')
        return self.PRODUCTION_API_BASE if env == 'production' else self.DEMO_API_BASE

    def _get_access_token(self) -> str:
        """
        Get access token from Airwallex.

        Airwallex uses client_id and api_key for authentication.
        """
        # Return cached token if still valid (Airwallex tokens last ~50 mins)
        if self._access_token and self._token_expires_at:
            if time.time() < self._token_expires_at - 60:
                return self._access_token

        client_id = self.config.get('client_id')
        api_key = self.config.get('api_key')

        if not client_id or not api_key:
            raise ValueError("Airwallex client_id and api_key are required")

        response = requests.post(
            f"{self._api_base}/authentication/login",
            headers={
                'x-client-id': client_id,
                'x-api-key': api_key,
                'Content-Type': 'application/json'
            },
            json={},
            timeout=30
        )

        if response.status_code != 201:
            logger.error(f"Airwallex auth failed: {response.text}")
            raise ValueError(f"Airwallex authentication failed: {response.status_code}")

        data = response.json()
        self._access_token = data['token']
        # Airwallex tokens typically last 50 minutes
        self._token_expires_at = time.time() + 3000

        return self._access_token

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make authenticated request to Airwallex API.
        """
        token = self._get_access_token()

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        url = f"{self._api_base}{endpoint}"

        response = requests.request(
            method=method,
            url=url,
            json=data,
            params=params,
            headers=headers,
            timeout=60
        )

        logger.debug(f"Airwallex API {method} {endpoint}: {response.status_code}")

        return {
            'status_code': response.status_code,
            'data': response.json() if response.text else {},
            'headers': dict(response.headers)
        }

    def validate_credentials(self) -> Dict[str, Any]:
        """Validate Airwallex credentials"""
        try:
            self._get_access_token()
            return {'valid': True}
        except Exception as e:
            return {'valid': False, 'error': str(e)}

    def test_connection(self) -> Dict[str, Any]:
        """Test connection to Airwallex API"""
        try:
            self._get_access_token()

            # Get account info to verify access
            result = self._make_request('GET', '/accounts/current')

            if result['status_code'] == 200:
                account = result['data']
                return {
                    'success': True,
                    'message': 'Successfully connected to Airwallex API',
                    'environment': self.config.get('environment', 'demo'),
                    'account_id': account.get('account_id'),
                    'account_name': account.get('account_name')
                }

            return {
                'success': False,
                'message': f"Unexpected response: {result['status_code']}"
            }

        except Exception as e:
            logger.error(f"Airwallex connection test failed: {e}")
            return {'success': False, 'message': str(e)}

    def _create_beneficiary(self, recipient: PayoutRecipient, currency: str) -> Optional[str]:
        """
        Create or get beneficiary for bank transfer.

        Returns beneficiary_id if successful.
        """
        # Build beneficiary data
        beneficiary_data = {
            'bank_details': {
                'account_currency': currency,
                'account_name': recipient.bank_account_holder,
                'account_number': recipient.bank_account_number,
                'bank_country_code': recipient.bank_country,
            },
            'entity_type': 'PERSONAL',
            'beneficiary_name': recipient.bank_account_holder or 'Unknown',
        }

        # Add optional bank details
        if recipient.bank_swift_code:
            beneficiary_data['bank_details']['swift_code'] = recipient.bank_swift_code

        if recipient.bank_routing_code:
            beneficiary_data['bank_details']['local_clearing_system'] = recipient.bank_routing_code

        try:
            result = self._make_request('POST', '/beneficiaries/create', data=beneficiary_data)

            if result['status_code'] in (200, 201):
                return result['data'].get('beneficiary_id')
            else:
                logger.error(f"Failed to create beneficiary: {result['data']}")
                return None

        except Exception as e:
            logger.error(f"Error creating beneficiary: {e}")
            return None

    def create_payout(self, request: PayoutRequest) -> PayoutResult:
        """
        Create a single bank transfer payout via Airwallex.
        """
        recipient = request.recipient

        # Validate bank details
        if not all([
            recipient.bank_account_holder,
            recipient.bank_account_number,
            recipient.bank_country
        ]):
            return PayoutResult(
                success=False,
                status=PayoutStatus.FAILED,
                message='Missing required bank details (account holder, account number, country)'
            )

        # Create beneficiary first
        beneficiary_id = self._create_beneficiary(recipient, request.currency)

        if not beneficiary_id:
            return PayoutResult(
                success=False,
                status=PayoutStatus.FAILED,
                message='Failed to create beneficiary'
            )

        # Determine transfer method
        transfer_method = self.config.get('default_transfer_method', 'LOCAL')

        # Build transfer request
        transfer_data = {
            'beneficiary_id': beneficiary_id,
            'payment_amount': float(request.amount),
            'payment_currency': request.currency,
            'reason': 'affiliate_commission',
            'reference': request.reference,
            'source_currency': request.currency,
            'transfer_method': transfer_method,
        }

        if request.note:
            transfer_data['payment_note'] = request.note[:140]

        try:
            result = self._make_request('POST', '/transfers/create', data=transfer_data)

            if result['status_code'] in (200, 201):
                data = result['data']
                transfer_id = data.get('id')
                status = data.get('status', 'NEW')

                return PayoutResult(
                    success=True,
                    provider_reference=transfer_id,
                    status=self.STATUS_MAP.get(status, PayoutStatus.PENDING),
                    message=f"Transfer created with status: {status}",
                    raw_response=data
                )
            else:
                error = result['data']
                return PayoutResult(
                    success=False,
                    status=PayoutStatus.FAILED,
                    message=error.get('message', f"HTTP {result['status_code']}"),
                    raw_response=error
                )

        except Exception as e:
            logger.error(f"Airwallex transfer creation failed: {e}")
            return PayoutResult(
                success=False,
                status=PayoutStatus.FAILED,
                message=str(e)
            )

    def get_payout_status(self, provider_reference: str) -> PayoutResult:
        """
        Get status of a transfer.
        """
        try:
            result = self._make_request('GET', f'/transfers/{provider_reference}')

            if result['status_code'] == 200:
                data = result['data']
                status = data.get('status', 'NEW')

                return PayoutResult(
                    success=True,
                    provider_reference=provider_reference,
                    status=self.STATUS_MAP.get(status, PayoutStatus.PENDING),
                    message=status,
                    raw_response=data
                )
            else:
                return PayoutResult(
                    success=False,
                    status=PayoutStatus.FAILED,
                    message=result['data'].get('message', f"HTTP {result['status_code']}"),
                    raw_response=result['data']
                )

        except Exception as e:
            logger.error(f"Failed to get Airwallex transfer status: {e}")
            return PayoutResult(
                success=False,
                status=PayoutStatus.FAILED,
                message=str(e)
            )

    def cancel_payout(self, provider_reference: str) -> PayoutResult:
        """
        Cancel a transfer (if possible).

        Only NEW or READY_FOR_FUNDING transfers can be cancelled.
        """
        try:
            # First check current status
            status_result = self.get_payout_status(provider_reference)

            if not status_result.success:
                return status_result

            current_status = status_result.raw_response.get('status', '')
            if current_status not in ('NEW', 'READY_FOR_FUNDING'):
                return PayoutResult(
                    success=False,
                    status=PayoutStatus.FAILED,
                    message=f"Cannot cancel transfer in status: {current_status}"
                )

            # Cancel the transfer
            result = self._make_request('POST', f'/transfers/{provider_reference}/cancel')

            if result['status_code'] == 200:
                return PayoutResult(
                    success=True,
                    provider_reference=provider_reference,
                    status=PayoutStatus.CANCELLED,
                    message='Transfer cancelled successfully',
                    raw_response=result['data']
                )
            else:
                return PayoutResult(
                    success=False,
                    status=PayoutStatus.FAILED,
                    message=result['data'].get('message', f"HTTP {result['status_code']}"),
                    raw_response=result['data']
                )

        except Exception as e:
            logger.error(f"Failed to cancel Airwallex transfer: {e}")
            return PayoutResult(
                success=False,
                status=PayoutStatus.FAILED,
                message=str(e)
            )

    def verify_webhook_signature(
        self,
        payload: bytes,
        headers: Dict[str, str]
    ) -> bool:
        """
        Verify Airwallex webhook signature using HMAC-SHA256.
        """
        webhook_secret = self.config.get('webhook_secret')
        if not webhook_secret:
            logger.warning("No webhook_secret configured, skipping signature verification")
            return True

        timestamp = headers.get('x-timestamp', '')
        signature = headers.get('x-signature', '')

        if not timestamp or not signature:
            logger.warning("Missing webhook timestamp or signature headers")
            return False

        # Airwallex signature = HMAC-SHA256(timestamp + payload)
        try:
            payload_str = payload.decode('utf-8') if isinstance(payload, bytes) else payload
            message = f"{timestamp}{payload_str}"

            expected_sig = hmac.new(
                webhook_secret.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()

            return hmac.compare_digest(expected_sig, signature)

        except Exception as e:
            logger.error(f"Webhook signature verification failed: {e}")
            return False

    def handle_webhook(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process Airwallex webhook event.

        Relevant event types:
        - transfer.ready_for_funding
        - transfer.batch_confirmed
        - transfer.completed
        - transfer.failed
        - transfer.returned
        """
        event_name = event_data.get('name', '')
        data = event_data.get('data', {})

        # Extract transfer ID
        transfer_id = data.get('id') or data.get('transfer_id')
        status = data.get('status', 'NEW')

        return {
            'event_type': event_name,
            'payout_reference': transfer_id,
            'status': self.STATUS_MAP.get(status, PayoutStatus.PENDING),
            'message': status,
            'raw_data': event_data
        }

    def estimate_fees(self, amount: Decimal, currency: str, method: PayoutMethod) -> Optional[Decimal]:
        """
        Estimate Airwallex transfer fees.

        Fees vary by currency and transfer method. These are approximate.
        """
        if method == PayoutMethod.BANK_TRANSFER_LOCAL:
            # Local transfers are generally cheaper
            fee_structure = {
                'USD': Decimal('0.00'),  # Often free for USD domestic
                'EUR': Decimal('0.50'),
                'GBP': Decimal('0.50'),
                'AUD': Decimal('0.00'),
                'SGD': Decimal('0.00'),
            }
            return fee_structure.get(currency, Decimal('2.00'))

        elif method in (PayoutMethod.BANK_TRANSFER, PayoutMethod.BANK_TRANSFER_SWIFT):
            # SWIFT transfers have higher fees
            return Decimal('15.00')

        return Decimal('5.00')

    def get_estimated_arrival(self, method: PayoutMethod, country: str) -> Optional[str]:
        """Get estimated arrival time for Airwallex transfers"""
        if method == PayoutMethod.BANK_TRANSFER_LOCAL:
            # Local transfers by country
            instant_countries = ['AU', 'GB', 'SG', 'HK']
            same_day_countries = ['US', 'CA', 'EU']

            if country in instant_countries:
                return "Instant to 1 business day"
            elif country in same_day_countries:
                return "Same day to 1 business day"
            else:
                return "1-2 business days"

        elif method == PayoutMethod.BANK_TRANSFER_SWIFT:
            return "3-5 business days"

        return "1-3 business days"
