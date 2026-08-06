"""
Core API token authentication.

``APITokenAuthentication`` turns a merchant-generated ``core.APIToken`` into a
first-class DRF credential for the admin API. It is intentionally narrow:

- It only binds inside the ``admin_api`` URL namespace. Anywhere else — the
  storefront, the legacy help-metadata and instance-sync token consumers, any
  other DRF endpoint — it returns ``None`` and stays inert, so those paths are
  unchanged and a token cannot reach un-opted surfaces.
- It resolves the token to its ``created_by`` staff user, but caps that user to
  NON-SUPERUSER reach for the request (``is_superuser`` forced ``False`` on the
  in-memory instance, never persisted) so a long-lived token never inherits a
  superuser bypass.
- It enforces scopes fail-closed against ``admin_api.scope_map.SCOPE_MAP``: an
  unmapped endpoint, or a token lacking the required scope at the required
  access level, is denied. Read vs. write is derived from the HTTP method,
  unless the endpoint pins an override in ``admin_api.scope_map``.

Session and mobile-app-token requests never reach the scope logic here — they
present a different credential (session cookie / ``MobileAuthToken``), for
which this class returns ``None`` and lets the next authenticator handle them.
"""

from django.utils.translation import gettext_lazy as _
from rest_framework import authentication, exceptions

# HTTP header parsing is identical to MobileTokenAuthentication; both use the
# "Bearer" scheme. This class is registered FIRST so a core.APIToken is matched
# before MobileTokenAuthentication (which raises on an unknown Bearer token).


class APITokenAuthentication(authentication.BaseAuthentication):
    """
    Authenticate a ``core.APIToken`` Bearer credential for admin API calls.

    Returns ``(user, api_token)`` on success (so ``request.auth`` is the
    ``APIToken`` instance); ``None`` to defer to the next authenticator; or
    raises ``AuthenticationFailed`` / ``PermissionDenied`` for a bound-but-
    rejected token.

    Header:
        Authorization: Bearer <token>
    """

    keyword = "Bearer"

    def authenticate(self, request):
        # Only act inside the admin_api namespace; stay inert everywhere else.
        resolver_match = getattr(request, "resolver_match", None)
        if resolver_match is None or resolver_match.namespace != "admin_api":
            return None

        auth_header = authentication.get_authorization_header(request)
        if not auth_header:
            return None

        try:
            auth_parts = auth_header.decode("utf-8").split()
        except UnicodeDecodeError:
            # Malformed header — let the next authenticator surface the error.
            return None

        if not auth_parts or auth_parts[0].lower() != self.keyword.lower():
            return None
        if len(auth_parts) != 2:
            # A Bearer scheme with the wrong number of parts; defer.
            return None

        return self._authenticate_token(auth_parts[1], request)

    def _authenticate_token(self, key, request):
        from core.models import APIToken

        row = (
            APIToken.objects.filter(token=key, is_active=True).select_related("created_by").first()
        )
        if row is None:
            # Not one of ours (e.g. a mobile access token, or garbage) — defer
            # to MobileTokenAuthentication / the env-var help fallback.
            return None

        user = row.created_by
        if user is None or not (user.is_active and user.is_staff):
            # Unbindable legacy token (e.g. help/sync tokens with no creator).
            # Defer so the legacy validate_api_token() consumers keep working.
            return None

        # From here the token is bindable, so failures are hard denials.
        if row.is_expired:
            raise exceptions.AuthenticationFailed(_("Token has expired."))

        client_ip = self._get_client_ip(request)
        if row.allowed_ips and client_ip not in row.allowed_ips:
            raise exceptions.AuthenticationFailed(
                _("This token is not permitted from your IP address.")
            )

        # Least privilege: a token never carries superuser reach, regardless of
        # who created it. This mutates the in-memory instance ONLY — it is never
        # persisted here. INVARIANT: no admin_api handler reachable by a token
        # may call request.user.save(); doing so would demote the real creator
        # in the DB. Token-reachable self-service writes (profile, notifications)
        # are intentionally in admin_api.scope_map.TOKEN_FORBIDDEN. The marker
        # below lets such a handler detect a scoped-token user and refuse.
        user.is_superuser = False
        user._is_scoped_api_token = True

        self._enforce_scope(row, request)

        row.record_usage(ip_address=client_ip)
        return (user, row)

    def _enforce_scope(self, row, request):
        """Fail-closed scope check keyed off the resolved URL name."""
        from admin_api.scope_map import required_access, required_scope

        url_name = request.resolver_match.url_name
        scope_key = required_scope(url_name)
        if scope_key is None:
            # Unmapped endpoint: tokens are not permitted here.
            raise exceptions.PermissionDenied(
                _("API tokens are not permitted to access this endpoint.")
            )

        access = required_access(url_name, request.method)
        if not row.has_scope(scope_key, access=access):
            raise exceptions.PermissionDenied(
                _("This token does not have the required scope for this endpoint.")
            )

    def _get_client_ip(self, request):
        """Extract client IP (mirrors MobileTokenAuthentication)."""
        if request is None:
            return None
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")

    def authenticate_header(self, request):
        return self.keyword
