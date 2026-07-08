"""
URL configuration for Theme SDK Development Server API.

These endpoints enable the Spwig Theme SDK CLI to connect to a running
shop instance for live theme development with hot reload.

All endpoints are prefixed with /api/theme-dev/ in core/urls.py
"""

from django.urls import path
from . import dev_server_views as views

app_name = 'theme_dev'

urlpatterns = [
    # Session management
    path('connect/', views.dev_connect, name='connect'),
    path('disconnect/', views.dev_disconnect, name='disconnect'),
    path('status/', views.dev_status, name='status'),

    # File synchronization
    path('sync/', views.dev_sync_files, name='sync'),
    path('sync/full/', views.dev_sync_full, name='sync_full'),

    # Hot reload (Server-Sent Events)
    path('watch/', views.dev_watch, name='watch'),

    # Theme operations
    path('validate/', views.dev_validate, name='validate'),
    path('compile-css/', views.dev_compile_css, name='compile_css'),

    # Component operations
    path('components/', views.dev_list_components, name='list_components'),
    path('components/<str:component_name>/', views.dev_component_detail, name='component_detail'),

    # Preview
    path('preview/', views.dev_preview_url, name='preview_url'),
]
