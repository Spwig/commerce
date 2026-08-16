"""
Ship-to region selector (Slice 1 — storefront display/advisory).

A shopper picks a destination country; the storefront reflects that region's
availability. Region-restricted products are shown but marked "does not ship
to [destination]" (default), or hidden with ?ship_only=1. This slice is
display-only — server-side enforcement at checkout is a later slice.

Covers: the shared country->region helper, the set-region writer endpoint, the
sellable/visible/available queryset split, the ship-to widget context, and the
listing marking + toggle.
"""

import json

import pytest
from django.core.cache import cache
from django.urls import reverse

from catalog.context_processors import region_suggestion
from catalog.middleware import (
    get_region_for_country,
    get_ship_to_display,
)
from catalog.models import Product, ProductRegionVisibility
from tests.factories import (
    ProductFactory,
    SalesRegionFactory,
    ShippingCountryFactory,
    StockItemFactory,
    WarehouseFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


@pytest.fixture(autouse=True)
def _clear_region_cache():
    # get_region_for_country / default-region lookups are cached; clear so
    # region rows created per-test are seen.
    cache.clear()
    yield
    cache.clear()


# ---------------------------------------------------------------------------
# Helper: country -> region
# ---------------------------------------------------------------------------


def test_get_region_for_country_matches_countries_list():
    region = SalesRegionFactory(name="Oceania", code="OCE", countries=["AU", "NZ"], priority=5)
    assert get_region_for_country("AU") == region
    assert get_region_for_country("nz") == region  # case-insensitive
    assert get_region_for_country("US") is None
    assert get_region_for_country("") is None


# ---------------------------------------------------------------------------
# set_region endpoint
# ---------------------------------------------------------------------------


def test_set_region_persists_country_and_region(client):
    SalesRegionFactory(name="Oceania", code="OCE", countries=["AU", "NZ"], priority=5)
    ShippingCountryFactory(country_code="AU", is_active=True)

    resp = client.post(
        reverse("set_region"),
        data=json.dumps({"country": "AU"}),
        content_type="application/json",
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["country"] == "AU"
    assert body["region"] == "OCE"
    assert client.session["preferred_country"] == "AU"
    assert client.session["preferred_region"] == "OCE"
    assert resp.cookies["preferred_country"].value == "AU"
    assert resp.cookies["preferred_region"].value == "OCE"


def test_set_region_rejects_country_we_do_not_ship_to(client):
    SalesRegionFactory(name="Oceania", code="OCE", countries=["AU"], priority=5)
    # No active ShippingCountry for AU.

    resp = client.post(
        reverse("set_region"),
        data=json.dumps({"country": "AU"}),
        content_type="application/json",
    )

    assert resp.status_code == 400
    assert resp.json()["success"] is False
    assert "preferred_region" not in client.session


def test_set_region_requires_post(client):
    resp = client.get(reverse("set_region"))
    assert resp.status_code == 405


# ---------------------------------------------------------------------------
# Queryset split: sellable (stock only) vs visible (allowlist) vs available
# ---------------------------------------------------------------------------


def test_sellable_ignores_visibility_available_respects_it():
    home = SalesRegionFactory(name="Home", code="HOME", countries=["US"], priority=10)
    other = SalesRegionFactory(name="Oceania", code="OCE", countries=["AU"], priority=1)
    home_wh = WarehouseFactory(name="Home WH", code="HOME-WH", region=home)
    other_wh = WarehouseFactory(name="Oceania WH", code="OCE-WH", region=other)

    product = ProductFactory(
        track_inventory=True, status="published", region_restriction_mode="only_in"
    )
    StockItemFactory(product=product, warehouse=home_wh, on_hand=5, allocated=0)
    StockItemFactory(product=product, warehouse=other_wh, on_hand=5, allocated=0)
    # Allowlist the product to OTHER region only -> restricted in HOME.
    ProductRegionVisibility.objects.create(product=product, region=other)

    all_products = Product.objects.all()
    assert product in all_products.sellable_in_region(home)  # stock is fine
    assert product not in all_products.visible_in_region(home)  # geo-restricted
    assert product not in all_products.available_in_region(home)  # visibility gate
    # It IS available in the region it's allowlisted to (and has stock there).
    assert product in all_products.available_in_region(other)


# ---------------------------------------------------------------------------
# get_ship_to_display
# ---------------------------------------------------------------------------


def test_get_ship_to_display_prefers_explicit_country(rf):
    SalesRegionFactory(name="Oceania", code="OCE", countries=["AU"], priority=5)
    request = rf.get("/")
    request.session = {"preferred_country": "AU"}
    code, name = get_ship_to_display(request)
    assert code == "AU"
    assert name == "Australia"


# ---------------------------------------------------------------------------
# Ship-to widget context
# ---------------------------------------------------------------------------


def test_ship_to_widget_context_lists_shippable_countries():
    from design.templatetags.theme_tags import _get_ship_to_context

    ShippingCountryFactory(country_code="US", is_active=True)
    ShippingCountryFactory(country_code="AU", is_active=True)
    ShippingCountryFactory(country_code="GB", is_active=False)  # inactive -> excluded

    ctx = _get_ship_to_context(None)
    codes = {c["code"] for c in ctx["ship_to_countries"]}
    assert codes == {"US", "AU"}
    assert ctx["current_ship_to_code"] is None


# ---------------------------------------------------------------------------
# Listing marking + ship_only toggle
# ---------------------------------------------------------------------------


def _restricted_product_in_home_region():
    """A published, in-stock product allowlisted to a non-home region."""
    home = SalesRegionFactory(name="Home", code="HOME", countries=["US"], priority=10)
    other = SalesRegionFactory(name="Oceania", code="OCE", countries=["AU"], priority=1)
    warehouse = WarehouseFactory(region=home)
    product = ProductFactory(
        track_inventory=True, status="published", region_restriction_mode="only_in"
    )
    StockItemFactory(product=product, warehouse=warehouse, on_hand=5, allocated=0)
    ProductRegionVisibility.objects.create(product=product, region=other)
    return home, product


def test_products_listing_marks_restricted_by_default(client, site_settings):
    home, product = _restricted_product_in_home_region()

    resp = client.get(reverse("page_builder:products"))

    assert resp.status_code == 200
    assert product.id in resp.context["region_restricted_ids"]
    assert resp.context["region_restricted"] is True
    # Shown by default (not filtered out).
    assert product in resp.context["products"]


def test_products_listing_ship_only_hides_restricted(client, site_settings):
    home, product = _restricted_product_in_home_region()

    resp = client.get(reverse("page_builder:products") + "?ship_only=1")

    assert resp.status_code == 200
    assert product not in resp.context["products"]
    assert resp.context["ship_only"] is True


def test_pdp_shows_destination_worded_notice_for_restricted_product(client, site_settings):
    home, product = _restricted_product_in_home_region()

    resp = client.get(reverse("page_builder:product_detail", kwargs={"product_slug": product.slug}))

    assert resp.status_code == 200
    assert resp.context["region_unavailable"] is True
    # Destination-worded, not the old "not available in your region" geo message.
    assert resp.context["ship_destination_name"]  # non-empty region/country name
    content = resp.content.decode()
    assert "doesn't ship to" in content


# ---------------------------------------------------------------------------
# Region confirmation modal — trigger conditions (auto-apply + confirm)
# ---------------------------------------------------------------------------


def _suggestion_request(rf, current_region, session=None, cookies=None):
    request = rf.get("/")
    request.session = session or {}
    request.COOKIES = cookies or {}
    request.sales_region = current_region  # what get_region_from_request returns
    return request


def test_confirm_shows_when_localized_to_nondefault_region(rf):
    # 'default' is the highest-priority region; the visitor was auto-localized to
    # 'other', so we confirm it.
    SalesRegionFactory(name="Home", code="HOME", countries=["US"], priority=100)
    other = SalesRegionFactory(name="Oceania", code="OCE", countries=["AU"], priority=1)
    ShippingCountryFactory(country_code="AU", is_active=True)

    result = region_suggestion(_suggestion_request(rf, other))["region_suggestion"]

    assert result["show"] is True
    assert result["current_region_name"] == "Oceania"
    assert "countries" in result  # feeds the change-country picker


def test_confirm_hidden_when_in_default_region(rf):
    home = SalesRegionFactory(name="Home", code="HOME", countries=["US"], priority=100)
    SalesRegionFactory(name="Oceania", code="OCE", countries=["AU"], priority=1)
    # Auto-localized to the default region -> nothing to confirm.
    assert region_suggestion(_suggestion_request(rf, home))["region_suggestion"]["show"] is False


def test_confirm_hidden_with_only_one_region(rf):
    home = SalesRegionFactory(name="Home", code="HOME", countries=["US"], priority=100)
    assert region_suggestion(_suggestion_request(rf, home))["region_suggestion"]["show"] is False


def test_confirm_hidden_when_already_chosen(rf):
    SalesRegionFactory(name="Home", code="HOME", countries=["US"], priority=100)
    other = SalesRegionFactory(name="Oceania", code="OCE", countries=["AU"], priority=1)
    request = _suggestion_request(rf, other, session={"preferred_region": "OCE"})
    assert region_suggestion(request)["region_suggestion"]["show"] is False


def test_confirm_hidden_when_dismissed(rf):
    SalesRegionFactory(name="Home", code="HOME", countries=["US"], priority=100)
    other = SalesRegionFactory(name="Oceania", code="OCE", countries=["AU"], priority=1)
    request = _suggestion_request(rf, other, cookies={"region_prompt_dismissed": "1"})
    assert region_suggestion(request)["region_suggestion"]["show"] is False


# ---------------------------------------------------------------------------
# Guarded currency coupling on region switch
# ---------------------------------------------------------------------------


def test_currency_switches_with_region_for_multi_currency_store(client, site_settings):
    site_settings.enable_multi_currency = True
    site_settings.supported_currencies = ["USD", "SGD"]
    # skip_validation avoids the exchange-rate-provider prerequisite in
    # SiteSettings.full_clean(), which is unrelated to region currency switching.
    site_settings.save(skip_validation=True)
    cache.clear()

    SalesRegionFactory(name="Singapore", code="SG", countries=["SG"], default_currency="SGD")
    ShippingCountryFactory(country_code="SG", is_active=True)

    resp = client.post(
        reverse("set_region"),
        data=json.dumps({"country": "SG"}),
        content_type="application/json",
    )

    assert resp.status_code == 200
    assert resp.json()["currency"] == "SGD"
    assert client.session["currency"] == "SGD"
    assert resp.cookies["selected_currency"].value == "SGD"


def test_currency_untouched_when_multi_currency_disabled(client, site_settings):
    # Several currencies are listed, but the merchant has NOT enabled
    # multi-currency — the region switch must not silently change currency.
    site_settings.enable_multi_currency = False
    site_settings.supported_currencies = ["USD", "SGD"]
    site_settings.save(skip_validation=True)
    cache.clear()

    SalesRegionFactory(name="Singapore", code="SG", countries=["SG"], default_currency="SGD")
    ShippingCountryFactory(country_code="SG", is_active=True)

    resp = client.post(
        reverse("set_region"),
        data=json.dumps({"country": "SG"}),
        content_type="application/json",
    )

    assert resp.status_code == 200
    assert resp.json()["currency"] is None
    assert "currency" not in client.session
    assert "selected_currency" not in resp.cookies


def test_currency_untouched_for_single_currency_store(client, site_settings):
    site_settings.supported_currencies = ["USD"]  # single-currency merchant
    site_settings.save()
    cache.clear()

    SalesRegionFactory(name="Singapore", code="SG", countries=["SG"], default_currency="SGD")
    ShippingCountryFactory(country_code="SG", is_active=True)

    resp = client.post(
        reverse("set_region"),
        data=json.dumps({"country": "SG"}),
        content_type="application/json",
    )

    assert resp.status_code == 200
    assert resp.json()["currency"] is None
    assert "currency" not in client.session
    assert "selected_currency" not in resp.cookies


# ---------------------------------------------------------------------------
# region_restriction_mode: all / only_in / all_except
# ---------------------------------------------------------------------------


def test_mode_all_is_visible_everywhere():
    home = SalesRegionFactory(name="Home", code="HOME", countries=["US"], priority=10)
    other = SalesRegionFactory(name="Oceania", code="OCE", countries=["AU"], priority=1)
    product = ProductFactory(status="published")  # default mode 'all'

    qs = Product.objects.all()
    assert product in qs.visible_in_region(home)
    assert product in qs.visible_in_region(other)


def test_mode_only_in_is_an_allowlist():
    home = SalesRegionFactory(name="Home", code="HOME", countries=["US"], priority=10)
    other = SalesRegionFactory(name="Oceania", code="OCE", countries=["AU"], priority=1)
    product = ProductFactory(status="published", region_restriction_mode="only_in")
    ProductRegionVisibility.objects.create(product=product, region=other)

    qs = Product.objects.all()
    assert product in qs.visible_in_region(other)  # selected -> visible
    assert product not in qs.visible_in_region(home)  # not selected -> hidden
    assert product.is_visible_in_region(other) is True
    assert product.is_visible_in_region(home) is False


def test_mode_all_except_is_a_blocklist():
    home = SalesRegionFactory(name="Home", code="HOME", countries=["US"], priority=10)
    other = SalesRegionFactory(name="Oceania", code="OCE", countries=["AU"], priority=1)
    product = ProductFactory(status="published", region_restriction_mode="all_except")
    ProductRegionVisibility.objects.create(product=product, region=other)  # excluded here

    qs = Product.objects.all()
    assert product not in qs.visible_in_region(other)  # excluded -> hidden
    assert product in qs.visible_in_region(home)  # elsewhere -> visible
    assert product.is_visible_in_region(other) is False
    assert product.is_visible_in_region(home) is True


# ---------------------------------------------------------------------------
# StockDisplaySettings.region_restricted_action: hide vs show-marked
# ---------------------------------------------------------------------------


def test_listing_hides_restricted_when_action_is_hide(client, site_settings):
    from catalog.models import StockDisplaySettings

    settings = StockDisplaySettings.get_settings()
    settings.region_restricted_action = "hide"
    settings.save()
    cache.clear()

    home, product = _restricted_product_in_home_region()

    resp = client.get(reverse("page_builder:products"))

    assert resp.status_code == 200
    assert product not in resp.context["products"]  # hidden, not marked
    assert resp.context["region_restricted"] is False


def test_listing_marks_restricted_when_action_is_show(client, site_settings):
    from catalog.models import StockDisplaySettings

    settings = StockDisplaySettings.get_settings()
    settings.region_restricted_action = "show_unavailable"
    settings.save()
    cache.clear()

    home, product = _restricted_product_in_home_region()

    resp = client.get(reverse("page_builder:products"))

    assert resp.status_code == 200
    assert product in resp.context["products"]  # shown
    assert product.id in resp.context["region_restricted_ids"]  # marked


# ---------------------------------------------------------------------------
# Headless API parity: /api/store/set-region/ + ships_to_region + region filter
# ---------------------------------------------------------------------------


def test_store_set_region_api_sets_region(client, site_settings):
    SalesRegionFactory(name="Oceania", code="OCE", countries=["AU"], priority=5)
    ShippingCountryFactory(country_code="AU", is_active=True)

    resp = client.post(
        reverse("store-set-region"),
        data=json.dumps({"country": "AU"}),
        content_type="application/json",
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["region"] == "OCE"
    assert client.session["preferred_region"] == "OCE"


def test_store_set_region_api_rejects_non_shippable(client, site_settings):
    SalesRegionFactory(name="Oceania", code="OCE", countries=["AU"], priority=5)
    resp = client.post(
        reverse("store-set-region"),
        data=json.dumps({"country": "AU"}),
        content_type="application/json",
    )
    assert resp.status_code == 400
    assert "preferred_region" not in client.session


def test_ships_to_region_field_reflects_restriction(rf):
    from catalog.serializers import _ships_to_region

    home = SalesRegionFactory(name="Home", code="HOME", countries=["US"], priority=100)
    other = SalesRegionFactory(name="Oceania", code="OCE", countries=["AU"], priority=1)

    restricted = ProductFactory(status="published", region_restriction_mode="only_in")
    ProductRegionVisibility.objects.create(product=restricted, region=other)  # sold only in OCE
    open_product = ProductFactory(status="published")  # mode 'all'

    request = rf.get("/")
    request.sales_region = home  # what get_region_from_request returns
    assert _ships_to_region(restricted, request) is False  # not sold in HOME
    assert _ships_to_region(open_product, request) is True


def test_region_filtered_products_shows_or_hides_by_setting(rf):
    from catalog.api_views import region_filtered_products
    from catalog.models import StockDisplaySettings

    home = SalesRegionFactory(name="Home", code="HOME", countries=["US"], priority=100)
    other = SalesRegionFactory(name="Oceania", code="OCE", countries=["AU"], priority=1)
    wh = WarehouseFactory(name="Home WH", code="HOME-WH", region=home)

    restricted = ProductFactory(status="published", region_restriction_mode="only_in")
    StockItemFactory(product=restricted, warehouse=wh, on_hand=5, allocated=0)
    ProductRegionVisibility.objects.create(product=restricted, region=other)

    settings = StockDisplaySettings.get_settings()

    # show_unavailable -> restricted product stays in the list (client marks it)
    settings.region_restricted_action = "show_unavailable"
    settings.save()
    cache.clear()
    shown = region_filtered_products(Product.objects.all(), home, rf.get("/"))
    assert restricted in shown

    # ?ship_only=1 hides it
    hidden = region_filtered_products(Product.objects.all(), home, rf.get("/?ship_only=1"))
    assert restricted not in hidden

    # hide setting hides it too
    settings.region_restricted_action = "hide"
    settings.save()
    cache.clear()
    assert restricted not in region_filtered_products(Product.objects.all(), home, rf.get("/"))
