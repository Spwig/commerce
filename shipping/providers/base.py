"""
Base provider interface for shipping integrations.

All shipping provider implementations must inherit from ProviderBase
and implement all abstract methods defined here.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from decimal import Decimal
from datetime import datetime


class ProviderBase(ABC):
    """
    Abstract base class for all shipping providers.

    Providers (like Easyship, ShipEngine, ShipStation) extend this class
    to provide standardized shipping services including:
    - Rate calculation
    - Label generation
    - Tracking updates
    - Webhook processing

    Attributes:
        provider_key (str): Unique identifier for the provider (e.g., 'easyship')
        provider_name (str): Human-readable name (e.g., 'Easyship')
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

        # Validate credentials against schema
        self.validate_credentials(credentials)

    @property
    @abstractmethod
    def capabilities(self) -> Dict[str, bool]:
        """
        Return dictionary of provider capabilities.

        Example:
            {
                'rates': True,              # Can fetch shipping rates
                'labels': True,             # Can generate shipping labels
                'tracking': True,           # Can track shipments
                'international': True,      # Supports international shipping
                'returns': False,           # Does not support return labels
                'pickup': False,            # Does not support pickup scheduling
                'insurance': True,          # Supports shipment insurance
                'signature': True,          # Supports signature confirmation
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
                        'description': 'Your Easyship API key',
                        'required': True,
                        'secret': True
                    },
                    'environment': {
                        'type': 'string',
                        'title': 'Environment',
                        'enum': ['sandbox', 'production'],
                        'default': 'sandbox'
                    }
                }
            }

        Returns:
            JSON schema dictionary
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
                    'account_name': 'Acme Corp',
                    'environment': 'sandbox',
                    'api_version': 'v2'
                }
            }
        """
        pass

    @abstractmethod
    def get_rates(
        self,
        origin: Dict[str, str],
        destination: Dict[str, str],
        parcels: List[Dict[str, Any]],
        options: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get shipping rates for a shipment.

        Args:
            origin: Origin address dictionary
                {
                    'country': 'US',
                    'postal_code': '10001',
                    'state': 'NY',
                    'city': 'New York'
                }
            destination: Destination address dictionary (same format)
            parcels: List of parcel dictionaries
                [{
                    'length': 10,  # cm
                    'width': 10,
                    'height': 5,
                    'weight': 500,  # grams
                    'value': 100.00,  # USD
                    'currency': 'USD'
                }]
            options: Optional shipping options
                {
                    'insurance': True,
                    'signature': False,
                    'saturday_delivery': False
                }

        Returns:
            List of rate dictionaries:
            [{
                'service_code': 'ups_ground',
                'service_name': 'UPS Ground',
                'carrier': 'UPS',
                'rate': Decimal('12.50'),
                'currency': 'USD',
                'delivery_days': 3,
                'delivery_date': datetime(2025, 10, 23),
                'billable_weight': 500,
                'included_insurance': Decimal('100.00')
            }]

        Raises:
            ValueError: If parameters are invalid
            ConnectionError: If API request fails
        """
        pass

    @abstractmethod
    def buy_label(
        self,
        shipment_id: str,
        rate: Dict[str, Any],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Purchase shipping label for selected rate.

        Args:
            shipment_id: Internal shipment ID or external provider shipment ID
            rate: Rate dictionary returned from get_rates()
            options: Optional purchase options
                {
                    'label_format': 'PDF',  # PDF, PNG, ZPL
                    'label_size': '4x6',    # 4x6, A4
                }

        Returns:
            Dictionary with label information:
            {
                'tracking_number': '1Z999AA10123456784',
                'label_url': 'https://...',
                'label_format': 'PDF',
                'cost': Decimal('12.50'),
                'currency': 'USD',
                'carrier': 'UPS',
                'service': 'UPS Ground',
                'external_shipment_id': 'shp_abc123',
                'created_at': datetime(2025, 10, 20, 10, 30)
            }

        Raises:
            ValueError: If rate is invalid or expired
            ConnectionError: If API request fails
        """
        pass

    @abstractmethod
    def cancel_label(self, tracking_number: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Cancel a shipping label and request refund.

        Args:
            tracking_number: Tracking number of label to cancel
            reason: Optional cancellation reason

        Returns:
            Dictionary with cancellation result:
            {
                'success': True,
                'refunded': True,
                'refund_amount': Decimal('12.50'),
                'currency': 'USD',
                'message': 'Label cancelled successfully'
            }

        Raises:
            ValueError: If tracking number is invalid
            ConnectionError: If API request fails
        """
        pass

    @abstractmethod
    def get_tracking(self, tracking_number: str) -> Dict[str, Any]:
        """
        Get tracking information for a shipment.

        Args:
            tracking_number: Tracking number to look up

        Returns:
            Dictionary with tracking data:
            {
                'tracking_number': '1Z999AA10123456784',
                'status': 'in_transit',  # created, in_transit, out_for_delivery, delivered, exception
                'carrier': 'UPS',
                'service': 'UPS Ground',
                'estimated_delivery': datetime(2025, 10, 23),
                'actual_delivery': None,
                'events': [
                    {
                        'timestamp': datetime(2025, 10, 20, 10, 30),
                        'status': 'picked_up',
                        'location': 'New York, NY',
                        'description': 'Package picked up by UPS'
                    },
                    {
                        'timestamp': datetime(2025, 10, 20, 14, 15),
                        'status': 'in_transit',
                        'location': 'Newark, NJ',
                        'description': 'Arrived at UPS facility'
                    }
                ]
            }

        Raises:
            ValueError: If tracking number is invalid
            ConnectionError: If API request fails
        """
        pass

    @abstractmethod
    def verify_webhook_signature(self, payload: bytes, signature: str, **kwargs) -> bool:
        """
        Verify webhook authenticity using provider's signature method.

        Args:
            payload: Raw request body as bytes
            signature: Signature header value
            **kwargs: Additional headers or metadata needed for verification

        Returns:
            True if signature is valid, False otherwise
        """
        pass

    @abstractmethod
    def handle_webhook(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process webhook event from provider.

        Args:
            event_type: Type of webhook event (e.g., 'tracking.updated', 'label.created')
            payload: Webhook payload dictionary

        Returns:
            Dictionary with processed webhook data:
            {
                'action': 'update_tracking',  # update_tracking, update_status, create_event
                'tracking_number': '1Z999AA10123456784',
                'status': 'delivered',
                'event': {
                    'timestamp': datetime(2025, 10, 23, 16, 45),
                    'status': 'delivered',
                    'location': 'Chicago, IL',
                    'description': 'Package delivered'
                }
            }

        Raises:
            ValueError: If payload is invalid
        """
        pass

    # Helper methods (optional to override)

    def supports_capability(self, capability: str) -> bool:
        """
        Check if provider supports a specific capability.

        Args:
            capability: Capability name (e.g., 'rates', 'labels', 'tracking')

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
