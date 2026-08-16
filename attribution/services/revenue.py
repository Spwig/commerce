"""Net revenue for an order, as a frozen currency snapshot.

Attribution reports the money the merchant actually kept: the order total less
anything refunded. A partial refund therefore reduces attributed revenue
proportionally (prorate-to-net) and a full refund zeroes it — the dashboard
always reconciles to real takings. This is deliberately distinct from affiliate
*payout*, which does not prorate partial refunds; that invariant is untouched.

Currency is snapshotted the same way commissions are: the order-currency amount
plus a base-currency equivalent computed with the order's frozen exchange rate,
so a figure never silently moves when rates change later.
"""

from decimal import Decimal

CENTS = Decimal("0.01")


def _amount(money):
    """Return the Decimal amount from a MoneyField value (or a raw number)."""
    if money is None:
        return Decimal("0")
    return getattr(money, "amount", None) if hasattr(money, "amount") else Decimal(str(money))


def attributable_net(order, base_currency=None):
    """Net revenue for ``order`` as a snapshot dict.

    Keys: ``amount`` (order currency), ``currency``, ``amount_base`` (store base
    currency), ``base_currency``, ``exchange_rate``.

    ``base_currency`` may be passed in to avoid a per-call SiteSettings lookup —
    the batch preview resolves it once and threads it through thousands of orders.
    """
    total = _amount(order.total_amount)
    refunded = _amount(getattr(order, "amount_refunded", 0))
    net = max(total - refunded, Decimal("0")).quantize(CENTS)

    # Determine order currency and store base currency.
    order_currency = order.customer_currency
    if not order_currency:
        order_currency = (
            str(order.total_amount.currency) if hasattr(order.total_amount, "currency") else ""
        )

    if base_currency is None:
        try:
            from core.models import SiteSettings

            base_currency = SiteSettings.get_settings().default_currency
        except Exception:
            base_currency = order_currency

    rate = order.exchange_rate_used
    if order_currency and base_currency and order_currency != base_currency and rate:
        # Mirror the affiliate commission convention: amount_base = amount / rate.
        amount_base = (net / rate).quantize(CENTS)
    else:
        amount_base = net

    return {
        "amount": net,
        "currency": order_currency or base_currency,
        "amount_base": amount_base,
        "base_currency": base_currency,
        "exchange_rate": rate,
    }
