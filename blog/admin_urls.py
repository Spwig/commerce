"""
Admin URL configuration for blog app.

These URLs are for the installation wizard, admin AJAX endpoints, and list filtering.
"""

from django.urls import path

from blog import admin_views
from blog.views import wizard

app_name = "blog_admin"

urlpatterns = [
    # Admin List Filtering Endpoints
    path("blogcategory/filter/", admin_views.filter_blog_categories, name="filter_blog_categories"),
    path("blogtag/filter/", admin_views.filter_blog_tags, name="filter_blog_tags"),
    path(
        "blogsubscriber/filter/",
        admin_views.filter_blog_subscribers,
        name="filter_blog_subscribers",
    ),
    # Social Connectors - Installation Wizard
    path(
        "social-connectors/providers/browse/",
        wizard.ProviderBrowseView.as_view(),
        name="provider_browse",
    ),
    path("social-connectors/wizard/step1/", wizard.WizardStep1View.as_view(), name="wizard_step1"),
    path("social-connectors/wizard/step2/", wizard.WizardStep2View.as_view(), name="wizard_step2"),
    path("social-connectors/wizard/step3/", wizard.WizardStep3View.as_view(), name="wizard_step3"),
    path("social-connectors/wizard/step4/", wizard.WizardStep4View.as_view(), name="wizard_step4"),
    # OAuth callback
    path(
        "social-connectors/oauth/callback/",
        wizard.OAuthCallbackView.as_view(),
        name="oauth_callback",
    ),
    # Account selection (after OAuth) - unified view that loads provider's template
    path(
        "social-connectors/wizard/select-account/",
        wizard.WizardSelectAccountView.as_view(),
        name="wizard_select_account",
    ),
    # Legacy routes for backward compatibility
    path(
        "social-connectors/wizard/select-page/",
        wizard.WizardSelectPageView.as_view(),
        name="wizard_select_page",
    ),
    path(
        "social-connectors/wizard/select-organization/",
        wizard.WizardSelectOrganizationView.as_view(),
        name="wizard_select_organization",
    ),
    # Provider Install/Update endpoints
    path(
        "social-connectors/providers/install/<slug:provider_slug>/",
        wizard.install_provider_ajax,
        name="install_provider",
    ),
    path(
        "social-connectors/providers/update/<slug:provider_slug>/",
        wizard.update_provider_ajax,
        name="update_provider",
    ),
    # Admin AJAX endpoints for social connectors
    path(
        "social-connectors/admin/<uuid:account_id>/test/",
        wizard.test_connection_ajax,
        name="test_connection",
    ),
    path(
        "social-connectors/admin/<uuid:account_id>/delete/",
        wizard.delete_account_ajax,
        name="delete_account",
    ),
]
