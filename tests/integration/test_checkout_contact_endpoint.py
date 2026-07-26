"""Checkout contact endpoint (`POST /api/checkout/contact/`).

The contact step was reworked so the client persists the shopper's email
server-side and, when a password is supplied, an account is created and the
browser is logged in. ``checkout.js`` posts to ``/api/checkout/contact/``
(``endpoints.contact``), which maps to ``CheckoutViewSet.contact``.

Two things are exercised here:

1. That the URL is actually routed. ``CheckoutViewSet`` is NOT
   router-registered — every action is wired by hand in ``cart/urls.py`` — so
   an ``@action`` decorator alone routes nothing. At the time of writing the
   ``contact`` action has no path entry, so the endpoint the frontend calls
   404s. ``test_contact_url_is_routed`` documents that gap (xfail, strict).

2. That the logic behind the action is sound once wired: the underlying
   ``CheckoutService.ensure_checkout_user`` creates a real account when a
   password is given and a guest otherwise, and the action persists the email
   into session metadata without ever storing the password.
"""

import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from cart.services.checkout_service import CheckoutService
from cart.views import CheckoutViewSet
from tests.factories import CartFactory, CartItemFactory

pytestmark = [pytest.mark.django_db, pytest.mark.checkout, pytest.mark.integration]

CONTACT_URL = "/api/checkout/contact/"


@pytest.fixture
def digital_cart(customer_user, digital_product, site_settings):
    cart = CartFactory(user=customer_user)
    CartItemFactory(cart=cart, product=digital_product, quantity=1)
    return cart


def _attach_session(request):
    """Give a bare APIRequestFactory request a usable session."""
    from django.contrib.sessions.middleware import SessionMiddleware

    SessionMiddleware(lambda r: None).process_request(request)
    request.session.save()
    return request


class TestContactEndpointRouting:
    def test_contact_url_is_routed(self, auth_client, digital_cart):
        """The URL the frontend (checkout.js submitContact) POSTs to must not
        404. Regression guard: CheckoutViewSet is hand-wired in cart/urls.py, so
        an @action decorator alone routes nothing — the path must be explicit."""
        resp = auth_client.post(CONTACT_URL, {"email": "shopper@example.com"}, format="json")
        assert resp.status_code != 404, (
            "POST /api/checkout/contact/ is unreachable — checkout.js posts here."
        )


class TestContactActionLogic:
    """Drives CheckoutViewSet.contact directly (bypassing the missing route) so
    the action's own behaviour is verified regardless of the wiring gap."""

    def _call(self, user, data, authenticated=True):
        factory = APIRequestFactory()
        request = factory.post(CONTACT_URL, data, format="json")
        _attach_session(request)
        if authenticated:
            force_authenticate(request, user=user)
        view = CheckoutViewSet.as_view({"post": "contact"})
        return view(request)

    def test_email_required(self, customer_user, digital_cart):
        resp = self._call(customer_user, {})
        assert resp.status_code == 400
        assert "email" in str(resp.data).lower()

    def test_email_persisted_to_session_metadata(self, customer_user, digital_cart):
        resp = self._call(customer_user, {"email": "shopper@example.com"})
        assert resp.status_code == 200, resp.data
        session = CheckoutService.get_or_create_session(digital_cart)
        assert session.metadata.get("email") == "shopper@example.com"

    def test_password_never_stored_in_session(self, customer_user, digital_cart):
        """A password may ride along, but it must never be persisted on the
        session (the metadata is serialized back to the client)."""
        self._call(
            customer_user,
            {"email": "shopper@example.com", "password": "s3cret-passphrase"},
        )
        session = CheckoutService.get_or_create_session(digital_cart)
        assert "password" not in (session.metadata or {})
        assert "s3cret-passphrase" not in str(session.metadata or {})

    def test_name_persisted_to_session_metadata(self, customer_user, digital_cart):
        resp = self._call(
            customer_user,
            {"email": "shopper@example.com", "first_name": "Ada", "last_name": "Lovelace"},
        )
        assert resp.status_code == 200, resp.data
        session = CheckoutService.get_or_create_session(digital_cart)
        assert session.metadata.get("contact_name") == "Ada Lovelace"


class TestEnsureCheckoutUserAccountCreation:
    """The 'previously-dead' function the contact endpoint wires. A password
    (opt-in) must create a real, non-guest account; no password stays guest."""

    def _guest_cart(self, digital_product):
        # A cart with no user is the guest starting point.
        cart = CartFactory(user=None)
        CartItemFactory(cart=cart, product=digital_product, quantity=1)
        return cart

    def test_password_creates_real_account(self, digital_product, site_settings):
        site_settings.account_creation_timing = "during_checkout"
        site_settings.save(update_fields=["account_creation_timing"])
        cart = self._guest_cart(digital_product)
        session = CheckoutService.get_or_create_session(cart)

        ok, _msg = CheckoutService.ensure_checkout_user(
            session,
            {
                "email": "realuser@example.com",
                "first_name": "Real",
                "last_name": "User",
                "password": "a-strong-passphrase-123",
            },
        )
        assert ok
        cart.refresh_from_db()
        assert cart.user is not None
        assert not cart.user.username.startswith("guest_")
        assert cart.user.email == "realuser@example.com"
        # Password is hashed, never stored in plaintext.
        assert cart.user.password != "a-strong-passphrase-123"
        assert cart.user.check_password("a-strong-passphrase-123")

    def test_no_password_creates_guest(self, digital_product, site_settings):
        site_settings.account_creation_timing = "during_checkout"
        site_settings.save(update_fields=["account_creation_timing"])
        cart = self._guest_cart(digital_product)
        session = CheckoutService.get_or_create_session(cart)

        ok, _msg = CheckoutService.ensure_checkout_user(
            session, {"email": "guestuser@example.com", "first_name": "Gwen"}
        )
        assert ok
        cart.refresh_from_db()
        assert cart.user is not None
        assert cart.user.username.startswith("guest_")
