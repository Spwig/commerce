"""Storefront newsletter URLs, mounted at ``/newsletter/`` (non-i18n).

Served at ``/newsletter/`` (not the app's ``/marketing/`` prefix) to match the
default form action that ships in the page-builder newsletter element and the
footer/header widget — existing merchant pages post there already.
"""

from django.urls import path

from . import views

app_name = "newsletter"

urlpatterns = [
    path("subscribe/", views.subscribe, name="subscribe"),
    path("confirm/<str:token>/", views.confirm, name="confirm"),
]
