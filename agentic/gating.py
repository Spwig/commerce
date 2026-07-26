"""
The one place anything asks "is agentic commerce on?".

Nothing outside this module reads ``AgenticSettings.is_enabled`` or checks the
kill switch directly. That keeps the on/off logic in a single spot: the day the
gate grows a Redis-backed fast path, an edition check, or a hosted-service seam,
every call site inherits it without changing (the lesson of pos_app/license.py,
whose gates all collapsed into a few functions when POS was de-monetised).

Two hard rules:

- **Off means 404, not 403.** A 403 on ``/.well-known/ucp`` tells a crawler the
  endpoint exists and the merchant is holding out; a 404 says "not an agentic
  merchant", which is the truth. ``require_agentic()`` raises ``Http404``.
- The master switch and the emergency stop are read together: engaged kill
  switch ⇒ off, regardless of ``is_enabled``.
"""

from __future__ import annotations

from django.http import Http404


def _settings():
    from agentic.models import AgenticSettings

    return AgenticSettings.get_settings()


def agentic_is_enabled() -> bool:
    """True only when the master switch is on and the emergency stop is clear."""
    s = _settings()
    return bool(s.is_enabled and not s.kill_switch_engaged)


def protocol_is_enabled(protocol: str) -> bool:
    """
    Whether a specific protocol surface is live.

    ``protocol`` is one of ``"ucp"``, ``"acp"``, ``"mcp"``. Always False when
    agentic commerce is off overall.
    """
    if not agentic_is_enabled():
        return False
    s = _settings()
    return {
        "ucp": s.ucp_enabled,
        "acp": s.acp_enabled,
        "mcp": s.mcp_storefront_enabled,
    }.get(protocol, False)


def require_agentic() -> None:
    """Raise Http404 unless agentic commerce is enabled. Off is invisible."""
    if not agentic_is_enabled():
        raise Http404("Agentic commerce is not enabled on this store.")


def require_protocol(protocol: str) -> None:
    """Raise Http404 unless the given protocol surface is enabled."""
    if not protocol_is_enabled(protocol):
        raise Http404(f"The {protocol} surface is not enabled on this store.")


def agentic_status() -> dict:
    """A small status dict for an admin dashboard card. Never raises."""
    s = _settings()
    return {
        "enabled": bool(s.is_enabled and not s.kill_switch_engaged),
        "is_enabled": s.is_enabled,
        "kill_switch_engaged": s.kill_switch_engaged,
        "protocols": {
            "ucp": s.ucp_enabled,
            "acp": s.acp_enabled,
            "mcp": s.mcp_storefront_enabled,
        },
    }
