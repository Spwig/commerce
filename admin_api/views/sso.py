"""
Admin API SSO Views

Mobile SSO endpoints for the Spwig iOS app using ASWebAuthenticationSession.
Implements OIDC authorization code flow with one-time code exchange for
mobile token authentication.
"""

import logging
import re
import secrets
from urllib.parse import quote, urlencode

import requests as http_requests
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from admin_api.models import MobileAuthToken
from admin_api.permissions import HasMobileAppKey
from admin_api.serializers.auth import (
    ErrorResponseSerializer,
    StaffProfileSerializer,
)
from admin_api.services.audit_service import AuditService
from admin_api.throttling import AdminAPIThrottle, AdminAuthThrottle

logger = logging.getLogger(__name__)

MOBILE_SSO_CALLBACK_SCHEME = "spwig-sso"
SSO_STATE_CACHE_PREFIX = "sso_mobile_state:"
SSO_STATE_TTL = 300  # 5 minutes
SSO_CODE_CACHE_PREFIX = "sso_mobile_code:"
SSO_CODE_TTL = 60  # 60 seconds


def _generate_error_reference():
    return f"ERR-{secrets.token_hex(3).upper()}"


def _get_sso_status():
    """Check if SSO is enabled and configured. Returns (enabled, config) tuple."""
    try:
        from core.models import SiteSettings
        from enterprise_sso.models import SSOProviderConfig

        site_settings = SiteSettings.get_settings()
        if not site_settings.admin_sso_enabled:
            return False, None
        config = SSOProviderConfig.get_config()
        if not config.is_configured:
            return False, None
        return True, config
    except Exception:
        return False, None


