"""
Tests for Product Customization API endpoints.
Verifies customization_options and validate_customizations actions.
"""
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from catalog.models import Product, Category, CustomizationOption
from djmoney.money import Money
from decimal import Decimal


class CustomizationOptionsAPITest(APITestCase):
    """Test /api/catalog/products/{slug}/customization_options/ endpoint"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()

        # Create site settings (required for middleware)
        from core.models import SiteSettings
        from django.contrib.sites.models import Site

        # Ensure Site exists
        if not Site.objects.filter(pk=1).exists():
            Site.objects.create(pk=1, domain='testserver', name='Test Site')

        # Use get_or_create to avoid conflicts between test methods
        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'admin_email': 'admin@example.com',
                'default_currency': 'USD',
                'enable_multi_warehouse': False
            }
        )

        # Create category
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

        # Create product with customization enabled
        self.product = Product.objects.create(
            name='Custom T-Shirt',
            slug='custom-tshirt',
            sku='TSH-001',
            price=Money(25, 'USD'),
            allow_customization=True,
            category=self.category,
            status='published'
        )

        # Create customization options
        self.text_option = CustomizationOption.objects.create(
            product=self.product,
            name='Name on Back',
            slug='name-on-back',
            description='Add your name to the back of the shirt',
            option_type='text',
            is_required=False,
            pricing_type='per_unit',
            price_amount=Money('0.50', 'USD'),
            max_length=20,
            sort_order=1
        )

        self.color_option = CustomizationOption.objects.create(
            product=self.product,
            name='Thread Color',
            slug='thread-color',
            description='Choose thread color for embroidery',
            option_type='select',
            is_required=True,
            pricing_type='fixed',
            price_amount=Money('5.00', 'USD'),
            choices=[
                {'value': 'white', 'label': 'White Thread', 'price_modifier': 0},
                {'value': 'gold', 'label': 'Gold Thread', 'price_modifier': 10.00}
            ],
            sort_order=2
        )

        # Create non-customizable product
        self.standard_product = Product.objects.create(
            name='Standard T-Shirt',
            slug='standard-tshirt',
            sku='TSH-002',
            price=Money(20, 'USD'),
            allow_customization=False,
            category=self.category,
            status='published'
        )

    def test_get_customization_options_success(self):
        """Test retrieving customization options for customizable product"""
        url = reverse('catalog_api:product-customization-options', kwargs={'slug': self.product.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['allow_customization'], True)
        self.assertEqual(len(response.data['options']), 2)

        # Verify first option (text)
        text_opt = response.data['options'][0]
        self.assertEqual(text_opt['name'], 'Name on Back')
        self.assertEqual(text_opt['slug'], 'name-on-back')
        self.assertEqual(text_opt['option_type'], 'text')
        self.assertEqual(text_opt['is_required'], False)
        self.assertEqual(text_opt['pricing_type'], 'per_unit')
        self.assertEqual(Decimal(text_opt['price_amount']), Decimal('0.50'))
        self.assertEqual(text_opt['max_length'], 20)

        # Verify second option (select)
        color_opt = response.data['options'][1]
        self.assertEqual(color_opt['name'], 'Thread Color')
        self.assertEqual(color_opt['option_type'], 'select')
        self.assertEqual(color_opt['is_required'], True)
        self.assertEqual(len(color_opt['choices']), 2)
        self.assertEqual(color_opt['choices'][0]['value'], 'white')
        self.assertEqual(color_opt['choices'][1]['value'], 'gold')

    def test_get_customization_options_non_customizable(self):
        """Test retrieving options for non-customizable product"""
        url = reverse('catalog_api:product-customization-options', kwargs={'slug': self.standard_product.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['allow_customization'], False)
        self.assertEqual(response.data['options'], [])

    def test_get_customization_options_product_not_found(self):
        """Test retrieving options for non-existent product"""
        url = reverse('catalog_api:product-customization-options', kwargs={'slug': 'nonexistent'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_customization_options_in_product_detail(self):
        """Test that customization_options are included in product detail endpoint"""
        url = reverse('catalog_api:product-detail', kwargs={'slug': self.product.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['allow_customization'], True)
        self.assertIn('customization_options', response.data)
        self.assertEqual(len(response.data['customization_options']), 2)

    def test_customization_options_ordering(self):
        """Test that options are returned in correct sort_order"""
        url = reverse('catalog_api:product-customization-options', kwargs={'slug': self.product.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should be ordered by sort_order (1, 2)
        self.assertEqual(response.data['options'][0]['sort_order'], 1)
        self.assertEqual(response.data['options'][1]['sort_order'], 2)


class ValidateCustomizationsAPITest(APITestCase):
    """Test /api/catalog/products/{slug}/validate_customizations/ endpoint"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()

        # Create site settings (required for middleware)
        from core.models import SiteSettings
        from django.contrib.sites.models import Site

        # Ensure Site exists
        if not Site.objects.filter(pk=1).exists():
            Site.objects.create(pk=1, domain='testserver', name='Test Site')

        # Use get_or_create to avoid conflicts between test methods
        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'admin_email': 'admin@example.com',
                'default_currency': 'USD',
                'enable_multi_warehouse': False
            }
        )

        # Create category
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

        # Create product with customization
        self.product = Product.objects.create(
            name='Custom Cutting Board',
            slug='custom-cutting-board',
            sku='CB-001',
            price=Money(79.99, 'USD'),
            allow_customization=True,
            category=self.category,
            status='published'
        )

        # Text option (not required, per_unit pricing)
        self.text_option = CustomizationOption.objects.create(
            product=self.product,
            name='Engraving Text',
            slug='engraving-text',
            option_type='text',
            is_required=False,
            pricing_type='per_unit',
            price_amount=Money('0.50', 'USD'),
            max_length=50,
            sort_order=1
        )

        # Select option (required, has choice price modifiers)
        self.wood_option = CustomizationOption.objects.create(
            product=self.product,
            name='Wood Type',
            slug='wood-type',
            option_type='select',
            is_required=True,
            pricing_type='fixed',
            price_amount=Money('0.00', 'USD'),
            choices=[
                {'value': 'oak', 'label': 'Oak Wood', 'price_modifier': 0},
                {'value': 'walnut', 'label': 'Walnut Wood', 'price_modifier': 25.00},
                {'value': 'mahogany', 'label': 'Mahogany Wood', 'price_modifier': 50.00}
            ],
            sort_order=2
        )

        # Create non-customizable product
        self.standard_product = Product.objects.create(
            name='Standard Cutting Board',
            slug='standard-cutting-board',
            sku='CB-002',
            price=Money(50, 'USD'),
            allow_customization=False,
            category=self.category,
            status='published'
        )

    def test_validate_customizations_success(self):
        """Test successful validation with all required options"""
        url = reverse('catalog_api:product-validate-customizations', kwargs={'slug': self.product.slug})
        data = {
            'customizations': {
                str(self.text_option.id): 'John Smith',
                str(self.wood_option.id): 'walnut'
            }
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['valid'], True)
        self.assertIn('validated_customizations', response.data)
        self.assertIn('total_customization_price', response.data)
        self.assertIn('total_product_price', response.data)

        # Check text option validation
        text_val = response.data['validated_customizations'][str(self.text_option.id)]
        self.assertEqual(text_val['value'], 'John Smith')
        # "John Smith" = 10 characters, 10 * 0.50 = 5.00
        self.assertEqual(Decimal(text_val['calculated_price']), Decimal('5.00'))

        # Check wood option validation
        wood_val = response.data['validated_customizations'][str(self.wood_option.id)]
        self.assertEqual(wood_val['value'], 'walnut')
        # Walnut has price_modifier of 25.00
        self.assertEqual(Decimal(wood_val['calculated_price']), Decimal('25.00'))

        # Check total prices
        # Total customization: 5.00 (text) + 25.00 (walnut) = 30.00
        self.assertEqual(Decimal(response.data['total_customization_price']['amount']), Decimal('30.00'))
        # Total product: 79.99 (base) + 30.00 (customization) = 109.99
        self.assertEqual(Decimal(response.data['total_product_price']['amount']), Decimal('109.99'))

    def test_validate_customizations_optional_only(self):
        """Test validation with only required option (optional skipped)"""
        url = reverse('catalog_api:product-validate-customizations', kwargs={'slug': self.product.slug})
        data = {
            'customizations': {
                str(self.wood_option.id): 'oak'
            }
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['valid'], True)

        # Only wood option should be in validated_customizations
        self.assertEqual(len(response.data['validated_customizations']), 1)
        self.assertIn(str(self.wood_option.id), response.data['validated_customizations'])

        # Oak has price_modifier of 0
        self.assertEqual(Decimal(response.data['total_customization_price']['amount']), Decimal('0.00'))
        self.assertEqual(Decimal(response.data['total_product_price']['amount']), Decimal('79.99'))

    def test_validate_customizations_missing_required(self):
        """Test validation fails when required option is missing"""
        url = reverse('catalog_api:product-validate-customizations', kwargs={'slug': self.product.slug})
        data = {
            'customizations': {
                str(self.text_option.id): 'John'
            }
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['valid'], False)
        self.assertIn('errors', response.data)
        # Check error message mentions the required option
        self.assertIn('Wood Type', response.data['errors'][0])

    def test_validate_customizations_text_too_long(self):
        """Test validation fails when text exceeds max_length"""
        url = reverse('catalog_api:product-validate-customizations', kwargs={'slug': self.product.slug})
        # max_length is 50, this is 51 characters
        long_text = 'A' * 51
        data = {
            'customizations': {
                str(self.text_option.id): long_text,
                str(self.wood_option.id): 'oak'
            }
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['valid'], False)
        self.assertIn('errors', response.data)
        self.assertIn('maximum length', response.data['errors'][0])

    def test_validate_customizations_invalid_choice(self):
        """Test validation fails with invalid choice value"""
        url = reverse('catalog_api:product-validate-customizations', kwargs={'slug': self.product.slug})
        data = {
            'customizations': {
                str(self.text_option.id): 'John',
                str(self.wood_option.id): 'pine'  # Invalid choice
            }
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['valid'], False)
        self.assertIn('errors', response.data)
        # Check error message mentions invalid selection
        self.assertIn('Invalid', response.data['errors'][0])

    def test_validate_customizations_empty(self):
        """Test validation with empty customizations fails (missing required)"""
        url = reverse('catalog_api:product-validate-customizations', kwargs={'slug': self.product.slug})
        data = {
            'customizations': {}
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['valid'], False)

    def test_validate_customizations_non_customizable_product(self):
        """Test validation fails for non-customizable product"""
        url = reverse('catalog_api:product-validate-customizations', kwargs={'slug': self.standard_product.slug})
        data = {
            'customizations': {}
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['valid'], False)
        self.assertIn('does not support customization', response.data['errors'][0])

    def test_validate_customizations_product_not_found(self):
        """Test validation fails for non-existent product"""
        url = reverse('catalog_api:product-validate-customizations', kwargs={'slug': 'nonexistent'})
        data = {
            'customizations': {}
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_validate_customizations_complex_pricing(self):
        """Test validation with multiple pricing types"""
        url = reverse('catalog_api:product-validate-customizations', kwargs={'slug': self.product.slug})
        data = {
            'customizations': {
                str(self.text_option.id): 'Smith Family',  # 12 chars * 0.50 = 6.00
                str(self.wood_option.id): 'mahogany'  # price_modifier = 50.00
            }
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['valid'], True)

        # Text: "Smith Family" = 12 chars * 0.50 = 6.00
        text_val = response.data['validated_customizations'][str(self.text_option.id)]
        self.assertEqual(Decimal(text_val['calculated_price']), Decimal('6.00'))

        # Mahogany price_modifier should be 50.00
        wood_val = response.data['validated_customizations'][str(self.wood_option.id)]
        self.assertEqual(Decimal(wood_val['calculated_price']), Decimal('50.00'))

        # Total customization: 6.00 (text) + 50.00 (mahogany) = 56.00
        self.assertEqual(Decimal(response.data['total_customization_price']['amount']), Decimal('56.00'))

        # Total product: 79.99 (base) + 56.00 (customization) = 135.99
        self.assertEqual(Decimal(response.data['total_product_price']['amount']), Decimal('135.99'))
