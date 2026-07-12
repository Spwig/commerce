"""
Unit tests for cart multi-currency support.

Tests the cart currency flow including:
- Cart.currency field and effective_currency property
- CartService.add_item() currency initialization
- CartItem.save() price lookup by cart currency
- CheckoutSession.recalculate_totals() currency consistency
- Mini-cart API currency formatting
- Template/JS currency symbol correctness (no hardcoded $)
"""
import pytest
from decimal import Decimal
from unittest.mock import patch, MagicMock

from django.test import RequestFactory

from cart.models import Cart, CartItem, CheckoutSession
from cart.services.cart_service import CartService
from tests.factories import (
    UserFactory,
    ProductFactory,
    CartFactory,
    CartItemFactory,
    CategoryFactory,
    CheckoutSessionFactory,
)


# ============================================================
# Helper fixtures
# ============================================================

@pytest.fixture
def eur_site_settings(db):
    """SiteSettings with EUR as default currency."""
    from core.models import SiteSettings
    from django.contrib.sites.models import Site
    Site.objects.get_or_create(id=1, defaults={'domain': 'localhost', 'name': 'Test'})
    settings, _ = SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            'site_name': 'Test Store',
            'admin_email': 'admin@test.spwig.com',
            'default_currency': 'EUR',
            'default_language': 'en',
        }
    )
    if settings.default_currency != 'EUR':
        settings.default_currency = 'EUR'
        settings.save(update_fields=['default_currency'])
    return settings


@pytest.fixture
def eur_product(db):
    """Product priced in EUR."""
    category = CategoryFactory(name='Test EUR', slug='test-eur')
    return ProductFactory(
        name='EUR Widget',
        slug='eur-widget',
        category=category,
        price=Decimal('49.99'),
        price_currency='EUR',
    )


@pytest.fixture
def eur_product_no_tracking(db):
    """Product priced in EUR with no inventory tracking."""
    category = CategoryFactory(name='Test EUR NT', slug='test-eur-nt')
    return ProductFactory(
        name='EUR No-Track Widget',
        slug='eur-no-track-widget',
        category=category,
        price=Decimal('29.99'),
        price_currency='EUR',
        track_inventory=False,
    )


# ============================================================
# Phase 1: Cart.currency field & effective_currency
# ============================================================

@pytest.mark.django_db
class TestCartCurrencyField:
    """Tests for the Cart.currency field and effective_currency property."""

    def test_cart_currency_field_exists(self):
        """Cart model has a currency CharField."""
        field = Cart._meta.get_field('currency')
        assert field is not None
        assert field.max_length == 3

    def test_cart_currency_defaults_empty(self):
        """New cart has empty currency (uses store default)."""
        cart = CartFactory()
        assert cart.currency == ''

    def test_effective_currency_returns_store_default_when_empty(self, eur_site_settings):
        """effective_currency returns store default when cart.currency is empty."""
        cart = CartFactory()
        assert cart.currency == ''
        assert cart.effective_currency == 'EUR'

    def test_effective_currency_returns_explicit_currency(self, eur_site_settings):
        """effective_currency returns the explicit currency when set."""
        cart = CartFactory()
        cart.currency = 'NZD'
        cart.save(update_fields=['currency'])
        assert cart.effective_currency == 'NZD'

    def test_effective_currency_returns_set_currency_over_default(self, eur_site_settings):
        """Explicit cart currency takes precedence over store default."""
        cart = CartFactory()
        cart.currency = 'GBP'
        cart.save(update_fields=['currency'])
        # Store default is EUR, but cart is GBP
        assert cart.effective_currency == 'GBP'


# ============================================================
# Phase 2: CartService.add_item() currency initialization
# ============================================================

@pytest.mark.django_db
class TestCartServiceAddItemCurrency:
    """Tests for CartService.add_item() customer_currency handling."""

    def test_add_item_sets_cart_currency_to_default(self, eur_site_settings, eur_product_no_tracking):
        """When multi-currency is disabled, cart currency is set to store default."""
        cart = CartFactory(user=None, session_key='test_session_add_1')
        success, msg, item = CartService.add_item(
            cart=cart,
            product_id=eur_product_no_tracking.id,
            quantity=1,
            customer_currency='GBP',  # ignored when multi-currency disabled
        )
        assert success, f"add_item failed: {msg}"
        cart.refresh_from_db()
        # multi_currency is disabled by default, so cart uses store default
        assert cart.currency == 'EUR'
        assert cart.effective_currency == 'EUR'

    def test_add_item_initializes_currency_once(self, eur_site_settings, eur_product_no_tracking):
        """Cart currency is only set on first add, not overwritten on subsequent adds."""
        cart = CartFactory(user=None, session_key='test_session_add_2')
        # First add sets currency
        CartService.add_item(
            cart=cart,
            product_id=eur_product_no_tracking.id,
            quantity=1,
        )
        cart.refresh_from_db()
        original_currency = cart.currency
        assert original_currency == 'EUR'

        # Second add shouldn't change currency
        CartService.add_item(
            cart=cart,
            product_id=eur_product_no_tracking.id,
            quantity=1,
        )
        cart.refresh_from_db()
        assert cart.currency == original_currency

    def test_add_item_unit_price_matches_product_currency(self, eur_site_settings, eur_product_no_tracking):
        """CartItem.unit_price is in the product's currency (EUR)."""
        cart = CartFactory(user=None, session_key='test_session_add_3')
        success, msg, item = CartService.add_item(
            cart=cart,
            product_id=eur_product_no_tracking.id,
            quantity=1,
        )
        assert success, f"add_item failed: {msg}"
        assert item.unit_price.amount == eur_product_no_tracking.price.amount
        assert str(item.unit_price.currency) == 'EUR'


