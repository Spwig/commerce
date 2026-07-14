"""
Blog Integration Tests for Communication Preferences.

Tests the dual system support where blog notifications check both
BlogSubscriber (legacy) and CommunicationPreference (new).

Notes
-----
- The task is ``blog.tasks.notify_subscribers_of_new_post`` (imported from
  ``blog.tasks``); older suites called it ``send_post_notification`` which
  never existed.
- BlogPost content lives in ``simple_content``, not ``content``.
- BlogSubscriber uses ``notification_frequency`` (not ``frequency``) and
  requires ``unsubscribe_token``.
- BlogPost has a single ``category`` FK, not a ``categories`` M2M.
- The blog task uses ``EmailSendingService.queue_email(...)`` inside a
  helper (``_send_new_post_notification``), so patching send_template_email
  will not intercept it.
"""

import uuid
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model

from blog.models import BlogCategory, BlogPost, BlogSubscriber
from blog.tasks import notify_subscribers_of_new_post
from tests.factories import EmailAccountFactory, UserFactory

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.blog_preferences]


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture(autouse=True)
def _default_email_account(_integration_django_site):
    """Create default EmailAccount for the queue_email path."""
    return EmailAccountFactory(default=True, site=_integration_django_site)


@pytest.fixture(autouse=True)
def _disable_sandbox_mode():
    with (
        patch("core.license.is_sandbox_mode", return_value=False),
        patch("email_system.services.email_sender.is_sandbox_mode", return_value=False),
        patch("core.sandbox.email_guard.is_sandbox_mode", return_value=False),
    ):
        yield


@pytest.fixture
def blog_category(db):
    """Test blog category."""
    return BlogCategory.objects.create(
        name="Test Category",
        slug="test-category",
        is_active=True,
    )


@pytest.fixture
def published_post(db, blog_category):
    """Published blog post using the correct ``simple_content`` field."""
    post = BlogPost.objects.create(
        title="Test Blog Post",
        slug="test-blog-post",
        simple_content="This is a test post.",
        status="published",
        category=blog_category,
    )
    return post


@pytest.fixture
def legacy_subscriber(db):
    """Legacy BlogSubscriber (not a registered user).

    Uses notification_frequency='immediate' and needs an unsubscribe_token.
    """
    return BlogSubscriber.objects.create(
        email="legacy@example.com",
        notification_frequency="immediate",
        verification_status="verified",
        unsubscribe_token=uuid.uuid4().hex,
    )


@pytest.fixture
def user_with_blog_preferences(db):
    """Registered user with blog preferences enabled + email verified."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_enabled = True
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.app_preferences["blog"]["enabled"] = True
    prefs.app_preferences["blog"]["frequency"] = "immediate"
    prefs.save()
    return user


# ============================================================
# Dual System Support
# ============================================================


def test_blog_notification_sent_to_legacy_subscriber(legacy_subscriber, published_post):
    """Blog notifications sent to legacy BlogSubscriber users."""
    with patch("email_system.services.email_sender.EmailSendingService.queue_email") as mock_send:
        notify_subscribers_of_new_post(published_post.pk)

        # Should send to legacy subscriber
        assert mock_send.called
        call_args_list = [call.kwargs for call in mock_send.call_args_list]
        emails_sent = [call["to_email"] for call in call_args_list]
        assert legacy_subscriber.email in emails_sent


def test_blog_notification_sent_to_new_system_user(user_with_blog_preferences, published_post):
    """Blog notifications sent to users with CommunicationPreference enabled."""
    with patch("email_system.services.email_sender.EmailSendingService.queue_email") as mock_send:
        notify_subscribers_of_new_post(published_post.pk)

        assert mock_send.called
        call_args_list = [call.kwargs for call in mock_send.call_args_list]
        emails_sent = [call["to_email"] for call in call_args_list]
        assert user_with_blog_preferences.email in emails_sent


def test_blog_notification_no_duplicates(legacy_subscriber, published_post):
    """Blog notifications don't send duplicates when email exists in both systems."""
    # Create a user with same email as legacy subscriber
    user = UserFactory(email=legacy_subscriber.email)
    prefs = user.communication_preferences
    prefs.email_enabled = True
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.app_preferences["blog"]["enabled"] = True
    prefs.app_preferences["blog"]["frequency"] = "immediate"
    prefs.save()

    with patch("email_system.services.email_sender.EmailSendingService.queue_email") as mock_send:
        notify_subscribers_of_new_post(published_post.pk)

        # BlogSubscriber takes precedence; the new-system loop excludes emails
        # already sent via the legacy path.
        call_args_list = [call.kwargs for call in mock_send.call_args_list]
        emails_sent = [call["to_email"] for call in call_args_list]
        email_count = emails_sent.count(legacy_subscriber.email)
        assert email_count == 1


