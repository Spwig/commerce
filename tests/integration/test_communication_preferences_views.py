"""
Communication Preferences View Tests.

Tests customer-facing preference center and unsubscribe page views.
"""
import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.messages import get_messages

from accounts.models import CommunicationPreference
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


# ============================================================
# Preference Center View - GET
# ============================================================

def test_preference_center_requires_login(client):
    """Preference center redirects unauthenticated users to login."""
    url = reverse('accounts:communication_preferences')
    response = client.get(url)

    assert response.status_code == 302
    assert '/account/login/' in response.url


def test_preference_center_displays_for_authenticated_user(logged_in_client):
    """Preference center loads for authenticated user."""
    client, user = logged_in_client
    url = reverse('accounts:communication_preferences')

    response = client.get(url)

    assert response.status_code == 200
    assert 'Communication Preferences' in response.content.decode()


def test_preference_center_shows_current_preferences(logged_in_client):
    """Preference center displays user's current preference values."""
    client, user = logged_in_client

    # Set custom preferences
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.sms_transactional = True
    prefs.app_preferences['blog']['frequency'] = 'immediate'
    prefs.save()

    url = reverse('accounts:communication_preferences')
    response = client.get(url)
    content = response.content.decode()

    # Check that values are reflected in page
    assert response.status_code == 200
    # Marketing checkbox should be checked
    assert 'checked' in content  # At least some checkboxes checked


def test_preference_center_shows_verification_badge(logged_in_client):
    """Preference center shows verification status."""
    client, user = logged_in_client

    prefs = user.communication_preferences
    prefs.email_verified = True
    prefs.save()

    url = reverse('accounts:communication_preferences')
    response = client.get(url)
    content = response.content.decode()

    assert 'verified' in content.lower() or 'Verified' in content


def test_preference_center_creates_preference_if_missing(logged_in_client):
    """Preference center auto-creates preference if missing."""
    client, user = logged_in_client

    # Delete preference
    if hasattr(user, 'communication_preferences'):
        user.communication_preferences.delete()

    url = reverse('accounts:communication_preferences')
    response = client.get(url)

    # Should still load successfully
    assert response.status_code == 200

    # Preference should be created
    user.refresh_from_db()
    assert hasattr(user, 'communication_preferences')


# ============================================================
# Preference Center View - POST
# ============================================================

def test_preference_center_update_email_marketing(logged_in_client):
    """POST to preference center updates email_marketing."""
    client, user = logged_in_client
    url = reverse('accounts:communication_preferences')

    response = client.post(url, {
        'email_marketing': 'on',
    })

    # Should redirect on success
    assert response.status_code == 302

    # Verify preference updated
    user.refresh_from_db()
    assert user.communication_preferences.email_marketing is True


def test_preference_center_update_unchecked_checkbox(logged_in_client):
    """POST with unchecked checkbox sets value to False."""
    client, user = logged_in_client

    # Enable marketing first
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.save()

    url = reverse('accounts:communication_preferences')
    # Don't include email_marketing in POST data (unchecked)
    response = client.post(url, {
        'email_transactional': 'on',
    })

    assert response.status_code == 302

    # email_marketing should be False now
    user.refresh_from_db()
    assert user.communication_preferences.email_marketing is False


def test_preference_center_update_app_preferences(logged_in_client):
    """POST updates app-specific preferences."""
    client, user = logged_in_client
    url = reverse('accounts:communication_preferences')

    response = client.post(url, {
        'blog_enabled': 'on',
        'blog_frequency': 'immediate',
        'loyalty_enabled': 'on',
        'loyalty_points_earned': 'on',
    })

    assert response.status_code == 302

    # Verify app_preferences updated
    user.refresh_from_db()
    prefs = user.communication_preferences
    assert prefs.app_preferences['blog']['enabled'] is True
    assert prefs.app_preferences['blog']['frequency'] == 'immediate'
    assert prefs.app_preferences['loyalty']['enabled'] is True
    assert prefs.app_preferences['loyalty']['points_earned'] is True


def test_preference_center_update_shows_success_message(logged_in_client):
    """POST shows success message after update."""
    client, user = logged_in_client
    url = reverse('accounts:communication_preferences')

    response = client.post(url, {
        'email_marketing': 'on',
    }, follow=True)

    # Check for success message
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0
    assert 'updated' in str(messages[0]).lower()


def test_preference_center_update_invalidates_cache(logged_in_client):
    """POST invalidates preference cache."""
    client, user = logged_in_client
    from django.core.cache import cache

    # Populate cache
    from accounts.services.preference_service import PreferenceService
    PreferenceService.check_email_permission(user, 'newsletter')

    cache_key = f'comm_pref_{user.id}'
    assert cache.get(cache_key) is not None

    # Update via form
    url = reverse('accounts:communication_preferences')
    client.post(url, {'email_marketing': 'on'})

    # Cache should be cleared
    assert cache.get(cache_key) is None


# ============================================================
# Unsubscribe View - Token Access
# ============================================================

def test_unsubscribe_page_accessible_with_valid_token(db, client):
    """Unsubscribe page loads with valid unsubscribe token (no login required)."""
    user = UserFactory()
    token = user.communication_preferences.unsubscribe_token

    url = reverse('accounts:unsubscribe', kwargs={'token': token})
    response = client.get(url)

    assert response.status_code == 200
    assert 'unsubscribe' in response.content.decode().lower()


