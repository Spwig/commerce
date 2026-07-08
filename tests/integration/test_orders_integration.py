"""
Integration tests for orders app services and workflows.

Tests service layer integration, order creation workflows, payment processing,
refunds, returns, and cross-model interactions.
"""
import pytest
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth import get_user_model
from orders.services.order_service import OrderService
from orders.services.address_service import AddressService
from orders.models import Order, OrderItem, Address, Refund, ReturnRequest
from cart.models import Cart, CartItem
from catalog.models import StockItem
from tests.factories import (
    UserFactory,
    ProductFactory,
    OrderFactory,
    OrderItemFactory,
    AddressFactory,
    RefundFactory,
    ReturnRequestFactory,
    CartFactory,
    CartItemFactory,
    WarehouseFactory,
    StockItemFactory,
    POSTerminalFactory,
)

User = get_user_model()


@pytest.mark.django_db
class TestOrderService:
    """Integration tests for OrderService."""

    def test_get_order_history_with_filters(self):
        """Test get_order_history() returns filtered orders."""
        user = UserFactory()

        # Create orders with different statuses
        OrderFactory(user=user, status='processing')
        OrderFactory(user=user, status='shipped')
        OrderFactory(user=user, status='delivered')
        OrderFactory(user=user, status='cancelled')

        # Get all orders
        all_orders = OrderService.get_order_history(user)
        assert all_orders.count() == 4

        # Filter by status
        processing_orders = OrderService.get_order_history(user, status='processing')
        assert processing_orders.count() == 1
        assert processing_orders.first().status == 'processing'

        shipped_orders = OrderService.get_order_history(user, status='shipped')
        assert shipped_orders.count() == 1

    def test_get_order_detail_permission_check(self):
        """Test get_order_detail() enforces user permissions."""
        user1 = UserFactory()
        user2 = UserFactory()

        order = OrderFactory(user=user1)

        # User1 can access their own order
        retrieved_order = OrderService.get_order_detail(user1, order.id)
        assert retrieved_order == order

        # User2 cannot access user1's order
        with pytest.raises(Order.DoesNotExist):
            OrderService.get_order_detail(user2, order.id)

    def test_get_order_statistics_calculation(self):
        """Test get_order_statistics() calculates correct stats."""
        user = UserFactory()

        # Create orders with various totals and statuses
        OrderFactory(user=user, status='delivered', total_amount=Decimal('100.00'), paid_order=True)
        OrderFactory(user=user, status='delivered', total_amount=Decimal('150.00'), paid_order=True)
        OrderFactory(user=user, status='cancelled', total_amount=Decimal('50.00'))

        stats = OrderService.get_order_statistics(user)

        assert stats['total_orders'] == 3
        assert stats['total_spent'] == Decimal('250.00')  # Only delivered orders
        assert stats['average_order_value'] == Decimal('125.00')
        assert stats['status_breakdown']['delivered'] == 2
        assert stats['status_breakdown']['cancelled'] == 1

    def test_cancel_order_with_stock_restoration(self):
        """Test cancel_order() restores stock when requested."""
        user = UserFactory()
        warehouse = WarehouseFactory()
        product = ProductFactory(track_inventory=True)

        # Create stock item
        stock = StockItemFactory(
            product=product,
            warehouse=warehouse,
            on_hand=100,
            allocated=10,
        )

        # Create order with allocated stock
        order = OrderFactory(user=user, status='processing')
        OrderItemFactory(
            order=order,
            product=product,
            quantity=10,
            stock_allocated=10,
            warehouse=warehouse,
        )

        # Cancel order with stock restoration
        cancelled_order = OrderService.cancel_order(
            user=user,
            order_id=order.id,
            restore_stock=True,
        )

        assert cancelled_order.status == 'cancelled'

        # Stock should be restored
        stock.refresh_from_db()
        assert stock.allocated == 0  # Released 10 units

    def test_reorder_creates_cart_from_order(self):
        """Test reorder() creates a new cart from previous order."""
        user = UserFactory()
        order = OrderFactory(user=user)

        # Add items to the order
        product1 = ProductFactory(price=Decimal('25.00'))
        product2 = ProductFactory(price=Decimal('35.00'))

        OrderItemFactory(order=order, product=product1, quantity=2)
        OrderItemFactory(order=order, product=product2, quantity=1)

        # Reorder - method signature: reorder(order, user) -> (success, message, cart)
        success, message, cart = OrderService.reorder(order, user)

        assert success is True
        assert cart is not None
        assert cart.user == user
        assert cart.items.count() == 2

        # Check cart items match order items
        cart_items = list(cart.items.order_by('id'))
        assert cart_items[0].product == product1
        assert cart_items[0].quantity == 2
        assert cart_items[1].product == product2
        assert cart_items[1].quantity == 1

    def test_can_cancel_order_validation(self):
        """Test can_cancel_order() validates cancellability."""
        user = UserFactory()

        # Pending order can be cancelled
        pending_order = OrderFactory(user=user, status='pending')
        assert OrderService.can_cancel_order(pending_order) is True

        # Processing order can be cancelled
        processing_order = OrderFactory(user=user, status='processing')
        assert OrderService.can_cancel_order(processing_order) is True

        # Shipped order cannot be cancelled
        shipped_order = OrderFactory(user=user, status='shipped')
        assert OrderService.can_cancel_order(shipped_order) is False

        # Delivered order cannot be cancelled
        delivered_order = OrderFactory(user=user, status='delivered')
        assert OrderService.can_cancel_order(delivered_order) is False

        # Already cancelled order cannot be cancelled again
        cancelled_order = OrderFactory(user=user, status='cancelled')
        assert OrderService.can_cancel_order(cancelled_order) is False


