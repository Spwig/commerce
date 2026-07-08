"""
POS Authentication integration tests.

Tests login, token refresh, and logout flows for the POS API,
including credential validation, role-based access, terminal config,
and token lifecycle management.
"""
import pytest
from datetime import timedelta
from django.utils import timezone
from rest_framework.test import APIClient

from tests.factories import UserFactory, MobileAuthTokenFactory
from tests.helpers import assert_pos_error, assert_pos_success

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.pos]

LOGIN_URL = '/api/pos/auth/login/'
REFRESH_URL = '/api/pos/auth/refresh/'
LOGOUT_URL = '/api/pos/auth/logout/'


# ============================================================
# TestPOSLogin
# ============================================================

class TestPOSLogin:
    """Tests for POST /api/pos/auth/login/."""

    def test_login_with_email_and_password(self, anon_client, pos_staff_user):
        """Valid login with email and password returns success with tokens and user profile."""
        response = anon_client.post(LOGIN_URL, {
            'email': pos_staff_user.email,
            'password': 'testpass123',
        })
        data = assert_pos_success(response, http_status=200)

        assert 'access_token' in data
        assert 'refresh_token' in data
        assert 'user' in data
        assert data['user']['email'] == pos_staff_user.email

    def test_login_with_username_fallback(self, anon_client, pos_staff_user):
        """Login using the username field instead of email still authenticates."""
        response = anon_client.post(LOGIN_URL, {
            'email': pos_staff_user.username,
            'password': 'testpass123',
        })
        data = assert_pos_success(response, http_status=200)
        assert data['user']['email'] == pos_staff_user.email

    def test_login_returns_tokens(self, anon_client, pos_staff_user):
        """Successful login returns both access_token and refresh_token strings."""
        response = anon_client.post(LOGIN_URL, {
            'email': pos_staff_user.email,
            'password': 'testpass123',
        })
        data = assert_pos_success(response)

        assert isinstance(data['access_token'], str)
        assert len(data['access_token']) > 20
        assert isinstance(data['refresh_token'], str)
        assert len(data['refresh_token']) > 20
        assert data['access_token'] != data['refresh_token']
        assert 'expires_at' in data

    def test_login_returns_user_profile(self, anon_client, pos_staff_user):
        """Response includes user object with id, email, first_name, last_name, full_name."""
        response = anon_client.post(LOGIN_URL, {
            'email': pos_staff_user.email,
            'password': 'testpass123',
        })
        data = assert_pos_success(response)

        user_data = data['user']
        assert user_data['id'] == pos_staff_user.id
        assert user_data['email'] == pos_staff_user.email
        assert user_data['first_name'] == pos_staff_user.first_name
        assert user_data['last_name'] == pos_staff_user.last_name
        assert 'full_name' in user_data

    def test_login_with_terminal_uuid(self, anon_client, pos_staff_user, pos_terminal):
        """When terminal_uuid is provided, response includes terminal config."""
        response = anon_client.post(LOGIN_URL, {
            'email': pos_staff_user.email,
            'password': 'testpass123',
            'terminal_uuid': str(pos_terminal.uuid),
        })
        data = assert_pos_success(response)

        assert data['terminal'] is not None
        assert data['terminal']['uuid'] == str(pos_terminal.uuid)
        assert data['terminal']['name'] == pos_terminal.name
        assert 'warehouse_id' in data['terminal']
        assert 'warehouse_name' in data['terminal']
        assert 'currency' in data['terminal']

    def test_login_without_terminal(self, anon_client, pos_staff_user):
        """When no terminal_uuid is sent, terminal config is null."""
        response = anon_client.post(LOGIN_URL, {
            'email': pos_staff_user.email,
            'password': 'testpass123',
        })
        data = assert_pos_success(response)
        assert data['terminal'] is None

    def test_login_returns_pos_permissions(self, anon_client, pos_staff_user):
        """Response includes permissions dict derived from the user's StaffRole."""
        response = anon_client.post(LOGIN_URL, {
            'email': pos_staff_user.email,
            'password': 'testpass123',
        })
        data = assert_pos_success(response)

        assert 'permissions' in data
        assert isinstance(data['permissions'], dict)
        # The cashier role has pos_access=True in its pos_permissions
        assert data['permissions'].get('pos_access') is True

    def test_login_invalid_password(self, anon_client, pos_staff_user):
        """Wrong password returns 401 with INVALID_CREDENTIALS error code."""
        response = anon_client.post(LOGIN_URL, {
            'email': pos_staff_user.email,
            'password': 'wrong_password',
        })
        assert_pos_error(response, 'INVALID_CREDENTIALS', http_status=401)

    def test_login_nonexistent_user(self, anon_client):
        """Non-existent email returns 401 with INVALID_CREDENTIALS error code."""
        response = anon_client.post(LOGIN_URL, {
            'email': 'nobody@nowhere.test',
            'password': 'testpass123',
        })
        assert_pos_error(response, 'INVALID_CREDENTIALS', http_status=401)

    def test_login_non_staff_user(self, anon_client, pos_cashier_group):
        """A regular user (is_staff=False) returns 403 NOT_STAFF."""
        regular_user = UserFactory(
            username='regular_shopper',
            email='shopper@test.spwig.com',
            is_staff=False,
        )
        # Even adding the POS group shouldn't help without is_staff
        regular_user.groups.add(pos_cashier_group)

        response = anon_client.post(LOGIN_URL, {
            'email': regular_user.email,
            'password': 'testpass123',
        })
        assert_pos_error(response, 'NOT_STAFF', http_status=403)

    def test_login_staff_without_pos_access(self, anon_client, db):
        """Staff user without any POS role returns 403 NO_POS_ACCESS."""
        from django.contrib.auth.models import Group
        from staff_roles.models import StaffRole

        # Create a group with can_access_pos=False
        group, _ = Group.objects.get_or_create(name='Admin Only')
        StaffRole.objects.update_or_create(
            group=group,
            defaults={
                'display_name': 'Admin Only',
                'can_access_pos': False,
                'pos_permissions': {},
            }
        )
        staff_no_pos = UserFactory(
            username='admin_only',
            email='adminonly@test.spwig.com',
            is_staff=True,
        )
        staff_no_pos.groups.add(group)

        response = anon_client.post(LOGIN_URL, {
            'email': staff_no_pos.email,
            'password': 'testpass123',
        })
        assert_pos_error(response, 'NO_POS_ACCESS', http_status=403)

    def test_login_missing_credentials(self, anon_client):
        """Request with no email/password returns 400 MISSING_CREDENTIALS."""
        response = anon_client.post(LOGIN_URL, {})
        assert_pos_error(response, 'MISSING_CREDENTIALS', http_status=400)

    def test_login_superuser_gets_all_permissions(self, anon_client, db):
        """Superuser login returns all POS permission flags as True."""
        from staff_roles.pos_permissions import POS_PERMISSION_FLAGS

        superuser = UserFactory(
            username='superadmin',
            email='super@test.spwig.com',
            is_staff=True,
            is_superuser=True,
        )

        response = anon_client.post(LOGIN_URL, {
            'email': superuser.email,
            'password': 'testpass123',
        })
        data = assert_pos_success(response)

        permissions = data['permissions']
        for key, flag_def in POS_PERMISSION_FLAGS.items():
            assert key in permissions, f"Missing permission key: {key}"
            if flag_def.get('type') == 'integer':
                assert permissions[key] == flag_def.get('max', 100), (
                    f"Integer permission '{key}' should be max value"
                )
            else:
                assert permissions[key] is True, (
                    f"Boolean permission '{key}' should be True for superuser"
                )


