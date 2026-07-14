"""
Admin API Role Management Views

Role CRUD and permission listing endpoints for the merchant mobile app.
"""

import logging
import secrets

from django.contrib.auth.models import Group
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from admin_api.permissions import category_permission
from admin_api.serializers.auth import AdminDataResponseSerializer, ErrorResponseSerializer
from admin_api.serializers.staff import (
    RoleCreateSerializer,
    RoleUpdateSerializer,
    StaffRoleListSerializer,
)
from admin_api.services.audit_service import AuditService
from admin_api.throttling import AdminAPIThrottle, AdminSensitiveOperationThrottle
from core.api.api_descriptions import AUTH_REQUIRED, PERMISSION_DENIED, RATE_LIMIT_EXCEEDED

logger = logging.getLogger(__name__)


def generate_error_reference():
    return f"ERR-{secrets.token_hex(3).upper()}"


@extend_schema(
    tags=["Admin - Roles"],
    summary=_("List all roles"),
    description=_("List all staff roles including built-in and custom roles."),
    responses={
        200: AdminDataResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["GET"])
@permission_classes([category_permission("users", "view")])
@throttle_classes([AdminAPIThrottle])
def role_list(request):
    """List all roles."""
    from staff_roles.models import StaffRole

    roles = StaffRole.objects.all().select_related("group")
    return Response(
        {
            "success": True,
            "data": {
                "roles": StaffRoleListSerializer(roles, many=True).data,
            },
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin - Roles"],
    summary=_("Create a custom role"),
    description=_("Create a new custom role with specified permissions."),
    request=RoleCreateSerializer,
    responses={
        201: AdminDataResponseSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        409: ErrorResponseSerializer,
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["POST"])
@permission_classes([category_permission("users", "full")])
@throttle_classes([AdminSensitiveOperationThrottle])
def role_create(request):
    """Create a custom role."""
    serializer = RoleCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": _("Invalid role data."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    name = serializer.validated_data["name"]
    description = serializer.validated_data.get("description", "")
    permission_categories = serializer.validated_data["permissions"]

    from staff_roles.models import StaffRole

    # Check for duplicate name
    if StaffRole.objects.filter(display_name__iexact=name).exists():
        return Response(
            {
                "success": False,
                "error": {
                    "code": "CONFLICT",
                    "message": _("A role with this name already exists."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_409_CONFLICT,
        )

    with transaction.atomic():
        # Create Django Group
        group = Group.objects.create(
            name=f"role_{name.lower().replace(' ', '_')}_{secrets.token_hex(3)}"
        )

        # Create StaffRole
        role = StaffRole.objects.create(
            group=group,
            display_name=name,
            description=description,
            is_predefined=False,
            permission_categories=permission_categories,
        )

    AuditService.log(
        user=request.user,
        action="role.create",
        resource_type="role",
        resource_id=str(role.id),
        new_value={"name": name, "permissions": permission_categories},
        request=request,
    )

    return Response(
        {
            "success": True,
            "data": StaffRoleListSerializer(role).data,
        },
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    tags=["Admin - Roles"],
    summary=_("Update a custom role"),
    description=_(
        "Update name, description, or permissions of a custom role. Cannot modify built-in roles."
    ),
    request=RoleUpdateSerializer,
    responses={
        200: AdminDataResponseSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        404: ErrorResponseSerializer,
        409: ErrorResponseSerializer,
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["PATCH"])
@permission_classes([category_permission("users", "full")])
@throttle_classes([AdminSensitiveOperationThrottle])
def role_update(request, role_id):
    """Update a custom role."""
    from staff_roles.models import StaffRole

    try:
        role = StaffRole.objects.select_related("group").get(id=role_id)
    except StaffRole.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": _("Role not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    if role.is_predefined:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "CONFLICT",
                    "message": _("Cannot modify a built-in role."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_409_CONFLICT,
        )

    serializer = RoleUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": _("Invalid role data."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    old_values = {}
    new_values = {}

    with transaction.atomic():
        if "name" in serializer.validated_data:
            old_values["name"] = role.display_name
            role.display_name = serializer.validated_data["name"]
            new_values["name"] = role.display_name

        if "description" in serializer.validated_data:
            old_values["description"] = role.description
            role.description = serializer.validated_data["description"]
            new_values["description"] = role.description

        if "permissions" in serializer.validated_data:
            old_values["permissions"] = role.permission_categories
            role.permission_categories = serializer.validated_data["permissions"]
            new_values["permissions"] = role.permission_categories

        role.save()  # triggers sync_permissions()

    # Invalidate cache for all users in this role
    from staff_roles.services import invalidate_user_cache

    for user in role.group.user_set.all():
        invalidate_user_cache(user)

    AuditService.log(
        user=request.user,
        action="role.update",
        resource_type="role",
        resource_id=str(role.id),
        old_value=old_values,
        new_value=new_values,
        request=request,
    )

    return Response(
        {
            "success": True,
            "data": StaffRoleListSerializer(role).data,
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin - Roles"],
    summary=_("Delete a custom role"),
    description=_("Delete a custom role. Cannot delete built-in roles."),
    responses={
        204: None,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        404: ErrorResponseSerializer,
        409: ErrorResponseSerializer,
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["DELETE"])
@permission_classes([category_permission("users", "full")])
@throttle_classes([AdminSensitiveOperationThrottle])
def role_delete(request, role_id):
    """Delete a custom role."""
    from staff_roles.models import StaffRole

    try:
        role = StaffRole.objects.select_related("group").get(id=role_id)
    except StaffRole.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": _("Role not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    if role.is_predefined:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "CONFLICT",
                    "message": _("Cannot delete a built-in role."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_409_CONFLICT,
        )

    role_name = role.display_name
    role_id_val = role.id

    # Invalidate cache for affected users before deletion
    from staff_roles.services import invalidate_user_cache

    for user in role.group.user_set.all():
        invalidate_user_cache(user)

    with transaction.atomic():
        group = role.group
        role.delete()
        group.delete()

    AuditService.log(
        user=request.user,
        action="role.delete",
        resource_type="role",
        resource_id=str(role_id_val),
        old_value={"name": role_name},
        request=request,
    )

    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["Admin - Roles"],
    summary=_("List all available permissions"),
    description=_("List all permission categories and their access levels for role editing UIs."),
    responses={
        200: AdminDataResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["GET"])
@permission_classes([category_permission("users", "view")])
@throttle_classes([AdminAPIThrottle])
def permissions_list(request):
    """List all available permission categories."""
    from staff_roles.categories import PERMISSION_CATEGORIES

    modules = []
    for key, category in sorted(PERMISSION_CATEGORIES.items(), key=lambda x: x[1]["sort_order"]):
        modules.append(
            {
                "name": key,
                "display_name": str(category["label"]),
                "description": str(category["description"]),
                "icon": category["icon"],
                "levels": ["none", "view", "full"],
            }
        )

    return Response(
        {
            "success": True,
            "data": {
                "modules": modules,
            },
        },
        status=status.HTTP_200_OK,
    )
