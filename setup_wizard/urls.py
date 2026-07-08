from django.urls import path
from . import views

app_name = 'setup_wizard'

urlpatterns = [
    # Legacy routes (redirect to dashboard)
    path('', views.wizard_start, name='start'),
    path('step/<str:step_key>/', views.wizard_step, name='step'),
    path('complete/', views.wizard_complete, name='complete'),
    path('skip/', views.wizard_skip, name='skip'),

    # AJAX API endpoints for modal wizard
    path('api/progress/', views.progress_api, name='progress_api'),
    path('api/step/<str:group_key>/', views.api_step_content, name='api_step_content'),
    path('api/step/<str:group_key>/save/', views.api_step_save, name='api_step_save'),
]
