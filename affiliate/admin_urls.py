"""
Admin URL configuration for affiliate app.
These URLs are for admin AJAX endpoints and list filtering.
"""

from django.urls import path

from affiliate import admin_views

app_name = "affiliate_admin"

urlpatterns = [
    # Admin List Filtering Endpoints
    path("commission/filter/", admin_views.filter_commissions, name="filter_commissions"),
    path("affiliates/filter/", admin_views.filter_affiliates, name="filter_affiliates"),
    path("programs/filter/", admin_views.filter_programs, name="filter_programs"),
    path("memberships/filter/", admin_views.filter_memberships, name="filter_memberships"),
    path("payouts/filter/", admin_views.filter_payouts, name="filter_payouts"),
]
