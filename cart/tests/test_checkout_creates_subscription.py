"""
CheckoutService._create_subscriptions.

When an order is created from a cart containing subscription lines, each line
with a plan + payment token becomes a CustomerSubscription linked back to the
originating order. The step is idempotent (one set of subscriptions per order),
and a line missing its token is recorded on the order rather than silently
dropped — the customer has already paid.
"""

import pytest

from cart.services import CheckoutService
from subscriptions.models import CustomerSubscription
from tests.factories import (
    CartFactory,
    CartItemFactory,
    OrderFactory,
    PaymentProviderAccountFactory,
    PaymentTokenFactory,
    PlanPricingTierFactory,
    ProductFactory,
    SubscriptionPlanFactory,
    UserFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


def _subscription_cart(user):
    """A cart owned by ``user`` holding one fully-specified subscription line."""
    cart = CartFactory(user=user)
    plan = SubscriptionPlanFactory()
    tier = PlanPricingTierFactory(plan=plan)
    account = PaymentProviderAccountFactory(subscribable=True)
    token = PaymentTokenFactory(user=user, provider_account=account)
    product = ProductFactory(is_subscription_enabled=True, subscription_plans=[plan])
    item = CartItemFactory(
        cart=cart,
        product=product,
        is_subscription=True,
        subscription_plan=plan,
        pricing_tier=tier,
        payment_token=token,
    )
    return cart, item, plan, product


def test_subscription_is_created_and_linked_to_the_originating_order():
    user = UserFactory()
    cart, item, plan, product = _subscription_cart(user)
    order = OrderFactory(user=user)

    created = CheckoutService._create_subscriptions(cart, order)

    assert len(created) == 1
    subscription = CustomerSubscription.objects.get(originating_order=order)
    assert subscription.user == user
    assert subscription.product == product
    assert subscription.plan == plan
    assert subscription.pricing_tier == item.pricing_tier
    # Fallback provider → internal billing engine.
    assert subscription.provider_mode == "fallback"


def test_create_subscriptions_is_idempotent_for_the_same_order():
    user = UserFactory()
    cart, _item, _plan, _product = _subscription_cart(user)
    order = OrderFactory(user=user)

    first = CheckoutService._create_subscriptions(cart, order)
    second = CheckoutService._create_subscriptions(cart, order)

    assert len(first) == 1
    # Per-line idempotency: the second call returns the SAME existing
    # subscription instead of creating a duplicate. This is deliberately safer
    # than a blanket order-level skip — it also retries any line that failed on
    # a previous attempt. The invariant that matters is that no duplicate is
    # ever created.
    assert second == first
    assert CustomerSubscription.objects.filter(originating_order=order).count() == 1


def test_subscription_line_without_a_token_records_a_failure():
    """No token → no subscription, and the gap is recorded on the order."""
    user = UserFactory()
    cart = CartFactory(user=user)
    product = ProductFactory(is_subscription_enabled=True)
    # The ``subscription`` trait wires a plan + tier but leaves payment_token unset.
    item = CartItemFactory(cart=cart, product=product, subscription=True)
    order = OrderFactory(user=user)

    created = CheckoutService._create_subscriptions(cart, order)

    assert created == []
    assert CustomerSubscription.objects.filter(originating_order=order).count() == 0

    order.refresh_from_db()
    assert order.metadata.get("subscription_creation_failures") == [item.id]
