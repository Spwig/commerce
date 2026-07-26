"""Billing + email persistence on the billing-address step.

`persistBilling()` in checkout.js now records billing AND email on both the
create-payment-intent path and the zero-due `placeOrderFree` path, so a fully
tendered (zero-due) order still lands with the customer's email and billing.

Server side, `CheckoutService.set_billing_address` gained an `email` argument
and `SetBillingAddressSerializer` gained an `email` field. Before this, a
zero-due order created via `placeOrderFree` had no email recorded (the shipping
step, which normally captures it, is skipped for digital / fully-tendered
carts) — guest order creation reads `metadata['email']` and would have found
nothing.
"""

import pytest

from cart.services.checkout_service import CheckoutService
from tests.factories import CartFactory, CartItemFactory

pytestmark = [pytest.mark.django_db, pytest.mark.checkout, pytest.mark.integration]

BILLING_URL = "/api/checkout/billing-address/"


@pytest.fixture
def digital_cart(customer_user, digital_product, site_settings):
    cart = CartFactory(user=customer_user)
    CartItemFactory(cart=cart, product=digital_product, quantity=1)
    return cart


class TestBillingEmailPersistenceService:
    def test_set_billing_address_persists_email(self, digital_cart):
        session = CheckoutService.get_or_create_session(digital_cart)
        ok, msg = CheckoutService.set_billing_address(
            session,
            same_as_shipping=True,
            contact_name="Zoe Zero",
            email="zoe@example.com",
        )
        assert ok, msg
        session.refresh_from_db()
        assert session.metadata.get("email") == "zoe@example.com"
        assert session.metadata.get("contact_name") == "Zoe Zero"

    def test_blank_email_does_not_overwrite_existing(self, digital_cart):
        """A later same_as_shipping call without email must not wipe a
        previously-persisted email (the shipping step may have set it)."""
        session = CheckoutService.get_or_create_session(digital_cart)
        session.metadata = {"email": "earlier@example.com"}
        session.save(update_fields=["metadata"])

        ok, _ = CheckoutService.set_billing_address(session, same_as_shipping=True, email="")
        assert ok
        session.refresh_from_db()
        assert session.metadata.get("email") == "earlier@example.com"


class TestBillingEmailPersistenceApi:
    def test_billing_api_persists_email_into_metadata(self, auth_client, digital_cart):
        resp = auth_client.post(
            BILLING_URL,
            {"same_as_shipping": True, "name": "Zoe Zero", "email": "zoe@example.com"},
            format="json",
        )
        assert resp.status_code == 200, resp.content
        session = resp.json()["session"]
        assert session["metadata"].get("email") == "zoe@example.com"

    def test_physical_zero_due_billing_same_as_shipping_persists_email(
        self, auth_client, cart_with_item
    ):
        """The zero-due path can be a physical cart fully covered by a gift card
        / voucher; `placeOrderFree` still calls persistBilling with the email."""
        # Full billing supplied (physical carts require it), plus email.
        resp = auth_client.post(
            BILLING_URL,
            {
                "same_as_shipping": False,
                "name": "Percy Physical",
                "address1": "1 Billing Way",
                "city": "Boston",
                "state": "MA",
                "postal_code": "02110",
                "country": "US",
                "phone": "+1 617 555 0100",
                "email": "percy@example.com",
            },
            format="json",
        )
        assert resp.status_code == 200, resp.content
        session = resp.json()["session"]
        assert session["metadata"].get("email") == "percy@example.com"
