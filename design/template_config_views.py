"""
Views for the Page Template Configuration admin interface.
Allows merchants to choose checkout and product page templates and configure their options.
"""

import json

from django.contrib.admin.views.decorators import staff_member_required
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import PageTemplateConfig
from .template_registry import (
    BLOG_LIST_TEMPLATE_META,
    BLOG_LIST_TEMPLATE_OPTIONS,
    BLOG_POST_TEMPLATE_META,
    BLOG_POST_TEMPLATE_OPTIONS,
    CATEGORY_TEMPLATE_META,
    CATEGORY_TEMPLATE_OPTIONS,
    CHECKOUT_TEMPLATE_META,
    CHECKOUT_TEMPLATE_OPTIONS,
    PRODUCT_TEMPLATE_META,
    PRODUCT_TEMPLATE_OPTIONS,
    get_blog_list_options,
    get_blog_post_options,
    get_category_options,
    get_checkout_options,
    get_product_options,
)


@staff_member_required
def template_config_view(request):
    """Render the template configuration page."""
    config = PageTemplateConfig.get_config()

    # Build template card data with resolved options
    checkout_cards = []
    for key, meta in CHECKOUT_TEMPLATE_META.items():
        options_schema = CHECKOUT_TEMPLATE_OPTIONS.get(key, {})
        resolved = get_checkout_options(
            key, config.checkout_options if config.checkout_template == key else {}
        )
        checkout_cards.append(
            {
                "key": key,
                "name": str(meta["name"]),
                "description": str(meta["description"]),
                "icon": meta["icon"],
                "preview_image": meta.get("preview_image"),
                "is_active": config.checkout_template == key,
                "options_schema": options_schema,
                "resolved_options": resolved,
            }
        )

    product_cards = []
    for key, meta in PRODUCT_TEMPLATE_META.items():
        options_schema = PRODUCT_TEMPLATE_OPTIONS.get(key, {})
        resolved = get_product_options(
            key, config.product_options if config.product_template == key else {}
        )
        product_cards.append(
            {
                "key": key,
                "name": str(meta["name"]),
                "description": str(meta["description"]),
                "icon": meta["icon"],
                "preview_image": meta.get("preview_image"),
                "is_active": config.product_template == key,
                "options_schema": options_schema,
                "resolved_options": resolved,
            }
        )

    category_cards = []
    for key, meta in CATEGORY_TEMPLATE_META.items():
        options_schema = CATEGORY_TEMPLATE_OPTIONS.get(key, {})
        resolved = get_category_options(
            key, config.category_options if config.category_template == key else {}
        )
        category_cards.append(
            {
                "key": key,
                "name": str(meta["name"]),
                "description": str(meta["description"]),
                "icon": meta["icon"],
                "preview_image": meta.get("preview_image"),
                "is_active": config.category_template == key,
                "options_schema": options_schema,
                "resolved_options": resolved,
            }
        )

    blog_post_cards = []
    for key, meta in BLOG_POST_TEMPLATE_META.items():
        options_schema = BLOG_POST_TEMPLATE_OPTIONS.get(key, {})
        resolved = get_blog_post_options(
            key, config.blog_post_options if config.blog_post_template == key else {}
        )
        blog_post_cards.append(
            {
                "key": key,
                "name": str(meta["name"]),
                "description": str(meta["description"]),
                "icon": meta["icon"],
                "preview_image": meta.get("preview_image"),
                "is_active": config.blog_post_template == key,
                "options_schema": options_schema,
                "resolved_options": resolved,
            }
        )

    blog_list_cards = []
    for key, meta in BLOG_LIST_TEMPLATE_META.items():
        options_schema = BLOG_LIST_TEMPLATE_OPTIONS.get(key, {})
        resolved = get_blog_list_options(
            key, config.blog_list_options if config.blog_list_template == key else {}
        )
        blog_list_cards.append(
            {
                "key": key,
                "name": str(meta["name"]),
                "description": str(meta["description"]),
                "icon": meta["icon"],
                "preview_image": meta.get("preview_image"),
                "is_active": config.blog_list_template == key,
                "options_schema": options_schema,
                "resolved_options": resolved,
            }
        )

    context = {
        "title": "Page Templates",
        "config": config,
        "checkout_cards": checkout_cards,
        "product_cards": product_cards,
        "category_cards": category_cards,
        "blog_post_cards": blog_post_cards,
        "blog_list_cards": blog_list_cards,
        "checkout_cards_json": json.dumps(checkout_cards, cls=DjangoJSONEncoder),
        "product_cards_json": json.dumps(product_cards, cls=DjangoJSONEncoder),
        "category_cards_json": json.dumps(category_cards, cls=DjangoJSONEncoder),
        "blog_post_cards_json": json.dumps(blog_post_cards, cls=DjangoJSONEncoder),
        "blog_list_cards_json": json.dumps(blog_list_cards, cls=DjangoJSONEncoder),
        "checkout_trust_badges_json": json.dumps(
            config.checkout_trust_badges or [], cls=DjangoJSONEncoder
        ),
        "product_trust_badges_json": json.dumps(
            config.product_trust_badges or [], cls=DjangoJSONEncoder
        ),
        "digital_trust_badges_json": json.dumps(
            config.digital_trust_badges or [], cls=DjangoJSONEncoder
        ),
    }
    return render(request, "design/template_config.html", context)


