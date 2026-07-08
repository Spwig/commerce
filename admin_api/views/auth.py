"""
Admin API Authentication Views

Endpoints for staff login, logout, token refresh, profile, and 2FA verification.
"""
import secrets
import logging
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from admin_api.models import MobileAuthToken
from core.models import TrustedDevice
from admin_api.permissions import IsStaffUser
from admin_api.authentication import MobileTokenAuthentication
from admin_api.throttling import AdminAuthThrottle, AdminAPIThrottle
from admin_api.services.audit_service import AuditService
from core.api.api_descriptions import (
    RATE_LIMIT_EXCEEDED,
)
from admin_api.serializers.auth import (
    StaffLoginSerializer,
    TokenResponseSerializer,
    LoginResponseSerializer,
    RefreshTokenSerializer,
    LogoutSerializer,
    StaffProfileSerializer,
    ErrorResponseSerializer,
    SuccessResponseSerializer,
    TwoFactorVerifySerializer,
    TwoFactorRequiredResponseSerializer,
    StaffPasswordResetRequestSerializer,
    StaffPasswordResetConfirmSerializer,
)

logger = logging.getLogger(__name__)


def generate_error_reference():
    """Generate a unique error reference for debugging."""
    return f"ERR-{secrets.token_hex(3).upper()}"


def _check_user_mfa_enabled(user):
    """
    Check if MFA is enabled for a user.

    Returns:
        bool: True if user has TOTP or recovery codes set up
    """
    try:
        from allauth.mfa.utils import is_mfa_enabled
        return is_mfa_enabled(user)
    except ImportError:
        logger.warning("allauth.mfa not available, skipping MFA check")
        return False
    except Exception as e:
        logger.error(f"Error checking MFA status: {e}")
        return False


def _verify_totp_or_recovery(user, code):
    """
    Verify a TOTP code or recovery code for a user.

    Args:
        user: The user to verify for
        code: The TOTP code (6 digits) or recovery code

    Returns:
        tuple: (success: bool, method: str or None, error: str or None)
            - success: True if code is valid
            - method: 'totp' or 'recovery_codes' if successful
            - error: Error message if failed
    """
    try:
        from allauth.mfa.models import Authenticator

        # Clean up the code
        code = code.strip().replace(' ', '').replace('-', '')

        # Try TOTP first (6 digits)
        if len(code) == 6 and code.isdigit():
            try:
                totp_auth = Authenticator.objects.get(
                    user=user,
                    type=Authenticator.Type.TOTP
                )
                totp = totp_auth.wrap()
                if totp.validate_code(code):
                    # Update last used
                    totp_auth.last_used_at = timezone.now()
                    totp_auth.save(update_fields=['last_used_at'])
                    return True, 'totp', None
            except Authenticator.DoesNotExist:
                pass

        # Try recovery codes (typically longer, may have dashes)
        try:
            recovery_auth = Authenticator.objects.get(
                user=user,
                type=Authenticator.Type.RECOVERY_CODES
            )
            recovery = recovery_auth.wrap()
            if recovery.validate_code(code):
                # Update last used
                recovery_auth.last_used_at = timezone.now()
                recovery_auth.save(update_fields=['last_used_at'])
                return True, 'recovery_codes', None
        except Authenticator.DoesNotExist:
            pass

        return False, None, _('Invalid verification code.')

    except ImportError:
        logger.error("allauth.mfa not available")
        return False, None, _('Two-factor authentication is not available.')
    except Exception as e:
        logger.exception(f"Error verifying 2FA code: {e}")
        return False, None, _('Verification failed. Please try again.')


