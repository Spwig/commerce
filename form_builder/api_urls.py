"""
Form Builder API URLs

These URLs are included outside i18n_patterns under /api/form-builder/
For public form submission endpoints.
"""
from django.urls import path
from . import api_views

app_name = 'form_builder_api'

urlpatterns = [
    # Form list for Page Builder selector (requires admin auth)
    path('forms/list/', api_views.FormListForSelectorView.as_view(), name='form-list'),

    # Form retrieval (public)
    path('forms/<slug:slug>/', api_views.FormDetailView.as_view(), name='form-detail'),

    # Form submission (public)
    path('forms/<slug:slug>/submit/', api_views.FormSubmitView.as_view(), name='form-submit'),

    # Partial response saving (for multi-step forms)
    path('forms/<slug:slug>/partial/', api_views.SavePartialView.as_view(), name='form-partial'),

    # File upload for form fields
    path('forms/<slug:slug>/upload/', api_views.FileUploadView.as_view(), name='form-upload'),
]
