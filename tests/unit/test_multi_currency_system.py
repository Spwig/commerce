"""
Unit tests for multi-currency FX accounting model.

Tests the end-to-end multi-currency system including:
- SiteSettings validation (exchange rate provider prerequisites)
- Order.compute_base_amounts() for single- and multi-currency orders
- Refund.compute_base_amounts() using parent order's locked rate
- Affiliate Commission currency tracking
- Analytics base-currency aggregation
"""
import pytest
from decimal import Decimal
from unittest.mock import patch, MagicMock

from django.core.exceptions import ValidationError
from django.db.models import Sum, DecimalField, Value
from django.db.models.functions import Coalesce
from django.utils import timezone

from orders.models import Order, Refund
from tests.factories import (
    UserFactory,
    OrderFactory,
    OrderItemFactory,
    RefundFactory,
    ProductFactory,
)


# ============================================================
# Phase 1: SiteSettings multi-currency validation
# ============================================================

@pytest.mark.django_db
class TestSiteSettingsMultiCurrencyValidation:
    """Verify that SiteSettings.clean() blocks multi-currency without providers."""

    def _get_settings(self):
        from core.models import SiteSettings
        settings, _ = SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'Test Store',
                'admin_email': 'admin@test.spwig.com',
                'default_currency': 'EUR',
                'default_language': 'en',
            }
        )
        return settings

    def _ensure_site(self):
        from django.contrib.sites.models import Site
        Site.objects.get_or_create(id=1, defaults={'domain': 'localhost', 'name': 'Test'})

    def test_enable_multi_currency_without_providers_raises(self):
        """Cannot enable multi-currency without an active exchange rate provider."""
        self._ensure_site()
        settings = self._get_settings()
        settings.enable_multi_currency = True
        settings.supported_currencies = ['EUR', 'NZD']

        with pytest.raises(ValidationError) as exc_info:
            settings.clean()

        assert 'enable_multi_currency' in exc_info.value.message_dict

    def test_primary_strategy_without_primary_provider_raises(self, django_site):
        """Strategy='primary' with no primary provider raises ValidationError."""
        from exchange_rates.models import ExchangeRateProviderAccount
        from component_updates.models import ComponentRegistry

        component, _ = ComponentRegistry.objects.get_or_create(
            slug='test-fx-provider',
            component_type='exchange_rate_provider',
            defaults={'name': 'Test FX', 'current_version': '1.0.0', 'author': 'Spwig'}
        )
        ExchangeRateProviderAccount.objects.create(
            site=django_site,
            component=component,
            is_active=True,
            is_primary=False,
            name='Secondary Provider',
            credentials=b'',
        )

        settings = self._get_settings()
        settings.enable_multi_currency = True
        settings.exchange_rate_selection_strategy = 'primary'
        settings.supported_currencies = ['EUR', 'NZD']

        with pytest.raises(ValidationError) as exc_info:
            settings.clean()

        assert 'exchange_rate_selection_strategy' in exc_info.value.message_dict

    def test_supported_currencies_too_few_raises(self, django_site):
        """supported_currencies with only 1 entry raises ValidationError."""
        from exchange_rates.models import ExchangeRateProviderAccount
        from component_updates.models import ComponentRegistry

        component, _ = ComponentRegistry.objects.get_or_create(
            slug='test-fx-provider',
            component_type='exchange_rate_provider',
            defaults={'name': 'Test FX', 'current_version': '1.0.0', 'author': 'Spwig'}
        )
        ExchangeRateProviderAccount.objects.get_or_create(
            site=django_site,
            component=component,
            defaults={'is_active': True, 'is_primary': True, 'name': 'Test Provider', 'credentials': b''}
        )

        settings = self._get_settings()
        settings.enable_multi_currency = True
        settings.supported_currencies = ['EUR']

        with pytest.raises(ValidationError) as exc_info:
            settings.clean()

        assert 'supported_currencies' in exc_info.value.message_dict

    def test_default_currency_not_in_supported_raises(self, django_site):
        """default_currency must be included in supported_currencies."""
        from exchange_rates.models import ExchangeRateProviderAccount
        from component_updates.models import ComponentRegistry

        component, _ = ComponentRegistry.objects.get_or_create(
            slug='test-fx-provider',
            component_type='exchange_rate_provider',
            defaults={'name': 'Test FX', 'current_version': '1.0.0', 'author': 'Spwig'}
        )
        ExchangeRateProviderAccount.objects.get_or_create(
            site=django_site,
            component=component,
            defaults={'is_active': True, 'is_primary': True, 'name': 'Test Provider', 'credentials': b''}
        )

        settings = self._get_settings()
        settings.enable_multi_currency = True
        settings.default_currency = 'EUR'
        settings.supported_currencies = ['NZD', 'USD']  # EUR missing

        with pytest.raises(ValidationError) as exc_info:
            settings.clean()

        assert 'supported_currencies' in exc_info.value.message_dict

    def test_valid_multi_currency_config_passes(self, django_site):
        """A fully valid multi-currency configuration passes validation."""
        from exchange_rates.models import ExchangeRateProviderAccount
        from component_updates.models import ComponentRegistry

        component, _ = ComponentRegistry.objects.get_or_create(
            slug='test-fx-provider',
            component_type='exchange_rate_provider',
            defaults={'name': 'Test FX', 'current_version': '1.0.0', 'author': 'Spwig'}
        )
        ExchangeRateProviderAccount.objects.get_or_create(
            site=django_site,
            component=component,
            defaults={'is_active': True, 'is_primary': True, 'name': 'Test Provider', 'credentials': b''}
        )

        settings = self._get_settings()
        settings.enable_multi_currency = True
        settings.exchange_rate_selection_strategy = 'primary'
        settings.default_currency = 'EUR'
        settings.supported_currencies = ['EUR', 'NZD', 'USD']

        # Should not raise
        settings.clean()

    def test_single_currency_store_unaffected(self):
        """Stores not enabling multi-currency skip all FX validation."""
        self._ensure_site()
        settings = self._get_settings()
        settings.enable_multi_currency = False
        settings.supported_currencies = []

        # Should not raise even without providers
        settings.clean()


