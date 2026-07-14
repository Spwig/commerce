"""
API views for Domain & SSL configuration.

All endpoints require staff authentication.
Includes self-hosted domain/SSL pipeline and hosted custom domain proxy.
"""

import json
import logging
import re

import httpx
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from domain_ssl.models import DomainConfiguration
from domain_ssl.services import domain_service
from domain_ssl.tasks import configure_domain_task

logger = logging.getLogger(__name__)

# RFC 1123 compliant domain validation
_DOMAIN_RE = re.compile(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63})*\.[A-Za-z]{2,}$")


@require_GET
@staff_member_required
def domain_ssl_status(request):
    """
    GET /api/domain-ssl/status/

    Returns current domain and SSL configuration state.
    """
    config = DomainConfiguration.get_instance()

    return JsonResponse(
        {
            "domain": config.domain,
            "previous_domain": config.previous_domain,
            "ssl_mode": config.ssl_mode,
            "ssl_mode_display": config.get_ssl_mode_display(),
            "status": config.status,
            "status_display": config.get_status_display(),
            "last_error": config.last_error,
            "task_id": config.task_id,
            "cert": {
                "domain": config.cert_domain,
                "issuer": config.cert_issuer,
                "expires_at": config.cert_expires_at.isoformat()
                if config.cert_expires_at
                else None,
                "obtained_at": config.cert_obtained_at.isoformat()
                if config.cert_obtained_at
                else None,
                "is_wildcard": config.is_wildcard,
                "has_valid_cert": config.has_valid_cert,
                "days_remaining": config.cert_days_remaining,
                "needs_renewal": config.needs_renewal,
            },
            "admin_email": config.admin_email,
            "auto_renew": config.auto_renew,
            "is_ssl_enabled": config.is_ssl_enabled,
            "ssl_modes": [
                {"value": choice[0], "label": str(choice[1])}
                for choice in DomainConfiguration.SSLMode.choices
            ],
        }
    )


@require_POST
@staff_member_required
def validate_dns_view(request):
    """
    POST /api/domain-ssl/validate-dns/

    Check if a domain resolves via DNS.
    Body: {"domain": "shop.example.com"}
    """
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    domain = data.get("domain", "").strip().lower()
    if not domain:
        return JsonResponse({"error": "Domain is required"}, status=400)
    if not _DOMAIN_RE.match(domain):
        return JsonResponse({"error": "Invalid domain format"}, status=400)

    result = domain_service.validate_dns(domain)

    # Also detect server IP for comparison
    server_ip = domain_service.get_server_ip()

    ip_match = False
    if server_ip and result["valid"]:
        ip_match = server_ip in result["resolved_ips"]

    return JsonResponse(
        {
            "domain": domain,
            "valid": result["valid"],
            "resolved_ips": result["resolved_ips"],
            "server_ip": server_ip,
            "ip_match": ip_match,
            "error": result.get("error", ""),
        }
    )


