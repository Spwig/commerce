"""
Shared translation utilities for applying display translations to model instances.

Used by page builder context providers, announcement tags, widget rendering,
storefront views, and any other code that needs to resolve translated content
at render time.
"""

from django.core.cache import cache

# ---------------------------------------------------------------------------
# Canonical field maps for all translatable storefront models.
# Keys = model field names, Values = JSON key (str) or fallback keys (tuple).
#
# Tuple values try keys in order — first non-empty match wins.  This handles
# the two sources of translation data:
#   • Merchant translation service: uses model field names (short_description)
#   • Theme bot demo data: uses _html suffixed keys (short_description_html)
# ---------------------------------------------------------------------------

PRODUCT_FIELD_MAP = {
    "name": "name",
    "short_description": ("short_description", "short_description_html"),
    "full_description": ("full_description", "description_html"),
    "meta_title": "meta_title",
    "meta_description": "meta_description",
}

CATEGORY_FIELD_MAP = {
    "name": "name",
    "description": "description",
    "meta_title": "meta_title",
    "meta_description": "meta_description",
}

BLOG_POST_FIELD_MAP = {
    "title": "title",
    "excerpt": "excerpt",
    "simple_content": "simple_content",
    "meta_title": "meta_title",
    "meta_description": "meta_description",
}

BLOG_CATEGORY_FIELD_MAP = {
    "name": "name",
    "description": "description",
    "meta_title": "meta_title",
    "meta_description": "meta_description",
}

BLOG_TAG_FIELD_MAP = {
    "name": "name",
}


def get_primary_language():
    """Get the merchant's primary language, with caching to avoid repeated DB hits."""
    primary = cache.get("site_primary_language")
    if primary is None:
        try:
            from core.models import SiteSettings

            primary = SiteSettings.objects.values_list("default_language", flat=True).get(pk=1)
        except Exception:
            from django.conf import settings

            primary = getattr(settings, "LANGUAGE_CODE", "en")
        cache.set("site_primary_language", primary, 300)  # 5 min cache
    return primary


def translate_instance(obj, lang, field_map):
    """
    Override model instance fields in-place with translated values.

    Args:
        obj: A Django model instance with a `translations` JSONField
        lang: Target language code (e.g. 'ar', 'es')
        field_map: Dict mapping model field names to translation JSON keys.
                   Values can be a string (single key) or a tuple of strings
                   (try keys in order, use first non-empty match).
    """
    translations = getattr(obj, "translations", None)
    if not translations or not isinstance(translations, dict):
        return
    lang_data = translations.get(lang)
    if not lang_data:
        return
    for model_field, json_keys in field_map.items():
        if isinstance(json_keys, str):
            json_keys = (json_keys,)
        for key in json_keys:
            value = lang_data.get(key)
            if value:
                setattr(obj, model_field, value)
                break


def translate_menu_items(items, lang):
    """
    Apply translations to MenuItem instances recursively (including children).

    Args:
        items: Iterable of MenuItem instances (top-level)
        lang: Target language code
    """
    field_map = {"title": "title", "badge_text": "badge_text"}
    for item in items:
        translate_instance(item, lang, field_map)
        # Handle nested children (prefetched via children_list or _prefetched_objects_cache)
        children = getattr(item, "children_list", None)
        if children:
            translate_menu_items(children, lang)
        elif (
            hasattr(item, "_prefetched_objects_cache")
            and "children" in item._prefetched_objects_cache
        ):
            translate_menu_items(item._prefetched_objects_cache["children"], lang)


def translate_storefront_context(context, request):
    """
    Apply translations to all translatable model instances in a view context dict.

    Walks context values (single instances, lists, querysets, Page objects) and
    applies the appropriate field map based on model type.  No-op when the
    request language matches the merchant's primary language.

    Call this once in each storefront view, just before ``render()``.

    Args:
        context: Template context dict
        request: Django HttpRequest (must have LANGUAGE_CODE attribute)
    """
    if not request or not hasattr(request, "LANGUAGE_CODE"):
        return

    lang = request.LANGUAGE_CODE
    primary = get_primary_language()
    if lang == primary:
        return  # Most common case — zero overhead

    # Lazy imports to avoid circular dependencies at module load time
    from django.db.models import QuerySet

    from blog.models import BlogCategory, BlogPost, BlogTag
    from catalog.models import Category, Product

    translated_pks = {}  # {model_class: set()} — avoid re-translating shared instances

    def _translate(obj):
        """Translate a single model instance if not already done."""
        cls = type(obj)
        if cls not in translated_pks:
            translated_pks[cls] = set()
        pk = getattr(obj, "pk", None)
        if pk and pk in translated_pks[cls]:
            return
        if pk:
            translated_pks[cls].add(pk)

        if isinstance(obj, Product):
            translate_instance(obj, lang, PRODUCT_FIELD_MAP)
            # Translate select_related category
            cat = getattr(obj, "category", None)
            if cat:
                _translate(cat)
        elif isinstance(obj, Category):
            translate_instance(obj, lang, CATEGORY_FIELD_MAP)
        elif isinstance(obj, BlogPost):
            translate_instance(obj, lang, BLOG_POST_FIELD_MAP)
            cat = getattr(obj, "category", None)
            if cat:
                _translate(cat)
            # Translate prefetched tags (no extra queries)
            prefetched = getattr(obj, "_prefetched_objects_cache", None)
            if prefetched and "tags" in prefetched:
                for tag in prefetched["tags"]:
                    _translate(tag)
        elif isinstance(obj, BlogCategory):
            translate_instance(obj, lang, BLOG_CATEGORY_FIELD_MAP)
        elif isinstance(obj, BlogTag):
            translate_instance(obj, lang, BLOG_TAG_FIELD_MAP)
        else:
            # Handle objects with component_product (e.g. BundleItem)
            comp = getattr(obj, "component_product", None)
            if comp and isinstance(comp, Product):
                _translate(comp)

    for value in context.values():
        if isinstance(value, (list, tuple, QuerySet)):
            for item in value:
                _translate(item)
        elif hasattr(value, "object_list"):
            # Django Paginator Page objects
            for item in value.object_list:
                _translate(item)
        elif hasattr(value, "pk"):
            _translate(value)
