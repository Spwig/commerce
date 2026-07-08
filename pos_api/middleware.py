import json

from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _


class POSLicenseMiddleware:
    """
    Gates /api/pos/ endpoints behind a valid POS license.

    Checks that a valid POS license is configured. If not, returns 403.
    The license check is cached for 24 hours to avoid repeated lookups.

    Also injects X-Spwig-Sandbox header when platform is in sandbox mode,
    so the POS frontend can show a sandbox indicator.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/pos/'):
            from pos_app.license import pos_license_is_valid

            if not pos_license_is_valid():
                return JsonResponse({
                    'success': False,
                    'error': {
                        'code': 'POS_LICENSE_REQUIRED',
                        'message': str(_('A valid POS license is required to access this endpoint.')),
                    }
                }, status=403)

        response = self.get_response(request)

        # Inject sandbox header for POS API and POS frontend requests
        if request.path.startswith(('/api/pos/', '/pos/')):
            from core.license import is_sandbox_mode
            if is_sandbox_mode():
                response['X-Spwig-Sandbox'] = 'true'

        return response