@require_POST
@staff_member_required
def configure_domain_view(request):
    """
    POST /api/domain-ssl/configure/

    Start the domain configuration pipeline as a background Celery task.
    Body: {
        "domain": "shop.example.com",
        "ssl_mode": "letsencrypt",
        "email": "admin@example.com",
        "cloudflare_token": "",
        "cloudflare_zone_id": ""
    }
    """
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    domain = data.get("domain", "").strip().lower()
    ssl_mode = data.get("ssl_mode", DomainConfiguration.SSLMode.NONE)
    email = data.get("email", "").strip()

    # Validate SSL mode
    valid_modes = [c[0] for c in DomainConfiguration.SSLMode.choices]
    if ssl_mode not in valid_modes:
        return JsonResponse({"error": f"Invalid SSL mode: {ssl_mode}"}, status=400)

    # Domain is required when SSL mode is not "none"
    if ssl_mode != DomainConfiguration.SSLMode.NONE and not domain:
        return JsonResponse({"error": "Domain is required when SSL is enabled"}, status=400)

    # Validate domain format when provided
    if domain and not _DOMAIN_RE.match(domain):
        return JsonResponse({"error": "Invalid domain format"}, status=400)

    # Let's Encrypt requires email
    if ssl_mode in ("letsencrypt", "letsencrypt_dns") and not email:
        return JsonResponse(
            {"error": "Email is required for Let's Encrypt certificates"}, status=400
        )

    # Check if a task is already running
    config = DomainConfiguration.get_instance()
    if config.status not in (
        DomainConfiguration.Status.IDLE,
        DomainConfiguration.Status.ERROR,
    ):
        return JsonResponse(
            {
                "error": "A configuration task is already in progress",
                "status": config.status,
            },
            status=409,
        )

    # Try to dispatch as a Celery task; fall back to synchronous execution
    # if the broker is unreachable (e.g. Celery worker not running).
    task_kwargs = {
        "domain": domain,
        "ssl_mode": ssl_mode,
        "email": email,
        "cloudflare_token": data.get("cloudflare_token", ""),
        "cloudflare_zone_id": data.get("cloudflare_zone_id", ""),
        "custom_cert_pem": data.get("custom_cert_pem", ""),
        "custom_key_pem": data.get("custom_key_pem", ""),
    }

    try:
        task = configure_domain_task.delay(**task_kwargs)
        return JsonResponse(
            {
                "task_id": task.id,
                "status": "started",
                "message": "Domain configuration started",
                "warning": (
                    "Your site may be briefly inaccessible while the web server "
                    "reloads with the new configuration. This typically takes "
                    "only a few seconds."
                ),
            }
        )
    except Exception as e:
        # Celery broker unavailable — run synchronously so the merchant
        # isn't left with a silently-queued task that never executes.
        logger.warning(
            "Celery unavailable (%s), running domain config synchronously",
            e,
        )
        success, message = domain_service.configure_domain(**task_kwargs)
        if success:
            return JsonResponse(
                {
                    "status": "completed",
                    "message": message,
                }
            )
        return JsonResponse(
            {
                "status": "error",
                "error": message,
            },
            status=500,
        )


@require_GET
@staff_member_required
def domain_ssl_progress(request):
    """
    GET /api/domain-ssl/progress/

    Poll for task progress. Returns current status from the model.
    """
    config = DomainConfiguration.get_instance()

    is_reloading = config.status == DomainConfiguration.Status.RELOADING
    return JsonResponse(
        {
            "status": config.status,
            "status_display": config.get_status_display(),
            "last_error": config.last_error,
            "task_id": config.task_id,
            "domain": config.domain,
            "ssl_mode": config.ssl_mode,
            "is_complete": config.status == DomainConfiguration.Status.IDLE,
            "is_error": config.status == DomainConfiguration.Status.ERROR,
            "info": (
                "The web server is reloading. Your site may be briefly "
                "inaccessible for a few seconds."
            )
            if is_reloading
            else "",
        }
    )


