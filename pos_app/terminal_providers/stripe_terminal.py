"""
Stripe Terminal provider for integrated card reader payments.

Uses the Stripe Python SDK to:
- Create connection tokens for the frontend JS SDK
- Create PaymentIntents with card_present type
- Manage readers and locations
- Process refunds
"""
import logging
from decimal import Decimal
from typing import Dict, Any, Optional

import stripe

from .base import TerminalProviderBase

logger = logging.getLogger(__name__)


class StripeTerminalProvider(TerminalProviderBase):
    provider_key = 'stripe_terminal'
    provider_name = 'Stripe Terminal'

    @property
    def credential_schema(self):
        return {
            'type': 'object',
            'properties': {
                'secret_key': {
                    'type': 'string',
                    'title': 'Secret Key',
                    'description': 'Stripe secret key (sk_live_... or sk_test_...)',
                    'required': True,
                    'secret': True,
                },
                'location_id': {
                    'type': 'string',
                    'title': 'Location ID',
                    'description': 'Stripe Terminal Location ID (tml_...). Created automatically if blank.',
                    'required': False,
                },
            },
        }

    def validate_credentials(self, credentials):
        secret_key = credentials.get('secret_key', '')
        if not secret_key:
            raise ValueError("Stripe secret key is required")
        if not secret_key.startswith(('sk_live_', 'sk_test_')):
            raise ValueError("Stripe secret key must start with 'sk_live_' or 'sk_test_'")

    def _get_stripe(self):
        """Return stripe module configured with this provider's key."""
        stripe.api_key = self.credentials['secret_key']
        return stripe

    # ── Connection ───────────────────────────────────────────────────

    def test_connection(self):
        s = self._get_stripe()
        try:
            account = s.Account.retrieve()
            name = (account.get('business_profile') or {}).get('name', 'Stripe Account')
            return {'success': True, 'message': f'Connected to {name}'}
        except stripe.error.AuthenticationError as e:
            return {'success': False, 'message': f'Invalid API key: {e}'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    def create_connection_token(self):
        s = self._get_stripe()
        try:
            params = {}
            location_id = self.config.get('location_id') or self.credentials.get('location_id')
            if location_id:
                params['location'] = location_id
            token = s.terminal.ConnectionToken.create(**params)
            return {'success': True, 'secret': token.secret}
        except Exception as e:
            logger.error(f"Stripe Terminal connection token error: {e}")
            return {'success': False, 'message': str(e)}

    # ── Readers ──────────────────────────────────────────────────────

    def list_readers(self, location_id=None):
        s = self._get_stripe()
        try:
            params = {'limit': 100}
            loc = location_id or self.config.get('location_id') or self.credentials.get('location_id')
            if loc:
                params['location'] = loc
            readers = s.terminal.Reader.list(**params)
            return {
                'success': True,
                'readers': [
                    {
                        'id': r.id,
                        'label': r.label or '',
                        'type': r.device_type,
                        'serial_number': getattr(r, 'serial_number', '') or '',
                        'ip_address': getattr(r, 'ip_address', '') or '',
                        'status': r.status,
                        'location': r.location,
                    }
                    for r in readers.data
                ],
            }
        except Exception as e:
            logger.error(f"Stripe Terminal list readers error: {e}")
            return {'success': False, 'message': str(e), 'readers': []}

    def register_reader(self, registration_code, label, location_id=None):
        s = self._get_stripe()
        loc = location_id or self.config.get('location_id') or self.credentials.get('location_id')
        try:
            params = {'registration_code': registration_code, 'label': label}
            if loc:
                params['location'] = loc
            reader = s.terminal.Reader.create(**params)
            return {
                'success': True,
                'reader_id': reader.id,
                'label': reader.label,
                'type': reader.device_type,
                'serial_number': getattr(reader, 'serial_number', ''),
            }
        except Exception as e:
            logger.error(f"Stripe Terminal register reader error: {e}")
            return {'success': False, 'message': str(e)}

    def create_location(self, display_name, address):
        s = self._get_stripe()
        try:
            loc = s.terminal.Location.create(
                display_name=display_name,
                address=address,
            )
            return {'success': True, 'location_id': loc.id}
        except Exception as e:
            logger.error(f"Stripe Terminal create location error: {e}")
            return {'success': False, 'message': str(e)}

    # ── Payment Operations ───────────────────────────────────────────

    def create_payment_intent(self, amount, currency, metadata=None):
        s = self._get_stripe()
        try:
            intent = s.PaymentIntent.create(
                amount=int(amount * 100),  # Stripe uses smallest currency unit
                currency=currency.lower(),
                payment_method_types=['card_present'],
                capture_method='automatic',
                metadata=metadata or {},
            )
            return {
                'success': True,
                'payment_intent_id': intent.id,
                'client_secret': intent.client_secret,
            }
        except Exception as e:
            logger.error(f"Stripe Terminal create payment intent error: {e}")
            return {'success': False, 'message': str(e)}

    def capture_payment_intent(self, payment_intent_id):
        s = self._get_stripe()
        try:
            intent = s.PaymentIntent.retrieve(payment_intent_id)

            card_brand = ''
            last4 = ''
            amount = Decimal('0')

            if intent.status == 'succeeded':
                amount = Decimal(str(intent.amount_received)) / 100
                # Extract card details from the charge
                latest_charge_id = intent.get('latest_charge')
                if latest_charge_id:
                    charge = s.Charge.retrieve(latest_charge_id)
                    pm_details = (charge.get('payment_method_details') or {}).get('card_present', {})
                    card_brand = pm_details.get('brand', '')
                    last4 = pm_details.get('last4', '')

            return {
                'success': intent.status == 'succeeded',
                'status': intent.status,
                'card_brand': card_brand,
                'last4': last4,
                'amount': amount,
            }
        except Exception as e:
            logger.error(f"Stripe Terminal capture error: {e}")
            return {'success': False, 'message': str(e)}

    def cancel_payment_intent(self, payment_intent_id):
        s = self._get_stripe()
        try:
            s.PaymentIntent.cancel(payment_intent_id)
            return {'success': True}
        except Exception as e:
            logger.error(f"Stripe Terminal cancel error: {e}")
            return {'success': False, 'message': str(e)}

    def refund_payment(self, payment_intent_id, amount=None):
        s = self._get_stripe()
        try:
            params = {'payment_intent': payment_intent_id}
            if amount is not None:
                params['amount'] = int(amount * 100)
            refund = s.Refund.create(**params)
            return {
                'success': True,
                'refund_id': refund.id,
                'status': refund.status,
            }
        except Exception as e:
            logger.error(f"Stripe Terminal refund error: {e}")
            return {'success': False, 'message': str(e)}

    # ── Splash Screen ─────────────────────────────────────────────────

    # Mapping of reader types to Stripe Configuration parameter keys
    READER_CONFIG_KEYS = {
        'stripe_s700': 'stripe_s700',
        'bbpos_wisepos_e': 'bbpos_wisepos_e',
        'verifone_p400': 'verifone_p400',
        'bbpos_wisepad_3': 'bbpos_wisepad_3',
    }

    def _get_reader_config_key(self, reader_type: str) -> str:
        """Get Stripe Configuration parameter key for a reader type."""
        normalized = reader_type.lower().strip() if reader_type else ''
        return self.READER_CONFIG_KEYS.get(normalized, 'bbpos_wisepos_e')

    def upload_splash_screen(self, png_bytes: bytes) -> str:
        """
        Upload a splash screen PNG to Stripe Files API.

        Args:
            png_bytes: PNG image data

        Returns:
            file_id (e.g., 'file_xxx')
        """
        import io
        s = self._get_stripe()
        try:
            # Create a file-like object from bytes
            file_obj = io.BytesIO(png_bytes)
            file_obj.name = 'splash_screen.png'

            file = s.File.create(
                purpose='terminal_reader_splashscreen',
                file=file_obj,
            )
            logger.info(f"Uploaded splash screen to Stripe: {file.id}")
            return file.id
        except Exception as e:
            logger.error(f"Stripe Terminal upload splash screen error: {e}")
            raise

    def create_splash_configuration(self, file_id: str, reader_type: str) -> str:
        """
        Create a Terminal Configuration with the splash screen.

        Args:
            file_id: Stripe File ID for the splash screen
            reader_type: Reader type (e.g., 'bbpos_wisepos_e')

        Returns:
            configuration_id (e.g., 'cfg_xxx')
        """
        s = self._get_stripe()
        try:
            config_key = self._get_reader_config_key(reader_type)

            # Build the configuration parameters
            # Each reader type has its own configuration section
            config_params = {
                config_key: {
                    'splashscreen': file_id
                }
            }

            config = s.terminal.Configuration.create(**config_params)
            logger.info(f"Created Stripe Terminal configuration: {config.id}")
            return config.id
        except Exception as e:
            logger.error(f"Stripe Terminal create configuration error: {e}")
            raise

    def assign_configuration_to_reader(self, reader_id: str, config_id: str):
        """
        Assign a Configuration to the reader's location.

        Note: Stripe Terminal configurations are assigned at the Location level,
        not per-reader. This will affect all readers at the same location.

        Args:
            reader_id: Stripe Reader ID (e.g., 'tmr_xxx')
            config_id: Stripe Configuration ID (e.g., 'cfg_xxx')
        """
        s = self._get_stripe()
        try:
            # First, get the reader to find its location
            reader = s.terminal.Reader.retrieve(reader_id)
            location_id = reader.location

            if not location_id:
                # Try to get location from provider config
                location_id = self.config.get('location_id') or self.credentials.get('location_id')

            if not location_id:
                raise ValueError(f"Reader {reader_id} has no location assigned")

            # Assign configuration to the location
            s.terminal.Location.modify(
                location_id,
                configuration_overrides=config_id
            )
            logger.info(f"Assigned configuration {config_id} to location {location_id} (reader {reader_id})")
        except Exception as e:
            logger.error(f"Stripe Terminal assign configuration error: {e}")
            raise
