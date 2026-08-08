"""
Payout Provider Admin URLs

Admin-facing views: browse, wizard, install/update.
These are included inside i18n_patterns for language prefix support.

Webhook URLs are in webhook_urls.py (outside i18n_patterns).
"""

from django.contrib.auth.decorators import permission_required
from django.urls import path

from .views.provider_browse import (
    ProviderBrowseView,
    install_provider_ajax,
    update_provider_ajax,
)
from .views.wizard import (
    ProviderWizardStep1View,
    ProviderWizardStep2View,
    ProviderWizardStep3View,
    ProviderWizardStep4View,
)

app_name = "payout_providers"


def require_perm(perm, view):
    """Gate a staff view behind a specific model permission (403 if missing).

    These endpoints mutate installed provider code or create live payout
    accounts, so staff access alone is not sufficient — the caller must also
    hold the relevant add/change permission.
    """
    return permission_required(perm, raise_exception=True)(view)


urlpatterns = [
    # Provider browse and marketplace
    path("providers/browse/", ProviderBrowseView.as_view(), name="provider_browse"),
    path(
        "providers/install/<slug:provider_slug>/",
        require_perm("component_updates.add_componentregistry", install_provider_ajax),
        name="install_provider",
    ),
    path(
        "providers/update/<slug:provider_slug>/",
        require_perm("component_updates.change_componentregistry", update_provider_ajax),
        name="update_provider",
    ),
    # Provider connection wizard
    path("wizard/", ProviderWizardStep1View.as_view(), name="wizard_step1"),
    path("wizard/setup/", ProviderWizardStep2View.as_view(), name="wizard_step2"),
    path(
        "wizard/credentials/",
        require_perm(
            "payout_providers.add_payoutprovideraccount",
            ProviderWizardStep3View.as_view(),
        ),
        name="wizard_step3",
    ),
    path(
        "wizard/test/",
        require_perm(
            "payout_providers.add_payoutprovideraccount",
            ProviderWizardStep4View.as_view(),
        ),
        name="wizard_step4",
    ),
]
