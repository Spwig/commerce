"""
Abstract base class for POS terminal payment providers.

Terminal providers handle integrated card reader communication:
- Connection token generation (for frontend SDK auth)
- Reader discovery and management
- PaymentIntent creation for card_present payments
- Payment collection and processing

Supports two integration modes:
- 'sdk': Frontend loads provider JS SDK and communicates with reader directly
         (e.g. Stripe Terminal). Backend provides connection tokens.
- 'cloud': Backend sends API calls to provider cloud, which pushes payment
           requests to the reader. Frontend polls for status.
           (e.g. Adyen, Square, SumUp, Zettle)

Much simpler than PaymentProviderBase — no webhooks, no hosted checkout,
no subscriptions.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from decimal import Decimal


class TerminalProviderBase(ABC):
    """
    Abstract base class for POS terminal payment providers.

    Subclasses implement the bridge between the POS backend and a specific
    terminal SDK (Stripe Terminal, SumUp, Square, etc.).

    Two integration modes are supported:
    - 'sdk': Frontend JS SDK talks to reader directly (Stripe Terminal)
    - 'cloud': Backend pushes payment to reader via cloud API (Adyen, Square, etc.)
    """

    provider_key: str = None
    provider_name: str = None

    def __init__(self, credentials: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        if not self.provider_key:
            raise ValueError("provider_key must be set by subclass")
        if not self.provider_name:
            raise ValueError("provider_name must be set by subclass")

        self.credentials = credentials
        self.config = config or {}
        self.validate_credentials(credentials)

    # ── Integration Mode ──────────────────────────────────────────────

    @property
    def integration_mode(self) -> str:
        """
        Return the integration mode for this provider.

        Returns:
            'sdk' - Frontend loads JS SDK and communicates with reader directly.
                    Requires create_connection_token() and frontend SDK loading.
            'cloud' - Backend pushes payment to reader via cloud API.
                      Uses initiate_cloud_payment() and check_payment_status().
        """
        return 'sdk'

    # ── Credential & Connection ──────────────────────────────────────

    @property
    @abstractmethod
    def credential_schema(self) -> Dict[str, Any]:
        """JSON schema describing required credentials for admin forms."""
        pass

    @abstractmethod
    def validate_credentials(self, credentials: Dict[str, Any]) -> None:
        """Validate credentials. Raise ValueError if invalid."""
        pass

    @abstractmethod
    def test_connection(self) -> Dict[str, Any]:
        """
        Test API connection.

        Returns:
            {'success': bool, 'message': str}
        """
        pass

    # ── Frontend SDK Support (sdk mode) ───────────────────────────────

    def create_connection_token(self) -> Dict[str, Any]:
        """
        Create a short-lived connection token for the frontend SDK.

        Only used by SDK-mode providers (e.g. Stripe Terminal).
        Cloud-mode providers should not override this.

        Returns:
            {'success': True, 'secret': 'pst_test_xxx'}
        """
        raise NotImplementedError(
            f"{self.provider_name} does not support connection tokens "
            f"(integration_mode='{self.integration_mode}')"
        )

    # ── Reader Management ────────────────────────────────────────────

    @abstractmethod
    def list_readers(self, location_id: Optional[str] = None) -> Dict[str, Any]:
        """
        List available readers from the provider.

        Returns:
            {'success': True, 'readers': [{'id': '...', 'label': '...', 'type': '...', ...}]}
        """
        pass

    def register_reader(self, registration_code: str, label: str,
                        location_id: Optional[str] = None) -> Dict[str, Any]:
        """Register a new reader device. Optional — not all providers require this."""
        raise NotImplementedError(f"{self.provider_name} does not support reader registration")

    def create_location(self, display_name: str, address: Dict[str, str]) -> Dict[str, Any]:
        """Create a Location object. Optional — Stripe-specific."""
        raise NotImplementedError(f"{self.provider_name} does not require locations")

    # ── Payment Operations (sdk mode) ─────────────────────────────────

    def create_payment_intent(
        self, amount: Decimal, currency: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a PaymentIntent for card_present collection on the terminal.

        Used by SDK-mode providers where the frontend SDK collects the card.
        Cloud-mode providers use initiate_cloud_payment() instead.

        Args:
            amount: Payment amount in major currency units (e.g. 49.99)
            currency: ISO 4217 currency code (e.g. 'USD')
            metadata: Optional metadata dict

        Returns:
            {'success': True, 'payment_intent_id': 'pi_xxx', 'client_secret': 'pi_xxx_secret'}
        """
        raise NotImplementedError(
            f"{self.provider_name} does not support SDK payment intents "
            f"(integration_mode='{self.integration_mode}')"
        )

    def capture_payment_intent(self, payment_intent_id: str) -> Dict[str, Any]:
        """
        Retrieve and verify a completed PaymentIntent.

        Used by SDK-mode providers to verify the frontend SDK collected successfully.
        Cloud-mode providers use check_payment_status() instead.

        Returns:
            {
                'success': True,
                'status': 'succeeded',
                'card_brand': 'visa',
                'last4': '4242',
                'amount': Decimal('49.99'),
            }
        """
        raise NotImplementedError(
            f"{self.provider_name} does not support SDK payment capture "
            f"(integration_mode='{self.integration_mode}')"
        )

    def cancel_payment_intent(self, payment_intent_id: str) -> Dict[str, Any]:
        """
        Cancel a pending PaymentIntent (e.g. customer cancelled).

        Works for both SDK and cloud providers. Cloud providers may also
        use cancel_cloud_payment() for transaction_id-based cancellation.

        Returns:
            {'success': True}
        """
        raise NotImplementedError(
            f"{self.provider_name} does not support payment cancellation"
        )

    # ── Payment Operations (cloud mode) ───────────────────────────────

    def initiate_cloud_payment(
        self, amount: Decimal, currency: str,
        reader_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Push a payment request to a reader via the provider's cloud API.

        Used by cloud-mode providers (Adyen, Square, SumUp, Zettle).
        The provider's cloud sends the payment to the specified reader,
        and the customer presents their card on the reader.

        Args:
            amount: Payment amount in major currency units (e.g. 49.99)
            currency: ISO 4217 currency code (e.g. 'USD')
            reader_id: Provider-specific reader identifier
            metadata: Optional metadata dict

        Returns:
            {
                'success': True,
                'transaction_id': 'txn_xxx',
                'status': 'pending',
            }
        """
        raise NotImplementedError(
            f"{self.provider_name} does not support cloud payments "
            f"(integration_mode='{self.integration_mode}')"
        )

    def check_payment_status(self, transaction_id: str) -> Dict[str, Any]:
        """
        Check the status of a cloud-initiated payment.

        Called by the frontend (via backend API) to poll for completion.

        Args:
            transaction_id: Transaction ID returned by initiate_cloud_payment()

        Returns:
            {
                'success': True,
                'status': 'pending' | 'succeeded' | 'failed' | 'canceled',
                'card_brand': 'visa',      # populated on success
                'last4': '4242',           # populated on success
                'amount': Decimal('49.99'), # populated on success
                'message': '...',          # populated on failure
            }
        """
        raise NotImplementedError(
            f"{self.provider_name} does not support payment status checks "
            f"(integration_mode='{self.integration_mode}')"
        )

    def cancel_cloud_payment(self, transaction_id: str) -> Dict[str, Any]:
        """
        Cancel a pending cloud payment.

        Args:
            transaction_id: Transaction ID returned by initiate_cloud_payment()

        Returns:
            {'success': True}
        """
        raise NotImplementedError(
            f"{self.provider_name} does not support cloud payment cancellation"
        )

    # ── Refunds ───────────────────────────────────────────────────────

    def refund_payment(self, payment_intent_id: str,
                       amount: Optional[Decimal] = None) -> Dict[str, Any]:
        """
        Refund a terminal payment. amount=None means full refund.
        Optional — not all providers support terminal refunds.
        """
        raise NotImplementedError(f"{self.provider_name} does not support refunds through terminal")
