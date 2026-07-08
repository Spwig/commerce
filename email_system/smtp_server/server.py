"""
Built-in SMTP Server using aiosmtpd

Provides a localhost-only SMTP server that accepts emails from the Django app
and forwards them to Postfix for delivery. All outgoing emails are signed with DKIM.
"""
import asyncio
import logging
import smtplib
from typing import Optional
from email.message import Message
from email.parser import BytesParser
from email.policy import default

from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP as SMTPProtocol, Envelope

from django.conf import settings
from django.core.cache import cache

from email_system.smtp_server.dkim_handler import DKIMHandler
from email_system.models import EmailAccount

logger = logging.getLogger(__name__)


class BuiltinSMTPHandler:
    """
    Message handler for aiosmtpd that processes emails from the Django app.

    This handler:
    1. Receives emails from localhost (Django app)
    2. Signs them with DKIM
    3. Forwards them to Postfix for delivery
    """

    def __init__(self, postfix_host: str = '127.0.0.1', postfix_port: int = 25, dev_mode: bool = False):
        """
        Initialize the SMTP handler.

        Args:
            postfix_host: Postfix server hostname (default: localhost)
            postfix_port: Postfix server port (default: 25)
            dev_mode: If True, log emails instead of sending via Postfix (for development)
        """
        self.postfix_host = postfix_host
        self.postfix_port = postfix_port
        self.dev_mode = dev_mode
        self.stats = {
            'received': 0,
            'signed': 0,
            'forwarded': 0,
            'failed': 0
        }

    async def handle_DATA(self, server: SMTPProtocol, session, envelope: Envelope):
        """
        Handle the DATA command - process the email message.

        Args:
            server: SMTP server instance
            session: SMTP session
            envelope: Email envelope with sender, recipients, content

        Returns:
            SMTP response code
        """
        self.stats['received'] += 1

        try:
            # Parse the message
            message_bytes = envelope.content
            parser = BytesParser(policy=default)
            message = parser.parsebytes(message_bytes)

            # Extract domain from sender
            mail_from = envelope.mail_from
            if '@' in mail_from:
                domain = mail_from.split('@')[1].lower()
            else:
                logger.warning(f"Invalid sender address: {mail_from}")
                return '550 Invalid sender address'

            # Get the default EmailAccount for built-in server
            account = self._get_builtin_account()

            # Sign with DKIM
            dkim_handler = DKIMHandler(domain=domain)
            signed_message = dkim_handler.sign_message(message_bytes, account)

            if signed_message != message_bytes:
                self.stats['signed'] += 1
                logger.debug(f"Message signed with DKIM for domain: {domain}")

            # Forward to Postfix or log in dev mode
            if self.dev_mode:
                # Development mode: just log the email
                logger.info(f"[DEV MODE] Email processed: {mail_from} -> {envelope.rcpt_tos}")
                logger.debug(f"[DEV MODE] Message size: {len(signed_message)} bytes")
                self.stats['forwarded'] += 1
                return '250 Message accepted for delivery (dev mode)'
            else:
                # Production mode: forward to Postfix
                success = await self._forward_to_postfix(
                    envelope.mail_from,
                    envelope.rcpt_tos,
                    signed_message
                )

                if success:
                    self.stats['forwarded'] += 1
                    logger.info(f"Email forwarded to Postfix: {mail_from} -> {envelope.rcpt_tos}")
                    return '250 Message accepted for delivery'
                else:
                    self.stats['failed'] += 1
                    return '451 Temporary failure forwarding to Postfix'

        except Exception as e:
            self.stats['failed'] += 1
            logger.error(f"Error handling email: {e}", exc_info=True)
            return '451 Internal server error'

    async def _forward_to_postfix(self, mail_from: str, rcpt_tos: list, message: bytes) -> bool:
        """
        Forward the signed message to Postfix for delivery.

        Args:
            mail_from: Sender email address
            rcpt_tos: List of recipient email addresses
            message: Signed message bytes

        Returns:
            True if forwarded successfully, False otherwise
        """
        loop = asyncio.get_event_loop()

        try:
            # Run SMTP sending in thread pool (smtplib is synchronous)
            await loop.run_in_executor(
                None,
                self._send_via_smtp,
                mail_from,
                rcpt_tos,
                message
            )
            return True

        except Exception as e:
            logger.error(f"Failed to forward to Postfix: {e}", exc_info=True)
            return False

    def _send_via_smtp(self, mail_from: str, rcpt_tos: list, message: bytes):
        """
        Send message via SMTP (synchronous, runs in thread pool).

        Args:
            mail_from: Sender email address
            rcpt_tos: List of recipient email addresses
            message: Message bytes
        """
        with smtplib.SMTP(self.postfix_host, self.postfix_port, timeout=30) as smtp:
            smtp.sendmail(mail_from, rcpt_tos, message)

    def _get_builtin_account(self) -> Optional[EmailAccount]:
        """
        Get the default built-in EmailAccount.

        Returns:
            EmailAccount instance or None
        """
        # Cache the account lookup
        cache_key = 'builtin_smtp_account'
        account = cache.get(cache_key)

        if not account:
            try:
                account = EmailAccount.objects.filter(
                    provider_key='builtin_smtp',
                    is_active=True
                ).first()

                if account:
                    cache.set(cache_key, account, 300)  # Cache for 5 minutes

            except Exception as e:
                logger.error(f"Failed to get built-in account: {e}")

        return account

    def get_stats(self) -> dict:
        """Get server statistics."""
        return self.stats.copy()


