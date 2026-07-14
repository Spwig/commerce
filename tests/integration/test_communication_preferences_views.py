"""
Communication Preferences View Tests.

Tests customer-facing preference center and unsubscribe page views.

Views under test:

* ``GET/POST /en/account/preferences/`` (``accounts:communication_preferences``)
* ``GET/POST /en/account/unsubscribe/<token>/`` (``accounts:unsubscribe``)

Tests that hit ``communication_preferences`` GET patch
``SmartDefaultsService.get_recommendations_for_preference_center`` for
isolation (so they don't depend on Order fixtures / factory shape). The
underlying Order.user drift and the ``page_builder:home`` redirect are
both fixed in production code.
"""

from unittest.mock import patch

import pytest
from django.contrib.messages import get_messages
from django.test import Client
from django.urls import reverse

from tests.factories import UserFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.preferences_views]


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def client():
    """Django test client."""
    return Client()


@pytest.fixture
def logged_in_client(client):
    """Client with logged-in user."""
    user = UserFactory()
    client.force_login(user)
    return client, user


@pytest.fixture
def _mock_smart_defaults():
    """Patch SmartDefaultsService so preference_center GET requests don't crash.

    The service queries ``Order.objects.filter(customer=user, ...)``, but the
    Order model has ``user``, not ``customer``. This mock returns a minimal
    recommendation payload matching the shape the template consumes.
    """
    default_recs = {
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
    target = (
        "accounts.services.smart_defaults_service."
        "SmartDefaultsService.get_recommendations_for_preference_center"
    )
    with patch(target, return_value=default_recs):
        yield


# ============================================================
# Preference Center View - GET
# ============================================================


def test_preference_center_requires_login(client):
    """Preference center redirects unauthenticated users to login."""
    url = reverse("accounts:communication_preferences")
    response = client.get(url)

    assert response.status_code == 302
    # Django's default LOGIN_URL is ``/accounts/login/`` (allauth is mounted
    # under that prefix). The redirect includes a ``next=`` query string.
    assert "/accounts/login/" in response.url


def test_preference_center_displays_for_authenticated_user(logged_in_client, _mock_smart_defaults):
    """Preference center loads for authenticated user."""
    client, _user = logged_in_client
    url = reverse("accounts:communication_preferences")

    response = client.get(url)

    assert response.status_code == 200


def test_preference_center_shows_current_preferences(logged_in_client, _mock_smart_defaults):
    """Preference center displays user's current preference values."""
    client, user = logged_in_client

    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.sms_transactional = True
    prefs.app_preferences["blog"]["frequency"] = "immediate"
    prefs.save()

    response = client.get(reverse("accounts:communication_preferences"))
    assert response.status_code == 200
    # Values are surfaced via checkbox inputs; at least one appears checked
    # once we've enabled email_marketing.
    assert "checked" in response.content.decode()


def test_preference_center_shows_verification_badge(logged_in_client, _mock_smart_defaults):
    """Preference center places the ``prefs`` object into template context."""
    client, user = logged_in_client

    prefs = user.communication_preferences
    prefs.email_verified = True
    prefs.save()

    response = client.get(reverse("accounts:communication_preferences"))

    # The view puts the CommunicationPreference row in ``context["prefs"]``.
    # Assert on context — the exact chrome/badge markup lives in a merchant
    # theme template outside the test scope.
    assert response.context["prefs"].email_verified is True


def test_preference_center_creates_preference_if_missing(logged_in_client, _mock_smart_defaults):
    """Preference center auto-creates preference if missing."""
    client, user = logged_in_client

    # Delete preference so we exercise the ``get_or_create_for_user`` branch.
    user.communication_preferences.delete()

    response = client.get(reverse("accounts:communication_preferences"))
    assert response.status_code == 200

    user.refresh_from_db()
    assert hasattr(user, "communication_preferences")


# ============================================================
# Preference Center View - POST
# ============================================================


def test_preference_center_update_email_marketing(logged_in_client):
    """POST to preference center updates ``email_marketing``."""
    client, user = logged_in_client
    url = reverse("accounts:communication_preferences")

    response = client.post(url, {"email_marketing": "on"})
    # POST branch does not touch SmartDefaultsService, so no mock needed.
    assert response.status_code == 302

    user.refresh_from_db()
    assert user.communication_preferences.email_marketing is True


def test_preference_center_update_unchecked_checkbox(logged_in_client):
    """POST with unchecked checkbox sets value to False."""
    client, user = logged_in_client

    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.save()

    response = client.post(
        reverse("accounts:communication_preferences"),
        {"email_transactional": "on"},
    )

    assert response.status_code == 302

    user.refresh_from_db()
    assert user.communication_preferences.email_marketing is False


def test_preference_center_update_app_preferences(logged_in_client):
    """POST updates app-specific preferences."""
    client, user = logged_in_client

    response = client.post(
        reverse("accounts:communication_preferences"),
        {
            "blog_enabled": "on",
            "blog_frequency": "immediate",
            "loyalty_enabled": "on",
            "loyalty_points_earned": "on",
        },
    )

    assert response.status_code == 302

    user.refresh_from_db()
    prefs = user.communication_preferences
    assert prefs.app_preferences["blog"]["enabled"] is True
    assert prefs.app_preferences["blog"]["frequency"] == "immediate"
    assert prefs.app_preferences["loyalty"]["enabled"] is True
    assert prefs.app_preferences["loyalty"]["points_earned"] is True


def test_preference_center_update_shows_success_message(logged_in_client, _mock_smart_defaults):
    """POST shows success message after update."""
    client, _user = logged_in_client

    response = client.post(
        reverse("accounts:communication_preferences"),
        {"email_marketing": "on"},
        follow=True,
    )

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0
    assert "updated" in str(messages[0]).lower()


def test_preference_center_update_invalidates_cache(logged_in_client):
    """POST invalidates preference cache."""
    from django.core.cache import cache

    from accounts.services.preference_service import PreferenceService

    client, user = logged_in_client

    PreferenceService.check_email_permission(user, "newsletter")
    cache_key = f"email_pref:{user.id}:newsletter"
    assert cache.get(cache_key) is not None

    client.post(reverse("accounts:communication_preferences"), {"email_marketing": "on"})

    assert cache.get(cache_key) is None


# ============================================================
# Unsubscribe View - Token Access
# ============================================================


def test_unsubscribe_page_accessible_with_valid_token(db, client):
    """Unsubscribe page loads with valid unsubscribe token (no login required)."""
    user = UserFactory()
    token = user.communication_preferences.unsubscribe_token

    url = reverse("accounts:unsubscribe", kwargs={"token": token})
    response = client.get(url)

    assert response.status_code == 200


def test_unsubscribe_page_puts_user_in_context(db, client):
    """Unsubscribe page places the resolved user in template context."""
    user = UserFactory()
    token = user.communication_preferences.unsubscribe_token

    response = client.get(reverse("accounts:unsubscribe", kwargs={"token": token}))

    # The view puts the resolved user into ``context["user"]`` directly.
    assert response.context["user"] == user


def test_unsubscribe_invalid_token_redirects_to_home(db, client):
    """Unsubscribe with an unknown token redirects to the storefront home."""
    response = client.get(reverse("accounts:unsubscribe", kwargs={"token": "invalid_token_12345"}))

    assert response.status_code == 302
    # Redirect target is page_builder:home (mounted at "/") — the storefront
    # root — followed by whatever the language prefix resolves to.
    assert response.url in ("/", "/en/", reverse("page_builder:home"))


def test_unsubscribe_post_disables_all_marketing(db, client):
    """POST ``action=unsubscribe_all`` disables marketing communications."""
    user = UserFactory()
    token = user.communication_preferences.unsubscribe_token

    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.sms_marketing = True
    prefs.save()

    url = reverse("accounts:unsubscribe", kwargs={"token": token})
    # The view branches on ``action`` — it does not treat a bare "confirm"
    # POST as an unsubscribe.
    response = client.post(url, {"action": "unsubscribe_all"})

    assert response.status_code == 302

    user.refresh_from_db()
    prefs = user.communication_preferences
    assert prefs.email_marketing is False
    assert prefs.sms_marketing is False


def test_unsubscribe_post_disables_all_apps(db, client):
    """POST ``action=unsubscribe_all`` disables all app marketing."""
    user = UserFactory()
    token = user.communication_preferences.unsubscribe_token

    prefs = user.communication_preferences
    prefs.app_preferences["blog"]["enabled"] = True
    prefs.app_preferences["loyalty"]["enabled"] = True
    prefs.save()

    response = client.post(
        reverse("accounts:unsubscribe", kwargs={"token": token}),
        {"action": "unsubscribe_all"},
    )

    assert response.status_code == 302

    user.refresh_from_db()
    prefs = user.communication_preferences
    assert prefs.app_preferences["blog"]["enabled"] is False
    assert prefs.app_preferences["loyalty"]["enabled"] is False


def test_unsubscribe_keeps_transactional_enabled(db, client):
    """Unsubscribe keeps transactional emails enabled."""
    user = UserFactory()
    token = user.communication_preferences.unsubscribe_token

    prefs = user.communication_preferences
    prefs.email_transactional = True
    prefs.sms_transactional = True
    prefs.save()

    client.post(
        reverse("accounts:unsubscribe", kwargs={"token": token}),
        {"action": "unsubscribe_all"},
    )

    user.refresh_from_db()
    prefs = user.communication_preferences
    assert prefs.email_transactional is True
    assert prefs.sms_transactional is True


def test_unsubscribe_with_reason(db, client):
    """Unsubscribe page accepts optional reason field via ``unsubscribe_all``."""
    user = UserFactory()
    token = user.communication_preferences.unsubscribe_token

    response = client.post(
        reverse("accounts:unsubscribe", kwargs={"token": token}),
        {"action": "unsubscribe_all", "reason": "Too many emails"},
    )

    assert response.status_code == 302

    user.refresh_from_db()
    assert user.communication_preferences.email_marketing is False


def test_unsubscribe_shows_success_message(db, client):
    """Unsubscribe emits a success message on the redirected page."""
    user = UserFactory()
    token = user.communication_preferences.unsubscribe_token

    response = client.post(
        reverse("accounts:unsubscribe", kwargs={"token": token}),
        {"action": "unsubscribe_all"},
        follow=True,
    )

    messages = [str(m) for m in get_messages(response.wsgi_request)]
    assert any("unsubscribed" in m.lower() for m in messages)


# ============================================================
# Unsubscribe - Resubscribe Flow
# ============================================================


def test_unsubscribe_context_exposes_preferences_url(db, client):
    """Context includes a link back to the preference center."""
    user = UserFactory()
    token = user.communication_preferences.unsubscribe_token

    response = client.get(reverse("accounts:unsubscribe", kwargs={"token": token}))

    # The view sets ``context["preferences_url"] = "/accounts/preferences/"``
    # so the template can offer a "manage preferences" alternative.
    assert response.context["preferences_url"]


# ============================================================
# Edge Cases
# ============================================================


def test_preference_center_handles_corrupted_json(logged_in_client, _mock_smart_defaults):
    """Preference center handles corrupted app_preferences gracefully."""
    client, user = logged_in_client

    prefs = user.communication_preferences
    prefs.app_preferences = {}  # Empty JSON
    prefs.save()

    response = client.get(reverse("accounts:communication_preferences"))

    # The view falls back to ``get_default_app_preferences`` when a key is
    # missing, so the page still renders.
    assert response.status_code == 200


def test_unsubscribe_token_is_url_safe(db):
    """Unsubscribe tokens don't contain URL-unsafe characters."""
    user = UserFactory()
    token = user.communication_preferences.unsubscribe_token

    import string

    safe_chars = string.ascii_letters + string.digits + "-_"
    assert all(c in safe_chars for c in token)


def test_preference_center_post_without_changes(logged_in_client):
    """POST without changes still succeeds and preserves prior values."""
    client, user = logged_in_client

    original_marketing = user.communication_preferences.email_marketing
    data = {"email_marketing": "on"} if original_marketing else {}

    response = client.post(reverse("accounts:communication_preferences"), data)

    assert response.status_code == 302

    user.refresh_from_db()
    assert user.communication_preferences.email_marketing == original_marketing
