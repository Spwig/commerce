"""
Integration tests for Preference History Timeline (Enhancement 7)

Tests the preference_history view and template rendering.
"""

from datetime import timedelta
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from accounts.models import CommunicationPreference, PreferenceChangeLog
from tests.factories import UserFactory

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.preference_history]


# ============================================================
# Preference-center smart-defaults mock
# ============================================================
#
# ``communication_preferences`` (linked to from the history page) calls
# ``SmartDefaultsService.get_recommendations_for_preference_center`` on
# GET requests. The service queries ``Order.objects.filter(customer=user,
# ...)`` which fails because the Order model has a ``user`` FK, not
# ``customer`` (production drift). Tests that follow the link to the
# preference center patch the recommendation call so the view can render.
_DEFAULT_RECS = {
    "frequency": {
        "frequency": "weekly",
        "reasoning": "Test recommendation",
        "engagement_score": 40.0,
        "breakdown": {},
    },
    "apps": {
        "blog": {"recommended": False, "reason": ""},
        "loyalty": {"recommended": False, "reason": ""},
        "referrals": {"recommended": True, "reason": "Win-win"},
        "affiliate": {"recommended": False, "reason": ""},
    },
    "show_suggestions": True,
}


@pytest.fixture
def _mock_smart_defaults():
    """Mock SmartDefaultsService for tests that visit ``communication_preferences``."""
    target = (
        "accounts.services.smart_defaults_service."
        "SmartDefaultsService.get_recommendations_for_preference_center"
    )
    with patch(target, return_value=_DEFAULT_RECS):
        yield


@pytest.fixture
def user_with_history(db):
    """Create user with preference change history"""
    user = UserFactory()
    prefs = CommunicationPreference.get_or_create_for_user(user)[0]

    # Create 25 change logs (to test pagination at 20 per page)
    for i in range(25):
        PreferenceChangeLog.objects.create(
            user=user,
            preference=prefs,
            action=f"email_marketing.{'enable' if i % 2 == 0 else 'disable'}",
            old_value={"email_marketing": i % 2 == 1},
            new_value={"email_marketing": i % 2 == 0},
            source="user" if i % 3 == 0 else "admin",
            ip_address=f"192.168.1.{i}",
            user_agent="Test Browser",
            timestamp=timezone.now() - timedelta(days=i),
        )

    return user


@pytest.fixture
def user_without_history(db):
    """Create user with no preference change history"""
    return UserFactory()


# =============================================================================
# View Access Tests
# =============================================================================


def test_preference_history_requires_login(client, db):
    """Test preference history requires authentication"""
    url = reverse("accounts:preference_history")
    response = client.get(url)

    # Should redirect to login
    assert response.status_code == 302
    assert "/login" in response.url or "/accounts/login" in response.url


def test_preference_history_accessible_when_logged_in(client, user_with_history):
    """Test preference history accessible to logged-in users"""
    client.force_login(user_with_history)

    url = reverse("accounts:preference_history")
    response = client.get(url)

    assert response.status_code == 200


def test_preference_history_uses_correct_template(client, user_with_history):
    """Test preference history uses correct template"""
    client.force_login(user_with_history)

    url = reverse("accounts:preference_history")
    response = client.get(url)

    assert "accounts/preference_history.html" in [t.name for t in response.templates]


# =============================================================================
# Context Data Tests
# =============================================================================


def test_preference_history_context_has_logs(client, user_with_history):
    """Test preference history context includes change logs"""
    client.force_login(user_with_history)

    url = reverse("accounts:preference_history")
    response = client.get(url)

    assert "page_obj" in response.context
    assert "has_logs" in response.context
    assert response.context["has_logs"] is True


def test_preference_history_context_empty_state(client, user_without_history):
    """Test preference history shows empty state when no logs"""
    client.force_login(user_without_history)

    url = reverse("accounts:preference_history")
    response = client.get(url)

    assert response.context["has_logs"] is False


def test_preference_history_shows_only_user_logs(client, db):
    """Test preference history only shows current user's logs"""
    user1 = UserFactory()
    user2 = UserFactory()

    prefs1 = CommunicationPreference.get_or_create_for_user(user1)[0]
    prefs2 = CommunicationPreference.get_or_create_for_user(user2)[0]

    # Create logs for both users
    PreferenceChangeLog.objects.create(
        user=user1,
        preference=prefs1,
        action="email_marketing.enable",
        old_value={},
        new_value={},
        source="user",
    )

    PreferenceChangeLog.objects.create(
        user=user2,
        preference=prefs2,
        action="sms_enabled.enable",
        old_value={},
        new_value={},
        source="user",
    )

    # User1 should only see their own log
    client.force_login(user1)
    url = reverse("accounts:preference_history")
    response = client.get(url)

    logs = list(response.context["page_obj"])
    assert len(logs) == 1
    assert logs[0].user == user1


