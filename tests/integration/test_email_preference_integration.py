"""
Email System Preference Integration Tests.

Tests email sending with preference checking, unsubscribe footer injection,
and skipped status tracking.
"""
import pytest
from django.contrib.auth import get_user_model
from django.core import mail

from accounts.models import CommunicationPreference
from email_system.models import EmailOutbox
from email_system.services.email_sender import EmailSendingService
from tests.factories import UserFactory

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.email_preferences]


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def email_service():
    """Email sending service instance."""
    return EmailSendingService()


@pytest.fixture
def user_with_verified_email(db):
    """User with verified email and marketing opt-in."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.save()
    return user


@pytest.fixture
def user_without_marketing(db):
    """User who opted out of marketing emails."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = False
    prefs.save()
    return user


# ============================================================
# queue_email with Preference Checking
# ============================================================

def test_queue_email_transactional_always_sent(db, email_service, user_without_marketing):
    """Transactional emails are sent regardless of marketing preferences."""
    result = email_service.queue_email(
        to_email=user_without_marketing.email,
        subject='Your Order Confirmation',
        body='Your order has been confirmed.',
        template_type='order_confirmation',
    )

    assert result['success'] is True
    assert 'outbox_id' in result

    # Check outbox entry
    outbox = EmailOutbox.objects.get(pk=result['outbox_id'])
    assert outbox.status == 'pending'
    assert outbox.to_email == user_without_marketing.email


def test_queue_email_marketing_skipped_when_disabled(db, email_service, user_without_marketing):
    """Marketing emails are skipped when user has marketing disabled."""
    result = email_service.queue_email(
        to_email=user_without_marketing.email,
        subject='Our Newsletter',
        body='Check out our latest products!',
        template_type='newsletter',
    )

    assert result['success'] is False
    assert result.get('skipped') is True
    assert result.get('reason') == 'user_preference_disabled'

    # Check outbox entry has skipped status
    outbox = EmailOutbox.objects.get(pk=result['outbox_id'])
    assert outbox.status == 'skipped'
    assert outbox.skip_reason == 'user_preference_disabled'


def test_queue_email_marketing_sent_when_verified(db, email_service, user_with_verified_email):
    """Marketing emails sent when user is verified and opted in."""
    result = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject='Our Newsletter',
        body='Check out our latest products!',
        template_type='newsletter',
    )

    assert result['success'] is True

    outbox = EmailOutbox.objects.get(pk=result['outbox_id'])
    assert outbox.status == 'pending'


