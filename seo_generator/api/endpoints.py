"""
SEO Generation API Endpoints

Provides REST API for generating SEO content for products, categories, brands,
pages, blog posts, and blog categories.
"""

import json
import logging
import re

from django.apps import apps
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers

from core.models import SiteSettings
from seo_generator.providers.base import GenerationError, ProviderNotAvailable
from seo_generator.providers.registry import ProviderRegistry

logger = logging.getLogger(__name__)


# Model type mapping
MODEL_MAP = {
    "product": ("catalog", "Product"),
    "category": ("catalog", "Category"),
    "brand": ("catalog", "Brand"),
    "page": ("page_builder", "Page"),
    "blogpost": ("blog", "BlogPost"),
    "blogcategory": ("blog", "BlogCategory"),
}

# Valid provider key pattern
PROVIDER_KEY_RE = re.compile(r"^[a-zA-Z0-9_-]+$")


def get_model_class(model_type: str):
    """
    Get Django model class from model type string.

    Args:
        model_type: One of 'product', 'category', 'brand', 'page', 'blogpost', 'blogcategory'

    Returns:
        Model class

    Raises:
        ValueError: If model_type is invalid
    """
    if model_type not in MODEL_MAP:
        raise ValueError(
            _("Invalid model type: %(type)s. Must be one of: %(valid)s")
            % {"type": model_type, "valid": ", ".join(MODEL_MAP.keys())}
        )

    app_label, model_name = MODEL_MAP[model_type]
    return apps.get_model(app_label, model_name)


def _check_change_permission(request, model_class):
    """
    Check that the user has change permission for the given model.

    Returns:
        JsonResponse with 403 if permission denied, None if allowed.
    """
    perm = f"{model_class._meta.app_label}.change_{model_class._meta.model_name}"
    if not request.user.has_perm(perm):
        return JsonResponse({"success": False, "error": _("Permission denied.")}, status=403)
    return None


def _validate_provider_key(provider_key: str) -> bool:
    """Validate that provider_key is safe (alphanumeric, underscore, hyphen)."""
    return bool(PROVIDER_KEY_RE.match(provider_key))


def _validate_language(language: str) -> bool:
    """Validate that language is a known language code."""
    valid_codes = [code for code, name in settings.LANGUAGES]
    return language in valid_codes


def _get_default_language():
    """Get default language from SiteSettings or fall back to 'en'."""
    try:
        site_settings = SiteSettings.objects.get(pk=1)
        return site_settings.default_language
    except SiteSettings.DoesNotExist:
        return "en"


def extract_content_from_object(obj, model_type: str) -> dict[str, str]:
    """
    Extract content fields from model instance for SEO generation.

    Args:
        obj: Model instance
        model_type: Type of model

    Returns:
        Dictionary with content fields
    """
    from django.utils.html import strip_tags

    content = {
        "type": model_type,
        "name": getattr(obj, "name", "") or getattr(obj, "title", ""),
    }

    if model_type == "product":
        # Product model has CKEditor5 fields - use helper methods to get plain text
        if hasattr(obj, "get_translated_description"):
            content["description"] = obj.get_translated_description(plain_text=True) or ""
        elif hasattr(obj, "full_description"):
            content["description"] = (
                strip_tags(obj.full_description) if obj.full_description else ""
            )

        # Add short description
        if hasattr(obj, "get_translated_short_description"):
            short_desc = obj.get_translated_short_description(plain_text=True) or ""
            if short_desc:
                content["description"] = short_desc + " " + content.get("description", "")
        elif hasattr(obj, "short_description"):
            short_desc = strip_tags(obj.short_description) if obj.short_description else ""
            if short_desc:
                content["description"] = short_desc + " " + content.get("description", "")

        # Add brand and category
        if hasattr(obj, "brand") and obj.brand:
            content["brand"] = obj.brand.name
        if hasattr(obj, "category") and obj.category:
            content["category"] = obj.category.name

    elif model_type == "blogpost":
        # BlogPost uses 'title' (already captured above) and has excerpt/content
        content["name"] = getattr(obj, "title", "") or ""
        if hasattr(obj, "excerpt") and obj.excerpt:
            content["description"] = strip_tags(obj.excerpt)
        elif hasattr(obj, "simple_content") and obj.simple_content:
            content["description"] = strip_tags(obj.simple_content)
        elif hasattr(obj, "content") and obj.content:
            content["description"] = strip_tags(obj.content)
        # Add category if available
        if hasattr(obj, "category") and obj.category:
            content["category"] = obj.category.name

    elif model_type == "blogcategory":
        content["name"] = getattr(obj, "name", "") or ""
        if hasattr(obj, "description") and obj.description:
            content["description"] = strip_tags(obj.description)

    else:
        # For other models (category, brand, page), description is plain text
        if hasattr(obj, "description"):
            desc = obj.description or ""
            content["description"] = strip_tags(desc) if desc else ""

    return content


