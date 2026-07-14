"""
URL configuration for Customers API (Customer-facing)
"""

from django.urls import path

from . import views

# Customer-facing REST API URLs (accessed via /api/customers/)
# These endpoints provide analytics and insights for logged-in customers
# No app_name to avoid namespace conflict with admin URLs
urlpatterns = [
    # Dashboard & Statistics
    path("dashboard/", views.CustomerDashboardViewSet.as_view({"get": "list"}), name="dashboard"),
    path("stats/", views.CustomerDashboardViewSet.as_view({"get": "stats"}), name="stats"),
    path("insights/", views.CustomerDashboardViewSet.as_view({"get": "insights"}), name="insights"),
    # Analytics
    path(
        "lifetime-value/",
        views.CustomerAnalyticsViewSet.as_view({"get": "lifetime_value"}),
        name="lifetime-value",
    ),
    path(
        "loyalty-status/",
        views.CustomerAnalyticsViewSet.as_view({"get": "loyalty_status"}),
        name="loyalty-status",
    ),
    path("savings/", views.CustomerAnalyticsViewSet.as_view({"get": "savings"}), name="savings"),
    # Preferences & Recommendations
    path(
        "favorites/",
        views.CustomerPreferencesViewSet.as_view({"get": "favorites"}),
        name="favorites",
    ),
    path(
        "recommendations/",
        views.CustomerPreferencesViewSet.as_view({"get": "recommendations"}),
        name="recommendations",
    ),
    # Digital Products
    path(
        "digital-products/",
        views.CustomerDigitalProductsViewSet.as_view({"get": "list"}),
        name="digital-products",
    ),
    path(
        "digital-products/<int:pk>/download/",
        views.CustomerDigitalProductsViewSet.as_view({"get": "get_download_link"}),
        name="digital-product-download",
    ),
    path(
        "digital-products/licenses/",
        views.CustomerDigitalProductsViewSet.as_view({"get": "licenses"}),
        name="digital-product-licenses",
    ),
    path(
        "digital-products/licenses/<int:license_id>/activate/",
        views.CustomerDigitalProductsViewSet.as_view({"post": "activate_license"}),
        name="digital-product-license-activate",
    ),
    path(
        "digital-products/licenses/<int:license_id>/deactivate/",
        views.CustomerDigitalProductsViewSet.as_view({"post": "deactivate_license"}),
        name="digital-product-license-deactivate",
    ),
    # Admin-only address management endpoints
    path(
        "admin/addresses/<int:address_id>/set-default/",
        views.set_address_default,
        name="admin-set-address-default",
    ),
]
