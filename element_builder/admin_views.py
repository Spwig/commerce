"""
Element Builder Admin Views

Provides AJAX filter endpoint and visual builder view.
"""

import json

from django.apps import apps
from django.contrib.admin.views.decorators import staff_member_required
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.functional import Promise
from django.utils.translation import gettext_lazy as _


class LazyEncoder(DjangoJSONEncoder):
    """JSON encoder that handles Django's lazy translation strings."""

    def default(self, obj):
        if isinstance(obj, Promise):
            return force_str(obj)
        return super().default(obj)


from component_updates.utility_registry import get_utility_assets

from .models import CustomElement
from .registry import BINDABLE_MODELS


@staff_member_required
def quick_add_view(request):
    """
    Instantly creates a draft element and redirects to the visual builder.
    No form needed - the admin can modify all details in the builder.
    """
    # Use first available model as default
    default_model = list(BINDABLE_MODELS.keys())[0]

    # Generate unique name and slug
    base_name = "Untitled Element"
    base_slug = "untitled-element"

    # Find next available number
    counter = 1
    slug = base_slug
    name = base_name
    while CustomElement.objects.filter(slug=slug).exists():
        counter += 1
        slug = f"{base_slug}-{counter}"
        name = f"{base_name} {counter}"

    # Create draft element
    element = CustomElement.objects.create(
        name=name,
        slug=slug,
        target_model=default_model,
        description="",
        icon="fas fa-puzzle-piece",
        category="custom",
        is_active=False,  # Draft - inactive until published
    )

    # Redirect directly to builder
    return HttpResponseRedirect(
        reverse("admin:element_builder_customelement_builder", args=[element.pk])
    )


@staff_member_required
def filter_elements(request):
    """
    AJAX endpoint for filtering custom elements.
    Returns rendered HTML partial with matching elements.
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    search = request.GET.get("search", "").strip()
    target_model = request.GET.get("model", "").strip()
    status = request.GET.get("status", "").strip()

    queryset = CustomElement.objects.all()

    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) | Q(description__icontains=search) | Q(slug__icontains=search)
        )

    if target_model:
        queryset = queryset.filter(target_model=target_model)

    if status == "active":
        queryset = queryset.filter(is_active=True)
    elif status == "inactive":
        queryset = queryset.filter(is_active=False)

    queryset = queryset.order_by("name")

    html = render_to_string(
        "admin/element_builder/partials/element_cards.html",
        {
            "elements": queryset,
            "request": request,
            "bindable_models": BINDABLE_MODELS,
        },
    )

    return JsonResponse(
        {
            "html": html,
            "count": queryset.count(),
        }
    )


@staff_member_required
def visual_builder_view(request, pk):
    """
    Visual builder view for editing custom element structure.
    Uses a 3-column layout with element library, canvas, and properties panel.
    Element library is loaded via API (see ElementPrimitivesAPI).
    """
    element = get_object_or_404(CustomElement, pk=pk)

    # Get model configuration
    model_config = BINDABLE_MODELS.get(element.target_model, {})
    model_fields = model_config.get("fields", {})

    # Get thumbnail presets if available
    try:
        from media_library.models import ImageSizePreset

        thumbnail_presets = list(
            ImageSizePreset.objects.filter(is_active=True).values("slug", "name", "width", "height")
        )
    except Exception:
        thumbnail_presets = [
            {"slug": "small", "name": "Small", "width": 150, "height": 150},
            {"slug": "medium", "name": "Medium", "width": 300, "height": 300},
            {"slug": "large", "name": "Large", "width": 600, "height": 600},
        ]

    # Get utility assets (CSS and JS files) using auto-discovery
    utility_assets = get_utility_assets()

    # Build complete bindable models data for JavaScript (for model selector)
    all_models_data = {
        "": {  # "None" option for static elements
            "label": str(_("None (Static Element)")),
            "icon": "fas fa-cube",
            "fields": {},
        }
    }
    for model_key, model_cfg in BINDABLE_MODELS.items():
        all_models_data[model_key] = {
            "label": str(model_cfg["label"]),
            "icon": model_cfg.get("icon", "fas fa-database"),
            "fields": {
                field_name: {
                    "type": field_cfg.get("type", "text"),
                    "label": str(field_cfg.get("label", field_name)),
                }
                for field_name, field_cfg in model_cfg.get("fields", {}).items()
            },
        }

    # Serialize element tree for JavaScript
    from .serializers import ElementBindingSerializer, ElementTreeSerializer

    element_tree_data = None
    if element.root_element:
        element_tree_data = ElementTreeSerializer(
            element.root_element, context={"custom_element": element}
        ).data

    bindings_data = ElementBindingSerializer(
        element.bindings.select_related("element").all(), many=True
    ).data

    context = {
        "element": element,
        "bindable_models": BINDABLE_MODELS,
        "model_config": model_config,
        "model_fields_json": json.dumps(model_fields, cls=LazyEncoder),
        "all_bindable_models_json": json.dumps(all_models_data, cls=LazyEncoder),
        "element_tree_json": json.dumps(element_tree_data, cls=LazyEncoder),
        "bindings_json": json.dumps(bindings_data, cls=LazyEncoder),
        "thumbnail_presets": json.dumps(thumbnail_presets, cls=LazyEncoder),
        "utility_css_files": utility_assets.get("css", []),
        "utility_js_files": utility_assets.get("js", []),
        "title": _("Element Builder: %(name)s") % {"name": element.name},
        "opts": CustomElement._meta,
        "has_change_permission": True,
    }

    return render(request, "admin/element_builder/visual_builder.html", context)


@staff_member_required
def search_model_items(request):
    """
    AJAX endpoint to search items from a bindable model.
    Returns list of items with id and label for preview selection.
    """
    model_key = request.GET.get("model", "")
    search = request.GET.get("q", "").strip()

    if not model_key or model_key not in BINDABLE_MODELS:
        return JsonResponse({"items": []})

    try:
        # Get the model class
        app_label, model_name = model_key.split(".")
        model_class = apps.get_model(app_label, model_name)

        # Build queryset
        queryset = model_class.objects.all()

        # Search by common name fields (name or title)
        if search:
            # Try filtering by name first, fallback to title
            if hasattr(model_class, "name"):
                queryset = queryset.filter(name__icontains=search)
            elif hasattr(model_class, "title"):
                queryset = queryset.filter(title__icontains=search)

        # Limit results
        queryset = queryset[:20]

        items = [{"id": item.pk, "label": str(item)} for item in queryset]
        return JsonResponse({"items": items})

    except Exception as e:
        return JsonResponse({"items": [], "error": str(e)})
