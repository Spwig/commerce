"""
Referrals API Serializers
Serializers for referral program models
"""

from djmoney.contrib.django_rest_framework import MoneyField as MoneySerializerField
from rest_framework import serializers

from referrals.models import (
    ReferralAttribution,
    ReferralEvent,
    ReferralIdentity,
    ReferralProgram,
    ReferralReward,
)


class ReferralProgramSerializer(serializers.ModelSerializer):
    """Serializer for referral program configuration"""

    class Meta:
        model = ReferralProgram
        fields = [
            "id",
            "name",
            "status",
            "reward_config",
            "eligibility_rules",
            "timing_config",
            "caps_config",
            "tracking_config",
            "fraud_policy",
            "terms_and_conditions",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ReferralIdentitySerializer(serializers.ModelSerializer):
    """Full serializer for referral identity"""

    customer_email = serializers.EmailField(source="customer.email", read_only=True)
    customer_name = serializers.SerializerMethodField()
    referral_link = serializers.SerializerMethodField()
    conversion_rate = serializers.SerializerMethodField()
    signup_rate = serializers.SerializerMethodField()

    class Meta:
        model = ReferralIdentity
        fields = [
            "id",
            "customer",
            "customer_email",
            "customer_name",
            "token",
            "qr_code",
            "total_clicks",
            "total_signups",
            "total_conversions",
            "total_rewards_earned",
            "referral_link",
            "conversion_rate",
            "signup_rate",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "token",
            "total_clicks",
            "total_signups",
            "total_conversions",
            "total_rewards_earned",
            "created_at",
            "updated_at",
            "customer_email",
            "customer_name",
            "referral_link",
            "conversion_rate",
            "signup_rate",
        ]

    def get_customer_name(self, obj) -> str:
        """Get customer's full name or email"""
        return obj.customer.get_full_name() or obj.customer.email

    def get_referral_link(self, obj) -> str:
        """Get full referral link"""
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri("/") + f"?ref={obj.token}"
        return f"/?ref={obj.token}"

    def get_conversion_rate(self, obj) -> float:
        """Get conversion rate percentage"""
        return obj.get_conversion_rate()

    def get_signup_rate(self, obj) -> float:
        """Get signup rate percentage"""
        return obj.get_signup_rate()


class ReferralIdentityListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing identities"""

    customer_email = serializers.EmailField(source="customer.email", read_only=True)
    customer_name = serializers.SerializerMethodField()
    conversion_rate = serializers.SerializerMethodField()

    class Meta:
        model = ReferralIdentity
        fields = [
            "id",
            "customer",
            "customer_email",
            "customer_name",
            "token",
            "total_clicks",
            "total_signups",
            "total_conversions",
            "total_rewards_earned",
            "conversion_rate",
            "created_at",
        ]
        read_only_fields = fields

    def get_customer_name(self, obj) -> str:
        """Get customer's full name or email"""
        return obj.customer.get_full_name() or obj.customer.email

    def get_conversion_rate(self, obj) -> float:
        """Get conversion rate percentage"""
        return obj.get_conversion_rate()


class ReferralEventSerializer(serializers.ModelSerializer):
    """Serializer for referral events"""

    referrer_name = serializers.SerializerMethodField()
    customer_email = serializers.EmailField(
        source="customer.email", read_only=True, allow_null=True
    )

    class Meta:
        model = ReferralEvent
        fields = [
            "id",
            "program",
            "referrer_identity",
            "referrer_name",
            "customer",
            "customer_email",
            "event_type",
            "metadata",
            "created_at",
        ]
        read_only_fields = ["id", "referrer_name", "customer_email", "created_at"]

    def get_referrer_name(self, obj) -> str | None:
        """Get referrer's name"""
        if obj.referrer_identity:
            return (
                obj.referrer_identity.customer.get_full_name()
                or obj.referrer_identity.customer.email
            )
        return None


class ReferralAttributionSerializer(serializers.ModelSerializer):
    """Serializer for referral attributions"""

    referrer_name = serializers.SerializerMethodField()
    referee_email = serializers.EmailField(source="referee_customer.email", read_only=True)
    risk_score_display = serializers.SerializerMethodField()

    class Meta:
        model = ReferralAttribution
        fields = [
            "id",
            "program",
            "referrer_identity",
            "referrer_name",
            "referee_customer",
            "referee_email",
            "first_order",
            "status",
            "risk_score",
            "risk_score_display",
            "validation_data",
            "rejection_reason",
            "rejection_notes",
            "approved_at",
            "reviewed_by",
            "reviewed_at",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "referrer_name",
            "referee_email",
            "risk_score_display",
            "approved_at",
            "reviewed_by",
            "reviewed_at",
            "created_at",
        ]

    def get_referrer_name(self, obj) -> str | None:
        """Get referrer's name"""
        if obj.referrer_identity:
            return (
                obj.referrer_identity.customer.get_full_name()
                or obj.referrer_identity.customer.email
            )
        return None

    def get_risk_score_display(self, obj) -> str:
        """Get risk score with risk level"""
        if obj.risk_score is None:
            return "Not checked"
        if obj.risk_score < 30:
            return f"{obj.risk_score} (Low Risk)"
        elif obj.risk_score < 70:
            return f"{obj.risk_score} (Medium Risk)"
        else:
            return f"{obj.risk_score} (High Risk)"


class ReferralAttributionListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing attributions"""

    referrer_name = serializers.SerializerMethodField()
    referee_email = serializers.EmailField(source="referee_customer.email", read_only=True)

    class Meta:
        model = ReferralAttribution
        fields = [
            "id",
            "referrer_identity",
            "referrer_name",
            "referee_customer",
            "referee_email",
            "first_order",
            "status",
            "risk_score",
            "created_at",
        ]
        read_only_fields = fields

    def get_referrer_name(self, obj) -> str | None:
        """Get referrer's name"""
        if obj.referrer_identity:
            return (
                obj.referrer_identity.customer.get_full_name()
                or obj.referrer_identity.customer.email
            )
        return None


class ReferralRewardSerializer(serializers.ModelSerializer):
    """Serializer for referral rewards"""

    amount = MoneySerializerField(max_digits=12, decimal_places=2)
    customer_email = serializers.EmailField(source="customer.email", read_only=True)
    customer_name = serializers.SerializerMethodField()
    is_expiring_soon = serializers.SerializerMethodField()

    class Meta:
        model = ReferralReward
        fields = [
            "id",
            "program",
            "attribution",
            "customer",
            "customer_email",
            "customer_name",
            "recipient_type",
            "kind",
            "amount",
            "percentage",
            "description",
            "voucher_code_id",
            "wallet_transaction",
            "status",
            "issued_at",
            "redeemed_at",
            "expires_at",
            "revoked_at",
            "revocation_reason",
            "is_expiring_soon",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "customer_email",
            "customer_name",
            "is_expiring_soon",
            "created_at",
        ]

    def get_customer_name(self, obj) -> str:
        """Get customer's name"""
        return obj.customer.get_full_name() or obj.customer.email

    def get_is_expiring_soon(self, obj) -> bool:
        """Check if reward is expiring soon"""
        return obj.is_expiring_soon()


class ReferralRewardListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing rewards"""

    amount = MoneySerializerField(max_digits=12, decimal_places=2)
    customer_email = serializers.EmailField(source="customer.email", read_only=True)

    class Meta:
        model = ReferralReward
        fields = [
            "id",
            "customer",
            "customer_email",
            "recipient_type",
            "kind",
            "amount",
            "status",
            "issued_at",
            "expires_at",
            "created_at",
        ]
        read_only_fields = fields


class TrackClickSerializer(serializers.Serializer):
    """Serializer for tracking referral clicks"""

    token = serializers.CharField(max_length=32, required=True)

    def validate_token(self, value):
        """Check if token exists"""
        try:
            ReferralIdentity.objects.get(token=value)
            return value
        except ReferralIdentity.DoesNotExist:
            raise serializers.ValidationError("Invalid referral token")


class ApproveAttributionSerializer(serializers.Serializer):
    """Serializer for approving attributions"""

    note = serializers.CharField(max_length=500, required=False, allow_blank=True)


class RejectAttributionSerializer(serializers.Serializer):
    """Serializer for rejecting attributions"""

    rejection_reason = serializers.ChoiceField(
        choices=ReferralAttribution.REJECTION_REASON_CHOICES, required=True
    )
    rejection_note = serializers.CharField(max_length=500, required=False, allow_blank=True)
