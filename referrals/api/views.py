"""
Referral Program API Views

Public API endpoints for click tracking and referrer dashboard data.
"""

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework import status as drf_status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.api.throttling import ReferralTrackingThrottle

from ..models import ReferralIdentity, ReferralProgram, ReferralReward
from ..services import set_ref_cookie, track_click
from .serializers import TrackClickSerializer


@extend_schema(
    tags=["Referrals"],
    summary=_("Track referral link click"),
    description=_("""Track a referral link click using a referral token. Records visitor IP, user agent, and referrer information.

    Sets a cookie to attribute future conversions to this referral. Cookie TTL is configurable per referral program.

    **Security**: Rate limited to 30 requests/hour per IP to prevent token enumeration, fake click generation, and database spam.

    **Use Case**: Call this endpoint when a visitor lands on your site via a referral link (e.g., ?ref=abc123xyz)."""),
    request=TrackClickSerializer,
    responses={
        200: inline_serializer(
            name="TrackClickResponse",
            fields={
                "success": serializers.BooleanField(),
                "message": serializers.CharField(),
                "referrer": inline_serializer(
                    name="ReferrerInfo",
                    fields={
                        "name": serializers.CharField(allow_null=True),
                        "total_referrals": serializers.IntegerField(),
                    },
                ),
            },
        ),
        400: OpenApiResponse(description=_("Invalid token or missing required fields")),
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([ReferralTrackingThrottle])
def track_click_api(request):
    """
    API endpoint to track referral link clicks.

    POST /api/referrals/click/
    {
        "token": "abc123xyz",
    }

    Returns:
    {
        "success": true,
        "message": "Click tracked successfully",
        "referrer": {
            "name": "John Doe",
            "total_referrals": 5
        }
    }

    Security: Rate limited to 30 requests per hour per IP to prevent:
    - Token enumeration attacks
    - Fake click generation
    - Database spam
    """
    token = request.data.get("token", "").strip()

    if not token:
        return Response(
            {"success": False, "message": _("Token is required")},
            status=drf_status.HTTP_400_BAD_REQUEST,
        )

    # Track the click
    success, identity, message = track_click(token, request)

    if not success:
        return Response(
            {"success": False, "message": message}, status=drf_status.HTTP_400_BAD_REQUEST
        )

    # Prepare response
    response_data = {
        "success": True,
        "message": message,
        "referrer": {
            "name": identity.customer.get_full_name() or identity.customer.email
            if identity
            else None,
            "total_referrals": identity.total_conversions if identity else 0,
        },
    }

    # Create DRF response
    response = Response(response_data)

    # Set referral tracking cookie
    program = ReferralProgram.get_program()
    ttl_days = program.get_cookie_ttl_days()
    set_ref_cookie(response, token, ttl_days)

    return response


@login_required
@require_http_methods(["GET"])
def referrer_dashboard_data(request):
    """
    API endpoint to get referrer dashboard data for logged-in customer.

    GET /api/referrals/me/

    Returns:
    {
        "success": true,
        "referrer": {
            "token": "abc123xyz",
            "referral_link": "https://example.com/?ref=abc123xyz",
            "stats": {
                "total_clicks": 10,
                "total_signups": 5,
                "total_conversions": 3,
                "total_rewards_earned": 30.00,
                "conversion_rate": 30.0
            },
            "rewards": [
                {
                    "id": 1,
                    "amount": 10.00,
                    "currency": "USD",
                    "kind": "credit",
                    "status": "issued",
                    "issued_at": "2025-11-03T10:00:00Z",
                    "expires_at": "2026-02-03T10:00:00Z"
                }
            ]
        }
    }
    """
    try:
        # Get or create referral identity for customer
        identity, created = ReferralIdentity.objects.get_or_create(customer=request.user)

        # Get stats
        stats = {
            "total_clicks": identity.total_clicks,
            "total_signups": identity.total_signups,
            "total_conversions": identity.total_conversions,
            "total_rewards_earned": float(identity.total_rewards_earned),
            "conversion_rate": identity.get_conversion_rate(),
            "signup_rate": identity.get_signup_rate(),
        }

        # Get rewards
        rewards_qs = ReferralReward.objects.filter(
            customer=request.user, recipient_type="referrer"
        ).order_by("-created_at")

        rewards = []
        for reward in rewards_qs:
            rewards.append(
                {
                    "id": reward.id,
                    "amount": float(reward.amount.amount),
                    "currency": str(reward.amount.currency),
                    "kind": reward.kind,
                    "kind_display": reward.get_kind_display(),
                    "status": reward.status,
                    "status_display": reward.get_status_display(),
                    "description": reward.description,
                    "created_at": reward.created_at.isoformat() if reward.created_at else None,
                    "issued_at": reward.issued_at.isoformat() if reward.issued_at else None,
                    "expires_at": reward.expires_at.isoformat() if reward.expires_at else None,
                    "is_expiring_soon": reward.is_expiring_soon(),
                }
            )

        # Get referral link
        referral_link = request.build_absolute_uri("/") + f"?ref={identity.token}"

        response_data = {
            "success": True,
            "referrer": {
                "token": identity.token,
                "referral_link": referral_link,
                "stats": stats,
                "rewards": rewards,
            },
        }

        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({"success": False, "message": f"Error: {str(e)}"}, status=500)
