"""
Twilio WhatsApp Provider.

Sends WhatsApp messages via Twilio's WhatsApp Business API.

Note: WhatsApp Business API requires:
1. Meta Business verification
2. Pre-approved message templates for outbound messages
3. Twilio WhatsApp-enabled number or WhatsApp Sandbox for testing
"""

import json
import logging
from typing import Any

from .base import SMSProviderBase

logger = logging.getLogger(__name__)


class TwilioWhatsAppProvider(SMSProviderBase):
    """Twilio WhatsApp provider implementation."""

    provider_key = "twilio_whatsapp"
    provider_name = "Twilio WhatsApp"

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
                    "title": "WhatsApp Number",
                    "description": "Twilio WhatsApp-enabled number (E.164 format, e.g., +1234567890). For sandbox use +14155238886.",
                    "required": True,
                },
                "content_sid_prefix": {
                    "type": "string",
                    "title": "Content SID Prefix",
                    "description": "Optional: Content template SID prefix for approved templates",
                    "required": False,
                },
                "content_templates": {
                    "type": "object",
                    "title": "Content Templates",
                    "description": (
                        "Optional: Mapping of template name to its approved Twilio "
                        'Content SID (e.g. {"order_receipt": "HXxxxxxxxx"})'
                    ),
                    "required": False,
                },
            },
        }

    def validate_credentials(self) -> None:
        """Validate Twilio WhatsApp credentials."""
        if not self.credentials.get("account_sid"):
            raise ValueError("Account SID is required")
        if not self.credentials.get("auth_token"):
            raise ValueError("Auth Token is required")
        if not self.credentials.get("from_number"):
            raise ValueError("WhatsApp Number is required")

    def _get_client(self):
        """Get Twilio client."""
        from twilio.rest import Client

        return Client(
            self.credentials["account_sid"],
            self.credentials["auth_token"],
        )

    def _format_whatsapp_number(self, phone: str) -> str:
        """Format phone number for WhatsApp (whatsapp:+1234567890)."""
        normalized = self.normalize_phone(phone)
        if not normalized.startswith("whatsapp:"):
            return f"whatsapp:{normalized}"
        return normalized

    def _resolve_content_sid(self, template_name: str) -> str:
        """Resolve a template name to its configured Twilio Content SID.

        Raises:
            ValueError: If the template name has no configured Content SID.
        """
        templates = self.credentials.get("content_templates") or {}
        # The credential wizard stores every field as a form string, so an
        # object-typed field arrives as a JSON string that must be parsed
        # back into a mapping before lookup.
        if isinstance(templates, str):
            try:
                templates = json.loads(templates)
            except (ValueError, TypeError):
                raise ValueError("content_templates is not valid JSON")
        if not isinstance(templates, dict):
            raise ValueError("content_templates must be a mapping of name to Content SID")
        content_sid = templates.get(template_name)
        if not content_sid:
            raise ValueError(f"Unknown WhatsApp template: {template_name!r}")
        return content_sid

    def test_connection(self) -> dict[str, Any]:
        """Test Twilio WhatsApp connection."""
        try:
            self.validate_credentials()
            client = self._get_client()

            # Fetch account to verify credentials
            account = client.api.accounts(self.credentials["account_sid"]).fetch()

            return {
                "success": True,
                "message": f"Connected to Twilio WhatsApp: {account.friendly_name}",
            }

        except ImportError:
            return {
                "success": False,
                "message": "Twilio SDK not installed. Run: pip install twilio",
            }
        except Exception as e:
            logger.error(f"Twilio WhatsApp connection test failed: {e}")
            return {
                "success": False,
                "message": str(e),
            }

    def send_sms(self, phone: str, message: str) -> dict[str, Any]:
        """
        Send a freeform WhatsApp message.

        Note: Freeform messages are only allowed within 24-hour session window.
        For unsolicited messages, use send_whatsapp with a template.

        Args:
            phone: Recipient phone number
            message: Message text

        Returns:
            Dict with success status and message ID
        """
        try:
            self.validate_credentials()
            client = self._get_client()

            # Format numbers for WhatsApp
            to_number = self._format_whatsapp_number(phone)
            from_number = self._format_whatsapp_number(self.credentials["from_number"])

            # Send message
            msg = client.messages.create(
                to=to_number,
                from_=from_number,
                body=message,
            )

            logger.info(f"Twilio WhatsApp sent: {msg.sid} to {to_number}")

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
            logger.error(f"Twilio WhatsApp send failed: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    def send_whatsapp(
        self,
        phone: str,
        template_name: str,
        template_params: dict[str, str],
    ) -> dict[str, Any]:
        """
        Send a WhatsApp template message.

        Template messages are pre-approved by Meta and required for
        outbound messages outside the 24-hour session window.

        Args:
            phone: Recipient phone number
            template_name: Template name (registered with Twilio/Meta)
            template_params: Parameter values for template placeholders

        Returns:
            Dict with success status and message ID
        """
        try:
            self.validate_credentials()
            client = self._get_client()

            # Resolve the requested template to its approved Content SID.
            # Sending a template message (rather than a free-form body) is
            # required outside WhatsApp's 24-hour session window.
            content_sid = self._resolve_content_sid(template_name)

            # Format numbers for WhatsApp
            to_number = self._format_whatsapp_number(phone)
            from_number = self._format_whatsapp_number(self.credentials["from_number"])

            # Send the approved template via Twilio's Content API. All template
            # parameters are passed as JSON-encoded content variables so the
            # placeholders defined by the template are populated verbatim.
            msg = client.messages.create(
                to=to_number,
                from_=from_number,
                content_sid=content_sid,
                content_variables=json.dumps(template_params),
            )

            logger.info(f"Twilio WhatsApp template sent: {msg.sid} to {to_number}")

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
            logger.error(f"Twilio WhatsApp template send failed: {e}")
            return {
                "success": False,
                "error": str(e),
            }
