"""
Blog Integration Tests for Communication Preferences.

Tests the dual system support where blog notifications check both
BlogSubscriber (legacy) and CommunicationPreference (new).
"""
import pytest
from unittest.mock import Mock, patch
from django.contrib.auth import get_user_model

from blog.models import BlogPost, BlogCategory, BlogSubscriber
from accounts.models import CommunicationPreference
from tests.factories import UserFactory

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.blog_preferences]


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def blog_category(db):
    """Test blog category."""
    return BlogCategory.objects.create(
        name='Test Category',
        slug='test-category',
        is_active=True,
    )


@pytest.fixture
def published_post(db, blog_category):
    """Published blog post."""
    post = BlogPost.objects.create(
        title='Test Blog Post',
        slug='test-blog-post',
        content='This is a test post.',
        status='published',
    )
    post.categories.add(blog_category)
    return post


@pytest.fixture
def legacy_subscriber(db):
    """Legacy BlogSubscriber (not a registered user)."""
    return BlogSubscriber.objects.create(
        email='legacy@example.com',
        frequency='immediate',
        verification_status='verified',
    )


@pytest.fixture
def user_with_blog_preferences(db):
    """Registered user with blog preferences enabled."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.app_preferences['blog']['enabled'] = True
    prefs.app_preferences['blog']['frequency'] = 'immediate'
    prefs.save()
    return user


# ============================================================
# Dual System Support
# ============================================================

def test_blog_notification_sent_to_legacy_subscriber(legacy_subscriber, published_post):
    """Blog notifications sent to legacy BlogSubscriber users."""
    from blog.tasks import send_post_notification

    with patch('email_system.services.email_sender.EmailSendingService.send_template_email') as mock_send:
        mock_send.return_value = {'success': True}

        send_post_notification(published_post.id)

        # Should send to legacy subscriber
        assert mock_send.called
        call_args_list = [call[1] for call in mock_send.call_args_list]
        emails_sent = [call['to_email'] for call in call_args_list]
        assert legacy_subscriber.email in emails_sent


def test_blog_notification_sent_to_new_system_user(user_with_blog_preferences, published_post):
    """Blog notifications sent to users with CommunicationPreference enabled."""
    from blog.tasks import send_post_notification

    with patch('email_system.services.email_sender.EmailSendingService.send_template_email') as mock_send:
        mock_send.return_value = {'success': True}

        send_post_notification(published_post.id)

        # Should send to new system user
        assert mock_send.called
        call_args_list = [call[1] for call in mock_send.call_args_list]
        emails_sent = [call['to_email'] for call in call_args_list]
        assert user_with_blog_preferences.email in emails_sent


def test_blog_notification_no_duplicates(legacy_subscriber, published_post):
    """Blog notifications don't send duplicates when email exists in both systems."""
    from blog.tasks import send_post_notification

    # Create a user with same email as legacy subscriber
    user = UserFactory(email=legacy_subscriber.email)
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.app_preferences['blog']['enabled'] = True
    prefs.save()

    with patch('email_system.services.email_sender.EmailSendingService.send_template_email') as mock_send:
        mock_send.return_value = {'success': True}

        send_post_notification(published_post.id)

        # Should only send once (BlogSubscriber takes precedence)
        call_args_list = [call[1] for call in mock_send.call_args_list]
        emails_sent = [call['to_email'] for call in call_args_list]
        email_count = emails_sent.count(legacy_subscriber.email)
        assert email_count == 1


def test_blog_notification_respects_new_system_disabled(published_post):
    """Blog notifications not sent when user disabled blog in CommunicationPreference."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.app_preferences['blog']['enabled'] = False  # Disabled
    prefs.save()

    from blog.tasks import send_post_notification

    with patch('email_system.services.email_sender.EmailSendingService.send_template_email') as mock_send:
        mock_send.return_value = {'success': True}

        send_post_notification(published_post.id)

        # Should NOT send to this user
        if mock_send.called:
            call_args_list = [call[1] for call in mock_send.call_args_list]
            emails_sent = [call['to_email'] for call in call_args_list]
            assert user.email not in emails_sent


def test_blog_notification_respects_frequency_preference(user_with_blog_preferences, published_post):
    """Blog notifications respect frequency setting."""
    from blog.tasks import send_post_notification

    # Set to weekly digest
    prefs = user_with_blog_preferences.communication_preferences
    prefs.app_preferences['blog']['frequency'] = 'weekly'
    prefs.save()

    with patch('email_system.services.email_sender.EmailSendingService.send_template_email') as mock_send:
        mock_send.return_value = {'success': True}

        send_post_notification(published_post.id)

        # Should NOT send immediately (queued for weekly digest)
        if mock_send.called:
            call_args_list = [call[1] for call in mock_send.call_args_list]
            emails_sent = [call['to_email'] for call in call_args_list]
            assert user_with_blog_preferences.email not in emails_sent


def test_blog_notification_respects_email_not_verified(published_post):
    """Blog notifications not sent when email_verified=False."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = False  # Not verified
    prefs.app_preferences['blog']['enabled'] = True
    prefs.save()

    from blog.tasks import send_post_notification

    with patch('email_system.services.email_sender.EmailSendingService.send_template_email') as mock_send:
        mock_send.return_value = {'success': True}

        send_post_notification(published_post.id)

        # Should NOT send (not verified)
        if mock_send.called:
            call_args_list = [call[1] for call in mock_send.call_args_list]
            emails_sent = [call['to_email'] for call in call_args_list]
            assert user.email not in emails_sent


# ============================================================
# Category Preferences
# ============================================================

