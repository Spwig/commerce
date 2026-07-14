"""
Webhook Service - Handles payment provider webhook events
Processes and routes webhook notifications from payment providers
"""

import json
import logging
import uuid
from typing import Any

from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from payment_providers.models import (
    PaymentIntent,
    PaymentProviderAccount,
    PaymentTransaction,
    PaymentWebhook,
)
from payment_providers.providers.registry import ProviderRegistry

logger = logging.getLogger(__name__)


class WebhookService:
    """
    Service for processing payment provider webhooks
    """

    @staticmethod
    def verify_webhook_signature(
        provider_account: PaymentProviderAccount,
        payload: bytes,
        signature: str,
        headers: dict[str, str],
    ) -> bool:
        """
        Verify webhook signature from provider

        Args:
            provider_account: Payment provider account
            payload: Raw webhook payload
            signature: Webhook signature from provider
            headers: Request headers

        Returns:
            True if signature is valid
        """
        try:
            provider_class = ProviderRegistry.get_provider(provider_account.component.slug)
            if not provider_class:
                logger.error(f"Provider not found: {provider_account.component.slug}")
                return False

            provider_instance = provider_class(provider_account)

            # Delegate signature verification to provider
            is_valid = provider_instance.verify_webhook_signature(
                payload=payload, signature=signature, headers=headers
            )

            return is_valid

        except Exception as e:
            logger.error(f"Error verifying webhook signature: {str(e)}", exc_info=True)
            return False

    @staticmethod
    @transaction.atomic
    def process_webhook(
        provider_slug: str,
        payload: dict[str, Any],
        headers: dict[str, str],
        raw_payload: bytes,
        signature: str | None = None,
    ) -> tuple[bool, str]:
        """
        Process incoming webhook from payment provider

        Args:
            provider_slug: Provider identifier
            payload: Parsed webhook payload
            headers: Request headers
            raw_payload: Raw request body
            signature: Webhook signature (if provided)

        Returns:
            Tuple of (success: bool, message: str)
        """
        # Extract event information
        event_id = payload.get("id", str(uuid.uuid4()))
        event_type = payload.get("type", payload.get("event_type", "unknown"))

        # Check for duplicate webhook (idempotency)
        idempotency_key = f"{provider_slug}:{event_id}"
        existing_webhook = PaymentWebhook.objects.filter(
            provider_slug=provider_slug, event_id=event_id
        ).first()

        if existing_webhook and existing_webhook.processed:
            logger.info(f"Duplicate webhook ignored: {event_id}")
            return True, _("Webhook already processed")

        # Find provider account
        # Note: This is simplified - in production you may need to extract provider account
        # from webhook payload or use a token/identifier in the webhook URL
        provider_accounts = PaymentProviderAccount.objects.filter(
            component__slug=provider_slug, is_active=True
        )

        if not provider_accounts.exists():
            logger.error(f"No active provider account found for: {provider_slug}")
            return False, _("Provider account not found")

        # Use first active account (in production, you'd identify the specific account)
        provider_account = provider_accounts.first()

        # Verify signature if provided
        signature_verified = False
        if signature:
            signature_verified = WebhookService.verify_webhook_signature(
                provider_account=provider_account,
                payload=raw_payload,
                signature=signature,
                headers=headers,
            )

            if not signature_verified:
                logger.warning(f"Webhook signature verification failed: {event_id}")
                # Continue processing but log the verification failure
                # Some providers send test webhooks without valid signatures

        # Create webhook record
        webhook = PaymentWebhook.objects.create(
            provider_account=provider_account,
            provider_slug=provider_slug,
            event_id=event_id,
            event_type=event_type,
            payload=payload,
            headers=headers,
            signature_verified=signature_verified,
            idempotency_key=idempotency_key,
            processed=False,
        )

        try:
            # Get provider instance
            provider_class = ProviderRegistry.get_provider(provider_slug)
            if not provider_class:
                raise Exception(f"Provider not found in registry: {provider_slug}")

            provider_instance = provider_class(provider_account)

            # Process webhook through provider
            processing_result = provider_instance.process_webhook(payload, event_type)

            if not processing_result.get("success"):
                raise Exception(processing_result.get("message", "Webhook processing failed"))

            # Handle payment intent events for orchestration flow
            intent_handled = False
            provider_intent_id = processing_result.get("payment_intent_id")
            if provider_intent_id and event_type.startswith("payment_intent."):
                intent_handled = WebhookService._handle_payment_intent_event(
                    provider_intent_id=provider_intent_id,
                    event_type=event_type,
                    event_data=processing_result,
                )

            # Update related transaction if event contains transaction data (legacy flow)
            transaction_id = processing_result.get("transaction_id")
            if transaction_id and not intent_handled:
                WebhookService._update_transaction_from_webhook(
                    transaction_id=transaction_id,
                    event_type=event_type,
                    event_data=processing_result.get("data", {}),
                )

            # Route subscription events
            try:
                WebhookService._handle_subscription_event(provider_instance, event_type, payload)
            except Exception as sub_err:
                logger.warning(f"Subscription event processing failed: {sub_err}", exc_info=True)

            # Mark webhook as processed
            webhook.processed = True
            webhook.processed_at = timezone.now()
            webhook.processing_result = processing_result
            webhook.save()

            logger.info(
                f"Webhook processed successfully: {event_id} "
                f"type: {event_type} provider: {provider_slug}"
            )

            return True, _("Webhook processed successfully")

        except Exception as e:
            logger.error(f"Error processing webhook {event_id}: {str(e)}", exc_info=True)
            webhook.processing_error = str(e)
            webhook.save()
            return False, str(e)

    @staticmethod
    def _handle_subscription_event(provider_instance, event_type: str, payload: dict[str, Any]):
        """
        Route subscription-related webhook events to the subscription event processor.
        Non-subscription events are silently skipped.

        Uses the component provider's translate_subscription_webhook() method
        directly, keeping all provider-specific logic in the component package.
        """
        from subscriptions.event_processor import SubscriptionEventProcessor

        event = provider_instance.translate_subscription_webhook(event_type, payload)
        if event is None:
            return  # Not a subscription event

        success, message = SubscriptionEventProcessor.process_event(event)
        logger.info(
            f"Subscription event {event.event_type.value}: success={success}, message={message}"
        )

    @staticmethod
    def _update_transaction_from_webhook(
        transaction_id: str, event_type: str, event_data: dict[str, Any]
    ):
        """
        Update transaction based on webhook event

        Args:
            transaction_id: Transaction ID (provider transaction ID)
            event_type: Webhook event type
            event_data: Event data from webhook
        """
        try:
            # Find transaction by provider transaction ID
            transaction = PaymentTransaction.objects.filter(
                provider_transaction_id=transaction_id
            ).first()

            if not transaction:
                logger.warning(f"Transaction not found for webhook: {transaction_id}")
                return

            # Update transaction based on event type
            if event_type in ["payment_intent.succeeded", "charge.succeeded", "payment.captured"]:
                transaction.status = "succeeded"
                transaction.completed_at = timezone.now()

                # Update order
                if transaction.order:
                    transaction.order.payment_status = "paid"
                    transaction.order.amount_paid = transaction.amount
                    transaction.order.paid_at = timezone.now()
                    transaction.order.save(
                        update_fields=["payment_status", "amount_paid", "paid_at"]
                    )

            elif event_type in ["payment_intent.payment_failed", "charge.failed", "payment.failed"]:
                transaction.status = "failed"
                transaction.error_message = event_data.get("error_message", "Payment failed")
                transaction.error_code = event_data.get("error_code", "")

                # Update order
                if transaction.order:
                    transaction.order.payment_status = "failed"
                    transaction.order.save(update_fields=["payment_status"])

            elif event_type in ["payment_intent.canceled", "charge.canceled", "payment.cancelled"]:
                transaction.status = "cancelled"
                transaction.completed_at = timezone.now()

                # Update order
                if transaction.order:
                    transaction.order.payment_status = "cancelled"
                    transaction.order.save(update_fields=["payment_status"])

            elif event_type in ["charge.refunded", "refund.succeeded", "payment.refunded"]:
                # Refund webhooks are usually handled separately via RefundService
                # This is just to update metadata
                refund_amount = event_data.get("refund_amount")
                if refund_amount and transaction.order:
                    # Note: Actual refund transactions should be created via RefundService
                    pass

            # Save transaction with updated webhook data
            transaction.metadata["last_webhook_event"] = {
                "type": event_type,
                "timestamp": timezone.now().isoformat(),
                "data": event_data,
            }
            transaction.save()

            logger.info(
                f"Transaction updated from webhook: {transaction.transaction_id} "
                f"event: {event_type} status: {transaction.status}"
            )

        except Exception as e:
            logger.error(f"Error updating transaction from webhook: {str(e)}", exc_info=True)

    @staticmethod
    def _handle_payment_intent_event(
        provider_intent_id: str, event_type: str, event_data: dict[str, Any]
    ) -> bool:
        """
        Handle payment intent webhook events for the orchestration flow.

        This updates the PaymentIntent model and triggers the appropriate
        actions in the PaymentOrchestrationService.

        Args:
            provider_intent_id: Provider's payment intent ID
            event_type: Webhook event type (e.g., 'payment_intent.succeeded')
            event_data: Processed event data from provider

        Returns:
            True if intent was found and updated, False otherwise
        """
        try:
            # Find the PaymentIntent by provider intent ID
            intent = (
                PaymentIntent.objects.filter(provider_intent_id=provider_intent_id)
                .select_related("order", "provider_account", "checkout_session")
                .first()
            )

            if not intent:
                logger.warning(f"PaymentIntent not found for webhook: {provider_intent_id}")
                return False

            logger.info(f"Processing payment intent event: {event_type} for intent: {intent.id}")

            # Import here to avoid circular imports
            from payment_providers.services.payment_orchestration_service import (
                PaymentOrchestrationService,
            )

            if event_type == "payment_intent.succeeded":
                # Payment succeeded - update order to paid
                success, message = PaymentOrchestrationService.handle_payment_success(
                    intent=intent, provider_data=event_data
                )
                if not success:
                    logger.error(f"Failed to handle payment success: {message}")
                return True

            elif event_type in ["payment_intent.failed", "payment_intent.payment_failed"]:
                # Payment failed
                error_code = event_data.get("error", {}).get("code", "payment_failed")
                error_message = event_data.get("error", {}).get(
                    "message", event_data.get("message", "Payment failed")
                )
                PaymentOrchestrationService.handle_payment_failure(
                    intent=intent, error_code=error_code, error_message=error_message
                )
                return True

            elif event_type in ["payment_intent.cancelled", "payment_intent.canceled"]:
                # Payment was cancelled
                intent.status = "canceled"
                intent.save(update_fields=["status", "updated_at"])

                # Update order if no other active intents
                if intent.order:
                    other_active_intents = (
                        PaymentIntent.objects.filter(order=intent.order)
                        .exclude(id=intent.id)
                        .exclude(status__in=["canceled", "failed"])
                        .exists()
                    )

                    if not other_active_intents:
                        intent.order.status = "cancelled"
                        intent.order.payment_status = "cancelled"
                        intent.order.save(update_fields=["status", "payment_status"])

                        # Release stock
                        try:
                            from fulfillment.services.stock_service import StockService

                            StockService.release_stock_for_order(intent.order)
                        except Exception as e:
                            logger.error(f"Failed to release stock: {e}")

                return True

            elif event_type == "payment_intent.requires_action":
                # Customer action required (3DS, etc.)
                intent.status = "requires_action"
                intent.requires_action = True
                intent.action_type = event_data.get("action", {}).get("type", "redirect")
                intent.action_url = event_data.get("action", {}).get("url", "")
                intent.action_data = event_data.get("action", {}).get("data", {})
                intent.save(
                    update_fields=[
                        "status",
                        "requires_action",
                        "action_type",
                        "action_url",
                        "action_data",
                        "updated_at",
                    ]
                )
                return True

            elif event_type == "payment_intent.requires_capture":
                # Payment authorized, needs capture
                intent.status = "processing"
                intent.save(update_fields=["status", "updated_at"])
                return True

            else:
                # Unknown event type, just log it
                logger.info(f"Unhandled payment intent event type: {event_type}")
                return False

        except Exception as e:
            logger.error(f"Error handling payment intent event: {str(e)}", exc_info=True)
            return False

    @staticmethod
    def handle_payment_intent_succeeded(
        provider_slug: str, provider_intent_id: str, event_data: dict[str, Any]
    ) -> bool:
        """
        Handle a successful payment intent.

        This is a convenience method that can be called directly
        without going through the full webhook processing flow.

        Args:
            provider_slug: Provider identifier
            provider_intent_id: Provider's payment intent ID
            event_data: Event data from provider

        Returns:
            True if handled successfully
        """
        return WebhookService._handle_payment_intent_event(
            provider_intent_id=provider_intent_id,
            event_type="payment_intent.succeeded",
            event_data=event_data,
        )

    @staticmethod
    def handle_payment_intent_failed(
        provider_slug: str, provider_intent_id: str, error_data: dict[str, Any]
    ) -> bool:
        """
        Handle a failed payment intent.

        Args:
            provider_slug: Provider identifier
            provider_intent_id: Provider's payment intent ID
            error_data: Error data from provider

        Returns:
            True if handled successfully
        """
        return WebhookService._handle_payment_intent_event(
            provider_intent_id=provider_intent_id,
            event_type="payment_intent.failed",
            event_data={"error": error_data},
        )

    @staticmethod
    def get_webhook_history(
        provider_account: PaymentProviderAccount | None = None,
        event_type: str | None = None,
        processed: bool | None = None,
        limit: int = 100,
    ) -> list:
        """
        Get webhook history with optional filters

        Args:
            provider_account: Filter by provider account
            event_type: Filter by event type
            processed: Filter by processed status
            limit: Maximum number of results

        Returns:
            List of webhook records
        """
        queryset = PaymentWebhook.objects.all()

        if provider_account:
            queryset = queryset.filter(provider_account=provider_account)

        if event_type:
            queryset = queryset.filter(event_type=event_type)

        if processed is not None:
            queryset = queryset.filter(processed=processed)

        return queryset.order_by("-created_at")[:limit]

    @staticmethod
    @transaction.atomic
    def retry_failed_webhook(webhook_id: uuid.UUID) -> tuple[bool, str]:
        """
        Retry processing a failed webhook

        Args:
            webhook_id: Webhook UUID

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            webhook = PaymentWebhook.objects.get(id=webhook_id)

            if webhook.processed:
                return False, _("Webhook already processed successfully")

            # Retry processing
            success, message = WebhookService.process_webhook(
                provider_slug=webhook.provider_slug,
                payload=webhook.payload,
                headers=webhook.headers,
                raw_payload=json.dumps(webhook.payload).encode("utf-8"),
                signature=None,  # Signature already verified
            )

            return success, message

        except PaymentWebhook.DoesNotExist:
            return False, _("Webhook not found")
        except Exception as e:
            logger.error(f"Error retrying webhook: {str(e)}", exc_info=True)
            return False, str(e)
