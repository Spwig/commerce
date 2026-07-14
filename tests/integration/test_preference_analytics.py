"""
Integration tests for Preference Analytics Dashboard (Enhancement 4)

Tests the PreferenceAnalyticsService and admin analytics dashboard view.
"""

from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from accounts.models import CommunicationPreference, PreferenceChangeLog
from accounts.services.preference_analytics_service import PreferenceAnalyticsService
from tests.factories import UserFactory

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.preference_analytics]


@pytest.fixture
def users_with_varied_preferences(db):
    """Create users with different preference states for analytics testing"""
    users = []

    # 5 users with marketing opted in and email verified
    for _i in range(5):
        user = UserFactory()
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]
        prefs.email_marketing = True
        prefs.email_verified = True
        prefs.save()
        users.append(user)

    # 3 users with marketing opted in but not verified
    for _i in range(3):
        user = UserFactory()
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]
        prefs.email_marketing = True
        prefs.email_verified = False
        prefs.save()
        users.append(user)

    # 2 users with SMS opted in
    for _i in range(2):
        user = UserFactory()
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]
        prefs.sms_enabled = True
        prefs.sms_transactional = True
        prefs.save()
        users.append(user)

    # 5 users with no marketing preferences (defaults)
    for _i in range(5):
        user = UserFactory()
        CommunicationPreference.get_or_create_for_user(user)
        users.append(user)

    return users


# =============================================================================
# Date Range Tests
# =============================================================================


def test_get_date_range_for_period_today():
    """Test date range calculation for 'today' period"""
    start, end = PreferenceAnalyticsService.get_date_range_for_period("today")

    assert start.date() == timezone.now().date()
    assert end.date() == timezone.now().date()


def test_get_date_range_for_period_last_7_days():
    """Test date range calculation for 'last_7_days' period"""
    start, end = PreferenceAnalyticsService.get_date_range_for_period("last_7_days")

    expected_start = timezone.now() - timedelta(days=7)
    assert start.date() == expected_start.date()
    assert end.date() == timezone.now().date()


def test_get_date_range_for_period_last_30_days():
    """Test date range calculation for 'last_30_days' period"""
    start, end = PreferenceAnalyticsService.get_date_range_for_period("last_30_days")

    expected_start = timezone.now() - timedelta(days=30)
    assert start.date() == expected_start.date()
    assert end.date() == timezone.now().date()


def test_get_date_range_for_period_custom():
    """Test custom date range"""
    custom_start = timezone.now() - timedelta(days=14)
    custom_end = timezone.now() - timedelta(days=7)

    start, end = PreferenceAnalyticsService.get_date_range_for_period(
        "custom", start_date=custom_start, end_date=custom_end
    )

    assert start == custom_start
    assert end == custom_end


# =============================================================================
# Action Cards Tests
# =============================================================================


def test_get_action_cards_structure(users_with_varied_preferences):
    """Test action cards returns correct structure"""
    cards = PreferenceAnalyticsService.get_action_cards()

    assert "unverified_users" in cards
    assert "recent_unsubscribes" in cards
    assert "pending_verifications" in cards
    assert "total_subscribers" in cards


def test_get_action_cards_unverified_count(users_with_varied_preferences):
    """Test unverified users count (marketing enabled but email not verified)"""
    cards = PreferenceAnalyticsService.get_action_cards()

    # Should be 3 users with email_marketing=True but email_verified=False
    assert cards["unverified_users"] == 3


def test_get_action_cards_total_subscribers(users_with_varied_preferences):
    """Test total active subscribers count"""
    cards = PreferenceAnalyticsService.get_action_cards()

    # Should be 5 users with both email_marketing=True AND email_verified=True
    assert cards["total_subscribers"] == 5


def test_get_action_cards_pending_verifications(users_with_varied_preferences):
    """``pending_verifications`` counts users needing verification action.

    The fixture creates 3 users with email_marketing=True + email_verified=False
    and no SMS verification codes pending, so only those 3 match the
    email predicate.
    """
    cards = PreferenceAnalyticsService.get_action_cards()

    assert cards["pending_verifications"] == 3


# =============================================================================
# Opt-In Metrics Tests
# =============================================================================


def test_get_opt_in_metrics_structure(users_with_varied_preferences):
    """Test opt-in metrics returns correct structure"""
    start_date = timezone.now() - timedelta(days=30)
    end_date = timezone.now()

    metrics = PreferenceAnalyticsService.get_opt_in_metrics(start_date, end_date)

    assert "total_users" in metrics
    assert "marketing_opted_in" in metrics
    assert "email_verified" in metrics
    assert "sms_opted_in" in metrics

    # Check nested structure
    assert "count" in metrics["marketing_opted_in"]
    assert "percentage" in metrics["marketing_opted_in"]


