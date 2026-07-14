"""
Shipping API Serializers
DRF serializers for shipping models
"""

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from shipping.models import (
    CarrierPreset,
    Location,
    ProviderAccount,
    Shipment,
    ShippingPromotion,
    ShippingRateTable,
    ShippingZone,
    TrackingEvent,
)


class CarrierPresetSerializer(serializers.ModelSerializer):
    """Serializer for CarrierPreset model"""

    class Meta:
        model = CarrierPreset
        fields = [
            "id",
            "name",
            "slug",
            "tracking_url_template",
            "logo",
            "is_active",
            "is_default",
            "is_system",
        ]
        read_only_fields = ["id", "is_system"]


class TrackingEventSerializer(serializers.ModelSerializer):
    """Serializer for TrackingEvent model - read-only"""

    class Meta:
        model = TrackingEvent
        fields = [
            "id",
            "occurred_at",
            "status",
            "location",
            "description",
            "created_at",
        ]
        read_only_fields = fields  # All fields are read-only


class ShipmentSerializer(serializers.ModelSerializer):
    """Serializer for Shipment model with computed fields"""

    # Computed fields
    tracking_url = serializers.SerializerMethodField()
    carrier_name = serializers.SerializerMethodField()
    provider_name = serializers.SerializerMethodField()
    is_manual = serializers.SerializerMethodField()
    is_api = serializers.SerializerMethodField()

    # Nested serializers
    tracking_events = TrackingEventSerializer(many=True, read_only=True)

    class Meta:
        model = Shipment
        fields = [
            "id",
            "order",
            "user",
            "status",
            "tracking_id",
            "tracking_url",
            "label_url",
            "packing_slip_url",  # Phase 6: Document Generation
            "commercial_invoice_url",
            "customs_form_url",
            "carrier_preset",
            "carrier_name",
            "provider_account",
            "provider_name",
            "origin_country",
            "dest_country",
            "service_level",
            "packages",
            "shipping_cost",
            "carrier_cost",
            "pricing_mode_used",
            "is_manual",
            "is_api",
            "tracking_events",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "tracking_url",
            "carrier_name",
            "provider_name",
            "is_manual",
            "is_api",
            "tracking_events",
            "created_at",
            "updated_at",
        ]

    @extend_schema_field(serializers.URLField(allow_null=True))
    def get_tracking_url(self, obj):
        """Get tracking URL using model method"""
        return obj.get_tracking_url()

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_carrier_name(self, obj):
        """Get carrier name"""
        if obj.carrier_preset:
            return obj.carrier_preset.name
        return None

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_provider_name(self, obj):
        """Get provider name"""
        if obj.provider_account:
            return obj.provider_account.display_name or obj.provider_account.component.name
        return None

    @extend_schema_field(serializers.BooleanField())
    def get_is_manual(self, obj):
        """Check if manual shipment"""
        return obj.is_manual

    @extend_schema_field(serializers.BooleanField())
    def get_is_api(self, obj):
        """Check if API shipment"""
        return obj.is_api


class ShipmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating shipments (simplified fields)"""

    class Meta:
        model = Shipment
        fields = [
            "order",
            "carrier_preset",
            "provider_account",
            "tracking_id",
            "origin_country",
            "dest_country",
            "service_level",
            "packages",
        ]

    def validate(self, data):
        """Validate shipment data"""
        # Must have either carrier_preset or provider_account
        if not data.get("carrier_preset") and not data.get("provider_account"):
            raise serializers.ValidationError(
                "Either carrier_preset or provider_account must be provided."
            )

        # If provider_account, tracking_id is optional (will be generated)
        # If carrier_preset only, tracking_id is required
        if data.get("carrier_preset") and not data.get("provider_account"):
            if not data.get("tracking_id"):
                raise serializers.ValidationError(
                    "tracking_id is required when using manual carrier preset."
                )

        return data

    def create(self, validated_data):
        """Create shipment with user from request"""
        # Set user from request context
        validated_data["user"] = self.context["request"].user

        # Set initial status
        if validated_data.get("tracking_id"):
            validated_data["status"] = "in_transit"
        else:
            validated_data["status"] = "created"

        shipment = super().create(validated_data)
        return shipment

    def to_representation(self, instance):
        """Use full serializer for response"""
        return ShipmentSerializer(instance, context=self.context).data


class ProviderAccountSerializer(serializers.ModelSerializer):
    """Serializer for ProviderAccount - credentials are redacted"""

    component_name = serializers.CharField(source="component.name", read_only=True)
    provider_type = serializers.CharField(source="component.slug", read_only=True)

    class Meta:
        model = ProviderAccount
        fields = [
            "id",
            "component",
            "component_name",
            "provider_type",
            "user",
            "display_name",
            "is_active",
            "is_default",
            "connection_status",
            "last_tested_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "component_name",
            "provider_type",
            "connection_status",
            "last_tested_at",
            "created_at",
            "updated_at",
        ]

    # Note: credentials_encrypted is explicitly excluded for security


class ProviderAccountListSerializer(serializers.ModelSerializer):
    """Minimal serializer for listing provider accounts"""

    component_name = serializers.CharField(source="component.name", read_only=True)

    class Meta:
        model = ProviderAccount
        fields = [
            "id",
            "component_name",
            "display_name",
            "is_active",
            "is_default",
            "connection_status",
        ]


# Phase 2: Shipping Zones
class ShippingZoneSerializer(serializers.ModelSerializer):
    """Serializer for ShippingZone - Phase 2"""

    coverage_summary = serializers.SerializerMethodField()
    country_count = serializers.SerializerMethodField()
    state_count = serializers.SerializerMethodField()

    class Meta:
        model = ShippingZone
        fields = [
            "id",
            "name",
            "description",
            "countries",
            "states",
            "postal_code_patterns",
            "is_active",
            "coverage_summary",
            "country_count",
            "state_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "coverage_summary",
            "country_count",
            "state_count",
            "created_at",
            "updated_at",
        ]

    def get_coverage_summary(self, obj):
        """Get human-readable coverage summary"""
        return obj.get_coverage_summary()

    def get_country_count(self, obj):
        """Get number of countries"""
        return obj.get_country_count()

    def get_state_count(self, obj):
        """Get number of states"""
        return obj.get_state_count()


class ShippingZoneListSerializer(serializers.ModelSerializer):
    """Minimal serializer for listing shipping zones"""

    coverage_summary = serializers.CharField(source="get_coverage_summary", read_only=True)

    class Meta:
        model = ShippingZone
        fields = ["id", "name", "is_active", "coverage_summary"]


# Phase 3: Shipping Promotions
class ShippingPromotionSerializer(serializers.ModelSerializer):
    """Serializer for ShippingPromotion - Phase 3"""

    zones_count = serializers.SerializerMethodField()
    methods_count = serializers.SerializerMethodField()

    class Meta:
        model = ShippingPromotion
        fields = [
            "id",
            "name",
            "description",
            "promotion_type",
            "promotion_value",
            "priority",
            "min_cart_value",
            "max_cart_value",
            "min_cart_weight",
            "max_cart_weight",
            "min_item_count",
            "max_item_count",
            "zones_count",
            "methods_count",
            "stop_further_promotions",
            "controls_visibility",
            "is_active",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "zones_count",
            "methods_count",
            "created_at",
            "updated_at",
        ]

    def get_zones_count(self, obj):
        """Get number of zones this promotion applies to"""
        return obj.zones.count()

    def get_methods_count(self, obj):
        """Get number of shipping methods this promotion applies to"""
        return obj.shipping_methods.count()


class ShippingPromotionListSerializer(serializers.ModelSerializer):
    """Minimal serializer for listing shipping promotions"""

    class Meta:
        model = ShippingPromotion
        fields = ["id", "name", "promotion_type", "priority", "is_active"]


# Phase 3: Rate Tables
class ShippingRateTableSerializer(serializers.ModelSerializer):
    """Serializer for ShippingRateTable - Phase 3"""

    tier_count = serializers.SerializerMethodField()

    class Meta:
        model = ShippingRateTable
        fields = [
            "id",
            "name",
            "description",
            "basis_type",
            "shipping_method",
            "tiers",
            "tier_count",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "tier_count",
            "created_at",
            "updated_at",
        ]

    def get_tier_count(self, obj):
        """Get number of rate tiers"""
        return len(obj.tiers) if obj.tiers else 0


# Phase 4: Pickup Locations
class LocationSerializer(serializers.ModelSerializer):
    """Serializer for pickup Location - Phase 4"""

    distance_to = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = [
            "id",
            "name",
            "address1",
            "address2",
            "city",
            "state",
            "postal_code",
            "country",
            "latitude",
            "longitude",
            "phone",
            "email",
            "pickup_instructions",
            "operating_hours",
            "is_active",
            "distance_to",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "distance_to",
            "created_at",
            "updated_at",
        ]

    def get_distance_to(self, obj):
        """Get distance to location from coordinates in context"""
        lat = self.context.get("latitude")
        lon = self.context.get("longitude")

        if lat is not None and lon is not None:
            return obj.calculate_distance_to(lat, lon)

        return None


class LocationListSerializer(serializers.ModelSerializer):
    """Minimal serializer for listing pickup locations"""

    class Meta:
        model = Location
        fields = [
            "id",
            "name",
            "city",
            "state",
            "country",
            "is_active",
        ]
