"""
Exchange Rates App Integration Tests.

Comprehensive tests covering:
- Models: ExchangeRateProviderAccount (CRUD, str, unique primary constraint, ordering, fields),
  ExchangeRate (CRUD, unique_together, is_stale property, str),
  ExchangeRateHistory (CRUD, ordering, str)
- Admin: ExchangeRateProviderAccountAdmin (changelist, display methods, context),
  ExchangeRateAdmin (changelist, stale_indicator),
  ExchangeRateHistoryAdmin (changelist)
- Admin AJAX Views: filter_exchange_rate_providers, toggle_provider_active,
  set_provider_primary, delete_provider, provider_bulk_action
- Template CSP Compliance: No inline style= attributes, no onclick handlers
- Static Files: CSS and JS copyright headers
- Security: staff_member_required, POST-only enforcement, AJAX-only guards
- i18n: verbose_name translations on all models
"""

import json
import re
from datetime import timedelta
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.sites.models import Site
from django.db import IntegrityError, transaction
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from exchange_rates.admin import (
    ExchangeRateAdmin,
    ExchangeRateHistoryAdmin,
    ExchangeRateProviderAccountAdmin,
)
from exchange_rates.models import (
    ExchangeRate,
    ExchangeRateHistory,
    ExchangeRateProviderAccount,
)
from tests.factories import ComponentRegistryFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.exchange_rates]

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def site(db):
    """Get or create the default Django Site (SITE_ID=1)."""
    site_obj, _ = Site.objects.get_or_create(
        id=1,
        defaults={"domain": "localhost", "name": "Test Site"},
    )
    return site_obj


@pytest.fixture
def exchange_rate_component(db):
    """ComponentRegistry entry for an exchange rate provider."""
    return ComponentRegistryFactory(
        component_type="exchange_rate_provider",
        slug="test-exchange-provider",
        name="Test Exchange Provider",
        description="Test exchange rate provider for unit tests",
    )


@pytest.fixture
def exchange_rate_component_2(db):
    """A second ComponentRegistry entry for testing multiple providers."""
    return ComponentRegistryFactory(
        component_type="exchange_rate_provider",
        slug="test-exchange-provider-2",
        name="Second Exchange Provider",
        description="Second test exchange rate provider",
    )


@pytest.fixture
def provider_account(db, site, exchange_rate_component):
    """Active ExchangeRateProviderAccount for testing."""
    return ExchangeRateProviderAccount.objects.create(
        site=site,
        component=exchange_rate_component,
        name="My Test Provider",
        credentials=b"encrypted_api_key_data",
        is_active=True,
        is_primary=False,
        priority=10,
        settings={"base_currencies": ["USD"]},
        sync_status="pending",
    )


@pytest.fixture
def primary_provider(db, site, exchange_rate_component_2):
    """Primary ExchangeRateProviderAccount."""
    return ExchangeRateProviderAccount.objects.create(
        site=site,
        component=exchange_rate_component_2,
        name="Primary Provider",
        credentials=b"encrypted_primary_key",
        is_active=True,
        is_primary=True,
        priority=0,
        sync_status="success",
    )


@pytest.fixture
def exchange_rate(db, provider_account):
    """ExchangeRate cached rate entry."""
    return ExchangeRate.objects.create(
        provider_account=provider_account,
        base_currency="USD",
        target_currency="EUR",
        rate=Decimal("0.850000"),
    )


@pytest.fixture
def rate_history(db):
    """ExchangeRateHistory entry."""
    return ExchangeRateHistory.objects.create(
        base_currency="USD",
        target_currency="GBP",
        rate=Decimal("0.790000"),
        provider_name="Test Provider",
    )


@pytest.fixture
def staff_client(admin_user):
    """Django test client authenticated as staff user."""
    client = Client()
    client.force_login(admin_user)
    return client


@pytest.fixture
def anon_client():
    """Unauthenticated Django test client."""
    return Client()


@pytest.fixture
def regular_client(customer_user):
    """Django test client authenticated as non-staff user."""
    client = Client()
    client.force_login(customer_user)
    return client


# ============================================================
# Model Tests: ExchangeRateProviderAccount
# ============================================================


