"""
Edge- and negative-case hardening for four subscription capabilities that
previously carried a single happy-path test each:

* ``calculate_subscription_price`` — ``PlanPricingTier.calculate_price`` and the
  quantity-aware ``SubscriptionManager.calculate_subscription_price`` wrapper.
* ``create_subscription`` — token ownership / provider / active guards, the
  required-product guard, and the per-order idempotency path.
* ``reactivate_subscription`` — the reactivation-window, token-active,
  token-expiry and non-canceled guards.
* ``retry_failed_billing`` — the ``retry_billing_cycle`` Celery task: recovery,
  exponential backoff scheduling, grace period, and auto-cancel.

Reuses the deterministic fake fallback providers and factories from
``tests/factories.py`` (succeeding + ``declining`` provider accounts). No
non-test code is touched.
"""

from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

import pytest
from django.utils import timezone
from djmoney.money import Money

from subscriptions.manager import SubscriptionManager
from subscriptions.models import CustomerSubscription
from subscriptions.tasks import retry_billing_cycle
from tests.factories import (
    BillingCycleLogFactory,
    CustomerSubscriptionFactory,
    OrderFactory,
    PaymentProviderAccountFactory,
    PaymentTokenFactory,
    PlanPricingTierFactory,
    ProductFactory,
    ProductVariantFactory,
    SubscriptionPlanFactory,
    UserFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


def _manager_for(subscription):
    return SubscriptionManager(subscription.payment_provider_account)


# ============================================================
# 1. calculate_subscription_price
# ============================================================


def test_zero_discount_tier_returns_full_product_price():
    """A 0% tier charges the untouched product price."""
    product = ProductFactory(price=Decimal("40.00"))
    tier = PlanPricingTierFactory(discount_percentage=Decimal("0.00"))

    price = tier.calculate_price(product)

    assert price.amount == Decimal("40.00")


def test_variant_price_is_used_when_a_variant_is_passed():
    """When a variant with its own price is supplied, the tier discounts the
    variant price, not the parent product price."""
    product = ProductFactory(price=Decimal("40.00"))
    variant = ProductVariantFactory(product=product, price=Money(Decimal("55.00"), "USD"))
    tier = PlanPricingTierFactory(discount_percentage=Decimal("10.00"))

    price = tier.calculate_price(product, variant)

    # 55.00 * (1 - 0.10) — derived from the variant, not the 40.00 product price.
    assert price.amount == Decimal("49.50")


def test_quantity_multiplier_scales_the_discounted_price():
    """The manager wrapper multiplies the per-unit discounted price by quantity."""
    product = ProductFactory(price=Decimal("40.00"))
    tier = PlanPricingTierFactory(discount_percentage=Decimal("0.00"))

    price = SubscriptionManager.calculate_subscription_price(product, None, tier, quantity=3)

    assert price.amount == Decimal("120.00")


def test_calculated_price_preserves_the_product_currency():
    """The discounted price keeps the product's own currency, not a USD default."""
    product = ProductFactory(price=Decimal("40.00"), price_currency="EUR")
    tier = PlanPricingTierFactory(discount_percentage=Decimal("25.00"))

    price = tier.calculate_price(product)

    assert price.amount == Decimal("30.00")
    assert str(price.currency) == "EUR"


def test_full_discount_floors_at_zero_not_negative():
    """A 100% tier discount yields exactly zero and never a negative charge."""
    product = ProductFactory(price=Decimal("40.00"))
    tier = PlanPricingTierFactory(discount_percentage=Decimal("100.00"))

    price = tier.calculate_price(product)

    assert price.amount == Decimal("0.00")
    assert price.amount >= Decimal("0.00")


# ============================================================
# 2. create_subscription (negative + idempotency)
# ============================================================


def _create_args(user, account):
    """Build a valid create_subscription kwargs bundle for `user`/`account`."""
    plan = SubscriptionPlanFactory()
    tier = PlanPricingTierFactory(plan=plan)
    product = ProductFactory(price=Decimal("30.00"))
    token = PaymentTokenFactory(user=user, provider_account=account)
    return {
        "user": user,
        "plan": plan,
        "pricing_tier": tier,
        "payment_token": token,
        "product": product,
    }


def test_create_subscription_rejects_a_token_owned_by_another_user():
    """A payment token belonging to a different user is refused."""
    user = UserFactory()
    account = PaymentProviderAccountFactory(subscribable=True)
    args = _create_args(user, account)
    other_user = UserFactory()
    args["payment_token"] = PaymentTokenFactory(user=other_user, provider_account=account)

    with pytest.raises(ValueError, match="does not belong to this user"):
        SubscriptionManager(account).create_subscription(**args)


def test_create_subscription_rejects_a_token_for_a_different_provider_account():
    """A token minted against a different provider account is refused even when
    it belongs to the right user."""
    user = UserFactory()
    account = PaymentProviderAccountFactory(subscribable=True)
    other_account = PaymentProviderAccountFactory(subscribable=True)
    args = _create_args(user, account)
    args["payment_token"] = PaymentTokenFactory(user=user, provider_account=other_account)

    with pytest.raises(ValueError, match="different provider account"):
        SubscriptionManager(account).create_subscription(**args)


def test_create_subscription_rejects_an_inactive_token():
    """An inactive payment token cannot start a subscription."""
    user = UserFactory()
    account = PaymentProviderAccountFactory(subscribable=True)
    args = _create_args(user, account)
    args["payment_token"].is_active = False
    args["payment_token"].save(update_fields=["is_active"])

    with pytest.raises(ValueError, match="not active"):
        SubscriptionManager(account).create_subscription(**args)


def test_create_subscription_requires_a_product():
    """A missing product (SET_NULL / omitted) is rejected — it drives pricing."""
    user = UserFactory()
    account = PaymentProviderAccountFactory(subscribable=True)
    args = _create_args(user, account)
    args["product"] = None

    with pytest.raises(ValueError, match="Product is required"):
        SubscriptionManager(account).create_subscription(**args)


def test_create_subscription_is_idempotent_per_originating_order():
    """A second create for the same order + product + plan returns the EXISTING
    subscription rather than duplicating it (checkout-retry / dual-settlement)."""
    user = UserFactory()
    account = PaymentProviderAccountFactory(subscribable=True)
    args = _create_args(user, account)
    order = OrderFactory(user=user)
    manager = SubscriptionManager(account)

    first = manager.create_subscription(originating_order=order, **args)
    second = manager.create_subscription(originating_order=order, **args)

    assert first.pk == second.pk
    assert (
        CustomerSubscription.objects.filter(
            originating_order=order, product=args["product"], plan=args["plan"]
        ).count()
        == 1
    )


# ============================================================
# 3. reactivate_subscription (guards)
# ============================================================


def test_reactivate_refused_outside_the_reactivation_window():
    """A canceled subscription past its reactivation deadline cannot reactivate."""
    now = timezone.now()
    subscription = CustomerSubscriptionFactory(
        status="canceled",
        canceled_at=now - timedelta(days=10),
        reactivation_deadline=now - timedelta(days=1),
    )

    with pytest.raises(ValueError, match="cannot be reactivated"):
        _manager_for(subscription).reactivate_subscription(subscription)


def test_reactivate_refused_when_owner_token_is_inactive():
    """Inside the window, an inactive owner token still blocks reactivation."""
    now = timezone.now()
    subscription = CustomerSubscriptionFactory(
        status="canceled",
        canceled_at=now,
        reactivation_deadline=now + timedelta(days=7),
        payment_token__is_active=False,
    )

    with pytest.raises(ValueError, match="not active"):
        _manager_for(subscription).reactivate_subscription(subscription)


def test_reactivate_refused_when_owner_token_is_expired():
    """Inside the window, an expired card token is refused with a re-add prompt."""
    now = timezone.now()
    subscription = CustomerSubscriptionFactory(
        status="canceled",
        canceled_at=now,
        reactivation_deadline=now + timedelta(days=7),
        payment_token__card_exp_month=1,
        payment_token__card_exp_year=2020,
    )

    with pytest.raises(ValueError, match="expired"):
        _manager_for(subscription).reactivate_subscription(subscription)


def test_reactivate_refused_for_a_non_canceled_subscription():
    """An active subscription (never canceled) cannot be reactivated."""
    now = timezone.now()
    subscription = CustomerSubscriptionFactory(
        status="active",
        reactivation_deadline=now + timedelta(days=7),
    )

    with pytest.raises(ValueError, match="cannot be reactivated"):
        _manager_for(subscription).reactivate_subscription(subscription)


# ============================================================
# 4. retry_failed_billing (retry_billing_cycle task)
# ============================================================


def _failed_subscription(*, declining=False, grace_period_days=0):
    """A past_due subscription with the given provider + plan grace window."""
    user = UserFactory()
    account = PaymentProviderAccountFactory(declining=declining, subscribable=not declining)
    token = PaymentTokenFactory(user=user, provider_account=account)
    return CustomerSubscriptionFactory(
        user=user,
        payment_token=token,
        status="past_due",
        billing_cycle_count=0,
        plan__grace_period_days=grace_period_days,
    )


def test_retry_success_clears_the_failure_and_reactivates():
    """A retry that charges successfully marks the log successful, advances the
    cycle count, and restores the subscription to active.

    Regression: the retry task previously assigned the raw provider charge_result
    (carrying a Decimal 'amount') straight into the provider_response JSONField
    without the json.dumps(default=str) sanitisation the main engine uses, so the
    save raised TypeError, the outer except swallowed it, and a recovered payment
    was silently never recorded. The task now sanitises via tasks._json_safe."""
    subscription = _failed_subscription()
    log = BillingCycleLogFactory(
        subscription=subscription, cycle_number=1, failed=True, retry_count=0, max_retries=3
    )

    result = retry_billing_cycle(log.id)

    assert result["status"] == "successful"
    log.refresh_from_db()
    subscription.refresh_from_db()
    assert log.status == "successful"
    assert log.retry_count == 1
    assert subscription.status == "active"
    assert subscription.billing_cycle_count == 1
    assert subscription.last_billing_status == "successful"


def test_retry_still_failing_schedules_backoff_and_counts_the_attempt():
    """A retry that still declines but is under the ceiling increments the count,
    stamps next_retry_date, and reschedules with exponential backoff."""
    subscription = _failed_subscription(declining=True)
    log = BillingCycleLogFactory(
        subscription=subscription, cycle_number=1, failed=True, retry_count=0, max_retries=3
    )

    with patch.object(retry_billing_cycle, "apply_async") as mock_async:
        result = retry_billing_cycle(log.id)

    log.refresh_from_db()
    assert result["status"] == "failed"
    assert result["will_retry"] is True
    assert log.retry_count == 1
    assert log.status == "failed"
    assert log.next_retry_date is not None
    # retry_hours = 2 ** retry_count (=1) → 2h → countdown 7200s.
    mock_async.assert_called_once()
    assert mock_async.call_args.kwargs["countdown"] == 2 * 3600


def test_retry_exhausted_enters_grace_period_when_plan_allows():
    """Once retries are exhausted, a plan with a grace window keeps access: the
    subscription stays past_due and gets a grace_period_end_date."""
    subscription = _failed_subscription(declining=True, grace_period_days=5)
    log = BillingCycleLogFactory(
        subscription=subscription, cycle_number=1, failed=True, retry_count=2, max_retries=3
    )

    with patch.object(retry_billing_cycle, "apply_async") as mock_async:
        result = retry_billing_cycle(log.id)

    log.refresh_from_db()
    subscription.refresh_from_db()
    assert result["status"] == "failed"
    assert log.retry_count == 3
    assert log.can_retry() is False
    # No further retry is scheduled once the ceiling is reached.
    mock_async.assert_not_called()
    assert subscription.status == "past_due"
    assert subscription.grace_period_end_date is not None


def test_retry_exhausted_auto_cancels_when_no_grace_period():
    """With grace_period_days=0, an exhausted retry auto-cancels the subscription."""
    subscription = _failed_subscription(declining=True, grace_period_days=0)
    log = BillingCycleLogFactory(
        subscription=subscription, cycle_number=1, failed=True, retry_count=2, max_retries=3
    )

    with patch.object(retry_billing_cycle, "apply_async") as mock_async:
        retry_billing_cycle(log.id)

    subscription.refresh_from_db()
    mock_async.assert_not_called()
    assert subscription.status == "canceled"
    assert subscription.canceled_at is not None
    assert "Payment failed after" in subscription.cancellation_reason
    assert subscription.grace_period_end_date is None


def test_retry_is_a_no_op_when_the_log_is_not_eligible():
    """A log that cannot be retried (retries already exhausted) is left untouched."""
    subscription = _failed_subscription(declining=True)
    log = BillingCycleLogFactory(
        subscription=subscription, cycle_number=1, failed=True, retry_count=3, max_retries=3
    )

    result = retry_billing_cycle(log.id)

    log.refresh_from_db()
    assert result == {"status": "not_eligible"}
    assert log.retry_count == 3
    assert log.status == "failed"
