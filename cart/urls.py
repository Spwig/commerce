"""
URL configuration for Cart API
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CartViewSet, WishlistViewSet, CheckoutViewSet,
    RecentlyViewedViewSet, ShippingMethodViewSet,
    TaxRateViewSet, TaxPresetViewSet,
)
from .mini_cart_api import (
    mini_cart_get, mini_cart_update, mini_cart_remove, cart_empty_recommendations
)
from .method_wizard import (
    MethodWizardStep1View, MethodWizardStep2View, MethodWizardStep3View,
    MethodWizardStep4View, MethodWizardStep5View
)

app_name = 'cart'

# Create router for viewsets
router = DefaultRouter()
router.register(r'wishlists', WishlistViewSet, basename='wishlist')
router.register(r'recently-viewed', RecentlyViewedViewSet, basename='recently-viewed')
router.register(r'shipping-methods', ShippingMethodViewSet, basename='shipping-method')
router.register(r'tax-rates', TaxRateViewSet, basename='tax-rate')
router.register(r'tax-presets', TaxPresetViewSet, basename='tax-preset')

# Cart and Checkout use custom routing due to their non-standard endpoints
urlpatterns = [
    # Mini-cart API endpoints (simple JSON for frontend)
    path('cart/get/', mini_cart_get, name='mini-cart-get'),
    path('cart/update/', mini_cart_update, name='mini-cart-update'),
    path('cart/remove/', mini_cart_remove, name='mini-cart-remove'),
    path('cart/empty-recommendations/', cart_empty_recommendations, name='cart-empty-recommendations'),

    # Cart endpoints
    path('cart/', CartViewSet.as_view({'get': 'list'}), name='cart-detail'),
    path('cart/add/', CartViewSet.as_view({'post': 'add'}), name='cart-add'),
    path('cart/items/<int:item_id>/', CartViewSet.as_view({
        'patch': 'update_item',
        'delete': 'remove_item'
    }), name='cart-item-detail'),
    path('cart/clear/', CartViewSet.as_view({'post': 'clear'}), name='cart-clear'),
    path('cart/apply-voucher/', CartViewSet.as_view({'post': 'apply_voucher'}), name='cart-apply-voucher'),
    path('cart/remove-voucher/<str:code>/', CartViewSet.as_view({'delete': 'remove_voucher'}), name='cart-remove-voucher'),
    path('cart/summary/', CartViewSet.as_view({'get': 'summary'}), name='cart-summary'),

    # Checkout endpoints
    path('checkout/', CheckoutViewSet.as_view({'get': 'list'}), name='checkout-session'),
    path('checkout/shipping-address/', CheckoutViewSet.as_view({'post': 'set_shipping_address'}), name='checkout-shipping-address'),
    path('checkout/billing-address/', CheckoutViewSet.as_view({'post': 'set_billing_address'}), name='checkout-billing-address'),
    path('checkout/shipping-methods/', CheckoutViewSet.as_view({'get': 'get_shipping_methods'}), name='checkout-shipping-methods'),
    path('checkout/shipping-method/', CheckoutViewSet.as_view({'post': 'set_shipping_method'}), name='checkout-shipping-method'),
    path('checkout/payment-providers/', CheckoutViewSet.as_view({'get': 'get_payment_providers'}), name='checkout-payment-providers'),
    path('checkout/payment-method/', CheckoutViewSet.as_view({'post': 'set_payment_method'}), name='checkout-payment-method'),
    path('checkout/validate/', CheckoutViewSet.as_view({'post': 'validate'}), name='checkout-validate'),
    path('checkout/complete/', CheckoutViewSet.as_view({'post': 'complete'}), name='checkout-complete'),

    # Router URLs (wishlists, recently-viewed, shipping-methods)
    path('', include(router.urls)),

    # Shipping Method Wizard (Admin)
    path('admin/method-wizard/step1/', MethodWizardStep1View.as_view(), name='method_wizard_step1'),
    path('admin/method-wizard/step2/', MethodWizardStep2View.as_view(), name='method_wizard_step2'),
    path('admin/method-wizard/step3/', MethodWizardStep3View.as_view(), name='method_wizard_step3'),
    path('admin/method-wizard/step4/', MethodWizardStep4View.as_view(), name='method_wizard_step4'),
    path('admin/method-wizard/step5/', MethodWizardStep5View.as_view(), name='method_wizard_step5'),
]
