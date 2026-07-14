"""
API URL configuration for Header/Footer Builder
These endpoints are outside i18n_patterns (no language prefix required)
"""

from django.urls import path

from .hf_api_views import (
    ClonePresetAPIView,
    DeleteHeaderAPIView,
    DuplicateHeaderAPIView,
    FooterBuilderAPIView,
    FooterDiscardAPIView,
    FooterPublishAPIView,
    HeaderBuilderAPIView,
    HeaderDiscardAPIView,
    HeaderPublishAPIView,
    MenuListAPIView,
    PresetGalleryAPIView,
    ReorderPlacementsAPIView,
    SetDefaultHeaderAPIView,
    SiteLogoAPIView,
    WidgetLibraryAPIView,
    WidgetPlacementAPIView,
    WidgetPreviewAPIView,
    WidgetSchemasAPIView,
)

app_name = "hf_api"

urlpatterns = [
    # Header/Footer Builder API
    path("header/<int:header_id>/", HeaderBuilderAPIView.as_view(), name="header_builder"),
    path("header/<int:header_id>/publish/", HeaderPublishAPIView.as_view(), name="header_publish"),
    path("header/<int:header_id>/discard/", HeaderDiscardAPIView.as_view(), name="header_discard"),
    path("footer/<int:footer_id>/", FooterBuilderAPIView.as_view(), name="footer_builder"),
    path("footer/<int:footer_id>/publish/", FooterPublishAPIView.as_view(), name="footer_publish"),
    path("footer/<int:footer_id>/discard/", FooterDiscardAPIView.as_view(), name="footer_discard"),
    # Widget placement management
    path("widget-placement/", WidgetPlacementAPIView.as_view(), name="widget_placement_create"),
    path(
        "widget-placement/<int:placement_id>/",
        WidgetPlacementAPIView.as_view(),
        name="widget_placement_update",
    ),
    path(
        "widget-placement/reorder/", ReorderPlacementsAPIView.as_view(), name="reorder_placements"
    ),
    # Widget resources
    path("widget-library/", WidgetLibraryAPIView.as_view(), name="widget_library"),
    path("widget-schemas/", WidgetSchemasAPIView.as_view(), name="widget_schemas"),
    path("widget-preview/", WidgetPreviewAPIView.as_view(), name="widget_preview"),
    # Menu list for widget configuration
    path("menus/", MenuListAPIView.as_view(), name="menu_list"),
    # Site logo for logo widget
    path("site-logo/", SiteLogoAPIView.as_view(), name="site_logo"),
    # Preset gallery
    path("presets/<str:template_type>/", PresetGalleryAPIView.as_view(), name="preset_gallery"),
    path(
        "presets/<str:template_type>/<int:preset_id>/clone/",
        ClonePresetAPIView.as_view(),
        name="clone_preset",
    ),
    # Header management
    path(
        "header/<int:header_id>/duplicate/",
        DuplicateHeaderAPIView.as_view(),
        name="duplicate_header",
    ),
    path("header/<int:header_id>/delete/", DeleteHeaderAPIView.as_view(), name="delete_header"),
    path(
        "header/<int:header_id>/set-default/",
        SetDefaultHeaderAPIView.as_view(),
        name="set_default_header",
    ),
]
