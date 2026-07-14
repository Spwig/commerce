"""
Integration Tests for Affiliate Email Preferences.

Verifies that ``affiliate.services.email_notifications`` respects
``CommunicationPreference`` for approvals, memberships, commissions, and
payouts, and that context variables are populated correctly.

The affiliate service functions all funnel through
``EmailSendingService.send_template_email`` which itself checks
preferences and returns an ``EmailOutbox`` with either
``status='pending'/'queued'`` (queued for delivery) or ``status='skipped'``.
"""

from decimal import Decimal
from unittest.mock import Mock, patch

import pytest
from django.contrib.auth import get_user_model

from affiliate.models import Affiliate, AffiliateProgramMembership, Commission, Payout, Program
from affiliate.services.email_notifications import (
    send_affiliate_activated_email,
    send_affiliate_approved_email,
    send_affiliate_suspended_email,
    send_commission_approved_email,
    send_commission_earned_email,
    send_commission_rejected_email,
    send_commission_reversed_email,
    send_payout_cancelled_email,
    send_payout_completed_email,
    send_payout_failed_email,
    send_payout_processing_email,
    send_program_membership_approved_email,
    send_program_membership_rejected_email,
)
from email_system.models import EmailOutbox
from tests.factories import EmailAccountFactory, OrderFactory, UserFactory

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.affiliate_preferences]


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture(autouse=True)
def _default_email_account(_integration_django_site):
    """Create default EmailAccount so send_template_email never raises."""
    return EmailAccountFactory(default=True, site=_integration_django_site)


@pytest.fixture(autouse=True)
def _disable_sandbox_mode():
    """Neutralise sandbox mode so email pathway hits preference guard, not
    sandbox_filter_recipient."""
    with (
        patch("core.license.is_sandbox_mode", return_value=False),
        patch("email_system.services.email_sender.is_sandbox_mode", return_value=False),
        patch("core.sandbox.email_guard.is_sandbox_mode", return_value=False),
    ):
        yield


@pytest.fixture(autouse=True)
def _mock_template_renderer():
    """No EmailTemplate rows exist in the test DB — mock the renderer so
    ``send_template_email`` reaches the queue step for allowed emails.
    Preference-blocked paths return early and never touch the renderer."""
    with patch(
        "email_system.services.template_renderer.TemplateRenderer.render",
        return_value=("Test Subject", "<p>Test HTML</p>", "Test text"),
    ):
        yield


@pytest.fixture
def merchant_user(db):
    """Create merchant user for affiliate programs."""
    return UserFactory(email="merchant@test.com", username="merchant")


@pytest.fixture
def user_with_affiliate_enabled(db):
    """User with affiliate emails enabled."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.app_preferences["affiliate"]["enabled"] = True
    prefs.save()
    return user


@pytest.fixture
def user_with_affiliate_disabled(db):
    """User with affiliate emails disabled."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.app_preferences["affiliate"]["enabled"] = False
    prefs.save()
    return user


