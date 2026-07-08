from django import template
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from ..element_registry import get_registry
from ..models import Element
from ..context_providers import get_element_context, ELEMENT_CONTEXT_PROVIDERS
import logging

register = template.Library()
logger = logging.getLogger(__name__)

@register.inclusion_tag('page_builder/elements/element_wrapper.html', takes_context=True)
def render_element(context, element):
    """
    Render an element using the new modular element system.
    Falls back to old templates if modular version doesn't exist.
    """
    registry = get_registry()
    element_config = registry.get_element(element.element_type)

    # Check if we're in builder context
    request = context.get('request')
    is_builder = False
    if request and request.path:
        is_builder = '/admin/page_builder/builder/' in request.path or '/visual-builder/' in request.path

    template_path = None
    use_modular = False

    if element_config:
        # Use modular template
        if is_builder:
            template_path = f"page_builder/elements/{element.element_type}/template.html"
        else:
            # Try frontend template first, fall back to regular template
            try:
                get_template(f"page_builder/elements/{element.element_type}/frontend.html")
                template_path = f"page_builder/elements/{element.element_type}/frontend.html"
            except:
                template_path = f"page_builder/elements/{element.element_type}/template.html"
        use_modular = True
    else:
        # Fallback to old template structure
        template_path = f"page_builder/elements/{element.element_type}.html"

    # Try to load the template
    try:
        template = get_template(template_path)

        # Get the current language from the request
        current_language = None
        if request:
            current_language = request.LANGUAGE_CODE if hasattr(request, 'LANGUAGE_CODE') else None

        # Get translated content for the element
        original_content = element.content
        if current_language:
            # Temporarily replace element content with translated version
            element.content = element.get_translated_content(current_language)

        # Get dynamic context from context providers
        # Called for elements with data_source='dynamic' OR elements that have a registered provider
        dynamic_context = {}
        content = element.content or {}
        if content.get('data_source') == 'dynamic' or element.element_type in ELEMENT_CONTEXT_PROVIDERS:
            dynamic_context = get_element_context(element.element_type, content, request)

        # Create a fresh context for rendering
        element_context = context.flatten()
        element_context.update({
            'element': element,
            'element_config': element_config,
            'element_context': dynamic_context
        })

        rendered_content = template.render(element_context)

        # Restore original content (don't modify the database object)
        element.content = original_content
        
        logger.debug(f"Successfully rendered element {element.element_type} using {'modular' if use_modular else 'legacy'} template")
        
        return {
            'element': element,
            'element_config': element_config,
            'rendered_content': mark_safe(rendered_content),
            'use_modular': use_modular,
            'template_path': template_path
        }
    except Exception as e:
        logger.error(f"Failed to render element {element.element_type}: {str(e)}")
        
        # Return error state
        return {
            'element': element,
            'element_config': None,
            'rendered_content': mark_safe(f'<div class="element-error bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">Element "{element.element_type}" failed to render: {str(e)}</div>'),
            'use_modular': False,
            'template_path': template_path,
            'error': str(e)
        }


@register.simple_tag(takes_context=True)
def resolve_element_context(context, element):
    """
    Resolve dynamic context for an element via its context provider.
    Used by the visual builder partial to provide element_context to included templates.
    """
    content = element.content or {}
    request = context.get('request')
    if content.get('data_source') == 'dynamic' or element.element_type in ELEMENT_CONTEXT_PROVIDERS:
        try:
            return get_element_context(element.element_type, content, request)
        except Exception:
            return {}
    return {}


@register.simple_tag
def get_reviews_list(element, element_context):
    """
    Resolve the correct reviews list based on data_source setting.
    For 'static' data_source, returns element.content.reviews (normalized).
    For 'dynamic', returns element_context.reviews from the context provider.

    Static reviews use 'content' for review text (from config.json),
    but templates use 'comment' (matching the ProductReview model).
    This tag normalizes static reviews so templates can use 'comment' consistently.
    """
    content = element.content or {}
    if content.get('data_source') == 'static':
        reviews = content.get('reviews')
        if not isinstance(reviews, list):
            return []
        # Normalize static review dicts: map 'content' → 'comment'
        normalized = []
        for r in reviews:
            if isinstance(r, dict):
                review = dict(r)
                if 'content' in review and 'comment' not in review:
                    review['comment'] = review.pop('content')
                normalized.append(review)
        return normalized
    # Dynamic: use context provider reviews
    if isinstance(element_context, dict):
        return element_context.get('reviews') or []
    return []


