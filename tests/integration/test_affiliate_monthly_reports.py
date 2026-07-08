"""
Integration tests for Affiliate Monthly Reports (Enhancement 6)

Tests the AffiliateReportSettings model and send_affiliate_monthly_reports task.
"""

import pytest
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from unittest.mock import patch, Mock

from affiliate.models import AffiliateReportSettings, Affiliate, Commission, Payout
from affiliate.tasks import send_affiliate_monthly_reports
from accounts.models import CommunicationPreference
from tests.factories import UserFactory

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.affiliate_reports]


@pytest.fixture
def affiliate_with_commissions(db):
    """Create affiliate with commission history"""
    from orders.models import Order
    from affiliate.models import Program

    user = UserFactory()

    # Create affiliate
    affiliate = Affiliate.objects.create(
        user=user,
        status='active'
    )

    # Create program
    program = Program.objects.create(
        name='Test Program',
        slug='test-program',
        merchant=UserFactory(),
        commission_type='percentage',
        commission_value=Decimal('10.00')
    )

    # Create commissions from last month
    last_month_start = (timezone.now().replace(day=1) - timedelta(days=1)).replace(day=1)

    for i in range(5):
        order = Order.objects.create(
            customer=UserFactory(),
            status='completed',
            total=Decimal('100.00'),
            created_at=last_month_start + timedelta(days=i)
        )

        Commission.objects.create(
            affiliate=affiliate,
            order=order,
            amount=Decimal('10.00'),
            status='approved',
            created_at=last_month_start + timedelta(days=i)
        )

    # Enable monthly reports in preferences
    prefs = CommunicationPreference.get_or_create_for_user(user)[0]
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.app_preferences['affiliate']['enabled'] = True
    prefs.app_preferences['affiliate']['monthly_report'] = True
    prefs.save()

    return affiliate


# =============================================================================
# AffiliateReportSettings Model Tests
# =============================================================================

def test_affiliate_report_settings_singleton():
    """Test AffiliateReportSettings is a singleton (pk=1)"""
    settings1 = AffiliateReportSettings.get_settings()
    settings2 = AffiliateReportSettings.get_settings()

    assert settings1.pk == 1
    assert settings1.pk == settings2.pk


def test_affiliate_report_settings_defaults():
    """Test AffiliateReportSettings has correct defaults"""
    settings = AffiliateReportSettings.get_settings()

    assert settings.monthly_report_enabled is True
    assert settings.monthly_report_day == 1
    assert settings.monthly_report_hour == 9
    assert settings.include_top_orders_count == 5


def test_affiliate_report_settings_str():
    """Test AffiliateReportSettings string representation"""
    settings = AffiliateReportSettings.get_settings()

    str_repr = str(settings)

    assert 'Affiliate Report Settings' in str_repr
    assert 'Enabled' in str_repr


def test_affiliate_report_settings_update():
    """Test updating AffiliateReportSettings"""
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

@patch('affiliate.tasks.EmailSendingService.send_template_email')
def test_send_affiliate_monthly_reports_disabled(mock_send, db):
    """Test task skips when reports are disabled"""
    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_enabled = False
    settings.save()

    result = send_affiliate_monthly_reports()

    assert result['reason'] == 'disabled'
    assert result['sent'] == 0
    assert mock_send.call_count == 0


@patch('affiliate.tasks.EmailSendingService.send_template_email')
def test_send_affiliate_monthly_reports_wrong_day(mock_send, db):
    """Test task skips when not on configured send day"""
    settings = AffiliateReportSettings.get_settings()
    today = timezone.now().day

    # Set to different day
    settings.monthly_report_day = (today % 28) + 1  # Different day
    settings.save()

    result = send_affiliate_monthly_reports()

    assert result['reason'] == 'not_send_day'
    assert result['sent'] == 0
    assert mock_send.call_count == 0


@patch('affiliate.tasks.EmailSendingService.send_template_email')
def test_send_affiliate_monthly_reports_wrong_hour(mock_send, db):
    """Test task skips when not on configured send hour"""
    settings = AffiliateReportSettings.get_settings()
    current_hour = timezone.now().hour

    # Set to different hour
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = (current_hour + 1) % 24  # Different hour
    settings.save()

    result = send_affiliate_monthly_reports()

    assert result['reason'] == 'not_send_hour'
    assert mock_send.call_count == 0


