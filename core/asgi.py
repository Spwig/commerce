"""
ASGI config for core project.

Supports HTTP via Django and WebSocket via Django Channels
for the POS customer-facing display.
"""

import os

from django.core.asgi import get_asgi_application

# Force core.settings - prevent bypass via DJANGO_SETTINGS_MODULE override
os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings"

# Initialize Django ASGI application early to populate AppRegistry
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter  # noqa: E402

from pos_app.ws_routing import websocket_urlpatterns  # noqa: E402

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": URLRouter(websocket_urlpatterns),
    }
)
