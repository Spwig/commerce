"""
Core views for the shop application.
"""

import hashlib
import hmac
import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path

import jwt
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit

logger = logging.getLogger(__name__)


@staff_member_required
@require_POST
@ensure_csrf_cookie
def switch_admin_theme(request):
    """
    View to switch admin theme preference.
    """
    logger.info(f"Theme switch request from {request.user}")
    logger.info(f"Request method: {request.method}")
    logger.info(f"Request content type: {request.content_type}")
    logger.info(f"Request body: {request.body}")

    try:
        # Handle different content types
        if request.content_type == "application/json":
            data = json.loads(request.body)
        else:
            # Fallback to POST data
            data = request.POST

        theme = data.get("theme", "dark")
        logger.info(f"Requested theme: {theme}")

        # Validate theme
        if theme not in ["light", "dark"]:
            logger.error(f"Invalid theme requested: {theme}")
            return JsonResponse(
                {"success": False, "error": _(f"Invalid theme: {theme}. Must be light or dark.")},
                status=400,
            )

        # Store theme preference in session
        request.session["admin_theme"] = theme
        logger.info(f"Set session admin_theme to: {theme}")

        # Create response
        response = JsonResponse(
            {"success": True, "theme": theme, "message": _(f"Theme switched to {theme}")}
        )

        # Also set as cookie for persistence
        response.set_cookie("admin_theme", theme, max_age=365 * 24 * 60 * 60)  # 1 year
        logger.info(f"Set cookie admin_theme to: {theme}")

        return response

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return JsonResponse({"success": False, "error": _(f"Invalid JSON: {str(e)}")}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in theme switch: {e}")
        return JsonResponse({"success": False, "error": _(f"Server error: {str(e)}")}, status=500)


@login_required
def community_redirect(request):
    """
    Redirect authenticated users to the Spwig community forum via SSO broker.

    This view handles automatic registration with the SSO broker on first use,
    then generates a short-lived JWT token and redirects to the broker.

    Flow:
    1. User clicks "Community" in Spwig admin
    2. If not registered, auto-register with SSO broker
    3. Generate JWT with user data (60s expiry)
    4. Redirect to SSO broker: https://sso.spwig.com/login?token={jwt}
    5. SSO broker validates JWT and redirects to Discourse
    6. User is logged into Discourse community forum
    """
    from allauth.account.models import EmailAddress

    from component_updates.models import UpdateServerConfig

    from .models import SiteSettings

    user = request.user

    # Check if user has a verified email address
    if not user.email:
        messages.error(
            request, _("You must have an email address configured to access the Community.")
        )
        return HttpResponseRedirect(reverse("admin:auth_user_change", args=[user.id]))

    if not EmailAddress.objects.filter(user=user, email=user.email, verified=True).exists():
        messages.warning(
            request,
            _(
                "Please verify your email address before accessing the Community. "
                "Check your inbox for a verification email or request a new one below."
            ),
        )
        return HttpResponseRedirect(reverse("account_email"))

    # Get site settings
    site_settings = SiteSettings.get_settings()
    broker_url = getattr(settings, "SSO_BROKER_URL", "https://sso.spwig.com")

    # Check if already registered with SSO broker
    if not site_settings.community_merchant_id or not site_settings.community_client_secret:
        # Need to register with SSO broker
        logger.info("First community access - registering with SSO broker")

        try:
            # Get store information
            update_config = UpdateServerConfig.get_instance()
            installation_uuid = str(update_config.installation_uuid)
            license_key = update_config.license_key or ""

            store_url = site_settings.site_url
            store_name = site_settings.site_name
            admin_email = site_settings.admin_email
            timestamp = int(time.time())

            # Get registration secret from platform secrets (DB first, then env fallback)
            from core.platform_secrets import get_sso_secret

            registration_secret = get_sso_secret()
            if not registration_secret:
                logger.error("SSO_REGISTRATION_SECRET not configured")
                return HttpResponse(
                    "Community integration is not properly configured. Missing registration secret.",
                    status=500,
                )

            # Build HMAC signature
            message = f"{installation_uuid}:{store_url}:{store_name}:{admin_email}:{timestamp}"
            if license_key:
                message += f":{license_key}"

            signature = hmac.new(
                registration_secret.encode(), message.encode(), hashlib.sha256
            ).hexdigest()

            # Call registration API
            registration_url = f"{broker_url}/api/register/"
            registration_data = {
                "installation_uuid": installation_uuid,
                "store_url": store_url,
                "store_name": store_name,
                "admin_email": admin_email,
                "license_key": license_key,
                "timestamp": timestamp,
                "signature": signature,
            }

            response = requests.post(
                registration_url,
                json=registration_data,
                timeout=10,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code != 200:
                error_msg = response.json().get("error", "Unknown error")
                logger.error(f"SSO registration failed: {error_msg}")
                return HttpResponse(
                    f"Failed to register with community services: {error_msg}", status=500
                )

            # Save credentials to SiteSettings
            result = response.json()
            site_settings.community_merchant_id = result["merchant_id"]
            site_settings.community_client_secret = result["client_secret"]
            site_settings.community_registered_at = timezone.now()
            site_settings.save(
                update_fields=[
                    "community_merchant_id",
                    "community_client_secret",
                    "community_registered_at",
                ],
                skip_validation=True,
            )

            logger.info(
                f"Successfully registered with SSO broker: merchant_id={result['merchant_id']}"
            )

        except requests.RequestException as e:
            logger.error(f"Failed to connect to SSO broker: {e}")
            return HttpResponse(
                "Failed to connect to community services. Please try again later.", status=503
            )
        except Exception as e:
            import traceback

            logger.error(f"Community registration failed: {e}\n{traceback.format_exc()}")
            return HttpResponse(
                f"Failed to register with community services. Please try again later. Error: {e}",
                status=500,
            )

    # Now we have credentials - generate JWT
    merchant_id = site_settings.community_merchant_id
    secret = site_settings.community_client_secret

    # Determine user groups for Discourse
    groups = ["merchants"]  # All authenticated users are merchants

    if user.is_staff:
        groups.append("staff")

    if user.is_superuser:
        groups.append("developers")

    # Build JWT payload
    payload = {
        "user_id": str(user.id),
        "email": user.email,
        "username": user.username,
        "name": user.get_full_name() or user.username,
        "merchant_id": merchant_id,
        "groups": groups,
        "exp": datetime.utcnow() + timedelta(seconds=60),
        "iat": datetime.utcnow(),
    }

    try:
        # Generate JWT token
        token = jwt.encode(payload, secret, algorithm="HS256")

        # Build redirect URL to SSO broker
        redirect_url = f"{broker_url}/sso?token={token}"

        logger.info(
            f"Community redirect: user={user.username} ({user.email}), merchant={merchant_id}"
        )

        return HttpResponseRedirect(redirect_url)

    except Exception as e:
        logger.error(f"Failed to generate community token for user {user.username}: {e}")
        return HttpResponse(
            "Failed to generate authentication token. Please try again later.", status=500
        )


# =============================================================================
# APPLE APP SITE ASSOCIATION (iOS Universal Links)
# =============================================================================


def apple_app_site_association(request):
    """
    Serve the Apple App Site Association file for iOS Universal Links.

    Reads IOS_APP_ID from MOBILE_API_SETTINGS. If not configured,
    returns a valid but empty AASA response.
    """
    ios_app_id = settings.MOBILE_API_SETTINGS.get("IOS_APP_ID", "")

    if ios_app_id:
        data = {
            "applinks": {
                "details": [
                    {
                        "appIDs": [ios_app_id],
                        "components": [
                            {"/": "/reset-password/*/*"},
                        ],
                    }
                ]
            }
        }
    else:
        data = {"applinks": {"details": []}}

    return JsonResponse(data, content_type="application/json")


# =============================================================================
# SECURITY.TXT (RFC 9116)
# =============================================================================


def security_txt(request):
    """
    Serve /.well-known/security.txt per RFC 9116.

    Tells security researchers how to report vulnerabilities.
    Contact and policy details are read from SiteSettings if available,
    with sensible defaults for the Spwig platform.
    """
    try:
        from core.models import SiteSettings

        site_settings = SiteSettings.objects.first()
        contact_email = (
            site_settings.contact_email
            if site_settings and site_settings.contact_email
            else "security@spwig.com"
        )
    except Exception:
        contact_email = "security@spwig.com"

    lines = [
        f"Contact: mailto:{contact_email}",
        "Expires: 2027-12-31T23:59:00.000Z",
        "Preferred-Languages: en",
        "Canonical: https://spwig.com/.well-known/security.txt",
        "Policy: https://spwig.com/security-policy",
    ]

    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


# =============================================================================
# HEALTH CHECK ENDPOINTS
# =============================================================================


def health_check(request):
    """
    Minimal public health check endpoint.

    Returns basic status without exposing internal infrastructure details.
    For detailed diagnostics, use /health/detailed/ (requires staff authentication).

    Used by:
    - Load balancers
    - Uptime monitors
    - Public status pages
    """
    # Simple check: can we serve HTTP requests? (If we got here, yes!)
    return JsonResponse({"status": "ok"})


def health_detailed(request):
    """
    Detailed health check for all services (requires staff authentication).

    Returns comprehensive status including database, cache, storage, celery, and migrations.
    Only accessible to authenticated staff users.

    Returns 200 if all healthy, 503 if any component fails.

    Used by:
    - Monitoring systems
    - Internal dashboards
    - DevOps debugging
    """
    # Require staff authentication
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse(
            {
                "status": "error",
                "message": "Authentication required. This endpoint is only accessible to staff users.",
            },
            status=403,
        )

    from django.conf import settings as django_settings
    from django.core.cache import cache
    from django.db import connection

    checks = {}
    all_healthy = True

    # Database check
    try:
        connection.ensure_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        checks["database"] = {"status": "healthy"}
    except Exception as e:
        checks["database"] = {"status": "unhealthy", "error": str(e)}
        all_healthy = False

    # Redis/Cache check
    try:
        cache.set("health_check", "ok", 10)
        if cache.get("health_check") == "ok":
            checks["cache"] = {"status": "healthy"}
        else:
            checks["cache"] = {"status": "unhealthy", "error": "Cache read/write failed"}
            all_healthy = False
    except Exception as e:
        checks["cache"] = {"status": "unhealthy", "error": str(e)}
        all_healthy = False

    # MinIO check (optional - don't fail health if MinIO is slow)
    try:
        from minio import Minio

        minio_client = Minio(
            django_settings.MINIO_ENDPOINT,
            access_key=django_settings.MINIO_ACCESS_KEY,
            secret_key=django_settings.MINIO_SECRET_KEY,
            secure=django_settings.MINIO_USE_SSL,
        )
        minio_client.bucket_exists(django_settings.MINIO_MEDIA_BUCKET)
        checks["storage"] = {"status": "healthy"}
    except Exception as e:
        checks["storage"] = {"status": "degraded", "error": str(e)}
        # Don't fail overall health for storage issues

    # Celery check (optional)
    try:
        from celery import current_app

        inspect = current_app.control.inspect()
        if inspect.ping():
            checks["celery"] = {"status": "healthy"}
        else:
            checks["celery"] = {"status": "degraded", "error": "No workers responding"}
    except Exception as e:
        checks["celery"] = {"status": "degraded", "error": str(e)}
        # Don't fail overall health for Celery issues

    # Migration check
    try:
        from django.db.migrations.executor import MigrationExecutor

        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        if plan:
            checks["migrations"] = {"status": "pending", "count": len(plan)}
        else:
            checks["migrations"] = {"status": "up_to_date"}
    except Exception as e:
        checks["migrations"] = {"status": "unknown", "error": str(e)}

    response_data = {
        "status": "healthy" if all_healthy else "unhealthy",
        "checks": checks,
        "version": getattr(django_settings, "SPWIG_VERSION", "unknown"),
        "timestamp": timezone.now().isoformat(),
    }

    return JsonResponse(response_data, status=200 if all_healthy else 503)


def health_live(request):
    """
    Kubernetes liveness probe - is the process running?
    Lightweight check, always returns 200 unless process is dead.
    """
    return JsonResponse({"status": "alive"})


def health_ready(request):
    """
    Kubernetes readiness probe - can we serve traffic?
    Returns 200 only if database is accessible AND migrations are complete.

    nginx will not route traffic to this container until ready.
    """
    from django.db import connection
    from django.db.migrations.executor import MigrationExecutor

    try:
        # Check database connection
        connection.ensure_connection()

        # Check if migrations are complete
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())

        if plan:
            # Migrations pending - not ready
            return JsonResponse(
                {"status": "not_ready", "reason": "migrations_pending", "pending_count": len(plan)},
                status=503,
            )

        return JsonResponse({"status": "ready"})

    except Exception as e:
        return JsonResponse(
            {"status": "not_ready", "reason": "database_unavailable", "error": str(e)}, status=503
        )


# =============================================================================
# SSO REDIRECT ENDPOINT FOR EXTERNAL SPWIG SERVICES
# =============================================================================


@login_required
def sso_redirect(request):
    """
    SSO redirect endpoint for external Spwig services.

    This endpoint allows external Spwig services (like License Server, SSO Broker)
    to redirect users here for authentication. The store validates the logged-in
    user and generates a JWT that is sent back to the requesting service.

    Flow:
    1. External service redirects user to: /admin/sso/redirect/?
           client_id=sso-broker&
           redirect_uri=https://sso.spwig.com/sso/callback/&
           state=<RANDOM_STATE>
    2. Store validates user is logged in (or redirects to login)
    3. Store generates JWT with merchant/user data
    4. Store redirects back to the service with the token

    GET Parameters:
        client_id: The client requesting authentication (e.g., 'sso-broker')
        redirect_uri: Where to redirect after authentication
        state: CSRF protection state parameter (passed through)

    Security:
        - Requires staff login (same as community_redirect)
        - Validates client_id against allowed clients
        - Validates redirect_uri against allowed URIs for that client
        - JWT is short-lived (60 seconds)
    """
    from allauth.account.models import EmailAddress

    from component_updates.models import UpdateServerConfig

    from .models import SiteSettings

    user = request.user

    # Get request parameters
    client_id = request.GET.get("client_id")
    redirect_uri = request.GET.get("redirect_uri")
    state = request.GET.get("state", "")

    # Validate required parameters
    if not client_id:
        return JsonResponse(
            {"error": "missing_client_id", "message": "client_id parameter is required"}, status=400
        )

    if not redirect_uri:
        return JsonResponse(
            {"error": "missing_redirect_uri", "message": "redirect_uri parameter is required"},
            status=400,
        )

    # Define allowed clients and their redirect URIs
    # In production, the SSO broker is the only allowed client
    allowed_clients = {
        "sso-broker": {
            "name": "Spwig SSO Broker",
            "redirect_uris": [
                "https://sso.spwig.com/sso/callback/",
                "https://sso.spwig.com/authorize/callback/",
                # Allow localhost for development
                "http://localhost:8000/sso/callback/",
                "http://127.0.0.1:8000/sso/callback/",
            ],
        }
    }

    # Validate client_id
    if client_id not in allowed_clients:
        logger.warning(f"SSO redirect: invalid client_id '{client_id}' from user {user.username}")
        return JsonResponse(
            {"error": "invalid_client", "message": f"Unknown client: {client_id}"}, status=400
        )

    # Validate redirect_uri
    client_config = allowed_clients[client_id]
    if redirect_uri not in client_config["redirect_uris"]:
        logger.warning(
            f"SSO redirect: invalid redirect_uri '{redirect_uri}' for client '{client_id}'"
        )
        return JsonResponse(
            {
                "error": "invalid_redirect_uri",
                "message": f"Redirect URI not allowed for client {client_id}",
            },
            status=400,
        )

    # Validate user has verified email
    if not user.email:
        messages.error(request, _("You must have an email address configured to use SSO services."))
        return HttpResponseRedirect(reverse("admin:auth_user_change", args=[user.id]))

    if not EmailAddress.objects.filter(user=user, email=user.email, verified=True).exists():
        messages.warning(
            request,
            _(
                "Please verify your email address before using SSO services. "
                "Check your inbox for a verification email or request a new one below."
            ),
        )
        return HttpResponseRedirect(reverse("account_email"))

    # Get site settings and merchant info
    site_settings = SiteSettings.get_settings()

    # Get merchant credentials (same as community_redirect)
    # If not registered with SSO broker yet, we need to register first
    if not site_settings.community_merchant_id or not site_settings.community_client_secret:
        # Auto-register with SSO broker (same logic as community_redirect)
        broker_url = getattr(settings, "SSO_BROKER_URL", "https://sso.spwig.com")

        try:
            update_config = UpdateServerConfig.get_instance()
            installation_uuid = str(update_config.installation_uuid)
            license_key = update_config.license_key or ""

            store_url = site_settings.site_url
            store_name = site_settings.site_name
            admin_email = site_settings.admin_email
            timestamp = int(time.time())

            from core.platform_secrets import get_sso_secret

            registration_secret = get_sso_secret()
            if not registration_secret:
                logger.error("SSO_REGISTRATION_SECRET not configured for SSO redirect")
                return JsonResponse(
                    {
                        "error": "configuration_error",
                        "message": "SSO integration is not properly configured",
                    },
                    status=500,
                )

            # Build HMAC signature
            message = f"{installation_uuid}:{store_url}:{store_name}:{admin_email}:{timestamp}"
            if license_key:
                message += f":{license_key}"

            signature = hmac.new(
                registration_secret.encode(), message.encode(), hashlib.sha256
            ).hexdigest()

            # Call registration API
            registration_url = f"{broker_url}/api/register/"
            registration_data = {
                "installation_uuid": installation_uuid,
                "store_url": store_url,
                "store_name": store_name,
                "admin_email": admin_email,
                "license_key": license_key,
                "timestamp": timestamp,
                "signature": signature,
            }

            response = requests.post(
                registration_url,
                json=registration_data,
                timeout=10,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code != 200:
                error_msg = response.json().get("error", "Unknown error")
                logger.error(f"SSO registration failed during sso_redirect: {error_msg}")
                return JsonResponse(
                    {
                        "error": "registration_failed",
                        "message": f"Failed to register with SSO broker: {error_msg}",
                    },
                    status=500,
                )

            # Save credentials to SiteSettings
            result = response.json()
            site_settings.community_merchant_id = result["merchant_id"]
            site_settings.community_client_secret = result["client_secret"]
            site_settings.community_registered_at = timezone.now()
            site_settings.save(
                update_fields=[
                    "community_merchant_id",
                    "community_client_secret",
                    "community_registered_at",
                ],
                skip_validation=True,
            )

            logger.info(
                f"Auto-registered with SSO broker via sso_redirect: merchant_id={result['merchant_id']}"
            )

        except requests.RequestException as e:
            logger.error(f"Failed to connect to SSO broker during sso_redirect: {e}")
            return JsonResponse(
                {
                    "error": "connection_error",
                    "message": "Failed to connect to SSO services. Please try again later.",
                },
                status=503,
            )
        except Exception as e:
            import traceback

            logger.error(
                f"SSO registration failed during sso_redirect: {e}\n{traceback.format_exc()}"
            )
            return JsonResponse(
                {
                    "error": "internal_error",
                    "message": "An error occurred during SSO setup. Please try again later.",
                },
                status=500,
            )

    # Build JWT payload with merchant and user data
    merchant_id = site_settings.community_merchant_id
    secret = site_settings.community_client_secret
    store_url = site_settings.site_url
    store_name = site_settings.site_name

    payload = {
        # Merchant/store data
        "merchant_id": merchant_id,
        "store_url": store_url,
        "merchant_name": store_name,
        # User data
        "user_id": str(user.id),
        "email": user.email,
        "username": user.username,
        "name": user.get_full_name() or user.username,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        # Token metadata
        "auth_type": "merchant",  # Identifies this as a merchant SSO auth
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(seconds=60),  # Short-lived
    }

    try:
        # Generate JWT token
        token = jwt.encode(payload, secret, algorithm="HS256")

        # Build redirect URL back to SSO broker
        from urllib.parse import urlencode

        params = {"token": token}
        if state:
            params["state"] = state

        final_redirect = f"{redirect_uri}?{urlencode(params)}"

        logger.info(
            f"SSO redirect: user={user.username}, merchant={merchant_id}, client={client_id}"
        )

        return HttpResponseRedirect(final_redirect)

    except Exception as e:
        logger.error(f"Failed to generate SSO token for user {user.username}: {e}")
        return JsonResponse(
            {
                "error": "token_generation_failed",
                "message": "Failed to generate authentication token. Please try again later.",
            },
            status=500,
        )


# =============================================================================
# MAINTENANCE MODE PREVIEW
# =============================================================================


@staff_member_required
def maintenance_preview(request):
    """
    Preview the maintenance page without enabling maintenance mode.
    Only accessible by staff members.
    """
    from django.shortcuts import render

    from core.models import SiteSettings

    site_settings = SiteSettings.objects.first()
    if not site_settings:
        site_settings = SiteSettings.objects.create()

    # Get logo URL if available
    logo_url = None
    if hasattr(site_settings, "site_logo") and site_settings.site_logo:
        try:
            logo_url = site_settings.site_logo.file.url if site_settings.site_logo.file else None
        except Exception:
            pass

    # Check if we have a PageBuilder maintenance page
    page_id = getattr(site_settings, "maintenance_page_id", None)

    if page_id:
        try:
            from page_builder.models import Page

            page = (
                Page.objects.prefetch_related("elements")
                .select_related("theme", "header_template", "footer_template")
                .get(pk=page_id, status="published")
            )

            elements = page.elements.filter(parent_element__isnull=True, is_active=True).order_by(
                "order"
            )

            # Get brand CSS
            brand_css_url = None
            try:
                from design.theme_models import ThemeBranding

                branding = ThemeBranding.objects.first()
                if branding:
                    brand_css_url = branding.get_css_url()
            except Exception:
                pass

            context = {
                "page": page,
                "elements": elements,
                "page_title": f"[Preview] {page.meta_title or page.title}",
                "brand_css_url": brand_css_url,
                "is_maintenance": True,
                "is_preview": True,
                "hide_header": getattr(page, "hide_header", True),
                "hide_footer": getattr(page, "hide_footer", True),
            }

            return render(request, "page_builder/page.html", context, status=200)

        except Page.DoesNotExist:
            logger.warning(f"Maintenance page {page_id} not found, using fallback preview")
        except Exception as e:
            logger.error(f"Error rendering maintenance preview: {e}")

    # Fallback to static template preview
    context = {
        "store_name": site_settings.site_name or "Our Store",
        "maintenance_message": site_settings.maintenance_message,
        "store_logo": logo_url,
        "spwig_url": "https://spwig.com",
    }

    return render(request, "maintenance/maintenance.html", context, status=200)


@staff_member_required
def filter_users(request):
    """
    AJAX endpoint for filtering users.
    Returns filtered user list as HTML with count.
    """
    from django.contrib.auth import get_user_model
    from django.db.models import Q
    from django.template.loader import render_to_string

    User = get_user_model()

    # Ensure this is an AJAX request
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Get filter parameters
    search = request.GET.get("search", "").strip()
    is_staff = request.GET.get("is_staff", "").strip()
    is_active = request.GET.get("is_active", "").strip()
    is_superuser = request.GET.get("is_superuser", "").strip()
    group = request.GET.get("group", "").strip()

    # Build query with prefetch_related for performance
    users = User.objects.prefetch_related("groups", "user_permissions")

    # Apply search filter
    if search:
        users = users.filter(
            Q(username__icontains=search)
            | Q(email__icontains=search)
            | Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
        )

    # Apply is_staff filter
    if is_staff == "true":
        users = users.filter(is_staff=True)
    elif is_staff == "false":
        users = users.filter(is_staff=False)

    # Apply is_active filter
    if is_active == "true":
        users = users.filter(is_active=True)
    elif is_active == "false":
        users = users.filter(is_active=False)

    # Apply is_superuser filter
    if is_superuser == "true":
        users = users.filter(is_superuser=True)
    elif is_superuser == "false":
        users = users.filter(is_superuser=False)

    # Apply group filter
    if group:
        users = users.filter(groups__id=group)

    # Order by username
    users = users.order_by("username")

    # Render partial template
    html = render_to_string(
        "admin/auth/user/partials/user_cards.html", {"users": users, "request": request}
    )

    return JsonResponse({"html": html, "count": users.count()})


# ============================================================================
# License Acceptance Views
# ============================================================================


def license_accept(request):
    """
    License acceptance page.

    GET: Display license text with acceptance form.
    POST: Record acceptance and redirect to admin.

    This view does NOT require authentication — it runs before
    the admin is set up on fresh installations.
    """
    from core.license_acceptance import get_license_acceptance_service

    service = get_license_acceptance_service()

    # If already accepted and no re-acceptance needed, redirect onwards
    if service.is_accepted():
        needs_reaccept, _ = service.needs_reacceptance()
        if not needs_reaccept:
            return redirect("/")

    license_text = service.get_license_text()
    license_version = service.extract_license_version(license_text) or "1.0.0"

    # Determine if this is a re-acceptance (upgrade scenario)
    acceptance_info = service.get_acceptance_info()
    is_reacceptance = acceptance_info is not None and acceptance_info.get("accepted", False)

    if request.method == "POST":
        if request.POST.get("accept") == "true" and request.POST.get("accept_checkbox"):
            # Get client IP
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(",")[0].strip()
            else:
                ip_address = request.META.get("REMOTE_ADDR")

            # Get user if authenticated
            user = request.user if request.user.is_authenticated else None
            email = ""
            if user:
                email = user.email

            service.record_acceptance(
                accepted_via="web",
                ip_address=ip_address,
                email=email,
                user=user,
            )

            return redirect("/")

    context = {
        "license_text": license_text,
        "license_version": license_version,
        "is_reacceptance": is_reacceptance,
    }
    return render(request, "core/license_acceptance.html", context)


def license_view(request):
    """
    Read-only license text display.
    """
    from core.license_acceptance import get_license_acceptance_service

    service = get_license_acceptance_service()
    license_text = service.get_license_text()
    license_version = service.extract_license_version(license_text) or "1.0.0"

    context = {
        "license_text": license_text,
        "license_version": license_version,
    }
    return render(request, "core/license_acceptance.html", context)


def third_party_notices_view(request):
    """Serve THIRD_PARTY_NOTICES.txt as a downloadable file."""
    from django.http import FileResponse, Http404

    notices_path = Path(settings.BASE_DIR) / "THIRD_PARTY_NOTICES.txt"
    if not notices_path.exists():
        raise Http404("Third-party notices file not found.")

    return FileResponse(
        open(notices_path, "rb"),
        content_type="text/plain; charset=utf-8",
        filename="THIRD_PARTY_NOTICES.txt",
    )


@csrf_exempt
@require_POST
def csp_report(request):
    """
    Endpoint for Content-Security-Policy violation reports.
    Browsers POST JSON violation reports here when CSP_REPORT_ONLY is active.
    """
    csp_logger = logging.getLogger("csp")
    try:
        body = json.loads(request.body)
        report = body.get("csp-report", body)
        blocked = report.get("blocked-uri", "unknown")
        directive = report.get("violated-directive", "unknown")
        source = report.get("source-file", "unknown")
        line = report.get("line-number", "")
        csp_logger.warning(
            "CSP violation: blocked=%s directive=%s source=%s line=%s",
            blocked,
            directive,
            source,
            line,
            extra={"csp_report": report},
        )
    except Exception:
        csp_logger.warning("CSP report received but could not be parsed", exc_info=True)
    return HttpResponse(status=204)


# =============================================================================
# PLATFORM ACTIVATION
# =============================================================================


def activate(request):
    """
    Public activation page for fresh installations.

    GET: Show activation form (enter setup token)
    POST: Validate token, activate license, create admin user, redirect to admin

    This view is the web-UI counterpart of the activate_with_token management
    command. Both use core.activation for the shared activation logic.
    """
    from core.activation import activate_with_token as do_activation

    # If already activated, redirect to homepage
    license_path = Path(
        getattr(settings, "LICENSE_PATH", "/opt/shop-platform/license/license.json")
    )
    if license_path.exists():
        return redirect("/")

    context = {"error": None, "result": None}

    if request.method == "POST":
        setup_token = request.POST.get("setup_token", "").strip()

        if not setup_token:
            context["error"] = "Please enter your setup token."
        else:
            # Use the request host as domain
            domain = request.get_host().split(":")[0]  # Strip port
            result = do_activation(setup_token, domain=domain)

            if result.success:
                context["result"] = result
                # Don't redirect immediately — show credentials page first
            else:
                context["error"] = result.error

    return render(request, "core/activate.html", context)


@require_POST
@csrf_exempt
@ratelimit(key="ip", rate="10/m", method="POST", block=True)
def cookie_consent_view(request):
    """
    Store cookie consent choices. CSRF-exempt because this must work
    on first visit before any CSRF cookie exists.

    Accepts JSON: {"analytics": bool, "marketing": bool, "functional": bool}
    Logs the consent decision server-side for GDPR Article 7(1) compliance,
    and returns JSON confirmation. The cookie itself is set client-side by
    cookie_banner.js.
    """
    if len(request.body) > 1024:
        return JsonResponse({"ok": False, "error": "request_too_large"}, status=413)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"ok": False, "error": "invalid_json"}, status=400)

    if not isinstance(data, dict):
        return JsonResponse({"ok": False, "error": "invalid_payload"}, status=400)

    consent = {
        "necessary": True,
        "analytics": bool(data.get("analytics", False)),
        "marketing": bool(data.get("marketing", False)),
        "functional": bool(data.get("functional", False)),
    }

    # Log consent server-side for GDPR proof-of-consent (Article 7(1))
    try:
        from .models import CookieConsentLog

        # Determine action from consent choices
        optional = (consent["analytics"], consent["marketing"], consent["functional"])
        if all(optional):
            action = "accept_all"
        elif not any(optional):
            action = "reject_all"
        else:
            action = "save_preferences"

        # Extract client IP (proxy-aware)
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(",")[0].strip()
        else:
            ip_address = request.META.get("REMOTE_ADDR")

        CookieConsentLog.objects.create(
            action=action,
            consent_data=consent,
            ip_address=ip_address,
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key or "",
        )
    except Exception:
        # Never fail the main operation because of logging issues
        logger.exception("Failed to log cookie consent")

    # Note: cookie is set client-side by cookie_banner.js using
    # encodeURIComponent(JSON.stringify(...)). We must NOT set it here
    # because Django's SimpleCookie uses Python's _quote() which encodes
    # the JSON differently (backslash-escaped quotes), causing the JS
    # getCookie/JSON.parse flow to fail on subsequent page loads.
    return JsonResponse({"ok": True, "consent": consent})


# =============================================================================
# ADMIN STYLE GUIDE (Development tool)
# =============================================================================


@staff_member_required
def admin_style_guide(request):
    """
    Visual style guide showing all classes from admin-base.css.
    Development tool for template migration reference.
    """
    return render(
        request,
        "admin/style_guide.html",
        {
            "title": "Admin CSS Style Guide",
        },
    )
