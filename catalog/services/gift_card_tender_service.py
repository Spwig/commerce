"""
Gift cards as a payment tender.

A gift card is money the customer already handed over, so it behaves like a
payment method rather than a discount. That distinction is the whole point of
this service:

* A **discount** reduces the bill before tax and is capped at the subtotal. That
  is what ``cart.AppliedGiftCard`` did until P2.2f, and it meant a $200 card against
  a $100 + $10 tax + $10 shipping order covers only $100 and still charges $20
  to a card — while $100 of the customer's own money sits unused.
* A **tender** settles the full post-tax total, does not touch the tax base, and
  is not a "saving" in any report.

The lifecycle mirrors a card payment, recorded as ``PaymentTransaction`` rows:

    authorize  -- a hold placed when the customer keys the code at checkout.
                  Reserves value WITHOUT debiting the card, so an abandoned
                  checkout costs the customer nothing.
    capture    -- on payment confirmation. Debits the card, writes the ledger
                  entry, voids the hold.
    void       -- releases a hold (abandoned or superseded checkout).
    refund     -- returns captured value to the card.

The rows are append-only: an authorize row is never mutated into a capture, so
both the hold and its settlement remain visible afterwards.

This is the ONLY code that should move gift card balance during checkout.
``GiftCard.redeem`` is the primitive it calls; nothing else should call that
directly on a checkout path.
"""

import logging
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction as db_transaction
from django.db.models import Q
from djmoney.money import Money

logger = logging.getLogger(__name__)


class GiftCardTenderError(Exception):
    """A tender operation could not be completed."""


class InsufficientGiftCardBalance(GiftCardTenderError):
    """The card cannot cover the requested amount (after existing holds)."""


