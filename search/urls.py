"""
Frontend URL routing for search pages.
"""
from django.urls import path

from .views import SearchResultsView

app_name = 'search'

urlpatterns = [
    path('', SearchResultsView.as_view(), name='search'),
]