def test_get_opt_in_metrics_calculations(users_with_varied_preferences):
    """Test opt-in metrics calculations are correct.

    ``sms_opted_in`` is defined in the service as ``sms_marketing=True``
    (not ``sms_enabled=True``). The fixture's "SMS opted-in" cohort only
    flips ``sms_transactional`` on, so it does not count toward
    ``sms_opted_in``. The assertions below reflect that.
    """
    start_date = timezone.now() - timedelta(days=30)
    end_date = timezone.now()

    metrics = PreferenceAnalyticsService.get_opt_in_metrics(start_date, end_date)

    # Total users: 15 (5 verified + 3 unverified + 2 SMS + 5 defaults)
    assert metrics["total_users"] == 15

    # Marketing opted in: 8 (5 verified + 3 unverified)
    assert metrics["marketing_opted_in"]["count"] == 8
    assert metrics["marketing_opted_in"]["percentage"] == pytest.approx(53.33, rel=0.1)

    # Email verified: 5
    assert metrics["email_verified"]["count"] == 5
    assert metrics["email_verified"]["percentage"] == pytest.approx(33.33, rel=0.1)

    # SMS opted in: 0 — no fixture user sets ``sms_marketing``.
    assert metrics["sms_opted_in"]["count"] == 0


def test_get_opt_in_metrics_with_comparison(users_with_varied_preferences):
    """Test opt-in metrics with period comparison"""
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)

    metrics = PreferenceAnalyticsService.get_opt_in_metrics(start_date, end_date, compare=True)

    # Should include changes
    assert "changes" in metrics
    assert "marketing_opted_in" in metrics["changes"]
    assert "email_verified" in metrics["changes"]
    assert "sms_opted_in" in metrics["changes"]


# =============================================================================
# App Preference Breakdown Tests
# =============================================================================


def test_get_app_preference_breakdown_structure():
    """Test app preference breakdown returns all apps"""
    breakdown = PreferenceAnalyticsService.get_app_preference_breakdown()

    assert "blog" in breakdown
    assert "loyalty" in breakdown
    assert "referrals" in breakdown
    assert "affiliate" in breakdown


def test_get_app_preference_breakdown_counts():
    """Test app preference breakdown counts correctly.

    ``get_default_app_preferences`` already enables blog / loyalty /
    referrals / affiliate by default, so freshly created users count
    toward every app's total. We capture the baseline before creating
    additional cohorts so the assertions are drift-resistant.
    """
    baseline = PreferenceAnalyticsService.get_app_preference_breakdown()

    # Create 3 users with blog explicitly enabled, loyalty explicitly off.
    for _i in range(3):
        user = UserFactory()
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]
        prefs.app_preferences["blog"]["enabled"] = True
        prefs.app_preferences["loyalty"]["enabled"] = False
        prefs.save()

    # 2 users with the reverse configuration.
    for _i in range(2):
        user = UserFactory()
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]
        prefs.app_preferences["blog"]["enabled"] = False
        prefs.app_preferences["loyalty"]["enabled"] = True
        prefs.save()

    breakdown = PreferenceAnalyticsService.get_app_preference_breakdown()

    assert breakdown["blog"] == baseline["blog"] + 3
    assert breakdown["loyalty"] == baseline["loyalty"] + 2


# =============================================================================
# Verification Funnel Tests
# =============================================================================


def test_get_verification_funnel_structure(users_with_varied_preferences):
    """Test verification funnel returns correct structure"""
    funnel = PreferenceAnalyticsService.get_verification_funnel()

    assert "signup" in funnel
    assert "opted_in" in funnel
    assert "verified" in funnel
    assert "active" in funnel
    assert "conversion_rates" in funnel


def test_get_verification_funnel_counts(users_with_varied_preferences):
    """Test verification funnel counts"""
    funnel = PreferenceAnalyticsService.get_verification_funnel()

    # Signup: all users (15)
    assert funnel["signup"] == 15

    # Opted in: users with email_marketing=True (8)
    assert funnel["opted_in"] == 8

    # Verified: users with email_verified=True (5)
    assert funnel["verified"] == 5

    # Active: users with both marketing AND verified (5)
    assert funnel["active"] == 5


