"""
Admin URL routing for search AJAX endpoints and wizard.
"""
from django.urls import path

from . import admin_views
from .views.engine_wizard import (
    EngineWizardStep1View,
    EngineWizardStep2View,
    EngineWizardStep3View,
    EngineWizardStep4View,
)

app_name = 'search_admin'

urlpatterns = [
    # Analytics
    path('analytics/filter/', admin_views.filter_search_queries, name='analytics_filter'),
    path('analytics/dashboard-data/', admin_views.dashboard_data, name='dashboard_data'),
    path('analytics/export/', admin_views.export_analytics, name='export_analytics'),

    # Synonyms
    path('synonyms/filter/', admin_views.filter_synonyms, name='synonyms_filter'),

    # Redirects
    path('redirects/filter/', admin_views.filter_redirects, name='redirects_filter'),

    # Search Engines
    path('engines/filter/', admin_views.filter_engines, name='engines_filter'),

    # Search Engine Wizard
    path('engine/wizard/step-1/', EngineWizardStep1View.as_view(), name='engine_wizard_step1'),
    path('engine/wizard/step-2/', EngineWizardStep2View.as_view(), name='engine_wizard_step2'),
    path('engine/wizard/step-3/', EngineWizardStep3View.as_view(), name='engine_wizard_step3'),
    path('engine/wizard/step-4/', EngineWizardStep4View.as_view(), name='engine_wizard_step4'),
]
