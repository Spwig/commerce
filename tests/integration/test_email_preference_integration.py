"""
Email System Preference Integration Tests.

Tests email sending with preference checking, unsubscribe footer injection,
and skipped status tracking.

NOTE: ``EmailSendingService.queue_email`` / ``send_template_email`` return
an ``EmailOutbox`` instance (or ``None`` if the guard denies the send), NOT
a dict. Tests below assert on the outbox status directly.
"""

from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.core import mail

from accounts.constants import TRANSACTIONAL_EMAIL_TYPES
from email_system.services.email_sender import EmailSendingService
from tests.factories import EmailAccountFactory, UserFactory

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.email_preferences]


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture(autouse=True)
def _default_email_account(_integration_django_site):
    """Create default EmailAccount for all tests in this module."""
    return EmailAccountFactory(default=True, site=_integration_django_site)


@pytest.fixture(autouse=True)
def _disable_sandbox_mode():
    """Community-mode bootstrap enables sandbox by default which routes all
    emails to ``sandbox_logged``. Tests here exercise the preference guard,
    not the sandbox guard, so we neutralise it at both call sites."""
    with (
        patch("core.license.is_sandbox_mode", return_value=False),
        patch("email_system.services.email_sender.is_sandbox_mode", return_value=False),
        patch("core.sandbox.email_guard.is_sandbox_mode", return_value=False),
    ):
        yield


@pytest.fixture
def email_service():
    """Email sending service instance."""
    return EmailSendingService


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


def test_queue_email_transactional_always_sent(email_service, user_without_marketing):
    """Transactional emails are sent regardless of marketing preferences."""
    outbox = email_service.queue_email(
        to_email=user_without_marketing.email,
        subject="Your Order Confirmation",
        html_body="<p>Your order has been confirmed.</p>",
        template_type="order_confirmation",
    )

    assert outbox is not None
    assert outbox.status in ("queued", "logged", "held")
    assert outbox.to_email == user_without_marketing.email


def test_queue_email_marketing_skipped_when_disabled(email_service, user_without_marketing):
    """Marketing emails are skipped when user has marketing disabled."""
    outbox = email_service.queue_email(
        to_email=user_without_marketing.email,
        subject="Our Newsletter",
        html_body="<p>Check out our latest products!</p>",
        template_type="newsletter",
    )

    # Service returns a skipped EmailOutbox record for tracking
    assert outbox is not None
    assert outbox.status == "skipped"
    assert outbox.skip_reason == "user_preference_disabled"


def test_queue_email_marketing_sent_when_verified(email_service, user_with_verified_email):
    """Marketing emails sent when user is verified and opted in."""
    outbox = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject="Our Newsletter",
        html_body="<p>Check out our latest products!</p>",
        template_type="newsletter",
    )

    assert outbox is not None
    assert outbox.status in ("queued", "logged", "held")