def _validate_template_options(options, schema):
    """Validate submitted template options against their registry schema.

    Whitelists keys to the schema, requires booleans for ``bool`` options and
    membership in ``definition["options"]`` for ``select`` options. Returns the
    validated dict or raises ``ValueError`` describing the first invalid entry.
    """
    validated = {}
    for key, value in options.items():
        definition = schema.get(key)
        if definition is None:
            raise ValueError(f"Unknown option '{key}'.")
        option_type = definition.get("type")
        if option_type == "bool":
            if not isinstance(value, bool):
                raise ValueError(f"Option '{key}' must be a boolean.")
        elif option_type == "select":
            if value not in definition["options"]:
                raise ValueError(f"Option '{key}' has an invalid value.")
        validated[key] = value
    return validated


@staff_member_required
@require_POST
def template_config_save(request):
    """Save template configuration via AJAX."""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"success": False, "message": "Invalid JSON."}, status=400)

    if not isinstance(data, dict):
        return JsonResponse(
            {"success": False, "message": "Request body must be a JSON object."}, status=400
        )

    config = PageTemplateConfig.get_config()

    # (attribute prefix, template META registry, option schema registry)
    template_kinds = (
        ("checkout", CHECKOUT_TEMPLATE_META, CHECKOUT_TEMPLATE_OPTIONS),
        ("product", PRODUCT_TEMPLATE_META, PRODUCT_TEMPLATE_OPTIONS),
        ("category", CATEGORY_TEMPLATE_META, CATEGORY_TEMPLATE_OPTIONS),
        ("blog_post", BLOG_POST_TEMPLATE_META, BLOG_POST_TEMPLATE_OPTIONS),
        ("blog_list", BLOG_LIST_TEMPLATE_META, BLOG_LIST_TEMPLATE_OPTIONS),
    )

    for prefix, meta, option_schema in template_kinds:
        template_value = data.get(f"{prefix}_template")
        if template_value and template_value in meta:
            setattr(config, f"{prefix}_template", template_value)

        options_value = data.get(f"{prefix}_options")
        if options_value is None:
            continue
        if not isinstance(options_value, dict):
            return JsonResponse(
                {"success": False, "message": f"{prefix}_options must be an object."}, status=400
            )
        active_template = getattr(config, f"{prefix}_template")
        # "default" is a backward-compatibility alias for the "grid" category schema.
        if prefix == "category" and active_template == "default":
            active_template = "grid"
        try:
            validated = _validate_template_options(
                options_value, option_schema.get(active_template, {})
            )
        except ValueError as exc:
            return JsonResponse({"success": False, "message": str(exc)}, status=400)
        setattr(config, f"{prefix}_options", validated)

    # Trust badges: list of {icon, text} dicts, max 6
    def _validate_badges(raw):
        if raw is None or not isinstance(raw, list):
            return None
        validated = []
        for badge in raw[:6]:
            if isinstance(badge, dict) and badge.get("icon") and badge.get("text"):
                validated.append(
                    {
                        "icon": str(badge["icon"])[:50],
                        "text": str(badge["text"])[:60],
                    }
                )
        return validated

    checkout_badges = _validate_badges(data.get("checkout_trust_badges"))
    if checkout_badges is not None:
        config.checkout_trust_badges = checkout_badges

    product_badges = _validate_badges(data.get("product_trust_badges"))
    if product_badges is not None:
        config.product_trust_badges = product_badges

    digital_badges = _validate_badges(data.get("digital_trust_badges"))
    if digital_badges is not None:
        config.digital_trust_badges = digital_badges

    config.save()

    return JsonResponse({"success": True, "message": "Template configuration saved."})