def test_blog_notification_respects_new_system_disabled(published_post):
    """Blog notifications not sent when user disabled blog in CommunicationPreference."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.app_preferences["blog"]["enabled"] = False  # Disabled
    prefs.save()

    with patch("email_system.services.email_sender.EmailSendingService.queue_email") as mock_send:
        notify_subscribers_of_new_post(published_post.pk)

        # Should NOT send to this user
        call_args_list = [call.kwargs for call in mock_send.call_args_list]
        emails_sent = [call["to_email"] for call in call_args_list]
        assert user.email not in emails_sent


def test_blog_notification_respects_frequency_preference(
    user_with_blog_preferences, published_post
):
    """Blog notifications respect frequency setting.

    Only ``frequency='immediate'`` subscribers get notified for new-post
    events; weekly/monthly digests are handled by separate scheduled tasks.
    """
    # Set to weekly digest
    prefs = user_with_blog_preferences.communication_preferences
    prefs.app_preferences["blog"]["frequency"] = "weekly"
    prefs.save()

    with patch("email_system.services.email_sender.EmailSendingService.queue_email") as mock_send:
        notify_subscribers_of_new_post(published_post.pk)

        # Should NOT send immediately (queued for weekly digest)
        call_args_list = [call.kwargs for call in mock_send.call_args_list]
        emails_sent = [call["to_email"] for call in call_args_list]
        assert user_with_blog_preferences.email not in emails_sent


def test_blog_notification_respects_email_not_verified(published_post):
    """Blog notifications not sent when email_verified=False."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = False  # Not verified
    prefs.app_preferences["blog"]["enabled"] = True
    prefs.save()

    with patch("email_system.services.email_sender.EmailSendingService.queue_email") as mock_send:
        notify_subscribers_of_new_post(published_post.pk)

        # Should NOT send (not verified)
        call_args_list = [call.kwargs for call in mock_send.call_args_list]
        emails_sent = [call["to_email"] for call in call_args_list]
        assert user.email not in emails_sent


# ============================================================
# Category Preferences (legacy subscriber-side categories)
# ============================================================


def test_blog_notification_respects_category_preferences(
    legacy_subscriber, blog_category, published_post
):
    """Legacy subscribers with a matching category filter still receive."""
    legacy_subscriber.subscribed_categories.add(blog_category)

    with patch("email_system.services.email_sender.EmailSendingService.queue_email") as mock_send:
        notify_subscribers_of_new_post(published_post.pk)

        assert mock_send.called
        call_args_list = [call.kwargs for call in mock_send.call_args_list]
        emails_sent = [call["to_email"] for call in call_args_list]
        assert legacy_subscriber.email in emails_sent