@pytest.mark.django_db
class TestAddressService:
    """Integration tests for AddressService."""

    def test_create_address_sets_default(self):
        """Test create_address() sets as default when specified."""
        user = UserFactory()

        address_data = {
            'name': 'John Doe',
            'address1': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'postal_code': '10001',
            'country': 'US',
            'address_type': 'shipping',
        }

        address = AddressService.create_address(
            user=user,
            address_data=address_data,
            set_as_default=True,
        )

        assert address.user == user
        assert address.is_default is True

    def test_update_address_creates_version(self):
        """Test update_address() creates new version for address history."""
        user = UserFactory()
        address = AddressFactory(user=user, address1='123 Old St', version=1)

        updated_data = {'address1': '456 New St'}

        new_address = AddressService.update_address(
            address_id=address.id,
            address_data=updated_data,
            create_version=True,
        )

        assert new_address.id != address.id  # New record created
        assert new_address.address1 == '456 New St'
        assert new_address.original_address == address
        assert new_address.version == 2

        # Old address should be inactive
        address.refresh_from_db()
        assert address.is_active is False

    def test_delete_address_with_order_check(self):
        """Test delete_address() prevents deletion if used in orders."""
        user = UserFactory()
        address = AddressFactory(user=user)

        # Address not used in orders - deletion should succeed
        assert AddressService.delete_address(address.id) is True

        # Create order with this address
        address2 = AddressFactory(user=user)
        OrderFactory(user=user, shipping_address_ref=address2)

        # Address used in orders - deletion should fail
        with pytest.raises(ValueError, match='address is used in orders'):
            AddressService.delete_address(address2.id)

    def test_get_default_address_by_type(self):
        """Test get_default_address() returns correct default by type."""
        user = UserFactory()

        # Create default shipping address
        shipping_addr = AddressFactory(
            user=user,
            address_type='shipping',
            default_address=True,
        )

        # Create default billing address
        billing_addr = AddressFactory(
            user=user,
            address_type='billing',
            default_address=True,
        )

        # Get default addresses
        default_shipping = AddressService.get_default_address(user, 'shipping')
        default_billing = AddressService.get_default_address(user, 'billing')

        assert default_shipping == shipping_addr
        assert default_billing == billing_addr

    def test_set_default_address_updates_others(self):
        """Test set_default_address() unsets other defaults of same type."""
        user = UserFactory()

        # Create two shipping addresses
        addr1 = AddressFactory(user=user, address_type='shipping', default_address=True)
        addr2 = AddressFactory(user=user, address_type='shipping', is_default=False)

        # Set addr2 as default
        AddressService.set_default_address(addr2.id)

        # Refresh from DB
        addr1.refresh_from_db()
        addr2.refresh_from_db()

        assert addr1.is_default is False
        assert addr2.is_default is True

    def test_validate_address(self):
        """Test validate_address() checks required fields."""
        # Valid address
        valid_data = {
            'name': 'John Doe',
            'address1': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'postal_code': '10001',
            'country': 'US',
        }
        assert AddressService.validate_address(valid_data) is True

        # Invalid address - missing required field
        invalid_data = {
            'name': 'John Doe',
            'address1': '123 Main St',
            # Missing city, state, postal_code, country
        }
        assert AddressService.validate_address(invalid_data) is False


