"""
POS Customer Display WebSocket consumer.

Simple message relay: the POS terminal sends display updates,
connected customer-facing displays receive them in real time.

Security: Display clients must authenticate with a short-lived
pairing code before receiving messages.
"""

import logging

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
    - Terminal sends messages directly (already authenticated via API)
    - Display clients must first send AUTHENTICATE with a valid pairing code
    - Only authenticated displays receive relayed messages
    """

    async def connect(self):
        self.terminal_uuid = self.scope["url_route"]["kwargs"]["terminal_uuid"]
        self.group_name = f"pos_display_{self.terminal_uuid}"
        self.authenticated = False  # Display clients start unauthenticated

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

        - AUTHENTICATE: Display client sends pairing code for verification
        - Other messages: Relayed to all authenticated displays (from terminal)
        """
        msg_type = content.get("type")

        # Handle authentication from display clients
        if msg_type == "AUTHENTICATE":
            code = content.get("code", "")
            if await self._validate_pairing_code(code):
                self.authenticated = True
                await self.send_json({"type": "AUTHENTICATED"})
                logger.info("Display authenticated for terminal %s", self.terminal_uuid)
            else:
                await self.send_json({"type": "AUTH_FAILED"})
                logger.warning(
                    "Display auth failed for terminal %s (invalid code)", self.terminal_uuid
                )
            return

        # All other messages are relayed to the group (from terminal to displays)
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
        if self.authenticated:
            await self.send_json(event["message"])

    @database_sync_to_async
    def _terminal_exists(self, uuid):
        from pos_app.models import POSTerminal

        return POSTerminal.objects.filter(uuid=uuid, is_active=True).exists()

    @database_sync_to_async
    def _validate_pairing_code(self, code):
        """Validate a pairing code. Returns True if valid, marks as used."""
        from pos_app.models import DisplayPairingCode

        return DisplayPairingCode.validate_code(self.terminal_uuid, code)