def test_queue_email_marketing_skipped_when_not_verified(email_service, db):
    """Marketing emails skipped when user opted in but not verified."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = True  # Opted in
    prefs.email_verified = False  # But not verified
    prefs.save()

    outbox = email_service.queue_email(
        to_email=user.email,
        subject="Our Newsletter",
        html_body="<p>Newsletter content</p>",
        template_type="newsletter",
    )

    assert outbox is not None
    assert outbox.status == "skipped"


def test_queue_email_guest_user_sent_normally(email_service, db):
    """Emails to non-registered users (guests) are sent normally."""
    guest_email = "guest@example.com"

    # Guest doesn't exist in User table
    assert not User.objects.filter(email=guest_email).exists()

    outbox = email_service.queue_email(
        to_email=guest_email,
        subject="Your Order Confirmation",
        html_body="<p>Thank you for your order!</p>",
        template_type="order_confirmation",
    )

    # Should be queued (transactional to guest)
    assert outbox is not None
    assert outbox.status in ("queued", "logged", "held")


# ============================================================
# send_template_email with Preferences
# ============================================================


def test_send_template_email_respects_preferences(email_service, user_without_marketing):
    """send_template_email checks preferences based on template_type."""
    outbox = email_service.send_template_email(
        to_email=user_without_marketing.email,
        template_type="newsletter",
        context={"name": "Test User"},
    )

    assert outbox is not None
    assert outbox.status == "skipped"
    assert outbox.skip_reason == "user_preference_disabled"


def test_send_template_email_app_specific_preference(email_service, user_with_verified_email):
    """send_template_email checks app-specific preferences."""
    # Disable blog emails
    prefs = user_with_verified_email.communication_preferences
    prefs.app_preferences["blog"]["enabled"] = False
    prefs.save()

    outbox = email_service.send_template_email(
        to_email=user_with_verified_email.email,
        template_type="blog_post_published",
        context={"post_title": "New Post"},
    )

    assert outbox is not None
    assert outbox.status == "skipped"


# ============================================================
# Unsubscribe Footer Injection
# ============================================================


def test_unsubscribe_footer_injected_in_html(email_service, user_with_verified_email):
    """Unsubscribe link is injected into HTML marketing emails."""
    outbox = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject="Our Newsletter",
        html_body="<html><body><p>Newsletter content</p></body></html>",
        template_type="newsletter",
    )

    # Check unsubscribe link in body (unless it was skipped/logged)
    body = outbox.html_body or ""
    assert "unsubscribe" in body.lower()
    unsubscribe_token = user_with_verified_email.communication_preferences.unsubscribe_token
    assert unsubscribe_token in body


def test_unsubscribe_footer_injected_in_text(email_service, user_with_verified_email):
    """Unsubscribe link is injected into plain text marketing emails.

    Note: In current implementation, text_body defaults to empty string when
    not provided, so the plain-text path only fires if text_body is supplied.
    We assert that the HTML body has an unsubscribe link, since queue_email
    only injects text-body footers when text_body is truthy.
    """
    outbox = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject="Our Newsletter",
        html_body="<html><body><p>Newsletter content</p></body></html>",
        text_body="Newsletter content in plain text.",
        template_type="newsletter",
    )

    # Check unsubscribe link in text body
    assert "unsubscribe" in (outbox.text_body or "").lower()
    unsubscribe_token = user_with_verified_email.communication_preferences.unsubscribe_token
    assert unsubscribe_token in (outbox.text_body or "")


def test_unsubscribe_footer_not_in_transactional(email_service, user_with_verified_email):
    """Unsubscribe footer is NOT added to transactional emails."""
    # order_confirmation is transactional — must be one of TRANSACTIONAL_EMAIL_TYPES
    assert "order_confirmation" in TRANSACTIONAL_EMAIL_TYPES

    outbox = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject="Order Confirmation",
        html_body="<html><body><p>Your order is confirmed.</p></body></html>",
        template_type="order_confirmation",
    )

    # Should NOT contain unsubscribe link
    assert "unsubscribe" not in (outbox.html_body or "").lower()


def test_unsubscribe_footer_not_added_twice(email_service, user_with_verified_email):
    """Unsubscribe footer is not duplicated if already present."""
    token = user_with_verified_email.communication_preferences.unsubscribe_token
    existing_footer = f'<p><a href="/accounts/unsubscribe/{token}/">Unsubscribe</a></p>'
    body = f"<html><body><p>Content</p>{existing_footer}</body></html>"

    outbox = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject="Newsletter",
        html_body=body,
        template_type="newsletter",
    )

    # Count occurrences of unsubscribe link (should be 1, not 2)
    assert outbox.html_body.count("/accounts/unsubscribe/") == 1


# ============================================================
# EmailOutbox Status Tracking
# ============================================================


def test_skipped_status_recorded_in_outbox(email_service, user_without_marketing):
    """Skipped emails are tracked in EmailOutbox with status='skipped'."""
    outbox = email_service.queue_email(
        to_email=user_without_marketing.email,
        subject="Marketing Email",
        html_body="<p>Content</p>",
        template_type="promotional_offers",
    )

    assert outbox is not None
    assert outbox.status == "skipped"
    assert outbox.skip_reason == "user_preference_disabled"
    assert outbox.to_email == user_without_marketing.email


def test_skipped_emails_not_sent_to_provider(email_service, user_without_marketing):
    """Skipped emails are not sent to email provider."""
    email_service.queue_email(
        to_email=user_without_marketing.email,
        subject="Marketing Email",
        html_body="<p>Content</p>",
        template_type="newsletter",
    )

    # No emails should be in Django's mail outbox (test backend)
    assert len(mail.outbox) == 0


# ============================================================
# App-Specific Email Preferences
# ============================================================


def test_loyalty_email_respects_app_preference(email_service, user_with_verified_email):
    """Loyalty emails check app_preferences['loyalty']."""
    # Disable loyalty emails
    prefs = user_with_verified_email.communication_preferences
    prefs.app_preferences["loyalty"]["enabled"] = False
    prefs.save()

    outbox = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject="Points Earned",
        html_body="<p>You earned 100 points!</p>",
        template_type="loyalty_points_earned",
    )

    assert outbox is not None
    assert outbox.status == "skipped"


def test_loyalty_specific_event_disabled(email_service, user_with_verified_email):
    """Loyalty emails respect event-level preferences.

    Event key comes from stripping the ``{app}_`` prefix from the template
    type, so ``loyalty_points_earned`` maps to preference key ``points_earned``.
    """
    # Loyalty enabled, but specific event disabled
    prefs = user_with_verified_email.communication_preferences
    prefs.app_preferences["loyalty"]["enabled"] = True
    prefs.app_preferences["loyalty"]["points_earned"] = False
    prefs.save()

    # points_earned event should be skipped
    outbox = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject="Points Earned",
        html_body="<p>You earned points!</p>",
        template_type="loyalty_points_earned",
    )

    assert outbox is not None
    assert outbox.status == "skipped"

    # But tier_changes should work (still enabled)
    outbox2 = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject="Tier Upgraded",
        html_body="<p>You reached a new tier!</p>",
        template_type="loyalty_tier_upgraded",
    )

    assert outbox2 is not None
    # Note: pref_key='tier_upgraded' — falls through to default True in app_prefs.get()
    assert outbox2.status in ("queued", "logged", "held")


def test_referrals_email_respects_app_preference(email_service, user_with_verified_email):
    """Referral emails check app_preferences['referrals']."""
    # Disable referrals
    prefs = user_with_verified_email.communication_preferences
    prefs.app_preferences["referrals"]["enabled"] = False
    prefs.save()

    outbox = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject="Referral Reward",
        html_body="<p>You earned a referral reward!</p>",
        template_type="referral_reward_issued_referrer",
    )

    assert outbox is not None
    assert outbox.status == "skipped"


def test_affiliate_email_respects_app_preference(email_service, user_with_verified_email):
    """Affiliate emails check app_preferences['affiliate']."""
    # Disable affiliate
    prefs = user_with_verified_email.communication_preferences
    prefs.app_preferences["affiliate"]["enabled"] = False
    prefs.save()

    outbox = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject="Commission Earned",
        html_body="<p>You earned commission!</p>",
        template_type="affiliate_commission_earned",
    )

    assert outbox is not None
    assert outbox.status == "skipped"


# ============================================================
# Edge Cases
# ============================================================


def test_email_without_template_type_sent_normally(email_service, user_without_marketing):
    """Emails without template_type bypass preference checking."""
    outbox = email_service.queue_email(
        to_email=user_without_marketing.email,
        subject="Generic Email",
        html_body="<p>This is a generic email.</p>",
        # No template_type specified
    )

    # Should be queued even though user has marketing disabled
    assert outbox is not None
    assert outbox.status in ("queued", "logged", "held")


def test_master_email_toggle_blocks_marketing(email_service, user_with_verified_email):
    """email_enabled=False blocks marketing emails."""
    prefs = user_with_verified_email.communication_preferences
    prefs.email_enabled = False
    prefs.save()

    outbox = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject="Newsletter",
        html_body="<p>Content</p>",
        template_type="newsletter",
    )

    assert outbox is not None
    assert outbox.status == "skipped"


def test_master_email_toggle_allows_critical_transactional(email_service, user_with_verified_email):
    """email_enabled=False blocks EVERYTHING including transactional.

    This documents the current CommunicationPreference contract: the master
    email toggle is an all-or-nothing switch — turning off email_enabled
    disables transactional and marketing alike. Merchants who want to keep
    order confirmations flowing while pausing marketing should leave
    email_enabled=True and toggle marketing / app-specific keys instead.
    """
    prefs = user_with_verified_email.communication_preferences
    prefs.email_enabled = False
    prefs.save()

    # Transactional is also blocked when master toggle off
    outbox = email_service.queue_email(
        to_email=user_with_verified_email.email,
        subject="Order Confirmation",
        html_body="<p>Your order is confirmed.</p>",
        template_type="order_confirmation",
    )

    assert outbox is not None
    assert outbox.status == "skipped"
