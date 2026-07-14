"""
Refund Service - Handles payment refunds
Supports full and partial refunds
"""

import logging
import uuid
from decimal import Decimal
from typing import Any

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from payment_providers.models import PaymentIntent, PaymentTransaction
from payment_providers.providers.registry import ProviderRegistry

logger = logging.getLogger(__name__)


class RefundService:
    """
    Service for processing payment refunds
    """

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
        if refund_amount <= 0:
            return False, _("Refund amount must be greater than zero")

        # Calculate already refunded amount
        already_refunded = PaymentTransaction.objects.filter(
            provider_account=original_transaction.provider_account,
            order=original_transaction.order,
            transaction_type="refund",
            status="succeeded",
        ).aggregate(total=sum("amount"))["total"] or Decimal("0")

        # Check if refund amount exceeds available amount
        available_for_refund = original_transaction.amount - already_refunded
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
    ) -> tuple[bool, PaymentTransaction | None, str]:
        """
        Create a refund for a successful payment

        Args:
            original_transaction: Original payment transaction to refund
            refund_amount: Amount to refund (None for full refund)
            reason: Reason for refund
            metadata: Additional metadata

        Returns:
            Tuple of (success: bool, refund_transaction: PaymentTransaction|None, message: str)
        """
        # Validate original transaction can be refunded
        if original_transaction.status != "succeeded":
            return False, None, _("Only successful payments can be refunded")

        if original_transaction.transaction_type != "charge":
            return False, None, _("Only charge transactions can be refunded")

        # Default to full refund
        refund_amount = refund_amount or original_transaction.amount

        # Validate refund amount
        is_valid, message = RefundService.validate_refund_amount(
            original_transaction, refund_amount
        )
        if not is_valid:
            return False, None, message

        # Check if provider supports refunds
        provider_account = original_transaction.provider_account
        # Note: This check would need provider capability info
        # For now, we'll attempt the refund and let the provider fail if not supported

        # Generate unique refund transaction ID
        refund_transaction_id = f"rfnd_{uuid.uuid4().hex[:16]}"

        try:
            # Get provider instance
            provider_class = ProviderRegistry.get_provider(provider_account.component.slug)
            if not provider_class:
                return False, None, _("Payment provider not found in registry")

            provider_instance = provider_class(provider_account)

            # Check if provider supports partial refunds
            # capabilities = provider_instance.get_capabilities()
            # if is_partial and not capabilities.get('supports_partial_refunds'):
            #     return False, None, _("Provider does not support partial refunds")

            # Create refund via provider
            refund_response = provider_instance.create_refund(
                transaction_id=original_transaction.provider_transaction_id,
                amount=float(refund_amount),
                reason=reason,
                metadata=metadata or {},
            )

            if not refund_response.get("success"):
                return False, None, refund_response.get("message", _("Refund failed"))

            # Create refund transaction record
            refund_transaction = PaymentTransaction.objects.create(
                transaction_id=refund_transaction_id,
                provider_account=provider_account,
                order=original_transaction.order,
                amount=refund_amount,
                amount_currency=original_transaction.amount_currency,
                status="succeeded",
                transaction_type="refund",
                provider_transaction_id=refund_response.get("provider_refund_id", ""),
                provider_response=PaymentIntent._json_safe(refund_response),
                metadata={
                    **(metadata or {}),
                    "original_transaction_id": original_transaction.transaction_id,
                    "refund_reason": reason,
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

                # Calculate total refunded amount
                total_refunded = PaymentTransaction.objects.filter(
                    order=order, transaction_type="refund", status="succeeded"
                ).aggregate(total=sum("amount"))["total"] or Decimal("0")

                order.amount_refunded = total_refunded

                # Update payment status
                if total_refunded >= order.amount_paid:
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
        Get refund status from provider

        Args:
            refund_transaction: Refund transaction

        Returns:
            Dict with refund status information
        """
        if refund_transaction.transaction_type != "refund":
            return {"success": False, "error": _("Transaction is not a refund")}

        try:
            provider_class = ProviderRegistry.get_provider(
                refund_transaction.provider_account.component.slug
            )
            provider_instance = provider_class(refund_transaction.provider_account)

            # Get refund status from provider
            status_response = provider_instance.get_refund_status(
                refund_id=refund_transaction.provider_transaction_id
            )

            return {
                "success": True,
                "status": status_response.get("status"),
                "amount": status_response.get("amount"),
                "currency": status_response.get("currency"),
                "reason": status_response.get("reason"),
                "provider_data": status_response,
            }

        except Exception as e:
            logger.error(f"Error getting refund status: {str(e)}", exc_info=True)
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_refundable_amount(transaction: PaymentTransaction) -> Decimal:
        """
        Calculate how much of a transaction can still be refunded

        Args:
            transaction: Payment transaction

        Returns:
            Amount available for refund
        """
        if transaction.status != "succeeded" or transaction.transaction_type != "charge":
            return Decimal("0")

        # Calculate already refunded amount
        already_refunded = PaymentTransaction.objects.filter(
            provider_account=transaction.provider_account,
            order=transaction.order,
            transaction_type="refund",
            status="succeeded",
        ).aggregate(total=sum("amount"))["total"] or Decimal("0")

        return max(Decimal("0"), transaction.amount - already_refunded)

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