# ============================================================
# Phase 2 & 3: Order / OrderItem / Refund compute_base_amounts
# ============================================================

@pytest.mark.django_db
class TestOrderComputeBaseAmounts:
    """Tests for Order.compute_base_amounts() method."""

    def test_single_currency_copies_amounts(self):
        """Single-currency order: *_base fields equal raw amounts."""
        order = OrderFactory(
            subtotal=Decimal('100.00'),
            tax_amount=Decimal('8.88'),
            shipping_cost=Decimal('5.99'),
            discount_amount=Decimal('10.00'),
            gift_card_discount=Decimal('0.00'),
            total_amount=Decimal('104.87'),
            amount_paid=Decimal('104.87'),
            amount_refunded=Decimal('0.00'),
            customer_currency='USD',
            base_currency='USD',
        )
        order.compute_base_amounts()

        assert order.subtotal_base == Decimal('100.00')
        assert order.tax_amount_base == Decimal('8.88')
        assert order.shipping_cost_base == Decimal('5.99')
        assert order.discount_amount_base == Decimal('10.00')
        assert order.total_amount_base == Decimal('104.87')
        assert order.amount_paid_base == Decimal('104.87')
        assert order.amount_refunded_base == Decimal('0.00')

    def test_multi_currency_computes_base(self):
        """Multi-currency order: base = customer_amount / rate."""
        # EUR base store, customer pays in NZD
        # Rate: 1 EUR = 1.78 NZD (base->customer)
        order = OrderFactory(
            subtotal=Decimal('178.00'),
            subtotal_currency='NZD',
            tax_amount=Decimal('26.70'),
            tax_amount_currency='NZD',
            shipping_cost=Decimal('17.80'),
            shipping_cost_currency='NZD',
            discount_amount=Decimal('0.00'),
            discount_amount_currency='NZD',
            gift_card_discount=Decimal('0.00'),
            gift_card_discount_currency='NZD',
            total_amount=Decimal('222.50'),
            total_amount_currency='NZD',
            amount_paid=Decimal('222.50'),
            amount_paid_currency='NZD',
            amount_refunded=Decimal('0.00'),
            amount_refunded_currency='NZD',
            customer_currency='NZD',
            base_currency='EUR',
            exchange_rate_used=Decimal('1.780000'),
            fx_policy='spot',
        )
        order.compute_base_amounts()

        # 178.00 / 1.78 = 100.00
        assert order.subtotal_base == Decimal('100.00')
        # 26.70 / 1.78 = 15.00
        assert order.tax_amount_base == Decimal('15.00')
        # 17.80 / 1.78 = 10.00
        assert order.shipping_cost_base == Decimal('10.00')
        # 222.50 / 1.78 = 125.00
        assert order.total_amount_base == Decimal('125.00')
        assert order.amount_paid_base == Decimal('125.00')

    def test_null_rate_leaves_base_null(self):
        """If exchange_rate_used is None on cross-currency order, base amounts stay NULL."""
        order = OrderFactory(
            total_amount=Decimal('100.00'),
            customer_currency='NZD',
            base_currency='EUR',
            exchange_rate_used=None,
            total_amount_base=None,
        )
        order.compute_base_amounts()

        # Cross-currency with no rate: base amounts left NULL for manual review
        assert order.total_amount_base is None

    def test_zero_rate_leaves_base_null(self):
        """If exchange_rate_used is 0 on cross-currency order, base amounts stay NULL."""
        order = OrderFactory(
            total_amount=Decimal('100.00'),
            customer_currency='NZD',
            base_currency='EUR',
            exchange_rate_used=Decimal('0'),
            total_amount_base=None,
        )
        order.compute_base_amounts()

        # Cross-currency with zero rate: base amounts left NULL for manual review
        assert order.total_amount_base is None

    def test_no_customer_currency_copies_directly(self):
        """If customer_currency is empty, treat as single-currency."""
        order = OrderFactory(
            total_amount=Decimal('50.00'),
            customer_currency='',
            base_currency='USD',
        )
        order.compute_base_amounts()

        assert order.total_amount_base == Decimal('50.00')

    def test_fx_policy_values(self):
        """Verify fx_policy field accepts expected choices."""
        for policy in ['none', 'spot', 'daily', 'psp']:
            order = OrderFactory(fx_policy=policy)
            assert order.fx_policy == policy


