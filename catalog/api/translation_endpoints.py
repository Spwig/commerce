"""
Translation API endpoints for Product model
"""

import json

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.utils.html import strip_tags
from django.views.decorators.http import require_http_methods

from catalog.models import Product
from translations.models import SiteLanguage


@staff_member_required
@require_http_methods(["GET"])
def get_product_translations(request, product_id):
    """
    Get all translations for a product.

    Returns:
        {
            "translations": {
                "en": {
                    "name": "Product Name",
                    "description_html": "<p>Rich text</p>",
                    "description_text": "Plain text",
                    ...
                },
                ...
            }
        }
    """
    try:
        product = Product.objects.get(pk=product_id)

        return JsonResponse({"success": True, "translations": product.translations or {}})
    except Product.DoesNotExist:
        return JsonResponse({"success": False, "error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
@require_http_methods(["POST"])
def save_product_translation(request, product_id):
    """
    Save translation for a specific language and field.

    POST data:
        {
            "language": "en",
            "field": "name",
            "value": "Product Name",
            "html_value": "<p>Rich text</p>"  // Optional, for description fields
        }

    For description fields, both HTML and plain text versions are saved:
    - description_html and description_text
    - short_description_html and short_description_text
    """
    try:
        product = Product.objects.get(pk=product_id)

        # Parse JSON body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON data"}, status=400)

        language = data.get("language")
        field = data.get("field")
        value = data.get("value")
        html_value = data.get("html_value")

        if not language or not field:
            return JsonResponse(
                {"success": False, "error": "Missing required fields: language, field"}, status=400
            )

        # Handle rich text fields (description and short_description)
        if field in ["description", "short_description"]:
            # Save HTML version
            if html_value is not None:
                product.set_translation(language, f"{field}_html", html_value)
                # Auto-generate plain text from HTML
                plain_text = strip_tags(html_value)
                product.set_translation(language, f"{field}_text", plain_text)
            # If only plain text provided, save it to text field
            elif value is not None:
                product.set_translation(language, f"{field}_text", value)
        else:
            # Regular text fields (name, meta_title, meta_description)
            if value is not None:
                product.set_translation(language, field, value)

        product.save()

        return JsonResponse({"success": True, "translations": product.translations})

    except Product.DoesNotExist:
        return JsonResponse({"success": False, "error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
@require_http_methods(["POST"])
def save_all_product_translations(request, product_id):
    """
    Save all translations for a product at once.

    POST data:
        {
            "translations": {
                "en": {
                    "name": "Product Name",
                    "description_html": "<p>Rich text</p>",
                    "description_text": "Plain text",
                    ...
                },
                ...
            }
        }
    """
    try:
        product = Product.objects.get(pk=product_id)

        # Parse JSON body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON data"}, status=400)

        translations = data.get("translations")

        if not isinstance(translations, dict):
            return JsonResponse(
                {"success": False, "error": "translations must be a dictionary"}, status=400
            )

        # Auto-generate plain text from HTML for description fields
        for _lang_code, fields in translations.items():
            if isinstance(fields, dict):
                # Generate plain text from description_html if present
                if "description_html" in fields and "description_text" not in fields:
                    fields["description_text"] = strip_tags(fields["description_html"])

                # Generate plain text from short_description_html if present
                if "short_description_html" in fields and "short_description_text" not in fields:
                    fields["short_description_text"] = strip_tags(fields["short_description_html"])

        product.translations = translations
        product.save()

        return JsonResponse({"success": True, "translations": product.translations})

    except Product.DoesNotExist:
        return JsonResponse({"success": False, "error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
@require_http_methods(["GET"])
def get_available_languages(request):
    """
    Get list of available languages for product translations.

    This endpoint returns languages configured in the Translations app
    (merchant-configurable frontend languages), NOT the Django admin
    interface languages.

    Returns:
        {
            "success": true,
            "languages": [
                {
                    "code": "en",
                    "name": "English",
                    "native_name": "English",
                    "rtl": false
                },
                {
                    "code": "ar",
                    "name": "Arabic",
                    "native_name": "العربية",
                    "rtl": true
                },
                ...
            ]
        }
    """
    try:
        # Get active languages from translations app (merchant-configured)
        site_languages = SiteLanguage.objects.filter(is_active=True).order_by("order", "name")

        languages = [
            {
                "code": lang.code,
                "name": lang.name,
                "native_name": lang.native_name,
                "rtl": getattr(lang, "rtl", False),  # Text direction
            }
            for lang in site_languages
        ]

        return JsonResponse({"success": True, "languages": languages})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
