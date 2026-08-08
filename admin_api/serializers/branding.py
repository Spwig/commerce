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
        help_text=_("Street address line 1."),
    )
    line2 = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        help_text=_("Street address line 2."),
    )
    city = serializers.CharField(
        max_length=100, required=False, allow_blank=True, help_text=_("City.")
    )
    state = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        help_text=_("State or province."),
    )
    postal_code = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        help_text=_("ZIP or postal code."),
    )
    country = serializers.CharField(
        max_length=100, required=False, allow_blank=True, help_text=_("Country.")
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

    # Use FileField, not ImageField: Pillow-backed ImageField validation rejects
    # SVG, which this endpoint documents as supported. Content-based validation
    # in validate_image accepts SVG alongside raster formats.
    image = serializers.FileField(
        help_text=_("Logo image file. Supported formats: JPEG, PNG, GIF, WebP, SVG.")
    )

    def validate_image(self, value):
        """Validate the logo by content, allowing raster images and safe SVG.

        Raster uploads are verified against their magic bytes; SVG uploads are
        checked for obviously malicious content and then sanitized to strip
        scripts, event handlers, and external references before storage.
        """
        import os

        import magic
        from django.core.files.base import ContentFile
        from PIL import Image, UnidentifiedImageError

        from media_library.svg_sanitizer import is_svg_safe, sanitize_svg

        allowed_raster_mimes = {"image/jpeg", "image/png", "image/gif", "image/webp"}

        _, ext = os.path.splitext(value.name.lower())
        ext = ext.lstrip(".")

        value.seek(0)
        header = value.read(2048)
        value.seek(0)
        detected_mime = magic.from_buffer(header, mime=True)

        is_svg = detected_mime in ("image/svg+xml", "text/xml", "text/plain") and ext in (
            "svg",
            "svgz",
        )

        if is_svg:
            svg_content = value.read()
            value.seek(0)

            is_safe, reason = is_svg_safe(svg_content)
            if not is_safe:
                raise serializers.ValidationError(
                    _(
                        "SVG file rejected: %(reason)s. Please remove scripts, event "
                        "handlers, and external references before uploading."
                    )
                    % {"reason": reason}
                )

            try:
                sanitized = sanitize_svg(svg_content)
            except ValueError as exc:
                raise serializers.ValidationError(str(exc))

            return ContentFile(sanitized, name=value.name)

        if detected_mime not in allowed_raster_mimes:
            raise serializers.ValidationError(
                _("Unsupported image format. Supported formats: JPEG, PNG, GIF, WebP, SVG.")
            )

        # MIME sniffing only inspects magic bytes, so it accepts corrupt or
        # truncated raster files whose header happens to match. Retain the
        # Pillow-backed decode check the previous ImageField provided.
        try:
            value.seek(0)
            Image.open(value).verify()
        except (UnidentifiedImageError, OSError, ValueError) as exc:
            raise serializers.ValidationError(_("Uploaded file is not a valid image.")) from exc
        finally:
            value.seek(0)

        return value
