"""
Payment Service - Core payment processing logic
Handles payment creation, authorization, and capture
"""
from decimal import Decimal
from typing import Dict, Any, Tuple, Optional
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import uuid
import logging

from payment_providers.models import (
    PaymentProviderAccount,
    PaymentIntent,
    PaymentTransaction,
)
from orders.models import Order
from payment_providers.providers.registry import ProviderRegistry

logger = logging.getLogger(__name__)


class PaymentService:
    """
    Service for processing payments through configured providers
    """

    @staticmethod
    def validate_payment_amount(amount: Decimal, currency: str = 'USD') -> Tuple[bool, str]:
        """
        Validate payment amount

        Args:
            amount: Payment amount
            currency: Currency code

        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        if amount <= 0:
            return False, _("Payment amount must be greater than zero")

        # Check for reasonable maximum (e.g., $1,000,000)
        if amount > Decimal('1000000.00'):
            return False, _("Payment amount exceeds maximum allowed")

        return True, ""

    @staticmethod
    @transaction.atomic
    def create_payment_intent(
        provider_account: PaymentProviderAccount,
        order: Order,
        amount: Decimal,
        currency: str = 'USD',
        metadata: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, Optional[PaymentTransaction], str]:
        """
        Create a payment intent with the provider

        Args:
            provider_account: Payment provider account to use
            order: Order being paid for
            amount: Payment amount
            currency: Currency code
            metadata: Additional metadata

        Returns:
            Tuple of (success: bool, transaction: PaymentTransaction|None, message: str)
        """
        # Validate provider is active and connected
        if not provider_account.is_active:
            return False, None, _("Payment provider is not active")

        if provider_account.connection_status != 'connected':
            return False, None, _("Payment provider is not properly configured")

        # Validate amount
        is_valid, message = PaymentService.validate_payment_amount(amount, currency)
        if not is_valid:
            return False, None, message

        # Generate unique transaction ID
        transaction_id = f"txn_{uuid.uuid4().hex[:16]}"

        try:
            # Get provider instance from registry
            provider_class = ProviderRegistry.get_provider(provider_account.component.slug)
            if not provider_class:
                return False, None, _("Payment provider not found in registry")

            provider_instance = provider_class(provider_account)

            # Create payment intent via provider
            # This will vary by provider - Stripe creates PaymentIntent, PayPal creates Order, etc.
            provider_response = provider_instance.create_payment_intent(
                amount=float(amount),
                currency=currency,
                order_id=order.id,
                metadata=metadata or {}
            )

            if not provider_response.get('success'):
                return False, None, provider_response.get('message', _("Payment intent creation failed"))

            # Create transaction record
            transaction = PaymentTransaction.objects.create(
                transaction_id=transaction_id,
                provider_account=provider_account,
                order=order,
                amount=amount,
                amount_currency=currency,
                status='pending',
                transaction_type='charge',
                provider_transaction_id=provider_response.get('provider_transaction_id', ''),
                provider_response=PaymentIntent._json_safe(provider_response),
                metadata=metadata or {},
                customer_name=order.shipping_address.name if order.shipping_address else '',
                customer_email=order.customer.email if order.customer else '',
            )

            logger.info(
                f"Payment intent created: {transaction_id} for order {order.id} "
                f"via {provider_account.display_name}"
            )

            return True, transaction, _("Payment intent created successfully")

        except Exception as e:
            logger.error(f"Error creating payment intent: {str(e)}", exc_info=True)
            return False, None, _("Payment processing error: {error}").format(error=str(e))

    @staticmethod
    @transaction.atomic
    def authorize_payment(
        transaction: PaymentTransaction,
        payment_method_details: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, str]:
        """
        Authorize a payment (hold funds without capturing)

        Args:
            transaction: Payment transaction to authorize
            payment_method_details: Payment method details (card, bank, etc.)

        Returns:
            Tuple of (success: bool, message: str)
        """
        if transaction.status != 'pending':
            return False, _("Payment transaction is not in pending state")

        try:
            provider_class = ProviderRegistry.get_provider(
                transaction.provider_account.component.slug
            )
            provider_instance = provider_class(transaction.provider_account)

            # Authorize payment via provider
            auth_response = provider_instance.authorize_payment(
                transaction_id=transaction.provider_transaction_id,
                payment_method_details=payment_method_details or {}
            )

            if not auth_response.get('success'):
                transaction.status = 'failed'
                transaction.error_message = auth_response.get('message', _("Authorization failed"))
                transaction.error_code = auth_response.get('error_code', '')
                transaction.save()
                return False, transaction.error_message

            # Update transaction
            transaction.status = 'authorized'
            transaction.authorization_id = auth_response.get('authorization_id', '')
            transaction.payment_method_type = auth_response.get('payment_method_type', '')
            transaction.payment_method_last4 = auth_response.get('payment_method_last4', '')
            transaction.provider_response = PaymentIntent._json_safe(auth_response)
            transaction.save()

            # Update order
            if transaction.order:
                transaction.order.payment_status = 'authorized'
                transaction.order.save(update_fields=['payment_status'])

            logger.info(f"Payment authorized: {transaction.transaction_id}")

            return True, _("Payment authorized successfully")

        except Exception as e:
            logger.error(f"Error authorizing payment: {str(e)}", exc_info=True)
            transaction.status = 'failed'
            transaction.error_message = str(e)
            transaction.save()
            return False, _("Payment authorization error: {error}").format(error=str(e))

    @staticmethod
    @transaction.atomic
    def capture_payment(
        transaction: PaymentTransaction,
        amount: Optional[Decimal] = None
    ) -> Tuple[bool, str]:
        """
        Capture an authorized payment

        Args:
            transaction: Payment transaction to capture
            amount: Amount to capture (if partial capture supported)

        Returns:
            Tuple of (success: bool, message: str)
        """
        if transaction.status != 'authorized':
            return False, _("Payment transaction is not authorized")

        # Default to full transaction amount
        capture_amount = amount or transaction.amount

        # Validate capture amount doesn't exceed authorized amount
        if capture_amount > transaction.amount:
            return False, _("Capture amount exceeds authorized amount")

        try:
            provider_class = ProviderRegistry.get_provider(
                transaction.provider_account.component.slug
            )
            provider_instance = provider_class(transaction.provider_account)

            # Capture payment via provider
            capture_response = provider_instance.capture_payment(
                authorization_id=transaction.authorization_id,
                amount=float(capture_amount)
            )

            if not capture_response.get('success'):
                return False, capture_response.get('message', _("Capture failed"))

            # Update transaction
            transaction.status = 'succeeded'
            transaction.amount = capture_amount
            transaction.completed_at = timezone.now()
            transaction.provider_response = PaymentIntent._json_safe(capture_response)
            transaction.save()

            # Update order
            if transaction.order:
                transaction.order.payment_status = 'paid'
                transaction.order.amount_paid = capture_amount
                transaction.order.paid_at = timezone.now()
                transaction.order.save(update_fields=['payment_status', 'amount_paid', 'paid_at'])

            logger.info(
                f"Payment captured: {transaction.transaction_id} "
                f"amount: {capture_amount} {transaction.amount_currency}"
            )

            return True, _("Payment captured successfully")

        except Exception as e:
            logger.error(f"Error capturing payment: {str(e)}", exc_info=True)
            return False, _("Payment capture error: {error}").format(error=str(e))

    @staticmethod
    def get_payment_status(transaction: PaymentTransaction) -> Dict[str, Any]:
        """
        Get current payment status from provider

        Args:
            transaction: Payment transaction

        Returns:
            Dict with status information
        """
        try:
            provider_class = ProviderRegistry.get_provider(
                transaction.provider_account.component.slug
            )
            provider_instance = provider_class(transaction.provider_account)

            # Get status from provider
            status_response = provider_instance.get_payment_status(
                transaction_id=transaction.provider_transaction_id
            )

            return {
                'success': True,
                'status': status_response.get('status'),
                'amount': status_response.get('amount'),
                'currency': status_response.get('currency'),
                'payment_method': status_response.get('payment_method'),
                'provider_data': status_response
            }

        except Exception as e:
            logger.error(f"Error getting payment status: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    @transaction.atomic
    def cancel_payment(transaction: PaymentTransaction) -> Tuple[bool, str]:
        """
        Cancel a pending or authorized payment

        Args:
            transaction: Payment transaction to cancel

        Returns:
            Tuple of (success: bool, message: str)
        """
        if transaction.status not in ['pending', 'authorized']:
            return False, _("Only pending or authorized payments can be cancelled")

        try:
            provider_class = ProviderRegistry.get_provider(
                transaction.provider_account.component.slug
            )
            provider_instance = provider_class(transaction.provider_account)

            # Cancel payment via provider
            cancel_response = provider_instance.cancel_payment(
                transaction_id=transaction.provider_transaction_id,
                authorization_id=transaction.authorization_id
            )

            if not cancel_response.get('success'):
                return False, cancel_response.get('message', _("Cancellation failed"))

            # Update transaction
            transaction.status = 'cancelled'
            transaction.completed_at = timezone.now()
            transaction.provider_response = PaymentIntent._json_safe(cancel_response)
            transaction.save()

            # Update order
            if transaction.order:
                transaction.order.payment_status = 'cancelled'
                transaction.order.save(update_fields=['payment_status'])

            logger.info(f"Payment cancelled: {transaction.transaction_id}")

            return True, _("Payment cancelled successfully")

        except Exception as e:
            logger.error(f"Error cancelling payment: {str(e)}", exc_info=True)
            return False, _("Payment cancellation error: {error}").format(error=str(e))
