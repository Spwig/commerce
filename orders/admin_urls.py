"""
Orders Admin URLs.
Routes for AJAX filter endpoints used in admin change lists.
"""

from django.urls import path

from . import admin_views

app_name = "orders_admin"

urlpatterns = [
    path("returns/filter/", admin_views.filter_return_requests, name="filter_return_requests"),
]
