"""
Celery Tasks for Catalog App
Handles scheduled gift card email delivery.
"""

import logging

from celery import shared_task
from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(
    name="catalog.issue_gift_cards_for_order",
    ignore_result=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def issue_gift_cards_for_order(order_pk):
    """
    Mint and deliver the gift cards an order paid for.

    Dispatched by ``issue_gift_cards_on_payment_confirmed`` after commit.

    Retrying is safe — and is why this raises rather than swallows. Every card
    claims a unique ``(order_item, issue_index)`` slot, so a retry re-mints
    nothing; it only fills slots a previous attempt did not reach. Swallowing
    here would leave a paying customer with no card and no exception anywhere.
    """
    from orders.models import Order

    from .services.gift_card_service import GiftCardService

    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        logger.warning(f"Gift card issuance: order {order_pk} no longer exists")
        return None

    count, codes = GiftCardService.create_gift_cards_for_order(order)
    if count:
        logger.info(f"Issued {count} gift card(s) for order {order.order_number}")
    return count


@shared_task(name="catalog.reconcile_gift_card_issuance", ignore_result=True)
def reconcile_gift_card_issuance(hours=48):
    """
    Find paid orders whose gift cards were never minted, and mint them.

    The safety net beneath the receiver. A dropped Celery message, a broker
    outage, or a worker killed mid-run all produce the same silent outcome:
    the customer paid and holds nothing, with no exception raised anywhere.
    Nothing else in the system would ever notice.

    Cheap because it only looks at recently-paid orders and compares a count.
    """
    from datetime import timedelta

    from django.db.models import Count, IntegerField, OuterRef, Subquery, Sum, Value
    from django.db.models.functions import Coalesce

    from orders.models import Order, OrderItem

    from .models import GiftCard
    from .services.gift_card_service import GiftCardService

    since = timezone.now() - timedelta(hours=hours)

    # Compute the two aggregates in independent subqueries. Annotating both
    # Sum("items__quantity") and Count("items__gift_cards") on one query joins
    # each gift_card line against every card minted from it, so the quantity Sum
    # is multiplied by the gift_cards fan-out (a line of qty 2 with 2 cards sums
    # to 4) and a fully-minted order reads as under-minted on every run.
    # Correlated subqueries cannot cross-join, so each aggregate stays honest.
    gift_card_lines = OrderItem.objects.filter(
        order=OuterRef("pk"),
        product__product_type="gift_card",
        parent_bundle__isnull=True,
    )
    wanted_sq = (
        gift_card_lines.order_by().values("order").annotate(total=Sum("quantity")).values("total")
    )
    minted_sq = (
        GiftCard.objects.filter(
            order_item__order=OuterRef("pk"),
            order_item__product__product_type="gift_card",
            order_item__parent_bundle__isnull=True,
        )
        .order_by()
        .values("order_item__order")
        .annotate(total=Count("id"))
        .values("total")
    )

    candidates = (
        Order.objects.filter(
            payment_status="paid",
            paid_at__gte=since,
            items__product__product_type="gift_card",
            items__parent_bundle__isnull=True,
        )
        .annotate(
            wanted=Coalesce(Subquery(wanted_sq, output_field=IntegerField()), Value(0)),
            minted=Coalesce(Subquery(minted_sq, output_field=IntegerField()), Value(0)),
        )
        .filter(minted__lt=models.F("wanted"))
        .distinct()
    )

    repaired = 0
    for order in candidates:
        try:
            count, _codes = GiftCardService.create_gift_cards_for_order(order)
            if count:
                repaired += count
                logger.warning(
                    f"Reconcile minted {count} missing gift card(s) for paid order "
                    f"{order.order_number} — the issuance task never completed"
                )
        except Exception:
            logger.exception(f"Reconcile could not mint gift cards for order {order.order_number}")

    if repaired:
        logger.warning(f"Gift card reconcile repaired {repaired} card(s)")
    return repaired


def _claim_and_send_gift_card(gift_card_id):
    """Atomically claim one gift card and deliver it exactly once.

    Locks the card row and re-checks ``issued_at`` inside the transaction before
    sending, so two overlapping workers — the scheduled sweep and a redelivered
    immediate-send racing each other — can never both read ``issued_at IS NULL``
    and both email the recipient. The loser blocks on the row lock, then reads
    the stamped ``issued_at`` and reports ``already_issued``. A failed send makes
    no write, leaving the card unstamped and retryable by a later run.

    Returns ``(status, code)`` where status is one of ``sent``, ``failed``,
    ``already_issued``, or ``not_found``.
    """
    from django.db import transaction

    from .models import GiftCard
    from .services.gift_card_service import GiftCardService

    with transaction.atomic():
        gift_card = (
            GiftCard.objects.select_for_update()
            .filter(pk=gift_card_id)
            .select_related("product")
            .first()
        )
        if gift_card is None:
            return "not_found", None
        if gift_card.issued_at:
            return "already_issued", gift_card.code
        if not GiftCardService._send_gift_card_email(gift_card):
            # No write made: the claim is released and the card stays retryable.
            return "failed", gift_card.code

        gift_card.issued_at = timezone.now()
        gift_card.save(update_fields=["issued_at"])
        return "sent", gift_card.code


@shared_task(name="catalog.send_scheduled_gift_card_emails", ignore_result=True)
def send_scheduled_gift_card_emails():
    """
    Send gift card emails that are scheduled for delivery.
    Runs every 5-10 minutes via Celery Beat.

    Finds gift cards where:
    - scheduled_send_at <= now
    - issued_at is NULL (not yet sent)
    - is_active is True
    """
    from .models import GiftCard

    now = timezone.now()

    # Claim IDs up front, then re-check-and-lock each card individually inside
    # _claim_and_send_gift_card. Reading the batch here is only a candidate list;
    # the atomic claim is what guarantees a single delivery even if another
    # worker (or a redelivered immediate-send task) is sweeping the same card.
    scheduled_ids = list(
        GiftCard.objects.filter(
            scheduled_send_at__lte=now, issued_at__isnull=True, is_active=True
        ).values_list("pk", flat=True)
    )

    total = len(scheduled_ids)

    if total == 0:
        logger.debug("No scheduled gift cards to send")
        return None

    logger.info(f"Found {total} scheduled gift cards to send")

    sent_count = 0
    failed_count = 0

    for gift_card_id in scheduled_ids:
        try:
            status, code = _claim_and_send_gift_card(gift_card_id)
            if status == "sent":
                sent_count += 1
                logger.info(f"Sent scheduled gift card {code}")
            elif status == "failed":
                # Left unstamped on purpose: the next run retries it.
                failed_count += 1
                logger.error(f"Failed to send scheduled gift card {code}")
            # not_found / already_issued: another worker handled it — skip.
        except Exception as e:
            logger.exception(f"Error sending scheduled gift card {gift_card_id}: {str(e)}")
            failed_count += 1

    logger.info(
        f"Scheduled gift card delivery complete: {sent_count} sent, {failed_count} failed out of {total}"
    )

    return {
        "total": total,
        "sent": sent_count,
        "failed": failed_count,
    }


@shared_task(name="catalog.send_gift_card_email")
def send_gift_card_email_task(gift_card_id: int):
    """
    Send a single gift card email immediately.
    Used when scheduled_send_at is not set.

    Args:
        gift_card_id: ID of the gift card to send
    """
    try:
        # Same atomic claim the scheduled sweep uses, so an immediate send that
        # is redelivered (or races the sweep) can never double-send the card.
        status, code = _claim_and_send_gift_card(gift_card_id)

        if status == "sent":
            logger.info(f"Sent gift card {code}")
            return {"status": "sent", "code": code}
        if status == "already_issued":
            logger.warning(f"Gift card {code} already issued")
            return {"status": "already_issued"}
        if status == "not_found":
            logger.error(f"Gift card with ID {gift_card_id} not found")
            return {"status": "not_found"}

        logger.error(f"Failed to send gift card {code}")
        return {"status": "failed", "code": code}

    except Exception as e:
        logger.exception(f"Error sending gift card {gift_card_id}: {str(e)}")
        return {"status": "error", "error": str(e)}


@shared_task(name="catalog.release_expired_stock_reservations", ignore_result=True)
def release_expired_stock_reservations():
    """
    Release stock reservations that have passed their expiry time.
    Runs every 60 seconds via Celery Beat.

    Decrements StockItem.allocated for each expired reservation
    and deletes the reservation record.
    """
    from .services.stock_reservation import StockReservationService

    try:
        released = StockReservationService.release_expired_reservations()
        if released > 0:
            logger.info(f"Released {released} expired stock reservations")
        return {"released": released}
    except Exception as e:
        logger.exception(f"Error releasing expired stock reservations: {e}")
        return {"released": 0, "error": str(e)}


@shared_task(name="catalog.cleanup_cart_items_for_deleted_products")
def cleanup_cart_items_for_deleted_products():
    """
    Remove cart items for soft-deleted products.
    Runs periodically (e.g., hourly) via Celery Beat.

    This cleanup task helps maintain data integrity by removing
    cart items that reference products that have been deleted.
    """
    from cart.models import CartItem

    from .models import Product

    try:
        # Get all deleted product IDs
        deleted_product_ids = Product.all_objects.filter(is_deleted=True).values_list(
            "id", flat=True
        )

        # Delete cart items for deleted products
        deleted_count, _ = CartItem.objects.filter(product_id__in=deleted_product_ids).delete()

        if deleted_count > 0:
            logger.info(f"Cleaned up {deleted_count} cart items for deleted products")

        return {"deleted_count": deleted_count}
    except Exception as e:
        logger.exception(f"Error cleaning up cart items for deleted products: {e}")
        return {"deleted_count": 0, "error": str(e)}


@shared_task(name="catalog.release_expired_booking_slot_reservations", ignore_result=True)
def release_expired_booking_slot_reservations():
    """
    Release booking slot reservations that have passed their expiry time.
    Runs every 60 seconds via Celery Beat (same schedule as stock reservations).
    """
    from .services.booking_service import BookingAvailabilityService

    try:
        released = BookingAvailabilityService.cleanup_expired_reservations()
        if released > 0:
            logger.info(f"Released {released} expired booking slot reservations")
        return {"released": released}
    except Exception as e:
        logger.exception(f"Error releasing expired booking slot reservations: {e}")
        return {"released": 0, "error": str(e)}


@shared_task(name="catalog.send_booking_reminders", ignore_result=True)
def send_booking_reminders():
    """
    Send email reminders for upcoming bookings.
    Runs every 15 minutes via Celery Beat.

    Checks BookingConfig.reminder_hours_before for each booking product
    and sends reminders at the configured intervals (e.g., 1hr, 24hr, 168hr before).
    """
    from django.utils import timezone as tz

    from .models import Booking, BookingConfig

    now = tz.now()
    sent_count = 0

    try:
        # Get bookings that are confirmed and upcoming
        upcoming = Booking.objects.filter(
            status="confirmed",
            start_datetime__gt=now,
            reminder_sent_at__isnull=True,
        ).select_related("product")

        for booking in upcoming:
            try:
                config = booking.product.booking_config
            except BookingConfig.DoesNotExist:
                continue

            if not config.reminder_enabled or not config.reminder_hours_before:
                continue

            hours_until = (booking.start_datetime - now).total_seconds() / 3600

            # Check if any reminder threshold has been crossed
            for reminder_hours in sorted(config.reminder_hours_before, reverse=True):
                if hours_until <= reminder_hours:
                    # Send email reminder via lifecycle service. Only stamp
                    # reminder_sent_at once the send is confirmed — the service
                    # returns False on an empty address or a delivery error, and
                    # stamping regardless would permanently silence the booking
                    # instead of leaving it for the next run to retry.
                    from catalog.services.booking_service import BookingLifecycleService

                    sent = BookingLifecycleService.send_booking_email(
                        booking,
                        "booking_reminder",
                        {"hours_until": round(hours_until)},
                    )
                    if not sent:
                        logger.warning(
                            f"Booking reminder not sent for #{booking.pk} "
                            f"({reminder_hours}h before) — left for retry"
                        )
                        break

                    booking.reminder_sent_at = now
                    booking.save(update_fields=["reminder_sent_at"])
                    sent_count += 1
                    logger.info(
                        f"Booking reminder sent for #{booking.pk} ({reminder_hours}h before)"
                    )
                    break

        return {"sent": sent_count}
    except Exception as e:
        logger.exception(f"Error sending booking reminders: {e}")
        return {"sent": sent_count, "error": str(e)}


@shared_task(name="catalog.expire_gift_card_holds", ignore_result=True)
def expire_gift_card_holds():
    """
    Release gift card holds left behind by abandoned checkouts.

    A hold reserves value without debiting it, so an abandoned basket does not
    cost the customer money — but it does make their card look empty until the
    hold is released. Without this sweep, keying a code and closing the tab
    would strand the balance indefinitely.

    Runs on Celery Beat; see CELERY_BEAT_SCHEDULE.
    """
    from wallet.tender_service import WalletTenderService

    from .services.gift_card_tender_service import GiftCardTenderService

    released = GiftCardTenderService.expire_stale_holds()
    # Same sweep, second internal tender. One task rather than two beat
    # entries: the two rails share hold semantics by design, and a wallet
    # hold left behind by an abandoned checkout locks the customer's own
    # money exactly the way a card hold does.
    wallet_released = WalletTenderService.expire_stale_holds()
    if released or wallet_released:
        logger.info(
            f"Released {released} stale gift card hold(s), {wallet_released} stale wallet hold(s)"
        )
    return {"released": released, "wallet_released": wallet_released}


# ============================================================================
# Back-In-Stock Notifications
# ============================================================================


def _send_back_in_stock_email(notification, stock_item):
    """Render + queue the 'back_in_stock' email for one subscriber.

    Goes through EmailSendingService.send_template_email so it inherits the
    shared communication-preference check, HQ-template gating, account
    selection, and outbox queuing — rather than re-rendering by hand.
    """
    from django.urls import reverse

    from core.translation_utils import get_primary_language
    from email_system.services.email_sender import EmailSendingService

    product = notification.product
    variant = notification.variant

    product_url = reverse("page_builder:product_detail", kwargs={"product_slug": product.slug})

    image_url = getattr(product, "primary_image_url", None)
    if not image_url and variant and getattr(variant, "image_asset", None):
        image_url = variant.image_asset.get_display_url()

    context = {
        "product_name": product.name,
        "variant_name": variant.name if variant else None,
        "product_url": product_url,
        "product_image_url": image_url,
        "subscriber_email": notification.email,
    }
    return EmailSendingService.send_template_email(
        to_email=notification.email,
        template_type="back_in_stock",
        context=context,
        language=get_primary_language(),
        enable_tracking=True,
    )


@shared_task(
    name="catalog.send_back_in_stock_notifications",
    ignore_result=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def send_back_in_stock_notifications(stock_item_id):
    """Notify subscribers that a product is back in stock.

    Dispatched after commit by the StockItem post_save signal when a stock
    item's availability crosses from zero to positive. Sends the
    'back_in_stock' email to every pending StockNotification for the product
    (matching the variant, honouring any preferred-warehouse) and stamps
    notified_at. Each notification is row-locked with skip_locked so two
    concurrent restocks can never double-send, and stamping happens in the same
    transaction as the send so a retry re-sends nothing already delivered.
    """
    from django.db import transaction

    from catalog.models import StockItem, StockNotification

    try:
        stock_item = StockItem.objects.select_related("product", "variant", "warehouse").get(
            pk=stock_item_id
        )
    except StockItem.DoesNotExist:
        return 0

    # Re-check under current state — availability may have changed since dispatch.
    if stock_item.available <= 0:
        return 0

    pending = StockNotification.objects.filter(product=stock_item.product, notified_at__isnull=True)
    if stock_item.variant_id:
        pending = pending.filter(variant_id=stock_item.variant_id)
    else:
        pending = pending.filter(variant__isnull=True)
    pending = pending.filter(
        models.Q(preferred_warehouse__isnull=True)
        | models.Q(preferred_warehouse=stock_item.warehouse)
    )

    sent = 0
    for notif_id in list(pending.values_list("pk", flat=True)):
        with transaction.atomic():
            notif = (
                # of=("self",) locks only the notification row; without it the
                # select_related outer-join on nullable variant makes Postgres
                # reject FOR UPDATE ("nullable side of an outer join").
                StockNotification.objects.select_for_update(skip_locked=True, of=("self",))
                .filter(pk=notif_id, notified_at__isnull=True)
                .select_related("product", "variant")
                .first()
            )
            if notif is None:
                continue  # already claimed by a concurrent run
            _send_back_in_stock_email(notif, stock_item)
            notif.notified_at = timezone.now()
            notif.save(update_fields=["notified_at"])
            sent += 1

    if sent:
        logger.info("back_in_stock: sent %d notification(s) for %s", sent, stock_item.product)
    return sent
