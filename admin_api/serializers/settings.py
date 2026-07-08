"""
Settings Serializers for Admin API

Serializers for app settings and device management.
"""
from rest_framework import serializers
from admin_api.models import DeviceRegistration


class DeviceRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for device registration."""

    class Meta:
        model = DeviceRegistration
        fields = [
            'device_id',
            'push_token',
            'platform',
            'notify_new_orders',
            'notify_low_stock',
            'notify_customer_messages',
        ]


class DeviceListSerializer(serializers.ModelSerializer):
    """Serializer for listing registered devices."""

    class Meta:
        model = DeviceRegistration
        fields = [
            'id',
            'device_id',
            'platform',
            'is_active',
            'notify_new_orders',
            'notify_low_stock',
            'notify_customer_messages',
            'last_notification_at',
            'created_at',
        ]


class NotificationPreferencesSerializer(serializers.Serializer):
    """Serializer for notification preferences."""
    notify_new_orders = serializers.BooleanField(required=False)
    notify_low_stock = serializers.BooleanField(required=False)
    notify_customer_messages = serializers.BooleanField(required=False)


class UpdatePushTokenSerializer(serializers.Serializer):
    """Serializer for updating push token."""
    push_token = serializers.CharField(max_length=500)


class AppSettingsSerializer(serializers.Serializer):
    """Serializer for app settings response."""
    # User info
    user_id = serializers.IntegerField()
    email = serializers.EmailField()
    full_name = serializers.CharField()

    # Store info
    store_name = serializers.CharField()
    store_currency = serializers.CharField()
    store_timezone = serializers.CharField()

    # App settings
    language = serializers.CharField()

    # Notification preferences (for current device)
    notifications = NotificationPreferencesSerializer()


class LanguageUpdateSerializer(serializers.Serializer):
    """Serializer for updating preferred language."""
    language = serializers.CharField(max_length=10)

    def validate_language(self, value):
        """Validate language code."""
        from django.conf import settings
        valid_codes = [code for code, name in settings.LANGUAGES]
        if value not in valid_codes:
            raise serializers.ValidationError(f"Invalid language code. Valid: {valid_codes}")
        return value


class ActiveSessionSerializer(serializers.Serializer):
    """Serializer for active session info."""
    device_id = serializers.CharField()
    device_name = serializers.CharField()
    platform = serializers.CharField(allow_blank=True)
    is_current = serializers.BooleanField()
    last_used_at = serializers.DateTimeField(allow_null=True)
    last_used_ip = serializers.CharField(allow_null=True)
    created_at = serializers.DateTimeField()
