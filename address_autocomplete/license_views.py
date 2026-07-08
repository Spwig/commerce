"""
Views for license-based geocoder token provisioning
"""

import json
import asyncio
import logging
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.conf import settings
from .license_integration import LicenseBasedGeocoderAuth

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class ProvisionGeocoderTokenView(View):
    """
    API endpoint for shops to get their geocoder JWT token.
    Called during shop initialization or when token expires.
    """

    def post(self, request):
        """
        Provision geocoder token based on license.

        Expected POST data:
        {
            "license_key": "XXXX-XXXX-XXXX-XXXX",
            "installation_uuid": "uuid-here"
        }

        Returns:
        {
            "success": true,
            "token": "jwt-token-here",
            "expires_at": "2024-01-01T00:00:00Z",
            "tier": "premium",
            "rate_limit": 500,
            "merchant_id": "merchant_123abc"
        }
        """
        try:
            # Parse request data
            data = json.loads(request.body)
            license_key = data.get('license_key')
            installation_uuid = data.get('installation_uuid')

            if not license_key:
                return JsonResponse({
                    'success': False,
                    'error': 'License key is required'
                }, status=400)

            # Check rate limiting (prevent abuse)
            rate_limit_key = f'provision_rate:{request.META.get("REMOTE_ADDR")}'
            if cache.get(rate_limit_key, 0) > 10:  # Max 10 requests per hour
                return JsonResponse({
                    'success': False,
                    'error': 'Rate limit exceeded'
                }, status=429)

            cache.set(rate_limit_key, cache.get(rate_limit_key, 0) + 1, 3600)

            # Initialize auth manager
            auth_manager = LicenseBasedGeocoderAuth()

            # Run async validation
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                result = loop.run_until_complete(
                    auth_manager.validate_license_and_get_token(
                        license_key,
                        installation_uuid or self._generate_installation_uuid(request)
                    )
                )
            finally:
                loop.close()

            if result['success']:
                # Log successful provisioning
                logger.info(f"Geocoder token provisioned for merchant {result['merchant_id']}")

                return JsonResponse({
                    'success': True,
                    'token': result['token'],
                    'expires_at': result['expires_at'],
                    'tier': result['tier'],
                    'rate_limit': result['rate_limit'],
                    'merchant_id': result['merchant_id'],
                    'license_type': result.get('license_type', 'standard')
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': result.get('error', 'License validation failed')
                }, status=401)

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON in request body'
            }, status=400)
        except Exception as e:
            logger.error(f"Token provisioning error: {e}")
            return JsonResponse({
                'success': False,
                'error': 'Internal server error'
            }, status=500)

    def _generate_installation_uuid(self, request):
        """Generate installation UUID based on request data."""
        import uuid
        import hashlib

        # Create UUID based on IP and user agent
        ip = request.META.get('REMOTE_ADDR', '')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        unique_str = f"{ip}-{user_agent}"

        return str(uuid.uuid5(uuid.NAMESPACE_DNS, unique_str))


class RefreshGeocoderTokenView(View):
    """
    Refresh an existing geocoder JWT token.
    """

    def post(self, request):
        """
        Refresh geocoder token.

        Expected POST data:
        {
            "token": "current-jwt-token"
        }
        """
        try:
            data = json.loads(request.body)
            current_token = data.get('token')

            if not current_token:
                return JsonResponse({
                    'success': False,
                    'error': 'Current token is required'
                }, status=400)

            auth_manager = LicenseBasedGeocoderAuth()
            new_token_info = auth_manager.geocoder_jwt_auth.refresh_token(current_token)

            if new_token_info:
                return JsonResponse({
                    'success': True,
                    'token': new_token_info['token'],
                    'expires_at': new_token_info['expires_at']
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Token refresh failed'
                }, status=401)

        except Exception as e:
            logger.error(f"Token refresh error: {e}")
            return JsonResponse({
                'success': False,
                'error': 'Internal server error'
            }, status=500)


class GeocoderTokenStatusView(View):
    """
    Check status of a geocoder token.
    """

    def get(self, request):
        """
        Check token status.

        Query params:
        ?token=jwt-token-here
        """
        token = request.GET.get('token')

        if not token:
            return JsonResponse({
                'success': False,
                'error': 'Token parameter is required'
            }, status=400)

        auth_manager = LicenseBasedGeocoderAuth()
        is_valid, payload = auth_manager.geocoder_jwt_auth.verify_token(token)

        if is_valid:
            return JsonResponse({
                'success': True,
                'valid': True,
                'merchant_id': payload['sub'],
                'tier': payload.get('tier', 'standard'),
                'expires_at': payload['exp']
            })
        else:
            return JsonResponse({
                'success': True,
                'valid': False,
                'error': payload.get('error', 'Invalid token')
            })