@extend_schema(
    tags=["Admin - SSO"],
    summary=_("Get SSO configuration"),
    description=_("""
    Check if SSO is enabled and get provider details.

    **Public** — no authentication required.
    Called by the iOS app on login screen load to decide whether to show the SSO button.
    """),
    responses={200: dict},
)
@api_view(["GET"])
@permission_classes([HasMobileAppKey])
@throttle_classes([AdminAPIThrottle])
def sso_config(request):
    """Return SSO availability and provider display info."""
    enabled, config = _get_sso_status()

    return Response(
        {
            "success": True,
            "data": {
                "enabled": enabled,
                "provider_name": config.provider_name if enabled else None,
                "provider_display_name": config.provider_name if enabled else None,
            },
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin - SSO"],
    summary=_("Initiate SSO login"),
    description=_("""
    Start the OIDC authorization flow for mobile SSO.

    **Public** — no authentication required.
    The iOS app opens this URL in ASWebAuthenticationSession. Returns a 302 redirect
    to the identity provider's authorization endpoint.
    """),
    parameters=[
        OpenApiParameter(
            name="device_id",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Unique device identifier"),
            required=True,
        ),
    ],
    responses={
        302: OpenApiResponse(description="Redirect to identity provider"),
        400: ErrorResponseSerializer,
    },
)
@api_view(["GET"])
@permission_classes([AllowAny])
@throttle_classes([AdminAuthThrottle])
def sso_mobile_authorize(request):
    """Initiate OIDC authorization flow for mobile SSO."""
    device_id = request.query_params.get("device_id", "").strip()
    if not device_id or len(device_id) > 255 or not re.match(r"^[a-zA-Z0-9\-_.:]+$", device_id):
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("device_id parameter is required and must be a valid identifier."),
                    "reference": _generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    enabled, config = _get_sso_status()
    if not enabled:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("SSO is not enabled or not configured."),
                    "reference": _generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Generate state nonce and store with device_id
    state = secrets.token_urlsafe(32)
    cache.set(
        f"{SSO_STATE_CACHE_PREFIX}{state}",
        {"device_id": device_id},
        timeout=SSO_STATE_TTL,
    )

    # Build the callback URL
    callback_path = "/api/admin/auth/sso/mobile/callback/"
    callback_url = request.build_absolute_uri(callback_path)

    # Build the OIDC authorize URL
    params = {
        "response_type": "code",
        "client_id": config.oidc_client_id,
        "redirect_uri": callback_url,
        "scope": config.oidc_scopes or "openid email profile",
        "state": state,
    }
    authorize_url = f"{config.oidc_authorization_endpoint}?{urlencode(params)}"

    return HttpResponseRedirect(authorize_url)


@extend_schema(exclude=True)
@api_view(["GET"])
@permission_classes([AllowAny])
@throttle_classes([AdminAuthThrottle])
def sso_mobile_callback(request):
    """
    OIDC callback for mobile SSO.

    Called by the identity provider after user authentication — NOT by the iOS app.
    Exchanges the IdP code for tokens, validates the user, generates a one-time code,
    and redirects to spwig-sso://callback?code=<one_time_code>.
    """
    error = request.query_params.get("error")
    if error:
        error_desc = request.query_params.get("error_description", error)
        logger.warning("SSO mobile callback received IdP error: %s - %s", error, error_desc)
        return HttpResponseRedirect(
            f"{MOBILE_SSO_CALLBACK_SCHEME}://callback?error=idp_error&detail={quote(error, safe='')}"
        )

    code = request.query_params.get("code", "")
    state = request.query_params.get("state", "")

    if not code or not state:
        return HttpResponseRedirect(f"{MOBILE_SSO_CALLBACK_SCHEME}://callback?error=missing_params")

    # Validate state
    cache_key = f"{SSO_STATE_CACHE_PREFIX}{state}"
    state_data = cache.get(cache_key)
    if not state_data:
        logger.warning("SSO mobile callback: invalid or expired state")
        return HttpResponseRedirect(f"{MOBILE_SSO_CALLBACK_SCHEME}://callback?error=invalid_state")

    # Delete state (single-use, atomic check to prevent race conditions)
    if not cache.delete(cache_key):
        logger.warning("SSO mobile callback: state already consumed (concurrent request)")
        return HttpResponseRedirect(f"{MOBILE_SSO_CALLBACK_SCHEME}://callback?error=invalid_state")
    device_id = state_data["device_id"]

    # Get SSO config
    enabled, config = _get_sso_status()
    if not enabled:
        return HttpResponseRedirect(f"{MOBILE_SSO_CALLBACK_SCHEME}://callback?error=sso_disabled")

    # Exchange IdP code for tokens (server-to-server)
    callback_path = "/api/admin/auth/sso/mobile/callback/"
    callback_url = request.build_absolute_uri(callback_path)

    try:
        token_response = http_requests.post(
            config.oidc_token_endpoint,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": callback_url,
                "client_id": config.oidc_client_id,
                "client_secret": config.get_client_secret(),
            },
            timeout=15,
        )
        token_response.raise_for_status()
        token_data = token_response.json()
    except http_requests.RequestException as e:
        logger.error("SSO mobile token exchange failed: %s", e)
        return HttpResponseRedirect(
            f"{MOBILE_SSO_CALLBACK_SCHEME}://callback?error=token_exchange_failed"
        )

    # Get user claims from userinfo endpoint
    access_token = token_data.get("access_token")
    if not access_token:
        logger.error("SSO mobile token exchange: no access_token in response")
        return HttpResponseRedirect(
            f"{MOBILE_SSO_CALLBACK_SCHEME}://callback?error=token_exchange_failed"
        )

    try:
        userinfo_response = http_requests.get(
            config.oidc_userinfo_endpoint,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )
        userinfo_response.raise_for_status()
        claims = userinfo_response.json()
    except http_requests.RequestException as e:
        logger.error("SSO mobile userinfo fetch failed: %s", e)
        return HttpResponseRedirect(
            f"{MOBILE_SSO_CALLBACK_SCHEME}://callback?error=userinfo_failed"
        )

    # Verify email is confirmed by the IdP
    email_verified = claims.get("email_verified", False)
    if not email_verified:
        logger.warning("SSO mobile callback: email not verified by IdP")
        return HttpResponseRedirect(
            f"{MOBILE_SSO_CALLBACK_SCHEME}://callback?error=email_not_verified"
        )

    # Extract email from claims
    email = claims.get(config.claim_email, "").strip()
    if not email:
        logger.warning("SSO mobile callback: no email in claims")
        return HttpResponseRedirect(f"{MOBILE_SSO_CALLBACK_SCHEME}://callback?error=no_email")

    # Find or create user
    from django.contrib.auth import get_user_model

    User = get_user_model()
    user = User.objects.filter(email__iexact=email).first()

    if not user and config.auto_create_users:
        first_name = claims.get(config.claim_first_name, "")
        last_name = claims.get(config.claim_last_name, "")
        username = email.split("@")[0]
        # Ensure unique username (capped to prevent DoS)
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            if counter > 100:
                username = f"{base_username}_{secrets.token_hex(4)}"
                break
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        logger.info("SSO mobile: auto-created user %s", username)

    if not user:
        logger.warning(
            "SSO mobile callback: no user found for email %s***@%s",
            email[:2],
            email.split("@")[1] if "@" in email else "?",
        )
        return HttpResponseRedirect(f"{MOBILE_SSO_CALLBACK_SCHEME}://callback?error=user_not_found")

    if not user.is_active:
        return HttpResponseRedirect(
            f"{MOBILE_SSO_CALLBACK_SCHEME}://callback?error=account_disabled"
        )

    if config.restrict_to_staff and not user.is_staff:
        logger.warning(
            "SSO mobile callback: user %s***@%s is not staff",
            email[:2],
            email.split("@")[1] if "@" in email else "?",
        )
        return HttpResponseRedirect(f"{MOBILE_SSO_CALLBACK_SCHEME}://callback?error=unauthorized")

    # Apply role mapping from IdP group claims (same as web SSO)
    from enterprise_sso.backends import _apply_role_mapping

    if _apply_role_mapping(user, claims, config):
        user.save()

    # Generate one-time code for the iOS app
    one_time_code = secrets.token_urlsafe(32)
    cache.set(
        f"{SSO_CODE_CACHE_PREFIX}{one_time_code}",
        {"user_id": user.id, "device_id": device_id},
        timeout=SSO_CODE_TTL,
    )

    logger.info(
        "SSO mobile: generated one-time code for user_id=%s (device %s)", user.id, device_id[:8]
    )
    return HttpResponseRedirect(f"{MOBILE_SSO_CALLBACK_SCHEME}://callback?code={one_time_code}")


