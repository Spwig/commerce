"""
DRF API views for announcements endpoints.

Public storefront endpoints for fetching active announcements
and their detail content for modal display.
"""

from django.db.models import Q
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Announcement


def _get_image_url(ann):
    """Resolve the best available image URL for an announcement."""
    if ann.image:
        if ann.image.webp_file:
            return ann.image.webp_file.url
        elif ann.image.original_file:
            return ann.image.original_file.url
    return None


def _get_active_queryset():
    """Return the base queryset for active, non-expired announcements."""
    now = timezone.now()
    return Announcement.objects.filter(
        is_enabled=True,
    ).filter(Q(expires_at__isnull=True) | Q(expires_at__gt=now))


class ActiveAnnouncementsView(APIView):
    """
    List active announcements for storefront display.

    Returns all enabled, non-expired announcements ordered by priority.
    Used by the storefront announcement widget in headers and footers.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        summary=_("List active announcements"),
        description=_(
            "Public endpoint. Returns all enabled, non-expired announcements "
            "ordered by priority ascending, then created_at descending. "
            "Used by the storefront announcement widget."
        ),
        tags=["Announcements"],
        responses={
            200: OpenApiResponse(description=_("List of active announcements")),
        },
    )
    def get(self, request):
        announcements = (
            _get_active_queryset()
            .select_related(
                "image",
                "product_reference",
                "category_reference",
                "blog_post_reference",
                "page_reference",
            )
            .order_by("priority", "-created_at")
        )

        data = []
        for ann in announcements:
            data.append(
                {
                    "id": ann.id,
                    "title": ann.title,
                    "title_plain": strip_tags(ann.title),
                    "show_modal": ann.show_modal,
                    "link_url": ann.get_resolved_url(),
                    "link_text": ann.link_text,
                }
            )

        return Response({"announcements": data})


class AnnouncementDetailView(APIView):
    """
    Get full announcement detail for modal display.

    Returns complete announcement data including body HTML, image URL,
    and display settings. Used by the storefront modal popup.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        summary=_("Get announcement detail"),
        description=_(
            "Public endpoint. Returns full announcement data including body HTML, "
            "image URL, and display mode for the storefront modal. "
            "Returns 404 if the announcement is inactive, expired, or does not exist."
        ),
        tags=["Announcements"],
        parameters=[
            OpenApiParameter(
                "pk",
                int,
                OpenApiParameter.PATH,
                description=_("Announcement primary key"),
            ),
        ],
        responses={
            200: OpenApiResponse(description=_("Announcement detail")),
            404: OpenApiResponse(description=_("Not found, inactive, or expired")),
        },
    )
    def get(self, request, pk):
        try:
            ann = _get_active_queryset().select_related("image").get(pk=pk)
        except Announcement.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        return Response(
            {
                "id": ann.id,
                "title": ann.title,
                "body": ann.body,
                "image_url": _get_image_url(ann),
                "image_display_mode": ann.image_display_mode,
                "image_overlay_opacity": float(ann.image_overlay_opacity),
                "link_url": ann.get_resolved_url(),
                "link_text": ann.link_text,
            }
        )
