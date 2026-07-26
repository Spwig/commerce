"""
Regression coverage for today's checkout-auth fixes.

Three fixes are pinned here, all driven through the real HTTP endpoints:

1. ``core/api/authentication.py`` — ``HeadlessAPIMixin`` now lists
   ``SessionAuthentication`` alongside the token classes. A customer logged
   in to the storefront in a browser must be recognised by the cart/checkout
   APIs and get their *account* cart, instead of being treated as an
   anonymous visitor with a throwaway session cart (the pre-fix bug). DRF
   still enforces CSRF on session-authenticated *unsafe* requests, while
   token-authenticated headless clients stay CSRF-free.

2. ``cart/views.py::CartViewSet.get_cart`` + ``cart/signals.py::
   merge_guest_cart_on_login`` — a guest's session cart is adopted into the
   account at login (and, if the user already had a cart, merged), with the
   documented guard rails (empty carts and already-owned carts are left
   alone).

3. ``cart/views.py::CheckoutViewSet.set_shipping_address`` — a logged-in
   customer can select one of their own saved ``orders.Address`` records by
   id; another customer's address id is rejected.
"""

from decimal import Decimal

import pytest
from django.conf import settings as dj_settings
from django.middleware.csrf import get_token
from django.test import Client, RequestFactory
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from cart.models import Cart, CheckoutSession
from tests.factories import (
    AddressFactory,
    CartFactory,
    CartItemFactory,
    ProductFactory,
    UserFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.checkout]

ADD_URL = "/api/cart/add/"
CART_URL = "/api/cart/"
SHIPPING_ADDRESS_URL = "/api/checkout/shipping-address/"


@pytest.fixture(autouse=True)
def _clear_fx_cache():
    """sync_cart_currency negative-caches failed FX pairs for 300s; with
    pytest.ini's --reuse-db that key survives across runs. Start clean so a
    stale key never changes what these auth tests observe."""
    from django.core.cache import cache

    cache.clear()
    yield


@pytest.fixture
def product(db, category):
    """A simple, in-stock, USD-priced product usable via /api/cart/add/."""
    return ProductFactory(
        name="Auth Test Widget",
        slug="auth-test-widget",
        category=category,
        price=Decimal("25.00"),
        price_currency="USD",
    )


def _csrf_pair(client):
    """Prime a matching CSRF cookie on ``client`` and return the token to send
    as the request header.

    Django's CSRF check passes when the cookie and the submitted token unmask
    to the same secret; using the *same* masked token for both trivially
    satisfies that. This mirrors what the storefront JS does (cookie set by
    the server, echoed back in X-CSRFToken) without depending on a specific
    page rendering the token.
    """
    token = get_token(RequestFactory().get("/"))
    client.cookies[dj_settings.CSRF_COOKIE_NAME] = token
    return token


# ============================================================
# 1. SessionAuthentication on the storefront cart API
# ============================================================


