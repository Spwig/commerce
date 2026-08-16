import ipaddress
import logging
import socket
from urllib.parse import urljoin, urlparse

import requests
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from mozilla_django_oidc.views import (
    OIDCAuthenticationCallbackView,
    OIDCAuthenticationRequestView,
    OIDCLogoutView,
)
from requests.adapters import HTTPAdapter

from .backends import _get_db_setting

logger = logging.getLogger(__name__)


def _validate_discovery_url(url):
    """Reject discovery URLs that could enable SSRF.

    Requires HTTPS and rejects any host that resolves to a loopback,
    private, link-local, or otherwise non-global address. Returns a
    ``(error, pinned_ip)`` tuple: ``error`` is a message string if the URL
    is disallowed (with ``pinned_ip`` ``None``), otherwise ``error`` is
    ``None`` and ``pinned_ip`` is the validated address the connection must
    be pinned to. Pinning the address closes the DNS-rebinding gap where the
    hostname could resolve to a different (private) IP when Requests
    reconnects.
    """
    parsed = urlparse(url)
    if parsed.scheme != "https":
        return "discovery_url must use HTTPS", None

    hostname = parsed.hostname
    if not hostname:
        return "discovery_url must include a valid host", None

    try:
        addrinfo = socket.getaddrinfo(hostname, parsed.port or 443, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return "Could not resolve discovery host", None

    if not addrinfo:
        return "Could not resolve discovery host", None

    for info in addrinfo:
        ip = ipaddress.ip_address(info[4][0])
        if not ip.is_global or ip.is_reserved:
            return "discovery_url resolves to a disallowed address", None

    # Pin the first validated address for the actual connection so the
    # hostname is not re-resolved (and possibly rebound to a private IP)
    # when the request is sent.
    return None, addrinfo[0][4][0]


class _PinnedIPHTTPSAdapter(HTTPAdapter):
    """Force HTTPS connections to a pre-validated IP address.

    The connection is opened to ``pinned_ip`` (the address vetted by
    ``_validate_discovery_url``) while SNI and certificate verification stay
    bound to the original hostname, preventing a DNS-rebinding SSRF between
    validation and connection.
    """

    def __init__(self, pinned_ip, *args, **kwargs):
        self._pinned_ip = pinned_ip
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        parsed = urlparse(request.url)
        hostname = parsed.hostname
        port = parsed.port

        # Keep TLS SNI + certificate hostname verification tied to the real
        # hostname even though we connect to the pinned IP.
        pool_kw = self.poolmanager.connection_pool_kw
        pool_kw["server_hostname"] = hostname
        pool_kw["assert_hostname"] = hostname

        host_header = hostname
        if port:
            host_header = f"{hostname}:{port}"
        request.headers["Host"] = host_header

        # Rewrite the netloc to the validated IP so no second DNS lookup can
        # redirect the connection to a private/loopback address.
        ip_netloc = f"[{self._pinned_ip}]" if ":" in self._pinned_ip else self._pinned_ip
        if port:
            ip_netloc = f"{ip_netloc}:{port}"
        request.url = parsed._replace(netloc=ip_netloc).geturl()

        return super().send(request, **kwargs)


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
        # Follow redirects manually so every hop is re-validated against the
        # SSRF checks below; a public URL must not be able to redirect the
        # server to a loopback/private/link-local address.
        current_url = discovery_url
        for _ in range(5):
            error, pinned_ip = _validate_discovery_url(current_url)
            if error:
                return JsonResponse({"error": error}, status=400)
            # Connect to the exact IP that passed validation so the hostname
            # cannot be re-resolved to a private address (DNS rebinding).
            session = requests.Session()
            session.mount("https://", _PinnedIPHTTPSAdapter(pinned_ip))
            with session:
                response = session.get(current_url, timeout=10, allow_redirects=False)
            if response.is_redirect or response.is_permanent_redirect:
                current_url = urljoin(current_url, response.headers.get("Location", ""))
                continue
            break
        else:
            return JsonResponse({"error": "Too many redirects"}, status=400)
        response.raise_for_status()
        config = response.json()
    except requests.RequestException as e:
        logger.warning("OIDC discovery failed for %s: %s", discovery_url, e)
        return JsonResponse({"error": f"Failed to fetch discovery document: {e}"}, status=400)
    except ValueError:
        return JsonResponse({"error": "Invalid JSON in discovery response"}, status=400)

    if not isinstance(config, dict):
        return JsonResponse({"error": "Discovery document must be a JSON object"}, status=400)

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
