"""
Integration tests for Affiliate Monthly Reports.

Verifies the ``AffiliateReportSettings`` singleton model and the
``send_affiliate_monthly_reports`` Celery task. The task is guarded by day
+ hour toggles and consults per-user CommunicationPreference before firing
each email.

The task imports ``EmailSendingService`` lazily inside the function body
(``from email_system.services.email_sender import EmailSendingService``),
so ``@patch("affiliate.tasks.EmailSendingService...")`` will always raise
``AttributeError``. We patch at source:
``email_system.services.email_sender.EmailSendingService.send_template_email``.
"""

from datetime import timedelta
from decimal import Decimal
from unittest.mock import Mock, patch

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from accounts.models import CommunicationPreference
from affiliate.models import Affiliate, AffiliateReportSettings, Commission, Payout, Program
from affiliate.tasks import send_affiliate_monthly_reports
from tests.factories import EmailAccountFactory, OrderFactory, UserFactory

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.affiliate_reports]


# Patch path constant — task imports EmailSendingService lazily inside the
# function body, so we patch at the source module.
_SEND_TEMPLATE_PATH = "email_system.services.email_sender.EmailSendingService.send_template_email"


# ============================================================
# Autouse infrastructure fixtures
# ============================================================


@pytest.fixture(autouse=True)
def _default_email_account(_integration_django_site):
    return EmailAccountFactory(default=True, site=_integration_django_site)


@pytest.fixture(autouse=True)
def _disable_sandbox_mode():
    with (
        patch("core.license.is_sandbox_mode", return_value=False),
        patch("email_system.services.email_sender.is_sandbox_mode", return_value=False),
        patch("core.sandbox.email_guard.is_sandbox_mode", return_value=False),
    ):
        yield


# ============================================================
# Data fixtures
# ============================================================


@pytest.fixture
def affiliate_with_commissions(db):
    """Create affiliate with 5 commissions in the previous month."""
    user = UserFactory()

    # Create affiliate
    affiliate = Affiliate.objects.create(user=user, status="active")

    # Create program
    program = Program.objects.create(
        name="Test Program",
        slug="test-program",
        merchant=UserFactory(),
        commission_type="percentage",
        commission_value=Decimal("10.00"),
    )

    # Create commissions from last month
    last_month_start = (timezone.now().replace(day=1) - timedelta(days=1)).replace(day=1)

    for i in range(5):
        order = OrderFactory(user=UserFactory(), status="delivered")

        commission = Commission.objects.create(
            affiliate=affiliate,
            program=program,
            order=order,
            amount=Decimal("10.00"),
            status="approved",
        )
        # Bypass auto_now via .update() so we can plant a last-month timestamp
        Commission.objects.filter(pk=commission.pk).update(
            created_at=last_month_start + timedelta(days=i)
        )

    # Enable monthly reports in preferences
    prefs, _ = CommunicationPreference.get_or_create_for_user(user)
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.app_preferences["affiliate"]["enabled"] = True
    prefs.app_preferences["affiliate"]["monthly_report"] = True
    prefs.save()

    return affiliate


# =============================================================================
# AffiliateReportSettings Model Tests
# =============================================================================


def test_affiliate_report_settings_singleton():
    """AffiliateReportSettings is a singleton (pk=1)."""
    settings1 = AffiliateReportSettings.get_settings()
    settings2 = AffiliateReportSettings.get_settings()

    assert settings1.pk == 1
    assert settings1.pk == settings2.pk


def test_affiliate_report_settings_defaults():
    """AffiliateReportSettings has correct defaults."""
    settings = AffiliateReportSettings.get_settings()

    assert settings.monthly_report_enabled is True
    assert settings.monthly_report_day == 1
    assert settings.monthly_report_hour == 9
    assert settings.include_top_orders_count == 5


def test_affiliate_report_settings_str():
    """AffiliateReportSettings string representation is human-readable."""
    settings = AffiliateReportSettings.get_settings()
    str_repr = str(settings)

    assert "Affiliate Report Settings" in str_repr
    assert "Enabled" in str_repr


def test_affiliate_report_settings_update():
    """Updating AffiliateReportSettings persists."""
    settings = AffiliateReportSettings.get_settings()

    settings.monthly_report_day = 15
    settings.monthly_report_hour = 14
    settings.include_top_orders_count = 10
    settings.save()

    # Get again - should have updated values
    updated = AffiliateReportSettings.get_settings()

    assert updated.monthly_report_day == 15
    assert updated.monthly_report_hour == 14
    assert updated.include_top_orders_count == 10


# =============================================================================
# Monthly Report Task Tests
# =============================================================================


@patch(_SEND_TEMPLATE_PATH)
def test_send_affiliate_monthly_reports_disabled(mock_send, db):
    """Task short-circuits when reports are disabled."""
    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_enabled = False
    settings.save()

    result = send_affiliate_monthly_reports()

    assert result["reason"] == "disabled"
    assert result["sent"] == 0
    assert mock_send.call_count == 0