def test_queue_email_marketing_skipped_when_not_verified(db, email_service):
    """Marketing emails skipped when user opted in but not verified."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = True  # Opted in
    prefs.email_verified = False  # But not verified
    prefs.save()

    result = email_service.queue_email(
        to_email=user.email,
        subject='Our Newsletter',
        body='Newsletter content',
        template_type='newsletter',
    )

    assert result['success'] is False
    assert result.get('skipped') is True

    outbox = EmailOutbox.objects.get(pk=result['outbox_id'])
    assert outbox.status == 'skipped'


def test_queue_email_guest_user_sent_normally(db, email_service):
    """Emails to non-registered users (guests) are sent normally."""
    guest_email = 'guest@example.com'

    # Guest doesn't exist in User table
    assert not User.objects.filter(email=guest_email).exists()

    result = email_service.queue_email(
        to_email=guest_email,
        subject='Your Order Confirmation',
        body='Thank you for your order!',
        template_type='order_confirmation',
    )

    # Should send successfully
    assert result['success'] is True

    outbox = EmailOutbox.objects.get(pk=result['outbox_id'])
    assert outbox.status == 'pending'


# ============================================================
# send_template_email with Preferences
# ============================================================

def test_send_template_email_respects_preferences(db, email_service, user_without_marketing):
    """send_template_email checks preferences based on template_type."""
    result = email_service.send_template_email(
        to_email=user_without_marketing.email,
        template_type='newsletter',
        context={'name': 'Test User'},
    )

    assert result['success'] is False
    assert result.get('skipped') is True


def test_send_template_email_app_specific_preference(db, email_service, user_with_verified_email):
    """send_template_email checks app-specific preferences."""
    # Disable blog emails
    prefs = user_with_verified_email.communication_preferences
    prefs.app_preferences['blog']['enabled'] = False
    prefs.save()

    result = email_service.send_template_email(
        to_email=user_with_verified_email.email,
        template_type='blog_post_published',
        context={'post_title': 'New Post'},
    )

    assert result['success'] is False
    assert result.get('skipped') is True

    outbox = EmailOutbox.objects.get(pk=result['outbox_id'])
    assert outbox.status == 'skipped'


# ============================================================
# Unsubscribe Footer Injection
# ============================================================

def test_unsubscribe_footer_injected_in_html(db, email_service, user_with_verified_email):
    """Unsubscribe link is injected into HTML marketing emails."""
    result = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject='Our Newsletter',
        body='<html><body><p>Newsletter content</p></body></html>',
        template_type='newsletter',
    )

    outbox = EmailOutbox.objects.get(pk=result['outbox_id'])

    # Check unsubscribe link in body
    assert 'unsubscribe' in outbox.body.lower()
    assert user_with_verified_email.communication_preferences.unsubscribe_token in outbox.body


def test_unsubscribe_footer_injected_in_text(db, email_service, user_with_verified_email):
    """Unsubscribe link is injected into plain text marketing emails."""
    result = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject='Our Newsletter',
        body='Newsletter content in plain text.',
        template_type='newsletter',
    )

    outbox = EmailOutbox.objects.get(pk=result['outbox_id'])

    # Check unsubscribe link in body
    assert 'unsubscribe' in outbox.body.lower()
    assert '/accounts/unsubscribe/' in outbox.body
    assert user_with_verified_email.communication_preferences.unsubscribe_token in outbox.body


def test_unsubscribe_footer_not_in_transactional(db, email_service, user_with_verified_email):
    """Unsubscribe footer is NOT added to transactional emails."""
    result = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject='Order Confirmation',
        body='<html><body><p>Your order is confirmed.</p></body></html>',
        template_type='order_confirmation',
    )

    outbox = EmailOutbox.objects.get(pk=result['outbox_id'])

    # Should NOT contain unsubscribe link
    assert 'unsubscribe' not in outbox.body.lower()


def test_unsubscribe_footer_not_added_twice(db, email_service, user_with_verified_email):
    """Unsubscribe footer is not duplicated if already present."""
    existing_footer = f'<p><a href="/accounts/unsubscribe/{user_with_verified_email.communication_preferences.unsubscribe_token}/">Unsubscribe</a></p>'
    body = f'<html><body><p>Content</p>{existing_footer}</body></html>'

    result = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject='Newsletter',
        body=body,
        template_type='newsletter',
    )

    outbox = EmailOutbox.objects.get(pk=result['outbox_id'])

    # Count occurrences of unsubscribe link (should be 1, not 2)
    assert outbox.body.count('/accounts/unsubscribe/') == 1


# ============================================================
# EmailOutbox Status Tracking
# ============================================================

def test_skipped_status_recorded_in_outbox(db, email_service, user_without_marketing):
    """Skipped emails are tracked in EmailOutbox with status='skipped'."""
    result = email_service.queue_email(
        to_email=user_without_marketing.email,
        subject='Marketing Email',
        body='Content',
        template_type='promotional_offers',
    )

    assert result['success'] is False

    # Check outbox entry
    outbox = EmailOutbox.objects.get(pk=result['outbox_id'])
    assert outbox.status == 'skipped'
    assert outbox.skip_reason == 'user_preference_disabled'
    assert outbox.to_email == user_without_marketing.email


def test_skipped_emails_not_sent_to_provider(db, email_service, user_without_marketing):
    """Skipped emails are not sent to email provider."""
    result = email_service.queue_email(
        to_email=user_without_marketing.email,
        subject='Marketing Email',
        body='Content',
        template_type='newsletter',
    )

    # No emails should be in Django's mail outbox (test backend)
    assert len(mail.outbox) == 0


# ============================================================
# App-Specific Email Preferences
# ============================================================

def test_loyalty_email_respects_app_preference(db, email_service, user_with_verified_email):
    """Loyalty emails check app_preferences['loyalty']."""
    # Disable loyalty emails
    prefs = user_with_verified_email.communication_preferences
    prefs.app_preferences['loyalty']['enabled'] = False
    prefs.save()

    result = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject='Points Earned',
        body='You earned 100 points!',
        template_type='loyalty_points_earned',
    )

    assert result['success'] is False
    assert result.get('skipped') is True


def test_loyalty_specific_event_disabled(db, email_service, user_with_verified_email):
    """Loyalty emails respect event-level preferences."""
    # Loyalty enabled, but specific event disabled
    prefs = user_with_verified_email.communication_preferences
    prefs.app_preferences['loyalty']['enabled'] = True
    prefs.app_preferences['loyalty']['campaign_offers'] = False
    prefs.save()

    # Campaign offer should be skipped
    result = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject='Campaign Offer',
        body='Special offer just for you!',
        template_type='loyalty_campaign_offer',
    )

    assert result['success'] is False
    assert result.get('skipped') is True

    # But points earned should work
    result2 = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject='Points Earned',
        body='You earned points!',
        template_type='loyalty_points_earned',
    )

    assert result2['success'] is True


def test_referrals_email_respects_app_preference(db, email_service, user_with_verified_email):
    """Referral emails check app_preferences['referrals']."""
    # Disable referrals
    prefs = user_with_verified_email.communication_preferences
    prefs.app_preferences['referrals']['enabled'] = False
    prefs.save()

    result = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject='Referral Reward',
        body='You earned a referral reward!',
        template_type='referral_reward_issued',
    )

    assert result['success'] is False
    assert result.get('skipped') is True


def test_affiliate_email_respects_app_preference(db, email_service, user_with_verified_email):
    """Affiliate emails check app_preferences['affiliate']."""
    # Disable affiliate
    prefs = user_with_verified_email.communication_preferences
    prefs.app_preferences['affiliate']['enabled'] = False
    prefs.save()

    result = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject='Commission Earned',
        body='You earned commission!',
        template_type='affiliate_commission_earned',
    )

    assert result['success'] is False
    assert result.get('skipped') is True


# ============================================================
# Edge Cases
# ============================================================

def test_email_without_template_type_sent_normally(db, email_service, user_without_marketing):
    """Emails without template_type bypass preference checking."""
    result = email_service.queue_email(
        to_email=user_without_marketing.email,
        subject='Generic Email',
        body='This is a generic email.',
        # No template_type specified
    )

    # Should be sent even though user has marketing disabled
    assert result['success'] is True

    outbox = EmailOutbox.objects.get(pk=result['outbox_id'])
    assert outbox.status == 'pending'


def test_master_email_toggle_blocks_marketing(db, email_service, user_with_verified_email):
    """email_enabled=False blocks marketing emails."""
    prefs = user_with_verified_email.communication_preferences
    prefs.email_enabled = False
    prefs.save()

    result = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject='Newsletter',
        body='Content',
        template_type='newsletter',
    )

    assert result['success'] is False
    assert result.get('skipped') is True


def test_master_email_toggle_allows_critical_transactional(db, email_service, user_with_verified_email):
    """email_enabled=False still allows critical transactional emails."""
    prefs = user_with_verified_email.communication_preferences
    prefs.email_enabled = False
    prefs.save()

    # Critical transactional should still work
    result = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject='Order Confirmation',
        body='Your order is confirmed.',
        template_type='order_confirmation',
    )

    assert result['success'] is True
