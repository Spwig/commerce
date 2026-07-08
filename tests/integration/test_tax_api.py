"""
Tax Management API integration tests.

Tests TaxService calculation, TaxRate API endpoints, TaxPreset API,
and AJAX admin endpoints for filtering and preset loading.
"""
import pytest
from decimal import Decimal
from django.test import Client

from tests.factories import (
    ProductFactory, TaxRateFactory, CategoryFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.tax]


@pytest.fixture
def django_admin_client(admin_user):
    """Django test client logged in as staff user (for admin views)."""
    client = Client()
    client.force_login(admin_user)
    return client


# ============================================================
# TaxService — Core Calculation Logic
# ============================================================

class TestTaxServiceCalculation:
    """Tests for cart.services.tax_service.TaxService."""

    def test_get_applicable_taxes_by_country(self, site_settings):
        """Finds tax rates matching a country code."""
        from cart.services.tax_service import TaxService

        de_vat = TaxRateFactory(de_vat=True)
        TaxRateFactory(uk_vat=True)

        taxes = TaxService.get_applicable_taxes(country='DE')
        assert len(taxes) == 1
        assert taxes[0].pk == de_vat.pk

    def test_get_applicable_taxes_by_state(self, site_settings):
        """State-level rate is found when country + state match."""
        from cart.services.tax_service import TaxService

        ny_tax = TaxRateFactory(ny=True)
        TaxRateFactory(ca=True)

        taxes = TaxService.get_applicable_taxes(country='US', state='NY')
        assert len(taxes) == 1
        assert taxes[0].pk == ny_tax.pk

    def test_inactive_rates_excluded(self, site_settings):
        """Inactive rates are not returned."""
        from cart.services.tax_service import TaxService

        TaxRateFactory(de_vat=True, is_active=False)

        taxes = TaxService.get_applicable_taxes(country='DE')
        assert len(taxes) == 0

    def test_calculate_tax_single_rate(self, site_settings, simple_product):
        """Single rate applied to items produces correct tax amount."""
        from cart.services.tax_service import TaxService

        # DE VAT = 19%, applies_to_shipping=True (factory trait)
        TaxRateFactory(de_vat=True)

        items = [(simple_product, 2, Decimal('50.00'))]
        total_tax, breakdown = TaxService.calculate_tax(
            items=items,
            shipping_cost=Decimal('5.00'),
            country='DE',
        )
        # 19% of (50.00 + 5.00) = 10.45 (DE VAT applies to shipping)
        assert total_tax == Decimal('10.45')
        assert len(breakdown) == 1
        assert breakdown[0]['rate_display'] == '19.0000%'

    def test_calculate_tax_without_shipping(self, site_settings, simple_product):
        """Tax excludes shipping when applies_to_shipping is False."""
        from cart.services.tax_service import TaxService

        TaxRateFactory(
            name='Test VAT',
            country='FR',
            rate=Decimal('0.2000'),
            tax_type='vat',
            applies_to_shipping=False,
        )

        items = [(simple_product, 1, Decimal('100.00'))]
        total_tax, breakdown = TaxService.calculate_tax(
            items=items,
            shipping_cost=Decimal('10.00'),
            country='FR',
        )
        # 20% of 100.00 only (shipping excluded)
        assert total_tax == Decimal('20.00')

    def test_calculate_tax_with_shipping(self, site_settings, simple_product):
        """Tax applies to shipping when applies_to_shipping is True."""
        from cart.services.tax_service import TaxService

        TaxRateFactory(
            name='UK VAT with shipping',
            country='GB',
            rate=Decimal('0.2000'),
            tax_type='vat',
            applies_to_shipping=True,
        )

        items = [(simple_product, 1, Decimal('100.00'))]
        total_tax, breakdown = TaxService.calculate_tax(
            items=items,
            shipping_cost=Decimal('10.00'),
            country='GB',
        )
        # 20% of (100 + 10) = 22.00
        assert total_tax == Decimal('22.00')

    def test_calculate_tax_no_matching_rates(self, site_settings, simple_product):
        """No tax when no rates match the address."""
        from cart.services.tax_service import TaxService

        TaxRateFactory(de_vat=True)

        items = [(simple_product, 1, Decimal('100.00'))]
        total_tax, breakdown = TaxService.calculate_tax(
            items=items,
            shipping_cost=Decimal('5.00'),
            country='JP',
        )
        assert total_tax == Decimal('0.00')
        assert len(breakdown) == 0

    def test_calculate_tax_empty_items_with_shipping_tax(self, site_settings):
        """Shipping-only tax is calculated when items list is empty but shipping taxed."""
        from cart.services.tax_service import TaxService

        # DE VAT applies to shipping
        TaxRateFactory(de_vat=True)

        total_tax, breakdown = TaxService.calculate_tax(
            items=[],
            shipping_cost=Decimal('5.00'),
            country='DE',
        )
        # 19% of 5.00 shipping = 0.95
        assert total_tax == Decimal('0.95')

    def test_calculate_tax_empty_items_no_shipping_tax(self, site_settings):
        """No tax when items empty and rate doesn't apply to shipping."""
        from cart.services.tax_service import TaxService

        TaxRateFactory(
            name='FR VAT',
            country='FR',
            rate=Decimal('0.2000'),
            tax_type='vat',
            applies_to_shipping=False,
        )

        total_tax, breakdown = TaxService.calculate_tax(
            items=[],
            shipping_cost=Decimal('5.00'),
            country='FR',
        )
        assert total_tax == Decimal('0.00')

    def test_specificity_state_over_country(self, site_settings, simple_product):
        """State-level rate takes priority over country-wide rate."""
        from cart.services.tax_service import TaxService

        # Country-wide US rate
        TaxRateFactory(name='US Federal', country='US', rate=Decimal('0.0500'))
        # State-specific CA rate
        TaxRateFactory(ca=True)  # 7.25%

        taxes = TaxService.get_applicable_taxes(country='US', state='CA')
        # Both should match — country-wide and state-specific
        assert len(taxes) == 2
        # State-specific should be first (higher specificity)
        assert taxes[0].state == 'CA'


