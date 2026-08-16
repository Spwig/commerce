"""
Template tags for theme system
"""

import json

from django import template
from django.conf import settings
from django.core.cache import cache
from django.utils.safestring import mark_safe

register = template.Library()

# Import theme utility for consistent active theme access
from ..theme_utils import get_active_theme_cached


def _nav_object_state(obj, request):
    """Shell-stage visibility state for a nav object (WidgetPlacement / MenuItem):
    ``"show"`` / ``"hide"`` / ``"defer"``.

    Shell rules (geo_region / market, language, currency) and temporal rules are
    evaluated server-side — deterministic per market URL. Per-visitor (deferred)
    rules resolve to ``"defer"`` so the object can be resolved after the shell,
    never leaking into the shared cache. Fail-closed (``"hide"``) on any evaluation
    error — a broken rule must never expose gated nav.
    """
    if request is None:
        # No request context (e.g. management rendering) — can't evaluate rules;
        # show ungated objects, hide anything carrying a rule group.
        try:
            return "show" if not obj.get_visibility_rule_groups().exists() else "hide"
        except Exception:
            return "show"
    try:
        from visibility.service import resolve_visibility

        return resolve_visibility(obj, request)
    except Exception:
        return "hide"


def _menu_widget_defers(placement, request):
    """True if a menu/account widget placement — visible on its own — contains a
    per-visitor (deferred) menu item, so the whole widget must defer and be
    resolved per visitor (its entitled items rendered by the personalization
    pass). Keeps per-visitor items out of the shared cached shell."""
    widget = getattr(placement, "widget", None)
    if not widget or widget.widget_type not in ("menu", "account"):
        return False
    try:
        from visibility.service import requires_personalization

        from ..header_footer_models import Menu

        config = {**(widget.config or {}), **(placement.override_config or {})}
        menu_id = config.get("menu_id")
        menu = None
        if menu_id:
            menu = Menu.objects.filter(pk=menu_id).first()
        elif widget.widget_type == "account":
            menu = Menu.objects.filter(slug="account-menu", is_active=True).first()
        if not menu:
            return False
        items = menu.items.filter(is_active=True).prefetch_related("rule_groups")
        return any(requires_personalization(item) for item in items)
    except Exception:
        return False


def _placement_nav_state(placement, request):
    """Nav state for a widget placement: ``"hide"`` / ``"defer"`` / ``"show"``.

    The placement's own rule groups decide first; a placement that shows but is a
    menu widget carrying a per-visitor item defers as a whole (see
    ``_menu_widget_defers``)."""
    state = _nav_object_state(placement, request)
    if state != "show":
        return state
    if _menu_widget_defers(placement, request):
        return "defer"
    return "show"


def _nav_shell_visible(obj, request):
    """True if the object renders directly in the shell (state == show). Used by
    the widget-zone tags to drop hidden/deferred placements."""
    return _placement_nav_state(obj, request) == "show"


def _filter_visible_menu_items(items, request, full=False):
    """Keep the menu items this visitor should see, preserving order. In the shell
    (``full=False``) only ``show`` items are kept (deferred items are resolved when
    the whole menu widget is personalized). In the personalization pass
    (``full=True``) items are evaluated with the real visitor context."""
    if full:
        from visibility.service import is_fully_visible

        return [item for item in items if is_fully_visible(item, request)]
    return [item for item in items if _nav_object_state(item, request) == "show"]


# Depth cap for nested-menu filtering. The menu templates render at most 3 levels
# (mega mode: item -> child -> subchild); this bounds the walk well past any real
# menu so a merchant-authored parent cycle (the builder does not reject
# ``parent == self`` or a longer loop) can never recurse without limit.
_MAX_MENU_DEPTH = 6


