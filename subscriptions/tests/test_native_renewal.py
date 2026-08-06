"""
Native (webhook-driven) renewal fulfilment.

A native subscription is billed by the provider, which sends a
PAYMENT_SUCCEEDED webhook each cycle. SubscriptionEventProcessor must then create
a paid renewal Order so recurring stock/shipping + digital-licence fulfilment run
— just like the fallback engine — while NOT double-fulfilling the first cycle
(checkout already fulfilled it) and staying idempotent on webhook redelivery.
"""

from decimal import Decimal

import pytest

from orders.models import Order
from subscriptions.event_processor import SubscriptionEventProcessor
from subscriptions.events import SubscriptionEvent, SubscriptionEventType
from tests.factories import (
    BillingCycleLogFactory,
    CustomerSubscriptionFactory,
    OrderFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


def _payment_succeeded(event_id, provider_subscription_id="", amount="20.00"):
    return SubscriptionEvent(
        event_type=SubscriptionEventType.PAYMENT_SUCCEEDED,
        event_id=event_id,
        source="webhook",
        provider_subscription_id=provider_subscription_id,
        amount=Decimal(amount),
        currency="USD",
    )


def test_native_first_invoice_records_the_cycle_without_a_second_order():
    order = OrderFactory()
    sub = CustomerSubscriptionFactory(
        provider_mode="native", originating_order=order, billing_cycle_count=0
    )
    before = Order.objects.count()

    SubscriptionEventProcessor._apply_event(sub, _payment_succeeded("evt_first"))

    sub.refresh_from_db()
    # The first invoice is the checkout cycle: recorded + linked to the order,
    # but NO second fulfilment order is created.
    assert sub.billing_logs.count() == 1
    log = sub.billing_logs.get()
    assert log.cycle_number == 1
    assert log.order_id == order.id
    assert sub.billing_cycle_count == 1
    assert Order.objects.count() == before


def test_native_subsequent_invoice_creates_a_paid_renewal_order():
    order = OrderFactory()
    sub = CustomerSubscriptionFactory(
        provider_mode="native", originating_order=order, billing_cycle_count=1
    )
    # Cycle 1 (the checkout cycle) already recorded.
    BillingCycleLogFactory(subscription=sub, cycle_number=1, order=order)
    before = Order.objects.count()

    SubscriptionEventProcessor._apply_event(sub, _payment_succeeded("evt_second"))

    sub.refresh_from_db()
    assert sub.billing_cycle_count == 2
    log = sub.billing_logs.get(cycle_number=2)
    assert log.order_id is not None
    renewal = Order.objects.get(id=log.order_id)
    assert renewal.payment_status == "paid"
    assert renewal.metadata.get("is_subscription_renewal") is True
    assert Order.objects.count() == before + 1


def test_native_first_invoice_without_originating_order_does_fulfil():
    # API-created native sub (no checkout order) — its first invoice must fulfil.
    sub = CustomerSubscriptionFactory(
        provider_mode="native", originating_order=None, billing_cycle_count=0
    )
    before = Order.objects.count()

    SubscriptionEventProcessor._apply_event(sub, _payment_succeeded("evt_api_first"))

    sub.refresh_from_db()
    log = sub.billing_logs.get(cycle_number=1)
    assert log.order_id is not None
    assert Order.objects.get(id=log.order_id).payment_status == "paid"
    assert Order.objects.count() == before + 1


def test_native_renewal_is_idempotent_on_webhook_redelivery():
    order = OrderFactory()
    sub = CustomerSubscriptionFactory(
        provider_mode="native",
        originating_order=order,
        billing_cycle_count=1,
        provider_subscription_id="sub_native_redeliver",
    )
    BillingCycleLogFactory(subscription=sub, cycle_number=1, order=order)
    before = Order.objects.count()

    event = _payment_succeeded("evt_redeliver", provider_subscription_id="sub_native_redeliver")
    SubscriptionEventProcessor.process_event(event)
    SubscriptionEventProcessor.process_event(event)  # redelivery — must be a no-op

    assert Order.objects.count() == before + 1  # exactly one renewal order
