"""
Shipping URL Configuration
URL patterns for shipping app views
"""

from django.urls import path

from shipping.views import (
    ProviderBrowseView,
    ProviderWizardStep1View,
    ProviderWizardStep2View,
    ProviderWizardStep3View,
    ProviderWizardStep4View,
    ProviderWizardStep5View,
    RuleWizardStep1View,
    RuleWizardStep2View,
    RuleWizardStep3View,
    RuleWizardStep4View,
    RuleWizardStep5View,
    ZoneWizardStep1View,
    ZoneWizardStep2View,
    ZoneWizardStep3View,
    get_states_for_countries,
    install_provider_ajax,
    update_provider_ajax,
    validate_country_code,
    validate_postal_pattern,
)
from shipping.views.admin_views import (
    bulk_action,
    delete_carrier,
    delete_provider,
    provider_bulk_action,
    rule_bulk_action,
    set_carrier_default,
    set_provider_default,
    test_provider_connection,
    toggle_carrier_active,
    toggle_provider_active,
    zone_bulk_action,
)
from shipping.webhooks import (
    provider_webhook,
    webhook_documentation,
    webhook_health_check,
)

app_name = "shipping"

urlpatterns = [
    # Provider Browse & Installation
    path("providers/browse/", ProviderBrowseView.as_view(), name="provider_browse"),
    path("providers/install/<slug:provider_slug>/", install_provider_ajax, name="provider_install"),
    path("providers/update/<slug:provider_slug>/", update_provider_ajax, name="provider_update"),
    # Provider Connection Wizard
    path("wizard/step1/", ProviderWizardStep1View.as_view(), name="wizard_step1"),
    path("wizard/step2/", ProviderWizardStep2View.as_view(), name="wizard_step2"),
    path("wizard/step3/", ProviderWizardStep3View.as_view(), name="wizard_step3"),
    path("wizard/step4/", ProviderWizardStep4View.as_view(), name="wizard_step4"),
    path("wizard/step5/", ProviderWizardStep5View.as_view(), name="wizard_step5"),
    # Carrier Admin AJAX Endpoints
    path(
        "admin/carrierpreset/<uuid:carrier_id>/toggle-active/",
        toggle_carrier_active,
        name="carrier_toggle_active",
    ),
    path(
        "admin/carrierpreset/<uuid:carrier_id>/set-default/",
        set_carrier_default,
        name="carrier_set_default",
    ),
    path("admin/carrierpreset/<uuid:carrier_id>/delete/", delete_carrier, name="carrier_delete"),
    path("admin/carrierpreset/bulk-action/", bulk_action, name="carrier_bulk_action"),
    # Provider Account Admin AJAX Endpoints
    path(
        "admin/provideraccount/<uuid:provider_id>/toggle-active/",
        toggle_provider_active,
        name="provider_toggle_active",
    ),
    path(
        "admin/provideraccount/<uuid:provider_id>/set-default/",
        set_provider_default,
        name="provider_set_default",
    ),
    path(
        "admin/provideraccount/<uuid:provider_id>/test-connection/",
        test_provider_connection,
        name="provider_test_connection",
    ),
    path(
        "admin/provideraccount/<uuid:provider_id>/delete/", delete_provider, name="provider_delete"
    ),
    path("admin/provideraccount/bulk-action/", provider_bulk_action, name="provider_bulk_action"),
    # Shipping Zone Admin AJAX Endpoints
    path("admin/shippingzone/bulk-action/", zone_bulk_action, name="zone_bulk_action"),
    # Shipping Promotion Admin AJAX Endpoints
    path("admin/shippingpromotion/bulk-action/", rule_bulk_action, name="rule_bulk_action"),
    # Webhook Endpoints
    path("webhooks/", webhook_documentation, name="webhook_docs"),
    path("webhooks/health/", webhook_health_check, name="webhook_health"),
    path("webhooks/<str:provider_key>/", provider_webhook, name="provider_webhook"),
    # Zone Configuration Wizard
    path("zone-wizard/step1/", ZoneWizardStep1View.as_view(), name="zone_wizard_step1"),
    path("zone-wizard/step2/", ZoneWizardStep2View.as_view(), name="zone_wizard_step2"),
    path("zone-wizard/step3/", ZoneWizardStep3View.as_view(), name="zone_wizard_step3"),
    path("zone-wizard/validate-country/", validate_country_code, name="validate_country_code"),
    path("zone-wizard/validate-postal/", validate_postal_pattern, name="validate_postal_pattern"),
    path("zone-wizard/get-states/", get_states_for_countries, name="get_states_for_countries"),
    # Promotion Configuration Wizard
    path("promotion-wizard/step1/", RuleWizardStep1View.as_view(), name="promotion_wizard_step1"),
    path("promotion-wizard/step2/", RuleWizardStep2View.as_view(), name="promotion_wizard_step2"),
    path("promotion-wizard/step3/", RuleWizardStep3View.as_view(), name="promotion_wizard_step3"),
    path("promotion-wizard/step4/", RuleWizardStep4View.as_view(), name="promotion_wizard_step4"),
    path("promotion-wizard/step5/", RuleWizardStep5View.as_view(), name="promotion_wizard_step5"),
]
