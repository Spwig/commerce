"""
Storefront MCP tools — the read-only shopper surface.

Matches the shape Shopify normalised for its storefront MCP server
(search_catalog / get_product), so agents that already integrate against that
work here unchanged. Every tool projects the SAME live catalog through
`catalog_service` that the UCP REST binding uses — one source of truth, no
parallel catalog.

This is the storefront (shopper) server: unauthenticated, catalog-only. It is
NOT the admin/store-management server (product/order CRUD) — that would belong
in admin_api if it were ever built.
"""

from __future__ import annotations

from agentic.services import catalog_service


class ToolError(Exception):
    """A tool could not run (bad arguments, unknown tool)."""


TOOLS = [
    {
        "name": "search_catalog",
        "description": (
            "Search the store's catalogue for products matching a query. Returns "
            "products in UCP catalog shape (id, title, description, price_range, "
            "variants); prices are integer minor units plus an ISO 4217 currency."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Free-text search query."},
                "page": {"type": "integer", "description": "1-based page number.", "default": 1},
                "page_size": {
                    "type": "integer",
                    "description": "Results per page (max 100).",
                    "default": 20,
                },
            },
        },
    },
    {
        "name": "get_product",
        "description": "Fetch one product by its id, in UCP catalog shape.",
        "inputSchema": {
            "type": "object",
            "properties": {"id": {"type": "string", "description": "Product id."}},
            "required": ["id"],
        },
    },
]

TOOL_NAMES = {t["name"] for t in TOOLS}


def _int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def call_tool(name: str, arguments: dict, request=None) -> dict:
    """Run a storefront tool and return its (JSON-serialisable) result."""
    arguments = arguments or {}

    if name == "search_catalog":
        query = str(arguments.get("query", "")).strip()
        page = _int(arguments.get("page"), 1)
        page_size = _int(arguments.get("page_size"), 20)
        products, total = catalog_service.search(query, page=page, page_size=page_size)
        return {
            "products": [catalog_service.to_ucp_product(p, request) for p in products],
            "page": max(1, page),
            "page_size": max(1, min(page_size, 100)),
            "total": total,
        }

    if name == "get_product":
        raw = arguments.get("id")
        pid = _int(raw, None)
        product = catalog_service.get_product(pid) if pid is not None else None
        if product is None:
            raise ToolError(f"No such product: {raw!r}")
        return catalog_service.to_ucp_product(product, request)

    raise ToolError(f"Unknown tool: {name!r}")
