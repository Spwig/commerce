from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.BrowseView.as_view(), name='browse'),
    path('api/browse/', views.browse_api, name='browse_api'),
    path('api/install/', views.install_ajax, name='install_ajax'),
    path('api/review/', views.review_ajax, name='review_ajax'),
    path('<slug:slug>/', views.DetailView.as_view(), name='detail'),
    path('<slug:slug>/purchase/', views.purchase_redirect, name='purchase_redirect'),
]
