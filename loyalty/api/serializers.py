"""
Loyalty Program API Serializers

Serializers for customer-facing loyalty program endpoints.
These serializers expose loyalty data to headless frontends.
"""

from decimal import Decimal

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from loyalty.models import (
    LoyaltyBadge,
    LoyaltyBalance,
    LoyaltyMember,
    LoyaltyMemberBadge,
    LoyaltyRedemption,
    LoyaltyReward,
    LoyaltyRule,
    LoyaltyTier,
    LoyaltyTransaction,
)


class LoyaltyTierSerializer(serializers.ModelSerializer):
    """
    Serializer for loyalty tiers.

    Exposes tier information including benefits and requirements.
    """

    benefits = serializers.SerializerMethodField()

    class Meta:
        model = LoyaltyTier
        fields = [
            "uuid",
            "name",
            "slug",
            "description",
            "icon",
            "color",
            "rank",
            "min_spend",
            "min_orders",
            "min_points_earned",
            "points_multiplier",
            "benefits",
        ]
        read_only_fields = fields

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_benefits(self, obj) -> list:
        """Get list of tier benefits as strings"""
        benefits = []

        if obj.points_multiplier > Decimal("1.00"):
            multiplier_pct = (obj.points_multiplier - 1) * 100
            benefits.append(f"{int(multiplier_pct)}% bonus points on all purchases")

        if obj.has_free_shipping:
            benefits.append("Free shipping on all orders")

        if obj.has_early_access:
            benefits.append("Early access to sales and new products")

        return benefits


class LoyaltyBalanceSerializer(serializers.ModelSerializer):
    """
    Serializer for loyalty point balance.
    """

    total_points = serializers.ReadOnlyField()

    class Meta:
        model = LoyaltyBalance
        fields = [
            "available_points",
            "pending_points",
            "total_points",
            "lifetime_earned",
            "lifetime_redeemed",
            "lifetime_expired",
            "last_earned_at",
            "last_redeemed_at",
        ]
        read_only_fields = fields


class LoyaltyStatusSerializer(serializers.Serializer):
    """
    Serializer for customer's loyalty status.

    Combines member info, balance, and tier data.
    """

    member_uuid = serializers.UUIDField()
    enrolled_at = serializers.DateTimeField()
    is_active = serializers.BooleanField()

    # Balance
    available_points = serializers.IntegerField()
    pending_points = serializers.IntegerField()
    total_points = serializers.IntegerField()
    lifetime_earned = serializers.IntegerField()
    lifetime_redeemed = serializers.IntegerField()

    # Current tier
    current_tier = LoyaltyTierSerializer(allow_null=True)

    # Badges summary
    badges_earned_count = serializers.IntegerField()


class LoyaltyProgressSerializer(serializers.Serializer):
    """
    Serializer for tier progress information.

    Shows customer's progress toward the next tier.
    """

    current_tier = LoyaltyTierSerializer(allow_null=True)
    next_tier = LoyaltyTierSerializer(allow_null=True)

    # Current values
    current_spend = serializers.DecimalField(max_digits=10, decimal_places=2)
    current_orders = serializers.IntegerField()
    current_points_earned = serializers.IntegerField()

    # Progress percentages
    spend_progress_percent = serializers.IntegerField()
    orders_progress_percent = serializers.IntegerField()
    points_progress_percent = serializers.IntegerField()

    # Remaining to next tier
    spend_remaining = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    orders_remaining = serializers.IntegerField(allow_null=True)
    points_remaining = serializers.IntegerField(allow_null=True)

    # Message
    progress_message = serializers.CharField()


class LoyaltyTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for loyalty point transactions.
    """

    transaction_type_display = serializers.CharField(
        source="get_transaction_type_display", read_only=True
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = LoyaltyTransaction
        fields = [
            "uuid",
            "transaction_type",
            "transaction_type_display",
            "points",
            "status",
            "status_display",
            "description",
            "reason",
            "expires_at",
            "created_at",
        ]
        read_only_fields = fields


class LoyaltyBadgeSerializer(serializers.ModelSerializer):
    """
    Serializer for loyalty badges.
    """

    criteria_type_display = serializers.CharField(
        source="get_criteria_type_display", read_only=True
    )
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = LoyaltyBadge
        fields = [
            "uuid",
            "name",
            "slug",
            "description",
            "icon",
            "image_url",
            "criteria_type",
            "criteria_type_display",
            "criteria_value",
            "points_reward",
            "is_visible",
        ]
        read_only_fields = fields

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_image_url(self, obj) -> str | None:
        """Get badge image URL if available"""
        if obj.image:
            return obj.image.file.url if obj.image.file else None
        return None


class LoyaltyMemberBadgeSerializer(serializers.ModelSerializer):
    """
    Serializer for badges earned by a member.
    """

    badge = LoyaltyBadgeSerializer(read_only=True)

    class Meta:
        model = LoyaltyMemberBadge
        fields = [
            "badge",
            "earned_at",
        ]
        read_only_fields = fields


class LoyaltyRewardSerializer(serializers.ModelSerializer):
    """
    Serializer for available rewards.
    """

    reward_type_display = serializers.CharField(source="get_reward_type_display", read_only=True)
    discount_type_display = serializers.CharField(
        source="get_discount_type_display", read_only=True, allow_null=True
    )
    is_available = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = LoyaltyReward
        fields = [
            "uuid",
            "name",
            "slug",
            "description",
            "reward_type",
            "reward_type_display",
            "points_cost",
            "discount_type",
            "discount_type_display",
            "discount_value",
            "min_purchase_amount",
            "product_name",
            "image_url",
            "icon",
            "is_available",
            "quantity_remaining",
            "max_redemptions_per_member",
            "required_tier",
            "redemption_expires_days",
            "featured",
            "terms",
        ]
        read_only_fields = fields

    @extend_schema_field(serializers.BooleanField())
    def get_is_available(self, obj) -> bool:
        """Check if reward is currently available"""
        return obj.is_available()

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_product_name(self, obj) -> str | None:
        """Get product name for product rewards"""
        if obj.product:
            return obj.product.name
        return None

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_image_url(self, obj) -> str | None:
        """Get reward image URL"""
        if obj.image:
            return obj.image.url
        return None


class LoyaltyRewardDetailSerializer(LoyaltyRewardSerializer):
    """
    Detailed reward serializer with eligibility info.
    """

    can_redeem = serializers.SerializerMethodField()
    eligibility_message = serializers.SerializerMethodField()
    member_redemption_count = serializers.SerializerMethodField()

    class Meta(LoyaltyRewardSerializer.Meta):
        fields = LoyaltyRewardSerializer.Meta.fields + [
            "can_redeem",
            "eligibility_message",
            "member_redemption_count",
        ]

    @extend_schema_field(serializers.BooleanField())
    def get_can_redeem(self, obj) -> bool:
        """Check if current user can redeem this reward"""
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False

        try:
            member = request.user.loyalty_member
            can_redeem, _ = obj.can_member_redeem(member)
            return can_redeem
        except LoyaltyMember.DoesNotExist:
            return False

    @extend_schema_field(serializers.CharField())
    def get_eligibility_message(self, obj) -> str:
        """Get eligibility message for current user"""
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return "Login required"

        try:
            member = request.user.loyalty_member
            _, message = obj.can_member_redeem(member)
            return message
        except LoyaltyMember.DoesNotExist:
            return "Not enrolled in loyalty program"

    @extend_schema_field(serializers.IntegerField())
    def get_member_redemption_count(self, obj) -> int:
        """Get how many times current user has redeemed this reward"""
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return 0

        try:
            member = request.user.loyalty_member
            return LoyaltyRedemption.objects.filter(
                member=member,
                reward=obj,
                status__in=[
                    LoyaltyRedemption.STATUS_PENDING,
                    LoyaltyRedemption.STATUS_CONFIRMED,
                    LoyaltyRedemption.STATUS_FULFILLED,
                ],
            ).count()
        except LoyaltyMember.DoesNotExist:
            return 0


class LoyaltyRedemptionSerializer(serializers.ModelSerializer):
    """
    Serializer for reward redemptions.
    """

    reward = LoyaltyRewardSerializer(read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    voucher_code_value = serializers.SerializerMethodField()

    class Meta:
        model = LoyaltyRedemption
        fields = [
            "uuid",
            "redemption_code",
            "reward",
            "points_spent",
            "status",
            "status_display",
            "voucher_code_value",
            "expires_at",
            "created_at",
            "confirmed_at",
            "fulfilled_at",
        ]
        read_only_fields = fields

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_voucher_code_value(self, obj) -> str | None:
        """Get the voucher code value if applicable"""
        if obj.voucher_code:
            return obj.voucher_code.code
        return None


class RedeemRewardSerializer(serializers.Serializer):
    """
    Serializer for reward redemption requests.
    """

    reward_uuid = serializers.UUIDField(required=True)


class RedemptionResponseSerializer(serializers.Serializer):
    """
    Serializer for redemption response.
    """

    success = serializers.BooleanField()
    redemption = LoyaltyRedemptionSerializer(allow_null=True)
    message = serializers.CharField()


class LoyaltyRuleSerializer(serializers.ModelSerializer):
    """
    Serializer for earning rules (public info only).
    """

    rule_type_display = serializers.CharField(source="get_rule_type_display", read_only=True)
    action_type_display = serializers.CharField(
        source="get_action_type_display", read_only=True, allow_null=True
    )
    scope_display = serializers.CharField(source="get_scope_display", read_only=True)

    class Meta:
        model = LoyaltyRule
        fields = [
            "uuid",
            "name",
            "description",
            "rule_type",
            "rule_type_display",
            "action_type",
            "action_type_display",
            "scope",
            "scope_display",
            "points_rate",
            "min_order_amount",
        ]
        read_only_fields = fields


class LoyaltyEarningRulesSerializer(serializers.Serializer):
    """
    Serializer for earning rules summary.
    """

    spend_rules = LoyaltyRuleSerializer(many=True)
    action_rules = LoyaltyRuleSerializer(many=True)
    bonus_rules = LoyaltyRuleSerializer(many=True)
