"""
Admin API Branding Views

Store branding settings management endpoints: get/update branding info
and logo upload for the merchant mobile app.
"""
import logging
import secrets

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from core.models import SiteSettings
from media_library.models import MediaAsset
from admin_api.permissions import category_permission
from admin_api.throttling import AdminAPIThrottle, AdminSensitiveOperationThrottle
from admin_api.services.audit_service import AuditService
from admin_api.serializers.branding import (
    BrandingSettingsResponseSerializer,
    BrandingSettingsUpdateSerializer,
    BrandingLogoUploadSerializer,
)
from admin_api.serializers.auth import ErrorResponseSerializer
from core.api.api_descriptions import AUTH_REQUIRED, PERMISSION_DENIED, RATE_LIMIT_EXCEEDED

logger = logging.getLogger(__name__)


def generate_error_reference():
    """Generate a unique error reference for debugging."""
    return f"ERR-{secrets.token_hex(3).upper()}"


def _get_site_settings():
    """Get or create the SiteSettings singleton."""
    site_settings = SiteSettings.objects.first()
    if not site_settings:
        site_settings = SiteSettings.objects.create()
    return site_settings


def _get_logo_url(site_settings):
    """Get the logo URL from SiteSettings, returning None if not set."""
    if not site_settings.site_logo:
        return None
    try:
        logo = site_settings.site_logo
        # Prefer WebP version, fall back to original
        if hasattr(logo, 'webp_file') and logo.webp_file:
            return logo.webp_file.url
        if hasattr(logo, 'original_file') and logo.original_file:
            return logo.original_file.url
        return None
    except Exception:
        return None


def _build_branding_response(site_settings):
    """Build the branding settings response dictionary."""
    return {
        'store_name': site_settings.site_name or '',
        'logo_url': _get_logo_url(site_settings),
        'primary_color': getattr(site_settings, 'primary_color', ''),
        'invoice_footer_text': getattr(site_settings, 'invoice_footer_text', ''),
        'packing_slip_footer_text': getattr(site_settings, 'packing_slip_footer_text', ''),
        'tax_id': getattr(site_settings, 'tax_id', ''),
        'business_address': {
            'line1': getattr(site_settings, 'address_line_1', ''),
            'line2': getattr(site_settings, 'address_line_2', ''),
            'city': getattr(site_settings, 'city', ''),
            'state': getattr(site_settings, 'state_province', ''),
            'postal_code': getattr(site_settings, 'postal_code', ''),
            'country': getattr(site_settings, 'country', ''),
        },
        'business_phone': getattr(site_settings, 'phone_number', ''),
        'business_email': getattr(site_settings, 'admin_email', ''),
    }


