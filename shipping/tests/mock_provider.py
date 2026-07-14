"""
Mock shipping provider for testing.

This provider implements all ProviderBase methods but doesn't make real API calls.
Used for testing the provider SDK infrastructure.
"""

import hashlib
import hmac
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any

from shipping.providers.base import ProviderBase


class MockProvider(ProviderBase):
    """
    Mock shipping provider for testing.

    Simulates a real provider with:
    - Rate calculation
    - Label generation
    - Tracking updates
    - Webhook processing

    All operations return fake data without making external API calls.
    """

    provider_key = "mock_provider"
    provider_name = "Mock Shipping Provider"

    @property
    def capabilities(self) -> dict[str, bool]:
        """Return all capabilities as enabled for testing."""
        return {
            "rates": True,
            "labels": True,
            "tracking": True,
            "international": True,
            "returns": True,
            "pickup": True,
            "insurance": True,
            "signature": True,
        }

    @property
    def credential_schema(self) -> dict[str, Any]:
        """Return mock credential schema."""
        return {
            "type": "object",
            "properties": {
                "api_key": {
                    "type": "string",
                    "title": "API Key",
                    "description": "Your Mock Provider API key",
                    "required": True,
                    "secret": True,
                },
                "api_secret": {
                    "type": "string",
                    "title": "API Secret",
                    "description": "Your Mock Provider API secret",
                    "required": True,
                    "secret": True,
                },
                "environment": {
                    "type": "string",
                    "title": "Environment",
                    "enum": ["sandbox", "production"],
                    "default": "sandbox",
                    "required": False,
                },
            },
        }

    def validate_credentials(self, credentials: dict[str, Any]) -> None:
        """Validate credentials against schema."""
        required = ["api_key", "api_secret"]
        missing = [field for field in required if not credentials.get(field)]

        if missing:
            raise ValueError(f"Missing required credentials: {', '.join(missing)}")

        # Validate api_key format
        if len(credentials["api_key"]) < 10:
            raise ValueError("API key must be at least 10 characters")

    def redact_credentials(self, credentials: dict[str, Any]) -> dict[str, Any]:
        """Redact sensitive values for logging."""
        redacted = credentials.copy()

        if "api_key" in redacted and len(redacted["api_key"]) > 6:
            redacted["api_key"] = f"***{redacted['api_key'][-4:]}"

        if "api_secret" in redacted and len(redacted["api_secret"]) > 6:
            redacted["api_secret"] = f"***{redacted['api_secret'][-4:]}"

        return redacted

    def test_connection(self) -> dict[str, Any]:
        """Test connection (always succeeds for mock)."""
        return {
            "success": True,
            "message": "Mock connection successful",
            "details": {
                "account_name": "Mock Test Account",
                "environment": self.credentials.get("environment", "sandbox"),
                "api_version": "v1",
                "balance": Decimal("1000.00"),
            },
        }

    def get_rates(
        self,
        origin: dict[str, str],
        destination: dict[str, str],
        parcels: list[dict[str, Any]],
        options: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Return mock shipping rates."""
        # Calculate fake rate based on weight
        total_weight = sum(p.get("weight", 500) for p in parcels)
        base_rate = Decimal(str(total_weight / 100))  # $1 per 100g

        # International shipping costs more
        is_international = origin.get("country") != destination.get("country")
        if is_international:
            base_rate *= Decimal("2.5")

        # Return 3 mock services
        rates = [
            {
                "service_code": "mock_ground",
                "service_name": "Mock Ground",
                "carrier": "Mock Carrier",
                "rate": base_rate,
                "currency": "USD",
                "delivery_days": 5,
                "delivery_date": datetime.now() + timedelta(days=5),
                "billable_weight": total_weight,
                "included_insurance": Decimal("100.00"),
            },
            {
                "service_code": "mock_express",
                "service_name": "Mock Express",
                "carrier": "Mock Carrier",
                "rate": base_rate * Decimal("2.0"),
                "currency": "USD",
                "delivery_days": 2,
                "delivery_date": datetime.now() + timedelta(days=2),
                "billable_weight": total_weight,
                "included_insurance": Decimal("200.00"),
            },
            {
                "service_code": "mock_overnight",
                "service_name": "Mock Overnight",
                "carrier": "Mock Carrier",
                "rate": base_rate * Decimal("3.5"),
                "currency": "USD",
                "delivery_days": 1,
                "delivery_date": datetime.now() + timedelta(days=1),
                "billable_weight": total_weight,
                "included_insurance": Decimal("500.00"),
            },
        ]

        return rates

    def buy_label(
        self, shipment_id: str, rate: dict[str, Any], options: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Generate mock shipping label."""
        tracking_number = f"MOCK{datetime.now().strftime('%Y%m%d%H%M%S')}"

        return {
            "tracking_number": tracking_number,
            "label_url": f"https://mock-provider.com/labels/{tracking_number}.pdf",
            "label_format": options.get("label_format", "PDF") if options else "PDF",
            "cost": rate["rate"],
            "currency": rate["currency"],
            "carrier": rate["carrier"],
            "service": rate["service_name"],
            "external_shipment_id": f"mock_shp_{shipment_id}",
            "created_at": datetime.now(),
        }

    def cancel_label(self, tracking_number: str, reason: str | None = None) -> dict[str, Any]:
        """Cancel mock label (always succeeds)."""
        return {
            "success": True,
            "refunded": True,
            "refund_amount": Decimal("12.50"),
            "currency": "USD",
            "message": f"Mock label {tracking_number} cancelled successfully",
        }

    def get_tracking(self, tracking_number: str) -> dict[str, Any]:
        """Return mock tracking information."""
        return {
            "tracking_number": tracking_number,
            "status": "in_transit",
            "carrier": "Mock Carrier",
            "service": "Mock Express",
            "estimated_delivery": datetime.now() + timedelta(days=2),
            "actual_delivery": None,
            "events": [
                {
                    "timestamp": datetime.now() - timedelta(hours=4),
                    "status": "picked_up",
                    "location": "Mock Origin, CA",
                    "description": "Package picked up by carrier",
                },
                {
                    "timestamp": datetime.now() - timedelta(hours=2),
                    "status": "in_transit",
                    "location": "Mock Hub, NV",
                    "description": "Arrived at sorting facility",
                },
                {
                    "timestamp": datetime.now(),
                    "status": "in_transit",
                    "location": "Mock Hub, NV",
                    "description": "Departed sorting facility",
                },
            ],
        }

    def verify_webhook_signature(self, payload: bytes, signature: str, **kwargs) -> bool:
        """Verify mock webhook signature using HMAC."""
        # Use api_secret as webhook secret
        secret = self.credentials.get("api_secret", "").encode("utf-8")

        # Calculate expected signature
        expected = hmac.new(secret, payload, hashlib.sha256).hexdigest()

        return hmac.compare_digest(signature, expected)

    def handle_webhook(self, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Process mock webhook event."""
        if event_type == "tracking.updated":
            return {
                "action": "update_tracking",
                "tracking_number": payload.get("tracking_number"),
                "status": payload.get("status", "in_transit"),
                "event": {
                    "timestamp": datetime.now(),
                    "status": payload.get("status", "in_transit"),
                    "location": payload.get("location", "Unknown"),
                    "description": payload.get("description", "Status updated"),
                },
            }
        elif event_type == "label.created":
            return {
                "action": "label_created",
                "tracking_number": payload.get("tracking_number"),
                "label_url": payload.get("label_url"),
            }
        else:
            return {"action": "unknown", "event_type": event_type, "payload": payload}
