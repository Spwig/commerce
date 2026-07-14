"""
Payment Orchestration API Serializers

Serializers for the public payment orchestration API endpoints.
"""

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core.utils import get_default_country, get_default_currency
from payment_providers.models import PaymentIntent


class CreatePaymentIntentSerializer(serializers.Serializer):
    """
    Request serializer for creating a payment intent.
    """

    checkout_session_id = serializers.UUIDField(
        required=False,
        help_text=_("Checkout session ID. If not provided, uses current user's active session."),
    )
    provider_id = serializers.UUIDField(
        required=False,
        help_text=_(
            "Payment provider account ID. If not provided, uses session's selected provider."
        ),
    )
    saved_method_id = serializers.UUIDField(
        required=False, help_text=_("Saved payment method ID for returning customers.")
    )
    return_url = serializers.URLField(
        required=True, help_text=_("URL to redirect after successful payment.")
    )
    cancel_url = serializers.URLField(
        required=True, help_text=_("URL to redirect on payment cancellation.")
    )
    metadata = serializers.JSONField(
        required=False, default=dict, help_text=_("Additional metadata to attach to the payment.")
    )


class PaymentActionSerializer(serializers.Serializer):
    """
    Serializer for payment actions (3DS, redirects, etc.)
    """

    type = serializers.CharField(
        help_text=_("Type of action required (redirect, 3ds_challenge, etc.)")
    )
    url = serializers.URLField(
        required=False, allow_null=True, help_text=_("URL to redirect for action completion.")
    )
    data = serializers.JSONField(
        required=False, default=dict, help_text=_("Provider-specific action data for SDK handling.")
    )


