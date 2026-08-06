"""
Tier-1 cross-customer isolation invariants (plan invariant #9).

Spwig is single-tenant by design (SITE_ID=1, one merchant per install), so the
"cross-merchant/tenant" half of #9 has no runtime surface. The real, testable
property is customer-to-customer: **a customer must never see or act on another
customer's order**, and a guest must not open an order just by knowing its
number.

The ownership gates already exist (OrderService.get_order_detail, the
order_confirmation_view user/guest branches, ReturnRequestViewSet.create_for_order).
These tests are the release-blocking guard that they STAY intact across the real
customer order API, the confirmation page, and the returns flow — the load-
bearing controls behind every amount/address/line the storefront shows a buyer.
"""

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from tests.factories import OrderFactory, OrderItemFactory, UserFactory

pytestmark = [pytest.mark.django_db, pytest.mark.invariant]


@pytest.fixture
def two_customers(db, site_settings):
    """Alice and Bob, each with their own order (Alice's has a line item)."""
    alice = UserFactory()
    bob = UserFactory()
    alice_order = OrderFactory(user=alice, email=alice.email, status="processing")
    OrderItemFactory(order=alice_order)
    bob_order = OrderFactory(user=bob, email=bob.email, status="processing")
    return alice, bob, alice_order, bob_order


