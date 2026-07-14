"""
Element Builder API URLs

These URLs are included outside i18n_patterns under /api/element-builder/.
"""

from django.urls import path

from . import api_views

app_name = "element_builder_api"

urlpatterns = [
    # Custom element CRUD
    path("custom-elements/", api_views.CustomElementListAPI.as_view(), name="list"),
    path("custom-elements/<int:pk>/", api_views.CustomElementDetailAPI.as_view(), name="detail"),
    # Element tree management
    path(
        "custom-elements/<int:pk>/elements/",
        api_views.ElementTreeAddAPI.as_view(),
        name="element_add",
    ),
    # Element preview
    path(
        "custom-elements/<int:pk>/preview/",
        api_views.ElementPreviewAPI.as_view(),
        name="element_preview",
    ),
    path(
        "custom-elements/<int:pk>/preview/<int:element_id>/",
        api_views.ElementPreviewAPI.as_view(),
        name="element_preview_single",
    ),
    path(
        "custom-elements/<int:pk>/elements/<int:element_id>/",
        api_views.ElementTreeUpdateAPI.as_view(),
        name="element_update",
    ),
    path(
        "custom-elements/<int:pk>/elements/<int:element_id>/delete/",
        api_views.ElementTreeDeleteAPI.as_view(),
        name="element_delete",
    ),
    # Container layout
    path(
        "custom-elements/<int:pk>/elements/<int:element_id>/layout/",
        api_views.ContainerLayoutAPI.as_view(),
        name="container_layout",
    ),
    # Element move/reorder
    path(
        "custom-elements/<int:pk>/elements/<int:element_id>/move/",
        api_views.ElementMoveAPI.as_view(),
        name="element_move",
    ),
    # Element bindings
    path(
        "custom-elements/<int:pk>/bindings/", api_views.ElementBindingAPI.as_view(), name="bindings"
    ),
    path(
        "custom-elements/<int:pk>/bindings/clear/",
        api_views.ElementBindingClearAPI.as_view(),
        name="bindings_clear",
    ),
    # Reference data
    path("primitives/", api_views.ElementPrimitivesAPI.as_view(), name="primitives"),
    path(
        "element-config/<str:element_type>/",
        api_views.ElementConfigAPI.as_view(),
        name="element_config",
    ),
    path("bindable-models/", api_views.BindableModelsAPI.as_view(), name="bindable_models"),
    path("thumbnail-presets/", api_views.ThumbnailPresetsAPI.as_view(), name="thumbnail_presets"),
]
