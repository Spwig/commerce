"""
Admin product management E2E tests.

Tests that merchants can create, edit, and manage products of all types
through the Django admin interface, plus inventory management.

The product admin uses a custom tabbed UI with conditional tabs that
appear based on product type selection.

Run with: pytest tests/e2e/test_admin_product_management.py -v
"""
import pytest
from decimal import Decimal
import uuid

from tests.factories import (
    ProductFactory, CategoryFactory, WarehouseFactory, SalesRegionFactory,
)

pytestmark = [pytest.mark.django_db(transaction=True), pytest.mark.e2e, pytest.mark.admin]


@pytest.fixture
def test_category(db):
    """Category for admin product tests."""
    return CategoryFactory(name='Admin Test Products', slug='admin-test-products')


# ============================================================
# Product Creation (one per type)
# ============================================================

class TestAdminProductCreation:
    """Tests for creating products of each type via admin UI.

    Each test fills basic info, sets category/status, fills price
    (which switches to Pricing tab), and saves.
    """

    def test_create_simple_product(self, admin_product, test_category):
        """Create a simple product via admin and verify it saves."""
        unique_id = uuid.uuid4().hex[:6]
        admin_product.go_to_product_add()

        admin_product.fill_basic_info(
            name=f'Simple Widget {unique_id}',
            sku=f'SIMPLE-{unique_id}',
            product_type='simple',
        )
        admin_product.set_category(test_category.id)
        admin_product.set_status('published')
        admin_product.fill_price('29.99')
        admin_product.save_product()

        msg = admin_product.get_success_message()
        assert 'was added successfully' in msg or 'was changed successfully' in msg

    def test_create_variable_product(self, admin_product, test_category):
        """Create a variable product via admin, verify Variations tab appears."""
        unique_id = uuid.uuid4().hex[:6]
        admin_product.go_to_product_add()

        admin_product.fill_basic_info(
            name=f'Variable Product {unique_id}',
            sku=f'VAR-{unique_id}',
            product_type='variable',
        )
        # Variations tab should now be visible
        assert admin_product.is_tab_visible('tab-variations')

        admin_product.set_category(test_category.id)
        admin_product.set_status('published')
        admin_product.fill_price('34.99')
        admin_product.save_and_continue()

        msg = admin_product.get_success_message()
        assert 'success' in msg.lower()
        # Should be on change form after save-and-continue
        assert '/change/' in admin_product.page.url

    def test_create_digital_product(self, admin_product, test_category):
        """Create a digital product via admin, verify Digital Assets tab appears."""
        unique_id = uuid.uuid4().hex[:6]
        admin_product.go_to_product_add()

        admin_product.fill_basic_info(
            name=f'Digital Product {unique_id}',
            sku=f'DIG-{unique_id}',
            product_type='digital',
        )
        # Digital Assets tab should now be visible
        assert admin_product.is_tab_visible('tab-digital-assets')

        admin_product.set_category(test_category.id)
        admin_product.set_status('published')
        admin_product.fill_price('14.99')
        admin_product.save_product()

        msg = admin_product.get_success_message()
        assert 'was added successfully' in msg or 'was changed successfully' in msg

    def test_create_bundle_product(self, admin_product, test_category):
        """Create a bundle product via admin, verify Bundle Items tab appears."""
        unique_id = uuid.uuid4().hex[:6]
        admin_product.go_to_product_add()

        admin_product.fill_basic_info(
            name=f'Bundle Product {unique_id}',
            sku=f'BDL-{unique_id}',
            product_type='bundle',
        )
        # Bundle Items tab should now be visible
        assert admin_product.is_tab_visible('tab-bundle-items')

        admin_product.set_category(test_category.id)
        admin_product.set_status('published')
        admin_product.fill_price('49.99')

        # Bundle pricing strategy field should be visible on the Pricing tab
        page = admin_product.page
        bundle_field = page.query_selector('#id_bundle_pricing_strategy')
        assert bundle_field is not None

        admin_product.save_product()
        msg = admin_product.get_success_message()
        assert 'was added successfully' in msg or 'was changed successfully' in msg

    def test_create_gift_card_product(self, admin_product, test_category):
        """Create a gift card product via admin, verify Gift Card tab appears."""
        unique_id = uuid.uuid4().hex[:6]
        admin_product.go_to_product_add()

        admin_product.fill_basic_info(
            name=f'Gift Card {unique_id}',
            sku=f'GC-{unique_id}',
            product_type='gift_card',
        )
        # Gift Card tab should now be visible
        assert admin_product.is_tab_visible('tab-gift-card')

        admin_product.set_category(test_category.id)
        admin_product.set_status('published')
        admin_product.fill_price('50.00')

        # Check gift card denomination field on the Gift Card tab
        admin_product.click_tab('tab-gift-card')
        page = admin_product.page
        denom_field = page.query_selector('#id_gift_card_denomination_type')
        assert denom_field is not None

        admin_product.save_product()
        msg = admin_product.get_success_message()
        assert 'was added successfully' in msg or 'was changed successfully' in msg

    def test_create_customizable_product(self, admin_product, test_category):
        """Create a customizable product via admin, verify Customization tab appears."""
        unique_id = uuid.uuid4().hex[:6]
        admin_product.go_to_product_add()

        admin_product.fill_basic_info(
            name=f'Custom Product {unique_id}',
            sku=f'CUST-{unique_id}',
            product_type='customizable',
        )
        # Customization tab should now be visible
        assert admin_product.is_tab_visible('tab-customization')

        admin_product.set_category(test_category.id)
        admin_product.set_status('published')
        admin_product.fill_price('19.99')

        # Check allow_customization checkbox on the Customization tab
        admin_product.click_tab('tab-customization')
        page = admin_product.page
        customization_field = page.query_selector('#id_allow_customization')
        assert customization_field is not None

        admin_product.save_product()
        msg = admin_product.get_success_message()
        assert 'was added successfully' in msg or 'was changed successfully' in msg

    def test_create_configurable_product(self, admin_product, test_category):
        """Create a configurable product via admin, verify Configuration tab appears."""
        unique_id = uuid.uuid4().hex[:6]
        admin_product.go_to_product_add()

        admin_product.fill_basic_info(
            name=f'Configurable Product {unique_id}',
            sku=f'CFG-{unique_id}',
            product_type='configurable',
        )
        # Configuration tab should now be visible
        assert admin_product.is_tab_visible('tab-configuration')

        admin_product.set_category(test_category.id)
        admin_product.set_status('published')
        admin_product.fill_price('999.99')

        # Note: configurator_pricing_strategy only shows on edit ({% if original %})
        # For add form, just verify the tab is visible and save succeeds
        admin_product.save_product()
        msg = admin_product.get_success_message()
        assert 'was added successfully' in msg or 'was changed successfully' in msg