@extend_schema(
    tags=["SEO Generator"],
    summary=_("Generate SEO content for a single object"),
    description=_(
        "Generate meta title, meta description, and keywords for a product, category, brand, page, blog post, or blog category. The generated content is automatically saved to the object."
    ),
    parameters=[
        OpenApiParameter(
            name="model_type",
            location="path",
            type=str,
            description=_("Model type: product, category, brand, page, blogpost, or blogcategory"),
        ),
        OpenApiParameter(
            name="object_id",
            location="path",
            type=int,
            description=_("ID of the object to generate SEO for"),
        ),
    ],
    request=inline_serializer(
        name="SEOGenerateRequest",
        fields={
            "provider": serializers.CharField(
                required=False,
                help_text="Provider key (default: primary provider, or deterministic if none configured)",
            ),
            "language": serializers.CharField(
                required=False, help_text="Language code (default: site primary language)"
            ),
        },
    ),
    responses={
        200: inline_serializer(
            name="SEOGenerateResponse",
            fields={
                "success": serializers.BooleanField(),
                "meta_title": serializers.CharField(),
                "meta_description": serializers.CharField(),
                "keywords": serializers.ListField(child=serializers.CharField()),
                "saved": serializers.BooleanField(),
            },
        ),
        400: OpenApiResponse(description=_("Invalid model type, provider key, or language code")),
        403: OpenApiResponse(description=_("Permission denied")),
        404: OpenApiResponse(description=_("Object not found")),
        500: OpenApiResponse(description=_("Generation failed or unexpected error")),
    },
)
@staff_member_required
@require_http_methods(["POST"])
def generate_seo(request, model_type: str, object_id: int):
    """Generate SEO content for a single object."""
    try:
        # Parse optional body parameters
        body = {}
        if request.body:
            try:
                body = json.loads(request.body)
            except json.JSONDecodeError:
                pass

        provider_key = body.get("provider") or None
        language = body.get("language")

        # Validate provider key
        if provider_key and not _validate_provider_key(provider_key):
            return JsonResponse({"success": False, "error": _("Invalid provider key.")}, status=400)

        # Get default language if not specified
        if not language:
            language = _get_default_language()
        elif not _validate_language(language):
            return JsonResponse(
                {"success": False, "error": _("Invalid language code.")}, status=400
            )

        # Get model and object
        try:
            model_class = get_model_class(model_type)
        except ValueError as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

        # Check permissions
        perm_denied = _check_change_permission(request, model_class)
        if perm_denied:
            return perm_denied

        try:
            obj = model_class.objects.get(pk=object_id)
        except ObjectDoesNotExist:
            return JsonResponse({"success": False, "error": _("Object not found.")}, status=404)

        # Get provider instance (with credentials for external providers)
        try:
            provider = ProviderRegistry.get_provider_instance(provider_key)
        except ProviderNotAvailable as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

        # Extract content
        content = extract_content_from_object(obj, model_type)

        # Generate SEO
        try:
            result = provider.generate_seo(content, language)
        except GenerationError as e:
            logger.warning("SEO generation failed for %s %s: %s", model_type, object_id, e)
            return JsonResponse(
                {"success": False, "error": _("SEO generation failed. Please try again.")},
                status=500,
            )

        # Save to object
        obj.meta_title = result["meta_title"]
        obj.meta_description = result["meta_description"]
        obj.save(update_fields=["meta_title", "meta_description"])

        # Invalidate coverage cache
        from seo_generator.services.coverage_service import invalidate_seo_coverage_cache

        invalidate_seo_coverage_cache()

        logger.info("Generated SEO for %s %s: %s", model_type, object_id, result["meta_title"])

        return JsonResponse(
            {
                "success": True,
                "meta_title": result["meta_title"],
                "meta_description": result["meta_description"],
                "keywords": result["keywords"],
                "saved": True,
            }
        )

    except Exception as e:
        logger.error("SEO generation error for %s %s: %s", model_type, object_id, e, exc_info=True)
        return JsonResponse(
            {"success": False, "error": _("An unexpected error occurred. Please try again.")},
            status=500,
        )