def _annotate_visible_children(items, request, full=False, _depth=0, _seen=None):
    """Recursively annotate each menu item with ``_visible_children`` — the child
    items this market/visitor should see, order-preserving and filtered by the same
    visibility engine as the top level.

    The menu templates iterate ``item.get_children`` / ``item.has_children`` at
    every depth; those methods honour this annotation (see
    ``design.header_footer_models.MenuItem.get_children``), so a per-visitor or
    per-market rule on a NESTED item gates it exactly like a top-level one — closing
    both the shell market-on-child leak and the personalization-pass gap. In the
    shell (``full=False``) a per-visitor child resolves to ``defer`` and is dropped
    here (kept out of the cached shell); the whole menu widget then defers and is
    re-annotated with ``full=True`` in the personalization pass, where the child is
    evaluated against the real visitor.

    Bounded against merchant-authored parent cycles: a per-branch ``_seen`` set of
    item ids breaks any loop, and ``_MAX_MENU_DEPTH`` caps the walk. On the cap a
    node is annotated with no visible children (fail-closed — never render an
    unfiltered subtree).
    """
    if _depth >= _MAX_MENU_DEPTH:
        for item in items:
            item._visible_children = []
        return items
    for item in items:
        seen = set(_seen or ())
        if item.pk in seen:
            item._visible_children = []  # cycle — stop descending
            continue
        seen.add(item.pk)
        children = list(item.get_children().prefetch_related("rule_groups"))
        visible = _filter_visible_menu_items(children, request, full=full)
        item._visible_children = visible
        _annotate_visible_children(visible, request, full=full, _depth=_depth + 1, _seen=seen)
    return items


@register.simple_tag
def theme_css():
    """
    Include all theme CSS files with proper layering
    Usage: {% theme_css %}
    """
    from ..theme_models import ThemeBranding

    css_tags = []

    # 1. Base CSS (platform utilities)
    base_css_url = settings.STATIC_URL + "css/base.css"
    css_tags.append(f'<link rel="stylesheet" href="{base_css_url}">')

    # 2. Theme CSS (from GlobalDesignSettings)
    theme = get_active_theme_cached()
    if theme and theme.get_css_url():
        css_tags.append(f'<link rel="stylesheet" href="{theme.get_css_url()}">')

    # 3. Brand CSS
    try:
        branding = ThemeBranding.objects.first()
        if branding:
            brand_url = branding.get_css_url()
            css_tags.append(f'<link rel="stylesheet" href="{brand_url}">')
    except Exception:
        pass

    return mark_safe("\n".join(css_tags))


@register.simple_tag
def active_theme_css_url():
    """
    Get the CSS URL for the currently active theme.
    Returns the theme CSS URL or empty string if no theme is active.
    Usage: {% active_theme_css_url as theme_css_url %}
    """
    theme = get_active_theme_cached()
    if theme:
        css_url = theme.get_css_url()
        if css_url:
            return css_url
    return ""


@register.simple_tag
def get_active_theme():
    """
    Get the active theme object for use in templates.
    Usage: {% get_active_theme as active_theme %}
    """
    return get_active_theme_cached()


@register.simple_tag
def theme_var(token_name, default=""):
    """
    Get a theme/brand token value
    Usage: {% theme_var 'color-primary' '#3B82F6' %}
    """
    from ..theme_models import ThemeBranding

    # Try cache first
    cache_key = f"theme_token_{token_name}"
    value = cache.get(cache_key)

    if value is None:
        try:
            branding = ThemeBranding.objects.first()
            if branding:
                # Check all token dictionaries
                for token_dict_name in [
                    "color_tokens",
                    "typography_tokens",
                    "spacing_tokens",
                    "border_tokens",
                    "shadow_tokens",
                    "animation_tokens",
                ]:
                    token_dict = getattr(branding, token_dict_name, {})
                    if token_name in token_dict:
                        value = token_dict[token_name]
                        break
        except Exception:
            pass

        if value is None:
            value = default

        # Cache for 5 minutes
        cache.set(cache_key, value, 300)

    return value


@register.simple_tag
def theme_asset(path):
    """
    Get URL for theme asset
    Usage: {% theme_asset 'images/logo.png' %}
    """
    theme = get_active_theme_cached()
    if theme:
        return f"/static/themes/{theme.slug}/{path}"
    return ""


@register.inclusion_tag("design/theme_variables.html")
def theme_variables():
    """
    Include CSS variables for current theme/brand
    Usage: {% theme_variables %}
    """
    from ..theme_models import ThemeBranding

    variables = {}

    # Get theme tokens (from GlobalDesignSettings)
    theme = get_active_theme_cached()
    if theme:
        theme_tokens = theme.get_tokens()
        variables.update(theme_tokens)

    # Override with brand tokens
    try:
        branding = ThemeBranding.objects.first()
        if branding:
            for token_dict_name in [
                "color_tokens",
                "typography_tokens",
                "spacing_tokens",
                "border_tokens",
                "shadow_tokens",
                "animation_tokens",
            ]:
                token_dict = getattr(branding, token_dict_name, {})
                variables.update(token_dict)
    except Exception:
        pass

    return {"variables": variables}


