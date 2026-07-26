"""
Checkout contact/address completeness — API tests.

Server-side requirements introduced with the checkout completeness work:

- Shipping addresses require a phone number (carriers need a delivery
  contact) with a lenient, international-friendly format check.
- Saved addresses without a phone are rejected unless a supplemental
  phone rides along with address_id (which also completes the record).
- The billing endpoint accepts a bare contact name alongside
  same_as_shipping so digital-only guest checkouts are never nameless
  (stored in session metadata as contact_name).
"""

import pytest

from tests.factories import AddressFactory, CartFactory, CartItemFactory, ProductFactory

pytestmark = [pytest.mark.django_db, pytest.mark.checkout, pytest.mark.integration]

SHIPPING_URL = "/api/checkout/shipping-address/"
BILLING_URL = "/api/checkout/billing-address/"

VALID_ADDRESS = {
    "name": "Recipient Name",
    "address1": "456 Broadway",
    "city": "New York",
    "state": "NY",
    "postal_code": "10013",
    "country": "US",
}


class TestShippingPhoneRequired:
    def test_inline_address_without_phone_rejected(self, auth_client, cart_with_item):
        resp = auth_client.post(SHIPPING_URL, {**VALID_ADDRESS})
        assert resp.status_code == 400
        body = resp.json()
        flat = str(body).lower()
        assert "phone" in flat

    def test_inline_address_blank_phone_rejected(self, auth_client, cart_with_item):
        resp = auth_client.post(SHIPPING_URL, {**VALID_ADDRESS, "phone": "   "})
        assert resp.status_code == 400

    @pytest.mark.parametrize("bad", ["call me", "123", "+", "12 34", "555-CALL"])
    def test_implausible_phone_rejected(self, auth_client, cart_with_item, bad):
        resp = auth_client.post(SHIPPING_URL, {**VALID_ADDRESS, "phone": bad})
        assert resp.status_code == 400, bad

    @pytest.mark.parametrize(
        "good",
        ["+65 9123 4567", "020 7946 0958", "(212) 555-0100", "0412.345.678"],
    )
    def test_international_formats_accepted(self, auth_client, cart_with_item, good):
        resp = auth_client.post(SHIPPING_URL, {**VALID_ADDRESS, "phone": good})
        assert resp.status_code == 200, resp.content
        session = resp.json()["session"]
        assert session["shipping_address_data"]["phone"] == good

    def test_recipient_name_still_required(self, auth_client, cart_with_item):
        payload = {**VALID_ADDRESS, "phone": "+1 212 555 0100"}
        payload.pop("name")
        resp = auth_client.post(SHIPPING_URL, payload)
        assert resp.status_code == 400


class TestSavedAddressPhone:
    def test_saved_address_with_phone_accepted(self, auth_client, cart_with_item, customer_user):
        addr = AddressFactory(user=customer_user)  # factory sets a phone
        resp = auth_client.post(SHIPPING_URL, {"address_id": addr.id})
        assert resp.status_code == 200, resp.content
        assert resp.json()["session"]["shipping_address"]["id"] == addr.id

    def test_saved_address_without_phone_rejected(self, auth_client, cart_with_item, customer_user):
        addr = AddressFactory(user=customer_user, phone="")
        resp = auth_client.post(SHIPPING_URL, {"address_id": addr.id})
        assert resp.status_code == 400
        body = resp.json()
        assert body["success"] is False
        assert "phone" in body["message"].lower()

    def test_supplemental_phone_completes_saved_address(
        self, auth_client, cart_with_item, customer_user
    ):
        addr = AddressFactory(user=customer_user, phone="")
        resp = auth_client.post(SHIPPING_URL, {"address_id": addr.id, "phone": "+44 20 7946 0958"})
        assert resp.status_code == 200, resp.content
        addr.refresh_from_db()
        assert addr.phone == "+44 20 7946 0958"
        assert resp.json()["session"]["shipping_address"]["id"] == addr.id


class TestBillingCompleteness:
    def _set_shipping(self, client):
        resp = client.post(SHIPPING_URL, {**VALID_ADDRESS, "phone": "+1 212 555 0100"})
        assert resp.status_code == 200, resp.content

    def test_billing_requires_name_when_not_same_as_shipping(self, auth_client, cart_with_item):
        self._set_shipping(auth_client)
        payload = {
            "same_as_shipping": False,
            "address1": "1 Billing Way",
            "city": "Boston",
            "state": "MA",
            "postal_code": "02110",
            "country": "US",
        }
        resp = auth_client.post(BILLING_URL, payload)
        assert resp.status_code == 400
        assert "name" in str(resp.json()).lower()

    def test_billing_full_address_accepted(self, auth_client, cart_with_item):
        self._set_shipping(auth_client)
        payload = {
            "same_as_shipping": False,
            "name": "Bill Payer",
            "address1": "1 Billing Way",
            "city": "Boston",
            "state": "MA",
            "postal_code": "02110",
            "country": "US",
            "phone": "+1 617 555 0100",
        }
        resp = auth_client.post(BILLING_URL, payload)
        assert resp.status_code == 200, resp.content
        assert resp.json()["session"]["billing_address_data"]["name"] == "Bill Payer"

    def test_billing_implausible_phone_rejected(self, auth_client, cart_with_item):
        self._set_shipping(auth_client)
        payload = {
            "same_as_shipping": False,
            "name": "Bill Payer",
            "address1": "1 Billing Way",
            "city": "Boston",
            "state": "MA",
            "postal_code": "02110",
            "country": "US",
            "phone": "not-a-phone",
        }
        resp = auth_client.post(BILLING_URL, payload)
        assert resp.status_code == 400


class TestDigitalOnlyContactName:
    """Digital-only carts never show the shipping form — the contact name
    rides with same_as_shipping billing and lands in session metadata so
    orders and payment providers get a customer name."""

    @pytest.fixture
    def digital_cart(self, customer_user, site_settings):
        product = ProductFactory(digital=True, name="Test Ebook")
        cart = CartFactory(user=customer_user)
        CartItemFactory(cart=cart, product=product, quantity=1)
        return cart

    def test_contact_name_stored_in_session_metadata(self, auth_client, digital_cart):
        resp = auth_client.post(BILLING_URL, {"same_as_shipping": True, "name": "Digital Buyer"})
        assert resp.status_code == 200, resp.content
        session = resp.json()["session"]
        assert session["metadata"].get("contact_name") == "Digital Buyer"

    def test_same_as_shipping_without_name_still_accepted(self, auth_client, digital_cart):
        # Backwards compatible: the name is optional at the API level
        # (physical flows inherit the shipping name instead)
        resp = auth_client.post(BILLING_URL, {"same_as_shipping": True})
        assert resp.status_code == 200, resp.content
