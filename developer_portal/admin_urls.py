"""
Developer Portal Admin URL Configuration
AJAX filter endpoints for developer portal admin change_list pages.
"""

from django.urls import path
from . import admin_views

app_name = 'developer_portal_admin'

urlpatterns = [
    path('componentsubmission/filter/', admin_views.filter_submissions, name='filter_submissions'),
    path('developerprofile/filter/', admin_views.filter_developers, name='filter_developers'),
    path('developerlicenserequest/filter/', admin_views.filter_license_requests, name='filter_license_requests'),
]
