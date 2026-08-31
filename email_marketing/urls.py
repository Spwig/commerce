"""Public (non-i18n) URLs for the Campaign Studio."""

from django.urls import path

from . import views

app_name = "email_marketing"

urlpatterns = [
    path("unsubscribe/<str:token>/", views.unsubscribe, name="unsubscribe"),
]
