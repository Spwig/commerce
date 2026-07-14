from django.urls import path

from . import admin_views, views
from .views import payment_dashboard, provider_browse, wizard

app_name = "payment_providers"

urlpatterns = [
    # Payment Dashboard
    path("dashboard/", payment_dashboard.payment_dashboard_view, name="payment_dashboard"),
    path("dashboard/api/", payment_dashboard.payment_dashboard_api, name="payment_dashboard_api"),
    # Provider Browse
    path("providers/browse/", provider_browse.ProviderBrowseView.as_view(), name="provider_browse"),
    path(
        "providers/install/<str:provider_slug>/",
        provider_browse.install_provider_ajax,
        name="install_provider",
    ),
    path(
        "providers/update/<str:provider_slug>/",
        provider_browse.update_provider_ajax,
        name="update_provider",
    ),
    # Provider Setup Wizard
    path("wizard/step1/", wizard.ProviderWizardStep1View.as_view(), name="wizard_step1"),
    path("wizard/step2/", wizard.ProviderWizardStep2View.as_view(), name="wizard_step2"),
    path("wizard/step3/", wizard.ProviderWizardStep3View.as_view(), name="wizard_step3"),
    path("wizard/step4/", wizard.ProviderWizardStep4View.as_view(), name="wizard_step4"),
    path("wizard/step5/", wizard.ProviderWizardStep5View.as_view(), name="wizard_step5"),
    # Webhook endpoints for payment providers
    path("webhook/<str:provider_slug>/", views.webhook_handler, name="webhook"),
    # AJAX filter endpoints for admin change lists
    path("transactions/filter/", admin_views.filter_transactions, name="transactions_filter"),
    path("webhooks/filter/", admin_views.filter_webhooks, name="webhooks_filter"),
    # API endpoints for provider configuration testing
    path(
        "api/test-connection/<uuid:account_id>/",
        views.test_provider_connection,
        name="test_connection",
    ),
    path("api/provider-info/<str:provider_key>/", views.provider_info, name="provider_info"),
]