# ============================================================
# Product Editing
# ============================================================

class TestAdminProductEditing:
    """Tests for editing existing products via admin UI."""

    def test_edit_product_name(self, admin_product, test_category):
        """Edit product name via admin, verify change persists."""
        product = ProductFactory(
            name='Original Name', slug='edit-name-test',
            category=test_category, price=Decimal('25.00'),
            status='published',
        )

        admin_product.go_to_product_edit(product.id)

        # Clear and refill name (on Basic Info tab, which is default)
        admin_product.page.fill('#id_name', '')
        admin_product.page.fill('#id_name', 'Updated Name')
        admin_product.save_product()

        msg = admin_product.get_success_message()
        assert 'success' in msg.lower()

        from catalog.models import Product
        product.refresh_from_db()
        assert product.name == 'Updated Name'

    def test_edit_product_price(self, admin_product, test_category):
        """Edit product price via admin."""
        product = ProductFactory(
            name='Price Edit Test', slug='edit-price-test',
            category=test_category, price=Decimal('25.00'),
            status='published',
        )

        admin_product.go_to_product_edit(product.id)

        # fill_price switches to Pricing tab automatically
        admin_product.fill_price('49.99')
        admin_product.save_product()

        msg = admin_product.get_success_message()
        assert 'success' in msg.lower()

        from catalog.models import Product
        product.refresh_from_db()
        # price is a Money field, compare the amount
        assert product.price.amount == Decimal('49.99')

    def test_edit_product_status_to_draft(self, admin_product, test_category):
        """Set product status to draft, verify it becomes unpublished."""
        product = ProductFactory(
            name='Draft Test', slug='draft-status-test',
            category=test_category, price=Decimal('25.00'),
            status='published',
        )

        admin_product.go_to_product_edit(product.id)
        admin_product.set_status('draft')
        admin_product.save_product()

        msg = admin_product.get_success_message()
        assert 'success' in msg.lower()

        from catalog.models import Product
        product.refresh_from_db()
        assert product.status == 'draft'


