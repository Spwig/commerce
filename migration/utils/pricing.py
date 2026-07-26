"""Shared price-adjustment for the migration importers.

Step 4 offers an optional across-the-board price change — "+15%", "-2.00" — to
apply as data is imported. It must land on every price a customer would pay for
a product going forward, and on none of the prices that record what a customer
already paid.

Apply it to:
  * a product's regular price
  * a custom variant price (an "inherit" variant has no price of its own; it
    follows the already-adjusted parent, so there is nothing to do)
  * a sale price, so a discount stays proportional rather than deepening when
    the regular price is marked up

Never apply it to order or order-item prices. Those are a historical record;
changing them would falsify past transactions and break financial
reconciliation.
"""

from decimal import Decimal, InvalidOperation


def apply_price_adjustment(price, adjustment_type, adjustment_value):
    """Return `price` with the configured adjustment applied.

    `price` may be a Decimal, a Money instance, a number or a numeric string;
    None passes straight through (an inherited variant price, a missing sale
    price). The return type matches the input for Money and Decimal so callers
    can assign it straight back.

    A percentage or fixed adjustment can never drive a price below zero.
    """
    if price is None:
        return None
    if adjustment_type not in ("percentage", "fixed"):
        return price

    try:
        value = Decimal(str(adjustment_value))
    except (InvalidOperation, TypeError):
        return price
    if value == 0:
        return price

    # Money wraps a Decimal in .amount and rewraps on arithmetic, so operate on
    # the amount and let the caller keep whatever type it passed in.
    money = getattr(price, "amount", None)
    base = money if money is not None else price
    if not isinstance(base, Decimal):
        try:
            base = Decimal(str(base))
        except (InvalidOperation, TypeError):
            return price

    if adjustment_type == "percentage":
        adjusted = base * (Decimal("1") + value / Decimal("100"))
    else:  # fixed
        adjusted = base + value

    if adjusted < 0:
        adjusted = Decimal("0")

    if money is not None:
        # Rebuild a Money of the same currency rather than doing Money arithmetic
        # (Money + Decimal is not supported).
        return type(price)(adjusted, price.currency)
    return adjusted


def get_adjustment(connection_config):
    """Pull (type, value) out of a job's connection_config, or (None, None)."""
    cfg = connection_config or {}
    adjustment_type = cfg.get("price_adjustment_type", "none")
    if adjustment_type not in ("percentage", "fixed"):
        return None, None
    return adjustment_type, cfg.get("price_adjustment_value", "0")
