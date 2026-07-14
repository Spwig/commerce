"""
Manual/fallback terminal provider.

Preserves the current behavior where the cashier processes payment
on a standalone card terminal and manually enters a card reference.
No SDK, no connection tokens, no reader management.
"""

import uuid
from decimal import Decimal

from .base import TerminalProviderBase


class ManualTerminalProvider(TerminalProviderBase):
    provider_key = "manual"
    provider_name = "Manual Entry"

    @property
    def credential_schema(self):
        return {"type": "object", "properties": {}}

    def validate_credentials(self, credentials):
        pass  # No credentials needed

    def test_connection(self):
        return {"success": True, "message": "Manual entry — no connection needed"}

    def create_connection_token(self):
        raise NotImplementedError("Manual provider has no SDK")

    def list_readers(self, location_id=None):
        return {"success": True, "readers": []}

    def create_payment_intent(self, amount, currency, metadata=None):
        return {
            "success": True,
            "payment_intent_id": f"manual_{uuid.uuid4().hex[:12]}",
            "client_secret": "",
        }

    def capture_payment_intent(self, payment_intent_id):
        return {
            "success": True,
            "status": "succeeded",
            "card_brand": "",
            "last4": "",
            "amount": Decimal("0"),
        }

    def cancel_payment_intent(self, payment_intent_id):
        return {"success": True}
