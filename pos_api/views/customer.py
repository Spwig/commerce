"""
POS Customer API views.

Search, create, and view customer profiles for POS transactions.
Customers are User objects with optional CustomerProfile data.
All endpoints require staff authentication and a valid POS license.
"""

from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db.models import Count, Q, Sum
from django.utils.translation import gettext_lazy as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from admin_api.authentication import MobileTokenAuthentication
from core.api.api_descriptions import (
    AUTH_REQUIRED,
    CUSTOMER_NOT_FOUND,
    INVALID_REQUEST,
    POS_LICENSE_REQUIRED,
)
from pos_api.permissions import IsStaffUser
from pos_api.serializers.customer import (
    POSCustomerCreateSerializer,
    POSCustomerSerializer,
)

User = get_user_model()


def _serialize_customer(user):
    """Build a POS customer response dict from a User object."""
    phone = ""
    if hasattr(user, "profile") and user.profile:
        phone = getattr(user.profile, "phone", "") or ""

    total_orders = 0
    total_spent = "0.00"
    if hasattr(user, "orders"):
        order_stats = user.orders.aggregate(
            count=Count("id"),
            total=Sum("total_amount"),
        )
        total_orders = order_stats["count"] or 0
        total_spent = str(order_stats["total"] or 0)

    return {
        "id": user.id,
        "email": user.email or "",
        "first_name": user.first_name,
        "last_name": user.last_name,
        "full_name": user.get_full_name(),
        "phone": phone,
        "total_orders": total_orders,
        "total_spent": total_spent,
    }


@extend_schema(
    summary=_("Search customers"),
    description=_(
        "Search for customers by email, phone, first name, or last name. "
        "Returns up to 20 matching results. Minimum 2 characters required. "
        "Requires staff authentication and valid POS license."
    ),
    parameters=[
        OpenApiParameter(
            "q",
            OpenApiTypes.STR,
            required=True,
            description=_("Search query (email, phone, or name). Minimum 2 characters."),
        ),
    ],
    responses={
        200: POSCustomerSerializer(many=True),
        400: OpenApiResponse(description=_("Search query too short")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Customers"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def customer_search(request):
    """Search customers by email, phone, or name."""
    q = request.query_params.get("q", "").strip()
    if len(q) < 2:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "QUERY_TOO_SHORT",
                    "message": "Search query must be at least 2 characters.",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    users = (
        User.objects.filter(
            Q(email__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q)
        )
        .filter(
            is_active=True,
            is_staff=False,
        )
        .select_related("profile")[:20]
    )

    results = [_serialize_customer(u) for u in users]
    return Response({"success": True, "results": results, "count": len(results)})


@extend_schema(
    summary=_("Create walk-in customer"),
    description=_(
        "Create a new customer for a walk-in sale. If a customer with the given email "
        "already exists, returns the existing customer instead of creating a duplicate. "
        "Email is optional for truly anonymous walk-in customers. "
        "Requires staff authentication and valid POS license."
    ),
    request=POSCustomerCreateSerializer,
    responses={
        201: POSCustomerSerializer,
        200: OpenApiResponse(description=_("Existing customer found with this email")),
        400: OpenApiResponse(description=INVALID_REQUEST),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Customers"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def customer_create(request):
    """Create a walk-in customer."""
    serializer = POSCustomerCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    email = data.get("email", "").strip()
    first_name = data.get("first_name", "").strip()
    last_name = data.get("last_name", "").strip()
    phone = data.get("phone", "").strip()

    # Check if a customer with this email already exists
    if email:
        try:
            existing = User.objects.select_related("profile").get(email=email)
            return Response(
                {
                    "success": True,
                    "message": "Existing customer found with this email.",
                    "customer": _serialize_customer(existing),
                    "is_existing": True,
                }
            )
        except User.DoesNotExist:
            pass

    # Create new user
    username = email if email else f"pos_walkin_{uuid4().hex[:8]}"
    user = User.objects.create_user(
        username=username,
        email=email or "",
        first_name=first_name,
        last_name=last_name,
        is_staff=False,
    )
    # Set unusable password for walk-in customers
    user.set_unusable_password()
    user.save()

    # Create profile with phone if provided
    if phone:
        from accounts.models import CustomerProfile

        CustomerProfile.objects.update_or_create(
            user=user,
            defaults={"phone": phone},
        )

    return Response(
        {
            "success": True,
            "message": "Customer created.",
            "customer": _serialize_customer(user),
            "is_existing": False,
        },
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    summary=_("Get customer details"),
    description=_(
        "Retrieve customer details including contact info and recent order history. "
        "Requires staff authentication and valid POS license."
    ),
    responses={
        200: POSCustomerSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        404: OpenApiResponse(description=CUSTOMER_NOT_FOUND),
    },
    tags=["POS - Customers"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def customer_detail(request, customer_id):
    """Get customer details with recent order history."""
    try:
        user = User.objects.select_related("profile").get(id=customer_id)
    except User.DoesNotExist:
        return Response(
            {"success": False, "error": {"code": "NOT_FOUND", "message": "Customer not found."}},
            status=status.HTTP_404_NOT_FOUND,
        )

    customer_data = _serialize_customer(user)

    # Add recent orders
    recent_orders = []
    if hasattr(user, "orders"):
        for order in user.orders.order_by("-created_at")[:5]:
            recent_orders.append(
                {
                    "id": order.id,
                    "order_number": order.order_number,
                    "total": str(order.total_amount.amount)
                    if hasattr(order.total_amount, "amount")
                    else str(order.total_amount),
                    "status": order.status,
                    "created_at": order.created_at.isoformat(),
                }
            )

    customer_data["recent_orders"] = recent_orders
    return Response({"success": True, "customer": customer_data})
