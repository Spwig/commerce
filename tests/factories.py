"""
Factory Boy factories for Spwig test pipeline.

These factories create test data for any app that needs users, products,
addresses, shipping, tax, etc. Use them directly or compose them via
scenario builders in tests/fixtures/.
"""
import factory
import secrets
import uuid
from datetime import timedelta
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify

User = get_user_model()


# ============================================================
# Users
# ============================================================

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'testuser_{n}')
    email = factory.LazyAttribute(lambda o: f'{o.username}@test.spwig.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop('password', 'testpass123')
        user = super()._create(model_class, *args, **kwargs)
        user.set_password(password)
        user.save(update_fields=['password'])
        return user

    class Params:
        staff = factory.Trait(is_staff=True, is_superuser=True)


# ============================================================
# Catalog
# ============================================================

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'catalog.Category'
        django_get_or_create = ('slug',)

    name = factory.Sequence(lambda n: f'Test Category {n}')
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    is_active = True


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'catalog.Product'
        django_get_or_create = ('slug',)

    name = factory.Sequence(lambda n: f'Test Product {n}')
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    sku = factory.LazyFunction(lambda: f'TEST-{uuid.uuid4().hex[:8].upper()}')
    category = factory.SubFactory(CategoryFactory)
    price = Decimal('25.00')
    price_currency = 'USD'
    product_type = 'simple'
    status = 'published'
    track_inventory = False  # Default off for easier testing
    weight = Decimal('0.5')

    class Params:
        digital = factory.Trait(
            product_type='digital',
            weight=None,
        )
        expensive = factory.Trait(price=Decimal('150.00'), weight=Decimal('3.0'))
        heavy = factory.Trait(weight=Decimal('8.0'))


class SalesRegionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'catalog.SalesRegion'
        django_get_or_create = ('code',)

    name = 'Default Region'
    code = 'DEFAULT'
    countries = factory.LazyFunction(lambda: ['US', 'GB', 'DE', 'AU', 'CA', 'JP'])
    default_currency = 'USD'
    is_active = True


class WarehouseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'catalog.Warehouse'
        django_get_or_create = ('code',)

    name = 'Test Warehouse'
    code = 'TEST-WH'
    region = factory.SubFactory(SalesRegionFactory)
    address_line1 = '100 Warehouse Drive'
    city = 'Newark'
    state_province = 'NJ'
    postal_code = '07102'
    country = 'US'
    is_active = True


# ============================================================
# Addresses
# ============================================================

class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'orders.Address'

    user = factory.SubFactory(UserFactory)
    address_type = 'both'
    name = 'Test User'
    address1 = '456 Broadway'
    city = 'New York'
    state = 'NY'
    postal_code = '10013'
    country = 'US'
    is_default = False
    is_active = True

    class Params:
        # Address type traits
        shipping_address = factory.Trait(address_type='shipping')
        billing_address = factory.Trait(address_type='billing')
        default_address = factory.Trait(is_default=True)

        # Country-specific addresses
        uk = factory.Trait(
            name='Test User UK',
            address1='10 Downing Street',
            city='London',
            state='Greater London',
            postal_code='SW1A 2AA',
            country='GB',
        )
        de = factory.Trait(
            name='Test User DE',
            address1='Unter den Linden 1',
            city='Berlin',
            state='Berlin',
            postal_code='10117',
            country='DE',
        )
        au = factory.Trait(
            name='Test User AU',
            address1='1 George Street',
            city='Sydney',
            state='NSW',
            postal_code='2000',
            country='AU',
        )
        ca = factory.Trait(
            name='Test User CA',
            address1='24 Sussex Drive',
            city='Ottawa',
            state='ON',
            postal_code='K1M 1M4',
            country='CA',
        )
        jp = factory.Trait(
            name='Test User JP',
            address1='1-1 Chiyoda',
            city='Tokyo',
            state='Tokyo',
            postal_code='100-0001',
            country='JP',
        )

    @factory.post_generation
    def versioned_address(self, create, extracted, **kwargs):
        """Create an address with version history."""
        if not create or not extracted:
            return

        # Create the original address version
        from orders.models import Address
        original = Address.objects.create(
            user=self.user,
            address_type=self.address_type,
            name=f'{self.name} - Original',
            address1=self.address1,
            city=self.city,
            state=self.state,
            postal_code=self.postal_code,
            country=self.country,
            is_default=False,
            is_active=False,
            version=1,
        )

        # Update current address to reference the original
        self.original_address = original
        self.version = 2
        self.save(update_fields=['original_address', 'version'])


# ============================================================
# Shipping
# ============================================================

class ShippingZoneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'shipping.ShippingZone'

    name = factory.Sequence(lambda n: f'Zone {n}')
    countries = factory.LazyFunction(lambda: ['US'])
    is_active = True


class ShippingMethodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'cart.ShippingMethod'

    name = factory.Sequence(lambda n: f'Shipping Method {n}')
    method_type = 'flat_rate'
    flat_rate_cost = Decimal('5.99')
    flat_rate_cost_currency = 'USD'
    min_delivery_days = 3
    max_delivery_days = 7
    is_active = True

    @factory.post_generation
    def zones(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for zone in extracted:
                self.zones.add(zone)

    class Params:
        free = factory.Trait(
            method_type='free_shipping',
            flat_rate_cost=Decimal('0.00'),
        )
        express = factory.Trait(
            flat_rate_cost=Decimal('14.99'),
            min_delivery_days=1,
            max_delivery_days=3,
        )


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'shipping.Location'

    name = factory.Sequence(lambda n: f'Test Location {n}')
    location_type = 'store'
    address_line1 = '789 Store Street'
    city = 'New York'
    state = 'NY'
    postal_code = '10001'
    country = 'US'
    phone_number = '+1-555-0300'
    email_address = factory.Sequence(lambda n: f'location{n}@test.spwig.com')
    is_active = True

    class Params:
        warehouse = factory.Trait(location_type='warehouse')
        fulfillment_center = factory.Trait(location_type='fulfillment_center')
        dispatch_center = factory.Trait(location_type='dispatch_center')


class CarrierPresetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'shipping.CarrierPreset'
        django_get_or_create = ('slug',)

    name = factory.Sequence(lambda n: f'Test Carrier {n}')
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    tracking_url_template = 'https://track.example.com/{tracking_number}'
    is_active = True
    is_default = False

    class Params:
        ups = factory.Trait(
            name='UPS',
            slug='ups',
            tracking_url_template='https://www.ups.com/track?tracknum={tracking_number}',
        )
        fedex = factory.Trait(
            name='FedEx',
            slug='fedex',
            tracking_url_template='https://www.fedex.com/fedextrack/?tracknumbers={tracking_number}',
        )
        dhl = factory.Trait(
            name='DHL',
            slug='dhl',
            tracking_url_template='https://www.dhl.com/tracking/{tracking_number}',
        )
        usps = factory.Trait(
            name='USPS',
            slug='usps',
            tracking_url_template='https://tools.usps.com/go/TrackConfirmAction?tLabels={tracking_number}',
        )


# ============================================================
# Tax
# ============================================================

class TaxRateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'cart.TaxRate'

    name = factory.LazyAttribute(lambda o: f'{o.country} Tax')
    country = 'US'
    state = ''
    rate = Decimal('0.0000')
    tax_type = 'sales_tax'
    applies_to_shipping = False
    is_active = True

    class Params:
        ny = factory.Trait(
            name='NY Sales Tax',
            country='US',
            state='NY',
            rate=Decimal('0.0888'),
            tax_type='sales_tax',
        )
        ca = factory.Trait(
            name='CA Sales Tax',
            country='US',
            state='CA',
            rate=Decimal('0.0725'),
            tax_type='sales_tax',
        )
        uk_vat = factory.Trait(
            name='UK VAT',
            country='GB',
            rate=Decimal('0.2000'),
            tax_type='vat',
            applies_to_shipping=True,
        )
        de_vat = factory.Trait(
            name='DE VAT',
            country='DE',
            rate=Decimal('0.1900'),
            tax_type='vat',
            applies_to_shipping=True,
        )


# ============================================================
# Cart
# ============================================================

class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'cart.Cart'

    user = factory.SubFactory(UserFactory)


class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'cart.CartItem'

    cart = factory.SubFactory(CartFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = 1
    unit_price = factory.LazyAttribute(lambda o: o.product.price)
    unit_price_currency = 'USD'


# ============================================================
# Vouchers
# ============================================================

class VoucherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'vouchers.VoucherCode'
        django_get_or_create = ('code',)

    code = factory.Sequence(lambda n: f'TEST{n:04d}')
    name = factory.LazyAttribute(lambda o: f'Voucher {o.code}')
    discount_type = 'percentage'
    discount_value = Decimal('10.00')
    application_scope = 'cart'
    is_active = True

    class Params:
        fixed = factory.Trait(
            discount_type='fixed',
            discount_value=Decimal('5.00'),
        )


# ============================================================
# Translation
# ============================================================

class SiteLanguageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'translations.SiteLanguage'
        django_get_or_create = ('code',)

    code = factory.Sequence(lambda n: f'lang{n}')
    name = factory.Sequence(lambda n: f'Language {n}')
    native_name = factory.LazyAttribute(lambda o: o.name)
    is_active = True
    is_default = False
    flag = ''

    class Params:
        spanish = factory.Trait(code='es', name='Spanish', native_name='Español', flag='🇪🇸')
        french = factory.Trait(code='fr', name='French', native_name='Français', flag='🇫🇷')
        english_default = factory.Trait(code='en', name='English', native_name='English', flag='🇺🇸', is_default=True)


# ============================================================
# Page Builder
# ============================================================

class PageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'page_builder.Page'
        django_get_or_create = ('slug',)

    title = factory.Sequence(lambda n: f'Test Page {n}')
    slug = factory.LazyAttribute(lambda o: slugify(o.title))
    status = 'published'


# ============================================================
# POS
# ============================================================

class StoreGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'pos_app.StoreGroup'
        django_get_or_create = ('code',)

    name = factory.Sequence(lambda n: f'Store Group {n}')
    code = factory.Sequence(lambda n: f'SG-{n:03d}')
    currency = ''
    is_active = True


class POSTerminalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'pos_app.POSTerminal'

    name = factory.Sequence(lambda n: f'Terminal {n}')
    uuid = factory.LazyFunction(uuid.uuid4)
    warehouse = factory.SubFactory(WarehouseFactory)
    hardware_config = factory.LazyFunction(dict)
    currency = ''
    is_active = True

    class Params:
        inactive = factory.Trait(is_active=False)
        eur = factory.Trait(currency='EUR')


class POSShiftFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'pos_app.POSShift'

    terminal = factory.SubFactory(POSTerminalFactory)
    cashier = factory.SubFactory(UserFactory, is_staff=True)
    opening_cash = Decimal('100.00')

    class Params:
        closed = factory.Trait(
            ended_at=factory.LazyFunction(timezone.now),
            closing_cash=Decimal('150.00'),
        )


class CashMovementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'pos_app.CashMovement'

    shift = factory.SubFactory(POSShiftFactory)
    movement_type = 'in'
    amount = Decimal('20.00')
    reason = 'Float top-up'
    performed_by = factory.LazyAttribute(lambda o: o.shift.cashier)


class POSStaffDiscountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'pos_app.POSStaffDiscount'

    user = factory.SubFactory(UserFactory, is_staff=True)
    max_discount_percentage = Decimal('10.00')
    can_apply_item_discounts = True
    can_apply_cart_discounts = True
    is_manager = False
    cashier_pin = '1234'

    class Params:
        manager = factory.Trait(
            is_manager=True,
            manager_pin='9999',
            max_discount_percentage=Decimal('50.00'),
        )


class MobileAuthTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'admin_api.MobileAuthToken'

    user = factory.SubFactory(UserFactory, is_staff=True)
    token = factory.LazyFunction(lambda: secrets.token_urlsafe(48))
    token_type = 'access'
    device_id = factory.LazyFunction(lambda: f'test-device-{uuid.uuid4().hex[:8]}')
    device_name = 'Test POS Device'
    expires_at = factory.LazyFunction(lambda: timezone.now() + timedelta(hours=1))

    class Params:
        refresh = factory.Trait(
            token_type='refresh',
            expires_at=factory.LazyFunction(lambda: timezone.now() + timedelta(days=30)),
        )
        expired = factory.Trait(
            expires_at=factory.LazyFunction(lambda: timezone.now() - timedelta(hours=1)),
        )


class ProductVariantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'catalog.ProductVariant'

    product = factory.SubFactory(ProductFactory, product_type='variable')
    name = factory.Sequence(lambda n: f'Variant {n}')
    sku = factory.LazyFunction(lambda: f'VAR-{uuid.uuid4().hex[:8].upper()}')
    is_active = True


class StockItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'catalog.StockItem'

    product = factory.SubFactory(ProductFactory, track_inventory=True)
    warehouse = factory.SubFactory(WarehouseFactory)
    on_hand = 50
    allocated = 0

    class Params:
        low_stock = factory.Trait(on_hand=3)


class CheckoutSessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'cart.CheckoutSession'

    cart = factory.SubFactory(CartFactory)
    expires_at = factory.LazyFunction(lambda: timezone.now() + timedelta(hours=2))


class ShippingCountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'shipping.ShippingCountry'

    site = factory.LazyFunction(lambda: __import__('django.contrib.sites.models', fromlist=['Site']).Site.objects.get_or_create(id=1, defaults={'domain': 'localhost', 'name': 'Test'})[0])
    country_code = 'US'
    is_active = True
    priority = 0


class CountryWarehouseFallbackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'shipping.CountryWarehouseFallback'

    country = factory.SubFactory(ShippingCountryFactory)
    warehouse = factory.SubFactory(WarehouseFactory)
    priority = 0


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'orders.Order'

    user = factory.SubFactory(UserFactory)
    order_number = factory.LazyFunction(lambda: f'ORD-{uuid.uuid4().hex[:12].upper()}')
    status = 'processing'
    channel = 'web'
    source = 'direct'
    email = factory.LazyAttribute(lambda o: o.user.email if o.user else 'guest@test.spwig.com')
    phone = '+1-555-0100'

    # Shipping address (snapshot)
    shipping_name = factory.LazyAttribute(lambda o: f'{o.user.first_name} {o.user.last_name}' if o.user else 'Guest Customer')
    shipping_address1 = '123 Main Street'
    shipping_address2 = ''
    shipping_city = 'New York'
    shipping_state = 'NY'
    shipping_postal_code = '10001'
    shipping_country = 'US'
    shipping_phone = '+1-555-0100'

    # Billing (same as shipping by default)
    billing_same_as_shipping = True

    # Order totals
    subtotal = Decimal('100.00')
    subtotal_currency = 'USD'
    tax_amount = Decimal('8.88')
    tax_amount_currency = 'USD'
    shipping_cost = Decimal('5.99')
    shipping_cost_currency = 'USD'
    discount_amount = Decimal('0.00')
    discount_amount_currency = 'USD'
    gift_card_discount = Decimal('0.00')
    gift_card_discount_currency = 'USD'
    total_amount = Decimal('114.87')
    total_amount_currency = 'USD'

    # Payment
    payment_status = 'unpaid'
    amount_paid = Decimal('0.00')
    amount_paid_currency = 'USD'
    amount_refunded = Decimal('0.00')
    amount_refunded_currency = 'USD'

    # Multi-currency / FX fields
    fx_policy = 'none'
    base_currency = 'USD'
    subtotal_base = factory.LazyAttribute(lambda o: o.subtotal)
    tax_amount_base = factory.LazyAttribute(lambda o: o.tax_amount)
    shipping_cost_base = factory.LazyAttribute(lambda o: o.shipping_cost)
    discount_amount_base = factory.LazyAttribute(lambda o: o.discount_amount)
    gift_card_discount_base = factory.LazyAttribute(lambda o: o.gift_card_discount)
    total_amount_base = factory.LazyAttribute(lambda o: o.total_amount)
    amount_paid_base = factory.LazyAttribute(lambda o: o.amount_paid)
    amount_refunded_base = factory.LazyAttribute(lambda o: o.amount_refunded)

    # Display preferences
    order_page_layout = 'standard'
    show_order_progress = True
    show_shipping_updates = True
    show_item_images = True

    # Test flag
    is_test_order = False

    class Params:
        # Channel traits
        web_order = factory.Trait(
            channel='web',
            order_number=factory.LazyFunction(lambda: f'WEB-{uuid.uuid4().hex[:12].upper()}'),
            pos_terminal=None,
            cashier=None,
        )
        pos_order = factory.Trait(
            channel='pos',
            order_number=factory.LazyFunction(lambda: f'POS-{uuid.uuid4().hex[:12].upper()}'),
            pos_terminal=factory.SubFactory(POSTerminalFactory),
            cashier=factory.SubFactory(UserFactory, staff=True),
            shipping_name='POS Customer',
            shipping_address1='In-Store',
            shipping_city='N/A',
            shipping_state='N/A',
            shipping_postal_code='00000',
        )

        # Payment status traits
        pending_payment = factory.Trait(
            payment_status='unpaid',
            paid_at=None,
            amount_paid=Decimal('0.00'),
        )
        paid_order = factory.Trait(
            payment_status='paid',
            paid_at=factory.LazyFunction(timezone.now),
            amount_paid=factory.LazyAttribute(lambda o: o.total_amount),
        )

        # Shipping traits
        with_shipping = factory.Trait(
            shipping_cost=Decimal('12.99'),
            shipping_cost_currency='USD',
            total_amount=Decimal('121.87'),
        )
        with_pickup = factory.Trait(
            shipping_cost=Decimal('0.00'),
            pickup_location=factory.SubFactory('tests.factories.LocationFactory'),
            pickup_date=factory.LazyFunction(lambda: timezone.now() + timedelta(days=2)),
        )

        # Billing trait
        with_billing = factory.Trait(
            billing_same_as_shipping=False,
            billing_name='Billing Department',
            billing_address1='456 Business Ave',
            billing_address2='Suite 100',
            billing_city='Los Angeles',
            billing_state='CA',
            billing_postal_code='90001',
            billing_country='US',
            billing_phone='+1-555-0200',
        )

        # Order status traits
        cancelled = factory.Trait(status='cancelled')
        shipped = factory.Trait(status='shipped')
        delivered = factory.Trait(status='delivered')

        # Refund trait
        refunded = factory.Trait(
            payment_status='refunded',
            amount_refunded=factory.LazyAttribute(lambda o: o.total_amount),
        )
        partially_refunded = factory.Trait(
            payment_status='partially_refunded',
            amount_refunded=Decimal('50.00'),
        )

        # Multi-currency trait
        multi_currency = factory.Trait(
            customer_currency='EUR',
            exchange_rate_used=Decimal('0.85'),
            exchange_rate_provider='ecb',
            base_currency='USD',
        )

        # Tracking trait
        with_tracking = factory.Trait(
            tracking_number=factory.LazyFunction(lambda: f'1Z999AA1{uuid.uuid4().hex[:10].upper()}'),
            carrier=factory.SubFactory('tests.factories.CarrierPresetFactory'),
        )

        # Test order trait
        test_order = factory.Trait(is_test_order=True)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'orders.OrderItem'

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    product_name = factory.LazyAttribute(lambda o: o.product.name)
    sku = factory.LazyAttribute(lambda o: o.product.sku)
    quantity = 1
    unit_price = factory.LazyAttribute(lambda o: o.product.price)
    unit_price_currency = 'USD'
    base_price = factory.LazyAttribute(lambda o: o.product.price)
    base_price_currency = 'USD'
    total_price = factory.LazyAttribute(lambda o: o.unit_price * o.quantity)
    total_price_currency = 'USD'

    # Base-currency equivalents
    unit_price_base = factory.LazyAttribute(lambda o: o.unit_price.amount if hasattr(o.unit_price, 'amount') else Decimal(str(o.unit_price)))
    total_price_base = factory.LazyAttribute(lambda o: o.total_price.amount if hasattr(o.total_price, 'amount') else Decimal(str(o.total_price)))

    # Discount fields (default: no discount)
    discount_type = 'none'
    discount_value = Decimal('0.00')
    discount_reason = ''
    exclude_from_vouchers = False

    # Stock tracking
    stock_allocated = 0
    stock_fulfilled = 0

    # Customizations
    customizations = factory.LazyFunction(dict)

    class Params:
        # Discount traits
        with_discount = factory.Trait(
            discount_type='percentage',
            discount_value=Decimal('10.00'),
            discount_reason='Promotional discount',
            unit_price=factory.LazyAttribute(lambda o: o.base_price * Decimal('0.90')),
        )
        percentage_discount = factory.Trait(
            discount_type='percentage',
            discount_value=Decimal('15.00'),
            discount_reason='Percentage discount',
            unit_price=factory.LazyAttribute(lambda o: o.base_price * Decimal('0.85')),
        )
        fixed_discount = factory.Trait(
            discount_type='fixed',
            discount_value=Decimal('5.00'),
            discount_reason='Fixed amount discount',
            unit_price=factory.LazyAttribute(lambda o: o.base_price - Decimal('5.00')),
        )

        # Bundle traits
        bundle_parent = factory.Trait(
            product=factory.SubFactory(ProductFactory, product_type='bundle'),
        )
        bundle_component = factory.Trait(
            parent_bundle=factory.SubFactory('tests.factories.OrderItemFactory', bundle_parent=True),
            exclude_from_vouchers=True,
        )

        # Stock traits
        with_stock_allocated = factory.Trait(
            stock_allocated=factory.LazyAttribute(lambda o: o.quantity),
            warehouse=factory.SubFactory(WarehouseFactory),
        )
        with_stock_fulfilled = factory.Trait(
            stock_allocated=factory.LazyAttribute(lambda o: o.quantity),
            stock_fulfilled=factory.LazyAttribute(lambda o: o.quantity),
            warehouse=factory.SubFactory(WarehouseFactory),
        )

        # Customizations trait
        with_customizations = factory.Trait(
            customizations=factory.LazyFunction(lambda: {
                'engraving': 'Happy Birthday!',
                'color': 'Blue',
                'size': 'Medium',
            })
        )


class OrderNoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'orders.OrderNote'

    order = factory.SubFactory(OrderFactory)
    author = factory.SubFactory(UserFactory, staff=True)
    note = factory.Faker('sentence', nb_words=10)
    is_customer_note = False
    is_read = False

    class Params:
        customer_note = factory.Trait(
            is_customer_note=True,
            author=factory.LazyAttribute(lambda o: o.order.user),
        )
        staff_note = factory.Trait(
            is_customer_note=False,
            author=factory.SubFactory(UserFactory, staff=True),
        )
        read = factory.Trait(is_read=True)


class RefundFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'orders.Refund'

    order = factory.SubFactory(OrderFactory, paid_order=True)
    processed_by = factory.SubFactory(UserFactory, staff=True)
    refund_type = 'full'
    reason = 'Customer requested refund'
    status = 'requested'

    # Refund amounts
    total_amount = factory.LazyAttribute(lambda o: o.order.total_amount)
    total_amount_currency = 'USD'
    shipping_refund_amount = Decimal('0.00')
    shipping_refund_amount_currency = 'USD'
    tax_refund_amount = Decimal('0.00')
    tax_refund_amount_currency = 'USD'

    # Base-currency equivalents
    total_amount_base = factory.LazyAttribute(lambda o: o.total_amount.amount if hasattr(o.total_amount, 'amount') else Decimal(str(o.total_amount)))
    shipping_refund_amount_base = factory.LazyAttribute(lambda o: Decimal(str(o.shipping_refund_amount)))
    tax_refund_amount_base = factory.LazyAttribute(lambda o: Decimal(str(o.tax_refund_amount)))

    # Refund method (dynamic - no hardcoded choices)
    refund_method = 'original_payment'
    refund_method_display = 'Original Payment Method'

    # Items being refunded (JSON)
    items_json = factory.LazyFunction(list)

    # Notes
    customer_notes = ''
    staff_notes = ''

    class Params:
        # Refund type traits
        full_refund = factory.Trait(
            refund_type='full',
            total_amount=factory.LazyAttribute(lambda o: o.order.total_amount),
            shipping_refund_amount=factory.LazyAttribute(lambda o: o.order.shipping_cost),
            tax_refund_amount=factory.LazyAttribute(lambda o: o.order.tax_amount),
        )
        partial_refund = factory.Trait(
            refund_type='partial',
            total_amount=Decimal('50.00'),
            shipping_refund_amount=Decimal('0.00'),
            tax_refund_amount=Decimal('4.44'),
        )

        # Status traits
        requested = factory.Trait(status='requested')
        approved = factory.Trait(
            status='approved',
            approved_at=factory.LazyFunction(timezone.now),
        )
        processing = factory.Trait(
            status='processing',
            approved_at=factory.LazyFunction(timezone.now),
        )
        completed = factory.Trait(
            status='completed',
            approved_at=factory.LazyFunction(timezone.now),
            processed_at=factory.LazyFunction(timezone.now),
            completed_at=factory.LazyFunction(timezone.now),
        )
        failed = factory.Trait(
            status='failed',
            approved_at=factory.LazyFunction(timezone.now),
            processed_at=factory.LazyFunction(timezone.now),
        )

        # POS refund trait
        pos_refund = factory.Trait(
            pos_terminal=factory.SubFactory(POSTerminalFactory),
            refund_method='cash',
            refund_method_display='Cash',
        )


class ReturnRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'orders.ReturnRequest'

    order = factory.SubFactory(OrderFactory, paid_order=True, delivered=True)
    user = factory.LazyAttribute(lambda o: o.order.user)
    reason = 'Product defective'
    status = 'pending'

    # Items being returned (JSON)
    items_json = factory.LazyFunction(lambda: [
        {
            'order_item_id': 1,
            'quantity': 1,
            'reason': 'Defective',
        }
    ])

    # Notes
    customer_notes = 'Product arrived damaged'
    merchant_notes = ''
    rejection_reason = ''
    inspection_notes = ''

    # Return details
    items_condition = None
    restocking_fee = Decimal('0.00')
    restocking_fee_currency = 'USD'

    # Return label tracking
    return_label_generated = False
    return_tracking_number = ''
    return_label_url = ''

    # Timestamps
    requested_at = factory.LazyFunction(timezone.now)

    class Params:
        # Status traits
        pending_return = factory.Trait(status='pending')
        approved_return = factory.Trait(
            status='approved',
            approved_at=factory.LazyFunction(timezone.now),
            approved_by=factory.SubFactory(UserFactory, staff=True),
        )
        rejected = factory.Trait(
            status='rejected',
            rejected_at=factory.LazyFunction(timezone.now),
            rejection_reason='Outside return window',
        )
        label_sent = factory.Trait(
            status='label_sent',
            approved_at=factory.LazyFunction(timezone.now),
            label_sent_at=factory.LazyFunction(timezone.now),
            return_label_generated=True,
            return_tracking_number=factory.LazyFunction(lambda: f'RET-{uuid.uuid4().hex[:12].upper()}'),
        )
        in_transit = factory.Trait(
            status='in_transit',
            approved_at=factory.LazyFunction(timezone.now),
            label_sent_at=factory.LazyFunction(timezone.now),
            return_label_generated=True,
            return_tracking_number=factory.LazyFunction(lambda: f'RET-{uuid.uuid4().hex[:12].upper()}'),
        )
        received = factory.Trait(
            status='received',
            approved_at=factory.LazyFunction(timezone.now),
            received_at=factory.LazyFunction(timezone.now),
        )
        inspected = factory.Trait(
            status='inspected',
            approved_at=factory.LazyFunction(timezone.now),
            received_at=factory.LazyFunction(timezone.now),
            inspected_at=factory.LazyFunction(timezone.now),
            inspected_by=factory.SubFactory(UserFactory, staff=True),
            items_condition='good',
            inspection_notes='Items in good condition',
        )
        completed_return = factory.Trait(
            status='completed',
            approved_at=factory.LazyFunction(timezone.now),
            received_at=factory.LazyFunction(timezone.now),
            inspected_at=factory.LazyFunction(timezone.now),
            completed_at=factory.LazyFunction(timezone.now),
            refund=factory.SubFactory(RefundFactory, completed=True),
        )

        # Restocking fee trait
        with_restocking_fee = factory.Trait(
            restocking_fee=Decimal('10.00'),
            restocking_fee_currency='USD',
        )


# ============================================================
# Custom Fields
# ============================================================

class CustomFieldGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'custom_fields.CustomFieldGroup'
        django_get_or_create = ('slug', 'content_type')

    name = factory.Sequence(lambda n: f'Field Group {n}')
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    content_type = factory.LazyFunction(
        lambda: __import__(
            'django.contrib.contenttypes.models', fromlist=['ContentType']
        ).ContentType.objects.get(app_label='catalog', model='product')
    )
    sort_order = 0
    is_active = True
    show_on_storefront = False


class CustomFieldDefinitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'custom_fields.CustomFieldDefinition'
        django_get_or_create = ('slug', 'content_type')

    group = factory.SubFactory(CustomFieldGroupFactory)
    content_type = factory.LazyAttribute(lambda o: o.group.content_type)
    name = factory.Sequence(lambda n: f'Custom Field {n}')
    slug = factory.LazyAttribute(lambda o: slugify(o.name).replace('-', '_'))
    field_type = 'text'
    help_text_value = ''
    is_required = False
    is_active = True
    show_on_storefront = False
    is_translatable = False
    sort_order = 0

    class Params:
        number = factory.Trait(field_type='number')
        decimal = factory.Trait(field_type='decimal')
        boolean = factory.Trait(field_type='boolean', default_value=False)
        select = factory.Trait(
            field_type='select',
            validation_config={'choices': [
                {'value': 'opt_a', 'label': 'Option A'},
                {'value': 'opt_b', 'label': 'Option B'},
                {'value': 'opt_c', 'label': 'Option C'},
            ]}
        )
        required = factory.Trait(is_required=True)
        storefront = factory.Trait(show_on_storefront=True)


# ============================================================
# Customer Messages
# ============================================================

class CustomerMessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'admin_api.CustomerMessage'

    user = factory.SubFactory(UserFactory)
    name = factory.LazyAttribute(
        lambda o: f"{o.user.first_name} {o.user.last_name}".strip() or o.user.email
    )
    email = factory.LazyAttribute(lambda o: o.user.email)
    subject = factory.Sequence(lambda n: f'Test Message {n}')
    message = 'This is a test message body.'
    message_type = 'general'
    status = 'unread'

    class Params:
        replied = factory.Trait(
            status='replied',
            reply_text='Thank you for your message.',
            replied_at=factory.LazyFunction(timezone.now),
        )
        anonymous = factory.Trait(
            user=None,
        )


# ============================================================
# Communication Preferences
# ============================================================

class CommunicationPreferenceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'accounts.CommunicationPreference'

    user = factory.SubFactory(UserFactory)
    email_enabled = True
    sms_enabled = False
    email_transactional = True
    email_marketing = False  # GDPR opt-out default
    sms_transactional = False
    sms_marketing = False
    email_verified = False
    sms_verified = False
    consent_source = 'registration'
    language_code = 'en'

    class Params:
        verified = factory.Trait(
            email_verified=True,
            email_verified_at=factory.LazyFunction(timezone.now),
        )
        marketing_opted_in = factory.Trait(
            email_marketing=True,
            email_verified=True,
            email_verified_at=factory.LazyFunction(timezone.now),
        )
        sms_opted_in = factory.Trait(
            sms_enabled=True,
            sms_transactional=True,
            sms_verified=True,
            sms_verified_at=factory.LazyFunction(timezone.now),
        )


class BlogSubscriberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'blog.BlogSubscriber'

    email = factory.Sequence(lambda n: f'subscriber_{n}@test.spwig.com')
    frequency = 'immediate'
    verification_status = 'verified'
    language = 'en'

    class Params:
        weekly = factory.Trait(frequency='weekly_digest')
        monthly = factory.Trait(frequency='monthly_digest')
        unverified = factory.Trait(verification_status='pending')


# ============================================================
# Media Library
# ============================================================

class MediaFolderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'media_library.MediaFolder'

    name = factory.Sequence(lambda n: f'Test Folder {n}')
    slug = factory.LazyAttribute(lambda obj: obj.name.lower().replace(' ', '-'))
    description = 'Test media folder'
    parent = None

    class Params:
        nested = factory.Trait(
            parent=factory.SubFactory('tests.factories.MediaFolderFactory')
        )


class ImageSizePresetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'media_library.ImageSizePreset'
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: f'test_preset_{n}')
    slug = factory.LazyAttribute(lambda obj: obj.name)
    display_name = factory.LazyAttribute(lambda obj: obj.name.replace('_', ' ').title())
    width = 800
    height = 600
    crop_mode = 'cover'
    quality = 85
    is_active = True
    is_system_preset = False

    class Params:
        small = factory.Trait(
            name='test_small',
            width=300,
            height=300
        )
        medium = factory.Trait(
            name='test_medium',
            width=600,
            height=600
        )
        large = factory.Trait(
            name='test_large',
            width=1200,
            height=1200
        )
        system = factory.Trait(is_system_preset=True)


class MediaAssetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'media_library.MediaAsset'

    title = factory.Sequence(lambda n: f'Test Asset {n}')
    alt_text = ''
    description = ''
    mime_type = 'image/jpeg'
    file_size = 102400  # 100KB
    width = 1920
    height = 1080
    folder = None
    uploaded_by = factory.SubFactory(UserFactory)
    is_public = False
    usage_count = 0

    # File fields need to be set by tests using actual files
    original_file = factory.django.FileField(filename='test_image.jpg')

    class Params:
        # Image types
        jpeg = factory.Trait(mime_type='image/jpeg')
        png = factory.Trait(mime_type='image/png')
        webp = factory.Trait(mime_type='image/webp')
        gif = factory.Trait(mime_type='image/gif')
        svg = factory.Trait(
            mime_type='image/svg+xml',
            width=None,
            height=None
        )

        # Video types
        video = factory.Trait(
            mime_type='video/mp4',
            width=1920,
            height=1080
        )
        webm = factory.Trait(
            mime_type='video/webm',
            width=1920,
            height=1080
        )

        # 3D model
        model_3d = factory.Trait(
            mime_type='model/gltf-binary',
            width=None,
            height=None
        )

        # Size variants
        small_image = factory.Trait(
            width=800,
            height=600,
            file_size=51200  # 50KB
        )
        large_image = factory.Trait(
            width=4000,
            height=3000,
            file_size=2097152  # 2MB
        )

        # With folder
        in_folder = factory.Trait(
            folder=factory.SubFactory(MediaFolderFactory)
        )

        # In use
        in_use = factory.Trait(usage_count=5, last_used_at=factory.LazyFunction(timezone.now))


class ThumbnailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'media_library.MediaThumbnail'

    media_asset = factory.SubFactory(MediaAssetFactory)
    size_preset = 'medium'  # CharField, not FK
    width = 800
    height = 600

    # File field needs actual file in tests
    file = factory.django.FileField(filename='test_thumbnail.jpg')
    webp_file = factory.django.FileField(filename='test_thumbnail.webp')

    class Params:
        small = factory.Trait(
            size_preset='small',
            width=300,
            height=300
        )
        medium = factory.Trait(
            size_preset='medium',
            width=600,
            height=600
        )
        large = factory.Trait(
            size_preset='large',
            width=1200,
            height=1200
        )


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'media_library.Tag'
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: f'test-tag-{n}')
    slug = factory.LazyAttribute(lambda obj: obj.name)

    @factory.post_generation
    def media_assets(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for asset in extracted:
                self.media_assets.add(asset)


class MediaProcessingJobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'media_library.MediaProcessingJob'

    media_asset = factory.SubFactory(MediaAssetFactory)
    user = factory.SubFactory(UserFactory)
    job_type = 'webp_conversion'
    status = 'pending'
    progress = 0
    error_message = ''

    class Params:
        thumbnail_gen = factory.Trait(job_type='generate_thumbnails')
        webp_conv = factory.Trait(job_type='webp_conversion')
        video_conv = factory.Trait(job_type='video_conversion')

        processing = factory.Trait(status='processing', progress=50)
        completed = factory.Trait(status='completed', progress=100)
        failed = factory.Trait(
            status='failed',
            error_message='Test error message'
        )


# ============================================================
# Component Registry
# ============================================================

class ComponentRegistryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'component_updates.ComponentRegistry'
        django_get_or_create = ('slug', 'component_type')

    component_type = 'payment_provider'
    slug = factory.Sequence(lambda n: f'test-provider-{n}')
    name = factory.Sequence(lambda n: f'Test Provider {n}')
    current_version = '1.0.0'
    author = 'Spwig'
    description = 'Test payment provider'

    class Params:
        stripe = factory.Trait(
            slug='stripe',
            name='Stripe',
            description='Stripe payment processing',
        )
        paypal = factory.Trait(
            slug='paypal_checkout',
            name='PayPal Checkout',
            description='PayPal checkout processing',
        )
        airwallex = factory.Trait(
            slug='airwallex',
            name='AirWallex',
            description='AirWallex payment processing',
        )


# ============================================================
# Payment Providers
# ============================================================

class PaymentProviderAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'payment_providers.PaymentProviderAccount'

    component = factory.SubFactory(ComponentRegistryFactory, stripe=True)
    user = factory.SubFactory(UserFactory, staff=True)
    display_name = 'Test Stripe'
    is_active = True
    is_default = True
    checkout_mode = 'hosted'
    connection_status = 'connected'
    settings = factory.LazyFunction(dict)
    available_payment_methods = factory.LazyFunction(lambda: {'US': ['card'], 'GB': ['card'], 'DE': ['card']})
    enabled_payment_methods = factory.LazyFunction(lambda: {'US': ['card'], 'GB': ['card'], 'DE': ['card']})

    @factory.lazy_attribute
    def credentials_encrypted(self):
        """Encrypt test credentials using the payment provider encryption utility."""
        import os
        from payment_providers.utils.encryption import encrypt_credentials
        return encrypt_credentials({
            'secret_key': os.environ.get('STRIPE_TEST_SECRET_KEY', 'sk_test_placeholder'),
            'publishable_key': os.environ.get('STRIPE_TEST_PUBLISHABLE_KEY', 'pk_test_placeholder'),
            'webhook_secret': os.environ.get('STRIPE_TEST_WEBHOOK_SECRET', 'whsec_test_placeholder'),
            'environment': 'test',
        })

    class Params:
        hosted = factory.Trait(checkout_mode='hosted')
        integrated = factory.Trait(checkout_mode='integrated')


# ============================================================
# Configurator 3D
# ============================================================

class ConfigurationSlotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'catalog.ConfigurationSlot'
        django_get_or_create = ('product', 'slug')

    product = factory.SubFactory(ProductFactory, product_type='configurable')
    name = factory.Sequence(lambda n: f'Slot {n}')
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    sort_order = 0
    is_required = True
    min_selections = 1
    max_selections = 1


class ConfigurationSlotOptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'catalog.ConfigurationSlotOption'

    slot = factory.SubFactory(ConfigurationSlotFactory)
    option_product = factory.SubFactory(ProductFactory)
    sort_order = 0
    is_default = False
    quantity = 1


class SceneConfigFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'configurator_3d.SceneConfig'

    product = factory.SubFactory(ProductFactory, product_type='configurable')
    camera_orbit = '0deg 75deg 2m'
    camera_target = '0m 0m 0m'
    exposure = 1.0
    shadow_intensity = 0.5
    auto_rotate = True
    ar_enabled = True
    background_color = '#ffffff'
    is_enabled = True
    node_tree = factory.LazyFunction(dict)


class NodeMappingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'configurator_3d.NodeMapping'

    scene_config = factory.SubFactory(SceneConfigFactory)
    slot_option = factory.SubFactory(ConfigurationSlotOptionFactory)
    action_type = 'material_color'
    target_node = 'Body'
    action_data = factory.LazyFunction(lambda: {'color': '#ff0000'})
    sort_order = 0


class GeometryAssetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'configurator_3d.GeometryAsset'

    scene_config = factory.SubFactory(SceneConfigFactory)
    label = factory.Sequence(lambda n: f'Geometry Asset {n}')
    media_asset = factory.SubFactory(MediaAssetFactory, model_3d=True)
    target_node = 'Collar'
    node_data = factory.LazyFunction(dict)


class TextureAssetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'configurator_3d.TextureAsset'

    scene_config = factory.SubFactory(SceneConfigFactory)
    label = factory.Sequence(lambda n: f'Texture Asset {n}')
    media_asset = factory.SubFactory(MediaAssetFactory)
    texture_type = 'base_color'


# ============================================================
# Email System
# ============================================================

class EmailAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'email_system.EmailAccount'

    site = factory.LazyFunction(lambda: __import__('django.contrib.sites.models', fromlist=['Site']).Site.objects.get(pk=1))
    name = factory.Sequence(lambda n: f'Email Account {n}')
    from_email = factory.Sequence(lambda n: f'sender{n}@test.spwig.com')
    from_name = factory.Sequence(lambda n: f'Sender {n}')
    provider_key = 'builtin_smtp'
    credentials = factory.LazyFunction(
        lambda: __import__('email_system.utils.encryption', fromlist=['encrypt_credentials']).encrypt_credentials({
            'host': 'smtp.test.com', 'port': 587, 'username': 'test', 'password': 'test'
        })
    )
    is_active = True
    is_default = False
    settings = factory.LazyFunction(dict)
    connection_status = 'unknown'

    class Params:
        default = factory.Trait(is_default=True)
        inactive = factory.Trait(is_active=False)
        connected = factory.Trait(connection_status='connected')


class EmailTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'email_system.EmailTemplate'

    site = factory.LazyFunction(lambda: __import__('django.contrib.sites.models', fromlist=['Site']).Site.objects.get(pk=1))
    template_type = 'order_confirmation'
    language_code = 'en'
    subject = factory.Sequence(lambda n: f'Test Subject {n}')
    html_content = '<mjml><mj-body><mj-section><mj-column><mj-text>Hello {{ customer_name }}</mj-text></mj-column></mj-section></mj-body></mjml>'
    text_content = 'Hello {{ customer_name }}'
    is_active = True
    is_system = False
    version = 1

    class Params:
        system = factory.Trait(is_system=True)
        inactive = factory.Trait(is_active=False)
        deleted = factory.Trait(is_deleted=True, deleted_at=factory.LazyFunction(timezone.now))


class EmailOutboxFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'email_system.EmailOutbox'

    site = factory.LazyFunction(lambda: __import__('django.contrib.sites.models', fromlist=['Site']).Site.objects.get(pk=1))
    to_email = factory.Sequence(lambda n: f'recipient{n}@test.spwig.com')
    from_email = 'noreply@test.spwig.com'
    from_name = 'Test Store'
    subject = factory.Sequence(lambda n: f'Test Email {n}')
    html_body = '<html><body>Test</body></html>'
    text_body = 'Test'
    template_type = 'order_confirmation'
    status = 'queued'
    priority = 5

    class Params:
        sent = factory.Trait(status='sent', sent_at=factory.LazyFunction(timezone.now))
        failed = factory.Trait(status='failed', error_message='Test error', failed_at=factory.LazyFunction(timezone.now))
        skipped = factory.Trait(status='skipped', skip_reason='user_preference_disabled')


class EmailEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'email_system.EmailEvent'

    email = factory.SubFactory(EmailOutboxFactory)
    event_type = 'delivered'
    event_data = factory.LazyFunction(dict)

    class Params:
        opened = factory.Trait(event_type='opened', user_agent='Mozilla/5.0', ip_address='127.0.0.1')
        clicked = factory.Trait(event_type='clicked', user_agent='Mozilla/5.0', ip_address='127.0.0.1')
        bounced = factory.Trait(event_type='bounced', bounce_type='hard', bounce_reason='Mailbox not found')


# ============================================================
# GeoIP
# ============================================================

class GeoLocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'geoip.GeoLocation'
        django_get_or_create = ('ip_address',)

    ip_address = factory.Sequence(lambda n: f'203.0.113.{n % 256}')
    ip_prefix = factory.LazyAttribute(lambda o: '.'.join(o.ip_address.split('.')[:3]) + '.0/24')
    country_code = 'US'
    country_name = 'United States'
    region_code = 'CA'
    region_name = 'California'
    city_name = 'San Francisco'
    postal_code = '94102'
    latitude = 37.7749
    longitude = -122.4194
    source = 'test'
    confidence = 0.95

    class Params:
        expired = factory.Trait(
            expires_at=factory.LazyFunction(lambda: timezone.now() - timedelta(hours=1))
        )
        vpn = factory.Trait(is_vpn=True)
        proxy = factory.Trait(is_proxy=True)
        tor = factory.Trait(is_tor=True)
        mobile = factory.Trait(is_mobile=True)


class CountryMappingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'geoip.CountryMapping'
        django_get_or_create = ('country_code',)

    country_code = 'US'
    country_name = 'United States'
    default_currency = 'USD'
    accepted_currencies = ['USD', 'CAD']
    default_language = 'en'
    supported_languages = ['en', 'es']
    timezone = 'America/New_York'
    date_format = 'MM/DD/YYYY'
    uses_metric = False
    tax_rate = Decimal('0.00')
    is_eu_member = False
    requires_vat = False
    is_active = True

    class Params:
        eu = factory.Trait(
            is_eu_member=True,
            requires_vat=True,
            default_currency='EUR',
            uses_metric=True,
        )


class GeoIPProviderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'geoip.GeoIPProvider'

    name = factory.Sequence(lambda n: f'Test Provider {n}')
    provider_type = 'spwig'
    is_active = True
    priority = factory.Sequence(lambda n: n)
    config = factory.LazyFunction(dict)

    class Params:
        maxmind = factory.Trait(
            name='MaxMind GeoLite2',
            provider_type='maxmind',
            config={'license_key': 'test_key'},
        )


class VisitorLocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'geoip.VisitorLocation'

    session_key = factory.Sequence(lambda n: f'session_{n:08d}')
    ip_address = factory.Sequence(lambda n: f'198.51.100.{n % 256}')
    resolved_country = 'US'
    resolved_region = 'California'
    resolved_city = 'San Francisco'
    device_type = 'desktop'
    page_views = 1

    class Params:
        corrected = factory.Trait(
            actual_country='CA',
            actual_region='Ontario',
            actual_city='Toronto',
        )
        mobile_device = factory.Trait(device_type='mobile')
        tablet_device = factory.Trait(device_type='tablet')


class BusinessRuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'geoip.BusinessRule'

    name = factory.Sequence(lambda n: f'Test Rule {n}')
    description = 'Test business rule'
    is_active = True
    priority = factory.Sequence(lambda n: n)
    conditions = factory.LazyFunction(lambda: {'country_in': ['US', 'CA']})
    actions = factory.LazyFunction(lambda: {'set_currency': 'USD'})
