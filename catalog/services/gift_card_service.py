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
    def create_gift_cards_for_order(order) -> tuple[int, list[str]]:
        """
        Mint the gift cards an order paid for, then deliver them.

        Called once payment is confirmed. Two properties carry the risk:

        **Idempotent, by database constraint.** Every card claims a slot
        ``(order_item, issue_index)`` protected by a unique index. A retried
        webhook, an admin re-save, or a concurrent worker racing this one all
        lose the insert and skip, so an order can never mint a second set of
        funded cards. A count-then-create check would not do: both workers read
        zero before either commits.

        **Each slot gets its own savepoint.** An IntegrityError raised inside an
        enclosing atomic block aborts the whole Postgres transaction, so without
        the nested ``atomic()`` a single lost race would turn a double-mint into
        a *partial* mint — the customer paying for three cards and receiving
        one. That is worse than the problem being solved.

        Note there is deliberately NO ``@transaction.atomic`` on this method.
        Delivery sends real email, and email sent inside a transaction that
        later rolls back cannot be recalled: the recipient holds a code for a
        card that no longer exists.

        Returns:
            Tuple of (count, gift_card_codes) for cards minted by THIS call.
        """
        from django.db import IntegrityError

        created = []

        gift_card_items = order.items.filter(
            product__product_type="gift_card",
            parent_bundle__isnull=True,  # Bundle components are refused at add-to-cart
        )

        if not gift_card_items.exists():
            logger.debug(f"Order {order.order_number} has no gift card products")
            return 0, []

        for order_item in gift_card_items:
            # Cap minting at what the line's MONEY supports, not at its
            # quantity field.
            #
            # The unique index protects (order_item, issue_index), but it
            # cannot see that raising quantity on an ALREADY-PAID line opens
            # genuinely-unused slots. A later run would fill them with funded
            # cards nobody paid for.
            #
            # Quantity alone cannot distinguish that from the legitimate case
            # this must still handle — a crash after minting 1 of 3, which the
            # reconcile task exists to repair. Both look like
            # "existing < quantity on a paid order". Total price can tell them
            # apart: it is what the customer was actually charged.
            paid_quantity = order_item.quantity
            unit = order_item.unit_price
            total = order_item.total_price
            if unit and unit.amount > 0 and total is not None:
                affordable = int(total.amount // unit.amount)
                if affordable < paid_quantity:
                    logger.warning(
                        f"Order item {order_item.pk} says quantity="
                        f"{order_item.quantity} but {total} at {unit} each only "
                        f"covers {affordable}. Minting {affordable} — the rest "
                        f"was never paid for."
                    )
                    paid_quantity = affordable

            for index in range(paid_quantity):
                try:
                    with transaction.atomic():
                        gift_card = GiftCardService._create_gift_card_from_order_item(
                            order_item=order_item, order=order, issue_index=index
                        )
                except IntegrityError:
                    # Slot already claimed — this order line was minted before.
                    # Expected on any retry; not an error.
                    logger.info(
                        f"Gift card slot {index} on order item {order_item.pk} already "
                        f"issued; skipping"
                    )
                    continue
                except ValueError as exc:
                    # The line itself is unmintable — no recipient, for
                    # instance. Retrying will never fix it, so do not raise into
                    # the Celery task's retry loop, and do not abort the other
                    # lines on this order: a customer who bought three gifts
                    # should still receive the two that are well-formed.
                    #
                    # Surfaced to staff rather than only logged: the customer
                    # has paid and someone has to make this right by hand.
                    logger.error(
                        f"Cannot mint gift card slot {index} on order item {order_item.pk}: {exc}"
                    )
                    GiftCardService._flag_for_staff(
                        order,
                        f"Gift card on line '{order_item.product_name}' could not be "
                        f"issued: {exc}. The customer has paid — issue it manually "
                        f"from the gift card admin.",
                    )
                    break  # every slot on this line has the same defect
                created.append(gift_card)
                logger.info(f"Minted gift card {gift_card.code} for order {order.order_number}")

        # Delivery happens AFTER every card is committed, and outside any
        # transaction of ours. A send failure must not undo a mint: the card is
        # real, the customer paid for it, and `scheduled_send_at` leaves it in
        # the sweeper's queryset to retry.
        for gift_card in created:
            GiftCardService._deliver(gift_card)

        return len(created), [gc.code for gc in created]

    @staticmethod
    def _flag_for_staff(order, note: str) -> None:
        """Leave a staff-only OrderNote; never let note-writing break issuance."""
        try:
            from orders.models import OrderNote

            OrderNote.objects.create(order=order, note=note, is_customer_note=False)
        except Exception:
            logger.exception(f"Could not write staff note on order {order.pk}: {note}")

    @staticmethod
    def _deliver(gift_card) -> None:
        """Send or schedule a minted card, never raising into the mint loop."""
        try:
            if gift_card.scheduled_send_at and gift_card.scheduled_send_at > timezone.now():
                # Future-dated: the beat task picks it up. Nothing to do now.
                logger.info(
                    f"Gift card {gift_card.code} scheduled for {gift_card.scheduled_send_at}"
                )
                return
            if GiftCardService._send_gift_card_email(gift_card):
                gift_card.issued_at = timezone.now()
                gift_card.save(update_fields=["issued_at"])
        except Exception:
            # The card exists and is spendable; only delivery failed. Leaving
            # issued_at NULL keeps it in the sweeper's retry queryset.
            logger.exception(
                f"Delivery failed for gift card {gift_card.code}; the card is valid "
                f"and will be retried by send_scheduled_gift_card_emails"
            )

    @staticmethod
    def _create_gift_card_from_order_item(order_item, order, issue_index) -> "GiftCard":
        """
        Mint one gift card for one slot on an order line.

        Raises IntegrityError if the slot is already taken — that is the
        idempotency guarantee, and the caller treats it as "already issued".

        Args:
            order_item: OrderItem instance
            order: Order instance
            issue_index: 0-based slot within the line; claims the unique index

        Returns:
            GiftCard instance
        """

        from catalog.models import GiftCard, GiftCardTransaction

        product = order_item.product

        # Face value is what the customer paid for this line, in the currency
        # they paid in. No conversion.
        #
        # This used to convert into product.gift_card_currency at the spot rate,
        # falling back silently to the paid currency when the rate lookup
        # failed. Both branches are wrong under D5 (single-currency cards):
        #   * Converting means the customer pays GBP and receives a EUR card
        #     whose value was fixed by one day's rate — an open-ended,
        #     unhedgeable liability, which is the exact thing D5 exists to
        #     avoid.
        #   * The silent fallback issued a card in a currency the merchant did
        #     not intend, recorded only in a log line.
        # And under D5 a mismatched card is not merely risky but unspendable:
        # GiftCardTenderService.authorize_for_session refuses it outright.
        initial_value = order_item.unit_price
        conversion_note = ""

        # Recipient details come from OrderItem.gift_card_data, copied from the
        # cart at order creation and validated by GiftCardDataSerializer.
        #
        # This used to read order_item.customizations, which could never work:
        # CartService._validate_customizations rejects any payload when the
        # product has allow_customization=False, and reshapes values into
        # {option_id: {value, calculated_price}} — so recipient_email read back
        # a dict, not an address.
        #
        # The order.email / order.shipping_name fallbacks are gone deliberately.
        # Silently mailing a gift to the BUYER when the recipient is missing is
        # worse than failing loudly: the intended recipient never learns the
        # gift exists, and the buyer believes it was sent.
        data = order_item.gift_card_data or {}
        recipient_email = (data.get("recipient_email") or "").strip()
        if not recipient_email:
            raise ValueError(
                f"Order item {order_item.pk} has no gift card recipient; refusing "
                f"to mint a card with nowhere to send it"
            )
        recipient_name = data.get("recipient_name", "")
        sender_name = data.get("sender_name", "")
        message = data.get("message", "")
        scheduled_send_at = data.get("scheduled_send_at")

        # Calculate expiration date
        expires_at = None
        if product.gift_card_expires_days and product.gift_card_expires_days > 0:
            expires_at = timezone.now() + timedelta(days=product.gift_card_expires_days)

        # Generate unique code
        code = GiftCard.generate_code()

        # Create gift card (issued_at is set when email is actually sent)
        # scheduled_send_at is ALWAYS set, even for immediate delivery, so that
        # send_scheduled_gift_card_emails is a universal retry net. Previously a
        # failed immediate send left both scheduled_send_at and issued_at NULL,
        # and no query ever found the card again — the customer had paid and the
        # recipient heard nothing, permanently.
        send_at = scheduled_send_at or timezone.now()

        gift_card = GiftCard.objects.create(
            code=code,
            product=product,
            order_item=order_item,
            issue_index=issue_index,  # claims the unique slot; may raise IntegrityError
            initial_value=initial_value,
            current_balance=initial_value,
            recipient_email=recipient_email,
            recipient_name=recipient_name,
            sender_name=sender_name,
            message=message,
            is_active=True,
            expires_at=expires_at,
            scheduled_send_at=send_at,
            # issued_at is stamped only on a genuine send, by _deliver()
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

        # No sending here. Delivery is the caller's second pass, outside any
        # transaction — see create_gift_cards_for_order. Sending from inside the
        # savepoint meant a later rollback un-created a card whose code was
        # already in a recipient's inbox.
        return gift_card

    @staticmethod
    def _send_gift_card_email(gift_card) -> bool:
        """
        Send gift card delivery email to recipient.

        Delegates to :meth:`catalog.models.GiftCard.send_delivery_email`, which
        sends via ``EmailSendingService`` (the real email API) and — importantly
        — does **not** touch ``issued_at``. The caller owns that, so a failed
        send stays retryable.

        This method previously imported
        ``email_system.services.email_service.EmailService``, a module that does
        not exist (the real one is ``email_system.services.email_sender``). The
        resulting ImportError was swallowed, so it returned False on every call,
        silently — and the ``send_scheduled_gift_card_emails`` beat task, which
        runs every 300s, drained into it and could never deliver anything.

        Args:
            gift_card: GiftCard instance

        Returns:
            bool: True if the email was sent.
        """
        sent = gift_card.send_delivery_email()
        if sent:
            logger.info(f"Gift card {gift_card.code} email sent to {gift_card.recipient_email}")
        else:
            logger.error(f"Failed to send gift card email for {gift_card.code}")
        return sent

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
                # Zero the balance as well as deactivating. The ledger row below
                # records -initial_value; leaving current_balance at its full
                # face value made the two disagree, so reconciliation
                # (balance == initial - redemptions + refunds + adjustments)
                # failed on every refunded card.
                from djmoney.money import Money

                zero = Money(0, gift_card.current_balance.currency)
                gift_card.is_active = False
                gift_card.current_balance = zero
                gift_card.save(update_fields=["is_active", "current_balance"])

                # Create refund transaction
                GiftCardTransaction.objects.create(
                    gift_card=gift_card,
                    transaction_type="refund",
                    amount=-gift_card.initial_value,
                    balance_after=zero,
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

        # --- Part 2: gift cards USED AS PAYMENT — deliberately disabled ---
        #
        # This restored the FULL original redemption whenever an order was
        # refunded, regardless of how much was actually refunded: refund £20 of
        # a £200 order paid entirely by gift card and the customer got all £200
        # back on the card while also receiving the £20. It wrote no
        # PaymentTransaction refund row either, so the tender ledger and the
        # gift card ledger disagreed afterwards.
        #
        # It was only ever dead because order_item was never populated —
        # issuance had never run. P2.3 makes issuance real, which would have
        # brought this to life too.
        #
        # Refunds to a gift card tender belong to the tender rail
        # (PaymentTransaction capture rows), and are P2.4's TenderRefundAllocator.
        # Refusing loudly is better than a partly-correct restore that silently
        # over-credits.
        redeemed_here = GiftCardTransaction.objects.filter(
            order=order, transaction_type="redemption"
        ).exists()
        if redeemed_here:
            logger.warning(
                f"Order {order.order_number} was paid at least partly by gift card. "
                f"Automatic balance restoration is disabled — it used to refund the "
                f"whole original redemption regardless of the refunded amount. "
                f"Adjust the card by hand from the gift card admin until P2.4 ships "
                f"tender-aware refunds."
            )

        return processed_count

    @staticmethod
    def cart_contains_gift_card(items) -> bool:
        """
        True if any line in ``items`` is a gift card product.

        A gift card must never pay for another gift card: it converts a
        traceable instrument into a fresh one with a reset expiry and no chain
        back to the original purchase, which is a laundering step for a stolen
        code.

        Shared because the rule has to hold on every channel.
        ``GiftCardTenderService.authorize_for_session`` covers web checkout, but
        POS never calls it — ``checkout_gift_card`` and ``_pay_multi`` go
        straight to ``validate_card``/``deduct_balance`` — so without this the
        till would happily sell a gift card paid for with another gift card.

        Args:
            items: any queryset or iterable of CartItem/OrderItem.
        """
        try:
            return items.filter(product__product_type="gift_card").exists()
        except AttributeError:
            return any(getattr(i.product, "product_type", None) == "gift_card" for i in items)

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