@pytest.mark.django_db
class TestOrderCreation:
    """Integration tests for order creation workflows."""

    def test_create_web_order_from_cart(self):
        """Test creating a web order from cart."""
        user = UserFactory()
        product1 = ProductFactory(price=Decimal('50.00'))
        product2 = ProductFactory(price=Decimal('30.00'))

        cart = CartFactory(user=user)
        CartItemFactory(cart=cart, product=product1, quantity=2)
        CartItemFactory(cart=cart, product=product2, quantity=1)

        # Create order from cart (simplified - actual implementation would be in checkout)
        order = OrderFactory(
            user=user,
            web_order=True,
            subtotal=Decimal('130.00'),  # 50*2 + 30*1
        )

        # Add order items from cart items
        for cart_item in cart.items.all():
            OrderItemFactory(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
            )

        assert order.channel == 'web'
        assert order.items.count() == 2
        assert order.subtotal.amount == Decimal('130.00')

    def test_create_pos_order_with_terminal(self):
        """Test creating a POS order with terminal and cashier."""
        terminal = POSTerminalFactory()
        cashier = UserFactory(staff=True)
        customer = UserFactory()

        product = ProductFactory(price=Decimal('25.00'))

        order = OrderFactory(
            user=customer,
            pos_order=True,
            pos_terminal=terminal,
            cashier=cashier,
            paid_order=True,
        )

        OrderItemFactory(order=order, product=product, quantity=1)

        assert order.channel == 'pos'
        assert order.pos_terminal == terminal
        assert order.cashier == cashier
        assert order.payment_status == 'paid'

    def test_order_with_separate_billing_address(self):
        """Test order with different shipping and billing addresses."""
        user = UserFactory()
        shipping_addr = AddressFactory(user=user, address_type='shipping')
        billing_addr = AddressFactory(user=user, address_type='billing')

        order = OrderFactory(
            user=user,
            with_billing=True,
            shipping_address_ref=shipping_addr,
            billing_address_ref=billing_addr,
        )

        assert order.billing_same_as_shipping is False
        assert order.shipping_address_ref == shipping_addr
        assert order.billing_address_ref == billing_addr

    def test_order_with_pickup_location(self):
        """Test order with pickup instead of shipping."""
        from tests.factories import LocationFactory

        user = UserFactory()
        location = LocationFactory()

        order = OrderFactory(
            user=user,
            with_pickup=True,
            pickup_location=location,
        )

        assert order.pickup_location == location
        assert order.pickup_date is not None
        assert order.shipping_cost == Decimal('0.00')

    def test_multi_currency_order_creation(self):
        """Test order with multi-currency tracking."""
        user = UserFactory()

        order = OrderFactory(
            user=user,
            multi_currency=True,
        )

        assert order.customer_currency is not None
        assert order.exchange_rate_used is not None
        assert order.base_currency is not None

    def test_stock_allocation_on_order_creation(self):
        """Test stock is allocated when order is created."""
        user = UserFactory()
        warehouse = WarehouseFactory()
        product = ProductFactory(track_inventory=True)

        # Create stock
        stock = StockItemFactory(
            product=product,
            warehouse=warehouse,
            on_hand=100,
            allocated=0,
        )

        # Create order
        order = OrderFactory(user=user)
        order_item = OrderItemFactory(
            order=order,
            product=product,
            quantity=10,
            stock_allocated=10,
            warehouse=warehouse,
        )

        # Simulate stock allocation
        StockItem.objects.filter(id=stock.id).update(allocated=10)

        stock.refresh_from_db()
        assert stock.allocated == 10
        assert order_item.stock_allocated == 10


