"""
Tests for provider SDK foundation.

Tests cover:
- ProviderBase interface
- Mock provider implementation
- Provider registry
- Provider loader
"""
from django.test import TestCase
from decimal import Decimal
from datetime import datetime
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from shipping.providers.base import ProviderBase
from shipping.providers.registry import ProviderRegistry
from shipping.providers.loader import (
    load_provider_manifest,
    validate_provider_package,
    check_platform_compatibility,
    get_provider_metadata
)
from shipping.tests.mock_provider import MockProvider


class ProviderBaseTest(TestCase):
    """Test ProviderBase abstract class."""

    def test_cannot_instantiate_base_class(self):
        """Test that ProviderBase cannot be instantiated directly."""
        with self.assertRaises(TypeError):
            # Should fail because it's abstract
            ProviderBase(credentials={'api_key': 'test'})

    def test_mock_provider_implements_interface(self):
        """Test that MockProvider implements all required methods."""
        provider = MockProvider(credentials={
            'api_key': 'test_key_12345',
            'api_secret': 'test_secret_12345'
        })

        # Check class attributes
        self.assertEqual(provider.provider_key, 'mock_provider')
        self.assertEqual(provider.provider_name, 'Mock Shipping Provider')

        # Check all abstract methods are implemented
        self.assertIsNotNone(provider.capabilities)
        self.assertIsNotNone(provider.credential_schema)
        self.assertIsInstance(provider.capabilities, dict)
        self.assertIsInstance(provider.credential_schema, dict)

    def test_provider_requires_key_and_name(self):
        """Test that provider must set provider_key and provider_name."""
        class InvalidProvider(ProviderBase):
            # Missing provider_key and provider_name
            @property
            def capabilities(self):
                return {}

            @property
            def credential_schema(self):
                return {}

            def validate_credentials(self, credentials):
                pass

            def redact_credentials(self, credentials):
                return {}

            def test_connection(self):
                return {}

            def get_rates(self, origin, destination, parcels, options=None):
                return []

            def buy_label(self, shipment_id, rate, options=None):
                return {}

            def cancel_label(self, tracking_number, reason=None):
                return {}

            def get_tracking(self, tracking_number):
                return {}

            def verify_webhook_signature(self, payload, signature, **kwargs):
                return False

            def handle_webhook(self, event_type, payload):
                return {}

        with self.assertRaises(ValueError) as cm:
            InvalidProvider(credentials={'api_key': 'test'})

        self.assertIn('provider_key', str(cm.exception))