@extend_schema(
    tags=['Admin'],
    summary=_("Staff login"),
    description=_("""
    Authenticate a staff member and return access/refresh token pair.

    **Rate Limit:** 5 requests per minute

    **Request:**
    - email: Staff user email address
    - password: Account password
    - device_id: Unique device identifier
    - device_name: Optional human-readable device name

    **Response (no 2FA):**
    - access_token: Short-lived token for API calls (30 min)
    - refresh_token: Long-lived token for refreshing access (14 days)
    - expires_in: Access token expiry in seconds

    **Response (2FA required):**
    - requires_2fa: true
    - pending_token: Token to use for 2FA verification
    - expires_in: Seconds until pending token expires (5 min)

    If the user has 2FA enabled, the response will include `requires_2fa: true`
    and a `pending_token`. Use the pending_token with POST /auth/verify-2fa/
    to complete authentication.
    """),
    request=StaffLoginSerializer,
    responses={
        200: LoginResponseSerializer,
        400: ErrorResponseSerializer,
        401: ErrorResponseSerializer,
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([AdminAuthThrottle])
def staff_login(request):
    """
    Staff login endpoint.

    Authenticates a staff member and returns access/refresh tokens.
    If 2FA is enabled, returns a pending token for 2FA verification.
    """
    serializer = StaffLoginSerializer(data=request.data, context={'request': request})

    if not serializer.is_valid():
        # Log failed login attempt
        email = request.data.get('email', 'unknown')
        AuditService.log(
            user=None,
            action='auth.login_failed',
            resource_type='user',
            resource_id=email,
            old_value={},
            new_value={'reason': 'validation_error', 'errors': serializer.errors},
            request=request,
            success=False,
            error_message=str(serializer.errors)
        )

        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid login credentials.'),
                'reference': generate_error_reference(),
                'details': serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.validated_data['user']
    device_id = serializer.validated_data['device_id']
    device_name = serializer.validated_data.get('device_name', '')

    # Check if user has 2FA enabled
    if _check_user_mfa_enabled(user):
        # Check if this device is trusted (can skip 2FA)
        trusted_device = TrustedDevice.is_device_trusted(user, device_id)
        if trusted_device:
            # Device is trusted - update last used and skip 2FA
            trusted_device.update_last_used(
                ip_address=request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
            )

            # Log the trusted device bypass
            AuditService.log(
                user=user,
                action='auth.2fa_bypassed',
                resource_type='user',
                resource_id=str(user.id),
                old_value={},
                new_value={'device_id': device_id, 'reason': 'trusted_device'},
                request=request,
                success=True
            )
            # Continue to normal login (skip 2FA)
        else:
            # Create a 2FA pending token instead of full auth
            pending_token = MobileAuthToken.create_2fa_pending_token(
                user=user,
                device_id=device_id,
                device_name=device_name
            )

            # Log the 2FA challenge
            AuditService.log(
                user=user,
                action='auth.2fa_required',
                resource_type='user',
                resource_id=str(user.id),
                old_value={},
                new_value={'device_id': device_id, 'device_name': device_name},
                request=request,
                success=True
            )

            return Response({
                'success': True,
                'requires_2fa': True,
                'message': _('Two-factor authentication required.'),
                'data': {
                    'pending_token': pending_token.token,
                    'expires_in': MobileAuthToken.TWO_FA_PENDING_LIFETIME_MINUTES * 60
                }
            }, status=status.HTTP_200_OK)

    # Check device limit from SiteSettings (configurable by merchant)
    from core.models import SiteSettings
    site_settings = SiteSettings.get_settings()
    max_devices = site_settings.max_devices_per_user

    # 0 means unlimited
    if max_devices > 0:
        # Get count of unique devices for this user
        existing_devices = MobileAuthToken.objects.filter(
            user=user,
            is_revoked=False,
            token_type='refresh'
        ).values('device_id').distinct().count()

        # Check if this is a new device
        is_existing_device = MobileAuthToken.objects.filter(
            user=user,
            device_id=device_id,
            is_revoked=False
        ).exists()

        if not is_existing_device and existing_devices >= max_devices:
            return Response({
                'success': False,
                'error': {
                    'code': 403,
                    'message': _('Maximum device limit reached. Please remove a device from your profile or ask an administrator to increase the limit.'),
                    'reference': generate_error_reference()
                }
            }, status=status.HTTP_403_FORBIDDEN)

    # Revoke existing tokens for this device
    MobileAuthToken.revoke_all_for_device(user, device_id, reason='New login')

    # Create new token pair
    access_token, refresh_token = MobileAuthToken.create_token_pair(
        user=user,
        device_id=device_id,
        device_name=device_name
    )

    # Calculate expiry in seconds
    mobile_settings = getattr(settings, 'MOBILE_API_SETTINGS', {})
    access_lifetime = mobile_settings.get('ACCESS_TOKEN_LIFETIME_MINUTES', 30)
    expires_in = access_lifetime * 60

    # Log successful login
    AuditService.log_login(
        user=user,
        device_id=device_id,
        device_name=device_name,
        request=request,
        success=True
    )

    return Response({
        'success': True,
        'message': _('Login successful.'),
        'data': {
            'user': StaffProfileSerializer(user).data,
            'tokens': {
                'access_token': access_token.token,
                'refresh_token': refresh_token.token,
                'token_type': 'Bearer',
                'expires_in': expires_in
            }
        }
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Admin'],
    summary=_("Refresh access token"),
    description=_("""
    Get a new access token using a refresh token.

    **Rate Limit:** 5 requests per minute

    The refresh token may also be rotated depending on server configuration.
    """),
    request=RefreshTokenSerializer,
    responses={
        200: LoginResponseSerializer,
        401: ErrorResponseSerializer,
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([AdminAuthThrottle])
def refresh_token(request):
    """
    Refresh access token using a refresh token.

    Uses database-level locking to prevent race conditions when
    concurrent requests try to refresh the same token.
    """
    serializer = RefreshTokenSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid request.'),
                'reference': generate_error_reference(),
                'details': serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    refresh_token_str = serializer.validated_data['refresh_token']
    device_id = serializer.validated_data.get('device_id')  # Optional now

    # Use transaction with select_for_update to prevent race conditions
    # when multiple concurrent requests try to refresh the same token
    try:
        with transaction.atomic():
            query = {
                'token': refresh_token_str,
                'token_type': 'refresh',
            }
            # If device_id provided, include it in the query for extra validation
            if device_id:
                query['device_id'] = device_id

            # Lock the token row to prevent concurrent refresh
            try:
                token = MobileAuthToken.objects.select_for_update(nowait=True).select_related('user').get(**query)
            except MobileAuthToken.DoesNotExist:
                return Response({
                    'success': False,
                    'error': {
                        'code': 401,
                        'message': _('Invalid refresh token.'),
                        'reference': generate_error_reference()
                    }
                }, status=status.HTTP_401_UNAUTHORIZED)

            # Use device_id from the token if not provided in request
            if not device_id:
                device_id = token.device_id

            # Check token validity inside the lock
            if token.is_revoked:
                return Response({
                    'success': False,
                    'error': {
                        'code': 401,
                        'message': _('Refresh token has been revoked.'),
                        'reference': generate_error_reference()
                    }
                }, status=status.HTTP_401_UNAUTHORIZED)

            if token.is_expired:
                return Response({
                    'success': False,
                    'error': {
                        'code': 401,
                        'message': _('Refresh token has expired. Please login again.'),
                        'reference': generate_error_reference()
                    }
                }, status=status.HTTP_401_UNAUTHORIZED)

            user = token.user

            if not user.is_active:
                return Response({
                    'success': False,
                    'error': {
                        'code': 401,
                        'message': _('User account is disabled.'),
                        'reference': generate_error_reference()
                    }
                }, status=status.HTTP_401_UNAUTHORIZED)

            if not user.is_staff:
                return Response({
                    'success': False,
                    'error': {
                        'code': 403,
                        'message': _('Staff access required.'),
                        'reference': generate_error_reference()
                    }
                }, status=status.HTTP_403_FORBIDDEN)

            # Perform the token refresh inside the transaction
            return _perform_token_refresh(request, token, user, device_id)

    except Exception as e:
        # Handle lock contention (nowait=True raises DatabaseError if locked)
        if 'could not obtain lock' in str(e).lower() or 'lock' in str(e).lower():
            return Response({
                'success': False,
                'error': {
                    'code': 409,
                    'message': _('Token refresh in progress. Please retry.'),
                    'reference': generate_error_reference()
                }
            }, status=status.HTTP_409_CONFLICT)
        raise


def _perform_token_refresh(request, token, user, device_id):
    """
    Perform the actual token refresh operation.

    This is called within a transaction with the refresh token locked.
    """

    # Get settings
    mobile_settings = getattr(settings, 'MOBILE_API_SETTINGS', {})
    access_lifetime = mobile_settings.get('ACCESS_TOKEN_LIFETIME_MINUTES', 30)
    rotate_refresh = mobile_settings.get('ROTATE_REFRESH_TOKENS', True)
    refresh_lifetime = mobile_settings.get('REFRESH_TOKEN_LIFETIME_DAYS', 14)

    # Revoke old access tokens for this device
    MobileAuthToken.objects.filter(
        user=user,
        device_id=device_id,
        token_type='access',
        is_revoked=False
    ).update(
        is_revoked=True,
        revoked_at=timezone.now(),
        revoked_reason='Token refreshed'
    )

    # Create new access token
    new_access_token = MobileAuthToken.objects.create(
        user=user,
        token=MobileAuthToken.generate_token(),
        token_type='access',
        device_id=device_id,
        device_name=token.device_name,
        expires_at=timezone.now() + timezone.timedelta(minutes=access_lifetime)
    )

    response_data = {
        'success': True,
        'message': _('Token refreshed successfully.'),
        'data': {
            'tokens': {
                'access_token': new_access_token.token,
                'token_type': 'Bearer',
                'expires_in': access_lifetime * 60
            }
        }
    }

    # Optionally rotate refresh token
    if rotate_refresh:
        token.revoke(reason='Token rotated')
        new_refresh_token = MobileAuthToken.objects.create(
            user=user,
            token=MobileAuthToken.generate_token(),
            token_type='refresh',
            device_id=device_id,
            device_name=token.device_name,
            expires_at=timezone.now() + timezone.timedelta(days=refresh_lifetime)
        )
        response_data['data']['tokens']['refresh_token'] = new_refresh_token.token

    return Response(response_data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Admin'],
    summary=_("Staff logout"),
    description=_("""
    Logout from the current device or all devices.

    **Rate Limit:** 300 requests per minute

    **Options:**
    - device_id: Logout from specific device (defaults to current)
    - logout_all: Logout from all devices
    """),
    request=LogoutSerializer,
    responses={
        200: SuccessResponseSerializer,
        401: ErrorResponseSerializer,
    }
)
@api_view(['POST'])
@permission_classes([IsStaffUser])
@throttle_classes([AdminAPIThrottle])
def staff_logout(request):
    """
    Staff logout endpoint.
    """
    # Get the current token from authentication
    current_token = getattr(request, 'auth', None)

    serializer = LogoutSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid request.'),
                'reference': generate_error_reference(),
                'details': serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    logout_all = serializer.validated_data.get('logout_all', False)
    device_id = serializer.validated_data.get('device_id')

    # If no device_id provided, use current device
    if not device_id and current_token:
        device_id = current_token.device_id

    if logout_all:
        MobileAuthToken.revoke_all_for_user(request.user, reason='Logout from all devices')
        AuditService.log_logout(
            user=request.user,
            device_id=device_id or '',
            logout_all=True,
            request=request
        )
        return Response({
            'success': True,
            'message': _('Logged out from all devices.')
        }, status=status.HTTP_200_OK)
    elif device_id:
        MobileAuthToken.revoke_all_for_device(
            request.user,
            device_id,
            reason='Device logout'
        )
        AuditService.log_logout(
            user=request.user,
            device_id=device_id,
            logout_all=False,
            request=request
        )
        return Response({
            'success': True,
            'message': _('Logged out successfully.')
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Device ID required for logout.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Admin'],
    summary=_("Get staff profile"),
    description=_("""
    Get the current authenticated staff user's profile.

    **Rate Limit:** 300 requests per minute
    """),
    responses={
        200: StaffProfileSerializer,
        401: ErrorResponseSerializer,
    }
)
@api_view(['GET'])
@permission_classes([IsStaffUser])
@throttle_classes([AdminAPIThrottle])
def staff_profile(request):
    """
    Get staff user profile.
    """
    return Response({
        'success': True,
        'data': StaffProfileSerializer(request.user).data
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Admin'],
    summary=_("Verify 2FA code"),
    description=_("""
    Complete two-factor authentication by verifying a TOTP or recovery code.

    **Rate Limit:** 5 requests per minute

    **Request:**
    - pending_token: The token received from /auth/login/ when 2FA is required
    - code: 6-digit TOTP code from authenticator app, or recovery code
    - device_id: Same device_id used in the login request

    **Response (success):**
    - access_token: Short-lived token for API calls (30 min)
    - refresh_token: Long-lived token for refreshing access (14 days)
    - expires_in: Access token expiry in seconds

    **Response (failure):**
    - error with code 401: Invalid or expired pending token
    - error with code 400: Invalid 2FA code
    """),
    request=TwoFactorVerifySerializer,
    responses={
        200: LoginResponseSerializer,
        400: ErrorResponseSerializer,
        401: ErrorResponseSerializer,
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([AdminAuthThrottle])
def verify_2fa(request):
    """
    Verify 2FA code and complete authentication.

    After successful password verification with 2FA enabled, the client
    receives a pending_token. This endpoint verifies the TOTP or recovery
    code and issues the full access/refresh token pair.
    """
    # Log incoming request for debugging
    logger.debug(f"2FA verify request data: {request.data}")

    serializer = TwoFactorVerifySerializer(data=request.data)

    if not serializer.is_valid():
        # Log validation errors for debugging
        logger.warning(f"2FA verify validation failed: {serializer.errors}, data: {request.data}")

        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid request.'),
                'reference': generate_error_reference(),
                'details': serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    pending_token_str = serializer.validated_data['pending_token']
    code = serializer.validated_data['code']
    device_id = serializer.validated_data['device_id']
    trust_device = serializer.validated_data.get('trust_device', False)

    # Validate the pending token
    try:
        pending_token = MobileAuthToken.objects.select_related('user').get(
            token=pending_token_str,
            token_type='2fa_pending',
            device_id=device_id
        )
    except MobileAuthToken.DoesNotExist:
        AuditService.log(
            user=None,
            action='auth.2fa_verify_failed',
            resource_type='token',
            resource_id='unknown',
            old_value={},
            new_value={'reason': 'invalid_token', 'device_id': device_id},
            request=request,
            success=False,
            error_message='Invalid pending token'
        )
        return Response({
            'success': False,
            'error': {
                'code': 401,
                'message': _('Invalid or expired verification session. Please login again.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_401_UNAUTHORIZED)

    if pending_token.is_revoked:
        return Response({
            'success': False,
            'error': {
                'code': 401,
                'message': _('Verification session has been cancelled. Please login again.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_401_UNAUTHORIZED)

    if pending_token.is_expired:
        return Response({
            'success': False,
            'error': {
                'code': 401,
                'message': _('Verification session has expired. Please login again.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_401_UNAUTHORIZED)

    user = pending_token.user

    # Verify user is still valid
    if not user.is_active:
        return Response({
            'success': False,
            'error': {
                'code': 401,
                'message': _('User account is disabled.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_401_UNAUTHORIZED)

    if not user.is_staff:
        return Response({
            'success': False,
            'error': {
                'code': 403,
                'message': _('Staff access required.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_403_FORBIDDEN)

    # Verify the 2FA code
    success, method, error = _verify_totp_or_recovery(user, code)

    if not success:
        AuditService.log(
            user=user,
            action='auth.2fa_verify_failed',
            resource_type='user',
            resource_id=str(user.id),
            old_value={},
            new_value={'reason': 'invalid_code', 'device_id': device_id},
            request=request,
            success=False,
            error_message=str(error)
        )
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': error,
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    # 2FA verified - revoke the pending token
    pending_token.revoke(reason='2FA verified')

    # Trust the device if requested
    if trust_device:
        TrustedDevice.trust_device(
            user=user,
            device_id=device_id,
            device_name=pending_token.device_name
        )
        AuditService.log(
            user=user,
            action='auth.device_trusted',
            resource_type='device',
            resource_id=device_id,
            old_value={},
            new_value={'device_name': pending_token.device_name},
            request=request,
            success=True
        )

    # Check device limit from SiteSettings (configurable by merchant)
    from core.models import SiteSettings
    site_settings = SiteSettings.get_settings()
    max_devices = site_settings.max_devices_per_user

    # 0 means unlimited
    if max_devices > 0:
        # Get count of unique devices for this user
        existing_devices = MobileAuthToken.objects.filter(
            user=user,
            is_revoked=False,
            token_type='refresh'
        ).values('device_id').distinct().count()

        # Check if this is a new device
        is_existing_device = MobileAuthToken.objects.filter(
            user=user,
            device_id=device_id,
            token_type='refresh',
            is_revoked=False
        ).exists()

        if not is_existing_device and existing_devices >= max_devices:
            return Response({
                'success': False,
                'error': {
                    'code': 403,
                    'message': _('Maximum device limit reached. Please remove a device from your profile or ask an administrator to increase the limit.'),
                    'reference': generate_error_reference()
                }
            }, status=status.HTTP_403_FORBIDDEN)

    # Revoke existing tokens for this device
    MobileAuthToken.revoke_all_for_device(user, device_id, reason='New login after 2FA')

    # Create new token pair
    access_token, refresh_token = MobileAuthToken.create_token_pair(
        user=user,
        device_id=device_id,
        device_name=pending_token.device_name
    )

    # Calculate expiry in seconds
    mobile_settings = getattr(settings, 'MOBILE_API_SETTINGS', {})
    access_lifetime = mobile_settings.get('ACCESS_TOKEN_LIFETIME_MINUTES', 30)
    expires_in = access_lifetime * 60

    # Log successful 2FA verification and login
    AuditService.log(
        user=user,
        action='auth.2fa_verified',
        resource_type='user',
        resource_id=str(user.id),
        old_value={},
        new_value={
            'device_id': device_id,
            'device_name': pending_token.device_name,
            'method': method
        },
        request=request,
        success=True
    )

    AuditService.log_login(
        user=user,
        device_id=device_id,
        device_name=pending_token.device_name,
        request=request,
        success=True
    )

    return Response({
        'success': True,
        'message': _('Login successful.'),
        'data': {
            'user': StaffProfileSerializer(user).data,
            'tokens': {
                'access_token': access_token.token,
                'refresh_token': refresh_token.token,
                'token_type': 'Bearer',
                'expires_in': expires_in
            }
        }
    }, status=status.HTTP_200_OK)


# ============================================================================
# Password Reset
# ============================================================================

User = get_user_model()


@extend_schema(
    tags=['Admin Auth'],
    summary=_("Request staff password reset"),
    description=_("Request a password reset email for a staff account. Always returns success to prevent email enumeration. Rate limited to 5 requests per minute."),
    request=StaffPasswordResetRequestSerializer,
    responses={
        200: OpenApiResponse(description=_("Password reset email sent (if staff account exists)")),
        400: OpenApiResponse(description=_("Invalid email format")),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([AdminAuthThrottle])
def staff_password_reset_request(request):
    """
    Request staff password reset.
    POST /api/admin/auth/password-reset/
    """
    serializer = StaffPasswordResetRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid email address.'),
                'details': serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data['email']

    # Only look for active staff users
    staff_users = User.objects.filter(email=email, is_active=True, is_staff=True)

    for user in staff_users:
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Build reset URL using the Site domain (single-tenant, always pk=1)
        from django.contrib.sites.models import Site
        try:
            site = Site.objects.get(pk=1)
            base_url = f"https://{site.domain}"
        except Site.DoesNotExist:
            base_url = request.build_absolute_uri('/').rstrip('/')
        reset_url = f"{base_url}/reset-password/{uid}/{token}/"

        # Send via platform email template system
        try:
            from email_system.services.email_sender import EmailSendingService

            EmailSendingService.send_template_email(
                to_email=user.email,
                template_type='password_reset',
                context={
                    'user_name': user.get_full_name() or user.email,
                    'reset_url': reset_url,
                    'expiry_hours': getattr(settings, 'PASSWORD_RESET_TIMEOUT', 259200) // 3600,
                },
            )
        except Exception as e:
            logger.error(f"Failed to send password reset email to {user.email}: {e}")

        logger.info(f"Password reset requested for staff user {user.email}")

    # Audit log (regardless of whether user was found)
    AuditService.log(
        user=None,
        action='auth.password_reset_request',
        resource_type='user',
        resource_id=email,
        old_value={},
        new_value={'email': email},
        request=request,
        success=True,
    )

    # Always return success to prevent email enumeration
    return Response({
        'success': True,
        'message': _('If a staff account with that email exists, a password reset link has been sent.')
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Admin Auth'],
    summary=_("Confirm staff password reset"),
    description=_("Complete staff password reset using the uid and token from the reset email."),
    request=StaffPasswordResetConfirmSerializer,
    responses={
        200: OpenApiResponse(description=_("Password successfully reset")),
        400: OpenApiResponse(description=_("Invalid or expired reset link, or invalid password")),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([AdminAuthThrottle])
def staff_password_reset_confirm(request):
    """
    Confirm staff password reset with token.
    POST /api/admin/auth/password-reset/confirm/
    """
    serializer = StaffPasswordResetConfirmSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Password reset failed.'),
                'details': serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    uid_encoded = serializer.validated_data['uid']
    token = serializer.validated_data['token']

    # Decode uid and fetch user
    try:
        uid = urlsafe_base64_decode(uid_encoded).decode()
        user = User.objects.get(pk=uid, is_active=True, is_staff=True)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        AuditService.log(
            user=None,
            action='auth.password_reset_failed',
            resource_type='user',
            resource_id=uid_encoded,
            old_value={},
            new_value={'reason': 'invalid_token_or_user'},
            request=request,
            success=False,
            error_message='Invalid password reset link',
        )
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid or expired password reset link.'),
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    # Set the new password
    user.set_password(serializer.validated_data['new_password'])
    user.save()

    # Revoke all existing mobile auth tokens for security
    MobileAuthToken.revoke_all_for_user(user, reason='Password reset')

    AuditService.log(
        user=user,
        action='auth.password_reset_completed',
        resource_type='user',
        resource_id=str(user.pk),
        old_value={},
        new_value={'email': user.email},
        request=request,
        success=True,
    )

    logger.info(f"Password reset completed for staff user {user.email}")

    return Response({
        'success': True,
        'message': _('Password has been reset successfully.')
    }, status=status.HTTP_200_OK)
