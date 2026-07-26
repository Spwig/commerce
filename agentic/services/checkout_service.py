"""
UCP checkout sessions, mapped onto the store's existing checkout machinery.

The cardinal rule (per the plan's "what NOT to build"): this holds **no** totals,
addresses, line items, shipping method, or payment state of its own. All of that
lives in `cart.CheckoutSession`, which the storefront, POS and now agents share.
This module is a thin translator + orchestrator:

- a UCP checkout session id maps 1:1 to an anonymous `Cart` via its
  `session_key` (`agentic:<id>`), and that cart's `CheckoutSession` IS the
  state;
- pricing, tax, shipping and validation all go through `CartService` /
  `CheckoutService` — never reimplemented here;
- ownership is enforced: a session created by one agent identity cannot be read
  or mutated by another.

Completion (`complete_checkout_session`) drives the shared
`PaymentOrchestrationService` — it creates no order and no payment logic of its
own, it only sequences the existing calls (place_order via the drift gate →
create intent for `amount_due` → confirm with the agent's credential). The REST
binding stays a thin HTTP shell over these functions.
"""

from __future__ import annotations

import uuid
from decimal import Decimal
from typing import Any

from agentic.services import catalog_service
from agentic.services.catalog_service import money_to_ucp

SESSION_KEY_PREFIX = "agentic:"

# UCP checkout session statuses (the subset the store can be in).
STATUS_NOT_READY = "not_ready_for_payment"
STATUS_READY = "ready_for_payment"
STATUS_COMPLETED = "completed"
STATUS_CANCELED = "canceled"


class CheckoutError(Exception):
    """A checkout operation the store refuses (bad product, add failure, …)."""

    def __init__(self, code: str, message: str, *, status: int = 400):
        self.code = code
        self.message = message
        self.http_status = status
        self.messages: list[str] = []
        super().__init__(message)

    def with_messages(self, messages) -> CheckoutError:
        """Attach human-readable validation messages (e.g. from validate_checkout)."""
        self.messages = list(messages or [])
        return self


def _session_key(checkout_id: str) -> str:
    return f"{SESSION_KEY_PREFIX}{checkout_id}"


def _agent_id(agent) -> str | None:
    return str(agent.id) if agent is not None else None


# --------------------------------------------------------------------------- #
# Loading / ownership
# --------------------------------------------------------------------------- #


def load_session(checkout_id: str, agent):
    """
    Return the `CheckoutSession` for a UCP checkout id, or None.

    Enforces ownership: a session stamped with a different agent identity is
    treated as not found (never a 403 that would confirm its existence).
    """
    from cart.models import Cart

    try:
        cart = Cart.objects.select_related("checkout_session").get(
            session_key=_session_key(checkout_id), user__isnull=True
        )
    except Cart.DoesNotExist:
        return None
    session = getattr(cart, "checkout_session", None)
    if session is None:
        return None
    # If the session is owned by a specific agent, ONLY that agent may touch it —
    # including when the caller is anonymous (allow_unverified_checkout). Skipping
    # this for agent=None would turn the checkout id into an unscoped bearer token
    # for someone else's money-moving session.
    owner = (session.metadata or {}).get("agent_identity_id")
    if owner is not None and owner != _agent_id(agent):
        return None
    return session


# --------------------------------------------------------------------------- #
# Buyer / fulfillment application (all through CheckoutService)
# --------------------------------------------------------------------------- #


def _apply_buyer(session, buyer: dict) -> None:
    """Set shipping/billing address + contact from a UCP buyer block."""
    from cart.services.checkout_service import CheckoutService

    email = buyer.get("email") or ""
    name = buyer.get("name") or ""
    shipping = buyer.get("shipping_address")
    billing = buyer.get("billing_address")

    if session.cart.requires_shipping:
        if not shipping:
            raise CheckoutError("shipping_address_required", "A shipping address is required.")
        ok, msg = CheckoutService.set_shipping_address(
            session, address_data=shipping, email=email, phone=shipping.get("phone", "")
        )
        if not ok:
            raise CheckoutError("invalid_shipping_address", msg)

    if billing:
        ok, msg = CheckoutService.set_billing_address(
            session,
            same_as_shipping=False,
            address_data=billing,
            contact_name=name,
            email=email,
        )
    elif session.cart.requires_shipping:
        ok, msg = CheckoutService.set_billing_address(
            session, same_as_shipping=True, contact_name=name, email=email
        )
    else:
        # Digital-only cart with no billing block: the shipping block, if any,
        # doubles as billing; otherwise validation will surface the gap.
        if not shipping:
            raise CheckoutError("billing_address_required", "A billing address is required.")
        ok, msg = CheckoutService.set_billing_address(
            session,
            same_as_shipping=False,
            address_data=shipping,
            contact_name=name,
            email=email,
        )
    if not ok:
        raise CheckoutError("invalid_billing_address", msg)