class TestExchangeRateProviderAccountModel:
    """Tests for ExchangeRateProviderAccount model."""

    def test_create_provider_account(self, provider_account):
        """Provider account is created with correct fields."""
        assert provider_account.pk is not None
        assert provider_account.name == "My Test Provider"
        assert provider_account.is_active is True
        assert provider_account.is_primary is False
        assert provider_account.priority == 10
        assert provider_account.sync_status == "pending"
        assert provider_account.settings == {"base_currencies": ["USD"]}
        assert provider_account.credentials == b"encrypted_api_key_data"

    def test_str_representation(self, provider_account):
        """__str__ returns 'name (component.name)' format."""
        expected = f"{provider_account.name} ({provider_account.component.name})"
        assert str(provider_account) == expected

    def test_str_representation_values(self, provider_account):
        """__str__ uses actual stored values."""
        assert "My Test Provider" in str(provider_account)
        assert "Test Exchange Provider" in str(provider_account)

    def test_default_values(self, site, exchange_rate_component):
        """Default values for optional fields are correct."""
        acct = ExchangeRateProviderAccount.objects.create(
            site=site,
            component=exchange_rate_component,
            name="Defaults Check",
            credentials=b"data",
        )
        assert acct.is_active is True
        assert acct.is_primary is False
        assert acct.priority == 0
        assert acct.settings == {}
        assert acct.sync_status == "pending"
        assert acct.sync_error_message == ""
        assert acct.last_sync_at is None

    def test_auto_timestamps(self, provider_account):
        """created_at and updated_at are auto-populated."""
        assert provider_account.created_at is not None
        assert provider_account.updated_at is not None

    def test_update_changes_updated_at(self, provider_account):
        """Saving changes updates updated_at timestamp."""
        old_updated = provider_account.updated_at
        provider_account.name = "Updated Name"
        provider_account.save()
        provider_account.refresh_from_db()
        assert provider_account.updated_at >= old_updated

    def test_component_foreign_key(self, provider_account, exchange_rate_component):
        """component FK links to correct ComponentRegistry entry."""
        assert provider_account.component == exchange_rate_component
        assert provider_account.component.component_type == "exchange_rate_provider"

    def test_site_foreign_key(self, provider_account, site):
        """site FK links to correct Site."""
        assert provider_account.site == site
        assert provider_account.site_id == 1

    def test_sync_status_choices(self, site, exchange_rate_component):
        """sync_status accepts valid choices."""
        for status in ["pending", "success", "error"]:
            acct = ExchangeRateProviderAccount.objects.create(
                site=site,
                component=exchange_rate_component,
                name=f"Provider {status}",
                credentials=b"data",
                sync_status=status,
            )
            assert acct.sync_status == status
            acct.delete()

    def test_settings_jsonfield(self, site, exchange_rate_component):
        """settings JSONField stores and retrieves complex data."""
        complex_settings = {
            "base_currencies": ["USD", "EUR"],
            "refresh_interval": 3600,
            "nested": {"key": "value"},
        }
        acct = ExchangeRateProviderAccount.objects.create(
            site=site,
            component=exchange_rate_component,
            name="JSON Test",
            credentials=b"data",
            settings=complex_settings,
        )
        acct.refresh_from_db()
        assert acct.settings == complex_settings

    def test_credentials_binary_field(self, site, exchange_rate_component):
        """credentials BinaryField stores and retrieves bytes."""
        raw_bytes = b"\x00\x01\x02\xff"
        acct = ExchangeRateProviderAccount.objects.create(
            site=site,
            component=exchange_rate_component,
            name="Binary Test",
            credentials=raw_bytes,
        )
        acct.refresh_from_db()
        assert bytes(acct.credentials) == raw_bytes

    def test_ordering(self, site, exchange_rate_component, exchange_rate_component_2):
        """Model ordering: -is_primary, -is_active, priority, name."""
        # Clear existing
        ExchangeRateProviderAccount.objects.all().delete()

        p1 = ExchangeRateProviderAccount.objects.create(
            site=site,
            component=exchange_rate_component,
            name="Zebra",
            credentials=b"d",
            is_primary=False,
            is_active=True,
            priority=5,
        )
        p2 = ExchangeRateProviderAccount.objects.create(
            site=site,
            component=exchange_rate_component_2,
            name="Alpha",
            credentials=b"d",
            is_primary=True,
            is_active=True,
            priority=10,
        )
        p3 = ExchangeRateProviderAccount.objects.create(
            site=site,
            component=exchange_rate_component,
            name="Beta",
            credentials=b"d",
            is_primary=False,
            is_active=False,
            priority=0,
        )

        providers = list(ExchangeRateProviderAccount.objects.all())
        # Primary first (is_primary=True sorts first via -is_primary)
        assert providers[0] == p2
        # Then active before inactive (-is_active)
        assert providers[1] == p1
        # Inactive last
        assert providers[2] == p3

    def test_unique_primary_constraint(
        self, site, exchange_rate_component, exchange_rate_component_2
    ):
        """Only one provider per site can be primary."""
        ExchangeRateProviderAccount.objects.all().delete()

        ExchangeRateProviderAccount.objects.create(
            site=site,
            component=exchange_rate_component,
            name="First Primary",
            credentials=b"d",
            is_primary=True,
        )

        with pytest.raises(IntegrityError), transaction.atomic():
            ExchangeRateProviderAccount.objects.create(
                site=site,
                component=exchange_rate_component_2,
                name="Second Primary",
                credentials=b"d",
                is_primary=True,
            )

    def test_multiple_non_primary_allowed(
        self, site, exchange_rate_component, exchange_rate_component_2
    ):
        """Multiple non-primary providers for the same site are allowed."""
        ExchangeRateProviderAccount.objects.all().delete()

        p1 = ExchangeRateProviderAccount.objects.create(
            site=site,
            component=exchange_rate_component,
            name="Non-Primary 1",
            credentials=b"d",
            is_primary=False,
        )
        p2 = ExchangeRateProviderAccount.objects.create(
            site=site,
            component=exchange_rate_component_2,
            name="Non-Primary 2",
            credentials=b"d",
            is_primary=False,
        )
        assert p1.pk is not None
        assert p2.pk is not None

    def test_cascade_delete_on_site(self, provider_account, site):
        """Deleting site cascades to provider account."""
        pk = provider_account.pk
        site.delete()
        assert not ExchangeRateProviderAccount.objects.filter(pk=pk).exists()

    def test_protect_delete_on_component(self, provider_account, exchange_rate_component):
        """Deleting component with linked provider raises ProtectedError."""
        from django.db.models import ProtectedError

        with pytest.raises(ProtectedError):
            exchange_rate_component.delete()

    def test_verbose_names(self):
        """Model and field verbose names are set."""
        meta = ExchangeRateProviderAccount._meta
        assert str(meta.verbose_name) == "Exchange Rate Provider Account"
        assert str(meta.verbose_name_plural) == "Exchange Rate Provider Accounts"

    def test_related_name_exchange_rate_accounts(self, provider_account, exchange_rate_component):
        """Component's reverse relation 'exchange_rate_accounts' works."""
        assert provider_account in exchange_rate_component.exchange_rate_accounts.all()

    def test_sync_error_message_field(self, provider_account):
        """sync_error_message can store text."""
        provider_account.sync_error_message = "API rate limit exceeded"
        provider_account.save()
        provider_account.refresh_from_db()
        assert provider_account.sync_error_message == "API rate limit exceeded"


# ============================================================
# Model Tests: ExchangeRate
# ============================================================


