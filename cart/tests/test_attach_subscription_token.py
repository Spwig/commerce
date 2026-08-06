"""
CartViewSet.attach_subscription_token behaviour.

The storefront defers card capture to the checkout payment step: it mints a
reusable PaymentToken and binds it to each subscription cart line via
``POST /api/cart/items/<id>/attach-subscription-token/``.

NOTE ON ROUTING: this ``@action`` is currently NOT wired by a ``path()`` in
``cart/urls.py`` (CartViewSet is not router-registered, so an ``@action``
decorator alone routes nothing — see the module docstring of
``tests/integration/test_cart_action_routing.py``, which already fails for it).
These tests therefore exercise the action *handler directly* via
``APIRequestFactory`` so the implemented behaviour is verified independently of
the routing gap.
"""

import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from cart.views import CartViewSet
from tests.factories import (
    CartFactory,
    CartItemFactory,
    ComponentRegistryFactory,
    PaymentProviderAccountFactory,
    PaymentTokenFactory,
    PlanPricingTierFactory,
    ProductFactory,
    SubscriptionPlanFactory,
    UserFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration]

_view = CartViewSet.as_view({"post": "attach_subscription_token"})


def _call_attach(user, item_id, data):
    """Invoke the attach action directly with an optional authenticated user."""
    request = APIRequestFactory().post("/", data, format="json")
    if user is not None:
        force_authenticate(request, user=user)
    return _view(request, item_id=str(item_id))


def _subscription_item(user):
    """A subscription cart line on ``user``'s account cart."""
    cart = CartFactory(user=user)
    plan = SubscriptionPlanFactory()
    tier = PlanPricingTierFactory(plan=plan)
    product = ProductFactory(is_subscription_enabled=True)
    return CartItemFactory(
        cart=cart,
        product=product,
        is_subscription=True,
        subscription_plan=plan,
        pricing_tier=tier,
    )


def test_valid_owned_token_is_attached_to_the_subscription_line():
    user = UserFactory()
    item = _subscription_item(user)
    token = PaymentTokenFactory(user=user)  # default provider account is subscribable

    response = _call_attach(user, item.id, {"payment_token_id": str(token.token_id)})

    assert response.status_code == 200
    assert response.data["success"] is True
    item.refresh_from_db()
    assert item.payment_token == token


def test_token_not_owned_by_the_user_is_rejected():
    user = UserFactory()
    other = UserFactory()
    item = _subscription_item(user)
    foreign_token = PaymentTokenFactory(user=other)

    response = _call_attach(user, item.id, {"payment_token_id": str(foreign_token.token_id)})

    assert response.status_code == 400
    assert response.data["success"] is False
    item.refresh_from_db()
    assert item.payment_token is None


def test_token_whose_provider_does_not_support_subscriptions_is_rejected():
    user = UserFactory()
    item = _subscription_item(user)
    # A provider account whose component slug is not a registered subscription
    # provider → is_subscription_supported() is False.
    unsupported_component = ComponentRegistryFactory(
        slug="unsupported-sub-provider",
        component_type="payment_provider",
        name="Unsupported Provider",
    )
    account = PaymentProviderAccountFactory(component=unsupported_component)
    token = PaymentTokenFactory(user=user, provider_account=account)

    response = _call_attach(user, item.id, {"payment_token_id": str(token.token_id)})

    assert response.status_code == 400
    assert response.data["success"] is False
    item.refresh_from_db()
    assert item.payment_token is None


def test_attaching_to_a_non_subscription_item_is_rejected():
    user = UserFactory()
    cart = CartFactory(user=user)
    non_sub_item = CartItemFactory(cart=cart)  # is_subscription defaults False
    token = PaymentTokenFactory(user=user)

    response = _call_attach(user, non_sub_item.id, {"payment_token_id": str(token.token_id)})

    assert response.status_code == 400
    assert response.data["success"] is False


def test_anonymous_request_is_rejected():
    user = UserFactory()
    item = _subscription_item(user)
    token = PaymentTokenFactory(user=user)

    response = _call_attach(None, item.id, {"payment_token_id": str(token.token_id)})

    assert response.status_code == 401


def test_missing_payment_token_id_is_rejected():
    user = UserFactory()
    item = _subscription_item(user)

    response = _call_attach(user, item.id, {})

    assert response.status_code == 400
    assert response.data["success"] is False
