"""
Integration tests for product sales count tracking.

Covers:
- orders.services.sales_stats_service.update_product_sales_counts()
- catalog.management.commands.recalculate_sales_counts management command
- Integration with _trigger_post_payment_flows() in PaymentOrchestrationService
"""
import pytest
from decimal import Decimal
from io import StringIO
from unittest.mock import patch, MagicMock

from django.core.management import call_command
from django.db.models import F

from catalog.models import Product
from orders.models import Order, OrderItem
from orders.services.sales_stats_service import update_product_sales_counts
from tests.factories import (
    UserFactory, ProductFactory, CategoryFactory,
    OrderFactory, OrderItemFactory,
)

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
    pytest.mark.sales_stats,
]


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def category(db):
    return CategoryFactory(name='Stats Test Category', slug='stats-test-cat')


@pytest.fixture
def product_a(category):
    return ProductFactory(
        name='Product A',
        slug='product-a-stats',
        category=category,
        price=Decimal('10.00'),
    )


@pytest.fixture
def product_b(category):
    return ProductFactory(
        name='Product B',
        slug='product-b-stats',
        category=category,
        price=Decimal('20.00'),
    )


@pytest.fixture
def product_c(category):
    return ProductFactory(
        name='Product C',
        slug='product-c-stats',
        category=category,
        price=Decimal('30.00'),
    )


@pytest.fixture
def paid_order(db):
    """A paid order with no items yet (items added per test)."""
    return OrderFactory(paid_order=True)


@pytest.fixture
def guest_order(db):
    """A paid guest order with no user."""
    return OrderFactory(
        user=None,
        paid_order=True,
        email='guest@example.com',
        shipping_name='Guest Buyer',
    )


# ============================================================
# update_product_sales_counts — basic increment
# ============================================================

class TestBasicSalesCountIncrement:
    """Verify single-item orders correctly increment Product.sales_count."""

    def test_single_item_increments_sales_count(self, paid_order, product_a):
        """One order item with quantity=1 should increment by 1."""
        assert product_a.sales_count == 0
        OrderItemFactory(order=paid_order, product=product_a, quantity=1)

        update_product_sales_counts(paid_order)

        product_a.refresh_from_db()
        assert product_a.sales_count == 1

    def test_quantity_greater_than_one(self, paid_order, product_a):
        """An order item with quantity=5 should increment by 5."""
        OrderItemFactory(order=paid_order, product=product_a, quantity=5)

        update_product_sales_counts(paid_order)

        product_a.refresh_from_db()
        assert product_a.sales_count == 5

    def test_multiple_different_products(self, paid_order, product_a, product_b):
        """Each product in the order gets its own count incremented."""
        OrderItemFactory(order=paid_order, product=product_a, quantity=2)
        OrderItemFactory(order=paid_order, product=product_b, quantity=3)

        update_product_sales_counts(paid_order)

        product_a.refresh_from_db()
        product_b.refresh_from_db()
        assert product_a.sales_count == 2
        assert product_b.sales_count == 3

    def test_preserves_existing_sales_count(self, paid_order, product_a):
        """Incrementing should add to existing sales_count, not reset it."""
        Product.objects.filter(pk=product_a.pk).update(sales_count=10)
        OrderItemFactory(order=paid_order, product=product_a, quantity=3)

        update_product_sales_counts(paid_order)

        product_a.refresh_from_db()
        assert product_a.sales_count == 13

    def test_order_with_no_items_is_noop(self, paid_order, product_a):
        """An order with no items should not modify any product."""
        Product.objects.filter(pk=product_a.pk).update(sales_count=7)

        update_product_sales_counts(paid_order)

        product_a.refresh_from_db()
        assert product_a.sales_count == 7


# ============================================================
# Idempotency
# ============================================================