class MockProviderTest(TestCase):
    """Test MockProvider implementation."""

    def setUp(self):
        """Set up test provider."""
        self.provider = MockProvider(credentials={
            'api_key': 'test_key_12345',
            'api_secret': 'test_secret_12345',
            'environment': 'sandbox'
        })

    def test_capabilities(self):
        """Test provider capabilities."""
        caps = self.provider.capabilities

        self.assertTrue(caps['rates'])
        self.assertTrue(caps['labels'])
        self.assertTrue(caps['tracking'])
        self.assertTrue(caps['international'])

    def test_supports_capability(self):
        """Test supports_capability helper method."""
        self.assertTrue(self.provider.supports_capability('rates'))
        self.assertTrue(self.provider.supports_capability('labels'))
        self.assertFalse(self.provider.supports_capability('nonexistent'))

    def test_credential_validation(self):
        """Test credential validation."""
        # Valid credentials
        valid_creds = {
            'api_key': 'test_key_12345',
            'api_secret': 'test_secret_12345'
        }
        self.provider.validate_credentials(valid_creds)  # Should not raise

        # Missing api_key
        with self.assertRaises(ValueError) as cm:
            self.provider.validate_credentials({'api_secret': 'test'})
        self.assertIn('api_key', str(cm.exception))

        # Api_key too short
        with self.assertRaises(ValueError) as cm:
            self.provider.validate_credentials({
                'api_key': 'short',
                'api_secret': 'test_secret_12345'
            })
        self.assertIn('10 characters', str(cm.exception))

    def test_credential_redaction(self):
        """Test sensitive credential redaction."""
        creds = {
            'api_key': 'sk_live_1234567890',
            'api_secret': 'secret_abcdefghijk'
        }

        redacted = self.provider.redact_credentials(creds)

        self.assertEqual(redacted['api_key'], '***7890')
        self.assertEqual(redacted['api_secret'], '***hijk')

    def test_connection_test(self):
        """Test connection testing."""
        result = self.provider.test_connection()

        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'Mock connection successful')
        self.assertIn('account_name', result['details'])
        self.assertEqual(result['details']['environment'], 'sandbox')

    def test_get_rates(self):
        """Test rate calculation."""
        origin = {'country': 'US', 'postal_code': '10001'}
        destination = {'country': 'US', 'postal_code': '90001'}
        parcels = [{'weight': 500, 'length': 10, 'width': 10, 'height': 5}]

        rates = self.provider.get_rates(origin, destination, parcels)

        self.assertIsInstance(rates, list)
        self.assertGreater(len(rates), 0)

        # Check first rate structure
        rate = rates[0]
        self.assertIn('service_code', rate)
        self.assertIn('service_name', rate)
        self.assertIn('rate', rate)
        self.assertIn('currency', rate)
        self.assertIn('delivery_days', rate)
        self.assertIsInstance(rate['rate'], Decimal)

    def test_international_rates_higher(self):
        """Test that international shipping costs more."""
        origin = {'country': 'US', 'postal_code': '10001'}
        parcels = [{'weight': 500}]

        # Domestic
        domestic_dest = {'country': 'US', 'postal_code': '90001'}
        domestic_rates = self.provider.get_rates(origin, domestic_dest, parcels)

        # International
        intl_dest = {'country': 'CA', 'postal_code': 'M5H 2N2'}
        intl_rates = self.provider.get_rates(origin, intl_dest, parcels)

        # International should cost more
        self.assertGreater(intl_rates[0]['rate'], domestic_rates[0]['rate'])

    def test_buy_label(self):
        """Test label purchase."""
        rate = {
            'service_code': 'mock_express',
            'service_name': 'Mock Express',
            'carrier': 'Mock Carrier',
            'rate': Decimal('12.50'),
            'currency': 'USD'
        }

        result = self.provider.buy_label('test_shipment_123', rate)

        self.assertIn('tracking_number', result)
        self.assertIn('label_url', result)
        self.assertIn('cost', result)
        self.assertEqual(result['cost'], Decimal('12.50'))
        self.assertEqual(result['currency'], 'USD')
        self.assertTrue(result['tracking_number'].startswith('MOCK'))

    def test_cancel_label(self):
        """Test label cancellation."""
        result = self.provider.cancel_label('MOCK12345')

        self.assertTrue(result['success'])
        self.assertTrue(result['refunded'])
        self.assertIsInstance(result['refund_amount'], Decimal)

    def test_get_tracking(self):
        """Test tracking retrieval."""
        result = self.provider.get_tracking('MOCK12345')

        self.assertEqual(result['tracking_number'], 'MOCK12345')
        self.assertEqual(result['status'], 'in_transit')
        self.assertIn('events', result)
        self.assertIsInstance(result['events'], list)
        self.assertGreater(len(result['events']), 0)

        # Check event structure
        event = result['events'][0]
        self.assertIn('timestamp', event)
        self.assertIn('status', event)
        self.assertIn('location', event)
        self.assertIn('description', event)

    def test_webhook_signature_verification(self):
        """Test webhook signature verification."""
        payload = b'{"event": "tracking.updated", "tracking_number": "MOCK12345"}'

        # Calculate correct signature
        import hmac
        import hashlib
        secret = self.provider.credentials['api_secret'].encode('utf-8')
        correct_sig = hmac.new(secret, payload, hashlib.sha256).hexdigest()

        # Test with correct signature
        self.assertTrue(
            self.provider.verify_webhook_signature(payload, correct_sig)
        )

        # Test with incorrect signature
        self.assertFalse(
            self.provider.verify_webhook_signature(payload, 'wrong_signature')
        )

    def test_handle_webhook(self):
        """Test webhook event handling."""
        # Tracking update event
        result = self.provider.handle_webhook('tracking.updated', {
            'tracking_number': 'MOCK12345',
            'status': 'delivered',
            'location': 'Chicago, IL',
            'description': 'Package delivered'
        })

        self.assertEqual(result['action'], 'update_tracking')
        self.assertEqual(result['tracking_number'], 'MOCK12345')
        self.assertEqual(result['status'], 'delivered')
        self.assertIn('event', result)


