"""
Stock operations service — the execution paths behind the StockMovement types.

Each function is a named inventory capability that creates the corresponding
StockMovement audit rows and mutates StockItem quantities atomically and
race-safely (row locks + integer arithmetic under a single transaction, never
read-modify-write on unlocked rows). These back the movement types that were
previously declared on StockMovement.MOVEMENT_TYPES but had no code creating
them: 'transfer', 'damage', and 'recount'.
"""

import logging

from django.db import transaction

from catalog.models import StockItem, StockMovement

logger = logging.getLogger(__name__)


class StockOperationError(Exception):
    """Base error for an invalid stock operation."""


class InsufficientStockError(StockOperationError):
    """Raised when an operation would move/remove more than is available."""


def _require_quantity(quantity, *, allow_zero, label):
    """Reject any quantity that is not a real integer in the allowed range.

    Stock and movement columns are IntegerFields, so a fractional value is
    silently truncated at save time — separately for the on-hand total and the
    movement delta — which desynchronises inventory from its audit trail.
    Booleans (an ``int`` subclass) are rejected too.
    """
    if isinstance(quantity, bool) or not isinstance(quantity, int):
        raise StockOperationError(f"{label} must be an integer.")
    if allow_zero:
        if quantity < 0:
            raise StockOperationError(f"{label} must be zero or a positive integer.")
    elif quantity <= 0:
        raise StockOperationError(f"{label} must be a positive integer.")


def _existing_by_reference(reference_key):
    """Return the StockMovement rows already recorded under an idempotency key.

    Lets a retried offline/queued operation no-op instead of double-applying.
    """
    if not reference_key:
        return []
    return list(StockMovement.objects.filter(reference_key=reference_key))


@transaction.atomic
def transfer_stock(
    product,
    source_warehouse,
    dest_warehouse,
    quantity,
    variant=None,
    user=None,
    reason="",
    reference_key=None,
):
    """Move available on-hand stock from one warehouse to another.

    Decrements the source StockItem's on_hand and increments the destination's,
    recording a paired 'transfer' StockMovement at each end (negative at source,
    positive at destination) so the audit trail is symmetric. Only unreserved
    stock (available = on_hand - allocated) can be transferred; allocated units
    stay put for the orders that hold them. Atomic and idempotent on
    reference_key.

    Returns a dict with the source/destination StockItems and their movements.
    """
    _require_quantity(quantity, allow_zero=False, label="Transfer quantity")
    if source_warehouse == dest_warehouse:
        raise StockOperationError("Source and destination warehouses must differ.")

    if reference_key:
        prior = _existing_by_reference(reference_key)
        if prior:
            logger.info("transfer_stock: reference_key=%s already applied, skipping", reference_key)
            return {"idempotent": True, "movements": prior}

    src_row = StockItem.objects.filter(
        product=product, warehouse=source_warehouse, variant=variant
    ).first()
    if src_row is None:
        raise InsufficientStockError(f"No stock record for {product} at {source_warehouse}.")
    # Create the destination row if absent (unique_together makes this safe).
    dst_row, _ = StockItem.objects.get_or_create(
        product=product,
        warehouse=dest_warehouse,
        variant=variant,
        defaults={"on_hand": 0, "allocated": 0},
    )
    # Lock both rows in a deterministic (pk) order to avoid deadlocking against
    # a concurrent transfer of the same pair in the opposite direction.
    locked = {
        si.pk: si
        for si in StockItem.objects.select_for_update()
        .filter(pk__in=[src_row.pk, dst_row.pk])
        .order_by("pk")
    }
    source = locked[src_row.pk]
    dest = locked[dst_row.pk]

    available = max(0, source.on_hand - source.allocated)
    if quantity > available:
        raise InsufficientStockError(
            f"Cannot transfer {quantity} units. Only {available} available at {source_warehouse}."
        )

    src_prev, dst_prev = source.on_hand, dest.on_hand
    source.on_hand = src_prev - quantity
    dest.on_hand = dst_prev + quantity
    source.save(update_fields=["on_hand"])
    dest.save(update_fields=["on_hand"])

    out_mv = StockMovement.objects.create(
        stock_item=source,
        movement_type="transfer",
        quantity=-quantity,
        previous_quantity=src_prev,
        new_quantity=source.on_hand,
        reason=reason or f"Transfer to {dest_warehouse}",
        user=user,
        reference_key=reference_key,
    )
    in_mv = StockMovement.objects.create(
        stock_item=dest,
        movement_type="transfer",
        quantity=quantity,
        previous_quantity=dst_prev,
        new_quantity=dest.on_hand,
        reason=reason or f"Transfer from {source_warehouse}",
        user=user,
        # Same key as the outbound leg: reference_key is indexed but not unique,
        # so both legs share it and idempotency lookup finds the pair on retry.
        # (A suffixed key risked exceeding the 64-char field limit.)
        reference_key=reference_key,
    )
    logger.info(
        "transfer_stock: %s x%d %s -> %s", product, quantity, source_warehouse, dest_warehouse
    )
    return {"source": source, "destination": dest, "movements": [out_mv, in_mv]}


