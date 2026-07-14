from rest_framework import serializers

from pos_app.models import POSTerminal


class POSTerminalSerializer(serializers.ModelSerializer):
    warehouse_name = serializers.CharField(source="warehouse.name", read_only=True)
    pos_display_name = serializers.CharField(source="warehouse.pos_display_name", read_only=True)
    effective_currency = serializers.CharField(read_only=True)

    class Meta:
        model = POSTerminal
        fields = [
            "uuid",
            "name",
            "warehouse",
            "warehouse_name",
            "pos_display_name",
            "hardware_config",
            "is_active",
            "last_heartbeat",
            "currency",
            "effective_currency",
            "remote_unlock_at",
            "order_sync_days",
            "order_sync_limit",
        ]
        read_only_fields = ["uuid", "last_heartbeat", "effective_currency", "remote_unlock_at"]


class POSTerminalConfigSerializer(serializers.Serializer):
    """Configuration returned after terminal registration/login."""

    terminal = POSTerminalSerializer()
    warehouse_id = serializers.IntegerField()
    warehouse_name = serializers.CharField()
    currency = serializers.CharField()
    tax_rate = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)


class POSTerminalRegisterSerializer(serializers.Serializer):
    """Register a terminal using its pairing code."""

    pairing_code = serializers.CharField(max_length=8)
    device_name = serializers.CharField(max_length=200, required=False, default="")