@extend_schema(
    tags=["SEO Generator"],
    summary=_("Batch generate SEO for multiple objects"),
    description=_(
        "Generate SEO content for multiple objects at once. Each item specifies a model type and object ID. Results include per-item success/failure and a summary."
    ),
    request=inline_serializer(
        name="SEOBatchRequest",
        fields={
            "items": serializers.ListField(
                child=inline_serializer(
                    name="SEOBatchItem",
                    fields={
                        "model_type": serializers.CharField(
                            help_text="Model type: product, category, brand, page, blogpost, or blogcategory"
                        ),
                        "object_id": serializers.IntegerField(help_text="ID of the object"),
                    },
                ),
                help_text="List of items to generate SEO for",
            ),
            "provider": serializers.CharField(
                required=False, help_text="Provider key (default: primary provider)"
            ),
            "language": serializers.CharField(required=False, help_text="Language code"),
        },
    ),
    responses={
        200: inline_serializer(
            name="SEOBatchResponse",
            fields={
                "success": serializers.BooleanField(),
                "results": serializers.ListField(child=serializers.DictField()),
                "summary": inline_serializer(
                    name="SEOBatchSummary",
                    fields={
                        "total": serializers.IntegerField(),
                        "successful": serializers.IntegerField(),
                        "failed": serializers.IntegerField(),
                    },
                ),
            },
        ),
        400: OpenApiResponse(description=_("Invalid request body, no items, or invalid provider")),
        500: OpenApiResponse(description=_("Unexpected error")),
    },
)
@staff_member_required
@require_http_methods(["POST"])
def batch_generate(request):
    """Generate SEO for multiple objects at once."""
    try:
        # Parse body
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": _("Invalid request body.")}, status=400)

        items = body.get("items", [])
        if not items:
            return JsonResponse({"success": False, "error": _("No items provided.")}, status=400)

        provider_key = body.get("provider") or None
        language = body.get("language")

        # Validate provider key
        if provider_key and not _validate_provider_key(provider_key):
            return JsonResponse({"success": False, "error": _("Invalid provider key.")}, status=400)

        # Get default language if not specified
        if not language:
            language = _get_default_language()

        # Get provider instance (with credentials for external providers)
        try:
            provider = ProviderRegistry.get_provider_instance(provider_key)
        except ProviderNotAvailable as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

        # Process each item
        results = []
        successful = 0
        failed = 0

        for item in items:
            item_model_type = item.get("model_type")
            item_object_id = item.get("object_id")

            if not item_model_type or not item_object_id:
                results.append(
                    {
                        "model_type": item_model_type,
                        "object_id": item_object_id,
                        "success": False,
                        "error": _("Missing model_type or object_id."),
                    }
                )
                failed += 1
                continue

            try:
                # Get model and object
                model_class = get_model_class(item_model_type)

                # Check permissions per model type
                perm = f"{model_class._meta.app_label}.change_{model_class._meta.model_name}"
                if not request.user.has_perm(perm):
                    results.append(
                        {
                            "model_type": item_model_type,
                            "object_id": item_object_id,
                            "success": False,
                            "error": _("Permission denied."),
                        }
                    )
                    failed += 1
                    continue

                obj = model_class.objects.get(pk=item_object_id)

                # Extract content and generate SEO
                content = extract_content_from_object(obj, item_model_type)
                result = provider.generate_seo(content, language)

                # Save to object
                obj.meta_title = result["meta_title"]
                obj.meta_description = result["meta_description"]
                obj.save(update_fields=["meta_title", "meta_description"])

                results.append(
                    {
                        "model_type": item_model_type,
                        "object_id": item_object_id,
                        "success": True,
                        "meta_title": result["meta_title"],
                        "meta_description": result["meta_description"],
                    }
                )
                successful += 1

            except Exception as e:
                results.append(
                    {
                        "model_type": item_model_type,
                        "object_id": item_object_id,
                        "success": False,
                        "error": _("Generation failed for this item."),
                    }
                )
                failed += 1
                logger.error(
                    "Batch SEO generation failed for %s %s: %s", item_model_type, item_object_id, e
                )

        # Invalidate coverage cache after batch processing
        if successful > 0:
            from seo_generator.services.coverage_service import invalidate_seo_coverage_cache

            invalidate_seo_coverage_cache()

        return JsonResponse(
            {
                "success": True,
                "results": results,
                "summary": {"total": len(items), "successful": successful, "failed": failed},
            }
        )

    except Exception as e:
        logger.error("Batch SEO generation error: %s", e, exc_info=True)
        return JsonResponse(
            {"success": False, "error": _("An unexpected error occurred. Please try again.")},
            status=500,
        )