# ============================================================
# TaxService — Preset Loading
# ============================================================

class TestTaxServicePresets:
    """Tests for loading DB-stored tax presets."""

    def test_load_preset_creates_rates(self, site_settings):
        """Loading a preset group creates TaxRate records."""
        from cart.services.tax_service import TaxService
        from cart.models import TaxRate

        initial_count = TaxRate.objects.count()
        created, skipped = TaxService.load_preset('eu_vat')

        assert created == 27
        assert skipped == 0
        assert TaxRate.objects.count() == initial_count + 27

    def test_load_preset_idempotent(self, site_settings):
        """Loading the same preset twice doesn't duplicate rates."""
        from cart.services.tax_service import TaxService
        from cart.models import TaxRate

        TaxService.load_preset('eu_vat')
        count_after_first = TaxRate.objects.count()

        created, skipped = TaxService.load_preset('eu_vat')
        assert created == 0
        assert skipped == 27
        assert TaxRate.objects.count() == count_after_first

    def test_load_preset_invalid_key(self, site_settings):
        """Loading a non-existent preset key returns (0, 0)."""
        from cart.services.tax_service import TaxService

        created, skipped = TaxService.load_preset('nonexistent_preset')
        assert created == 0
        assert skipped == 0


# ============================================================
# TaxRate REST API
# ============================================================

