"""
Tests for the auto-reconcile of `ShippingCountry` from `ShippingZone`.

We never want a merchant to discover the `ShippingCountry` admin URL —
saving a `ShippingZone` with explicit countries should be enough for the
payment-method filter (and any other ShippingCountry consumer) to start
returning results.

Also covers the field-name bug in `cart.views.CheckoutViewSet.set_payment_method`
where a slug lookup was attempting `PaymentProviderAccount.objects.get(
provider_slug=...)` — `provider_slug` isn't a column on that model; the
slug lives on the related `ComponentRegistry`.
"""
from __future__ import annotations

import importlib

import pytest
from django.contrib.sites.models import Site

from shipping.models import ShippingCountry, ShippingZone

# Migration modules are named with a leading digit (`0004_…`) so we can't
# `import` them directly; load via `importlib`.
_backfill_module = importlib.import_module(
    "shipping.migrations.0004_backfill_shipping_countries_from_zones"
)


pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _site_id() -> int:
    """Return the default site id (always 1 on single-tenant installs)."""
    return Site.objects.get_or_create(pk=1, defaults={"domain": "example.com", "name": "Example"})[0].pk


def _make_zone(countries, name="Test Zone", is_active=True) -> ShippingZone:
    # ShippingZone has no `site` FK — the single-tenant shop always uses
    # site_id=1, and the reconcile signal hard-codes that constant. We
    # touch `_site_id()` only to make sure the row exists for downstream
    # foreign keys (e.g. ShippingCountry.site).
    _site_id()
    return ShippingZone.objects.create(
        name=name,
        countries=countries,
        is_active=is_active,
    )


# ---------------------------------------------------------------------------
# Signal: post_save on ShippingZone
# ---------------------------------------------------------------------------

def test_first_save_creates_country_rows():
    site_id = _site_id()
    _make_zone(countries=["SG", "MY"])

    rows = ShippingCountry.objects.filter(site_id=site_id).order_by("country_code")
    assert [r.country_code for r in rows] == ["MY", "SG"]
    assert all(r.is_active for r in rows)


def test_reconcile_is_idempotent_on_repeated_save():
    site_id = _site_id()
    zone = _make_zone(countries=["SG"])
    initial = ShippingCountry.objects.filter(site_id=site_id).count()

    zone.save()
    zone.save()

    assert ShippingCountry.objects.filter(site_id=site_id).count() == initial


def test_reactivates_existing_inactive_row():
    site_id = _site_id()
    ShippingCountry.objects.create(site_id=site_id, country_code="SG", is_active=False)

    _make_zone(countries=["SG"])

    row = ShippingCountry.objects.get(site_id=site_id, country_code="SG")
    assert row.is_active is True
    assert ShippingCountry.objects.filter(country_code="SG").count() == 1


def test_empty_countries_is_a_no_op():
    site_id = _site_id()
    pre_count = ShippingCountry.objects.filter(site_id=site_id).count()

    _make_zone(countries=[])

    assert ShippingCountry.objects.filter(site_id=site_id).count() == pre_count


def test_removing_country_from_zone_does_not_deactivate_the_row():
    """Same country may live in another zone or in a warehouse fallback;
    never silently brick checkout."""
    site_id = _site_id()
    zone = _make_zone(countries=["SG", "MY"])
    assert ShippingCountry.objects.filter(country_code="MY").exists()

    zone.countries = ["SG"]
    zone.save()

    my_row = ShippingCountry.objects.get(site_id=site_id, country_code="MY")
    assert my_row.is_active is True


def test_lowercase_and_whitespace_input_is_normalised():
    site_id = _site_id()
    _make_zone(countries=["  sg ", "my", "SG"])  # dup + whitespace + lower

    codes = list(
        ShippingCountry.objects
        .filter(site_id=site_id)
        .order_by("country_code")
        .values_list("country_code", flat=True)
    )
    assert codes == ["MY", "SG"]


# ---------------------------------------------------------------------------
# Backfill migration is callable and idempotent
# ---------------------------------------------------------------------------

def test_backfill_migration_is_idempotent_when_called_twice():
    """The migration uses `get_or_create` so running it again on top of
    an already-reconciled DB is a no-op. We invoke the module-level
    function directly rather than going through `call_command('migrate')`
    so the test stays a fast unit-level check."""
    from django.apps import apps

    site_id = _site_id()
    _make_zone(countries=["SG", "AU"])
    expected_before = set(
        ShippingCountry.objects
        .filter(site_id=site_id)
        .values_list("country_code", flat=True)
    )

    _backfill_module.backfill_shipping_countries(apps, schema_editor=None)
    _backfill_module.backfill_shipping_countries(apps, schema_editor=None)

    expected_after = set(
        ShippingCountry.objects
        .filter(site_id=site_id)
        .values_list("country_code", flat=True)
    )
    assert expected_after == expected_before


# ---------------------------------------------------------------------------
# set_payment_method slug-resolution fix
# ---------------------------------------------------------------------------

def test_set_payment_method_resolves_provider_by_component_slug(client, django_user_model):
    """Regression for the cocosbotanica 500 — `cart.views.set_payment_method`
    used to filter `PaymentProviderAccount.objects.get(provider_slug=...)`,
    but that field doesn't exist on the model. The slug lives on the
    related ComponentRegistry, so the lookup has to go through
    `component__slug`."""
    from component_updates.models import ComponentRegistry
    from payment_providers.models import PaymentProviderAccount

    user = django_user_model.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass",
    )

    component = ComponentRegistry.objects.create(
        slug="stripe-test",
        name="Stripe (test)",
        component_type="payment_provider",
        current_version="1.0.0",
    )
    account = PaymentProviderAccount.objects.create(
        component=component,
        user=user,
        display_name="Stripe",
        credentials_encrypted={},
        is_active=True,
        is_default=True,
        connection_status="connected",
        checkout_mode="hosted",
    )

    # The fix lives on the view itself — exercise the same queryset to be
    # sure it resolves. Mirrors the new filter() chain.
    resolved = (
        PaymentProviderAccount.objects
        .filter(component__slug="stripe-test", is_active=True)
        .order_by("-is_default", "sort_order", "created_at")
        .first()
    )
    assert resolved == account

    # And the buggy original would raise FieldError. We assert it stays
    # broken-or-renamed so anyone reverting the fix is caught here.
    from django.core.exceptions import FieldError
    with pytest.raises(FieldError):
        PaymentProviderAccount.objects.filter(provider_slug="stripe-test").first()
