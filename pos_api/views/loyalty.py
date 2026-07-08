"""
POS Loyalty API views.

Thin wrapper around existing loyalty services for POS frontend integration.
"""
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

from admin_api.authentication import MobileTokenAuthentication
from pos_api.permissions import IsStaffUser
from core.api.api_descriptions import AUTH_REQUIRED, POS_LICENSE_REQUIRED, CUSTOMER_NOT_FOUND


@extend_schema(
    summary=_("Get customer loyalty info"),
    description=_(
        "Retrieve loyalty membership status, tier, and points balance for a customer. "
        "Returns `is_member: false` if the customer has no active loyalty membership. "
        "Requires staff authentication and valid POS license."
    ),
    responses={
        200: OpenApiResponse(
            description=_(
                "Loyalty membership info. `is_member` indicates whether the "
                "customer has an active membership. When true, includes `tier_name`, "
                "`tier_color`, and `available_points`."
            )
        ),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        404: OpenApiResponse(description=CUSTOMER_NOT_FOUND),
    },
    tags=['POS - Customers'],
)
@api_view(['GET'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def loyalty_member(request, customer_id):
    """Get loyalty membership info for a customer."""
    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        user = User.objects.get(pk=customer_id)
    except User.DoesNotExist:
        return Response(
            {'success': False, 'error': {'code': 'NOT_FOUND'}},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        member = user.loyalty_member
    except Exception:
        return Response({
            'success': True,
            'is_member': False,
        })

    if not member or not member.is_active:
        return Response({
            'success': True,
            'is_member': False,
        })

    # Get balance
    available_points = 0
    try:
        from loyalty.models import LoyaltyBalance
        balance = LoyaltyBalance.objects.filter(member=member).first()
        if balance:
            available_points = balance.available_points
    except Exception:
        pass

    # Get tier info
    tier_name = None
    tier_color = None
    if member.current_tier:
        tier_name = str(member.current_tier.name)
        tier_color = getattr(member.current_tier, 'color', None)

    return Response({
        'success': True,
        'is_member': True,
        'tier_name': tier_name,
        'tier_color': tier_color,
        'available_points': available_points,
    })


@extend_schema(
    summary=_("Preview loyalty points for cart"),
    description=_(
        "Calculate the loyalty points a customer would earn for a given cart total. "
        "Returns 0 if the customer has no active loyalty membership. "
        "Requires staff authentication and valid POS license."
    ),
    parameters=[
        OpenApiParameter(
            "cart_total", OpenApiTypes.STR,
            description=_("Cart total as a decimal string (e.g. '49.99'). Defaults to '0'."),
        ),
    ],
    responses={
        200: OpenApiResponse(
            description=_(
                "Points preview. `points_preview` is the number of points "
                "the customer would earn for the given cart total."
            )
        ),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=['POS - Customers'],
)
@api_view(['GET'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def loyalty_preview(request, customer_id):
    """Preview loyalty points that would be earned for a given cart total."""
    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        user = User.objects.get(pk=customer_id)
        member = user.loyalty_member
    except Exception:
        return Response({
            'success': True,
            'points_preview': 0,
        })

    if not member or not member.is_active:
        return Response({
            'success': True,
            'points_preview': 0,
        })

    cart_total = request.query_params.get('cart_total', '0')

    try:
        from decimal import Decimal
        from loyalty.services.points_engine import PointsEngine

        # Build a minimal mock order-like object for calculation
        class MockOrder:
            def __init__(self, total):
                self.total_amount = total
                self.subtotal = total
                self.id = 0

        mock = MockOrder(Decimal(str(cart_total)))
        engine = PointsEngine()
        result = engine.calculate_order_points(mock, member)
        return Response({
            'success': True,
            'points_preview': result.get('total_points', 0),
        })
    except Exception:
        return Response({
            'success': True,
            'points_preview': 0,
        })
