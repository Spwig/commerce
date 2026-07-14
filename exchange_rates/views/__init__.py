"""
Exchange Rates Views Package
"""

from .admin_views import (
    delete_provider,
    filter_exchange_rate_providers,
    provider_bulk_action,
    set_provider_primary,
    sync_from_provider,
    sync_provider_rates,
    toggle_manual_rate_active,
    toggle_manual_rate_locked,
    toggle_provider_active,
)
from .provider_browse import (
    ProviderBrowseView,
    install_provider_ajax,
    update_provider_ajax,
)
from .wizard import (
    ProviderWizardStep1View,
    ProviderWizardStep2View,
    ProviderWizardStep3View,
    ProviderWizardStep4View,
)

__all__ = [
    "filter_exchange_rate_providers",
    "toggle_provider_active",
    "set_provider_primary",
    "sync_provider_rates",
    "delete_provider",
    "provider_bulk_action",
    "toggle_manual_rate_active",
    "toggle_manual_rate_locked",
    "sync_from_provider",
    "ProviderWizardStep1View",
    "ProviderWizardStep2View",
    "ProviderWizardStep3View",
    "ProviderWizardStep4View",
    "ProviderBrowseView",
    "install_provider_ajax",
    "update_provider_ajax",
]
