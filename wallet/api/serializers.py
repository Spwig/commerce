"""
Wallet API Serializers

Serializers for customer-facing and admin wallet endpoints.
"""

from decimal import Decimal

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from core.utils import get_default_currency
from wallet.models import CustomerWallet, WalletTransaction

# =====================================================================
# CUSTOMER-FACING SERIALIZERS
# =====================================================================


class WalletBalanceSerializer(serializers.ModelSerializer):
    """
    Customer-facing wallet balance.
    """

    available_balance = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        source="available_balance.amount",
    )
    available_balance_currency = serializers.CharField(
        source="available_balance.currency",
        read_only=True,
    )
    pending_balance = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        source="pending_balance.amount",
    )
    pending_balance_currency = serializers.CharField(
        source="pending_balance.currency",
        read_only=True,
    )
    lifetime_credited = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        source="lifetime_credited.amount",
    )
    lifetime_used = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        source="lifetime_used.amount",
    )

    class Meta:
        model = CustomerWallet
        fields = [
            "available_balance",
            "available_balance_currency",
            "pending_balance",
            "pending_balance_currency",
            "lifetime_credited",
            "lifetime_used",
            "is_active",
        ]
        read_only_fields = fields


class WalletTransactionListSerializer(serializers.ModelSerializer):
    """
    Compact transaction representation for list views.
    """

    transaction_type_display = serializers.CharField(
        source="get_transaction_type_display",
        read_only=True,
    )
    source_display = serializers.CharField(
        source="get_source_display",
        read_only=True,
    )
    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        source="amount.amount",
    )
    amount_currency = serializers.CharField(
        source="amount.currency",
        read_only=True,
    )
    balance_after = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        source="balance_after.amount",
    )
    balance_after_currency = serializers.CharField(
        source="balance_after.currency",
        read_only=True,
    )

    class Meta:
        model = WalletTransaction
        fields = [
            "id",
            "transaction_type",
            "transaction_type_display",
            "amount",
            "amount_currency",
            "balance_after",
            "balance_after_currency",
            "status",
            "source",
            "source_display",
            "description",
            "created_at",
        ]
        read_only_fields = fields


# =====================================================================
# ADMIN SERIALIZERS
# =====================================================================


class CustomerWalletSerializer(serializers.ModelSerializer):
    """
    Full wallet detail for admin views.
    """

    customer_email = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    available_balance = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        source="available_balance.amount",
    )
    available_balance_currency = serializers.CharField(
        source="available_balance.currency",
        read_only=True,
    )
    pending_balance = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        source="pending_balance.amount",
    )
    pending_balance_currency = serializers.CharField(
        source="pending_balance.currency",
        read_only=True,
    )
    lifetime_credited = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        source="lifetime_credited.amount",
    )
    lifetime_credited_currency = serializers.CharField(
        source="lifetime_credited.currency",
        read_only=True,
    )
    lifetime_used = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        source="lifetime_used.amount",
    )
    lifetime_used_currency = serializers.CharField(
        source="lifetime_used.currency",
        read_only=True,
    )

    class Meta:
        model = CustomerWallet
        fields = [
            "id",
            "customer_email",
            "customer_name",
            "available_balance",
            "available_balance_currency",
            "pending_balance",
            "pending_balance_currency",
            "lifetime_credited",
            "lifetime_credited_currency",
            "lifetime_used",
            "lifetime_used_currency",
            "is_active",
            "last_credited_at",
            "last_used_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

    @extend_schema_field(serializers.CharField())
    def get_customer_email(self, obj) -> str:
        return obj.customer.email

    @extend_schema_field(serializers.CharField(allow_blank=True))
    def get_customer_name(self, obj) -> str:
        return obj.customer.get_full_name() or ""


class CustomerWalletListSerializer(CustomerWalletSerializer):
    """
    Compact wallet representation for admin list views.
    """

    class Meta(CustomerWalletSerializer.Meta):
        fields = [
            "id",
            "customer_email",
            "customer_name",
            "available_balance",
            "available_balance_currency",
            "is_active",
            "last_credited_at",
            "last_used_at",
        ]


class WalletTransactionSerializer(WalletTransactionListSerializer):
    """
    Full transaction detail for admin views.
    """

    created_by_email = serializers.SerializerMethodField()

    class Meta(WalletTransactionListSerializer.Meta):
        fields = WalletTransactionListSerializer.Meta.fields + [
            "reference_id",
            "created_by_email",
        ]

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_created_by_email(self, obj) -> str | None:
        if obj.created_by:
            return obj.created_by.email
        return None


class AdminTransactionSerializer(WalletTransactionSerializer):
    """
    Admin transaction view that includes wallet customer info.
    """

    wallet_customer_email = serializers.SerializerMethodField()

    class Meta(WalletTransactionSerializer.Meta):
        fields = WalletTransactionSerializer.Meta.fields + [
            "wallet_id",
            "wallet_customer_email",
        ]

    @extend_schema_field(serializers.CharField())
    def get_wallet_customer_email(self, obj) -> str:
        return obj.wallet.customer.email


# =====================================================================
# INPUT SERIALIZERS
# =====================================================================


class WalletCreditSerializer(serializers.Serializer):
    """
    Input serializer for manual wallet credit.
    """

    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.01"),
    )
    currency = serializers.CharField(max_length=3, default=get_default_currency)
    source = serializers.ChoiceField(
        choices=[
            ("manual", _("Manual Adjustment")),
            ("promotion", _("Promotion")),
            ("refund", _("Order Refund")),
        ],
        default="manual",
    )
    description = serializers.CharField(max_length=500)
    reference_id = serializers.CharField(max_length=100, required=False, default="")


class WalletDebitSerializer(serializers.Serializer):
    """
    Input serializer for manual wallet debit.
    """

    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.01"),
    )
    currency = serializers.CharField(max_length=3, default=get_default_currency)
    source = serializers.ChoiceField(
        choices=[
            ("manual", _("Manual Adjustment")),
            ("order", _("Order Payment")),
        ],
        default="manual",
    )
    description = serializers.CharField(max_length=500)
    reference_id = serializers.CharField(max_length=100, required=False, default="")
