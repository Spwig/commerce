"""
API URL configuration for custom fields (non-i18n).

These URLs live under /api/custom-fields/ (outside i18n_patterns).
"""
from django.urls import path
from . import api_views

app_name = 'custom_fields_api'

urlpatterns = [
    path('definitions/', api_views.FieldDefinitionListView.as_view(), name='definitions_list'),
    path('definitions/<int:pk>/', api_views.FieldDefinitionDetailView.as_view(), name='definition_detail'),
]
