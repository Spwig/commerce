from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class POSCustomerSerializer(serializers.Serializer):
    """Customer data for POS display."""
    id = serializers.IntegerField()
    email = serializers.EmailField()
    first_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)
    full_name = serializers.CharField()
    phone = serializers.CharField(allow_blank=True)
    total_orders = serializers.IntegerField(required=False)
    total_spent = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False
    )
    loyalty_points = serializers.IntegerField(required=False)


class POSCustomerSearchSerializer(serializers.Serializer):
    """Search parameters for customer lookup."""
    q = serializers.CharField(
        max_length=200,
        help_text=_('Search by email, phone, or name')
    )


class POSCustomerCreateSerializer(serializers.Serializer):
    """Create a walk-in customer."""
    email = serializers.EmailField(required=False, allow_blank=True)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=50, required=False, allow_blank=True)
