"""
ORM backend for the footprint oracle — in-process only (needs Django).

``footprint_for_order`` gathers, from a single :class:`orders.models.Order`,
every side effect the commercial-lifecycle tests assert on and returns a
Django-free :class:`~commerce_footprint.footprint.Footprint`.

Correlation basis (be honest about what is and isn't a hard link):

- payments, intents, stock movements, gift-card transactions and voucher
  usages all carry an ``order`` FK — these are exact.
- ``EmailOutbox`` has **no** order FK; order emails are correlated by
  recipient (``to_email == order.email``). A test that needs tighter
  correlation should filter by ``template_type``.
- ``PaymentWebhook`` has **no** order FK either; webhooks are correlated by
  the provider intent/transaction ids that appear on the order's own intents
  and transactions. A webhook that names none of them is not attributed here.
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from commerce_footprint.footprint import (
    Amount,
    BookingLineRecord,
    EmailRecord,
    Footprint,
    GiftCardEventRecord,
    IntentRecord,
    OrderLineRecord,
    OrderRecord,
    PaymentRecord,
    StockMovementRecord,
    StockStateRecord,
    VoucherUsageRecord,
    WebhookRecord,
)

if TYPE_CHECKING:  # pragma: no cover - typing only
    from djmoney.money import Money


def _amt(money: Money | None, *, fallback_currency: str = "USD") -> Amount:
    """djmoney ``Money`` (or None/0) -> Django-free ``Amount``."""
    if money is None:
        return Amount(Decimal("0"), fallback_currency)
    currency = str(getattr(money, "currency", fallback_currency))
    return Amount(Decimal(str(money.amount)), currency)


def _order_line(item, order_currency: str) -> OrderLineRecord:
    """Build a line record, reading the type-specific detail off the OrderItem
    (variant, customizations._configuration/_design, gift_card_data) and the
    linked Booking row — so the footprint can assert the RIGHT variant/config/
    booking/design was bought, not merely that a line exists."""
    custom = item.customizations or {}
    # _configuration is {slot_id: [option_ids]} — normalise to a sorted, hashable
    # tuple so line records compare/round-trip deterministically.
    config = tuple(
        (str(slot), tuple(str(o) for o in opts))
        for slot, opts in sorted((custom.get("_configuration") or {}).items())
    )

    # CustomizationOption values: every non-internal key. Validated form is
    # {option_id: {"value": ..., "calculated_price": ...}}; a raw form stores the
    # value directly. Extract the display value either way.
    def _cust_value(v):
        return str(v.get("value")) if isinstance(v, dict) and "value" in v else str(v)

    customizations = tuple(
        (str(k), _cust_value(v))
        for k, v in sorted(custom.items())
        if k not in ("_design", "_configuration")
    )

    booking = None
    booking_row = next(iter(item.bookings.all()), None)  # prefetched; ≤1 per line
    if booking_row is not None:
        booking = BookingLineRecord(
            start=booking_row.start_datetime.isoformat() if booking_row.start_datetime else "",
            end=booking_row.end_datetime.isoformat() if booking_row.end_datetime else "",
            resource_id=booking_row.resource_id,
            persons=tuple(sorted((str(k), int(v)) for k, v in (booking_row.persons or {}).items())),
            status=booking_row.status or "",
        )
    return OrderLineRecord(
        sku=item.sku,
        name=item.product_name,
        quantity=item.quantity,
        unit_price=_amt(item.unit_price, fallback_currency=order_currency),
        line_total=_amt(item.total_price, fallback_currency=order_currency),
        variant_sku=(item.variant.sku if item.variant_id else ""),
        is_bundle_component=item.parent_bundle_id is not None,
        configuration=config,
        customization_token=(custom.get("_design") or {}).get("token", ""),
        customizations=customizations,
        gift_card_recipient=(item.gift_card_data or {}).get("recipient_email", ""),
        booking=booking,
    )


def footprint_for_order(order_or_number) -> Footprint:
    """Build a :class:`Footprint` for an order (instance or order_number).

    Everything is re-fetched from the DB so the footprint reflects committed
    state, not stale in-memory instances — important right after a webhook or
    a refund mutated rows the caller still holds.
    """
    from orders.models import Order

    if isinstance(order_or_number, str):
        order = Order.objects.get(order_number=order_or_number)
    else:
        order = Order.objects.get(pk=order_or_number.pk)

    order_currency = str(order.total_amount.currency)

    lines = tuple(
        _order_line(item, order_currency)
        for item in order.items.select_related("variant").prefetch_related("bookings")
    )

    order_record = OrderRecord(
        number=order.order_number,
        email=order.email,
        status=order.status,
        payment_status=order.payment_status,
        subtotal=_amt(order.subtotal, fallback_currency=order_currency),
        tax=_amt(order.tax_amount, fallback_currency=order_currency),
        shipping=_amt(order.shipping_cost, fallback_currency=order_currency),
        discount=_amt(order.discount_amount, fallback_currency=order_currency),
        gift_card_discount=_amt(order.gift_card_discount, fallback_currency=order_currency),
        total=_amt(order.total_amount, fallback_currency=order_currency),
        amount_paid=_amt(order.amount_paid, fallback_currency=order_currency),
        amount_refunded=_amt(order.amount_refunded, fallback_currency=order_currency),
        lines=lines,
    )

    payments = tuple(
        PaymentRecord(
            reference=txn.transaction_id,
            transaction_type=txn.transaction_type,
            tender_type=txn.tender_type,
            status=txn.status,
            amount=_amt(txn.amount, fallback_currency=order_currency),
            provider_transaction_id=txn.provider_transaction_id or "",
        )
        for txn in order.payment_transactions.all()
    )

    intents = tuple(
        IntentRecord(
            reference=intent.provider_intent_id,
            status=intent.status,
            amount=_amt(intent.amount, fallback_currency=order_currency),
        )
        for intent in order.payment_intents.all()
    )

    stock_movements = tuple(
        StockMovementRecord(
            stock_item_id=m.stock_item_id,
            movement_type=m.movement_type,
            quantity=m.quantity,
            previous_quantity=m.previous_quantity,
            new_quantity=m.new_quantity,
            reference_key=m.reference_key,
        )
        for m in order.stock_movements.all()
    )

    gift_card_events = tuple(
        GiftCardEventRecord(
            gift_card_code=gct.gift_card.code,
            transaction_type=gct.transaction_type,
            amount=_amt(gct.amount, fallback_currency=order_currency),
            balance_after=_amt(gct.balance_after, fallback_currency=order_currency),
        )
        for gct in order.gift_card_transactions.select_related("gift_card").all()
    )

    from vouchers.models import VoucherUsage

    voucher_usages = tuple(
        VoucherUsageRecord(
            voucher_code=usage.voucher.code,
            discount_amount=_amt(usage.discount_amount, fallback_currency=order_currency),
            cart_total=_amt(usage.cart_total, fallback_currency=order_currency),
        )
        for usage in VoucherUsage.objects.filter(order=order).select_related("voucher")
    )

    from email_system.models import EmailOutbox

    emails = tuple(
        EmailRecord(
            to_email=e.to_email,
            template_type=e.template_type,
            subject=e.subject,
            status=e.status,
            tags=tuple(e.tags or ()),
        )
        for e in EmailOutbox.objects.filter(to_email=order.email).order_by("created_at")
    )

    stock_state = _stock_state_for(order)
    webhooks = _correlated_webhooks(payments, intents)

    return Footprint(
        correlation=order.order_number,
        orders=(order_record,),
        payments=payments,
        intents=intents,
        stock_movements=stock_movements,
        stock_state=stock_state,
        gift_card_events=gift_card_events,
        voucher_usages=voucher_usages,
        emails=emails,
        webhooks=webhooks,
    )


def _stock_state_for(order) -> tuple[StockStateRecord, ...]:
    """Snapshot the StockItem counters for every stock item this order touches.

    The checkout path records allocation on ``StockItem.allocated`` /
    ``on_hand`` and writes no ledger row, so the counters ARE the inventory
    truth. Each order item names its (product, warehouse, variant); we resolve
    the matching StockItem the same way ``fulfillment._build_stock_filter``
    does. Items on products that don't track inventory, or not yet assigned a
    warehouse, have no stock item to snapshot and are skipped. Deduped by
    stock-item pk so two lines hitting the same item don't double-count.
    """
    from catalog.models import StockItem

    seen: dict[int, StockStateRecord] = {}
    for item in order.items.select_related("product", "variant", "warehouse"):
        if not getattr(item.product, "track_inventory", False):
            continue
        if item.warehouse_id is None:
            continue
        flt = {"product": item.product, "warehouse_id": item.warehouse_id}
        if item.variant_id is not None:
            flt["variant_id"] = item.variant_id
        else:
            flt["variant__isnull"] = True
        # Mirror fulfillment's own `.get()` lookup rather than `.first()`: a
        # `.first()` would silently pick an arbitrary row if duplicate NULL-
        # variant stock rows exist, snapshotting a different item than the one
        # allocation actually touched. Ambiguity is a real data bug — surface
        # it. A missing row (line not yet stocked) is a legitimate skip.
        try:
            stock = StockItem.objects.get(**flt)
        except StockItem.DoesNotExist:
            continue
        except StockItem.MultipleObjectsReturned as exc:
            raise AssertionError(
                f"ambiguous stock lookup for order line (product={item.product_id}, "
                f"warehouse={item.warehouse_id}, variant={item.variant_id}): "
                "multiple matching StockItem rows — the inventory oracle cannot "
                "trust which one allocation touched"
            ) from exc
        if stock.pk in seen:
            continue
        seen[stock.pk] = StockStateRecord(
            stock_item_id=stock.pk,
            on_hand=stock.on_hand,
            allocated=stock.allocated,
            available=stock.available,
        )
    return tuple(seen.values())


def _correlated_webhooks(
    payments: tuple[PaymentRecord, ...], intents: tuple[IntentRecord, ...]
) -> tuple[WebhookRecord, ...]:
    """Webhooks whose payload names one of this order's provider ids.

    ``PaymentWebhook`` has no order FK, so we match on the provider intent and
    transaction ids the order actually holds. This is best-effort by design —
    a webhook naming none of them is genuinely unattributable to this order.
    """
    from payment_providers.models import PaymentWebhook

    provider_ids = {i.reference for i in intents if i.reference} | {
        p.provider_transaction_id for p in payments if p.provider_transaction_id
    }
    if not provider_ids:
        return ()

    matched: list[WebhookRecord] = []
    # Exact scalar match against the payload's JSON values — not a substring
    # scan of str(payload). Substring matching false-positives on id prefixes
    # (pi_1 in pi_10) and false-negatives when a value is nested or non-string;
    # walking the JSON and comparing scalar values by equality avoids both. No
    # row cap: a test DB is small and transaction-isolated, so scan all rows
    # rather than silently dropping older ones past an arbitrary limit.
    for wh in PaymentWebhook.objects.order_by("-created_at").iterator():
        if provider_ids & _scalar_strings(wh.payload):
            matched.append(
                WebhookRecord(
                    provider_slug=wh.provider_slug,
                    event_id=wh.event_id,
                    event_type=wh.event_type,
                    processed=wh.processed,
                )
            )
    return tuple(matched)


def _scalar_strings(value) -> set[str]:
    """All scalar values in a JSON-ish structure, stringified, as a set.

    Used to match provider ids against a webhook payload by exact value rather
    than substring, regardless of how deeply they're nested.
    """
    out: set[str] = set()
    stack = [value]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            stack.extend(current.values())
        elif isinstance(current, (list, tuple)):
            stack.extend(current)
        elif current is not None and not isinstance(current, bool):
            out.add(str(current))
    return out
