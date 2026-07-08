from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class POSTerminalCardPaymentSerializer(serializers.Serializer):
    """Terminal card payment — processed via integrated card reader (Stripe Terminal, etc.)."""
    provider_payment_id = serializers.CharField(
        max_length=255,
        help_text=_('Payment ID from the terminal provider (e.g. Stripe PaymentIntent ID)'),
    )
    card_last_four = serializers.CharField(max_length=4, required=False, allow_blank=True)
    card_brand = serializers.CharField(max_length=20, required=False, allow_blank=True)


class ConnectionTokenResponseSerializer(serializers.Serializer):
    """Response from the connection token endpoint."""
    success = serializers.BooleanField()
    secret = serializers.CharField()


class CreatePaymentIntentSerializer(serializers.Serializer):
    """Request to create a PaymentIntent for terminal collection."""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3, required=False, allow_blank=True)


class PaymentIntentResponseSerializer(serializers.Serializer):
    """Response from create-payment-intent endpoint."""
    success = serializers.BooleanField()
    payment_intent_id = serializers.CharField()
    client_secret = serializers.CharField()


class CapturePaymentSerializer(serializers.Serializer):
    """Request to verify/capture a terminal payment."""
    payment_intent_id = serializers.CharField(max_length=255)


class CancelPaymentSerializer(serializers.Serializer):
    """Request to cancel a pending terminal payment."""
    payment_intent_id = serializers.CharField(max_length=255)


class InitiateCloudPaymentSerializer(serializers.Serializer):
    """Request to initiate a cloud-based payment on a terminal reader."""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3, required=False, allow_blank=True)
    reader_id = serializers.CharField(
        max_length=255,
        help_text=_('Provider-specific reader ID (e.g. Adyen POIID, Square device_id)'),
    )


class CancelCloudPaymentSerializer(serializers.Serializer):
    """Request to cancel a pending cloud payment."""
    transaction_id = serializers.CharField(max_length=255)


class CloudPaymentInitiatedSerializer(serializers.Serializer):
    """Response from initiate-cloud-payment when successful."""
    success = serializers.BooleanField(default=True)
    transaction_id = serializers.CharField(
        help_text=_('Provider-specific transaction ID for status polling'),
    )
    status = serializers.ChoiceField(
        choices=['pending', 'succeeded'],
        help_text=_('Initial status -- typically "pending" for async providers, "succeeded" for sync (Adyen)'),
    )
    card_brand = serializers.CharField(required=False, allow_blank=True)
    last4 = serializers.CharField(required=False, allow_blank=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)


class CloudPaymentStatusSerializer(serializers.Serializer):
    """Response from payment-status polling endpoint."""
    success = serializers.BooleanField()
    status = serializers.ChoiceField(
        choices=['pending', 'succeeded', 'failed', 'canceled'],
        help_text=_('Current payment status'),
    )
    card_brand = serializers.CharField(required=False, allow_blank=True)
    last4 = serializers.CharField(required=False, allow_blank=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    payment_id = serializers.CharField(required=False, help_text=_('Provider payment ID (when succeeded)'))
    cancel_reason = serializers.CharField(required=False, help_text=_('Reason for cancellation (when canceled)'))


class ProviderConfigResponseSerializer(serializers.Serializer):
    """Response from terminal provider config endpoint."""
    success = serializers.BooleanField()
    provider_key = serializers.CharField()
    provider_name = serializers.CharField()
    integration_mode = serializers.ChoiceField(choices=['sdk', 'cloud', 'manual'])
    has_reader = serializers.BooleanField()
    reader = serializers.DictField(required=False, allow_null=True)


class ReaderListResponseSerializer(serializers.Serializer):
    """Response from list-readers endpoint."""
    success = serializers.BooleanField()
    readers = serializers.ListField(child=serializers.DictField())


class ErrorDetailSerializer(serializers.Serializer):
    """Standard error detail."""
    code = serializers.CharField()
    message = serializers.CharField()


class ErrorResponseSerializer(serializers.Serializer):
    """Standard error response for terminal provider endpoints."""
    success = serializers.BooleanField(default=False)
    error = ErrorDetailSerializer()


class SuccessResponseSerializer(serializers.Serializer):
    """Generic success response."""
    success = serializers.BooleanField(default=True)
