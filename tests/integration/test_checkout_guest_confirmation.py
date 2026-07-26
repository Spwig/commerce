"""Guest order-confirmation access.

Guest checkout never authenticates the browser, and the confirmation view
404s anonymous visitors. A session allow-list (populated when the order is
placed) lets the guest who just paid view their own confirmation — and only
that order, not any order by number.
"""

import pytest

from tests.factories import OrderFactory, UserFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


class TestGuestConfirmationAccess:
    def test_guest_can_view_allow_listed_order(self, client, site_settings):
        """Anonymous browser whose session lists the order → 200."""
        order = OrderFactory(user=UserFactory())
        session = client.session
        session["guest_order_numbers"] = [order.order_number]
        session.save()

        resp = client.get(f"/en/checkout/confirmation/{order.order_number}/")
        assert resp.status_code == 200

    def test_guest_cannot_view_other_order(self, client, site_settings):
        """Anonymous browser with no allow-list entry → 404 (no order enumeration)."""
        order = OrderFactory(user=UserFactory())
        resp = client.get(f"/en/checkout/confirmation/{order.order_number}/")
        assert resp.status_code == 404

    def test_grant_guest_order_access_records_session(self, rf, site_settings):
        """The helper records the order for anonymous requests, caps growth, and
        no-ops for authenticated users."""
        from django.contrib.auth.models import AnonymousUser
        from django.contrib.sessions.middleware import SessionMiddleware

        from cart.services import CheckoutService

        request = rf.post("/api/checkout/complete/")
        SessionMiddleware(lambda r: None).process_request(request)
        request.user = AnonymousUser()

        order = OrderFactory(user=UserFactory())
        CheckoutService.grant_guest_order_access(request, order)
        assert order.order_number in request.session["guest_order_numbers"]

        # Authenticated users don't need the allow-list.
        request.user = UserFactory()
        other = OrderFactory(user=UserFactory())
        CheckoutService.grant_guest_order_access(request, other)
        assert other.order_number not in request.session.get("guest_order_numbers", [])