@register.filter
def theme_class(component_type, variant="default"):
    """
    Get theme-specific CSS classes for a component
    Usage: {{ 'button'|theme_class:'primary' }}
    """
    from ..models import ComponentStyle

    cache_key = f"theme_class_{component_type}_{variant}"
    classes = cache.get(cache_key)

    if classes is None:
        try:
            style = ComponentStyle.objects.filter(
                component_type=component_type, variant=variant, is_active=True
            ).first()

            if style and style.css_classes:
                classes = " ".join(style.css_classes.get("classes", []))
            else:
                # Default classes
                default_classes = {
                    "button": "btn",
                    "card": "card",
                    "form": "form-control",
                }
                classes = default_classes.get(component_type, "")
        except Exception:
            classes = ""

        cache.set(cache_key, classes, 300)

    return classes


@register.simple_tag(takes_context=True)
def theme_template(context, template_name, **kwargs):
    """
    Include a theme-specific template
    Usage: {% theme_template 'components/button.html' text='Click me' %}
    """
    from django.template.loader import get_template

    try:
        # Try theme-specific template first
        theme_template_name = f"theme/{template_name}"
        template = get_template(theme_template_name)
    except Exception:
        # Fallback to regular template
        try:
            template = get_template(template_name)
        except Exception:
            return ""

    # Merge context
    template_context = context.flatten()
    template_context.update(kwargs)

    return template.render(template_context)


@register.simple_tag
def critical_css(route=""):
    """
    Include critical CSS for specific route
    Usage: {% critical_css 'home' %}
    """
    from ..theme_models import ThemeAsset

    theme = get_active_theme_cached()
    if not theme:
        return ""

    # Get critical CSS for route
    critical_assets = ThemeAsset.objects.filter(
        theme=theme, asset_type="css", is_critical=True, route=route
    )

    css_content = []
    for asset in critical_assets:
        if asset.file:
            try:
                with open(asset.file.path) as f:
                    css_content.append(f.read())
            except Exception:
                pass

    if css_content:
        return mark_safe(f"<style>{' '.join(css_content)}</style>")

    return ""


@register.simple_tag
def theme_js():
    """
    Include theme JavaScript files
    Usage: {% theme_js %}
    """
    from ..theme_models import ThemeAsset

    theme = get_active_theme_cached()
    if not theme:
        return ""

    js_tags = []

    # Get all JS assets
    js_assets = ThemeAsset.objects.filter(theme=theme, asset_type="js").order_by("path")

    for asset in js_assets:
        js_url = f"/static/themes/{theme.slug}/{asset.path}"
        js_tags.append(f'<script src="{js_url}" defer></script>')

    return mark_safe("\n".join(js_tags))


@register.inclusion_tag("design/theme_meta.html")
def theme_meta():
    """
    Include theme metadata in page head
    Usage: {% theme_meta %}
    """
    from ..theme_utils import get_active_theme_with_metadata

    theme_data = get_active_theme_with_metadata()

    if theme_data:
        return {
            "theme": theme_data["theme"],
            "theme_name": theme_data["name"],
            "theme_version": theme_data["version"],
            "theme_author": theme_data["author"],  # Now from ComponentRegistry (Spwig)
        }

    return {
        "theme": None,
        "theme_name": "Default",
        "theme_version": "1.0.0",
        "theme_author": "",
    }


@register.simple_tag
def widget_config(widget_name):
    """
    Get configuration for a theme widget
    Usage: {% widget_config 'mini-cart' as config %}
    """
    theme = get_active_theme_cached()
    if not theme:
        return {}

    widgets = theme.get_widgets()
    for widget in widgets:
        if widget.get("name") == widget_name:
            return widget.get("config", {})

    return {}


@register.filter
def json_encode(value):
    """
    Encode value as JSON for use in templates
    Usage: {{ my_dict|json_encode }}
    """
    try:
        return mark_safe(json.dumps(value))
    except Exception:
        return "{}"


@register.filter
def get_item(dictionary, key):
    """
    Get an item from a dictionary by key.
    Usage: {{ my_dict|get_item:'key_name' }}
    """
    if dictionary is None:
        return []
    return dictionary.get(key, [])


