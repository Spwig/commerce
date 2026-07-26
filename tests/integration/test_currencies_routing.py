"""Regression guard: the literal ``/api/currencies/`` routes must not be
swallowed by the ``<str:code>/`` catch-all.

``core/urls.py`` wires the currency admin endpoints by hand. ``bulk-update`` is
a literal path that must be registered **before** ``api/currencies/<str:code>/``
— otherwise ``<str:code>`` matches ``"bulk-update"`` and every POST to
``/api/currencies/bulk-update/`` resolves to ``update_currency_settings``
(PATCH-only) and 405s, never reaching ``bulk_update_currencies``. That is the
bug this test locks down.
"""

import pytest
from django.urls import resolve

from core.api import currency_endpoints

pytestmark = [
    pytest.mark.integration,
    pytest.mark.url_routing,
]


@pytest.mark.parametrize(
    "path,expected_view",
    [
        ("/api/currencies/bulk-update/", currency_endpoints.bulk_update_currencies),
        ("/api/currencies/reorder/", currency_endpoints.reorder_currencies),
        ("/api/currencies/activate/", currency_endpoints.activate_currencies),
        ("/api/currencies/deactivate/", currency_endpoints.deactivate_currencies),
        ("/api/currencies/active/", currency_endpoints.list_active_currencies),
        # A real currency code still resolves to the per-code settings view.
        ("/api/currencies/USD/", currency_endpoints.update_currency_settings),
    ],
)
def test_currency_literal_routes_not_shadowed(path, expected_view):
    assert resolve(path).func is expected_view, (
        f"{path} resolved to the wrong view — a literal route is being "
        f"swallowed by the <str:code>/ catch-all; check ordering in core/urls.py"
    )
