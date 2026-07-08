"""
Social Sharing URL Configuration

URLs for admin views and AJAX endpoints.
"""

from django.urls import path
from . import views

app_name = 'social_sharing'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.social_sharing_dashboard, name='dashboard'),

    # AJAX filter endpoints for admin
    path('socialshare/filter/', views.filter_shares, name='filter_shares'),
    path('sharecount/filter/', views.filter_sharecounts, name='filter_sharecounts'),
]