@register.simple_tag
def get_element_template_path(element_type):
    """Get the template path for an element type"""
    registry = get_registry()
    element_config = registry.get_element(element_type)
    
    if element_config:
        return f"page_builder/elements/{element_type}/template.html"
    else:
        return f"page_builder/elements/{element_type}.html"


@register.simple_tag
def get_element_config(element_type):
    """Get configuration for an element type"""
    registry = get_registry()
    return registry.get_element(element_type)


@register.filter
def has_modular_template(element_type):
    """Check if an element has a modular template"""
    registry = get_registry()
    return registry.get_element(element_type) is not None


@register.inclusion_tag('page_builder/elements/element_debug.html')
def debug_element(element):
    """Debug template tag for development"""
    registry = get_registry()
    element_config = registry.get_element(element.element_type)

    return {
        'element': element,
        'element_config': element_config,
        'has_modular': element_config is not None,
        'registry_count': len(registry.get_all_elements())
    }


@register.simple_tag
def get_page_elements(page):
    """Get all top-level elements that belong directly to a page"""
    return Element.objects.filter(
        page=page,
        parent_element__isnull=True
    ).order_by('order')


@register.inclusion_tag('page_builder/includes/sidebar_elements.html')
def render_sidebar_elements():
    """
    Render the element sidebar for the visual builder.
    Returns all available elements organized by category in display order.
    """
    registry = get_registry()
    categories = registry.get_elements_for_sidebar()
    return {'categories': categories}


@register.simple_tag
def base_styles(element, exclude=''):
    """
    Render CSS styles from base properties inherited via inherit_base: true.

    Base properties include:
    - background: Full CSS value (e.g., "linear-gradient(...)" or "url(...)")
    - border: CSS string with properties (e.g., "border-width: 2px; border-style: solid;")
    - box_shadow: CSS value (e.g., "0 4px 6px rgba(0,0,0,0.1)")
    - opacity: Number from 0 to 1
    - rounded: Preset value (sm, md, lg, xl, 2xl, 3xl, full)
    - z_index: Integer for stacking order

    Args:
        element: The page builder element
        exclude: Comma-separated list of properties to exclude (e.g., 'box_shadow' or 'box_shadow,opacity')

    Usage in templates:
        style="{% base_styles element %} other-styles: value;"
        style="{% base_styles element exclude='box_shadow' %}"
    """
    from django.utils.html import escape

    if not element or not hasattr(element, 'content'):
        return ''

    content = element.content or {}
    styles = []

    # Parse excluded properties
    excluded = [p.strip() for p in exclude.split(',') if p.strip()] if exclude else []

    # Background (stored as CSS value only)
    if 'background' not in excluded:
        background = content.get('background')
        if background:
            # Escape quotes for HTML attribute safety
            styles.append(f'background: {escape(background)};')

    # Border (stored as full CSS string with property names)
    if 'border' not in excluded:
        border = content.get('border')
        if border:
            styles.append(escape(border))

    # Border Radius presets (from base 'rounded' property)
    if 'rounded' not in excluded:
        rounded = content.get('rounded')
        if rounded:
            radius_map = {
                'sm': '0.125rem',
                'md': '0.375rem',
                'lg': '0.5rem',
                'xl': '0.75rem',
                '2xl': '1rem',
                '3xl': '1.5rem',
                'full': '9999px',
            }
            if rounded in radius_map:
                styles.append(f'border-radius: {radius_map[rounded]};')

    # Box Shadow (stored as CSS value only)
    if 'box_shadow' not in excluded:
        box_shadow = content.get('box_shadow')
        if box_shadow:
            styles.append(f'box-shadow: {escape(box_shadow)};')

    # Opacity
    if 'opacity' not in excluded:
        opacity = content.get('opacity')
        if opacity is not None and opacity != 1 and opacity != '1':
            styles.append(f'opacity: {opacity};')

    # Z-Index
    if 'z_index' not in excluded:
        z_index = content.get('z_index')
        if z_index is not None:
            styles.append(f'z-index: {z_index};')

    # Custom styles (raw CSS)
    if 'custom_styles' not in excluded:
        custom_styles = content.get('custom_styles')
        if custom_styles:
            styles.append(escape(custom_styles))

    # Hover Animation Transition Properties
    hover_type = content.get('hover_animation_type')
    if hover_type and 'hover_animation' not in excluded:
        hover_duration = content.get('hover_animation_duration', '0.3s')
        hover_timing = content.get('hover_animation_timing', 'ease-out')
        styles.append(f'transition-duration: {escape(hover_duration)};')
        styles.append(f'transition-timing-function: {escape(hover_timing)};')
        styles.append('transition-property: transform, opacity, filter, box-shadow, border-color;')

    # Return as mark_safe since we've manually escaped dangerous characters
    return mark_safe(' '.join(styles))