@patch('affiliate.tasks.EmailSendingService.send_template_email')
def test_send_affiliate_monthly_reports_success(mock_send, affiliate_with_commissions):
    """Test task sends reports on correct day/hour"""
    # Configure to current day/hour
    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.save()

    # Mock successful email send
    mock_outbox = Mock()
    mock_outbox.status = 'queued'
    mock_send.return_value = mock_outbox

    result = send_affiliate_monthly_reports()

    assert result['sent'] == 1
    assert result['skipped'] == 0
    assert mock_send.call_count == 1


@patch('affiliate.tasks.EmailSendingService.send_template_email')
def test_send_affiliate_monthly_reports_email_context(mock_send, affiliate_with_commissions):
    """Test task builds correct email context"""
    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.save()

    mock_outbox = Mock()
    mock_outbox.status = 'queued'
    mock_send.return_value = mock_outbox

    send_affiliate_monthly_reports()

    # Check send_template_email was called with correct params
    assert mock_send.called
    call_args = mock_send.call_args

    # Check to_email
    assert call_args[1]['to_email'] == affiliate_with_commissions.user.email

    # Check template_type
    assert call_args[1]['template_type'] == 'affiliate_monthly_report'

    # Check context has required fields
    context = call_args[1]['context']
    assert 'affiliate_name' in context
    assert 'month_name' in context
    assert 'year' in context
    assert 'total_earned' in context
    assert 'commission_count' in context
    assert 'avg_commission' in context
    assert 'top_orders' in context
    assert 'pending_balance' in context
    assert 'payment_status' in context
    assert 'portal_url' in context
    assert 'shop_name' in context


@patch('affiliate.tasks.EmailSendingService.send_template_email')
def test_send_affiliate_monthly_reports_calculates_correctly(mock_send, affiliate_with_commissions):
    """Test task calculates totals correctly"""
    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.save()

    mock_outbox = Mock()
    mock_outbox.status = 'queued'
    mock_send.return_value = mock_outbox

    send_affiliate_monthly_reports()

    context = mock_send.call_args[1]['context']

    # 5 commissions × $10 = $50
    assert '$50.00' in context['total_earned']

    # 5 commissions
    assert context['commission_count'] == 5

    # $50 / 5 = $10 average
    assert '$10.00' in context['avg_commission']


@patch('affiliate.tasks.EmailSendingService.send_template_email')
def test_send_affiliate_monthly_reports_top_orders(mock_send, affiliate_with_commissions):
    """Test task includes top N orders"""
    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.include_top_orders_count = 3
    settings.save()

    mock_outbox = Mock()
    mock_outbox.status = 'queued'
    mock_send.return_value = mock_outbox

    send_affiliate_monthly_reports()

    context = mock_send.call_args[1]['context']

    # Should include top 3 orders
    assert len(context['top_orders']) == 3
    assert context['top_orders_count'] == 3


@patch('affiliate.tasks.EmailSendingService.send_template_email')
def test_send_affiliate_monthly_reports_skips_no_activity(mock_send, db):
    """Test task skips affiliates with no commissions last month"""
    user = UserFactory()
    affiliate = Affiliate.objects.create(user=user, status='active')

    # Enable preferences
    prefs = CommunicationPreference.get_or_create_for_user(user)[0]
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.app_preferences['affiliate']['monthly_report'] = True
    prefs.save()

    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.save()

    result = send_affiliate_monthly_reports()

    # Should skip (no commissions)
    assert result['sent'] == 0
    assert result['skipped'] == 1
    assert mock_send.call_count == 0


@patch('affiliate.tasks.EmailSendingService.send_template_email')
def test_send_affiliate_monthly_reports_respects_preferences(mock_send, affiliate_with_commissions):
    """Test task respects communication preferences"""
    # Disable monthly reports in preferences
    prefs = affiliate_with_commissions.user.communication_preferences
    prefs.app_preferences['affiliate']['monthly_report'] = False
    prefs.save()

    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.save()

    result = send_affiliate_monthly_reports()

    # Should skip (preference disabled)
    assert result['sent'] == 0
    assert result['skipped'] == 1
    assert mock_send.call_count == 0