def _autoselect_provider(session) -> None:
    """
    Pick a gateway for the session when one is needed and not yet set.

    Agent orders are gateway-only (no customer gift-card/wallet tenders), so the
    provider is simply the store's first available connected gateway for the
    destination. If none is available the session just stays not-ready.
    """
    from cart.services.checkout_service import CheckoutService

    if session.amount_due.amount <= 0 or session.payment_provider_id:
        return
    providers = CheckoutService.get_available_payment_providers(session)
    if providers:
        CheckoutService.set_payment_method(session, str(providers[0].id))


# --------------------------------------------------------------------------- #
# Create / update
# --------------------------------------------------------------------------- #


def create_checkout_session(*, agent, line_items: list[dict], buyer: dict | None = None) -> str:
    """
    Create a UCP checkout session from line items and return its id.

    `line_items` is `[{"product_id": int, "quantity": int, "variant_id"?: int}]`.
    Only agent-visible/sellable products are accepted (via catalog_service).
    """
    from cart.services.cart_service import CartService
    from cart.services.checkout_service import CheckoutService

    if not isinstance(line_items, list) or not line_items:
        raise CheckoutError("empty_cart", "A non-empty line_items list is required.")
    if buyer is not None and not isinstance(buyer, dict):
        raise CheckoutError("invalid_buyer", "buyer must be an object.")

    checkout_id = uuid.uuid4().hex
    cart = CartService.get_or_create_cart(session_key=_session_key(checkout_id))

    for li in line_items:
        try:
            product_id = int(li["product_id"])
            quantity = int(li.get("quantity", 1))
        except (KeyError, TypeError, ValueError) as exc:
            raise CheckoutError("invalid_line_item", "Malformed line item.") from exc
        if quantity < 1:
            raise CheckoutError("invalid_quantity", "Quantity must be at least 1.")
        # get_product only returns sellable, agent-visible products — this is
        # the visibility gate: a hidden product simply doesn't exist to an agent.
        if catalog_service.get_product(product_id) is None:
            raise CheckoutError(
                "unknown_product", f"Product {product_id} is not available.", status=404
            )
        # A variant must be an ACTIVE variant of that product. CartService only
        # checks the variant belongs to the product, not that it is active, so an
        # inactive/hidden variant (never exposed by the catalog) could otherwise
        # be ordered — possibly at a stale price. Gate it here.
        variant_id = li.get("variant_id")
        if variant_id is not None:
            from catalog.models import ProductVariant

            if not ProductVariant.objects.filter(
                id=variant_id, product_id=product_id, is_active=True
            ).exists():
                raise CheckoutError(
                    "unknown_variant", f"Variant {variant_id} is not available.", status=404
                )
        ok, msg, _item = CartService.add_item(
            cart, product_id=product_id, quantity=quantity, variant_id=variant_id
        )
        if not ok:
            raise CheckoutError("add_item_failed", msg)

    session = CheckoutService.get_or_create_session(cart)
    session.metadata = {
        **(session.metadata or {}),
        "channel": "agent",
        "ucp_checkout_id": checkout_id,
        "agent_identity_id": _agent_id(agent),
    }
    session.save(update_fields=["metadata"])

    if buyer:
        _apply_buyer(session, buyer)
    session.recalculate_totals()
    session.refresh_from_db()
    _autoselect_provider(session)
    return checkout_id