@register.filter
def focal_point_css(focal_point):
    """
    Convert focal point data to CSS object-position value.

    Handles:
    - Dict format: {"x": 0.65, "y": 0.40}
    - Nested format: {"default": {"x": 0.65, "y": 0.40}}
    - String format: "0.65 0.40" or "65% 40%"
    - JSON string: '{"x": 0.65, "y": 0.40}'

    Returns CSS value like "65% 40%"
    """
    import json

    if not focal_point:
        return "center"

    x, y = 0.5, 0.5  # Default to center

    try:
        # Handle string input (might be JSON)
        if isinstance(focal_point, str):
            focal_point = focal_point.strip()
            if focal_point.startswith('{'):
                focal_point = json.loads(focal_point)
            else:
                # Try parsing "65% 40%" or "0.65 0.40" format
                import re
                match = re.match(r'(\d+(?:\.\d+)?)\s*%?\s+(\d+(?:\.\d+)?)\s*%?', focal_point)
                if match:
                    val1, val2 = float(match.group(1)), float(match.group(2))
                    # If values are > 1, assume percentages
                    x = val1 / 100 if val1 > 1 else val1
                    y = val2 / 100 if val2 > 1 else val2
                    return f"{int(x * 100)}% {int(y * 100)}%"
                return focal_point  # Return as-is if can't parse

        # Handle dict input
        if isinstance(focal_point, dict):
            if 'default' in focal_point:
                x = focal_point['default'].get('x', 0.5)
                y = focal_point['default'].get('y', 0.5)
            elif 'x' in focal_point:
                x = focal_point.get('x', 0.5)
                y = focal_point.get('y', 0.5)

    except (json.JSONDecodeError, TypeError, ValueError, AttributeError):
        return "center"

    # Convert to percentage
    x_pct = int(float(x) * 100)
    y_pct = int(float(y) * 100)

    return f"{x_pct}% {y_pct}%"


@register.simple_tag
def focal_point_responsive_css(element):
    """
    Generate responsive CSS for focal point with breakpoint support.

    For elements with responsive focal points (tablet/mobile overrides),
    this outputs a <style> block with media queries.

    Usage in templates:
        {% focal_point_responsive_css element %}
    """
    import json

    if not element or not hasattr(element, 'content'):
        return ''

    content = element.content or {}
    focal_point = content.get('focal_point')

    if not focal_point:
        return ''

    # Parse if string
    if isinstance(focal_point, str):
        try:
            focal_point = json.loads(focal_point)
        except json.JSONDecodeError:
            return ''

    if not isinstance(focal_point, dict):
        return ''

    # Check if there are responsive breakpoints
    has_tablet = 'tablet' in focal_point
    has_mobile = 'mobile' in focal_point

    if not has_tablet and not has_mobile:
        return ''  # No responsive styles needed

    # Get element ID for targeting
    element_id = element.id

    styles = []
    styles.append(f'<style>')

    # Default focal point
    default_fp = focal_point.get('default', focal_point)
    if isinstance(default_fp, dict) and 'x' in default_fp:
        default_x = int(float(default_fp.get('x', 0.5)) * 100)
        default_y = int(float(default_fp.get('y', 0.5)) * 100)
        styles.append(f'.pb-image__img[data-element-id="{element_id}"] {{')
        styles.append(f'  --fp-x: {default_x}%;')
        styles.append(f'  --fp-y: {default_y}%;')
        styles.append(f'  object-position: var(--fp-x) var(--fp-y);')
        styles.append(f'}}')

    # Tablet breakpoint
    if has_tablet:
        tablet_fp = focal_point['tablet']
        if isinstance(tablet_fp, dict) and 'x' in tablet_fp:
            tablet_x = int(float(tablet_fp.get('x', 0.5)) * 100)
            tablet_y = int(float(tablet_fp.get('y', 0.5)) * 100)
            styles.append(f'@media (max-width: 1024px) {{')
            styles.append(f'  .pb-image__img[data-element-id="{element_id}"] {{')
            styles.append(f'    --fp-x: {tablet_x}%;')
            styles.append(f'    --fp-y: {tablet_y}%;')
            styles.append(f'  }}')
            styles.append(f'}}')

    # Mobile breakpoint
    if has_mobile:
        mobile_fp = focal_point['mobile']
        if isinstance(mobile_fp, dict) and 'x' in mobile_fp:
            mobile_x = int(float(mobile_fp.get('x', 0.5)) * 100)
            mobile_y = int(float(mobile_fp.get('y', 0.5)) * 100)
            styles.append(f'@media (max-width: 640px) {{')
            styles.append(f'  .pb-image__img[data-element-id="{element_id}"] {{')
            styles.append(f'    --fp-x: {mobile_x}%;')
            styles.append(f'    --fp-y: {mobile_y}%;')
            styles.append(f'  }}')
            styles.append(f'}}')

    styles.append(f'</style>')

    return mark_safe('\n'.join(styles))