@require_POST
@staff_member_required
def upload_cert_view(request):
    """
    POST /api/domain-ssl/upload-cert/

    Upload a custom SSL certificate and key.
    Body: {"cert_pem": "...", "key_pem": "..."}
    """
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    cert_pem = data.get("cert_pem", "").strip()
    key_pem = data.get("key_pem", "").strip()

    if not cert_pem or not key_pem:
        return JsonResponse({"error": "Both cert_pem and key_pem are required"}, status=400)

    # Basic PEM validation
    if "-----BEGIN CERTIFICATE-----" not in cert_pem:
        return JsonResponse({"error": "Invalid certificate format (expected PEM)"}, status=400)
    if "-----BEGIN" not in key_pem or "KEY-----" not in key_pem:
        return JsonResponse({"error": "Invalid key format (expected PEM)"}, status=400)

    from domain_ssl.services import ssl_service

    success, message = ssl_service.save_custom_cert(cert_pem, key_pem)

    if success:
        # Parse and store cert metadata
        cert_info = ssl_service.parse_certificate()
        config = DomainConfiguration.get_instance()
        domain_mismatch = False

        if cert_info:
            config.cert_domain = cert_info.get("domain", "")
            config.cert_issuer = cert_info.get("issuer", "")
            config.cert_expires_at = cert_info.get("expires_at")
            config.is_wildcard = cert_info.get("is_wildcard", False)
            config.save()

            # Check if cert matches the configured domain
            cert_domain = cert_info.get("domain", "")
            if config.domain and cert_domain:
                if cert_domain.startswith("*."):
                    # Wildcard: *.example.com matches shop.example.com
                    wildcard_base = cert_domain[2:]
                    domain_mismatch = (
                        not config.domain.endswith(f".{wildcard_base}")
                        and config.domain != wildcard_base
                    )
                else:
                    domain_mismatch = cert_domain != config.domain

        # If domain and a local-cert SSL mode are configured, regenerate
        # the NGINX SSL config so the cert is actually served. This handles
        # the case where certs are uploaded after the domain was set (e.g.
        # via setup wizard) but before the full configure pipeline ran.
        from domain_ssl.services import docker_service, nginx_service

        _LOCAL_CERT_MODES = (
            DomainConfiguration.SSLMode.CUSTOM,
            DomainConfiguration.SSLMode.CLOUDFLARE_ORIGIN,
            DomainConfiguration.SSLMode.SELF_SIGNED,
            DomainConfiguration.SSLMode.LETSENCRYPT,
            DomainConfiguration.SSLMode.LETSENCRYPT_DNS,
        )
        if config.domain and config.ssl_mode in _LOCAL_CERT_MODES:
            try:
                nginx_service.write_ssl_config(
                    config.domain,
                    ssl_mode=config.ssl_mode,
                )
                logger.info(
                    "Wrote SSL NGINX config for %s after cert upload",
                    config.domain,
                )
            except Exception as e:
                logger.warning(
                    "Failed to write SSL NGINX config after cert upload: %s",
                    e,
                )

        # Reload NGINX to use the new certificate / config
        try:
            docker_service.reload_nginx()
        except Exception as e:
            logger.warning("NGINX reload after cert upload failed: %s", e)

        response_data = {
            "success": True,
            "message": message,
        }
        if domain_mismatch:
            response_data["warning"] = (
                f'Certificate is for "{cert_info.get("domain", "")}" but '
                f'your configured domain is "{config.domain}". '
                f"This may cause browser security warnings."
            )
        return JsonResponse(response_data)

    return JsonResponse(
        {
            "success": False,
            "message": message,
        }
    )


# ── Hosted Custom Domain Management ──────────────────────────────────
#
# These views proxy to the update server's domain API.
# Only available when IS_HOSTED=True.


def _get_store_slug():
    """Get the store slug from the SPWIG_DOMAIN env var or SiteSettings.

    Works both before and after a custom domain is active.
    """
    import os

    # Prefer the SPWIG_DOMAIN env var (set by merchant-ctl, never changes)
    spwig_domain = os.environ.get("SPWIG_DOMAIN", "")
    if spwig_domain.endswith(".myspwig.com"):
        return spwig_domain.replace(".myspwig.com", "")

    # Fallback: parse from SiteSettings (may fail if custom domain is active)
    try:
        from core.models import SiteSettings

        site_settings = SiteSettings.get_settings()
        if site_settings and site_settings.site_url:
            from urllib.parse import urlparse

            parsed = urlparse(site_settings.site_url)
            hostname = parsed.hostname or ""
            if hostname.endswith(".myspwig.com"):
                return hostname.replace(".myspwig.com", "")
    except Exception:
        pass
    return None


