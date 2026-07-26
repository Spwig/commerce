"""
ACP product-feed projection + binding.

ACP is off by default, so the feed 404s until the merchant enables both agentic
commerce and the ACP surface. The projection reuses the UCP catalogue service,
so these focus on the ACP-specific reshaping (envelope, barcodes, underscore
path) and the gating.
"""

import pytest
from django.test import Client

from agentic.models import AgenticSettings
from agentic.services import acp_service
from tests.factories import ProductFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration]

FEED_URL = "/api/agentic/acp/product_feed/"


def _product(**kw):
    kw.setdefault("status", "published")
    kw.setdefault("price", "25.00")
    return ProductFactory(**kw)


def _enable_acp(**overrides):
    s = AgenticSettings.get_settings()
    s.is_enabled = True
    s.acp_enabled = True
    for k, v in overrides.items():
        setattr(s, k, v)
    s.save()


class TestGating:
    def test_404_when_agentic_off(self, site_settings):
        assert Client().get(FEED_URL).status_code == 404

    def test_404_when_acp_off_but_agentic_on(self, site_settings):
        s = AgenticSettings.get_settings()
        s.is_enabled = True
        s.acp_enabled = False  # default
        s.save()
        assert Client().get(FEED_URL).status_code == 404

    def test_200_when_acp_enabled(self, site_settings):
        _enable_acp()
        assert Client().get(FEED_URL).status_code == 200


class TestProjection:
    def test_acp_shape_with_barcodes(self, site_settings):
        p = _product(name="Barcoded", gtin="0123456789012")
        doc = acp_service.to_acp_product(p)
        assert doc["title"] == "Barcoded"
        # Converged shape: nested variants + availability {available,status}.
        assert doc["availability"]["available"] in (True, False)
        assert isinstance(doc["variants"], list) and doc["variants"]
        # ACP barcodes[{type,value}].
        assert {"type": "gtin", "value": "0123456789012"} in doc["barcodes"]

    def test_feed_envelope_and_pagination(self, site_settings):
        for i in range(3):
            _product(name=f"P{i}")
        feed = acp_service.product_feed(page=1, page_size=2)
        assert feed["version"] == "acp-feed-1"
        assert feed["total"] == 3
        assert len(feed["products"]) == 2
        assert feed["next_page"] == 2  # more remain
        page2 = acp_service.product_feed(page=2, page_size=2)
        assert len(page2["products"]) == 1
        assert "next_page" not in page2

    def test_hidden_products_excluded(self, site_settings):
        _product(name="Visible")
        _product(name="Hidden", agent_visible=False)
        feed = acp_service.product_feed()
        titles = {p["title"] for p in feed["products"]}
        assert "Visible" in titles
        assert "Hidden" not in titles

    def test_feed_over_http(self, site_settings):
        _enable_acp()
        _product(name="Feed Item")
        body = Client().get(FEED_URL).json()
        assert body["version"] == "acp-feed-1"
        assert any(p["title"] == "Feed Item" for p in body["products"])
