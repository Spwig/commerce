"""
API views for accounts app
Provides customer-facing endpoints for authentication, profile, and address management
"""
import logging

from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view, permission_classes, action, throttle_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.api.throttling import PublicWriteThrottle
from core.api.authentication import HeadlessAPIMixin
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from core.api.api_descriptions import (
    AUTH_REQUIRED, VALIDATION_ERROR, RATE_LIMIT_EXCEEDED,
    NOT_FOUND, INVALID_REQUEST,
)

logger = logging.getLogger(__name__)

from .models import CustomerProfile
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    CustomerProfileSerializer,
    CustomerProfileUpdateSerializer,
    DashboardPreferencesSerializer,
    AddressSerializer,
    AddressListSerializer,
    CommunicationPreferenceSerializer,
    PreferenceUpdateSerializer,
    BulkPreferenceUpdateSerializer,
)
from orders.models import Address

User = get_user_model()


@extend_schema(
    tags=['Accounts'],
    summary=_("Register new user account"),
    description=_("Create a new customer account with email and password. Returns user profile and authentication token."),
    request=UserRegistrationSerializer,
    responses={
        201: OpenApiResponse(description=_("Registration successful, user created and logged in")),
        400: OpenApiResponse(description=_("Invalid registration data or email already exists")),
    }
)
@api_view(['POST'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user account
    POST /api/accounts/register/
    """
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        # Create auth token
        token, created = Token.objects.get_or_create(user=user)

        # Log the user in
        login(request, user)

        # Get profile data
        profile = user.profile
        profile_serializer = CustomerProfileSerializer(profile)

        return Response({
            'success': True,
            'message': _('Registration successful.'),
            'data': {
                'user': profile_serializer.data,
                'token': token.key
            }
        }, status=status.HTTP_201_CREATED)

    return Response({
        'success': False,
        'message': _('Registration failed.'),
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Accounts'],
    summary=_("User login"),
    description=_("Authenticate user with email and password. Returns user profile and authentication token for API access."),
    request=UserLoginSerializer,
    responses={
        200: OpenApiResponse(description=_("Login successful, returns user data and auth token")),
        400: OpenApiResponse(description=_("Invalid credentials or account inactive")),
    }
)
@api_view(['POST'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def user_login(request):
    """
    User login
    POST /api/accounts/login/
    """
    serializer = UserLoginSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        user = serializer.validated_data['user']

        # Create or get auth token
        token, created = Token.objects.get_or_create(user=user)

        # Log the user in
        login(request, user)

        # Get profile data
        profile = CustomerProfile.get_or_create_for_user(user)
        profile_serializer = CustomerProfileSerializer(profile)

        return Response({
            'success': True,
            'message': _('Login successful.'),
            'data': {
                'user': profile_serializer.data,
                'token': token.key
            }
        }, status=status.HTTP_200_OK)

    return Response({
        'success': False,
        'message': _('Login failed.'),
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Accounts'],
    summary=_("User logout"),
    description=_("Log out the current user and invalidate their authentication token. Requires authentication."),
    request=None,
    responses={
        200: OpenApiResponse(
            description=_("Logout successful, token deleted"),
            response={"success": True, "message": "Logout successful."}
        ),
    }
)
@api_view(['POST'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([IsAuthenticated])
def user_logout(request):
    """
    User logout
    POST /api/accounts/logout/
    """
    # Delete the token
    try:
        request.user.auth_token.delete()
    except:
        pass

    # Logout
    logout(request)

    return Response({
        'success': True,
        'message': _('Logout successful.')
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Accounts'],
    summary=_("Request password reset"),
    description=_("Request a password reset email. Sends reset link to email if account exists. Always returns success to prevent email enumeration. Rate limited to 20 requests per hour."),
    request=PasswordResetSerializer,
    responses={
        200: OpenApiResponse(description=_("Password reset email sent (if account exists)")),
        400: OpenApiResponse(description=_("Invalid email format")),
        429: OpenApiResponse(description=_("Rate limit exceeded - too many password reset requests")),
    }
)
@api_view(['POST'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
@throttle_classes([PublicWriteThrottle])
def password_reset_request(request):
    """
    Request password reset
    POST /api/accounts/password-reset/
    """
    serializer = PasswordResetSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']

        # Find users with this email
        users = User.objects.filter(email=email, is_active=True)

        for user in users:
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Create reset URL (frontend will handle this)
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

            # Send email via template system
            from email_system.services.email_sender import EmailSendingService
            try:
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

        # Always return success to prevent email enumeration
        return Response({
            'success': True,
            'message': _('If an account with that email exists, a password reset link has been sent.')
        }, status=status.HTTP_200_OK)

    return Response({
        'success': False,
        'message': _('Invalid email address.'),
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Accounts'],
    summary=_("Confirm password reset"),
    description=_("Complete password reset process using the token from email. Requires uidb64 and token from reset link."),
    request=PasswordResetConfirmSerializer,
    responses={
        200: OpenApiResponse(description=_("Password successfully reset")),
        400: OpenApiResponse(description=_("Invalid or expired reset token, or invalid password")),
    }
)
@api_view(['POST'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def password_reset_confirm(request, uidb64, token):
    """
    Confirm password reset with token
    POST /api/accounts/password-reset-confirm/{uidb64}/{token}/
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        return Response({
            'success': False,
            'message': _('Invalid password reset link.')
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer = PasswordResetConfirmSerializer(data=request.data)

    if serializer.is_valid():
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({
            'success': True,
            'message': _('Password has been reset successfully.')
        }, status=status.HTTP_200_OK)

    return Response({
        'success': False,
        'message': _('Password reset failed.'),
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Accounts'],
    summary=_("Get user profile"),
    description=_("Retrieve the current authenticated user's profile information including name, preferences, and settings."),
    responses=CustomerProfileSerializer
)
@api_view(['GET'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([IsAuthenticated])
def get_profile(request):
    """
    Get current user profile
    GET /api/accounts/profile/
    """
    profile = CustomerProfile.get_or_create_for_user(request.user)
    serializer = CustomerProfileSerializer(profile)

    return Response({
        'success': True,
        'data': serializer.data
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Accounts'],
    summary=_("Update user profile"),
    description=_("Update the current user's profile information. Use PUT for full update or PATCH for partial update."),
    request=CustomerProfileUpdateSerializer,
    responses={
        200: OpenApiResponse(description=_("Profile updated successfully")),
        400: OpenApiResponse(description=_("Invalid profile data")),
    }
)
@api_view(['PUT', 'PATCH'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update current user profile
    PUT/PATCH /api/accounts/profile/
    """
    profile = CustomerProfile.get_or_create_for_user(request.user)
    serializer = CustomerProfileUpdateSerializer(
        profile,
        data=request.data,
        partial=request.method == 'PATCH'
    )

    if serializer.is_valid():
        serializer.save()

        # Return full profile data
        full_serializer = CustomerProfileSerializer(profile)

        return Response({
            'success': True,
            'message': _('Profile updated successfully.'),
            'data': full_serializer.data
        }, status=status.HTTP_200_OK)

    return Response({
        'success': False,
        'message': _('Profile update failed.'),
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Accounts'],
    summary=_("Update user preferences"),
    description=_("Update user dashboard preferences including notification settings, display options, and other customization."),
    request=DashboardPreferencesSerializer,
    responses={
        200: DashboardPreferencesSerializer,
        400: OpenApiResponse(description=_("Invalid preference data")),
    }
)
@api_view(['PUT', 'PATCH'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([IsAuthenticated])
def update_preferences(request):
    """
    Update dashboard preferences
    PUT/PATCH /api/accounts/preferences/
    """
    profile = CustomerProfile.get_or_create_for_user(request.user)
    serializer = DashboardPreferencesSerializer(
        profile,
        data=request.data,
        partial=request.method == 'PATCH'
    )

    if serializer.is_valid():
        serializer.save()

        return Response({
            'success': True,
            'message': _('Preferences updated successfully.'),
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    return Response({
        'success': False,
        'message': _('Preferences update failed.'),
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Accounts'],
    summary=_("Refresh customer metrics"),
    description=_("Recalculate and update customer metrics including order count, total spent, lifetime value, etc."),
    request=None,
    responses={
        200: OpenApiResponse(
            description=_("Metrics refreshed successfully")
        ),
    }
)
@api_view(['POST'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([IsAuthenticated])
def refresh_metrics(request):
    """
    Refresh customer metrics
    POST /api/accounts/refresh-metrics/
    """
    profile = CustomerProfile.get_or_create_for_user(request.user)
    metrics = profile.refresh_metrics()

    # Return updated profile
    serializer = CustomerProfileSerializer(profile)

    return Response({
        'success': True,
        'message': _('Metrics refreshed successfully.'),
        'data': serializer.data
    }, status=status.HTTP_200_OK)


# ============================================================================
# Notification Preferences Endpoints
# ============================================================================

@extend_schema_view(
    list=extend_schema(tags=['Accounts']),
    create=extend_schema(tags=['Accounts']),
    retrieve=extend_schema(tags=['Accounts']),
    update=extend_schema(tags=['Accounts']),
    partial_update=extend_schema(tags=['Accounts']),
    destroy=extend_schema(tags=['Accounts']),
    set_default=extend_schema(tags=['Accounts'], summary=_("Set address as default")),
)
class AddressViewSet(HeadlessAPIMixin, viewsets.ModelViewSet):
    """
    ViewSet for address management

    list: GET /api/accounts/addresses/
    create: POST /api/accounts/addresses/
    retrieve: GET /api/accounts/addresses/{id}/
    update: PUT /api/accounts/addresses/{id}/
    partial_update: PATCH /api/accounts/addresses/{id}/
    destroy: DELETE /api/accounts/addresses/{id}/
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Use different serializers for list vs detail"""
        if self.action == 'list':
            return AddressListSerializer
        return AddressSerializer

    def get_queryset(self):
        """Return only current user's addresses"""
        return Address.objects.filter(user=self.request.user).order_by('-is_default', '-created_at')

    def create(self, request, *args, **kwargs):
        """Create new address"""
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'success': True,
                'message': _('Address created successfully.'),
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'success': False,
            'message': _('Address creation failed.'),
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """Update address"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'success': True,
                'message': _('Address updated successfully.'),
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'message': _('Address update failed.'),
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Delete address"""
        instance = self.get_object()
        instance.delete()

        return Response({
            'success': True,
            'message': _('Address deleted successfully.')
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """
        Set address as default
        POST /api/accounts/addresses/{id}/set-default/
        """
        address = self.get_object()
        address.is_default = True
        address.save()

        serializer = self.get_serializer(address)

        return Response({
            'success': True,
            'message': _('Default address updated.'),
            'data': serializer.data
        }, status=status.HTTP_200_OK)


# Social Authentication Views

@extend_schema(
    tags=['Accounts'],
    summary=_("List available social login providers"),
    description=_("Get list of enabled and configured OAuth social authentication providers (Google, Facebook, etc.) with their login URLs."),
    responses={
        200: OpenApiResponse(
            description=_("List of available social providers"),
            response={
                "providers": [
                    {
                        "provider": "google",
                        "display_name": "Google",
                        "login_url": "/accounts/google/login/"
                    }
                ]
            }
        ),
    }
)
@api_view(['GET'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def available_social_providers(request):
    """
    Returns list of enabled and configured OAuth providers

    GET /api/accounts/api/social/providers/

    Response:
    {
        "providers": [
            {
                "provider": "google",
                "display_name": "Google",
                "login_url": "/accounts/google/login/"
            },
            ...
        ]
    }
    """
    from .models import OAuthProviderSettings

    providers = OAuthProviderSettings.objects.filter(
        enabled=True,
        is_configured=True
    ).order_by('button_order')

    provider_list = []
    for provider_setting in providers:
        provider_list.append({
            'provider': provider_setting.provider,
            'display_name': provider_setting.display_name,
            'login_url': f'/{provider_setting.provider}/login/',
        })

    return Response({
        'success': True,
        'providers': provider_list
    }, status=status.HTTP_200_OK)


# Guest Account Conversion Endpoints

@extend_schema(
    tags=['Accounts'],
    summary=_("Convert guest user to full account"),
    description=_("Convert an authenticated guest user to a full account by setting a password. Only works for guest users (username starts with 'guest_')."),
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'password': {'type': 'string', 'minLength': 8},
            },
            'required': ['password']
        }
    },
    responses={
        200: OpenApiResponse(
            description=_("Account created successfully"),
            response={'success': True, 'username': 'string', 'message': 'string'}
        ),
        400: OpenApiResponse(description=_("Invalid request or password")),
        401: OpenApiResponse(description=_("Not authenticated or not a guest user")),
    }
)
@api_view(['POST'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def convert_guest_to_account(request):
    """
    Convert guest user to full account (post-purchase)

    POST /api/accounts/convert-guest/

    Payload:
    {
        "password": "newpassword123"
    }
    """
    from accounts.services.account_creation_service import AccountCreationService

    user = request.user

    if not user.is_authenticated:
        return Response(
            {'success': False, 'error': 'Not authenticated'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.username.startswith('guest_'):
        return Response(
            {'success': False, 'error': 'User already has a full account'},
            status=status.HTTP_400_BAD_REQUEST
        )

    password = request.data.get('password')
    if not password:
        return Response(
            {'success': False, 'error': 'Password required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validate password length
    if len(password) < 8:
        return Response(
            {'success': False, 'error': 'Password must be at least 8 characters'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Convert guest to full account
    success, message = AccountCreationService.convert_guest_to_full_account(
        user=user,
        password=password,
        send_confirmation_email=True
    )

    if success:
        # Re-login user with new credentials (update session)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return Response({
            'success': True,
            'username': user.username,
            'email': user.email,
            'message': message
        }, status=status.HTTP_200_OK)

    return Response(
        {'success': False, 'error': message},
        status=status.HTTP_400_BAD_REQUEST
    )


@extend_schema(
    tags=['Accounts'],
    summary=_("Get account creation context"),
    description=_("Get context for account creation UI including custom message and available social auth providers."),
    responses={
        200: OpenApiResponse(
            description=_("Account creation context"),
            response={
                'account_creation_message': 'string',
                'show_social_auth': 'boolean',
                'social_providers': 'array',
                'prefill_email': 'string',
                'prefill_first_name': 'string',
                'prefill_last_name': 'string',
            }
        ),
    }
)
@api_view(['GET'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def account_creation_context(request):
    """
    Get context for account creation UI (message, social providers)

    GET /api/accounts/creation-context/
    """
    from accounts.services.account_creation_service import AccountCreationService

    context = AccountCreationService.get_account_creation_context(
        user=request.user if request.user.is_authenticated else None
    )

    return Response({
        'success': True,
        **context
    }, status=status.HTTP_200_OK)


# Communication Preference API Views

@extend_schema(
    tags=['Accounts'],
    summary=_("Get communication preferences"),
    description=_(
        "Retrieve customer's communication preferences including email, SMS, "
        "and app-specific settings (blog, loyalty, referrals, affiliate). "
        "Returns preferences grouped by category for easier UI consumption. "
        "Requires authentication."
    ),
    responses={
        200: CommunicationPreferenceSerializer,
        404: OpenApiResponse(description=_("Preferences not found - will be auto-created")),
    }
)
@api_view(['GET'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([IsAuthenticated])
def get_communication_preferences(request):
    """
    Get customer's communication preferences.

    GET /api/accounts/communication-preferences/

    Returns comprehensive preference data including:
    - Email channel settings (enabled, transactional, marketing, verified)
    - SMS channel settings (enabled, transactional, marketing, verified)
    - App-specific preferences (blog, loyalty, referrals, affiliate)
    - Preferences grouped by category for UI
    - Available frequency options
    """
    from accounts.services.preference_service import PreferenceService

    prefs, created = PreferenceService.get_or_create_for_user(request.user)
    serializer = CommunicationPreferenceSerializer(prefs)

    return Response({
        'success': True,
        'data': serializer.data
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Accounts'],
    summary=_("Update single preference"),
    description=_(
        "Update a single communication preference (granular control). "
        "Allows enabling/disabling specific message types with optional frequency settings. "
        "Transactional messages cannot be disabled. "
        "Marketing messages require email verification. "
        "Changes are tracked for GDPR compliance. "
        "Requires authentication."
    ),
    request=PreferenceUpdateSerializer,
    responses={
        200: OpenApiResponse(
            description=_("Preference updated successfully"),
            response={'success': 'boolean', 'message': 'string'}
        ),
        400: OpenApiResponse(
            description=_("Invalid request or cannot disable locked preference"),
            response={'success': 'boolean', 'error': 'string'}
        ),
    }
)
@api_view(['POST'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([IsAuthenticated])
def update_communication_preference(request):
    """
    Update a single communication preference.

    POST /api/accounts/communication-preferences/update/

    Request body:
    {
        "channel": "email",  // or "sms"
        "message_type": "loyalty_points_earned",
        "enabled": true,
        "frequency": "immediate"  // optional: immediate, daily, weekly, monthly
    }

    Security:
    - Transactional messages cannot be disabled (GDPR legitimate interest)
    - Changes tracked with IP and user agent for audit trail
    - Cache invalidated automatically

    Validation:
    - message_type must be valid (see constants.py for taxonomy)
    - frequency only applies to digest-capable types
    """
    from accounts.services.preference_service import PreferenceService

    serializer = PreferenceUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # Get client IP for audit trail
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')

    result = PreferenceService.update_preference(
        user=request.user,
        channel=serializer.validated_data['channel'],
        message_type=serializer.validated_data['message_type'],
        enabled=serializer.validated_data['enabled'],
        frequency=serializer.validated_data.get('frequency'),
        ip_address=ip_address,
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
    )

    if result['success']:
        return Response({
            'success': True,
            'message': _('Preference updated successfully.')
        }, status=status.HTTP_200_OK)

    return Response({
        'success': False,
        'error': result.get('error')
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Accounts'],
    summary=_("Bulk update preferences"),
    description=_(
        "Update multiple communication preferences in a single request. "
        "More efficient than individual updates when changing multiple settings. "
        "All updates are atomic - if any fails, none are applied. "
        "Requires authentication."
    ),
    request=BulkPreferenceUpdateSerializer,
    responses={
        200: OpenApiResponse(
            description=_("All preferences updated successfully"),
            response={'success': 'boolean', 'message': 'string'}
        ),
        400: OpenApiResponse(
            description=_("One or more updates failed"),
            response={'success': 'boolean', 'errors': 'array'}
        ),
    }
)
@api_view(['POST'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([IsAuthenticated])
def bulk_update_communication_preferences(request):
    """
    Update multiple communication preferences at once.

    POST /api/accounts/communication-preferences/bulk-update/

    Request body:
    {
        "updates": [
            {
                "channel": "email",
                "message_type": "loyalty_points_earned",
                "enabled": true,
                "frequency": "immediate"
            },
            {
                "channel": "email",
                "message_type": "newsletter",
                "enabled": false
            }
        ]
    }

    Performance:
    - More efficient than multiple individual requests
    - Single cache invalidation after all updates
    - Atomic operation - all or nothing

    Use cases:
    - Initial preference setup
    - Importing preferences from another system
    - "Unsubscribe from all" functionality
    """
    from accounts.services.preference_service import PreferenceService

    serializer = BulkPreferenceUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    result = PreferenceService.bulk_update_preferences(
        user=request.user,
        updates=serializer.validated_data['updates']
    )

    if result['success']:
        return Response({
            'success': True,
            'message': _('Preferences updated successfully.')
        }, status=status.HTTP_200_OK)

    return Response({
        'success': False,
        'errors': result.get('errors')
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Accounts'],
    summary=_("Unsubscribe from all communications"),
    description=_(
        "Unsubscribe from all non-transactional communications (email and SMS). "
        "Transactional messages (order confirmations, shipping updates) remain enabled. "
        "This action is logged for GDPR compliance. "
        "Optional reason can be provided for analytics. "
        "Requires authentication."
    ),
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'reason': {
                    'type': 'string',
                    'description': _('Optional reason for unsubscribing')
                }
            }
        }
    },
    responses={
        200: OpenApiResponse(
            description=_("Successfully unsubscribed from all communications"),
            response={'success': 'boolean', 'message': 'string'}
        ),
        400: OpenApiResponse(description=_("Unsubscribe failed")),
    }
)
@api_view(['POST'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([IsAuthenticated])
def unsubscribe_all_communications(request):
    """
    Unsubscribe from all non-transactional communications.

    POST /api/accounts/communication-preferences/unsubscribe-all/

    Request body (optional):
    {
        "reason": "Too many emails"
    }

    What this does:
    - Disables email_marketing
    - Disables sms_marketing
    - Disables all app-specific preferences (blog, loyalty, referrals, affiliate)
    - Keeps transactional emails enabled (required for account management)
    - Logs the action with timestamp and reason

    Compliance:
    - GDPR right to withdraw consent
    - CAN-SPAM opt-out requirement
    - Audit trail maintained
    """
    from accounts.services.preference_service import PreferenceService

    reason = request.data.get('reason', '')
    result = PreferenceService.unsubscribe_all(request.user, reason=reason)

    if result['success']:
        return Response({
            'success': True,
            'message': _('You have been unsubscribed from all marketing communications.')
        }, status=status.HTTP_200_OK)

    return Response({
        'success': False,
        'error': result.get('error')
    }, status=status.HTTP_400_BAD_REQUEST)


# ENHANCEMENT 3: Export Preferences (GDPR Right to Access)

@extend_schema(
    summary=_("Export Communication Preferences"),
    description=_("Export all preference data including change history for GDPR Article 15 (Right to Access)"),
    tags=["Communication Preferences"],
    responses={
        200: {
            "type": "object",
            "properties": {
                "user": {"type": "object"},
                "preferences": {"type": "object"},
                "consent": {"type": "object"},
                "verification": {"type": "object"},
                "change_history": {"type": "array"},
                "export_metadata": {"type": "object"},
            }
        },
        403: {"description": AUTH_REQUIRED},
    }
)
@api_view(['GET'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([IsAuthenticated])
def export_preferences(request):
    """Export user's complete preference data (GDPR Article 15)."""
    from accounts.services.preference_export_service import PreferenceExportService

    data = PreferenceExportService.export_user_preferences(request.user)

    return Response(data, status=status.HTTP_200_OK)


# ENHANCEMENT 2: SMS Double Opt-In

@extend_schema(
    summary=_("Send SMS Verification Code"),
    description=_("Send a 6-digit OTP code via SMS for TCPA-compliant double opt-in verification"),
    tags=["SMS Verification"],
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'phone_number': {
                    'type': 'string',
                    'description': _('Phone number in E.164 format (e.g., +1234567890)')
                }
            },
            'required': ['phone_number']
        }
    },
    responses={
        200: {
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'expires_at': {'type': 'string', 'format': 'date-time'},
                'phone_last_4': {'type': 'string'}
            }
        },
        400: {'description': _('Invalid request or rate limited')},
    }
)
@api_view(['POST'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([IsAuthenticated])
def send_sms_verification(request):
    """Send SMS verification code to user's phone number."""
    from accounts.services.sms_verification_service import SMSVerificationService

    phone_number = request.data.get('phone_number')

    if not phone_number:
        return Response({
            'success': False,
            'error': 'phone_number is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    result = SMSVerificationService.send_verification_code(
        user=request.user,
        phone_number=phone_number
    )

    if result['success']:
        return Response(result, status=status.HTTP_200_OK)

    return Response(result, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary=_("Verify SMS Code"),
    description=_("Verify the 6-digit OTP code sent via SMS. Uses constant-time comparison for security."),
    tags=["SMS Verification"],
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'code': {
                    'type': 'string',
                    'description': _('6-digit verification code')
                },
                'phone_number': {
                    'type': 'string',
                    'description': _('Phone number being verified')
                }
            },
            'required': ['code', 'phone_number']
        }
    },
    responses={
        200: {
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'message': {'type': 'string'}
            }
        },
        400: {
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'error': {'type': 'string'},
                'attempts_remaining': {'type': 'integer'}
            }
        },
    }
)
@api_view(['POST'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([IsAuthenticated])
def verify_sms_code(request):
    """Verify SMS verification code."""
    from accounts.services.sms_verification_service import SMSVerificationService

    code = request.data.get('code')
    phone_number = request.data.get('phone_number')

    if not code or not phone_number:
        return Response({
            'success': False,
            'error': 'code and phone_number are required'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Extract IP and user agent for audit trail
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip_address:
        ip_address = ip_address.split(',')[0].strip()
    else:
        ip_address = request.META.get('REMOTE_ADDR')

    user_agent = request.META.get('HTTP_USER_AGENT', '')

    result = SMSVerificationService.verify_code(
        user=request.user,
        code=code,
        phone_number=phone_number,
        ip_address=ip_address,
        user_agent=user_agent
    )

    if result['success']:
        return Response(result, status=status.HTTP_200_OK)

    return Response(result, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary=_("Resend SMS Verification Code"),
    description=_("Request a new verification code. Clears the old code before sending new one."),
    tags=["SMS Verification"],
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'phone_number': {
                    'type': 'string',
                    'description': _('Phone number to send code to')
                }
            },
            'required': ['phone_number']
        }
    },
    responses={
        200: {
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'expires_at': {'type': 'string', 'format': 'date-time'},
                'phone_last_4': {'type': 'string'}
            }
        },
        400: {'description': _('Invalid request or rate limited')},
    }
)
@api_view(['POST'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([IsAuthenticated])
def resend_sms_verification(request):
    """Resend SMS verification code."""
    from accounts.services.sms_verification_service import SMSVerificationService

    phone_number = request.data.get('phone_number')

    if not phone_number:
        return Response({
            'success': False,
            'error': 'phone_number is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    result = SMSVerificationService.resend_code(
        user=request.user,
        phone_number=phone_number
    )

    if result['success']:
        return Response(result, status=status.HTTP_200_OK)

    return Response(result, status=status.HTTP_400_BAD_REQUEST)
