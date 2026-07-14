"""
URL configuration for theme system
"""

from django.urls import path

from .branding_builder_view import (
    BrandingBuilderView,
    BrandingExportView,
    BrandingImportView,
    BrandingPreviewFrameView,
    BrandingSaveView,
    BrandingUpdateView,
)
from .dashboard_view import (
    ClearThemeCacheView,
    DesignDashboardView,
    RegenerateCSSView,
    ToggleForceLightModeView,
)
from .header_footer_views import (
    BrandingPreviewView,
    MenuBuilderView,
    PreviewFooterView,
    PreviewHeaderView,
    WidgetConfigView,
)

# NOTE: hf_api_views imports moved to design/hf_api_urls.py
# API endpoints are now at /api/hf-builder/... (outside i18n_patterns)
from .hf_builder_views import (
    FooterBuilderView,
    HeaderBuilderView,
)
from .template_config_views import (
    template_config_save,
    template_config_view,
)
from .theme_package_view import (
    package_theme_ajax,
    theme_package_view,
    validate_theme_ajax,
)
from .unified_theme_views import (
    activate_theme_ajax,
    check_theme_updates_ajax,
    get_theme_detail_ajax,
    install_theme_ajax,
    rollback_theme_ajax,
    unified_theme_management_view,
    uninstall_theme_ajax,
)
from .views import (
    AdoptThemePaletteView,
    BrandCSSView,
    LayeredCSSView,
    ThemeCSSView,
    ThemePreviewView,
    ThemeTokenDiffView,
)

app_name = "design"

urlpatterns = [
    # Dashboard
    path("dashboard/", DesignDashboardView.as_view(), name="dashboard"),
    path("dashboard/regenerate-css/", RegenerateCSSView.as_view(), name="regenerate_css"),
    path("dashboard/clear-cache/", ClearThemeCacheView.as_view(), name="clear_theme_cache"),
    path(
        "dashboard/toggle-force-light-mode/",
        ToggleForceLightModeView.as_view(),
        name="toggle_force_light_mode",
    ),
    # CSS generation endpoints
    path("css/brand.css", BrandCSSView.as_view(), name="brand_css"),
    path("css/layered.css", LayeredCSSView.as_view(), name="layered_css"),
    path("css/theme/<slug:slug>.css", ThemeCSSView.as_view(), name="theme_css"),
    # Unified Theme Management (New)
    path("themes/unified/", unified_theme_management_view, name="unified_theme_management"),
    path("themes/activate/<slug:slug>/", activate_theme_ajax, name="activate_theme"),
    path("themes/rollback/<slug:slug>/", rollback_theme_ajax, name="rollback_theme"),
    path("themes/install/<slug:slug>/", install_theme_ajax, name="install_theme"),
    path("themes/uninstall/<slug:slug>/", uninstall_theme_ajax, name="uninstall_theme"),
    path("themes/check-updates/", check_theme_updates_ajax, name="check_theme_updates"),
    path("themes/<slug:slug>/detail/", get_theme_detail_ajax, name="get_theme_detail"),
    # Theme Packaging
    path("themes/packager/", theme_package_view, name="theme_package"),
    path("themes/validate/", validate_theme_ajax, name="validate_theme"),
    path("themes/create-package/", package_theme_ajax, name="package_theme_ajax"),
    # Legacy Theme management
    path("theme/<int:theme_id>/preview/", ThemePreviewView.as_view(), name="theme_preview"),
    path("theme/<int:theme_id>/diff/", ThemeTokenDiffView.as_view(), name="theme_token_diff"),
    path(
        "theme/<int:theme_id>/adopt/", AdoptThemePaletteView.as_view(), name="adopt_theme_palette"
    ),
    # Header/Footer preview
    path("header/<int:header_id>/preview/", PreviewHeaderView.as_view(), name="preview_header"),
    path("footer/<int:footer_id>/preview/", PreviewFooterView.as_view(), name="preview_footer"),
    # Header/Footer visual builders
    path("header/builder/", HeaderBuilderView.as_view(), name="header_builder_default"),
    path("header/<int:header_id>/builder/", HeaderBuilderView.as_view(), name="header_builder"),
    path("footer/builder/", FooterBuilderView.as_view(), name="footer_builder_default"),
    path("footer/<int:footer_id>/builder/", FooterBuilderView.as_view(), name="footer_builder"),
    # Menu builder
    path("menu/builder/", MenuBuilderView.as_view(), name="menu_builder_default"),
    path("menu/<int:menu_id>/builder/", MenuBuilderView.as_view(), name="menu_builder"),
    # Branding Builder
    path(
        "branding/<int:branding_id>/builder/",
        BrandingBuilderView.as_view(),
        name="branding_builder",
    ),
    path(
        "branding/<int:branding_id>/preview-frame/",
        BrandingPreviewFrameView.as_view(),
        name="branding_preview_frame",
    ),
    path(
        "branding/<int:branding_id>/update/", BrandingUpdateView.as_view(), name="branding_update"
    ),
    path("branding/<int:branding_id>/save/", BrandingSaveView.as_view(), name="branding_save"),
    path(
        "branding/<int:branding_id>/export/", BrandingExportView.as_view(), name="branding_export"
    ),
    path(
        "branding/<int:branding_id>/import/", BrandingImportView.as_view(), name="branding_import"
    ),
    # Old branding preview (kept for compatibility)
    path("branding/preview/", BrandingPreviewView.as_view(), name="branding_preview"),
    # Widget configuration
    path("widget/<int:widget_id>/config/", WidgetConfigView.as_view(), name="widget_config"),
    # Page Template Configuration
    path("template-config/", template_config_view, name="template_config"),
    path("template-config/save/", template_config_save, name="template_config_save"),
    # NOTE: Header/Footer Builder API routes moved to design/hf_api_urls.py
    # They are now available at /api/hf-builder/... (outside i18n_patterns)
]
