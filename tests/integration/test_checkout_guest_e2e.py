"""End-to-end GUEST checkout through the real API endpoints.

Codex's #1 coverage gap: nothing exercised the whole guest sequence together —
contact -> billing -> tender -> complete -> confirmation — proving that email,
name, the full billing address, guest-user order creation, and guest
confirmation access all actually work as one flow. This drives the real
endpoints as an anonymous browser (digital cart, zero-due via a gift card, so
no gateway is needed).
"""

from decimal import Decimal

import pytest
from djmoney.money import Money
from rest_framework.test import APIClient

from catalog.models import GiftCard
from orders.models import Order
from tests.factories import ProductFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


def test_guest_digital_checkout_completes_and_persists(digital_product, site_settings, warehouse):
    # A gift card that covers the whole (small) digital total → zero due.
    gc_product = ProductFactory(product_type="gift_card", status="published")
    card = GiftCard.objects.create(
        product=gc_product,
        initial_value=Money(Decimal("100.00"), "USD"),
        recipient_email="r@test.spwig.com",
        is_active=True,
    )

    client = APIClient()  # anonymous — persists the session cookie across calls

    # 1. Add the digital item to the guest's session cart.
    r = client.post(
        "/api/cart/add/", {"product_id": digital_product.id, "quantity": 1}, format="json"
    )
    assert r.status_code in (200, 201), r.content

    # 2. Contact — persists email/name to the session (the ONLY place a
    #    no-shipping guest's email is recorded before payment).
    r = client.post(
        "/api/checkout/contact/",
        {"email": "guest@example.com", "first_name": "Gwen", "last_name": "Guest"},
        format="json",
    )
    assert r.status_code == 200, r.content

    # 3. Full billing address (digital carts collect a complete one).
    r = client.post(
        "/api/checkout/billing-address/",
        {
            "same_as_shipping": False,
            "name": "Gwen Guest",
            "address1": "9 Guest Rd",
            "city": "Portland",
            "state": "OR",
            "postal_code": "97201",
            "country": "US",
            "email": "guest@example.com",
        },
        format="json",
    )
    assert r.status_code == 200, r.content

    # 4. Cover the total with the gift card → amount due becomes zero.
    r = client.post("/api/checkout/tenders/gift-card/", {"code": card.code}, format="json")
    assert r.status_code == 200, r.content

    # 5. Complete — zero-due path (no gateway). Creates the order + guest user.
    r = client.post("/api/checkout/complete/", {}, format="json")
    assert r.status_code == 201, r.content
    order_number = r.json()["order"]["order_number"]

    # 6. Everything the flow was supposed to persist is actually on the order.
    order = Order.objects.get(order_number=order_number)
    assert order.email == "guest@example.com"
    assert order.billing_name == "Gwen Guest"
    assert order.billing_address1 == "9 Guest Rd"
    assert order.billing_city == "Portland"
    assert order.billing_country == "US"
    assert order.user is not None and order.user.username.startswith("guest_"), (
        "a guest User should have been materialised for the order"
    )

    # 7. The same (guest) browser can view its confirmation…
    r = client.get(f"/en/checkout/confirmation/{order_number}/")
    assert r.status_code == 200

    # 8. …but a different anonymous browser (no allow-list entry) cannot.
    other = APIClient()
    assert other.get(f"/en/checkout/confirmation/{order_number}/").status_code == 404