class ProviderRegistryTest(TestCase):
    """Test ProviderRegistry."""

    def setUp(self):
        """Clear registry before each test."""
        ProviderRegistry._providers.clear()
        ProviderRegistry._discovered = False

    def tearDown(self):
        """Clean up after each test."""
        ProviderRegistry._providers.clear()
        ProviderRegistry._discovered = False

    def test_manual_registration(self):
        """Test manually registering a provider."""
        ProviderRegistry.register_provider(MockProvider)

        self.assertTrue(ProviderRegistry.is_registered('mock_provider'))

        provider_class = ProviderRegistry.get_provider('mock_provider')
        self.assertEqual(provider_class, MockProvider)

    def test_list_providers(self):
        """Test listing all providers."""
        ProviderRegistry.register_provider(MockProvider)

        providers = ProviderRegistry.list_providers()

        self.assertIn('mock_provider', providers)
        self.assertEqual(providers['mock_provider'], MockProvider)

    def test_get_provider_info(self):
        """Test getting provider information."""
        ProviderRegistry.register_provider(MockProvider)

        info = ProviderRegistry.get_provider_info('mock_provider')

        self.assertEqual(info['provider_key'], 'mock_provider')
        self.assertEqual(info['provider_name'], 'Mock Shipping Provider')
        self.assertEqual(info['class_name'], 'MockProvider')

    def test_unregister_provider(self):
        """Test unregistering a provider."""
        ProviderRegistry.register_provider(MockProvider)
        self.assertTrue(ProviderRegistry.is_registered('mock_provider'))

        result = ProviderRegistry.unregister_provider('mock_provider')
        self.assertTrue(result)
        self.assertFalse(ProviderRegistry.is_registered('mock_provider'))

        # Unregistering again should return False
        result = ProviderRegistry.unregister_provider('mock_provider')
        self.assertFalse(result)

    def test_reload_providers(self):
        """Test reloading providers."""
        ProviderRegistry.register_provider(MockProvider)
        ProviderRegistry._discovered = True

        ProviderRegistry.reload_providers()

        # Should clear cache
        self.assertFalse(ProviderRegistry.is_registered('mock_provider'))


class ProviderLoaderTest(TestCase):
    """Test provider loader utilities."""

    def test_validate_manifest_structure(self):
        """Test manifest validation."""
        # Valid manifest
        valid_manifest = {
            'name': 'Test Provider',
            'version': '1.0.0',
            'type': 'shipping_provider',
            'provider_key': 'test',
            'entry_point': 'provider.py',
            'class_name': 'TestProvider'
        }

        # Create temp directory with manifest
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            # Write manifest
            manifest_path = tmpdir_path / 'manifest.json'
            manifest_path.write_text(json.dumps(valid_manifest))

            # Write entry point
            entry_path = tmpdir_path / 'provider.py'
            entry_path.write_text('# Provider code')

            # Should not raise
            validate_provider_package(valid_manifest, tmpdir_path)

    def test_missing_manifest_fields(self):
        """Test validation with missing required fields."""
        invalid_manifest = {
            'name': 'Test Provider',
            'version': '1.0.0'
            # Missing required fields
        }

        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaises(ValueError) as cm:
                validate_provider_package(invalid_manifest, Path(tmpdir))

            self.assertIn('Missing required manifest fields', str(cm.exception))

    def test_platform_compatibility_check(self):
        """Test platform version compatibility."""
        # Compatible
        manifest = {
            'name': 'Test Provider',
            'min_platform_version': '1.0.0'
        }
        self.assertTrue(check_platform_compatibility(manifest, '1.5.0'))
        self.assertTrue(check_platform_compatibility(manifest, '2.0.0'))

        # Incompatible
        self.assertFalse(check_platform_compatibility(manifest, '0.9.0'))

        # No requirement
        self.assertTrue(check_platform_compatibility({}, '1.0.0'))
