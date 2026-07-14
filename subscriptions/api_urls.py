"""
Subscription API URLs
Separate from UI URLs - included outside i18n_patterns in core/urls.py
"""

from rest_framework.routers import DefaultRouter

from .api_views import (
    CustomerSubscriptionViewSet,
    PaymentTokenViewSet,
    SubscriptionPlanViewSet,
)

app_name = "subscriptions_api"

router = DefaultRouter()
router.register(r"plans", SubscriptionPlanViewSet, basename="plan")
router.register(r"tokens", PaymentTokenViewSet, basename="token")
router.register(r"subscriptions", CustomerSubscriptionViewSet, basename="subscription")

urlpatterns = router.urls
