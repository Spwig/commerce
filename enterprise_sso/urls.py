from django.urls import path

from . import views

urlpatterns = [
    path('callback/', views.SpwigOIDCCallbackView.as_view(), name='oidc_authentication_callback'),
    path('authenticate/', views.SpwigOIDCAuthenticateView.as_view(), name='oidc_authentication_init'),
    path('logout/', views.SpwigOIDCLogoutView.as_view(), name='oidc_logout'),
    path('discover/', views.oidc_discover, name='oidc_discover'),
]
