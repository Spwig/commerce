"""
Gift Card Service - Business logic for gift card creation and management
"""

import logging
from datetime import timedelta
from typing import TYPE_CHECKING

from django.db import transaction
from django.utils import timezone

if TYPE_CHECKING:
    from catalog.models import GiftCard

logger = logging.getLogger(__name__)


class GiftCardService:
    """Service class for gift card operations"""

    @staticmethod
    @transaction.atomic
    def create_gift_cards_for_order(order) -> tuple[int, list[str]]:
        """
        Create gift cards for all gift card products in an order after payment is completed.

        This method should be called after payment is confirmed (transaction status = 'completed').

        Args:
            order: Order instance with confirmed payment

        Returns:
            Tuple of (count: int, gift_card_codes: List[str])
        """

        created_codes = []

        # Get all order items for gift card products
        gift_card_items = order.items.filter(
            product__product_type="gift_card",
            parent_bundle__isnull=True,  # Only process top-level items, not bundle components
        )

        if not gift_card_items.exists():
            logger.debug(f"Order {order.order_number} has no gift card products")
            return 0, []

        for order_item in gift_card_items:
            # Create one gift card per quantity
            for _i in range(order_item.quantity):
                try:
                    gift_card = GiftCardService._create_gift_card_from_order_item(
                        order_item=order_item, order=order
                    )
                    created_codes.append(gift_card.code)
                    logger.info(
                        f"Created gift card {gift_card.code} for order {order.order_number}"
                    )

                except Exception as e:
                    logger.error(f"Failed to create gift card for order item {order_item.id}: {e}")
                    # Continue creating other gift cards even if one fails
                    continue

        return len(created_codes), created_codes

    @staticmethod
    def _create_gift_card_from_order_item(order_item, order) -> "GiftCard":
        """
        Create a single gift card from an order item.

        Args:
            order_item: OrderItem instance
            order: Order instance

        Returns:
            GiftCard instance
        """
        from djmoney.money import Money

        from catalog.models import GiftCard, GiftCardTransaction

        product = order_item.product

        # Get gift card value from order item price (base currency)
        initial_value = order_item.unit_price
        conversion_note = ""

        # Convert to target currency if product specifies a gift card currency
        target_currency = product.gift_card_currency
        if target_currency and str(initial_value.currency) != target_currency:
            try:
                from exchange_rates.services.exchange_service import ExchangeRateService

                fx_service = ExchangeRateService()
                converted_amount = fx_service.convert(
                    initial_value.amount, str(initial_value.currency), target_currency
                )
                rate_used = fx_service.get_rate(str(initial_value.currency), target_currency)
                conversion_note = (
                    f" | Converted from {initial_value} at rate "
                    f"{str(initial_value.currency)}->{target_currency}: {rate_used}"
                )
                initial_value = Money(converted_amount, target_currency)
                logger.info(
                    f"Gift card value converted: {order_item.unit_price} -> {initial_value} "
                    f"(rate: {rate_used})"
                )
            except Exception as e:
                logger.error(
                    f"Failed to convert gift card value to {target_currency}: {e}. "
                    f"Falling back to base currency."
                )
                # Fall back to base currency if conversion fails
                conversion_note = (
                    f" | Currency conversion to {target_currency} failed, using base currency"
                )

        # Get recipient information from order item customizations
        customizations = order_item.customizations or {}
        recipient_email = customizations.get("recipient_email", order.email)
        recipient_name = customizations.get("recipient_name", "")
        sender_name = customizations.get("sender_name", order.shipping_name)
        message = customizations.get("message", "")
        scheduled_send_date = customizations.get("scheduled_send_date")

        # Calculate expiration date
        expires_at = None
        if product.gift_card_expires_days and product.gift_card_expires_days > 0:
            expires_at = timezone.now() + timedelta(days=product.gift_card_expires_days)

        # Generate unique code
        code = GiftCard.generate_code()

        # Create gift card (issued_at is set when email is actually sent)
        gift_card = GiftCard.objects.create(
            code=code,
            product=product,
            order_item=order_item,
            initial_value=initial_value,
            current_balance=initial_value,
            recipient_email=recipient_email,
            recipient_name=recipient_name,
            sender_name=sender_name,
            message=message,
            is_active=True,
            expires_at=expires_at,
            # issued_at is set when email is sent, not at creation
        )

        # Create initial transaction record
        GiftCardTransaction.objects.create(
            gift_card=gift_card,
            transaction_type="issue",
            amount=initial_value,
            balance_after=initial_value,
            order=order,
            notes=f"Gift card issued from order {order.order_number}{conversion_note}",
            created_by=order.user if order.user else None,
        )

        # Schedule or send email delivery
        if scheduled_send_date:
            # Schedule for future delivery - Celery task will set issued_at
            GiftCardService._schedule_gift_card_email(gift_card, scheduled_send_date)
        else:
            # Send immediately and set issued_at on success
            if GiftCardService._send_gift_card_email(gift_card):
                gift_card.issued_at = timezone.now()
                gift_card.save(update_fields=["issued_at"])

        return gift_card

    @staticmethod
    def _send_gift_card_email(gift_card) -> bool:
        """
        Send gift card delivery email to recipient.

        Args:
            gift_card: GiftCard instance

        Returns:
            bool: True if email sent successfully
        """
        from django.contrib.sites.models import Site

        from email_system.services.email_service import EmailService

        try:
            site = Site.objects.get(pk=1)

            # Build context for email template
            context = {
                "gift_card": gift_card,
                "shop_url": f"https://{site.domain}",
                "check_balance_url": f"https://{site.domain}/gift-cards/check-balance/",
            }

            # Send email using email service
            EmailService.send_transactional_email(
                template_type="gift_card_delivery",
                recipient_email=gift_card.recipient_email,
                recipient_name=gift_card.recipient_name or gift_card.recipient_email,
                context=context,
                site=site,
            )

            logger.info(f"Gift card {gift_card.code} email sent to {gift_card.recipient_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send gift card email for {gift_card.code}: {e}")
            return False

    @staticmethod
    def _schedule_gift_card_email(gift_card, send_date) -> bool:
        """
        Schedule gift card delivery email for future date.

        The scheduled email is sent by the Celery task `catalog.send_scheduled_gift_card_emails`
        which runs periodically and picks up gift cards with scheduled_send_at <= now.

        Args:
            gift_card: GiftCard instance
            send_date: Date/time to send email (can be string or datetime)

        Returns:
            bool: True if scheduled successfully
        """
        from datetime import datetime

        from django.utils import timezone

        try:
            # Parse send_date if it's a string
            if isinstance(send_date, str):
                send_date = datetime.fromisoformat(send_date.replace("Z", "+00:00"))

            # Make sure it's timezone aware
            if send_date.tzinfo is None:
                send_date = timezone.make_aware(send_date)

            # Set the scheduled_send_at field
            gift_card.scheduled_send_at = send_date
            gift_card.save(update_fields=["scheduled_send_at"])

            logger.info(f"Gift card {gift_card.code} scheduled for delivery on {send_date}")
            return True

        except Exception as e:
            logger.error(f"Failed to schedule gift card {gift_card.code}: {e}")
            # Fall back to immediate send
            return GiftCardService._send_gift_card_email(gift_card)

    @staticmethod
    @transaction.atomic
    def process_gift_card_refund(order) -> int:
        """
        Handle gift card refunds when an order is refunded.

        This handles two scenarios:
        1. Gift cards PURCHASED in this order - deactivate them if unused
        2. Gift cards USED AS PAYMENT for this order - restore their balance

        Args:
            order: Order instance being refunded

        Returns:
            int: Number of gift cards processed
        """
        from catalog.models import GiftCard, GiftCardTransaction

        processed_count = 0

        # --- Part 1: Gift cards PURCHASED in this order ---
        # Exclude GCs that already have a refund transaction for this order
        already_deactivated_gc_ids = GiftCardTransaction.objects.filter(
            order=order, transaction_type="refund", gift_card__order_item__order=order
        ).values_list("gift_card_id", flat=True)

        purchased_gift_cards = GiftCard.objects.filter(order_item__order=order).exclude(
            id__in=already_deactivated_gc_ids
        )

        for gift_card in purchased_gift_cards:
            # Only refund if gift card hasn't been used yet
            if gift_card.current_balance == gift_card.initial_value:
                # Deactivate gift card
                gift_card.is_active = False
                gift_card.save(update_fields=["is_active"])

                # Create refund transaction
                GiftCardTransaction.objects.create(
                    gift_card=gift_card,
                    transaction_type="refund",
                    amount=-gift_card.initial_value,
                    balance_after=gift_card.current_balance,
                    order=order,
                    notes=f"Gift card deactivated due to order {order.order_number} refund",
                    created_by=None,
                )

                processed_count += 1
                logger.info(f"Deactivated gift card {gift_card.code} due to order refund")
            else:
                # Gift card has been partially used - log warning
                logger.warning(
                    f"Gift card {gift_card.code} has been used "
                    f"(balance: {gift_card.current_balance} of {gift_card.initial_value}). "
                    f"Cannot auto-refund. Manual adjustment required."
                )

        # --- Part 2: Gift cards USED AS PAYMENT for this order ---
        # Guard against double-refund: only process redemptions that don't already
        # have a corresponding refund transaction for this order
        already_refunded_gc_ids = GiftCardTransaction.objects.filter(
            order=order,
            transaction_type="refund",
            amount__gt=0,  # Positive refund = balance restoration (Part 2)
        ).values_list("gift_card_id", flat=True)

        redemption_transactions = (
            GiftCardTransaction.objects.filter(order=order, transaction_type="redemption")
            .exclude(gift_card_id__in=already_refunded_gc_ids)
            .select_related("gift_card")
        )

        for txn in redemption_transactions:
            gift_card = txn.gift_card
            # The redemption amount is stored as negative, so negate it to get positive
            restore_amount = abs(txn.amount)

            try:
                # Restore the balance
                new_balance = gift_card.current_balance + restore_amount
                gift_card.current_balance = new_balance
                gift_card.is_active = True  # Re-activate if it was fully redeemed
                gift_card.save(update_fields=["current_balance", "is_active"])

                # Create refund transaction
                GiftCardTransaction.objects.create(
                    gift_card=gift_card,
                    transaction_type="refund",
                    amount=restore_amount,
                    balance_after=new_balance,
                    order=order,
                    notes=f"Balance restored due to order {order.order_number} refund",
                    created_by=None,
                )

                processed_count += 1
                logger.info(
                    f"Restored {restore_amount} to gift card {gift_card.code} "
                    f"due to order {order.order_number} refund"
                )
            except Exception as e:
                logger.error(
                    f"Failed to restore gift card {gift_card.code} balance "
                    f"for order {order.order_number} refund: {e}"
                )

        return processed_count

    @staticmethod
    def check_balance(code: str) -> dict | None:
        """
        Check gift card balance without requiring authentication.

        Args:
            code: Gift card code

        Returns:
            dict with gift card info or None if not found
        """
        from catalog.models import GiftCard

        try:
            gift_card = GiftCard.objects.get(code=code)

            return {
                "code": gift_card.code,
                "current_balance": {
                    "amount": str(gift_card.current_balance.amount),
                    "currency": gift_card.current_balance.currency.code,
                },
                "initial_value": {
                    "amount": str(gift_card.initial_value.amount),
                    "currency": gift_card.initial_value.currency.code,
                },
                "is_active": gift_card.is_active,
                "is_expired": gift_card.is_expired,
                "is_valid": gift_card.is_valid,
                "expires_at": gift_card.expires_at.isoformat() if gift_card.expires_at else None,
                "redemption_percentage": gift_card.redemption_percentage,
            }
        except GiftCard.DoesNotExist:
            return None

    @staticmethod
    def validate_card(code: str) -> tuple[bool, any]:
        """
        Validate a gift card code and return its balance.

        Used by POS checkout to verify gift card before payment.

        Args:
            code: Gift card code to validate

        Returns:
            Tuple of (is_valid: bool, balance_or_error: Decimal | str)
            - On success: (True, current_balance as Decimal)
            - On failure: (False, error_message as str)
        """
        from catalog.models import GiftCard

        try:
            gift_card = GiftCard.objects.get(code=code)

            if not gift_card.is_active:
                return False, "Gift card is not active"

            if gift_card.is_expired:
                return False, "Gift card has expired"

            if gift_card.is_fully_redeemed:
                return False, "Gift card has no remaining balance"

            if not gift_card.is_valid:
                return False, "Gift card is not valid"

            # Return the balance as a Decimal (not Money object)
            return True, gift_card.current_balance.amount

        except GiftCard.DoesNotExist:
            return False, "Gift card not found"
        except Exception as e:
            logger.error(f"Error validating gift card {code}: {e}")
            return False, "Error validating gift card"

    @staticmethod
    @transaction.atomic
    def deduct_balance(code: str, amount, order=None, notes: str = "") -> tuple[bool, str]:
        """
        Deduct an amount from a gift card balance.

        Used by POS checkout to process gift card payments.

        Args:
            code: Gift card code
            amount: Amount to deduct (Decimal or Money)
            order: Optional Order this is being redeemed for
            notes: Optional notes about the redemption

        Returns:
            Tuple of (success: bool, message: str)
        """
        from decimal import Decimal

        from djmoney.money import Money

        from catalog.models import GiftCard

        try:
            # Lock the gift card row to prevent concurrent balance depletion (TOCTOU)
            gift_card = GiftCard.objects.select_for_update().get(code=code)

            # Convert amount to Money if it's a Decimal
            if isinstance(amount, (Decimal, int, float)):
                amount = Money(Decimal(str(amount)), gift_card.current_balance.currency)

            # Check if redemption is allowed
            can_redeem, error_msg = gift_card.can_redeem(amount)
            if not can_redeem:
                return False, error_msg

            # Perform redemption
            gift_card.redeem(amount=amount, order=order, notes=notes or "POS payment redemption")

            logger.info(
                f"Gift card {code} deducted {amount} - new balance: {gift_card.current_balance}"
            )

            return True, f"Deducted {amount} from gift card"

        except GiftCard.DoesNotExist:
            return False, "Gift card not found"
        except Exception as e:
            logger.error(f"Error deducting from gift card {code}: {e}")
            return False, f"Error processing gift card: {str(e)}"
