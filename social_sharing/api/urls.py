"""
Social Sharing API URLs
"""

from django.urls import path

from social_sharing.api import views

app_name = "social_sharing_api"

urlpatterns = [
    # Track a share (authenticated users only — 50/hour rate limit)
    path("track/", views.track_share, name="track_share"),
    # Track a share anonymously (guests — strict 20/hour IP rate limit)
    path("track/anonymous/", views.track_share_anonymous, name="track_share_anonymous"),
    # Get share counts for content
    path(
        "counts/<str:content_type_str>/<int:object_id>/",
        views.get_share_counts,
        name="get_share_counts",
    ),
    # Get current user's shares
    path("user/shares/", views.get_user_shares, name="get_user_shares"),
]