def test_unsubscribe_page_shows_user_email(db, client):
    """Unsubscribe page displays user's email address."""
    user = UserFactory()
    token = user.communication_preferences.unsubscribe_token

    url = reverse('accounts:unsubscribe', kwargs={'token': token})
    response = client.get(url)
    content = response.content.decode()

    assert user.email in content


def test_unsubscribe_invalid_token_returns_404(db, client):
    """Unsubscribe page returns 404 for invalid token."""
    url = reverse('accounts:unsubscribe', kwargs={'token': 'invalid_token_12345'})
    response = client.get(url)

    assert response.status_code == 404


def test_unsubscribe_post_disables_marketing(db, client):
    """POST to unsubscribe disables marketing communications."""
    user = UserFactory()
    token = user.communication_preferences.unsubscribe_token

    # Enable marketing first
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.sms_marketing = True
    prefs.save()

    url = reverse('accounts:unsubscribe', kwargs={'token': token})
    response = client.post(url, {
        'confirm': 'yes',
    })

    # Should redirect on success
    assert response.status_code == 302

    # Verify marketing disabled
    user.refresh_from_db()
    prefs = user.communication_preferences
    assert prefs.email_marketing is False
    assert prefs.sms_marketing is False


def test_unsubscribe_post_disables_all_apps(db, client):
    """POST to unsubscribe disables all app marketing."""
    user = UserFactory()
    token = user.communication_preferences.unsubscribe_token

    # Enable apps
    prefs = user.communication_preferences
    prefs.app_preferences['blog']['enabled'] = True
    prefs.app_preferences['loyalty']['enabled'] = True
    prefs.save()

    url = reverse('accounts:unsubscribe', kwargs={'token': token})
    response = client.post(url, {'confirm': 'yes'})

    assert response.status_code == 302

    # Verify apps disabled
    user.refresh_from_db()
    prefs = user.communication_preferences
    assert prefs.app_preferences['blog']['enabled'] is False
    assert prefs.app_preferences['loyalty']['enabled'] is False


def test_unsubscribe_keeps_transactional_enabled(db, client):
    """Unsubscribe keeps transactional emails enabled."""
    user = UserFactory()
    token = user.communication_preferences.unsubscribe_token

    # Enable transactional
    prefs = user.communication_preferences
    prefs.email_transactional = True
    prefs.sms_transactional = True
    prefs.save()

    url = reverse('accounts:unsubscribe', kwargs={'token': token})
    response = client.post(url, {'confirm': 'yes'})

    # Transactional should still be enabled
    user.refresh_from_db()
    prefs = user.communication_preferences
    assert prefs.email_transactional is True
    assert prefs.sms_transactional is True


def test_unsubscribe_with_reason(db, client):
    """Unsubscribe page accepts optional reason."""
    user = UserFactory()
    token = user.communication_preferences.unsubscribe_token

    url = reverse('accounts:unsubscribe', kwargs={'token': token})
    response = client.post(url, {
        'confirm': 'yes',
        'reason': 'Too many emails',
    })

    assert response.status_code == 302

    # Reason should be stored (if implemented)
    # For now, just verify unsubscribe worked
    user.refresh_from_db()
    assert user.communication_preferences.email_marketing is False


def test_unsubscribe_shows_success_message(db, client):
    """Unsubscribe shows confirmation message."""
    user = UserFactory()
    token = user.communication_preferences.unsubscribe_token

    url = reverse('accounts:unsubscribe', kwargs={'token': token})
    response = client.post(url, {'confirm': 'yes'}, follow=True)

    # Check for success message
    content = response.content.decode()
    assert 'unsubscribed' in content.lower() or 'success' in content.lower()


# ============================================================
# Unsubscribe - Resubscribe Flow
# ============================================================

def test_unsubscribe_page_shows_resubscribe_option(db, client):
    """Unsubscribe page shows option to manage preferences instead."""
    user = UserFactory()
    token = user.communication_preferences.unsubscribe_token

    url = reverse('accounts:unsubscribe', kwargs={'token': token})
    response = client.get(url)
    content = response.content.decode()

    # Should mention preference center
    assert 'preference' in content.lower() or 'manage' in content.lower()


# ============================================================
# Edge Cases
# ============================================================

def test_preference_center_handles_corrupted_json(logged_in_client):
    """Preference center handles corrupted app_preferences gracefully."""
    client, user = logged_in_client

    # Corrupt app_preferences
    prefs = user.communication_preferences
    prefs.app_preferences = {}  # Empty JSON
    prefs.save()

    url = reverse('accounts:communication_preferences')
    response = client.get(url)

    # Should still load, not crash
    assert response.status_code == 200


def test_unsubscribe_token_is_url_safe(db):
    """Unsubscribe tokens don't contain URL-unsafe characters."""
    user = UserFactory()
    token = user.communication_preferences.unsubscribe_token

    # Should not contain characters that need URL encoding
    import string
    safe_chars = string.ascii_letters + string.digits + '-_'
    assert all(c in safe_chars for c in token)


def test_preference_center_post_without_changes(logged_in_client):
    """POST without changes still succeeds."""
    client, user = logged_in_client

    # Get current state
    original_prefs = user.communication_preferences
    original_marketing = original_prefs.email_marketing

    url = reverse('accounts:communication_preferences')
    # Submit same values
    if original_marketing:
        data = {'email_marketing': 'on'}
    else:
        data = {}

    response = client.post(url, data)

    assert response.status_code == 302

    # Values should be unchanged
    user.refresh_from_db()
    assert user.communication_preferences.email_marketing == original_marketing
