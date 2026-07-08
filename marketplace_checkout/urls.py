from django.urls import path
from . import views

app_name = 'marketplace_checkout'

urlpatterns = [
    path(
        'purchase-token/<uuid:token_uuid>/',
        views.ValidatePurchaseTokenView.as_view(),
        name='validate-purchase-token'
    ),
    path(
        'checkout/',
        views.InitiateMarketplaceCheckoutView.as_view(),
        name='initiate-checkout'
    ),
    path(
        'payment-status/<uuid:intent_id>/',
        views.MarketplacePaymentStatusView.as_view(),
        name='payment-status'
    ),
]
