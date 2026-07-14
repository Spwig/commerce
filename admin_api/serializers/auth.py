"""
Admin API Authentication Serializers

Serializers for login, logout, token refresh, and profile endpoints.
"""

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class StaffLoginSerializer(serializers.Serializer):
    """
    Serializer for staff login requests.

    Accepts either 'email' or 'username' field for the login identifier.
    """

    email = serializers.EmailField(required=False, help_text=_("Staff user email address"))
    username = serializers.CharField(
        required=False, help_text=_("Staff username or email (alternative to email field)")
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
        help_text=_("Account password"),
    )
    device_id = serializers.CharField(
        required=True, max_length=255, help_text=_("Unique device identifier")
    )
    device_name = serializers.CharField(
        required=True,
        max_length=255,
        help_text=_('Human-readable device name (e.g., "iPhone 15 Pro")'),
    )

    def validate(self, attrs):
        # Accept either email or username field
        email = attrs.get("email") or attrs.get("username")
        password = attrs.get("password")

        if email and password:
            # Use email as username for authentication
            user = authenticate(
                request=self.context.get("request"), username=email, password=password
            )

            if not user:
                raise serializers.ValidationError(
                    _("Invalid email or password."), code="invalid_credentials"
                )

            if not user.is_active:
                raise serializers.ValidationError(
                    _("User account is disabled."), code="user_inactive"
                )

            if not user.is_staff:
                raise serializers.ValidationError(_("Staff access required."), code="not_staff")

            attrs["user"] = user
        else:
            raise serializers.ValidationError(
                _("Email and password are required."), code="missing_credentials"
            )

        return attrs


class TokenResponseSerializer(serializers.Serializer):
    """
    Serializer for token response data.
    """

    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    token_type = serializers.CharField(read_only=True, default="Bearer")
    expires_in = serializers.IntegerField(
        read_only=True, help_text=_("Access token expiry time in seconds")
    )


class LoginResponseSerializer(serializers.Serializer):
    """
    Serializer for login response.
    """

    success = serializers.BooleanField(read_only=True)
    message = serializers.CharField(read_only=True)
    data = serializers.DictField(read_only=True)


class RefreshTokenSerializer(serializers.Serializer):
    """
    Serializer for token refresh requests.

    device_id is optional - if not provided, it will be extracted from the token.
    """

    refresh_token = serializers.CharField(required=True, help_text=_("The refresh token to use"))
    device_id = serializers.CharField(
        required=False,
        max_length=255,
        help_text=_("Device identifier (optional - extracted from token if not provided)"),
    )


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for logout requests.
    """

    device_id = serializers.CharField(
        required=False,
        max_length=255,
        help_text=_("Device identifier (if omitted, uses current device)"),
    )
    logout_all = serializers.BooleanField(
        required=False, default=False, help_text=_("Logout from all devices")
    )


class StaffProfileSerializer(serializers.Serializer):
    """
    Serializer for staff user profile.

    Includes groups (roles) and resolved permission categories
    for the mobile app to determine UI feature access.
    """

    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    full_name = serializers.SerializerMethodField()
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_owner = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    groups = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        """Get user's full name or email if name not set."""
        full_name = obj.get_full_name()
        return full_name if full_name else obj.email

    def get_is_owner(self, obj):
        """Check if user is the store owner (superuser)."""
        return obj.is_superuser

    def get_groups(self, obj):
        """Get the user's assigned roles (StaffRole objects)."""
        from staff_roles.services import get_user_roles

        roles = get_user_roles(obj)
        return [
            {
                "id": role.id,
                "name": role.display_name,
            }
            for role in roles
        ]

    def get_permissions(self, obj):
        """
        Get merged permission categories across all roles.

        Returns a dict like {"catalog": "full", "orders": "view", ...}
        Superusers get 'full' on all categories.
        """
        if obj.is_superuser:
            from staff_roles.categories import PERMISSION_CATEGORIES

            return dict.fromkeys(PERMISSION_CATEGORIES, "full")

        from staff_roles.services import get_user_roles

        merged = {}
        for role in get_user_roles(obj):
            for category_key, level in role.permission_categories.items():
                current = merged.get(category_key, "none")
                if level == "full" or (level == "view" and current == "none"):
                    merged[category_key] = level
        return merged


class ErrorResponseSerializer(serializers.Serializer):
    """
    Serializer for error responses.
    """

    success = serializers.BooleanField(default=False)
    error = serializers.DictField()


