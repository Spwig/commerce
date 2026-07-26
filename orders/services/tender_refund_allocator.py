"""
Split a refund across the tenders that actually paid for an order.

An order can be paid by several things at once — a gift card for part of it and
a card for the rest. Refunding then is not one movement but several, and which
tender gets money back first is a decision with consequences.

**Gift card before gateway.** Refunding cash the merchant never collected is the
worse failure of the two, and taking the internal leg first closes the
buy-with-a-stolen-card, spend, refund-elsewhere path: the value goes back where
it came from rather than out to a card that may not be the buyer's.

**Capacity is per capture row, never per order.** Invariant I3 —
``sum(refunds) <= sum(captures)`` for each row. Capping on ``Order.amount_paid``
instead would permit refunding gift card value out through the gateway, which is
precisely the mistake this exists to prevent. That field has been wrong once
already (P2.2 assigned it the gateway leg only) and has two writers.

Two phases, deliberately:

* ``plan()`` is pure. It reads the ledger and returns what it *would* do. It
  moves nothing, so it can be called to preview, to validate, or in a test.
* ``execute()`` moves money, gateway legs first. If an internal leg fails after
  a gateway refund has already gone out, the gateway money is gone and must not
  be un-refunded; the reverse ordering would risk crediting a gift card for a
  gateway refund that then failed.

Both internal tenders refund here: gift cards to the card (or a replacement if
it expired), wallet legs back to the wallet through ``WalletTenderService`` —
which is why dispatch is on ``tender_type``. The P2.4 version raised for wallet
because no spendable destination existed yet; P2.5a filled the branch in.

Plan: docs/.claude_code/plans/wondrous-moseying-wolf.md (R2, P2.4 + P2.5a)
"""

import logging
from decimal import Decimal

from django.db import transaction as db_transaction
from django.db.models import Sum
from djmoney.money import Money

logger = logging.getLogger(__name__)


class RefundAllocationError(Exception):
    """The refund cannot be allocated against what was actually captured."""


