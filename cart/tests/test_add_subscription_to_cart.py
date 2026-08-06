"""
Adding a subscription line to the cart.

Covers two surfaces:

* ``AddToCartSerializer.validate`` — the auth requirement, the product-type
  gate, and the (new) optionality of ``payment_token_id`` at add-to-cart time.
* ``CartService.add_item`` — the first-cycle tier discount baked into the stored
  ``unit_price``, and the rule that a subscription line never merges with a
  one-time line for the same product.
"""

from decimal import Decimal

import pytest
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIRequestFactory

from cart.serializers import AddToCartSerializer
from cart.services import CartService
from tests.factories import (
    CartFactory,
    PlanPricingTierFactory,
    ProductFactory,
    SubscriptionPlanFactory,
    UserFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


def _serializer_for(user, payload):
    """Build an AddToCartSerializer with a request context carrying ``user``."""
    request = APIRequestFactory().post("/api/cart/add/")
    request.user = user
    return AddToCartSerializer(data=payload, context={"request": request})


# ---------------------------------------------------------------------------
# AddToCartSerializer.validate
# ---------------------------------------------------------------------------


def test_subscription_can_be_added_without_a_prior_payment_token():
    """payment_token_id is optional at add-to-cart; the card is bound later."""
    user = UserFactory()
    plan = SubscriptionPlanFactory()
    tier = PlanPricingTierFactory(plan=plan, is_default=True)
    product = ProductFactory(is_subscription_enabled=True, subscription_plans=[plan])

    serializer = _serializer_for(
        user,
        {
            "product_id": product.id,
            "quantity": 1,
            "is_subscription": True,
            "subscription_plan_id": str(plan.plan_id),
        },
    )

    assert serializer.is_valid(), serializer.errors
    # No token supplied and none required — validation resolves plan + tier only.
    assert serializer.validated_data.get("payment_token") is None
    assert serializer.validated_data["subscription_plan"] == plan
    assert serializer.validated_data["pricing_tier"] == tier


def test_anonymous_request_cannot_add_a_subscription():
    """A subscription is owned by a user account, so guests are rejected."""
    plan = SubscriptionPlanFactory()
    PlanPricingTierFactory(plan=plan, is_default=True)
    product = ProductFactory(is_subscription_enabled=True, subscription_plans=[plan])

    serializer = _serializer_for(
        AnonymousUser(),
        {
            "product_id": product.id,
            "quantity": 1,
            "is_subscription": True,
            "subscription_plan_id": str(plan.plan_id),
        },
    )

    assert not serializer.is_valid()
    assert "is_subscription" in serializer.errors


def test_subscription_rejected_on_gated_product_type():
    """A gated product type (gift_card) cannot be sold as a subscription."""
    user = UserFactory()
    plan = SubscriptionPlanFactory()
    PlanPricingTierFactory(plan=plan, is_default=True)
    # is_subscription_enabled=True on a gift_card can never be saved through the
    # admin (Product.clean forbids it), but a stale/headless client could still
    # POST it — the serializer is defence in depth over the model gate.
    product = ProductFactory(
        product_type="gift_card",
        is_subscription_enabled=True,
        subscription_plans=[plan],
    )

    serializer = _serializer_for(
        user,
        {
            "product_id": product.id,
            "quantity": 1,
            "is_subscription": True,
            "subscription_plan_id": str(plan.plan_id),
        },
    )

    assert not serializer.is_valid()
    assert "is_subscription" in serializer.errors


# ---------------------------------------------------------------------------
# CartService.add_item
# ---------------------------------------------------------------------------


def test_subscription_line_unit_price_carries_the_tier_discount():
    """The stored unit_price is effective price × (1 − discount%)."""
    user = UserFactory()
    cart = CartFactory(user=user)
    plan = SubscriptionPlanFactory()
    tier = PlanPricingTierFactory(plan=plan, discount_percentage=Decimal("20.00"))
    product = ProductFactory(price=Decimal("25.00"), is_subscription_enabled=True)

    success, _message, item = CartService.add_item(
        cart=cart,
        product_id=product.id,
        quantity=1,
        is_subscription=True,
        subscription_plan=plan,
        pricing_tier=tier,
        payment_token=None,
    )

    assert success is True
    assert item is not None
    assert item.is_subscription is True
    assert item.subscription_plan == plan
    assert item.pricing_tier == tier
    # 25.00 × (1 − 0.20) = 20.00
    assert item.unit_price.amount == Decimal("20.00")


def test_subscription_line_does_not_merge_with_a_one_time_line():
    """Same product added one-time then as a subscription yields two lines."""
    user = UserFactory()
    cart = CartFactory(user=user)
    plan = SubscriptionPlanFactory()
    tier = PlanPricingTierFactory(plan=plan)
    product = ProductFactory(price=Decimal("25.00"), is_subscription_enabled=True)

    ok_one_time, _m1, one_time_item = CartService.add_item(
        cart=cart, product_id=product.id, quantity=1
    )
    ok_sub, _m2, sub_item = CartService.add_item(
        cart=cart,
        product_id=product.id,
        quantity=1,
        is_subscription=True,
        subscription_plan=plan,
        pricing_tier=tier,
        payment_token=None,
    )

    assert ok_one_time is True
    assert ok_sub is True
    assert one_time_item.id != sub_item.id

    parents = cart.items.filter(parent_bundle__isnull=True)
    assert parents.count() == 2
    assert one_time_item.is_subscription is False
    assert sub_item.is_subscription is True
