"""
Admin API Authentication

Custom authentication backend for mobile app token authentication.
Supports access tokens with expiry and device tracking.
"""

from django.utils.translation import gettext_lazy as _
from rest_framework import authentication, exceptions


class MobileTokenAuthentication(authentication.BaseAuthentication):
    """
    Token-based authentication for the Admin API.

    Uses MobileAuthToken model for access tokens with:
    - Expiry checking
    - Revocation support
    - Device tracking
    - Last-used timestamp updates

    Usage:
        class MyView(APIView):
            authentication_classes = [MobileTokenAuthentication]

    Headers:
        Authorization: Bearer <access_token>
    """

    keyword = "Bearer"
    model = None

    def get_model(self):
        """Get the MobileAuthToken model."""
        if self.model is not None:
            return self.model
        from admin_api.models import MobileAuthToken

        return MobileAuthToken

    def authenticate(self, request):
        """
        Authenticate the request and return a tuple of (user, token).
        """
        auth_header = authentication.get_authorization_header(request)

        if not auth_header:
            return None

        try:
            auth_parts = auth_header.decode("utf-8").split()
        except UnicodeDecodeError:
            raise exceptions.AuthenticationFailed(
                _("Invalid token header. Token string should not contain invalid characters.")
            )

        if len(auth_parts) == 0:
            return None

        if auth_parts[0].lower() != self.keyword.lower():
            # Not using our token type
            return None

        if len(auth_parts) == 1:
            raise exceptions.AuthenticationFailed(
                _("Invalid token header. No credentials provided.")
            )
        elif len(auth_parts) > 2:
            raise exceptions.AuthenticationFailed(
                _("Invalid token header. Token string should not contain spaces.")
            )

        token = auth_parts[1]
        return self.authenticate_credentials(token, request)

    def authenticate_credentials(self, key, request=None):
        """
        Validate the token and return the associated user.
        """
        model = self.get_model()

        try:
            token = model.objects.select_related("user").get(token=key, token_type="access")
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_("Invalid token."))

        # Check if token is revoked
        if token.is_revoked:
            raise exceptions.AuthenticationFailed(_("Token has been revoked."))

        # Check if token is expired
        if token.is_expired:
            raise exceptions.AuthenticationFailed(_("Token has expired."))

        # Check if user is active and staff
        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_("User account is disabled."))

        if not token.user.is_staff:
            raise exceptions.AuthenticationFailed(_("Staff access required."))

        # Update last used timestamp
        ip_address = self._get_client_ip(request)
        token.update_last_used(ip_address)

        return (token.user, token)

    def _get_client_ip(self, request):
        """Extract client IP from request."""
        if not request:
            return None
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response.
        """
        return self.keyword


class RefreshTokenAuthentication(authentication.BaseAuthentication):
    """
    Authentication using refresh tokens for the token refresh endpoint.

    Headers:
        Authorization: Refresh <refresh_token>
    """

    keyword = "Refresh"

    def get_model(self):
        from admin_api.models import MobileAuthToken

        return MobileAuthToken

    def authenticate(self, request):
        """
        Authenticate using a refresh token.
        """
        auth_header = authentication.get_authorization_header(request)

        if not auth_header:
            return None

        try:
            auth_parts = auth_header.decode("utf-8").split()
        except UnicodeDecodeError:
            raise exceptions.AuthenticationFailed(_("Invalid token header."))

        if len(auth_parts) == 0:
            return None

        if auth_parts[0].lower() != self.keyword.lower():
            return None

        if len(auth_parts) != 2:
            raise exceptions.AuthenticationFailed(_("Invalid refresh token header."))

        token = auth_parts[1]
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        """
        Validate the refresh token and return the associated user.
        """
        model = self.get_model()

        try:
            token = model.objects.select_related("user").get(token=key, token_type="refresh")
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_("Invalid refresh token."))

        if token.is_revoked:
            raise exceptions.AuthenticationFailed(_("Refresh token has been revoked."))

        if token.is_expired:
            raise exceptions.AuthenticationFailed(_("Refresh token has expired."))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_("User account is disabled."))

        if not token.user.is_staff:
            raise exceptions.AuthenticationFailed(_("Staff access required."))

        return (token.user, token)

    def authenticate_header(self, request):
        return self.keyword