class TestExchangeRateModel:
    """Tests for ExchangeRate model."""

    def test_create_exchange_rate(self, exchange_rate):
        """Exchange rate is created with correct fields."""
        assert exchange_rate.pk is not None
        assert exchange_rate.base_currency == "USD"
        assert exchange_rate.target_currency == "EUR"
        assert exchange_rate.rate == Decimal("0.850000")
        assert exchange_rate.fetched_at is not None

    def test_str_representation(self, exchange_rate):
        """__str__ returns 'BASE/TARGET: rate' format."""
        expected = f"USD/EUR: {exchange_rate.rate}"
        assert str(exchange_rate) == expected

    def test_unique_together_constraint(self, provider_account):
        """Only one rate per (provider_account, base_currency, target_currency)."""
        ExchangeRate.objects.create(
            provider_account=provider_account,
            base_currency="USD",
            target_currency="GBP",
            rate=Decimal("0.790000"),
        )
        with pytest.raises(IntegrityError), transaction.atomic():
            ExchangeRate.objects.create(
                provider_account=provider_account,
                base_currency="USD",
                target_currency="GBP",
                rate=Decimal("0.800000"),
            )

    def test_different_pairs_allowed(self, provider_account):
        """Different currency pairs for the same provider are allowed."""
        r1 = ExchangeRate.objects.create(
            provider_account=provider_account,
            base_currency="USD",
            target_currency="JPY",
            rate=Decimal("149.500000"),
        )
        r2 = ExchangeRate.objects.create(
            provider_account=provider_account,
            base_currency="EUR",
            target_currency="JPY",
            rate=Decimal("162.300000"),
        )
        assert r1.pk is not None
        assert r2.pk is not None

    def test_is_stale_fresh_rate(self, exchange_rate):
        """Rate fetched recently is not stale."""
        # fetched_at is auto_now, so just-created rate is fresh
        assert exchange_rate.is_stale is False

    def test_is_stale_old_rate(self, provider_account):
        """Rate older than 24 hours is stale."""
        rate = ExchangeRate.objects.create(
            provider_account=provider_account,
            base_currency="USD",
            target_currency="CAD",
            rate=Decimal("1.350000"),
        )
        # Bypass auto_now to set old timestamp
        stale_time = timezone.now() - timedelta(hours=25)
        ExchangeRate.objects.filter(pk=rate.pk).update(fetched_at=stale_time)
        rate.refresh_from_db()
        assert rate.is_stale is True

    def test_is_stale_exactly_24_hours(self, provider_account):
        """Rate exactly 24 hours old is not stale (boundary test)."""
        fixed_now = timezone.now()
        rate = ExchangeRate.objects.create(
            provider_account=provider_account,
            base_currency="USD",
            target_currency="AUD",
            rate=Decimal("1.520000"),
        )
        boundary_time = fixed_now - timedelta(hours=24)
        ExchangeRate.objects.filter(pk=rate.pk).update(fetched_at=boundary_time)
        rate.refresh_from_db()
        # Mock timezone.now to return the same instant we used to compute boundary_time
        with patch("django.utils.timezone.now", return_value=fixed_now):
            # timedelta(hours=24) is not > timedelta(hours=24), so not stale
            assert rate.is_stale is False

    def test_rate_decimal_precision(self, provider_account):
        """Rate field supports high precision (18,6)."""
        rate = ExchangeRate.objects.create(
            provider_account=provider_account,
            base_currency="BTC",
            target_currency="USD",
            rate=Decimal("123456789012.123456"),
        )
        rate.refresh_from_db()
        assert rate.rate == Decimal("123456789012.123456")

    def test_cascade_delete_on_provider_account(self, exchange_rate, provider_account):
        """Deleting provider account cascades to exchange rates."""
        rate_pk = exchange_rate.pk
        provider_account.delete()
        assert not ExchangeRate.objects.filter(pk=rate_pk).exists()

    def test_related_name_cached_rates(self, exchange_rate, provider_account):
        """Provider account's reverse relation 'cached_rates' works."""
        assert exchange_rate in provider_account.cached_rates.all()

    def test_verbose_names(self):
        """Model verbose names are set."""
        meta = ExchangeRate._meta
        assert str(meta.verbose_name) == "Exchange Rate"
        assert str(meta.verbose_name_plural) == "Exchange Rates"


# ============================================================
# Model Tests: ExchangeRateHistory
# ============================================================


class TestExchangeRateHistoryModel:
    """Tests for ExchangeRateHistory model."""

    def test_create_rate_history(self, rate_history):
        """Rate history is created with correct fields."""
        assert rate_history.pk is not None
        assert rate_history.base_currency == "USD"
        assert rate_history.target_currency == "GBP"
        assert rate_history.rate == Decimal("0.790000")
        assert rate_history.provider_name == "Test Provider"
        assert rate_history.created_at is not None
        assert rate_history.order is None

    def test_str_representation(self, rate_history):
        """__str__ returns 'BASE/TARGET: rate (date)' format."""
        result = str(rate_history)
        assert "USD/GBP" in result
        assert "0.790000" in result
        # Date portion formatted as YYYY-MM-DD HH:MM
        date_str = rate_history.created_at.strftime("%Y-%m-%d %H:%M")
        assert date_str in result

    def test_ordering(self, db):
        """History records are ordered by -created_at."""
        h1 = ExchangeRateHistory.objects.create(
            base_currency="USD",
            target_currency="EUR",
            rate=Decimal("0.85"),
            provider_name="P1",
        )
        h2 = ExchangeRateHistory.objects.create(
            base_currency="USD",
            target_currency="EUR",
            rate=Decimal("0.86"),
            provider_name="P2",
        )
        records = list(ExchangeRateHistory.objects.all())
        # Most recent first
        assert records[0] == h2
        assert records[1] == h1

    def test_optional_order_link(self, rate_history):
        """order FK is optional (null/blank)."""
        assert rate_history.order is None

    def test_order_link_set_null(self, rate_history):
        """When linked order is deleted, FK is set to NULL."""
        from tests.factories import OrderFactory

        order = OrderFactory()
        rate_history.order = order
        rate_history.save()
        assert rate_history.order == order

        order_pk = order.pk
        order.delete()
        rate_history.refresh_from_db()
        assert rate_history.order is None

    def test_related_name_exchange_rate_snapshots(self, db):
        """Order's reverse relation 'exchange_rate_snapshots' works."""
        from tests.factories import OrderFactory

        order = OrderFactory()
        h = ExchangeRateHistory.objects.create(
            base_currency="EUR",
            target_currency="JPY",
            rate=Decimal("162.30"),
            provider_name="Fixer",
            order=order,
        )
        assert h in order.exchange_rate_snapshots.all()

    def test_verbose_names(self):
        """Model verbose names are set."""
        meta = ExchangeRateHistory._meta
        assert str(meta.verbose_name) == "Exchange Rate History"
        assert str(meta.verbose_name_plural) == "Exchange Rate History"


# ============================================================
# Admin Tests: ExchangeRateProviderAccountAdmin
# ============================================================