class SMTPServerManager:
    """
    Manages the lifecycle of the built-in SMTP server.

    This server listens on localhost only and accepts emails from the Django app.
    """

    def __init__(self, host: str = '127.0.0.1', port: int = 2525,
                 postfix_host: str = '127.0.0.1', postfix_port: int = 25,
                 dev_mode: bool = False):
        """
        Initialize the SMTP server manager.

        Args:
            host: Listen hostname (default: 127.0.0.1 - localhost only)
            port: Listen port (default: 2525 - non-privileged port)
            postfix_host: Postfix relay host (default: 127.0.0.1)
            postfix_port: Postfix relay port (default: 25)
            dev_mode: Development mode - log emails instead of sending via Postfix
        """
        self.host = host
        self.port = port
        self.postfix_host = postfix_host
        self.postfix_port = postfix_port
        self.dev_mode = dev_mode

        self.handler = BuiltinSMTPHandler(postfix_host, postfix_port, dev_mode=dev_mode)
        self.controller: Optional[Controller] = None

    def start(self):
        """
        Start the SMTP server.

        Note: This blocks the current thread. Run in a separate process/thread
        or use start_async() in an async context.
        """
        if self.controller:
            logger.warning("SMTP server is already running")
            return

        logger.info(f"Starting built-in SMTP server on {self.host}:{self.port}")
        logger.info(f"Relay configured to Postfix at {self.postfix_host}:{self.postfix_port}")

        self.controller = Controller(
            self.handler,
            hostname=self.host,
            port=self.port,
            ready_timeout=30
        )

        try:
            self.controller.start()
            logger.info(f"SMTP server started successfully on {self.host}:{self.port}")

        except Exception as e:
            logger.error(f"Failed to start SMTP server: {e}", exc_info=True)
            raise

    def stop(self):
        """Stop the SMTP server."""
        if not self.controller:
            logger.warning("SMTP server is not running")
            return

        logger.info("Stopping built-in SMTP server...")

        try:
            self.controller.stop()
            self.controller = None
            logger.info("SMTP server stopped successfully")

        except Exception as e:
            logger.error(f"Error stopping SMTP server: {e}", exc_info=True)

    def is_running(self) -> bool:
        """Check if the server is running."""
        return self.controller is not None

    def get_stats(self) -> dict:
        """Get server statistics."""
        return self.handler.get_stats()

    def health_check(self) -> bool:
        """
        Perform a health check on the SMTP server.

        Returns:
            True if server is healthy, False otherwise
        """
        if not self.is_running():
            return False

        try:
            # Try to connect to the server
            with smtplib.SMTP(self.host, self.port, timeout=5) as smtp:
                code, _ = smtp.noop()
                return code == 250

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