class TenderRefundAllocator:
    # Internal, merchant-controlled value first; external money last.
    #
    # Tender CLASS is primary and recency is only the tie-break within a class.
    # Reading recency as primary would silently invert this on POS, which writes
    # its gift card leg before the card leg — and POS is exactly where the
    # stolen-card-to-gift-card path is easiest, so the inversion would be
    # invisible while web orders kept behaving correctly.
    TENDER_PRIORITY = (
        "gift_card",
        "wallet",
        "cash",
        "terminal_card",
        "card",
        "gateway",
    )

    @classmethod
    def get_tender_priority(cls, tender_type):
        """Lower sorts earlier. Unknown tenders refund last, with real money."""
        try:
            return cls.TENDER_PRIORITY.index(tender_type)
        except ValueError:
            return len(cls.TENDER_PRIORITY)

    # ------------------------------------------------------------------
    # plan — pure
    # ------------------------------------------------------------------

    @classmethod
    def captures_for(cls, order):
        """
        The rows a refund can draw against.

        Captures and charges only. Never ``authorize``: a hold is a reservation
        and, since P2.2f caps captures at what the order actually owed, a hold
        can be larger than what was taken. Refunding against it would return
        money that was never captured.
        """
        from payment_providers.models import PaymentTransaction

        return list(
            PaymentTransaction.objects.filter(
                order=order,
                transaction_type__in=("capture", "charge"),
                status="completed",
            )
        )

    @classmethod
    def refundable_on(cls, capture):
        """
        What is left on one capture row, as a Money in the order's currency.

        ``settlement_amount`` is the order-currency figure and is what refunds
        are denominated in; gateway charges written by the orchestration service
        leave it NULL, hence the fallback.

        ``pending`` refunds count against capacity as well as ``completed``
        ones, or two concurrent refunds are each told the same room is free.
        """
        from payment_providers.models import PaymentTransaction

        captured = capture.settlement_amount or capture.amount
        already = PaymentTransaction.objects.filter(
            parent_transaction=capture,
            transaction_type="refund",
            status__in=("pending", "completed"),
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0")

        remaining = captured.amount - already
        return Money(max(remaining, Decimal("0")), captured.currency)

    @classmethod
    def plan(cls, order, amount):
        """
        Work out which tenders fund a refund of ``amount``.

        Returns a list of ``{"capture", "amount", "tender_type"}`` legs.

        Raises RefundAllocationError if the ledger cannot fund it — the cap is
        the sum of what was captured, NOT ``Order.amount_paid``.
        """
        if amount.amount <= 0:
            raise RefundAllocationError("Refund amount must be greater than zero")

        captures = cls.captures_for(order)
        if not captures:
            raise RefundAllocationError(
                f"Order {order.order_number} has no completed captures to refund against"
            )

        # Tender class first, then most-recent-first within a class.
        # `pk` is a UUID and cannot be negated, so it is only a stable
        # tiebreak — arbitrary but deterministic, which is all it needs to be
        # for two rows written in the same instant.
        captures.sort(
            key=lambda c: (
                cls.get_tender_priority(c.tender_type),
                -(c.created_at.timestamp() if c.created_at else 0),
                str(c.pk),
            )
        )

        legs = []
        remaining = amount
        for capture in captures:
            if remaining.amount <= 0:
                break
            available = cls.refundable_on(capture)
            if available.amount <= 0:
                continue
            if available.currency != remaining.currency:
                # Refusing beats guessing a conversion on a refund.
                logger.error(
                    f"Capture {capture.pk} settles in {available.currency} but the "
                    f"refund is in {remaining.currency}; skipping it"
                )
                continue

            take = Money(min(available.amount, remaining.amount), remaining.currency)
            legs.append({"capture": capture, "amount": take, "tender_type": capture.tender_type})
            remaining -= take

        if remaining.amount > 0:
            capacity = sum((cls.refundable_on(c).amount for c in captures), Decimal("0"))
            raise RefundAllocationError(
                f"Cannot refund {amount} against order {order.order_number}: only "
                f"{capacity} remains across its captures. Refunding beyond that "
                f"would return money the order never took."
            )

        return legs

    # ------------------------------------------------------------------
    # execute — moves money
    # ------------------------------------------------------------------

    @classmethod
    def execute(cls, order, amount, reason="", refund=None):
        """
        Allocate and perform a refund.

        External legs run first. If an internal leg then fails, the gateway
        money has already gone and must not be reversed — better to have
        refunded the customer and owe the gift card a manual credit than to
        credit a card for a gateway refund that never happened.

        Returns the list of refund PaymentTransactions created.
        """
        from orders.models import Order

        # A refund identity is required. The gift-card leg keys its idempotency
        # on refund.pk; without it, refund_to_card falls back to a positional
        # counter that is not retry-safe (a re-run computes a different count
        # and credits the card twice). Every production caller is
        # Refund.execute(), which passes self — so a missing refund here is a
        # programming error, and failing loudly beats silently taking the
        # non-idempotent path.
        if refund is None:
            raise RefundAllocationError(
                "TenderRefundAllocator.execute requires a refund for idempotency; "
                "call it through Refund.execute()."
            )

        # The lock MUST be held across the money movement, not just the plan.
        #
        # A previous version closed the atomic block right after plan() and ran
        # the legs unlocked. Because plan() derives capacity from the refund
        # rows that already exist, two refunds on the same order could each lock,
        # plan against the same free capacity, release, and then both pay out —
        # the capacity a leg consumes is not visible to the other until its
        # refund row commits. Two distinct Refund rows on one order (a
        # double-tapped mobile button, or an admin + app race) is the concrete
        # path. Holding the lock across the whole operation serialises them: the
        # second refund blocks until the first commits, then re-plans against the
        # first's now-committed rows.
        #
        # Residual, documented honestly: the gateway leg makes an irreversible
        # provider call, and it runs inside this transaction. If a later leg
        # raised, the outer rollback would discard the gateway refund ROW while
        # the provider money had already moved. External legs run first and the
        # only legs after them are local gift-card DB writes that plan() already
        # validated, so this window is narrow — but a true two-phase (reserve
        # pending, call provider, mark completed) is the correct long-term shape
        # and is deferred. All-or-nothing under the lock is strictly safer than
        # the released-lock over-refund it replaces.
        with db_transaction.atomic():
            locked = Order.objects.select_for_update().get(pk=order.pk)
            legs = cls.plan(locked, amount)

            external = [leg for leg in legs if leg["tender_type"] not in ("gift_card", "wallet")]
            internal = [leg for leg in legs if leg["tender_type"] in ("gift_card", "wallet")]

            created = []
            for leg in external + internal:
                created.append(cls._refund_leg(leg, reason=reason, refund=refund))

            cls._recompute_amount_refunded(locked)
            return created

    @classmethod
    def _refund_leg(cls, leg, reason="", refund=None):
        """Dispatch one leg to whatever knows how to move that kind of money."""
        capture = leg["capture"]
        tender = leg["tender_type"]

        if tender == "gift_card":
            from catalog.services.gift_card_tender_service import GiftCardTenderService

            return GiftCardTenderService.refund_to_card(
                capture,
                amount=leg["amount"],
                reason=reason,
                # Stable per refund attempt, so a retry collides on the unique
                # transaction_id instead of crediting the card a second time.
                refund_ref=getattr(refund, "pk", None),
            )

        if tender == "wallet":
            from wallet.tender_service import WalletTenderError, WalletTenderService

            try:
                return WalletTenderService.refund_to_wallet(
                    capture,
                    amount=leg["amount"],
                    reason=reason,
                    # Same idempotency stance as the gift card leg: keyed off
                    # the caller's refund identity so a retry returns the
                    # existing row instead of crediting twice.
                    refund_ref=getattr(refund, "pk", None),
                )
            except WalletTenderError as exc:
                raise RefundAllocationError(
                    f"Wallet refund of {leg['amount']} failed: {exc}"
                ) from exc

        from payment_providers.services.refund_service import RefundService

        success, txn, message = RefundService.create_refund(
            original_transaction=capture,
            refund_amount=leg["amount"].amount,
            reason=reason,
        )
        if not success:
            raise RefundAllocationError(f"Gateway refund of {leg['amount']} failed: {message}")
        return txn

    @classmethod
    def _recompute_amount_refunded(cls, order):
        """
        Derive the total from the ledger rather than incrementing it.

        Incrementing drifts the moment any path writes a refund row without
        going through here, and the whole point of the allocator is that the
        rows are the truth.
        """
        from payment_providers.models import PaymentTransaction

        total = PaymentTransaction.objects.filter(
            order=order,
            transaction_type="refund",
            status="completed",
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0")

        currency = order.amount_refunded.currency
        order.amount_refunded = Money(total, currency)
        order.payment_status = (
            "refunded"
            if total >= order.amount_paid.amount
            else "partially_refunded"
            if total > 0
            else order.payment_status
        )
        order.save(update_fields=["amount_refunded", "payment_status", "updated_at"])
        return order.amount_refunded