@register.filter
def zone_override_styles(zone_overrides, zone_name):
    """
    Convert zone_overrides dict to inline CSS string for a specific zone.
    Only outputs styles for properties that have been overridden by merchant.

    Usage: style="{{ zone_overrides|zone_override_styles:'top-bar' }}"

    Input zone_overrides structure:
    {
        "top-bar": {
            "background": "#ff0000",
            "height": 50,
            "text_color": "#ffffff"
        }
    }

    Output: "background: #ff0000; min-height: 50px; color: #ffffff"
    """
    if not zone_overrides or not isinstance(zone_overrides, dict):
        return ""

    overrides = zone_overrides.get(zone_name, {})
    if not overrides:
        return ""

    styles = []

    # Map override keys to CSS properties
    property_map = {
        "background": "background",
        "text_color": "color",
        "height": "min-height",
        "padding_y": "padding-top",  # Will also set padding-bottom
        "padding_x": "padding-left",  # Will also set padding-right
        "border_color": "border-color",
        "font_size": "font-size",
    }

    for key, value in overrides.items():
        if value is None:
            continue

        # Handle nested value objects like {"type": "theme", "value": "..."}
        if isinstance(value, dict) and "value" in value:
            value = value["value"]

        css_prop = property_map.get(key)
        if css_prop:
            # Add units for certain properties
            if key == "height" and isinstance(value, (int, float)):
                value = f"{value}px"

            styles.append(f"{css_prop}: {value}")

            # Handle paired properties
            if key == "padding_y":
                styles.append(f"padding-bottom: {value}")
            elif key == "padding_x":
                styles.append(f"padding-right: {value}")

    return "; ".join(styles)


# =============================================================================
# Header/Footer Template Tags
# =============================================================================


@register.simple_tag
def get_default_header():
    """
    Get the default HeaderTemplate with all widgets and placements.
    Usage: {% get_default_header as header %}
    """
    from ..header_footer_models import HeaderTemplate

    cache_key = "default_header_template"
    header = cache.get(cache_key)

    if header is None:
        try:
            header = (
                HeaderTemplate.objects.filter(is_default=True, is_active=True)
                .prefetch_related("widget_placements", "widget_placements__widget")
                .first()
            )

            # Cache for 5 minutes
            if header:
                cache.set(cache_key, header, 300)
        except Exception:
            header = None

    return header


@register.simple_tag
def get_default_footer():
    """
    Get the default FooterTemplate with all widgets and placements.
    Usage: {% get_default_footer as footer %}
    """
    from ..header_footer_models import FooterTemplate

    cache_key = "default_footer_template"
    footer = cache.get(cache_key)

    if footer is None:
        try:
            footer = (
                FooterTemplate.objects.filter(is_default=True, is_active=True)
                .prefetch_related("widget_placements", "widget_placements__widget")
                .first()
            )

            # Cache for 5 minutes
            if footer:
                cache.set(cache_key, footer, 300)
        except Exception:
            footer = None

    return footer


@register.simple_tag(takes_context=True)
def get_header_widgets_by_zone(context, header, zone_name):
    """
    Get widgets for a specific zone in a header.
    Zone name should be in format 'primary-zone_sub-zone' e.g., 'main-header_left'.
    Usage: {% get_header_widgets_by_zone header 'main-header_left' as widgets %}
    """
    if not header:
        return []

    # The cached candidate list is region-blind on purpose — it holds every
    # active placement in the zone. Shell visibility (market/geo, language,
    # currency, time) is applied per request AFTER the cache read, so one
    # market's decisions never bake into another's cache.
    cache_key = f"header_{header.pk}_widgets_{zone_name}"
    widgets = cache.get(cache_key)

    if widgets is None:
        try:
            placements = (
                header.widget_placements.filter(
                    zone=zone_name, is_active=True, widget__is_active=True
                )
                .prefetch_related("rule_groups")
                .select_related("widget")
                .order_by("order")
            )

            widgets = list(placements)
            cache.set(cache_key, widgets, 300)
        except Exception:
            widgets = []

    request = context.get("request")
    return [p for p in widgets if _nav_shell_visible(p, request)]


@register.simple_tag(takes_context=True)
def get_footer_widgets_by_zone(context, footer, zone_name):
    """
    Get widgets for a specific zone in a footer.
    Usage: {% get_footer_widgets_by_zone footer 'column_1' as widgets %}
    """
    if not footer:
        return []

    # Region-blind candidate cache + per-request shell filter (see
    # get_header_widgets_by_zone).
    cache_key = f"footer_{footer.pk}_widgets_{zone_name}"
    widgets = cache.get(cache_key)

    if widgets is None:
        try:
            placements = (
                footer.widget_placements.filter(
                    zone=zone_name, is_active=True, widget__is_active=True
                )
                .prefetch_related("rule_groups")
                .select_related("widget")
                .order_by("order")
            )

            widgets = list(placements)
            cache.set(cache_key, widgets, 300)
        except Exception:
            widgets = []

    request = context.get("request")
    return [p for p in widgets if _nav_shell_visible(p, request)]