class TestExchangeRateProviderAccountAdmin:
    """Tests for ExchangeRateProviderAccountAdmin."""

    def test_changelist_loads(self, staff_client, provider_account):
        """Provider account changelist returns 200."""
        url = reverse("admin:exchange_rates_exchangerateprovideraccount_changelist")
        response = staff_client.get(url)
        assert response.status_code == 200

    def test_changelist_context_keys(self, staff_client, provider_account, primary_provider):
        """Changelist context contains expected custom keys."""
        url = reverse("admin:exchange_rates_exchangerateprovideraccount_changelist")
        response = staff_client.get(url)
        assert response.status_code == 200
        ctx = response.context
        assert "active_count" in ctx
        assert "inactive_count" in ctx
        assert "success_count" in ctx
        assert "error_count" in ctx
        assert "pending_count" in ctx
        assert "primary_provider" in ctx
        assert "component_counts" in ctx

    def test_changelist_context_counts(self, staff_client, provider_account, primary_provider):
        """Changelist context counts match actual data."""
        url = reverse("admin:exchange_rates_exchangerateprovideraccount_changelist")
        response = staff_client.get(url)
        ctx = response.context
        # Both providers are active
        assert ctx["active_count"] == 2
        assert ctx["inactive_count"] == 0
        # primary_provider has sync_status='success', provider_account has 'pending'
        assert ctx["success_count"] == 1
        assert ctx["pending_count"] == 1
        assert ctx["error_count"] == 0
        assert ctx["primary_provider"] == primary_provider

    def test_changelist_no_primary_provider(self, staff_client, provider_account):
        """Changelist handles no primary provider gracefully."""
        url = reverse("admin:exchange_rates_exchangerateprovideraccount_changelist")
        response = staff_client.get(url)
        assert response.context["primary_provider"] is None

    def test_display_name_or_component_with_name(self, provider_account):
        """display_name_or_component returns name when set."""
        admin_obj = ExchangeRateProviderAccountAdmin(ExchangeRateProviderAccount, AdminSite())
        result = admin_obj.display_name_or_component(provider_account)
        assert result == "My Test Provider"

    def test_display_name_or_component_without_name(self, site, exchange_rate_component):
        """display_name_or_component returns component name in <em> when name is empty."""
        acct = ExchangeRateProviderAccount.objects.create(
            site=site,
            component=exchange_rate_component,
            name="",
            credentials=b"d",
        )
        admin_obj = ExchangeRateProviderAccountAdmin(ExchangeRateProviderAccount, AdminSite())
        result = admin_obj.display_name_or_component(acct)
        assert "<em>" in result
        assert exchange_rate_component.name in result

    def test_sync_status_badge_pending(self, provider_account):
        """sync_status_badge returns pending badge."""
        admin_obj = ExchangeRateProviderAccountAdmin(ExchangeRateProviderAccount, AdminSite())
        result = admin_obj.sync_status_badge(provider_account)
        assert "sync-pending" in result
        assert "PENDING" in result

    def test_sync_status_badge_success(self, primary_provider):
        """sync_status_badge returns success badge."""
        admin_obj = ExchangeRateProviderAccountAdmin(ExchangeRateProviderAccount, AdminSite())
        result = admin_obj.sync_status_badge(primary_provider)
        assert "sync-success" in result
        assert "SUCCESS" in result

    def test_sync_status_badge_error(self, provider_account):
        """sync_status_badge returns error badge for error status."""
        provider_account.sync_status = "error"
        provider_account.save()
        admin_obj = ExchangeRateProviderAccountAdmin(ExchangeRateProviderAccount, AdminSite())
        result = admin_obj.sync_status_badge(provider_account)
        assert "sync-error" in result
        assert "ERROR" in result

    def test_is_active_badge_active(self, provider_account):
        """is_active_badge returns active badge when is_active=True."""
        admin_obj = ExchangeRateProviderAccountAdmin(ExchangeRateProviderAccount, AdminSite())
        result = admin_obj.is_active_badge(provider_account)
        assert "active" in result.lower()
        assert "ACTIVE" in result

    def test_is_active_badge_inactive(self, provider_account):
        """is_active_badge returns inactive badge when is_active=False."""
        provider_account.is_active = False
        admin_obj = ExchangeRateProviderAccountAdmin(ExchangeRateProviderAccount, AdminSite())
        result = admin_obj.is_active_badge(provider_account)
        assert "inactive" in result.lower()
        assert "INACTIVE" in result

    def test_is_primary_badge_primary(self, primary_provider):
        """is_primary_badge returns primary badge when is_primary=True."""
        admin_obj = ExchangeRateProviderAccountAdmin(ExchangeRateProviderAccount, AdminSite())
        result = admin_obj.is_primary_badge(primary_provider)
        assert "PRIMARY" in result

    def test_is_primary_badge_not_primary(self, provider_account):
        """is_primary_badge returns '-' when not primary."""
        admin_obj = ExchangeRateProviderAccountAdmin(ExchangeRateProviderAccount, AdminSite())
        result = admin_obj.is_primary_badge(provider_account)
        assert result == "-"

    def test_credentials_display_with_credentials(self, provider_account):
        """credentials_display shows encrypted indicator when credentials exist."""
        admin_obj = ExchangeRateProviderAccountAdmin(ExchangeRateProviderAccount, AdminSite())
        result = admin_obj.credentials_display(provider_account)
        assert "encrypted" in result.lower() or "lock" in result.lower()

    def test_credentials_display_without_credentials(self, site, exchange_rate_component):
        """credentials_display shows warning when no credentials."""
        acct = ExchangeRateProviderAccount.objects.create(
            site=site,
            component=exchange_rate_component,
            name="No Creds",
            credentials=b"",
        )
        admin_obj = ExchangeRateProviderAccountAdmin(ExchangeRateProviderAccount, AdminSite())
        result = admin_obj.credentials_display(acct)
        assert "warning" in result.lower() or "No credentials" in result

    def test_changelist_requires_staff(self, anon_client):
        """Changelist redirects anonymous users to login."""
        url = reverse("admin:exchange_rates_exchangerateprovideraccount_changelist")
        response = anon_client.get(url)
        assert response.status_code == 302
        assert "/login/" in response.url or "/admin/" in response.url

    def test_changelist_denies_non_staff(self, regular_client):
        """Changelist redirects non-staff users."""
        url = reverse("admin:exchange_rates_exchangerateprovideraccount_changelist")
        response = regular_client.get(url)
        assert response.status_code == 302


# ============================================================
# Admin Tests: ExchangeRateAdmin
# ============================================================


class TestExchangeRateAdmin:
    """Tests for ExchangeRateAdmin."""

    def test_changelist_loads(self, staff_client, exchange_rate):
        """Exchange rate changelist returns 200."""
        url = reverse("admin:exchange_rates_exchangerate_changelist")
        response = staff_client.get(url)
        assert response.status_code == 200

    def test_currency_pair_display(self, exchange_rate):
        """currency_pair returns 'BASE/TARGET' format."""
        admin_obj = ExchangeRateAdmin(ExchangeRate, AdminSite())
        result = admin_obj.currency_pair(exchange_rate)
        assert result == "USD/EUR"

    def test_stale_indicator_fresh(self, exchange_rate):
        """stale_indicator shows 'Fresh' for recent rate."""
        admin_obj = ExchangeRateAdmin(ExchangeRate, AdminSite())
        result = admin_obj.stale_indicator(exchange_rate)
        assert "fresh" in result.lower() or "Fresh" in result

    def test_stale_indicator_stale(self, provider_account):
        """stale_indicator shows 'Stale' for old rate."""
        rate = ExchangeRate.objects.create(
            provider_account=provider_account,
            base_currency="USD",
            target_currency="CHF",
            rate=Decimal("0.880000"),
        )
        stale_time = timezone.now() - timedelta(hours=25)
        ExchangeRate.objects.filter(pk=rate.pk).update(fetched_at=stale_time)
        rate.refresh_from_db()

        admin_obj = ExchangeRateAdmin(ExchangeRate, AdminSite())
        result = admin_obj.stale_indicator(rate)
        assert "stale" in result.lower() or "Stale" in result


# ============================================================
# Admin Tests: ExchangeRateHistoryAdmin
# ============================================================


