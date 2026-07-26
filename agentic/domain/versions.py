"""
Supported protocol versions and capability identifiers.

Kept as explicit tuples, never derived from an imported SDK, so that adding a
version is a deliberate, reviewed change rather than an incidental consequence
of a dependency bump. UCP ships roughly quarterly; a new version is added here
alongside a version-keyed adapter, not by editing a constant in passing.
"""

from __future__ import annotations

# UCP spec versions this install can speak. The first entry is the default
# advertised in the discovery profile.
SUPPORTED_UCP_VERSIONS: tuple[str, ...] = ("2026-04-08",)
DEFAULT_UCP_VERSION: str = SUPPORTED_UCP_VERSIONS[0]

# UCP capability identifiers (reverse-domain, per the spec). The discovery
# profile advertises the SUBSET of these that the live install can actually
# perform — computed from real state (payment providers configured, shipping
# quotable, keys present), never hardcoded on. This tuple is the vocabulary,
# not the advertised set.
CAPABILITY_CATALOG_SEARCH = "dev.ucp.shopping.catalog.search"
CAPABILITY_CATALOG_LOOKUP = "dev.ucp.shopping.catalog.lookup"
CAPABILITY_CART = "dev.ucp.shopping.cart"
CAPABILITY_CHECKOUT = "dev.ucp.shopping.checkout"
CAPABILITY_ORDER = "dev.ucp.shopping.order"
CAPABILITY_FULFILLMENT = "dev.ucp.shopping.fulfillment"
CAPABILITY_AP2_MANDATE = "dev.ucp.shopping.ap2_mandate"
CAPABILITY_PERMALINK = "dev.ucp.shopping.permalink"

ALL_CAPABILITY_IDS: tuple[str, ...] = (
    CAPABILITY_CATALOG_SEARCH,
    CAPABILITY_CATALOG_LOOKUP,
    CAPABILITY_CART,
    CAPABILITY_CHECKOUT,
    CAPABILITY_ORDER,
    CAPABILITY_FULFILLMENT,
    CAPABILITY_AP2_MANDATE,
    CAPABILITY_PERMALINK,
)
