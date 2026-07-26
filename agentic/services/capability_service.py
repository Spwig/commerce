"""
Computes the UCP capability set from live install state.

The discovery profile must only ever advertise what the store can actually do —
advertising a checkout with no payment provider configured is worse than
advertising nothing, because an agent will try and fail. So every capability is
DERIVED from real state, never hardcoded on.

Each probe is conservative: if it cannot determine the answer (a query error,
say), it treats the capability as ABSENT. Under-advertising is safe; a false
positive strands an agent mid-transaction.
"""

from __future__ import annotations

import logging

from agentic.domain.versions import (
    CAPABILITY_AP2_MANDATE,
    CAPABILITY_CART,
    CAPABILITY_CATALOG_LOOKUP,
    CAPABILITY_CATALOG_SEARCH,
    CAPABILITY_CHECKOUT,
    CAPABILITY_FULFILLMENT,
    CAPABILITY_ORDER,
)

logger = logging.getLogger(__name__)

# Shipping method types that produce a cost programmatically. local_pickup is
# excluded: it is a real fulfilment option, but it cannot quote delivery to an
# agent-supplied address, which is what the fulfillment capability promises.
_QUOTABLE_METHOD_TYPES = ("flat_rate", "real_time", "table_rate")


def _has_active_payment_provider() -> bool:
    """True when at least one payment provider can actually take a payment."""
    try:
        from payment_providers.models import PaymentProviderAccount

        return PaymentProviderAccount.objects.filter(
            is_active=True, connection_status="connected"
        ).exists()
    except Exception:
        logger.warning("capability probe: payment provider check failed", exc_info=True)
        return False


def _shipping_is_quotable() -> bool:
    """
    True when shipping can be priced programmatically for an agent.

    Requires an active shipping method whose type yields a computable cost.
    A pickup-only store cannot quote delivery and must not advertise
    fulfillment — an agent would otherwise wait forever for a rate.
    """
    try:
        from cart.models import ShippingMethod

        return ShippingMethod.objects.filter(
            is_active=True, method_type__in=_QUOTABLE_METHOD_TYPES
        ).exists()
    except Exception:
        logger.warning("capability probe: shipping check failed", exc_info=True)
        return False


def _has_ap2_signing_key() -> bool:
    """
    True when an active ECDSA key exists to sign AP2 checkout mandates.

    Without a key the store cannot produce a merchant_authorization, so it must
    not advertise ap2_mandate.
    """
    try:
        from agentic.models import AgentKey

        return AgentKey.objects.filter(
            purpose=AgentKey.PURPOSE_AP2, status=AgentKey.STATUS_ACTIVE
        ).exists()
    except Exception:
        logger.warning("capability probe: AP2 key check failed", exc_info=True)
        return False


def compute_capabilities() -> list[str]:
    """
    The live UCP capability identifiers this install can honour, in a stable
    order. Callers gate on ``agentic.gating.require_agentic()`` first; this
    function assumes the feature is on.
    """
    caps: list[str] = [
        # Always available: search falls back to the ORM, lookup is a direct
        # fetch, and the cart service always exists.
        CAPABILITY_CATALOG_SEARCH,
        CAPABILITY_CATALOG_LOOKUP,
        CAPABILITY_CART,
    ]

    if _has_active_payment_provider():
        # No provider ⇒ an order cannot be paid for, so neither checkout nor
        # order tracking is honestly on offer.
        caps.append(CAPABILITY_CHECKOUT)
        caps.append(CAPABILITY_ORDER)

    if _shipping_is_quotable():
        caps.append(CAPABILITY_FULFILLMENT)

    if _has_ap2_signing_key():
        caps.append(CAPABILITY_AP2_MANDATE)

    return caps
