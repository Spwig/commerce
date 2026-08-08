"""
Refund Service - Handles payment refunds
Supports full and partial refunds
"""

import inspect
import logging
import uuid
from decimal import Decimal
from typing import Any

from django.conf import settings
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from djmoney.money import Money

from payment_providers.models import PaymentIntent, PaymentTransaction

logger = logging.getLogger(__name__)


class RefundService:
    """
    Service for processing payment refunds
    """

    @staticmethod
    def _callable_accepts_kwarg(func: Any, name: str) -> bool:
        """Return True if ``func`` can be called with keyword ``name``.

        True when the signature declares a parameter of that name or accepts
        arbitrary ``**kwargs``. Defaults to True if the signature can't be
        introspected (e.g. a C-extension or heavily wrapped callable), so we
        don't strip a kwarg a provider might actually accept.
        """
        try:
            params = inspect.signature(func).parameters
        except (TypeError, ValueError):
            return True
        if name in params:
            return True
        return any(p.kind is inspect.Parameter.VAR_KEYWORD for p in params.values())

    @staticmethod
    def validate_refund_amount(
        original_transaction: PaymentTransaction, refund_amount: Decimal
    ) -> tuple[bool, str]:
        """
        Validate refund amount against original transaction

        Args:
            original_transaction: Original payment transaction
            refund_amount: Amount to refund

        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        # Normalise to a Decimal. Callers pass either a Money (full-refund
        # default is original_transaction.amount) or a bare Decimal (the
        # allocator/POS pass `<Money>.amount`). Comparing a Money against a
        # Decimal/int raises moneyed.MoneyComparisonError — which, caught by
        # create_refund's broad except, silently turned every gateway refund
        # into a generic failure. Compare like with like.
        if isinstance(refund_amount, Money):
            refund_amount = refund_amount.amount

        if refund_amount <= 0:
            return False, _("Refund amount must be greater than zero")

        # Capacity is PER CAPTURE ROW, not per order (invariant I3:
        # sum(refunds) <= sum(captures) for each tender row).
        #
        # The previous filter keyed on (provider_account, order), which is wrong
        # in both directions: refunds against a DIFFERENT charge on the same
        # provider account ate this transaction's capacity, and gift card
        # refunds — which carry provider_account=None — were not counted at all,
        # so a gift card leg could be refunded repeatedly.
        #
        # `pending` counts as well as `completed`: two concurrent refunds must
        # not both be told the same capacity is free.
        already_refunded = PaymentTransaction.objects.filter(
            parent_transaction=original_transaction,
            transaction_type="refund",
            status__in=("pending", "completed"),
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0")

        # Check if refund amount exceeds available amount. Use the Decimal
        # component of the captured Money so this is a Decimal-vs-Decimal
        # comparison (already_refunded is a Decimal aggregate).
        available_for_refund = original_transaction.amount.amount - already_refunded
        if refund_amount > available_for_refund:
            return False, _(
                "Refund amount ({amount}) exceeds available amount ({available})"
            ).format(amount=refund_amount, available=available_for_refund)

        return True, ""

    @staticmethod
    @transaction.atomic
    def create_refund(
        original_transaction: PaymentTransaction,
        refund_amount: Decimal | None = None,
        reason: str = "",
        metadata: dict[str, Any] | None = None,
        idempotency_key: str | int | None = None,
    ) -> tuple[bool, PaymentTransaction | None, str]:
        """
        Create a refund for a successful payment.

        Args:
            original_transaction: Original payment transaction to refund
            refund_amount: Amount to refund (None for full refund)
            reason: Reason for refund
            metadata: Additional metadata
            idempotency_key: Stable identifier for THIS logical refund attempt.
                Pass the caller's refund identity (e.g. the parent Refund pk) —
                the SAME stance GiftCardTenderService/WalletTenderService take via
                ``refund_ref``. When supplied it (a) makes the refund row's
                ``transaction_id`` deterministic, so a retry collides on the
                unique constraint instead of paying out again, and (b) is sent to
                the PSP as its idempotency key, so a retry whose first row rolled
                back after the PSP succeeded is de-duplicated by the PSP too.
                Without it the id is random and the refund is NOT idempotent
                across separate invocations — only within one PSP call.

        Returns:
            Tuple of (success: bool, refund_transaction: PaymentTransaction|None, message: str)
        """
        # Validate original transaction can be refunded.
        #
        # These two guards were the last survivors of the dead status
        # vocabulary. The aggregate filters below were fixed to "completed", but
        # these were left on "succeeded" — which is not in STATUS_CHOICES — and
        # "charge" — which excludes the "capture" rows the tender rail writes.
        # So every gateway refund routed here returned "Only successful payments
        # can be refunded", the allocator raised, and the whole refund failed.
        # The tests missed it because none exercised a refund large enough to
        # spill onto the gateway leg.
        if original_transaction.status != "completed":
            return False, None, _("Only successful payments can be refunded")

        if original_transaction.transaction_type not in ("charge", "capture"):
            return False, None, _("Only charge transactions can be refunded")

        # Default to full refund, then normalise to a Decimal in the captured
        # transaction's currency. Callers pass either a Money or a bare Decimal;
        # downstream we need a Decimal for validation/comparison and provider
        # amounts, and a Money for the stored MoneyField rows.
        # `is None`, not truthiness: a Decimal("0") must fall through to
        # validation (and be rejected as non-positive), not be silently
        # promoted to a full refund.
        if refund_amount is None:
            refund_amount = original_transaction.amount
        refund_currency = original_transaction.amount.currency
        if isinstance(refund_amount, Money):
            refund_amount = refund_amount.amount
        refund_amount = Decimal(refund_amount)
        refund_money = Money(refund_amount, refund_currency)
        # settlement_amount is denominated in the ORDER currency (see
        # PaymentTransaction.settlement_amount); use the original row's
        # settlement currency. Cross-currency FX conversion is out of scope for
        # this fix — single-currency stores (the common case) have tender and
        # order currency equal, so amount and settlement coincide.
        settlement_currency = (
            original_transaction.settlement_amount or original_transaction.amount
        ).currency
        refund_settlement = Money(refund_amount, settlement_currency)

        # provider_account is read from the row-locked transaction inside the
        # atomic block below (see the select_for_update note).

        # Refund-row id. With a caller idempotency key, derive it DETERMINISTICALLY
        # from (capture, key) so a retry of the same logical refund reuses the id
        # and collides on the unique `transaction_id` constraint instead of paying
        # out a second time — mirroring the gift-card/wallet tender rails. Keying
        # on the capture too keeps distinct legs of one multi-tender refund from
        # colliding with each other. Without a key, fall back to a random id (no
        # cross-invocation idempotency; see the docstring).
        if idempotency_key is not None:
            refund_transaction_id = f"rfnd:{original_transaction.transaction_id}:{idempotency_key}"
        else:
            refund_transaction_id = f"rfnd_{uuid.uuid4().hex[:16]}"

        try:
            # Serialize refunds against THIS capture row. Capacity is checked
            # per capture (parent_transaction) by reading already-refunded and
            # comparing to the captured amount; without a row lock two
            # concurrent refunds (a double-tapped POS button, or a POS refund
            # racing an admin refund) can both read the same remaining capacity,
            # both pass validation, and both pay out — an over-refund. The admin
            # path locks the Order in TenderRefundAllocator.execute; POS calls
            # this service directly, so the lock has to live here to cover every
            # caller. select_for_update() is held for the rest of this atomic
            # block, across the capacity read and the refund-row insert.
            original_transaction = PaymentTransaction.objects.select_for_update().get(
                pk=original_transaction.pk
            )
            provider_account = original_transaction.provider_account

            # Validated INSIDE the try. Raising out of here escapes the
            # documented (success, transaction, message) contract that POS
            # unpacks, turning a refused refund into a 500.
            is_valid, message = RefundService.validate_refund_amount(
                original_transaction, refund_amount
            )
            if not is_valid:
                return False, None, message

            # Idempotent short-circuit. With a caller key the refund-row id is
            # deterministic, so a retry of an ALREADY-COMPLETED refund is caught
            # here — under the parent row lock, so it can't race the original —
            # and returns that row WITHOUT hitting the PSP again. (The random-id
            # path can't dedupe and skips this.)
            if idempotency_key is not None:
                existing = PaymentTransaction.objects.filter(
                    transaction_id=refund_transaction_id
                ).first()
                if existing is not None:
                    return True, existing, _("Refund already processed")

            # Build the provider client the SAME way every live payment path
            # does. PaymentProviderAccount.get_provider_instance() decrypts the
            # stored credentials, applies the sandbox guard, and constructs the
            # provider with `credentials=` — its actual __init__ contract.
            #
            # This path used to call `provider_class(provider_account)`, handing
            # the account MODEL where the constructor expects a credentials dict.
            # That raised TypeError inside _select_credentials ("argument of type
            # 'PaymentProviderAccount' is not iterable"), the broad except below
            # swallowed it, and every gateway refund came back as a generic
            # "Refund processing error". The invariant tests missed it because
            # they stub the provider with a MagicMock, which both accepts any
            # constructor args and auto-vivifies whatever method is called.
            provider_instance = provider_account.get_provider_instance()

            # Refund via the provider. The provider contract is `refund(...)`
            # (there is no `create_refund` on the base class or any provider).
            # Amount is a Decimal (not float — float risks money-precision drift
            # converting to minor units).
            #
            # `refund_id` rides in the metadata so a provider can build a stable
            # PSP idempotency key (Stripe/Square/PayPal/Revolut/RazorPay read
            # `metadata['idempotency_key'] or metadata['refund_id']`). When the
            # caller supplied an idempotency key we also set `idempotency_key`
            # explicitly: that closes the window the DB collision can't — a retry
            # whose first row rolled back AFTER the PSP succeeded is de-duplicated
            # by the PSP itself. A caller-provided `metadata['idempotency_key']`
            # still wins (we spread `metadata` first).
            refund_metadata = {
                **(metadata or {}),
                "refund_id": refund_transaction_id,
            }
            if idempotency_key is not None:
                refund_metadata.setdefault("idempotency_key", str(idempotency_key))

            # Providers are pluggable and marketplace-distributed, so their
            # `refund()` signatures can drift from the base contract. The base
            # declares `metadata`, but a provider may omit it (Airwallex's
            # wrapper historically did). Passing an unaccepted kwarg would raise
            # TypeError, and the broad except below would turn a legitimate
            # refund into a generic failure. Send `metadata` only when the
            # callee actually accepts it; otherwise refund WITHOUT it (idempotency
            # unavailable for that provider) and log loudly so the drift is
            # visible rather than silently swallowed.
            refund_kwargs: dict[str, Any] = {
                "transaction_id": original_transaction.provider_transaction_id,
                "amount": refund_amount,
                "reason": reason,
            }
            if RefundService._callable_accepts_kwarg(provider_instance.refund, "metadata"):
                refund_kwargs["metadata"] = refund_metadata
            else:
                logger.warning(
                    "Provider %s refund() does not accept a `metadata` argument; "
                    "sending refund without an idempotency key. Update the provider "
                    "to the base refund(transaction_id, amount, reason, metadata) "
                    "contract so retried refunds cannot double-pay.",
                    provider_account.component.slug,
                )
            refund_response = provider_instance.refund(**refund_kwargs)

            if not refund_response.get("success"):
                return False, None, refund_response.get("message", _("Refund failed"))

            # Create refund transaction record
            refund_transaction = PaymentTransaction.objects.create(
                transaction_id=refund_transaction_id,
                provider_account=provider_account,
                order=original_transaction.order,
                amount=refund_money,
                status="completed",
                transaction_type="refund",
                # Link the refund to the capture it draws against. Without this
                # there is no per-row capacity: refund capacity can only be
                # checked against the order in aggregate, which permits
                # refunding gift card value out through the gateway.
                # GiftCardTenderService.refund_to_card already does this.
                parent_transaction=original_transaction,
                settlement_amount=refund_settlement,
                tender_type=original_transaction.tender_type,
                provider_transaction_id=refund_response.get("provider_refund_id", ""),
                provider_response=PaymentIntent._json_safe(refund_response),
                metadata={
                    **(metadata or {}),
                    "original_transaction_id": original_transaction.transaction_id,
                    "refund_reason": reason,
                    **(
                        {"idempotency_key": str(idempotency_key)}
                        if idempotency_key is not None
                        else {}
                    ),
                },
                customer_name=original_transaction.customer_name,
                customer_email=original_transaction.customer_email,
                completed_at=timezone.now(),
            )

            # Log to Sales Bell (HQ only)
            if getattr(settings, "SPWIG_IS_HQ", False):
                try:
                    from core.models import SalesBellEvent

                    SalesBellEvent.log_refund(refund_transaction)
                except Exception as e:
                    logger.error(f"Failed to log sales bell refund event: {e}")

            # Update order
            if original_transaction.order:
                order = original_transaction.order

                # Total refunded. Label the order-level field with the ORDER
                # currency (order.amount_paid), not the tender currency. Sum()
                # yields a Decimal; normalise defensively in case a money-aware
                # backend returns a Money. (Cross-currency stores where a
                # refund row's tender currency differs from the order currency
                # need FX-aware settlement totalling — out of scope here; the
                # single-currency common case is correct.)
                order_currency = order.amount_paid.currency
                total_refunded = PaymentTransaction.objects.filter(
                    order=order, transaction_type="refund", status="completed"
                ).aggregate(total=Sum("amount"))["total"] or Decimal("0")
                if isinstance(total_refunded, Money):
                    total_refunded = total_refunded.amount

                order.amount_refunded = Money(total_refunded, order_currency)

                # Update payment status. Compare Decimal-to-Decimal — this line
                # fires AFTER the provider refund has already moved money, so a
                # Money/Decimal comparison error here would strand a real refund
                # (provider paid out, order left showing unpaid).
                if total_refunded >= order.amount_paid.amount:
                    order.payment_status = "refunded"
                else:
                    order.payment_status = "partially_refunded"

                order.save(update_fields=["amount_refunded", "payment_status"])

            logger.info(
                f"Refund created: {refund_transaction_id} for original transaction "
                f"{original_transaction.transaction_id} amount: {refund_amount}"
            )

            return True, refund_transaction, _("Refund processed successfully")

        except Exception as e:
            logger.error(f"Error creating refund: {str(e)}", exc_info=True)
            return False, None, _("Refund processing error: {error}").format(error=str(e))

    @staticmethod
    def get_refund_status(refund_transaction: PaymentTransaction) -> dict[str, Any]:
        """
        Return the recorded status of a refund.

        Reads Spwig's own PaymentTransaction record rather than polling the
        provider: no payment provider implements a refund-status endpoint, and
        the refund row already carries the authoritative result written when the
        refund was created. The previous version handed the account model to
        ``provider_class(...)`` and then called a ``get_refund_status()`` that no
        provider defines — so it raised on every call (TypeError at construction,
        AttributeError if it had got that far).

        Args:
            refund_transaction: Refund transaction

        Returns:
            Dict with refund status information
        """
        if refund_transaction.transaction_type != "refund":
            return {"success": False, "error": _("Transaction is not a refund")}

        amount = refund_transaction.amount
        return {
            "success": True,
            "status": refund_transaction.status,
            "amount": amount.amount,
            "currency": str(amount.currency),
            "reason": (refund_transaction.metadata or {}).get("refund_reason", ""),
            "provider_refund_id": refund_transaction.provider_transaction_id,
            "provider_data": refund_transaction.provider_response,
        }

    @staticmethod
    def get_refundable_amount(transaction: PaymentTransaction) -> Decimal:
        """
        Calculate how much of a transaction can still be refunded

        Args:
            transaction: Payment transaction

        Returns:
            Amount available for refund
        """
        # "completed" is the live status vocabulary ("succeeded" is not in
        # STATUS_CHOICES); "charge" and "capture" are both refundable tender
        # rows — mirror create_refund's guards.
        if transaction.status != "completed" or transaction.transaction_type not in (
            "charge",
            "capture",
        ):
            return Decimal("0")

        # Calculate already refunded amount
        already_refunded = PaymentTransaction.objects.filter(
            provider_account=transaction.provider_account,
            order=transaction.order,
            transaction_type="refund",
            status="completed",
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0")

        # Decimal-vs-Decimal: transaction.amount is Money, already_refunded a
        # Decimal aggregate.
        return max(Decimal("0"), transaction.amount.amount - already_refunded)

    @staticmethod
    def get_refund_history(order) -> list:
        """
        Get all refunds for an order

        Args:
            order: Order instance

        Returns:
            List of refund transactions
        """
        return PaymentTransaction.objects.filter(order=order, transaction_type="refund").order_by(
            "-created_at"
        )
