"""
Payment Orchestration Service

Orchestrates payment flows between checkout and payment providers.
This is the main entry point for initiating payments from checkout.

Flow:
1. create_payment_intent() → Creates Order (unpaid) + PaymentIntent
2. Customer pays via provider (hosted/embedded)
3. handle_payment_success() → Updates Order to 'paid'
"""

import logging
from datetime import timedelta
from typing import Any

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from cart.models import CheckoutSession
from orders.models import Order
from payment_providers.models import (
    PaymentIntent,
    PaymentProviderAccount,
    PaymentTransaction,
)
from payment_providers.providers.registry import ProviderRegistry

logger = logging.getLogger(__name__)

# Default payment intent expiry (24 hours)
DEFAULT_INTENT_EXPIRY_HOURS = 24


class PaymentOrchestrationService:
    """
    Orchestrates payment flows for checkout.

    Responsibilities:
    - Create orders and payment intents
    - Handle payment success/failure callbacks
    - Manage payment intent lifecycle
    """

    @staticmethod
    @transaction.atomic
    def create_payment_intent(
        checkout_session: CheckoutSession,
        provider_account: PaymentProviderAccount,
        return_url: str,
        cancel_url: str,
        saved_method_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        expected_total=None,
    ) -> tuple[bool, PaymentIntent | None, str]:
        """
        Create order and payment intent for checkout.

        This method:
        1. Validates checkout session is complete
        2. Creates Order with payment_status='unpaid' (stock allocated)
        3. Calls provider to create payment intent
        4. Creates PaymentIntent record linked to Order
        5. Returns intent with checkout_url or client_secret

        Args:
            checkout_session: Valid CheckoutSession with all steps complete
            provider_account: Payment provider to use
            return_url: URL to redirect after successful payment
            cancel_url: URL to redirect on payment cancellation
            saved_method_id: Optional saved payment method ID
            metadata: Optional additional metadata

        Returns:
            Tuple of (success, PaymentIntent or None, message)
        """

        # Validate provider is active and connected
        if not provider_account.is_active:
            return False, None, _("Payment provider is not active")

        if provider_account.connection_status != "connected":
            return False, None, _("Payment provider is not properly configured")

        # Serialize concurrent intent creation for this session. Without a lock,
        # a double-clicked "Pay" (two requests in flight at once) can both find
        # no existing intent and each create a separate order + provider intent
        # — double charge, double stock allocation. Locking the session row here
        # (inside the surrounding atomic block) makes the second request wait for
        # the first to commit, after which the existing-intent reuse below kicks
        # in. Re-fetch to actually take the row lock.
        checkout_session = CheckoutSession.objects.select_for_update().get(pk=checkout_session.pk)

        # Check for existing unpaid order for this session
        existing_intent = (
            PaymentIntent.objects.filter(
                checkout_session=checkout_session,
                status__in=["created", "requires_payment_method", "requires_action", "processing"],
            )
            .select_related("order")
            .first()
        )

        checkout_session.recalculate_totals()
        if (
            existing_intent
            and existing_intent.order
            and existing_intent.order.total_amount == checkout_session.total_amount
        ):
            # Reuse existing order, create new intent
            order = existing_intent.order
            logger.info(f"Reusing existing order {order.order_number} for retry payment")
        else:
            if existing_intent and existing_intent.order:
                # Cart changed since the order was raised (voucher applied,
                # item edited): a reused order would record the OLD total
                # while the gateway charges the new amount_due. Retire the
                # stale intent and raise a fresh order at current figures.
                logger.info(
                    "Not reusing order %s: total %s != session %s",
                    existing_intent.order.order_number,
                    existing_intent.order.total_amount,
                    checkout_session.total_amount,
                )
                existing_intent.status = "canceled"
                existing_intent.save(update_fields=["status", "updated_at"])
            # Store metadata (including email) in checkout session for order creation
            if metadata:
                if not checkout_session.metadata:
                    checkout_session.metadata = {}
                checkout_session.metadata.update(metadata)
                checkout_session.save(update_fields=["metadata"])

            # Create new order with payment_status='unpaid'.
            # Pass clear_session=False to keep session active. Routed through the
            # placement facade so the drift gate re-prices the cart before an
            # order — and then a payment intent for its amount_due — is created
            # against it. Warn-only by default (SPWIG_ENFORCE_QUOTE_DRIFT), so
            # behaviour is identical to create_order until the flag is flipped.
            from commerce import OrderPlacementService, PlacementRequest

            # Carry the sales channel through so an agent-placed order is
            # attributed as such on the Order. The channel is stamped into the
            # session metadata by the caller (the agentic checkout binding); the
            # web/POS paths leave it unset and default to "web".
            session_channel = (checkout_session.metadata or {}).get("channel", "web")

            # expected_total, when the caller asserts one (an agent attesting a
            # price), is enforced by the drift gate INSIDE the locked placement —
            # it raises QuoteDriftError if the fresh price differs, closing the
            # TOCTOU window between an agent's price check and this charge.
            result = OrderPlacementService.place_order(
                PlacementRequest(
                    session=checkout_session,
                    clear_session=False,
                    channel=session_channel,
                    expected_total=expected_total,
                )
            )
            success, message, order = result.ok, result.message, result.order

            if not success:
                return False, None, message

        # Get provider instance
        try:
            provider_class = ProviderRegistry.get_provider(provider_account.component.slug)
            if not provider_class:
                return False, None, _("Payment provider not found")

            provider = provider_account.get_provider_instance()
        except Exception as e:
            logger.error(f"Failed to get provider instance: {e}")
            return False, None, _("Failed to initialize payment provider")

        # Charge the gateway what is still OWED, not the gross order total.
        #
        # Gift card and wallet tenders are money the customer has already
        # handed over, held against this session. Asking the gateway for
        # `total_amount` bills them a second time for the tendered portion and
        # the card is then debited too on settlement: a 100 order with a 40
        # gift card charged 100 to the card on file AND took 40 off the gift
        # card — 140 collected for a 100 order.
        #
        # `amount_due` is total minus authorized tenders, floored at zero.
        amount_due = checkout_session.amount_due
        amount = amount_due.amount
        currency = str(amount_due.currency)

        # Build metadata
        intent_metadata = {
            "order_id": str(order.id),
            "order_number": order.order_number,
            "checkout_session_id": str(checkout_session.id),
            **(metadata or {}),
        }

        # Get customer email and name.
        # Digital-only orders have no shipping (and usually no billing)
        # address, so fall back to the account holder's name — providers
        # validating like real PSPs (e.g. the Test Gateway in strict mode)
        # reject nameless customers, and real PSPs (Stripe/PayPal) want a
        # billing name for fraud screening and dispute evidence.
        customer_email = order.email or (order.user.email if order.user else None)
        customer_name = order.shipping_name or order.billing_name or ""
        if not customer_name and order.metadata:
            customer_name = (order.metadata.get("contact_name") or "").strip()
        if not customer_name and order.user:
            customer_name = (order.user.get_full_name() or "").strip()

        # Physical deliveries need a carrier-reachable phone number; pass it
        # so providers validating like real PSPs (Test Gateway strict mode)
        # can enforce it. order.phone mirrors the shipping phone at order
        # creation, with billing phone as fallback.
        customer_phone = order.shipping_phone or order.phone or order.billing_phone or ""
        order_requires_shipping = bool(
            checkout_session.cart.requires_shipping if checkout_session.cart_id else False
        )

        # Get customer country from shipping/billing address
        from core.utils import get_default_country

        customer_country = order.shipping_country or order.billing_country or get_default_country()

        # Look up enabled payment methods for customer's country.
        # Country-specific config takes priority; falls back to _global config.
        # If neither exists, pass None so providers show all available methods.
        enabled_methods = (
            provider_account.get_enabled_methods_for_country(customer_country)
            if customer_country
            else []
        )
        payment_method_types = enabled_methods if enabled_methods else None

        # Call provider to create payment intent
        try:
            if hasattr(provider, "create_payment_intent_for_checkout"):
                # customer_phone / order_requires_shipping land in **kwargs
                # for providers that don't consume them (all bundled
                # providers accept **kwargs).
                provider_response = provider.create_payment_intent_for_checkout(
                    amount=amount,
                    currency=currency,
                    return_url=return_url,
                    cancel_url=cancel_url,
                    customer_email=customer_email,
                    customer_name=customer_name,
                    customer_country=customer_country,
                    customer_phone=customer_phone,
                    order_requires_shipping=order_requires_shipping,
                    payment_method_types=payment_method_types,
                    metadata=intent_metadata,
                )
            else:
                # Fallback to standard create_payment_intent if method not implemented
                provider_response = provider.create_payment_intent(
                    amount=float(amount),
                    currency=currency,
                    order_id=order.id,
                    metadata=intent_metadata,
                )
        except Exception as e:
            logger.error(f"Provider create_payment_intent failed: {e}")
            return (
                False,
                None,
                _("Failed to create payment with provider: {error}").format(error=str(e)),
            )

        if not provider_response.get("success"):
            error_msg = provider_response.get("message", "Payment intent creation failed")
            return False, None, error_msg

        # Calculate expiry
        expires_at = timezone.now() + timedelta(hours=DEFAULT_INTENT_EXPIRY_HOURS)
        if provider_response.get("expires_at"):
            expires_at = provider_response["expires_at"]

        # Determine status based on provider response
        status = "created"
        if provider_response.get("requires_action"):
            status = "requires_action"
        elif provider_response.get("status"):
            # Map provider status to our status
            status_map = {
                "requires_payment_method": "requires_payment_method",
                "requires_confirmation": "requires_confirmation",
                "requires_action": "requires_action",
                "processing": "processing",
                "succeeded": "succeeded",
                "canceled": "canceled",
                "failed": "failed",
            }
            status = status_map.get(provider_response["status"], "created")

        # Create PaymentIntent record
        # Safely extract action data (handle case where 'action' key exists but is None)
        action = provider_response.get("action") or {}

        # `.get(key, default)` only returns the default when the key is
        # absent — a present `None` slips through. Providers (e.g. Stripe's
        # embedded-PaymentElement branch) intentionally set
        # `checkout_url`/`client_secret` to `None` when no hosted URL or
        # secret applies. These fields are non-nullable on the model
        # (`CharField`/`URLField` with `blank=True` only), so a `None`
        # would raise NotNullViolation at insert time. Coalesce here.
        payment_intent = PaymentIntent.objects.create(
            checkout_session=checkout_session,
            provider_account=provider_account,
            order=order,
            provider_intent_id=provider_response.get("provider_intent_id") or "",
            client_secret=provider_response.get("client_secret") or "",
            checkout_url=provider_response.get("checkout_url") or "",
            status=status,
            # The amount actually requested from the provider — see above.
            # Order.amount_paid reconciles against settlement rows, so this
            # must be the net figure or the gateway leg reads as an overpay.
            amount=amount_due,
            requires_action=provider_response.get("requires_action", False),
            action_type=action.get("type") or "",
            action_url=action.get("url") or "",
            action_data=action.get("data") or {},
            metadata=intent_metadata,
            provider_response=PaymentIntent._json_safe(
                provider_response.get("raw_response", provider_response)
            ),
            expires_at=expires_at,
        )

        logger.info(
            f"Created PaymentIntent {payment_intent.id} for order {order.order_number} "
            f"via {provider_account.display_name}"
        )

        return True, payment_intent, _("Payment intent created successfully")

    @staticmethod
    def get_payment_intent_status(intent: PaymentIntent) -> dict[str, Any]:
        """
        Get current payment intent status from provider.

        Args:
            intent: PaymentIntent to check

        Returns:
            Dict with status information
        """
        try:
            provider = intent.provider_account.get_provider_instance()

            if hasattr(provider, "retrieve_payment_intent"):
                status_response = provider.retrieve_payment_intent(
                    intent_id=intent.provider_intent_id
                )
            else:
                status_response = provider.get_payment_status(
                    transaction_id=intent.provider_intent_id
                )

            return {
                "success": True,
                "status": status_response.get("status"),
                "provider_status": status_response.get("provider_status"),
                "requires_action": status_response.get("requires_action", False),
                "error": status_response.get("error"),
                "provider_data": status_response,
            }

        except Exception as e:
            logger.error(f"Error getting payment intent status: {e}")
            return {"success": False, "error": str(e)}

    @staticmethod
    def verify_and_sync_payment_status(intent: PaymentIntent) -> dict[str, Any]:
        """
        Verify payment status with provider and trigger webhook handlers
        if the remote status differs from local. Safe to call on any intent —
        returns immediately for terminal intents or intents without provider data.

        Use this from status-polling endpoints to handle delayed/missing webhooks.

        Returns:
            Dict with 'status', 'synced' (bool), and optionally 'error'
        """
        if intent.is_terminal():
            return {"status": intent.status, "synced": False}

        if not intent.provider_intent_id or not intent.provider_account:
            return {"status": intent.status, "synced": False}

        try:
            remote = PaymentOrchestrationService.get_payment_intent_status(intent)
            if not remote.get("success"):
                return {"status": intent.status, "synced": False, "error": remote.get("error")}

            remote_status = remote.get("status", "")
            provider_slug = (
                intent.provider_account.component.slug
                if intent.provider_account and intent.provider_account.component
                else "unknown"
            )

            if remote_status == "succeeded" and intent.status != "succeeded":
                logger.info(
                    f"Payment verification: provider reports succeeded for intent {intent.id}, "
                    f"triggering payment success handling"
                )
                from payment_providers.services.webhook_service import WebhookService

                WebhookService.handle_payment_intent_succeeded(
                    provider_slug=provider_slug,
                    provider_intent_id=intent.provider_intent_id,
                    event_data=remote.get("provider_data", {}),
                )
                intent.refresh_from_db()
                return {"status": intent.status, "synced": True}

            elif remote_status == "failed" and intent.status != "failed":
                logger.info(f"Payment verification: provider reports failed for intent {intent.id}")
                from payment_providers.services.webhook_service import WebhookService

                WebhookService.handle_payment_intent_failed(
                    provider_slug=provider_slug,
                    provider_intent_id=intent.provider_intent_id,
                    error_data=remote.get("provider_data", {}),
                )
                intent.refresh_from_db()
                return {"status": intent.status, "synced": True}

            return {"status": intent.status, "synced": False}

        except Exception as e:
            logger.warning(f"Payment verification failed for intent {intent.id}: {e}")
            return {"status": intent.status, "synced": False, "error": str(e)}

    @staticmethod
    def confirm_payment_intent(
        intent: PaymentIntent, confirmation_data: dict[str, Any] | None = None
    ) -> tuple[bool, str]:
        """
        Confirm payment intent after 3DS or other action.

        Args:
            intent: PaymentIntent to confirm
            confirmation_data: Optional provider-specific confirmation data

        Returns:
            Tuple of (success, message)
        """
        if intent.is_terminal():
            return False, _("Payment intent is already in terminal state")

        # Never charge the gateway for an order that is already paid. Two intents
        # can point at one order (the create-time reuse path mints a fresh intent
        # against an existing order); without this, confirming the second one
        # after the first settled would charge the card a second time.
        order = intent.order
        if order is not None and order.payment_status == "paid":
            return False, _("Order already paid")

        try:
            provider = intent.provider_account.get_provider_instance()

            if hasattr(provider, "confirm_payment_intent"):
                response = provider.confirm_payment_intent(
                    intent_id=intent.provider_intent_id, confirmation_data=confirmation_data
                )
            else:
                return False, _("Provider does not support payment confirmation")

            if response.get("success"):
                # Update intent status
                new_status = response.get("status", "processing")
                if new_status == "succeeded":
                    # handle_payment_success marks the intent succeeded AND
                    # settles the order/transaction/session atomically.
                    # Marking it succeeded here first would trip its
                    # already-processed guard and leave the order unpaid.
                    PaymentOrchestrationService.handle_payment_success(intent, response)
                elif response.get("requires_action"):
                    intent.mark_requires_action(
                        action_type=response.get("action", {}).get("type", ""),
                        action_url=response.get("action", {}).get("url", ""),
                        action_data=response.get("action", {}).get("data"),
                    )
                else:
                    intent.status = new_status
                    intent.provider_response = PaymentIntent._json_safe(response)
                    update_fields = ["status", "provider_response", "updated_at"]
                    # Soft declines (e.g. requires_payment_method after a card
                    # decline) carry the reason so the UI can show it while
                    # the intent stays retryable
                    if response.get("error_code"):
                        intent.error_code = response.get("error_code", "")
                        intent.error_message = response.get("message", "")
                        update_fields += ["error_code", "error_message"]
                    intent.save(update_fields=update_fields)

                return True, _("Payment confirmed")
            else:
                error_msg = response.get("message", "Confirmation failed")
                intent.mark_failed(
                    error_code=response.get("error_code", ""),
                    error_message=error_msg,
                    provider_data=response,
                )
                return False, error_msg

        except Exception as e:
            logger.error(f"Error confirming payment intent: {e}")
            return False, str(e)

    @staticmethod
    def handle_payment_success(
        intent: PaymentIntent, provider_data: dict[str, Any]
    ) -> tuple[bool, str]:
        """
        Handle successful payment.

        This method:
        1. (atomic) Updates Order.payment_status to 'paid'
        2. (atomic) Updates PaymentIntent.status to 'succeeded'
        3. (atomic) Creates PaymentTransaction record
        4. (atomic) Clears checkout session
        5. (non-atomic) Triggers post-payment flows (email, provisioning, etc.)

        Post-payment flows run outside the atomic block so that failures
        in emails, SalesBell logging, or license provisioning don't roll
        back the core payment success.
        """
        # --- Atomic block: core payment state ---
        with transaction.atomic():
            # Re-fetch with row lock to prevent duplicate processing from concurrent polls
            intent = (
                PaymentIntent.objects.select_for_update(of=("self",))
                .select_related("order", "provider_account", "checkout_session")
                .get(pk=intent.pk)
            )

            if intent.status == "succeeded":
                logger.info(f"Payment intent {intent.id} already marked as succeeded")
                return True, _("Payment already processed")

            order = intent.order

            # Lock the ORDER row too: two distinct intents settling the same order
            # concurrently only serialise if they contend on the order, not just
            # their own (distinct) intent rows.
            if order is not None:
                from orders.models import Order

                order = Order.objects.select_for_update().get(pk=order.pk)
                intent.order = order

            # Order-level idempotency: if a DIFFERENT intent already settled this
            # order, record this intent as succeeded but do NOT settle again (no
            # second PaymentTransaction, no amount_paid overwrite). The per-intent
            # guard above cannot catch this — the two intents are distinct rows.
            if order is not None and order.payment_status == "paid":
                logger.warning(
                    "Intent %s confirmed against already-paid order %s; "
                    "recording success without re-settling.",
                    intent.id,
                    order.id,
                )
                intent.mark_succeeded(provider_data)
                return True, _("Order already paid")

            # Update intent status
            intent.mark_succeeded(provider_data)

            # Update order payment status
            order.payment_status = "paid"
            order.paid_at = timezone.now()
            order.amount_paid = intent.amount
            order.payment_provider = intent.provider_account

            # Compute base-currency equivalent for amount_paid
            from decimal import Decimal

            if (
                order.customer_currency
                and order.customer_currency != order.base_currency
                and order.exchange_rate_used
            ):
                rate = order.exchange_rate_used
                if rate and rate != 0:
                    paid_amt = (
                        intent.amount.amount
                        if hasattr(intent.amount, "amount")
                        else Decimal(str(intent.amount or 0))
                    )
                    order.amount_paid_base = (paid_amt / rate).quantize(Decimal("0.01"))
            else:
                order.amount_paid_base = (
                    intent.amount.amount
                    if hasattr(intent.amount, "amount")
                    else Decimal(str(intent.amount or 0))
                )

            # Extract payment method info from provider response
            payment_method_type = provider_data.get("payment_method_type", "")
            payment_method_last4 = provider_data.get("payment_method_last4", "")

            if payment_method_type:
                order.payment_method_type = payment_method_type
            if payment_method_last4:
                order.payment_method_last4 = payment_method_last4

            order.save(
                update_fields=[
                    "payment_status",
                    "paid_at",
                    "amount_paid",
                    "amount_paid_base",
                    "payment_provider",
                    "payment_method_type",
                    "payment_method_last4",
                    "updated_at",
                ]
            )

            # Create PaymentTransaction record
            PaymentTransaction.objects.create(
                provider_account=intent.provider_account,
                order=order,
                transaction_id=f"txn_{intent.id.hex[:16]}",
                provider_transaction_id=intent.provider_intent_id,
                amount=intent.amount,
                status="completed",
                transaction_type="charge",
                customer_email=order.email,
                customer_name=order.shipping_name,
                payment_method_type=payment_method_type,
                payment_method_last4=payment_method_last4,
                provider_response=PaymentIntent._json_safe(provider_data),
                metadata=intent.metadata,
                completed_at=timezone.now(),
            )

            # Create subscriptions and clear checkout session
            if intent.checkout_session:
                cart = intent.checkout_session.cart
                if cart:
                    try:
                        from cart.services.checkout_service import CheckoutService

                        CheckoutService._create_subscriptions(cart, order)
                    except Exception as e:
                        logger.error(
                            f"Failed to create subscriptions for order {order.order_number}: {e}"
                        )

                    cart.items.all().delete()
                    cart.applied_vouchers.all().delete()
                intent.checkout_session.delete()

        # --- Outside atomic: post-payment side effects ---
        # These must not roll back the payment if they fail.
        PaymentOrchestrationService._trigger_post_payment_flows(order)

        logger.info(f"Payment success handled for order {order.order_number}")
        return True, _("Payment processed successfully")

    @staticmethod
    def handle_payment_failure(
        intent: PaymentIntent,
        error_code: str = "",
        error_message: str = "",
        provider_data: dict[str, Any] | None = None,
    ) -> None:
        """
        Handle payment failure.

        Updates intent status to 'failed'.
        Order remains with payment_status='unpaid' for retry.

        Args:
            intent: PaymentIntent that failed
            error_code: Error code from provider
            error_message: Error message from provider
            provider_data: Optional full provider response
        """
        intent.mark_failed(
            error_code=error_code, error_message=error_message, provider_data=provider_data
        )

        logger.warning(f"Payment failed for intent {intent.id}: {error_code} - {error_message}")

    @staticmethod
    @transaction.atomic
    def cancel_payment_intent(intent: PaymentIntent) -> tuple[bool, str]:
        """
        Cancel payment intent and optionally cancel the order.

        Args:
            intent: PaymentIntent to cancel

        Returns:
            Tuple of (success, message)
        """
        if intent.is_terminal():
            return False, _("Payment intent is already in terminal state")

        try:
            # Try to cancel with provider
            provider = intent.provider_account.get_provider_instance()

            if hasattr(provider, "cancel_payment_intent"):
                response = provider.cancel_payment_intent(intent_id=intent.provider_intent_id)
                if not response.get("success"):
                    logger.warning(
                        f"Provider cancel failed for intent {intent.id}: {response.get('message')}"
                    )

            # Update intent status
            intent.status = "canceled"
            intent.save(update_fields=["status", "updated_at"])

            # Update order status if this is the only intent
            order = intent.order
            other_intents = (
                PaymentIntent.objects.filter(order=order)
                .exclude(id=intent.id)
                .exclude(status__in=["canceled", "failed"])
            )

            if not other_intents.exists():
                # Cancel order and release stock
                from catalog.services import fulfillment_service

                for item in order.items.filter(stock_allocated=True):
                    try:
                        fulfillment_service.release_stock(item, item.warehouse)
                        item.stock_allocated = False
                        item.save(update_fields=["stock_allocated"])
                    except Exception as e:
                        logger.error(f"Failed to release stock for item {item.id}: {e}")

                order.status = "cancelled"
                order.payment_status = "cancelled"
                order.save(update_fields=["status", "payment_status", "updated_at"])

            logger.info(f"Payment intent {intent.id} cancelled")
            return True, _("Payment cancelled")

        except Exception as e:
            logger.error(f"Error cancelling payment intent: {e}")
            return False, str(e)

    @staticmethod
    def _trigger_post_payment_flows(order: Order) -> None:
        """
        Trigger post-payment flows after successful payment.

        Args:
            order: Order that was paid
        """
        # Note: Order confirmation email is sent via post_save signal on Order
        # creation (email_system/signals.py). License orders are skipped there
        # and use their own templates via license_checkout.services.

        # Trigger outbound webhooks
        try:
            from webhooks.services import trigger_webhook

            trigger_webhook("order.paid", instance=order)
        except Exception as e:
            logger.error(f"Failed to trigger order.paid webhook: {e}")

        # Award loyalty points if applicable
        try:
            from loyalty.services import award_order_points

            award_order_points(order)
        except Exception as e:
            logger.error(f"Failed to award loyalty points: {e}")

        # Update product sales statistics
        try:
            from orders.services.sales_stats_service import update_product_sales_counts

            update_product_sales_counts(order)
        except Exception as e:
            logger.error(
                f"Failed to update product sales counts for order {order.order_number}: {e}"
            )

        # Update customer metrics (skip guest orders)
        if order.user and not order.user.username.startswith("guest_"):
            try:
                from customers.models import CustomerMetrics

                CustomerMetrics.calculate_for_user(order.user)
            except Exception as e:
                logger.error(
                    f"Failed to update customer metrics for order {order.order_number}: {e}"
                )

        # Log to Sales Bell (HQ only)
        if getattr(settings, "SPWIG_IS_HQ", False):
            try:
                from core.models import SalesBellEvent

                meta = order.metadata or {}
                if meta.get("marketplace"):
                    subtype = "marketplace"
                elif meta.get("dev_license_purchase"):
                    subtype = "dev_license"
                else:
                    subtype = "license"
                SalesBellEvent.log_sale(order, subtype=subtype)
            except Exception as e:
                logger.error(f"Failed to log sales bell event: {e}")

        # Grant marketplace component entitlement (HQ only)
        if getattr(settings, "SPWIG_IS_HQ", False) and order.metadata.get("marketplace"):
            try:
                from marketplace_checkout.services import grant_component_entitlement

                grant_component_entitlement(order)
            except Exception as e:
                logger.error(f"Failed to grant marketplace entitlement: {e}")
                # Flag the order and schedule retry via Celery
                order.metadata["entitlement_grant_failed"] = True
                order.metadata["entitlement_grant_error"] = str(e)[:500]
                order.save(update_fields=["metadata"])
                try:
                    from marketplace_checkout.tasks import retry_grant_entitlement

                    retry_grant_entitlement.delay(str(order.id))
                except Exception as task_err:
                    logger.error(f"Failed to schedule entitlement retry: {task_err}")

        # Provision developer license after purchase (HQ only)
        if getattr(settings, "SPWIG_IS_HQ", False) and order.metadata.get("dev_license_purchase"):
            try:
                from developer_portal.services.license_provisioning import (
                    provision_paid_dev_license,
                )

                provision_paid_dev_license(order)
            except Exception as e:
                logger.error(f"Failed to provision dev license: {e}")
                order.metadata["dev_license_provision_failed"] = True
                order.metadata["dev_license_provision_error"] = str(e)[:500]
                order.save(update_fields=["metadata"])

        # Provision license checkout purchase (HQ only)
        if getattr(settings, "SPWIG_IS_HQ", False) and order.metadata.get("license_checkout"):
            try:
                from license_checkout.services import provision_paid_license

                provision_paid_license(order)
            except Exception as e:
                logger.error(f"Failed to provision license checkout: {e}")
                order.metadata["license_provision_failed"] = True
                order.metadata["license_provision_error"] = str(e)[:500]
                order.save(update_fields=["metadata"])

        # Provision hosted subscription purchase (HQ only)
        if getattr(settings, "SPWIG_IS_HQ", False) and order.metadata.get("hosted_checkout"):
            try:
                from license_checkout.services import provision_hosted_subscription

                provision_hosted_subscription(order)
            except Exception as e:
                logger.error(f"Failed to provision hosted subscription: {e}")
                order.metadata["hosted_provision_failed"] = True
                order.metadata["hosted_provision_error"] = str(e)[:500]
                order.save(update_fields=["metadata"])