def test_blog_notification_respects_category_preferences(user_with_blog_preferences, blog_category, published_post):
    """Blog notifications respect category subscriptions."""
    # Subscribe to specific category
    prefs = user_with_blog_preferences.communication_preferences
    prefs.app_preferences['blog']['categories'] = [blog_category.id]
    prefs.save()

    from blog.tasks import send_post_notification

    with patch('email_system.services.email_sender.EmailSendingService.send_template_email') as mock_send:
        mock_send.return_value = {'success': True}

        send_post_notification(published_post.id)

        # Should send (post is in subscribed category)
        assert mock_send.called
        call_args_list = [call[1] for call in mock_send.call_args_list]
        emails_sent = [call['to_email'] for call in call_args_list]
        assert user_with_blog_preferences.email in emails_sent


def test_blog_notification_skips_unsubscribed_category(user_with_blog_preferences, published_post):
    """Blog notifications not sent for unsubscribed categories."""
    # Create different category
    other_category = BlogCategory.objects.create(
        name='Other Category',
        slug='other-category',
        is_active=True,
    )

    # Subscribe to other category only
    prefs = user_with_blog_preferences.communication_preferences
    prefs.app_preferences['blog']['categories'] = [other_category.id]
    prefs.save()

    # Post is in different category
    from blog.tasks import send_post_notification

    with patch('email_system.services.email_sender.EmailSendingService.send_template_email') as mock_send:
        mock_send.return_value = {'success': True}

        send_post_notification(published_post.id)

        # Should NOT send (post not in subscribed category)
        if mock_send.called:
            call_args_list = [call[1] for call in mock_send.call_args_list]
            emails_sent = [call['to_email'] for call in call_args_list]
            assert user_with_blog_preferences.email not in emails_sent


# ============================================================
# Email Message Type
# ============================================================

def test_blog_notification_uses_correct_message_type(user_with_blog_preferences, published_post):
    """Blog notifications use correct template_type for preference checking."""
    from blog.tasks import send_post_notification

    with patch('email_system.services.email_sender.EmailSendingService.send_template_email') as mock_send:
        mock_send.return_value = {'success': True}

        send_post_notification(published_post.id)

        # Verify template_type is blog_post_published
        assert mock_send.called
        call_kwargs = mock_send.call_args[1]
        assert call_kwargs['template_type'] == 'blog_post_published'


# ============================================================
# Legacy BlogSubscriber Compatibility
# ============================================================

def test_legacy_subscriber_frequency_immediate(legacy_subscriber, published_post):
    """Legacy BlogSubscriber with immediate frequency receives notifications."""
    legacy_subscriber.frequency = 'immediate'
    legacy_subscriber.save()

    from blog.tasks import send_post_notification

    with patch('email_system.services.email_sender.EmailSendingService.send_template_email') as mock_send:
        mock_send.return_value = {'success': True}

        send_post_notification(published_post.id)

        # Should send immediately
        assert mock_send.called


def test_legacy_subscriber_frequency_weekly_digest(legacy_subscriber, published_post):
    """Legacy BlogSubscriber with weekly digest doesn't receive immediate notifications."""
    legacy_subscriber.frequency = 'weekly_digest'
    legacy_subscriber.save()

    from blog.tasks import send_post_notification

    with patch('email_system.services.email_sender.EmailSendingService.send_template_email') as mock_send:
        mock_send.return_value = {'success': True}

        send_post_notification(published_post.id)

        # Should NOT send immediately (queued for digest)
        if mock_send.called:
            call_args_list = [call[1] for call in mock_send.call_args_list]
            emails_sent = [call['to_email'] for call in call_args_list]
            assert legacy_subscriber.email not in emails_sent


def test_legacy_subscriber_unverified_skipped(published_post):
    """Unverified legacy BlogSubscriber doesn't receive notifications."""
    subscriber = BlogSubscriber.objects.create(
        email='unverified@example.com',
        frequency='immediate',
        verification_status='pending',  # Not verified
    )

    from blog.tasks import send_post_notification

    with patch('email_system.services.email_sender.EmailSendingService.send_template_email') as mock_send:
        mock_send.return_value = {'success': True}

        send_post_notification(published_post.id)

        # Should NOT send (not verified)
        if mock_send.called:
            call_args_list = [call[1] for call in mock_send.call_args_list]
            emails_sent = [call['to_email'] for call in call_args_list]
            assert subscriber.email not in emails_sent


# ============================================================
# Edge Cases
# ============================================================

def test_blog_notification_no_subscribers(published_post):
    """Blog notification handles no subscribers gracefully."""
    from blog.tasks import send_post_notification

    with patch('email_system.services.email_sender.EmailSendingService.send_template_email') as mock_send:
        send_post_notification(published_post.id)

        # Should not crash, just not send any emails
        # (or send none if no subscribers)
        pass  # No assertion needed, just verify no exception


def test_blog_notification_both_systems_have_users(legacy_subscriber, user_with_blog_preferences, published_post):
    """Blog notification sends to both legacy and new system users."""
    from blog.tasks import send_post_notification

    with patch('email_system.services.email_sender.EmailSendingService.send_template_email') as mock_send:
        mock_send.return_value = {'success': True}

        send_post_notification(published_post.id)

        # Should send to both
        assert mock_send.called
        call_args_list = [call[1] for call in mock_send.call_args_list]
        emails_sent = [call['to_email'] for call in call_args_list]

        assert legacy_subscriber.email in emails_sent
        assert user_with_blog_preferences.email in emails_sent
        # Total 2 emails
        assert len(emails_sent) == 2
