"""
Cart customization integration tests.

Tests the customization workflow: adding customized products to cart,
validation of customization values, price calculation, and checkout
flow that creates CustomizationValue records on order items.
"""
import pytest
from decimal import Decimal
from djmoney.money import Money

from cart.services.cart_service import CartService
from cart.services.checkout_service import CheckoutService

from tests.factories import (
    CartFactory, ProductFactory, CategoryFactory,
    ShippingMethodFactory, ShippingZoneFactory,
    AddressFactory, PaymentProviderAccountFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.checkout]


# ============================================================
# Helpers
# ============================================================

@pytest.fixture
def customizable_product(db, category):
    """Product with text and select customization options."""
    from catalog.models import CustomizationOption

    product = ProductFactory(
        name='Custom T-Shirt',
        slug='custom-tshirt',
        category=category,
        price=Decimal('25.00'),
        product_type='customizable',
        allow_customization=True,
        track_inventory=False,
    )

    text_option = CustomizationOption.objects.create(
        product=product,
        name='Name to Print',
        slug='name-to-print',
        option_type='text',
        is_required=True,
        max_length=20,
        pricing_type='fixed',
        price_amount=Money(5.00, 'USD'),
        sort_order=1,
    )

    color_option = CustomizationOption.objects.create(
        product=product,
        name='Thread Color',
        slug='thread-color',
        option_type='select',
        is_required=False,
        pricing_type='free',
        choices=[
            {'value': 'red', 'label': 'Red', 'price_modifier': 0},
            {'value': 'blue', 'label': 'Blue', 'price_modifier': 2},
            {'value': 'gold', 'label': 'Gold', 'price_modifier': 5},
        ],
        sort_order=2,
    )

    return {
        'product': product,
        'text_option': text_option,
        'color_option': color_option,
    }


# ============================================================
# A. Add to Cart
# ============================================================

class TestAddCustomizedProductToCart:

    def test_add_with_valid_customizations(
        self, customer_user, site_settings, customizable_product,
    ):
        """Adding a customized product stores validated customizations with prices."""
        p = customizable_product
        cart = CartService.get_or_create_cart(user=customer_user)

        customizations = {
            str(p['text_option'].id): 'John Doe',
            str(p['color_option'].id): 'gold',
        }

        success, message, cart_item = CartService.add_item(
            cart=cart,
            product_id=p['product'].id,
            quantity=1,
            customizations=customizations,
        )

        assert success, f"Failed to add item: {message}"
        assert cart_item is not None

        # Customizations stored with calculated prices
        text_data = cart_item.customizations[str(p['text_option'].id)]
        assert text_data['value'] == 'John Doe'
        assert Decimal(text_data['calculated_price']) == Decimal('5.00')

        color_data = cart_item.customizations[str(p['color_option'].id)]
        assert Decimal(color_data['calculated_price']) == Decimal('5.00')  # gold = +$5

        # Total: base $25 + text $5 + gold $5 = $35
        assert cart_item.customization_price == Money(10.00, 'USD')
        assert cart_item.total_price == Money(35.00, 'USD')

    def test_missing_required_customization_rejected(
        self, customer_user, site_settings, customizable_product,
    ):
        """Validation fails when a required customization is omitted."""
        p = customizable_product
        cart = CartService.get_or_create_cart(user=customer_user)

        # Only provide optional color, missing required text
        customizations = {
            str(p['color_option'].id): 'red',
        }

        success, message, cart_item = CartService.add_item(
            cart=cart,
            product_id=p['product'].id,
            quantity=1,
            customizations=customizations,
        )

        assert not success
        assert 'required' in message.lower()
        assert cart_item is None

    def test_text_exceeding_max_length_rejected(
        self, customer_user, site_settings, customizable_product,
    ):
        """Validation fails when text exceeds the option's max_length."""
        p = customizable_product
        cart = CartService.get_or_create_cart(user=customer_user)

        customizations = {
            str(p['text_option'].id): 'This is a very long name that exceeds twenty characters',
            str(p['color_option'].id): 'red',
        }

        success, message, cart_item = CartService.add_item(
            cart=cart,
            product_id=p['product'].id,
            quantity=1,
            customizations=customizations,
        )

        assert not success
        assert '20' in message
        assert cart_item is None


# ============================================================
# B. Cart Item Merging
# ============================================================

