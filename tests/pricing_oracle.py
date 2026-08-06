"""
Independent total-recalculation oracle.

``tests/helpers.assert_totals`` compares Spwig's displayed totals against
values *you pass in* — but nothing stops those expected values from having
been copied out of Spwig in the first place. This module is the missing
independent oracle: it recomputes subtotal / discount / shipping / tax / total
from **raw inputs using pure Decimal arithmetic**, calling none of Spwig's
pricing code (``PricingService``, ``TaxService``, ``ShippingRuleService``). A
Tier-1 test then constructs a cart whose raw inputs it fully controls and
asserts Spwig's quote equals this oracle. A divergence is a Spwig pricing bug
or a convention the test hasn't pinned — never a tautology.

The top-level identity it encodes is exactly the one in
``commerce/pricing.py``::

    total = subtotal + shipping + tax - discount

What Spwig leaves *configurable* — the tax base, tax-inclusive vs exclusive,
and line- vs order-level rounding — is made explicit here as parameters, so
the test states the convention it built the store to use rather than this
oracle silently guessing one.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from commerce_footprint.footprint import Amount

_CENTS = Decimal("0.01")


def _q(value: Decimal) -> Decimal:
    """Quantise to 2dp, banker's-averse ROUND_HALF_UP (matches djmoney/display)."""
    return Decimal(value).quantize(_CENTS, rounding=ROUND_HALF_UP)


# Tax-base options: which figure the tax rate is applied to. Spwig's
# ``_calculate_tax`` passes shipping into TaxService, so a store that taxes
# shipping uses ``SUBTOTAL_LESS_DISCOUNT_PLUS_SHIPPING``.
TAX_BASE_SUBTOTAL = "subtotal"
TAX_BASE_LESS_DISCOUNT = "subtotal_less_discount"
TAX_BASE_LESS_DISCOUNT_PLUS_SHIPPING = "subtotal_less_discount_plus_shipping"

ROUND_PER_LINE = "line"
ROUND_PER_ORDER = "order"


@dataclass(frozen=True, slots=True)
class LineSpec:
    """One cart line, as raw inputs. ``unit_price`` is the effective price the
    customer pays per unit (any per-line discount already folded in)."""

    unit_price: Decimal
    quantity: int

    def raw_total(self) -> Decimal:
        return Decimal(self.unit_price) * self.quantity


@dataclass(frozen=True, slots=True)
class CartSpec:
    lines: tuple[LineSpec, ...]
    currency: str = "USD"
    order_discount: Decimal = Decimal("0")  # absolute order-level discount
    shipping: Decimal = Decimal("0")
    tax_rate: Decimal = Decimal("0")  # e.g. Decimal("0.08") for 8%
    tax_base: str = TAX_BASE_LESS_DISCOUNT
    # True => unit prices already include tax (Spwig supports both display
    # modes). A test using this MUST have configured the store as tax-inclusive
    # (SiteSettings / tax config) — otherwise the oracle and Spwig disagree by
    # design, not by bug. Default is exclusive, matching the common setup.
    tax_inclusive: bool = False
    rounding: str = ROUND_PER_LINE


@dataclass(frozen=True, slots=True)
class ExpectedTotals:
    subtotal: Amount
    discount: Amount
    shipping: Amount
    tax: Amount
    total: Amount

    def as_dict(self) -> dict[str, str]:
        """String-value dict compatible with ``tests.helpers.assert_totals``."""
        return {
            "subtotal": str(self.subtotal.value),
            "discount": str(self.discount.value),
            "shipping": str(self.shipping.value),
            "tax": str(self.tax.value),
            "total": str(self.total.value),
        }


def recompute_expected_total(spec: CartSpec) -> ExpectedTotals:
    """Recompute every total from ``spec`` with independent Decimal arithmetic."""
    cur = spec.currency

    # Subtotal — rounding discipline chosen by the spec.
    if spec.rounding == ROUND_PER_LINE:
        subtotal = sum((_q(line.raw_total()) for line in spec.lines), Decimal("0"))
    elif spec.rounding == ROUND_PER_ORDER:
        subtotal = _q(sum((line.raw_total() for line in spec.lines), Decimal("0")))
    else:  # pragma: no cover - guarded input
        raise ValueError(f"unknown rounding mode {spec.rounding!r}")

    discount = _q(Decimal(spec.order_discount))
    shipping = _q(Decimal(spec.shipping))

    tax = _compute_tax(spec, subtotal=subtotal, discount=discount, shipping=shipping)

    if spec.tax_inclusive:
        # Prices already include tax: the tax is carved *out* of the subtotal,
        # not added on top, so it must not inflate the total.
        total = _q(subtotal + shipping - discount)
    else:
        total = _q(subtotal + shipping + tax - discount)

    return ExpectedTotals(
        subtotal=Amount(subtotal, cur),
        discount=Amount(discount, cur),
        shipping=Amount(shipping, cur),
        tax=Amount(tax, cur),
        total=Amount(total, cur),
    )


def _compute_tax(
    spec: CartSpec, *, subtotal: Decimal, discount: Decimal, shipping: Decimal
) -> Decimal:
    rate = Decimal(spec.tax_rate)
    if rate == 0:
        return Decimal("0.00")

    if spec.tax_inclusive:
        # tax = base - base/(1+rate); base is the tax-inclusive amount.
        base = _tax_base(spec, subtotal=subtotal, discount=discount, shipping=shipping)
        return _q(base - (base / (Decimal("1") + rate)))

    base = _tax_base(spec, subtotal=subtotal, discount=discount, shipping=shipping)
    return _q(base * rate)


def _tax_base(
    spec: CartSpec, *, subtotal: Decimal, discount: Decimal, shipping: Decimal
) -> Decimal:
    if spec.tax_base == TAX_BASE_SUBTOTAL:
        base = subtotal
    elif spec.tax_base == TAX_BASE_LESS_DISCOUNT:
        base = subtotal - discount
    elif spec.tax_base == TAX_BASE_LESS_DISCOUNT_PLUS_SHIPPING:
        base = subtotal - discount + shipping
    else:
        raise ValueError(f"unknown tax_base {spec.tax_base!r}")  # pragma: no cover
    # Clamp to zero. A discount larger than the subtotal must not produce a
    # negative tax base (and thus negative tax) — Spwig's TaxService skips
    # non-positive bases, so mirroring that keeps the oracle from asserting an
    # impossible negative tax.
    return base if base > 0 else Decimal("0")
