"""
Payout Provider Admin URLs

Admin-facing views: browse, wizard, install/update.
These are included inside i18n_patterns for language prefix support.

Webhook URLs are in webhook_urls.py (outside i18n_patterns).
"""

from django.urls import path
from .views.wizard import (
    ProviderWizardStep1View,
    ProviderWizardStep2View,
    ProviderWizardStep3View,
    ProviderWizardStep4View,
)
from .views.provider_browse import (
    ProviderBrowseView,
    install_provider_ajax,
    update_provider_ajax,
)

app_name = 'payout_providers'

urlpatterns = [
    # Provider browse and marketplace
    path('providers/browse/', ProviderBrowseView.as_view(), name='provider_browse'),
    path('providers/install/<slug:provider_slug>/', install_provider_ajax, name='install_provider'),
    path('providers/update/<slug:provider_slug>/', update_provider_ajax, name='update_provider'),

    # Provider connection wizard
    path('wizard/', ProviderWizardStep1View.as_view(), name='wizard_step1'),
    path('wizard/setup/', ProviderWizardStep2View.as_view(), name='wizard_step2'),
    path('wizard/credentials/', ProviderWizardStep3View.as_view(), name='wizard_step3'),
    path('wizard/test/', ProviderWizardStep4View.as_view(), name='wizard_step4'),
]
