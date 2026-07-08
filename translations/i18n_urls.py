"""
Custom i18n URL patterns that replace django.conf.urls.i18n.

The custom set_language view accepts any active SiteLanguage code,
not just those in settings.LANGUAGES (handles race conditions when
a language was just activated but LANGUAGES wasn't updated yet).
"""
from django.urls import path
from translations.i18n_views import merchant_set_language

urlpatterns = [
    path('setlang/', merchant_set_language, name='set_language'),
]
