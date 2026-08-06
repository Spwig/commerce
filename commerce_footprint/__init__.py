"""
Transaction-footprint oracle — the shared assertion surface for the
commercial-lifecycle test programme.

Given one commercial transaction, a ``Footprint`` is the complete
financial/operational record of it: the order and its lines, every payment
transaction and intent, the stock-movement ledger, gift-card and voucher
activity, the emails it produced, and the webhooks it received. A lifecycle
test asserts on the *whole* footprint at once rather than just "the thank-you
page appeared".

Two backends, one identical dataclass:

- ``orm_backend.footprint_for_order`` reads the footprint straight from the
  Django ORM (in-process tiers: ``tests/domain``, ``tests/invariants``,
  ``tests/e2e`` against ``live_server``).
- A future ``http_backend`` (Phase 3, in the standalone ``spwig-e2e`` repo)
  reads the *same* record shapes over HTTP from the read-only
  ``/api/e2e/inspect/`` endpoint against a deployed host.

Everything in ``footprint.py`` is deliberately Django-free — pure dataclasses
and assertion helpers — so it can be vendored by the standalone repo without
pulling in Django. Only ``orm_backend.py`` imports models.
"""

from commerce_footprint.footprint import (
    Amount,
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
    assert_charged_equals,
    assert_exactly_one_order,
    assert_no_duplicate_reference_keys,
    assert_no_paid_order,
    assert_refund_reconciles,
    assert_same_side_effects,
    count_emails,
    net_ledger_movement_by_stock_item,
    total_captured,
    total_refunded,
)

__all__ = [
    "Amount",
    "EmailRecord",
    "Footprint",
    "GiftCardEventRecord",
    "IntentRecord",
    "OrderLineRecord",
    "OrderRecord",
    "PaymentRecord",
    "StockMovementRecord",
    "StockStateRecord",
    "VoucherUsageRecord",
    "WebhookRecord",
    "assert_charged_equals",
    "assert_exactly_one_order",
    "assert_no_duplicate_reference_keys",
    "assert_no_paid_order",
    "assert_refund_reconciles",
    "assert_same_side_effects",
    "count_emails",
    "net_ledger_movement_by_stock_item",
    "total_captured",
    "total_refunded",
]

# orm_backend is imported lazily by callers (it needs Django configured);
# keeping it out of this __init__ lets the standalone repo import the
# Django-free footprint module on its own.
