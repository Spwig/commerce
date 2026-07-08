"""
API URL configuration for core app.
Help system and core platform APIs.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.api import help_views, badge_api

app_name = 'core_api'

# Create router for viewsets
router = DefaultRouter()
router.register(r'help/categories', help_views.HelpCategoryViewSet, basename='help-category')
router.register(r'help/topics', help_views.HelpTopicViewSet, basename='help-topic')
router.register(r'help/feedback', help_views.HelpFeedbackViewSet, basename='help-feedback')

# API URL patterns
urlpatterns = [
    # Help system endpoints (router-based)
    path('', include(router.urls)),

    # Admin metadata endpoint for help system documentation discovery
    path('admin-metadata/', help_views.admin_metadata_api, name='admin-metadata'),

    # Badge counts for AJAX sidebar refresh
    path('badges/', badge_api.get_badge_counts, name='badge-counts'),
]
