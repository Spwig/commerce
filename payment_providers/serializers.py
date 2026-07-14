"""
Serializers for Payment Providers
"""

from rest_framework import serializers

from .models import PaymentProviderAccount


class PaymentProviderAccountSerializer(serializers.ModelSerializer):
    """
    Serializer for PaymentProviderAccount.

    Used in checkout flow to display available payment providers.
    """

    provider_name = serializers.CharField(source="component.name", read_only=True)
    provider_slug = serializers.CharField(source="component.slug", read_only=True)
    provider_logo = serializers.SerializerMethodField()
    provider_description = serializers.CharField(source="component.description", read_only=True)

    # Available payment methods for the customer's country
    available_methods = serializers.SerializerMethodField()
    test_mode = serializers.SerializerMethodField()
    publishable_key = serializers.SerializerMethodField()

    class Meta:
        model = PaymentProviderAccount
        fields = [
            "id",
            "provider_name",
            "provider_slug",
            "provider_logo",
            "provider_description",
            "display_name",
            "connection_status",
            "available_methods",
            "is_default",
            "test_mode",
            "publishable_key",
        ]
        read_only_fields = fields

    def get_provider_logo(self, obj):
        """Get provider logo URL"""
        if obj.component and obj.component.logo:
            logo_data = obj.component.logo
            # logo property returns a dict with 'url' key, or could be a FileField
            logo_url = (
                logo_data.get("url")
                if isinstance(logo_data, dict)
                else getattr(logo_data, "url", None)
            )
            if logo_url:
                request = self.context.get("request")
                if request:
                    return request.build_absolute_uri(logo_url)
                return logo_url
        return None

    def get_available_methods(self, obj):
        """
        Get available payment methods for this provider.

        If customer country is provided in context, returns methods for that country.
        Otherwise returns all available methods.
        """
        customer_country = self.context.get("customer_country")

        if customer_country:
            # Get enabled methods for specific country
            enabled_methods = obj.get_enabled_methods_for_country(customer_country)
            return enabled_methods

        # Return all enabled methods across all countries
        all_methods = set()
        for country_methods in obj.enabled_payment_methods.values():
            all_methods.update(country_methods)

        return sorted(all_methods)

    def get_test_mode(self, obj):
        """Return whether provider is in test/sandbox mode."""
        return obj.test_mode

    def get_publishable_key(self, obj):
        """Return the provider's safe-to-publish client-side key.

        For Stripe and Revolut this is the key Stripe.js / Revolut's
        Checkout Widget needs to initialise from the customer's browser
        without going through the storefront's own build. Headless
        storefronts read this from the API response so they don't have
        to bake the key in at build time (every new merchant otherwise
        has to rebuild their storefront with their own key).

        Returns None for providers that don't have a publishable-style
        credential (Airwallex, PayPal, Square use server-side auth only).
        Also returns None on any decryption failure — surfacing a stub
        error in the API response would brick checkout for everybody.
        """
        if not obj.component_id:
            return None
        try:
            from payment_providers.utils.encryption import decrypt_credentials

            creds = decrypt_credentials(obj.credentials_encrypted or {})
        except Exception:
            return None

        slug = obj.component.slug
        test_mode = bool(creds.get("test_mode"))

        if slug == "stripe":
            field = "test_publishable_key" if test_mode else "live_publishable_key"
            return creds.get(field) or None

        if slug == "revolut":
            # Revolut's Checkout Widget uses a single `public_key` (no
            # test/live split in the credential shape).
            return creds.get("public_key") or None

        # Airwallex / PayPal / Square have no publishable-style key.
        return None