@register.simple_tag(takes_context=True)
def render_widget(context, placement):
    """
    Render a widget with the current template context.
    Usage: {% render_widget placement %}
    """
    if not placement or not placement.widget:
        return ""

    request = context.get("request")

    # Personalization pass (full=True): the widget was deferred in the shell and
    # is being resolved with the real visitor context. Render it only if this
    # visitor is entitled; menu items inside are filtered with full visibility.
    full_visibility = bool(request and getattr(request, "_nav_full_visibility", False))
    if full_visibility:
        from visibility.service import is_fully_visible

        if not is_fully_visible(placement, request):
            return ""
    else:
        # Shell pass: hide → omit; defer → emit a content-less placeholder the
        # personalization endpoint resolves per visitor (never the widget itself,
        # so per-visitor content is never baked into the cached shell).
        state = getattr(placement, "_nav_state", None) or _placement_nav_state(placement, request)
        if state == "hide":
            return ""
        if state == "defer":
            # Carry the URL-authoritative market into the placeholder so the
            # personalization request (which has no /nz/ prefix) evaluates shell
            # geo_region / language rules against the SAME market, not the default.
            market = getattr(request, "market_slug", "") or ""
            return mark_safe(
                f'<div class="pb-nav-defer" data-pb-defer-nav-widget="{placement.id}"'
                f' data-pb-market="{market}"></div>'
            )

    widget = placement.widget

    # Merge widget config with placement overrides
    config = widget.config.copy() if widget.config else {}
    if placement.override_config:
        config.update(placement.override_config)

    # Apply widget translations for non-primary languages (config + content)
    content = widget.content
    if request and hasattr(request, "LANGUAGE_CODE") and widget.translations:
        from core.translation_utils import get_primary_language

        lang = request.LANGUAGE_CODE
        if lang != get_primary_language():
            config = widget.get_translated_config(lang, base_config=config)
            if widget.widget_type in ("text",):
                content = widget.get_translated_content(lang) or content

    # Sanitize content for widgets that render HTML with |safe
    if widget.widget_type in ("text",) and content:
        from ..content_sanitizer import ContentSanitizer

        sanitizer = ContentSanitizer(tier="C")
        content = sanitizer.sanitize_html(content)

    # Sanitize map_embed in contact widget config
    if widget.widget_type == "contact" and config.get("map_embed"):
        from ..content_sanitizer import ContentSanitizer

        sanitizer = ContentSanitizer(tier="C")
        config["map_embed"] = sanitizer.sanitize_html(config["map_embed"])

    # Build widget context
    widget_context = context.flatten()
    widget_context.update(
        {
            "widget": widget,
            "config": config,
            "content": content,
            "placement": placement,
        }
    )

    # Add menu context for menu widgets
    if widget.widget_type == "menu" and config.get("menu_id"):
        from ..header_footer_models import Menu

        try:
            menu = Menu.objects.get(pk=config["menu_id"])
            widget_context["menu"] = menu
            # Apply visibility rules per request, omitting top-level items this
            # market/visitor shouldn't see. In the personalization pass (full
            # mode) items are evaluated against the real visitor context; in the
            # shell only market/geo/language/currency/time items are decided.
            # Nested items are filtered recursively just below.
            menu_items = _filter_visible_menu_items(
                list(menu.get_items().prefetch_related("rule_groups")),
                request,
                full=full_visibility,
            )
            # Recursively filter nested items so a per-visitor / per-market rule on
            # a child gates it the same way it does a top-level item (the template
            # renders children via item.get_children, which honours the annotation).
            _annotate_visible_children(menu_items, request, full=full_visibility)
            # Apply translations for non-primary languages
            if request and hasattr(request, "LANGUAGE_CODE"):
                from core.translation_utils import get_primary_language, translate_menu_items

                lang = request.LANGUAGE_CODE
                if lang != get_primary_language():
                    translate_menu_items(menu_items, lang)
            widget_context["menu_items"] = menu_items
        except Menu.DoesNotExist:
            widget_context["menu"] = None
            widget_context["menu_items"] = []

    # Add account menu items for account widgets
    if widget.widget_type == "account":
        widget_context["menu_items"] = _get_account_menu_items(context, config)

    # Add shippable countries + current selection for ship-to widgets
    if widget.widget_type == "ship_to":
        widget_context.update(_get_ship_to_context(context.get("request")))

    try:
        from django.template.loader import render_to_string

        return mark_safe(render_to_string(widget.get_template_path(), widget_context))
    except Exception as e:
        if settings.DEBUG:
            return mark_safe(f"<!-- Widget error: {e} -->")
        return ""


