"""
Serializers for accounts app API endpoints
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_field
from .models import CustomerProfile
from orders.models import Address

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirm')

    def validate_email(self, value):
        """Check if email is already registered"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("A user with this email already exists."))
        return value

    def validate_username(self, value):
        """Check if username is already taken"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(_("A user with this username already exists."))
        return value

    def validate(self, attrs):
        """Validate that passwords match"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': _("Passwords do not match.")
            })
        return attrs

    def create(self, validated_data):
        """Create user and profile"""
        # Remove password_confirm as it's not needed for user creation
        validated_data.pop('password_confirm')

        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )

        # Create customer profile
        CustomerProfile.get_or_create_for_user(user)

        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate credentials"""
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )

            if not user:
                raise serializers.ValidationError(
                    _("Unable to log in with provided credentials."),
                    code='authorization'
                )

            if not user.is_active:
                raise serializers.ValidationError(
                    _("User account is disabled."),
                    code='authorization'
                )

        else:
            raise serializers.ValidationError(
                _("Must include 'username' and 'password'."),
                code='authorization'
            )

        attrs['user'] = user
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    """Serializer for password reset request"""
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """Validate that email exists"""
        if not User.objects.filter(email=value, is_active=True).exists():
            # Don't reveal if email exists or not for security
            pass
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for password reset confirmation"""
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """Validate that passwords match"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': _("Passwords do not match.")
            })
        return attrs


class CustomerProfileSerializer(serializers.ModelSerializer):
    """Serializer for customer profile"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    full_name = serializers.SerializerMethodField()

    # Communication preferences (read-only, from CommunicationPreference model)
    email_marketing = serializers.SerializerMethodField()
    email_transactional = serializers.SerializerMethodField()
    newsletter_enabled = serializers.SerializerMethodField()

    # Analytics properties (read-only)
    lifetime_value = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total_spent = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total_orders = serializers.IntegerField(read_only=True)
    completed_orders_count = serializers.IntegerField(read_only=True)
    average_order_value = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    days_since_last_order = serializers.IntegerField(read_only=True, allow_null=True)
    is_vip_customer = serializers.BooleanField(read_only=True)
    is_at_risk = serializers.BooleanField(read_only=True)

    class Meta:
        model = CustomerProfile
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'date_of_birth', 'dashboard_layout',
            'show_order_history', 'show_wishlist', 'show_recent_products', 'show_recommendations',
            'email_marketing', 'email_transactional', 'newsletter_enabled',
            'lifetime_value', 'total_spent', 'total_orders', 'completed_orders_count',
            'average_order_value', 'days_since_last_order', 'is_vip_customer', 'is_at_risk',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    @extend_schema_field(serializers.CharField())
    def get_full_name(self, obj):
        """Get user's full name"""
        return obj.user.get_full_name()

    @extend_schema_field(serializers.BooleanField())
    def get_email_marketing(self, obj):
        try:
            return obj.user.communication_preferences.email_marketing
        except Exception:
            return False

    @extend_schema_field(serializers.BooleanField())
    def get_email_transactional(self, obj):
        try:
            return obj.user.communication_preferences.email_transactional
        except Exception:
            return True

    @extend_schema_field(serializers.BooleanField())
    def get_newsletter_enabled(self, obj):
        try:
            prefs = obj.user.communication_preferences
            return prefs.app_preferences.get('blog', {}).get('enabled', False)
        except Exception:
            return False

    def update(self, instance, validated_data):
        """Update profile and user fields"""
        # Update user fields if present
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.save()

        # Update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class CustomerProfileUpdateSerializer(serializers.ModelSerializer):
    """Simplified serializer for profile updates"""
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = CustomerProfile
        fields = (
            'first_name', 'last_name', 'phone', 'date_of_birth',
        )

    def update(self, instance, validated_data):
        """Update profile and user fields"""
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class DashboardPreferencesSerializer(serializers.ModelSerializer):
    """Serializer for dashboard display preferences"""
    class Meta:
        model = CustomerProfile
        fields = (
            'dashboard_layout', 'show_order_history', 'show_wishlist',
            'show_recent_products', 'show_recommendations'
        )


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for customer addresses"""
    is_default = serializers.BooleanField(default=False)

    class Meta:
        model = Address
        fields = (
            'id', 'address_type', 'name', 'company', 'address1', 'address2',
            'city', 'state', 'postal_code', 'country', 'phone',
            'is_default', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        """Create address for current user"""
        user = self.context['request'].user
        address = Address.objects.create(user=user, **validated_data)
        return address


class AddressListSerializer(serializers.ModelSerializer):
    """Simplified serializer for address listing"""
    class Meta:
        model = Address
        fields = (
            'id', 'address_type', 'name', 'address1', 'address2',
            'city', 'state', 'postal_code', 'country', 'is_default'
        )


# Communication Preference Serializers

class CommunicationPreferenceSerializer(serializers.ModelSerializer):
    """
    Comprehensive communication preference serializer.

    Returns all preference data including email, SMS, and app-specific settings.
    Includes grouped categories for easier UI consumption.
    """

    email_categories = serializers.SerializerMethodField(
        help_text=_("Preferences grouped by category (transactional, marketing, apps)")
    )
    available_frequencies = serializers.SerializerMethodField(
        help_text=_("Available frequency options for digest preferences")
    )

    class Meta:
        from accounts.models import CommunicationPreference
        model = CommunicationPreference
        fields = (
            'email_enabled',
            'sms_enabled',
            'email_transactional',
            'email_marketing',
            'email_verified',
            'email_verified_at',
            'sms_transactional',
            'sms_marketing',
            'sms_verified',
            'sms_verified_at',
            'app_preferences',
            'email_categories',
            'available_frequencies',
            'language_code',
            'updated_at',
        )
        read_only_fields = (
            'email_verified',
            'email_verified_at',
            'sms_verified',
            'sms_verified_at',
            'email_categories',
            'available_frequencies',
            'updated_at',
        )

    def get_email_categories(self, obj):
        """Group preferences by category for UI display"""
        from accounts.constants import TRANSACTIONAL_EMAIL_TYPES, MARKETING_EMAIL_TYPES

        return {
            'transactional': {
                'locked': True,  # Not user-controllable
                'enabled': obj.email_transactional,
                'types': TRANSACTIONAL_EMAIL_TYPES,
            },
            'marketing': {
                'locked': False,
                'enabled': obj.email_marketing,
                'verified': obj.email_verified,
                'types': MARKETING_EMAIL_TYPES,
            },
            'blog': obj.app_preferences.get('blog', {}),
            'loyalty': obj.app_preferences.get('loyalty', {}),
            'referrals': obj.app_preferences.get('referrals', {}),
            'affiliate': obj.app_preferences.get('affiliate', {}),
        }

    def get_available_frequencies(self, obj):
        """Return available frequency options"""
        return {
            'immediate': str(_('Immediately')),
            'daily': str(_('Daily Digest')),
            'weekly': str(_('Weekly Digest')),
            'monthly': str(_('Monthly Digest')),
            '3_days': str(_('3 Days Before')),
            '7_days': str(_('7 Days Before')),
        }


class PreferenceUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating a single preference.

    Used for granular updates to specific message type preferences.
    """
    channel = serializers.ChoiceField(
        choices=['email', 'sms'],
        help_text=_("Communication channel (email or sms)")
    )
    message_type = serializers.CharField(
        max_length=100,
        help_text=_("Message type identifier (e.g., 'loyalty_points_earned', 'newsletter')")
    )
    enabled = serializers.BooleanField(
        help_text=_("Whether to enable or disable this message type")
    )
    frequency = serializers.CharField(
        max_length=20,
        required=False,
        allow_null=True,
        help_text=_("Optional frequency setting (immediate, daily, weekly, monthly)")
    )


class BulkPreferenceUpdateSerializer(serializers.Serializer):
    """
    Serializer for bulk preference updates.

    Allows updating multiple preferences in a single request.
    """
    updates = serializers.ListField(
        child=PreferenceUpdateSerializer(),
        allow_empty=False,
        help_text=_("List of preference updates to apply")
    )
