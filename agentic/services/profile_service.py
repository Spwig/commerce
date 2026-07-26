"""
Builds the ``/.well-known/ucp`` discovery document.

For now this advertises the protocol version, the merchant block, and the
service endpoints, with an empty capability set. Capabilities are deliberately
NOT hardcoded on — the next increment computes them from live install state
(payment providers configured, shipping quotable, signing keys present), so the
profile only ever claims what the store can actually do. Publishing an empty
set is the honest state of a store that has enabled agentic commerce but wired
nothing behind it yet.
"""

from __future__ import annotations

from typing import Any

from agentic.domain.versions import DEFAULT_UCP_VERSION


def _merchant_block(request) -> dict[str, Any]:
    """Merchant identity, preferring AgenticSettings, falling back to SiteSettings."""
    from agentic.models import AgenticSettings

    s = AgenticSettings.get_settings()

    name = s.merchant_display_name
    if not name:
        try:
            from core.models import SiteSettings

            site = SiteSettings.objects.first()
            name = (site.site_name if site and site.site_name else "") or ""
        except Exception:
            name = ""

    block = {"name": name, "url": request.build_absolute_uri("/")}
    # Only include optional policy URLs the merchant has actually set.
    for key, value in (
        ("support_url", s.support_url),
        ("terms_url", s.terms_url),
        ("privacy_url", s.privacy_url),
        ("return_policy_url", s.return_policy_url),
    ):
        if value:
            block[key] = value
    return block


def build_ucp_profile(request) -> dict[str, Any]:
    """
    Assemble the UCP discovery profile for this request.

    Callers must gate on ``agentic.gating.require_agentic()`` before calling —
    this function assumes the feature is on and does not itself check.
    """
    from agentic.identity.keys import get_jwks
    from agentic.services.capability_service import compute_capabilities

    base = request.build_absolute_uri("/").rstrip("/")

    return {
        "ucp": {
            "version": DEFAULT_UCP_VERSION,
            "capabilities": compute_capabilities(),
        },
        "merchant": _merchant_block(request),
        "services": {
            "catalog": {"endpoint": f"{base}/api/agentic/ucp"},
            "checkout": {"endpoint": f"{base}/api/agentic/ucp"},
            "mcp": {"endpoint": f"{base}/api/agentic/mcp"},
        },
        # Public signing keys, so an agent can verify the store's signatures and
        # (dual-audience) resolve the same key for a Web Bot Auth lookup.
        "keys": {"jwks": get_jwks()},
    }