def update_checkout_session(
    checkout_id: str,
    agent,
    *,
    buyer: dict | None = None,
    fulfillment_option_id: int | None = None,
):
    """Apply buyer/fulfillment changes to an existing session. Returns the model."""
    from cart.services.checkout_service import CheckoutService

    session = load_session(checkout_id, agent)
    if session is None:
        raise CheckoutError("not_found", "No such checkout session.", status=404)

    if buyer is not None and not isinstance(buyer, dict):
        raise CheckoutError("invalid_buyer", "buyer must be an object.")
    if buyer:
        _apply_buyer(session, buyer)
    if fulfillment_option_id is not None:
        try:
            method_id = int(fulfillment_option_id)
        except (TypeError, ValueError) as exc:
            raise CheckoutError("invalid_fulfillment_option", "Bad option id.") from exc
        ok, msg = CheckoutService.set_shipping_method(session, method_id)
        if not ok:
            raise CheckoutError("invalid_fulfillment_option", msg)

    session.recalculate_totals()
    session.refresh_from_db()
    _autoselect_provider(session)
    return session


# --------------------------------------------------------------------------- #
# UCP projection
# --------------------------------------------------------------------------- #


def _derive_status(session, order=None) -> tuple[str, list[str]]:
    from cart.services.checkout_service import CheckoutService

    if order is not None and getattr(order, "payment_status", "") == "paid":
        return STATUS_COMPLETED, []
    valid, errors = CheckoutService.validate_checkout(session)
    return (STATUS_READY if valid else STATUS_NOT_READY), list(errors or [])


def _line_items(session) -> list[dict]:
    # Top-level items only — bundle children are priced into their parent and
    # must not appear as separate lines (the same rule as the tax fix).
    items = session.cart.items.filter(parent_bundle__isnull=True).select_related(
        "product", "variant"
    )
    out = []
    for it in items:
        out.append(
            {
                "id": str(it.id),
                "product_id": str(it.product_id),
                "variant_id": str(it.variant_id) if it.variant_id else None,
                "title": it.product.name if it.product else "",
                "quantity": it.quantity,
                "unit_price": money_to_ucp(it.unit_price),
                "total": money_to_ucp(it.total_price),
            }
        )
    return out


def _fulfillment(session) -> dict | None:
    if not session.cart.requires_shipping:
        return None
    options = []
    for m in session.get_available_shipping_methods():
        from djmoney.money import Money

        price = Money(str(m.get("final_cost", 0)), m.get("currency", "USD"))
        options.append(
            {
                "id": str(m.get("id")),
                "label": m.get("name", ""),
                "description": m.get("description", ""),
                "price": money_to_ucp(price),
                "estimated_delivery": m.get("estimated_delivery"),
                "min_days": m.get("min_delivery_days"),
                "max_days": m.get("max_delivery_days"),
            }
        )
    return {
        "selected_option_id": (
            str(session.selected_shipping_method_id)
            if session.selected_shipping_method_id
            else None
        ),
        "options": options,
    }


def build_ucp_checkout_session(
    session, checkout_id: str, *, order=None, continue_url: str | None = None
) -> dict[str, Any]:
    """Project a store CheckoutSession (+ optional Order) into UCP shape."""
    status, messages = _derive_status(session, order)
    payment = {
        "status": "completed" if status == STATUS_COMPLETED else "requires_payment",
        # Escalation: a human can finish this in the storefront if the agent
        # cannot complete it headlessly. Best-effort; may be None.
        "continue_url": continue_url,
    }
    body: dict[str, Any] = {
        "id": checkout_id,
        "status": status,
        "currency": str(session.total_amount.currency),
        "line_items": _line_items(session),
        "buyer": _buyer_view(session),
        "fulfillment": _fulfillment(session),
        "totals": {
            "subtotal": money_to_ucp(session.subtotal),
            "shipping": money_to_ucp(session.shipping_cost),
            "tax": money_to_ucp(session.tax_amount),
            "discount": money_to_ucp(session.discount_amount),
            "total": money_to_ucp(session.total_amount),
            "amount_due": money_to_ucp(session.amount_due),
        },
        "payment": payment,
        "messages": messages,
    }
    if order is not None:
        body["order"] = {
            "id": str(order.id),
            "number": getattr(order, "order_number", "") or str(order.id),
            "status": getattr(order, "payment_status", ""),
        }
    return body


def _buyer_view(session) -> dict | None:
    email = (session.metadata or {}).get("email")
    name = (session.metadata or {}).get("contact_name")
    if not (email or name):
        return None
    return {"email": email, "name": name}


# --------------------------------------------------------------------------- #
# Completion (drives PaymentOrchestrationService — moves money)
# --------------------------------------------------------------------------- #


