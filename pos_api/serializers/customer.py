from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from accounts.models import CustomerProfile

# Persisted-column limits: a walk-in customer's email is stored as User.username
# and their phone as CustomerProfile.phone, so validation must match those columns.
USERNAME_MAX_LENGTH = get_user_model()._meta.get_field("username").max_length
PHONE_MAX_LENGTH = CustomerProfile._meta.get_field("phone").max_length


class POSCustomerSerializer(serializers.Serializer):
    """Customer data for POS display."""

    id = serializers.IntegerField()
    email = serializers.EmailField()
    first_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)
    full_name = serializers.CharField()
    phone = serializers.CharField(allow_blank=True)
    total_orders = serializers.IntegerField(required=False)
    total_spent = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    loyalty_points = serializers.IntegerField(required=False)


class POSCustomerSearchSerializer(serializers.Serializer):
    """Search parameters for customer lookup."""

    q = serializers.CharField(max_length=200, help_text=_("Search by email, phone, or name"))


class POSCustomerCreateSerializer(serializers.Serializer):
    """Create a walk-in customer."""

    email = serializers.EmailField(max_length=USERNAME_MAX_LENGTH, required=False, allow_blank=True)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=PHONE_MAX_LENGTH, required=False, allow_blank=True)