def _get_ship_to_context(request):
    """Widget context for the ship-to selector (see get_ship_to_options)."""
    from catalog.middleware import get_ship_to_options

    opts = get_ship_to_options(request)
    return {
        "ship_to_countries": opts["countries"],
        "current_ship_to_code": opts["current_code"],
        "current_ship_to_name": opts["current_name"],
    }


def _get_account_menu_items(context, config):
    """
    Get account menu items filtered by visibility rules.
    Returns list of menu items appropriate for current user's authentication state.
    """
    from ..header_footer_models import Menu

    # Get menu by ID from config, or use default account-menu
    menu_id = config.get("menu_id")
    menu = None

    if menu_id:
        menu = Menu.objects.filter(id=menu_id, is_active=True).first()

    if not menu:
        # Fall back to default account menu
        menu = Menu.objects.filter(slug="account-menu", is_active=True).first()

    if not menu:
        return []

    # Get user authentication state from context
    request = context.get("request")
    user = getattr(request, "user", None) if request else context.get("user")
    is_authenticated = user.is_authenticated if user else False
    is_staff = getattr(user, "is_staff", False) if user else False

    # Get all active menu items
    items = list(
        menu.items.filter(is_active=True, parent__isnull=True)
        .prefetch_related("rule_groups")
        .order_by("order")
    )

    # Apply translations for non-primary languages
    if request and hasattr(request, "LANGUAGE_CODE"):
        from core.translation_utils import get_primary_language, translate_instance

        lang = request.LANGUAGE_CODE
        if lang != get_primary_language():
            menu_field_map = {"title": "title", "badge_text": "badge_text"}
            for item in items:
                translate_instance(item, lang, menu_field_map)

    # Filter by visibility rules: the legacy shallow user_status JSON AND the
    # shared engine. In the personalization pass (full mode) items are evaluated
    # against the real visitor context; in the shell only market/geo/language/
    # currency/time items are decided (deferred items resolve when the whole
    # account widget is personalized). Legacy stays live until the engine fully
    # supersedes it.
    full_visibility = bool(request and getattr(request, "_nav_full_visibility", False))

    def _engine_ok(item):
        if full_visibility:
            from visibility.service import is_fully_visible

            return is_fully_visible(item, request)
        return _nav_object_state(item, request) == "show"

    filtered_items = []
    for item in items:
        if _should_show_menu_item(item, is_authenticated) and _engine_ok(item):
            filtered_items.append(
                {
                    "title": item.title,
                    "url": item.url,
                    "icon": item.icon,
                    "item_type": item.item_type,
                    "target": item.target,
                    "css_classes": item.css_classes,
                }
            )

    # Add admin panel link for staff users
    if is_authenticated and is_staff:
        # Insert before last item (Sign Out)
        admin_item = {
            "title": "Admin Panel",
            "url": "/admin/",
            "icon": "fas fa-cog",
            "item_type": "custom_url",
            "target": "_blank",
            "css_classes": "",
        }
        # Find position before Sign Out (usually last item)
        insert_pos = len(filtered_items) - 1 if filtered_items else 0
        filtered_items.insert(insert_pos, admin_item)

    return filtered_items


def _should_show_menu_item(item, is_authenticated):
    """
    Check if a menu item should be shown based on visibility rules.
    """
    visibility_rules = item.visibility_rules or []

    # No rules = always show
    if not visibility_rules:
        return True

    for rule in visibility_rules:
        rule_type = rule.get("type")
        rule_value = rule.get("value")

        if rule_type == "user_status":
            if rule_value == "logged_in" and not is_authenticated:
                return False
            if rule_value == "logged_out" and is_authenticated:
                return False

    return True