@extend_schema(
    tags=['Admin - Branding'],
    summary=_("Get branding settings"),
    description=_("""
    Retrieve the store's branding and identity settings.

    **Rate Limit:** 300 requests per minute

    Returns store name, logo URL, colors, document footer texts,
    tax ID, business address, phone, and email.
    """),
    responses={
        200: BrandingSettingsResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    }
)
@api_view(['GET'])
@permission_classes([category_permission('settings', 'view')])
@throttle_classes([AdminAPIThrottle])
def branding_settings_get(request):
    """
    Get store branding settings.
    """
    site_settings = _get_site_settings()
    branding_data = _build_branding_response(site_settings)

    return Response({
        'success': True,
        'data': branding_data
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Admin - Branding'],
    summary=_("Update branding settings"),
    description=_("""
    Update the store's branding and identity settings.

    **Rate Limit:** 30 requests per minute (sensitive operation)

    Only provided fields will be updated. Supports partial updates.

    **Updatable fields:**
    - store_name: Store display name
    - primary_color: Brand color hex code
    - invoice_footer_text: Custom invoice footer
    - packing_slip_footer_text: Custom packing slip footer
    - tax_id: Business tax ID / VAT number
    - business_address: Address object (line1, line2, city, state, postal_code, country)
    - business_phone: Business phone number
    - business_email: Business email address
    """),
    request=BrandingSettingsUpdateSerializer,
    responses={
        200: BrandingSettingsResponseSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    }
)
@api_view(['PATCH'])
@permission_classes([category_permission('settings', 'full')])
@throttle_classes([AdminSensitiveOperationThrottle])
def branding_settings_update(request):
    """
    Update store branding settings.
    """
    serializer = BrandingSettingsUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid branding settings.'),
                'reference': generate_error_reference(),
                'details': serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    site_settings = _get_site_settings()
    data = serializer.validated_data

    old_values = {}
    new_values = {}
    update_fields = []

    # Map API field names to model field names
    field_mapping = {
        'store_name': 'site_name',
        'primary_color': 'primary_color',
        'invoice_footer_text': 'invoice_footer_text',
        'packing_slip_footer_text': 'packing_slip_footer_text',
        'tax_id': 'tax_id',
        'business_phone': 'phone_number',
        'business_email': 'admin_email',
    }

    for api_field, model_field in field_mapping.items():
        if api_field in data:
            old_val = getattr(site_settings, model_field, '')
            new_val = data[api_field]
            if old_val != new_val:
                old_values[api_field] = old_val
                new_values[api_field] = new_val
                setattr(site_settings, model_field, new_val)
                update_fields.append(model_field)

    # Handle nested business_address
    if 'business_address' in data:
        address_data = data['business_address']
        address_field_mapping = {
            'line1': 'address_line_1',
            'line2': 'address_line_2',
            'city': 'city',
            'state': 'state_province',
            'postal_code': 'postal_code',
            'country': 'country',
        }
        for api_field, model_field in address_field_mapping.items():
            if api_field in address_data:
                old_val = getattr(site_settings, model_field, '')
                new_val = address_data[api_field]
                if old_val != new_val:
                    old_values[f'address.{api_field}'] = old_val
                    new_values[f'address.{api_field}'] = new_val
                    setattr(site_settings, model_field, new_val)
                    update_fields.append(model_field)

    if update_fields:
        site_settings.save(update_fields=update_fields)

        AuditService.log(
            user=request.user,
            action='branding.update',
            resource_type='site_settings',
            resource_id='1',
            old_value=old_values,
            new_value=new_values,
            request=request
        )

    branding_data = _build_branding_response(site_settings)

    return Response({
        'success': True,
        'message': _('Branding settings updated successfully.'),
        'data': branding_data
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Admin - Branding'],
    summary=_("Upload branding logo"),
    description=_("""
    Upload a new store logo image.

    **Rate Limit:** 30 requests per minute (sensitive operation)

    Accepts multipart/form-data with an image file.
    Supported formats: JPEG, PNG, GIF, WebP, SVG.

    The uploaded image will be:
    - Stored as a MediaAsset
    - Set as the store's site_logo in SiteSettings
    - Previous logo association is replaced (previous MediaAsset is retained)
    """),
    request={'multipart/form-data': BrandingLogoUploadSerializer},
    responses={
        200: BrandingSettingsResponseSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    }
)
@api_view(['POST'])
@permission_classes([category_permission('settings', 'full')])
@throttle_classes([AdminSensitiveOperationThrottle])
def branding_logo_upload(request):
    """
    Upload a new store logo.
    """
    serializer = BrandingLogoUploadSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid logo upload.'),
                'reference': generate_error_reference(),
                'details': serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    image_file = serializer.validated_data['image']

    try:
        import mimetypes
        from PIL import Image as PILImage

        # Extract image metadata
        mime_type, _ = mimetypes.guess_type(image_file.name)
        width = None
        height = None

        # Only try to open with PIL for raster images (not SVG)
        if mime_type and 'svg' not in mime_type.lower():
            try:
                image_file.seek(0)
                img = PILImage.open(image_file)
                width, height = img.size
                if not mime_type:
                    format_to_mime = {
                        'JPEG': 'image/jpeg',
                        'PNG': 'image/png',
                        'GIF': 'image/gif',
                        'WEBP': 'image/webp',
                    }
                    mime_type = format_to_mime.get(img.format, 'image/png')
                image_file.seek(0)
            except Exception:
                image_file.seek(0)

        if not mime_type:
            mime_type = 'image/png'

        # Create MediaAsset
        media_asset = MediaAsset.objects.create(
            title="Store Logo",
            alt_text="Store Logo",
            original_file=image_file,
            mime_type=mime_type,
            file_size=image_file.size,
            width=width,
            height=height,
            uploaded_by=request.user,
        )

        # Generate WebP version for raster images
        if mime_type and 'svg' not in mime_type.lower():
            try:
                from media_library.services import ImageProcessor
                processor = ImageProcessor()
                image_file.seek(0)
                webp_content = processor.convert_to_webp(image_file)
                if webp_content:
                    media_asset.webp_file.save(
                        f"{media_asset.id}.webp", webp_content, save=True
                    )
            except Exception as e:
                logger.warning(f"WebP conversion failed for logo: {e}")

        # Update SiteSettings
        site_settings = _get_site_settings()
        old_logo_id = str(site_settings.site_logo_id) if site_settings.site_logo_id else None

        site_settings.site_logo = media_asset
        site_settings.save(update_fields=['site_logo'])

        AuditService.log(
            user=request.user,
            action='branding.logo_upload',
            resource_type='site_settings',
            resource_id='1',
            old_value={'logo_media_asset_id': old_logo_id},
            new_value={'logo_media_asset_id': str(media_asset.id)},
            request=request
        )

        branding_data = _build_branding_response(site_settings)

        return Response({
            'success': True,
            'message': _('Logo uploaded successfully.'),
            'data': branding_data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Logo upload failed: {e}", exc_info=True)
        return Response({
            'success': False,
            'error': {
                'code': 500,
                'message': _('Failed to upload logo.'),
                'reference': generate_error_reference()
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
