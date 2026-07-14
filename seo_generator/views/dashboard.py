"""
SEO Dashboard Views

Provides the SEO coverage dashboard and related API endpoints.
"""

import json
import logging

from django.apps import apps
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from seo_generator.api.endpoints import MODEL_MAP
from seo_generator.services.coverage_service import (
    SEOCoverageService,
    invalidate_seo_coverage_cache,
)

logger = logging.getLogger(__name__)

# Map model_type to the field used as the display name
NAME_FIELD_MAP = {
    "product": "name",
    "category": "name",
    "brand": "name",
    "page": "title",
    "blogpost": "title",
    "blogcategory": "name",
}


@staff_member_required
def seo_dashboard_view(request):
    """SEO Dashboard - coverage overview and quick actions."""
    from seo_generator.models import SEOProviderAccount
    from seo_generator.providers.registry import ProviderRegistry

    # Coverage data
    try:
        coverage = SEOCoverageService().get_site_coverage()
    except Exception as e:
        logger.error("Failed to load SEO coverage: %s", e)
        coverage = {
            "overall_percentage": 0,
            "total_items": 0,
            "with_title": 0,
            "with_description": 0,
            "with_both": 0,
            "missing_any": 0,
            "content_types": [],
            "quality": {
                "title_too_short": 0,
                "title_too_long": 0,
                "desc_too_short": 0,
                "desc_too_long": 0,
                "total_issues": 0,
            },
        }

    # Provider info
    try:
        primary_account = SEOProviderAccount.objects.get(is_primary=True, is_active=True)
    except SEOProviderAccount.DoesNotExist:
        primary_account = None

    active_providers = SEOProviderAccount.objects.filter(is_active=True).count()
    available_providers = len(ProviderRegistry.list_providers())

    context = {
        "title": _("SEO Dashboard"),
        "coverage": coverage,
        "coverage_json": json.dumps(coverage, default=str),
        "primary_account": primary_account,
        "active_providers": active_providers,
        "available_providers": available_providers,
        "has_custom_template": True,
    }

    return render(request, "admin/seo_generator/dashboard.html", context)


@staff_member_required
@require_http_methods(["GET"])
def seo_coverage_api(request):
    """JSON API for SEO coverage data."""
    try:
        coverage = SEOCoverageService().get_site_coverage()
        return JsonResponse({"success": True, **coverage})
    except Exception as e:
        logger.error("SEO coverage API error: %s", e, exc_info=True)
        return JsonResponse(
            {"success": False, "error": _("Failed to calculate coverage.")}, status=500
        )


@staff_member_required
@require_http_methods(["POST"])
def seo_coverage_refresh_api(request):
    """Invalidate cache and return fresh coverage data."""
    try:
        invalidate_seo_coverage_cache()
        coverage = SEOCoverageService().get_site_coverage(use_cache=False)
        return JsonResponse({"success": True, **coverage})
    except Exception as e:
        logger.error("SEO coverage refresh error: %s", e, exc_info=True)
        return JsonResponse(
            {"success": False, "error": _("Failed to refresh coverage.")}, status=500
        )


@staff_member_required
@require_http_methods(["GET"])
def seo_missing_items_api(request):
    """Return list of items missing SEO fields for frontend-driven batch processing."""
    try:
        items = SEOCoverageService().get_missing_items()
        return JsonResponse(
            {
                "success": True,
                "items": items,
                "total": len(items),
            }
        )
    except Exception as e:
        logger.error("SEO missing items API error: %s", e, exc_info=True)
        return JsonResponse(
            {"success": False, "error": _("Failed to get missing items.")}, status=500
        )


@staff_member_required
@require_http_methods(["GET"])
def seo_items_api(request, content_type):
    """Return items for a content type with their SEO status for drill-down display."""
    if content_type not in MODEL_MAP:
        return JsonResponse({"success": False, "error": _("Invalid content type.")}, status=400)

    filter_mode = request.GET.get("filter", "all")

    try:
        app_label, model_name = MODEL_MAP[content_type]
        model_class = apps.get_model(app_label, model_name)
        name_field = NAME_FIELD_MAP.get(content_type, "name")

        qs = model_class.objects.all()

        # Apply filter
        has_both = (
            ~Q(meta_title="")
            & Q(meta_title__isnull=False)
            & ~Q(meta_description="")
            & Q(meta_description__isnull=False)
        )
        if filter_mode == "missing":
            qs = qs.exclude(has_both)
        elif filter_mode == "complete":
            qs = qs.filter(has_both)

        # Order: missing first, then by name
        qs = qs.order_by("meta_title", name_field)

        # Build admin change URL pattern
        admin_url_name = f"admin:{app_label}_{model_name.lower()}_change"

        items = []
        for obj in qs[:500]:  # Cap at 500 items
            obj_name = getattr(obj, name_field, "") or ""
            meta_title = obj.meta_title or ""
            meta_description = obj.meta_description or ""
            item_has_both = bool(meta_title and meta_description)

            try:
                edit_url = reverse(admin_url_name, args=[obj.pk])
            except Exception:
                edit_url = ""

            items.append(
                {
                    "id": obj.pk,
                    "name": str(obj_name),
                    "meta_title": meta_title,
                    "meta_description": meta_description,
                    "has_title": bool(meta_title),
                    "has_description": bool(meta_description),
                    "has_both": item_has_both,
                    "seo_auto_generated": getattr(obj, "seo_auto_generated", False),
                    "edit_url": edit_url,
                }
            )

        return JsonResponse(
            {
                "success": True,
                "content_type": content_type,
                "items": items,
                "total": len(items),
            }
        )

    except Exception as e:
        logger.error("SEO items API error for %s: %s", content_type, e, exc_info=True)
        return JsonResponse({"success": False, "error": _("Failed to load items.")}, status=500)
