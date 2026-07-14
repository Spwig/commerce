"""
Admin API Staff Management Views

Staff member CRUD endpoints for the merchant mobile app.
"""

import logging
import secrets
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from admin_api.models import MobileAuthToken, StaffInvitation
from admin_api.permissions import category_permission
from admin_api.serializers.auth import AdminDataResponseSerializer, ErrorResponseSerializer
from admin_api.serializers.staff import (
    StaffInviteSerializer,
    StaffMemberDetailSerializer,
    StaffMemberListSerializer,
    StaffUpdateSerializer,
)
from admin_api.services.audit_service import AuditService
from admin_api.throttling import AdminAPIThrottle, AdminSensitiveOperationThrottle
from core.api.api_descriptions import AUTH_REQUIRED, PERMISSION_DENIED, RATE_LIMIT_EXCEEDED

User = get_user_model()
logger = logging.getLogger(__name__)


def generate_error_reference():
    return f"ERR-{secrets.token_hex(3).upper()}"


@extend_schema(
    tags=["Admin - Staff"],
    summary=_("List staff members"),
    description=_("List all staff members, paginated and filterable."),
    parameters=[
        OpenApiParameter(name="page", type=int, default=1),
        OpenApiParameter(name="page_size", type=int, default=20),
        OpenApiParameter(name="search", type=str, required=False),
        OpenApiParameter(name="role_id", type=int, required=False),
        OpenApiParameter(name="is_active", type=bool, required=False),
        OpenApiParameter(name="ordering", type=str, default="-date_joined"),
    ],
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
def staff_list(request):
    """List all staff members."""
    queryset = User.objects.filter(is_staff=True)

    # Search filter
    search = request.query_params.get("search", "").strip()
    if search:
        queryset = queryset.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(email__icontains=search)
        )

    # Role filter
    role_id = request.query_params.get("role_id")
    if role_id:
        try:
            from staff_roles.models import StaffRole

            role = StaffRole.objects.get(id=int(role_id))
            queryset = queryset.filter(groups=role.group)
        except (ValueError, StaffRole.DoesNotExist):
            pass

    # Active filter
    is_active = request.query_params.get("is_active")
    if is_active is not None:
        queryset = queryset.filter(is_active=is_active.lower() == "true")

    # Ordering
    ordering = request.query_params.get("ordering", "-date_joined")
    valid_orderings = {
        "first_name",
        "-first_name",
        "email",
        "-email",
        "date_joined",
        "-date_joined",
        "last_login",
        "-last_login",
    }
    if ordering in valid_orderings:
        queryset = queryset.order_by(ordering)
    else:
        queryset = queryset.order_by("-date_joined")

    # Pagination
    try:
        page = max(1, int(request.query_params.get("page", 1)))
    except (ValueError, TypeError):
        page = 1
    try:
        page_size = min(max(1, int(request.query_params.get("page_size", 20))), 100)
    except (ValueError, TypeError):
        page_size = 20

    total_count = queryset.count()
    start = (page - 1) * page_size
    staff_members = queryset[start : start + page_size]

    return Response(
        {
            "success": True,
            "data": {
                "staff": StaffMemberListSerializer(staff_members, many=True).data,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_count": total_count,
                    "total_pages": (total_count + page_size - 1) // page_size
                    if total_count > 0
                    else 0,
                },
            },
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin - Staff"],
    summary=_("Invite a new staff member"),
    description=_("Send an invitation email to a new staff member."),
    request=StaffInviteSerializer,
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
def staff_invite(request):
    """Invite a new staff member by email."""
    serializer = StaffInviteSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": _("Invalid invitation data."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    email = serializer.validated_data["email"]

    # Check if already a staff member
    if User.objects.filter(email=email, is_staff=True).exists():
        return Response(
            {
                "success": False,
                "error": {
                    "code": "CONFLICT",
                    "message": _("This email is already registered as a staff member."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_409_CONFLICT,
        )

    # Validate role IDs
    from staff_roles.models import StaffRole

    group_ids = serializer.validated_data["group_ids"]
    roles = StaffRole.objects.filter(id__in=group_ids)
    if roles.count() != len(group_ids):
        return Response(
            {
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": _("One or more role IDs are invalid."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    with transaction.atomic():
        invitation = StaffInvitation.objects.create(
            email=email,
            first_name=serializer.validated_data["first_name"],
            last_name=serializer.validated_data["last_name"],
            invited_by=request.user,
            token=StaffInvitation.generate_token(),
            group_ids=group_ids,
            expires_at=timezone.now() + timedelta(days=7),
        )

    # Queue invitation email via email_system
    try:
        from core.models import SiteSettings
        from email_system.services.email_sender import EmailSendingService
        from email_system.services.template_renderer import TemplateRenderer

        site_settings = SiteSettings.objects.first()
        store_name = site_settings.site_name if site_settings else "Store"
        site_url = (
            site_settings.site_url.rstrip("/") if site_settings and site_settings.site_url else ""
        )

        renderer = TemplateRenderer()
        context = {
            "first_name": invitation.first_name,
            "store_name": store_name,
            "invited_by": request.user.get_full_name() or request.user.email,
            "invitation_url": f"{site_url}/en/admin/accept-invitation/{invitation.token}/",
            "expires_at": invitation.expires_at,
        }
        subject, html_body, text_body = renderer.render("staff_invitation", context)

        EmailSendingService.queue_email(
            to_email=email,
            subject=subject,
            html_body=html_body,
            text_body=text_body,
            template_type="staff_invitation",
        )
    except Exception as e:
        logger.warning(f"Failed to queue invitation email for {email}: {e}")

    AuditService.log(
        user=request.user,
        action="staff.invite",
        resource_type="staff_invitation",
        resource_id=str(invitation.id),
        new_value={"email": email, "group_ids": group_ids},
        request=request,
    )

    role_data = [{"id": r.id, "name": r.display_name} for r in roles]

    return Response(
        {
            "success": True,
            "data": {
                "id": invitation.id,
                "email": invitation.email,
                "first_name": invitation.first_name,
                "last_name": invitation.last_name,
                "is_active": False,
                "is_owner": False,
                "invitation_sent_at": invitation.created_at.isoformat()
                if invitation.created_at
                else timezone.now().isoformat(),
                "groups": role_data,
            },
        },
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    tags=["Admin - Staff"],
    summary=_("Update a staff member"),
    description=_("Update roles, status, or name of a staff member."),
    request=StaffUpdateSerializer,
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
def staff_update(request, staff_id):
    """Update a staff member's roles and/or status."""
    try:
        staff_user = User.objects.get(id=staff_id, is_staff=True)
    except User.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": _("Staff member not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # Cannot modify the store owner
    if staff_user.is_superuser and staff_user != request.user:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "CONFLICT",
                    "message": _("Cannot modify the store owner."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_409_CONFLICT,
        )

    serializer = StaffUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": _("Invalid update data."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    old_values = {}
    new_values = {}

    with transaction.atomic():
        # Update groups
        if "group_ids" in serializer.validated_data:
            from staff_roles.models import StaffRole

            group_ids = serializer.validated_data["group_ids"]
            roles = StaffRole.objects.filter(id__in=group_ids)
            old_groups = list(staff_user.groups.values_list("id", flat=True))
            staff_user.groups.set([r.group for r in roles])
            old_values["group_ids"] = old_groups
            new_values["group_ids"] = group_ids

            from staff_roles.services import invalidate_user_cache

            invalidate_user_cache(staff_user)

        # Update active status
        if "is_active" in serializer.validated_data:
            old_values["is_active"] = staff_user.is_active
            staff_user.is_active = serializer.validated_data["is_active"]
            new_values["is_active"] = staff_user.is_active

        # Update name fields
        if "first_name" in serializer.validated_data:
            old_values["first_name"] = staff_user.first_name
            staff_user.first_name = serializer.validated_data["first_name"]
            new_values["first_name"] = staff_user.first_name

        if "last_name" in serializer.validated_data:
            old_values["last_name"] = staff_user.last_name
            staff_user.last_name = serializer.validated_data["last_name"]
            new_values["last_name"] = staff_user.last_name

        staff_user.save()

    AuditService.log(
        user=request.user,
        action="staff.update",
        resource_type="staff",
        resource_id=str(staff_user.id),
        old_value=old_values,
        new_value=new_values,
        request=request,
    )

    return Response(
        {
            "success": True,
            "data": StaffMemberDetailSerializer(staff_user).data,
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin - Staff"],
    summary=_("Remove a staff member"),
    description=_("Deactivate and revoke access for a staff member."),
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
def staff_delete(request, staff_id):
    """Remove a staff member (deactivate + revoke tokens)."""
    try:
        staff_user = User.objects.get(id=staff_id, is_staff=True)
    except User.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": _("Staff member not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # Cannot delete yourself
    if staff_user == request.user:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "CONFLICT",
                    "message": _("Cannot remove your own account."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_409_CONFLICT,
        )

    # Cannot delete the store owner
    if staff_user.is_superuser:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "CONFLICT",
                    "message": _("Cannot remove the store owner."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_409_CONFLICT,
        )

    with transaction.atomic():
        staff_user.is_staff = False
        staff_user.is_active = False
        staff_user.save(update_fields=["is_staff", "is_active"])

        # Revoke all mobile tokens
        MobileAuthToken.revoke_all_for_user(staff_user, reason="Staff member removed")

        # Clear groups
        staff_user.groups.clear()

    from staff_roles.services import invalidate_user_cache

    invalidate_user_cache(staff_user)

    AuditService.log(
        user=request.user,
        action="staff.delete",
        resource_type="staff",
        resource_id=str(staff_user.id),
        old_value={"email": staff_user.email, "is_staff": True},
        new_value={"is_staff": False, "is_active": False},
        request=request,
    )

    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["Admin - Staff"],
    summary=_("Accept staff invitation"),
    description=_(
        "GET: Validate an invitation token and return details. "
        "POST: Accept the invitation by setting a password to create the staff account."
    ),
    responses={
        200: AdminDataResponseSerializer,
        400: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
)
@api_view(["GET", "POST"])
@permission_classes([])
@throttle_classes([AdminSensitiveOperationThrottle])
def accept_invitation(request, token):
    """Accept a staff invitation (public endpoint — no auth required)."""
    try:
        invitation = StaffInvitation.objects.select_related("invited_by").get(token=token)
    except StaffInvitation.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": _("Invitation not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    if invitation.is_accepted:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "ALREADY_ACCEPTED",
                    "message": _("This invitation has already been accepted."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if invitation.is_expired:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "EXPIRED",
                    "message": _("This invitation has expired."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    from core.models import SiteSettings

    site_settings = SiteSettings.objects.first()
    store_name = site_settings.site_name if site_settings else "Store"

    if request.method == "GET":
        from staff_roles.models import StaffRole

        roles = StaffRole.objects.filter(id__in=invitation.group_ids)
        return Response(
            {
                "success": True,
                "data": {
                    "valid": True,
                    "email": invitation.email,
                    "first_name": invitation.first_name,
                    "last_name": invitation.last_name,
                    "store_name": store_name,
                    "invited_by": invitation.invited_by.get_full_name()
                    if invitation.invited_by
                    else "",
                    "roles": [{"id": r.id, "name": r.display_name} for r in roles],
                    "expires_at": invitation.expires_at.isoformat(),
                },
            }
        )

    # POST — accept invitation and create user
    password = request.data.get("password", "").strip()
    if not password or len(password) < 8:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": _("Password must be at least 8 characters."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check if email already registered
    if User.objects.filter(email=invitation.email).exists():
        return Response(
            {
                "success": False,
                "error": {
                    "code": "CONFLICT",
                    "message": _("An account with this email already exists."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_409_CONFLICT,
        )

    with transaction.atomic():
        user = User.objects.create_user(
            username=invitation.email,
            email=invitation.email,
            password=password,
            first_name=invitation.first_name,
            last_name=invitation.last_name,
            is_staff=True,
            is_active=True,
        )

        # Assign roles
        from staff_roles.models import StaffRole

        roles = StaffRole.objects.filter(id__in=invitation.group_ids)
        user.groups.set([r.group for r in roles])

        # Mark invitation as accepted
        invitation.is_accepted = True
        invitation.accepted_at = timezone.now()
        invitation.save(update_fields=["is_accepted", "accepted_at"])

    AuditService.log(
        user=user,
        action="staff.invitation_accepted",
        resource_type="staff_invitation",
        resource_id=str(invitation.id),
        new_value={
            "email": user.email,
            "group_ids": invitation.group_ids,
        },
        request=request,
    )

    return Response(
        {
            "success": True,
            "data": {
                "message": _("Invitation accepted. You can now log in."),
                "email": user.email,
            },
        },
        status=status.HTTP_201_CREATED,
    )
