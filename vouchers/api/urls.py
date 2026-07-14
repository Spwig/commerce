"""
Vouchers API URLs
These URLs should be included WITHOUT language prefixes
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from vouchers.api import views

# Create router for API viewsets
router = DefaultRouter()
router.register(r"vouchers", views.VoucherCodeViewSet, basename="voucher")
router.register(r"usage", views.VoucherUsageViewSet, basename="voucher-usage")
router.register(r"gift-cards", views.GiftCardViewSet, basename="gift-card")
router.register(r"restrictions", views.VoucherRestrictionViewSet, basename="voucher-restriction")
router.register(r"applied", views.AppliedVoucherViewSet, basename="applied-voucher")

app_name = "vouchers_api"

urlpatterns = [
    path("", include(router.urls)),
]