class TestSessionAuthOnCartAPI:
    def test_session_logged_in_user_gets_account_cart_not_session_cart(
        self, customer_user, product
    ):
        """A browser-session-authenticated customer POSTing to /api/cart/add/
        gets their USER cart (cart.user == their id, session_key is NULL) — not
        an anonymous session cart. Pre-fix, SessionAuthentication was absent so
        request.user was AnonymousUser and get_cart built a session cart."""
        client = Client()
        client.force_login(customer_user)
        token = _csrf_pair(client)

        resp = client.post(
            ADD_URL,
            {"product_id": product.id, "quantity": 1},
            **{dj_settings.CSRF_HEADER_NAME: token},
        )

        assert resp.status_code == 200, resp.content
        body = resp.json()
        assert body["success"] is True
        cart_data = body["cart"]
        # The exact regression: the cart is the account's, keyed to the user
        # and with no session_key.
        assert cart_data["user"] == customer_user.id
        assert cart_data["session_key"] is None

        # And it is genuinely persisted as a user cart, not a session cart.
        cart = Cart.objects.get(id=cart_data["id"])
        assert cart.user_id == customer_user.id
        assert cart.session_key is None
        assert not Cart.objects.filter(user__isnull=True, items__product=product).exists()

    def test_session_auth_unsafe_request_without_csrf_is_rejected(self, customer_user, product):
        """DRF enforces CSRF on session-authenticated unsafe requests: a POST
        with no CSRF token is rejected with 403 and nothing is added."""
        client = Client(enforce_csrf_checks=True)
        client.force_login(customer_user)

        resp = client.post(ADD_URL, {"product_id": product.id, "quantity": 1})

        assert resp.status_code == 403, resp.content
        # Specifically a CSRF rejection (not some unrelated 403) — this is the
        # DRF SessionAuthentication.enforce_csrf path, which only runs because
        # the session-authenticated user was recognised in the first place.
        assert "CSRF" in resp.json()["detail"]
        # No cart item leaked through the rejected request.
        assert not Cart.objects.filter(user=customer_user, items__isnull=False).exists()

    def test_token_auth_request_is_csrf_free(self, customer_user, product):
        """Token-authenticated headless clients stay CSRF-free: the same unsafe
        POST, authenticated by DRF token instead of session and carrying no
        CSRF token, succeeds and still resolves to the user's account cart."""
        token = Token.objects.create(user=customer_user)
        client = APIClient(enforce_csrf_checks=True)
        client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        resp = client.post(ADD_URL, {"product_id": product.id, "quantity": 1}, format="json")

        assert resp.status_code == 200, resp.content
        body = resp.json()
        assert body["success"] is True
        assert body["cart"]["user"] == customer_user.id
        assert body["cart"]["session_key"] is None


# ============================================================
# 2. Guest cart adoption / merge at login
# ============================================================


class TestGuestCartMergeOnLogin:
    def test_guest_cart_is_adopted_at_login(self, customer_user, product):
        """Guest adds an item (anonymous session cart), then logs in through
        the real auth path. The user_logged_in receiver adopts the guest cart:
        user gets set, session_key cleared, and /api/cart/ as the user shows
        the item."""
        client = Client()
        add = client.post(ADD_URL, {"product_id": product.id, "quantity": 2})
        assert add.status_code == 200, add.content

        guest_cart_id = client.session["guest_cart_id"]
        guest_cart = Cart.objects.get(id=guest_cart_id)
        assert guest_cart.user_id is None
        assert guest_cart.items.count() == 1

        assert client.login(username=customer_user.username, password="testpass123")

        guest_cart.refresh_from_db()
        assert guest_cart.user_id == customer_user.id
        assert guest_cart.session_key is None

        resp = client.get(CART_URL)
        assert resp.status_code == 200, resp.content
        body = resp.json()
        assert body["user"] == customer_user.id
        product_ids = [item["product"]["id"] for item in body["items"]]
        assert product.id in product_ids

    def test_empty_guest_cart_is_not_adopted(self, customer_user, product):
        """An empty guest cart (guest merely viewed /api/cart/) is left alone:
        the receiver requires items.exists() before adopting."""
        client = Client()
        view = client.get(CART_URL)
        assert view.status_code == 200, view.content

        guest_cart_id = client.session["guest_cart_id"]
        assert Cart.objects.get(id=guest_cart_id).items.count() == 0

        assert client.login(username=customer_user.username, password="testpass123")

        empty_cart = Cart.objects.get(id=guest_cart_id)
        assert empty_cart.user_id is None  # not adopted
        assert empty_cart.session_key is not None

    def test_cart_owned_by_another_user_is_never_adopted(self, customer_user, product):
        """If session['guest_cart_id'] points at a cart that already belongs to
        someone else, the receiver's user__isnull=True filter refuses it — a
        login can never steal another account's cart."""
        other_user = UserFactory(username="other_owner")
        other_cart = CartFactory(user=other_user)
        CartItemFactory(cart=other_cart, product=product)

        client = Client()
        session = client.session
        session["guest_cart_id"] = other_cart.id
        session.save()

        assert client.login(username=customer_user.username, password="testpass123")

        other_cart.refresh_from_db()
        assert other_cart.user_id == other_user.id  # untouched

    def test_existing_user_cart_merges_with_adopted_guest_cart(self, customer_user, product):
        """User already has a regular account cart with an item; a guest cart
        with a different item is adopted at login. The next get_or_create_cart
        folds the two account carts together — both items survive, one cart
        remains."""
        other_product = ProductFactory(
            name="Existing Cart Widget",
            slug="existing-cart-widget",
            category=product.category,
            price=Decimal("15.00"),
            price_currency="USD",
        )
        existing_cart = CartFactory(user=customer_user)
        CartItemFactory(cart=existing_cart, product=other_product)

        client = Client()
        add = client.post(ADD_URL, {"product_id": product.id, "quantity": 1})
        assert add.status_code == 200, add.content
        guest_cart_id = client.session["guest_cart_id"]

        assert client.login(username=customer_user.username, password="testpass123")

        resp = client.get(CART_URL)
        assert resp.status_code == 200, resp.content
        body = resp.json()
        product_ids = {item["product"]["id"] for item in body["items"]}
        assert {product.id, other_product.id} <= product_ids

        # Exactly one regular (session_key IS NULL) account cart remains.
        regular_carts = Cart.objects.filter(user=customer_user, session_key__isnull=True)
        assert regular_carts.count() == 1


