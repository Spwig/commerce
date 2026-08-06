"""
SubscriptionManager.process_billing_cycle — the fallback billing engine.

Exercised with the deterministic fake fallback providers registered in
``tests/factories.py`` (a succeeding one and a declining one). Covers the
happy path (charge + period advance + paid renewal order), a declined charge,
the not-yet-due skip, and the product-gone safety net.
"""

from datetime import timedelta
from decimal import Decimal

import pytest
from django.utils import timezone

from orders.models import Order
from subscriptions.manager import SubscriptionManager
from tests.factories import (
    BillingCycleLogFactory,
    CustomerSubscriptionFactory,
    PaymentProviderAccountFactory,
    PaymentTokenFactory,
    ProductFactory,
    UserFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


def _manager_for(subscription):
    return SubscriptionManager(subscription.payment_provider_account)


def test_due_subscription_is_charged_and_the_period_advances():
    subscription = CustomerSubscriptionFactory(due=True, billing_cycle_count=0)

    log = _manager_for(subscription).process_billing_cycle(subscription)

    subscription.refresh_from_db()
    assert log.status == "successful"
    assert subscription.status == "active"
    assert subscription.billing_cycle_count == 1
    # next_billing_date advanced roughly a month into the future.
    assert subscription.next_billing_date > timezone.now()
    assert subscription.billing_logs.filter(status="successful").count() == 1


def test_failed_charge_moves_subscription_to_past_due():
    user = UserFactory()
    declining_account = PaymentProviderAccountFactory(declining=True)
    token = PaymentTokenFactory(user=user, provider_account=declining_account)
    subscription = CustomerSubscriptionFactory(
        due=True,
        billing_cycle_count=0,
        user=user,
        payment_token=token,
        payment_provider_account=declining_account,
    )

    log = _manager_for(subscription).process_billing_cycle(subscription)

    subscription.refresh_from_db()
    assert log.status == "failed"
    assert subscription.status == "past_due"
    assert subscription.last_billing_status == "failed"
    assert "declined" in (log.error_message or "").lower()


def test_subscription_not_yet_due_is_skipped_and_returns_latest_log():
    now = timezone.now()
    subscription = CustomerSubscriptionFactory(
        billing_cycle_count=1,
        current_period_start=now,
        current_period_end=now + timedelta(days=30),
        next_billing_date=now + timedelta(days=30),  # still in the future
    )
    prior_log = BillingCycleLogFactory(
        subscription=subscription, cycle_number=1, status="successful"
    )

    result = _manager_for(subscription).process_billing_cycle(subscription)

    # No new charge, no new log — the pre-existing log is returned as-is.
    assert result.id == prior_log.id
    assert subscription.billing_logs.count() == 1
    subscription.refresh_from_db()
    assert subscription.billing_cycle_count == 1


def test_subscription_with_no_product_is_marked_past_due_without_crashing():
    subscription = CustomerSubscriptionFactory(due=True, billing_cycle_count=0, product=None)

    log = _manager_for(subscription).process_billing_cycle(subscription)

    subscription.refresh_from_db()
    assert log.status == "failed"
    assert subscription.status == "past_due"
    assert "no longer available" in (log.error_message or "").lower()


def test_successful_cycle_creates_a_paid_renewal_order():
    user = UserFactory()
    product = ProductFactory(price=Decimal("25.00"))
    subscription = CustomerSubscriptionFactory(
        due=True, billing_cycle_count=0, user=user, product=product
    )
    manager = _manager_for(subscription)

    log = manager.process_billing_cycle(subscription)

    log.refresh_from_db()
    assert log.order_id is not None
    order = log.order
    assert order.payment_status == "paid"
    assert order.user == user
    assert order.items.count() == 1
    assert order.items.first().product == product


def test_renewal_order_creation_is_idempotent_for_a_cycle():
    subscription = CustomerSubscriptionFactory(due=True, billing_cycle_count=0)
    manager = _manager_for(subscription)

    log = manager.process_billing_cycle(subscription)
    log.refresh_from_db()
    assert log.order_id is not None

    orders_before = Order.objects.count()
    # A second call for the same cycle must reuse the existing order.
    same_order = manager._create_renewal_order(subscription, log)

    assert same_order.id == log.order_id
    assert Order.objects.count() == orders_before
