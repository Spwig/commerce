"""
SMS Provider Base Class.

Abstract interface for SMS/WhatsApp providers.
"""

from abc import ABC, abstractmethod
from typing import Any

import phonenumbers


class SMSProviderBase(ABC):
    """Base class for SMS/WhatsApp providers."""

    provider_key = None
    provider_name = None

    def __init__(self, account):
        """
        Initialize provider with account.

        Args:
            account: SMSProviderAccount instance
        """
        self.account = account
        self.credentials = account.get_credentials()

    @property
    @abstractmethod
    def credential_schema(self) -> dict[str, Any]:
        """
        Return JSON schema for required credentials.

        Returns:
            Dict describing credential fields
        """
        pass

    @abstractmethod
    def validate_credentials(self) -> None:
        """
        Validate that required credentials are present.

        Raises:
            ValueError: If credentials are invalid
        """
        pass

    @abstractmethod
    def test_connection(self) -> dict[str, Any]:
        """
        Test connection to the provider.

        Returns:
            Dict with 'success' boolean and 'message' string
        """
        pass

    @abstractmethod
    def send_sms(self, phone: str, message: str) -> dict[str, Any]:
        """
        Send an SMS message.

        Args:
            phone: Recipient phone number (E.164 format preferred)
            message: Message text

        Returns:
            Dict with 'success' boolean, 'message_id' on success,
            'error' on failure
        """
        pass

    def send_whatsapp(
        self,
        phone: str,
        template_name: str,
        template_params: dict[str, str],
    ) -> dict[str, Any]:
        """
        Send a WhatsApp template message.

        Override in providers that support WhatsApp.

        Args:
            phone: Recipient phone number
            template_name: WhatsApp template name
            template_params: Template parameter values

        Returns:
            Dict with 'success' boolean and details
        """
        return {
            "success": False,
            "error": "WhatsApp not supported by this provider",
        }

    def normalize_phone(self, phone: str) -> str:
        """
        Normalize phone number to E.164 format.

        Numbers without an international prefix are interpreted using the
        installation's configured default country.

        Args:
            phone: Phone number in various formats

        Returns:
            Phone number in E.164 format (e.g., +1234567890)

        Raises:
            ValueError: If the input cannot be parsed as a valid phone number
        """
        from core.utils import get_default_country

        # phonenumbers.parse() is lenient: it treats a leading "+" as the
        # international prefix and silently strips any other "+" while
        # normalizing digits, so misplaced/duplicated plus signs would be
        # accepted instead of rejected. Require "+" to appear at most once,
        # and only as the very first character.
        candidate = phone.strip()
        if "+" in candidate[1:]:
            raise ValueError(f"Invalid phone number: {phone!r}")

        try:
            parsed = phonenumbers.parse(phone, get_default_country())
        except phonenumbers.NumberParseException as exc:
            raise ValueError(f"Invalid phone number: {phone!r}") from exc

        if not phonenumbers.is_valid_number(parsed):
            raise ValueError(f"Invalid phone number: {phone!r}")

        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
