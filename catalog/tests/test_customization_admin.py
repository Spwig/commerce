"""
Tests for CustomizationOption Django Admin interface.
Verifies admin registration, inline display, and static file references.
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from catalog.models import Product, Category, CustomizationOption
from djmoney.money import Money
from decimal import Decimal


User = get_user_model()


class CustomizationOptionAdminTest(TestCase):
    """Test CustomizationOption admin interface"""

    def setUp(self):
        """Set up test data"""
        # Create superuser for admin access
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )

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

        # Create test category
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

        # Create test product with customization enabled
        self.product = Product.objects.create(
            name='Customizable Product',
            slug='customizable-product',
            sku='CUSTOM-001',
            price=Money(100, 'USD'),
            allow_customization=True,
            category=self.category
        )

        # Create test customization option
        self.option = CustomizationOption.objects.create(
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

        # Create client and log in as admin
        self.client = Client()
        self.client.login(username='admin', password='admin123')

    def test_customization_option_admin_registered(self):
        """Test that CustomizationOption admin is registered"""
        url = reverse('admin:catalog_customizationoption_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_customization_option_list_display(self):
        """Test CustomizationOption list view displays correctly"""
        url = reverse('admin:catalog_customizationoption_changelist')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Engraving Text')
        self.assertContains(response, 'text')
        self.assertContains(response, 'per_unit')

    def test_customization_option_detail_view(self):
        """Test CustomizationOption detail/edit view"""
        url = reverse('admin:catalog_customizationoption_change', args=[self.option.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Engraving Text')
        self.assertContains(response, 'admin_customization.css')
        self.assertContains(response, 'admin_customization.js')

    def test_customization_option_inline_on_product(self):
        """Test CustomizationOption inline appears on Product admin"""
        url = reverse('admin:catalog_product_change', args=[self.product.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # Check for customization option in the response
        # (Product admin uses custom template, so check for the actual option name)
        self.assertContains(response, 'Engraving Text')

    def test_customization_option_inline_hidden_when_disabled(self):
        """Test CustomizationOption inline hidden when allow_customization=False"""
        # Create product without customization
        product_no_custom = Product.objects.create(
            name='Standard Product',
            slug='standard-product',
            sku='STD-001',
            price=Money(50, 'USD'),
            allow_customization=False,
            category=self.category
        )

        url = reverse('admin:catalog_product_change', args=[product_no_custom.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # Inline should not be present
        self.assertNotContains(response, 'customizationoption_set-group')

    def test_customization_option_fieldsets(self):
        """Test CustomizationOption admin fieldsets are configured"""
        url = reverse('admin:catalog_customizationoption_change', args=[self.option.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # Check for fieldset sections
        self.assertContains(response, 'Basic Information')
        self.assertContains(response, 'Option Configuration')
        self.assertContains(response, 'Validation Rules')
        self.assertContains(response, 'Pricing')

    def test_static_files_referenced(self):
        """Test that admin references the correct static files"""
        url = reverse('admin:catalog_customizationoption_change', args=[self.option.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # Check static file references in Media class
        content = response.content.decode('utf-8')
        self.assertIn('catalog/css/admin_customization.css', content)
        self.assertIn('catalog/js/admin_customization.js', content)

    def test_customization_option_choices_display(self):
        """Test choices_display readonly field for select options"""
        # Create select option with choices
        select_option = CustomizationOption.objects.create(
            product=self.product,
            name='Wood Type',
            slug='wood-type',
            option_type='select',
            is_required=True,
            pricing_type='fixed',
            price_amount=Money('0.00', 'USD'),
            choices=[
                {'value': 'oak', 'label': 'Oak Wood', 'price_modifier': 0},
                {'value': 'walnut', 'label': 'Walnut Wood', 'price_modifier': 25.00}
            ],
            sort_order=2
        )

        url = reverse('admin:catalog_customizationoption_change', args=[select_option.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Oak Wood')
        self.assertContains(response, 'Walnut Wood')

    def test_create_new_customization_option(self):
        """Test creating a new customization option via admin"""
        url = reverse('admin:catalog_customizationoption_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Submit new option
        post_data = {
            'product': self.product.pk,
            'name': 'Gift Message',
            'slug': 'gift-message',
            'option_type': 'textarea',
            'is_required': False,
            'pricing_type': 'free',
            'price_amount_0': '0.00',
            'price_amount_1': 'USD',
            'max_length': 200,
            'sort_order': 3,
        }

        response = self.client.post(url, post_data)

        # Should redirect to changelist on success
        self.assertEqual(response.status_code, 302)

        # Verify option was created
        self.assertTrue(
            CustomizationOption.objects.filter(slug='gift-message').exists()
        )

    def test_admin_list_filters(self):
        """Test admin list view has correct filters"""
        url = reverse('admin:catalog_customizationoption_changelist')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # Check filter sidebar exists
        self.assertContains(response, 'option_type')
        self.assertContains(response, 'pricing_type')
        self.assertContains(response, 'is_required')

    def test_admin_search_functionality(self):
        """Test admin search works correctly"""
        url = reverse('admin:catalog_customizationoption_changelist')

        # Search by name
        response = self.client.get(url, {'q': 'Engraving'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Engraving Text')

        # Search by product SKU
        response = self.client.get(url, {'q': 'CUSTOM-001'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Engraving Text')

    def test_admin_ordering(self):
        """Test admin list is ordered correctly"""
        # Create additional options
        CustomizationOption.objects.create(
            product=self.product,
            name='Gift Wrap',
            slug='gift-wrap',
            option_type='select',
            is_required=False,
            pricing_type='fixed',
            price_amount=Money('5.00', 'USD'),
            sort_order=0,  # Lower sort order
            choices=[{'value': 'yes', 'label': 'Yes', 'price_modifier': 0}]
        )

        url = reverse('admin:catalog_customizationoption_changelist')
        response = self.client.get(url)

        content = response.content.decode('utf-8')

        # Gift Wrap (sort_order=0) should appear before Engraving Text (sort_order=1)
        gift_wrap_pos = content.find('Gift Wrap')
        engraving_pos = content.find('Engraving Text')

        self.assertLess(gift_wrap_pos, engraving_pos)


class CustomizationOptionInlineTest(TestCase):
    """Test CustomizationOption inline in Product admin"""

    def setUp(self):
        """Set up test data"""
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )

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

        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

        self.product = Product.objects.create(
            name='Customizable Product',
            slug='customizable-product',
            sku='CUSTOM-001',
            price=Money(100, 'USD'),
            allow_customization=True,
            category=self.category
        )

        self.client = Client()
        self.client.login(username='admin', password='admin123')

    def test_inline_media_files_loaded(self):
        """Test inline loads correct CSS and JS files"""
        url = reverse('admin:catalog_product_change', args=[self.product.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        # Check Media class files are loaded
        self.assertIn('catalog/css/admin_customization.css', content)
        self.assertIn('catalog/js/admin_customization.js', content)

    def test_inline_fields_present(self):
        """Test inline displays correct fields"""
        url = reverse('admin:catalog_product_change', args=[self.product.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        # Check for inline field names
        self.assertContains(response, 'name')
        self.assertContains(response, 'option_type')
        self.assertContains(response, 'is_required')
        self.assertContains(response, 'pricing_type')
        self.assertContains(response, 'price_amount')

    def test_create_option_via_product_inline(self):
        """Test creating customization option via Product admin inline"""
        url = reverse('admin:catalog_product_change', args=[self.product.pk])

        # Submit with new inline option
        post_data = {
            # Product fields
            'name': 'Customizable Product',
            'slug': 'customizable-product',
            'sku': 'CUSTOM-001',
            'price_0': '100.00',
            'price_1': 'USD',
            'allow_customization': 'on',
            'category': self.category.pk,

            # Required Product fields
            'product_type': 'simple',
            'pricing_strategy': 'dynamic',
            'sale_type': 'none',
            'gift_card_expires_days': '365',
            'low_stock_threshold': '5',
            'gallery_type': 'standard',
            'template_variant': 'default',
            'status': 'draft',

            # Customization options inline formset management form
            'customization_options-TOTAL_FORMS': '1',
            'customization_options-INITIAL_FORMS': '0',
            'customization_options-MIN_NUM_FORMS': '0',
            'customization_options-MAX_NUM_FORMS': '1000',

            # New inline option
            'customization_options-0-name': 'Gift Message',
            'customization_options-0-option_type': 'text',
            'customization_options-0-is_required': False,
            'customization_options-0-pricing_type': 'free',
            'customization_options-0-price_amount_0': '0.00',
            'customization_options-0-price_amount_1': 'USD',
            'customization_options-0-sort_order': '1',

            # Other required formsets management forms
            'variants-TOTAL_FORMS': '0',
            'variants-INITIAL_FORMS': '0',
            'variants-MIN_NUM_FORMS': '0',
            'variants-MAX_NUM_FORMS': '1000',

            'currency_prices-TOTAL_FORMS': '0',
            'currency_prices-INITIAL_FORMS': '0',
            'currency_prices-MIN_NUM_FORMS': '0',
            'currency_prices-MAX_NUM_FORMS': '1000',

            'region_visibility-TOTAL_FORMS': '0',
            'region_visibility-INITIAL_FORMS': '0',
            'region_visibility-MIN_NUM_FORMS': '0',
            'region_visibility-MAX_NUM_FORMS': '1000',
        }

        response = self.client.post(url, post_data, follow=True)

        # Check option was created
        self.assertTrue(
            CustomizationOption.objects.filter(
                product=self.product,
                name='Gift Message'
            ).exists()
        )
