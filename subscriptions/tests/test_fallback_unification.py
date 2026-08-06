"""
Storefront subscriptions bill through the platform's fallback engine for EVERY
provider — including native-capable ones (Stripe/PayPal) — so a provider-managed
subscription never charges cycle 1 a second time on top of the checkout charge.
"""

from datetime import timedelta

import pytest
from django.utils import timezone

from subscriptions.manager import SubscriptionManager
from tests.factories import (
    OrderFactory,
    PaymentProviderAccountFactory,
    PaymentTokenFactory,
    PlanPricingTierFactory,
    ProductFactory,
    SubscriptionPlanFactory,
    UserFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


def test_storefront_subscription_on_a_native_provider_is_fallback_no_double_charge():
    user = UserFactory()
    account = PaymentProviderAccountFactory(native_capable=True, user=user)
    token = PaymentTokenFactory(provider_account=account, user=user)
    plan = SubscriptionPlanFactory()
    tier = PlanPricingTierFactory(plan=plan)
    manager = SubscriptionManager(account)

    # The provider genuinely CAN manage subscriptions natively...
    assert manager.is_native is True

    sub = manager.create_subscription(
        user=user,
        plan=plan,
        pricing_tier=tier,
        payment_token=token,
        product=ProductFactory(),
        originating_order=OrderFactory(user=user),
    )

    # ...but the storefront default creates it in FALLBACK mode with NO native
    # provider subscription, so the provider does not bill cycle 1 again.
    assert sub.provider_mode == "fallback"
    assert sub.provider_subscription_id == ""

    # And the platform billing engine bills its renewals (the gate keys off the
    # subscription's mode, not the provider's capability).
    sub.next_billing_date = timezone.now() - timedelta(hours=1)
    sub.save(update_fields=["next_billing_date"])
    log = manager.process_billing_cycle(sub)
    assert log is not None
    assert log.status == "successful"


def test_native_provider_managed_billing_is_available_on_explicit_opt_in():
    # Opt-in native mode still creates a provider-managed subscription.
    user = UserFactory()
    account = PaymentProviderAccountFactory(native_capable=True, user=user)
    token = PaymentTokenFactory(provider_account=account, user=user)
    plan = SubscriptionPlanFactory(provider_plan_mappings={account.component.slug: "price_fake"})
    tier = PlanPricingTierFactory(plan=plan)
    manager = SubscriptionManager(account)

    sub = manager.create_subscription(
        user=user,
        plan=plan,
        pricing_tier=tier,
        payment_token=token,
        product=ProductFactory(),
        use_native_provider=True,
    )

    assert sub.provider_mode == "native"
    assert sub.provider_subscription_id == "sub_native_fake"
