"""
URL configuration for webhooks app (admin/frontend URLs).

These URLs go inside i18n_patterns for language-prefixed admin URLs.
"""
from django.urls import path
from . import views

app_name = 'webhooks'

urlpatterns = [
    path('endpoints/filter/', views.filter_endpoints, name='filter_endpoints'),
    path('endpoints/wizard/', views.endpoint_wizard, name='endpoint_wizard'),
    path('documentation/', views.webhook_documentation, name='documentation'),
]
