"""
Social Sharing Test Factories

Helper functions for creating test data.
"""

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from social_sharing.models import SocialShare, ShareCount
from social_sharing.settings_models import SocialSharingSettings

User = get_user_model()

_user_counter = 0


def create_user(email=None, is_staff=False, **kwargs):
    """Create a test user."""
    global _user_counter
    _user_counter += 1
    if email is None:
        email = f'testuser{_user_counter}@test.spwig.com'
    defaults = {
        'username': email,
        'email': email,
        'is_staff': is_staff,
        'is_superuser': is_staff,
    }
    defaults.update(kwargs)
    user = User.objects.create_user(password='testpass123', **defaults)
    return user


def get_product_content_type():
    """
    Get a ContentType for a model that is in ``SHAREABLE_CONTENT_TYPES``.

    Historically this returned ``auth.User``'s ContentType, but the share
    tracking views now enforce a whitelist of shareable storefront models,
    and ``user`` is (correctly) not in the whitelist. We use ``BlogPost``
    here because:
      - It's in the whitelist (``blogpost``)
      - It has minimal required fields (just ``title`` + ``slug``)
      - The blog app is always installed in Spwig
    """
    from blog.models import BlogPost
    return ContentType.objects.get_for_model(BlogPost)


def create_test_blog_post(title='Test Post', slug=None):
    """Create a minimal BlogPost for testing share tracking.

    Returns the created instance so tests can pass ``.pk`` as ``object_id``
    and satisfy the existence check in the tracking views.
    """
    from blog.models import BlogPost
    from django.utils.text import slugify
    import uuid
    if slug is None:
        # Ensure uniqueness across tests
        slug = f"{slugify(title)}-{uuid.uuid4().hex[:8]}"
    return BlogPost.objects.create(title=title, slug=slug)


def create_social_share(user=None, platform='facebook', content_type=None, object_id=1, **kwargs):
    """Create a SocialShare instance for testing."""
    if content_type is None:
        content_type = get_product_content_type()
    defaults = {
        'content_type': content_type,
        'object_id': object_id,
        'platform': platform,
        'shared_url': f'https://example.com/product/{object_id}/',
        'user': user,
        'device_type': SocialShare.DEVICE_DESKTOP,
    }
    defaults.update(kwargs)
    return SocialShare.objects.create(**defaults)


def create_share_count(platform='facebook', content_type=None, object_id=1, count=1, **kwargs):
    """Create a ShareCount instance for testing."""
    if content_type is None:
        content_type = get_product_content_type()
    defaults = {
        'content_type': content_type,
        'object_id': object_id,
        'platform': platform,
        'count': count,
    }
    defaults.update(kwargs)
    return ShareCount.objects.create(**defaults)


def create_settings(**kwargs):
    """Create or update the SocialSharingSettings singleton."""
    defaults = {
        'enable_on_products': True,
        'enable_on_categories': False,
        'enable_on_blog_posts': True,
        'enable_on_pages': False,
        'placement_position': 'below_content',
        'button_style': 'icon_only',
        'button_size': 'medium',
        'layout_direction': 'horizontal',
        'show_title': True,
        'mobile_visibility': 'show',
        'show_counts': True,
        'track_shares': True,
    }
    defaults.update(kwargs)
    settings, _ = SocialSharingSettings.objects.get_or_create(pk=1, defaults=defaults)
    if _:
        return settings
    for key, value in defaults.items():
        setattr(settings, key, value)
    settings.save()
    return settings
