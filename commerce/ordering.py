"""
Order placement with a quote-drift gate.

`OrderPlacementService.place_order()` is a thin facade over
`CheckoutService.create_order`. It creates no order itself -- order creation
stays in the single storefront site -- and adds exactly one thing of substance:
a **drift gate** that re-prices the cart immediately before placement and
compares the fresh figure against the total stored on the session.

Why this matters: the stored total was written by `recalculate_totals()`. If a
cart mutation ever failed to refresh it (the class of bug fixed in
`be0a5f815`), or a future edit makes the stored and computed paths disagree,
the gate turns "silently charge the wrong amount" into "refuse, or at least
log". Because it runs on every placement, it is a permanent, continuous check
that the live pricing path and `commerce.quote()` agree -- on real traffic,
across every currency/bundle/tender combination that actually occurs.

Two knobs, deliberately asymmetric:

- **Stored-vs-fresh drift** is governed by `settings.SPWIG_ENFORCE_QUOTE_DRIFT`.
  Default (warn-only) logs and proceeds; enforce mode refuses with a soft
  `ok=False` the customer can recover from by re-reviewing.
- **An explicit `expected_total`** asserted by the caller ALWAYS raises
  `QuoteDriftError` on mismatch, regardless of the flag. A caller that states a
  price and gets a different one has a broken contract, not a UX event. The web
  checkout does not pass `expected_total`; an agent attesting a price will.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

from django.conf import settings

from commerce.dto import QuoteRequest, QuoteResult
from commerce.errors import QuoteDriftError
from commerce.pricing import PricingService

if TYPE_CHECKING:  # pragma: no cover - typing only
    from djmoney.money import Money

    from cart.models import CheckoutSession
    from orders.models import Order

logger = logging.getLogger(__name__)

# Customer-facing refusal copy (only ever returned in enforce mode, or to a
# caller that asserted a price we could not verify).
_CART_CHANGED_MESSAGE = "Your cart changed since it was last priced. Please review and try again."
_UNVERIFIABLE_MESSAGE = "Could not verify the order price. Please try again."


@dataclass(frozen=True, slots=True)
class PlacementRequest:
    session: CheckoutSession
    expected_total: Money | None = None
    channel: str = "web"
    clear_session: bool = True


@dataclass(frozen=True, slots=True)
class PlacementResult:
    ok: bool
    order: Order | None
    message: str
    quote: QuoteResult | None


def _quote_for(session: CheckoutSession) -> QuoteResult:
    """Fresh price for the session's cart, using its address and method."""
    return PricingService.quote(
        QuoteRequest(
            cart=session.cart,
            shipping_address=session.shipping_address or session.shipping_address_data,
            shipping_method=session.selected_shipping_method,
        )
    )


class OrderPlacementService:
    """Places an order from a checkout session, behind a drift gate."""

    @staticmethod
    def place_order(request: PlacementRequest) -> PlacementResult:
        """
        Place an order from a checkout session.

        Delegates order creation to `CheckoutService.create_order`; adds a
        drift gate in front of it. Creates nothing itself.
        """
        # Import here: commerce/ must not import Django models at module load,
        # and this keeps the dependency direction one-way (commerce -> cart),
        # never imported back by cart at import time.
        from cart.services.checkout_service import CheckoutService

        session = request.session
        stored_total = session.total_amount
        enforce = getattr(settings, "SPWIG_ENFORCE_QUOTE_DRIFT", False)

        # The verification quote is an OBSERVER in warn-only mode. It must never
        # be able to break a checkout that would otherwise place — pricing a
        # cart happens to touch shipping/tax services, and a failure there (bad
        # data, a provider hiccup) must not become a lost order while we are
        # only watching. So a quote failure is swallowed and logged in
        # warn-only mode, and the order proceeds exactly as create_order would
        # have. In enforce mode we cannot proceed unverified, so we refuse.
        fresh: QuoteResult | None = None
        try:
            fresh = _quote_for(session)
        except Exception:
            logger.exception(
                "place_order: could not compute a verification quote for "
                "checkout session %s (cart %s); enforce=%s",
                session.pk,
                session.cart_id,
                enforce,
            )

        if fresh is None:
            # No quote to check against. Refuse only when someone is relying on
            # it: enforce mode, or a caller that asserted a price we now cannot
            # verify (an agent). Otherwise the web path places as before.
            if enforce or request.expected_total is not None:
                return PlacementResult(
                    ok=False,
                    order=None,
                    message=_UNVERIFIABLE_MESSAGE,
                    quote=None,
                )
        else:
            # 1) Explicit caller assertion: always authoritative, always raises.
            if request.expected_total is not None and request.expected_total != fresh.total_amount:
                raise QuoteDriftError(expected=request.expected_total, actual=fresh.total_amount)

            # 2) Stored-vs-fresh drift: the continuous self-check.
            if fresh.total_amount != stored_total:
                logger.warning(
                    "Quote drift on checkout session %s (cart %s): stored total %s, "
                    "fresh quote %s, fingerprint %s, enforce=%s",
                    session.pk,
                    session.cart_id,
                    stored_total,
                    fresh.total_amount,
                    fresh.inputs_fingerprint,
                    enforce,
                )
                if enforce:
                    return PlacementResult(
                        ok=False,
                        order=None,
                        message=_CART_CHANGED_MESSAGE,
                        quote=fresh,
                    )
                # warn-only: fall through and place. The stored total is what
                # create_order copies onto the Order, exactly as today.

        success, message, order = CheckoutService.create_order(
            session, clear_session=request.clear_session, channel=request.channel
        )
        return PlacementResult(ok=success, order=order, message=message, quote=fresh)
