from django.urls import path
from . import views

app_name = 'translations'

urlpatterns = [
    # Dashboard
    path('', views.dashboard_view, name='dashboard'),

    # Service management
    path('local-service/', views.local_service_view, name='local_service'),

    # Language management
    path('languages/', views.language_management_view, name='language_management'),

    # External providers management
    path('external-providers/', views.external_providers_view, name='external_providers'),
    path('browse-providers/', views.browse_providers_view, name='browse_providers'),
    path('providers/install/<slug:provider_slug>/', views.install_translation_provider_ajax, name='install_provider'),
    path('providers/update/<slug:provider_slug>/', views.update_translation_provider_ajax, name='update_provider'),
    path('provider-wizard/<str:provider_type>/', views.provider_wizard_view, name='provider_wizard'),

    # UI Translation Editor
    path('ui-translations/', views.ui_translations_editor_view, name='ui_translations_editor'),

    # Coverage
    path('coverage/', views.coverage_detail_view, name='coverage_detail'),

    # Translation Jobs Management
    path('jobs/', views.translation_jobs_view, name='translation_jobs'),
]