def _api(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


def _order_numbers(payload):
    """Extract order numbers from a list response (paginated or bare list)."""
    rows = payload.get("results", payload) if isinstance(payload, dict) else payload
    return {r.get("order_number") for r in rows}


def test_customer_cannot_retrieve_another_customers_order(two_customers):
    """GET /api/orders/{alice's number}/ as Bob -> 404 (not a leak of amounts).

    Guard-the-guard: Alice CAN fetch her own order at the same URL, so Bob's
    404 is the ownership gate firing, not a broken URL or auth."""
    alice, bob, alice_order, _bob_order = two_customers
    url = reverse("orders:order-detail", kwargs={"order_number": alice_order.order_number})

    owner_resp = _api(alice).get(url)
    assert owner_resp.status_code == 200, (
        "positive control failed — URL/auth broken, test is vacuous"
    )

    resp = _api(bob).get(url)
    assert resp.status_code == 404
    # And the response body must not carry Alice's total to Bob.
    assert str(alice_order.total_amount.amount) not in resp.content.decode()


def test_order_list_shows_only_own_orders(two_customers):
    """Bob's order list contains his order and never Alice's."""
    _alice, bob, alice_order, bob_order = two_customers
    resp = _api(bob).get(reverse("orders:order-list"))
    assert resp.status_code == 200
    numbers = _order_numbers(resp.json())
    assert bob_order.order_number in numbers
    assert alice_order.order_number not in numbers


def test_customer_cannot_cancel_another_customers_order(two_customers):
    """Bob cannot cancel Alice's order, and her order is left unchanged.

    Guard-the-guard: the owner reaches the action (NOT 404) at the same URL —
    a 400 "can't cancel this status" would still prove the ownership gate let
    the owner through, so Bob's 404 is ownership, not a routing/precondition
    404."""
    alice, bob, alice_order, _bob_order = two_customers
    before = alice_order.status
    url = reverse("orders:order-cancel", kwargs={"order_number": alice_order.order_number})

    owner_resp = _api(alice).post(url)
    assert owner_resp.status_code != 404, "positive control failed — owner blocked, test is vacuous"

    alice_order.refresh_from_db()  # owner may have cancelled; re-read baseline
    before = alice_order.status
    resp = _api(bob).post(url)
    assert resp.status_code == 404
    alice_order.refresh_from_db()
    assert alice_order.status == before


def test_confirmation_page_blocks_another_authenticated_customer(client, two_customers):
    """The order-confirmation page 404s for a logged-in non-owner.

    Guard-the-guard: the owner gets 200 at the same URL, so the non-owner's 404
    is the ownership branch, not a routing/middleware 404."""
    alice, bob, alice_order, _bob_order = two_customers
    url = reverse(
        "page_builder:order_confirmation",
        kwargs={"order_number": alice_order.order_number},
    )

    client.force_login(alice)
    assert client.get(url).status_code == 200, "positive control failed — test is vacuous"

    client.force_login(bob)
    assert client.get(url).status_code == 404


def test_confirmation_page_blocks_guest_without_session_grant(client, two_customers):
    """An anonymous visitor cannot open an order by number — the guest allow-list
    is populated only for the browser that placed the order."""
    _alice, _bob, alice_order, _bob_order = two_customers
    url = reverse(
        "page_builder:order_confirmation",
        kwargs={"order_number": alice_order.order_number},
    )
    resp = client.get(url)
    assert resp.status_code == 404


def test_customer_cannot_open_return_for_another_customers_order(two_customers):
    """create-for-order 404s before any item is read, and creates no return.

    Guard-the-guard: the owner reaches past the ownership gate at the same URL
    (an empty body then fails item validation with a non-404 status), so Bob's
    404 is the ownership branch, not the URL."""
    from orders.models import ReturnRequest

    alice, bob, alice_order, _bob_order = two_customers
    url = reverse(
        "orders:return-request-create-for-order",
        kwargs={"order_number": alice_order.order_number},
    )

    owner_resp = _api(alice).post(url, {}, format="json")
    assert owner_resp.status_code != 404, "positive control failed — owner blocked, test is vacuous"

    resp = _api(bob).post(url, {}, format="json")
    assert resp.status_code == 404
    assert not ReturnRequest.objects.filter(order=alice_order).exists()


def test_default_return_create_cannot_bind_a_foreign_order(two_customers):
    """The default POST /api/return-requests/ exposes a writable `order` field
    and does not bind the requester as owner. Whatever the response, it must
    NEVER create a return against another customer's order. (It currently errors
    rather than cleanly rejecting — a robustness wart, not an isolation hole;
    this pins the isolation half.)"""
    from orders.models import ReturnRequest

    _alice, bob, alice_order, _bob_order = two_customers
    api = _api(bob)
    api.raise_request_exception = False  # a 500 here must not fail the test
    resp = api.post(
        reverse("orders:return-request-list"),
        {"order": alice_order.id, "reason": "not as described"},
        format="json",
    )
    assert resp.status_code != 201
    assert not ReturnRequest.objects.filter(order=alice_order).exists()


def test_authenticated_user_cannot_open_a_guest_orders_confirmation(two_customers):
    """A logged-in user cannot open an ownerless GUEST order's confirmation by
    number — previously the `order.user and ...` guard let any authenticated
    user through for guest orders. The browser that placed it (session grant)
    still can, which is the positive control proving the 404 is the gate."""
    from django.test import Client

    _alice, bob, _ao, _bo = two_customers
    guest_order = OrderFactory(user=None, email="guest@example.test", status="processing")
    url = reverse(
        "page_builder:order_confirmation",
        kwargs={"order_number": guest_order.order_number},
    )

    authed = Client()
    authed.force_login(bob)
    assert authed.get(url).status_code == 404  # the fix: no free pass for authed users

    guest = Client()
    session = guest.session
    session["guest_order_numbers"] = [guest_order.order_number]
    session.save()
    assert guest.get(url).status_code == 200  # session grant still works


def test_contact_form_does_not_link_another_customers_order(two_customers):
    """The public contact form must not attach a message to an order the
    submitter doesn't own. Bob's message is still created, just not linked to
    Alice's order; the owner's message DOES link (positive control)."""
    from admin_api.models import CustomerMessage

    alice, bob, alice_order, _bob_order = two_customers
    url = reverse("contact-submit")
    base = {
        "name": "X",
        "subject": "About an order",
        "message": "hello",
        "order_number": alice_order.order_number,
    }

    resp = _api(bob).post(url, {**base, "email": bob.email}, format="json")
    assert resp.status_code in (200, 201)
    assert not CustomerMessage.objects.filter(order=alice_order).exists()  # not linked

    resp2 = _api(alice).post(url, {**base, "email": alice.email}, format="json")
    assert resp2.status_code in (200, 201)
    assert CustomerMessage.objects.filter(order=alice_order, user=alice).exists()  # owner links


# Every OrderViewSet read action routes through OrderService.get_order_detail,
# the single ownership gate. Cover extra surfaces so a regression in any one
# (not just the retrieve() we already test) is caught. Limited to actions whose
# OWNER response is distinguishable from a not-found (tracking -> 403 when no
# tracking yet; notes -> 200) so the positive control is meaningful; the
# document actions (packing-slip, commercial-invoice) 404 for an unshipped
# owner order too, which would make an owner-vs-nonowner 404 comparison vacuous
# — they share the exact same gate, already exercised by retrieve + these.
@pytest.mark.parametrize("action_name", ["order-get-tracking", "order-list-notes"])
def test_customer_cannot_read_another_customers_order_action(action_name, two_customers):
    alice, bob, alice_order, _bob_order = two_customers
    url = reverse(f"orders:{action_name}", kwargs={"order_number": alice_order.order_number})

    # Owner reaches the action (403 "no tracking" / 200 notes — both non-404);
    # the non-owner is 404'd by the ownership gate.
    assert _api(alice).get(url).status_code != 404, f"positive control failed for {action_name}"
    assert _api(bob).get(url).status_code == 404