@transaction.atomic
def record_damage(stock_item, quantity, user=None, reason="", reference_key=None):
    """Write off damaged or lost units, decrementing on-hand stock.

    Records a 'damage' StockMovement with a negative delta. Cannot write off
    units that are allocated to orders (on_hand must stay >= allocated). Atomic
    and idempotent on reference_key.
    """
    _require_quantity(quantity, allow_zero=False, label="Damage quantity")

    if reference_key:
        prior = _existing_by_reference(reference_key)
        if prior:
            logger.info("record_damage: reference_key=%s already applied, skipping", reference_key)
            return prior[0]

    item = StockItem.objects.select_for_update().get(pk=stock_item.pk)
    if item.on_hand - quantity < item.allocated:
        unreserved = max(0, item.on_hand - item.allocated)
        raise InsufficientStockError(
            f"Cannot write off {quantity} units. Only {unreserved} unreserved "
            f"units on hand (rest are allocated to orders)."
        )

    prev = item.on_hand
    item.on_hand = prev - quantity
    item.save(update_fields=["on_hand"])

    mv = StockMovement.objects.create(
        stock_item=item,
        movement_type="damage",
        quantity=-quantity,
        previous_quantity=prev,
        new_quantity=item.on_hand,
        reason=reason or "Damaged/lost stock",
        user=user,
        reference_key=reference_key,
    )
    logger.info("record_damage: %s -%d @ %s", item.product, quantity, item.warehouse)
    return mv


@transaction.atomic
def recount_stock(stock_item, counted_quantity, user=None, reason="", reference_key=None):
    """Reconcile on-hand stock to a physically counted quantity.

    Sets on_hand to counted_quantity and records a 'recount' StockMovement whose
    delta is the correction (positive or negative). Warns, but does not block,
    when the counted quantity is below the already-allocated amount — that is a
    real shortage the merchant needs to see. Atomic and idempotent on
    reference_key.
    """
    _require_quantity(counted_quantity, allow_zero=True, label="Counted quantity")

    if reference_key:
        prior = _existing_by_reference(reference_key)
        if prior:
            logger.info("recount_stock: reference_key=%s already applied, skipping", reference_key)
            return prior[0]

    item = StockItem.objects.select_for_update().get(pk=stock_item.pk)
    prev = item.on_hand
    delta = counted_quantity - prev

    if counted_quantity < item.allocated:
        logger.warning(
            "recount_stock: counted %d is below %d allocated for %s @ %s",
            counted_quantity,
            item.allocated,
            item.product,
            item.warehouse,
        )

    item.on_hand = counted_quantity
    item.save(update_fields=["on_hand"])

    mv = StockMovement.objects.create(
        stock_item=item,
        movement_type="recount",
        quantity=delta,
        previous_quantity=prev,
        new_quantity=counted_quantity,
        reason=reason or "Physical stock recount",
        user=user,
        reference_key=reference_key,
    )
    logger.info(
        "recount_stock: %s @ %s %d -> %d", item.product, item.warehouse, prev, counted_quantity
    )
    return mv