@register.simple_tag
def hover_animation_attrs(element):
    """
    Render data attributes for hover animations.

    Outputs:
    - data-hover-animation: The hover animation type (e.g., "scale-up", "lift-shadow")
    - data-hover-intensity: The intensity level (subtle, normal, strong) for effects that support it

    Usage in templates:
        <div {% hover_animation_attrs element %}>

    Example output:
        data-hover-animation="lift-shadow" data-hover-intensity="normal"
    """
    if not element or not hasattr(element, 'content'):
        return ''

    content = element.content or {}
    attrs = []

    hover_type = content.get('hover_animation_type')
    if hover_type:
        attrs.append(f'data-hover-animation="{hover_type}"')

        # Add intensity for effects that support it
        intensity_effects = ['scale-up', 'scale-down', 'lift', 'rotate-cw', 'rotate-ccw',
                            'shadow-grow', 'lift-shadow', 'zoom-brighten', 'skew']
        if hover_type in intensity_effects:
            intensity = content.get('hover_animation_intensity', 'normal')
            attrs.append(f'data-hover-intensity="{intensity}"')

    return mark_safe(' '.join(attrs))


@register.simple_tag
def entrance_animation_attrs(element):
    """
    Render data attributes for entrance animations.

    Outputs:
    - data-entrance-animation: The animation type (e.g., "fadeIn", "spin")
    - data-entrance-duration: Duration (e.g., "0.5s", "1s")
    - data-entrance-delay: Delay before animation starts (e.g., "0s", "0.3s")
    - data-entrance-timing: Timing function (e.g., "ease-out", "linear")
    - data-entrance-repeat: Iteration count ("1" or "infinite")

    Usage in templates:
        <div {% entrance_animation_attrs element %}>

    Example output:
        data-entrance-animation="spin" data-entrance-duration="1s" data-entrance-repeat="1"
    """
    if not element or not hasattr(element, 'content'):
        return ''

    content = element.content or {}
    attrs = []

    animation_type = content.get('animation_type')
    if animation_type:
        attrs.append(f'data-entrance-animation="{animation_type}"')

        # Duration
        duration = content.get('animation_duration')
        if duration:
            attrs.append(f'data-entrance-duration="{duration}"')

        # Delay
        delay = content.get('animation_delay')
        if delay:
            attrs.append(f'data-entrance-delay="{delay}"')

        # Timing function
        timing = content.get('animation_timing')
        if timing:
            attrs.append(f'data-entrance-timing="{timing}"')

        # Iteration count (once = 1, infinite = infinite)
        repeat = content.get('animation_repeat')
        if repeat:
            attrs.append(f'data-entrance-repeat="{repeat}"')

    return mark_safe(' '.join(attrs))


@register.simple_tag
def entrance_animation_class(element):
    """
    Render the CSS class for entrance animation.

    Usage in templates:
        <div class="{% entrance_animation_class element %}">

    Example output:
        animate-spin
    """
    if not element or not hasattr(element, 'content'):
        return ''

    content = element.content or {}
    animation_type = content.get('animation_type')

    if animation_type:
        return f'animate-{animation_type}'

    return ''


