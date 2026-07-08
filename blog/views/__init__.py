# Blog views package
# Re-export all frontend views for backwards compatibility

from blog.views.frontend import (
    get_blog_context,
    blog_list,
    post_detail,
    category_posts,
    tag_posts,
    subscribe,
    verify_subscription,
    unsubscribe,
    subscription_preferences,
    BlogRSSFeed,
    BlogRSSFeedGenerator,
)

# Wizard views are imported separately via blog.views.wizard
from blog.views import wizard

__all__ = [
    # Frontend views
    'get_blog_context',
    'blog_list',
    'post_detail',
    'category_posts',
    'tag_posts',
    'subscribe',
    'verify_subscription',
    'unsubscribe',
    'subscription_preferences',
    'BlogRSSFeed',
    'BlogRSSFeedGenerator',
    # Wizard module
    'wizard',
]
