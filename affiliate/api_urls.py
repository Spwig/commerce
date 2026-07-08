"""
Affiliate App API URLs
These URLs should be included WITHOUT language prefixes
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'affiliate_api'

# API Router
router = DefaultRouter()
router.register(r'programs', views.ProgramViewSet, basename='program')
router.register(r'affiliates', views.AffiliateViewSet, basename='affiliate')
router.register(r'links', views.LinkViewSet, basename='link')
router.register(r'commissions', views.CommissionViewSet, basename='commission')
router.register(r'payouts', views.PayoutViewSet, basename='payout')

urlpatterns = router.urls