def _update_server_request(method, path, json_data=None):
    """Make an authenticated request to the update server hosting API."""
    base_url = settings.UPGRADE_SERVER_URL.rstrip("/")
    api_key = settings.UPGRADE_SERVER_INTERNAL_API_KEY

    if not api_key:
        return None, "Update server API key not configured"

    try:
        response = httpx.request(
            method,
            f"{base_url}/api/v1/hosting/{path}",
            json=json_data,
            headers={
                "X-API-Key": api_key,
                "Content-Type": "application/json",
            },
            timeout=30,
            follow_redirects=True,
        )
        return response, None
    except Exception as e:
        logger.error("Update server request failed: %s %s — %s", method, path, e)
        return None, f"Could not connect to update server: {e}"


@require_GET
@staff_member_required
def custom_domain_status(request):
    """
    GET /api/domain-ssl/custom-domain/

    Returns current custom domain config from the update server.
    Only available for hosted shops.
    """
    if not settings.IS_HOSTED:
        return JsonResponse({"error": "Not a hosted installation"}, status=404)

    store_slug = _get_store_slug()
    if not store_slug:
        return JsonResponse({"error": "Could not determine store slug"}, status=500)

    response, error = _update_server_request("GET", f"instances/{store_slug}/domain/")
    if error:
        return JsonResponse({"error": error}, status=502)

    return JsonResponse(response.json(), status=response.status_code)


@require_POST
@staff_member_required
def custom_domain_verify(request):
    """
    POST /api/domain-ssl/custom-domain/verify/
    Body: {"domain": "www.example.com"}

    Initiates or checks domain verification on the update server.
    Returns verification instructions (TXT record) or confirms verification.
    """
    if not settings.IS_HOSTED:
        return JsonResponse({"error": "Not a hosted installation"}, status=404)

    store_slug = _get_store_slug()
    if not store_slug:
        return JsonResponse({"error": "Could not determine store slug"}, status=500)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    domain = data.get("domain", "").strip().lower()
    if not domain:
        return JsonResponse({"error": "Domain is required"}, status=400)
    if not _DOMAIN_RE.match(domain):
        return JsonResponse({"error": "Invalid domain format"}, status=400)

    response, error = _update_server_request(
        "POST",
        f"instances/{store_slug}/domain/verify/",
        json_data={"domain": domain},
    )
    if error:
        return JsonResponse({"error": error}, status=502)

    return JsonResponse(response.json(), status=response.status_code)


@require_POST
@staff_member_required
def custom_domain_add(request):
    """
    POST /api/domain-ssl/custom-domain/add/
    Body: {"domain": "www.example.com"}

    Adds a verified custom domain. Proxies to update server which
    creates Cloudflare Custom Hostname and updates fleet infrastructure.
    """
    if not settings.IS_HOSTED:
        return JsonResponse({"error": "Not a hosted installation"}, status=404)

    store_slug = _get_store_slug()
    if not store_slug:
        return JsonResponse({"error": "Could not determine store slug"}, status=500)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    domain = data.get("domain", "").strip().lower()
    if not domain:
        return JsonResponse({"error": "Domain is required"}, status=400)
    if not _DOMAIN_RE.match(domain):
        return JsonResponse({"error": "Invalid domain format"}, status=400)

    response, error = _update_server_request(
        "POST",
        f"instances/{store_slug}/domain/",
        json_data={"domain": domain},
    )
    if error:
        return JsonResponse({"error": error}, status=502)

    return JsonResponse(response.json(), status=response.status_code)


@require_POST
@staff_member_required
def custom_domain_remove(request):
    """
    POST /api/domain-ssl/custom-domain/remove/

    Removes custom domain and reverts to myspwig.com subdomain.
    Uses POST instead of DELETE for simpler AJAX compatibility.
    """
    if not settings.IS_HOSTED:
        return JsonResponse({"error": "Not a hosted installation"}, status=404)

    store_slug = _get_store_slug()
    if not store_slug:
        return JsonResponse({"error": "Could not determine store slug"}, status=500)

    response, error = _update_server_request(
        "DELETE",
        f"instances/{store_slug}/domain/",
    )
    if error:
        return JsonResponse({"error": error}, status=502)

    return JsonResponse(response.json(), status=response.status_code)