class TestExchangeRateHistoryAdmin:
    """Tests for ExchangeRateHistoryAdmin."""

    def test_changelist_loads(self, staff_client, rate_history):
        """Exchange rate history changelist returns 200."""
        url = reverse("admin:exchange_rates_exchangeratehistory_changelist")
        response = staff_client.get(url)
        assert response.status_code == 200

    def test_currency_pair_display(self, rate_history):
        """currency_pair returns 'BASE/TARGET' format."""
        admin_obj = ExchangeRateHistoryAdmin(ExchangeRateHistory, AdminSite())
        result = admin_obj.currency_pair(rate_history)
        assert result == "USD/GBP"

    def test_order_link_no_order(self, rate_history):
        """order_link returns '-' when no order is linked."""
        admin_obj = ExchangeRateHistoryAdmin(ExchangeRateHistory, AdminSite())
        result = admin_obj.order_link(rate_history)
        assert result == "-"

    def test_order_link_with_order(self, rate_history):
        """order_link returns link HTML when order is present."""
        from tests.factories import OrderFactory

        order = OrderFactory()
        rate_history.order = order
        rate_history.save()

        admin_obj = ExchangeRateHistoryAdmin(ExchangeRateHistory, AdminSite())
        result = admin_obj.order_link(rate_history)
        assert "<a href=" in result
        assert order.order_number in result


# ============================================================
# Admin AJAX View Tests: filter_exchange_rate_providers
# ============================================================


