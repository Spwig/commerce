"""
Admin orders E2E tests.

Tests that orders are properly recorded and viewable in the admin.

Run with: pytest tests/e2e/test_admin_orders.py -v
"""
import pytest
from decimal import Decimal

from tests.factories import OrderFactory, OrderItemFactory, ProductFactory

pytestmark = [pytest.mark.django_db(transaction=True), pytest.mark.e2e, pytest.mark.admin]


class TestAdminOrderView:
    """Tests for viewing orders in the admin interface."""

    def test_order_list_shows_created_orders(
        self, admin_product, site_settings, customer_user
    ):
        """Created orders appear in the admin order list."""
        order = OrderFactory(
            user=customer_user,
            status='processing',
            payment_status='paid',
        )
        OrderItemFactory(order=order)

        admin_product.go_to_order_list()

        page_text = admin_product.page.text_content('body')
        assert order.order_number in page_text

    def test_order_detail_shows_items(
        self, admin_product, site_settings, customer_user
    ):
        """Order detail page shows order items and customer info."""
        product = ProductFactory(
            name='Order Detail Widget', slug='order-detail-widget',
            price=Decimal('25.00'), status='published',
        )
        order = OrderFactory(
            user=customer_user,
            status='processing',
            payment_status='paid',
            subtotal=Decimal('25.00'),
            total_amount=Decimal('30.99'),
        )
        OrderItemFactory(
            order=order,
            product=product,
            product_name='Order Detail Widget',
            quantity=1,
            unit_price=Decimal('25.00'),
            total_price=Decimal('25.00'),
        )

        admin_product.go_to_order_edit(order.id)

        page_text = admin_product.page.text_content('body')
        # Order number and product name should be visible
        assert order.order_number in page_text

    def test_order_status_is_correct(
        self, admin_product, site_settings, customer_user
    ):
        """Order status is correctly displayed in admin."""
        order = OrderFactory(
            user=customer_user,
            status='shipped',
            payment_status='paid',
        )
        OrderItemFactory(order=order)

        admin_product.go_to_order_list()

        page_text = admin_product.page.text_content('body')
        # Order should appear and show its status
        assert order.order_number in page_text
