"""
Communication Preferences API Tests.

Tests REST API endpoints for retrieving and updating communication preferences.
"""
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import CommunicationPreference
from tests.factories import UserFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.preferences_api]


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def api_client():
    """REST framework API client."""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    """API client with authenticated user."""
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
    prefs.app_preferences['blog']['frequency'] = 'immediate'
    prefs.app_preferences['loyalty']['campaign_offers'] = True
    prefs.save()
    return user


# ============================================================
# GET /api/accounts/communication-preferences/
# ============================================================

def test_get_preferences_requires_authentication(api_client):
    """GET preferences endpoint requires authentication."""
    url = reverse('accounts:communication_preferences_get')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_preferences_returns_user_preferences(authenticated_client):
    """GET returns authenticated user's preferences."""
    api_client, user = authenticated_client
    url = reverse('accounts:communication_preferences_get')

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Check structure
    assert 'email_enabled' in data
    assert 'sms_enabled' in data
    assert 'email_transactional' in data
    assert 'email_marketing' in data
    assert 'sms_transactional' in data
    assert 'sms_marketing' in data
    assert 'app_preferences' in data
    assert 'email_categories' in data

    # Check defaults
    assert data['email_enabled'] is True
    assert data['email_marketing'] is False  # GDPR opt-out
    assert data['sms_enabled'] is False  # TCPA opt-in required


def test_get_preferences_returns_email_categories(authenticated_client):
    """GET returns structured email_categories for UI."""
    api_client, user = authenticated_client
    url = reverse('accounts:communication_preferences_get')

    response = api_client.get(url)
    data = response.json()

    # Should have email_categories grouping
    assert 'email_categories' in data
    categories = data['email_categories']

    assert 'transactional' in categories
    assert 'marketing' in categories
    assert 'blog' in categories
    assert 'loyalty' in categories
    assert 'referrals' in categories
    assert 'affiliate' in categories


def test_get_preferences_returns_custom_values(api_client, user_with_custom_prefs):
    """GET returns customized preference values."""
    api_client.force_authenticate(user=user_with_custom_prefs)
    url = reverse('accounts:communication_preferences_get')

    response = api_client.get(url)
    data = response.json()

    assert data['email_marketing'] is True
    assert data['email_verified'] is True
    assert data['sms_transactional'] is True
    assert data['app_preferences']['blog']['frequency'] == 'immediate'
    assert data['app_preferences']['loyalty']['campaign_offers'] is True


# ============================================================
# POST /api/accounts/communication-preferences/update/
# ============================================================

def test_update_preference_requires_authentication(api_client):
    """POST update endpoint requires authentication."""
    url = reverse('accounts:communication_preferences_update')
    response = api_client.post(url, {})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_preference_email_marketing(authenticated_client):
    """POST updates email_marketing preference."""
    api_client, user = authenticated_client
    url = reverse('accounts:communication_preferences_update')

    response = api_client.post(url, {
        'channel': 'email',
        'message_type': 'marketing',
        'enabled': True,
    }, format='json')

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['success'] is True

    # Verify preference updated
    user.refresh_from_db()
    assert user.communication_preferences.email_marketing is True


def test_update_preference_sms_transactional(authenticated_client):
    """POST updates sms_transactional preference."""
    api_client, user = authenticated_client
    url = reverse('accounts:communication_preferences_update')

    response = api_client.post(url, {
        'channel': 'sms',
        'message_type': 'transactional',
        'enabled': True,
    }, format='json')

    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()
    assert user.communication_preferences.sms_transactional is True


def test_update_preference_app_specific(authenticated_client):
    """POST updates app-specific preferences."""
    api_client, user = authenticated_client
    url = reverse('accounts:communication_preferences_update')

    response = api_client.post(url, {
        'channel': 'email',
        'message_type': 'blog',
        'enabled': False,
    }, format='json')

    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()
    assert user.communication_preferences.app_preferences['blog']['enabled'] is False


def test_update_preference_with_frequency(authenticated_client):
    """POST updates preference with frequency parameter."""
    api_client, user = authenticated_client
    url = reverse('accounts:communication_preferences_update')

    response = api_client.post(url, {
        'channel': 'email',
        'message_type': 'blog',
        'enabled': True,
        'frequency': 'immediate',
    }, format='json')

    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()
    prefs = user.communication_preferences
    assert prefs.app_preferences['blog']['enabled'] is True
    assert prefs.app_preferences['blog']['frequency'] == 'immediate'


