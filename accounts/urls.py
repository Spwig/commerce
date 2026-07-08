"""
URL configuration for accounts app
Provides OAuth admin dashboard views and customer account management.
NOTE: API endpoints have been moved to api_urls.py and are included at /api/accounts/
"""
from django.urls import path, include
from . import oauth_views, views

app_name = 'accounts'

# Admin URL patterns (for staff)
urlpatterns = [
    # OAuth Admin Dashboard & Wizards (staff only)
    path('oauth/dashboard/', oauth_views.oauth_dashboard, name='oauth_dashboard'),
    path('oauth/wizard/<str:provider_type>/', oauth_views.oauth_provider_wizard, name='oauth_wizard'),

    # Customer Subscription Management
    path('subscriptions/', views.subscription_list, name='subscription_list'),
    path('subscriptions/<uuid:subscription_id>/', views.subscription_detail, name='subscription_detail'),
    path('subscriptions/<uuid:subscription_id>/pause/', views.subscription_pause, name='subscription_pause'),
    path('subscriptions/<uuid:subscription_id>/resume/', views.subscription_resume, name='subscription_resume'),
    path('subscriptions/<uuid:subscription_id>/cancel/', views.subscription_cancel, name='subscription_cancel'),
    path('subscriptions/<uuid:subscription_id>/update-payment/', views.subscription_update_payment, name='subscription_update_payment'),

    # Payment Token Management
    path('payment-methods/', views.payment_token_list, name='payment_token_list'),
    path('payment-methods/<uuid:token_id>/delete/', views.payment_token_delete, name='payment_token_delete'),
    path('payment-methods/<uuid:token_id>/set-default/', views.payment_token_set_default, name='payment_token_set_default'),

    # Address Management
    path('addresses/', views.customer_address_list, name='address_list'),
    path('addresses/add/', views.customer_address_add, name='address_add'),
    path('addresses/<int:address_id>/edit/', views.customer_address_edit, name='address_edit'),
    path('addresses/<int:address_id>/delete/', views.customer_address_delete, name='address_delete'),
    path('addresses/<int:address_id>/set-default/<str:address_type>/', views.customer_address_set_default, name='address_set_default'),

    # Customer Messages
    path('messages/', views.message_list, name='message_list'),
    path('messages/new/', views.message_new, name='message_new'),
    path('messages/<int:message_id>/', views.message_detail, name='message_detail'),

    # Customer Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Profile Settings
    path('profile/', views.profile, name='profile'),

    # Guest Account Activation
    path('activate-guest/<str:uidb64>/<str:token>/', views.activate_guest_account, name='activate_guest_account'),

    # Guest Order Lookup (magic link)
    path('guest-orders/', views.guest_order_lookup, name='guest_order_lookup'),
    path('guest-orders/<str:uidb64>/<str:token>/', views.guest_orders_view, name='guest_orders_view'),

    # Communication Preferences
    path('preferences/', views.communication_preferences, name='communication_preferences'),
    path('preferences/history/', views.preference_history, name='preference_history'),
    path('unsubscribe/<str:token>/', views.unsubscribe, name='unsubscribe'),

    # Customer Bookings
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('bookings/<int:booking_id>/cancel/', views.booking_cancel_action, name='booking_cancel_action'),
    path('bookings/<int:booking_id>/reschedule/', views.booking_reschedule_action, name='booking_reschedule_action'),
]

# Hosted subscription management (HQ only — spwig.com)
from django.conf import settings as _settings
if getattr(_settings, 'SPWIG_IS_HQ', False):
    from . import views_hosting
    urlpatterns += [
        path('hosting/', views_hosting.hosting_detail, name='hosting_detail'),
        path('hosting/update-payment/', views_hosting.hosting_update_payment, name='hosting_update_payment'),
        path('hosting/cancel/', views_hosting.hosting_cancel, name='hosting_cancel'),
        path('hosting/undo-cancel/', views_hosting.hosting_undo_cancel, name='hosting_undo_cancel'),
        path('hosting/reactivate/', views_hosting.hosting_reactivate, name='hosting_reactivate'),
        path('hosting/change-interval/', views_hosting.hosting_change_interval, name='hosting_change_interval'),
    ]

# Include django-allauth URLs separately WITHOUT namespace
# This is required because allauth expects URLs like 'account_reauthenticate'
# without the 'accounts:' namespace prefix
# NOTE: These URLs are added to the parent urlconf without the accounts app_name namespace
from . import mfa_views

allauth_urlpatterns = [
    # Custom MFA authenticate view with trusted device support
    # This must come BEFORE allauth.urls to override the default
    path('2fa/authenticate/', mfa_views.authenticate, name='mfa_authenticate'),
    # All other allauth URLs (login, logout, password reset, etc.)
    path('', include('allauth.urls')),
]