class TestCustomizationCartItemMerging:

    def test_different_customizations_create_separate_items(
        self, customer_user, site_settings, customizable_product,
    ):
        """Products with different customizations are kept as separate cart items."""
        p = customizable_product
        cart = CartService.get_or_create_cart(user=customer_user)

        success1, _, item1 = CartService.add_item(
            cart=cart,
            product_id=p['product'].id,
            quantity=1,
            customizations={
                str(p['text_option'].id): 'John',
                str(p['color_option'].id): 'red',
            },
        )
        success2, _, item2 = CartService.add_item(
            cart=cart,
            product_id=p['product'].id,
            quantity=1,
            customizations={
                str(p['text_option'].id): 'Jane',
                str(p['color_option'].id): 'blue',
            },
        )

        assert success1 and success2
        assert item1.id != item2.id
        assert cart.items.count() == 2

    def test_identical_customizations_increase_quantity(
        self, customer_user, site_settings, customizable_product,
    ):
        """Adding the same customizations again merges into a single item."""
        p = customizable_product
        cart = CartService.get_or_create_cart(user=customer_user)

        customizations = {
            str(p['text_option'].id): 'John',
            str(p['color_option'].id): 'red',
        }

        success1, _, item1 = CartService.add_item(
            cart=cart, product_id=p['product'].id, quantity=1,
            customizations=customizations,
        )
        success2, _, item2 = CartService.add_item(
            cart=cart, product_id=p['product'].id, quantity=1,
            customizations=customizations,
        )

        assert success1 and success2
        assert item1.id == item2.id
        assert cart.items.count() == 1
        assert item2.quantity == 2


# ============================================================
# C. Cart Totals
# ============================================================

class TestCustomizationCartTotals:

    def test_multiple_customized_items_total(
        self, customer_user, site_settings, customizable_product,
    ):
        """Cart total reflects different customization prices across items."""
        p = customizable_product
        cart = CartService.get_or_create_cart(user=customer_user)

        # Item 1: base $25 + text $5 + red $0 = $30
        success1, _, item1 = CartService.add_item(
            cart=cart,
            product_id=p['product'].id,
            quantity=1,
            customizations={
                str(p['text_option'].id): 'Alice',
                str(p['color_option'].id): 'red',
            },
        )
        # Item 2: base $25 + text $5 + blue $2 = $32
        success2, _, item2 = CartService.add_item(
            cart=cart,
            product_id=p['product'].id,
            quantity=1,
            customizations={
                str(p['text_option'].id): 'Bob',
                str(p['color_option'].id): 'blue',
            },
        )

        assert success1 and success2
        assert item1.customization_price == Money(5.00, 'USD')   # text only (red is free)
        assert item2.customization_price == Money(7.00, 'USD')   # text + blue
        assert cart.total_amount == Money(62.00, 'USD')           # $30 + $32


# ============================================================
# D. Checkout → Order with Customization Values
# ============================================================

class TestCheckoutCreatesCustomizationValues:

    def test_checkout_transfers_customizations_to_order(
        self, customer_user, admin_user, site_settings, warehouse,
        customizable_product,
    ):
        """Full flow: cart → checkout → order creates CustomizationValue records."""
        p = customizable_product
        cart = CartService.get_or_create_cart(user=customer_user)

        customizations = {
            str(p['text_option'].id): 'John Doe',
            str(p['color_option'].id): 'gold',
        }

        CartService.add_item(
            cart=cart,
            product_id=p['product'].id,
            quantity=2,
            customizations=customizations,
        )

        # Shipping address
        address = AddressFactory(user=customer_user)

        # Checkout session
        session = CheckoutService.get_or_create_session(cart)
        CheckoutService.set_shipping_address(session, address_id=address.id)
        CheckoutService.set_billing_address(session, same_as_shipping=True)

        # Shipping method
        zone = ShippingZoneFactory(countries=['US'])
        method = ShippingMethodFactory(
            flat_rate_cost=Decimal('10.00'),
            zones=[zone],
        )
        CheckoutService.set_shipping_method(session, shipping_method_id=method.id)

        # Payment provider
        payment_provider = PaymentProviderAccountFactory(user=admin_user)
        session.payment_provider = payment_provider
        session.save()

        # Create order
        success, message, order = CheckoutService.create_order(session)
        assert success, f"Order creation failed: {message}"
        assert order is not None

        # Verify order item
        assert order.items.count() == 1
        order_item = order.items.first()
        assert order_item.quantity == 2

        # Customizations stored on order item
        assert order_item.customizations is not None
        assert len(order_item.customizations) == 2

        # CustomizationValue records created
        customization_values = order_item.customization_values.all()
        assert customization_values.count() == 2

        text_value = customization_values.get(customization_option=p['text_option'])
        assert text_value.text_value == 'John Doe'
        assert text_value.calculated_price == Money(5.00, 'USD')

        color_value = customization_values.get(customization_option=p['color_option'])
        assert color_value.choice_value == 'gold'
        assert color_value.calculated_price == Money(5.00, 'USD')

        # Subtotal: (base $25 + customizations $10) * 2 = $70
        assert order.subtotal == Money(70.00, 'USD')
