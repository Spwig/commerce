"""
Merchant-facing readiness: "can AI assistants actually buy from my store?"

Translates the live capability probes + install state into a single plain-
language verdict and a short list of checks, for the admin dashboard. Nothing
here gates a request — it is presentation only, and every probe fails soft so a
data error shows as "couldn't check", never as a false "ready".
"""

from __future__ import annotations

import logging

from django.utils.translation import gettext_lazy as _

from agentic.domain.versions import CAPABILITY_CHECKOUT, CAPABILITY_FULFILLMENT
from agentic.services import capability_service

logger = logging.getLogger(__name__)

# Verdicts, most-positive first.
VERDICT_READY = "ready"  # agents can discover AND buy
VERDICT_BROWSE_ONLY = "browse_only"  # discoverable, not purchasable
VERDICT_STOPPED = "stopped"  # emergency stop engaged
VERDICT_OFF = "off"  # feature disabled


def _product_counts() -> dict:
    """Sellable-to-agents vs hidden-from-agents, best effort."""
    try:
        from agentic.services.catalog_service import sellable_products
        from catalog.models import Product

        ready = sellable_products().count()
        hidden = (
            Product.objects.filter(status="published", is_deleted=False, agent_visible=False)
            .exclude(sales_channel="pos_only")
            .count()
        )
        return {"ready": ready, "hidden": hidden, "ok": True}
    except Exception:
        logger.warning("readiness: product count failed", exc_info=True)
        return {"ready": 0, "hidden": 0, "ok": False}


def _agent_stats() -> dict:
    try:
        from agentic.models import AgentEvent, AgentIdentity

        return {
            "total": AgentIdentity.objects.count(),
            "blocked": AgentIdentity.objects.filter(
                trust_state=AgentIdentity.TRUST_BLOCKED
            ).count(),
            "events": AgentEvent.objects.count(),
            "ok": True,
        }
    except Exception:
        logger.warning("readiness: agent stats failed", exc_info=True)
        return {"total": 0, "blocked": 0, "events": 0, "ok": False}


def store_readiness() -> dict:
    """
    A dashboard-ready readiness summary. Never raises.

    Shape:
        {
          "verdict": "ready|browse_only|stopped|off",
          "headline": <translated sentence>,
          "enabled": bool, "kill_switch": bool,
          "capabilities": {"checkout": bool, "fulfillment": bool},
          "checks": [{"key","label","ok","hint"}],
          "products": {"ready","hidden","ok"},
          "agents": {"total","blocked","events","ok"},
        }
    """
    from agentic.gating import agentic_status

    status = agentic_status()
    enabled = status["enabled"]

    caps = capability_service.compute_capabilities() if enabled else []
    can_checkout = CAPABILITY_CHECKOUT in caps
    can_fulfill = CAPABILITY_FULFILLMENT in caps

    if not status["is_enabled"]:
        verdict = VERDICT_OFF
        headline = _("Agentic commerce is off. AI assistants can't see your store.")
    elif status["kill_switch_engaged"]:
        verdict = VERDICT_STOPPED
        headline = _("Emergency stop is on. All AI assistant activity is halted.")
    elif can_checkout:
        verdict = VERDICT_READY
        headline = _("AI assistants can buy from your store.")
    else:
        verdict = VERDICT_BROWSE_ONLY
        headline = _("AI assistants can browse your store, but can't buy yet.")

    has_payment = capability_service._has_active_payment_provider()
    products = _product_counts()

    checks = [
        {
            "key": "payment",
            "label": _("Payment provider connected"),
            "ok": has_payment,
            "hint": _("Connect a payment provider so assistants can complete a purchase.")
            if not has_payment
            else "",
        },
        {
            "key": "fulfillment",
            "label": _("Shipping can be quoted automatically"),
            "ok": can_fulfill,
            "hint": _(
                "Add a flat-rate, table-rate or live shipping method. Pickup-only "
                "stores can still sell digital or pickup goods."
            )
            if not can_fulfill
            else "",
        },
        {
            "key": "products",
            "label": _("Products are visible to assistants"),
            "ok": products["ok"] and products["ready"] > 0,
            "hint": _("No products are available to assistants yet.")
            if products["ok"] and products["ready"] == 0
            else "",
        },
    ]

    return {
        "verdict": verdict,
        "headline": headline,
        "enabled": status["is_enabled"],
        "kill_switch": status["kill_switch_engaged"],
        "capabilities": {"checkout": can_checkout, "fulfillment": can_fulfill},
        "checks": checks,
        "products": products,
        "agents": _agent_stats(),
    }
