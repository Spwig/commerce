"""
URL configuration for product_feeds app.

Admin URLs are handled by Django admin autodiscovery.
These URLs are for the installation wizard and API endpoints.
"""

from django.urls import path

from product_feeds.views import wizard
from product_feeds.views.dashboard import product_feeds_dashboard

app_name = "product_feeds"

urlpatterns = [
    # Dashboard
    path("dashboard/", product_feeds_dashboard, name="dashboard"),
    # Installation Wizard
    path("providers/browse/", wizard.ProviderBrowseView.as_view(), name="provider_browse"),
    path("wizard/step1/", wizard.WizardStep1View.as_view(), name="wizard_step1"),
    path("wizard/step2/", wizard.WizardStep2View.as_view(), name="wizard_step2"),
    path("wizard/step3/", wizard.WizardStep3View.as_view(), name="wizard_step3"),
    path("wizard/step4/", wizard.WizardStep4View.as_view(), name="wizard_step4"),
    # Provider Install/Update endpoints
    path(
        "providers/install/<slug:provider_slug>/",
        wizard.install_provider_ajax,
        name="install_provider",
    ),
    path(
        "providers/update/<slug:provider_slug>/",
        wizard.update_provider_ajax,
        name="update_provider",
    ),
    # Admin AJAX endpoints
    path("admin/<int:account_id>/sync/", wizard.sync_feed_ajax, name="sync_feed"),
    path("admin/<int:account_id>/download/", wizard.download_feed, name="download_feed"),
    path("admin/<int:account_id>/test/", wizard.test_connection_ajax, name="test_connection"),
    path("admin/<int:account_id>/toggle/", wizard.toggle_account_ajax, name="toggle_account"),
    path("admin/<int:account_id>/set-primary/", wizard.set_primary_ajax, name="set_primary"),
    path("admin/<int:account_id>/delete/", wizard.delete_account_ajax, name="delete_account"),
    path("admin/bulk-action/", wizard.bulk_action_ajax, name="bulk_action"),
    path("admin/sync-logs/filter/", wizard.filter_sync_logs, name="filter_sync_logs"),
]
