"""
ACP (Agentic Commerce Protocol) catalog projection.

ACP is a PUSH/feed protocol; by the time of writing its product feed schema has
structurally converged with UCP's — the same nested ``Product → variants[]``,
the same ``availability {available, status}``, the same ``barcodes[{type,
value}]``. So this is a genuinely cheap projection: it reuses the UCP catalog
projection (`agentic.services.catalog_service`) and only reshapes the envelope
and adds barcodes. There is NO second catalog and no second pricing path.

Two ACP gotchas the plan flagged, honoured here:

- ACP paths use **underscores** where UCP uses hyphens — the feed lives at
  ``/api/agentic/acp/product_feed`` (not ``product-feed``).
- ``agenticcommerce.dev`` is stale (it stopped updating 2026-01-30); the ACP
  GitHub repo is the authoritative schema source. Keep this projection aligned
  to the repo, not the dead docs site.

ACP is **off by default** (`AgenticSettings.acp_enabled = False`). The plan's
research: ACP lost its flagship surface (OpenAI retired Instant Checkout), so it
ships as an opt-in projection for the few merchants who still need it, not a
default.
"""

from __future__ import annotations

from typing import Any

from agentic.services import catalog_service

# Barcode identifier types ACP recognises, mapped to the Product fields that may
# hold them. Only non-empty values are emitted.
_BARCODE_FIELDS = (("gtin", "gtin"), ("ean", "ean"), ("upc", "upc"), ("mpn", "mpn"))


def _barcodes(product) -> list[dict]:
    out = []
    for barcode_type, field in _BARCODE_FIELDS:
        value = (getattr(product, field, "") or "").strip()
        if value:
            out.append({"type": barcode_type, "value": value})
    return out


def to_acp_product(product, request=None) -> dict[str, Any]:
    """
    Project one Product into the ACP feed Product shape.

    Reuses the UCP projection for the heavy lifting (variants, availability,
    price range) since the two have converged, then adds ACP feed conventions:
    a ``link`` (feed term for the product URL) and ``barcodes[]``.
    """
    ucp = catalog_service.to_ucp_product(product, request)
    doc: dict[str, Any] = {
        "id": ucp["id"],
        "title": ucp["title"],
        "description": ucp["description"],
        "condition": ucp["condition"],
        "availability": ucp["availability"],
        "price_range": ucp["price_range"],
        "variants": ucp["variants"],
        "barcodes": _barcodes(product),
    }
    if ucp.get("url"):
        doc["link"] = ucp["url"]  # feed convention: 'link', not 'url'
    if ucp.get("brand"):
        doc["brand"] = ucp["brand"]
    return doc


def product_feed(*, page: int = 1, page_size: int = 100, request=None) -> dict[str, Any]:
    """
    A page of the ACP product feed over the agent-visible catalogue.

    Paginated (a full push feed is bounded here so one request can't scan the
    whole catalogue at once); ``next_page`` is present while more remain.
    """
    page = max(1, page)
    page_size = max(1, min(page_size, 250))
    qs = catalog_service.sellable_products().order_by("id")
    total = qs.count()
    start = (page - 1) * page_size
    products = list(qs[start : start + page_size])

    body: dict[str, Any] = {
        "version": "acp-feed-1",
        "products": [to_acp_product(p, request) for p in products],
        "page": page,
        "page_size": page_size,
        "total": total,
    }
    if start + page_size < total:
        body["next_page"] = page + 1
    return body
