"""
Celery Tasks for Catalog App
Handles scheduled gift card email delivery.
"""
from celery import shared_task
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


@shared_task(name='catalog.send_scheduled_gift_card_emails', ignore_result=True)
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
    from .services.gift_card_service import GiftCardService

    now = timezone.now()

    # Find gift cards scheduled for delivery
    scheduled_gift_cards = GiftCard.objects.filter(
        scheduled_send_at__lte=now,
        issued_at__isnull=True,
        is_active=True
    ).select_related('product')

    total = scheduled_gift_cards.count()

    if total == 0:
        logger.debug("No scheduled gift cards to send")
        return None

    logger.info(f"Found {total} scheduled gift cards to send")

    sent_count = 0
    failed_count = 0

    for gift_card in scheduled_gift_cards:
        try:
            # Send the email
            success = GiftCardService._send_gift_card_email(gift_card)

            if success:
                # Mark as issued
                gift_card.issued_at = now
                gift_card.save(update_fields=['issued_at'])
                sent_count += 1
                logger.info(f"Sent scheduled gift card {gift_card.code} to {gift_card.recipient_email}")
            else:
                failed_count += 1
                logger.error(f"Failed to send scheduled gift card {gift_card.code}")

        except Exception as e:
            logger.exception(f"Error sending scheduled gift card {gift_card.code}: {str(e)}")
            failed_count += 1

    logger.info(f"Scheduled gift card delivery complete: {sent_count} sent, {failed_count} failed out of {total}")

    return {
        'total': total,
        'sent': sent_count,
        'failed': failed_count,
    }


@shared_task(name='catalog.send_gift_card_email')
def send_gift_card_email_task(gift_card_id: int):
    """
    Send a single gift card email immediately.
    Used when scheduled_send_at is not set.

    Args:
        gift_card_id: ID of the gift card to send
    """
    from .models import GiftCard
    from .services.gift_card_service import GiftCardService

    try:
        gift_card = GiftCard.objects.select_related('product').get(id=gift_card_id)

        if gift_card.issued_at:
            logger.warning(f"Gift card {gift_card.code} already issued at {gift_card.issued_at}")
            return {'status': 'already_issued'}

        success = GiftCardService._send_gift_card_email(gift_card)

        if success:
            gift_card.issued_at = timezone.now()
            gift_card.save(update_fields=['issued_at'])
            logger.info(f"Sent gift card {gift_card.code} to {gift_card.recipient_email}")
            return {'status': 'sent', 'code': gift_card.code}
        else:
            logger.error(f"Failed to send gift card {gift_card.code}")
            return {'status': 'failed', 'code': gift_card.code}

    except GiftCard.DoesNotExist:
        logger.error(f"Gift card with ID {gift_card_id} not found")
        return {'status': 'not_found'}
    except Exception as e:
        logger.exception(f"Error sending gift card {gift_card_id}: {str(e)}")
        return {'status': 'error', 'error': str(e)}


@shared_task(name='catalog.release_expired_stock_reservations', ignore_result=True)
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
        return {'released': released}
    except Exception as e:
        logger.exception(f"Error releasing expired stock reservations: {e}")
        return {'released': 0, 'error': str(e)}


@shared_task(name='catalog.cleanup_cart_items_for_deleted_products')
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
        deleted_product_ids = Product.all_objects.filter(
            is_deleted=True
        ).values_list('id', flat=True)

        # Delete cart items for deleted products
        deleted_count, _ = CartItem.objects.filter(
            product_id__in=deleted_product_ids
        ).delete()

        if deleted_count > 0:
            logger.info(f"Cleaned up {deleted_count} cart items for deleted products")

        return {
            'deleted_count': deleted_count
        }
    except Exception as e:
        logger.exception(f"Error cleaning up cart items for deleted products: {e}")
        return {'deleted_count': 0, 'error': str(e)}


@shared_task(name='catalog.release_expired_booking_slot_reservations', ignore_result=True)
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
        return {'released': released}
    except Exception as e:
        logger.exception(f"Error releasing expired booking slot reservations: {e}")
        return {'released': 0, 'error': str(e)}


@shared_task(name='catalog.send_booking_reminders', ignore_result=True)
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
            status='confirmed',
            start_datetime__gt=now,
            reminder_sent_at__isnull=True,
        ).select_related('product')

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
                    # Send email reminder via lifecycle service
                    from catalog.services.booking_service import BookingLifecycleService
                    BookingLifecycleService.send_booking_email(
                        booking, 'booking_reminder',
                        {'hours_until': round(hours_until)},
                    )
                    booking.reminder_sent_at = now
                    booking.save(update_fields=['reminder_sent_at'])
                    sent_count += 1
                    logger.info(
                        f"Booking reminder sent for #{booking.pk} "
                        f"({reminder_hours}h before)"
                    )
                    break

        return {'sent': sent_count}
    except Exception as e:
        logger.exception(f"Error sending booking reminders: {e}")
        return {'sent': sent_count, 'error': str(e)}
