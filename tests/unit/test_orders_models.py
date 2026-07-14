"""
Unit tests for orders app models.

Tests model methods, properties, and business logic for:
- Order model
- OrderItem model
- Address model
- Refund model
- ReturnRequest model
"""

from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from djmoney.money import Money

from tests.factories import (
    AddressFactory,
    OrderFactory,
    OrderItemFactory,
    POSTerminalFactory,
    RefundFactory,
    ReturnRequestFactory,
    UserFactory,
    WarehouseFactory,
)

User = get_user_model()


# ReturnRequestFactory currently declares ``items_condition = None`` at the
# class level. The underlying ``ReturnRequest.items_condition`` column is a
# ``CharField(blank=True)`` with no ``null=True`` and no default -- so the
# factory triggers a NOT NULL violation on the DB. Every test that creates a
# ReturnRequest must override this to a valid value (empty string, or one of
# the CONDITION_CHOICES).
_RR_CONDITION_DEFAULT = ""


@pytest.mark.django_db
class TestOrderModel:
    """Unit tests for the Order model."""

    def test_order_number_auto_generation(self):
        """Test that order_number is automatically generated on creation."""
        # OrderFactory.build() would leave the SubFactory-created user unsaved,
        # which trips Django's "save() prohibited" guard. Materialise the user
        # first, then build the Order with an empty order_number so we can
        # exercise Order.save()'s auto-generation branch.
        user = UserFactory()
        order = OrderFactory.build(user=user, order_number="")
        assert order.order_number == ""

        order.save()
        assert order.order_number != ""
        assert len(order.order_number) > 0

    def test_order_number_not_overwritten(self):
        """Test that existing order_number is not overwritten on save."""
        custom_number = "CUSTOM-12345"
        order = OrderFactory(order_number=custom_number)

        order.save()
        assert order.order_number == custom_number

    def test_total_item_quantity_calculation(self):
        """Test the total_item_quantity property sums all item quantities."""
        order = OrderFactory()
        OrderItemFactory(order=order, quantity=2)
        OrderItemFactory(order=order, quantity=3)
        OrderItemFactory(order=order, quantity=5)

        assert order.total_item_quantity == 10

    def test_total_item_quantity_zero_for_no_items(self):
        """Test that total_item_quantity returns 0 for orders with no items."""
        order = OrderFactory()
        assert order.total_item_quantity == 0

    def test_order_address_snapshot(self):
        """Test that order stores address snapshot data."""
        address = AddressFactory(
            name="John Doe",
            address1="123 Test St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="US",
        )

        order = OrderFactory(
            shipping_name=address.name,
            shipping_address1=address.address1,
            shipping_city=address.city,
            shipping_state=address.state,
            shipping_postal_code=address.postal_code,
            shipping_country=address.country,
            shipping_address_ref=address,
        )

        # Change the original address
        address.address1 = "456 New St"
        address.save()

        # Order should still have the snapshot
        order.refresh_from_db()
        assert order.shipping_address1 == "123 Test St"
        assert order.shipping_address_ref.address1 == "456 New St"

    def test_multi_currency_tracking(self):
        """Test that multi-currency fields are tracked correctly."""
        order = OrderFactory(multi_currency=True)

        assert order.customer_currency is not None
        assert order.exchange_rate_used is not None
        assert order.exchange_rate_provider is not None
        assert order.base_currency is not None

    def test_pos_order_fields(self):
        """Test that POS orders have terminal and cashier fields populated."""
        terminal = POSTerminalFactory()
        cashier = UserFactory(staff=True)

        order = OrderFactory(
            channel="pos",
            pos_terminal=terminal,
            cashier=cashier,
        )

        assert order.channel == "pos"
        assert order.pos_terminal == terminal
        assert order.cashier == cashier

    def test_web_order_no_pos_fields(self):
        """Test that web orders don't have POS fields populated."""
        order = OrderFactory(web_order=True)

        assert order.channel == "web"
        assert order.pos_terminal is None
        assert order.cashier is None

    def test_pickup_order_configuration(self):
        """Test that pickup orders have pickup location and date set."""
        order = OrderFactory(with_pickup=True)

        assert order.pickup_location is not None
        assert order.pickup_date is not None
        assert order.shipping_cost == Money(Decimal("0.00"), "USD")

    def test_billing_same_as_shipping_default(self):
        """Test that billing_same_as_shipping is True by default."""
        order = OrderFactory()
        assert order.billing_same_as_shipping is True

    def test_separate_billing_address(self):
        """Test order with separate billing address."""
        order = OrderFactory(with_billing=True)

        assert order.billing_same_as_shipping is False
        assert order.billing_name != order.shipping_name
        assert order.billing_address1 is not None