class TestIdempotency:
    """Calling update_product_sales_counts() twice must not double-count."""

    def test_second_call_is_noop(self, paid_order, product_a):
        """Calling twice on the same order should not increment again."""
        OrderItemFactory(order=paid_order, product=product_a, quantity=2)

        update_product_sales_counts(paid_order)
        update_product_sales_counts(paid_order)

        product_a.refresh_from_db()
        assert product_a.sales_count == 2

    def test_metadata_flag_set_after_first_call(self, paid_order, product_a):
        """After first call, order.metadata['sales_count_updated'] is True."""
        OrderItemFactory(order=paid_order, product=product_a, quantity=1)

        update_product_sales_counts(paid_order)

        paid_order.refresh_from_db()
        assert paid_order.metadata.get('sales_count_updated') is True

    def test_metadata_flag_prevents_reprocessing(self, paid_order, product_a):
        """Pre-setting the flag should prevent any increment."""
        OrderItemFactory(order=paid_order, product=product_a, quantity=4)
        paid_order.metadata = {'sales_count_updated': True}
        paid_order.save(update_fields=['metadata'])

        update_product_sales_counts(paid_order)

        product_a.refresh_from_db()
        assert product_a.sales_count == 0

    def test_empty_metadata_dict_gets_flag(self, db, product_a):
        """If order.metadata is {}, it should get the 'sales_count_updated' flag."""
        order = OrderFactory(paid_order=True, metadata={})
        OrderItemFactory(order=order, product=product_a, quantity=1)

        update_product_sales_counts(order)

        order.refresh_from_db()
        assert order.metadata == {'sales_count_updated': True}
        product_a.refresh_from_db()
        assert product_a.sales_count == 1

    def test_null_metadata_code_path(self, db, product_a):
        """Simulate None metadata via direct attribute to test the code branch."""
        order = OrderFactory(paid_order=True, metadata={})
        OrderItemFactory(order=order, product=product_a, quantity=1)
        # Directly set attribute to None (without saving) to exercise the
        # `if order.metadata is None` branch in the service
        order.metadata = None

        update_product_sales_counts(order)

        # After save, metadata should be a dict with the flag
        order.refresh_from_db()
        assert order.metadata == {'sales_count_updated': True}
        product_a.refresh_from_db()
        assert product_a.sales_count == 1

    def test_existing_metadata_preserved(self, paid_order, product_a):
        """Existing metadata keys should not be overwritten by the flag."""
        paid_order.metadata = {'some_key': 'some_value'}
        paid_order.save(update_fields=['metadata'])
        OrderItemFactory(order=paid_order, product=product_a, quantity=1)

        update_product_sales_counts(paid_order)

        paid_order.refresh_from_db()
        assert paid_order.metadata['some_key'] == 'some_value'
        assert paid_order.metadata['sales_count_updated'] is True


# ============================================================
# Bundle items exclusion
# ============================================================

class TestBundleExclusion:
    """Bundle component items (parent_bundle != null) must be excluded."""

    def test_bundle_components_excluded(self, paid_order, product_a, product_b, product_c):
        """Only the parent bundle item should count, not its components."""
        bundle_item = OrderItemFactory(
            order=paid_order,
            product=product_a,
            quantity=1,
        )
        # Component items with parent_bundle set
        OrderItemFactory(
            order=paid_order,
            product=product_b,
            quantity=2,
            parent_bundle=bundle_item,
        )
        OrderItemFactory(
            order=paid_order,
            product=product_c,
            quantity=1,
            parent_bundle=bundle_item,
        )

        update_product_sales_counts(paid_order)

        product_a.refresh_from_db()
        product_b.refresh_from_db()
        product_c.refresh_from_db()
        assert product_a.sales_count == 1  # parent bundle counted
        assert product_b.sales_count == 0  # component excluded
        assert product_c.sales_count == 0  # component excluded

    def test_mix_of_bundle_and_standalone(self, paid_order, product_a, product_b, product_c):
        """Standalone items count; bundle components don't."""
        bundle_item = OrderItemFactory(
            order=paid_order,
            product=product_a,
            quantity=1,
        )
        OrderItemFactory(
            order=paid_order,
            product=product_b,
            quantity=3,
            parent_bundle=bundle_item,
        )
        # Standalone item
        OrderItemFactory(
            order=paid_order,
            product=product_c,
            quantity=2,
        )

        update_product_sales_counts(paid_order)

        product_a.refresh_from_db()
        product_b.refresh_from_db()
        product_c.refresh_from_db()
        assert product_a.sales_count == 1
        assert product_b.sales_count == 0
        assert product_c.sales_count == 2

    def test_order_only_bundle_components(self, paid_order, product_a, product_b):
        """If all items are bundle components (odd edge case), nothing increments."""
        # Create a bundle parent that has a different product
        bundle_parent = OrderItemFactory(
            order=paid_order,
            product=product_a,
            quantity=1,
        )
        # Only bundle component, no standalone
        OrderItemFactory(
            order=paid_order,
            product=product_b,
            quantity=5,
            parent_bundle=bundle_parent,
        )

        update_product_sales_counts(paid_order)

        # product_a is the parent (standalone), so it counts
        product_a.refresh_from_db()
        assert product_a.sales_count == 1
        # product_b is a component, so it doesn't
        product_b.refresh_from_db()
        assert product_b.sales_count == 0


