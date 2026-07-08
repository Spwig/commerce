from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.api.throttling import POSAuthThrottle
from drf_spectacular.utils import extend_schema, OpenApiResponse

from admin_api.authentication import MobileTokenAuthentication
from pos_api.permissions import IsStaffUser
from core.api.api_descriptions import AUTH_REQUIRED, INVALID_AUTH_TOKEN, POS_LICENSE_REQUIRED


@extend_schema(
    summary=_("POS staff login"),
    description=_(
        "Authenticate a staff member for POS access. Returns access and refresh tokens. "
        "Uses the same token system as the Admin API (MobileTokenAuthentication)."
    ),
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'email': {'type': 'string', 'description': 'Staff email address'},
                'password': {'type': 'string', 'description': 'Staff password'},
                'terminal_uuid': {
                    'type': 'string',
                    'format': 'uuid',
                    'description': 'UUID of the POS terminal (optional)'
                },
            },
            'required': ['email', 'password'],
        }
    },
    responses={
        200: OpenApiResponse(description=_("Login successful, returns tokens and terminal config")),
        401: OpenApiResponse(description=_("Invalid credentials")),
        403: OpenApiResponse(description=_("User is not a staff member")),
    },
    tags=['POS - Authentication'],
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([POSAuthThrottle])
def pos_login(request):
    """Authenticate staff for POS access."""
    from django.contrib.auth import authenticate

    email = request.data.get('email', '')  # accepts username or email
    password = request.data.get('password', '')
    terminal_uuid = request.data.get('terminal_uuid')

    if not email or not password:
        return Response(
            {'success': False, 'error': {'code': 'MISSING_CREDENTIALS', 'message': 'Username/email and password are required.'}},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Try to authenticate — first as username, then look up by email
    user = authenticate(request, username=email, password=password)
    if user is None:
        # Try with email field directly
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            pass

    if user is None:
        return Response(
            {'success': False, 'error': {'code': 'INVALID_CREDENTIALS', 'message': 'Invalid email or password.'}},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.is_staff:
        return Response(
            {'success': False, 'error': {'code': 'NOT_STAFF', 'message': 'POS access requires a staff account.'}},
            status=status.HTTP_403_FORBIDDEN
        )

    # Check POS access via staff roles
    from staff_roles.services import can_access_pos as check_pos_access
    if not check_pos_access(user):
        return Response(
            {'success': False, 'error': {'code': 'NO_POS_ACCESS', 'message': 'Your role does not have POS access.'}},
            status=status.HTTP_403_FORBIDDEN
        )

    # Create tokens using Admin API token system
    from admin_api.models import MobileAuthToken
    access_obj, refresh_obj = MobileAuthToken.create_token_pair(
        user=user,
        device_id=f'pos-{terminal_uuid or "unknown"}',
        device_name=f'POS Terminal {terminal_uuid or "unknown"}',
    )

    # Get terminal config if UUID provided
    terminal_data = None
    if terminal_uuid:
        from pos_app.models import POSTerminal
        try:
            terminal = POSTerminal.objects.select_related('warehouse').get(
                uuid=terminal_uuid, is_active=True
            )
            terminal.last_heartbeat = timezone.now()
            terminal.save(update_fields=['last_heartbeat'])
            terminal_data = {
                'uuid': str(terminal.uuid),
                'name': terminal.name,
                'warehouse_id': terminal.warehouse_id,
                'warehouse_name': terminal.warehouse.pos_display_name or terminal.warehouse.name,
                'hardware_config': terminal.hardware_config,
                'currency': terminal.effective_currency,
            }
        except POSTerminal.DoesNotExist:
            pass

    # Get merged POS permissions for the frontend
    from staff_roles.services import get_user_pos_permissions_summary
    pos_permissions = get_user_pos_permissions_summary(user)

    # Check if user has a cashier PIN configured
    from pos_app.models import POSStaffDiscount
    has_cashier_pin = False
    try:
        staff_discount = POSStaffDiscount.objects.get(user=user)
        has_cashier_pin = bool(staff_discount.cashier_pin_hash or staff_discount.cashier_pin)
    except POSStaffDiscount.DoesNotExist:
        pass

    return Response({
        'success': True,
        'access_token': access_obj.token,
        'refresh_token': refresh_obj.token,
        'expires_at': access_obj.expires_at.isoformat(),
        'user': {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': user.get_full_name(),
            'has_cashier_pin': has_cashier_pin,
        },
        'terminal': terminal_data,
        'permissions': pos_permissions,
    })


@extend_schema(
    summary=_("Refresh POS access token"),
    description=_("Exchange a refresh token for a new access token."),
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'refresh_token': {'type': 'string'},
            },
            'required': ['refresh_token'],
        }
    },
    responses={
        200: OpenApiResponse(description=_("New access token")),
        401: OpenApiResponse(description=_("Invalid or expired refresh token")),
    },
    tags=['POS - Authentication'],
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def pos_refresh_token(request):
    """Refresh the access token using a refresh token."""
    refresh_token = request.data.get('refresh_token')
    if not refresh_token:
        return Response(
            {'success': False, 'error': {'code': 'MISSING_TOKEN', 'message': 'Refresh token is required.'}},
            status=status.HTTP_400_BAD_REQUEST
        )

    from admin_api.models import MobileAuthToken
    try:
        token_obj = MobileAuthToken.objects.get(
            token=refresh_token,
            token_type='refresh',
            is_revoked=False,
        )
        if token_obj.is_expired:
            raise ValueError('Expired')
    except (MobileAuthToken.DoesNotExist, ValueError):
        return Response(
            {'success': False, 'error': {'code': 'INVALID_TOKEN', 'message': 'Invalid or expired refresh token.'}},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Create a new access token for the same device
    from django.conf import settings as django_settings
    mobile_settings = getattr(django_settings, 'MOBILE_API_SETTINGS', {})
    access_lifetime = mobile_settings.get('ACCESS_TOKEN_LIFETIME_MINUTES', 30)

    new_access = MobileAuthToken.objects.create(
        user=token_obj.user,
        token=MobileAuthToken.generate_token(),
        token_type='access',
        device_id=token_obj.device_id,
        device_name=token_obj.device_name,
        expires_at=timezone.now() + timezone.timedelta(minutes=access_lifetime),
    )

    return Response({
        'success': True,
        'access_token': new_access.token,
        'expires_at': new_access.expires_at.isoformat(),
    })


@extend_schema(
    summary=_("POS logout"),
    description=_("Invalidate the current access and refresh tokens."),
    responses={
        200: OpenApiResponse(description=_("Logged out successfully")),
    },
    tags=['POS - Authentication'],
)
@api_view(['POST'])
@permission_classes([IsStaffUser])
def pos_logout(request):
    """Logout and invalidate tokens."""
    # The MobileTokenAuthentication sets request.auth to the token
    if hasattr(request, 'auth') and request.auth:
        request.auth.delete()

    return Response({'success': True, 'message': 'Logged out successfully.'})
