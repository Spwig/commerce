"""
Blog URL configuration.

Provides URLs for:
- Blog listing and filtering
- Blog post detail view
- Category and tag pages
- Subscriber verification and management
- RSS feed

"""

from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    # Blog listing
    path("", views.blog_list, name="list"),
    # Category pages
    path("category/<slug:slug>/", views.category_posts, name="category"),
    # Tag pages
    path("tag/<slug:slug>/", views.tag_posts, name="tag"),
    # Post detail
    path("<slug:slug>/", views.post_detail, name="detail"),
    # Subscriber endpoints
    path("subscribe/", views.subscribe, name="subscribe"),
    path("verify/<str:token>/", views.verify_subscription, name="verify"),
    path("unsubscribe/<str:token>/", views.unsubscribe, name="unsubscribe"),
    path("preferences/<str:token>/", views.subscription_preferences, name="preferences"),
    # RSS Feed
    path("feed/rss/", views.BlogRSSFeed(), name="rss_feed"),
]
