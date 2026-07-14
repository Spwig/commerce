"""
Email System URL Configuration
"""

from django.urls import path

from email_system import views
from email_system.views import newsletter, template_management, template_preview, wizard

app_name = "email_system"

urlpatterns = [
    # NOTE: Tracking URLs (track/open, track/click) are in tracking_urls.py
    # and included outside i18n_patterns in core/urls.py
    # Newsletter Management
    path("newsletters/", newsletter.newsletter_list, name="newsletter_list"),
    path("newsletters/create/", newsletter.newsletter_create, name="newsletter_create"),
    path(
        "newsletters/<uuid:newsletter_id>/edit/", newsletter.newsletter_edit, name="newsletter_edit"
    ),
    path(
        "newsletters/<uuid:newsletter_id>/send/", newsletter.newsletter_send, name="newsletter_send"
    ),
    path(
        "newsletters/<uuid:newsletter_id>/duplicate/",
        newsletter.newsletter_duplicate,
        name="newsletter_duplicate",
    ),
    path(
        "newsletters/<uuid:newsletter_id>/delete/",
        newsletter.newsletter_delete,
        name="newsletter_delete",
    ),
    # Template Management
    path("templates/", template_management.template_list, name="template_list"),
    path(
        "templates/<uuid:template_id>/edit/",
        template_management.template_edit,
        name="template_edit",
    ),
    path(
        "templates/<uuid:template_id>/clone/",
        template_management.clone_template,
        name="clone_template",
    ),
    path(
        "templates/<uuid:template_id>/delete/",
        template_management.delete_template,
        name="delete_template",
    ),
    path(
        "templates/<uuid:template_id>/restore/",
        template_management.restore_template,
        name="restore_template",
    ),
    path(
        "templates/<uuid:template_id>/toggle-active/",
        template_management.toggle_template_active,
        name="toggle_template_active",
    ),
    path("templates/preview-render/", template_management.preview_render, name="preview_render"),
    # Translation Management
    path("translations/", template_management.translation_manager, name="translation_manager"),
    path(
        "translations/<uuid:template_id>/translate/",
        template_management.translate_template,
        name="translate_template",
    ),
    path(
        "translations/bulk-translate/",
        template_management.bulk_translate_all,
        name="bulk_translate_all",
    ),
    # Template Preview & Testing
    path(
        "templates/<uuid:template_id>/preview/",
        template_preview.template_preview,
        name="template_preview",
    ),
    path(
        "templates/<uuid:template_id>/preview/html/",
        template_preview.template_preview_html,
        name="template_preview_html",
    ),
    path(
        "templates/<uuid:template_id>/send-test/",
        template_preview.send_test_email,
        name="send_test_email",
    ),
    path(
        "templates/<uuid:template_id>/variables/",
        template_preview.template_variables,
        name="template_variables",
    ),
    path(
        "templates/<uuid:template_id>/translations/<str:language_code>/edit/",
        template_preview.edit_translation,
        name="edit_translation",
    ),
    # Provider Setup Wizard
    path("wizard/step1/", wizard.ProviderWizardStep1View.as_view(), name="wizard_step1"),
    path("wizard/step2/", wizard.ProviderWizardStep2View.as_view(), name="wizard_step2"),
    path("wizard/step3/", wizard.ProviderWizardStep3View.as_view(), name="wizard_step3"),
    path("wizard/step4/", wizard.ProviderWizardStep4View.as_view(), name="wizard_step4"),
    path("wizard/step5/", wizard.ProviderWizardStep5View.as_view(), name="wizard_step5"),
    path("wizard/step6/", wizard.ProviderWizardStep6View.as_view(), name="wizard_step6"),
    # Provider Browse & Installation
    path("providers/browse/", views.ProviderBrowseView.as_view(), name="provider_browse"),
    path(
        "providers/install/<slug:provider_slug>/",
        views.install_provider_ajax,
        name="provider_install",
    ),
    path(
        "providers/update/<slug:provider_slug>/", views.update_provider_ajax, name="provider_update"
    ),
    # OAuth flow URLs
    # DEPRECATED: oauth_setup is deprecated in favor of wizard flow
    # Kept for backward compatibility - will be removed in future version
    path("oauth/setup/<str:provider_key>/", views.oauth_setup_form, name="oauth_setup"),
    path("oauth/initiate/<str:provider_key>/", views.oauth_initiate, name="oauth_initiate"),
    path("oauth/callback/<str:provider_key>/", views.oauth_callback, name="oauth_callback"),
    # Connection testing
    path("test-connection/<uuid:account_id>/", views.test_connection, name="test_connection"),
]
