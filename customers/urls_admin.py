"""
URL configuration for Customers Admin (Staff-only views)
"""

from django.urls import path

from . import views

app_name = "customers"

# Staff-only URLs (admin interface) - accessed via /admin/customers/
urlpatterns = [
    path("dashboard/", views.customer_dashboard, name="dashboard"),
    path("analytics-api/", views.customer_analytics_api, name="analytics_api"),
    path("export/", views.export_customers, name="export"),
    path("refresh-metrics/", views.refresh_customer_metrics, name="refresh_metrics"),
    path("filter/", views.filter_customers, name="filter_customers"),
    path("add-note/", views.add_customer_note, name="add_customer_note"),
    path(
        "profile/<int:object_id>/actions/",
        views.customer_profile_actions,
        name="customer_profile_actions",
    ),
    # LTV Configuration and Analytics
    path("ltv/settings/", views.ltv_settings, name="ltv_settings"),
    path("ltv/cohorts/", views.cohort_dashboard, name="cohort_dashboard"),
    path("ltv/recalculate/", views.recalculate_ltv, name="recalculate_ltv"),
    path("ltv/cohort-data/", views.cohort_data_api, name="cohort_data_api"),
]
