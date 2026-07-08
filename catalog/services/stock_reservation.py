"""
Stock Reservation Service

Manages temporary stock reservations tied to cart items.
Reservations hold allocated stock while a customer shops,
preventing overselling between add-to-cart and checkout.
"""
from datetime import timedelta
from typing import Optional, Tuple

from django.db import transaction
from django.db.models import F
from django.utils import timezone
import logging

from catalog.models import StockItem, StockReservation, Product, Warehouse

logger = logging.getLogger(__name__)

RESERVATION_TTL = {
    'web': timedelta(minutes=30),
    'pos': timedelta(minutes=15),
}


class StockReservationService:
    """Service for managing cart-level stock reservations."""

    @staticmethod
    @transaction.atomic
    def reserve_stock(
        cart_item,
        quantity: int,
        channel: str = 'web',
        warehouse: Optional[Warehouse] = None,
        region=None,
    ) -> Tuple[bool, str, Optional[StockReservation]]:
        """
        Create or update a stock reservation for a cart item.

        For POS: warehouse is known (terminal's warehouse).
        For web: picks warehouse with most available stock, scoped to region if provided.

        Args:
            cart_item: CartItem instance
            quantity: Units to reserve
            channel: 'web' or 'pos'
            warehouse: Explicit warehouse (POS), None for auto-select (web)
            region: SalesRegion to scope warehouse selection (web). If None,
                    searches all active warehouses.

        Returns:
            Tuple of (success, message, reservation)
        """
        product = cart_item.product
        variant = cart_item.variant

        if not product.track_inventory:
            return True, 'Product does not track inventory', None

        if warehouse is None:
            # Re-use warehouse from existing reservation if one exists
            existing_res = StockReservation.objects.filter(
                cart_item=cart_item
            ).select_related('warehouse').first()
            if existing_res:
                warehouse = existing_res.warehouse
            else:
                warehouse = StockReservationService._select_best_warehouse(
                    product, variant, quantity, region=region
                )
                if warehouse is None:
                    return False, 'No warehouse with sufficient stock', None

        # Get stock item with row lock
        try:
            stock_query = StockItem.objects.select_for_update().filter(
                product=product,
                warehouse=warehouse,
            )
            if variant:
                stock_query = stock_query.filter(variant=variant)
            else:
                stock_query = stock_query.filter(variant__isnull=True)

            stock_item = stock_query.get()
        except StockItem.DoesNotExist:
            return False, f'No stock record at warehouse', None

        ttl = RESERVATION_TTL.get(channel, RESERVATION_TTL['web'])

        # Check for existing reservation on this cart_item + stock_item
        existing = StockReservation.objects.filter(
            cart_item=cart_item,
            stock_item=stock_item,
        ).first()

        if existing:
            delta = quantity - existing.quantity
            if delta > 0:
                if stock_item.available < delta:
                    return False, 'Insufficient stock for increased quantity', None
                StockItem.objects.filter(pk=stock_item.pk).update(
                    allocated=F('allocated') + delta
                )
            elif delta < 0:
                StockItem.objects.filter(pk=stock_item.pk).update(
                    allocated=F('allocated') + delta  # delta is negative
                )

            existing.quantity = quantity
            existing.expires_at = timezone.now() + ttl
            existing.save(update_fields=['quantity', 'expires_at'])

            logger.info(
                f"Updated reservation for cart_item {cart_item.id}: "
                f"{quantity}x {product.sku} @ {warehouse.code}"
            )
            return True, 'Reservation updated', existing

        # Release any reservation at a different warehouse for this cart_item
        old_reservations = StockReservation.objects.filter(
            cart_item=cart_item
        ).select_related('stock_item')
        for old_res in old_reservations:
            StockItem.objects.select_for_update().filter(
                pk=old_res.stock_item_id
            ).update(allocated=F('allocated') - old_res.quantity)
            old_res.delete()

        # Create new reservation
        if stock_item.available < quantity:
            return False, (
                f'Insufficient stock: need {quantity}, '
                f'have {stock_item.available}'
            ), None

        StockItem.objects.filter(pk=stock_item.pk).update(
            allocated=F('allocated') + quantity
        )

        reservation = StockReservation.objects.create(
            stock_item=stock_item,
            cart_item=cart_item,
            quantity=quantity,
            channel=channel,
            warehouse=warehouse,
            expires_at=timezone.now() + ttl,
        )

        logger.info(
            f"Created reservation for cart_item {cart_item.id}: "
            f"{quantity}x {product.sku} @ {warehouse.code} "
            f"(expires {reservation.expires_at})"
        )
        return True, 'Stock reserved', reservation

    @staticmethod
    @transaction.atomic
    def release_reservation(cart_item) -> bool:
        """
        Release all reservations for a cart item.
        Decrements allocated on StockItem.
        """
        reservations = StockReservation.objects.filter(
            cart_item=cart_item
        ).select_related('stock_item')

        released = False
        for reservation in reservations:
            StockItem.objects.select_for_update().filter(
                pk=reservation.stock_item_id
            ).update(allocated=F('allocated') - reservation.quantity)
            reservation.delete()
            released = True

            logger.info(
                f"Released reservation for cart_item {cart_item.id}: "
                f"{reservation.quantity}x @ {reservation.warehouse.code}"
            )

        return released

    @staticmethod
    @transaction.atomic
    def release_cart_reservations(cart) -> int:
        """Release all reservations for all items in a cart."""
        reservations = StockReservation.objects.filter(
            cart_item__cart=cart
        ).select_related('stock_item')

        count = 0
        for reservation in reservations:
            StockItem.objects.select_for_update().filter(
                pk=reservation.stock_item_id
            ).update(allocated=F('allocated') - reservation.quantity)
            reservation.delete()
            count += 1

        if count:
            logger.info(f"Released {count} reservations for cart {cart.id}")

        return count

    @staticmethod
    @transaction.atomic
    def convert_reservation_to_order_allocation(
        cart_item,
        warehouse: Warehouse,
    ) -> bool:
        """
        Convert a cart reservation to an order-level allocation at checkout.

        If reservation is at the same warehouse: delete it (allocated stays,
        now counts as order-level). Returns True.

        If different warehouse: release old reservation, return False so
        the caller does a fresh allocate_stock() at the new warehouse.
        """
        reservation = StockReservation.objects.filter(
            cart_item=cart_item
        ).select_related('stock_item').first()

        if not reservation:
            return False

        if reservation.warehouse_id == warehouse.id:
            reservation.delete()
            logger.info(
                f"Converted reservation for cart_item {cart_item.id} "
                f"to order allocation at {warehouse.code}"
            )
            return True
        else:
            StockItem.objects.select_for_update().filter(
                pk=reservation.stock_item_id
            ).update(allocated=F('allocated') - reservation.quantity)
            reservation.delete()
            logger.info(
                f"Released reservation at warehouse {reservation.warehouse_id} for "
                f"cart_item {cart_item.id} (order uses {warehouse.code})"
            )
            return False

    @staticmethod
    @transaction.atomic
    def convert_pos_reservation_to_fulfillment(
        cart_item,
        warehouse: Warehouse,
    ) -> bool:
        """
        POS checkout: convert reservation to immediate fulfillment.

        Deletes reservation, then does on_hand -= qty, allocated -= qty.
        Net: allocated returns to pre-reservation level, on_hand decreases
        (item physically removed from warehouse).
        """
        reservation = StockReservation.objects.filter(
            cart_item=cart_item
        ).select_related('stock_item').first()

        if not reservation:
            return False

        qty = reservation.quantity

        StockItem.objects.select_for_update().filter(
            pk=reservation.stock_item_id
        ).update(
            on_hand=F('on_hand') - qty,
            allocated=F('allocated') - qty,
        )

        reservation.delete()

        logger.info(
            f"POS fulfillment for cart_item {cart_item.id}: "
            f"{qty}x @ {warehouse.code}"
        )
        return True

    @staticmethod
    def release_expired_reservations() -> int:
        """
        Release all expired reservations. Called by Celery beat task.
        Processes individually so a single failure doesn't block others.
        """
        now = timezone.now()
        expired_ids = list(
            StockReservation.objects.filter(
                expires_at__lte=now
            ).values_list('id', flat=True)[:500]
        )

        count = 0
        for res_id in expired_ids:
            try:
                with transaction.atomic():
                    reservation = StockReservation.objects.select_related(
                        'stock_item'
                    ).filter(pk=res_id).first()
                    if not reservation:
                        continue

                    StockItem.objects.select_for_update().filter(
                        pk=reservation.stock_item_id
                    ).update(allocated=F('allocated') - reservation.quantity)
                    reservation.delete()
                    count += 1

                    logger.debug(
                        f"Expired reservation released: {reservation.quantity}x "
                        f"(cart_item {reservation.cart_item_id})"
                    )
            except Exception as e:
                logger.error(f"Failed to release expired reservation {res_id}: {e}")

        if count:
            logger.info(f"Released {count} expired stock reservations")

        return count

    @staticmethod
    def extend_reservation(cart_item, channel: str = 'web') -> bool:
        """Extend the TTL of an existing reservation."""
        ttl = RESERVATION_TTL.get(channel, RESERVATION_TTL['web'])
        updated = StockReservation.objects.filter(
            cart_item=cart_item
        ).update(
            expires_at=timezone.now() + ttl
        )
        return updated > 0

    @staticmethod
    def _select_best_warehouse(product, variant, quantity: int, region=None):
        """
        For web carts: pick warehouse with most available stock.

        If region is provided, searches only warehouses in that region first.
        Falls back to all active warehouses if no regional stock found.
        """
        stock_query = StockItem.objects.filter(
            product=product,
            warehouse__is_active=True,
        ).select_related('warehouse')

        if variant:
            stock_query = stock_query.filter(variant=variant)
        else:
            stock_query = stock_query.filter(variant__isnull=True)

        # If region provided, try regional warehouses first
        if region:
            regional_query = stock_query.filter(warehouse__region=region)
            best = StockReservationService._find_best_stock_item(
                regional_query, quantity
            )
            if best:
                return best.warehouse

        # Fall back to global search
        best = StockReservationService._find_best_stock_item(
            stock_query, quantity
        )
        return best.warehouse if best else None

    @staticmethod
    def _find_best_stock_item(stock_query, quantity: int):
        """Find the StockItem with the most available stock meeting quantity."""
        best_item = None
        best_available = -1

        for stock_item in stock_query:
            avail = stock_item.available
            if avail >= quantity and avail > best_available:
                best_available = avail
                best_item = stock_item

        return best_item