@patch(_SEND_TEMPLATE_PATH)
def test_send_affiliate_monthly_reports_wrong_day(mock_send, db):
    """Task skips when not on configured send day."""
    settings = AffiliateReportSettings.get_settings()
    today = timezone.now().day

    # Set to different day
    settings.monthly_report_day = (today % 28) + 1  # Different day
    settings.save()

    result = send_affiliate_monthly_reports()

    assert result["reason"] == "not_send_day"
    assert result["sent"] == 0
    assert mock_send.call_count == 0


@patch(_SEND_TEMPLATE_PATH)
def test_send_affiliate_monthly_reports_wrong_hour(mock_send, db):
    """Task skips when not on configured send hour."""
    settings = AffiliateReportSettings.get_settings()
    current_hour = timezone.now().hour

    # Set to different hour
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = (current_hour + 1) % 24  # Different hour
    settings.save()

    result = send_affiliate_monthly_reports()

    assert result["reason"] == "not_send_hour"
    assert mock_send.call_count == 0


@patch(_SEND_TEMPLATE_PATH)
def test_send_affiliate_monthly_reports_success(mock_send, affiliate_with_commissions):
    """Task sends reports on correct day/hour."""
    # Configure to current day/hour
    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.save()

    # Mock successful email send
    mock_outbox = Mock()
    mock_outbox.status = "queued"
    mock_send.return_value = mock_outbox

    result = send_affiliate_monthly_reports()

    assert result["sent"] == 1
    assert result["skipped"] == 0
    assert mock_send.call_count == 1


@patch(_SEND_TEMPLATE_PATH)
def test_send_affiliate_monthly_reports_email_context(mock_send, affiliate_with_commissions):
    """Task builds correct email context."""
    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.save()

    mock_outbox = Mock()
    mock_outbox.status = "queued"
    mock_send.return_value = mock_outbox

    send_affiliate_monthly_reports()

    # Check send_template_email was called with correct params
    assert mock_send.called
    call_args = mock_send.call_args

    # Check to_email
    assert call_args[1]["to_email"] == affiliate_with_commissions.user.email

    # Check template_type
    assert call_args[1]["template_type"] == "affiliate_monthly_report"

    # Check context has required fields
    context = call_args[1]["context"]
    for key in (
        "affiliate_name",
        "month_name",
        "year",
        "total_earned",
        "commission_count",
        "avg_commission",
        "top_orders",
        "pending_balance",
        "payment_status",
        "portal_url",
        "shop_name",
    ):
        assert key in context, f"Missing context key: {key}"


@patch(_SEND_TEMPLATE_PATH)
def test_send_affiliate_monthly_reports_calculates_correctly(mock_send, affiliate_with_commissions):
    """Task calculates totals correctly (5 commissions x $10 = $50 total)."""
    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.save()

    mock_outbox = Mock()
    mock_outbox.status = "queued"
    mock_send.return_value = mock_outbox

    send_affiliate_monthly_reports()

    context = mock_send.call_args[1]["context"]

    # 5 commissions × $10 = $50
    assert "$50.00" in context["total_earned"]
    # 5 commissions
    assert context["commission_count"] == 5
    # $50 / 5 = $10 average
    assert "$10.00" in context["avg_commission"]


@patch(_SEND_TEMPLATE_PATH)
def test_send_affiliate_monthly_reports_top_orders(mock_send, affiliate_with_commissions):
    """Task includes top N orders (configurable)."""
    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.include_top_orders_count = 3
    settings.save()

    mock_outbox = Mock()
    mock_outbox.status = "queued"
    mock_send.return_value = mock_outbox

    send_affiliate_monthly_reports()

    context = mock_send.call_args[1]["context"]

    # Should include top 3 orders
    assert len(context["top_orders"]) == 3
    assert context["top_orders_count"] == 3


@patch(_SEND_TEMPLATE_PATH)
def test_send_affiliate_monthly_reports_skips_no_activity(mock_send, db):
    """Task skips affiliates with no commissions last month."""
    user = UserFactory()
    Affiliate.objects.create(user=user, status="active")

    # Enable preferences
    prefs, _ = CommunicationPreference.get_or_create_for_user(user)
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.app_preferences["affiliate"]["monthly_report"] = True
    prefs.save()

    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.save()

    result = send_affiliate_monthly_reports()

    # Should skip (no commissions)
    assert result["sent"] == 0
    assert result["skipped"] == 1
    assert mock_send.call_count == 0