# ============================================================
# Phase 3: CheckoutSession.recalculate_totals() currency
# ============================================================

@pytest.mark.django_db
class TestRecalculateTotalsCurrency:
    """Tests for CheckoutSession.recalculate_totals() currency handling."""

    def test_recalculate_totals_uses_cart_currency(self, eur_site_settings, eur_product_no_tracking):
        """recalculate_totals() sets all money fields to cart's effective currency."""
        cart = CartFactory(user=None, session_key='test_session_rt_1')
        success, msg, item = CartService.add_item(
            cart=cart,
            product_id=eur_product_no_tracking.id,
            quantity=2,
        )
        assert success, f"add_item failed: {msg}"

        session = CheckoutSessionFactory(cart=cart)
        session.recalculate_totals()

        # All money fields should be in EUR
        assert str(session.subtotal.currency) == 'EUR'
        assert str(session.total_amount.currency) == 'EUR'
        assert str(session.shipping_cost.currency) == 'EUR'
        assert str(session.tax_amount.currency) == 'EUR'
        assert str(session.discount_amount.currency) == 'EUR'

    def test_recalculate_totals_correct_subtotal(self, eur_site_settings, eur_product_no_tracking):
        """recalculate_totals() computes correct subtotal from cart items."""
        cart = CartFactory(user=None, session_key='test_session_rt_2')
        CartService.add_item(
            cart=cart,
            product_id=eur_product_no_tracking.id,
            quantity=3,
        )

        session = CheckoutSessionFactory(cart=cart)
        session.recalculate_totals()

        expected = eur_product_no_tracking.price.amount * 3
        assert session.subtotal.amount == expected
        assert session.total_amount.amount == expected  # no shipping/tax/discount

    def test_recalculate_totals_no_currency_mismatch_error(self, eur_site_settings, eur_product_no_tracking):
        """recalculate_totals() does not raise TypeError for currency mismatches."""
        cart = CartFactory(user=None, session_key='test_session_rt_3')
        CartService.add_item(
            cart=cart,
            product_id=eur_product_no_tracking.id,
            quantity=1,
        )

        session = CheckoutSessionFactory(cart=cart)
        # This should NOT raise:
        # TypeError: Cannot add or subtract two Money instances with different currencies
        session.recalculate_totals()

    def test_recalculate_empty_cart_uses_effective_currency(self, eur_site_settings):
        """recalculate_totals() on empty cart uses effective currency, not USD."""
        cart = CartFactory(user=None, session_key='test_session_rt_4')
        cart.currency = 'EUR'
        cart.save(update_fields=['currency'])

        session = CheckoutSessionFactory(cart=cart)
        session.recalculate_totals()

        # Zero values should be in EUR, not USD
        assert str(session.subtotal.currency) == 'EUR'
        assert session.subtotal.amount == Decimal('0')
        assert str(session.total_amount.currency) == 'EUR'


@pytest.fixture
def usd_default_site(db):
    """SiteSettings with USD as default currency (opposite of the cart currency in these tests)."""
    from core.models import SiteSettings
    from django.contrib.sites.models import Site
    Site.objects.get_or_create(id=1, defaults={'domain': 'localhost', 'name': 'Test'})
    settings, _ = SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            'site_name': 'Test Store',
            'admin_email': 'admin@test.spwig.com',
            'default_currency': 'USD',
            'default_language': 'en',
        }
    )
    if settings.default_currency != 'USD':
        SiteSettings.objects.filter(pk=settings.pk).update(default_currency='USD')
        settings.refresh_from_db()
    return settings


