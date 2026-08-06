"""Contract + safety tests for the /api/e2e/inspect/ footprint endpoint.

Two things must hold, forever:

1. **Fail-closed.** Off by default, and even when the flag is on the shared
   secret is mandatory — every unauthorised shape 404s, indistinguishable from
   a route that doesn't exist. This is the guard that keeps the endpoint from
   ever becoming an information-leak surface on a real merchant install.
2. **Serialization parity.** When authorised, the JSON body is byte-identical
   to ``footprint_for_order(order).to_dict()`` — the same Footprint an
   in-process test reads from the ORM, so the black-box tier asserts on exactly
   the same record shapes.

These use the plain Django test client (no live_server) — fast, run in the
normal suite. The real-HTTP round-trip through ``HttpBackend`` is proved
separately in ``tests/e2e/test_oracle_parity.py``.
"""

import pytest
from django.test import Client, override_settings
from django.urls import reverse

from commerce_footprint.orm_backend import footprint_for_order
from tests.factories import OrderFactory, OrderItemFactory

pytestmark = [pytest.mark.django_db, pytest.mark.contract]

_TOKEN = "test-inspection-secret"
_HEADER = "HTTP_X_E2E_INSPECTION_TOKEN"

# Enabled + secret set: the only configuration under which the endpoint serves.
enabled = override_settings(SPWIG_E2E_INSPECTION=True, SPWIG_E2E_INSPECTION_TOKEN=_TOKEN)


def _order_with_line():
    order = OrderFactory()
    OrderItemFactory(order=order)
    return order


def _url(order_number):
    return reverse("e2e_inspect_order", args=[order_number])


def test_disabled_by_default_returns_404(client):
    """With no opt-in (the default on every install) the endpoint does not
    exist — even with a would-be-valid token."""
    order = _order_with_line()
    resp = client.get(_url(order.order_number), **{_HEADER: _TOKEN})
    assert resp.status_code == 404


@enabled
def test_enabled_but_missing_token_returns_404(client):
    order = _order_with_line()
    resp = client.get(_url(order.order_number))  # no secret header
    assert resp.status_code == 404


@enabled
def test_enabled_but_wrong_token_returns_404(client):
    order = _order_with_line()
    resp = client.get(_url(order.order_number), **{_HEADER: "not-the-secret"})
    assert resp.status_code == 404


@enabled
def test_enabled_unknown_order_returns_404(client):
    """A valid secret but a non-existent order still 404s (order existence isn't
    an oracle for the secret)."""
    resp = client.get(_url("NOPENOPENOPE"), **{_HEADER: _TOKEN})
    assert resp.status_code == 404


@override_settings(SPWIG_E2E_INSPECTION=True, SPWIG_E2E_INSPECTION_TOKEN="")
def test_enabled_without_configured_secret_never_authorises(client):
    """Belt-and-braces for the settings boot guard: even if inspection is on
    with an empty configured token, no request can authorise (fail closed)."""
    order = _order_with_line()
    resp = client.get(_url(order.order_number), **{_HEADER: ""})
    assert resp.status_code == 404


@enabled
def test_authorised_returns_footprint_matching_orm_backend(client):
    """The happy path: the JSON body equals the ORM footprint's ``to_dict`` —
    exact serialization parity, so both backends yield identical assertions."""
    order = _order_with_line()

    resp = client.get(_url(order.order_number), **{_HEADER: _TOKEN})
    assert resp.status_code == 200
    assert resp["Content-Type"] == "application/json"

    expected = footprint_for_order(order.order_number).to_dict()
    assert resp.json() == expected
    # Non-vacuous: the order and its one line actually round-tripped.
    assert expected["correlation"] == order.order_number
    assert len(expected["orders"]) == 1
    assert len(expected["orders"][0]["lines"]) == 1


@enabled
def test_endpoint_is_read_only_get(client):
    """An authorised POST is rejected by the method guard — no mutation. The
    view is ``@csrf_exempt`` (read-only), so an authorised POST reaches the
    method guard and gets 405 rather than being pre-empted by CSRF."""
    order = _order_with_line()
    resp = client.post(_url(order.order_number), **{_HEADER: _TOKEN})
    assert resp.status_code == 405


def test_disabled_unsafe_verb_is_404_not_403_under_csrf_enforcement():
    """Existence-leak guard: with CSRF *enforced* (as in production), a POST to
    the disabled route must 404 — not the 403 that CsrfViewMiddleware would give
    for a registered-but-CSRF-protected route, which would confirm it exists.
    ``@csrf_exempt`` on the view is what makes this hold."""
    csrf_client = Client(enforce_csrf_checks=True)
    resp = csrf_client.post(_url("ORD-DOESNTMATTER"))
    assert resp.status_code == 404


@enabled
def test_wrong_token_unsafe_verb_is_404_under_csrf_enforcement():
    """Same guard while enabled: a wrong-secret POST under CSRF enforcement is a
    uniform 404, indistinguishable from an absent route."""
    csrf_client = Client(enforce_csrf_checks=True)
    order = _order_with_line()
    resp = csrf_client.post(_url(order.order_number), **{_HEADER: "wrong"})
    assert resp.status_code == 404


@enabled
def test_non_ascii_token_header_is_404_not_500(client):
    """A non-ASCII secret header must fail closed (404), never raise inside
    ``hmac.compare_digest`` and surface a 500 that (on an enabled host)
    distinguishes this route from an absent one."""
    order = _order_with_line()
    resp = client.get(_url(order.order_number), **{_HEADER: "café-ÿ-not-the-secret"})
    assert resp.status_code == 404
