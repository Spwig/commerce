"""
API URL routing for search endpoints.
"""

from django.urls import path

from .api_views import (
    AutocompleteAPIView,
    SearchEnginesAPIView,
    SearchResultsAPIView,
    SearchSettingsAPIView,
    SuggestCorrectionsAPIView,
    TrackClickAPIView,
    TrendingSearchesAPIView,
)

app_name = "search_api"

urlpatterns = [
    path("autocomplete/", AutocompleteAPIView.as_view(), name="autocomplete"),
    path("results/", SearchResultsAPIView.as_view(), name="results"),
    path("trending/", TrendingSearchesAPIView.as_view(), name="trending"),
    path("settings/", SearchSettingsAPIView.as_view(), name="settings"),
    path("click/", TrackClickAPIView.as_view(), name="track_click"),
    path("suggest-corrections/", SuggestCorrectionsAPIView.as_view(), name="suggest"),
    path("engines/", SearchEnginesAPIView.as_view(), name="engines"),
]
