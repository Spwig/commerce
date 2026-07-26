"""
Cart pricing.

`PricingService.quote()` answers "what would this cost?" without committing
the answer. Until it existed, `CheckoutSession.recalculate_totals()` was the
only way to compute a total and it *wrote* -- so nothing could cheaply assert
that a stored total still matched a freshly computed one, and every caller had
to sequence its mutations correctly or silently charge a stale figure.

The body below is a deliberate line-for-line transcription of
`recalculate_totals` (cart/models.py) as it stood when this module was
introduced: same calls, in the same order, with the same rounding. Assignments
to `self` became locals; nothing else changed. Anything here that looks like a
bug is preserved on purpose, so that the equivalence test comparing the two
paths can stay strict. Fix such things in their own commit, with their own
test, never inside a transcription.
"""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from django.utils import timezone
from djmoney.money import Money

from commerce.dto import (
    QuoteLine,
    QuoteRequest,
    QuoteResult,
    ShippingQuote,
    TaxComponent,
)

if TYPE_CHECKING:  # pragma: no cover - typing only
    from cart.models import Cart


def _address_parts(addr: Any) -> tuple[str, str, str, str]:
    """
    Pull (country, state, city, postal_code) from an Address or a plain dict.

    Checkout holds the address in a JSONField until the order is placed, so
    both shapes are live on the pricing path. Mirrors the duality handled in
    `CheckoutSession._calculate_tax`.
    """
    if hasattr(addr, "country"):
        return (
            addr.country,
            getattr(addr, "state", "") or "",
            getattr(addr, "city", "") or "",
            getattr(addr, "postal_code", "") or "",
        )
    return (
        addr.get("country", ""),
        addr.get("state", ""),
        addr.get("city", ""),
        addr.get("postal_code", ""),
    )


def _calculate_tax(cart: Cart, addr: Any, shipping_cost: Money) -> tuple[Decimal, dict]:
    """
    Tax for this cart shipped to this address.

    Transcribed from `CheckoutSession._calculate_tax`. Bundle components are
    excluded for the same reason every money aggregation on Cart excludes
    them: the customer is billed the bundle price, not the sum of its parts.
    """
    if not addr:
        return Decimal("0.00"), {}

    from cart.services.tax_service import TaxService

    items = []
    for item in cart.items.filter(parent_bundle__isnull=True).select_related("product", "variant"):
        items.append((item.product, item.quantity, item.total_price.amount))

    if not items:
        return Decimal("0.00"), {}

    country, state, city, postal_code = _address_parts(addr)

    total_tax, breakdown = TaxService.calculate_tax(
        items=items,
        shipping_cost=shipping_cost.amount if shipping_cost else Decimal("0.00"),
        country=country,
        state=state,
        city=city,
        postal_code=postal_code,
    )
    return total_tax, {"taxes": breakdown}


def _build_lines(cart: Cart, currency: str) -> tuple[QuoteLine, ...]:
    """Per-line detail. Derived only -- contributes nothing to the totals."""
    lines = []
    for item in cart.items.all().select_related("product", "variant"):
        is_child = item.parent_bundle_id is not None
        lines.append(
            QuoteLine(
                cart_item_id=item.pk,
                product_id=item.product_id,
                variant_id=item.variant_id,
                sku=(item.variant.sku if item.variant_id else item.product.sku) or "",
                name=item.product.name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                line_total=item.total_price,
                is_bundle_child=is_child,
                counts_toward_subtotal=not is_child,
            )
        )
    return tuple(lines)


def _build_tax_components(breakdown: dict, currency: str) -> tuple[TaxComponent, ...]:
    """Reshape a TaxService breakdown into typed components."""
    entries = breakdown.get("taxes") or []
    components = []
    for entry in entries:
        components.append(
            TaxComponent(
                tax_rate_id=entry.get("tax_rate_id"),
                name=entry.get("name", ""),
                rate=Decimal(str(entry.get("rate", "0"))),
                amount=Money(Decimal(str(entry.get("amount", "0"))), currency),
                compound=bool(entry.get("compound", False)),
                jurisdiction=entry.get("jurisdiction", ""),
                tax_type=entry.get("tax_type", ""),
            )
        )
    return tuple(components)


