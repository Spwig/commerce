"""
Communication Preferences API Tests.

Tests REST API endpoints for retrieving and updating communication preferences.
The API lives under the ``accounts_api`` namespace at ``/api/accounts/`` and
uses refresh-token session/JWT auth (the DRF default of ``IsAuthenticated``).

Response shape:

* ``GET  /api/accounts/communication-preferences/``
  → ``{"success": True, "data": {<serialized preference>}}``
* ``POST /api/accounts/communication-preferences/update/``
  → ``{"success": True, "message": "..."}`` on 200,
    ``{"success": False, "errors": {...}}`` on 400
* ``POST /api/accounts/communication-preferences/bulk-update/``
  → same shape (400 if the ``updates`` list is empty — the serializer
    enforces ``allow_empty=False``)
* ``POST /api/accounts/communication-preferences/unsubscribe-all/``
  → ``{"success": True, "message": "..."}``
"""

import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.services.preference_service import PreferenceService
from tests.factories import UserFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.preferences_api]


# ============================================================
# URL name constants (keep tests independent of admin cleanup)
# ============================================================

GET_URL = "accounts_api:communication_preferences_get"
UPDATE_URL = "accounts_api:communication_preference_update"
BULK_UPDATE_URL = "accounts_api:communication_preferences_bulk_update"
UNSUBSCRIBE_URL = "accounts_api:unsubscribe_all"


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture(autouse=True)
def _clear_cache():
    """PreferenceService caches heavily — start each test with an empty cache."""
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def api_client():
    """REST framework API client."""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    """API client with an authenticated customer user."""
    user = UserFactory()
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.fixture
def user_with_custom_prefs(db):
    """User with customized preferences."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.sms_transactional = True
    prefs.app_preferences["blog"]["frequency"] = "immediate"
    prefs.app_preferences["loyalty"]["campaign_offers"] = True
    prefs.save()
    return user


# ============================================================
# GET /api/accounts/communication-preferences/
# ============================================================


def test_get_preferences_requires_authentication(api_client):
    """GET preferences endpoint requires authentication."""
    response = api_client.get(reverse(GET_URL))
    # DRF returns 401 or 403 depending on auth class order — either is a valid
    # rejection here. Both indicate the endpoint is not open to anonymous.
    assert response.status_code in (
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    )


def test_get_preferences_returns_user_preferences(authenticated_client):
    """GET returns authenticated user's preferences."""
    api_client, _user = authenticated_client
    response = api_client.get(reverse(GET_URL))

    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert payload["success"] is True
    data = payload["data"]

    # Check structure
    assert "email_enabled" in data
    assert "sms_enabled" in data
    assert "email_transactional" in data
    assert "email_marketing" in data
    assert "sms_transactional" in data
    assert "sms_marketing" in data
    assert "app_preferences" in data
    assert "email_categories" in data

    # Check defaults
    assert data["email_enabled"] is True
    assert data["email_marketing"] is False  # GDPR opt-out
    assert data["sms_enabled"] is False  # TCPA opt-in required


def test_get_preferences_returns_email_categories(authenticated_client):
    """GET returns structured ``email_categories`` for UI consumption."""
    api_client, _user = authenticated_client
    response = api_client.get(reverse(GET_URL))
    data = response.json()["data"]

    categories = data["email_categories"]

    # Baseline categories the serializer always emits
    assert "transactional" in categories
    assert "marketing" in categories

    # App groupings mirror app_preferences
    assert "blog" in categories
    assert "loyalty" in categories
    assert "referrals" in categories
    assert "affiliate" in categories


def test_get_preferences_returns_custom_values(api_client, user_with_custom_prefs):
    """GET returns customized preference values."""
    api_client.force_authenticate(user=user_with_custom_prefs)
    response = api_client.get(reverse(GET_URL))
    data = response.json()["data"]

    assert data["email_marketing"] is True
    assert data["email_verified"] is True
    assert data["sms_transactional"] is True
    assert data["app_preferences"]["blog"]["frequency"] == "immediate"
    assert data["app_preferences"]["loyalty"]["campaign_offers"] is True


# ============================================================
# POST /api/accounts/communication-preferences/update/
# ============================================================


