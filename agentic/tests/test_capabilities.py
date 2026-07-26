"""
Capabilities are derived from live install state, never hardcoded on.

The rule under test: the profile advertises catalog + cart unconditionally,
checkout/order only with a working payment provider, and fulfillment only when
shipping can quote programmatically. Advertising more than the store can do is
the failure mode this guards against.
"""

import pytest

from agentic.services.capability_service import compute_capabilities
from tests.factories import (
    PaymentProviderAccountFactory,
    ShippingMethodFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration]

CATALOG_SEARCH = "dev.ucp.shopping.catalog.search"
CATALOG_LOOKUP = "dev.ucp.shopping.catalog.lookup"
CART = "dev.ucp.shopping.cart"
CHECKOUT = "dev.ucp.shopping.checkout"
ORDER = "dev.ucp.shopping.order"
FULFILLMENT = "dev.ucp.shopping.fulfillment"
AP2 = "dev.ucp.shopping.ap2_mandate"


class TestBaselineCapabilities:
    def test_bare_store_advertises_only_catalog_and_cart(self):
        caps = compute_capabilities()
        assert set(caps) == {CATALOG_SEARCH, CATALOG_LOOKUP, CART}

    def test_no_checkout_without_a_payment_provider(self):
        caps = compute_capabilities()
        assert CHECKOUT not in caps
        assert ORDER not in caps

    def test_no_fulfillment_without_shipping(self):
        assert FULFILLMENT not in compute_capabilities()

    def test_ap2_absent_until_a_signing_key_exists(self):
        assert AP2 not in compute_capabilities()


class TestCheckoutCapability:
    def test_active_connected_provider_enables_checkout_and_order(self):
        PaymentProviderAccountFactory(is_active=True, connection_status="connected")
        caps = compute_capabilities()
        assert CHECKOUT in caps
        assert ORDER in caps

    def test_inactive_provider_does_not_enable_checkout(self):
        PaymentProviderAccountFactory(is_active=False, connection_status="connected")
        assert CHECKOUT not in compute_capabilities()

    def test_disconnected_provider_does_not_enable_checkout(self):
        PaymentProviderAccountFactory(is_active=True, connection_status="error")
        assert CHECKOUT not in compute_capabilities()


class TestFulfillmentCapability:
    def test_flat_rate_method_enables_fulfillment(self):
        ShippingMethodFactory(method_type="flat_rate", is_active=True)
        assert FULFILLMENT in compute_capabilities()

    def test_pickup_only_does_not_enable_fulfillment(self):
        # A pickup-only store cannot quote delivery to an agent's address.
        ShippingMethodFactory(method_type="local_pickup", is_active=True)
        assert FULFILLMENT not in compute_capabilities()

    def test_inactive_method_does_not_enable_fulfillment(self):
        ShippingMethodFactory(method_type="flat_rate", is_active=False)
        assert FULFILLMENT not in compute_capabilities()


class TestFullyConfiguredStore:
    def test_advertises_the_full_set(self):
        PaymentProviderAccountFactory(is_active=True, connection_status="connected")
        ShippingMethodFactory(method_type="table_rate", is_active=True)
        caps = set(compute_capabilities())
        assert caps == {
            CATALOG_SEARCH,
            CATALOG_LOOKUP,
            CART,
            CHECKOUT,
            ORDER,
            FULFILLMENT,
        }

    def test_capabilities_order_is_stable(self):
        PaymentProviderAccountFactory(is_active=True, connection_status="connected")
        assert compute_capabilities() == compute_capabilities()