@extend_schema(
    tags=["SEO Generator"],
    summary=_("Check SEO status for an object"),
    description=_(
        "Check whether an object has SEO content, whether it was auto-generated, and return the current meta title and description with their lengths."
    ),
    parameters=[
        OpenApiParameter(
            name="model_type",
            location="path",
            type=str,
            description=_("Model type: product, category, brand, page, blogpost, or blogcategory"),
        ),
        OpenApiParameter(
            name="object_id", location="path", type=int, description=_("ID of the object")
        ),
    ],
    responses={
        200: inline_serializer(
            name="SEOStatusResponse",
            fields={
                "success": serializers.BooleanField(),
                "has_seo": serializers.BooleanField(),
                "auto_generated": serializers.BooleanField(),
                "meta_title": serializers.CharField(),
                "meta_description": serializers.CharField(),
                "meta_title_length": serializers.IntegerField(),
                "meta_description_length": serializers.IntegerField(),
            },
        ),
        400: OpenApiResponse(description=_("Invalid model type")),
        404: OpenApiResponse(description=_("Object not found")),
        500: OpenApiResponse(description=_("Unexpected error")),
    },
)
@staff_member_required
@require_http_methods(["GET"])
def seo_status(request, model_type: str, object_id: int):
    """Check SEO status for an object."""
    try:
        # Get model and object
        try:
            model_class = get_model_class(model_type)
        except ValueError as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

        try:
            obj = model_class.objects.get(pk=object_id)
        except ObjectDoesNotExist:
            return JsonResponse({"success": False, "error": _("Object not found.")}, status=404)

        # Get SEO fields
        meta_title = getattr(obj, "meta_title", "") or ""
        meta_description = getattr(obj, "meta_description", "") or ""
        auto_generated = getattr(obj, "seo_auto_generated", False)

        return JsonResponse(
            {
                "success": True,
                "has_seo": bool(meta_title or meta_description),
                "auto_generated": auto_generated,
                "meta_title": meta_title,
                "meta_description": meta_description,
                "meta_title_length": len(meta_title),
                "meta_description_length": len(meta_description),
            }
        )

    except Exception as e:
        logger.error(
            "SEO status check error for %s %s: %s", model_type, object_id, e, exc_info=True
        )
        return JsonResponse(
            {"success": False, "error": _("An unexpected error occurred. Please try again.")},
            status=500,
        )
