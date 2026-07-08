"""
Spwig Hosted Mail Provider

Sends emails through the centralized Spwig Mail Gateway (Postfix + OpenDKIM).
Only available on Spwig-hosted deployments. Credentials are injected at
provisioning time and are read-only — merchants cannot change the gateway
configuration.

The gateway handles:
- Per-merchant SASL authentication
- DKIM signing (myspwig.com by default, or verified custom domain)
- Rate limiting based on subscription plan
- Bounce/complaint tracking
"""
import logging
import smtplib
import ssl
import uuid
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, Optional

from email_system.providers.base import (
    EmailMessage,
    EmailProviderAuthError,
    EmailProviderBase,
    EmailProviderError,
    EmailProviderRateLimitError,
    SendResult,
)

logger = logging.getLogger(__name__)

# Headers that must not be set via the custom headers dict
_PROTECTED_HEADERS = frozenset({
    'from', 'to', 'cc', 'bcc', 'subject', 'date', 'message-id',
    'mime-version', 'content-type', 'content-transfer-encoding',
    'return-path', 'received', 'dkim-signature',
})


class SpwigHostedMailProvider(EmailProviderBase):
    """
    Email provider for Spwig-hosted deployments.

    Sends email through the centralized Spwig Mail Gateway.
    Zero configuration required — credentials are injected at provisioning time.
    Supports both myspwig.com default sender and verified custom domains.
    """

    provider_key = "spwig_hosted_mail"
    provider_name = "Spwig Email"

    TIMEOUT = 30

    @staticmethod
    def _tls_context() -> ssl.SSLContext:
        """Create a hardened TLS context for STARTTLS (TLS 1.2+)."""
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2
        # Use default CA bundle for certificate verification
        ctx.load_default_certs()
        return ctx

    def __init__(self, credentials: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        super().__init__(credentials, config)
        self.gateway_host = credentials.get('gateway_host', 'mail-gw.spwig.com')
        self.gateway_port = int(credentials.get('gateway_port', 587))
        self.auth_user = credentials.get('auth_user', '')
        self.auth_token = credentials.get('auth_token', '')

    @property
    def capabilities(self) -> Dict[str, bool]:
        return {
            'send': True,
            'attachments': True,
            'html': True,
            'plaintext': True,
            'healthcheck': True,
            'dkim_signing': True,
            'custom_domains': True,
            'rate_limiting': True,
            'oauth': False,
            'batch_send': False,
            'webhooks': False,
            'tracking': False,
        }

    @property
    def credential_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            'gateway_host': {
                'type': 'text',
                'label': 'Mail Gateway Host',
                'required': True,
                'default': 'mail-gw.spwig.com',
                'help_text': 'Spwig Mail Gateway address (auto-configured)',
                'readonly': True,
                'secret': False,
            },
            'gateway_port': {
                'type': 'number',
                'label': 'Mail Gateway Port',
                'required': True,
                'default': 587,
                'help_text': 'SMTP submission port (auto-configured)',
                'readonly': True,
                'secret': False,
            },
            'auth_user': {
                'type': 'text',
                'label': 'Account ID',
                'required': True,
                'help_text': 'Your Spwig hosted account identifier',
                'readonly': True,
                'secret': False,
            },
            'auth_token': {
                'type': 'password',
                'label': 'Authentication Token',
                'required': True,
                'secret': True,
                'help_text': 'Mail gateway authentication token',
                'readonly': True,
            },
        }

    def _create_mime_message(self, message: EmailMessage) -> MIMEMultipart:
        """Create a MIME message from EmailMessage dict."""
        msg = MIMEMultipart('alternative')

        # Set headers
        msg['Subject'] = message['subject']

        # Build From header with display name if provided
        from_email = message['from_email']
        from_name = message.get('from_name')
        if from_name:
            msg['From'] = f'{from_name} <{from_email}>'
        else:
            msg['From'] = from_email

        msg['To'] = ', '.join(message['to'])

        if message.get('cc'):
            msg['Cc'] = ', '.join(message['cc'])

        if message.get('reply_to'):
            msg['Reply-To'] = message['reply_to']

        if message.get('headers'):
            for key, value in message['headers'].items():
                # Reject protected headers and CRLF injection attempts
                if key.lower() in _PROTECTED_HEADERS:
                    continue
                if '\r' in str(value) or '\n' in str(value):
                    logger.warning("Dropping header with CRLF: %s", key)
                    continue
                if '\r' in key or '\n' in key:
                    continue
                msg[key] = value

        # Add plain text body
        if message.get('text'):
            text_part = MIMEText(message['text'], 'plain', 'utf-8')
            msg.attach(text_part)

        # Add HTML body
        if message.get('html'):
            html_part = MIMEText(message['html'], 'html', 'utf-8')
            msg.attach(html_part)

        # Add attachments
        if message.get('attachments'):
            for attachment in message['attachments']:
                self._add_attachment(msg, attachment)

        return msg

    def _add_attachment(self, msg: MIMEMultipart, attachment: Dict[str, Any]):
        """Add an attachment to the MIME message."""
        filename = attachment.get('filename', 'attachment')
        content = attachment.get('content', b'')
        content_type = attachment.get('content_type', 'application/octet-stream')

        maintype, subtype = content_type.split('/', 1) if '/' in content_type else ('application', 'octet-stream')

        part = MIMEBase(maintype, subtype)
        part.set_payload(content)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(part)

    def send(self, message: EmailMessage) -> SendResult:
        """Send an email via the Spwig Mail Gateway."""
        try:
            mime_msg = self._create_mime_message(message)

            recipients = list(message['to'])
            if message.get('cc'):
                recipients.extend(message['cc'])
            if message.get('bcc'):
                recipients.extend(message['bcc'])

            with smtplib.SMTP(self.gateway_host, self.gateway_port, timeout=self.TIMEOUT) as smtp:
                smtp.starttls(context=self._tls_context())
                smtp.login(self.auth_user, self.auth_token)
                smtp.sendmail(
                    message['from_email'],
                    recipients,
                    mime_msg.as_string(),
                )

            message_id = f"<{uuid.uuid4()}@{self.gateway_host}>"

            logger.info(
                "Email sent via Spwig Mail Gateway: %s -> %s",
                message['from_email'], message['to'],
            )

            return SendResult(
                provider_message_id=message_id,
                accepted=True,
                status='sent',
                error=None,
                details={'gateway': self.gateway_host},
            )

        except smtplib.SMTPAuthenticationError as e:
            logger.error("Gateway authentication failed: %s", e)
            raise EmailProviderAuthError(f"Gateway auth failed: {e}")

        except smtplib.SMTPSenderRefused as e:
            # Rate limit exceeded returns 451 or 452
            if e.smtp_code in (451, 452):
                logger.warning("Gateway rate limit for %s: %s", self.auth_user, e)
                raise EmailProviderRateLimitError(f"Rate limit exceeded: {e}")
            raise EmailProviderError(f"Sender refused: {e}")

        except smtplib.SMTPException as e:
            logger.error("Gateway send error: %s", e)
            raise EmailProviderError(f"Gateway send failed: {e}")

        except Exception as e:
            logger.error("Unexpected error sending via gateway: %s", e, exc_info=True)
            raise EmailProviderError(f"Unexpected error: {e}")

    def healthcheck(self) -> Dict[str, Any]:
        """Check connection to the Spwig Mail Gateway."""
        try:
            with smtplib.SMTP(self.gateway_host, self.gateway_port, timeout=5) as smtp:
                smtp.starttls(context=self._tls_context())
                smtp.login(self.auth_user, self.auth_token)
                code, msg = smtp.noop()

                if code == 250:
                    return {
                        'healthy': True,
                        'message': 'Connected to Spwig Mail Gateway',
                        'gateway': self.gateway_host,
                    }
                return {
                    'healthy': False,
                    'message': f'Gateway returned code {code}',
                    'gateway': self.gateway_host,
                }

        except smtplib.SMTPAuthenticationError:
            return {
                'healthy': False,
                'message': 'Gateway authentication failed — credentials may be invalid',
                'gateway': self.gateway_host,
            }

        except ConnectionRefusedError:
            return {
                'healthy': False,
                'message': 'Cannot connect to Spwig Mail Gateway',
                'gateway': self.gateway_host,
            }

        except Exception as e:
            return {
                'healthy': False,
                'message': f'Health check failed: {e}',
                'gateway': self.gateway_host,
            }

    def validate_credentials(self, credentials: Dict[str, Any]) -> None:
        """Validate that required credential fields are present."""
        required = ['gateway_host', 'gateway_port', 'auth_user', 'auth_token']
        for field in required:
            if not credentials.get(field):
                raise EmailProviderError(f"Missing required credential: {field}")

    def get_rate_limits(self) -> Dict[str, Any]:
        """Rate limits are enforced at the gateway level, not the provider.

        Returns a note indicating gateway-enforced limits.
        """
        return {
            'note': 'Rate limits are enforced by the Spwig Mail Gateway based on your subscription plan.',
            'enforced_at': 'gateway',
        }
