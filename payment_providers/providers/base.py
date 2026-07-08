"""
Base provider interface for payment integrations.

All payment provider implementations must inherit from PaymentProviderBase
and implement all abstract methods defined here.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from decimal import Decimal
from datetime import datetime


class PaymentProviderBase(ABC):
    """
    Abstract base class for all payment providers.

    Providers (like Stripe, PayPal, AirWallex) extend this class
    to provide standardized payment services including:
    - Payment processing (charge, authorize, capture)
    - Refund processing (full and partial)
    - Subscription billing (native or fallback)
    - Webhook processing
    - Payment method storage

    Attributes:
        provider_key (str): Unique identifier for the provider (e.g., 'airwallex', 'stripe')
        provider_name (str): Human-readable name (e.g., 'AirWallex', 'Stripe')
        capabilities (dict): Dictionary of supported features
        credential_schema (dict): JSON schema for required credentials
    """

    # Must be set by subclass
    provider_key: str = None
    provider_name: str = None

    def __init__(self, credentials: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        """
        Initialize provider with credentials and configuration.

        Args:
            credentials: Dictionary of decrypted API credentials
            config: Optional configuration dictionary

        Raises:
            ValueError: If credentials are invalid or missing
        """
        if not self.provider_key:
            raise ValueError("provider_key must be set by subclass")
        if not self.provider_name:
            raise ValueError("provider_name must be set by subclass")

        self.credentials = credentials
        self.config = config or {}

        # Select active credentials (strips test_/live_ prefixes for dual-credential structure)
        # then validate the selected unprefixed credentials
        selected = self._select_credentials(credentials)
        self.validate_credentials(selected)

    def _select_credentials(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """
        Select test or live credentials based on test_mode flag.
        Handles both new dual-credential structure and legacy single-credential structure.

        New dual-credential structure has:
        - test_mode: boolean flag
        - test_* prefixed fields (e.g., test_publishable_key, test_secret_key)
        - live_* prefixed fields (e.g., live_publishable_key, live_secret_key)

        Legacy structure has:
        - environment: string field ('test', 'live', 'sandbox', 'production', etc.)
        - Unprefixed credential fields

        Args:
            credentials: Full credentials dict (may have test_/live_ prefixes)

        Returns:
            Dict with selected credentials using unprefixed keys for easy access

        Example:
            Input (new structure):
                {
                    'test_mode': True,
                    'test_publishable_key': 'pk_test_xxx',
                    'test_secret_key': 'sk_test_yyy',
                    'live_publishable_key': 'pk_live_xxx',
                    'live_secret_key': 'sk_live_yyy'
                }
            Output:
                {
                    'test_mode': True,
                    'publishable_key': 'pk_test_xxx',
                    'secret_key': 'sk_test_yyy'
                }
        """
        # Check for new dual-credential structure
        has_test_mode = 'test_mode' in credentials
        has_prefixed_fields = any(
            k.startswith('test_') or k.startswith('live_')
            for k in credentials.keys()
        )

        if not (has_test_mode and has_prefixed_fields):
            # Legacy structure - return as-is
            return credentials

        # New structure - select active credentials
        test_mode = credentials.get('test_mode', True)
        prefix = 'test_' if test_mode else 'live_'

        selected = {'test_mode': test_mode}

        # Extract fields with active prefix, remove prefix
        for key, value in credentials.items():
            if key.startswith(prefix):
                unprefixed_key = key[len(prefix):]  # Remove prefix
                selected[unprefixed_key] = value
            elif not key.startswith('test_') and not key.startswith('live_'):
                # Shared fields (no prefix) - copy as-is
                selected[key] = value

        return selected

    @property
    @abstractmethod
    def capabilities(self) -> Dict[str, bool]:
        """
        Return dictionary of provider capabilities.

        Example:
            {
                'charge': True,              # Can process immediate payments
                'authorize': True,           # Can authorize payments
                'capture': True,             # Can capture authorized payments
                'void': True,                # Can void authorizations
                'refund': True,              # Can refund payments
                'partial_refund': True,      # Supports partial refunds
                'recurring': True,           # Supports subscription billing
                'save_payment_method': True, # Can save payment methods for future use
                'hosted_checkout': True,     # Supports hosted checkout page
                'integrated_checkout': True, # Supports integrated (on-site) checkout
                'webhooks': True,            # Supports webhook notifications
                'multi_currency': True,      # Supports multiple currencies
            }

        Returns:
            Dictionary mapping capability names to boolean values
        """
        pass

    @property
    @abstractmethod
    def credential_schema(self) -> Dict[str, Any]:
        """
        Return JSON schema describing required credentials.

        Used to generate dynamic credential entry forms and validate inputs.

        Example:
            {
                'type': 'object',
                'properties': {
                    'api_key': {
                        'type': 'string',
                        'title': 'API Key',
                        'description': 'Your API key from provider dashboard',
                        'required': True,
                        'secret': True
                    },
                    'api_secret': {
                        'type': 'string',
                        'title': 'API Secret',
                        'description': 'Your API secret',
                        'required': True,
                        'secret': True
                    },
                    'environment': {
                        'type': 'string',
                        'title': 'Environment',
                        'enum': ['sandbox', 'production'],
                        'default': 'sandbox',
                        'required': True
                    }
                }
            }

        Returns:
            JSON schema dictionary
        """
        pass

    @property
    @abstractmethod
    def supported_payment_methods(self) -> List[str]:
        """
        Return list of supported payment method types.

        Example:
            ['credit_card', 'debit_card', 'bank_transfer', 'digital_wallet', 'buy_now_pay_later']

        Returns:
            List of payment method type strings
        """
        pass

    @property
    @abstractmethod
    def supported_currencies(self) -> List[str]:
        """
        Return list of supported currency codes.

        Example:
            ['USD', 'EUR', 'GBP', 'SGD', 'AUD']

        Returns:
            List of ISO 4217 currency codes
        """
        pass

    @property
    @abstractmethod
    def supported_countries(self) -> List[str]:
        """
        Return list of supported country codes (for merchant accounts).

        Example:
            ['US', 'SG', 'AU', 'GB', 'CA']

        Returns:
            List of ISO 3166-1 alpha-2 country codes
        """
        pass

    @abstractmethod
    def validate_credentials(self, credentials: Dict[str, Any]) -> None:
        """
        Validate credentials against schema and business logic.

        Args:
            credentials: Dictionary of credential values

        Raises:
            ValueError: If credentials are invalid or missing required fields
        """
        pass

    @abstractmethod
    def redact_credentials(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """
        Redact sensitive credential values for logging.

        Args:
            credentials: Original credentials dictionary

        Returns:
            Dictionary with sensitive values masked (e.g., 'sk_***456')
        """
        pass

    @abstractmethod
    def test_connection(self) -> Dict[str, Any]:
        """
        Test API connection and credential validity.

        Should make a simple API call to verify credentials work.

        Returns:
            Dictionary with test results:
            {
                'success': True,
                'message': 'Connection successful',
                'details': {
                    'account_id': 'acct_123',
                    'account_name': 'Acme Corp',
                    'environment': 'sandbox',
                    'api_version': 'v2'
                }
            }
        """
        pass

    # Payment Processing Methods

    @abstractmethod
    def charge(
        self,
        amount: Decimal,
        currency: str,
        payment_method: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process an immediate payment charge.

        Args:
            amount: Payment amount (e.g., Decimal('99.99'))
            currency: Currency code (e.g., 'USD')
            payment_method: Payment method details
                {
                    'type': 'credit_card',
                    'token': 'tok_visa_4242',  # Tokenized card
                    'save_for_future': False   # Whether to save payment method
                }
            metadata: Optional metadata to attach to transaction
                {
                    'order_id': '12345',
                    'customer_id': 'cust_abc',
                    'customer_email': 'john@example.com'
                }

        Returns:
            Dictionary with transaction result:
            {
                'success': True,
                'transaction_id': 'txn_abc123',         # Internal transaction ID
                'provider_transaction_id': 'ch_xyz789', # Provider's transaction ID
                'status': 'completed',                   # completed, pending, failed
                'amount': Decimal('99.99'),
                'currency': 'USD',
                'payment_method_id': 'pm_abc123',       # If saved
                'created_at': datetime(...),
                'message': 'Payment successful',
                'raw_response': {...}                    # Full provider response
            }

        Raises:
            ValueError: If parameters are invalid
            ConnectionError: If API request fails
        """
        pass

    @abstractmethod
    def authorize(
        self,
        amount: Decimal,
        currency: str,
        payment_method: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Authorize a payment without capturing funds.

        Args:
            amount: Authorization amount
            currency: Currency code
            payment_method: Payment method details (same format as charge())
            metadata: Optional metadata

        Returns:
            Dictionary with authorization result:
            {
                'success': True,
                'authorization_id': 'auth_abc123',
                'provider_authorization_id': 'pi_xyz789',
                'status': 'authorized',
                'amount': Decimal('99.99'),
                'currency': 'USD',
                'expires_at': datetime(...),           # Authorization expiry
                'created_at': datetime(...),
                'message': 'Authorization successful',
                'raw_response': {...}
            }

        Raises:
            ValueError: If parameters are invalid
            ConnectionError: If API request fails
        """
        pass

    @abstractmethod
    def capture(
        self,
        authorization_id: str,
        amount: Optional[Decimal] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Capture funds from a previous authorization.

        Args:
            authorization_id: Provider's authorization ID
            amount: Amount to capture (if None, captures full authorized amount)
            metadata: Optional metadata

        Returns:
            Dictionary with capture result:
            {
                'success': True,
                'transaction_id': 'txn_abc123',
                'provider_transaction_id': 'ch_xyz789',
                'status': 'completed',
                'amount': Decimal('99.99'),
                'currency': 'USD',
                'created_at': datetime(...),
                'message': 'Capture successful',
                'raw_response': {...}
            }

        Raises:
            ValueError: If authorization_id is invalid or expired
            ConnectionError: If API request fails
        """
        pass

    @abstractmethod
    def void(
        self,
        authorization_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Void an uncaptured authorization.

        Args:
            authorization_id: Provider's authorization ID
            metadata: Optional metadata

        Returns:
            Dictionary with void result:
            {
                'success': True,
                'authorization_id': 'auth_abc123',
                'status': 'voided',
                'message': 'Authorization voided',
                'raw_response': {...}
            }

        Raises:
            ValueError: If authorization_id is invalid
            ConnectionError: If API request fails
        """
        pass

    @abstractmethod
    def refund(
        self,
        transaction_id: str,
        amount: Optional[Decimal] = None,
        reason: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Refund a completed payment.

        Args:
            transaction_id: Provider's transaction ID to refund
            amount: Amount to refund (if None, refunds full amount)
            reason: Optional refund reason
            metadata: Optional metadata

        Returns:
            Dictionary with refund result:
            {
                'success': True,
                'refund_id': 'ref_abc123',
                'provider_refund_id': 're_xyz789',
                'status': 'completed',                # completed, pending, failed
                'amount': Decimal('99.99'),
                'currency': 'USD',
                'created_at': datetime(...),
                'message': 'Refund successful',
                'raw_response': {...}
            }

        Raises:
            ValueError: If transaction_id is invalid or amount exceeds original
            ConnectionError: If API request fails
        """
        pass

    # Subscription Methods (Optional - only if capabilities['recurring'] == True)

    def create_subscription(
        self,
        customer_id: str,
        plan_id: str,
        payment_method: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a subscription with native provider support.

        Only implement if capabilities['recurring'] == True.

        Args:
            customer_id: Provider's customer ID
            plan_id: Provider's plan/price ID
            payment_method: Payment method details
            metadata: Optional metadata

        Returns:
            Dictionary with subscription result:
            {
                'success': True,
                'subscription_id': 'sub_abc123',
                'provider_subscription_id': 'sub_xyz789',
                'status': 'active',
                'current_period_start': datetime(...),
                'current_period_end': datetime(...),
                'next_billing_date': datetime(...),
                'message': 'Subscription created',
                'raw_response': {...}
            }

        Raises:
            NotImplementedError: If provider doesn't support subscriptions
        """
        raise NotImplementedError(f"{self.provider_name} does not support native subscriptions")

    def cancel_subscription(
        self,
        subscription_id: str,
        immediately: bool = False,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Cancel a subscription.

        Only implement if capabilities['recurring'] == True.

        Args:
            subscription_id: Provider's subscription ID
            immediately: If True, cancel immediately; if False, cancel at period end
            metadata: Optional metadata

        Returns:
            Dictionary with cancellation result:
            {
                'success': True,
                'subscription_id': 'sub_abc123',
                'status': 'canceled',
                'canceled_at': datetime(...),
                'ends_at': datetime(...),
                'message': 'Subscription canceled',
                'raw_response': {...}
            }

        Raises:
            NotImplementedError: If provider doesn't support subscriptions
        """
        raise NotImplementedError(f"{self.provider_name} does not support native subscriptions")

    # Payment Method Storage (Optional - only if capabilities['save_payment_method'] == True)

    def save_payment_method(
        self,
        customer_id: str,
        payment_method: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Save a payment method for future use.

        Only implement if capabilities['save_payment_method'] == True.

        Args:
            customer_id: Provider's customer ID
            payment_method: Payment method details (token, type, etc.)
            metadata: Optional metadata

        Returns:
            Dictionary with saved payment method:
            {
                'success': True,
                'payment_method_id': 'pm_abc123',
                'provider_payment_method_id': 'pm_xyz789',
                'type': 'credit_card',
                'last4': '4242',
                'brand': 'visa',
                'exp_month': 12,
                'exp_year': 2025,
                'message': 'Payment method saved',
                'raw_response': {...}
            }

        Raises:
            NotImplementedError: If provider doesn't support saving payment methods
        """
        raise NotImplementedError(f"{self.provider_name} does not support saving payment methods")

    def delete_payment_method(
        self,
        payment_method_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Delete a saved payment method.

        Only implement if capabilities['save_payment_method'] == True.

        Args:
            payment_method_id: Provider's payment method ID
            metadata: Optional metadata

        Returns:
            Dictionary with deletion result:
            {
                'success': True,
                'payment_method_id': 'pm_abc123',
                'message': 'Payment method deleted',
                'raw_response': {...}
            }

        Raises:
            NotImplementedError: If provider doesn't support saving payment methods
        """
        raise NotImplementedError(f"{self.provider_name} does not support saving payment methods")

    # Webhook Methods

    @abstractmethod
    def verify_webhook_signature(self, payload: bytes, signature: str, **kwargs) -> bool:
        """
        Verify webhook authenticity using provider's signature method.

        Args:
            payload: Raw request body as bytes
            signature: Signature header value
            **kwargs: Additional headers or metadata needed for verification
                     (e.g., timestamp for Stripe, webhook_id for others)

        Returns:
            True if signature is valid, False otherwise
        """
        pass

    @abstractmethod
    def handle_webhook(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process webhook event from provider.

        Args:
            event_type: Type of webhook event
                       (e.g., 'payment.succeeded', 'refund.completed', 'subscription.canceled')
            payload: Webhook payload dictionary

        Returns:
            Dictionary with processed webhook data:
            {
                'action': 'payment_completed',  # payment_completed, refund_completed, subscription_updated
                'transaction_id': 'txn_abc123',
                'status': 'completed',
                'amount': Decimal('99.99'),
                'currency': 'USD',
                'metadata': {...},
                'raw_event': {...}
            }

        Raises:
            ValueError: If payload is invalid
        """
        pass

    def process_webhook(self, payload: Dict[str, Any], event_type: str = None) -> Dict[str, Any]:
        """
        Backward-compatible wrapper called by WebhookService.
        Delegates to the abstract handle_webhook() with correct parameter order.
        """
        if event_type is None:
            event_type = payload.get('type', payload.get('event_type', 'unknown'))
        result = self.handle_webhook(event_type, payload)
        if 'success' not in result:
            result['success'] = result.get('handled', True)
        return result

    def translate_subscription_webhook(self, event_type: str, payload: dict):
        """
        Translate a webhook event into a standardized SubscriptionEvent.
        Returns None if the event is not subscription-related.

        Payment provider components that declare ``recurring: true`` should
        override this to translate their provider-specific subscription
        events into the platform's SubscriptionEvent format.
        """
        return None

    # Checkout Methods

    def create_checkout_session(
        self,
        amount: Decimal,
        currency: str,
        success_url: str,
        cancel_url: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a hosted checkout session (if supported).

        Only implement if capabilities['hosted_checkout'] == True.

        Args:
            amount: Payment amount
            currency: Currency code
            success_url: URL to redirect on success
            cancel_url: URL to redirect on cancellation
            metadata: Optional metadata

        Returns:
            Dictionary with checkout session:
            {
                'success': True,
                'session_id': 'cs_abc123',
                'checkout_url': 'https://provider.com/checkout/cs_abc123',
                'expires_at': datetime(...),
                'message': 'Checkout session created',
                'raw_response': {...}
            }

        Raises:
            NotImplementedError: If provider doesn't support hosted checkout
        """
        raise NotImplementedError(f"{self.provider_name} does not support hosted checkout")

    def get_checkout_client_secret(
        self,
        amount: Decimal,
        currency: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get client secret for integrated checkout (if supported).

        Only implement if capabilities['integrated_checkout'] == True.

        Args:
            amount: Payment amount
            currency: Currency code
            metadata: Optional metadata

        Returns:
            Dictionary with client secret:
            {
                'success': True,
                'client_secret': 'pi_abc123_secret_xyz',
                'publishable_key': 'pk_test_abc',  # If needed for client SDK
                'intent_id': 'pi_abc123',
                'message': 'Client secret generated',
                'raw_response': {...}
            }

        Raises:
            NotImplementedError: If provider doesn't support integrated checkout
        """
        raise NotImplementedError(f"{self.provider_name} does not support integrated checkout")

    # Payment Intent Methods (for checkout orchestration)

    def create_payment_intent_for_checkout(
        self,
        amount: Decimal,
        currency: str,
        return_url: str,
        cancel_url: str,
        customer_email: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a payment intent for checkout orchestration.

        This method is used by the PaymentOrchestrationService to create
        payment intents for the checkout flow. It supports both hosted
        and embedded checkout modes.

        Args:
            amount: Payment amount
            currency: Currency code (e.g., 'USD', 'EUR')
            return_url: URL to redirect after successful payment
            cancel_url: URL to redirect on cancellation
            customer_email: Optional customer email for notifications
            metadata: Optional metadata (order_id, checkout_session_id, etc.)
            **kwargs: Additional params passed by orchestration service:
                payment_method_types: List of enabled method slugs for
                    the customer's country (from enabled_payment_methods).
                    Providers that support API-level filtering should use
                    this to constrain their checkout page.
                customer_name: Customer full name
                customer_country: ISO country code

        Returns:
            Dictionary with payment intent details:
            {
                'success': True,
                'provider_intent_id': 'pi_xxx' | 'int_xxx',  # Provider's intent ID
                'client_secret': 'pi_xxx_secret_yyy',        # For embedded checkout
                'checkout_url': 'https://checkout.../pay',    # For hosted checkout
                'status': 'created' | 'requires_payment_method' | 'requires_action',
                'requires_action': False,                     # True if 3DS needed
                'action': {                                   # If requires_action=True
                    'type': 'redirect' | '3ds_challenge',
                    'url': 'https://...',
                    'data': {...}
                },
                'expires_at': datetime,                       # When intent expires
                'raw_response': {...}                         # Full provider response
            }

        Raises:
            NotImplementedError: If provider doesn't support payment intents
        """
        raise NotImplementedError(
            f"{self.provider_name} does not support create_payment_intent_for_checkout. "
            f"Implement this method for checkout orchestration."
        )

    def retrieve_payment_intent(
        self,
        intent_id: str
    ) -> Dict[str, Any]:
        """
        Retrieve current status of a payment intent.

        Used to poll for payment status after hosted checkout redirect
        or during processing.

        Args:
            intent_id: Provider's payment intent ID

        Returns:
            Dictionary with intent status:
            {
                'success': True,
                'status': 'created' | 'requires_action' | 'processing' | 'succeeded' | 'failed',
                'provider_status': 'REQUIRES_PAYMENT_METHOD',  # Raw provider status
                'requires_action': False,
                'action': {...},                               # If requires_action
                'payment_method_type': 'card',                 # If payment method attached
                'payment_method_last4': '4242',
                'error': {                                     # If failed
                    'code': 'card_declined',
                    'message': 'Your card was declined'
                },
                'raw_response': {...}
            }

        Raises:
            NotImplementedError: If provider doesn't support payment intents
        """
        raise NotImplementedError(
            f"{self.provider_name} does not support retrieve_payment_intent. "
            f"Implement this method for checkout orchestration."
        )

    def confirm_payment_intent(
        self,
        intent_id: str,
        confirmation_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Confirm a payment intent after customer action (3DS, etc.)

        Called after customer completes 3DS authentication or other
        required actions.

        Args:
            intent_id: Provider's payment intent ID
            confirmation_data: Optional provider-specific confirmation data
                {
                    'payment_method': 'pm_xxx',  # Payment method to use
                    'return_url': 'https://...'  # For additional redirects
                }

        Returns:
            Dictionary with confirmation result:
            {
                'success': True,
                'status': 'succeeded' | 'processing' | 'requires_action',
                'requires_action': False,                     # True if more action needed
                'action': {...},                              # If requires_action
                'payment_method_type': 'card',
                'payment_method_last4': '4242',
                'message': 'Payment confirmed',
                'error': {...},                               # If failed
                'raw_response': {...}
            }

        Raises:
            NotImplementedError: If provider doesn't support payment intents
        """
        raise NotImplementedError(
            f"{self.provider_name} does not support confirm_payment_intent. "
            f"Implement this method for checkout orchestration."
        )

    def cancel_payment_intent(
        self,
        intent_id: str,
        cancellation_reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Cancel a payment intent.

        Args:
            intent_id: Provider's payment intent ID
            cancellation_reason: Optional reason for cancellation

        Returns:
            Dictionary with cancellation result:
            {
                'success': True,
                'status': 'canceled',
                'message': 'Payment intent canceled',
                'raw_response': {...}
            }

        Raises:
            NotImplementedError: If provider doesn't support payment intents
        """
        raise NotImplementedError(
            f"{self.provider_name} does not support cancel_payment_intent. "
            f"Implement this method for checkout orchestration."
        )

    def get_payment_method_types(self) -> Dict[str, Any]:
        """
        Get available payment method types from provider.

        Returns list of payment methods available per country, based on
        the provider account configuration.

        Returns:
            Dictionary with payment methods by country:
            {
                'success': True,
                'methods': {
                    'US': ['card', 'apple_pay', 'google_pay'],
                    'SG': ['card', 'paynow', 'grabpay'],
                    'AU': ['card', 'apple_pay']
                },
                'raw_response': {...}
            }

        Raises:
            NotImplementedError: If provider doesn't support method sync
        """
        # Default implementation returns static supported methods
        countries = self.supported_countries
        methods = self.supported_payment_methods

        return {
            'success': True,
            'methods': {country: methods for country in countries},
            'raw_response': {}
        }

    # Helper methods (optional to override)

    def supports_capability(self, capability: str) -> bool:
        """
        Check if provider supports a specific capability.

        Args:
            capability: Capability name (e.g., 'charge', 'refund', 'recurring')

        Returns:
            True if capability is supported and enabled
        """
        return self.capabilities.get(capability, False)

    def get_required_credentials(self) -> List[str]:
        """
        Get list of required credential field names.

        Returns:
            List of field names that are required
        """
        schema = self.credential_schema
        required = []

        if 'properties' in schema:
            for field_name, field_spec in schema['properties'].items():
                if field_spec.get('required', False):
                    required.append(field_name)

        return required

    def __repr__(self) -> str:
        """String representation of provider."""
        return f"<{self.__class__.__name__}({self.provider_key})>"
