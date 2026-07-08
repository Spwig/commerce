"""
Exchange Rates URL Configuration
URL patterns for exchange rates app views
"""
from django.urls import path
from exchange_rates.views import (
    # Admin AJAX views
    toggle_provider_active,
    set_provider_primary,
    sync_provider_rates,
    delete_provider,
    provider_bulk_action,
    toggle_manual_rate_active,
    toggle_manual_rate_locked,
    sync_from_provider,
    # Wizard views
    ProviderWizardStep1View,
    ProviderWizardStep2View,
    ProviderWizardStep3View,
    ProviderWizardStep4View,
    # Browse views
    ProviderBrowseView,
    install_provider_ajax,
    update_provider_ajax,
)

app_name = 'exchange_rates'

urlpatterns = [
    # Provider Browse & Installation
    path('providers/browse/', ProviderBrowseView.as_view(), name='provider_browse'),
    path('providers/install/<slug:provider_slug>/', install_provider_ajax, name='provider_install'),
    path('providers/update/<slug:provider_slug>/', update_provider_ajax, name='provider_update'),

    # Provider Connection Wizard
    path('wizard/step1/', ProviderWizardStep1View.as_view(), name='wizard_step1'),
    path('wizard/step2/', ProviderWizardStep2View.as_view(), name='wizard_step2'),
    path('wizard/step3/', ProviderWizardStep3View.as_view(), name='wizard_step3'),
    path('wizard/step4/', ProviderWizardStep4View.as_view(), name='wizard_step4'),

    # Provider Account Admin AJAX Endpoints
    path('admin/provideraccount/<int:provider_id>/toggle-active/', toggle_provider_active, name='provider_toggle_active'),
    path('admin/provideraccount/<int:provider_id>/set-primary/', set_provider_primary, name='provider_set_primary'),
    path('admin/provideraccount/<int:provider_id>/sync-rates/', sync_provider_rates, name='provider_sync_rates'),
    path('admin/provideraccount/<int:provider_id>/delete/', delete_provider, name='provider_delete'),
    path('admin/provideraccount/bulk-action/', provider_bulk_action, name='provider_bulk_action'),

    # Manual Exchange Rate Admin AJAX Endpoints
    path('admin/manual-rate/<int:rate_id>/toggle-active/', toggle_manual_rate_active, name='manual_rate_toggle_active'),
    path('admin/manual-rate/<int:rate_id>/toggle-locked/', toggle_manual_rate_locked, name='manual_rate_toggle_locked'),
    path('admin/manual-rate/sync-from-provider/', sync_from_provider, name='manual_rate_sync_from_provider'),
]
