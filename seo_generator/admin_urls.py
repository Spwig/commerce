"""
SEO Generator URL Configuration
URL patterns for SEO generator admin views (dashboard, browse, wizard).
"""

from django.urls import path

from seo_generator.views import (
    ProviderBrowseView,
    ProviderWizardStep1View,
    ProviderWizardStep2View,
    ProviderWizardStep3View,
    ProviderWizardStep4View,
    install_provider_ajax,
    seo_coverage_api,
    seo_coverage_refresh_api,
    seo_dashboard_view,
    seo_items_api,
    seo_missing_items_api,
    update_provider_ajax,
)

app_name = "seo_generator"

urlpatterns = [
    # Dashboard
    path("dashboard/", seo_dashboard_view, name="seo_dashboard"),
    # Dashboard API
    path("api/coverage/", seo_coverage_api, name="seo_coverage_api"),
    path("api/coverage/refresh/", seo_coverage_refresh_api, name="seo_coverage_refresh"),
    path("api/missing-items/", seo_missing_items_api, name="seo_missing_items"),
    path("api/items/<str:content_type>/", seo_items_api, name="seo_items"),
    # Provider Browse & Installation
    path("providers/browse/", ProviderBrowseView.as_view(), name="provider_browse"),
    path("providers/install/<slug:provider_slug>/", install_provider_ajax, name="provider_install"),
    path("providers/update/<slug:provider_slug>/", update_provider_ajax, name="provider_update"),
    # Provider Connection Wizard
    path("wizard/step1/", ProviderWizardStep1View.as_view(), name="wizard_step1"),
    path("wizard/step2/", ProviderWizardStep2View.as_view(), name="wizard_step2"),
    path("wizard/step3/", ProviderWizardStep3View.as_view(), name="wizard_step3"),
    path("wizard/step4/", ProviderWizardStep4View.as_view(), name="wizard_step4"),
]
