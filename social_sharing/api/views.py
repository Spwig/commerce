"""
Social Sharing API Views

REST API endpoints for tracking social media shares and retrieving share counts.
"""

import logging

from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework import status as drf_status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    throttle_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.api.authentication import HeadlessAPIMixin
from core.api.throttling import (
    AnonymousSocialTrackingThrottle,
    AuthenticatedUserThrottle,
    SocialTrackingThrottle,
)
from social_sharing.api.serializers import TrackShareSerializer
from social_sharing.models import ShareCount, SocialShare

logger = logging.getLogger(__name__)


def _get_client_ip(request):
    """Extract client IP from request headers"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def _detect_device_type(user_agent):
    """Simple device type detection from user agent"""
    user_agent_lower = user_agent.lower()
    if (
        "mobile" in user_agent_lower
        or "android" in user_agent_lower
        or "iphone" in user_agent_lower
    ):
        return SocialShare.DEVICE_MOBILE
    elif "tablet" in user_agent_lower or "ipad" in user_agent_lower:
        return SocialShare.DEVICE_TABLET
    elif any(browser in user_agent_lower for browser in ["chrome", "firefox", "safari", "edge"]):
        return SocialShare.DEVICE_DESKTOP
    return SocialShare.DEVICE_UNKNOWN


# Whitelist of content types that are allowed to be shared.
#
# Only models that represent public, customer-facing storefront content
# may be targeted by share tracking. This prevents attackers from:
#   - Creating SocialShare rows against sensitive internal models
#     (User, Session, AdminLog, payment records, etc.)
#   - Enumerating internal model names to probe the schema
#   - Polluting aggregate share counts on models that have no
#     user-facing share button in the first place
#
# Each entry is an explicit (app_label, model) pair so the resolution is
# deterministic across all installations — even ones where a third-party
# provider package registers a model with the same bare name. The bare
# model name below is the public wire format accepted by the API.
SHAREABLE_CONTENT_TYPES: dict[str, tuple[str, str]] = {
    "product": ("catalog", "product"),
    "category": ("catalog", "category"),
    "brand": ("catalog", "brand"),
    "collection": ("catalog", "collection"),
    "blogpost": ("blog", "blogpost"),
    "page": ("page_builder", "page"),
}


def _resolve_shareable_content_type(content_type_str):
    """
    Resolve a user-supplied content_type string to a ContentType instance,
    enforcing the SHAREABLE_CONTENT_TYPES whitelist deterministically.

    Accepts either:
      - Bare lowercase model name: "product"
      - Fully qualified form: "catalog.product"

    Resolution goes through the explicit (app_label, model) map — never
    via `ContentType.objects.filter(model=X).first()` — so the same input
    always points at the same first-party Spwig model, even in
    installations where third-party apps register a same-named model.

    Returns the ContentType instance on success, or None if rejected.
    """
    ct_str = (content_type_str or "").strip().lower()
    if not ct_str:
        return None

    # Parse app_label.model OR bare model — both forms must match the
    # whitelist's explicit (app_label, model) tuple.
    if "." in ct_str:
        try:
            app_label, model = ct_str.split(".", 1)
        except ValueError:
            return None
    else:
        model = ct_str
        app_label = None

    expected = SHAREABLE_CONTENT_TYPES.get(model)
    if expected is None:
        return None
    # If a qualified form was passed, reject app_label mismatches
    if app_label is not None and app_label != expected[0]:
        return None

    try:
        return ContentType.objects.get(app_label=expected[0], model=expected[1])
    except ContentType.DoesNotExist:
        return None


def _target_object_exists(content_type, object_id):
    """Verify the referenced object actually exists in the target model.

    Prevents orphan SocialShare rows (dangling FKs from enumeration attacks)
    and filters out share events for deleted or nonexistent content.
    """
    try:
        model = content_type.model_class()
        if model is None:
            return False
        return model.objects.filter(pk=object_id).exists()
    except Exception:
        return False


@extend_schema(
    tags=["Social Sharing"],
    summary=_("Track social media share"),
    description=_("""Track a social media share event for a product or other content. Records platform, URL, user, session, IP, and device type.

    Use this endpoint when a user shares content to social media platforms. Helps measure content virality and track most-shared products.

    **Supported Platforms**: facebook, twitter, linkedin, pinterest, whatsapp, telegram, email

    **Security**: Authentication required to prevent spam and database pollution. Rate limited to 50 requests/hour per user.

    **Use Case**: Call when user clicks a social share button to track sharing behavior and measure content engagement."""),
    request=TrackShareSerializer,
    responses={
        201: inline_serializer(
            name="TrackShareResponse",
            fields={
                "success": serializers.BooleanField(),
                "share_id": serializers.IntegerField(),
                "message": serializers.CharField(),
            },
        ),
        400: OpenApiResponse(
            description=_("Invalid request, missing required fields, or invalid platform")
        ),
        500: OpenApiResponse(description=_("Internal server error")),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([SocialTrackingThrottle])
def track_share(request):
    """
    Track a social media share event (requires authentication).

    POST /api/social/track/

    Payload is validated via `TrackShareSerializer` which enforces:
      - `url` passes Django `URLValidator` (rejects `javascript:`, `data:`, etc.)
      - `platform` is one of `SocialShare.PLATFORM_CHOICES`
      - `object_id` is an integer
      - `content_type` is a non-empty string

    Additional enforcement in this view:
      - `content_type` must be in `SHAREABLE_CONTENT_TYPES`
      - `object_id` must reference an existing row in the target model
    """
    serializer = TrackShareSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=drf_status.HTTP_400_BAD_REQUEST,
        )

    data = serializer.validated_data
    content_type_str = data["content_type"].lower()
    object_id = data["object_id"]
    platform = data["platform"].lower()
    shared_url = data["url"]

    # Whitelist check — only shareable storefront content types allowed
    content_type = _resolve_shareable_content_type(content_type_str)
    if content_type is None:
        return Response(
            {
                "success": False,
                "error": f"Invalid or non-shareable content_type: {content_type_str}",
            },
            status=drf_status.HTTP_400_BAD_REQUEST,
        )

    # Existence check — prevent orphan rows and ID enumeration
    if not _target_object_exists(content_type, object_id):
        return Response(
            {
                "success": False,
                "error": "Target object does not exist",
            },
            status=drf_status.HTTP_400_BAD_REQUEST,
        )

    # Create share record
    try:
        with transaction.atomic():
            share = SocialShare.objects.create(
                content_type=content_type,
                object_id=object_id,
                platform=platform,
                shared_url=shared_url,
                referrer=request.META.get("HTTP_REFERER", ""),
                user=request.user,  # User is guaranteed to be authenticated
                session_id=request.session.session_key or "",
                ip_address=_get_client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
                device_type=_detect_device_type(request.META.get("HTTP_USER_AGENT", "")),
            )

        logger.info(
            f"Tracked {platform} share of {content_type_str} #{object_id} by {request.user}"
        )

        return Response(
            {"success": True, "share_id": share.id, "message": "Share tracked successfully"},
            status=drf_status.HTTP_201_CREATED,
        )

    except Exception as e:
        logger.error(f"Error tracking share: {e}", exc_info=True)
        return Response(
            {"success": False, "error": "Internal server error"},
            status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@extend_schema(
    tags=["Social Sharing"],
    summary=_("Track social media share (anonymous)"),
    description=_("""Anonymous variant of the share tracking endpoint for guest visitors.

    Identical payload to the authenticated endpoint, but does not require a logged-in user. The resulting `SocialShare` row is stored with `user=None` and is linked only via the visitor's session key, IP, user agent, and device type.

    **Security**: No authentication required, but aggressively rate-limited (20 requests/hour per IP) to prevent spam and database pollution. Bots are not filtered at the endpoint level — consumers should apply their own bot detection if needed.

    **Use Case**: Headless storefronts where most visitors sharing content (product pages, blog posts) are not logged in. The authenticated `track_share` endpoint would exclude all guest shares from analytics, which is the majority of real traffic."""),
    request=TrackShareSerializer,
    responses={
        201: inline_serializer(
            name="TrackAnonymousShareResponse",
            fields={
                "success": serializers.BooleanField(),
                "share_id": serializers.IntegerField(),
                "message": serializers.CharField(),
            },
        ),
        400: OpenApiResponse(
            description=_("Invalid request, missing required fields, or invalid platform")
        ),
        429: OpenApiResponse(description=_("Rate limit exceeded")),
        500: OpenApiResponse(description=_("Internal server error")),
    },
)
@api_view(["POST"])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
@throttle_classes([AnonymousSocialTrackingThrottle])
def track_share_anonymous(request):
    """
    Track a social media share event without requiring authentication.

    POST /api/social/track/anonymous/

    Accepts the same payload as `track_share` but stores `user=None`.
    Rate-limited strictly (20/hour per IP) to prevent spam.

    **Deployment note — trusted proxy requirement:**
        Rate limiting is based on the visitor's IP address. The IP is
        extracted from `HTTP_X_FORWARDED_FOR` (first hop) or `REMOTE_ADDR`.
        This is only safe when the backend is deployed behind a trusted
        reverse proxy (nginx, Cloudflare, ELB) that overwrites
        `X-Forwarded-For` with the real client IP. If the backend is
        exposed directly to the internet without such a proxy, attackers
        can spoof the header to bypass rate limits. Self-hosted
        installations MUST deploy behind a trusted proxy.

    **Validation layering** (defense in depth):
        1. `TrackShareSerializer.is_valid()` — URL validator, platform
           choice field, object_id integer, content_type non-empty.
        2. `SHAREABLE_CONTENT_TYPES` whitelist — rejects non-storefront
           models (User, Session, admin models, etc.).
        3. Target object existence check — prevents orphan rows from
           ID enumeration.
        4. Session is only saved to disk AFTER all validation passes,
           so invalid requests cannot be used to amplify session storage.
    """
    # Step 1 — payload validation (serializer runs URLValidator on `url`,
    # enforces platform choices, coerces object_id to int)
    serializer = TrackShareSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=drf_status.HTTP_400_BAD_REQUEST,
        )

    data = serializer.validated_data
    content_type_str = data["content_type"].lower()
    object_id = data["object_id"]
    platform = data["platform"].lower()
    shared_url = data["url"]

    # Step 2 — whitelist check
    content_type = _resolve_shareable_content_type(content_type_str)
    if content_type is None:
        return Response(
            {
                "success": False,
                "error": f"Invalid or non-shareable content_type: {content_type_str}",
            },
            status=drf_status.HTTP_400_BAD_REQUEST,
        )

    # Step 3 — existence check (prevents orphan rows + ID enumeration)
    if not _target_object_exists(content_type, object_id):
        return Response(
            {
                "success": False,
                "error": "Target object does not exist",
            },
            status=drf_status.HTTP_400_BAD_REQUEST,
        )

    # Step 4 — NOW we can safely persist the visitor's session so the
    # share is linked to their session key (required for funnel
    # attribution). Only valid requests get sessions created — invalid
    # requests cannot be used to amplify session storage.
    if not request.session.session_key:
        request.session.save()

    # Create share record (no user linkage)
    try:
        with transaction.atomic():
            share = SocialShare.objects.create(
                content_type=content_type,
                object_id=object_id,
                platform=platform,
                shared_url=shared_url,
                referrer=request.META.get("HTTP_REFERER", ""),
                user=None,
                session_id=request.session.session_key or "",
                ip_address=_get_client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
                device_type=_detect_device_type(request.META.get("HTTP_USER_AGENT", "")),
            )

        logger.info(f"Tracked anonymous {platform} share of {content_type_str} #{object_id}")

        return Response(
            {"success": True, "share_id": share.id, "message": "Share tracked successfully"},
            status=drf_status.HTTP_201_CREATED,
        )

    except Exception as e:
        logger.error(f"Error tracking anonymous share: {e}", exc_info=True)
        return Response(
            {"success": False, "error": "Internal server error"},
            status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@extend_schema(
    tags=["Social Sharing"],
    summary=_("Get share counts for content"),
    description=_("""Get aggregated share counts by platform for a specific piece of content.

    Returns counts for each social platform plus a total. Useful for displaying share counts on product pages, blog posts, etc.

    **No authentication required** - share counts are public data."""),
    responses={
        200: inline_serializer(
            name="ShareCountsResponse",
            fields={
                "facebook": serializers.IntegerField(),
                "twitter": serializers.IntegerField(),
                "linkedin": serializers.IntegerField(),
                "pinterest": serializers.IntegerField(),
                "whatsapp": serializers.IntegerField(),
                "telegram": serializers.IntegerField(),
                "email": serializers.IntegerField(),
                "total": serializers.IntegerField(),
            },
        ),
        404: OpenApiResponse(description=_("Invalid content type")),
        500: OpenApiResponse(description=_("Internal server error")),
    },
)
@api_view(["GET"])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def get_share_counts(request, content_type_str, object_id):
    """
    Get aggregated share counts for content.

    GET /api/social/counts/<content_type>/<object_id>/
    """
    try:
        # Get ContentType
        try:
            content_type = ContentType.objects.get(model=content_type_str.lower())
        except ContentType.DoesNotExist:
            return Response(
                {"error": f"Invalid content_type: {content_type_str}"},
                status=drf_status.HTTP_404_NOT_FOUND,
            )

        # Get all share counts for this content
        share_counts = ShareCount.objects.filter(content_type=content_type, object_id=object_id)

        # Build response dict with all platforms
        counts = {}
        total = 0

        for platform_code, _platform_name in SocialShare.PLATFORM_CHOICES:
            count = 0
            share_count = share_counts.filter(platform=platform_code).first()
            if share_count:
                count = share_count.count
                total += count
            counts[platform_code] = count

        counts["total"] = total

        return Response(counts)

    except Exception as e:
        logger.error(f"Error retrieving share counts: {e}", exc_info=True)
        return Response(
            {"error": "Internal server error"}, status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    tags=["Social Sharing"],
    summary=_("Get current user's share history"),
    description=_("""Get the authenticated user's social sharing history, including total shares, breakdown by platform, and recent share events.

    **Authentication required.**"""),
    responses={
        200: inline_serializer(
            name="UserSharesResponse",
            fields={
                "total_shares": serializers.IntegerField(),
                "by_platform": serializers.DictField(child=serializers.IntegerField()),
                "recent_shares": serializers.ListField(child=serializers.DictField()),
            },
        ),
        401: OpenApiResponse(description=_("Authentication required")),
        500: OpenApiResponse(description=_("Internal server error")),
    },
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
@throttle_classes([AuthenticatedUserThrottle])
def get_user_shares(request):
    """
    Get current user's share history.

    GET /api/social/user/shares/
    """
    try:
        # Get user's shares
        shares = SocialShare.objects.filter(user=request.user)
        total_shares = shares.count()

        # Count by platform
        by_platform = {}
        for platform_code, _platform_name in SocialShare.PLATFORM_CHOICES:
            count = shares.filter(platform=platform_code).count()
            by_platform[platform_code] = count

        # Get recent shares (last 10)
        recent_shares = []
        for share in shares.select_related("content_type").order_by("-shared_at")[:10]:
            recent_shares.append(
                {
                    "id": share.id,
                    "platform": share.platform,
                    "content_type": share.content_type.model,
                    "object_id": share.object_id,
                    "shared_at": share.shared_at.isoformat(),
                }
            )

        return Response(
            {
                "total_shares": total_shares,
                "by_platform": by_platform,
                "recent_shares": recent_shares,
            }
        )

    except Exception as e:
        logger.error(f"Error retrieving user shares: {e}", exc_info=True)
        return Response(
            {"error": "Internal server error"}, status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR
        )