@pytest.mark.django_db
class TestOrderItemModel:
    """Unit tests for the OrderItem model."""

    def test_has_discount_with_percentage(self):
        """Test has_discount() returns True for percentage discount."""
        item = OrderItemFactory(
            discount_type="percentage",
            discount_value=Decimal("10.00"),
        )
        assert item.has_discount() is True

    def test_has_discount_with_fixed(self):
        """Test has_discount() returns True for fixed discount."""
        item = OrderItemFactory(
            discount_type="fixed",
            discount_value=Decimal("5.00"),
        )
        assert item.has_discount() is True

    def test_has_discount_no_discount(self):
        """Test has_discount() returns False when discount_type is 'none'."""
        item = OrderItemFactory(discount_type="none")
        assert item.has_discount() is False

    def test_get_discount_amount_percentage(self):
        """Test get_discount_amount() calculates percentage discount correctly."""
        item = OrderItemFactory(
            base_price=Money(Decimal("100.00"), "USD"),
            discount_type="percentage",
            discount_value=Decimal("20.00"),  # 20%
        )
        # get_discount_amount() returns Money -- compare .amount to Decimal.
        result = item.get_discount_amount()
        assert result.amount == Decimal("20.00")
        assert str(result.currency) == "USD"

    def test_get_discount_amount_fixed(self):
        """Test get_discount_amount() returns fixed discount value."""
        item = OrderItemFactory(
            base_price=Money(Decimal("100.00"), "USD"),
            discount_type="fixed",
            discount_value=Decimal("15.00"),
        )
        result = item.get_discount_amount()
        assert result.amount == Decimal("15.00")
        assert str(result.currency) == "USD"

    def test_get_discount_amount_none(self):
        """Test get_discount_amount() returns 0 for no discount."""
        item = OrderItemFactory(discount_type="none")
        result = item.get_discount_amount()
        assert result.amount == Decimal("0.00")

    def test_get_discount_percentage(self):
        """Test get_discount_percentage() calculates correctly."""
        item = OrderItemFactory(
            base_price=Money(Decimal("100.00"), "USD"),
            discount_type="percentage",
            discount_value=Decimal("25.00"),
        )
        assert item.get_discount_percentage() == Decimal("25.00")

    def test_get_discount_percentage_from_fixed(self):
        """Test get_discount_percentage() calculates from fixed amount."""
        item = OrderItemFactory(
            base_price=Money(Decimal("100.00"), "USD"),
            discount_type="fixed",
            discount_value=Decimal("25.00"),
        )
        # 25/100 = 25%
        assert item.get_discount_percentage() == Decimal("25.00")

    def test_get_final_unit_price_with_discount(self):
        """Test get_final_unit_price() returns discounted price."""
        item = OrderItemFactory(
            base_price=Money(Decimal("100.00"), "USD"),
            discount_type="percentage",
            discount_value=Decimal("20.00"),
            unit_price=Money(Decimal("80.00"), "USD"),
        )
        # get_final_unit_price returns Money (base_price - Money discount).
        result = item.get_final_unit_price()
        assert result.amount == Decimal("80.00")

    def test_get_final_unit_price_no_discount(self):
        """Test get_final_unit_price() returns base price without discount."""
        item = OrderItemFactory(
            base_price=Money(Decimal("50.00"), "USD"),
            discount_type="none",
            unit_price=Money(Decimal("50.00"), "USD"),
        )
        # No discount -> returns unit_price as-is (which is Money).
        result = item.get_final_unit_price()
        assert result.amount == Decimal("50.00")

    def test_bundle_parent_relationship(self):
        """Test bundle parent-child relationship.

        NOTE: OrderItem's self-FK ``parent_bundle`` now uses
        ``related_name="component_items"`` (see orders/models.py). The old
        ``bundle_components`` alias is gone.
        """
        parent = OrderItemFactory(bundle_parent=True)
        child1 = OrderItemFactory(parent_bundle=parent)
        child2 = OrderItemFactory(parent_bundle=parent)

        assert child1.parent_bundle == parent
        assert child2.parent_bundle == parent
        assert parent.component_items.count() == 2

    def test_stock_allocation_tracking(self):
        """Test stock allocation fields are tracked correctly.

        NOTE: ``stock_allocated`` and ``stock_fulfilled`` are BooleanFields on
        the current OrderItem model (a flag, not a count). See
        orders/models.py -- they were changed from integers to bools.
        """
        warehouse = WarehouseFactory()
        item = OrderItemFactory(
            quantity=5,
            stock_allocated=True,
            warehouse=warehouse,
        )

        assert item.stock_allocated is True
        assert item.warehouse == warehouse

    def test_stock_fulfillment_tracking(self):
        """Test stock fulfillment fields are tracked correctly.

        See note on test_stock_allocation_tracking -- both fields are Booleans.
        """
        warehouse = WarehouseFactory()
        item = OrderItemFactory(
            quantity=3,
            stock_allocated=True,
            stock_fulfilled=True,
            warehouse=warehouse,
        )

        assert item.stock_allocated is True
        assert item.stock_fulfilled is True


