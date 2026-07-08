"""
License Key API Views

Provides public API endpoints for license validation, activation, and management.
These endpoints are designed to be called by client software for license verification.
"""
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema, OpenApiResponse
from core.api.api_descriptions import INVALID_REQUEST, NOT_FOUND

from .models import (
    LicenseKey,
    LicenseActivation,
    LicensePool,
    Product,
)
from .license_serializers import (
    LicenseKeySerializer,
    LicenseValidationRequestSerializer,
    LicenseValidationResponseSerializer,
    LicenseActivationRequestSerializer,
    LicenseActivationResponseSerializer,
    LicenseDeactivationRequestSerializer,
    LicenseDeactivationResponseSerializer,
    LicensePoolSerializer,
    BulkGenerateRequestSerializer,
    BulkGenerateResponseSerializer,
    LicenseInfoRequestSerializer,
)
from .services.license_sync import LicenseProviderService
from .services.webhook_dispatcher import LicenseWebhookDispatcher, LicenseWebhookEvents

import logging

logger = logging.getLogger(__name__)


@extend_schema(
    tags=['Licenses'],
    summary=_("Validate a license key"),
    description=_("""
    Validate a license key without activating it.

    This endpoint checks:
    - License key exists and is valid format
    - License is active (not suspended, expired, or revoked)
    - License has not exceeded expiration date
    - Optionally validates key is for a specific product

    **Public endpoint** - no authentication required.
    Use this for quick validation checks before activation.
    """),
    request=LicenseValidationRequestSerializer,
    responses={
        200: LicenseValidationResponseSerializer,
        400: OpenApiResponse(description=INVALID_REQUEST),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def validate_license(request):
    """
    Validate a license key.

    Request body:
    {
        "key": "XXXX-XXXX-XXXX-XXXX",
        "product_id": 123  # Optional
    }
    """
    serializer = LicenseValidationRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            'valid': False,
            'message': 'Invalid request',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    key = serializer.validated_data['key']
    product_id = serializer.validated_data.get('product_id')

    try:
        # Get license key
        license_key = LicenseKey.objects.select_related(
            'order_item__product',
            'digital_asset',
            'user'
        ).get(key=key)

        # Check product match if specified
        if product_id:
            if license_key.order_item and license_key.order_item.product_id != product_id:
                return Response({
                    'valid': False,
                    'message': 'License key is not valid for this product',
                    'license_info': None
                })

        # Check status
        if license_key.status != 'active':
            return Response({
                'valid': False,
                'message': f'License is {license_key.status}',
                'license_info': LicenseKeySerializer(license_key).data
            })

        # Check expiration
        if not license_key.is_lifetime and license_key.expires_at:
            if timezone.now() > license_key.expires_at:
                # Auto-update status to expired
                license_key.status = 'expired'
                license_key.save(update_fields=['status'])

                return Response({
                    'valid': False,
                    'message': 'License has expired',
                    'license_info': LicenseKeySerializer(license_key).data
                })

        # Valid license
        return Response({
            'valid': True,
            'message': 'License is valid',
            'license_info': LicenseKeySerializer(license_key).data
        })

    except LicenseKey.DoesNotExist:
        return Response({
            'valid': False,
            'message': 'License key not found',
            'license_info': None
        })


@extend_schema(
    tags=['Licenses'],
    summary=_("Activate a license on a device"),
    description=_("""
    Activate a license key on a specific device.

    This endpoint:
    - Validates the license key
    - Checks activation limits
    - Registers the device with a unique fingerprint
    - Tracks IP address and device information
    - Dispatches webhook events
    - Syncs to external providers (if configured)

    **Public endpoint** - no authentication required.

    **Device Fingerprint:** Should be a unique, stable identifier for the device.
    Recommended format: hash of (CPU ID + MAC address + motherboard serial) or similar.
    """),
    request=LicenseActivationRequestSerializer,
    responses={
        200: LicenseActivationResponseSerializer,
        400: OpenApiResponse(description=_("Invalid request or activation failed")),
        404: OpenApiResponse(description=_("License not found")),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def activate_license(request):
    """
    Activate a license on a device.

    Request body:
    {
        "key": "XXXX-XXXX-XXXX-XXXX",
        "device_fingerprint": "unique-device-id",
        "device_name": "John's MacBook Pro",  # Optional
        "device_info": {  # Optional
            "os": "macOS 13.1",
            "version": "1.2.0",
            "hostname": "johns-macbook.local"
        }
    }
    """
    serializer = LicenseActivationRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            'success': False,
            'message': 'Invalid request',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    key = serializer.validated_data['key']
    device_fingerprint = serializer.validated_data['device_fingerprint']
    device_name = serializer.validated_data.get('device_name', '')
    device_info = serializer.validated_data.get('device_info', {})

    try:
        # Get license key
        license_key = LicenseKey.objects.select_related('order_item__product').get(key=key)

        # Validate license status
        if license_key.status != 'active':
            return Response({
                'success': False,
                'message': f'License is {license_key.status}',
                'license_info': LicenseKeySerializer(license_key).data
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check expiration
        if not license_key.is_lifetime and license_key.expires_at:
            if timezone.now() > license_key.expires_at:
                license_key.status = 'expired'
                license_key.save(update_fields=['status'])

                return Response({
                    'success': False,
                    'message': 'License has expired',
                    'license_info': LicenseKeySerializer(license_key).data
                }, status=status.HTTP_400_BAD_REQUEST)

        # Check if device already activated
        existing_activation = LicenseActivation.objects.filter(
            license_key=license_key,
            device_fingerprint=device_fingerprint,
            is_active=True
        ).first()

        if existing_activation:
            # Update last verified timestamp
            existing_activation.last_verified_at = timezone.now()
            existing_activation.save(update_fields=['last_verified_at'])

            return Response({
                'success': True,
                'message': 'Device already activated',
                'activation': LicenseActivationSerializer(existing_activation).data,
                'license_info': LicenseKeySerializer(license_key).data
            })

        # Check activation limits
        if license_key.current_activations >= license_key.max_activations:
            return Response({
                'success': False,
                'message': f'Maximum activations ({license_key.max_activations}) reached',
                'license_info': LicenseKeySerializer(license_key).data
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get client IP
        ip_address = request.META.get('REMOTE_ADDR', '')

        # Create activation
        activation = LicenseActivation.objects.create(
            license_key=license_key,
            device_fingerprint=device_fingerprint,
            device_name=device_name or device_fingerprint[:50],
            ip_address=ip_address,
            device_info=device_info,
            is_active=True
        )

        # Update license key counts
        license_key.current_activations += 1
        if not license_key.first_activated_at:
            license_key.first_activated_at = timezone.now()
        license_key.last_activated_at = timezone.now()
        license_key.save(update_fields=['current_activations', 'first_activated_at', 'last_activated_at'])

        # Dispatch webhook event
        try:
            LicenseWebhookDispatcher.dispatch(
                LicenseWebhookEvents.LICENSE_ACTIVATED,
                license_key,
                activation=activation
            )
        except Exception as e:
            logger.exception(f"Error dispatching license activation webhook: {e}")

        # Sync to external provider if configured
        try:
            from .models import LicenseProvider
            active_providers = LicenseProvider.objects.filter(
                is_active=True,
                sync_on_activation=True
            )

            for provider in active_providers:
                if license_key.order_item:
                    product_id_str = str(license_key.order_item.product_id)
                    if provider.product_mapping and product_id_str not in provider.product_mapping:
                        continue

                sync_service = LicenseProviderService(provider)
                adapter = sync_service.adapter
                if hasattr(adapter, 'activate_device'):
                    adapter.activate_device(license_key, device_fingerprint, device_info)
        except Exception as e:
            logger.exception(f"Error syncing activation to external providers: {e}")

        return Response({
            'success': True,
            'message': 'License activated successfully',
            'activation': LicenseActivationSerializer(activation).data,
            'license_info': LicenseKeySerializer(license_key).data
        })

    except LicenseKey.DoesNotExist:
        return Response({
            'success': False,
            'message': 'License key not found',
        }, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    tags=['Licenses'],
    summary=_("Deactivate a license from a device"),
    description=_("""
    Deactivate a license key from a specific device.

    This frees up an activation slot for use on another device.
    Requires the device fingerprint that was used during activation.

    **Public endpoint** - no authentication required.
    """),
    request=LicenseDeactivationRequestSerializer,
    responses={
        200: LicenseDeactivationResponseSerializer,
        400: OpenApiResponse(description=_("Invalid request or deactivation failed")),
        404: OpenApiResponse(description=_("License or activation not found")),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def deactivate_license(request):
    """
    Deactivate a license from a device.

    Request body:
    {
        "key": "XXXX-XXXX-XXXX-XXXX",
        "device_fingerprint": "unique-device-id"
    }
    """
    serializer = LicenseDeactivationRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            'success': False,
            'message': 'Invalid request',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    key = serializer.validated_data['key']
    device_fingerprint = serializer.validated_data['device_fingerprint']

    try:
        # Get license key
        license_key = LicenseKey.objects.get(key=key)

        # Find activation
        activation = LicenseActivation.objects.filter(
            license_key=license_key,
            device_fingerprint=device_fingerprint,
            is_active=True
        ).first()

        if not activation:
            return Response({
                'success': False,
                'message': 'No active activation found for this device',
                'license_info': LicenseKeySerializer(license_key).data
            }, status=status.HTTP_404_NOT_FOUND)

        # Deactivate
        activation.is_active = False
        activation.save(update_fields=['is_active'])

        # Update license key count
        license_key.current_activations = max(0, license_key.current_activations - 1)
        license_key.save(update_fields=['current_activations'])

        # Dispatch webhook event
        try:
            LicenseWebhookDispatcher.dispatch(
                LicenseWebhookEvents.LICENSE_DEACTIVATED,
                license_key,
                activation=activation
            )
        except Exception as e:
            logger.exception(f"Error dispatching license deactivation webhook: {e}")

        # Sync to external provider if configured
        try:
            from .models import LicenseProvider
            active_providers = LicenseProvider.objects.filter(
                is_active=True,
                sync_on_deactivation=True
            )

            for provider in active_providers:
                if license_key.order_item:
                    product_id_str = str(license_key.order_item.product_id)
                    if provider.product_mapping and product_id_str not in provider.product_mapping:
                        continue

                sync_service = LicenseProviderService(provider)
                adapter = sync_service.adapter
                if hasattr(adapter, 'deactivate_device'):
                    adapter.deactivate_device(license_key, device_fingerprint)
        except Exception as e:
            logger.exception(f"Error syncing deactivation to external providers: {e}")

        return Response({
            'success': True,
            'message': 'License deactivated successfully',
            'license_info': LicenseKeySerializer(license_key).data
        })

    except LicenseKey.DoesNotExist:
        return Response({
            'success': False,
            'message': 'License key not found',
        }, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    tags=['Licenses'],
    summary=_("Get license information"),
    description=_("""
    Retrieve detailed information about a license key.

    Returns license status, activation details, expiration info, and activation history.

    **Public endpoint** - no authentication required.
    """),
    responses={
        200: LicenseKeySerializer,
        404: OpenApiResponse(description=_("License not found")),
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_license_info(request, key):
    """
    Get license information by key.

    URL: /api/catalog/licenses/{key}/info/
    """
    try:
        license_key = LicenseKey.objects.prefetch_related('activations').get(key=key)
        serializer = LicenseKeySerializer(license_key)
        return Response(serializer.data)

    except LicenseKey.DoesNotExist:
        return Response({
            'error': 'License key not found'
        }, status=status.HTTP_404_NOT_FOUND)


# ============================================================================
# Admin License Pool Management Endpoints
# ============================================================================

@extend_schema(
    tags=['Licenses - Admin'],
    summary=_("List license pools"),
    description=_("List all license pools. **Admin only.**"),
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_license_pools(request):
    """
    List all license pools with generation status.
    """
    pools = LicensePool.objects.select_related('product', 'license_template').all()
    serializer = LicensePoolSerializer(pools, many=True)
    return Response({
        'success': True,
        'pools': serializer.data
    })


@extend_schema(
    tags=['Licenses - Admin'],
    summary=_("Get license pool details"),
    description=_("Get details of a specific license pool. **Admin only.**"),
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_license_pool(request, pool_id):
    """
    Get license pool details.
    """
    pool = get_object_or_404(LicensePool, id=pool_id)
    serializer = LicensePoolSerializer(pool)
    return Response({
        'success': True,
        'pool': serializer.data
    })


@extend_schema(
    tags=['Licenses - Admin'],
    summary=_("Bulk generate license keys"),
    description=_("""
    Generate license keys in bulk for a license pool.

    This endpoint can be used to:
    - Generate all remaining keys for a pool
    - Generate a specific number of additional keys

    **Admin only.**
    **May run as background task for large batches (>1000 keys).**
    """),
    request=BulkGenerateRequestSerializer,
    responses={
        200: BulkGenerateResponseSerializer,
        400: OpenApiResponse(description=INVALID_REQUEST),
        404: OpenApiResponse(description=_("Pool not found")),
    }
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def bulk_generate_licenses(request):
    """
    Bulk generate license keys for a pool.

    Request body:
    {
        "pool_id": 123,
        "count": 100  # Optional, defaults to pool.total_keys - pool.keys_generated
    }
    """
    from .services.license_generator import LicenseKeyGenerator
    from django.db import transaction

    serializer = BulkGenerateRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            'success': False,
            'message': 'Invalid request',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    pool_id = serializer.validated_data['pool_id']
    count = serializer.validated_data.get('count')

    pool = get_object_or_404(LicensePool, id=pool_id)

    # Calculate count if not provided
    if count is None:
        count = pool.total_keys - pool.keys_generated

    if count <= 0:
        return Response({
            'success': False,
            'message': 'Pool already has all keys generated'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Update pool status
    pool.status = 'generating'
    pool.generation_started_at = timezone.now()
    pool.save(update_fields=['status', 'generation_started_at'])

    # Get template
    template = pool.license_template or pool.product.license_template

    # Generate keys
    generator = LicenseKeyGenerator()
    generated_count = 0
    errors = []

    try:
        with transaction.atomic():
            for i in range(count):
                try:
                    # Prepare context
                    context = {
                        'product_sku': pool.product.sku,
                        'pool_id': pool.id,
                        'sequence': pool.keys_generated + i + 1,
                    }

                    # Generate key
                    key = generator.generate(template, context)

                    # Create license key record
                    LicenseKey.objects.create(
                        license_pool=pool,
                        digital_asset=pool.product.digital_assets.first() if pool.product.digital_assets.exists() else None,
                        key=key,
                        key_type=pool.key_type,
                        max_activations=pool.max_activations,
                        status='active',
                        is_lifetime=(pool.expires_after_days is None)
                    )

                    generated_count += 1
                    pool.keys_generated += 1

                except Exception as e:
                    errors.append(str(e))
                    logger.exception(f"Error generating license key {i+1}: {e}")
                    break

        # Update pool status
        pool.status = 'ready' if pool.keys_generated >= pool.total_keys else 'generating'
        pool.generation_completed_at = timezone.now()
        if errors:
            pool.generation_error = '; '.join(errors)
        pool.save(update_fields=['keys_generated', 'status', 'generation_completed_at', 'generation_error'])

        return Response({
            'success': True,
            'message': f'Generated {generated_count} license keys',
            'pool': LicensePoolSerializer(pool).data,
            'keys_generated': generated_count,
            'errors': errors if errors else None
        })

    except Exception as e:
        pool.status = 'ready'
        pool.generation_error = str(e)
        pool.save(update_fields=['status', 'generation_error'])

        logger.exception(f"Error during bulk license generation: {e}")
        return Response({
            'success': False,
            'message': f'Bulk generation failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
