"""
Branding Serializers for Admin API

Serializers for store branding settings management.
"""

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class BusinessAddressSerializer(serializers.Serializer):
    """Nested serializer for business address within branding settings."""

    line1 = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        default="",
        help_text=_("Street address line 1."),
    )
    line2 = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        default="",
        help_text=_("Street address line 2."),
    )
    city = serializers.CharField(
        max_length=100, required=False, allow_blank=True, default="", help_text=_("City.")
    )
    state = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        default="",
        help_text=_("State or province."),
    )
    postal_code = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        default="",
        help_text=_("ZIP or postal code."),
    )
    country = serializers.CharField(
        max_length=100, required=False, allow_blank=True, default="", help_text=_("Country.")
    )


class BrandingSettingsResponseSerializer(serializers.Serializer):
    """Serializer for branding settings GET response."""

    store_name = serializers.CharField(help_text=_("Store name displayed in header and emails."))
    logo_url = serializers.CharField(
        allow_null=True, allow_blank=True, help_text=_("URL of the store logo image.")
    )
    primary_color = serializers.CharField(
        allow_blank=True, help_text=_("Primary brand color hex code.")
    )
    invoice_footer_text = serializers.CharField(
        allow_blank=True, help_text=_("Custom footer text for invoices.")
    )
    packing_slip_footer_text = serializers.CharField(
        allow_blank=True, help_text=_("Custom footer text for packing slips.")
    )
    tax_id = serializers.CharField(allow_blank=True, help_text=_("Business tax ID / VAT number."))
    business_address = BusinessAddressSerializer(help_text=_("Business address details."))
    business_phone = serializers.CharField(allow_blank=True, help_text=_("Business phone number."))
    business_email = serializers.CharField(allow_blank=True, help_text=_("Business email address."))


class BrandingSettingsUpdateSerializer(serializers.Serializer):
    """Serializer for branding settings PATCH update."""

    store_name = serializers.CharField(
        max_length=100, required=False, help_text=_("Store name displayed in header and emails.")
    )
    primary_color = serializers.CharField(
        max_length=7,
        required=False,
        allow_blank=True,
        help_text=_("Primary brand color hex code (e.g., #2c3e50)."),
    )
    invoice_footer_text = serializers.CharField(
        max_length=1000,
        required=False,
        allow_blank=True,
        help_text=_("Custom footer text for invoices."),
    )
    packing_slip_footer_text = serializers.CharField(
        max_length=1000,
        required=False,
        allow_blank=True,
        help_text=_("Custom footer text for packing slips."),
    )
    tax_id = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True,
        help_text=_("Business tax ID / VAT number."),
    )
    business_address = BusinessAddressSerializer(
        required=False, help_text=_("Business address details.")
    )
    business_phone = serializers.CharField(
        max_length=20, required=False, allow_blank=True, help_text=_("Business phone number.")
    )
    business_email = serializers.EmailField(
        required=False, allow_blank=True, help_text=_("Business email address.")
    )


class BrandingLogoUploadSerializer(serializers.Serializer):
    """Serializer for branding logo upload."""

    image = serializers.ImageField(
        help_text=_("Logo image file. Supported formats: JPEG, PNG, GIF, WebP, SVG.")
    )
