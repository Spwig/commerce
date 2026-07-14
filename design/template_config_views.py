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


@staff_member_required
@require_POST
def template_config_save(request):
    """Save template configuration via AJAX."""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"success": False, "message": "Invalid JSON."}, status=400)

    config = PageTemplateConfig.get_config()

    checkout_template = data.get("checkout_template")
    if checkout_template and checkout_template in CHECKOUT_TEMPLATE_META:
        config.checkout_template = checkout_template

    checkout_options = data.get("checkout_options")
    if checkout_options is not None and isinstance(checkout_options, dict):
        config.checkout_options = checkout_options

    product_template = data.get("product_template")
    if product_template and product_template in PRODUCT_TEMPLATE_META:
        config.product_template = product_template

    product_options = data.get("product_options")
    if product_options is not None and isinstance(product_options, dict):
        config.product_options = product_options

    category_template = data.get("category_template")
    if category_template and category_template in CATEGORY_TEMPLATE_META:
        config.category_template = category_template

    category_options = data.get("category_options")
    if category_options is not None and isinstance(category_options, dict):
        config.category_options = category_options

    blog_post_template = data.get("blog_post_template")
    if blog_post_template and blog_post_template in BLOG_POST_TEMPLATE_META:
        config.blog_post_template = blog_post_template

    blog_post_options = data.get("blog_post_options")
    if blog_post_options is not None and isinstance(blog_post_options, dict):
        config.blog_post_options = blog_post_options

    blog_list_template = data.get("blog_list_template")
    if blog_list_template and blog_list_template in BLOG_LIST_TEMPLATE_META:
        config.blog_list_template = blog_list_template

    blog_list_options = data.get("blog_list_options")
    if blog_list_options is not None and isinstance(blog_list_options, dict):
        config.blog_list_options = blog_list_options

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