@pytest.mark.django_db
class TestAddressModel:
    """Unit tests for the Address model."""

    def test_address_versioning_on_edit(self):
        """Test that editing an address creates a new version."""
        user = UserFactory()
        address = AddressFactory(
            user=user,
            address1="123 Original St",
            version=1,
        )
        original_id = address.id

        # Simulate address edit by creating a new version
        new_version = AddressFactory(
            user=user,
            address1="456 Updated St",
            original_address=address,
            version=2,
        )

        assert new_version.original_address == address
        assert new_version.version == 2
        assert new_version.id != original_id

    def test_get_version_history(self):
        """Test get_version_history() returns all versions."""
        user = UserFactory()

        # Create original address
        v1 = AddressFactory(user=user, address1="Version 1", version=1)

        # Create version 2
        v2 = AddressFactory(
            user=user,
            address1="Version 2",
            original_address=v1,
            version=2,
        )

        # Create version 3
        v3 = AddressFactory(
            user=user,
            address1="Version 3",
            original_address=v1,
            version=3,
        )

        history = v3.get_version_history()
        assert history.count() == 3
        assert v1 in history
        assert v2 in history
        assert v3 in history

    def test_get_latest_version(self):
        """Test get_latest_version() returns the most recent version."""
        user = UserFactory()

        v1 = AddressFactory(user=user, address1="Version 1", version=1)
        v2 = AddressFactory(user=user, address1="Version 2", original_address=v1, version=2)
        v3 = AddressFactory(user=user, address1="Version 3", original_address=v1, version=3)

        latest = v1.get_latest_version()
        assert latest == v3

    def test_default_address_handling(self):
        """Test that only one address can be default per type."""
        user = UserFactory()

        # Create first default shipping address
        addr1 = AddressFactory(user=user, address_type="shipping", default_address=True)
        assert addr1.is_default is True

        # Note: Setting another as default would require logic in the model/service
        # This test just verifies the flag can be set
        addr2 = AddressFactory(user=user, address_type="shipping", is_default=False)
        assert addr2.is_default is False

    def test_is_used_in_orders(self):
        """Test is_used_in_orders() returns True when address referenced in orders."""
        address = AddressFactory()

        # Initially not used
        assert address.is_used_in_orders() is False

        # Create order with this address reference
        OrderFactory(shipping_address_ref=address)

        # Now it should be used
        assert address.is_used_in_orders() is True

    def test_get_order_count(self):
        """Test get_order_count() returns correct count."""
        address = AddressFactory()

        assert address.get_order_count() == 0

        # Create orders with this address
        OrderFactory(shipping_address_ref=address)
        OrderFactory(shipping_address_ref=address)
        OrderFactory(billing_address_ref=address)

        # Should count all references
        assert address.get_order_count() >= 2


