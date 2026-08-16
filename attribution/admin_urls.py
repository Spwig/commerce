"""Admin URLs for the Revenue Attribution dashboard.

Mounted under ``admin/insights/`` inside i18n_patterns, so the dashboard lives
at ``/<lang>/admin/insights/attribution/``.
"""

from django.urls import path

from . import admin_views

app_name = "attribution"

urlpatterns = [
    path("attribution/", admin_views.attribution_dashboard, name="dashboard"),
    path("attribution/data/", admin_views.attribution_data, name="dashboard_data"),
    path("attribution/export/", admin_views.attribution_export, name="dashboard_export"),
]