def test_get_verification_funnel_conversion_rates(users_with_varied_preferences):
    """Test verification funnel conversion rate calculations"""
    funnel = PreferenceAnalyticsService.get_verification_funnel()

    rates = funnel["conversion_rates"]

    # Signup to opted in: 8/15 = 53.33%
    assert rates["signup_to_opted_in"] == pytest.approx(53.33, rel=0.1)

    # Opted in to verified: 5/8 = 62.5%
    assert rates["opted_in_to_verified"] == pytest.approx(62.5, rel=0.1)

    # Verified to active: 5/5 = 100%
    assert rates["verified_to_active"] == pytest.approx(100.0, rel=0.1)


def test_get_verification_funnel_handles_zero_division():
    """Test funnel handles zero division gracefully"""
    # No users - should not crash
    funnel = PreferenceAnalyticsService.get_verification_funnel()

    assert funnel["signup"] == 0
    assert funnel["conversion_rates"]["signup_to_opted_in"] == 0.0


# =============================================================================
# Opt-In Trend Tests
# =============================================================================


def test_get_opt_in_over_time_structure():
    """Test opt-in trend returns array of data points"""
    start_date = timezone.now() - timedelta(days=7)
    end_date = timezone.now()

    trend = PreferenceAnalyticsService.get_opt_in_over_time(start_date, end_date)

    assert isinstance(trend, list)
    if len(trend) > 0:
        assert "date" in trend[0]
        assert "count" in trend[0]


def test_get_opt_in_over_time_counts_new_opt_ins():
    """Test opt-in trend counts new opt-ins by date"""
    # Create preference change logs for specific dates
    user1 = UserFactory()
    user2 = UserFactory()

    yesterday = timezone.now() - timedelta(days=1)

    # User 1 opted in yesterday
    PreferenceChangeLog.objects.create(
        user=user1,
        preference=CommunicationPreference.get_or_create_for_user(user1)[0],
        action="email_marketing.enable",
        old_value={"email_marketing": False},
        new_value={"email_marketing": True},
        source="user",
        timestamp=yesterday,
    )

    # User 2 opted in today
    PreferenceChangeLog.objects.create(
        user=user2,
        preference=CommunicationPreference.get_or_create_for_user(user2)[0],
        action="email_marketing.enable",
        old_value={"email_marketing": False},
        new_value={"email_marketing": True},
        source="user",
        timestamp=timezone.now(),
    )

    start_date = timezone.now() - timedelta(days=7)
    end_date = timezone.now()

    trend = PreferenceAnalyticsService.get_opt_in_over_time(start_date, end_date)

    # Should have data points for days with opt-ins
    assert len(trend) >= 2


# =============================================================================
# Admin Dashboard View Tests
# =============================================================================


def test_preference_analytics_dashboard_requires_staff(client, db):
    """Test analytics dashboard requires staff permission"""
    # Regular user
    user = UserFactory()
    client.force_login(user)

    url = reverse("preference_analytics_dashboard")
    response = client.get(url)

    # Should redirect to login
    assert response.status_code == 302


def test_preference_analytics_dashboard_accessible_by_staff(client, db):
    """Test analytics dashboard accessible by staff users"""
    # Staff user
    user = UserFactory(is_staff=True)
    client.force_login(user)

    url = reverse("preference_analytics_dashboard")
    response = client.get(url)

    assert response.status_code == 200


def test_preference_analytics_dashboard_context(client, db):
    """Test analytics dashboard includes all required context"""
    user = UserFactory(is_staff=True)
    client.force_login(user)

    url = reverse("preference_analytics_dashboard")
    response = client.get(url)

    assert "action_cards" in response.context
    assert "opt_in_metrics" in response.context
    assert "app_breakdown" in response.context
    assert "opt_in_trend" in response.context
    assert "verification_funnel" in response.context


def test_preference_analytics_dashboard_period_filter(client, db):
    """Test analytics dashboard accepts period parameter"""
    user = UserFactory(is_staff=True)
    client.force_login(user)

    url = reverse("preference_analytics_dashboard")
    response = client.get(url, {"period": "last_7_days"})

    assert response.status_code == 200
    assert response.context["period"] == "last_7_days"


def test_preference_analytics_dashboard_compare_mode(client, db):
    """Test analytics dashboard accepts compare parameter"""
    user = UserFactory(is_staff=True)
    client.force_login(user)

    url = reverse("preference_analytics_dashboard")
    response = client.get(url, {"compare": "true"})

    assert response.status_code == 200
    assert response.context["compare"] is True