@register.simple_tag
def element_style_vars(element, element_type, raw=False):
    """
    Generate CSS custom property declarations for element instance overrides.
    Only outputs variables that have been explicitly set by merchant.

    This enables the three-level token cascade:
        1. Instance override (from this tag) → 2. Element token → 3. Base token

    Usage in templates:
        <!-- As complete style attribute -->
        <div {% element_style_vars element 'divider' %}>

        <!-- As raw CSS declarations (for combining with other styles) -->
        <div style="{% element_style_vars element 'divider' raw=True %}other-style: value;">

    Example output:
        style="--divider-color: #ff0000; --divider-thickness: 2px;"
        (or with raw=True: "--divider-color: #ff0000; --divider-thickness: 2px; ")

    Args:
        element: The Element model instance
        element_type: String identifying the element type (e.g., 'divider', 'hero')
        raw: If True, returns just the CSS declarations without style="" wrapper

    Returns:
        Safe HTML string with style attribute (or raw CSS if raw=True), empty string if no overrides.
    """
    if not element or not hasattr(element, 'content'):
        return ''

    content = element.content or {}
    style_vars = []

    # Property mappings for each element type
    # Maps content property names to CSS variable names and optional value formatters
    # Note: divider, button, heading now use direct inline styles (no CSS variable mapping)
    property_maps = {
        'hero': {
            'min_height': ('--hero-min-height', None),
            'padding_y': ('--hero-padding-y', 'rem'),
            'padding_x': ('--hero-padding-x', 'rem'),
            'title_color': ('--hero-title-color', None),
            'title_size': ('--hero-title-size', 'rem'),
            'subtitle_color': ('--hero-subtitle-color', None),
            'subtitle_size': ('--hero-subtitle-size', 'rem'),
            'overlay_color': ('--hero-overlay-color', None),
            'overlay_opacity': ('--hero-overlay-opacity', None),
        },
        'card': {
            'background_color': ('--card-bg', None),
            'border_color': ('--card-border', None),
            'border_radius': ('--card-radius', None),
            'padding': ('--card-padding', None),
            'shadow': ('--card-shadow', None),
        },
        'form': {
            'input_bg': ('--form-input-bg', None),
            'input_border': ('--form-input-border', None),
            'input_radius': ('--form-input-radius', None),
            'label_color': ('--form-label-color', None),
        },
        'product': {
            'card_radius': ('--product-card-radius', None),
            'card_shadow': ('--product-card-shadow', None),
            'price_color': ('--product-price-color', None),
            'sale_price_color': ('--product-sale-price-color', None),
            'grid_gap': ('--product-grid-gap', None),
        },
    }

    prop_map = property_maps.get(element_type, {})

    for prop, (css_var, unit) in prop_map.items():
        value = content.get(prop)
        # Only include if value is explicitly set (not None or empty string)
        if value is not None and value != '':
            # Apply unit suffix if specified
            if unit:
                # Try to convert string numbers to actual numbers for unit appending
                try:
                    numeric_value = float(value) if isinstance(value, str) else value
                    if isinstance(numeric_value, (int, float)):
                        # Use int if it's a whole number for cleaner output
                        if numeric_value == int(numeric_value):
                            style_vars.append(f'{css_var}: {int(numeric_value)}{unit}')
                        else:
                            style_vars.append(f'{css_var}: {numeric_value}{unit}')
                    else:
                        style_vars.append(f'{css_var}: {value}')
                except (ValueError, TypeError):
                    # Not a number, use value as-is (might already include unit)
                    style_vars.append(f'{css_var}: {value}')
            else:
                style_vars.append(f'{css_var}: {value}')

    if style_vars:
        css_declarations = '; '.join(style_vars) + '; '
        if raw:
            return mark_safe(css_declarations)
        return mark_safe(f'style="{css_declarations}"')
    return ''


@register.simple_tag
def entrance_animation_styles(element):
    """
    Render inline styles for entrance animation properties.

    Outputs CSS for animation-duration, animation-delay, animation-timing-function,
    and animation-iteration-count to override defaults in the CSS classes.

    Usage in templates:
        style="{% entrance_animation_styles element %} other-styles: value;"

    Example output:
        animation-duration: 1s; animation-delay: 0.3s; animation-iteration-count: 1;
    """
    if not element or not hasattr(element, 'content'):
        return ''

    content = element.content or {}
    styles = []

    animation_type = content.get('animation_type')
    if not animation_type:
        return ''

    # Duration
    duration = content.get('animation_duration')
    if duration:
        styles.append(f'animation-duration: {duration};')

    # Delay
    delay = content.get('animation_delay')
    if delay:
        styles.append(f'animation-delay: {delay};')

    # Timing function
    timing = content.get('animation_timing')
    if timing:
        styles.append(f'animation-timing-function: {timing};')

    # Iteration count
    repeat = content.get('animation_repeat')
    if repeat:
        styles.append(f'animation-iteration-count: {repeat};')

    # Always set fill-mode to keep final state
    styles.append('animation-fill-mode: both;')

    return mark_safe(' '.join(styles))