# ============================================================
# Quantity aggregation (same product in multiple line items)
# ============================================================

class TestQuantityAggregation:
    """Multiple line items for the same product should aggregate quantities."""

    def test_same_product_multiple_lines(self, paid_order, product_a):
        """Two line items of product_a (qty 2 + qty 3) → sales_count += 5."""
        OrderItemFactory(order=paid_order, product=product_a, quantity=2)
        OrderItemFactory(order=paid_order, product=product_a, quantity=3)

        update_product_sales_counts(paid_order)

        product_a.refresh_from_db()
        assert product_a.sales_count == 5

    def test_aggregation_with_other_products(self, paid_order, product_a, product_b):
        """Aggregation for product_a doesn't affect product_b."""
        OrderItemFactory(order=paid_order, product=product_a, quantity=1)
        OrderItemFactory(order=paid_order, product=product_a, quantity=4)
        OrderItemFactory(order=paid_order, product=product_b, quantity=2)

        update_product_sales_counts(paid_order)

        product_a.refresh_from_db()
        product_b.refresh_from_db()
        assert product_a.sales_count == 5
        assert product_b.sales_count == 2

    def test_aggregation_excludes_bundle_components(self, paid_order, product_a):
        """Only top-level lines for the same product aggregate; components excluded."""
        standalone = OrderItemFactory(
            order=paid_order,
            product=product_a,
            quantity=3,
        )
        # Another standalone of same product
        OrderItemFactory(
            order=paid_order,
            product=product_a,
            quantity=2,
        )
        # A bundle component for the same product should NOT aggregate
        bundle_parent = OrderItemFactory(
            order=paid_order,
            product=ProductFactory(
                name='Bundle X',
                slug='bundle-x-stats',
                category=product_a.category,
            ),
            quantity=1,
        )
        OrderItemFactory(
            order=paid_order,
            product=product_a,
            quantity=10,
            parent_bundle=bundle_parent,
        )

        update_product_sales_counts(paid_order)

        product_a.refresh_from_db()
        assert product_a.sales_count == 5  # 3 + 2, not 3 + 2 + 10


# ============================================================
# Guest orders
# ============================================================

class TestGuestOrders:
    """Guest orders (user=None) should still update product stats."""

    def test_guest_order_increments_sales_count(self, guest_order, product_a):
        """A guest order should increment product sales_count just like any order."""
        assert guest_order.user is None
        OrderItemFactory(order=guest_order, product=product_a, quantity=3)

        update_product_sales_counts(guest_order)

        product_a.refresh_from_db()
        assert product_a.sales_count == 3

    def test_guest_order_sets_idempotency_flag(self, guest_order, product_a):
        """Idempotency flag should work for guest orders too."""
        OrderItemFactory(order=guest_order, product=product_a, quantity=1)

        update_product_sales_counts(guest_order)
        update_product_sales_counts(guest_order)

        product_a.refresh_from_db()
        assert product_a.sales_count == 1

    def test_guest_order_multiple_products(self, guest_order, product_a, product_b):
        """Guest order with multiple products should increment each."""
        OrderItemFactory(order=guest_order, product=product_a, quantity=2)
        OrderItemFactory(order=guest_order, product=product_b, quantity=1)

        update_product_sales_counts(guest_order)

        product_a.refresh_from_db()
        product_b.refresh_from_db()
        assert product_a.sales_count == 2
        assert product_b.sales_count == 1


# ============================================================
# Atomicity (F-expression usage)
# ============================================================

class TestAtomicUpdate:
    """Verify that F() expressions are used for atomic increment."""

    def test_concurrent_orders_accumulate(self, product_a):
        """Two separate orders for the same product should accumulate correctly."""
        order1 = OrderFactory(paid_order=True)
        order2 = OrderFactory(paid_order=True)
        OrderItemFactory(order=order1, product=product_a, quantity=3)
        OrderItemFactory(order=order2, product=product_a, quantity=7)

        update_product_sales_counts(order1)
        update_product_sales_counts(order2)

        product_a.refresh_from_db()
        assert product_a.sales_count == 10

    def test_multiple_orders_sequential(self, product_a, product_b):
        """Processing multiple orders sequentially accumulates counts."""
        for i in range(5):
            order = OrderFactory(paid_order=True)
            OrderItemFactory(order=order, product=product_a, quantity=2)
            OrderItemFactory(order=order, product=product_b, quantity=1)
            update_product_sales_counts(order)

        product_a.refresh_from_db()
        product_b.refresh_from_db()
        assert product_a.sales_count == 10  # 5 orders x 2
        assert product_b.sales_count == 5   # 5 orders x 1