def find_completed_order(checkout_id: str, agent):
    """
    The Order a UCP checkout produced, if it has been paid.

    After a successful charge the CheckoutSession is deleted, so a later GET
    resolves through the Order instead (matched on the ucp_checkout_id stamped
    into its metadata, scoped to the owning agent).
    """
    from orders.models import Order

    order = (
        Order.objects.filter(channel="agent", metadata__ucp_checkout_id=checkout_id)
        .order_by("-created_at")
        .first()
    )
    if order is None:
        return None
    owner = (order.metadata or {}).get("agent_identity_id")
    if owner is not None and owner != _agent_id(agent):
        return None
    return order


def _order_view(checkout_id: str, order) -> dict[str, Any]:
    """A completed UCP checkout session projected from a paid Order."""
    return {
        "id": checkout_id,
        "status": STATUS_COMPLETED,
        "currency": str(order.total_amount.currency),
        "line_items": [
            {
                "id": str(oi.id),
                "product_id": str(oi.product_id) if oi.product_id else None,
                "title": oi.product_name,
                "quantity": oi.quantity,
                "unit_price": money_to_ucp(oi.unit_price),
                "total": money_to_ucp(oi.total_price),
            }
            for oi in order.items.all()
        ],
        "buyer": {"email": order.email, "name": order.billing_name or order.shipping_name},
        "fulfillment": None,
        "totals": {
            "subtotal": money_to_ucp(order.subtotal),
            "shipping": money_to_ucp(order.shipping_cost),
            "tax": money_to_ucp(order.tax_amount),
            "discount": money_to_ucp(order.discount_amount),
            "total": money_to_ucp(order.total_amount),
            "amount_due": money_to_ucp(order.total_amount * 0),
        },
        "payment": {"status": "completed", "continue_url": None},
        "messages": [],
        "order": {
            "id": str(order.id),
            "number": getattr(order, "order_number", "") or str(order.id),
            "status": getattr(order, "payment_status", ""),
        },
        "mandate": _mandate_view(checkout_id),
    }


def _mandate_view(checkout_id: str) -> dict | None:
    """The AP2 checkout mandate for this checkout, if one was issued."""
    from agentic.services import mandate_service

    mandate = mandate_service.mandate_for_checkout(checkout_id)
    if mandate is None:
        return None
    return {
        "format": "ap2-checkout-mandate+sd-jwt",
        "alg": mandate.alg,
        "kid": mandate.kid,
        "value": mandate.sd_jwt,
    }


def get_mandate(checkout_id: str, agent) -> dict | None:
    """
    The AP2 mandate for a completed checkout, scoped to the owning agent.

    Returns None when the checkout isn't the agent's, isn't completed, or no
    mandate was issued (e.g. the store has no AP2 key) — the binding maps that
    to 404 either way, never confirming another agent's checkout.
    """
    order = find_completed_order(checkout_id, agent)
    if order is None:
        return None
    return _mandate_view(checkout_id)


def get_checkout_view(checkout_id: str, agent, *, continue_url: str | None = None) -> dict | None:
    """Retrieve a UCP checkout session by id — live session first, else its order."""
    session = load_session(checkout_id, agent)
    if session is not None:
        return build_ucp_checkout_session(session, checkout_id, continue_url=continue_url)
    order = find_completed_order(checkout_id, agent)
    if order is not None:
        return _order_view(checkout_id, order)
    return None