# ============================================================
# Inventory Management
# ============================================================

class TestAdminInventoryManagement:
    """Tests for stock/inventory management in admin."""

    def test_stock_item_inline_visible(self, admin_product, test_category):
        """Product with track_inventory=True shows StockItem inline on Inventory tab."""
        product = ProductFactory(
            name='Inventory Test', slug='inventory-test',
            category=test_category, price=Decimal('25.00'),
            status='published', track_inventory=True,
        )

        admin_product.go_to_product_edit(product.id)
        admin_product.click_tab('tab-inventory')

        page = admin_product.page
        # StockItem inline should be visible
        stock_inline = page.query_selector(
            '#stockitem_set-group, .inline-group'
        )
        assert stock_inline is not None

    def test_product_created_with_inventory_tracking(self, admin_product, test_category):
        """Create product with inventory tracking enabled, verify via ORM."""
        unique_id = uuid.uuid4().hex[:6]
        admin_product.go_to_product_add()

        admin_product.fill_basic_info(
            name=f'Tracked Product {unique_id}',
            sku=f'TRK-{unique_id}',
            product_type='simple',
        )
        admin_product.set_category(test_category.id)
        admin_product.set_status('published')
        admin_product.fill_price('25.00')

        # Switch to Inventory tab and enable tracking
        admin_product.click_tab('tab-inventory')
        page = admin_product.page
        track_checkbox = page.query_selector('#id_track_inventory')
        if track_checkbox:
            checked = page.evaluate('el => el.checked', track_checkbox)
            if not checked:
                track_checkbox.click()

        admin_product.save_product()

        msg = admin_product.get_success_message()
        assert 'success' in msg.lower()

        from catalog.models import Product
        product = Product.objects.get(sku=f'TRK-{unique_id}')
        assert product.track_inventory is True


# ============================================================
# Product List
# ============================================================

class TestAdminProductList:
    """Tests for the admin product list view.

    The product admin uses a custom card-based view with
    #products-container and .product-card elements.
    """

    def test_product_list_loads(self, admin_product, test_category):
        """Product list page loads and shows the products container."""
        ProductFactory(
            name='List Test A', slug='list-test-a',
            category=test_category, status='published',
        )
        ProductFactory(
            name='List Test B', slug='list-test-b',
            category=test_category, status='published',
        )

        admin_product.go_to_product_list()

        page = admin_product.page
        # Custom product list uses #products-container with .product-card cards
        products_container = page.query_selector('#products-container')
        assert products_container is not None

    def test_product_list_shows_product_names(self, admin_product, test_category):
        """Product list shows created product names."""
        ProductFactory(
            name='Findable Product', slug='findable-product',
            category=test_category, status='published',
        )

        admin_product.go_to_product_list()

        page_text = admin_product.page.text_content('body')
        assert 'Findable Product' in page_text