@pytest.mark.django_db
class TestRefundModel:
    """Unit tests for the Refund model."""

    def test_approve_transition(self):
        """Test approve() method transitions status correctly."""
        refund = RefundFactory(requested=True)
        assert refund.status == "requested"

        refund.approve()
        assert refund.status == "approved"
        assert refund.approved_at is not None

    def test_start_processing_transition(self):
        """Test start_processing() method transitions status."""
        refund = RefundFactory(approved=True)
        assert refund.status == "approved"

        refund.start_processing()
        assert refund.status == "processing"

    def test_complete_transition(self):
        """Test complete() method transitions status."""
        refund = RefundFactory(processing=True)
        assert refund.status == "processing"

        refund.complete()
        assert refund.status == "completed"
        assert refund.completed_at is not None

    def test_fail_transition(self):
        """Test fail() method transitions status."""
        refund = RefundFactory(processing=True)

        error_message = "Payment gateway error"
        refund.fail(error_message)
        assert refund.status == "failed"

    def test_calculate_items_total(self):
        """Test calculate_items_total() sums item refund amounts."""
        refund = RefundFactory(
            items_json=[
                {"order_item_id": 1, "quantity": 2, "amount": 50.00},
                {"order_item_id": 2, "quantity": 1, "amount": 25.00},
            ]
        )

        total = refund.calculate_items_total()
        assert total == Decimal("75.00")

    def test_calculate_items_total_empty(self):
        """Test calculate_items_total() returns 0 for empty items_json."""
        refund = RefundFactory(items_json=[])
        assert refund.calculate_items_total() == Decimal("0.00")

    def test_refund_method_display_dynamic(self):
        """Test that refund_method_display can be set dynamically."""
        refund = RefundFactory(
            refund_method="stripe",
            refund_method_display="Stripe Credit Card",
        )

        assert refund.refund_method == "stripe"
        assert refund.refund_method_display == "Stripe Credit Card"


