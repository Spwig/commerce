"""
Product.clean() subscription gating (catalog).

``Product.clean`` refuses ``is_subscription_enabled=True`` on any product type
outside ``SUBSCRIBABLE_PRODUCT_TYPES`` (simple / variable / digital). A
subscription re-charges every cycle and re-fulfils through a renewal Order; for
types we cannot re-fulfil that would take the customer's money and deliver
nothing after cycle 1.

These are pure model-validation tests: they build (never save) a Product and
call ``clean()`` directly, so the assertions are isolated from unrelated
required-field validation that ``full_clean`` would add.
"""

import pytest
from django.core.exceptions import ValidationError

from catalog.models import SUBSCRIBABLE_PRODUCT_TYPES
from tests.factories import ProductFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


# Types whose recurring fulfilment cannot be honoured — the gate must reject them.
GATED_PRODUCT_TYPES = ["gift_card", "booking", "bundle", "customizable", "configurable"]
# Types that may be sold as a subscription — the gate must allow them.
SUBSCRIBABLE_TYPES = sorted(SUBSCRIBABLE_PRODUCT_TYPES)  # simple, variable, digital


@pytest.mark.parametrize("product_type", GATED_PRODUCT_TYPES)
def test_subscription_enabled_is_rejected_for_gated_product_type(product_type):
    """clean() raises on is_subscription_enabled=True for a non-subscribable type."""
    product = ProductFactory.build(product_type=product_type, is_subscription_enabled=True)

    with pytest.raises(ValidationError) as excinfo:
        product.clean()

    # The error is attributed to the offending field, not a generic error.
    assert "is_subscription_enabled" in excinfo.value.message_dict


@pytest.mark.parametrize("product_type", SUBSCRIBABLE_TYPES)
def test_subscription_enabled_is_allowed_for_subscribable_product_type(product_type):
    """clean() does NOT raise for simple / variable / digital products."""
    product = ProductFactory.build(product_type=product_type, is_subscription_enabled=True)

    # Should not raise for the subscription gate. (Other clean() checks are
    # satisfied by the factory defaults: price > 0, no HS code, etc.)
    product.clean()


@pytest.mark.parametrize("product_type", GATED_PRODUCT_TYPES)
def test_gate_is_inert_when_subscription_disabled(product_type):
    """A gated product type is fine as long as subscriptions are not enabled."""
    product = ProductFactory.build(product_type=product_type, is_subscription_enabled=False)

    # is_subscription_enabled is False, so the subscription gate never fires.
    product.clean()
