"""
Unit tests for FedEx OAuth 2.0 authentication module.
"""
import hashlib
from unittest.mock import Mock, patch, MagicMock
from django.test import TestCase
from django.core.cache import cache

from shipping.providers.fedex.auth import FedExOAuthClient, create_oauth_client


class FedExOAuthClientTestCase(TestCase):
    """Test cases for FedExOAuthClient."""

    def setUp(self):
        """Set up test fixtures."""
        self.api_key = 'test_api_key_12345'
        self.api_secret = 'test_api_secret_67890'
        self.environment = 'sandbox'

        self.client = FedExOAuthClient(
            api_key=self.api_key,
            api_secret=self.api_secret,
            environment=self.environment
        )

        # Clear cache before each test
        cache.clear()

    def tearDown(self):
        """Clean up after tests."""
        cache.clear()

    def test_init_sandbox(self):
        """Test initialization with sandbox environment."""
        client = FedExOAuthClient(self.api_key, self.api_secret, 'sandbox')
        self.assertEqual(client.api_key, self.api_key)
        self.assertEqual(client.api_secret, self.api_secret)
        self.assertEqual(client.environment, 'sandbox')
        self.assertEqual(client.token_url, FedExOAuthClient.SANDBOX_TOKEN_URL)

    def test_init_production(self):
        """Test initialization with production environment."""
        client = FedExOAuthClient(self.api_key, self.api_secret, 'production')
        self.assertEqual(client.environment, 'production')
        self.assertEqual(client.token_url, FedExOAuthClient.PRODUCTION_TOKEN_URL)

    def test_get_cache_key(self):
        """Test cache key generation."""
        cache_key = self.client.get_cache_key()

        # Verify key format
        self.assertIn('fedex_oauth_token', cache_key)
        self.assertIn('sandbox', cache_key)

        # Verify consistent key generation
        cache_key2 = self.client.get_cache_key()
        self.assertEqual(cache_key, cache_key2)

        # Verify different clients have different keys
        client2 = FedExOAuthClient('different_key', self.api_secret, self.environment)
        cache_key3 = client2.get_cache_key()
        self.assertNotEqual(cache_key, cache_key3)

    @patch('shipping.providers.fedex.auth.requests.post')
    def test_acquire_token_success(self, mock_post):
        """Test successful token acquisition."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'test_access_token_xyz',
            'token_type': 'Bearer',
            'expires_in': 3600
        }
        mock_post.return_value = mock_response

        # Acquire token
        token = self.client._acquire_token()

        # Verify token
        self.assertEqual(token, 'test_access_token_xyz')

        # Verify request was made correctly
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args[1]
        self.assertEqual(call_kwargs['data']['grant_type'], 'client_credentials')
        self.assertEqual(call_kwargs['data']['client_id'], self.api_key)
        self.assertEqual(call_kwargs['data']['client_secret'], self.api_secret)

    @patch('shipping.providers.fedex.auth.requests.post')
    def test_acquire_token_invalid_credentials(self, mock_post):
        """Test token acquisition with invalid credentials."""
        # Mock 401 response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            'errors': [{'code': 'UNAUTHORIZED', 'message': 'Invalid credentials'}]
        }
        mock_post.return_value = mock_response

        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.client._acquire_token()

        self.assertIn('Invalid FedEx API credentials', str(context.exception))

    @patch('shipping.providers.fedex.auth.requests.post')
    def test_acquire_token_forbidden(self, mock_post):
        """Test token acquisition with forbidden access."""
        # Mock 403 response
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            'errors': [{'code': 'FORBIDDEN', 'message': 'Access denied'}]
        }
        mock_post.return_value = mock_response

        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.client._acquire_token()

        self.assertIn('forbidden', str(context.exception).lower())

    @patch('shipping.providers.fedex.auth.requests.post')
    def test_acquire_token_timeout(self, mock_post):
        """Test token acquisition with timeout."""
        import requests
        mock_post.side_effect = requests.exceptions.Timeout()

        # Should raise ConnectionError
        with self.assertRaises(ConnectionError) as context:
            self.client._acquire_token()

        self.assertIn('timeout', str(context.exception).lower())

    @patch('shipping.providers.fedex.auth.requests.post')
    def test_acquire_token_connection_error(self, mock_post):
        """Test token acquisition with connection error."""
        import requests
        mock_post.side_effect = requests.exceptions.ConnectionError()

        # Should raise ConnectionError
        with self.assertRaises(ConnectionError) as context:
            self.client._acquire_token()

        self.assertIn('connect', str(context.exception).lower())

    @patch('shipping.providers.fedex.auth.requests.post')
    def test_get_token_uses_cache(self, mock_post):
        """Test that get_token uses cached tokens."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'test_token_1',
            'token_type': 'Bearer',
            'expires_in': 3600
        }
        mock_post.return_value = mock_response

        # First call should acquire token
        token1 = self.client.get_token()
        self.assertEqual(token1, 'test_token_1')
        self.assertEqual(mock_post.call_count, 1)

        # Second call should use cache (no new request)
        token2 = self.client.get_token()
        self.assertEqual(token2, 'test_token_1')
        self.assertEqual(mock_post.call_count, 1)  # Still 1

    @patch('shipping.providers.fedex.auth.requests.post')
    def test_get_token_cache_expiration(self, mock_post):
        """Test that get_token acquires new token after cache expiration."""
        # Mock successful responses
        mock_response1 = Mock()
        mock_response1.status_code = 200
        mock_response1.json.return_value = {
            'access_token': 'token_1',
            'token_type': 'Bearer',
            'expires_in': 3600
        }

        mock_response2 = Mock()
        mock_response2.status_code = 200
        mock_response2.json.return_value = {
            'access_token': 'token_2',
            'token_type': 'Bearer',
            'expires_in': 3600
        }

        mock_post.side_effect = [mock_response1, mock_response2]

        # First call
        token1 = self.client.get_token()
        self.assertEqual(token1, 'token_1')

        # Invalidate cache (simulate expiration)
        self.client.invalidate_token()

        # Second call should acquire new token
        token2 = self.client.get_token()
        self.assertEqual(token2, 'token_2')
        self.assertEqual(mock_post.call_count, 2)

    @patch('shipping.providers.fedex.auth.requests.post')
    def test_get_auth_headers(self, mock_post):
        """Test get_auth_headers returns correct headers."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'test_token_abc',
            'token_type': 'Bearer',
            'expires_in': 3600
        }
        mock_post.return_value = mock_response

        # Get headers
        headers = self.client.get_auth_headers()

        # Verify headers
        self.assertEqual(headers['Authorization'], 'Bearer test_token_abc')
        self.assertEqual(headers['Content-Type'], 'application/json')
        self.assertEqual(headers['X-locale'], 'en_US')

    def test_invalidate_token(self):
        """Test token invalidation."""
        # Manually set cache
        cache_key = self.client.get_cache_key()
        cache.set(cache_key, 'test_token', 3600)

        # Verify cache has token
        self.assertEqual(cache.get(cache_key), 'test_token')

        # Invalidate
        self.client.invalidate_token()

        # Verify cache is empty
        self.assertIsNone(cache.get(cache_key))

    def test_parse_error_response_with_errors_array(self):
        """Test parsing FedEx error response format."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'errors': [
                {
                    'code': 'ACCOUNT.NUMBER.MISMATCH',
                    'message': 'Account number does not match'
                }
            ]
        }

        error_msg = self.client._parse_error_response(mock_response)
        self.assertIn('ACCOUNT.NUMBER.MISMATCH', error_msg)
        self.assertIn('Account number does not match', error_msg)

    def test_parse_error_response_fallback(self):
        """Test parsing error response without standard format."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.side_effect = Exception("Invalid JSON")

        error_msg = self.client._parse_error_response(mock_response)
        self.assertEqual(error_msg, 'HTTP 500')


class CreateOAuthClientTestCase(TestCase):
    """Test cases for create_oauth_client factory function."""

    def test_create_oauth_client_success(self):
        """Test successful OAuth client creation."""
        credentials = {
            'api_key': 'test_key',
            'api_secret': 'test_secret',
            'environment': 'production'
        }

        client = create_oauth_client(credentials)

        self.assertIsInstance(client, FedExOAuthClient)
        self.assertEqual(client.api_key, 'test_key')
        self.assertEqual(client.api_secret, 'test_secret')
        self.assertEqual(client.environment, 'production')

    def test_create_oauth_client_default_environment(self):
        """Test client creation with default environment."""
        credentials = {
            'api_key': 'test_key',
            'api_secret': 'test_secret'
        }

        client = create_oauth_client(credentials)
        self.assertEqual(client.environment, 'sandbox')

    def test_create_oauth_client_missing_api_key(self):
        """Test client creation with missing API key."""
        credentials = {
            'api_secret': 'test_secret'
        }

        with self.assertRaises(ValueError) as context:
            create_oauth_client(credentials)

        self.assertIn('api_key', str(context.exception))

    def test_create_oauth_client_missing_api_secret(self):
        """Test client creation with missing API secret."""
        credentials = {
            'api_key': 'test_key'
        }

        with self.assertRaises(ValueError) as context:
            create_oauth_client(credentials)

        self.assertIn('api_secret', str(context.exception))

    def test_create_oauth_client_missing_both(self):
        """Test client creation with missing both credentials."""
        credentials = {}

        with self.assertRaises(ValueError) as context:
            create_oauth_client(credentials)

        error_msg = str(context.exception)
        self.assertIn('api_key', error_msg)
        self.assertIn('api_secret', error_msg)
