"""
Subscription API URLs
Separate from UI URLs - included outside i18n_patterns in core/urls.py
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    SubscriptionPlanViewSet,
    PaymentTokenViewSet,
    CustomerSubscriptionViewSet,
)

app_name = 'subscriptions_api'

router = DefaultRouter()
router.register(r'plans', SubscriptionPlanViewSet, basename='plan')
router.register(r'tokens', PaymentTokenViewSet, basename='token')
router.register(r'subscriptions', CustomerSubscriptionViewSet, basename='subscription')

urlpatterns = router.urls
