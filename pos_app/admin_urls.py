from django.urls import path

from . import admin_views
from .dashboard_views import (
    activate_license,
    enable_store_location,
    filter_promo_slides,
    filter_receipt_templates,
    filter_shifts,
    filter_terminal_providers,
    filter_terminal_readers,
    filter_terminals,
    pos_dashboard,
    quick_assign_reader,
    refresh_reader_status,
    sync_readers,
    unlock_terminal,
)
from .wizard_views import (
    ReaderWizardStep1View,
    ReaderWizardStep2View,
    ReaderWizardStep3View,
    TerminalWizardStep1View,
    TerminalWizardStep2View,
    TerminalWizardStep3View,
    TerminalWizardStep4View,
    TerminalWizardStep5View,
)

app_name = "pos_admin"

urlpatterns = [
    path("", pos_dashboard, name="dashboard"),
    path("terminals/filter/", filter_terminals, name="terminal_filter"),
    path("shifts/filter/", filter_shifts, name="shift_filter"),
    path("store-location/enable/", enable_store_location, name="enable_store_location"),
    path("promoslide/filter/", filter_promo_slides, name="promoslide_filter"),
    path("receipttemplate/filter/", filter_receipt_templates, name="receipttemplate_filter"),
    path("storegroup/filter/", admin_views.filter_store_groups, name="storegroup_filter"),
    path("terminal-providers/filter/", filter_terminal_providers, name="terminal_provider_filter"),
    path("terminal-readers/filter/", filter_terminal_readers, name="terminal_reader_filter"),
    # Terminal Provider Wizard
    path("terminal-provider/wizard/step1/", TerminalWizardStep1View.as_view(), name="wizard_step1"),
    path("terminal-provider/wizard/step2/", TerminalWizardStep2View.as_view(), name="wizard_step2"),
    path("terminal-provider/wizard/step3/", TerminalWizardStep3View.as_view(), name="wizard_step3"),
    path("terminal-provider/wizard/step4/", TerminalWizardStep4View.as_view(), name="wizard_step4"),
    path("terminal-provider/wizard/step5/", TerminalWizardStep5View.as_view(), name="wizard_step5"),
    # Reader Wizard
    path("reader/wizard/step1/", ReaderWizardStep1View.as_view(), name="reader_wizard_step1"),
    path("reader/wizard/step2/", ReaderWizardStep2View.as_view(), name="reader_wizard_step2"),
    path("reader/wizard/step3/", ReaderWizardStep3View.as_view(), name="reader_wizard_step3"),
    # Terminal Quick Actions
    path("terminals/unlock/", unlock_terminal, name="terminal_unlock"),
    # Reader Quick Actions
    path("readers/sync/", sync_readers, name="sync_readers"),
    path("readers/quick-assign/", quick_assign_reader, name="quick_assign_reader"),
    path(
        "readers/<uuid:reader_id>/refresh-status/",
        refresh_reader_status,
        name="refresh_reader_status",
    ),
    # POS License activation
    path("license/activate/", activate_license, name="activate_license"),
]