@extend_schema(
    tags=["Admin - SSO"],
    summary=_("Exchange SSO code for tokens"),
    description=_("""
    Exchange a one-time SSO code for access/refresh tokens.

    **Public** — no authentication required.
    Called by the iOS app after receiving the one-time code from the SSO callback redirect.
    Returns the same response shape as the password login endpoint.
    """),
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "One-time SSO code"},
                "device_id": {"type": "string", "description": "Device identifier"},
                "device_name": {"type": "string", "description": "Human-readable device name"},
            },
            "required": ["code", "device_id"],
        }
    },
    responses={
        200: dict,
        400: ErrorResponseSerializer,
        403: ErrorResponseSerializer,
    },
)
@api_view(["POST"])
@permission_classes([HasMobileAppKey])
@throttle_classes([AdminAuthThrottle])
def sso_mobile_token(request):
    """Exchange a one-time SSO code for access/refresh tokens."""
    code = request.data.get("code", "").strip()
    device_id = request.data.get("device_id", "").strip()
    device_name = request.data.get("device_name", "")

    if (
        not code
        or not device_id
        or len(device_id) > 255
        or not re.match(r"^[a-zA-Z0-9\-_.:]+$", device_id)
    ):
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("code and a valid device_id are required."),
                    "reference": _generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Look up one-time code
    cache_key = f"{SSO_CODE_CACHE_PREFIX}{code}"
    code_data = cache.get(cache_key)
    if not code_data:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid or expired SSO code."),
                    "reference": _generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Delete code (single-use, atomic check to prevent race conditions)
    if not cache.delete(cache_key):
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid or expired SSO code."),
                    "reference": _generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Validate device_id matches
    if code_data["device_id"] != device_id:
        logger.warning(
            "SSO mobile token: device_id mismatch (expected %s, got %s)",
            code_data["device_id"][:8],
            device_id[:8],
        )
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Device mismatch."),
                    "reference": _generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Get user
    from django.contrib.auth import get_user_model

    User = get_user_model()
    try:
        user = User.objects.get(id=code_data["user_id"])
    except User.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid or expired SSO code."),
                    "reference": _generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not user.is_active:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 403,
                    "message": _("User account is disabled."),
                    "reference": _generate_error_reference(),
                },
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    if not user.is_staff:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 403,
                    "message": _("User is not authorized."),
                    "reference": _generate_error_reference(),
                },
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    # Device limit check (same logic as staff_login in auth.py)
    mobile_settings = getattr(settings, "MOBILE_API_SETTINGS", {})
    max_devices = mobile_settings.get("MAX_DEVICES_PER_USER", 5)

    existing_devices = (
        MobileAuthToken.objects.filter(
            user=user,
            is_revoked=False,
            token_type="refresh",
        )
        .values("device_id")
        .distinct()
        .count()
    )

    is_existing_device = MobileAuthToken.objects.filter(
        user=user,
        device_id=device_id,
        is_revoked=False,
    ).exists()

    if not is_existing_device and existing_devices >= max_devices:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 403,
                    "message": _(
                        "Maximum device limit reached. Please logout from another device."
                    ),
                    "reference": _generate_error_reference(),
                },
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    # Revoke existing tokens for this device
    MobileAuthToken.revoke_all_for_device(user, device_id, reason="SSO login")

    # Create new token pair
    access_token, refresh_token = MobileAuthToken.create_token_pair(
        user=user,
        device_id=device_id,
        device_name=device_name,
    )

    # Calculate expiry in seconds
    access_lifetime = mobile_settings.get("ACCESS_TOKEN_LIFETIME_MINUTES", 30)
    expires_in = access_lifetime * 60

    # Log successful SSO login
    AuditService.log_login(
        user=user,
        device_id=device_id,
        device_name=device_name,
        request=request,
        success=True,
    )

    return Response(
        {
            "success": True,
            "message": _("Login successful."),
            "data": {
                "user": StaffProfileSerializer(user).data,
                "tokens": {
                    "access_token": access_token.token,
                    "refresh_token": refresh_token.token,
                    "token_type": "Bearer",
                    "expires_in": expires_in,
                },
            },
        },
        status=status.HTTP_200_OK,
    )
