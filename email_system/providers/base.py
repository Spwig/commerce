"""
Email Provider Base Class

Abstract base class for all email provider integrations.
Pattern follows exchange_rates/providers/base.py and shipping provider architecture.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, TypedDict


class EmailAttachment(TypedDict):
    """Email attachment data structure"""
    filename: str
    content: bytes
    content_type: str


class EmailInlineImage(TypedDict):
    """Inline image data structure"""
    cid: str           # Content-ID for referencing in HTML
    filename: str
    content: bytes
    content_type: str


class EmailMessage(TypedDict, total=False):
    """
    Standard email message format passed to provider.send()

    All providers receive messages in this normalized format.
    Providers are responsible for converting to their API format.
    """
    message_id: str                          # Platform UUID
    from_email: str                          # Sender email (required)
    from_name: Optional[str]                 # Sender name
    to: List[str]                            # Recipient emails (required)
    cc: List[str]                            # CC recipients
    bcc: List[str]                           # BCC recipients
    reply_to: Optional[str]                  # Reply-To address
    subject: str                             # Email subject (required)
    html: str                                # HTML body (required)
    text: str                                # Plain text body
    headers: Dict[str, str]                  # Custom headers
    return_path: str                         # Return-Path for bounces (VERP)
    attachments: List[EmailAttachment]       # File attachments
    inline_images: List[EmailInlineImage]    # Inline images
    tags: List[str]                          # Provider tags
    metadata: Dict[str, str]                 # Custom metadata


class SendResult(TypedDict):
    """
    Result returned by provider.send()

    Standardized response format across all providers.
    """
    provider_message_id: str    # Provider's unique message ID
    accepted: bool              # Whether provider accepted the message
    status: str                 # "queued"|"sent"|"failed"
    error: Optional[str]        # Error message if failed
    details: Dict[str, Any]     # Additional provider-specific details


class EmailProviderBase(ABC):
    """
    Abstract base class for all email providers.

    All email provider integrations must inherit from this class and implement
    the required abstract methods and properties.

    Pattern follows exchange_rates/providers/base.py structure.
    """

    # Required class attributes - must be overridden in subclass
    provider_key: str = ""      # e.g., "gmail_api", "smtp", "postmark"
    provider_name: str = ""     # e.g., "Gmail API", "SMTP", "Postmark"

    def __init__(self, credentials: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        """
        Initialize provider with decrypted credentials.

        Args:
            credentials: Decrypted credential dictionary
            config: Optional provider-specific configuration
        """
        self.credentials = credentials
        self.config = config or {}

    @property
    @abstractmethod
    def capabilities(self) -> Dict[str, bool]:
        """
        Return provider capabilities.

        Returns:
            Dictionary of capability flags

        Example:
            {
                'send': True,
                'oauth': True,
                'healthcheck': True,
                'batch_send': False,
                'webhooks': False,
                'attachments': True,
                'inline_images': True,
                'tracking': True
            }
        """
        pass

    @property
    @abstractmethod
    def credential_schema(self) -> Dict[str, Dict[str, Any]]:
        """
        Return JSON schema for credentials.

        Must match manifest.json credential_schema format.
        Used for:
        - Admin form generation
        - Credential validation
        - Setup wizard display

        Returns:
            Dictionary mapping field names to schema definitions

        Example:
            {
                "api_key": {
                    "type": "string",
                    "title": "API Key",
                    "description": "Your API key from provider dashboard",
                    "required": True,
                    "secret": True,
                    "placeholder": "pk_abc123..."
                }
            }
        """
        pass

    @abstractmethod
    def send(self, message: EmailMessage) -> SendResult:
        """
        Send a single email message.

        This is the primary method that all providers must implement.
        The platform calls this method to send emails via the provider.

        Args:
            message: EmailMessage dictionary with all email data

        Returns:
            SendResult dictionary with send status and provider message ID

        Raises:
            Exception: If sending fails (exceptions are caught by platform)

        Implementation Notes:
        - Convert EmailMessage to provider's API format
        - Handle API authentication (OAuth token refresh, etc.)
        - Return provider's message ID for tracking
        - Set accepted=True if provider accepted the message
        - Set status to 'queued', 'sent', or 'failed'
        - Include error message if send failed
        """
        pass

    def validate_credentials(self, credentials: Dict[str, Any]) -> None:
        """
        Validate credential format before storage.

        Args:
            credentials: Credentials dictionary to validate

        Raises:
            ValueError: If credentials are invalid

        Default implementation does basic validation.
        Override for provider-specific validation.
        """
        schema = self.credential_schema

        for field_name, field_schema in schema.items():
            if field_schema.get('required', False):
                if field_name not in credentials:
                    raise ValueError(f"Missing required credential: {field_name}")

                if not credentials[field_name]:
                    raise ValueError(f"Credential '{field_name}' cannot be empty")

    def redact_credentials(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """
        Redact sensitive credential values for logging.

        Args:
            credentials: Plain credential dictionary

        Returns:
            Dictionary with sensitive values masked

        Default implementation redacts fields marked as secret in schema.
        """
        from email_system.utils.encryption import redact_credentials
        return redact_credentials(credentials)

    def healthcheck(self) -> Dict[str, Any]:
        """
        Test API connection and credential validity.

        Returns:
            Dictionary with health check results

        Example:
            {
                'success': True,
                'message': 'Successfully connected to provider',
                'details': {
                    'account_id': '12345',
                    'quota_remaining': 9999
                }
            }

        Default implementation returns unknown status.
        Override for actual health checks.
        """
        return {
            'success': None,
            'message': 'Health check not implemented for this provider',
            'details': {}
        }

    def get_oauth_handler(self):
        """
        Get OAuth handler instance for this provider.

        Returns:
            OAuth handler instance or None if OAuth not supported

        Override this method if provider supports OAuth.
        """
        return None

    def get_webhook_handler(self):
        """
        Get webhook handler instance for this provider.

        Returns:
            Webhook handler instance or None if webhooks not supported

        Override this method if provider supports webhooks.
        """
        return None

    def get_rate_limits(self) -> Dict[str, Any]:
        """
        Get current rate limit information.

        Returns:
            Dictionary with rate limit details

        Example:
            {
                'emails_per_second': 10,
                'emails_per_hour': 1000,
                'emails_per_month': 50000,
                'remaining': 9950,
                'reset_at': '2025-10-25T15:00:00Z'
            }
        """
        return {}


class EmailProviderError(Exception):
    """Base exception for email provider errors"""
    pass


class EmailProviderAuthError(EmailProviderError):
    """Authentication/authorization errors"""
    pass


class EmailProviderRateLimitError(EmailProviderError):
    """Rate limit exceeded errors"""
    pass


class EmailProviderValidationError(EmailProviderError):
    """Email validation errors (invalid address, etc.)"""
    pass