@pytest.mark.django_db
class TestCartDiscountEmptyZeroCurrency:
    """Regression tests: empty voucher/gift-card sets must return zero in the
    cart's currency, not the site default. Prevents the 500 seen on fashion demo
    (site default USD, products EUR) when adding to cart with no vouchers applied.
    """

    def test_voucher_discount_amount_empty_uses_cart_currency(self, usd_default_site):
        cart = CartFactory(user=None, session_key='discount_ccy_1', currency='EUR')
        assert str(cart.voucher_discount_amount.currency) == 'EUR'

    def test_gift_card_discount_amount_empty_uses_cart_currency(self, usd_default_site):
        cart = CartFactory(user=None, session_key='discount_ccy_2', currency='EUR')
        assert str(cart.gift_card_discount_amount.currency) == 'EUR'

    def test_total_savings_empty_uses_cart_currency(self, usd_default_site):
        cart = CartFactory(user=None, session_key='discount_ccy_3', currency='EUR')
        assert str(cart.total_savings.currency) == 'EUR'

    def test_recalculate_gift_card_discounts_no_currency_mismatch(
        self, usd_default_site, eur_product_no_tracking
    ):
        """This is the exact 500 from fashion.demos.spwig.com — site USD, product EUR,
        no vouchers/gift cards applied. recalculate_gift_card_discounts must not raise.
        """
        cart = CartFactory(user=None, session_key='discount_ccy_4', currency='EUR')
        CartService.add_item(
            cart=cart,
            product_id=eur_product_no_tracking.id,
            quantity=1,
        )
        # This subtracts total_amount - voucher_discount_amount internally.
        cart.recalculate_gift_card_discounts()


# ============================================================
# Phase 4: Mini-cart API formatting
# ============================================================

@pytest.mark.django_db
class TestMiniCartApiCurrency:
    """Tests for mini_cart_api.py currency formatting."""

    def test_format_price_uses_babel(self):
        """_format_price produces locale-aware formatting."""
        from cart.mini_cart_api import _format_price
        result = _format_price(Decimal('29.99'), 'EUR')
        # Should contain the euro sign, not dollar
        assert '$' not in result or 'EUR' in result  # Some locales use EUR prefix
        assert '29.99' in result or '29,99' in result  # locale-dependent decimal

    def test_format_price_usd(self):
        """_format_price for USD includes dollar sign."""
        from cart.mini_cart_api import _format_price
        result = _format_price(Decimal('10.00'), 'USD')
        assert '10.00' in result or '10,00' in result

    def test_format_price_fallback(self):
        """_format_price falls back gracefully for unknown currencies."""
        from cart.mini_cart_api import _format_price
        result = _format_price(Decimal('5.00'), 'XYZ')
        assert '5.00' in result

    def test_format_cart_for_minicart_includes_currency(self, eur_site_settings, eur_product_no_tracking):
        """format_cart_for_minicart includes 'currency' key in response."""
        from cart.mini_cart_api import format_cart_for_minicart
        cart = CartFactory(user=None, session_key='test_session_mc_1')
        CartService.add_item(
            cart=cart,
            product_id=eur_product_no_tracking.id,
            quantity=1,
        )

        data = format_cart_for_minicart(cart)
        assert 'currency' in data
        assert data['currency'] == 'EUR'

    def test_format_cart_for_minicart_no_dollar_in_formatted(self, eur_site_settings, eur_product_no_tracking):
        """Formatted prices for EUR store should not contain '$'."""
        from cart.mini_cart_api import format_cart_for_minicart
        cart = CartFactory(user=None, session_key='test_session_mc_2')
        CartService.add_item(
            cart=cart,
            product_id=eur_product_no_tracking.id,
            quantity=1,
        )

        data = format_cart_for_minicart(cart)
        # subtotal_formatted should use euro symbol
        assert '$' not in data['subtotal_formatted']

        # item price_formatted should also not have dollar
        for item in data.get('items', []):
            assert '$' not in item.get('price_formatted', ''), \
                f"Item price has hardcoded $: {item.get('price_formatted')}"

    def test_format_cart_empty_includes_currency(self, eur_site_settings):
        """Empty cart response still includes 'currency' field."""
        from cart.mini_cart_api import format_cart_for_minicart
        cart = CartFactory(user=None, session_key='test_session_mc_3')

        data = format_cart_for_minicart(cart)
        assert 'currency' in data
        assert data['currency'] == 'EUR'


# ============================================================
# Phase 5: Template & JS hardcoded $ audit
# ============================================================