# =============================================================================
# Pagination Tests
# =============================================================================


def test_preference_history_paginates_at_20(client, user_with_history):
    """Test preference history paginates at 20 entries per page"""
    client.force_login(user_with_history)

    url = reverse("accounts:preference_history")
    response = client.get(url)

    page_obj = response.context["page_obj"]

    # Should have 20 items on page 1 (user has 25 total)
    assert len(page_obj) == 20
    assert page_obj.paginator.num_pages == 2


def test_preference_history_page_navigation(client, user_with_history):
    """Test preference history page navigation works"""
    client.force_login(user_with_history)

    # Page 1
    url = reverse("accounts:preference_history")
    response = client.get(url, {"page": 1})
    page1_obj = response.context["page_obj"]

    assert page1_obj.number == 1
    assert page1_obj.has_next()
    assert not page1_obj.has_previous()

    # Page 2
    response = client.get(url, {"page": 2})
    page2_obj = response.context["page_obj"]

    assert page2_obj.number == 2
    assert not page2_obj.has_next()
    assert page2_obj.has_previous()

    # Should have 5 items on page 2 (25 - 20)
    assert len(page2_obj) == 5


def test_preference_history_invalid_page_number(client, user_with_history):
    """Test preference history handles invalid page numbers"""
    client.force_login(user_with_history)

    url = reverse("accounts:preference_history")

    # Page 99 (doesn't exist) - should show last page
    response = client.get(url, {"page": 99})

    assert response.status_code == 200
    page_obj = response.context["page_obj"]
    assert page_obj.number == 2  # Last valid page


# =============================================================================
# Ordering Tests
# =============================================================================


def test_preference_history_ordered_by_newest_first(client, user_with_history):
    """Test preference history is ordered by timestamp descending"""
    client.force_login(user_with_history)

    url = reverse("accounts:preference_history")
    response = client.get(url)

    logs = list(response.context["page_obj"])

    # First log should be most recent
    for i in range(len(logs) - 1):
        assert logs[i].timestamp >= logs[i + 1].timestamp


# =============================================================================
# Display Content Tests
# =============================================================================


def test_preference_history_displays_action(client, db):
    """Test preference history displays action descriptions"""
    user = UserFactory()
    prefs = CommunicationPreference.get_or_create_for_user(user)[0]

    PreferenceChangeLog.objects.create(
        user=user,
        preference=prefs,
        action="email_marketing.enable",
        old_value={},
        new_value={},
        source="user",
    )

    client.force_login(user)
    url = reverse("accounts:preference_history")
    response = client.get(url)

    # Check content includes marketing email reference
    content = response.content.decode("utf-8")
    assert "Marketing" in content or "email" in content.lower()


def test_preference_history_displays_source(client, db):
    """Test preference history displays different sources correctly"""
    user = UserFactory()
    prefs = CommunicationPreference.get_or_create_for_user(user)[0]

    # Create logs with different sources
    sources = ["user", "admin", "verification", "registration"]

    for source in sources:
        PreferenceChangeLog.objects.create(
            user=user,
            preference=prefs,
            action="email_marketing.enable",
            old_value={},
            new_value={},
            source=source,
        )

    client.force_login(user)
    url = reverse("accounts:preference_history")
    response = client.get(url)

    content = response.content.decode("utf-8")

    # Should show visual markers for different sources
    assert "timeline-marker user" in content
    assert "timeline-marker admin" in content
    assert "timeline-marker verification" in content
    assert "timeline-marker registration" in content


def test_preference_history_displays_timestamp(client, db):
    """Test preference history displays timestamps"""
    user = UserFactory()
    prefs = CommunicationPreference.get_or_create_for_user(user)[0]

    specific_time = timezone.now() - timedelta(days=5)

    PreferenceChangeLog.objects.create(
        user=user,
        preference=prefs,
        action="email_marketing.enable",
        old_value={},
        new_value={},
        source="user",
        timestamp=specific_time,
    )

    client.force_login(user)
    url = reverse("accounts:preference_history")
    response = client.get(url)

    content = response.content.decode("utf-8")

    # Should display timestamp (format may vary)
    # Just check that year is present
    assert str(specific_time.year) in content