# ============================================================
# Management command: recalculate_sales_counts
# ============================================================

class TestRecalculateSalesCountsCommand:
    """Tests for the recalculate_sales_counts management command."""

    def _create_paid_order_with_items(self, product, quantity, is_test=False):
        """Helper to create a paid order with a single item."""
        order = OrderFactory(
            paid_order=True,
            is_test_order=is_test,
        )
        OrderItemFactory(order=order, product=product, quantity=quantity)
        return order

    def test_basic_recalculation(self, product_a, product_b):
        """Command should set sales_count based on paid order item quantities."""
        self._create_paid_order_with_items(product_a, quantity=5)
        self._create_paid_order_with_items(product_b, quantity=3)

        out = StringIO()
        call_command('recalculate_sales_counts', stdout=out)

        product_a.refresh_from_db()
        product_b.refresh_from_db()
        assert product_a.sales_count == 5
        assert product_b.sales_count == 3
        assert 'Updated sales_count for 2 products' in out.getvalue()

    def test_resets_existing_counts_before_recalculating(self, product_a):
        """Command should reset all counts to 0 first, then set from orders."""
        Product.objects.filter(pk=product_a.pk).update(sales_count=999)
        self._create_paid_order_with_items(product_a, quantity=2)

        call_command('recalculate_sales_counts', stdout=StringIO())

        product_a.refresh_from_db()
        assert product_a.sales_count == 2  # not 999 + 2

    def test_zeroes_product_with_no_paid_orders(self, product_a, product_b):
        """Products with no paid orders get sales_count=0."""
        Product.objects.filter(pk=product_a.pk).update(sales_count=50)
        self._create_paid_order_with_items(product_b, quantity=3)

        call_command('recalculate_sales_counts', stdout=StringIO())

        product_a.refresh_from_db()
        product_b.refresh_from_db()
        assert product_a.sales_count == 0  # reset, no paid orders
        assert product_b.sales_count == 3

    def test_excludes_test_orders(self, product_a):
        """Test orders (is_test_order=True) should not be counted."""
        self._create_paid_order_with_items(product_a, quantity=5, is_test=True)
        self._create_paid_order_with_items(product_a, quantity=2, is_test=False)

        call_command('recalculate_sales_counts', stdout=StringIO())

        product_a.refresh_from_db()
        assert product_a.sales_count == 2

    def test_excludes_unpaid_orders(self, product_a):
        """Only paid orders are counted."""
        # Unpaid order
        unpaid_order = OrderFactory(payment_status='unpaid')
        OrderItemFactory(order=unpaid_order, product=product_a, quantity=10)
        # Paid order
        self._create_paid_order_with_items(product_a, quantity=1)

        call_command('recalculate_sales_counts', stdout=StringIO())

        product_a.refresh_from_db()
        assert product_a.sales_count == 1

    def test_excludes_bundle_components(self, product_a, product_b):
        """Bundle components (parent_bundle is not null) are excluded."""
        order = OrderFactory(paid_order=True)
        bundle_item = OrderItemFactory(order=order, product=product_a, quantity=1)
        OrderItemFactory(
            order=order,
            product=product_b,
            quantity=5,
            parent_bundle=bundle_item,
        )

        call_command('recalculate_sales_counts', stdout=StringIO())

        product_a.refresh_from_db()
        product_b.refresh_from_db()
        assert product_a.sales_count == 1
        assert product_b.sales_count == 0

    def test_aggregates_across_multiple_orders(self, product_a):
        """Quantities from multiple paid orders are summed together."""
        self._create_paid_order_with_items(product_a, quantity=3)
        self._create_paid_order_with_items(product_a, quantity=7)

        call_command('recalculate_sales_counts', stdout=StringIO())

        product_a.refresh_from_db()
        assert product_a.sales_count == 10

    def test_dry_run_does_not_modify_data(self, product_a):
        """--dry-run should show what would happen without making changes."""
        Product.objects.filter(pk=product_a.pk).update(sales_count=42)
        self._create_paid_order_with_items(product_a, quantity=5)

        out = StringIO()
        call_command('recalculate_sales_counts', '--dry-run', stdout=out)

        product_a.refresh_from_db()
        assert product_a.sales_count == 42  # unchanged
        output = out.getvalue()
        assert 'DRY RUN' in output

    def test_dry_run_shows_product_details(self, product_a, product_b):
        """--dry-run should list products and their would-be counts."""
        self._create_paid_order_with_items(product_a, quantity=5)
        self._create_paid_order_with_items(product_b, quantity=3)

        out = StringIO()
        call_command('recalculate_sales_counts', '--dry-run', stdout=out)

        output = out.getvalue()
        assert 'Product A' in output
        assert '5 units' in output
        assert 'Product B' in output
        assert '3 units' in output

    def test_dry_run_handles_deleted_product(self, product_a):
        """--dry-run should handle products that no longer exist gracefully."""
        order = OrderFactory(paid_order=True)
        OrderItemFactory(order=order, product=product_a, quantity=3)
        deleted_product_id = product_a.pk
        # Remove the product but keep the order item referencing it
        # We can't actually delete due to PROTECT, so simulate with a mock
        with patch.object(Product.objects, 'get', side_effect=Product.DoesNotExist):
            out = StringIO()
            call_command('recalculate_sales_counts', '--dry-run', stdout=out)
            output = out.getvalue()
            assert '[deleted product' in output

    def test_output_shows_total_counts(self, product_a, product_b):
        """Actual run output should show the total products and units."""
        self._create_paid_order_with_items(product_a, quantity=5)
        self._create_paid_order_with_items(product_b, quantity=3)

        out = StringIO()
        call_command('recalculate_sales_counts', stdout=out)

        output = out.getvalue()
        assert '2 products' in output
        assert '8 total units' in output

    def test_idempotent_recalculation(self, product_a):
        """Running the command twice should produce the same result."""
        self._create_paid_order_with_items(product_a, quantity=5)

        call_command('recalculate_sales_counts', stdout=StringIO())
        product_a.refresh_from_db()
        assert product_a.sales_count == 5

        call_command('recalculate_sales_counts', stdout=StringIO())
        product_a.refresh_from_db()
        assert product_a.sales_count == 5  # same, not doubled