class PaymentIntentResponseSerializer(serializers.Serializer):
    """
    Response serializer for payment intent creation and status.
    """

    success = serializers.SerializerMethodField(help_text=_("Whether the operation succeeded."))
    intent_id = serializers.UUIDField(source="id", help_text=_("Payment intent ID."))
    order_id = serializers.UUIDField(
        source="order.id", help_text=_("Order ID (created with 'unpaid' status).")
    )
    order_number = serializers.CharField(
        source="order.order_number", help_text=_("Order number for display.")
    )
    status = serializers.CharField(help_text=_("Current payment intent status."))
    checkout_type = serializers.SerializerMethodField(
        help_text=_("Type of checkout flow (hosted or embedded).")
    )
    checkout_url = serializers.URLField(
        required=False,
        allow_null=True,
        allow_blank=True,
        help_text=_("Hosted checkout redirect URL (for hosted checkout)."),
    )
    client_secret = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        help_text=_("Client secret for provider SDK (for embedded checkout)."),
    )
    publishable_key = serializers.SerializerMethodField(
        help_text=_("Provider's publishable key for SDK initialization.")
    )
    handler_url = serializers.SerializerMethodField(
        help_text=_("URL to provider's checkout handler JavaScript.")
    )
    handler_config = serializers.SerializerMethodField(
        help_text=_("Configuration data for handler initialization.")
    )
    sdk_dependencies = serializers.SerializerMethodField(
        help_text=_("External SDK URLs required by provider.")
    )
    provider_key = serializers.SerializerMethodField(
        help_text=_("Provider identifier (slug) for handler lookup.")
    )
    requires_action = serializers.BooleanField(
        help_text=_("Whether customer action is required (3DS, etc.).")
    )
    action = serializers.SerializerMethodField(
        help_text=_("Action details if requires_action is true.")
    )
    expires_at = serializers.DateTimeField(help_text=_("When this payment intent expires."))
    error = serializers.SerializerMethodField(help_text=_("Error details if payment failed."))

    def get_success(self, obj):
        """Always returns True for successful intent creation."""
        return True

    def get_checkout_type(self, obj):
        """Determine checkout type based on what's populated."""
        if obj.checkout_url:
            return "hosted"
        elif obj.client_secret:
            return "embedded"
        return "hosted"  # Default

    def get_publishable_key(self, obj):
        """Get publishable key from provider settings."""
        if obj.provider_account and obj.provider_account.settings:
            return obj.provider_account.settings.get("publishable_key", "")
        return ""

    def get_action(self, obj):
        """Get action details if action required."""
        if obj.requires_action:
            return {
                "type": obj.action_type,
                "url": obj.action_url or None,
                "data": obj.action_data or {},
            }
        return None

    def get_error(self, obj):
        """Get error details if failed."""
        if obj.status == "failed" and (obj.error_code or obj.error_message):
            return {"code": obj.error_code, "message": obj.error_message}
        return None

    def get_handler_url(self, obj):
        """Build URL to provider's checkout handler JavaScript."""
        if not obj.provider_account:
            return None

        # Get provider component
        component = obj.provider_account.component
        if not component:
            return None

        try:
            # Load manifest using component's method
            manifest = component.get_manifest()
            if not manifest:
                return None

            # Check if provider has frontend checkout handler
            if "frontend" in manifest and "checkout_handler" in manifest["frontend"]:
                handler_file = manifest["frontend"]["checkout_handler"]
                # Build URL: /components/payments/{slug}/current/{handler_file}
                return f"/components/payments/{component.slug}/current/{handler_file}"

        except Exception as e:
            # Log error but don't break the response
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Error getting handler URL for {component.slug}: {e}")

        return None

    def get_handler_config(self, obj):
        """Build handler configuration from payment intent data."""
        if not obj.provider_account or not obj.provider_response:
            return None

        # Check if provider is Airwallex (or other providers that need handler_config)
        component = obj.provider_account.component
        if not component:
            return None

        # Get manifest to check if provider has frontend integration
        try:
            manifest = component.get_manifest()
            if not manifest or "frontend" not in manifest:
                return None
        except Exception:
            return None

        # Build handler config dynamically from payment intent data
        config = {
            "intent_id": obj.provider_response.get("id") or obj.provider_intent_id,
            "currency": (obj.provider_response.get("currency") or get_default_currency()).upper(),
        }

        # Add provider-specific settings
        settings = obj.provider_account.settings or {}

        # Get decrypted credentials to determine test_mode
        try:
            from payment_providers.utils.encryption import decrypt_credentials

            decrypted_creds = decrypt_credentials(obj.provider_account.credentials_encrypted)
        except Exception:
            decrypted_creds = {}

        # Determine test_mode (NEW + LEGACY)
        test_mode = decrypted_creds.get("test_mode")
        if test_mode is None:
            # Legacy: derive from environment field
            env = decrypted_creds.get("environment", settings.get("environment", "test"))
            test_mode = env.lower() in ("test", "sandbox", "development", "dev", "demo")

        # For Airwallex
        if component.slug == "airwallex":
            config["environment"] = "demo" if test_mode else "production"
            # Get country from order if available
            if obj.order:
                config["country_code"] = (
                    obj.order.shipping_country or obj.order.billing_country or get_default_country()
                )
            else:
                config["country_code"] = get_default_country()

        # For Stripe
        elif component.slug == "stripe":
            # NEW: Select correct publishable key based on test_mode
            if test_mode:
                config["publishable_key"] = decrypted_creds.get("test_publishable_key", "")
            else:
                config["publishable_key"] = decrypted_creds.get("live_publishable_key", "")

            # LEGACY: Fallback for single-key structure
            if not config["publishable_key"]:
                config["publishable_key"] = decrypted_creds.get(
                    "publishable_key", settings.get("publishable_key", "")
                )

            config["environment"] = "test" if test_mode else "live"
            # Get country from order if available
            if obj.order:
                config["country_code"] = (
                    obj.order.shipping_country or obj.order.billing_country or get_default_country()
                )
            else:
                config["country_code"] = get_default_country()

        # For Square
        elif component.slug == "square":
            # handler_config already built in provider.py _create_embedded_checkout
            # Just pass it through from intent_data
            intent_data = self.context.get("intent_data", {})
            handler_config = intent_data.get("handler_config")
            if handler_config:
                return handler_config
            return None

        # For PayPal (v1.1.0+)
        elif component.slug == "paypal_checkout":
            # Extract handler_config from provider response
            provider_response = obj.provider_response or {}
            handler_config = provider_response.get("handler_config")
            if handler_config:
                return handler_config

            # Fallback: build from available data
            config = {
                "order_id": obj.provider_intent_id,
                "currency": obj.currency.upper(),
            }

            # Get client_id from provider credentials
            settings = obj.provider_account.decrypted_credentials
            if settings:
                config["client_id"] = settings.get("client_id", "")
                config["environment"] = settings.get("environment", "sandbox")

            # Get amount from order
            if obj.order:
                from decimal import ROUND_HALF_UP, Decimal

                amount = obj.order.total
                currency_upper = obj.currency.upper()
                zero_decimal = {"JPY", "HUF", "TWD", "KRW"}
                if currency_upper in zero_decimal:
                    config["amount"] = str(int(amount))
                else:
                    rounded = amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    config["amount"] = str(rounded)

            return config

        # For Revolut (v1.1.0+)
        elif component.slug == "revolut":
            # Extract handler_config from provider response
            provider_response = obj.provider_response or {}
            handler_config = provider_response.get("handler_config")
            if handler_config:
                return handler_config

            # Fallback: build from available data
            config = {
                "order_id": obj.provider_intent_id,
                "token": obj.provider_response.get("token", "") if obj.provider_response else "",
                "currency": obj.currency.upper(),
            }
            settings = obj.provider_account.decrypted_credentials
            if settings:
                config["public_key"] = settings.get("public_key", "")
                config["environment"] = settings.get("environment", "sandbox")

            return config

        return config

    def get_sdk_dependencies(self, obj):
        """Get SDK dependencies from provider manifest.

        Supports template variable resolution in SDK URLs:
        - Direct credential substitution: {{credential_key}} is replaced
          with the value from the provider's credentials/settings.
          E.g., "https://sdk.example.com/js?key={{client_id}}"
        - Mapped variables via sdk_variable_map: For values that need
          transformation (e.g., environment name → hostname), define a
          mapping in the manifest's frontend.sdk_variable_map section.
          E.g., sdk_variable_map: {"host": {"sandbox": "sandbox.example.com",
          "production": "example.com"}} resolves {{host}} by looking up the
          credential value for the map key in the mapping dict.
        """
        if not obj.provider_account:
            return []

        component = obj.provider_account.component
        if not component:
            return []

        try:
            manifest = component.get_manifest()
            if not manifest:
                return []

            frontend = manifest.get("frontend")
            if not frontend:
                return []

            urls = frontend.get("sdk_dependencies", [])
            if not urls:
                return []

            # Resolve template variables from provider credentials
            try:
                from payment_providers.utils.encryption import decrypt_credentials

                settings = decrypt_credentials(obj.provider_account.credentials_encrypted) or {}
            except Exception:
                settings = {}
            variable_map = frontend.get("sdk_variable_map", {})

            resolved = []
            for url in urls:
                # First pass: resolve mapped variables (e.g., environment → hostname)
                for var_name, mapping in variable_map.items():
                    placeholder = "{{" + var_name + "}}"
                    if placeholder in url and isinstance(mapping, dict):
                        # The map key matches a credential key; look up its value
                        # e.g., var_name="environment_host", mapping has a
                        # "source" key or uses the var_name stem as credential key
                        source_key = mapping.get("_source", var_name)
                        credential_value = settings.get(source_key, "")
                        resolved_value = mapping.get(credential_value, "")
                        if resolved_value:
                            url = url.replace(placeholder, str(resolved_value))

                # Second pass: resolve direct credential substitutions
                for key, value in settings.items():
                    placeholder = "{{" + key.upper() + "}}"
                    if placeholder in url:
                        url = url.replace(placeholder, str(value))
                    # Also try lowercase match
                    placeholder_lower = "{{" + key + "}}"
                    if placeholder_lower in url:
                        url = url.replace(placeholder_lower, str(value))

                resolved.append(url)

            return resolved

        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Error getting SDK dependencies for {component.slug}: {e}")

        return []

    def get_provider_key(self, obj):
        """Get provider slug for handler registry lookup."""
        if obj.provider_account and obj.provider_account.component:
            return obj.provider_account.component.slug
        return None