@patch('affiliate.tasks.EmailSendingService.send_template_email')
def test_send_affiliate_monthly_reports_uses_user_language(mock_send, affiliate_with_commissions):
    """Test task uses user's language preference"""
    prefs = affiliate_with_commissions.user.communication_preferences
    prefs.language_code = 'fr'
    prefs.save()

    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.save()

    mock_outbox = Mock()
    mock_outbox.status = 'queued'
    mock_send.return_value = mock_outbox

    send_affiliate_monthly_reports()

    # Check language parameter
    call_args = mock_send.call_args
    assert call_args[1]['language'] == 'fr'


@patch('affiliate.tasks.EmailSendingService.send_template_email')
def test_send_affiliate_monthly_reports_handles_skipped_email(mock_send, affiliate_with_commissions):
    """Test task counts skipped emails correctly"""
    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.save()

    # Mock email service returning skipped status
    mock_outbox = Mock()
    mock_outbox.status = 'skipped'
    mock_send.return_value = mock_outbox

    result = send_affiliate_monthly_reports()

    assert result['sent'] == 0
    assert result['skipped'] == 1


@patch('affiliate.tasks.EmailSendingService.send_template_email')
def test_send_affiliate_monthly_reports_includes_payout_status(mock_send, affiliate_with_commissions):
    """Test task includes payout status in context"""
    # Create a payout
    Payout.objects.create(
        affiliate=affiliate_with_commissions,
        amount=Decimal('50.00'),
        status='processing'
    )

    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.save()

    mock_outbox = Mock()
    mock_outbox.status = 'queued'
    mock_send.return_value = mock_outbox

    send_affiliate_monthly_reports()

    context = mock_send.call_args[1]['context']

    assert 'payment_status' in context
    assert 'Payout Processing' in context['payment_status']


# =============================================================================
# Edge Cases
# =============================================================================

@patch('affiliate.tasks.EmailSendingService.send_template_email')
def test_send_affiliate_monthly_reports_handles_exceptions(mock_send, affiliate_with_commissions):
    """Test task handles exceptions gracefully"""
    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.save()

    # Mock exception
    mock_send.side_effect = Exception("Email service error")

    # Should not crash
    result = send_affiliate_monthly_reports()

    # Should count as skipped
    assert result['skipped'] == 1


@patch('affiliate.tasks.EmailSendingService.send_template_email')
def test_send_affiliate_monthly_reports_multiple_affiliates(mock_send, db):
    """Test task processes multiple affiliates correctly"""
    from orders.models import Order
    from affiliate.models import Program

    program = Program.objects.create(
        name='Test Program',
        slug='test-program',
        merchant=UserFactory(),
        commission_type='percentage',
        commission_value=Decimal('10.00')
    )

    last_month_start = (timezone.now().replace(day=1) - timedelta(days=1)).replace(day=1)

    # Create 3 affiliates with commissions
    for i in range(3):
        user = UserFactory()
        affiliate = Affiliate.objects.create(user=user, status='active')

        # Enable preferences
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]
        prefs.email_marketing = True
        prefs.email_verified = True
        prefs.app_preferences['affiliate']['monthly_report'] = True
        prefs.save()

        # Create commission
        order = Order.objects.create(
            customer=UserFactory(),
            status='completed',
            total=Decimal('100.00'),
            created_at=last_month_start
        )
        Commission.objects.create(
            affiliate=affiliate,
            order=order,
            amount=Decimal('10.00'),
            status='approved',
            created_at=last_month_start
        )

    settings = AffiliateReportSettings.get_settings()
    settings.monthly_report_day = timezone.now().day
    settings.monthly_report_hour = timezone.now().hour
    settings.save()

    mock_outbox = Mock()
    mock_outbox.status = 'queued'
    mock_send.return_value = mock_outbox

    result = send_affiliate_monthly_reports()

    # Should send to all 3 affiliates
    assert result['sent'] == 3
    assert mock_send.call_count == 3
