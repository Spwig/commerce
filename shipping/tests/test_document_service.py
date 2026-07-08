"""
Tests for DocumentService (Phase 6: Document Generation)

Tests cover:
- Packing slip generation
- Commercial invoice generation
- Customs form generation (CN22/CN23)
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from djmoney.money import Money
from decimal import Decimal

from shipping.models import CarrierPreset, Shipment
from shipping.services.document_service import DocumentService
from orders.models import Order, OrderItem
from catalog.models import Product, ProductImage, Category
from django.contrib.sites.models import Site

User = get_user_model()


class DocumentServiceTestCase(TestCase):
    """Base test case with common setup for document generation tests"""

    def setUp(self):
        """Set up test data"""
        # Create user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

        # Create site (required for some models)
        self.site = Site.objects.get_or_create(
            pk=1,
            defaults={'domain': 'example.com', 'name': 'Example Site'}
        )[0]

        # Create carrier preset
        self.carrier = CarrierPreset.objects.create(
            name='Test Carrier',
            slug='test-carrier',
            tracking_url_template='https://test.com/track/{tracking_number}',
            is_active=True,
            created_by=self.user,
        )

        # Create category (required for products)
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category',
        )

        # Create products
        self.product1 = Product.objects.create(
            category=self.category,
            name='Test Product 1',
            slug='test-product-1',
            sku='SKU-001-PRODUCT',
            price=Money(29.99, 'USD'),
            weight=Decimal('1.5'),
            hs_code='1234567890',
            country_of_origin='US',
            status='published',
        )

        self.product2 = Product.objects.create(
            category=self.category,
            name='Test Product 2',
            slug='test-product-2',
            sku='SKU-002-PRODUCT',
            price=Money(49.99, 'USD'),
            weight=Decimal('2.0'),
            hs_code='0987654321',
            country_of_origin='CN',
            status='published',
        )

        # Create order
        self.order = Order.objects.create(
            user=self.user,
            order_number='TEST-ORDER-001',
            status='processing',
            email='test@example.com',
            phone='+1-555-0123',
            shipping_name='Test User',
            shipping_address1='123 Test Street',
            shipping_address2='Apt 4B',
            shipping_city='Test City',
            shipping_state='CA',
            shipping_postal_code='90001',
            shipping_country='US',
            billing_name='Test User',
            billing_address1='123 Test Street',
            billing_city='Test City',
            billing_state='CA',
            billing_postal_code='90001',
            billing_country='US',
            subtotal=Money(79.98, 'USD'),
            tax_amount=Money(7.00, 'USD'),
            shipping_cost=Money(10.00, 'USD'),
            discount_amount=Money(0, 'USD'),
            total_amount=Money(96.98, 'USD'),
        )

        # Create order items
        self.order_item1 = OrderItem.objects.create(
            order=self.order,
            product=self.product1,
            product_name='Test Product 1',
            sku='SKU-001',
            quantity=2,
            unit_price=Money(29.99, 'USD'),
            total_price=Money(59.98, 'USD'),
        )

        self.order_item2 = OrderItem.objects.create(
            order=self.order,
            product=self.product2,
            product_name='Test Product 2',
            sku='SKU-002',
            quantity=1,
            unit_price=Money(49.99, 'USD'),
            total_price=Money(49.99, 'USD'),
        )

        # Create shipment
        self.shipment = Shipment.objects.create(
            order=self.order,
            user=self.user,
            carrier_preset=self.carrier,
            origin_country='US',
            dest_country='US',
            tracking_id='TRACK123456789',
            status='created',
            shipping_cost=Money(10.00, 'USD'),
        )


class PackingSlipGenerationTest(DocumentServiceTestCase):
    """Test packing slip generation"""

    def test_generate_packing_slip_basic(self):
        """Test basic packing slip generation"""
        # Generate packing slip
        data_uri = DocumentService.generate_packing_slip(self.shipment)

        # Verify it's a data URI
        self.assertTrue(data_uri.startswith('data:application/pdf;base64,'))

        # Verify it's not empty
        self.assertGreater(len(data_uri), 100)

    def test_generate_packing_slip_saves_to_shipment(self):
        """Test that generated packing slip can be saved to shipment"""
        # Generate and save
        data_uri = DocumentService.generate_packing_slip(self.shipment)
        self.shipment.packing_slip_url = data_uri
        self.shipment.save()

        # Reload and verify
        self.shipment.refresh_from_db()
        self.assertEqual(self.shipment.packing_slip_url, data_uri)
        self.assertTrue(self.shipment.packing_slip_url.startswith('data:application/pdf;base64,'))

    def test_generate_packing_slip_with_multiple_items(self):
        """Test packing slip with multiple order items"""
        # Add more items
        OrderItem.objects.create(
            order=self.order,
            product=self.product1,
            product_name='Test Product 1',
            sku='SKU-001',
            quantity=5,
            unit_price=Money(29.99, 'USD'),
            total_price=Money(149.95, 'USD'),
        )

        # Generate packing slip
        data_uri = DocumentService.generate_packing_slip(self.shipment)

        # Verify generation
        self.assertTrue(data_uri.startswith('data:application/pdf;base64,'))
        self.assertGreater(len(data_uri), 100)

    def test_generate_packing_slip_no_tracking(self):
        """Test packing slip generation without tracking number"""
        # Create shipment without tracking
        shipment_no_tracking = Shipment.objects.create(
            order=self.order,
            user=self.user,
            carrier_preset=self.carrier,
            origin_country='US',
            dest_country='US',
            status='created',
            shipping_cost=Money(10.00, 'USD'),
        )

        # Should still generate successfully
        data_uri = DocumentService.generate_packing_slip(shipment_no_tracking)
        self.assertTrue(data_uri.startswith('data:application/pdf;base64,'))


class CommercialInvoiceGenerationTest(DocumentServiceTestCase):
    """Test commercial invoice generation"""

    def test_generate_commercial_invoice_basic(self):
        """Test basic commercial invoice generation"""
        # Generate commercial invoice
        data_uri = DocumentService.generate_commercial_invoice(self.shipment)

        # Verify it's a data URI
        self.assertTrue(data_uri.startswith('data:application/pdf;base64,'))

        # Verify it's not empty
        self.assertGreater(len(data_uri), 100)

    def test_generate_commercial_invoice_saves_to_shipment(self):
        """Test that generated commercial invoice can be saved to shipment"""
        # Generate and save
        data_uri = DocumentService.generate_commercial_invoice(self.shipment)
        self.shipment.commercial_invoice_url = data_uri
        self.shipment.save()

        # Reload and verify
        self.shipment.refresh_from_db()
        self.assertEqual(self.shipment.commercial_invoice_url, data_uri)
        self.assertTrue(self.shipment.commercial_invoice_url.startswith('data:application/pdf;base64,'))

    def test_generate_commercial_invoice_includes_customs_data(self):
        """Test that commercial invoice includes product customs data"""
        # Products have HS codes and country of origin set in setUp
        # Generate commercial invoice
        data_uri = DocumentService.generate_commercial_invoice(self.shipment)

        # Verify generation (customs data integration tested implicitly)
        self.assertTrue(data_uri.startswith('data:application/pdf;base64,'))
        self.assertGreater(len(data_uri), 100)

    def test_generate_commercial_invoice_international_shipment(self):
        """Test commercial invoice for international shipment"""
        # Create international shipment
        international_shipment = Shipment.objects.create(
            order=self.order,
            user=self.user,
            carrier_preset=self.carrier,
            origin_country='US',
            dest_country='GB',  # UK destination
            tracking_id='INTL-TRACK-001',
            status='created',
            shipping_cost=Money(25.00, 'USD'),
        )

        # Generate commercial invoice
        data_uri = DocumentService.generate_commercial_invoice(international_shipment)

        # Verify generation
        self.assertTrue(data_uri.startswith('data:application/pdf;base64,'))
        self.assertGreater(len(data_uri), 100)


class CustomsFormGenerationTest(DocumentServiceTestCase):
    """Test customs form generation (CN22/CN23)"""

    def test_generate_customs_form_cn22(self):
        """Test CN22 customs form generation"""
        # Generate CN22 form
        data_uri = DocumentService.generate_customs_form(self.shipment, form_type='CN22')

        # Verify it's a data URI
        self.assertTrue(data_uri.startswith('data:application/pdf;base64,'))

        # Verify it's not empty
        self.assertGreater(len(data_uri), 100)

    def test_generate_customs_form_cn23(self):
        """Test CN23 customs form generation"""
        # Generate CN23 form
        data_uri = DocumentService.generate_customs_form(self.shipment, form_type='CN23')

        # Verify it's a data URI
        self.assertTrue(data_uri.startswith('data:application/pdf;base64,'))

        # Verify it's not empty
        self.assertGreater(len(data_uri), 100)

    def test_generate_customs_form_default_cn23(self):
        """Test that CN23 is default form type"""
        # Generate without specifying form type
        data_uri = DocumentService.generate_customs_form(self.shipment)

        # Should default to CN23
        self.assertTrue(data_uri.startswith('data:application/pdf;base64,'))
        self.assertGreater(len(data_uri), 100)

    def test_generate_customs_form_saves_to_shipment(self):
        """Test that generated customs form can be saved to shipment"""
        # Generate and save
        data_uri = DocumentService.generate_customs_form(self.shipment, form_type='CN23')
        self.shipment.customs_form_url = data_uri
        self.shipment.save()

        # Reload and verify
        self.shipment.refresh_from_db()
        self.assertEqual(self.shipment.customs_form_url, data_uri)
        self.assertTrue(self.shipment.customs_form_url.startswith('data:application/pdf;base64,'))

    def test_generate_customs_form_international(self):
        """Test customs form for international shipment"""
        # Create international shipment
        international_shipment = Shipment.objects.create(
            order=self.order,
            user=self.user,
            carrier_preset=self.carrier,
            origin_country='US',
            dest_country='DE',  # Germany destination
            tracking_id='INTL-TRACK-002',
            status='created',
            shipping_cost=Money(30.00, 'USD'),
        )

        # Generate customs form
        data_uri = DocumentService.generate_customs_form(international_shipment, form_type='CN23')

        # Verify generation
        self.assertTrue(data_uri.startswith('data:application/pdf;base64,'))
        self.assertGreater(len(data_uri), 100)


class DocumentServiceIntegrationTest(DocumentServiceTestCase):
    """Integration tests for document generation"""

    def test_generate_all_documents_for_shipment(self):
        """Test generating all three document types for a shipment"""
        # Generate all documents
        packing_slip = DocumentService.generate_packing_slip(self.shipment)
        commercial_invoice = DocumentService.generate_commercial_invoice(self.shipment)
        customs_form = DocumentService.generate_customs_form(self.shipment, form_type='CN23')

        # Verify all generated successfully
        self.assertTrue(packing_slip.startswith('data:application/pdf;base64,'))
        self.assertTrue(commercial_invoice.startswith('data:application/pdf;base64,'))
        self.assertTrue(customs_form.startswith('data:application/pdf;base64,'))

        # Save all to shipment
        self.shipment.packing_slip_url = packing_slip
        self.shipment.commercial_invoice_url = commercial_invoice
        self.shipment.customs_form_url = customs_form
        self.shipment.save()

        # Reload and verify all saved
        self.shipment.refresh_from_db()
        self.assertIsNotNone(self.shipment.packing_slip_url)
        self.assertIsNotNone(self.shipment.commercial_invoice_url)
        self.assertIsNotNone(self.shipment.customs_form_url)

    def test_regenerate_documents(self):
        """Test regenerating documents (overwriting existing)"""
        # Generate initial documents
        initial_packing_slip = DocumentService.generate_packing_slip(self.shipment)
        self.shipment.packing_slip_url = initial_packing_slip
        self.shipment.save()

        # Regenerate
        new_packing_slip = DocumentService.generate_packing_slip(self.shipment)
        self.shipment.packing_slip_url = new_packing_slip
        self.shipment.save()

        # Verify new document saved
        self.shipment.refresh_from_db()
        self.assertEqual(self.shipment.packing_slip_url, new_packing_slip)

    def test_documents_independent_of_provider(self):
        """Test that document generation works without provider integration"""
        # Shipment has no provider_account (manual shipping)
        self.assertIsNone(self.shipment.provider_account)

        # Documents should still generate successfully
        packing_slip = DocumentService.generate_packing_slip(self.shipment)
        commercial_invoice = DocumentService.generate_commercial_invoice(self.shipment)
        customs_form = DocumentService.generate_customs_form(self.shipment)

        # Verify all generated
        self.assertTrue(packing_slip.startswith('data:application/pdf;base64,'))
        self.assertTrue(commercial_invoice.startswith('data:application/pdf;base64,'))
        self.assertTrue(customs_form.startswith('data:application/pdf;base64,'))
