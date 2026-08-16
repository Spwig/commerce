"""
Webhook action executor for form builder.
Posts form data to external URLs with optional HMAC signing.
"""

import hashlib
import hmac
import ipaddress
import json
import logging
import socket
from urllib.parse import urlparse, urlunparse

import requests
from requests.adapters import HTTPAdapter

from .base import BaseAction

logger = logging.getLogger(__name__)


def _addr_is_public(ip: str) -> bool:
    """True only for globally-routable addresses. Using ``is_global`` (rather
    than enumerating private/loopback/… categories) also excludes carrier-grade
    NAT (100.64.0.0/10) and other shared ranges that reach internal infra.
    Mirrors the SSRF check in ``agentic/identity/resolver.py``."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    if not addr.is_global or addr.is_multicast:
        return False
    # Unwrap an IPv4-mapped IPv6 address (::ffff:a.b.c.d) and re-check the v4.
    mapped = getattr(addr, "ipv4_mapped", None)
    return not (mapped is not None and (not mapped.is_global or mapped.is_multicast))


def resolve_public_ip(hostname: str) -> str | None:
    """Resolve ``hostname`` and return one address ONLY if every resolved
    address is public/routable. A host that resolves to any private/internal
    address (169.254.169.254, 127.0.0.1, RFC1918…) is rejected outright — a
    mixed public/private result is a classic SSRF dodge."""
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return None
    ips = {info[4][0] for info in infos}
    if not ips or not all(_addr_is_public(ip) for ip in ips):
        return None
    return sorted(ips)[0]


def validate_webhook_url(url: str) -> tuple[bool, str]:
    """Reject non-http(s) schemes and hosts that resolve into private/internal
    ranges (e.g. 169.254.169.254 cloud metadata). Returns (ok, reason)."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False, "Webhook URL must use http or https."
    if not parsed.hostname:
        return False, "Webhook URL has no host."
    if resolve_public_ip(parsed.hostname) is None:
        return False, "Webhook URL resolves to a disallowed (internal) address."
    return True, ""


class _PinnedIPAdapter(HTTPAdapter):
    """Pin the outbound connection to a pre-validated IP while keeping TLS SNI
    and certificate validation on the original hostname. This closes the
    DNS-rebinding TOCTOU: without it, ``requests`` performs a *second* DNS
    lookup after validation that could resolve to an internal address."""

    def __init__(self, hostname: str, ip: str, is_https: bool = True, **kw):
        self._hostname = hostname
        self._ip = ip
        self._is_https = is_https
        super().__init__(**kw)

    def init_poolmanager(self, connections, maxsize, block=False, **kw):
        # server_hostname/assert_hostname are HTTPS-only pool kwargs — passing
        # them to a plain-HTTP connection makes urllib3 raise TypeError, so only
        # add them for https webhooks.
        if self._is_https:
            kw["server_hostname"] = self._hostname  # SNI stays on the hostname
            kw["assert_hostname"] = self._hostname  # cert validated against hostname
        super().init_poolmanager(connections, maxsize, block=block, **kw)

    def send(self, request, **kwargs):
        parsed = urlparse(request.url)
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        # Bracket IPv6 literals so the rebuilt URL stays parseable.
        host = f"[{self._ip}]" if ":" in self._ip else self._ip
        request.url = urlunparse(parsed._replace(netloc=f"{host}:{port}"))
        # Keep the original Host (incl. a non-default port) so name-based vhosts
        # still route correctly.
        host_header = parsed.hostname + (f":{parsed.port}" if parsed.port else "")
        request.headers["Host"] = host_header
        return super().send(request, **kwargs)