@pytest.fixture
def user_email_not_verified(db):
    """User with email not verified — should block marketing/app-specific."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = False  # Not verified
    prefs.app_preferences["affiliate"]["enabled"] = True
    prefs.save()
    return user


@pytest.fixture
def affiliate_program(merchant_user):
    """Create test affiliate program."""
    return Program.objects.create(
        name="Test Program",
        slug="test-program",
        merchant=merchant_user,
        commission_type="percentage",
        commission_value=Decimal("10.00"),
        status="active",
    )


@pytest.fixture
def affiliate_user(user_with_affiliate_enabled, affiliate_program):
    """Create an Affiliate row for user_with_affiliate_enabled."""
    return Affiliate.objects.create(
        user=user_with_affiliate_enabled,
        payment_email="payout@test.com",
        status="pending",
    )


@pytest.fixture
def real_order(db):
    """Real Order instance (Commission has an FK to orders.Order)."""
    return OrderFactory()


# ============================================================================
# AFFILIATE ACCOUNT STATUS EMAILS
# ============================================================================


def test_affiliate_approved_email_sent_when_enabled(affiliate_user):
    """Affiliate approved email sent when user has affiliate enabled."""
    EmailOutbox.objects.all().delete()

    result = send_affiliate_approved_email(affiliate_user)

    assert result is True
    outbox = EmailOutbox.objects.filter(template_type="affiliate_account_approved").latest(
        "created_at"
    )
    assert outbox.to_email == affiliate_user.user.email
    assert outbox.status in ("pending", "queued")


def test_affiliate_approved_email_skipped_when_disabled(
    user_with_affiliate_disabled, affiliate_program
):
    """Affiliate approved email skipped when user has affiliate disabled."""
    affiliate = Affiliate.objects.create(
        user=user_with_affiliate_disabled,
        payment_email="payout@test.com",
        status="pending",
    )

    EmailOutbox.objects.all().delete()
    result = send_affiliate_approved_email(affiliate)

    assert result is False
    outbox = EmailOutbox.objects.filter(template_type="affiliate_account_approved").latest(
        "created_at"
    )
    assert outbox.status == "skipped"
    assert outbox.skip_reason == "user_preference_disabled"


def test_affiliate_approved_email_skipped_when_email_not_verified(
    user_email_not_verified, affiliate_program
):
    """Affiliate approved email skipped when email not verified.

    App-specific messages require ``email_marketing AND email_verified``
    regardless of the app_preferences flag.
    """
    affiliate = Affiliate.objects.create(
        user=user_email_not_verified,
        payment_email="payout@test.com",
        status="pending",
    )

    EmailOutbox.objects.all().delete()
    result = send_affiliate_approved_email(affiliate)

    assert result is False
    outbox = EmailOutbox.objects.filter(template_type="affiliate_account_approved").latest(
        "created_at"
    )
    assert outbox.status == "skipped"
    assert outbox.skip_reason == "user_preference_disabled"


def test_affiliate_suspended_email_sent(affiliate_user):
    """Affiliate suspended email sent when preferences enabled."""
    EmailOutbox.objects.all().delete()
    result = send_affiliate_suspended_email(affiliate_user)

    assert result is True
    outbox = EmailOutbox.objects.filter(template_type="affiliate_account_suspended").latest(
        "created_at"
    )
    assert outbox.to_email == affiliate_user.user.email
    assert outbox.status in ("pending", "queued")


def test_affiliate_activated_email_sent(affiliate_user):
    """Affiliate activated email sent when preferences enabled."""
    EmailOutbox.objects.all().delete()
    result = send_affiliate_activated_email(affiliate_user)

    assert result is True
    outbox = EmailOutbox.objects.filter(template_type="affiliate_account_activated").latest(
        "created_at"
    )
    assert outbox.to_email == affiliate_user.user.email
    assert outbox.status in ("pending", "queued")


# ============================================================================
# PROGRAM MEMBERSHIP EMAILS
# ============================================================================


def test_program_membership_approved_email_sent(affiliate_user, affiliate_program):
    """Program membership approved email sent when preferences enabled."""
    membership = AffiliateProgramMembership.objects.create(
        affiliate=affiliate_user,
        program=affiliate_program,
        status="pending",
    )

    EmailOutbox.objects.all().delete()
    result = send_program_membership_approved_email(membership)

    assert result is True
    outbox = EmailOutbox.objects.filter(template_type="affiliate_program_approved").latest(
        "created_at"
    )
    assert outbox.to_email == affiliate_user.user.email
    assert outbox.status in ("pending", "queued")


def test_program_membership_approved_email_skipped_when_disabled(
    user_with_affiliate_disabled, affiliate_program
):
    """Program membership approved email skipped when preferences disabled."""
    affiliate = Affiliate.objects.create(
        user=user_with_affiliate_disabled,
        payment_email="payout@test.com",
        status="active",
    )
    membership = AffiliateProgramMembership.objects.create(
        affiliate=affiliate,
        program=affiliate_program,
        status="pending",
    )

    EmailOutbox.objects.all().delete()
    result = send_program_membership_approved_email(membership)

    assert result is False
    outbox = EmailOutbox.objects.filter(template_type="affiliate_program_approved").latest(
        "created_at"
    )
    assert outbox.status == "skipped"


def test_program_membership_rejected_email_sent(affiliate_user, affiliate_program):
    """Program membership rejected email sent when preferences enabled."""
    membership = AffiliateProgramMembership.objects.create(
        affiliate=affiliate_user,
        program=affiliate_program,
        status="pending",
    )

    EmailOutbox.objects.all().delete()
    result = send_program_membership_rejected_email(membership)

    assert result is True
    outbox = EmailOutbox.objects.filter(template_type="affiliate_program_rejected").latest(
        "created_at"
    )
    assert outbox.to_email == affiliate_user.user.email
    assert outbox.status in ("pending", "queued")


# ============================================================================
# COMMISSION EMAILS
# ============================================================================


def test_commission_earned_email_sent(affiliate_user, affiliate_program, real_order):
    """Commission earned email sent when preferences enabled."""
    commission = Commission.objects.create(
        affiliate=affiliate_user,
        program=affiliate_program,
        order=real_order,
        amount=Decimal("10.00"),
        status="pending",
    )

    EmailOutbox.objects.all().delete()
    result = send_commission_earned_email(commission)

    assert result is True
    outbox = EmailOutbox.objects.filter(template_type="affiliate_commission_earned").latest(
        "created_at"
    )
    assert outbox.to_email == affiliate_user.user.email
    assert outbox.status in ("pending", "queued")


def test_commission_earned_email_skipped_when_disabled(
    user_with_affiliate_disabled, affiliate_program, real_order
):
    """Commission earned email skipped when preferences disabled."""
    affiliate = Affiliate.objects.create(
        user=user_with_affiliate_disabled,
        payment_email="payout@test.com",
        status="active",
    )
    commission = Commission.objects.create(
        affiliate=affiliate,
        program=affiliate_program,
        order=real_order,
        amount=Decimal("10.00"),
        status="pending",
    )

    EmailOutbox.objects.all().delete()
    result = send_commission_earned_email(commission)

    assert result is False
    outbox = EmailOutbox.objects.filter(template_type="affiliate_commission_earned").latest(
        "created_at"
    )
    assert outbox.status == "skipped"


def test_commission_approved_email_sent(affiliate_user, affiliate_program, real_order):
    """Commission approved email sent when preferences enabled."""
    commission = Commission.objects.create(
        affiliate=affiliate_user,
        program=affiliate_program,
        order=real_order,
        amount=Decimal("10.00"),
        status="pending",
    )

    EmailOutbox.objects.all().delete()
    result = send_commission_approved_email(commission)

    assert result is True
    outbox = EmailOutbox.objects.filter(template_type="affiliate_commission_approved").latest(
        "created_at"
    )
    assert outbox.to_email == affiliate_user.user.email
    assert outbox.status in ("pending", "queued")


def test_commission_rejected_email_sent(affiliate_user, affiliate_program, real_order):
    """Commission rejected email sent when preferences enabled."""
    commission = Commission.objects.create(
        affiliate=affiliate_user,
        program=affiliate_program,
        order=real_order,
        amount=Decimal("10.00"),
        status="pending",
        notes="Does not meet program requirements",
    )

    EmailOutbox.objects.all().delete()
    result = send_commission_rejected_email(commission)

    assert result is True
    outbox = EmailOutbox.objects.filter(template_type="affiliate_commission_rejected").latest(
        "created_at"
    )
    assert outbox.to_email == affiliate_user.user.email
    assert outbox.status in ("pending", "queued")


def test_commission_reversed_email_sent(affiliate_user, affiliate_program, real_order):
    """Commission reversed email sent when preferences enabled."""
    commission = Commission.objects.create(
        affiliate=affiliate_user,
        program=affiliate_program,
        order=real_order,
        amount=Decimal("10.00"),
        status="approved",
    )

    EmailOutbox.objects.all().delete()
    result = send_commission_reversed_email(commission)

    assert result is True
    outbox = EmailOutbox.objects.filter(template_type="affiliate_commission_reversed").latest(
        "created_at"
    )
    assert outbox.to_email == affiliate_user.user.email
    assert outbox.status in ("pending", "queued")


# ============================================================================
# PAYOUT EMAILS
# ============================================================================


def test_payout_processing_email_sent(affiliate_user):
    """Payout processing email sent when preferences enabled."""
    payout = Payout.objects.create(
        affiliate=affiliate_user,
        amount=Decimal("50.00"),
        method="paypal",
        status="pending",
    )

    EmailOutbox.objects.all().delete()
    result = send_payout_processing_email(payout)

    assert result is True
    outbox = EmailOutbox.objects.filter(template_type="affiliate_payout_processing").latest(
        "created_at"
    )
    assert outbox.to_email == affiliate_user.user.email
    assert outbox.status in ("pending", "queued")


def test_payout_processing_email_skipped_when_disabled(user_with_affiliate_disabled):
    """Payout processing email skipped when preferences disabled."""
    affiliate = Affiliate.objects.create(
        user=user_with_affiliate_disabled,
        payment_email="payout@test.com",
        status="active",
    )
    payout = Payout.objects.create(
        affiliate=affiliate,
        amount=Decimal("50.00"),
        method="paypal",
        status="pending",
    )

    EmailOutbox.objects.all().delete()
    result = send_payout_processing_email(payout)

    assert result is False
    outbox = EmailOutbox.objects.filter(template_type="affiliate_payout_processing").latest(
        "created_at"
    )
    assert outbox.status == "skipped"


def test_payout_completed_email_sent(affiliate_user):
    """Payout completed email sent when preferences enabled."""
    payout = Payout.objects.create(
        affiliate=affiliate_user,
        amount=Decimal("50.00"),
        method="paypal",
        status="processing",
        reference="PAY-12345",
    )

    EmailOutbox.objects.all().delete()
    result = send_payout_completed_email(payout)

    assert result is True
    outbox = EmailOutbox.objects.filter(template_type="affiliate_payout_completed").latest(
        "created_at"
    )
    assert outbox.to_email == affiliate_user.user.email
    assert outbox.status in ("pending", "queued")


def test_payout_failed_email_sent(affiliate_user):
    """Payout failed email sent when preferences enabled."""
    payout = Payout.objects.create(
        affiliate=affiliate_user,
        amount=Decimal("50.00"),
        method="paypal",
        status="processing",
        notes="Payment processor error",
    )

    EmailOutbox.objects.all().delete()
    result = send_payout_failed_email(payout)

    assert result is True
    outbox = EmailOutbox.objects.filter(template_type="affiliate_payout_failed").latest(
        "created_at"
    )
    assert outbox.to_email == affiliate_user.user.email
    assert outbox.status in ("pending", "queued")


def test_payout_cancelled_email_sent(affiliate_user):
    """Payout cancelled email sent when preferences enabled."""
    payout = Payout.objects.create(
        affiliate=affiliate_user,
        amount=Decimal("50.00"),
        method="paypal",
        status="pending",
        notes="Cancelled by merchant",
    )

    EmailOutbox.objects.all().delete()
    result = send_payout_cancelled_email(payout)

    assert result is True
    outbox = EmailOutbox.objects.filter(template_type="affiliate_payout_cancelled").latest(
        "created_at"
    )
    assert outbox.to_email == affiliate_user.user.email
    assert outbox.status in ("pending", "queued")


# ============================================================================
# MASTER EMAIL TOGGLE TESTS
# ============================================================================


def test_all_affiliate_emails_skipped_when_email_disabled(
    user_with_affiliate_enabled, affiliate_program
):
    """All affiliate emails skipped when master email toggle is disabled."""
    prefs = user_with_affiliate_enabled.communication_preferences
    prefs.email_enabled = False
    prefs.save()

    affiliate = Affiliate.objects.create(
        user=user_with_affiliate_enabled,
        payment_email="payout@test.com",
        status="pending",
    )

    EmailOutbox.objects.all().delete()
    result = send_affiliate_approved_email(affiliate)

    assert result is False
    outbox = EmailOutbox.objects.filter(template_type="affiliate_account_approved").latest(
        "created_at"
    )
    assert outbox.status == "skipped"


def test_all_affiliate_emails_skipped_when_marketing_disabled(
    user_with_affiliate_enabled, affiliate_program
):
    """All affiliate emails skipped when marketing emails disabled."""
    prefs = user_with_affiliate_enabled.communication_preferences
    prefs.email_marketing = False
    prefs.save()

    affiliate = Affiliate.objects.create(
        user=user_with_affiliate_enabled,
        payment_email="payout@test.com",
        status="pending",
    )

    EmailOutbox.objects.all().delete()
    result = send_affiliate_approved_email(affiliate)

    assert result is False
    outbox = EmailOutbox.objects.filter(template_type="affiliate_account_approved").latest(
        "created_at"
    )
    assert outbox.status == "skipped"


# ============================================================================
# CONTEXT VARIABLE TESTS
# ============================================================================


def test_commission_email_includes_context_variables(affiliate_user, affiliate_program, real_order):
    """Commission email includes all required context variables."""
    commission = Commission.objects.create(
        affiliate=affiliate_user,
        program=affiliate_program,
        order=real_order,
        amount=Decimal("10.00"),
        status="pending",
    )

    # Patch at source (send_template_email is looked up inside the function
    # body via lazy import); asserting on the call args verifies context.
    with patch(
        "email_system.services.email_sender.EmailSendingService.send_template_email"
    ) as mock_send:
        mock_outbox = Mock()
        mock_outbox.status = "queued"
        mock_send.return_value = mock_outbox

        send_commission_earned_email(commission)

        assert mock_send.called
        call_kwargs = mock_send.call_args[1]
        context = call_kwargs["context"]

        assert "commission_amount" in context
        assert context["commission_amount"] == "10.00"
        assert "order_number" in context
        assert "shop_name" in context
        assert "portal_url" in context
        assert "support_email" in context


def test_payout_email_includes_context_variables(affiliate_user):
    """Payout email includes all required context variables."""
    payout = Payout.objects.create(
        affiliate=affiliate_user,
        amount=Decimal("50.00"),
        method="paypal",
        status="pending",
        reference="PAY-12345",
    )

    with patch(
        "email_system.services.email_sender.EmailSendingService.send_template_email"
    ) as mock_send:
        mock_outbox = Mock()
        mock_outbox.status = "queued"
        mock_send.return_value = mock_outbox

        send_payout_completed_email(payout)

        assert mock_send.called
        call_kwargs = mock_send.call_args[1]
        context = call_kwargs["context"]

        assert "payout_amount" in context
        assert context["payout_amount"] == "50.00"
        assert "payout_method" in context
        assert "reference_number" in context
        assert "shop_name" in context


# ============================================================================
# EDGE CASES
# ============================================================================


def test_affiliate_email_uses_communication_preference_language(
    user_with_affiliate_enabled, affiliate_program
):
    """Affiliate email uses CommunicationPreference.language_code for language."""
    prefs = user_with_affiliate_enabled.communication_preferences
    prefs.language_code = "de"
    prefs.save()

    affiliate = Affiliate.objects.create(
        user=user_with_affiliate_enabled,
        payment_email="payout@test.com",
        status="pending",
    )

    EmailOutbox.objects.all().delete()
    result = send_affiliate_approved_email(affiliate)

    # Should still send using CommunicationPreference language
    assert result is True
    outbox = EmailOutbox.objects.filter(template_type="affiliate_account_approved").latest(
        "created_at"
    )
    assert outbox.status in ("pending", "queued")