# ============================================================
# 3. Checkout with saved addresses
# ============================================================


class TestCheckoutSavedAddress:
    def _login_and_csrf(self, customer_user, product):
        client = Client()
        client.force_login(customer_user)
        # Give the account cart an item so checkout has something to price.
        token = _csrf_pair(client)
        add = client.post(
            ADD_URL,
            {"product_id": product.id, "quantity": 1},
            **{dj_settings.CSRF_HEADER_NAME: token},
        )
        assert add.status_code == 200, add.content
        return client

    def test_logged_in_user_can_select_own_saved_address(self, customer_user, product):
        """POST /api/checkout/shipping-address/ with {'address_id': <own id>}
        succeeds and the saved Address is attached to the checkout session."""
        client = self._login_and_csrf(customer_user, product)
        address = AddressFactory(user=customer_user, address_type="shipping")

        token = _csrf_pair(client)
        resp = client.post(
            SHIPPING_ADDRESS_URL,
            {"address_id": address.id},
            **{dj_settings.CSRF_HEADER_NAME: token},
        )

        assert resp.status_code == 200, resp.content
        assert resp.json()["success"] is True

        cart = Cart.objects.get(user=customer_user, session_key__isnull=True)
        session = CheckoutSession.objects.get(cart=cart)
        assert session.shipping_address_id == address.id
        assert session.shipping_address_data is None

    def test_another_users_address_is_rejected(self, customer_user, product):
        """An address id belonging to a different user is rejected — the
        service scopes the lookup to session.cart.user, so it 404s internally
        and the endpoint returns a 400 without touching the session."""
        client = self._login_and_csrf(customer_user, product)
        other_user = UserFactory(username="address_owner")
        foreign_address = AddressFactory(user=other_user, address_type="shipping")

        token = _csrf_pair(client)
        resp = client.post(
            SHIPPING_ADDRESS_URL,
            {"address_id": foreign_address.id},
            **{dj_settings.CSRF_HEADER_NAME: token},
        )

        assert resp.status_code == 400, resp.content
        assert resp.json()["success"] is False

        cart = Cart.objects.get(user=customer_user, session_key__isnull=True)
        session = CheckoutSession.objects.filter(cart=cart).first()
        if session is not None:
            assert session.shipping_address_id != foreign_address.id
