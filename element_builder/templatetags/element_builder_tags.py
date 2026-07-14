"""
Element Builder Template Tags

Provides template tags for rendering custom elements using page_builder templates.
Custom elements are composed of page_builder Elements with data bindings.
"""

from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from element_builder.services import apply_bindings_to_element

register = template.Library()


def _render_element_tree(element, instance, bindings, request=None):
    """
    Recursively render an element tree with bindings applied.

    Args:
        element: page_builder.Element instance (root or child)
        instance: Model instance for data binding
        bindings: QuerySet of ElementBinding for the custom element
        request: Optional request object

    Returns:
        Safe HTML string of the rendered element tree
    """
    if not element:
        return ""

    # Apply bindings to get modified content
    bound_content = apply_bindings_to_element(element, instance, bindings)

    # Build context for template rendering
    context = {
        "element": element,
        "content": bound_content,
        "request": request,
        "is_custom_element": True,
    }

    # Render children first
    children_html = []
    for child in element.child_elements.filter(is_active=True).order_by("order"):
        child_html = _render_element_tree(child, instance, bindings, request)
        if child_html:
            children_html.append(child_html)

    context["children_html"] = mark_safe("".join(children_html))

    # Render this element using page_builder template
    template_path = f"page_builder/elements/{element.element_type}/template.html"
    try:
        return render_to_string(template_path, context)
    except template.TemplateDoesNotExist:
        # Fallback for unknown element types
        return f"<!-- Unknown element type: {element.element_type} -->"


@register.simple_tag(takes_context=True)
def render_custom_element(context, custom_element, instance):
    """
    Render a custom element with data from a model instance.

    Usage:
        {% load element_builder_tags %}
        {% render_custom_element product_card_element product %}

    Args:
        context: Template context (auto-injected)
        custom_element: CustomElement instance to render
        instance: Model instance to get data from

    Returns:
        Safe HTML string of the rendered element
    """
    if not custom_element or not instance:
        return ""

    if not custom_element.root_element:
        return ""

    request = context.get("request")
    bindings = custom_element.bindings.select_related("element").all()

    return mark_safe(_render_element_tree(custom_element.root_element, instance, bindings, request))


@register.simple_tag(takes_context=True)
def render_custom_element_by_slug(context, slug, instance):
    """
    Render a custom element by its slug.

    Usage:
        {% load element_builder_tags %}
        {% render_custom_element_by_slug "product-search-card" product %}

    Args:
        context: Template context (auto-injected)
        slug: The slug of the CustomElement to render
        instance: Model instance to get data from

    Returns:
        Safe HTML string of the rendered element
    """
    from element_builder.models import CustomElement

    try:
        custom_element = (
            CustomElement.objects.select_related("root_element")
            .prefetch_related("bindings__element", "root_element__child_elements")
            .get(slug=slug, is_active=True)
        )

        return render_custom_element(context, custom_element, instance)
    except CustomElement.DoesNotExist:
        return ""


@register.inclusion_tag("element_builder/element_wrapper.html", takes_context=True)
def render_custom_element_with_wrapper(context, custom_element, instance, css_class=""):
    """
    Render a custom element wrapped in a container div.

    Usage:
        {% load element_builder_tags %}
        {% render_custom_element_with_wrapper product_card product css_class="product-item" %}

    Args:
        context: Template context (auto-injected)
        custom_element: CustomElement instance to render
        instance: Model instance to get data from
        css_class: Additional CSS class for the wrapper

    Returns:
        Rendered template with wrapper
    """
    html = ""
    if custom_element and instance and custom_element.root_element:
        request = context.get("request")
        bindings = custom_element.bindings.select_related("element").all()
        html = _render_element_tree(custom_element.root_element, instance, bindings, request)

    return {
        "element_html": mark_safe(html),
        "css_class": css_class,
        "element": custom_element,
    }