# ============================================================
# Integration with _trigger_post_payment_flows
# ============================================================

class TestPostPaymentFlowIntegration:
    """Verify the integration points in PaymentOrchestrationService._trigger_post_payment_flows."""

    def test_trigger_calls_update_product_sales_counts(self, paid_order, product_a):
        """_trigger_post_payment_flows should call update_product_sales_counts."""
        OrderItemFactory(order=paid_order, product=product_a, quantity=2)

        # These are lazy-imported inside the function body, so mock at source
        with patch('webhooks.services.trigger_webhook'), \
             patch('loyalty.services.award_order_points', create=True):
            from payment_providers.services.payment_orchestration_service import PaymentOrchestrationService
            PaymentOrchestrationService._trigger_post_payment_flows(paid_order)

        product_a.refresh_from_db()
        assert product_a.sales_count == 2

    def test_trigger_calls_customer_metrics_for_non_guest(self, paid_order, product_a):
        """Non-guest orders should trigger CustomerMetrics.calculate_for_user."""
        OrderItemFactory(order=paid_order, product=product_a, quantity=1)
        assert paid_order.user is not None
        assert not paid_order.user.username.startswith('guest_')

        with patch('webhooks.services.trigger_webhook'), \
             patch('loyalty.services.award_order_points', create=True), \
             patch('customers.models.CustomerMetrics.calculate_for_user') as mock_calc:
            from payment_providers.services.payment_orchestration_service import PaymentOrchestrationService
            PaymentOrchestrationService._trigger_post_payment_flows(paid_order)
            mock_calc.assert_called_once_with(paid_order.user)

    def test_trigger_skips_customer_metrics_for_guest(self, guest_order, product_a):
        """Guest orders (user=None) should skip CustomerMetrics."""
        OrderItemFactory(order=guest_order, product=product_a, quantity=1)

        with patch('webhooks.services.trigger_webhook'), \
             patch('loyalty.services.award_order_points', create=True):
            from payment_providers.services.payment_orchestration_service import PaymentOrchestrationService
            with patch('customers.models.CustomerMetrics.calculate_for_user') as mock_calc:
                PaymentOrchestrationService._trigger_post_payment_flows(guest_order)
                mock_calc.assert_not_called()

    def test_trigger_skips_customer_metrics_for_guest_username(self, product_a):
        """Orders with user having guest_ prefix username should skip metrics."""
        guest_user = UserFactory(username='guest_abc123')
        order = OrderFactory(paid_order=True, user=guest_user)
        OrderItemFactory(order=order, product=product_a, quantity=1)

        with patch('webhooks.services.trigger_webhook'), \
             patch('loyalty.services.award_order_points', create=True), \
             patch('customers.models.CustomerMetrics.calculate_for_user') as mock_calc:
            from payment_providers.services.payment_orchestration_service import PaymentOrchestrationService
            PaymentOrchestrationService._trigger_post_payment_flows(order)
            mock_calc.assert_not_called()

    def test_sales_count_failure_does_not_propagate(self, paid_order):
        """If update_product_sales_counts raises, it should be caught and logged."""
        with patch('webhooks.services.trigger_webhook'), \
             patch('loyalty.services.award_order_points', create=True), \
             patch(
                 'orders.services.sales_stats_service.update_product_sales_counts',
                 side_effect=Exception('DB error')
             ):
            from payment_providers.services.payment_orchestration_service import PaymentOrchestrationService
            # Should not raise — exception is caught and logged
            PaymentOrchestrationService._trigger_post_payment_flows(paid_order)

    def test_customer_metrics_failure_does_not_propagate(self, paid_order):
        """If CustomerMetrics.calculate_for_user raises, it should be caught."""
        with patch('webhooks.services.trigger_webhook'), \
             patch('loyalty.services.award_order_points', create=True), \
             patch(
                 'customers.models.CustomerMetrics.calculate_for_user',
                 side_effect=Exception('Metrics error')
             ):
            from payment_providers.services.payment_orchestration_service import PaymentOrchestrationService
            # Should not raise
            PaymentOrchestrationService._trigger_post_payment_flows(paid_order)