def test_update_preference_validates_channel(authenticated_client):
    """POST validates channel parameter."""
    api_client, user = authenticated_client
    url = reverse('accounts:communication_preferences_update')

    response = api_client.post(url, {
        'channel': 'invalid_channel',
        'message_type': 'marketing',
        'enabled': True,
    }, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_preference_invalidates_cache(authenticated_client):
    """POST invalidates preference cache after update."""
    api_client, user = authenticated_client
    from django.core.cache import cache

    # Populate cache
    from accounts.services.preference_service import PreferenceService
    PreferenceService.check_email_permission(user, 'newsletter')

    cache_key = f'comm_pref_{user.id}'
    assert cache.get(cache_key) is not None

    # Update preference
    url = reverse('accounts:communication_preferences_update')
    api_client.post(url, {
        'channel': 'email',
        'message_type': 'marketing',
        'enabled': True,
    }, format='json')

    # Cache should be cleared
    assert cache.get(cache_key) is None


# ============================================================
# POST /api/accounts/communication-preferences/bulk-update/
# ============================================================

def test_bulk_update_requires_authentication(api_client):
    """POST bulk update requires authentication."""
    url = reverse('accounts:communication_preferences_bulk_update')
    response = api_client.post(url, {})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_bulk_update_multiple_preferences(authenticated_client):
    """POST bulk updates multiple preferences at once."""
    api_client, user = authenticated_client
    url = reverse('accounts:communication_preferences_bulk_update')

    response = api_client.post(url, {
        'updates': [
            {'channel': 'email', 'message_type': 'marketing', 'enabled': True},
            {'channel': 'sms', 'message_type': 'transactional', 'enabled': True},
            {'channel': 'email', 'message_type': 'blog', 'enabled': False},
        ]
    }, format='json')

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['success'] is True

    # Verify all updates applied
    user.refresh_from_db()
    prefs = user.communication_preferences
    assert prefs.email_marketing is True
    assert prefs.sms_transactional is True
    assert prefs.app_preferences['blog']['enabled'] is False


def test_bulk_update_partial_failure_rollback(authenticated_client):
    """POST bulk update rolls back all changes on validation error."""
    api_client, user = authenticated_client
    url = reverse('accounts:communication_preferences_bulk_update')

    # Include one invalid update
    response = api_client.post(url, {
        'updates': [
            {'channel': 'email', 'message_type': 'marketing', 'enabled': True},
            {'channel': 'invalid', 'message_type': 'bad', 'enabled': True},
        ]
    }, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # First update should NOT be applied (rollback)
    user.refresh_from_db()
    assert user.communication_preferences.email_marketing is False


def test_bulk_update_empty_list(authenticated_client):
    """POST bulk update with empty list returns success."""
    api_client, user = authenticated_client
    url = reverse('accounts:communication_preferences_bulk_update')

    response = api_client.post(url, {'updates': []}, format='json')

    assert response.status_code == status.HTTP_200_OK


# ============================================================
# POST /api/accounts/communication-preferences/unsubscribe-all/
# ============================================================

def test_unsubscribe_all_requires_authentication(api_client):
    """POST unsubscribe-all requires authentication."""
    url = reverse('accounts:communication_preferences_unsubscribe_all')
    response = api_client.post(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_unsubscribe_all_disables_marketing(authenticated_client):
    """POST unsubscribe-all disables all marketing communications."""
    api_client, user = authenticated_client

    # Enable everything first
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.sms_marketing = True
    prefs.app_preferences['blog']['enabled'] = True
    prefs.app_preferences['loyalty']['campaign_offers'] = True
    prefs.save()

    url = reverse('accounts:communication_preferences_unsubscribe_all')
    response = api_client.post(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['success'] is True

    # Verify all marketing disabled
    user.refresh_from_db()
    prefs = user.communication_preferences
    assert prefs.email_marketing is False
    assert prefs.sms_marketing is False
    assert prefs.app_preferences['blog']['enabled'] is False
    assert prefs.app_preferences['loyalty']['enabled'] is False
    assert prefs.app_preferences['referrals']['enabled'] is False
    assert prefs.app_preferences['affiliate']['enabled'] is False


def test_unsubscribe_all_keeps_transactional_enabled(authenticated_client):
    """POST unsubscribe-all keeps transactional emails enabled."""
    api_client, user = authenticated_client

    # Enable transactional
    prefs = user.communication_preferences
    prefs.email_transactional = True
    prefs.sms_transactional = True
    prefs.save()

    url = reverse('accounts:communication_preferences_unsubscribe_all')
    response = api_client.post(url)

    assert response.status_code == status.HTTP_200_OK

    # Transactional should still be enabled
    user.refresh_from_db()
    prefs = user.communication_preferences
    assert prefs.email_transactional is True
    assert prefs.sms_transactional is True


def test_unsubscribe_all_invalidates_cache(authenticated_client):
    """POST unsubscribe-all invalidates preference cache."""
    api_client, user = authenticated_client
    from django.core.cache import cache

    # Populate cache
    from accounts.services.preference_service import PreferenceService
    PreferenceService.check_email_permission(user, 'newsletter')

    cache_key = f'comm_pref_{user.id}'
    assert cache.get(cache_key) is not None

    # Unsubscribe all
    url = reverse('accounts:communication_preferences_unsubscribe_all')
    api_client.post(url)

    # Cache should be cleared
    assert cache.get(cache_key) is None


# ============================================================
# Edge Cases
# ============================================================

def test_update_preference_creates_if_missing(authenticated_client):
    """POST creates CommunicationPreference if it doesn't exist."""
    api_client, user = authenticated_client

    # Delete preference
    if hasattr(user, 'communication_preferences'):
        user.communication_preferences.delete()

    url = reverse('accounts:communication_preferences_update')
    response = api_client.post(url, {
        'channel': 'email',
        'message_type': 'marketing',
        'enabled': True,
    }, format='json')

    assert response.status_code == status.HTTP_200_OK

    # Preference should be created
    user.refresh_from_db()
    assert hasattr(user, 'communication_preferences')


def test_get_preferences_handles_missing_app_keys(authenticated_client):
    """GET handles missing app_preference keys gracefully."""
    api_client, user = authenticated_client

    # Corrupt app_preferences
    prefs = user.communication_preferences
    prefs.app_preferences = {'blog': {}}  # Missing keys
    prefs.save()

    url = reverse('accounts:communication_preferences_get')
    response = api_client.get(url)

    # Should still return 200, not crash
    assert response.status_code == status.HTTP_200_OK
