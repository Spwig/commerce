"""
Twilio SMS Provider.

Sends SMS messages via Twilio's REST API.
"""

import logging
from typing import Any

from .base import SMSProviderBase

logger = logging.getLogger(__name__)


class TwilioSMSProvider(SMSProviderBase):
    """Twilio SMS provider implementation."""

    provider_key = "twilio"
    provider_name = "Twilio SMS"

    @property
    def credential_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "account_sid": {
                    "type": "string",
                    "title": "Account SID",
                    "description": "Twilio Account SID (starts with AC...)",
                    "required": True,
                },
                "auth_token": {
                    "type": "string",
                    "title": "Auth Token",
                    "description": "Twilio Auth Token",
                    "required": True,
                    "secret": True,
                },
                "from_number": {
                    "type": "string",
                    "title": "From Number",
                    "description": "Twilio phone number to send from (E.164 format, e.g., +1234567890)",
                    "required": True,
                },
                "messaging_service_sid": {
                    "type": "string",
                    "title": "Messaging Service SID",
                    "description": "Optional: Messaging Service SID for high-volume sending",
                    "required": False,
                },
            },
        }

    def validate_credentials(self) -> None:
        """Validate Twilio credentials."""
        if not self.credentials.get("account_sid"):
            raise ValueError("Account SID is required")
        if not self.credentials.get("auth_token"):
            raise ValueError("Auth Token is required")
        if not self.credentials.get("from_number") and not self.credentials.get(
            "messaging_service_sid"
        ):
            raise ValueError("From Number or Messaging Service SID is required")

    def _get_client(self):
        """Get Twilio client."""
        from twilio.rest import Client

        return Client(
            self.credentials["account_sid"],
            self.credentials["auth_token"],
        )

    def test_connection(self) -> dict[str, Any]:
        """Test Twilio connection by fetching account info."""
        try:
            self.validate_credentials()
            client = self._get_client()

            # Fetch account to verify credentials
            account = client.api.accounts(self.credentials["account_sid"]).fetch()

            return {
                "success": True,
                "message": f"Connected to Twilio account: {account.friendly_name}",
            }

        except ImportError:
            return {
                "success": False,
                "message": "Twilio SDK not installed. Run: pip install twilio",
            }
        except Exception as e:
            logger.error(f"Twilio connection test failed: {e}")
            return {
                "success": False,
                "message": str(e),
            }

    def send_sms(self, phone: str, message: str) -> dict[str, Any]:
        """
        Send SMS via Twilio.

        Args:
            phone: Recipient phone number
            message: Message text

        Returns:
            Dict with success status and message ID
        """
        try:
            self.validate_credentials()
            client = self._get_client()

            # Normalize phone number
            to_number = self.normalize_phone(phone)

            # Build message params
            params = {
                "to": to_number,
                "body": message,
            }

            # Use messaging service if configured, otherwise use from number
            if self.credentials.get("messaging_service_sid"):
                params["messaging_service_sid"] = self.credentials["messaging_service_sid"]
            else:
                params["from_"] = self.credentials["from_number"]

            # Send message
            msg = client.messages.create(**params)

            logger.info(f"Twilio SMS sent: {msg.sid} to {to_number}")

            return {
                "success": True,
                "message_id": msg.sid,
                "status": msg.status,
            }

        except ImportError:
            return {
                "success": False,
                "error": "Twilio SDK not installed",
            }
        except Exception as e:
            logger.error(f"Twilio SMS send failed: {e}")
            return {
                "success": False,
                "error": str(e),
            }