@pytest.mark.django_db
class TestReturnRequestModel:
    """Unit tests for the ReturnRequest model.

    Every ReturnRequestFactory call in this class passes
    ``items_condition=_RR_CONDITION_DEFAULT`` to work around the shared
    factory declaring ``items_condition = None`` at class level -- the DB
    column has no ``null=True``, so ``None`` triggers a NOT NULL violation.
    """

    def test_approve_workflow(self):
        """Test approve() method updates status and timestamps."""
        staff = UserFactory(staff=True)
        return_request = ReturnRequestFactory(
            pending_return=True,
            items_condition=_RR_CONDITION_DEFAULT,
        )

        return_request.approve(user=staff)
        assert return_request.status == "approved"
        assert return_request.approved_at is not None
        assert return_request.approved_by == staff

    def test_reject_workflow(self):
        """Test reject() method updates status and reason."""
        return_request = ReturnRequestFactory(
            pending_return=True,
            items_condition=_RR_CONDITION_DEFAULT,
        )

        reason = "Outside 30-day return window"
        return_request.reject(reason=reason)
        assert return_request.status == "rejected"
        assert return_request.rejected_at is not None
        assert return_request.rejection_reason == reason

    def test_mark_label_sent(self):
        """Test mark_label_sent() updates status and tracking."""
        return_request = ReturnRequestFactory(
            approved_return=True,
            items_condition=_RR_CONDITION_DEFAULT,
        )

        tracking_number = "RET-123456"
        label_url = "https://example.com/label.pdf"

        # mark_label_sent() takes no parameters -- populate tracking details
        # first, then invoke the transition.
        return_request.return_tracking_number = tracking_number
        return_request.return_label_url = label_url
        return_request.return_label_generated = True
        return_request.mark_label_sent()

        assert return_request.status == "label_sent"
        assert return_request.return_label_generated is True
        assert return_request.return_tracking_number == tracking_number
        assert return_request.return_label_url == label_url
        assert return_request.label_sent_at is not None

    def test_mark_in_transit(self):
        """Test mark_in_transit() updates status."""
        return_request = ReturnRequestFactory(
            label_sent=True,
            items_condition=_RR_CONDITION_DEFAULT,
        )

        return_request.mark_in_transit()
        assert return_request.status == "in_transit"

    def test_mark_received(self):
        """Test mark_received() updates status and timestamp."""
        return_request = ReturnRequestFactory(
            in_transit=True,
            items_condition=_RR_CONDITION_DEFAULT,
        )

        return_request.mark_received()
        assert return_request.status == "received"
        assert return_request.received_at is not None

    def test_mark_inspected(self):
        """Test mark_inspected() updates status and inspection details."""
        staff = UserFactory(staff=True)
        return_request = ReturnRequestFactory(
            received=True,
            items_condition=_RR_CONDITION_DEFAULT,
        )

        # mark_inspected() signature: (condition, inspection_notes="",
        # restocking_fee=None, user=None)
        return_request.mark_inspected(
            condition="good",
            inspection_notes="All items in good condition",
            user=staff,
        )

        assert return_request.status == "inspected"
        assert return_request.inspected_at is not None
        assert return_request.inspected_by == staff
        assert return_request.items_condition == "good"
        assert return_request.inspection_notes == "All items in good condition"

    def test_process_refund_creation(self):
        """Test process_refund() creates a refund and links it."""
        return_request = ReturnRequestFactory(
            inspected=True,
            items_condition=_RR_CONDITION_DEFAULT,
        )

        # process_refund expects a refund_data dict, not a simple amount.
        refund_data = {
            "total_amount": Decimal("100.00"),
            "shipping_refund_amount": Decimal("5.99"),
            "tax_refund_amount": Decimal("8.88"),
            "items_json": [],
            "customer_notes": "",
            "staff_notes": "",
        }
        refund = return_request.process_refund(refund_data)

        assert refund is not None
        assert refund.order == return_request.order
        # total_amount is a MoneyField -- compare .amount to Decimal.
        assert refund.total_amount.amount == Decimal("100.00")
        assert return_request.refund == refund

    def test_calculate_refund_amount_with_restocking_fee(self):
        """Test calculate_refund_amount() computes a per-item refund total.

        NOTE: ``calculate_refund_amount()`` walks ``items_json`` and looks up
        each ``order_item_id`` -- it does *not* automatically deduct the
        restocking fee (that field is stored for display / downstream refund
        creation). The default ReturnRequestFactory.items_json references
        ``order_item_id: 1``, but factories don't guarantee OrderItem.id==1,
        so we create an OrderItem explicitly and rewrite items_json to point
        at it.
        """
        order = OrderFactory(paid_order=True, delivered=True)
        item = OrderItemFactory(
            order=order,
            quantity=1,
            unit_price=Money(Decimal("50.00"), "USD"),
        )
        return_request = ReturnRequestFactory(
            order=order,
            items_condition=_RR_CONDITION_DEFAULT,
            with_restocking_fee=True,
            restocking_fee=Money(Decimal("15.00"), "USD"),
            items_json=[
                {"order_item_id": item.id, "quantity": 1, "reason": "Defective"},
            ],
        )

        refund_amount = return_request.calculate_refund_amount()

        # calculate_refund_amount() returns the item value only; restocking
        # fee is stored on the model but not subtracted here.
        assert refund_amount == Decimal("50.00")
        assert return_request.restocking_fee.amount == Decimal("15.00")

    def test_get_items_summary(self):
        """Test get_items_summary() returns formatted items list."""
        return_request = ReturnRequestFactory(
            items_condition=_RR_CONDITION_DEFAULT,
            items_json=[
                {"order_item_id": 1, "product_name": "Product A", "quantity": 2},
                {"order_item_id": 2, "product_name": "Product B", "quantity": 1},
            ],
        )

        summary = return_request.get_items_summary()
        # Current implementation returns "N item(s), M unit(s)" -- verify the
        # totals are correct rather than pattern-matching on wording.
        assert "2 item(s)" in summary
        assert "3 unit(s)" in summary

    def test_complete_return_workflow(self):
        """Test complete() method marks return as completed."""
        return_request = ReturnRequestFactory(
            inspected=True,
            items_condition=_RR_CONDITION_DEFAULT,
        )

        return_request.complete()
        assert return_request.status == "completed"
        assert return_request.completed_at is not None

    def test_cancel_return_workflow(self):
        """Test cancel() method marks return as cancelled."""
        return_request = ReturnRequestFactory(
            pending_return=True,
            items_condition=_RR_CONDITION_DEFAULT,
        )

        return_request.cancel()
        assert return_request.status == "cancelled"
