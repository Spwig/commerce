"""
Non-i18n agentic API routes, mounted at /api/agentic/ (no language prefix).

Gating is per-view (require_agentic), so when the feature is off every route
below 404s.
"""

from django.urls import path

from agentic.bindings.mcp import server as mcp_server
from agentic.bindings.rest import acp_views, catalog_views, checkout_views

app_name = "agentic"

urlpatterns = [
    path("ucp/products/", catalog_views.ucp_product_search, name="ucp_product_search"),
    path(
        "ucp/products/<int:product_id>/",
        catalog_views.ucp_product_detail,
        name="ucp_product_detail",
    ),
    # UCP checkout sessions (hyphenated path, per the UCP spec).
    path(
        "ucp/checkout-sessions/",
        checkout_views.checkout_create,
        name="ucp_checkout_create",
    ),
    path(
        "ucp/checkout-sessions/<str:checkout_id>/",
        checkout_views.checkout_detail,
        name="ucp_checkout_detail",
    ),
    path(
        "ucp/checkout-sessions/<str:checkout_id>/update/",
        checkout_views.checkout_update,
        name="ucp_checkout_update",
    ),
    path(
        "ucp/checkout-sessions/<str:checkout_id>/complete/",
        checkout_views.checkout_complete,
        name="ucp_checkout_complete",
    ),
    path(
        "ucp/checkout-sessions/<str:checkout_id>/mandate/",
        checkout_views.checkout_mandate,
        name="ucp_checkout_mandate",
    ),
    # ACP product feed (underscore path per ACP convention; off by default).
    path("acp/product_feed/", acp_views.acp_product_feed, name="acp_product_feed"),
    # Storefront MCP (JSON-RPC 2.0). POST-only.
    path("mcp", mcp_server.mcp_endpoint, name="mcp_endpoint"),
]