@patch(_SEND_TEMPLATE_PATH)
def test_send_affiliate_monthly_reports_respects_preferences(mock_send, affiliate_with_commissions):
    """Task respects communication preferences: monthly_report=False → skipped.

    Note: the task calls ``prefs.should_send_email('affiliate_monthly_report')``.
    ``affiliate_monthly_report`` IS registered in
    ``APP_EMAIL_TYPES['affiliate']``, so category resolution is
    ``('app_specific', 'affiliate')`` — pref_key strips ``affiliate_`` and
    checks ``monthly_report`` (matches default key).
    """
    prefs = affiliate_with_commissions.user.communication_preferences
    prefs.app_preferences["affiliate"]["monthly_report"] = False
    prefs.save()

    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.save()

    result = send_affiliate_monthly_reports()

    # Should skip (preference disabled)
    assert result["sent"] == 0
    assert result["skipped"] == 1
    assert mock_send.call_count == 0


@patch(_SEND_TEMPLATE_PATH)
def test_send_affiliate_monthly_reports_uses_user_language(mock_send, affiliate_with_commissions):
    """Task uses user's language preference."""
    # Refresh the preference from DB and explicitly re-affirm the enabled
    # keys — mutating self.app_preferences["affiliate"]["monthly_report"] in
    # the fixture updates a nested dict which is persisted, but any second
    # instance load can silently reset the copy in memory. Reset explicitly.
    prefs = affiliate_with_commissions.user.communication_preferences
    prefs.refresh_from_db()
    prefs.language_code = "fr"
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.app_preferences["affiliate"]["enabled"] = True
    prefs.app_preferences["affiliate"]["monthly_report"] = True
    prefs.save()

    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.save()

    mock_outbox = Mock()
    mock_outbox.status = "queued"
    mock_send.return_value = mock_outbox

    send_affiliate_monthly_reports()

    # Check language parameter
    call_args = mock_send.call_args
    assert call_args[1]["language"] == "fr"


@patch(_SEND_TEMPLATE_PATH)
def test_send_affiliate_monthly_reports_handles_skipped_email(
    mock_send, affiliate_with_commissions
):
    """Task counts skipped emails as ``skipped``."""
    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.save()

    # Mock email service returning skipped status
    mock_outbox = Mock()
    mock_outbox.status = "skipped"
    mock_send.return_value = mock_outbox

    result = send_affiliate_monthly_reports()

    assert result["sent"] == 0
    assert result["skipped"] == 1


@patch(_SEND_TEMPLATE_PATH)
def test_send_affiliate_monthly_reports_includes_payout_status(
    mock_send, affiliate_with_commissions
):
    """Task includes payout status in context."""
    # Create a payout
    Payout.objects.create(
        affiliate=affiliate_with_commissions, amount=Decimal("50.00"), status="processing"
    )

    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.save()

    mock_outbox = Mock()
    mock_outbox.status = "queued"
    mock_send.return_value = mock_outbox

    send_affiliate_monthly_reports()

    context = mock_send.call_args[1]["context"]

    assert "payment_status" in context
    assert "Payout Processing" in context["payment_status"]


# =============================================================================
# Edge Cases
# =============================================================================


@patch(_SEND_TEMPLATE_PATH)
def test_send_affiliate_monthly_reports_handles_exceptions(mock_send, affiliate_with_commissions):
    """Task handles exceptions gracefully — counted as skipped."""
    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.save()

    # Mock exception
    mock_send.side_effect = Exception("Email service error")

    # Should not crash
    result = send_affiliate_monthly_reports()

    # Should count as skipped
    assert result["skipped"] == 1


@patch(_SEND_TEMPLATE_PATH)
def test_send_affiliate_monthly_reports_multiple_affiliates(mock_send, db):
    """Task processes multiple affiliates correctly."""
    program = Program.objects.create(
        name="Test Program",
        slug="test-program",
        merchant=UserFactory(),
        commission_type="percentage",
        commission_value=Decimal("10.00"),
    )

    last_month_start = (timezone.now().replace(day=1) - timedelta(days=1)).replace(day=1)

    # Create 3 affiliates with commissions
    for _i in range(3):
        user = UserFactory()
        affiliate = Affiliate.objects.create(user=user, status="active")

        # Enable preferences
        prefs, _ = CommunicationPreference.get_or_create_for_user(user)
        prefs.email_marketing = True
        prefs.email_verified = True
        prefs.app_preferences["affiliate"]["monthly_report"] = True
        prefs.save()

        # Create commission
        order = OrderFactory(user=UserFactory(), status="delivered")
        commission = Commission.objects.create(
            affiliate=affiliate,
            program=program,
            order=order,
            amount=Decimal("10.00"),
            status="approved",
        )
        Commission.objects.filter(pk=commission.pk).update(created_at=last_month_start)

    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.save()

    mock_outbox = Mock()
    mock_outbox.status = "queued"
    mock_send.return_value = mock_outbox

    result = send_affiliate_monthly_reports()

    # Should send to all 3 affiliates
    assert result["sent"] == 3
    assert mock_send.call_count == 3