def _fingerprint(
    cart: Cart, lines: tuple[QuoteLine, ...], addr: Any, method_id: int | None, currency: str
) -> str:
    """
    A stable hash of everything that went into the price.

    Answers "did the cart change since we quoted?" without diffing. Justified
    on its own merits -- the drift gate needs it -- and it happens to be the
    shape a signed cart credential wants later.
    """
    country, state, city, postal_code = _address_parts(addr) if addr else ("", "", "", "")
    payload = {
        "cart_id": cart.pk,
        "currency": currency,
        "method_id": method_id,
        "address": [country, state, city, postal_code],
        "lines": [
            [ln.cart_item_id, ln.variant_id, ln.quantity, str(ln.unit_price.amount)]
            for ln in sorted(lines, key=lambda x: x.cart_item_id)
        ],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


class PricingService:
    """Prices a cart. Performs no writes."""

    @staticmethod
    def quote(request: QuoteRequest) -> QuoteResult:
        """
        Price a cart.

        Pure: issues no INSERT or UPDATE. Same inputs give the same outputs, so
        it is safe to call in a loop, from an agent, or as a pre-charge
        verification. A persisted `CheckoutSession` is a *cache* of this
        result, never the source of truth.
        """
        cart = request.cart
        currency = cart.effective_currency
        zero = Money(0, currency)

        subtotal = cart.subtotal
        discount_amount = cart.voucher_discount_amount

        address = request.shipping_address
        shipping_method = request.shipping_method

        shipping: ShippingQuote | None = None
        if address and shipping_method:
            from shipping.services import ShippingRuleService

            user = request.user
            if user is None and cart.user_id:
                user = cart.user

            calculation = ShippingRuleService.calculate_shipping_for_cart(
                cart=cart,
                shipping_method=shipping_method,
                address=address,
                user=user,
            )
            shipping_cost = calculation["final_cost"]
            shipping = ShippingQuote(
                method_id=shipping_method.pk,
                method_name=str(getattr(shipping_method, "name", "")),
                base_cost=calculation.get("base_cost", shipping_cost),
                final_cost=shipping_cost,
                total_discount=calculation.get("total_discount", zero),
                total_surcharge=calculation.get("total_surcharge", zero),
                rules_applied=tuple(calculation.get("rules_applied", ()) or ()),
            )
        else:
            shipping_cost = zero

        if address:
            tax_decimal, tax_breakdown = _calculate_tax(cart, address, shipping_cost)
            tax_amount = Money(tax_decimal, currency)
        else:
            tax_amount = zero
            tax_breakdown = {}

        # Normalise before arithmetic. Shipping and tax can arrive in a
        # different currency than the cart operates in.
        def _in_cart_currency(value: Money) -> Money:
            if hasattr(value, "currency") and value.currency != currency:
                return Money(value.amount, currency)
            return value

        shipping_cost = _in_cart_currency(shipping_cost)
        tax_amount = _in_cart_currency(tax_amount)
        discount_amount = _in_cart_currency(discount_amount)

        # Vouchers reduce the total; gift cards do not. A voucher is a price
        # reduction, a gift card is money already handed over -- it settles
        # against amount_due, which is layered on outside this pure quote
        # because it depends on persisted PaymentTransaction rows.
        total_amount = subtotal + shipping_cost + tax_amount - discount_amount
        if total_amount.amount < 0:
            total_amount = zero

        lines = _build_lines(cart, currency)

        return QuoteResult(
            currency=str(currency),
            lines=lines,
            subtotal=subtotal,
            discount_amount=discount_amount,
            shipping=shipping,
            shipping_cost=shipping_cost,
            tax_amount=tax_amount,
            tax_components=_build_tax_components(tax_breakdown, currency),
            tax_breakdown=tax_breakdown,
            total_amount=total_amount,
            computed_at=request.as_of or timezone.now(),
            inputs_fingerprint=_fingerprint(
                cart,
                lines,
                address,
                shipping_method.pk if shipping_method else None,
                str(currency),
            ),
        )
