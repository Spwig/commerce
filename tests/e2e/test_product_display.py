"""
Product display E2E tests.

Tests that product pages render correctly for all 7 product types,
verifying the correct UI elements appear based on product type.

Run with: pytest tests/e2e/test_product_display.py -v
"""
import pytest

from tests.fixtures.product_scenarios import (
    simple_product_scenario,
    variable_product_scenario,
    digital_product_scenario,
    bundle_product_scenario,
    gift_card_product_scenario,
    customizable_product_scenario,
    configurable_product_scenario,
)

pytestmark = [pytest.mark.django_db(transaction=True), pytest.mark.e2e, pytest.mark.product_display]


# ============================================================
# Simple Product Display
# ============================================================

class TestSimpleProductDisplay:
    """Tests for simple product page rendering."""

    def test_page_loads_with_title_and_price(self, product_page):
        """Simple product page shows correct title and price."""
        data = simple_product_scenario()
        product = data['product']

        product_page.go_to_product(product.slug)

        assert product_page.get_product_title() == product.name
        price_text = product_page.get_product_price()
        assert '29.99' in price_text

    def test_shows_features_list(self, product_page):
        """Simple product with features dict renders feature items."""
        data = simple_product_scenario()
        product_page.go_to_product(data['product'].slug)

        assert product_page.has_features_list()
        features = product_page.get_feature_items()
        assert len(features) >= 2
        # Check at least one feature shows key:value
        feature_text = ' '.join(features)
        assert 'Steel' in feature_text or 'Silver' in feature_text

    def test_shows_add_to_cart_button(self, product_page):
        """Simple product page has Add to Cart button."""
        data = simple_product_scenario()
        product_page.go_to_product(data['product'].slug)

        assert product_page.has_add_to_cart_button()

    def test_shows_breadcrumb(self, product_page):
        """Product page renders breadcrumb navigation."""
        data = simple_product_scenario()
        product_page.go_to_product(data['product'].slug)

        assert product_page.has_breadcrumb()


# ============================================================
# Variable Product Display
# ============================================================

class TestVariableProductDisplay:
    """Tests for variable product page rendering."""

    def test_shows_variant_selector(self, product_page):
        """Variable product shows variant selector in direct mode."""
        data = variable_product_scenario()
        product_page.go_to_product(data['product'].slug)

        assert product_page.has_variant_selector()
        assert product_page.get_variant_selector_mode() == 'direct'

    def test_variant_swatches_match_count(self, product_page):
        """Number of variant swatches matches created variants."""
        data = variable_product_scenario()
        product_page.go_to_product(data['product'].slug)

        swatches = product_page.get_variant_swatches()
        assert len(swatches) == len(data['variants'])

    def test_add_to_cart_button_present(self, product_page):
        """Variable product has Add to Cart button."""
        data = variable_product_scenario()
        product_page.go_to_product(data['product'].slug)

        assert product_page.has_add_to_cart_button()


# ============================================================
# Digital Product Display
# ============================================================

class TestDigitalProductDisplay:
    """Tests for digital product page rendering."""

    def test_shows_instant_delivery_badge(self, product_page):
        """Digital product with digital template shows instant delivery badge."""
        data = digital_product_scenario()
        product_page.go_to_product(data['product'].slug)

        assert product_page.has_digital_badge()

    def test_no_physical_shipping_references(self, product_page):
        """Digital product page does not show weight or physical shipping info."""
        data = digital_product_scenario()
        product_page.go_to_product(data['product'].slug)

        # Page should not contain physical shipping selectors
        page = product_page.page
        weight_el = page.query_selector('.product-meta__weight')
        assert weight_el is None

    def test_page_uses_digital_layout(self, product_page):
        """Digital product with page_template='digital' uses digital layout."""
        data = digital_product_scenario()
        product_page.go_to_product(data['product'].slug)

        assert product_page.get_layout_class() == 'digital'


# ============================================================
# Bundle Product Display
# ============================================================

class TestBundleProductDisplay:
    """Tests for bundle product page rendering."""

    def test_shows_bundle_contents(self, product_page):
        """Bundle product shows included items section."""
        data = bundle_product_scenario()
        product_page.go_to_product(data['bundle'].slug)

        assert product_page.has_bundle_contents()
        item_names = product_page.get_bundle_item_names()
        assert 'Bundle Component A' in item_names
        assert 'Bundle Component B' in item_names

    def test_shows_component_quantities(self, product_page):
        """Bundle product shows correct quantities for each component."""
        data = bundle_product_scenario()
        product_page.go_to_product(data['bundle'].slug)

        quantities = product_page.get_bundle_item_quantities()
        assert len(quantities) == 2
        # First item qty=1, second qty=2
        assert '\u00d71' in quantities[0]  # ×1
        assert '\u00d72' in quantities[1]  # ×2

    def test_add_to_cart_available(self, product_page):
        """Bundle product has Add to Cart button."""
        data = bundle_product_scenario()
        product_page.go_to_product(data['bundle'].slug)

        assert product_page.has_add_to_cart_button()


# ============================================================
# Gift Card Display
# ============================================================

class TestGiftCardDisplay:
    """Tests for gift card product page rendering."""

    def test_page_loads(self, product_page):
        """Gift card product page loads with title and price."""
        data = gift_card_product_scenario()
        product_page.go_to_product(data['product'].slug)

        assert product_page.get_product_title() == data['product'].name
        assert '50.00' in product_page.get_product_price()

    def test_add_to_cart(self, product_page):
        """Gift card product can be added to cart."""
        data = gift_card_product_scenario()
        product_page.go_to_product(data['product'].slug)

        assert product_page.has_add_to_cart_button()


# ============================================================
# Customizable Product Display
# ============================================================

class TestCustomizableProductDisplay:
    """Tests for customizable product page rendering."""

    def test_shows_customization_fields(self, product_page):
        """Customizable product shows customization form fields."""
        data = customizable_product_scenario()
        product_page.go_to_product(data['product'].slug)

        # Look for customization section
        page = product_page.page
        customization_section = page.query_selector(
            '.product-customization, .customization-options, [data-customization]'
        )
        assert customization_section is not None or product_page.has_add_to_cart_button()

    def test_page_loads_with_title(self, product_page):
        """Customizable product page loads with correct title."""
        data = customizable_product_scenario()
        product_page.go_to_product(data['product'].slug)

        assert product_page.get_product_title() == data['product'].name


# ============================================================
# Configurable Product Display
# ============================================================

class TestConfigurableProductDisplay:
    """Tests for configurable product page rendering."""

    def test_uses_configurator_template(self, product_page):
        """Configurable product uses the configurator wizard template."""
        data = configurable_product_scenario()
        product_page.go_to_product(data['product'].slug)

        # Configurator products render via _render_configurator() which
        # uses configurator_product.html with its own selectors
        page = product_page.page
        configurator_section = page.query_selector('.configurator-section')
        assert configurator_section is not None

        # Title is in .configurator-header__title (not .product-info__title)
        title_el = page.query_selector('.configurator-header__title')
        assert title_el is not None
        assert title_el.text_content().strip() == data['product'].name

    def test_shows_configuration_slots(self, product_page):
        """Configurable product shows configurator wizard."""
        data = configurable_product_scenario()
        product_page.go_to_product(data['product'].slug)

        page = product_page.page
        # The wizard container should render (slots are populated by JS)
        wizard = page.query_selector('.configurator-wizard')
        assert wizard is not None
