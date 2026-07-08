"""
Tests for Catalog models, with comprehensive coverage of Customization features.
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from djmoney.money import Money
from catalog.models import (
    Category, Product, CustomizationOption, CustomizationValue,
    Brand
)
from orders.models import Order, OrderItem
from media_library.models import MediaAsset

User = get_user_model()


class CustomizationOptionModelTest(TestCase):
    """Tests for CustomizationOption model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Create category
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

        # Create product
        self.product = Product.objects.create(
            name='Custom T-Shirt',
            slug='custom-tshirt',
            sku='TSH-001',
            category=self.category,
            price=Money(25.00, 'USD'),
            allow_customization=True,
            status='published'
        )

    def test_create_text_customization_option(self):
        """Test creating a text input customization option"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Engraving Text',
            option_type='text',
            is_required=True,
            max_length=50,
            pricing_type='fixed',
            price_amount=Money(10.00, 'USD')
        )

        self.assertEqual(option.product, self.product)
        self.assertEqual(option.name, 'Engraving Text')
        self.assertEqual(option.option_type, 'text')
        self.assertTrue(option.is_required)
        self.assertEqual(option.max_length, 50)
        self.assertEqual(option.pricing_type, 'fixed')
        self.assertEqual(option.price_amount, Money(10.00, 'USD'))

    def test_auto_slug_generation(self):
        """Test that slug is auto-generated from name"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Wood Type Selection',
            option_type='select'
        )

        self.assertEqual(option.slug, 'wood-type-selection')

    def test_validate_value_text_required(self):
        """Test validation for required text field"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Name',
            option_type='text',
            is_required=True,
            max_length=20
        )

        # Test required validation
        is_valid, error = option.validate_value('')
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

        # Test valid value
        is_valid, error = option.validate_value('John Doe')
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_value_text_max_length(self):
        """Test max length validation for text"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Initials',
            option_type='text',
            is_required=False,
            max_length=3
        )

        # Valid length
        is_valid, error = option.validate_value('JD')
        self.assertTrue(is_valid)

        # Exceeds max length
        is_valid, error = option.validate_value('ABCD')
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

    def test_validate_value_number_range(self):
        """Test min/max validation for numeric input"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Desk Width',
            option_type='number',
            min_value=Decimal('24.00'),
            max_value=Decimal('72.00')
        )

        # Within range
        is_valid, error = option.validate_value('48.5')
        self.assertTrue(is_valid)

        # Below minimum
        is_valid, error = option.validate_value('20')
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

        # Above maximum
        is_valid, error = option.validate_value('80')
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

    def test_validate_value_select(self):
        """Test validation for dropdown selections"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Wood Type',
            option_type='select',
            choices=[
                {'value': 'oak', 'label': 'Oak', 'price_modifier': 0},
                {'value': 'walnut', 'label': 'Walnut', 'price_modifier': 25},
                {'value': 'maple', 'label': 'Maple', 'price_modifier': 15}
            ]
        )

        # Valid choice
        is_valid, error = option.validate_value('oak')
        self.assertTrue(is_valid)

        # Invalid choice
        is_valid, error = option.validate_value('pine')
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

    def test_validate_value_color(self):
        """Test validation for color picker"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Thread Color',
            option_type='color'
        )

        # Valid hex color
        is_valid, error = option.validate_value('#FF5733')
        self.assertTrue(is_valid)

        # Invalid format
        is_valid, error = option.validate_value('red')
        self.assertFalse(is_valid)

        # Missing #
        is_valid, error = option.validate_value('FF5733')
        self.assertFalse(is_valid)

    def test_calculate_price_free(self):
        """Test price calculation for free customization"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Gift Message',
            option_type='textarea',
            pricing_type='free'
        )

        base_price = Money(25.00, 'USD')
        additional_price = option.calculate_price('Happy Birthday!', base_price)

        self.assertEqual(additional_price, Money(0, 'USD'))

    def test_calculate_price_fixed(self):
        """Test fixed fee pricing"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Engraving',
            option_type='text',
            pricing_type='fixed',
            price_amount=Money(15.00, 'USD')
        )

        base_price = Money(50.00, 'USD')
        additional_price = option.calculate_price('John', base_price)

        self.assertEqual(additional_price, Money(15.00, 'USD'))

    def test_calculate_price_percentage(self):
        """Test percentage-based pricing"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Premium Finish',
            option_type='select',
            pricing_type='percentage',
            price_amount=Money(20.00, 'USD')  # 20% stored as 20.00
        )

        base_price = Money(100.00, 'USD')
        additional_price = option.calculate_price('premium', base_price)

        # 20% of $100 = $20
        self.assertEqual(additional_price, Money(20.00, 'USD'))

    def test_calculate_price_per_unit_text(self):
        """Test per-character pricing for text"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Monogram',
            option_type='text',
            pricing_type='per_unit',
            price_amount=Money(2.50, 'USD')  # $2.50 per character
        )

        base_price = Money(50.00, 'USD')
        text_value = 'ABC'  # 3 characters
        additional_price = option.calculate_price(text_value, base_price)

        # 3 chars * $2.50 = $7.50
        self.assertEqual(additional_price, Money(7.50, 'USD'))

    def test_calculate_price_per_unit_number(self):
        """Test per-unit pricing for numeric input"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Desk Length (inches)',
            option_type='number',
            pricing_type='per_unit',
            price_amount=Money(5.00, 'USD')  # $5 per inch
        )

        base_price = Money(200.00, 'USD')
        additional_price = option.calculate_price('48', base_price)

        # 48 inches * $5 = $240
        self.assertEqual(additional_price, Money(240.00, 'USD'))

    def test_calculate_price_select_with_choice_modifier(self):
        """Test pricing with per-choice price modifiers"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Wood Type',
            option_type='select',
            pricing_type='free',  # Base pricing is free, but choices have modifiers
            choices=[
                {'value': 'oak', 'label': 'Oak', 'price_modifier': 0},
                {'value': 'walnut', 'label': 'Walnut', 'price_modifier': 50},
                {'value': 'cherry', 'label': 'Cherry', 'price_modifier': 35}
            ]
        )

        base_price = Money(100.00, 'USD')

        # Oak (no modifier)
        price = option.calculate_price('oak', base_price)
        self.assertEqual(price, Money(0, 'USD'))

        # Walnut (+$50)
        price = option.calculate_price('walnut', base_price)
        self.assertEqual(price, Money(50, 'USD'))

    def test_sort_order(self):
        """Test that customization options are ordered correctly"""
        opt1 = CustomizationOption.objects.create(
            product=self.product,
            name='Option 3',
            option_type='text',
            sort_order=30
        )
        opt2 = CustomizationOption.objects.create(
            product=self.product,
            name='Option 1',
            option_type='text',
            sort_order=10
        )
        opt3 = CustomizationOption.objects.create(
            product=self.product,
            name='Option 2',
            option_type='text',
            sort_order=20
        )

        options = list(CustomizationOption.objects.filter(product=self.product))
        self.assertEqual(options[0], opt2)  # sort_order 10
        self.assertEqual(options[1], opt3)  # sort_order 20
        self.assertEqual(options[2], opt1)  # sort_order 30


class CustomizationValueModelTest(TestCase):
    """Tests for CustomizationValue model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Create category
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

        # Create product
        self.product = Product.objects.create(
            name='Custom Product',
            slug='custom-product',
            sku='CUST-001',
            category=self.category,
            price=Money(100.00, 'USD'),
            allow_customization=True,
            status='published'
        )

        # Create order
        self.order = Order.objects.create(
            user=self.user,
            email='test@example.com',
            status='pending',
            subtotal=Money(100.00, 'USD'),
            total_amount=Money(100.00, 'USD')
        )

        # Create order item
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            unit_price=Money(100.00, 'USD'),
            total_price=Money(100.00, 'USD')
        )

    def test_create_text_customization_value(self):
        """Test creating a text customization value"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Engraving Text',
            option_type='text'
        )

        value = CustomizationValue.objects.create(
            order_item=self.order_item,
            customization_option=option,
            text_value='Happy Birthday!',
            calculated_price=Money(10.00, 'USD')
        )

        self.assertEqual(value.text_value, 'Happy Birthday!')
        self.assertEqual(value.calculated_price, Money(10.00, 'USD'))

    def test_get_display_value_text(self):
        """Test display value for text input"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Name',
            option_type='text'
        )

        value = CustomizationValue.objects.create(
            order_item=self.order_item,
            customization_option=option,
            text_value='John Doe'
        )

        self.assertEqual(value.get_display_value(), 'John Doe')

    def test_get_display_value_number(self):
        """Test display value for numeric input"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Quantity',
            option_type='number'
        )

        value = CustomizationValue.objects.create(
            order_item=self.order_item,
            customization_option=option,
            number_value=Decimal('42.5')
        )

        self.assertEqual(value.get_display_value(), '42.5')

    def test_get_display_value_select(self):
        """Test display value for dropdown selection"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Wood Type',
            option_type='select',
            choices=[
                {'value': 'oak', 'label': 'Oak Wood'},
                {'value': 'walnut', 'label': 'Walnut Wood'}
            ]
        )

        value = CustomizationValue.objects.create(
            order_item=self.order_item,
            customization_option=option,
            choice_value='oak'
        )

        # Should return the label from choices
        self.assertEqual(value.get_display_value(), 'Oak Wood')

    def test_get_display_value_color(self):
        """Test display value for color picker"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Thread Color',
            option_type='color'
        )

        value = CustomizationValue.objects.create(
            order_item=self.order_item,
            customization_option=option,
            choice_value='#FF5733'
        )

        self.assertEqual(value.get_display_value(), '#FF5733')

    def test_get_value_for_export_text(self):
        """Test export value for text input"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Message',
            option_type='textarea'
        )

        value = CustomizationValue.objects.create(
            order_item=self.order_item,
            customization_option=option,
            text_value='Thank you for your business!'
        )

        export_data = value.get_value_for_export()

        self.assertEqual(export_data['type'], 'textarea')
        self.assertEqual(export_data['value'], 'Thank you for your business!')

    def test_get_value_for_export_number(self):
        """Test export value for numeric input"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Width',
            option_type='number'
        )

        value = CustomizationValue.objects.create(
            order_item=self.order_item,
            customization_option=option,
            number_value=Decimal('48.50')
        )

        export_data = value.get_value_for_export()

        self.assertEqual(export_data['type'], 'number')
        self.assertEqual(export_data['value'], 48.5)

    def test_get_value_for_export_select(self):
        """Test export value for dropdown selection"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Material',
            option_type='select',
            choices=[
                {'value': 'cotton', 'label': '100% Cotton'},
                {'value': 'polyester', 'label': 'Polyester Blend'}
            ]
        )

        value = CustomizationValue.objects.create(
            order_item=self.order_item,
            customization_option=option,
            choice_value='cotton'
        )

        export_data = value.get_value_for_export()

        self.assertEqual(export_data['type'], 'select')
        self.assertEqual(export_data['value'], 'cotton')
        self.assertEqual(export_data['label'], '100% Cotton')

    def test_str_representation(self):
        """Test string representation of CustomizationValue"""
        option = CustomizationOption.objects.create(
            product=self.product,
            name='Engraving',
            option_type='text'
        )

        value = CustomizationValue.objects.create(
            order_item=self.order_item,
            customization_option=option,
            text_value='John Doe'
        )

        expected = 'Engraving: John Doe'
        self.assertEqual(str(value), expected)


