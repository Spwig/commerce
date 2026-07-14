"""
Serializers for the Exchange Rates API.
"""

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from exchange_rates.models import ManualExchangeRate


class ManualExchangeRateListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list view"""

    currency_pair = serializers.SerializerMethodField()

    class Meta:
        model = ManualExchangeRate
        fields = [
            "id",
            "currency_pair",
            "base_currency",
            "target_currency",
            "rate",
            "is_active",
            "exclude_from_auto_sync",
            "updated_at",
        ]

    def get_currency_pair(self, obj):
        return f"{obj.base_currency}/{obj.target_currency}"


class ManualExchangeRateSerializer(serializers.ModelSerializer):
    """Full serializer for create/update/detail"""

    currency_pair = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ManualExchangeRate
        fields = [
            "id",
            "currency_pair",
            "base_currency",
            "target_currency",
            "rate",
            "is_active",
            "exclude_from_auto_sync",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_currency_pair(self, obj):
        return f"{obj.base_currency}/{obj.target_currency}"

    def validate_rate(self, value):
        if value <= 0:
            raise serializers.ValidationError(_("Exchange rate must be greater than zero."))
        return value

    def validate(self, data):
        base = data.get("base_currency", getattr(self.instance, "base_currency", None))
        target = data.get("target_currency", getattr(self.instance, "target_currency", None))

        if base and target and base == target:
            raise serializers.ValidationError(
                {"target_currency": _("Base and target currencies must be different.")}
            )

        return data


class ManualExchangeRateBulkSerializer(serializers.Serializer):
    """Serializer for bulk create/update of manual rates"""

    rates = serializers.ListField(
        child=serializers.DictField(),
        min_length=1,
        max_length=100,
        help_text=_(
            "List of rate objects with base_currency, target_currency, rate, and optional is_active/notes"
        ),
    )
