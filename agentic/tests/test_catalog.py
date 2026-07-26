"""
UCP catalog projection and the read endpoints.

Covers the money->minor-units conversion (incl. zero-decimal currencies), the
UCP product shape (required fields, simple-product-as-single-variant), the
sellable-products filter (no property traps), and endpoint gating.
"""

from decimal import Decimal

import pytest
from django.test import Client
from djmoney.money import Money

from agentic.models import AgenticSettings
from agentic.services import catalog_service
from tests.factories import ProductFactory, ProductVariantFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


@pytest.fixture
def client():
    return Client()


def _enable():
    s = AgenticSettings.get_settings()
    s.is_enabled = True
    s.save()


class TestMoneyToUcp:
    def test_usd_is_cents(self):
        assert catalog_service.money_to_ucp(Money(Decimal("19.99"), "USD")) == {
            "amount": 1999,
            "currency": "USD",
        }

    def test_zero_decimal_currency_is_not_multiplied(self):
        # JPY has no minor unit; 1000 yen is amount 1000, not 100000.
        assert catalog_service.money_to_ucp(Money(Decimal("1000"), "JPY")) == {
            "amount": 1000,
            "currency": "JPY",
        }

    def test_none_is_none(self):
        assert catalog_service.money_to_ucp(None) is None


class TestUcpProductShape:
    def test_required_fields_present(self, db):
        p = ProductFactory(name="Widget", price=Decimal("25.00"))
        doc = catalog_service.to_ucp_product(p)

        assert doc["id"] == str(p.id)
        assert doc["title"] == "Widget"
        assert doc["description"]  # non-empty (falls back to name)
        assert doc["price_range"]["min"] == {"amount": 2500, "currency": "USD"}
        assert len(doc["variants"]) >= 1

    def test_simple_product_becomes_one_synthetic_variant(self, db):
        p = ProductFactory(name="Simple", price=Decimal("10.00"))
        doc = catalog_service.to_ucp_product(p)

        assert len(doc["variants"]) == 1
        v = doc["variants"][0]
        assert v["id"] == f"product-{p.id}"
        assert v["title"] == "Simple"
        assert v["price"] == {"amount": 1000, "currency": "USD"}

    def test_variants_are_emitted(self, db):
        p = ProductFactory(name="Variable", price=Decimal("30.00"), product_type="variable")
        ProductVariantFactory(product=p, name="Small", is_active=True)
        ProductVariantFactory(product=p, name="Large", is_active=True)

        doc = catalog_service.to_ucp_product(p)
        titles = {v["title"] for v in doc["variants"]}
        assert {"Small", "Large"} <= titles
        assert all("price" in v for v in doc["variants"])


class TestSellableFilter:
    def test_only_sellable_products(self, db):
        visible = ProductFactory(name="Published", status="published")
        ProductFactory(name="Draft", status="draft")
        ProductFactory(name="Hidden", status="published", hide_from_storefront=True)

        ids = set(catalog_service.sellable_products().values_list("id", flat=True))
        assert visible.id in ids
        assert len(ids) == 1  # draft + hidden excluded

    def test_queryset_actually_executes(self, db):
        # Guard against the product_feeds failure mode: a queryset that only
        # constructs (and would blow up on a property filter) never runs here.
        ProductFactory(status="published")
        assert list(catalog_service.sellable_products()) is not None


class TestSearch:
    def test_matches_name(self, db):
        ProductFactory(name="Blue Shoes", status="published")
        ProductFactory(name="Red Hat", status="published")

        products, total = catalog_service.search("shoes")
        assert total == 1
        assert products[0].name == "Blue Shoes"

    def test_pagination(self, db):
        for i in range(5):
            ProductFactory(name=f"Item {i}", status="published")
        page1, total = catalog_service.search("", page=1, page_size=2)
        assert total == 5
        assert len(page1) == 2


class TestEndpoints:
    def test_search_404_when_disabled(self, client):
        assert client.get("/api/agentic/ucp/products/").status_code == 404

    def test_search_200_when_enabled(self, client, db):
        ProductFactory(name="Findable", status="published")
        _enable()
        resp = client.get("/api/agentic/ucp/products/?q=Findable")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 1
        assert data["products"][0]["title"] == "Findable"

    def test_lookup_404_when_disabled(self, client, db):
        p = ProductFactory(status="published")
        assert client.get(f"/api/agentic/ucp/products/{p.id}/").status_code == 404

    def test_lookup_returns_product_when_enabled(self, client, db):
        p = ProductFactory(name="Lookup Me", status="published")
        _enable()
        resp = client.get(f"/api/agentic/ucp/products/{p.id}/")
        assert resp.status_code == 200
        assert resp.json()["title"] == "Lookup Me"

    def test_lookup_404_for_nonsellable(self, client, db):
        draft = ProductFactory(status="draft")
        _enable()
        assert client.get(f"/api/agentic/ucp/products/{draft.id}/").status_code == 404


class TestAgentVisibilityAndCondition:
    def test_agent_invisible_product_is_excluded(self, db):
        visible = ProductFactory(name="Shown", status="published", agent_visible=True)
        ProductFactory(name="Hidden from agents", status="published", agent_visible=False)

        ids = set(catalog_service.sellable_products().values_list("id", flat=True))
        assert visible.id in ids
        assert len(ids) == 1

    def test_agent_invisible_lookup_returns_none(self, db):
        p = ProductFactory(status="published", agent_visible=False)
        assert catalog_service.get_product(p.id) is None

    def test_condition_defaults_to_new_in_ucp_output(self, db):
        p = ProductFactory(status="published")
        assert catalog_service.to_ucp_product(p)["condition"] == "new"

    def test_condition_is_reported(self, db):
        p = ProductFactory(status="published", condition="refurbished")
        assert catalog_service.to_ucp_product(p)["condition"] == "refurbished"