class SuccessResponseSerializer(serializers.Serializer):
    """
    Serializer for success responses.
    """

    success = serializers.BooleanField(default=True)
    message = serializers.CharField()


class AdminDataResponseSerializer(serializers.Serializer):
    """
    Generic serializer for admin API data responses.

    Used for endpoints that return {success: true, data: {...}}.
    """

    success = serializers.BooleanField(default=True)
    data = serializers.DictField(help_text=_("Response payload (structure varies by endpoint)"))
    error = serializers.CharField(allow_null=True, default=None, help_text=_("Null on success"))


class BulkOperationResponseSerializer(serializers.Serializer):
    """
    Serializer for bulk operation responses.

    Used for all bulk update endpoints that process items independently.
    """

    success = serializers.BooleanField(help_text=_("True if at least one item succeeded"))
    data = serializers.DictField(
        help_text=_("Contains total, succeeded, failed counts and per-item results array")
    )
    error = serializers.CharField(allow_null=True, default=None, help_text=_("Null on success"))


# ============================================================================
# Two-Factor Authentication Serializers
# ============================================================================


class TwoFactorVerifySerializer(serializers.Serializer):
    """
    Serializer for 2FA verification requests.

    Accepts either a TOTP code or a recovery code.
    Supports alternative field names for compatibility.
    """

    pending_token = serializers.CharField(
        required=True, help_text=_("The 2FA pending token received from login")
    )
    code = serializers.CharField(
        required=True,
        min_length=6,
        max_length=20,
        help_text=_("TOTP code (6 digits) or recovery code"),
    )
    device_id = serializers.CharField(
        required=True, max_length=255, help_text=_("Device identifier (must match login request)")
    )
    trust_device = serializers.BooleanField(
        required=False,
        default=False,
        help_text=_("Remember this device for 30 days (skip 2FA on future logins)"),
    )

    # Map alternative field names to canonical names
    FIELD_ALIASES = {
        "otp_code": "code",
        "totp_code": "code",
        "verification_code": "code",
        "otp": "code",
        "token": "pending_token",
        "2fa_token": "pending_token",
        "deviceId": "device_id",
        "deviceID": "device_id",
        "trustDevice": "trust_device",
        "remember_device": "trust_device",
        "rememberDevice": "trust_device",
    }

    def to_internal_value(self, data):
        """Handle alternative field names before validation."""
        # Create a mutable copy
        data = data.copy() if hasattr(data, "copy") else dict(data)

        # Map alternative field names to canonical names
        for alias, canonical in self.FIELD_ALIASES.items():
            if alias in data and canonical not in data:
                data[canonical] = data.pop(alias)

        return super().to_internal_value(data)

    def validate_code(self, value):
        """Clean up the code - remove spaces and dashes."""
        return value.replace(" ", "").replace("-", "")


class TwoFactorRequiredResponseSerializer(serializers.Serializer):
    """
    Serializer for 2FA required response.

    Returned when login credentials are valid but 2FA verification is needed.
    """

    success = serializers.BooleanField(default=True, read_only=True)
    requires_2fa = serializers.BooleanField(default=True, read_only=True)
    message = serializers.CharField(read_only=True)
    pending_token = serializers.CharField(
        read_only=True, help_text=_("Token to use for 2FA verification")
    )
    expires_in = serializers.IntegerField(
        read_only=True, help_text=_("Seconds until pending token expires")
    )


class TwoFactorStatusSerializer(serializers.Serializer):
    """
    Serializer for 2FA status information.
    """

    enabled = serializers.BooleanField(read_only=True)
    has_totp = serializers.BooleanField(read_only=True)
    has_recovery_codes = serializers.BooleanField(read_only=True)


# ============================================================================
# Password Reset Serializers
# ============================================================================


class StaffPasswordResetRequestSerializer(serializers.Serializer):
    """Serializer for staff password reset request."""

    email = serializers.EmailField(required=True, help_text=_("Staff user email address"))


class StaffPasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for staff password reset confirmation."""

    uid = serializers.CharField(
        required=True, help_text=_("Base64-encoded user ID from the reset link")
    )
    token = serializers.CharField(
        required=True, help_text=_("Password reset token from the reset link")
    )
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
        help_text=_("New password"),
    )
    new_password_confirm = serializers.CharField(
        required=True, style={"input_type": "password"}, help_text=_("Confirm new password")
    )

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError(
                {"new_password_confirm": _("Passwords do not match.")}
            )
        return attrs