class PaymentIntentStatusSerializer(serializers.Serializer):
    """
    Response serializer for payment intent status check.
    """

    intent_id = serializers.UUIDField(source="id", help_text=_("Payment intent ID."))
    status = serializers.CharField(help_text=_("Current payment intent status."))
    order_id = serializers.UUIDField(
        source="order.id", required=False, allow_null=True, help_text=_("Order ID.")
    )
    order_number = serializers.CharField(
        source="order.order_number",
        required=False,
        allow_null=True,
        help_text=_("Order number for display."),
    )
    requires_action = serializers.BooleanField(help_text=_("Whether customer action is required."))
    action = serializers.SerializerMethodField(
        help_text=_("Action details if requires_action is true.")
    )
    error = serializers.SerializerMethodField(help_text=_("Error details if payment failed."))

    def get_action(self, obj):
        """Get action details if action required."""
        if obj.requires_action:
            return {
                "type": obj.action_type,
                "url": obj.action_url or None,
                "data": obj.action_data or {},
            }
        return None

    def get_error(self, obj):
        """Get error details if failed."""
        if obj.status == "failed" and (obj.error_code or obj.error_message):
            return {"code": obj.error_code, "message": obj.error_message}
        return None


class ConfirmPaymentIntentSerializer(serializers.Serializer):
    """
    Request serializer for confirming a payment intent.
    """

    payment_method_data = serializers.JSONField(
        required=False,
        default=dict,
        help_text=_("Provider-specific payment method data for confirmation."),
    )