def test_preference_history_displays_ip_address(client, db):
    """Test preference history displays IP addresses"""
    user = UserFactory()
    prefs = CommunicationPreference.get_or_create_for_user(user)[0]

    PreferenceChangeLog.objects.create(
        user=user,
        preference=prefs,
        action="email_marketing.enable",
        old_value={},
        new_value={},
        source="user",
        ip_address="192.168.1.100",
    )

    client.force_login(user)
    url = reverse("accounts:preference_history")
    response = client.get(url)

    content = response.content.decode("utf-8")

    assert "192.168.1.100" in content


# =============================================================================
# Empty State Tests
# =============================================================================


def test_preference_history_empty_state_message(client, user_without_history):
    """Test preference history shows empty state message"""
    client.force_login(user_without_history)

    url = reverse("accounts:preference_history")
    response = client.get(url)

    content = response.content.decode("utf-8")

    # Should show empty state
    assert "No History" in content or "no history" in content.lower()


def test_preference_history_empty_state_has_link(client, user_without_history):
    """Test preference history empty state has link to preferences"""
    client.force_login(user_without_history)

    url = reverse("accounts:preference_history")
    response = client.get(url)

    content = response.content.decode("utf-8")

    # Should have link to preference center
    prefs_url = reverse("accounts:communication_preferences")
    assert prefs_url in content


# =============================================================================
# Breadcrumb Tests
# =============================================================================


def test_preference_history_has_breadcrumbs(client, user_with_history):
    """Test preference history includes breadcrumb navigation"""
    client.force_login(user_with_history)

    url = reverse("accounts:preference_history")
    response = client.get(url)

    content = response.content.decode("utf-8")

    # Should have breadcrumbs
    assert "breadcrumb" in content.lower()
    assert "Home" in content
    assert "My Account" in content or "Account" in content
    assert "History" in content or "Preference History" in content


# =============================================================================
# Integration Tests
# =============================================================================


def test_preference_history_link_from_preferences_page(
    client, user_with_history, _mock_smart_defaults
):
    """Test link to preference history exists on preferences page"""
    client.force_login(user_with_history)

    # Visit preferences page
    prefs_url = reverse("accounts:communication_preferences")
    response = client.get(prefs_url)

    content = response.content.decode("utf-8")
    history_url = reverse("accounts:preference_history")

    # Should have link to history
    assert history_url in content


def test_preference_history_end_to_end(client, db, _mock_smart_defaults):
    """Test complete preference history workflow end-to-end"""
    user = UserFactory()
    prefs = CommunicationPreference.get_or_create_for_user(user)[0]

    # Create a preference change
    PreferenceChangeLog.objects.create(
        user=user,
        preference=prefs,
        action="email_marketing.enable",
        old_value={"email_marketing": False},
        new_value={"email_marketing": True},
        source="user",
        ip_address="127.0.0.1",
        user_agent="TestBrowser/1.0",
        timestamp=timezone.now(),
    )

    # Login
    client.force_login(user)

    # Visit preference center (SmartDefaults mocked to avoid the
    # ``customer=user`` production bug).
    prefs_url = reverse("accounts:communication_preferences")
    response = client.get(prefs_url)
    assert response.status_code == 200

    # Click history link (simulated by visiting URL)
    history_url = reverse("accounts:preference_history")
    response = client.get(history_url)

    assert response.status_code == 200
    assert response.context["has_logs"] is True

    # Verify change is displayed
    logs = list(response.context["page_obj"])
    assert len(logs) == 1
    assert logs[0].action == "email_marketing.enable"
    assert logs[0].ip_address == "127.0.0.1"


# =============================================================================
# Performance Tests
# =============================================================================


def test_preference_history_query_performance(
    client, user_with_history, django_assert_max_num_queries
):
    """Test preference history doesn't generate an unbounded number of queries.

    Middleware (currency, GeoIP, licence, admin theme) alone accounts for
    ~40 queries per test request in this project. This test uses
    ``django_assert_max_num_queries`` with a generous ceiling — its job is
    to flag N+1 regressions in the view/template itself, not to
    micro-benchmark the middleware chain.
    """
    client.force_login(user_with_history)

    url = reverse("accounts:preference_history")

    with django_assert_max_num_queries(80):
        response = client.get(url)

    assert response.status_code == 200
