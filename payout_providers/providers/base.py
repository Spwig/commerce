"""
Base Payout Provider Interface

All payout providers must implement this interface to ensure consistent
behavior across different payment platforms (Airwallex, PayPal, etc.).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Any


class PayoutStatus(Enum):
    """Standard payout status across all providers"""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETURNED = "returned"


class PayoutMethod(Enum):
    """Supported payout methods"""

    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"
    BANK_TRANSFER_LOCAL = "bank_transfer_local"
    BANK_TRANSFER_SWIFT = "bank_transfer_swift"


@dataclass
class PayoutRecipient:
    """Recipient information for a payout"""

    affiliate_id: int
    email: str | None = None
    # Bank transfer fields
    bank_account_holder: str | None = None
    bank_account_number: str | None = None
    bank_routing_code: str | None = None
    bank_swift_code: str | None = None
    bank_country: str | None = None
    bank_currency: str | None = None
    # Additional fields some providers may need
    phone: str | None = None
    address: dict[str, str] | None = None


@dataclass
class PayoutRequest:
    """Request to create a payout"""

    payout_id: int  # Internal Payout model ID
    recipient: PayoutRecipient
    amount: Decimal
    currency: str
    reference: str  # Unique reference for idempotency
    note: str | None = None
    metadata: dict[str, Any] | None = None


@dataclass
class PayoutResult:
    """Result from a payout operation"""

    success: bool
    provider_reference: str | None = None
    status: PayoutStatus = PayoutStatus.PENDING
    message: str | None = None
    raw_response: dict[str, Any] | None = None
    fee: Decimal | None = None
    estimated_arrival: str | None = None


@dataclass
class BatchPayoutResult:
    """Result from a batch payout operation"""

    success: bool
    batch_reference: str | None = None
    results: list[PayoutResult] = None
    message: str | None = None
    raw_response: dict[str, Any] | None = None

    def __post_init__(self):
        if self.results is None:
            self.results = []


class BasePayoutProvider(ABC):
    """
    Abstract base class for payout providers.

    All payout provider implementations must inherit from this class
    and implement the required abstract methods.
    """

    def __init__(self, config: dict[str, Any]):
        """
        Initialize the provider with configuration.

        Args:
            config: Provider-specific configuration including API credentials
        """
        self.config = config

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name (e.g., 'paypal', 'airwallex')"""
        pass

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Return human-readable provider name"""
        pass

    @property
    @abstractmethod
    def supported_methods(self) -> list[PayoutMethod]:
        """Return list of supported payout methods"""
        pass

    @property
    @abstractmethod
    def supported_currencies(self) -> list[str]:
        """Return list of supported currency codes"""
        pass

    @property
    @abstractmethod
    def credential_schema(self) -> dict[str, Any]:
        """
        Return JSON schema for required credentials.

        Example:
        {
            "client_id": {"type": "string", "required": True, "label": "Client ID"},
            "client_secret": {"type": "string", "required": True, "label": "Client Secret", "sensitive": True},
        }
        """
        pass

    @abstractmethod
    def validate_credentials(self) -> dict[str, Any]:
        """
        Validate the provider credentials.

        Returns:
            Dict with 'valid' boolean and optional 'error' message
        """
        pass

    @abstractmethod
    def test_connection(self) -> dict[str, Any]:
        """
        Test the connection to the provider API.

        Returns:
            Dict with 'success' boolean, 'message', and optional details
        """
        pass

    @abstractmethod
    def create_payout(self, request: PayoutRequest) -> PayoutResult:
        """
        Create a single payout.

        Args:
            request: PayoutRequest with recipient and amount details

        Returns:
            PayoutResult with status and provider reference
        """
        pass

    def create_batch_payout(self, requests: list[PayoutRequest]) -> BatchPayoutResult:
        """
        Create multiple payouts in a batch.

        Default implementation processes individually. Providers that support
        native batching (like PayPal) should override this method.

        Args:
            requests: List of PayoutRequest objects

        Returns:
            BatchPayoutResult with individual results
        """
        results = []
        all_success = True

        for request in requests:
            result = self.create_payout(request)
            results.append(result)
            if not result.success:
                all_success = False

        return BatchPayoutResult(
            success=all_success, results=results, message=f"Processed {len(results)} payouts"
        )

    @abstractmethod
    def get_payout_status(self, provider_reference: str) -> PayoutResult:
        """
        Get the current status of a payout.

        Args:
            provider_reference: The reference returned when creating the payout

        Returns:
            PayoutResult with current status
        """
        pass

    @abstractmethod
    def cancel_payout(self, provider_reference: str) -> PayoutResult:
        """
        Attempt to cancel a payout.

        Args:
            provider_reference: The reference returned when creating the payout

        Returns:
            PayoutResult indicating success/failure of cancellation
        """
        pass

    @abstractmethod
    def verify_webhook_signature(self, payload: bytes, headers: dict[str, str]) -> bool:
        """
        Verify the authenticity of a webhook payload.

        Args:
            payload: Raw webhook payload bytes
            headers: HTTP headers from the webhook request

        Returns:
            True if signature is valid
        """
        pass

    @abstractmethod
    def handle_webhook(self, event_data: dict[str, Any]) -> dict[str, Any]:
        """
        Process a webhook event from the provider.

        Args:
            event_data: Parsed webhook event data

        Returns:
            Dict with:
                - 'event_type': The type of event
                - 'payout_reference': Provider reference for the payout
                - 'status': New PayoutStatus
                - 'message': Optional status message
                - 'raw_data': Original event data
        """
        pass

    def get_recipient_fields(self, method: PayoutMethod) -> list[dict[str, Any]]:
        """
        Get required recipient fields for a payout method.

        Args:
            method: The payout method

        Returns:
            List of field definitions with name, type, required, label
        """
        if method == PayoutMethod.PAYPAL:
            return [{"name": "email", "type": "email", "required": True, "label": "PayPal Email"}]
        elif method in (
            PayoutMethod.BANK_TRANSFER,
            PayoutMethod.BANK_TRANSFER_LOCAL,
            PayoutMethod.BANK_TRANSFER_SWIFT,
        ):
            return [
                {
                    "name": "bank_account_holder",
                    "type": "string",
                    "required": True,
                    "label": "Account Holder Name",
                },
                {
                    "name": "bank_account_number",
                    "type": "string",
                    "required": True,
                    "label": "Account Number",
                },
                {
                    "name": "bank_routing_code",
                    "type": "string",
                    "required": False,
                    "label": "Routing Code",
                },
                {
                    "name": "bank_swift_code",
                    "type": "string",
                    "required": True,
                    "label": "SWIFT/BIC Code",
                },
                {
                    "name": "bank_country",
                    "type": "country",
                    "required": True,
                    "label": "Bank Country",
                },
                {
                    "name": "bank_currency",
                    "type": "currency",
                    "required": True,
                    "label": "Account Currency",
                },
            ]
        return []

    def estimate_fees(self, amount: Decimal, currency: str, method: PayoutMethod) -> Decimal | None:
        """
        Estimate fees for a payout. Override if provider supports fee estimation.

        Args:
            amount: Payout amount
            currency: Currency code
            method: Payout method

        Returns:
            Estimated fee amount or None if not supported
        """
        return None

    def get_estimated_arrival(self, method: PayoutMethod, country: str) -> str | None:
        """
        Get estimated arrival time for a payout.

        Args:
            method: Payout method
            country: Destination country code

        Returns:
            Human-readable estimate (e.g., "1-2 business days") or None
        """
        return None