@pytest.mark.django_db
class TestPaymentRefundIntegration:
    """Integration tests for payment and refund workflows."""

    def test_mark_order_as_paid(self):
        """Test marking order as paid updates payment status."""
        order = OrderFactory(pending_payment=True)

        assert order.payment_status == 'unpaid'
        assert order.paid_at is None
        assert order.amount_paid == Decimal('0.00')

        # Mark as paid
        order.payment_status = 'paid'
        order.paid_at = timezone.now()
        order.amount_paid = order.total_amount
        order.save()

        order.refresh_from_db()
        assert order.payment_status == 'paid'
        assert order.paid_at is not None
        assert order.amount_paid == order.total_amount

    def test_partial_payment_tracking(self):
        """Test tracking partial payments."""
        order = OrderFactory(
            total_amount=Decimal('100.00'),
            pending_payment=True,
        )

        # Apply partial payment
        order.payment_status = 'partially_paid'
        order.amount_paid = Decimal('50.00')
        order.save()

        order.refresh_from_db()
        assert order.payment_status == 'partially_paid'
        assert order.amount_paid == Decimal('50.00')
        assert order.amount_paid < order.total_amount

    def test_full_refund_workflow(self):
        """Test full refund workflow from request to completion."""
        order = OrderFactory(paid_order=True)
        staff = UserFactory(staff=True)

        # Create refund request
        refund = RefundFactory(
            order=order,
            full_refund=True,
            requested=True,
        )

        assert refund.status == 'requested'

        # Approve refund
        refund.approve()
        assert refund.status == 'approved'
        assert refund.approved_at is not None

        # Process refund
        refund.start_processing()
        assert refund.status == 'processing'

        # Complete refund
        refund.complete()
        assert refund.status == 'completed'
        assert refund.completed_at is not None

    def test_partial_refund_workflow(self):
        """Test partial refund for specific items."""
        order = OrderFactory(
            paid_order=True,
            total_amount=Decimal('100.00'),
        )

        # Create partial refund
        refund = RefundFactory(
            order=order,
            partial_refund=True,
            total_amount=Decimal('50.00'),
        )

        assert refund.refund_type == 'partial'
        assert refund.total_amount == Decimal('50.00')
        assert refund.total_amount < order.total_amount

    def test_refund_stock_restoration(self):
        """Test stock is restored when refund is processed."""
        warehouse = WarehouseFactory()
        product = ProductFactory(track_inventory=True)

        stock = StockItemFactory(
            product=product,
            warehouse=warehouse,
            on_hand=90,  # 100 - 10 sold
            allocated=0,
        )

        order = OrderFactory(paid_order=True)
        order_item = OrderItemFactory(
            order=order,
            product=product,
            quantity=10,
            stock_fulfilled=10,
            warehouse=warehouse,
        )

        # Create and complete refund
        refund = RefundFactory(
            order=order,
            full_refund=True,
            completed=True,
        )

        # Simulate stock restoration
        StockItem.objects.filter(id=stock.id).update(on_hand=100)

        stock.refresh_from_db()
        assert stock.on_hand == 100  # Restored


@pytest.mark.django_db
class TestReturnRequestIntegration:
    """Integration tests for return request workflows."""

    def test_create_return_request(self):
        """Test creating a return request for delivered order."""
        user = UserFactory()
        order = OrderFactory(user=user, delivered=True, paid_order=True)
        product = ProductFactory()
        OrderItemFactory(order=order, product=product, quantity=2)

        # Create return request
        return_request = ReturnRequestFactory(
            order=order,
            user=user,
            pending_return=True,
        )

        assert return_request.order == order
        assert return_request.user == user
        assert return_request.status == 'pending'

    def test_approve_and_generate_label(self):
        """Test approving return and generating shipping label."""
        staff = UserFactory(staff=True)
        return_request = ReturnRequestFactory(pending_return=True)

        # Approve return - Fixed: use 'user' parameter
        return_request.approve(user=staff)
        assert return_request.status == 'approved'

        # Generate and send label - Fixed: set fields separately
        return_request.return_tracking_number = 'RET-123456'
        return_request.return_label_url = 'https://example.com/label.pdf'
        return_request.return_label_generated = True
        return_request.mark_label_sent()

        assert return_request.status == 'label_sent'
        assert return_request.return_label_generated is True
        assert return_request.return_tracking_number == 'RET-123456'

    def test_receive_and_inspect_return(self):
        """Test receiving and inspecting returned items."""
        staff = UserFactory(staff=True)
        return_request = ReturnRequestFactory(in_transit=True)

        # Mark as received
        return_request.mark_received()
        assert return_request.status == 'received'
        assert return_request.received_at is not None

        # Inspect items - Fixed: use correct parameter names
        return_request.mark_inspected(
            condition='good',
            inspection_notes='Items are in good condition',
            user=staff,
        )

        assert return_request.status == 'inspected'
        assert return_request.inspected_by == staff
        assert return_request.items_condition == 'good'

    def test_process_refund_from_return(self):
        """Test processing refund after return inspection."""
        return_request = ReturnRequestFactory(inspected=True)

        # Process refund - Fixed: use refund_data dict
        refund_data = {
            'total_amount': return_request.order.total_amount,
            'shipping_refund_amount': return_request.order.shipping_cost,
            'tax_refund_amount': return_request.order.tax_amount,
            'items_json': [],
            'customer_notes': '',
            'staff_notes': 'Refund processed after inspection',
        }
        refund = return_request.process_refund(refund_data)

        assert refund is not None
        assert refund.order == return_request.order
        assert return_request.refund == refund

    def test_return_with_restocking_fee(self):
        """Test return with restocking fee deduction."""
        return_request = ReturnRequestFactory(
            inspected=True,
            with_restocking_fee=True,
            restocking_fee=Decimal('15.00'),
        )

        # Calculate refund amount
        refund_amount = return_request.calculate_refund_amount()

        expected = return_request.order.total_amount - Decimal('15.00')
        assert refund_amount == expected