class GiftCardTenderService:
    """Place, settle and release gift card holds against a checkout."""

    # Holds older than this are treated as abandoned and swept. Long enough to
    # survive a redirect-based payment provider round trip, short enough that an
    # abandoned basket does not strand a customer's balance for hours.
    HOLD_MINUTES = 30

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _lock_cards(card_ids):
        """
        Lock cards in a deterministic order.

        Two checkouts touching the same two cards in opposite orders will
        deadlock; ordering by pk means everyone queues the same way.
        """
        from catalog.models import GiftCard

        return list(
            GiftCard.objects.select_for_update().filter(pk__in=sorted(card_ids)).order_by("pk")
        )

    @staticmethod
    def _auth_txn_id(session_id, card_id):
        # Doubles as the idempotency key: PaymentTransaction.transaction_id is
        # unique, so a retried authorize collides instead of double-holding.
        return f"gc-auth:{session_id}:{card_id}"

    @staticmethod
    def _capture_txn_id(order_id, card_id):
        return f"gc-cap:{order_id}:{card_id}"

    @staticmethod
    def _refund_txn_id(capture, refund_ref, positional):
        """
        Idempotency key for one refund leg of a capture.

        Prefers the caller's stable ``refund_ref`` so a retried refund resolves
        to the same id; falls back to a positional counter, which is only safe
        for a first attempt.
        """
        suffix = refund_ref if refund_ref is not None else positional
        return f"gc-ref:{capture.transaction_id}:{suffix}"

    # ------------------------------------------------------------------
    # authorize
    # ------------------------------------------------------------------

    @classmethod
    @db_transaction.atomic
    def authorize_for_session(cls, checkout_session, code, amount=None):
        """
        Place a hold on a gift card for an in-progress checkout.

        Args:
            checkout_session: CheckoutSession the hold belongs to.
            code: Gift card code as typed by the customer.
            amount: Money to hold. Defaults to the card's whole available
                balance.

                Deliberately not capped against ``session.amount_due`` here.
                A hold is a reservation, not a movement — over-holding costs
                the customer nothing permanent, the sweeper releases it, and
                ``capture_for_order`` caps the actual debit at what the order
                turns out to cost. Making the default depend on session totals
                would couple authorize to whether those totals happen to be
                computed yet, and hold nothing at all for a session whose
                ``amount_due`` reads zero. Callers that know what they owe
                (the checkout view does) pass it explicitly.

        Returns:
            PaymentTransaction: the authorize row.

        Raises:
            GiftCardTenderError: card unusable, or currency mismatch.
            InsufficientGiftCardBalance: nothing left to hold.
        """
        from catalog.models import GiftCard
        from payment_providers.models import PaymentTransaction

        try:
            card = GiftCard.objects.select_for_update().get(code=code)
        except GiftCard.DoesNotExist:
            raise GiftCardTenderError("Gift card not found") from None

        if not card.is_valid:
            raise GiftCardTenderError("This gift card is not valid")

        # A gift card must not buy another gift card. Allowing it converts a
        # traceable instrument into a fresh one — resetting expiry, breaking the
        # chain back to the original purchase, and giving anyone holding a stolen
        # code a laundering step. The rule used to live in `Cart.apply_gift_card`,
        # which P2.2f deleted, so it is enforced here now.
        #
        # Live as of P2.3, which made gift cards purchasable. POS enforces the
        # same rule separately in checkout_gift_card and checkout_split, which
        # never reach this method.
        cart = getattr(checkout_session, "cart", None)
        if cart is not None and cart.items.filter(product__product_type="gift_card").exists():
            raise GiftCardTenderError("A gift card cannot be used to buy another gift card")

        currency = card.current_balance.currency

        # A hold in a different currency from the card would make held_amount
        # unsummable, so refuse rather than guess a conversion here.
        if amount is not None and amount.currency != currency:
            raise GiftCardTenderError(
                f"Hold currency {amount.currency} does not match the card's {currency}"
            )

        # Supersede this session's own earlier holds FIRST, before working out
        # what is available. The customer re-submitting (typo, changed mind,
        # back button) must not be told their own previous hold has used up the
        # card — and if the default amount were computed first, a re-entry would
        # hold less than it should.
        #
        # Voids EVERY outstanding hold for this (session, card), not just the
        # one whose id matches the base string. The previous version looked up
        # only the base id and suffixed it with that row's pk: on a third
        # attempt it re-found the first (already voided) hold, derived the same
        # suffixed id as the second, and died on the unique constraint — while
        # leaving the second hold live, so the card was double-held. Three
        # attempts produced a 500.
        base_id = cls._auth_txn_id(checkout_session.pk, card.pk)
        superseded = PaymentTransaction.objects.filter(
            gift_card=card,
            checkout_session=checkout_session,
            tender_type=PaymentTransaction.TENDER_GIFT_CARD,
            transaction_type="authorize",
            status="authorized",
        ).update(status="voided")
        if superseded:
            logger.info(
                f"Superseded {superseded} existing hold(s) on {card.code} "
                f"for checkout {checkout_session.pk}"
            )
            card.refresh_from_db()

        available = card.available_balance
        if available.amount <= 0:
            raise InsufficientGiftCardBalance(f"Gift card {card.code} has no available balance")

        if amount is None:
            amount = available
        elif amount > available:
            raise InsufficientGiftCardBalance(
                f"Gift card has {available} available, cannot hold {amount}"
            )

        # Derive a genuinely unique id rather than one built from a row we
        # happened to find. Holds for this pair are all voided by now, so the
        # only collisions are with historical ids.
        txn_id = base_id
        attempt = 0
        while PaymentTransaction.objects.filter(transaction_id=txn_id).exists():
            attempt += 1
            txn_id = f"{base_id}:{attempt}"

        hold = PaymentTransaction.objects.create(
            transaction_id=txn_id,
            tender_type=PaymentTransaction.TENDER_GIFT_CARD,
            transaction_type="authorize",
            status="authorized",
            gift_card=card,
            checkout_session=checkout_session,
            amount=amount,
            settlement_amount=amount,
            exchange_rate=Decimal("1.00000000"),
            provider_account=None,
        )
        logger.info(f"Held {amount} on gift card {card.code} for checkout {checkout_session.pk}")
        return hold

    # ------------------------------------------------------------------
    # capture
    # ------------------------------------------------------------------

    @classmethod
    @db_transaction.atomic
    def capture_for_order(cls, order, checkout_session=None):
        """
        Settle every hold attached to a paid order.

        Called once payment is confirmed. Debits each card, writes its ledger
        entry, and voids the hold — all inside one transaction, so a partial
        settlement cannot leave some cards debited and others still held.

        Idempotent: a capture row already present for an (order, card) pair is
        left alone, so a retried payment webhook cannot double-charge a card.

        **Captures are capped at what the order actually costs.** A hold is
        sized when the customer keys the card, and the cart can shrink after
        that — go back, remove an item, return to checkout. The hold is still
        the old, larger figure. Debiting it in full would take money the order
        never needed: a 100 hold against an order that ended up at 50 would
        leave the customer 50 short with nothing to show for it. So each hold
        captures ``min(hold.amount, still owed)``, and a hold with nothing left
        to cover is voided rather than captured.

        Returns:
            list[PaymentTransaction]: the capture rows (existing or new).
        """
        from payment_providers.models import PaymentTransaction

        outstanding = PaymentTransaction.objects.filter(
            tender_type=PaymentTransaction.TENDER_GIFT_CARD,
            transaction_type="authorize",
            status="authorized",
        )
        # Holds are attached to the checkout session while the order does not
        # exist yet, and stamped with the order once it does — so look for both.
        scope = Q(order=order)
        if checkout_session is not None:
            scope |= Q(checkout_session=checkout_session)
        holds = list(outstanding.filter(scope))
        if not holds:
            return []

        cls._lock_cards({h.gift_card_id for h in holds})

        # What the order still needs, after EVERY completed capture and charge
        # REGARDLESS of tender type — not just gift card rows.
        #
        # Subtracting only own-type captures was correct by accident while
        # gift cards were the sole internal tender (holds + gateway charge
        # summed to the total exactly). With a second rail, each service
        # capping at "total minus my own captures" lets a cart that shrank
        # between hold and payment be jointly over-captured: both rails
        # believe the same residue is theirs. Wallet capture uses the same
        # all-tender subtraction; whichever runs second sees the first's rows.
        remaining = order.total_amount
        already_captured = PaymentTransaction.objects.filter(
            order=order,
            transaction_type__in=("capture", "charge"),
            status="completed",
        )
        for prior in already_captured:
            remaining -= prior.settlement_amount or prior.amount

        captures = []
        for hold in holds:
            capture_id = cls._capture_txn_id(order.pk, hold.gift_card_id)
            existing = PaymentTransaction.objects.filter(transaction_id=capture_id).first()
            if existing:
                logger.info(
                    f"Gift card {hold.gift_card.code} already captured for order "
                    f"{order.pk}; leaving it alone"
                )
                captures.append(existing)
                continue

            card = hold.gift_card

            # The cart may have shrunk since this hold was placed. Never debit
            # more than the order still owes.
            capture_amount = min(hold.amount, remaining)
            if capture_amount.amount <= 0:
                hold.status = "voided"
                hold.order = order
                hold.save(update_fields=["status", "order", "updated_at"])
                logger.info(
                    f"Voided hold of {hold.amount} on gift card {card.code}: order "
                    f"{order.pk} is already fully covered, nothing left to capture"
                )
                continue

            if capture_amount < hold.amount:
                logger.info(
                    f"Capping capture on gift card {card.code} at {capture_amount} "
                    f"(hold was {hold.amount}) — order {order.pk} costs less than "
                    f"when the card was keyed"
                )

            # redeem() locks, validates, debits and writes the ledger row.
            card.redeem(
                amount=capture_amount,
                order=order,
                notes=f"Gift card tender for order {order.order_number}",
            )

            capture = PaymentTransaction.objects.create(
                transaction_id=capture_id,
                tender_type=PaymentTransaction.TENDER_GIFT_CARD,
                transaction_type="capture",
                status="completed",
                gift_card=card,
                order=order,
                parent_transaction=hold,
                amount=capture_amount,
                settlement_amount=capture_amount,
                exchange_rate=hold.exchange_rate,
                provider_account=None,
            )
            remaining -= capture_amount

            # Append-only: the hold is voided, never rewritten as the capture.
            hold.status = "voided"
            hold.order = order
            hold.save(update_fields=["status", "order", "updated_at"])

            captures.append(capture)
            logger.info(
                f"Captured {capture_amount} from gift card {card.code} for order {order.pk}"
            )

        return captures

    # ------------------------------------------------------------------
    # void
    # ------------------------------------------------------------------

    @classmethod
    @db_transaction.atomic
    def void_holds(cls, checkout_session=None, order=None, reason=""):
        """
        Release holds without debiting anything.

        Used when a checkout is abandoned, superseded, or fails. Nothing was
        debited at authorize time, so this only frees the reservation.

        Returns:
            int: number of holds released.
        """
        from payment_providers.models import PaymentTransaction

        if not checkout_session and not order:
            raise ValueError("void_holds needs a checkout_session or an order")

        qs = PaymentTransaction.objects.filter(
            tender_type=PaymentTransaction.TENDER_GIFT_CARD,
            transaction_type="authorize",
            status="authorized",
        )
        qs = (
            qs.filter(checkout_session=checkout_session)
            if checkout_session
            else qs.filter(order=order)
        )

        released = qs.update(status="voided")
        if released:
            logger.info(f"Released {released} gift card hold(s): {reason or 'no reason given'}")
        return released

    @classmethod
    @db_transaction.atomic
    def expire_stale_holds(cls):
        """
        Sweep holds left behind by abandoned checkouts.

        Without this, a customer who keys a code and walks away has their
        balance reserved indefinitely — the card looks empty to them while no
        money has actually moved.
        """
        from datetime import timedelta

        from django.utils import timezone

        from payment_providers.models import PaymentTransaction

        cutoff = timezone.now() - timedelta(minutes=cls.HOLD_MINUTES)
        stale = PaymentTransaction.objects.filter(
            tender_type=PaymentTransaction.TENDER_GIFT_CARD,
            transaction_type="authorize",
            status="authorized",
            created_at__lt=cutoff,
            order__isnull=True,
        )
        count = stale.update(status="voided")
        if count:
            logger.info(f"Expired {count} stale gift card hold(s) older than {cls.HOLD_MINUTES}m")
        return count

    # ------------------------------------------------------------------
    # refund
    # ------------------------------------------------------------------

    @classmethod
    def _mint_replacement(cls, capture, dead_card, amount, reason="", txn_id=None):
        """
        Issue a fresh card carrying a refund the original can no longer hold.

        Addressed to the DEAD CARD's recipient, never to the order's buyer.
        A gift card is a bearer instrument: the person entitled to this value is
        whoever the card was for, and on a gift that is not the person who paid.
        Defaulting to order.email would quietly transfer a recipient's money to
        the buyer.

        No expiry. The customer already lost one card to time or deactivation
        through no act of their own; handing the value back on the same clock
        invites the same loss again.
        """
        from django.utils import timezone

        from catalog.models import GiftCard
        from payment_providers.models import PaymentTransaction

        recipient = (dead_card.recipient_email or "").strip()
        if not recipient:
            raise GiftCardTenderError(
                f"Gift card {dead_card.code} cannot hold this refund and has no "
                f"recipient on record, so a replacement cannot be addressed. "
                f"Refund this leg by hand."
            )

        replacement = GiftCard.objects.create(
            product=dead_card.product,
            initial_value=amount,
            current_balance=amount,
            recipient_email=recipient,
            recipient_name=dead_card.recipient_name,
            sender_name=dead_card.sender_name,
            message=f"Replacement for {dead_card.code}",
            is_active=True,
            expires_at=None,
            scheduled_send_at=timezone.now(),
        )
        logger.warning(
            f"Gift card {dead_card.code} could not receive a {amount} refund "
            f"(active={dead_card.is_active}, expired={dead_card.is_expired}); "
            f"minted replacement {replacement.code} for {recipient}"
        )

        return PaymentTransaction.objects.create(
            transaction_id=txn_id,
            tender_type=PaymentTransaction.TENDER_GIFT_CARD,
            transaction_type="refund",
            status="completed",
            gift_card=replacement,
            order=capture.order,
            parent_transaction=capture,
            amount=amount,
            settlement_amount=amount,
            exchange_rate=capture.exchange_rate,
            provider_account=None,
        )

    @classmethod
    @db_transaction.atomic
    def refund_to_card(cls, capture, amount=None, reason="", refund_ref=None):
        """
        Return captured value to the gift card.

        Args:
            capture: the capture PaymentTransaction being refunded.
            amount: Money to return. Defaults to the full captured amount.
            reason: recorded on the ledger entry.
            refund_ref: stable identifier for THIS refund attempt, used as the
                idempotency key. Pass the caller's refund pk. Without it the key
                falls back to a positional counter, which is not idempotent —
                see below.

        Raises:
            GiftCardTenderError: if this would refund more than was captured.
        """
        from payment_providers.models import PaymentTransaction

        if capture.transaction_type not in ("capture", "charge"):
            raise GiftCardTenderError(f"Cannot refund a {capture.transaction_type} transaction")

        # Default only when the caller passed nothing. `amount or capture.amount`
        # treated Money(0) as falsy — silently turning a zero refund into a full
        # one — and never rejected negatives, which would DEBIT the card.
        if amount is None:
            amount = capture.amount
        if amount.amount <= 0:
            raise GiftCardTenderError("Refund amount must be a positive value")
        if amount.currency != capture.amount.currency:
            raise GiftCardTenderError("Refund currency must match the capture")

        # Serialize refunds of the same capture. Locking the capture row means
        # the capacity read, balance move and refund-row write below cannot
        # interleave with a concurrent refund of the same capture — otherwise
        # two refunds with different refs both read the same prior total, both
        # pass the limit check, and jointly exceed what was captured.
        capture = PaymentTransaction.objects.select_for_update().get(pk=capture.pk)

        # Pending counts as well as completed, or two concurrent refunds are
        # each told the same capacity is free.
        already = PaymentTransaction.objects.filter(
            parent_transaction=capture,
            transaction_type="refund",
            status__in=("pending", "completed"),
        )

        # Resolve the idempotency key BEFORE moving any balance and return the
        # existing leg if this refund already ran. Crediting first and creating
        # the uniquely keyed row second meant a retry with the same refund_ref
        # re-credited the card and then died on the unique constraint.
        txn_id = cls._refund_txn_id(capture, refund_ref, already.count() + 1)
        existing = PaymentTransaction.objects.filter(transaction_id=txn_id).first()
        if existing:
            return existing

        refunded = sum((t.amount for t in already), Money(Decimal("0"), capture.amount.currency))
        if refunded + amount > capture.amount:
            raise GiftCardTenderError(
                f"Refunding {amount} would exceed the {capture.amount} captured "
                f"({refunded} already refunded)"
            )

        card = capture.gift_card

        # A card that has expired or been deactivated cannot hold the refund:
        # crediting it returns value the customer can never spend. Mint a
        # replacement instead, addressed to whoever the dead card was for.
        #
        # Note a ZERO-BALANCE card is still creditable — being spent out is not
        # the same as being dead.
        #
        # EXPIRED and DEACTIVATED are treated differently, deliberately.
        # Expiry is a clock event the customer had no hand in, so a refund
        # mints a fresh no-expiry card. Deactivation is a MERCHANT decision —
        # a card frozen for a chargeback or flagged as bought with a stolen
        # instrument — so auto-minting a spendable replacement would hand back
        # exactly the value the merchant froze. Refuse it and require a human.
        if card.is_expired and card.is_active:
            return cls._mint_replacement(capture, card, amount, reason=reason, txn_id=txn_id)
        if not card.is_active:
            raise GiftCardTenderError(
                f"Gift card {card.code} is deactivated; refusing to auto-mint a "
                f"replacement. A deactivated card is frozen deliberately — refund "
                f"this leg by hand after confirming it should be released."
            )

        try:
            card.adjust_balance(amount, reason=reason or f"Refund of {capture.transaction_id}")
        except ValidationError as exc:
            raise GiftCardTenderError(str(exc)) from exc

        return PaymentTransaction.objects.create(
            # Idempotency key resolved above, before the balance was moved.
            transaction_id=txn_id,
            tender_type=PaymentTransaction.TENDER_GIFT_CARD,
            transaction_type="refund",
            status="completed",
            gift_card=card,
            order=capture.order,
            parent_transaction=capture,
            amount=amount,
            settlement_amount=amount,
            exchange_rate=capture.exchange_rate,
            provider_account=None,
        )
