"""
HQ-only API URL configuration for the Spwig merchant account portal.

Only loaded when SPWIG_IS_HQ=True — registered in core/urls.py.
Auth endpoints (login, register, password-reset) are reused from the
existing /api/accounts/ routes — not duplicated here.
"""
from django.urls import path
from . import api_views_hq as views

app_name = 'accounts_hq_api'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.account_dashboard, name='dashboard'),

    # Hosting — subscription list
    path('hosting/subscriptions/', views.hosting_subscription_list, name='hosting_list'),

    # Hosting — scoped by subscription ID (multi-subscription support)
    path('hosting/<uuid:subscription_id>/', views.hosting_subscription_detail, name='hosting_detail_scoped'),
    path('hosting/<uuid:subscription_id>/billing-history/', views.hosting_billing_history, name='hosting_billing_scoped'),
    path('hosting/<uuid:subscription_id>/cancel/', views.hosting_cancel, name='hosting_cancel_scoped'),
    path('hosting/<uuid:subscription_id>/undo-cancel/', views.hosting_undo_cancel, name='hosting_undo_cancel_scoped'),
    path('hosting/<uuid:subscription_id>/reactivate/', views.hosting_reactivate, name='hosting_reactivate_scoped'),
    path('hosting/<uuid:subscription_id>/update-payment/', views.hosting_update_payment, name='hosting_update_payment_scoped'),
    path('hosting/<uuid:subscription_id>/change-interval/', views.hosting_change_interval, name='hosting_change_interval_scoped'),

    # Hosting — flat paths (backward compat, default to first subscription)
    path('hosting/subscription/', views.hosting_subscription_detail, name='hosting_detail'),
    path('hosting/billing-history/', views.hosting_billing_history, name='hosting_billing'),
    path('hosting/cancel/', views.hosting_cancel, name='hosting_cancel'),
    path('hosting/undo-cancel/', views.hosting_undo_cancel, name='hosting_undo_cancel'),
    path('hosting/reactivate/', views.hosting_reactivate, name='hosting_reactivate'),
    path('hosting/update-payment/', views.hosting_update_payment, name='hosting_update_payment'),
    path('hosting/change-interval/', views.hosting_change_interval, name='hosting_change_interval'),

    # License — all licenses (multi-license support)
    path('licenses/', views.license_list, name='license_list'),

    # License — singular (backward compat, returns first)
    path('license/', views.license_detail, name='license_detail'),
    path('license/maintenance/', views.license_maintenance, name='license_maintenance'),

    # Profile
    path('change-password/', views.change_password, name='change_password'),

    # Ghost account activation
    path('activate/', views.activate_ghost_account, name='activate_ghost'),
]