def test_update_preference_requires_authentication(api_client):
    """POST update endpoint requires authentication."""
    response = api_client.post(reverse(UPDATE_URL), {}, format="json")
    assert response.status_code in (
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    )


def test_update_preference_email_marketing(authenticated_client):
    """POST updates ``email_marketing`` via a marketing message type."""
    api_client, user = authenticated_client

    # ``newsletter`` is a marketing email type — the service maps it to
    # ``email_marketing`` on the preference row.
    response = api_client.post(
        reverse(UPDATE_URL),
        {"channel": "email", "message_type": "newsletter", "enabled": True},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True

    user.refresh_from_db()
    assert user.communication_preferences.email_marketing is True


def test_update_preference_sms_transactional(authenticated_client):
    """POST updates ``sms_transactional`` for a transactional SMS type."""
    api_client, user = authenticated_client

    response = api_client.post(
        reverse(UPDATE_URL),
        # ``order_shipped`` is a transactional SMS type per accounts.constants.
        {"channel": "sms", "message_type": "order_shipped", "enabled": True},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()
    assert user.communication_preferences.sms_transactional is True


def test_update_preference_app_specific(authenticated_client):
    """POST updates app-specific preferences via app message types."""
    api_client, user = authenticated_client

    # ``blog_post_published`` is an app-specific type; the service extracts
    # the key ``post_published`` from the message name.
    response = api_client.post(
        reverse(UPDATE_URL),
        {"channel": "email", "message_type": "blog_post_published", "enabled": False},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()
    assert user.communication_preferences.app_preferences["blog"]["post_published"] is False


def test_update_preference_with_frequency(authenticated_client):
    """POST updates preference with optional ``frequency`` parameter."""
    api_client, user = authenticated_client

    response = api_client.post(
        reverse(UPDATE_URL),
        {
            "channel": "email",
            "message_type": "blog_weekly_digest",
            "enabled": True,
            "frequency": "immediate",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()
    prefs = user.communication_preferences
    assert prefs.app_preferences["blog"]["weekly_digest"] is True
    assert prefs.app_preferences["blog"]["frequency"] == "immediate"


def test_update_preference_validates_channel(authenticated_client):
    """POST rejects unsupported channel values."""
    api_client, _user = authenticated_client
    response = api_client.post(
        reverse(UPDATE_URL),
        {"channel": "invalid_channel", "message_type": "newsletter", "enabled": True},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_preference_invalidates_cache(authenticated_client):
    """POST invalidates preference cache after update."""
    api_client, user = authenticated_client

    # Populate cache by making a permission check.
    PreferenceService.check_email_permission(user, "newsletter")

    # Sanity: the cache entry PreferenceService uses is keyed per message type.
    assert cache.get(f"email_pref:{user.id}:newsletter") is not None

    # Update the same preference.
    api_client.post(
        reverse(UPDATE_URL),
        {"channel": "email", "message_type": "newsletter", "enabled": True},
        format="json",
    )

    # Cache entry for the newsletter message type should be gone.
    assert cache.get(f"email_pref:{user.id}:newsletter") is None


# ============================================================
# POST /api/accounts/communication-preferences/bulk-update/
# ============================================================


def test_bulk_update_requires_authentication(api_client):
    """POST bulk update requires authentication."""
    response = api_client.post(reverse(BULK_UPDATE_URL), {}, format="json")
    assert response.status_code in (
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    )


def test_bulk_update_multiple_preferences(authenticated_client):
    """POST bulk-updates multiple preferences at once."""
    api_client, user = authenticated_client

    response = api_client.post(
        reverse(BULK_UPDATE_URL),
        {
            "updates": [
                {"channel": "email", "message_type": "newsletter", "enabled": True},
                {"channel": "sms", "message_type": "order_shipped", "enabled": True},
                {"channel": "email", "message_type": "blog_post_published", "enabled": False},
            ]
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True

    user.refresh_from_db()
    prefs = user.communication_preferences
    assert prefs.email_marketing is True
    assert prefs.sms_transactional is True
    assert prefs.app_preferences["blog"]["post_published"] is False


def test_bulk_update_partial_failure_returns_400(authenticated_client):
    """POST bulk update reports errors when any nested update fails validation."""
    api_client, _user = authenticated_client

    # Second update has an invalid ``channel`` — the nested serializer will
    # reject the whole payload before any change is applied.
    response = api_client.post(
        reverse(BULK_UPDATE_URL),
        {
            "updates": [
                {"channel": "email", "message_type": "newsletter", "enabled": True},
                {"channel": "invalid", "message_type": "bad", "enabled": True},
            ]
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_bulk_update_empty_list_rejected(authenticated_client):
    """The bulk serializer enforces ``allow_empty=False``, so an empty list is invalid."""
    api_client, _user = authenticated_client
    response = api_client.post(reverse(BULK_UPDATE_URL), {"updates": []}, format="json")

    # ``BulkPreferenceUpdateSerializer.updates`` uses ``allow_empty=False``,
    # so an empty list is a validation error, not a no-op success.
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# ============================================================
# POST /api/accounts/communication-preferences/unsubscribe-all/
# ============================================================


def test_unsubscribe_all_requires_authentication(api_client):
    """POST unsubscribe-all requires authentication."""
    response = api_client.post(reverse(UNSUBSCRIBE_URL))
    assert response.status_code in (
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    )


def test_unsubscribe_all_disables_marketing(authenticated_client):
    """POST unsubscribe-all disables all marketing communications."""
    api_client, user = authenticated_client

    # Enable everything first
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.sms_marketing = True
    prefs.app_preferences["blog"]["enabled"] = True
    prefs.app_preferences["loyalty"]["campaign_offers"] = True
    prefs.save()

    response = api_client.post(reverse(UNSUBSCRIBE_URL))

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True

    user.refresh_from_db()
    prefs = user.communication_preferences
    assert prefs.email_marketing is False
    assert prefs.sms_marketing is False
    assert prefs.app_preferences["blog"]["enabled"] is False
    assert prefs.app_preferences["loyalty"]["enabled"] is False
    assert prefs.app_preferences["referrals"]["enabled"] is False
    assert prefs.app_preferences["affiliate"]["enabled"] is False


def test_unsubscribe_all_keeps_transactional_enabled(authenticated_client):
    """POST unsubscribe-all keeps transactional emails enabled."""
    api_client, user = authenticated_client

    prefs = user.communication_preferences
    prefs.email_transactional = True
    prefs.sms_transactional = True
    prefs.save()

    response = api_client.post(reverse(UNSUBSCRIBE_URL))
    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()
    prefs = user.communication_preferences
    assert prefs.email_transactional is True
    assert prefs.sms_transactional is True


def test_unsubscribe_all_invalidates_cache(authenticated_client):
    """POST unsubscribe-all invalidates cached permission checks."""
    api_client, user = authenticated_client

    # Populate cache.
    PreferenceService.check_email_permission(user, "newsletter")
    assert cache.get(f"email_pref:{user.id}:newsletter") is not None

    # Unsubscribe all — the service walks ALL_EMAIL_TYPES / ALL_SMS_TYPES
    # to invalidate every key for the user.
    api_client.post(reverse(UNSUBSCRIBE_URL))

    # Every message-type cache entry for this user should be gone.
    assert cache.get(f"email_pref:{user.id}:newsletter") is None


# ============================================================
# Edge Cases
# ============================================================


def test_update_preference_creates_if_missing(authenticated_client):
    """POST creates ``CommunicationPreference`` if it was previously deleted."""
    api_client, user = authenticated_client

    # Delete preference so the view has to recreate it.
    user.communication_preferences.delete()

    response = api_client.post(
        reverse(UPDATE_URL),
        {"channel": "email", "message_type": "newsletter", "enabled": True},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    # PreferenceService.get_or_create_for_user should have recreated it.
    user.refresh_from_db()
    assert user.communication_preferences.email_marketing is True


def test_get_preferences_handles_missing_app_keys(authenticated_client):
    """GET tolerates a preference row with an empty ``app_preferences`` blob."""
    api_client, user = authenticated_client

    prefs = user.communication_preferences
    prefs.app_preferences = {"blog": {}}  # Missing keys
    prefs.save()

    response = api_client.get(reverse(GET_URL))

    # The serializer defaults missing app blobs to ``{}`` rather than crashing.
    assert response.status_code == status.HTTP_200_OK