@pytest.mark.django_db
class TestRefundComputeBaseAmounts:
    """Tests for Refund.compute_base_amounts() method."""

    def test_single_currency_refund(self):
        """Single-currency refund: *_base equals raw amounts."""
        order = OrderFactory(
            customer_currency='USD',
            base_currency='USD',
            total_amount=Decimal('100.00'),
            paid_order=True,
        )
        refund = RefundFactory(
            order=order,
            total_amount=Decimal('100.00'),
            shipping_refund_amount=Decimal('5.99'),
            tax_refund_amount=Decimal('8.88'),
        )
        refund.compute_base_amounts()

        assert refund.total_amount_base == Decimal('100.00')
        assert refund.shipping_refund_amount_base == Decimal('5.99')
        assert refund.tax_refund_amount_base == Decimal('8.88')

    def test_multi_currency_refund_uses_order_rate(self):
        """Multi-currency refund uses parent order's locked exchange rate."""
        order = OrderFactory(
            customer_currency='NZD',
            base_currency='EUR',
            exchange_rate_used=Decimal('1.780000'),
            total_amount=Decimal('222.50'),
            total_amount_currency='NZD',
            paid_order=True,
        )
        refund = RefundFactory(
            order=order,
            total_amount=Decimal('178.00'),
            total_amount_currency='NZD',
            shipping_refund_amount=Decimal('17.80'),
            shipping_refund_amount_currency='NZD',
            tax_refund_amount=Decimal('26.70'),
            tax_refund_amount_currency='NZD',
        )
        refund.compute_base_amounts()

        # 178.00 / 1.78 = 100.00
        assert refund.total_amount_base == Decimal('100.00')
        # 17.80 / 1.78 = 10.00
        assert refund.shipping_refund_amount_base == Decimal('10.00')
        # 26.70 / 1.78 = 15.00
        assert refund.tax_refund_amount_base == Decimal('15.00')


# ============================================================
# Phase 4: Affiliate Commission currency tracking
# ============================================================

@pytest.mark.django_db
class TestCommissionCurrencyFields:
    """Tests for Commission model currency fields."""

    def test_commission_currency_fields_exist(self):
        """Commission model has currency, amount_base, base_currency, exchange_rate_used."""
        from affiliate.models import Commission
        field_names = [f.name for f in Commission._meta.get_fields()]
        assert 'currency' in field_names
        assert 'amount_base' in field_names
        assert 'base_currency' in field_names
        assert 'exchange_rate_used' in field_names

    def test_payout_base_fields_exist(self):
        """Payout model has amount_base, base_currency."""
        from affiliate.models import Payout
        field_names = [f.name for f in Payout._meta.get_fields()]
        assert 'amount_base' in field_names
        assert 'base_currency' in field_names


# ============================================================
# Phase 6: Analytics base-currency aggregation
# ============================================================