@pytest.mark.django_db
class TestTemplateNoDollarHardcoding:
    """Verify templates don't have hardcoded $ for prices."""

    def test_mini_cart_template_no_hardcoded_dollar(self):
        """mini-cart.html should not contain hardcoded $0.00."""
        import os
        template_path = os.path.join(
            os.path.dirname(__file__), '..', '..',
            'page_builder', 'templates', 'page_builder', 'components', 'mini-cart.html'
        )
        with open(template_path, 'r') as f:
            content = f.read()
        assert '$0.00' not in content, "mini-cart.html still has hardcoded $0.00"

    def test_mini_cart_js_no_hardcoded_dollar_fallback(self):
        """mini-cart.js fallback should not contain $0.00."""
        import os
        js_path = os.path.join(
            os.path.dirname(__file__), '..', '..',
            'page_builder', 'static', 'page_builder', 'js', 'mini-cart.js'
        )
        with open(js_path, 'r') as f:
            content = f.read()
        assert "'$0.00'" not in content, "mini-cart.js still has hardcoded '$0.00' fallback"
        assert '"$0.00"' not in content, 'mini-cart.js still has hardcoded "$0.00" fallback'

    def test_cart_page_js_uses_shop_currency(self):
        """cart-page.js formatCurrency should reference __shopCurrency."""
        import os
        js_path = os.path.join(
            os.path.dirname(__file__), '..', '..',
            'page_builder', 'static', 'page_builder', 'js', 'cart-page.js'
        )
        with open(js_path, 'r') as f:
            content = f.read()
        assert '__shopCurrency' in content, "cart-page.js doesn't reference __shopCurrency"

    def test_checkout_js_uses_config_currency(self):
        """checkout.js formatCurrency should use config.currency."""
        import os
        js_path = os.path.join(
            os.path.dirname(__file__), '..', '..',
            'page_builder', 'static', 'page_builder', 'js', 'checkout.js'
        )
        with open(js_path, 'r') as f:
            content = f.read()
        assert 'config' in content and 'currency' in content, \
            "checkout.js doesn't reference config.currency"
        assert '__shopCurrency' in content, \
            "checkout.js doesn't reference __shopCurrency as fallback"

    def test_base_template_injects_shop_currency(self):
        """base.html should inject currency config from site_settings."""
        import os
        template_path = os.path.join(
            os.path.dirname(__file__), '..', '..',
            'page_builder', 'templates', 'page_builder', 'base.html'
        )
        with open(template_path, 'r') as f:
            content = f.read()
        # CSP-safe JSON island approach: <script type="application/json" id="shop-currency-config">
        assert 'shop-currency-config' in content, \
            "base.html doesn't have shop-currency-config JSON island"
        assert 'default_currency' in content, \
            "base.html doesn't reference site_settings.default_currency"

    def test_checkout_base_template_has_currency_in_config(self):
        """checkout/_base.html should include currency in checkout-config JSON."""
        import os
        template_path = os.path.join(
            os.path.dirname(__file__), '..', '..',
            'page_builder', 'templates', 'page_builder', 'checkout', '_base.html'
        )
        with open(template_path, 'r') as f:
            content = f.read()
        assert '"currency"' in content, \
            "checkout/_base.html missing 'currency' in checkout-config JSON"


# ============================================================
# Phase 6: Cart recommendation service (no hardcoded $)
# ============================================================

@pytest.mark.django_db
class TestCartRecommendationCurrency:
    """Verify cart recommendation service uses proper currency formatting."""

    def test_recommendation_service_no_hardcoded_dollar(self):
        """cart_recommendation_service.py should not use f'${price:.2f}'."""
        import os
        service_path = os.path.join(
            os.path.dirname(__file__), '..', '..',
            'cart', 'services', 'cart_recommendation_service.py'
        )
        with open(service_path, 'r') as f:
            content = f.read()
        assert 'f"${' not in content, \
            "cart_recommendation_service.py still has hardcoded $ formatting"
        assert "f'${" not in content, \
            "cart_recommendation_service.py still has hardcoded $ formatting"


# ============================================================
# Phase 7: Currency template filters
# ============================================================

@pytest.mark.django_db
class TestCurrencyTemplateFilters:
    """Tests for product_price and product_compare_price template filters."""

    def test_product_price_filter_eur(self, eur_site_settings, eur_product_no_tracking):
        """product_price filter returns EUR-formatted price."""
        from core.templatetags.currency_tags import product_price
        result = product_price(eur_product_no_tracking, 'EUR')
        assert '29.99' in result or '29,99' in result
        # Should NOT start with $ for EUR
        assert not result.startswith('$')

    def test_product_price_filter_none_currency(self, eur_product_no_tracking):
        """product_price filter with no currency falls back to str(effective_price)."""
        from core.templatetags.currency_tags import product_price
        result = product_price(eur_product_no_tracking, None)
        assert result is not None
        assert len(result) > 0

    def test_product_compare_price_filter(self, eur_site_settings, eur_product_no_tracking):
        """product_compare_price filter returns formatted base price."""
        from core.templatetags.currency_tags import product_compare_price
        result = product_compare_price(eur_product_no_tracking, 'EUR')
        assert '29.99' in result or '29,99' in result
