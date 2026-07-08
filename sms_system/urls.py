"""
SMS System URL Configuration.

Provides URLs for the SMS provider setup wizard and provider browsing.
"""
from django.urls import path

from . import views
from . import admin_views

app_name = 'sms_system'

urlpatterns = [
    # AJAX filter endpoints
    path('outbox/filter/', admin_views.filter_sms_outbox, name='outbox_filter'),

    # Provider wizard
    path('wizard/', views.WizardStep1View.as_view(), name='wizard_step1'),
    path('wizard/step2/', views.WizardStep2View.as_view(), name='wizard_step2'),
    path('wizard/step3/', views.WizardStep3View.as_view(), name='wizard_step3'),
    path('wizard/step4/', views.WizardStep4View.as_view(), name='wizard_step4'),
    path('wizard/complete/', views.WizardCompleteView.as_view(), name='wizard_complete'),

    # Provider browse
    path('providers/', views.ProviderBrowseView.as_view(), name='provider_browse'),
    path('providers/install/<slug:provider_slug>/', views.install_provider_ajax, name='provider_install'),
    path('providers/update/<slug:provider_slug>/', views.update_provider_ajax, name='provider_update'),

    # AJAX endpoints
    path('api/test-connection/', views.TestConnectionView.as_view(), name='test_connection'),
    path('api/setup-instructions/<str:provider_key>/', views.SetupInstructionsView.as_view(), name='setup_instructions'),
]