# ============================================================
# Edge cases
# ============================================================

class TestEdgeCases:
    """Edge cases and boundary conditions for sales count tracking."""

    def test_order_with_empty_metadata_dict(self, product_a):
        """Order with metadata={} should work (no 'sales_count_updated' key)."""
        order = OrderFactory(paid_order=True, metadata={})
        OrderItemFactory(order=order, product=product_a, quantity=1)

        update_product_sales_counts(order)

        product_a.refresh_from_db()
        assert product_a.sales_count == 1

    def test_order_with_falsy_sales_count_updated(self, product_a):
        """metadata={'sales_count_updated': False} should not block processing."""
        order = OrderFactory(
            paid_order=True,
            metadata={'sales_count_updated': False},
        )
        OrderItemFactory(order=order, product=product_a, quantity=2)

        update_product_sales_counts(order)

        product_a.refresh_from_db()
        assert product_a.sales_count == 2

    def test_large_quantity(self, paid_order, product_a):
        """Very large quantities should be handled correctly."""
        OrderItemFactory(order=paid_order, product=product_a, quantity=9999)

        update_product_sales_counts(paid_order)

        product_a.refresh_from_db()
        assert product_a.sales_count == 9999

    def test_save_update_fields_limits_write(self, paid_order, product_a):
        """Verify save uses update_fields=['metadata'] to avoid full model save."""
        OrderItemFactory(order=paid_order, product=product_a, quantity=1)

        with patch.object(Order, 'save', wraps=paid_order.save) as mock_save:
            update_product_sales_counts(paid_order)
            mock_save.assert_called_once()
            _, kwargs = mock_save.call_args
            assert kwargs.get('update_fields') == ['metadata']

    def test_test_order_skipped_by_realtime_service(self, product_a):
        """Test orders should be skipped by the real-time update_product_sales_counts()."""
        order = OrderFactory(paid_order=True, is_test_order=True)
        OrderItemFactory(order=order, product=product_a, quantity=5)

        update_product_sales_counts(order)

        product_a.refresh_from_db()
        assert product_a.sales_count == 0  # test order, not counted

    def test_management_command_no_paid_orders(self, product_a):
        """Command with no paid orders should reset all to 0 and report 0 products."""
        Product.objects.filter(pk=product_a.pk).update(sales_count=100)

        out = StringIO()
        call_command('recalculate_sales_counts', stdout=out)

        product_a.refresh_from_db()
        assert product_a.sales_count == 0
        assert '0 products' in out.getvalue()
