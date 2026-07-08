"""
API URL configuration for the blog app.
All endpoints live outside i18n_patterns (no language prefix).
Included in core/urls.py under path('api/blog/', ...).

"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

app_name = 'blog_api'

router = DefaultRouter()
router.register(r'posts', api_views.BlogPostViewSet, basename='post')
router.register(r'categories', api_views.BlogCategoryViewSet, basename='category')
router.register(r'tags', api_views.BlogTagViewSet, basename='tag')

urlpatterns = [
    # Subscription management endpoints (public, token-gated)
    path('subscribe/', api_views.blog_subscribe, name='subscribe'),
    path('verify/<str:token>/', api_views.blog_verify_subscription, name='verify'),
    path('unsubscribe/<str:token>/', api_views.blog_unsubscribe, name='unsubscribe'),
    path('preferences/<str:token>/', api_views.blog_subscription_preferences, name='preferences'),

    # Public settings
    path('settings/', api_views.blog_settings_api, name='settings'),

    # ViewSet routes (posts, categories, tags)
    path('', include(router.urls)),
]
