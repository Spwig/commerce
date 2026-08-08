"""Oracle parity: the ORM backend and the HTTP backend return the SAME Footprint.

Plan §8 verification. The whole "same tests, two targets" design rests on one
claim — that a footprint read in-process from the ORM and the *same* footprint
read over real HTTP from ``/api/e2e/inspect/`` reconstruct to an identical
:class:`Footprint`, so every lifecycle assertion runs unchanged against either.
This proves it end to end: a real order, a real socket, ``HttpBackend`` going
through ``urllib`` to a running ``live_server``, then dataclass equality.

Marked ``e2e`` because it needs ``live_server`` (a real bound socket), like the
golden flows — no browser, just HTTP.
"""

import pytest
from django.test import override_settings

from commerce_footprint.http_backend import HttpBackend, InspectionError
from commerce_footprint.orm_backend import footprint_for_order
from tests.factories import OrderFactory, OrderItemFactory

pytestmark = [pytest.mark.django_db(transaction=True), pytest.mark.e2e]

_TOKEN = "parity-inspection-secret"


@override_settings(SPWIG_E2E_INSPECTION=True, SPWIG_E2E_INSPECTION_TOKEN=_TOKEN)
def test_http_backend_footprint_equals_orm_backend(live_server, warehouse):
    """One scripted order, asserted via both backends → byte-identical."""
    order = OrderFactory()
    OrderItemFactory(order=order)

    orm_footprint = footprint_for_order(order.order_number)

    # 60s (not the 10s default): a threaded live_server serving a full footprint
    # query on a freshly --create-db'd test DB under CI contention is legitimately
    # slow; 10s intermittently trips a read-timeout and reddens unrelated PRs.
    backend = HttpBackend(live_server.url, _TOKEN, timeout=60)
    http_footprint = backend.footprint_for_order(order.order_number)

    # Frozen dataclasses compare by value: equality here means every nested
    # record — order, lines, amounts (Decimal + currency) — round-tripped
    # through JSON without drift.
    assert http_footprint == orm_footprint
    # Guard against a vacuous pass (two empty footprints comparing equal).
    assert http_footprint.correlation == order.order_number
    assert len(http_footprint.orders) == 1
    assert len(http_footprint.orders[0].lines) == 1


@override_settings(SPWIG_E2E_INSPECTION=True, SPWIG_E2E_INSPECTION_TOKEN=_TOKEN)
def test_http_backend_raises_inspection_error_on_wrong_secret(live_server):
    """A transport-level failure (bad secret → 404) surfaces as InspectionError,
    not a silent empty footprint that would make an assertion pass vacuously."""
    order = OrderFactory()
    backend = HttpBackend(live_server.url, "the-wrong-secret", timeout=60)
    with pytest.raises(InspectionError):
        backend.footprint_for_order(order.order_number)
