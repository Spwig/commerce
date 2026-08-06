"""
SubscriptionManager.create_subscription and _calculate_next_billing_date.

These use the fake fallback provider registered in ``tests/factories.py`` so the
manager routes through the internal (non-native) billing path.
"""

from datetime import datetime
from decimal import Decimal

import pytest
from django.utils import timezone

from subscriptions.manager import SubscriptionManager
from subscriptions.models import CustomerSubscription
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


def _manager_and_context():
    """Return (manager, user, account, token, product) wired to the fake provider."""
    user = UserFactory()
    account = PaymentProviderAccountFactory(subscribable=True)
    token = PaymentTokenFactory(user=user, provider_account=account)
    product = ProductFactory(price=Decimal("25.00"))
    return SubscriptionManager(account), user, account, token, product


def test_subscription_starts_in_trial_when_the_plan_has_a_trial():
    manager, user, _account, token, product = _manager_and_context()
    plan = SubscriptionPlanFactory(trial_period_days=14)
    tier = PlanPricingTierFactory(plan=plan)

    subscription = manager.create_subscription(
        user=user, plan=plan, pricing_tier=tier, payment_token=token, product=product
    )

    assert subscription.status == "trial"
    assert subscription.trial_end_date is not None
    # First charge is deferred to the end of the trial.
    assert subscription.next_billing_date == subscription.trial_end_date
    assert subscription.provider_mode == "fallback"


def test_subscription_without_a_trial_starts_active():
    manager, user, _account, token, product = _manager_and_context()
    plan = SubscriptionPlanFactory(trial_period_days=0)
    tier = PlanPricingTierFactory(plan=plan)

    subscription = manager.create_subscription(
        user=user, plan=plan, pricing_tier=tier, payment_token=token, product=product
    )

    assert subscription.status == "active"
    assert subscription.trial_end_date is None


def test_create_subscription_binds_the_originating_order():
    manager, user, _account, token, product = _manager_and_context()
    plan = SubscriptionPlanFactory()
    tier = PlanPricingTierFactory(plan=plan)
    order = OrderFactory(user=user)

    subscription = manager.create_subscription(
        user=user,
        plan=plan,
        pricing_tier=tier,
        payment_token=token,
        product=product,
        originating_order=order,
    )

    assert subscription.originating_order == order


def test_create_subscription_is_idempotent_per_order_product_and_plan():
    manager, user, _account, token, product = _manager_and_context()
    plan = SubscriptionPlanFactory()
    tier = PlanPricingTierFactory(plan=plan)
    order = OrderFactory(user=user)

    first = manager.create_subscription(
        user=user,
        plan=plan,
        pricing_tier=tier,
        payment_token=token,
        product=product,
        originating_order=order,
    )
    second = manager.create_subscription(
        user=user,
        plan=plan,
        pricing_tier=tier,
        payment_token=token,
        product=product,
        originating_order=order,
    )

    # The second call returns the existing subscription, not a duplicate.
    assert first.subscription_id == second.subscription_id
    assert (
        CustomerSubscription.objects.filter(
            originating_order=order, product=product, plan=plan
        ).count()
        == 1
    )


def test_monthly_next_billing_date_is_calendar_correct():
    """Monthly billing advances to the same day-of-month via relativedelta."""
    manager = SubscriptionManager(PaymentProviderAccountFactory(subscribable=True))
    tier = PlanPricingTierFactory(billing_cycle="monthly", billing_interval=1)

    # Jan 31 → Feb 28 in a non-leap year (relativedelta clamps to month end).
    jan31_2023 = timezone.make_aware(datetime(2023, 1, 31, 12, 0))
    nxt = manager._calculate_next_billing_date(jan31_2023, tier)
    assert (nxt.year, nxt.month, nxt.day) == (2023, 2, 28)

    # Jan 31 → Feb 29 in a leap year.
    jan31_2024 = timezone.make_aware(datetime(2024, 1, 31, 12, 0))
    nxt_leap = manager._calculate_next_billing_date(jan31_2024, tier)
    assert (nxt_leap.year, nxt_leap.month, nxt_leap.day) == (2024, 2, 29)

    # A normal mid-month date lands on the same day next month.
    mid = timezone.make_aware(datetime(2025, 3, 15, 9, 30))
    nxt_mid = manager._calculate_next_billing_date(mid, tier)
    assert (nxt_mid.year, nxt_mid.month, nxt_mid.day) == (2025, 4, 15)
