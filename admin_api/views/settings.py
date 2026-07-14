"""
Admin API Settings Views

Settings and device management endpoints for the merchant mobile app.
"""

import secrets

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from admin_api.models import DeviceRegistration, MobileAuthToken
from admin_api.permissions import IsStaffWithWritePermission
from admin_api.serializers.auth import ErrorResponseSerializer
from admin_api.serializers.settings import (
    ActiveSessionSerializer,
    AppSettingsSerializer,
    DeviceListSerializer,
    DeviceRegistrationSerializer,
    NotificationPreferencesSerializer,
    UpdatePushTokenSerializer,
)
from admin_api.throttling import AdminAPIThrottle
from core.utils import get_default_currency


def generate_error_reference():
    """Generate a unique error reference for debugging."""
    return f"ERR-{secrets.token_hex(3).upper()}"


@extend_schema(
    tags=["Admin"],
    summary=_("Get app settings"),
    description=_("""
    Get current app settings including user info, store info, and notification preferences.

    **Rate Limit:** 300 requests per minute
    """),
    responses={
        200: AppSettingsSerializer,
        401: ErrorResponseSerializer,
    },
)
@api_view(["GET"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def get_settings(request):
    """
    Get app settings.
    """
    from core.models import SiteSettings

    user = request.user
    current_token = getattr(request, "auth", None)
    device_id = current_token.device_id if current_token else None

    # Get store settings
    try:
        site_settings = SiteSettings.objects.first()
        store_name = site_settings.site_name if site_settings else "Store"
        store_currency = site_settings.default_currency if site_settings else get_default_currency()
        store_timezone = site_settings.timezone if site_settings else "UTC"
    except Exception:
        store_name = "Store"
        store_currency = get_default_currency()
        store_timezone = "UTC"

    # Get notification preferences for current device
    notifications = {
        "notify_new_orders": True,
        "notify_low_stock": True,
        "notify_customer_messages": True,
    }

    if device_id:
        device = DeviceRegistration.objects.filter(user=user, device_id=device_id).first()
        if device:
            notifications = {
                "notify_new_orders": device.notify_new_orders,
                "notify_low_stock": device.notify_low_stock,
                "notify_customer_messages": device.notify_customer_messages,
            }

    # Get user's preferred language
    language = getattr(user, "preferred_language", None) or settings.LANGUAGE_CODE

    return Response(
        {
            "success": True,
            "data": {
                "user_id": user.id,
                "email": user.email,
                "full_name": user.get_full_name() or user.email,
                "store_name": store_name,
                "store_currency": store_currency,
                "store_timezone": store_timezone,
                "language": language,
                "notifications": notifications,
            },
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin"],
    summary=_("Register device for push notifications"),
    description=_("""
    Register a device to receive push notifications.

    **Rate Limit:** 300 requests per minute

    If the device is already registered, updates the push token and preferences.
    """),
    request=DeviceRegistrationSerializer,
    responses={
        200: DeviceListSerializer,
        400: ErrorResponseSerializer,
        401: ErrorResponseSerializer,
    },
)
@api_view(["POST"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def register_device(request):
    """
    Register device for push notifications.
    """
    serializer = DeviceRegistrationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid device registration."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = serializer.validated_data

    # Create or update device registration
    device, created = DeviceRegistration.objects.update_or_create(
        user=request.user,
        device_id=data["device_id"],
        defaults={
            "push_token": data["push_token"],
            "platform": data["platform"],
            "notify_new_orders": data.get("notify_new_orders", True),
            "notify_low_stock": data.get("notify_low_stock", True),
            "notify_customer_messages": data.get("notify_customer_messages", True),
            "is_active": True,
            "failed_attempts": 0,
        },
    )

    return Response(
        {
            "success": True,
            "message": _("Device registered successfully.")
            if created
            else _("Device updated successfully."),
            "data": DeviceListSerializer(device).data,
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin"],
    summary=_("Update push token"),
    description=_("""
    Update the push notification token for the current device.

    **Rate Limit:** 300 requests per minute
    """),
    request=UpdatePushTokenSerializer,
    responses={
        200: DeviceListSerializer,
        400: ErrorResponseSerializer,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
)
@api_view(["POST"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def update_push_token(request):
    """
    Update push notification token for current device.
    """
    current_token = getattr(request, "auth", None)
    if not current_token:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Could not identify current device."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = UpdatePushTokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid push token."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        device = DeviceRegistration.objects.get(
            user=request.user, device_id=current_token.device_id
        )
        device.push_token = serializer.validated_data["push_token"]
        device.is_active = True
        device.failed_attempts = 0
        device.save()

        return Response(
            {
                "success": True,
                "message": _("Push token updated successfully."),
                "data": DeviceListSerializer(device).data,
            },
            status=status.HTTP_200_OK,
        )

    except DeviceRegistration.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Device not registered. Please register device first."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )


@extend_schema(
    tags=["Admin"],
    summary=_("Update notification preferences"),
    description=_("""
    Update notification preferences for the current device.

    **Rate Limit:** 300 requests per minute
    """),
    request=NotificationPreferencesSerializer,
    responses={
        200: NotificationPreferencesSerializer,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
)
@api_view(["POST"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def update_notifications(request):
    """
    Update notification preferences.
    """
    current_token = getattr(request, "auth", None)
    if not current_token:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Could not identify current device."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = NotificationPreferencesSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid notification preferences."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        device = DeviceRegistration.objects.get(
            user=request.user, device_id=current_token.device_id
        )

        # Update only provided fields
        data = serializer.validated_data
        if "notify_new_orders" in data:
            device.notify_new_orders = data["notify_new_orders"]
        if "notify_low_stock" in data:
            device.notify_low_stock = data["notify_low_stock"]
        if "notify_customer_messages" in data:
            device.notify_customer_messages = data["notify_customer_messages"]
        device.save()

        return Response(
            {
                "success": True,
                "message": _("Notification preferences updated successfully."),
                "data": {
                    "notify_new_orders": device.notify_new_orders,
                    "notify_low_stock": device.notify_low_stock,
                    "notify_customer_messages": device.notify_customer_messages,
                },
            },
            status=status.HTTP_200_OK,
        )

    except DeviceRegistration.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Device not registered."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )


@extend_schema(
    tags=["Admin"],
    summary=_("List registered devices"),
    description=_("""
    Get list of all registered devices for the current user.

    **Rate Limit:** 300 requests per minute
    """),
    responses={
        200: DeviceListSerializer(many=True),
        401: ErrorResponseSerializer,
    },
)
@api_view(["GET"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def list_devices(request):
    """
    List all registered devices for current user.
    """
    devices = DeviceRegistration.objects.filter(user=request.user).order_by("-updated_at")

    return Response(
        {"success": True, "data": DeviceListSerializer(devices, many=True).data},
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin"],
    summary=_("Unregister device"),
    description=_("""
    Unregister a device from receiving push notifications.

    **Rate Limit:** 300 requests per minute
    """),
    responses={
        200: dict,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
)
@api_view(["DELETE"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def unregister_device(request, device_id):
    """
    Unregister device from push notifications.
    """
    try:
        device = DeviceRegistration.objects.get(user=request.user, device_id=device_id)
        device.delete()

        return Response(
            {"success": True, "message": _("Device unregistered successfully.")},
            status=status.HTTP_200_OK,
        )

    except DeviceRegistration.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Device not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )


@extend_schema(
    tags=["Admin"],
    summary=_("Get active sessions"),
    description=_("""
    Get list of active sessions (devices with valid tokens) for the current user.

    **Rate Limit:** 300 requests per minute
    """),
    responses={
        200: ActiveSessionSerializer(many=True),
        401: ErrorResponseSerializer,
    },
)
@api_view(["GET"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def active_sessions(request):
    """
    Get active sessions for current user.
    """
    from django.utils import timezone

    current_token = getattr(request, "auth", None)
    current_device_id = current_token.device_id if current_token else None

    # Get unique devices with active refresh tokens
    active_tokens = MobileAuthToken.objects.filter(
        user=request.user, token_type="refresh", is_revoked=False, expires_at__gt=timezone.now()
    ).order_by("-last_used_at", "-created_at")

    # Get device registrations for platform info
    device_registrations = {
        d.device_id: d.platform for d in DeviceRegistration.objects.filter(user=request.user)
    }

    sessions = []
    seen_devices = set()
    for token in active_tokens:
        if token.device_id in seen_devices:
            continue
        seen_devices.add(token.device_id)

        sessions.append(
            {
                "device_id": token.device_id,
                "device_name": token.device_name or f"Device {token.device_id[:8]}",
                "platform": device_registrations.get(token.device_id, ""),
                "is_current": token.device_id == current_device_id,
                "last_used_at": token.last_used_at,
                "last_used_ip": token.last_used_ip,
                "created_at": token.created_at,
            }
        )

    return Response({"success": True, "data": sessions}, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Admin"],
    summary=_("Revoke session"),
    description=_("""
    Revoke all tokens for a specific device (logout that device).

    **Rate Limit:** 300 requests per minute

    Cannot revoke the current device's session using this endpoint.
    """),
    responses={
        200: dict,
        400: ErrorResponseSerializer,
        401: ErrorResponseSerializer,
    },
)
@api_view(["POST"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def revoke_session(request, device_id):
    """
    Revoke session for a specific device.
    """
    current_token = getattr(request, "auth", None)
    if current_token and current_token.device_id == device_id:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Cannot revoke current device session. Use logout instead."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Revoke all tokens for the device
    MobileAuthToken.revoke_all_for_device(
        request.user, device_id, reason="Revoked by user from another device"
    )

    return Response(
        {"success": True, "message": _("Session revoked successfully.")}, status=status.HTTP_200_OK
    )


@extend_schema(
    tags=["Admin"],
    summary=_("Get available languages"),
    description=_("""
    Get list of available languages for the app.

    **Rate Limit:** 300 requests per minute
    """),
    responses={
        200: dict,
        401: ErrorResponseSerializer,
    },
)
@api_view(["GET"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def available_languages(request):
    """
    Get available languages.
    """
    languages = [{"code": code, "name": name} for code, name in settings.LANGUAGES]

    return Response(
        {"success": True, "data": {"current": settings.LANGUAGE_CODE, "available": languages}},
        status=status.HTTP_200_OK,
    )
