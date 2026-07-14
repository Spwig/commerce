from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class POSCashPaymentSerializer(serializers.Serializer):
    """Cash payment with change calculation."""

    amount_tendered = serializers.DecimalField(max_digits=10, decimal_places=2)


class POSCardPaymentSerializer(serializers.Serializer):
    """Card payment (confirmed externally on standalone terminal)."""

    card_last_four = serializers.RegexField(
        r"^\d{4}$",
        max_length=4,
        required=False,
        allow_blank=True,
        help_text=_("Last four digits of card number (digits only)"),
    )
    card_reference = serializers.CharField(max_length=100, required=False, allow_blank=True)


class POSGiftCardPaymentSerializer(serializers.Serializer):
    """Gift card payment."""

    gift_card_code = serializers.CharField(max_length=50)
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        help_text=_("Amount to charge. If not provided, charges the full remaining balance."),
    )


class POSSplitTenderItemSerializer(serializers.Serializer):
    """A single payment in a split tender."""

    method = serializers.ChoiceField(choices=["cash", "card", "terminal_card", "gift_card"])
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    # Cash fields
    amount_tendered = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    # Card fields (manual)
    card_last_four = serializers.RegexField(
        r"^\d{4}$",
        max_length=4,
        required=False,
        allow_blank=True,
    )
    card_reference = serializers.CharField(max_length=100, required=False, allow_blank=True)

    # Terminal card fields (integrated reader)
    provider_payment_id = serializers.CharField(max_length=255, required=False, allow_blank=True)
    card_brand = serializers.CharField(max_length=20, required=False, allow_blank=True)

    # Gift card fields
    gift_card_code = serializers.CharField(max_length=50, required=False, allow_blank=True)


class POSSplitTenderSerializer(serializers.Serializer):
    """Split tender: multiple payment methods for one transaction."""

    payments = POSSplitTenderItemSerializer(many=True)

    def validate_payments(self, value):
        if not value:
            raise serializers.ValidationError("At least one payment is required.")
        return value