def test_blog_notification_skips_unsubscribed_category(legacy_subscriber, published_post):
    """Legacy subscribers with a category filter that DOESN'T match are skipped."""
    # Create different category
    other_category = BlogCategory.objects.create(
        name="Other Category",
        slug="other-category",
        is_active=True,
    )
    legacy_subscriber.subscribed_categories.add(other_category)

    with patch("email_system.services.email_sender.EmailSendingService.queue_email") as mock_send:
        notify_subscribers_of_new_post(published_post.pk)

        # Should NOT send (post not in subscribed category)
        call_args_list = [call.kwargs for call in mock_send.call_args_list]
        emails_sent = [call["to_email"] for call in call_args_list]
        assert legacy_subscriber.email not in emails_sent


# ============================================================
# Email Template Type
# ============================================================


def test_blog_notification_uses_correct_message_type(user_with_blog_preferences, published_post):
    """Blog notifications use ``blog_post_published`` for preference checking."""
    with patch("email_system.services.email_sender.EmailSendingService.queue_email") as mock_send:
        notify_subscribers_of_new_post(published_post.pk)

        assert mock_send.called
        # Every call should carry template_type='blog_post_published'
        for call in mock_send.call_args_list:
            assert call.kwargs["template_type"] == "blog_post_published"


# ============================================================
# Legacy BlogSubscriber Compatibility
# ============================================================


def test_legacy_subscriber_frequency_immediate(legacy_subscriber, published_post):
    """Legacy BlogSubscriber with immediate frequency receives notifications."""
    with patch("email_system.services.email_sender.EmailSendingService.queue_email") as mock_send:
        notify_subscribers_of_new_post(published_post.pk)

        # Should send immediately
        assert mock_send.called


def test_legacy_subscriber_frequency_weekly_digest(published_post):
    """Legacy BlogSubscriber with weekly frequency skipped by the immediate
    notify task."""
    subscriber = BlogSubscriber.objects.create(
        email="weekly@example.com",
        notification_frequency="weekly",
        verification_status="verified",
        unsubscribe_token=uuid.uuid4().hex,
    )

    with patch("email_system.services.email_sender.EmailSendingService.queue_email") as mock_send:
        notify_subscribers_of_new_post(published_post.pk)

        # Should NOT send immediately (queued for digest)
        call_args_list = [call.kwargs for call in mock_send.call_args_list]
        emails_sent = [call["to_email"] for call in call_args_list]
        assert subscriber.email not in emails_sent


def test_legacy_subscriber_unverified_skipped(published_post):
    """Unverified legacy BlogSubscriber doesn't receive notifications."""
    subscriber = BlogSubscriber.objects.create(
        email="unverified@example.com",
        notification_frequency="immediate",
        verification_status="pending",  # Not verified
        unsubscribe_token=uuid.uuid4().hex,
    )

    with patch("email_system.services.email_sender.EmailSendingService.queue_email") as mock_send:
        notify_subscribers_of_new_post(published_post.pk)

        # Should NOT send (not verified)
        call_args_list = [call.kwargs for call in mock_send.call_args_list]
        emails_sent = [call["to_email"] for call in call_args_list]
        assert subscriber.email not in emails_sent


# ============================================================
# Edge Cases
# ============================================================


def test_blog_notification_no_subscribers(published_post):
    """Blog notification handles no subscribers gracefully."""
    with patch("email_system.services.email_sender.EmailSendingService.queue_email"):
        # Should not crash
        notify_subscribers_of_new_post(published_post.pk)


def test_blog_notification_both_systems_have_users(
    legacy_subscriber, user_with_blog_preferences, published_post
):
    """Blog notification sends to both legacy and new system users."""
    with patch("email_system.services.email_sender.EmailSendingService.queue_email") as mock_send:
        notify_subscribers_of_new_post(published_post.pk)

        # Should send to both
        assert mock_send.called
        call_args_list = [call.kwargs for call in mock_send.call_args_list]
        emails_sent = [call["to_email"] for call in call_args_list]

        assert legacy_subscriber.email in emails_sent
        assert user_with_blog_preferences.email in emails_sent
        # Total 2 emails
        assert len(emails_sent) == 2
