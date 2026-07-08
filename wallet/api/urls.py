"""
Wallet API URL Configuration

All endpoints live under /api/wallet/ (no language prefix).
"""
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'wallets', views.AdminWalletViewSet, basename='wallet')
router.register(
    r'admin-transactions',
    views.AdminTransactionViewSet,
    basename='wallet-admin-transaction',
)

urlpatterns = [
    # Customer-facing endpoints
    path(
        'balance/',
        views.WalletBalanceViewSet.as_view({'get': 'list'}),
        name='wallet-balance',
    ),
    path(
        'transactions/',
        views.WalletTransactionViewSet.as_view({'get': 'list'}),
        name='wallet-transactions',
    ),
]

urlpatterns += router.urls
