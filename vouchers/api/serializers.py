"""
Vouchers API Serializers
Serializers for voucher, gift card, and usage models
"""

from djmoney.contrib.django_rest_framework import MoneyField as MoneySerializerField
from rest_framework import serializers

from catalog.models import Category, Product
from vouchers.models import AppliedVoucher, GiftCard, VoucherCode, VoucherRestriction, VoucherUsage


class VoucherRestrictionSerializer(serializers.ModelSerializer):
    """Serializer for voucher restrictions"""

    class Meta:
        model = VoucherRestriction
        fields = [
            "id",
            "restriction_type",
            "restriction_value",
            "is_inclusive",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class VoucherCodeSerializer(serializers.ModelSerializer):
    """Full serializer for voucher codes (admin)"""

    restrictions = VoucherRestrictionSerializer(many=True, read_only=True)
    max_discount_amount = MoneySerializerField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    min_order_value = MoneySerializerField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    gift_card_balance = MoneySerializerField(
        max_digits=10, decimal_places=2, required=False, allow_null=True, read_only=True
    )
    original_gift_card_value = MoneySerializerField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )

    # Computed fields
    is_valid = serializers.BooleanField(read_only=True)
    is_gift_card = serializers.BooleanField(read_only=True)
    uses_remaining = serializers.IntegerField(read_only=True, allow_null=True)

    # Related fields
    eligible_products = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Product.objects.all(), required=False
    )
    eligible_categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), required=False
    )

    class Meta:
        model = VoucherCode
        fields = [
            "id",
            "code",
            "name",
            "description",
            "external_id",
            "discount_type",
            "discount_value",
            "max_discount_amount",
            "application_scope",
            "start_date",
            "end_date",
            "days_valid",
            "max_uses_total",
            "max_uses_per_customer",
            "current_uses",
            "min_order_value",
            "exclude_sale_items",
            "cannot_combine_with_other_vouchers",
            "cannot_combine_with_sale_items",
            "first_time_customers_only",
            "gift_card_balance",
            "original_gift_card_value",
            "is_active",
            "created_at",
            "updated_at",
            "eligible_products",
            "eligible_categories",
            "restrictions",
            "is_valid",
            "is_gift_card",
            "uses_remaining",
        ]
        read_only_fields = [
            "id",
            "current_uses",
            "gift_card_balance",
            "created_at",
            "updated_at",
            "is_valid",
            "is_gift_card",
            "uses_remaining",
        ]


class VoucherCodeListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing vouchers"""

    max_discount_amount = MoneySerializerField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    min_order_value = MoneySerializerField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    gift_card_balance = MoneySerializerField(
        max_digits=10, decimal_places=2, required=False, allow_null=True, read_only=True
    )

    is_valid = serializers.BooleanField(read_only=True)
    is_gift_card = serializers.BooleanField(read_only=True)
    uses_remaining = serializers.IntegerField(read_only=True, allow_null=True)

    class Meta:
        model = VoucherCode
        fields = [
            "id",
            "code",
            "name",
            "discount_type",
            "discount_value",
            "max_discount_amount",
            "application_scope",
            "start_date",
            "end_date",
            "max_uses_total",
            "current_uses",
            "min_order_value",
            "gift_card_balance",
            "is_active",
            "is_valid",
            "is_gift_card",
            "uses_remaining",
        ]
        read_only_fields = [
            "id",
            "current_uses",
            "gift_card_balance",
            "is_valid",
            "is_gift_card",
            "uses_remaining",
        ]


class VoucherUsageSerializer(serializers.ModelSerializer):
    """Serializer for voucher usage tracking"""

    voucher_code = serializers.CharField(source="voucher.code", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True, allow_null=True)
    discount_amount = MoneySerializerField(max_digits=10, decimal_places=2)
    cart_total = MoneySerializerField(max_digits=10, decimal_places=2)

    class Meta:
        model = VoucherUsage
        fields = [
            "id",
            "voucher",
            "voucher_code",
            "user",
            "user_email",
            "order",
            "discount_amount",
            "cart_total",
            "session_key",
            "used_at",
        ]
        read_only_fields = ["id", "voucher_code", "user_email", "used_at"]


class GiftCardSerializer(serializers.ModelSerializer):
    """Serializer for gift cards"""

    voucher_code = serializers.CharField(source="voucher.code", read_only=True)
    balance = MoneySerializerField(max_digits=10, decimal_places=2, read_only=True)
    original_value = MoneySerializerField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = GiftCard
        fields = [
            "id",
            "voucher",
            "voucher_code",
            "recipient_email",
            "recipient_name",
            "sender_name",
            "message",
            "send_immediately",
            "delivery_date",
            "is_delivered",
            "delivered_at",
            "purchased_by",
            "purchase_order",
            "status",
            "balance",
            "original_value",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "voucher_code",
            "is_delivered",
            "delivered_at",
            "balance",
            "original_value",
            "created_at",
            "updated_at",
        ]


class AppliedVoucherSerializer(serializers.ModelSerializer):
    """Serializer for applied vouchers in cart"""

    voucher_code = serializers.CharField(source="voucher.code", read_only=True)
    voucher_name = serializers.CharField(source="voucher.name", read_only=True)
    discount_amount = MoneySerializerField(max_digits=10, decimal_places=2)

    class Meta:
        model = AppliedVoucher
        fields = [
            "id",
            "cart",
            "voucher",
            "voucher_code",
            "voucher_name",
            "discount_amount",
            "applied_at",
        ]
        read_only_fields = ["id", "voucher_code", "voucher_name", "applied_at"]


class VoucherValidationSerializer(serializers.Serializer):
    """Serializer for validating voucher codes"""

    code = serializers.CharField(max_length=50, required=True)
    cart_total = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    def validate_code(self, value):
        """Check if voucher code exists"""
        try:
            voucher = VoucherCode.objects.get(code=value.upper())
            return voucher.code
        except VoucherCode.DoesNotExist:
            raise serializers.ValidationError("Invalid voucher code")


class VoucherApplicationSerializer(serializers.Serializer):
    """Serializer for applying voucher to cart"""

    code = serializers.CharField(max_length=50, required=True)

    def validate_code(self, value):
        """Check if voucher code exists and is valid"""
        try:
            voucher = VoucherCode.objects.get(code=value.upper())
            if not voucher.is_valid:
                raise serializers.ValidationError("This voucher is not currently valid")
            return voucher.code
        except VoucherCode.DoesNotExist:
            raise serializers.ValidationError("Invalid voucher code")