class CancelPaymentIntentSerializer(serializers.Serializer):
    """
    Request serializer for cancelling a payment intent.
    """

    reason = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
        help_text=_("Optional reason for cancellation."),
    )


class PaymentIntentMinimalSerializer(serializers.ModelSerializer):
    """
    Minimal serializer for payment intent lists.
    """

    order_number = serializers.CharField(source="order.order_number", read_only=True)
    provider_name = serializers.CharField(source="provider_account.display_name", read_only=True)

    class Meta:
        model = PaymentIntent
        fields = [
            "id",
            "order_number",
            "provider_name",
            "status",
            "amount",
            "created_at",
            "expires_at",
        ]
        read_only_fields = fields


class SavedPaymentMethodSerializer(serializers.Serializer):
    """
    Serializer for saved payment methods (from subscriptions.PaymentToken).
    """

    id = serializers.UUIDField(source="token_id", read_only=True)
    provider_id = serializers.UUIDField(source="provider_account.id", read_only=True)
    provider_name = serializers.CharField(source="provider_account.display_name", read_only=True)
    payment_method_type = serializers.CharField(read_only=True)
    last_four = serializers.CharField(read_only=True)
    brand = serializers.CharField(read_only=True)
    exp_month = serializers.IntegerField(read_only=True)
    exp_year = serializers.IntegerField(read_only=True)
    is_default = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class CreateSavedPaymentMethodSerializer(serializers.Serializer):
    """
    Request serializer for saving a new payment method.
    """

    provider_id = serializers.UUIDField(help_text=_("Payment provider account ID."))
    payment_method_token = serializers.CharField(
        help_text=_("Token from provider SDK representing the payment method.")
    )
    set_as_default = serializers.BooleanField(
        default=False, help_text=_("Whether to set this as the default payment method.")
    )
