"""
Subscription Manager
Unified API for subscription operations that works with both native and fallback providers.
"""

import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any

from django.db import transaction
from django.utils import timezone

from .models import BillingCycleLog, CustomerSubscription, PaymentToken, SubscriptionPlan
from .provider_base import get_provider, is_subscription_supported

logger = logging.getLogger(__name__)


class SubscriptionManager:
    """
    High-level subscription management API.
    Automatically handles routing to native vs fallback providers.
    """

    def __init__(self, provider_account):
        """
        Initialize manager with payment provider account.

        Args:
            provider_account: PaymentProviderAccount instance
        """
        if not is_subscription_supported(provider_account):
            raise ValueError(
                f"Payment provider '{provider_account.component.name}' does not support subscriptions"
            )

        self.provider_account = provider_account
        self.provider = get_provider(provider_account)
        self.is_native = self.provider.capabilities["native_subscriptions"]

    # ===========================
    # Customer & Payment Methods
    # ===========================

    def create_customer_token(
        self, user, payment_method_data: dict[str, Any], set_as_default: bool = True
    ) -> PaymentToken:
        """
        Create a payment token for recurring billing.

        Args:
            user: Django User instance
            payment_method_data: Provider-specific payment data
            set_as_default: Set as default payment method

        Returns:
            PaymentToken: Created token instance
        """
        # Ensure customer exists at provider
        gateway_customer_id = self._get_or_create_provider_customer(user)

        # Create token at provider
        token_data = self.provider.create_payment_token(
            customer_id=gateway_customer_id, payment_method_data=payment_method_data
        )

        # Create PaymentToken record
        payment_token = PaymentToken.objects.create(
            user=user,
            provider_account=self.provider_account,
            gateway_customer_id=gateway_customer_id,
            gateway_token_id=token_data["token_id"],
            payment_method_type=token_data.get("payment_method_type", "card"),
            card_brand=token_data.get("card_brand", ""),
            card_last4=token_data.get("card_last4", ""),
            card_exp_month=token_data.get("card_exp_month"),
            card_exp_year=token_data.get("card_exp_year"),
            is_default=set_as_default,
            is_active=True,
            is_verified=True,
        )

        logger.info(f"Created payment token {payment_token.token_id} for user {user.id}")
        return payment_token

    def _get_or_create_provider_customer(self, user) -> str:
        """
        Get or create customer at payment provider.

        Args:
            user: Django User instance

        Returns:
            str: Provider's customer ID
        """
        # Check if we already have a customer ID stored
        existing_token = PaymentToken.objects.filter(
            user=user, provider_account=self.provider_account
        ).first()

        if existing_token and existing_token.gateway_customer_id:
            return existing_token.gateway_customer_id

        # Create new customer at provider
        customer_data = self.provider.create_customer(
            user=user, email=user.email, metadata={"user_id": str(user.id)}
        )

        return customer_data["customer_id"]

    # ===========================
    # Pricing Calculations
    # ===========================

    @staticmethod
    def calculate_subscription_price(product, variant, pricing_tier, quantity=1):
        """
        Calculate subscription price from product and pricing tier.

        Args:
            product: Product instance
            variant: Optional ProductVariant instance
            pricing_tier: PlanPricingTier instance
            quantity: Subscription quantity (for per-seat pricing)

        Returns:
            Money: Calculated subscription price
        """
        # Get base price with discount applied
        base_price = pricing_tier.calculate_price(product, variant)

        # Apply quantity multiplier if needed
        if quantity > 1:
            from djmoney.money import Money

            return Money(base_price.amount * quantity, base_price.currency)

        return base_price

    # ===========================
    # Subscription Creation
    # ===========================

    @transaction.atomic
    def create_subscription(
        self,
        user,
        plan: SubscriptionPlan,
        pricing_tier,
        payment_token: PaymentToken,
        product,
        variant=None,
        quantity: int = 1,
        trial_override_days: int | None = None,
        originating_order=None,
    ) -> CustomerSubscription:
        """
        Create a new subscription.
        Handles both native and fallback providers transparently.

        Args:
            user: Django User instance
            plan: SubscriptionPlan instance (template)
            pricing_tier: PlanPricingTier instance (defines billing cycle + discount)
            payment_token: PaymentToken instance
            product: Product instance (REQUIRED - provides base price)
            variant: Optional ProductVariant instance
            quantity: Subscription quantity (for per-seat pricing)
            trial_override_days: Override plan's trial period
            originating_order: Optional Order instance that triggered this subscription

        Returns:
            CustomerSubscription: Created subscription
        """
        # Validate product is provided (required for pricing)
        if not product:
            raise ValueError("Product is required for subscription pricing")

        # Validate payment token
        if payment_token.user != user:
            raise ValueError("Payment token does not belong to this user")

        if payment_token.provider_account != self.provider_account:
            raise ValueError("Payment token is for a different provider account")

        if not payment_token.is_active:
            raise ValueError("Payment token is not active")

        # Calculate trial end date
        trial_end = self._calculate_trial_end(plan, trial_override_days)

        # Calculate billing dates
        now = timezone.now()
        current_period_start = now
        current_period_end = self._calculate_next_billing_date(now, pricing_tier)
        next_billing_date = trial_end if trial_end else current_period_end

        # Determine provider mode
        provider_mode = "native" if self.is_native else "fallback"

        # Create subscription at provider (if native)
        provider_subscription_id = ""
        if self.is_native:
            provider_key = self.provider_account.component.provider_key
            provider_plan_id = plan.get_provider_plan_id(provider_key)
            if not provider_plan_id:
                raise ValueError(
                    f"Plan '{plan.name}' is not configured for provider '{provider_key}'"
                )

            subscription_data = self.provider.create_subscription(
                customer_id=payment_token.gateway_customer_id,
                plan_id=provider_plan_id,
                payment_token_id=payment_token.gateway_token_id,
                trial_end=trial_end,
                metadata={
                    "plan_id": str(plan.plan_id),
                    "user_id": str(user.id),
                },
            )

            provider_subscription_id = subscription_data["subscription_id"]
            # Use provider's dates if available
            current_period_start = subscription_data.get(
                "current_period_start", current_period_start
            )
            current_period_end = subscription_data.get("current_period_end", current_period_end)
            next_billing_date = subscription_data.get("next_billing_date", next_billing_date)

        # Create CustomerSubscription record
        subscription = CustomerSubscription.objects.create(
            user=user,
            plan=plan,
            pricing_tier=pricing_tier,
            product=product,
            variant=variant,
            originating_order=originating_order,
            quantity=quantity,
            payment_provider_account=self.provider_account,
            payment_token=payment_token,
            provider_mode=provider_mode,
            provider_subscription_id=provider_subscription_id,
            status="trial" if trial_end else "active",
            current_period_start=current_period_start,
            current_period_end=current_period_end,
            next_billing_date=next_billing_date,
            trial_end_date=trial_end,
        )

        logger.info(
            f"Created subscription {subscription.subscription_id} "
            f"for user {user.id} in {provider_mode} mode"
        )

        return subscription

    def _calculate_trial_end(
        self, plan: SubscriptionPlan, override_days: int | None
    ) -> datetime | None:
        """Calculate trial end date"""
        trial_days = override_days if override_days is not None else plan.trial_period_days

        if trial_days > 0:
            return timezone.now() + timedelta(days=trial_days)

        return None

    def _calculate_next_billing_date(self, from_date: datetime, pricing_tier) -> datetime:
        """Calculate next billing date based on pricing tier cycle"""
        interval = pricing_tier.billing_interval

        if pricing_tier.billing_cycle == "daily":
            return from_date + timedelta(days=interval)
        elif pricing_tier.billing_cycle == "weekly":
            return from_date + timedelta(weeks=interval)
        elif pricing_tier.billing_cycle == "monthly":
            return from_date + timedelta(days=30 * interval)
        elif pricing_tier.billing_cycle == "quarterly":
            return from_date + timedelta(days=91 * interval)
        elif pricing_tier.billing_cycle == "semiannual":
            return from_date + timedelta(days=182 * interval)
        elif pricing_tier.billing_cycle == "annual":
            return from_date + timedelta(days=365 * interval)
        else:
            raise ValueError(f"Unknown billing cycle: {pricing_tier.billing_cycle}")

    # ===========================
    # Subscription Management
    # ===========================

    @transaction.atomic
    def cancel_subscription(
        self, subscription: CustomerSubscription, immediately: bool = False, reason: str = ""
    ) -> CustomerSubscription:
        """
        Cancel a subscription.

        Args:
            subscription: CustomerSubscription instance
            immediately: If True, cancel immediately; otherwise at period end
            reason: Cancellation reason

        Returns:
            CustomerSubscription: Updated subscription
        """
        if subscription.status in ["canceled", "expired"]:
            raise ValueError("Subscription is already canceled or expired")

        # Cancel at provider (if native)
        if self.is_native and subscription.provider_subscription_id:
            self.provider.cancel_subscription(
                subscription_id=subscription.provider_subscription_id, immediately=immediately
            )

        # Update subscription
        if immediately:
            subscription.status = "canceled"
            subscription.canceled_at = timezone.now()
            subscription.cancellation_type = "immediate"
        else:
            subscription.cancellation_type = "end_of_period"

        subscription.cancellation_reason = reason
        subscription.scheduled_plan_change = {}

        # Set reactivation deadline if plan allows
        if subscription.plan.reactivation_period_days > 0:
            subscription.reactivation_deadline = timezone.now() + timedelta(
                days=subscription.plan.reactivation_period_days
            )
        else:
            subscription.reactivation_deadline = None

        subscription.save()

        logger.info(
            f"Canceled subscription {subscription.subscription_id} "
            f"({'immediately' if immediately else 'at period end'})"
        )

        return subscription

    @transaction.atomic
    def pause_subscription(
        self,
        subscription: CustomerSubscription,
        reason: str = "",
        auto_resume_date: datetime | None = None,
    ) -> CustomerSubscription:
        """
        Pause a subscription.

        Args:
            subscription: CustomerSubscription instance
            reason: Pause reason
            auto_resume_date: Optional date to automatically resume

        Returns:
            CustomerSubscription: Updated subscription
        """
        if subscription.status not in ["active", "trial"]:
            raise ValueError("Can only pause active or trial subscriptions")

        # Pause at provider (if native)
        if self.is_native and subscription.provider_subscription_id:
            self.provider.pause_subscription(subscription_id=subscription.provider_subscription_id)

        # Update subscription
        subscription.status = "paused"
        subscription.paused_at = timezone.now()
        subscription.pause_reason = reason
        subscription.auto_resume_date = auto_resume_date
        subscription.save()

        logger.info(f"Paused subscription {subscription.subscription_id}")

        return subscription

    @transaction.atomic
    def resume_subscription(self, subscription: CustomerSubscription) -> CustomerSubscription:
        """
        Resume a paused subscription.

        Args:
            subscription: CustomerSubscription instance

        Returns:
            CustomerSubscription: Updated subscription
        """
        if subscription.status != "paused":
            raise ValueError("Can only resume paused subscriptions")

        # Resume at provider (if native)
        if self.is_native and subscription.provider_subscription_id:
            self.provider.resume_subscription(subscription_id=subscription.provider_subscription_id)

        # Update subscription
        subscription.status = "active"
        subscription.paused_at = None
        subscription.pause_reason = ""
        subscription.auto_resume_date = None
        subscription.save()

        logger.info(f"Resumed subscription {subscription.subscription_id}")

        return subscription

    @transaction.atomic
    def reactivate_subscription(
        self, subscription: CustomerSubscription, payment_token: PaymentToken | None = None
    ) -> CustomerSubscription:
        """
        Reactivate a canceled subscription within the reactivation window.

        Starts a new billing period from now. For native providers, creates a
        new provider subscription (Stripe doesn't support un-canceling).

        Args:
            subscription: CustomerSubscription instance (must be canceled)
            payment_token: Optional new PaymentToken (uses existing if not provided)

        Returns:
            CustomerSubscription: Reactivated subscription
        """
        if not subscription.can_reactivate():
            raise ValueError(
                "Subscription cannot be reactivated. "
                "It may not be canceled or the reactivation window has expired."
            )

        # Determine effective payment token
        effective_token = payment_token or subscription.payment_token

        if not effective_token:
            raise ValueError("No payment token available for reactivation")

        if not effective_token.is_active:
            raise ValueError("Payment token is not active")

        if effective_token.is_expired():
            raise ValueError("Payment token has expired. Please provide a new payment method.")

        if effective_token.user != subscription.user:
            raise ValueError("Payment token does not belong to subscription owner")

        # Store previous cancellation date for event context
        previous_canceled_at = subscription.canceled_at

        # Calculate new billing period
        now = timezone.now()
        period_start = now
        period_end = self._calculate_next_billing_date(now, subscription.pricing_tier)
        next_billing_date = period_end

        # Native path: create new provider subscription
        if self.is_native:
            provider_key = self.provider_account.component.provider_key
            provider_plan_id = subscription.plan.get_provider_plan_id(provider_key)
            if not provider_plan_id:
                raise ValueError(
                    f"Plan '{subscription.plan.name}' is not configured for "
                    f"provider '{provider_key}'"
                )

            # Store old provider subscription ID in metadata
            old_provider_id = subscription.provider_subscription_id
            if old_provider_id:
                prev_ids = subscription.metadata.get("previous_provider_subscription_ids", [])
                prev_ids.append(old_provider_id)
                subscription.metadata["previous_provider_subscription_ids"] = prev_ids

            # Create new provider subscription
            subscription_data = self.provider.create_subscription(
                customer_id=effective_token.gateway_customer_id,
                plan_id=provider_plan_id,
                payment_token_id=effective_token.gateway_token_id,
                metadata={
                    "plan_id": str(subscription.plan.plan_id),
                    "user_id": str(subscription.user.id),
                    "reactivated_from": str(subscription.subscription_id),
                },
            )

            subscription.provider_subscription_id = subscription_data["subscription_id"]
            # Use provider's dates if available
            period_start = subscription_data.get("current_period_start", period_start)
            period_end = subscription_data.get("current_period_end", period_end)
            next_billing_date = subscription_data.get("next_billing_date", next_billing_date)

        # Update subscription fields
        subscription.status = "active"
        subscription.payment_token = effective_token
        subscription.current_period_start = period_start
        subscription.current_period_end = period_end
        subscription.next_billing_date = next_billing_date
        subscription.canceled_at = None
        subscription.cancellation_type = "none"
        subscription.cancellation_reason = ""
        subscription.reactivation_deadline = None
        subscription.scheduled_plan_change = {}
        subscription.save()

        logger.info(
            f"Reactivated subscription {subscription.subscription_id} "
            f"for user {subscription.user.id}"
        )

        # Emit reactivation event
        from .events import SubscriptionEventType
        from .tasks import _emit_fallback_event

        _emit_fallback_event(
            subscription,
            SubscriptionEventType.REACTIVATED,
            extra_data={
                "previous_cancellation_date": (
                    previous_canceled_at.isoformat() if previous_canceled_at else ""
                ),
            },
        )

        return subscription

    @transaction.atomic
    def update_payment_method(
        self, subscription: CustomerSubscription, payment_token: PaymentToken
    ) -> CustomerSubscription:
        """
        Update subscription payment method.

        Args:
            subscription: CustomerSubscription instance
            payment_token: New PaymentToken instance

        Returns:
            CustomerSubscription: Updated subscription
        """
        # Validate payment token
        if payment_token.user != subscription.user:
            raise ValueError("Payment token does not belong to subscription owner")

        if payment_token.provider_account != subscription.payment_provider_account:
            raise ValueError("Payment token is for a different provider account")

        # Update at provider (if native)
        if self.is_native and subscription.provider_subscription_id:
            self.provider.update_subscription(
                subscription_id=subscription.provider_subscription_id,
                payment_token_id=payment_token.gateway_token_id,
            )

        # Update subscription
        subscription.payment_token = payment_token
        subscription.save()

        logger.info(f"Updated payment method for subscription {subscription.subscription_id}")

        return subscription

    # ===========================
    # Plan Changes & Proration
    # ===========================

    @staticmethod
    def _calculate_proration(
        subscription: CustomerSubscription,
        new_plan: SubscriptionPlan,
        new_tier,
    ) -> dict:
        """
        Calculate proration for a plan change.

        Returns:
            dict: {
                'days_remaining': int,
                'total_days': int,
                'old_price': Money,
                'new_price': Money,
                'proration_amount': Money,  # positive=charge, negative=credit
                'change_type': 'upgrade' | 'downgrade',
            }
        """
        from djmoney.money import Money

        now = timezone.now()
        period_start = subscription.current_period_start
        period_end = subscription.current_period_end

        total_days = max((period_end - period_start).days, 1)
        days_remaining = max((period_end - now).days, 0)

        old_price = subscription.pricing_tier.calculate_price(
            subscription.product, subscription.variant
        )
        new_price = new_tier.calculate_price(subscription.product, subscription.variant)

        old_daily_rate = old_price.amount / Decimal(str(total_days))
        new_daily_rate = new_price.amount / Decimal(str(total_days))

        proration_raw = (new_daily_rate - old_daily_rate) * Decimal(str(days_remaining))
        change_type = "upgrade" if new_price.amount > old_price.amount else "downgrade"

        return {
            "days_remaining": days_remaining,
            "total_days": total_days,
            "old_price": old_price,
            "new_price": new_price,
            "proration_amount": Money(proration_raw.quantize(Decimal("0.01")), old_price.currency),
            "change_type": change_type,
        }

    @transaction.atomic
    def change_plan(
        self,
        subscription: CustomerSubscription,
        new_plan: SubscriptionPlan,
        new_tier,
        mode: str = "auto",
    ) -> CustomerSubscription:
        """
        Change subscription plan (upgrade or downgrade).

        Args:
            subscription: CustomerSubscription instance
            new_plan: Target SubscriptionPlan
            new_tier: Target PlanPricingTier
            mode: 'immediate', 'at_renewal', or 'auto' (uses plan config)

        Returns:
            CustomerSubscription: Updated subscription
        """
        if subscription.status not in ("active", "trial"):
            raise ValueError("Can only change plan for active or trial subscriptions")

        if new_plan == subscription.plan and new_tier == subscription.pricing_tier:
            raise ValueError("New plan/tier is the same as current")

        if not new_plan.is_active:
            raise ValueError("Target plan is not active")

        if not new_tier.is_active:
            raise ValueError("Target pricing tier is not active")

        if new_tier.plan != new_plan:
            raise ValueError("Pricing tier does not belong to the specified plan")

        proration = self._calculate_proration(subscription, new_plan, new_tier)
        change_type = proration["change_type"]

        if mode == "auto":
            if change_type == "upgrade":
                mode = new_plan.upgrade_behavior
            else:
                mode = subscription.plan.downgrade_behavior

        old_plan = subscription.plan
        old_tier = subscription.pricing_tier

        if mode == "at_renewal":
            return self._schedule_plan_change(
                subscription, new_plan, new_tier, proration, change_type
            )
        else:
            return self._apply_immediate_plan_change(
                subscription, old_plan, old_tier, new_plan, new_tier, proration, change_type
            )

    def _schedule_plan_change(self, subscription, new_plan, new_tier, proration, change_type):
        """Schedule plan change for next renewal."""
        subscription.scheduled_plan_change = {
            "new_plan_id": str(new_plan.plan_id),
            "new_tier_id": str(new_tier.tier_id),
            "change_type": change_type,
            "old_plan_id": str(subscription.plan.plan_id),
            "old_tier_id": str(subscription.pricing_tier.tier_id),
            "old_plan_name": subscription.plan.name,
            "new_plan_name": new_plan.name,
            "scheduled_at": timezone.now().isoformat(),
            "effective_date": (
                subscription.current_period_end.isoformat()
                if subscription.current_period_end
                else ""
            ),
        }
        subscription.save(update_fields=["scheduled_plan_change"])

        logger.info(
            f"Scheduled {change_type} for subscription {subscription.subscription_id} "
            f"from {subscription.plan.name} to {new_plan.name} at renewal"
        )

        # Emit event for email notification
        self._emit_plan_change_event(
            subscription,
            change_type,
            proration,
            new_plan,
            new_tier,
            scheduled=True,
        )

        return subscription

    def _apply_immediate_plan_change(
        self, subscription, old_plan, old_tier, new_plan, new_tier, proration, change_type
    ):
        """Apply plan change immediately with proration handling."""
        from djmoney.money import Money

        if self.is_native and subscription.provider_subscription_id:
            # Native provider path (e.g., Stripe) — provider handles proration
            provider_key = self.provider_account.component.provider_key
            new_provider_plan_id = new_plan.get_provider_plan_id(provider_key)
            if not new_provider_plan_id:
                raise ValueError(
                    f"Plan '{new_plan.name}' not configured for provider '{provider_key}'"
                )

            self.provider.update_subscription(
                subscription_id=subscription.provider_subscription_id,
                plan_id=new_provider_plan_id,
                proration_behavior="create_prorations",
            )
        else:
            # Fallback provider path — we handle proration
            is_trial = subscription.status == "trial"

            if (
                not is_trial
                and change_type == "upgrade"
                and proration["proration_amount"].amount > 0
            ):
                # Charge proration difference immediately
                charge_result = self.provider.charge_payment_token(
                    token_id=subscription.payment_token.gateway_token_id,
                    amount=proration["proration_amount"].amount,
                    currency=str(proration["proration_amount"].currency),
                    description=(f"Plan upgrade proration: {old_plan.name} -> {new_plan.name}"),
                    metadata={
                        "subscription_id": str(subscription.subscription_id),
                        "proration": True,
                        "change_type": change_type,
                    },
                )

                if charge_result["status"] != "succeeded":
                    raise ValueError(
                        f"Proration charge failed: "
                        f"{charge_result.get('error_message', 'Unknown error')}"
                    )

                # Store proration charge in metadata for audit trail
                subscription.metadata["last_proration_charge"] = {
                    "amount": str(proration["proration_amount"].amount),
                    "currency": str(proration["proration_amount"].currency),
                    "transaction_id": charge_result.get("transaction_id", ""),
                    "old_plan": old_plan.name,
                    "new_plan": new_plan.name,
                    "charged_at": timezone.now().isoformat(),
                }

            elif (
                not is_trial
                and change_type == "downgrade"
                and proration["proration_amount"].amount < 0
            ):
                # Store credit for next billing
                credit = Money(
                    abs(proration["proration_amount"].amount),
                    proration["proration_amount"].currency,
                )
                subscription.proration_credit = credit

        # Update subscription record
        subscription.plan = new_plan
        subscription.pricing_tier = new_tier
        subscription.scheduled_plan_change = {}
        subscription.save()

        logger.info(
            f"Applied immediate {change_type} for subscription "
            f"{subscription.subscription_id}: {old_plan.name} -> {new_plan.name}"
        )

        # Emit event for email notification
        self._emit_plan_change_event(
            subscription,
            change_type,
            proration,
            new_plan,
            new_tier,
            scheduled=False,
            old_plan=old_plan,
        )

        return subscription

    def _emit_plan_change_event(
        self,
        subscription,
        change_type,
        proration,
        new_plan,
        new_tier,
        scheduled=False,
        old_plan=None,
    ):
        """Emit a PLAN_UPGRADED or PLAN_DOWNGRADED event."""
        from .event_processor import SubscriptionEventProcessor
        from .events import SubscriptionEvent, SubscriptionEventType

        event_type = (
            SubscriptionEventType.PLAN_UPGRADED
            if change_type == "upgrade"
            else SubscriptionEventType.PLAN_DOWNGRADED
        )

        event_data = {
            "internal_subscription_id": str(subscription.subscription_id),
            "old_plan_name": (
                old_plan.name
                if old_plan
                else subscription.scheduled_plan_change.get("old_plan_name", "")
            ),
            "new_plan_name": new_plan.name,
            "change_type": change_type,
            "new_price": str(proration["new_price"]),
            "billing_period": new_tier.get_billing_display(),
            "scheduled": scheduled,
        }

        if scheduled and subscription.current_period_end:
            event_data["effective_date"] = subscription.current_period_end.isoformat()

        if change_type == "upgrade" and proration["proration_amount"].amount > 0:
            event_data["prorated_charge"] = str(proration["proration_amount"])
        elif change_type == "downgrade" and proration["proration_amount"].amount < 0:
            event_data["credit_amount"] = str(abs(proration["proration_amount"].amount))

        try:
            event = SubscriptionEvent(
                event_type=event_type,
                event_id=SubscriptionEvent.generate_fallback_event_id(
                    str(subscription.subscription_id), event_type.value
                ),
                source="fallback",
                provider_subscription_id=subscription.provider_subscription_id or "",
                data=event_data,
            )
            SubscriptionEventProcessor.process_event(event)
        except Exception as e:
            logger.warning(
                f"Failed to emit plan change event for {subscription.subscription_id}: {e}"
            )

    # ===========================
    # Fallback Billing Engine
    # ===========================

    def process_billing_cycle(self, subscription: CustomerSubscription) -> BillingCycleLog:
        """
        Process a billing cycle for fallback subscriptions.
        Called by Celery task for fallback providers.

        Args:
            subscription: CustomerSubscription instance

        Returns:
            BillingCycleLog: Created billing log
        """
        if self.is_native:
            raise ValueError("process_billing_cycle should only be called for fallback providers")

        from djmoney.money import Money

        cycle_number = subscription.billing_cycle_count + 1

        # Calculate amount from product price + tier discount
        base_amount = subscription.pricing_tier.calculate_price(
            subscription.product, subscription.variant
        )

        # Apply proration credit from downgrade if available
        proration_adjustment = Money(Decimal("0.00"), base_amount.currency)
        charge_amount = base_amount
        remaining_credit = None

        if subscription.proration_credit and subscription.proration_credit.amount > 0:
            credit = subscription.proration_credit
            if credit.amount >= base_amount.amount:
                # Credit covers entire bill
                proration_adjustment = Money(-base_amount.amount, base_amount.currency)
                remaining_credit = Money(credit.amount - base_amount.amount, credit.currency)
                charge_amount = Money(Decimal("0.00"), base_amount.currency)
            else:
                # Partial credit
                proration_adjustment = Money(-credit.amount, credit.currency)
                charge_amount = Money(base_amount.amount - credit.amount, base_amount.currency)
                remaining_credit = Money(Decimal("0.00"), credit.currency)

        # Create billing log
        billing_log = BillingCycleLog.objects.create(
            subscription=subscription,
            cycle_number=cycle_number,
            billing_date=timezone.now(),
            base_amount=base_amount,
            proration_amount=proration_adjustment,
            total_amount=charge_amount,
            status="processing",
        )

        try:
            if charge_amount.amount <= 0:
                # Credit covers full bill — no charge needed
                billing_log.status = "successful"
                billing_log.billing_breakdown = {
                    "proration_credit_applied": str(abs(proration_adjustment.amount)),
                    "charge_waived": True,
                }
                billing_log.save()
                charge_result = {"status": "succeeded"}
            else:
                # Charge payment token
                charge_result = self.provider.charge_payment_token(
                    token_id=subscription.payment_token.gateway_token_id,
                    amount=charge_amount.amount,
                    currency=str(charge_amount.currency),
                    description=f"Subscription billing - {subscription.plan.name}",
                    metadata={
                        "subscription_id": str(subscription.subscription_id),
                        "cycle_number": cycle_number,
                    },
                )

            if charge_result["status"] == "succeeded":
                # Successful charge
                if billing_log.status != "successful":
                    billing_log.status = "successful"
                    billing_log.provider_response = charge_result
                    billing_log.save()

                # Clear proration credit after successful application
                if remaining_credit is not None:
                    subscription.proration_credit = remaining_credit

                # Update subscription
                subscription.billing_cycle_count = cycle_number
                subscription.last_billing_date = timezone.now()
                subscription.last_billing_status = "successful"
                subscription.status = "active"

                # Calculate next billing date
                subscription.current_period_start = subscription.current_period_end
                subscription.current_period_end = self._calculate_next_billing_date(
                    subscription.current_period_end, subscription.pricing_tier
                )
                subscription.next_billing_date = subscription.current_period_end

                subscription.save()

                logger.info(f"Successfully billed subscription {subscription.subscription_id}")

            else:
                # Failed charge
                billing_log.status = "failed"
                billing_log.error_message = charge_result.get("error_message", "")
                billing_log.error_code = charge_result.get("error_code", "")
                billing_log.provider_response = charge_result
                billing_log.save()

                # Update subscription status
                subscription.status = "past_due"
                subscription.last_billing_status = "failed"
                subscription.save()

                logger.error(
                    f"Failed to bill subscription {subscription.subscription_id}: "
                    f"{charge_result.get('error_message')}"
                )

        except Exception as e:
            billing_log.status = "failed"
            billing_log.error_message = str(e)
            billing_log.save()

            subscription.status = "past_due"
            subscription.last_billing_status = "failed"
            subscription.save()

            logger.exception(f"Exception billing subscription {subscription.subscription_id}")

        return billing_log