@register.inclusion_tag("design/components/header.html", takes_context=True)
def render_header(context, page=None):
    """
    Render header with support for page-specific templates.

    Priority:
    1. If page.hide_header is True -> return hidden=True (no header rendered)
    2. If page.header_template is set -> use that template
    3. Otherwise -> use site default (is_default=True)

    Usage:
        {% render_header %}                    {# Uses site default #}
        {% render_header page=page %}          {# Uses page-specific or default #}
    """
    from ..header_footer_models import HeaderTemplate

    # Check if page wants to hide header
    if page and getattr(page, "hide_header", False):
        return {
            "header": None,
            "zones": {},
            "hidden": True,
            "request": context.get("request"),
            "user": context.get("user"),
            "design_settings": context.get("design_settings"),
            "site_settings": context.get("site_settings"),
        }

    header = None
    zones = {}

    try:
        # Try page-specific header first
        if page and getattr(page, "header_template_id", None):
            header = (
                HeaderTemplate.objects.filter(id=page.header_template_id, is_active=True)
                .prefetch_related("widget_placements", "widget_placements__widget")
                .first()
            )

        # Fallback to site default
        if not header:
            header = (
                HeaderTemplate.objects.filter(is_default=True, is_active=True)
                .prefetch_related("widget_placements", "widget_placements__widget")
                .first()
            )

        if header:
            request = context.get("request")
            # Group widget placements by zone, applying shell visibility rules
            # (market/geo, language, currency, time) per request — omitting a
            # placement the current market/visitor shouldn't see.
            for placement in (
                header.widget_placements.filter(is_active=True, widget__is_active=True)
                .prefetch_related("rule_groups")
                .select_related("widget")
                .order_by("order")
            ):
                state = _placement_nav_state(placement, request)
                if state == "hide":
                    continue
                # Keep deferred placements in the zone — render_widget emits a
                # per-visitor placeholder for them; the annotation avoids re-eval.
                placement._nav_state = state
                zone = placement.zone.replace("-", "_")
                if zone not in zones:
                    zones[zone] = []
                zones[zone].append(placement)

    except Exception:
        pass

    # Get zone overrides for inline style application
    zone_overrides = {}
    if header:
        zone_overrides = getattr(header, "zone_overrides", {}) or {}

    return {
        "header": header,
        "zones": zones,
        "zone_overrides": zone_overrides,
        "hidden": False,
        "request": context.get("request"),
        "user": context.get("user"),
        "design_settings": context.get("design_settings"),
        "site_settings": context.get("site_settings"),
    }


@register.inclusion_tag("design/components/footer.html", takes_context=True)
def render_footer(context, page=None):
    """
    Render footer with support for page-specific templates.

    Priority:
    1. If page.hide_footer is True -> return hidden=True (no footer rendered)
    2. If page.footer_template is set -> use that template
    3. Otherwise -> use site default (is_default=True)

    Usage:
        {% render_footer %}                    {# Uses site default #}
        {% render_footer page=page %}          {# Uses page-specific or default #}
    """
    from ..header_footer_models import FooterTemplate

    # Check if page wants to hide footer
    if page and getattr(page, "hide_footer", False):
        return {
            "footer": None,
            "zones": {},
            "hidden": True,
            "request": context.get("request"),
            "user": context.get("user"),
            "design_settings": context.get("design_settings"),
            "site_settings": context.get("site_settings"),
        }

    footer = None
    zones = {}

    try:
        # Try page-specific footer first
        if page and getattr(page, "footer_template_id", None):
            footer = (
                FooterTemplate.objects.filter(id=page.footer_template_id, is_active=True)
                .prefetch_related("widget_placements", "widget_placements__widget")
                .first()
            )

        # Fallback to site default
        if not footer:
            footer = (
                FooterTemplate.objects.filter(is_default=True, is_active=True)
                .prefetch_related("widget_placements", "widget_placements__widget")
                .first()
            )

        if footer:
            request = context.get("request")
            # Group widget placements by zone, applying shell visibility rules per
            # request (see render_header).
            for placement in (
                footer.widget_placements.filter(is_active=True, widget__is_active=True)
                .prefetch_related("rule_groups")
                .select_related("widget")
                .order_by("order")
            ):
                state = _placement_nav_state(placement, request)
                if state == "hide":
                    continue
                # Keep deferred placements in the zone — render_widget emits a
                # per-visitor placeholder for them; the annotation avoids re-eval.
                placement._nav_state = state
                zone = placement.zone.replace("-", "_")
                if zone not in zones:
                    zones[zone] = []
                zones[zone].append(placement)

    except Exception:
        pass

    return {
        "footer": footer,
        "zones": zones,
        "hidden": False,
        "request": context.get("request"),
        "user": context.get("user"),
        "design_settings": context.get("design_settings"),
        "site_settings": context.get("site_settings"),
    }


