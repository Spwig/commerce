# Blog views package
# Re-export all frontend views for backwards compatibility

# Wizard views are imported separately via blog.views.wizard
from blog.views import wizard
from blog.views.frontend import (
    BlogRSSFeed,
    BlogRSSFeedGenerator,
    blog_list,
    category_posts,
    get_blog_context,
    post_detail,
    subscribe,
    subscription_preferences,
    tag_posts,
    unsubscribe,
    verify_subscription,
)

__all__ = [
    # Frontend views
    "get_blog_context",
    "blog_list",
    "post_detail",
    "category_posts",
    "tag_posts",
    "subscribe",
    "verify_subscription",
    "unsubscribe",
    "subscription_preferences",
    "BlogRSSFeed",
    "BlogRSSFeedGenerator",
    # Wizard module
    "wizard",
]
