"""
POS Customer Display WebSocket consumer.

Message relay: the POS terminal sends display updates,
connected customer-facing displays receive them in real time.

Security: the two ends of the relay authenticate differently and
neither may act until it has.

- The POS terminal (the sender) authenticates with its staff access
  token — the same MobileAuthToken it already uses for the POS API.
  Only a token-authenticated terminal may relay messages.
- The customer display (the receiver) authenticates with a short-lived
  pairing code. Only a code-authenticated display receives messages.

Knowing the terminal UUID alone is not enough to inject or observe
messages.
"""

import logging
import uuid

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

logger = logging.getLogger(__name__)


class DisplayConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer for POS customer-facing displays.

    Both the POS terminal and the display connect to the same room
    (identified by terminal UUID). The terminal sends messages
    (CART_UPDATE, PAYMENT_PENDING, SALE_COMPLETE, IDLE) and
    display clients receive them.

    Security:
    - The terminal must send AUTHENTICATE_TERMINAL with a valid staff
      access token before it may relay messages.
    - The display must send AUTHENTICATE with a valid pairing code
      before it may receive messages.
    - A connection that only knows the terminal UUID can neither inject
      nor observe relayed messages.
    """

    async def connect(self):
        self.terminal_uuid = self.scope["url_route"]["kwargs"]["terminal_uuid"]
        self.group_name = f"pos_display_{self.terminal_uuid}"
        self.is_terminal = False  # Set once a valid staff token is presented (may relay)
        self.is_display = False  # Set once a valid pairing code is presented (may receive)

        # Validate that the terminal exists
        if not await self._terminal_exists(self.terminal_uuid):
            await self.close(code=4004)
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await self.send_json({"type": "CONNECTED", "terminal": self.terminal_uuid})
        logger.info("Display WebSocket connected for terminal %s", self.terminal_uuid)

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            logger.info("Display WebSocket disconnected for terminal %s", self.terminal_uuid)

    async def receive_json(self, content, **kwargs):
        """Handle incoming messages.

        - AUTHENTICATE_TERMINAL: terminal sends its staff access token for
          verification, gaining the right to relay messages.
        - AUTHENTICATE: display sends a pairing code for verification,
          gaining the right to receive messages.
        - Other messages: relayed to displays, but only from a connection
          that has authenticated as the terminal.
        """
        if not isinstance(content, dict):
            logger.warning(
                "Display WebSocket received non-object message for terminal %s",
                self.terminal_uuid,
            )
            await self.close(code=4003)
            return

        msg_type = content.get("type")

        # Terminal (sender) authenticates with its staff access token.
        if msg_type == "AUTHENTICATE_TERMINAL":
            token = content.get("token", "")
            if await self._validate_terminal_token(token):
                self.is_terminal = True
                await self.send_json({"type": "TERMINAL_AUTHENTICATED"})
                logger.info("Terminal authenticated for terminal %s", self.terminal_uuid)
            else:
                await self.send_json({"type": "AUTH_FAILED"})
                logger.warning(
                    "Terminal auth failed for terminal %s (invalid token)", self.terminal_uuid
                )
            return

        # Display (receiver) authenticates with a short-lived pairing code.
        if msg_type == "AUTHENTICATE":
            code = content.get("code", "")
            if await self._validate_pairing_code(code):
                self.is_display = True
                await self.send_json({"type": "AUTHENTICATED"})
                logger.info("Display authenticated for terminal %s", self.terminal_uuid)
            else:
                await self.send_json({"type": "AUTH_FAILED"})
                logger.warning(
                    "Display auth failed for terminal %s (invalid code)", self.terminal_uuid
                )
            return

        # Only a token-authenticated terminal may relay messages to displays.
        # This prevents a client that merely knows the terminal UUID (or that
        # holds only a display pairing code) from injecting spoofed
        # CART_UPDATE/PAYMENT_PENDING/SALE_COMPLETE messages.
        if not self.is_terminal:
            logger.warning(
                "Dropping relay from unauthenticated connection for terminal %s",
                self.terminal_uuid,
            )
            return

        # Relay the message to the group (from terminal to displays)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "display.message",
                "message": content,
            },
        )

    async def display_message(self, event):
        """Channel layer handler: send the relayed message to WebSocket client.

        Only send to authenticated display clients.
        """
        if self.is_display:
            await self.send_json(event["message"])

    @database_sync_to_async
    def _terminal_exists(self, terminal_uuid):
        from pos_app.models import POSTerminal

        try:
            parsed_uuid = uuid.UUID(str(terminal_uuid))
        except ValueError:
            return False

        return POSTerminal.objects.filter(uuid=parsed_uuid, is_active=True).exists()

    @database_sync_to_async
    def _validate_terminal_token(self, token):
        """Validate a POS terminal's staff access token.

        Returns True when the token is a live (unexpired, unrevoked) access
        token belonging to an active staff user — i.e. a legitimate POS
        terminal — and False otherwise.
        """
        if not token:
            return False

        from admin_api.models import MobileAuthToken

        auth_token = (
            MobileAuthToken.objects.select_related("user")
            .filter(token=token, token_type="access")
            .first()
        )
        if auth_token is None or not auth_token.is_valid:
            return False

        user = auth_token.user
        return bool(user.is_active and user.is_staff)

    @database_sync_to_async
    def _validate_pairing_code(self, code):
        """Validate a pairing code. Returns True if valid, marks as used."""
        from pos_app.models import DisplayPairingCode

        return DisplayPairingCode.validate_code(self.terminal_uuid, code)