class WebhookAction(BaseAction):
    """
    POST form data to an external webhook URL.

    Config schema:
    {
        "url": "https://example.com/webhook",
        "method": "POST",
        "headers": {"X-Custom": "value"},
        "include_fields": [],  # empty = all fields
        "secret": "optional-hmac-secret"
    }
    """

    TIMEOUT = 30  # seconds

    def execute(self):
        url = self.config.get("url", "")
        if not url:
            logger.warning("WebhookAction: No URL configured for action %s", self.action.pk)
            return {"status": "skipped", "reason": "No webhook URL configured"}

        # Resolve + validate ONCE, then pin the connection to that exact IP so a
        # rebinding DNS name can't flip to an internal address between check and
        # connect (TOCTOU).
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            return {"status": "error", "reason": "Webhook URL must be http(s) with a host."}
        pinned_ip = resolve_public_ip(parsed.hostname)
        if pinned_ip is None:
            logger.warning(
                "WebhookAction: blocked unsafe URL for action %s (%s)",
                self.action.pk,
                parsed.hostname,
            )
            return {"status": "error", "reason": "Webhook URL resolves to a disallowed address."}

        method = self.config.get("method", "POST").upper()
        custom_headers = self.config.get("headers", {})
        include_fields = self.config.get("include_fields", [])
        secret = self.config.get("secret", "")

        # Build payload
        payload = self._build_payload(include_fields)
        payload_json = json.dumps(payload, default=str)

        # Build headers
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Spwig-FormBuilder/1.0",
        }
        headers.update(custom_headers)

        # Add HMAC signature if secret is configured
        if secret:
            signature = hmac.new(
                secret.encode("utf-8"), payload_json.encode("utf-8"), hashlib.sha256
            ).hexdigest()
            headers["X-Signature-256"] = f"sha256={signature}"

        session = requests.Session()
        adapter = _PinnedIPAdapter(parsed.hostname, pinned_ip, is_https=(parsed.scheme == "https"))
        # Mount on the actual scheme only — the other scheme would otherwise fall
        # back to the default (unpinned) adapter and re-open the SSRF hole.
        session.mount(f"{parsed.scheme}://", adapter)
        try:
            response = session.request(
                method=method,
                url=url,
                data=payload_json,
                headers=headers,
                timeout=self.TIMEOUT,
                # A redirect would escape the pinned IP, so don't follow them.
                allow_redirects=False,
            )

            result = {
                "status": "sent",
                "http_status": response.status_code,
                "url": url,
            }

            if not response.ok:
                result["status"] = "error"
                result["response_body"] = response.text[:500]
                logger.warning(
                    "WebhookAction: HTTP %s from %s for response %s",
                    response.status_code,
                    url,
                    self.form_response.pk,
                )
            else:
                logger.info(
                    "WebhookAction: HTTP %s to %s for response %s",
                    response.status_code,
                    url,
                    self.form_response.pk,
                )

            return result

        except requests.Timeout:
            logger.error("WebhookAction: Timeout for %s (response %s)", url, self.form_response.pk)
            return {"status": "error", "error": f"Timeout after {self.TIMEOUT}s", "url": url}

        except requests.RequestException as e:
            logger.error(
                "WebhookAction: Failed for %s (response %s): %s", url, self.form_response.pk, e
            )
            return {"status": "error", "error": str(e), "url": url}

    def _build_payload(self, include_fields):
        """Build the webhook payload from form response data."""
        payload = {
            "event": "form_submission",
            "form": {
                "id": self.form_response.form.pk,
                "slug": self.form_response.form.slug,
                "name": self.form_response.form.name,
            },
            "response": {
                "id": self.form_response.pk,
                "submitted_at": str(self.form_response.submitted_at or ""),
                "status": self.form_response.status,
            },
            "data": {},
        }

        # Filter fields if include_fields is specified
        if include_fields:
            for field_name in include_fields:
                if field_name in self.form_response.data:
                    payload["data"][field_name] = self.form_response.data[field_name]
        else:
            payload["data"] = dict(self.form_response.data)

        # Add user info if available
        if self.form_response.user:
            payload["response"]["user_email"] = self.form_response.user.email

        return payload
