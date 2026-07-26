"""Checkout view template-selection tests.

Express is a returning-customer flow: it rides a saved default address straight
to payment. When there's no saved address to ride, the view resolves to the
fallback template server-side (rather than letting the client load the
express shell and redirect), so guests and address-less customers land on a
usable template first.
"""

import pytest

from tests.factories import AddressFactory, CartFactory, CartItemFactory

pytestmark = [pytest.mark.django_db, pytest.mark.checkout, pytest.mark.integration]


def _template_names(response):
    return {t.name for t in response.templates if t.name}


class TestExpressFallbackRouting:
    def test_express_falls_back_when_no_saved_address(self, customer_client, cart_with_item):
        """Shipping cart, no saved address → fallback (accordion), not express.

        A logged-in customer with no saved address exercises the same
        `not saved_addresses` branch a guest hits (guests always have none).
        """
        resp = customer_client.get("/en/checkout/?template=express")
        assert resp.status_code == 200
        names = _template_names(resp)
        assert "page_builder/checkout/express.html" not in names
        assert "page_builder/checkout/accordion.html" in names

    def test_express_renders_with_saved_address(
        self, customer_client, customer_user, cart_with_item
    ):
        """With a saved address to default from, express is served as asked."""
        AddressFactory(user=customer_user)
        resp = customer_client.get("/en/checkout/?template=express")
        assert resp.status_code == 200
        assert "page_builder/checkout/express.html" in _template_names(resp)

    def test_express_kept_for_no_shipping_cart(
        self, customer_client, customer_user, digital_product, site_settings
    ):
        """No-shipping carts have no address to default from; express handles
        them for anyone, so there's no fallback even without a saved address."""
        cart = CartFactory(user=customer_user)
        CartItemFactory(cart=cart, product=digital_product)
        resp = customer_client.get("/en/checkout/?template=express")
        assert resp.status_code == 200
        assert "page_builder/checkout/express.html" in _template_names(resp)

    def test_no_shipping_renders_full_billing_prefilled(
        self, customer_client, customer_user, digital_product, site_settings
    ):
        """Digital (no-shipping) checkout renders a FULL billing form, not the
        old country+postal minimal one, pre-filled from the default address."""
        AddressFactory(
            user=customer_user,
            is_default=True,
            address1="42 Galaxy Way",
            city="Portland",
        )
        cart = CartFactory(user=customer_user)
        CartItemFactory(cart=cart, product=digital_product)
        resp = customer_client.get("/en/checkout/?template=express")
        assert resp.status_code == 200
        html = resp.content.decode()
        # Full billing fields are present (not just country/postal)
        assert 'id="billing-address1"' in html
        assert 'id="billing-city"' in html
        assert 'id="billing-name"' in html
        # Pre-filled from the customer's default saved address
        assert "42 Galaxy Way" in html
        # The old minimal-billing block is gone
        assert 'id="billing-minimal"' not in html


class TestBillingCountryList:
    """Digital (no-shipping) carts offer the FULL ISO country list for billing,
    not just the countries the merchant ships to — restricting billing to
    ShippingCountry locks out valid customers abroad and hides the payment
    methods available in their country."""

    def _us_only_shipping(self):
        from django.contrib.sites.models import Site

        from shipping.models import ShippingCountry

        # --reuse-db can leak ShippingCountry rows between runs; pin the set.
        ShippingCountry.objects.update(is_active=False)
        site = Site.objects.get(pk=1)
        ShippingCountry.objects.update_or_create(
            site=site, country_code="US", defaults={"is_active": True, "priority": 0}
        )

    def test_billing_countries_is_full_list_not_shipping_countries(
        self, customer_client, customer_user, digital_product, site_settings
    ):
        self._us_only_shipping()
        AddressFactory(user=customer_user, is_default=True, country="US")
        cart = CartFactory(user=customer_user)
        CartItemFactory(cart=cart, product=digital_product)

        resp = customer_client.get("/en/checkout/?template=express")
        assert resp.status_code == 200

        billing = resp.context["billing_countries"]
        shipping = resp.context["shipping_countries"]
        billing_codes = {code for code, _ in billing}
        shipping_codes = {code for code, _ in shipping}

        # Full ISO list (~250 entries) — the whole point of the fix.
        assert len(billing) > 200
        # Countries the merchant does NOT ship to are still billing-selectable.
        assert "JP" in billing_codes
        assert "FR" in billing_codes
        assert "JP" not in shipping_codes, (
            "JP leaked into shipping countries; the US-only pin failed."
        )
        assert shipping_codes == {"US"}