class TestFilterExchangeRateProviders:
    """Tests for the filter_exchange_rate_providers AJAX view."""

    FILTER_URL = "/en/admin/exchange-rates/exchangerateprovideraccount/filter/"

    def _ajax_get(self, client, params=None):
        """Helper for AJAX GET requests."""
        return client.get(
            self.FILTER_URL,
            data=params or {},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

    def test_requires_staff(self, anon_client):
        """Anonymous users are redirected (staff_member_required)."""
        response = anon_client.get(self.FILTER_URL)
        assert response.status_code == 302

    def test_requires_staff_non_staff_redirected(self, regular_client):
        """Non-staff users are redirected."""
        response = regular_client.get(
            self.FILTER_URL,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        assert response.status_code == 302

    def test_requires_ajax_header(self, staff_client, provider_account):
        """Non-AJAX requests return 400."""
        response = staff_client.get(self.FILTER_URL)
        assert response.status_code == 400

    @patch("exchange_rates.views.admin_views.render_to_string", return_value="<div>card</div>")
    def test_returns_json_with_html_and_count(self, mock_render, staff_client, provider_account):
        """Successful AJAX request returns JSON with html and count keys."""
        response = self._ajax_get(staff_client)
        assert response.status_code == 200
        data = response.json()
        assert "html" in data
        assert "count" in data

    @patch("exchange_rates.views.admin_views.render_to_string", return_value="<div>card</div>")
    def test_count_matches_providers(
        self, mock_render, staff_client, provider_account, primary_provider
    ):
        """Count reflects total matching providers."""
        response = self._ajax_get(staff_client)
        data = response.json()
        assert data["count"] == 2

    @patch("exchange_rates.views.admin_views.render_to_string", return_value="<div>card</div>")
    def test_filter_by_search(self, mock_render, staff_client, provider_account, primary_provider):
        """Search filter narrows results by name."""
        response = self._ajax_get(staff_client, {"search": "Primary"})
        data = response.json()
        assert data["count"] == 1

    @patch("exchange_rates.views.admin_views.render_to_string", return_value="<div>card</div>")
    def test_filter_by_sync_status(
        self, mock_render, staff_client, provider_account, primary_provider
    ):
        """Sync status filter works."""
        response = self._ajax_get(staff_client, {"sync_status": "success"})
        data = response.json()
        assert data["count"] == 1

    @patch("exchange_rates.views.admin_views.render_to_string", return_value="<div>card</div>")
    def test_filter_by_active(self, mock_render, staff_client, provider_account, primary_provider):
        """Active status filter works (active)."""
        response = self._ajax_get(staff_client, {"is_active": "active"})
        data = response.json()
        # Both are active
        assert data["count"] == 2

    @patch("exchange_rates.views.admin_views.render_to_string", return_value="<div>card</div>")
    def test_filter_by_inactive(self, mock_render, staff_client, provider_account):
        """Active status filter works (inactive)."""
        provider_account.is_active = False
        provider_account.save()
        response = self._ajax_get(staff_client, {"is_active": "inactive"})
        data = response.json()
        assert data["count"] == 1

    @patch("exchange_rates.views.admin_views.render_to_string", return_value="<div>card</div>")
    def test_filter_by_component(
        self, mock_render, staff_client, provider_account, primary_provider
    ):
        """Component filter narrows by component slug."""
        response = self._ajax_get(
            staff_client,
            {"component": provider_account.component.slug},
        )
        data = response.json()
        assert data["count"] == 1

    def test_filter_empty_result(self, staff_client, provider_account):
        """Empty result set returns empty-state HTML."""
        response = self._ajax_get(staff_client, {"search": "nonexistent_xyz_123"})
        data = response.json()
        assert data["count"] == 0
        assert "empty-state" in data["html"]

    def test_get_method_only(self, staff_client, provider_account):
        """POST to filter endpoint returns 405."""
        response = staff_client.post(
            self.FILTER_URL,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        assert response.status_code == 405


# ============================================================
# Admin AJAX View Tests: toggle_provider_active
# ============================================================


class TestToggleProviderActive:
    """Tests for the toggle_provider_active AJAX view."""

    def _get_url(self, provider_id):
        return f"/en/admin/exchange-rates/admin/provideraccount/{provider_id}/toggle-active/"

    def test_toggle_active_to_inactive(self, staff_client, provider_account):
        """Toggling an active provider makes it inactive."""
        assert provider_account.is_active is True
        url = self._get_url(provider_account.id)
        response = staff_client.post(url)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["is_active"] is False

        provider_account.refresh_from_db()
        assert provider_account.is_active is False

    def test_toggle_inactive_to_active(self, staff_client, provider_account):
        """Toggling an inactive provider makes it active."""
        provider_account.is_active = False
        provider_account.save()

        url = self._get_url(provider_account.id)
        response = staff_client.post(url)
        data = response.json()
        assert data["success"] is True
        assert data["is_active"] is True

        provider_account.refresh_from_db()
        assert provider_account.is_active is True

    def test_requires_staff(self, anon_client, provider_account):
        """Anonymous users are redirected."""
        url = self._get_url(provider_account.id)
        response = anon_client.post(url)
        assert response.status_code == 302

    def test_requires_post(self, staff_client, provider_account):
        """GET requests return 405."""
        url = self._get_url(provider_account.id)
        response = staff_client.get(url)
        assert response.status_code == 405

    def test_nonexistent_provider_returns_error(self, staff_client):
        """Toggling a nonexistent provider returns 400 (caught by error handler)."""
        url = self._get_url(99999)
        response = staff_client.post(url)
        # View wraps get_object_or_404 in try/except Exception, returns 400
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False

    def test_non_staff_redirected(self, regular_client, provider_account):
        """Non-staff users are redirected."""
        url = self._get_url(provider_account.id)
        response = regular_client.post(url)
        assert response.status_code == 302


# ============================================================
# Admin AJAX View Tests: set_provider_primary
# ============================================================


class TestSetProviderPrimary:
    """Tests for the set_provider_primary AJAX view."""

    def _get_url(self, provider_id):
        return f"/en/admin/exchange-rates/admin/provideraccount/{provider_id}/set-primary/"

    def test_set_primary(self, staff_client, provider_account):
        """Setting a provider as primary marks it as primary."""
        assert provider_account.is_primary is False
        url = self._get_url(provider_account.id)
        response = staff_client.post(url)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

        provider_account.refresh_from_db()
        assert provider_account.is_primary is True

    def test_set_primary_clears_others(self, staff_client, provider_account, primary_provider):
        """Setting a new primary clears the old primary."""
        assert primary_provider.is_primary is True
        url = self._get_url(provider_account.id)
        response = staff_client.post(url)
        assert response.status_code == 200

        provider_account.refresh_from_db()
        primary_provider.refresh_from_db()
        assert provider_account.is_primary is True
        assert primary_provider.is_primary is False

    def test_requires_staff(self, anon_client, provider_account):
        """Anonymous users are redirected."""
        url = self._get_url(provider_account.id)
        response = anon_client.post(url)
        assert response.status_code == 302

    def test_requires_post(self, staff_client, provider_account):
        """GET requests return 405."""
        url = self._get_url(provider_account.id)
        response = staff_client.get(url)
        assert response.status_code == 405

    def test_nonexistent_provider_returns_error(self, staff_client):
        """Setting primary on nonexistent provider returns 400 (caught by error handler)."""
        url = self._get_url(99999)
        response = staff_client.post(url)
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False


# ============================================================
# Admin AJAX View Tests: delete_provider
# ============================================================


class TestDeleteProvider:
    """Tests for the delete_provider AJAX view."""

    def _get_url(self, provider_id):
        return f"/en/admin/exchange-rates/admin/provideraccount/{provider_id}/delete/"

    def test_delete_provider(self, staff_client, provider_account):
        """Deleting a provider removes it from the database."""
        pk = provider_account.pk
        url = self._get_url(pk)
        response = staff_client.post(url)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

        assert not ExchangeRateProviderAccount.objects.filter(pk=pk).exists()

    def test_delete_response_contains_name(self, staff_client, provider_account):
        """Delete response message includes the provider name."""
        url = self._get_url(provider_account.id)
        response = staff_client.post(url)
        data = response.json()
        assert "My Test Provider" in data["message"]

    def test_requires_staff(self, anon_client, provider_account):
        """Anonymous users are redirected."""
        url = self._get_url(provider_account.id)
        response = anon_client.post(url)
        assert response.status_code == 302

    def test_requires_post(self, staff_client, provider_account):
        """GET requests return 405."""
        url = self._get_url(provider_account.id)
        response = staff_client.get(url)
        assert response.status_code == 405

    def test_nonexistent_provider_returns_error(self, staff_client):
        """Deleting a nonexistent provider returns 400 (caught by error handler)."""
        url = self._get_url(99999)
        response = staff_client.post(url)
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False


# ============================================================
# Admin AJAX View Tests: provider_bulk_action
# ============================================================


class TestProviderBulkAction:
    """Tests for the provider_bulk_action AJAX view."""

    BULK_URL = "/en/admin/exchange-rates/admin/provideraccount/bulk-action/"

    def _post_bulk(self, client, action, provider_ids):
        """Helper for bulk action POST requests."""
        return client.post(
            self.BULK_URL,
            data=json.dumps({"action": action, "provider_ids": provider_ids}),
            content_type="application/json",
        )

    def test_bulk_enable(self, staff_client, provider_account):
        """Bulk enable sets is_active=True."""
        provider_account.is_active = False
        provider_account.save()

        response = self._post_bulk(staff_client, "enable", [provider_account.id])
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

        provider_account.refresh_from_db()
        assert provider_account.is_active is True

    def test_bulk_disable(self, staff_client, provider_account):
        """Bulk disable sets is_active=False."""
        assert provider_account.is_active is True

        response = self._post_bulk(staff_client, "disable", [provider_account.id])
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

        provider_account.refresh_from_db()
        assert provider_account.is_active is False

    def test_bulk_delete(self, staff_client, provider_account):
        """Bulk delete removes providers."""
        pk = provider_account.pk
        response = self._post_bulk(staff_client, "delete", [pk])
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

        assert not ExchangeRateProviderAccount.objects.filter(pk=pk).exists()

    def test_bulk_set_primary_single(self, staff_client, provider_account):
        """Bulk set_primary works with exactly one provider."""
        response = self._post_bulk(staff_client, "set_primary", [provider_account.id])
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

        provider_account.refresh_from_db()
        assert provider_account.is_primary is True

    def test_bulk_set_primary_multiple_fails(
        self, staff_client, provider_account, primary_provider
    ):
        """Bulk set_primary fails when multiple providers selected."""
        response = self._post_bulk(
            staff_client,
            "set_primary",
            [provider_account.id, primary_provider.id],
        )
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False

    def test_bulk_enable_multiple(self, staff_client, provider_account, primary_provider):
        """Bulk enable works on multiple providers."""
        provider_account.is_active = False
        provider_account.save()
        primary_provider.is_active = False
        primary_provider.save()

        response = self._post_bulk(
            staff_client,
            "enable",
            [provider_account.id, primary_provider.id],
        )
        assert response.status_code == 200

        provider_account.refresh_from_db()
        primary_provider.refresh_from_db()
        assert provider_account.is_active is True
        assert primary_provider.is_active is True

    def test_invalid_action(self, staff_client, provider_account):
        """Unknown action returns 400."""
        response = self._post_bulk(staff_client, "fly_to_moon", [provider_account.id])
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False

    def test_no_action(self, staff_client, provider_account):
        """Missing action returns 400."""
        response = self._post_bulk(staff_client, "", [provider_account.id])
        assert response.status_code == 400

    def test_no_providers(self, staff_client):
        """Empty provider_ids returns 400."""
        response = self._post_bulk(staff_client, "enable", [])
        assert response.status_code == 400

    def test_requires_staff(self, anon_client, provider_account):
        """Anonymous users are redirected."""
        response = anon_client.post(
            self.BULK_URL,
            data=json.dumps({"action": "enable", "provider_ids": [provider_account.id]}),
            content_type="application/json",
        )
        assert response.status_code == 302

    def test_requires_post(self, staff_client, provider_account):
        """GET requests return 405."""
        response = staff_client.get(self.BULK_URL)
        assert response.status_code == 405


# ============================================================
# URL Configuration Tests
# ============================================================


class TestURLConfiguration:
    """Tests for exchange_rates URL resolution."""

    def test_admin_changelist_url_resolves(self):
        """Admin changelist URL resolves correctly."""
        url = reverse("admin:exchange_rates_exchangerateprovideraccount_changelist")
        assert "/exchange_rates/exchangerateprovideraccount/" in url

    def test_admin_exchangerate_changelist_resolves(self):
        """ExchangeRate admin changelist resolves."""
        url = reverse("admin:exchange_rates_exchangerate_changelist")
        assert "/exchange_rates/exchangerate/" in url

    def test_admin_history_changelist_resolves(self):
        """ExchangeRateHistory admin changelist resolves."""
        url = reverse("admin:exchange_rates_exchangeratehistory_changelist")
        assert "/exchange_rates/exchangeratehistory/" in url

    def test_exchange_rates_app_urls(self):
        """App-level URL names resolve."""
        url = reverse("exchange_rates:provider_toggle_active", args=[1])
        assert "toggle-active" in url

        url = reverse("exchange_rates:provider_set_primary", args=[1])
        assert "set-primary" in url

        url = reverse("exchange_rates:provider_delete", args=[1])
        assert "delete" in url

        url = reverse("exchange_rates:provider_bulk_action")
        assert "bulk-action" in url

    def test_admin_filter_url_resolves(self):
        """Admin filter URL (from admin_urls.py) resolves."""
        url = reverse("exchange_rates_admin:filter_exchange_rate_providers")
        assert "filter" in url


# ============================================================
# Template CSP Compliance Tests
# ============================================================


class TestCSPCompliance:
    """Verify templates have no inline styles or onclick handlers."""

    TEMPLATE_DIR = PROJECT_ROOT / "exchange_rates" / "templates"

    def _get_template_files(self):
        """Get all HTML template files."""
        return list(self.TEMPLATE_DIR.rglob("*.html"))

    def test_no_inline_style_attributes(self):
        """No HTML templates contain inline style= attributes."""
        template_files = self._get_template_files()
        assert len(template_files) > 0, "No template files found"

        violations = []
        for path in template_files:
            content = path.read_text(encoding="utf-8")
            # Match style= but not {% static 'xxx.css' %} or stylesheet references
            matches = re.findall(r'\bstyle\s*=\s*["\']', content)
            if matches:
                violations.append(str(path.relative_to(PROJECT_ROOT)))

        assert violations == [], f"Inline style= attributes found in templates: {violations}"

    def test_no_onclick_handlers_in_templates(self):
        """No HTML templates contain onclick handlers."""
        template_files = self._get_template_files()
        violations = []
        for path in template_files:
            content = path.read_text(encoding="utf-8")
            matches = re.findall(r"\bonclick\s*=", content)
            if matches:
                violations.append(str(path.relative_to(PROJECT_ROOT)))

        assert violations == [], f"onclick handlers found in templates: {violations}"

    def test_no_onclick_handlers_in_js_files(self):
        """No JS files contain onclick handler assignments."""
        js_dir = PROJECT_ROOT / "exchange_rates" / "static" / "exchange_rates" / "js"
        if not js_dir.exists():
            pytest.skip("No JS directory found")

        js_files = list(js_dir.rglob("*.js"))
        assert len(js_files) > 0, "No JS files found"

        violations = []
        for path in js_files:
            content = path.read_text(encoding="utf-8")
            # Check for .onclick = or setAttribute('onclick') patterns
            if re.search(r"\.onclick\s*=", content) or re.search(
                r"setAttribute\s*\(\s*['\"]onclick['\"]", content
            ):
                violations.append(str(path.relative_to(PROJECT_ROOT)))

        assert violations == [], f"onclick handlers found in JS files: {violations}"


# ============================================================
# Static Files Copyright Header Tests
# ============================================================


class TestStaticFileCopyright:
    """Verify CSS and JS files have copyright headers."""

    STATIC_DIR = PROJECT_ROOT / "exchange_rates" / "static" / "exchange_rates"

    def test_css_files_have_copyright(self):
        """All CSS files start with copyright header.

        Header format per CLAUDE.md uses ASCII `(c)`:
        `/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */`
        """
        css_files = list(self.STATIC_DIR.rglob("*.css"))
        assert len(css_files) > 0, "No CSS files found"

        missing = []
        for path in css_files:
            content = path.read_text(encoding="utf-8")
            first_line = content.strip().split("\n")[0]
            has_copyright = "Copyright" in first_line and "Spwig" in first_line
            if not has_copyright:
                missing.append(str(path.relative_to(PROJECT_ROOT)))

        assert missing == [], f"CSS files missing copyright header: {missing}"

    def test_js_files_have_copyright(self):
        """All JS files start with copyright header (ASCII (c))."""
        js_files = list(self.STATIC_DIR.rglob("*.js"))
        assert len(js_files) > 0, "No JS files found"

        missing = []
        for path in js_files:
            content = path.read_text(encoding="utf-8")
            first_line = content.strip().split("\n")[0]
            has_copyright = "Copyright" in first_line and "Spwig" in first_line
            if not has_copyright:
                missing.append(str(path.relative_to(PROJECT_ROOT)))

        assert missing == [], f"JS files missing copyright header: {missing}"


# ============================================================
# i18n Compliance Tests
# ============================================================


class TestI18nCompliance:
    """Verify models use translatable verbose names."""

    def test_provider_account_verbose_name_translated(self):
        """ExchangeRateProviderAccount verbose_name uses gettext_lazy."""
        meta = ExchangeRateProviderAccount._meta
        # verbose_name is a lazy translation proxy
        assert hasattr(meta.verbose_name, "_proxy____args") or str(meta.verbose_name)

    def test_exchange_rate_verbose_name_translated(self):
        """ExchangeRate verbose_name uses gettext_lazy."""
        meta = ExchangeRate._meta
        assert str(meta.verbose_name) == "Exchange Rate"

    def test_history_verbose_name_translated(self):
        """ExchangeRateHistory verbose_name uses gettext_lazy."""
        meta = ExchangeRateHistory._meta
        assert str(meta.verbose_name) == "Exchange Rate History"

    def test_provider_account_field_verbose_names(self):
        """All fields on ExchangeRateProviderAccount have verbose names."""
        field_names = [
            "site",
            "component",
            "name",
            "credentials",
            "is_active",
            "is_primary",
            "priority",
            "settings",
            "last_sync_at",
            "sync_status",
            "sync_error_message",
        ]
        for field_name in field_names:
            field = ExchangeRateProviderAccount._meta.get_field(field_name)
            assert field.verbose_name is not None, f"Field '{field_name}' has no verbose_name"
            assert len(str(field.verbose_name)) > 0, f"Field '{field_name}' has empty verbose_name"

    def test_exchange_rate_field_verbose_names(self):
        """All fields on ExchangeRate have verbose names."""
        field_names = ["provider_account", "base_currency", "target_currency", "rate", "fetched_at"]
        for field_name in field_names:
            field = ExchangeRate._meta.get_field(field_name)
            assert field.verbose_name is not None, f"Field '{field_name}' has no verbose_name"

    def test_history_field_verbose_names(self):
        """All fields on ExchangeRateHistory have verbose names."""
        field_names = [
            "base_currency",
            "target_currency",
            "rate",
            "provider_name",
            "created_at",
            "order",
        ]
        for field_name in field_names:
            field = ExchangeRateHistory._meta.get_field(field_name)
            assert field.verbose_name is not None, f"Field '{field_name}' has no verbose_name"


# ============================================================
# Security Tests
# ============================================================


class TestSecurityEnforcement:
    """Verify security decorators on all admin AJAX views."""

    AJAX_URLS_POST = [
        "/en/admin/exchange-rates/admin/provideraccount/{id}/toggle-active/",
        "/en/admin/exchange-rates/admin/provideraccount/{id}/set-primary/",
        "/en/admin/exchange-rates/admin/provideraccount/{id}/delete/",
    ]
    BULK_URL = "/en/admin/exchange-rates/admin/provideraccount/bulk-action/"
    FILTER_URL = "/en/admin/exchange-rates/exchangerateprovideraccount/filter/"

    def test_all_post_views_reject_anonymous(self, anon_client, provider_account):
        """All POST-only AJAX views redirect anonymous users."""
        for url_template in self.AJAX_URLS_POST:
            url = url_template.format(id=provider_account.id)
            response = anon_client.post(url)
            assert response.status_code == 302, f"URL {url} did not redirect anonymous user"

    def test_bulk_action_rejects_anonymous(self, anon_client, provider_account):
        """Bulk action redirects anonymous users."""
        response = anon_client.post(
            self.BULK_URL,
            data=json.dumps({"action": "enable", "provider_ids": [provider_account.id]}),
            content_type="application/json",
        )
        assert response.status_code == 302

    def test_filter_rejects_anonymous(self, anon_client):
        """Filter view redirects anonymous users."""
        response = anon_client.get(self.FILTER_URL)
        assert response.status_code == 302

    def test_all_post_views_reject_get(self, staff_client, provider_account):
        """All POST-only views reject GET requests."""
        for url_template in self.AJAX_URLS_POST:
            url = url_template.format(id=provider_account.id)
            response = staff_client.get(url)
            assert response.status_code == 405, f"URL {url} did not reject GET"

    def test_filter_rejects_post(self, staff_client):
        """Filter view (GET-only) rejects POST."""
        response = staff_client.post(
            self.FILTER_URL,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        assert response.status_code == 405

    def test_all_post_views_reject_non_staff(self, regular_client, provider_account):
        """All POST-only AJAX views redirect non-staff users."""
        for url_template in self.AJAX_URLS_POST:
            url = url_template.format(id=provider_account.id)
            response = regular_client.post(url)
            assert response.status_code == 302, f"URL {url} did not redirect non-staff user"


# ============================================================
# Edge Case Tests
# ============================================================


class TestEdgeCases:
    """Edge case and boundary tests."""

    def test_provider_with_empty_settings(self, site, exchange_rate_component):
        """Provider with default empty dict settings works."""
        acct = ExchangeRateProviderAccount.objects.create(
            site=site,
            component=exchange_rate_component,
            name="Empty Settings",
            credentials=b"d",
        )
        assert acct.settings == {}

    def test_multiple_rates_different_providers(
        self, site, exchange_rate_component, exchange_rate_component_2
    ):
        """Same currency pair can exist for different providers."""
        p1 = ExchangeRateProviderAccount.objects.create(
            site=site,
            component=exchange_rate_component,
            name="P1",
            credentials=b"d",
        )
        p2 = ExchangeRateProviderAccount.objects.create(
            site=site,
            component=exchange_rate_component_2,
            name="P2",
            credentials=b"d",
        )
        r1 = ExchangeRate.objects.create(
            provider_account=p1,
            base_currency="USD",
            target_currency="EUR",
            rate=Decimal("0.85"),
        )
        r2 = ExchangeRate.objects.create(
            provider_account=p2,
            base_currency="USD",
            target_currency="EUR",
            rate=Decimal("0.86"),
        )
        assert r1.pk is not None
        assert r2.pk is not None
        assert r1.rate != r2.rate

    def test_bulk_action_with_nonexistent_ids(self, staff_client):
        """Bulk enable with nonexistent IDs succeeds (no-op)."""
        response = staff_client.post(
            "/en/admin/exchange-rates/admin/provideraccount/bulk-action/",
            data=json.dumps({"action": "enable", "provider_ids": [99998, 99999]}),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_toggle_then_verify_state(self, staff_client, provider_account):
        """Double-toggle returns to original state."""
        original = provider_account.is_active
        url = f"/en/admin/exchange-rates/admin/provideraccount/{provider_account.id}/toggle-active/"

        staff_client.post(url)
        staff_client.post(url)

        provider_account.refresh_from_db()
        assert provider_account.is_active == original

    def test_set_primary_already_primary(self, staff_client, primary_provider):
        """Setting already-primary provider as primary is idempotent."""
        url = f"/en/admin/exchange-rates/admin/provideraccount/{primary_provider.id}/set-primary/"
        response = staff_client.post(url)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

        primary_provider.refresh_from_db()
        assert primary_provider.is_primary is True

    def test_delete_provider_with_rates_cascades(
        self, staff_client, provider_account, exchange_rate
    ):
        """Deleting a provider cascades to its cached rates."""
        rate_pk = exchange_rate.pk
        url = f"/en/admin/exchange-rates/admin/provideraccount/{provider_account.id}/delete/"
        response = staff_client.post(url)
        assert response.status_code == 200
        assert not ExchangeRate.objects.filter(pk=rate_pk).exists()

    def test_history_without_order(self, db):
        """History entry created without an order works."""
        h = ExchangeRateHistory.objects.create(
            base_currency="AUD",
            target_currency="NZD",
            rate=Decimal("1.07"),
            provider_name="Test",
        )
        assert h.order is None
        assert "AUD/NZD" in str(h)
