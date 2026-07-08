"""
Middleware Tests

Tests for referral tracking middleware and request context management.
"""
from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from unittest.mock import Mock, patch, MagicMock
from threading import current_thread

from ..middleware import (
    ReferralTrackingMiddleware,
    RequestContextMiddleware,
    get_current_request,
)
from .factories import (
    create_user,
    create_referral_program,
    create_referral_identity,
)


class ReferralTrackingMiddlewareTest(TestCase):
    """Tests for ReferralTrackingMiddleware."""

    def setUp(self):
        self.program = create_referral_program()
        self.factory = RequestFactory()
        self.middleware = ReferralTrackingMiddleware(get_response=lambda r: HttpResponse())

    @patch('referrals.middleware.track_click')
    def test_process_request_with_ref_token(self, mock_track_click):
        """Test that request with ref token tracks click."""
        # Create identity
        identity = create_referral_identity()

        # Mock track_click success
        mock_track_click.return_value = (True, identity, 'Click tracked')

        # Create request with ref parameter
        request = self.factory.get('/', {'ref': identity.token})

        # Process request
        result = self.middleware.process_request(request)

        # Should return None to continue processing
        self.assertIsNone(result)

        # Should call track_click
        mock_track_click.assert_called_once_with(identity.token, request)

        # Should mark request for cookie setting
        self.assertTrue(hasattr(request, '_ref_token_to_set'))
        self.assertEqual(request._ref_token_to_set, identity.token)

    @patch('referrals.middleware.track_click')
    def test_process_request_without_ref_token(self, mock_track_click):
        """Test that request without ref token does nothing."""
        # Create request without ref parameter
        request = self.factory.get('/')

        # Process request
        result = self.middleware.process_request(request)

        # Should return None
        self.assertIsNone(result)

        # Should not call track_click
        mock_track_click.assert_not_called()

        # Should not mark request
        self.assertFalse(hasattr(request, '_ref_token_to_set'))

    @patch('referrals.middleware.track_click')
    def test_process_request_inactive_program(self, mock_track_click):
        """Test that inactive program doesn't track."""
        # Deactivate program
        self.program.status = 'paused'
        self.program.save()

        # Create identity
        identity = create_referral_identity()

        # Create request with ref parameter
        request = self.factory.get('/', {'ref': identity.token})

        # Process request
        result = self.middleware.process_request(request)

        # Should return None
        self.assertIsNone(result)

        # Should not call track_click
        mock_track_click.assert_not_called()

    @patch('referrals.middleware.track_click')
    def test_process_request_invalid_token(self, mock_track_click):
        """Test that invalid token doesn't set cookie."""
        # Mock track_click failure
        mock_track_click.return_value = (False, None, 'Invalid token')

        # Create request with invalid ref parameter
        request = self.factory.get('/', {'ref': 'invalid_token'})

        # Process request
        result = self.middleware.process_request(request)

        # Should return None
        self.assertIsNone(result)

        # Should call track_click
        mock_track_click.assert_called_once()

        # Should not mark request for cookie setting
        self.assertFalse(hasattr(request, '_ref_token_to_set'))

    @patch('referrals.middleware.set_ref_cookie')
    def test_process_response_sets_cookie(self, mock_set_cookie):
        """Test that response sets cookie when marked."""
        # Create identity
        identity = create_referral_identity()

        # Create request and mark it
        request = self.factory.get('/')
        request._ref_token_to_set = identity.token

        # Create response
        response = HttpResponse()

        # Process response
        result = self.middleware.process_response(request, response)

        # Should return response
        self.assertEqual(result, response)

        # Should call set_ref_cookie
        mock_set_cookie.assert_called_once()
        args = mock_set_cookie.call_args
        self.assertEqual(args[0][0], response)  # response
        self.assertEqual(args[0][1], identity.token)  # token
        self.assertEqual(args[0][2], 30)  # TTL days (default)

    @patch('referrals.middleware.set_ref_cookie')
    def test_process_response_no_cookie_to_set(self, mock_set_cookie):
        """Test that response without marker doesn't set cookie."""
        # Create request without marker
        request = self.factory.get('/')

        # Create response
        response = HttpResponse()

        # Process response
        result = self.middleware.process_response(request, response)

        # Should return response
        self.assertEqual(result, response)

        # Should not call set_ref_cookie
        mock_set_cookie.assert_not_called()

    @patch('referrals.middleware.set_ref_cookie')
    def test_process_response_custom_ttl(self, mock_set_cookie):
        """Test that custom cookie TTL is used."""
        # Set custom TTL in program
        self.program.tracking_config = {'cookie_ttl_days': 60}
        self.program.save()

        # Create identity
        identity = create_referral_identity()

        # Create request and mark it
        request = self.factory.get('/')
        request._ref_token_to_set = identity.token

        # Create response
        response = HttpResponse()

        # Process response
        result = self.middleware.process_response(request, response)

        # Should call set_ref_cookie with custom TTL
        mock_set_cookie.assert_called_once()
        args = mock_set_cookie.call_args
        self.assertEqual(args[0][2], 60)  # Custom TTL


