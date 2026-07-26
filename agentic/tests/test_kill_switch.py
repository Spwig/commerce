"""
THE contract: with agentic commerce off, every agentic URL is 404 — not 403,
not a redirect, not a 200 with an empty body. Off must be indistinguishable
from "this store has never heard of agentic commerce".

As new agentic URLs are added (catalog API, MCP, checkout sessions), each gets
an entry in AGENTIC_URLS below. The test then guards the whole surface at once.
"""

import pytest
from django.test import Client

from agentic.models import AgenticSettings

pytestmark = [pytest.mark.django_db, pytest.mark.integration]

# Every publicly reachable agentic URL that returns 200 when enabled. Extend
# this as the surface grows. (Lookup-by-id is data-dependent, so it is gated
# separately in test_catalog.py rather than listed here.)
AGENTIC_URLS = [
    "/.well-known/ucp",
    "/api/agentic/ucp/products/",
]


@pytest.fixture
def client():
    return Client()


def _enable(**overrides):
    s = AgenticSettings.get_settings()
    s.is_enabled = True
    for k, v in overrides.items():
        setattr(s, k, v)
    s.save()
    return s


@pytest.mark.parametrize("url", AGENTIC_URLS)
class TestKillSwitchContract:
    def test_404_when_disabled(self, client, url):
        # Default state is off.
        assert client.get(url).status_code == 404

    def test_404_when_kill_switch_engaged(self, client, url):
        _enable(kill_switch_engaged=True)
        assert client.get(url).status_code == 404

    def test_reachable_when_enabled(self, client, url):
        _enable()
        assert client.get(url).status_code == 200


class TestUcpDiscoveryProfile:
    def test_profile_shape_when_enabled(self, client):
        _enable()
        resp = client.get("/.well-known/ucp")

        assert resp.status_code == 200
        assert resp["Content-Type"] == "application/json"
        assert "public" in resp["Cache-Control"]

        data = resp.json()
        assert data["ucp"]["version"] == "2026-04-08"
        # Capabilities are live-computed from install state. Catalog + cart are
        # always available; checkout/fulfillment appear only when a provider /
        # shipping are configured (covered in test_capabilities.py). The shape
        # here just confirms it is a list of capability ids.
        caps = data["ucp"]["capabilities"]
        assert isinstance(caps, list)
        assert "dev.ucp.shopping.catalog.search" in caps
        assert "dev.ucp.shopping.cart" in caps
        assert "merchant" in data
        assert data["services"]["catalog"]["endpoint"].endswith("/api/agentic/ucp")

    def test_404_when_ucp_surface_disabled_even_if_master_on(self, client):
        _enable(ucp_enabled=False)
        assert client.get("/.well-known/ucp").status_code == 404
