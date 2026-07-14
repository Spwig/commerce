import logging

import requests
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from mozilla_django_oidc.views import (
    OIDCAuthenticationCallbackView,
    OIDCAuthenticationRequestView,
    OIDCLogoutView,
)

from .backends import _get_db_setting

logger = logging.getLogger(__name__)


class SpwigOIDCCallbackView(OIDCAuthenticationCallbackView):
    """OIDC callback view that reads settings from the database."""

    @staticmethod
    def get_settings(attr, *args):
        return _get_db_setting(attr, *args)

    @property
    def failure_url(self):
        """Redirect to admin login on failure."""
        from django.urls import reverse

        try:
            return reverse("admin:login")
        except Exception:
            return "/en/admin/login/"

    def login_failure(self):
        from django.contrib import messages
        from django.utils.translation import gettext as _

        messages.error(
            self.request, _("SSO authentication failed. Please try again or use local login.")
        )
        return super().login_failure()


class SpwigOIDCAuthenticateView(OIDCAuthenticationRequestView):
    """OIDC authentication initiation view that reads settings from the database."""

    @staticmethod
    def get_settings(attr, *args):
        return _get_db_setting(attr, *args)


class SpwigOIDCLogoutView(OIDCLogoutView):
    """OIDC logout view that reads settings from the database."""

    @staticmethod
    def get_settings(attr, *args):
        return _get_db_setting(attr, *args)


@staff_member_required
@require_POST
def oidc_discover(request):
    """
    AJAX endpoint for OIDC discovery. Fetches the well-known
    OpenID configuration and returns the endpoint URLs.
    """
    import json

    try:
        body = json.loads(request.body)
        discovery_url = body.get("discovery_url", "").strip()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({"error": "Invalid request body"}, status=400)

    if not discovery_url:
        return JsonResponse({"error": "discovery_url is required"}, status=400)

    # Ensure URL ends with well-known path
    if not discovery_url.endswith("/.well-known/openid-configuration"):
        if not discovery_url.endswith("/"):
            discovery_url += "/"
        discovery_url += ".well-known/openid-configuration"

    try:
        response = requests.get(discovery_url, timeout=10)
        response.raise_for_status()
        config = response.json()
    except requests.RequestException as e:
        logger.warning("OIDC discovery failed for %s: %s", discovery_url, e)
        return JsonResponse({"error": f"Failed to fetch discovery document: {e}"}, status=400)
    except ValueError:
        return JsonResponse({"error": "Invalid JSON in discovery response"}, status=400)

    return JsonResponse(
        {
            "authorization_endpoint": config.get("authorization_endpoint", ""),
            "token_endpoint": config.get("token_endpoint", ""),
            "userinfo_endpoint": config.get("userinfo_endpoint", ""),
            "jwks_uri": config.get("jwks_uri", ""),
            "end_session_endpoint": config.get("end_session_endpoint", ""),
            "issuer": config.get("issuer", ""),
            "scopes_supported": config.get("scopes_supported", []),
        }
    )