class TestTaxRateAPI:
    """Tests for /api/tax-rates/ endpoints."""

    def test_list_requires_auth(self, api_client):
        """Tax rate list requires authentication."""
        resp = api_client.get('/api/tax-rates/')
        assert resp.status_code in (401, 403)

    def test_list_returns_rates(self, admin_client, site_settings):
        """Admin can list tax rates."""
        TaxRateFactory(ny=True)
        TaxRateFactory(de_vat=True)

        resp = admin_client.get('/api/tax-rates/')
        assert resp.status_code == 200
        data = resp.json()
        assert data['count'] == 2

    def test_rate_display_field(self, admin_client, site_settings):
        """API includes rate_display as human-readable percentage."""
        TaxRateFactory(ny=True)  # 8.88%

        resp = admin_client.get('/api/tax-rates/')
        rate = resp.json()['results'][0]
        assert 'rate_display' in rate
        assert rate['rate_display'] == '8.8800%'

    def test_create_rate(self, admin_client, site_settings):
        """Admin can create a new tax rate via API."""
        resp = admin_client.post('/api/tax-rates/', {
            'name': 'Test Tax',
            'country': 'AU',
            'rate': '0.1000',
            'tax_type': 'gst',
            'is_active': True,
        })
        assert resp.status_code == 201
        assert resp.json()['name'] == 'Test Tax'

    def test_calculate_action(self, admin_client, site_settings, simple_product):
        """Calculate action returns tax for given address and items."""
        # Use a rate that does NOT apply to shipping for clear assertion
        TaxRateFactory(
            name='AU GST',
            country='AU',
            rate=Decimal('0.1000'),
            tax_type='gst',
            applies_to_shipping=False,
        )

        resp = admin_client.post('/api/tax-rates/calculate/', {
            'country': 'AU',
            'items': [
                {'product_id': simple_product.pk, 'quantity': 2, 'price': '25.00'},
            ],
            'shipping_cost': '5.00',
        }, format='json')
        assert resp.status_code == 200
        data = resp.json()
        # 10% of (25*2) = 5.00 (shipping excluded)
        assert Decimal(data['total_tax']) == Decimal('5.00')
        assert len(data['breakdown']) == 1

    def test_by_country_action(self, admin_client, site_settings):
        """by_country action groups rates by country."""
        TaxRateFactory(ny=True)
        TaxRateFactory(ca=True)
        TaxRateFactory(de_vat=True)

        resp = admin_client.get('/api/tax-rates/by_country/')
        assert resp.status_code == 200
        data = resp.json()
        # Response is a dict keyed by country code: {"US": [...], "DE": [...]}
        assert 'US' in data
        assert 'DE' in data
        assert len(data['US']) == 2  # NY + CA


# ============================================================
# TaxPreset REST API
# ============================================================

class TestTaxPresetAPI:
    """Tests for /api/tax-presets/ read-only endpoints."""

    def test_list_requires_admin(self, auth_client):
        """Regular customers cannot access presets."""
        resp = auth_client.get('/api/tax-presets/')
        assert resp.status_code == 403

    def test_list_presets(self, admin_client, site_settings):
        """Admin can list all preset groups."""
        resp = admin_client.get('/api/tax-presets/')
        assert resp.status_code == 200
        data = resp.json()
        # 11 groups from data migrations (10 initial + uk_vat)
        assert data['count'] == 11

    def test_preset_has_rate_count(self, admin_client, site_settings):
        """Each preset group includes a rate count."""
        resp = admin_client.get('/api/tax-presets/')
        results = resp.json()['results']
        eu = next(g for g in results if g['key'] == 'eu_vat')
        assert eu['rates_count'] == 27


# ============================================================
# Admin AJAX Endpoints
# ============================================================

class TestTaxAdminAJAX:
    """Tests for admin AJAX filter and preset load endpoints."""

    def test_filter_requires_staff(self, customer_user, site_settings):
        """Non-staff users cannot access filter endpoint."""
        client = Client()
        client.force_login(customer_user)
        resp = client.get(
            '/en/admin/cart/taxrate/filter/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        assert resp.status_code in (302, 403)

    def test_filter_returns_html(self, django_admin_client, site_settings):
        """Filter endpoint returns HTML partial and count."""
        TaxRateFactory(ny=True)
        TaxRateFactory(de_vat=True)

        resp = django_admin_client.get(
            '/en/admin/cart/taxrate/filter/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        assert resp.status_code == 200
        data = resp.json()
        assert 'html' in data
        assert data['count'] == 2

    def test_filter_by_country(self, django_admin_client, site_settings):
        """Filter narrows results to specific country."""
        TaxRateFactory(ny=True)
        TaxRateFactory(de_vat=True)

        resp = django_admin_client.get(
            '/en/admin/cart/taxrate/filter/?country=DE',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        data = resp.json()
        assert data['count'] == 1

    def test_filter_by_search(self, django_admin_client, site_settings):
        """Search filters by name."""
        TaxRateFactory(ny=True)
        TaxRateFactory(de_vat=True)

        resp = django_admin_client.get(
            '/en/admin/cart/taxrate/filter/?search=DE',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        data = resp.json()
        assert data['count'] == 1

    def test_load_preset_endpoint(self, django_admin_client, site_settings):
        """Load preset endpoint creates rates from DB presets."""
        import json
        from cart.models import TaxRate

        initial = TaxRate.objects.count()

        resp = django_admin_client.post(
            '/en/admin/cart/taxrate/load-preset/',
            json.dumps({'group_key': 'uk_vat'}),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data['created'] >= 1
        assert TaxRate.objects.count() > initial