class ProductCustomizationIntegrationTest(TestCase):
    """Integration tests for product customization workflow"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.category = Category.objects.create(
            name='Custom Furniture',
            slug='custom-furniture'
        )

        # Create a customizable product
        self.product = Product.objects.create(
            name='Custom Desk',
            slug='custom-desk',
            sku='DESK-001',
            category=self.category,
            price=Money(500.00, 'USD'),
            allow_customization=True,
            status='published'
        )

    def test_complete_customization_workflow(self):
        """Test complete workflow from option creation to order value"""
        # Create customization options
        wood_option = CustomizationOption.objects.create(
            product=self.product,
            name='Wood Type',
            option_type='select',
            sort_order=1,
            is_required=True,
            pricing_type='free',
            choices=[
                {'value': 'oak', 'label': 'Oak', 'price_modifier': 0},
                {'value': 'walnut', 'label': 'Walnut', 'price_modifier': 100},
                {'value': 'cherry', 'label': 'Cherry', 'price_modifier': 75}
            ]
        )

        width_option = CustomizationOption.objects.create(
            product=self.product,
            name='Desk Width (inches)',
            option_type='number',
            sort_order=2,
            is_required=True,
            min_value=Decimal('36'),
            max_value=Decimal('84'),
            pricing_type='per_unit',
            price_amount=Money(5.00, 'USD')
        )

        engraving_option = CustomizationOption.objects.create(
            product=self.product,
            name='Nameplate Engraving',
            option_type='text',
            sort_order=3,
            is_required=False,
            max_length=30,
            pricing_type='fixed',
            price_amount=Money(25.00, 'USD')
        )

        # Validate customer inputs
        wood_valid, wood_error = wood_option.validate_value('walnut')
        self.assertTrue(wood_valid)

        width_valid, width_error = width_option.validate_value('60')
        self.assertTrue(width_valid)

        engraving_valid, engraving_error = engraving_option.validate_value('Executive Office')
        self.assertTrue(engraving_valid)

        # Calculate prices
        base_price = self.product.price
        wood_price = wood_option.calculate_price('walnut', base_price)
        width_price = width_option.calculate_price('60', base_price)
        engraving_price = engraving_option.calculate_price('Executive Office', base_price)

        total_customization = wood_price + width_price + engraving_price

        # Expected: Walnut (+$100) + 60 inches * $5 ($300) + Engraving ($25) = $425
        self.assertEqual(total_customization, Money(425.00, 'USD'))

        # Create order with customizations
        order = Order.objects.create(
            user=self.user,
            email='test@example.com',
            status='pending',
            subtotal=base_price.amount + total_customization.amount,
            total_amount=base_price.amount + total_customization.amount
        )

        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
            unit_price=base_price,
            total_price=base_price.amount + total_customization.amount
        )

        # Create customization values
        CustomizationValue.objects.create(
            order_item=order_item,
            customization_option=wood_option,
            choice_value='walnut',
            calculated_price=wood_price
        )

        CustomizationValue.objects.create(
            order_item=order_item,
            customization_option=width_option,
            number_value=Decimal('60'),
            calculated_price=width_price
        )

        CustomizationValue.objects.create(
            order_item=order_item,
            customization_option=engraving_option,
            text_value='Executive Office',
            calculated_price=engraving_price
        )

        # Verify all customizations are stored
        customizations = order_item.customization_values.all()
        self.assertEqual(customizations.count(), 3)

        # Verify total price
        self.assertEqual(order.total_amount, Money(925.00, 'USD'))  # $500 + $425

    def test_product_allows_customization_flag(self):
        """Test that allow_customization flag works correctly"""
        self.assertTrue(self.product.allow_customization)

        # Create non-customizable product
        simple_product = Product.objects.create(
            name='Standard Chair',
            slug='standard-chair',
            sku='CHAIR-001',
            category=self.category,
            price=Money(150.00, 'USD'),
            allow_customization=False
        )

        self.assertFalse(simple_product.allow_customization)


class CustomizationAPITest(TestCase):
    """Tests for Customization API endpoints"""

    def setUp(self):
        """Set up test data"""
        from rest_framework.test import APIClient
        from core.models import SiteSettings

        self.client = APIClient()

        # Create site settings (required for middleware)
        SiteSettings.objects.create(
            pk=1,
            admin_email='admin@example.com',
            default_currency='USD',
            enable_multi_warehouse=False
        )

        # Create category
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

        # Create customizable product
        self.product = Product.objects.create(
            name='Custom T-Shirt',
            slug='custom-tshirt',
            sku='TSH-001',
            category=self.category,
            product_type='physical',
            price=Money(25.00, 'USD'),
            allow_customization=True,
            status='published',
            track_inventory=False
        )

        # Create customization options
        self.text_option = CustomizationOption.objects.create(
            product=self.product,
            name='Name to Print',
            slug='name-to-print',
            option_type='text',
            is_required=True,
            max_length=20,
            pricing_type='fixed',
            price_amount=Money(5.00, 'USD'),
            sort_order=1
        )

        self.color_option = CustomizationOption.objects.create(
            product=self.product,
            name='Thread Color',
            slug='thread-color',
            option_type='select',
            is_required=False,
            pricing_type='free',
            choices=[
                {'value': 'red', 'label': 'Red', 'price_modifier': 0},
                {'value': 'blue', 'label': 'Blue', 'price_modifier': 2},
                {'value': 'gold', 'label': 'Gold', 'price_modifier': 5}
            ],
            sort_order=2
        )

        # Create non-customizable product
        self.simple_product = Product.objects.create(
            name='Standard T-Shirt',
            slug='standard-tshirt',
            sku='TSH-002',
            category=self.category,
            product_type='physical',
            price=Money(20.00, 'USD'),
            allow_customization=False,
            status='published',
            track_inventory=False
        )

    def test_get_customization_options_success(self):
        """Test retrieving customization options for a product"""
        url = f'/api/catalog/products/{self.product.slug}/customization_options/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['allow_customization'])
        self.assertEqual(len(response.data['options']), 2)

        # Check first option (sorted by sort_order)
        option1 = response.data['options'][0]
        self.assertEqual(option1['name'], 'Name to Print')
        self.assertEqual(option1['option_type'], 'text')
        self.assertTrue(option1['is_required'])
        self.assertEqual(option1['max_length'], 20)
        self.assertEqual(option1['pricing_type'], 'fixed')
        self.assertEqual(float(option1['price_amount']), 5.00)
        self.assertEqual(option1['price_currency'], 'USD')

        # Check second option
        option2 = response.data['options'][1]
        self.assertEqual(option2['name'], 'Thread Color')
        self.assertEqual(option2['option_type'], 'select')
        self.assertFalse(option2['is_required'])
        self.assertEqual(len(option2['choices']), 3)

    def test_get_customization_options_non_customizable(self):
        """Test retrieving customization options for non-customizable product"""
        url = f'/api/catalog/products/{self.simple_product.slug}/customization_options/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['allow_customization'])
        self.assertEqual(len(response.data['options']), 0)

    def test_get_customization_options_product_not_found(self):
        """Test retrieving customization options for non-existent product"""
        url = '/api/catalog/products/non-existent-product/customization_options/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_validate_customizations_success(self):
        """Test validating customizations with all required fields"""
        url = f'/api/catalog/products/{self.product.slug}/validate_customizations/'
        data = {
            'customizations': {
                str(self.text_option.id): 'John Doe',
                str(self.color_option.id): 'gold'
            }
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['valid'])

        # Check validated customizations
        validated = response.data['validated_customizations']
        self.assertIn(str(self.text_option.id), validated)
        self.assertEqual(validated[str(self.text_option.id)]['value'], 'John Doe')
        self.assertEqual(
            Decimal(validated[str(self.text_option.id)]['calculated_price']),
            Decimal('5.00')
        )

        # Check gold thread price (price_modifier = 5)
        self.assertEqual(
            Decimal(validated[str(self.color_option.id)]['calculated_price']),
            Decimal('5.00')
        )

        # Check total customization price ($5 text + $5 gold = $10)
        self.assertEqual(
            Decimal(response.data['total_customization_price']['amount']),
            Decimal('10.00')
        )

        # Check total product price ($25 base + $10 customizations = $35)
        self.assertEqual(
            Decimal(response.data['total_product_price']['amount']),
            Decimal('35.00')
        )

    def test_validate_customizations_missing_required(self):
        """Test validation fails when required customization is missing"""
        url = f'/api/catalog/products/{self.product.slug}/validate_customizations/'
        data = {
            'customizations': {
                str(self.color_option.id): 'red'
            }
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['valid'])
        self.assertIn('errors', response.data)

    def test_validate_customizations_invalid_value(self):
        """Test validation fails with invalid value (text too long)"""
        url = f'/api/catalog/products/{self.product.slug}/validate_customizations/'
        data = {
            'customizations': {
                str(self.text_option.id): 'This is a very long name that exceeds the twenty character limit',
                str(self.color_option.id): 'red'
            }
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['valid'])

    def test_validate_customizations_invalid_choice(self):
        """Test validation fails with invalid choice value"""
        url = f'/api/catalog/products/{self.product.slug}/validate_customizations/'
        data = {
            'customizations': {
                str(self.text_option.id): 'John',
                str(self.color_option.id): 'purple'  # Not in choices
            }
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['valid'])

    def test_validate_customizations_non_customizable_product(self):
        """Test validation fails for non-customizable product"""
        url = f'/api/catalog/products/{self.simple_product.slug}/validate_customizations/'
        data = {
            'customizations': {
                'some_option': 'some_value'
            }
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['valid'])
        self.assertIn('does not support customization', response.data['errors'][0])

    def test_validate_customizations_empty_data(self):
        """Test validation with empty customizations"""
        url = f'/api/catalog/products/{self.product.slug}/validate_customizations/'
        data = {
            'customizations': {}
        }
        response = self.client.post(url, data, format='json')

        # Should fail because text_option is required
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['valid'])
