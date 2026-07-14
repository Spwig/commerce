"""
Admin URL routing for GeoIP AJAX endpoints and admin provider management.
"""

from django.urls import path

from . import admin_views, views

app_name = "geoip_admin"

urlpatterns = [
    # GeoLocation AJAX filter
    path("geolocations/filter/", admin_views.filter_geolocations, name="geolocations_filter"),
    # VisitorLocation AJAX filter
    path("visitors/filter/", admin_views.filter_visitor_locations, name="visitors_filter"),
    # Visitor Analytics Dashboard
    path("analytics/", admin_views.visitor_analytics_dashboard, name="visitor_analytics"),
    path("analytics/data/", admin_views.visitor_analytics_data, name="visitor_analytics_data"),
    # Admin provider management
    path("providers/", views.provider_dashboard, name="provider_dashboard"),
    path("provider-wizard/<str:provider_type>/", views.provider_wizard, name="provider_wizard"),
    path("test-provider/<str:provider_type>/", views.test_provider, name="test_provider"),
    path("toggle-provider/<int:provider_id>/", views.toggle_provider, name="toggle_provider"),
    path("update-database/<int:provider_id>/", views.update_database, name="update_database"),
]