# ============================================================
# TestPOSTokenRefresh
# ============================================================

class TestPOSTokenRefresh:
    """Tests for POST /api/pos/auth/refresh/."""

    def test_valid_refresh_returns_new_access(self, anon_client, pos_refresh_token):
        """Posting a valid refresh token returns a new access_token."""
        response = anon_client.post(REFRESH_URL, {
            'refresh_token': pos_refresh_token.token,
        })
        data = assert_pos_success(response, http_status=200)

        assert 'access_token' in data
        assert isinstance(data['access_token'], str)
        assert len(data['access_token']) > 20
        assert 'expires_at' in data
        # The new access token should differ from the refresh token
        assert data['access_token'] != pos_refresh_token.token

    def test_expired_refresh_rejected(self, anon_client, pos_staff_user, pos_terminal):
        """An expired refresh token returns 401 INVALID_TOKEN."""
        expired_refresh = MobileAuthTokenFactory(
            user=pos_staff_user,
            refresh=True,
            device_id=f'terminal-{pos_terminal.uuid}',
            expires_at=timezone.now() - timedelta(hours=1),
        )

        response = anon_client.post(REFRESH_URL, {
            'refresh_token': expired_refresh.token,
        })
        assert_pos_error(response, 'INVALID_TOKEN', http_status=401)

    def test_access_token_as_refresh_rejected(self, anon_client, pos_access_token):
        """Using an access token in the refresh endpoint returns 401."""
        response = anon_client.post(REFRESH_URL, {
            'refresh_token': pos_access_token.token,
        })
        assert_pos_error(response, 'INVALID_TOKEN', http_status=401)


# ============================================================
# TestPOSLogout
# ============================================================

class TestPOSLogout:
    """Tests for POST /api/pos/auth/logout/."""

    def test_logout_deletes_token(self, pos_staff_user, pos_access_token):
        """After logout, the access token is deleted from the database."""
        from admin_api.models import MobileAuthToken

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {pos_access_token.token}')

        initial_count = MobileAuthToken.objects.filter(user=pos_staff_user).count()

        response = client.post(LOGOUT_URL)
        assert response.status_code == 200

        final_count = MobileAuthToken.objects.filter(user=pos_staff_user).count()
        assert final_count == initial_count - 1

    def test_token_unusable_after_logout(self, pos_access_token):
        """The token used to logout can no longer authenticate requests."""
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {pos_access_token.token}')

        # Logout should succeed
        response = client.post(LOGOUT_URL)
        assert response.status_code == 200

        # Same token should now be rejected
        response = client.post(LOGOUT_URL)
        assert response.status_code == 401

    def test_logout_requires_auth(self, anon_client):
        """Unauthenticated request to logout returns 401."""
        response = anon_client.post(LOGOUT_URL)
        assert response.status_code == 401
