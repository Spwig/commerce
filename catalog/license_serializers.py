"""
DRF Serializers for License Key API

Provides serializers for license validation, activation, and management operations.
"""

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import (
    LicenseActivation,
    LicenseKey,
    LicensePool,
)


class LicenseActivationSerializer(serializers.ModelSerializer):
    """Serializer for license activation records"""

    class Meta:
        model = LicenseActivation
        fields = [
            "id",
            "device_name",
            "device_identifier",
            "ip_address",
            "device_info",
            "activated_at",
            "deactivated_at",
            "is_active",
        ]
        read_only_fields = ["id", "activated_at", "deactivated_at"]


class LicenseKeySerializer(serializers.ModelSerializer):
    """Serializer for license key information"""

    activations = LicenseActivationSerializer(many=True, read_only=True)
    remaining_activations = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()

    class Meta:
        model = LicenseKey
        fields = [
            "id",
            "key",
            "key_type",
            "status",
            "max_activations",
            "current_activations",
            "remaining_activations",
            "expires_at",
            "is_lifetime",
            "is_expired",
            "issued_at",
            "first_activated_at",
            "last_activated_at",
            "activations",
        ]
        read_only_fields = fields  # All fields are read-only for security

    def get_remaining_activations(self, obj):
        """Calculate remaining activation slots"""
        return max(0, obj.max_activations - obj.current_activations)

    def get_is_expired(self, obj):
        """Check if license is expired"""
        from django.utils import timezone

        if obj.is_lifetime or not obj.expires_at:
            return False
        return timezone.now() > obj.expires_at


class LicenseValidationRequestSerializer(serializers.Serializer):
    """Serializer for license validation requests"""

    key = serializers.CharField(
        max_length=255, required=True, help_text=_("License key to validate")
    )
    product_id = serializers.IntegerField(
        required=False, help_text=_("Optional product ID to validate key against")
    )


class LicenseValidationResponseSerializer(serializers.Serializer):
    """Serializer for license validation responses"""

    valid = serializers.BooleanField()
    message = serializers.CharField()
    license_info = LicenseKeySerializer(required=False, allow_null=True)
    errors = serializers.ListField(child=serializers.CharField(), required=False)


class LicenseActivationRequestSerializer(serializers.Serializer):
    """Serializer for license activation requests"""

    key = serializers.CharField(
        max_length=255, required=True, help_text=_("License key to activate")
    )
    device_fingerprint = serializers.CharField(
        max_length=255, required=True, help_text=_("Unique device identifier")
    )
    device_name = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        help_text=_("Human-readable device name (e.g., 'John's MacBook Pro')"),
    )
    device_info = serializers.JSONField(
        required=False, help_text=_("Additional device information (OS, version, etc.)")
    )


class LicenseActivationResponseSerializer(serializers.Serializer):
    """Serializer for license activation responses"""

    success = serializers.BooleanField()
    message = serializers.CharField()
    activation = LicenseActivationSerializer(required=False, allow_null=True)
    license_info = LicenseKeySerializer(required=False, allow_null=True)
    errors = serializers.ListField(child=serializers.CharField(), required=False)


class LicenseDeactivationRequestSerializer(serializers.Serializer):
    """Serializer for license deactivation requests"""

    key = serializers.CharField(max_length=255, required=True, help_text=_("License key"))
    device_fingerprint = serializers.CharField(
        max_length=255, required=True, help_text=_("Device fingerprint to deactivate")
    )


class LicenseDeactivationResponseSerializer(serializers.Serializer):
    """Serializer for license deactivation responses"""

    success = serializers.BooleanField()
    message = serializers.CharField()
    license_info = LicenseKeySerializer(required=False, allow_null=True)


class LicensePoolSerializer(serializers.ModelSerializer):
    """Serializer for license pools (admin use)"""

    product_name = serializers.CharField(source="product.name", read_only=True)
    progress = serializers.IntegerField(source="progress_percentage", read_only=True)
    available_count = serializers.IntegerField(source="available_keys_count", read_only=True)

    class Meta:
        model = LicensePool
        fields = [
            "id",
            "name",
            "description",
            "product",
            "product_name",
            "license_template",
            "total_keys",
            "keys_generated",
            "keys_distributed",
            "available_count",
            "progress",
            "status",
            "key_type",
            "max_activations",
            "expires_after_days",
            "pool_expires_at",
            "created_at",
            "created_by",
        ]
        read_only_fields = [
            "id",
            "keys_generated",
            "keys_distributed",
            "status",
            "created_at",
            "created_by",
        ]


class BulkGenerateRequestSerializer(serializers.Serializer):
    """Serializer for bulk license generation requests"""

    pool_id = serializers.IntegerField(
        required=True, help_text=_("License pool ID to generate keys for")
    )
    count = serializers.IntegerField(
        required=False,
        min_value=1,
        max_value=10000,
        help_text=_("Number of keys to generate (defaults to pool.total_keys)"),
    )


class BulkGenerateResponseSerializer(serializers.Serializer):
    """Serializer for bulk generation responses"""

    success = serializers.BooleanField()
    message = serializers.CharField()
    pool = LicensePoolSerializer(required=False, allow_null=True)
    keys_generated = serializers.IntegerField(required=False)
    task_id = serializers.CharField(
        required=False, help_text=_("Celery task ID for background generation (if async)")
    )


class LicenseInfoRequestSerializer(serializers.Serializer):
    """Serializer for license information requests"""

    key = serializers.CharField(
        max_length=255, required=True, help_text=_("License key to get information for")
    )