@pytest.mark.django_db
class TestAnalyticsBaseCurrencyAggregation:
    """Tests for currency-aware analytics aggregation."""

    def test_base_sum_helper(self):
        """_base_sum returns correct Coalesce expression."""
        from management.services.shop_analytics_service import ShopAnalyticsService
        expr = ShopAnalyticsService._base_sum('total_amount')
        # Should be a Coalesce wrapping Sum('total_amount_base'), Sum('total_amount'), Value(0)
        assert isinstance(expr, Coalesce)

    def test_base_avg_helper(self):
        """_base_avg returns correct Coalesce expression."""
        from management.services.shop_analytics_service import ShopAnalyticsService
        expr = ShopAnalyticsService._base_avg('total_amount')
        assert isinstance(expr, Coalesce)

    def test_mixed_currency_orders_aggregate_in_base(self):
        """Orders in different currencies aggregate correctly using *_base fields."""
        # EUR-base store
        # Order 1: paid in EUR (same as base) - 100 EUR
        order1 = OrderFactory(
            subtotal=Decimal('100.00'),
            total_amount=Decimal('100.00'),
            total_amount_base=Decimal('100.00'),
            customer_currency='EUR',
            base_currency='EUR',
            payment_status='paid',
            status='processing',
        )
        # Order 2: paid in NZD (foreign) - 178 NZD = 100 EUR at rate 1.78
        order2 = OrderFactory(
            subtotal=Decimal('178.00'),
            subtotal_currency='NZD',
            total_amount=Decimal('178.00'),
            total_amount_currency='NZD',
            total_amount_base=Decimal('100.00'),
            customer_currency='NZD',
            base_currency='EUR',
            exchange_rate_used=Decimal('1.780000'),
            fx_policy='spot',
            payment_status='paid',
            status='processing',
        )

        # Naive Sum('total_amount') would give 100 + 178 = 278 (WRONG, mixed currencies)
        naive_total = Order.objects.filter(
            id__in=[order1.id, order2.id]
        ).aggregate(
            total=Sum('total_amount', output_field=DecimalField())
        )['total']
        assert naive_total == Decimal('278.00')  # This is the bug we're fixing

        # Correct: Sum('total_amount_base') gives 100 + 100 = 200 EUR
        base_total = Order.objects.filter(
            id__in=[order1.id, order2.id]
        ).aggregate(
            total=Sum('total_amount_base', output_field=DecimalField())
        )['total']
        assert base_total == Decimal('200.00')

    def test_coalesce_fallback_for_null_base(self):
        """Coalesce falls back to raw amount when *_base is NULL."""
        # Legacy order without base amounts populated
        order = OrderFactory(
            total_amount=Decimal('50.00'),
            total_amount_base=None,
            status='processing',
        )

        result = Order.objects.filter(id=order.id).aggregate(
            total=Coalesce(
                Sum('total_amount_base', output_field=DecimalField()),
                Sum('total_amount', output_field=DecimalField()),
                Value(0, output_field=DecimalField()),
            )
        )['total']
        assert result == Decimal('50.00')

    def test_single_currency_store_unaffected(self):
        """Single-currency store: *_base equals raw amounts, no difference in reporting."""
        order1 = OrderFactory(
            total_amount=Decimal('75.00'),
            total_amount_base=Decimal('75.00'),
            customer_currency='USD',
            base_currency='USD',
            status='processing',
        )
        order2 = OrderFactory(
            total_amount=Decimal('125.00'),
            total_amount_base=Decimal('125.00'),
            customer_currency='USD',
            base_currency='USD',
            status='processing',
        )

        base_total = Order.objects.filter(
            id__in=[order1.id, order2.id]
        ).aggregate(
            total=Sum('total_amount_base', output_field=DecimalField())
        )['total']
        assert base_total == Decimal('200.00')


# ============================================================
# Integration: Factory defaults produce valid data
# ============================================================

@pytest.mark.django_db
class TestFactoryDefaults:
    """Verify factory defaults produce consistent base-currency data."""

    def test_order_factory_base_fields_default(self):
        """OrderFactory default: base fields mirror customer amounts."""
        order = OrderFactory()
        assert order.fx_policy == 'none'
        assert order.base_currency == 'USD'
        assert order.total_amount_base == order.total_amount.amount

    def test_order_factory_multi_currency_trait(self):
        """OrderFactory multi_currency trait sets FX fields."""
        order = OrderFactory(multi_currency=True)
        assert order.customer_currency == 'EUR'
        assert order.exchange_rate_used == Decimal('0.85')
        assert order.exchange_rate_provider == 'ecb'
        assert order.base_currency == 'USD'

    def test_order_item_factory_base_fields(self):
        """OrderItemFactory default: base fields mirror customer amounts."""
        item = OrderItemFactory()
        assert item.unit_price_base is not None
        assert item.total_price_base is not None

    def test_refund_factory_base_fields(self):
        """RefundFactory default: base fields mirror customer amounts."""
        refund = RefundFactory()
        assert refund.total_amount_base is not None
        assert refund.shipping_refund_amount_base is not None
        assert refund.tax_refund_amount_base is not None
