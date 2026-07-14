"""
SEO coverage calculation service.

Calculates how much of a merchant's site content has meta_title and
meta_description populated in the primary language.

"""

import logging

from django.apps import apps
from django.core.cache import cache
from django.db.models import Count, Q
from django.db.models.functions import Length

from seo_generator.api.endpoints import MODEL_MAP

logger = logging.getLogger(__name__)

SEO_COVERAGE_CACHE_KEY = "seo_coverage_v1"
SEO_COVERAGE_CACHE_TTL = 600  # 10 minutes

# Content type metadata for dashboard display
CONTENT_TYPE_META = {
    "product": {"label": "Products", "icon": "fas fa-box-open", "priority": 1},
    "category": {"label": "Categories", "icon": "fas fa-folder-tree", "priority": 1},
    "brand": {"label": "Brands", "icon": "fas fa-copyright", "priority": 2},
    "page": {"label": "Pages", "icon": "fas fa-file-alt", "priority": 2},
    "blogpost": {"label": "Blog Posts", "icon": "fas fa-newspaper", "priority": 3},
    "blogcategory": {"label": "Blog Categories", "icon": "fas fa-bookmark", "priority": 3},
}


class SEOCoverageService:
    """Calculates SEO coverage across all content types."""

    def get_site_coverage(self, use_cache=True):
        """
        Return overall SEO coverage for the site.

        Args:
            use_cache: Whether to use cached results.

        Returns:
            dict with overall_percentage, content_types breakdown, quality metrics.
        """
        if use_cache:
            cached = cache.get(SEO_COVERAGE_CACHE_KEY)
            if cached is not None:
                return cached

        content_types = []
        grand_total = 0
        grand_with_title = 0
        grand_with_description = 0
        grand_with_both = 0
        grand_title_too_short = 0
        grand_title_too_long = 0
        grand_desc_too_short = 0
        grand_desc_too_long = 0

        for model_type, (app_label, model_name) in MODEL_MAP.items():
            try:
                model_class = apps.get_model(app_label, model_name)
                result = self._calculate_model_coverage(model_type, model_class)
                if result:
                    content_types.append(result)
                    grand_total += result["total"]
                    grand_with_title += result["with_title"]
                    grand_with_description += result["with_description"]
                    grand_with_both += result["with_both"]
                    grand_title_too_short += result["quality"]["title_too_short"]
                    grand_title_too_long += result["quality"]["title_too_long"]
                    grand_desc_too_short += result["quality"]["desc_too_short"]
                    grand_desc_too_long += result["quality"]["desc_too_long"]
            except Exception as e:
                logger.warning("SEO coverage calc failed for %s: %s", model_type, e)

        overall_pct = round((grand_with_both / grand_total * 100), 1) if grand_total > 0 else 0

        result = {
            "overall_percentage": overall_pct,
            "total_items": grand_total,
            "with_title": grand_with_title,
            "with_description": grand_with_description,
            "with_both": grand_with_both,
            "missing_any": grand_total - grand_with_both,
            "content_types": sorted(content_types, key=lambda x: (x["priority"], x["label"])),
            "quality": {
                "title_too_short": grand_title_too_short,
                "title_too_long": grand_title_too_long,
                "desc_too_short": grand_desc_too_short,
                "desc_too_long": grand_desc_too_long,
                "total_issues": (
                    grand_title_too_short
                    + grand_title_too_long
                    + grand_desc_too_short
                    + grand_desc_too_long
                ),
            },
        }

        if use_cache:
            cache.set(SEO_COVERAGE_CACHE_KEY, result, SEO_COVERAGE_CACHE_TTL)

        return result

    def get_missing_items(self):
        """
        Get list of all items missing meta_title or meta_description.

        Returns:
            list of dicts with model_type and object_id.
        """
        items = []
        for model_type, (app_label, model_name) in MODEL_MAP.items():
            try:
                model_class = apps.get_model(app_label, model_name)
                if not hasattr(model_class, "meta_title"):
                    continue

                missing = model_class.objects.filter(
                    Q(meta_title="")
                    | Q(meta_title__isnull=True)
                    | Q(meta_description="")
                    | Q(meta_description__isnull=True)
                ).values_list("pk", flat=True)

                for pk in missing:
                    items.append(
                        {
                            "model_type": model_type,
                            "object_id": pk,
                        }
                    )
            except Exception as e:
                logger.warning("Failed to get missing items for %s: %s", model_type, e)

        return items

    def _calculate_model_coverage(self, model_type, model_class):
        """Calculate SEO coverage for a single model type."""
        if not hasattr(model_class, "meta_title") or not hasattr(model_class, "meta_description"):
            return None

        meta = CONTENT_TYPE_META.get(model_type, {})

        qs = model_class.objects.annotate(
            title_len=Length("meta_title"),
            desc_len=Length("meta_description"),
        )

        stats = qs.aggregate(
            total=Count("pk"),
            with_title=Count("pk", filter=~Q(meta_title="") & Q(meta_title__isnull=False)),
            with_description=Count(
                "pk", filter=~Q(meta_description="") & Q(meta_description__isnull=False)
            ),
            with_both=Count(
                "pk",
                filter=(
                    ~Q(meta_title="")
                    & Q(meta_title__isnull=False)
                    & ~Q(meta_description="")
                    & Q(meta_description__isnull=False)
                ),
            ),
            # Quality metrics for titles
            title_too_short=Count("pk", filter=Q(title_len__gt=0, title_len__lt=30)),
            title_too_long=Count("pk", filter=Q(title_len__gt=60)),
            # Quality metrics for descriptions
            desc_too_short=Count("pk", filter=Q(desc_len__gt=0, desc_len__lt=70)),
            desc_too_long=Count("pk", filter=Q(desc_len__gt=160)),
        )

        total = stats["total"]
        if total == 0:
            return None  # Skip empty content types

        with_both = stats["with_both"]
        pct = round((with_both / total * 100), 1) if total > 0 else 0

        return {
            "key": model_type,
            "label": meta.get("label", model_type.capitalize()),
            "icon": meta.get("icon", "fas fa-file"),
            "priority": meta.get("priority", 3),
            "total": total,
            "with_title": stats["with_title"],
            "with_description": stats["with_description"],
            "with_both": with_both,
            "missing": total - with_both,
            "percentage": pct,
            "quality": {
                "title_too_short": stats["title_too_short"],
                "title_too_long": stats["title_too_long"],
                "desc_too_short": stats["desc_too_short"],
                "desc_too_long": stats["desc_too_long"],
            },
        }


def invalidate_seo_coverage_cache():
    """Invalidate SEO coverage cache. Call after SEO fields are updated."""
    cache.delete(SEO_COVERAGE_CACHE_KEY)
