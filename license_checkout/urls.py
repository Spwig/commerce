from django.urls import path

from . import views

app_name = 'license_checkout'

urlpatterns = [
    # Self-hosted license purchase
    path('catalog/', views.LicenseCatalogView.as_view(), name='catalog'),
    path('trial/', views.StartTrialView.as_view(), name='start_trial'),
    path('checkout/', views.InitiateCheckoutView.as_view(), name='checkout'),
    path('renew-info/<str:license_key>/', views.RenewalInfoView.as_view(), name='renew_info'),
    path('renew/', views.InitiateRenewalView.as_view(), name='renew'),
    path('status/<uuid:intent_id>/', views.PaymentStatusView.as_view(), name='payment_status'),
    path('status/by-checkout/<uuid:checkout_id>/', views.PaymentStatusByCheckoutView.as_view(), name='payment_status_by_checkout'),

    # Hosted subscription purchase
    path('hosted-catalog/', views.HostedCatalogView.as_view(), name='hosted_catalog'),
    path('check-store-name/', views.CheckStoreNameView.as_view(), name='check_store_name'),
    path('hosted-checkout/', views.InitiateHostedCheckoutView.as_view(), name='hosted_checkout'),
    path('hosted-status/<uuid:checkout_id>/', views.HostedCheckoutStatusView.as_view(), name='hosted_status'),
    path('hosted-cancel/', views.CancelHostedSubscriptionView.as_view(), name='hosted_cancel'),
]
