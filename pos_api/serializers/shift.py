from rest_framework import serializers


class POSShiftSerializer(serializers.Serializer):
    """Shift data for POS display."""

    id = serializers.IntegerField()
    terminal_name = serializers.CharField()
    cashier_name = serializers.CharField()
    started_at = serializers.DateTimeField()
    ended_at = serializers.DateTimeField(allow_null=True)
    is_open = serializers.BooleanField()
    opening_cash = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_sales = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_refunds = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_transactions = serializers.IntegerField()
    net_sales = serializers.DecimalField(max_digits=10, decimal_places=2)

    # Payment method breakdown
    cash_total = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    card_total = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    gift_card_total = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)


class POSShiftOpenSerializer(serializers.Serializer):
    """Open a new shift."""

    opening_cash = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)


class POSShiftCloseSerializer(serializers.Serializer):
    """Close the current shift."""

    closing_cash = serializers.DecimalField(max_digits=10, decimal_places=2)
    notes = serializers.CharField(required=False, allow_blank=True)


class POSCashMovementSerializer(serializers.Serializer):
    """Record a cash movement."""

    movement_type = serializers.ChoiceField(choices=["in", "out"])
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    reason = serializers.CharField(max_length=200)
