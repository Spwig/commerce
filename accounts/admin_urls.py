"""
Admin URL patterns for accounts app.

Staff-only views for analytics and reporting.
"""

from django.urls import path

from . import admin_views

urlpatterns = [
    path(
        "preference-analytics/",
        admin_views.preference_analytics_dashboard,
        name="preference_analytics_dashboard",
    ),
    path(
        "communicationpreference/filter/",
        admin_views.filter_preferences,
        name="filter_communication_preferences",
    ),
    path(
        "preferencechangelog/filter/",
        admin_views.filter_preference_changelogs,
        name="filter_preference_changelogs",
    ),
]