@register.simple_tag(takes_context=True)
def header_widget_css(context, header=None, page=None):
    """
    Generate CSS link tags for all widgets in a header.

    Usage:
        {% header_widget_css %}
        {% header_widget_css header=header_obj %}
        {% header_widget_css page=page %}

    Priority:
    1. Use provided header parameter if given
    2. Check page's header_template_id if page is provided
    3. Fall back to default header
    """
    from ..header_footer_models import HeaderTemplate

    # If no header provided, try to get from page or default
    if header is None:
        # Try page-specific header first
        if page is None:
            page = context.get("page")

        if page and getattr(page, "header_template_id", None):
            try:
                header = (
                    HeaderTemplate.objects.filter(id=page.header_template_id, is_active=True)
                    .prefetch_related("widget_placements", "widget_placements__widget")
                    .first()
                )
            except Exception:
                pass

        # Fallback to default header
        if header is None:
            try:
                header = (
                    HeaderTemplate.objects.filter(is_default=True, is_active=True)
                    .prefetch_related("widget_placements", "widget_placements__widget")
                    .first()
                )
            except Exception:
                return ""

    if not header:
        return ""

    css_urls = set()
    try:
        for placement in header.widget_placements.filter(
            is_active=True, widget__is_active=True
        ).select_related("widget"):
            css_url = placement.widget.get_css_url()
            if css_url:
                css_urls.add(css_url)
    except Exception:
        pass

    links = [f'<link rel="stylesheet" href="{url}">' for url in css_urls]
    return mark_safe("\n".join(links))


@register.simple_tag(takes_context=True)
def footer_widget_css(context, footer=None, page=None):
    """
    Generate CSS link tags for all widgets in a footer.

    Usage:
        {% footer_widget_css %}
        {% footer_widget_css footer=footer_obj %}
        {% footer_widget_css page=page %}

    Priority:
    1. Use provided footer parameter if given
    2. Check page's footer_template_id if page is provided
    3. Fall back to default footer
    """
    from ..header_footer_models import FooterTemplate

    # If no footer provided, try to get from page or default
    if footer is None:
        # Try page-specific footer first
        if page is None:
            page = context.get("page")

        if page and getattr(page, "footer_template_id", None):
            try:
                footer = (
                    FooterTemplate.objects.filter(id=page.footer_template_id, is_active=True)
                    .prefetch_related("widget_placements", "widget_placements__widget")
                    .first()
                )
            except Exception:
                pass

        # Fallback to default footer
        if footer is None:
            try:
                footer = (
                    FooterTemplate.objects.filter(is_default=True, is_active=True)
                    .prefetch_related("widget_placements", "widget_placements__widget")
                    .first()
                )
            except Exception:
                return ""

    if not footer:
        return ""

    css_urls = set()
    try:
        for placement in footer.widget_placements.filter(
            is_active=True, widget__is_active=True
        ).select_related("widget"):
            css_url = placement.widget.get_css_url()
            if css_url:
                css_urls.add(css_url)
    except Exception:
        pass

    links = [f'<link rel="stylesheet" href="{url}">' for url in css_urls]
    return mark_safe("\n".join(links))


@register.simple_tag(takes_context=True)
def notification_zone_assets(context, page=None):
    """
    Conditionally load notification zone CSS + JS.
    Only emits tags when the active header has enable_notification_zone=True.
    """
    from django.templatetags.static import static as static_url

    from ..header_footer_models import HeaderTemplate

    header = None
    try:
        if page is None:
            page = context.get("page")

        if page and getattr(page, "header_template_id", None):
            header = (
                HeaderTemplate.objects.filter(id=page.header_template_id, is_active=True)
                .only("enable_notification_zone")
                .first()
            )
        if not header:
            header = (
                HeaderTemplate.objects.filter(is_default=True, is_active=True)
                .only("enable_notification_zone")
                .first()
            )
    except Exception:
        return ""

    if not header or not header.enable_notification_zone:
        return ""

    css = static_url("design/css/widgets/announcement.css")
    js = static_url("design/js/announcement-widget.js")
    return mark_safe(f'<link rel="stylesheet" href="{css}">\n<script src="{js}" defer></script>')
