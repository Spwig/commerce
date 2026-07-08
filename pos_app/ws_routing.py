"""
WebSocket URL routing for POS customer-facing display.
"""

from django.urls import re_path
from pos_app.consumers import DisplayConsumer

websocket_urlpatterns = [
    re_path(r'ws/pos/display/(?P<terminal_uuid>[0-9a-f\-]+)/$', DisplayConsumer.as_asgi()),
]
