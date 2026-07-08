"""
Product template layout E2E tests.

Tests that each frontend product template renders the correct
layout structure and CSS classes.

Run with: pytest tests/e2e/test_product_templates.py -v
"""
import pytest
from tests.factories import ProductFactory, CategoryFactory
from decimal import Decimal

pytestmark = [pytest.mark.django_db(transaction=True), pytest.mark.e2e, pytest.mark.product_display]


@pytest.fixture
def template_product(db):
    """Create a simple product for template testing."""
    category = CategoryFactory(name='Template Test', slug='template-test')
    return ProductFactory(
        name='Template Test Product',
        slug='template-test-product',
        category=category,
        price=Decimal('49.99'),
        product_type='simple',
        status='published',
        weight=Decimal('1.0'),
        short_description='Product for testing page templates',
        page_template='',  # Will be overridden per test
    )


# ============================================================
# Classic Template
# ============================================================

class TestClassicTemplate:
    """Tests for the Classic product template (50/50 gallery + info)."""

    def test_classic_layout_class(self, product_page, template_product):
        """Default template renders with .product-layout--classic."""
        # Empty page_template defaults to classic
        template_product.page_template = ''
        template_product.save(update_fields=['page_template'])

        product_page.go_to_product(template_product.slug)

        assert product_page.get_layout_class() == 'classic'

    def test_classic_has_gallery_and_info(self, product_page, template_product):
        """Classic template has both gallery and info sections."""
        template_product.page_template = 'classic'
        template_product.save(update_fields=['page_template'])

        product_page.go_to_product(template_product.slug)

        page = product_page.page
        assert page.query_selector('.product-layout--classic') is not None
        assert page.query_selector('.product-info') is not None


# ============================================================
# Gallery Focus Template
# ============================================================

class TestGalleryFocusTemplate:
    """Tests for the Gallery Focus product template (60/40 with sticky sidebar)."""

    def test_gallery_focus_layout_class(self, product_page, template_product):
        """Gallery focus template renders correct layout class."""
        template_product.page_template = 'gallery_focus'
        template_product.save(update_fields=['page_template'])

        product_page.go_to_product(template_product.slug)

        assert product_page.get_layout_class() == 'gallery-focus'

    def test_gallery_focus_sidebar(self, product_page, template_product):
        """Gallery focus template has sidebar section."""
        template_product.page_template = 'gallery_focus'
        template_product.save(update_fields=['page_template'])

        product_page.go_to_product(template_product.slug)

        assert product_page.has_gallery_focus_sidebar()


# ============================================================
# Full Width Template
# ============================================================

class TestFullWidthTemplate:
    """Tests for the Full Width product template (hero gallery)."""

    def test_full_width_layout_class(self, product_page, template_product):
        """Full width template renders correct layout class."""
        template_product.page_template = 'full_width'
        template_product.save(update_fields=['page_template'])

        product_page.go_to_product(template_product.slug)

        assert product_page.get_layout_class() == 'full-width'

    def test_full_width_hero(self, product_page, template_product):
        """Full width template has hero gallery section."""
        template_product.page_template = 'full_width'
        template_product.save(update_fields=['page_template'])

        product_page.go_to_product(template_product.slug)

        assert product_page.has_hero_section()


# ============================================================
# Digital Template
# ============================================================

class TestDigitalTemplate:
    """Tests for the Digital product template (optimized for downloads)."""

    def test_digital_layout_class(self, product_page, template_product):
        """Digital template renders correct layout class."""
        template_product.page_template = 'digital'
        template_product.save(update_fields=['page_template'])

        product_page.go_to_product(template_product.slug)

        assert product_page.get_layout_class() == 'digital'

    def test_digital_features(self, product_page, template_product):
        """Digital template has digital-specific sections."""
        template_product.page_template = 'digital'
        template_product.save(update_fields=['page_template'])

        product_page.go_to_product(template_product.slug)

        page = product_page.page
        # Digital template renders its own info section with digital badges
        digital_layout = page.query_selector('.product-layout--digital')
        assert digital_layout is not None
