"""
Built-in SMTP Server Provider

This provider sends emails through the platform's built-in SMTP server,
which automatically signs emails with DKIM and relays through Postfix.
"""

import logging
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

from email_system.providers.base import (
    EmailMessage,
    EmailProviderAuthError,
    EmailProviderBase,
    EmailProviderError,
    SendResult,
)

logger = logging.getLogger(__name__)


class BuiltinSMTPProvider(EmailProviderBase):
    """
    Built-in SMTP server provider.

    Sends emails through the platform's own SMTP server running on localhost.
    The SMTP server handles DKIM signing automatically.
    """

    # Required class attributes
    provider_key = "builtin_smtp"
    provider_name = "Built-in SMTP Server"

    # Server configuration
    SMTP_HOST = "127.0.0.1"
    SMTP_PORT = 2525  # Built-in server listens on 2525
    TIMEOUT = 30

    def __init__(self, credentials: dict[str, Any], config: dict[str, Any] | None = None):
        """
        Initialize the built-in SMTP provider.

        Args:
            credentials: Provider credentials (minimal for built-in server)
            config: Optional provider configuration
        """
        super().__init__(credentials, config)
        self.config = config or {}

    @property
    def capabilities(self) -> dict[str, bool]:
        """
        Return provider capabilities.

        Returns:
            Dict of capability flags
        """
        return {
            "send": True,
            "attachments": True,
            "html": True,
            "plaintext": True,
            "healthcheck": True,
            "dkim_signing": True,  # Automatic DKIM signing
            "oauth": False,
        }

    @property
    def credential_schema(self) -> dict[str, dict[str, Any]]:
        """
        Define credential schema for the built-in provider.

        The built-in provider requires minimal configuration since it uses
        the platform's own SMTP server.

        Returns:
            Credential schema dictionary
        """
        return {
            "enabled": {
                "type": "boolean",
                "required": False,
                "default": True,
                "label": "Enable Built-in SMTP Server",
                "help_text": "Use the platform's built-in SMTP server for sending emails",
            },
            "dkim_selector": {
                "type": "string",
                "required": False,
                "default": "mail",
                "label": "DKIM Selector",
                "help_text": "DKIM selector for email signing (default: mail)",
            },
        }

    def _create_mime_message(self, message: EmailMessage) -> MIMEMultipart:
        """
        Create a MIME message from EmailMessage.

        Args:
            message: EmailMessage dict

        Returns:
            MIMEMultipart message
        """
        # Create message container
        msg = MIMEMultipart("alternative")

        # Set headers
        msg["Subject"] = message["subject"]
        msg["From"] = message["from_email"]
        msg["To"] = ", ".join(message["to"])

        if message.get("cc"):
            msg["Cc"] = ", ".join(message["cc"])

        if message.get("reply_to"):
            msg["Reply-To"] = message["reply_to"]

        if message.get("headers"):
            for key, value in message["headers"].items():
                msg[key] = value

        # Add plain text body
        if message.get("text_body"):
            text_part = MIMEText(message["text_body"], "plain", "utf-8")
            msg.attach(text_part)

        # Add HTML body
        if message.get("html_body"):
            html_part = MIMEText(message["html_body"], "html", "utf-8")
            msg.attach(html_part)

        # Add attachments
        if message.get("attachments"):
            for attachment in message["attachments"]:
                self._add_attachment(msg, attachment)

        return msg

    def _add_attachment(self, msg: MIMEMultipart, attachment: dict[str, Any]):
        """
        Add an attachment to the MIME message.

        Args:
            msg: MIME message to add attachment to
            attachment: Attachment dict with 'filename', 'content', 'mimetype'
        """
        filename = attachment.get("filename", "attachment")
        content = attachment.get("content", b"")
        mimetype = attachment.get("mimetype", "application/octet-stream")

        # Parse mimetype
        maintype, subtype = (
            mimetype.split("/", 1) if "/" in mimetype else ("application", "octet-stream")
        )

        # Create attachment part
        part = MIMEBase(maintype, subtype)
        part.set_payload(content)
        encoders.encode_base64(part)

        part.add_header("Content-Disposition", f'attachment; filename="{filename}"')

        msg.attach(part)

    def send(self, message: EmailMessage) -> SendResult:
        """
        Send an email via the built-in SMTP server.

        Args:
            message: EmailMessage to send

        Returns:
            SendResult with success status and message ID

        Raises:
            EmailProviderError: If sending fails
        """
        try:
            # Create MIME message
            mime_message = self._create_mime_message(message)

            # Get all recipients
            recipients = list(message["to"])
            if message.get("cc"):
                recipients.extend(message["cc"])
            if message.get("bcc"):
                recipients.extend(message["bcc"])

            # Connect to built-in SMTP server
            with smtplib.SMTP(self.SMTP_HOST, self.SMTP_PORT, timeout=self.TIMEOUT) as smtp:
                # Send message
                # The built-in server will handle DKIM signing
                response = smtp.sendmail(
                    message["from_email"], recipients, mime_message.as_string()
                )

            # Generate message ID (use email.utils.make_msgid in production)
            import uuid

            message_id = f"<{uuid.uuid4()}@{self.SMTP_HOST}>"

            logger.info(f"Email sent via built-in SMTP: {message['from_email']} -> {message['to']}")

            return SendResult(
                provider_message_id=message_id,
                accepted=True,
                status="sent",
                error=None,
                details={"smtp_response": response},
            )

        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP authentication error: {e}")
            raise EmailProviderAuthError(f"Authentication failed: {e}")

        except smtplib.SMTPException as e:
            logger.error(f"SMTP error sending email: {e}")
            raise EmailProviderError(f"Failed to send email: {e}")

        except Exception as e:
            logger.error(f"Unexpected error sending email: {e}", exc_info=True)
            raise EmailProviderError(f"Unexpected error: {e}")

    def healthcheck(self) -> dict[str, Any]:
        """
        Check if the built-in SMTP server is healthy and accessible.

        Returns:
            Dict with health status and details
        """
        try:
            # Try to connect to the SMTP server
            with smtplib.SMTP(self.SMTP_HOST, self.SMTP_PORT, timeout=5) as smtp:
                code, message = smtp.noop()

                if code == 250:
                    return {
                        "healthy": True,
                        "message": "Built-in SMTP server is running",
                        "smtp_code": code,
                        "smtp_message": message.decode("utf-8")
                        if isinstance(message, bytes)
                        else message,
                    }
                else:
                    return {
                        "healthy": False,
                        "message": f"SMTP server returned code {code}",
                        "smtp_code": code,
                        "smtp_message": message.decode("utf-8")
                        if isinstance(message, bytes)
                        else message,
                    }

        except ConnectionRefusedError:
            return {
                "healthy": False,
                "message": "Built-in SMTP server is not running",
                "error": "Connection refused - server may not be started",
            }

        except TimeoutError:
            return {
                "healthy": False,
                "message": "Built-in SMTP server timeout",
                "error": "Server did not respond in time",
            }

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"healthy": False, "message": f"Health check failed: {str(e)}", "error": str(e)}

    def validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        Validate provider credentials.

        Args:
            credentials: Credentials dictionary to validate

        Raises:
            EmailProviderError: If credentials are invalid
        """
        # Built-in provider has minimal validation
        # Just check that it's not explicitly disabled
        if not credentials.get("enabled", True):
            raise EmailProviderError("Built-in SMTP provider is disabled")

    def redact_credentials(self, credentials: dict[str, Any]) -> dict[str, Any]:
        """
        Redact sensitive credential fields for logging.

        Args:
            credentials: Credentials dictionary

        Returns:
            Redacted credentials dictionary
        """
        # No sensitive fields to redact for built-in provider
        return credentials.copy()
