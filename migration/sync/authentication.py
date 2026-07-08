"""
SyncToken Authentication Backend

Authenticates Spwig-to-Spwig sync API requests using SyncTokens.
Requests must include: Authorization: SyncToken <token>
HTTPS is required for security.
"""
import logging
from django.utils.translation import gettext_lazy as _
from core.utils.api_tokens import validate_api_token
from core.models import APIToken

logger = logging.getLogger(__name__)


class SyncTokenAuthError(Exception):
    """Raised when sync token authentication fails."""
    pass


def authenticate_sync_request(request):
    """
    Authenticate a sync API request using the SyncToken header.

    Args:
        request: Django HTTP request

    Returns:
        APIToken: The validated token object

    Raises:
        SyncTokenAuthError: If authentication fails
    """
    # Enforce HTTPS in production
    if not request.is_secure() and not _is_development(request):
        raise SyncTokenAuthError(_("HTTPS is required for sync API requests."))

    # Extract token from Authorization header
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if not auth_header.startswith('SyncToken '):
        raise SyncTokenAuthError(_("Missing or invalid Authorization header. Expected: SyncToken <token>"))

    token_string = auth_header[len('SyncToken '):]
    if not token_string:
        raise SyncTokenAuthError(_("Empty sync token."))

    # Validate against APIToken model
    ip_address = _get_client_ip(request)
    api_token = validate_api_token(
        token_string,
        token_type=APIToken.TOKEN_TYPE_SYNC,
        record_usage=True,
        ip_address=ip_address
    )

    if api_token is None:
        logger.warning(f"Sync auth failed from IP {ip_address}")
        raise SyncTokenAuthError(_("Invalid or expired sync token."))

    return api_token


def _get_client_ip(request):
    """Extract client IP from request, accounting for proxies."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def _is_development(request):
    """Check if running in development mode."""
    from django.conf import settings
    return getattr(settings, 'DEBUG', False)
