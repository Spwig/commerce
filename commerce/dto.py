"""
Value objects for the commerce service layer.

All frozen. A quote is a statement about a cart at a moment; letting a caller
mutate one would make it a suggestion instead. Money values are djmoney
`Money`, matching the rest of the platform.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from djmoney.money import Money

if TYPE_CHECKING:  # pragma: no cover - typing only
    from cart.models import Cart, ShippingMethod
    from orders.models import Address


@dataclass(frozen=True, slots=True)
class QuoteRequest:
    """
    Inputs to a price calculation.

    `cart` must be persisted. Every downstream consumer -- shipping rules,
    promotion conditions, tax item gathering -- reaches `cart.items`, a
    reverse-FK manager that raises on an unsaved instance. Accepting a
    duck-typed stand-in was considered and rejected: it would be a second code
    path through the pricing engine, which is the exact divergence this layer
    exists to prevent.
    """

    cart: Cart
    shipping_address: Address | dict | None = None
    shipping_method: ShippingMethod | None = None
    user: Any = None
    channel: str = "web"
    as_of: datetime | None = None


@dataclass(frozen=True, slots=True)
class QuoteLine:
    """One priced line. Bundle children are reported but excluded from totals."""

    cart_item_id: int
    product_id: int
    variant_id: int | None
    sku: str
    name: str
    quantity: int
    unit_price: Money
    line_total: Money
    is_bundle_child: bool
    counts_toward_subtotal: bool


@dataclass(frozen=True, slots=True)
class TaxComponent:
    """One applied tax rate, mirroring a TaxService breakdown entry."""

    tax_rate_id: int | None
    name: str
    rate: Decimal
    amount: Money
    compound: bool
    jurisdiction: str
    tax_type: str


@dataclass(frozen=True, slots=True)
class ShippingQuote:
    """The selected shipping method priced against this cart and address."""

    method_id: int
    method_name: str
    base_cost: Money
    final_cost: Money
    total_discount: Money
    total_surcharge: Money
    rules_applied: tuple[dict[str, Any], ...]


@dataclass(frozen=True, slots=True)
class QuoteResult:
    """
    What a cart costs, and why.

    `CheckoutSession` stores these figures, but this object -- not the row --
    is the authority. The row is a cache that anything may re-derive and
    verify.
    """

    currency: str
    lines: tuple[QuoteLine, ...]
    subtotal: Money
    discount_amount: Money
    shipping: ShippingQuote | None
    shipping_cost: Money
    tax_amount: Money
    tax_components: tuple[TaxComponent, ...]
    tax_breakdown: dict[str, Any]
    total_amount: Money
    computed_at: datetime
    inputs_fingerprint: str

    @property
    def gift_card_discount(self) -> Money:
        """
        Always zero, and structurally incapable of being anything else.

        A gift card is a payment tender, not a discount: it settles against
        `amount_due` after tax and shipping and must never reduce the figure
        the customer is billed. Treating it as a discount once capped a card at
        the pre-tax subtotal and let a $200 card leave $20 to charge on a $120
        order. A read-only property means that cannot be reintroduced by
        assignment.
        """
        return Money(Decimal("0"), self.currency)