class RequestContextMiddlewareTest(TestCase):
    """Tests for RequestContextMiddleware."""

    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = RequestContextMiddleware(get_response=lambda r: HttpResponse())

    def test_process_request_stores_context(self):
        """Test that request is stored in thread-local storage."""
        # Create request
        request = self.factory.get('/')

        # Process request
        result = self.middleware.process_request(request)

        # Should return None
        self.assertIsNone(result)

        # Should store request in thread-local
        thread = current_thread()
        self.assertTrue(hasattr(thread, 'request'))
        self.assertEqual(thread.request, request)

    def test_process_response_cleans_up(self):
        """Test that response cleans up thread-local storage."""
        # Create and process request
        request = self.factory.get('/')
        self.middleware.process_request(request)

        # Verify request is stored
        thread = current_thread()
        self.assertTrue(hasattr(thread, 'request'))

        # Create and process response
        response = HttpResponse()
        result = self.middleware.process_response(request, response)

        # Should return response
        self.assertEqual(result, response)

        # Should clean up thread-local
        self.assertFalse(hasattr(thread, 'request'))

    def test_process_exception_cleans_up(self):
        """Test that exception handler cleans up thread-local storage."""
        # Create and process request
        request = self.factory.get('/')
        self.middleware.process_request(request)

        # Verify request is stored
        thread = current_thread()
        self.assertTrue(hasattr(thread, 'request'))

        # Process exception
        exception = Exception('Test exception')
        result = self.middleware.process_exception(request, exception)

        # Should return None (allow exception to propagate)
        self.assertIsNone(result)

        # Should clean up thread-local
        self.assertFalse(hasattr(thread, 'request'))

    def test_get_current_request(self):
        """Test get_current_request helper function."""
        # Initially should return None
        self.assertIsNone(get_current_request())

        # Process request
        request = self.factory.get('/')
        self.middleware.process_request(request)

        # Should now return request
        self.assertEqual(get_current_request(), request)

        # Clean up
        response = HttpResponse()
        self.middleware.process_response(request, response)

        # Should return None again
        self.assertIsNone(get_current_request())

    def test_multiple_requests_in_sequence(self):
        """Test that multiple requests are handled correctly."""
        # First request
        request1 = self.factory.get('/page1')
        self.middleware.process_request(request1)
        self.assertEqual(get_current_request(), request1)

        response1 = HttpResponse()
        self.middleware.process_response(request1, response1)
        self.assertIsNone(get_current_request())

        # Second request
        request2 = self.factory.get('/page2')
        self.middleware.process_request(request2)
        self.assertEqual(get_current_request(), request2)

        response2 = HttpResponse()
        self.middleware.process_response(request2, response2)
        self.assertIsNone(get_current_request())


class MiddlewareIntegrationTest(TestCase):
    """Integration tests for middleware stack."""

    def setUp(self):
        self.program = create_referral_program()
        self.factory = RequestFactory()
        self.tracking_middleware = ReferralTrackingMiddleware(
            get_response=lambda r: HttpResponse()
        )
        self.context_middleware = RequestContextMiddleware(
            get_response=lambda r: HttpResponse()
        )

    @patch('referrals.middleware.track_click')
    @patch('referrals.middleware.set_ref_cookie')
    def test_full_referral_tracking_flow(self, mock_set_cookie, mock_track_click):
        """Test complete referral tracking flow through both middlewares."""
        # Create identity
        referrer = create_user(email='referrer@example.com')
        identity = create_referral_identity(customer=referrer)

        # Mock track_click success
        mock_track_click.return_value = (True, identity, 'Click tracked')

        # Create request with ref parameter
        request = self.factory.get('/', {'ref': identity.token})

        # Process through both middlewares
        # 1. Context middleware - process_request
        self.context_middleware.process_request(request)

        # Verify request is in context
        self.assertEqual(get_current_request(), request)

        # 2. Tracking middleware - process_request
        self.tracking_middleware.process_request(request)

        # Verify click was tracked
        mock_track_click.assert_called_once_with(identity.token, request)
        self.assertTrue(hasattr(request, '_ref_token_to_set'))

        # 3. Create response
        response = HttpResponse()

        # 4. Tracking middleware - process_response
        self.tracking_middleware.process_response(request, response)

        # Verify cookie was set
        mock_set_cookie.assert_called_once()

        # 5. Context middleware - process_response
        self.context_middleware.process_response(request, response)

        # Verify context was cleaned up
        self.assertIsNone(get_current_request())