def complete_checkout_session(
    checkout_id: str,
    agent,
    *,
    payment: dict,
    attested_total: dict | None = None,
    return_url: str = "",
    cancel_url: str = "",
    continue_url: str | None = None,
) -> dict[str, Any]:
    """
    Charge and place an agent's checkout.

    `payment` is the agent's payment credential passed straight to the provider.
    In production this should be a DELEGATED PAYMENT TOKEN (an agent network
    token), NOT a raw PAN — accepting raw card numbers here would pull the
    merchant's server into PCI DSS scope. Raw card data (`{"card": {...}}`) is
    the Test Gateway sandbox path only. The credential is never logged or stored
    in order/intent metadata.
    `attested_total`, if given, is the UCP money the agent asserts it is paying;
    a mismatch against the freshly-priced total refuses with `price_changed`
    (the agent must re-read and re-confirm) — this is the checkout-time price
    lock. The drift gate inside place_order remains the deeper backstop.

    Returns a UCP checkout-session body. Raises CheckoutError on refusal.
    """
    from django.core.cache import cache
    from djmoney.money import Money

    from cart.services.checkout_service import CheckoutService
    from commerce.errors import QuoteDriftError
    from payment_providers.services.payment_orchestration_service import (
        PaymentOrchestrationService,
    )

    # Serialise completion per checkout: two concurrent completes (e.g. distinct
    # Idempotency-Keys) could otherwise both pass the pre-checks and each raise a
    # gateway intent before the first deletes the session — a double charge. A
    # short cache lock lets only one completion run at a time; the loser is told
    # to retry (by which point the winner has finished and it replays the order).
    lock_key = f"agentic:complete-lock:{checkout_id}"
    if not cache.add(lock_key, "1", 120):
        raise CheckoutError(
            "completion_in_progress", "This checkout is already being completed.", status=409
        )
    try:
        session = load_session(checkout_id, agent)
        if session is None:
            # Idempotent replay after a successful completion: return the order.
            order = find_completed_order(checkout_id, agent)
            if order is not None:
                return _order_view(checkout_id, order)
            raise CheckoutError("not_found", "No such checkout session.", status=404)

        session.recalculate_totals()
        session.refresh_from_db()

        valid, errors = CheckoutService.validate_checkout(session)
        if not valid:
            raise CheckoutError(
                "not_ready", "Checkout is not ready for payment.", status=409
            ).with_messages(errors)

        # Fast-fail price check for a clear message. NOT the authoritative lock —
        # that is `expected_total` below, enforced inside the placement's row lock,
        # which closes the window between this check and the charge.
        expected_total = None
        if attested_total is not None:
            if money_to_ucp(session.total_amount) != attested_total:
                raise CheckoutError(
                    "price_changed",
                    "The price changed since it was quoted; re-read and confirm.",
                    status=409,
                )
            try:
                minor = int(attested_total["amount"])
                currency = str(attested_total["currency"])
                sub_unit = getattr(session.total_amount.currency, "sub_unit", 100) or 100
                expected_total = Money(Decimal(minor) / sub_unit, currency)
            except (KeyError, TypeError, ValueError) as exc:
                raise CheckoutError(
                    "invalid_attested_total", "Malformed attested_total.", status=400
                ) from exc

        _autoselect_provider(session)
        if not session.payment_provider_id:
            raise CheckoutError(
                "no_payment_provider", "No payment method is available.", status=409
            )

        try:
            ok, intent, msg = PaymentOrchestrationService.create_payment_intent(
                checkout_session=session,
                provider_account=session.payment_provider,
                return_url=return_url or continue_url or "",
                cancel_url=cancel_url or continue_url or "",
                metadata={"channel": "agent", "ucp_checkout_id": checkout_id},
                expected_total=expected_total,
            )
        except QuoteDriftError as exc:
            # The attested price no longer matches the freshly-priced cart.
            raise CheckoutError(
                "price_changed",
                "The price changed since it was quoted; re-read and confirm.",
                status=409,
            ) from exc
        if not ok or intent is None:
            raise CheckoutError(
                "payment_init_failed", msg or "Could not start payment.", status=502
            )

        ok, msg = PaymentOrchestrationService.confirm_payment_intent(
            intent, confirmation_data=payment
        )
    finally:
        cache.delete(lock_key)
    intent.refresh_from_db()
    order = intent.order
    if order is not None:
        order.refresh_from_db()

    if order is not None and getattr(order, "payment_status", "") == "paid":
        # Issue the AP2 checkout mandate (once) attesting what was charged. A
        # no-op when the store has no AP2 key; never blocks the paid order.
        from agentic.services import mandate_service

        if mandate_service.mandate_for_checkout(checkout_id) is None:
            mandate_service.issue_checkout_mandate(order, ucp_checkout_id=checkout_id, agent=agent)
        return _order_view(checkout_id, order)

    # Not paid yet. 3DS / redirect flows escalate to a human via continue_url.
    if getattr(intent, "status", "") in ("requires_action", "processing"):
        body = build_ucp_checkout_session(
            session, checkout_id, order=order, continue_url=intent.checkout_url or continue_url
        )
        body["status"] = STATUS_READY
        body["payment"]["status"] = "requires_action"
        return body

    raise CheckoutError("payment_failed", msg or "Payment was declined.", status=402)
