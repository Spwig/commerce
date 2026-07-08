"""
Guest-to-Account Conversion integration tests.

Tests the full guest checkout user lifecycle:
- Guest user deduplication (create_guest_user get-or-create)
- Guest user merging (merge_guest_users, merge_all_guests_for_email)
- Guest-to-full-account conversion (convert_guest_to_full_account, create_account_during_checkout)
- Email normalization
- Guest order lookup views (magic link flow)
- Guest account activation view
- Order confirmation signal (activation URL for guests)
- Admin bulk action (send activation invitations)
- Management command (merge_duplicate_guests)
"""
import pytest
from pathlib import Path
from decimal import Decimal
from unittest.mock import patch, MagicMock

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages import get_messages
from django.test import Client, override_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from tests.factories import (
    UserFactory, OrderFactory, AddressFactory, CustomerMessageFactory,
    CommunicationPreferenceFactory,
)

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.guest_account]

# Path to test-only templates directory (contains a minimal base.html
# for views that extend base.html -- which normally resolves via the theme loader).
TEST_TEMPLATES_DIR = str(Path(__file__).resolve().parent.parent / 'templates')


@pytest.fixture
def guest_view_settings(settings):
    """
    Override the TEMPLATES setting so that ``base.html`` can be resolved
    during tests.  The production ``base.html`` is served by the
    CachedThemeTemplateLoader, which requires an active theme in the DB.
    We swap the loader chain for the standard filesystem + app_directories
    loaders and prepend the test-only templates directory to DIRS.

    After mutating ``settings.TEMPLATES`` we manually trigger the same
    reset that Django's ``@override_settings`` would perform.
    """
    import copy
    from django.template import engines
    from django.template.engine import Engine
    from django.forms.renderers import get_default_renderer

    original_templates = copy.deepcopy(settings.TEMPLATES)

    # Build a new TEMPLATES list with the test dir first and no theme loader.
    settings.TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                TEST_TEMPLATES_DIR,
                *original_templates[0].get('DIRS', []),
            ],
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                ],
                'loaders': [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ],
            },
        },
    ]

    # --- Reset template engine (mirrors django.test.signals.reset_template_engines) ---
    try:
        del engines.templates
    except AttributeError:
        pass
    engines._templates = None
    engines._engines = {}
    Engine.get_default.cache_clear()
    get_default_renderer.cache_clear()

    yield

    # Restore the original settings and reset again.
    settings.TEMPLATES = original_templates
    try:
        del engines.templates
    except AttributeError:
        pass
    engines._templates = None
    engines._engines = {}
    Engine.get_default.cache_clear()
    get_default_renderer.cache_clear()


# ============================================================
# Helpers
# ============================================================

def _make_guest(email='guest@example.com', first_name='', last_name='', **kwargs):
    """Create a guest user directly (bypassing the service for setup)."""
    import uuid
    username = f"guest_{uuid.uuid4().hex[:12]}"
    user = User.objects.create_user(
        username=username,
        email=email.lower().strip(),
        first_name=first_name,
        last_name=last_name,
        **kwargs,
    )
    user.set_unusable_password()
    user.save(update_fields=['password'])
    return user


def _make_uid_token(user):
    """Return (uidb64, token) pair for a user."""
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return uid, token


# ============================================================
# 1. AccountCreationService — Email normalization
# ============================================================

class TestEmailNormalization:

    def test_lowercase_and_strip(self):
        """_normalize_email lowercases and strips whitespace."""
        from accounts.services.account_creation_service import AccountCreationService
        assert AccountCreationService._normalize_email('  User@Example.COM  ') == 'user@example.com'

    def test_empty_string(self):
        """_normalize_email returns empty string for empty input."""
        from accounts.services.account_creation_service import AccountCreationService
        assert AccountCreationService._normalize_email('') == ''

    def test_none_returns_empty(self):
        """_normalize_email returns empty string for None."""
        from accounts.services.account_creation_service import AccountCreationService
        assert AccountCreationService._normalize_email(None) == ''

    def test_already_normalized(self):
        """_normalize_email is idempotent for already-normalized emails."""
        from accounts.services.account_creation_service import AccountCreationService
        assert AccountCreationService._normalize_email('user@example.com') == 'user@example.com'


# ============================================================
# 2. AccountCreationService — Guest user deduplication
# ============================================================

class TestCreateGuestUser:

    def test_creates_new_guest_user(self):
        """First call for an email creates a new guest user."""
        from accounts.services.account_creation_service import AccountCreationService

        user = AccountCreationService.create_guest_user('new@example.com', 'Jane', 'Doe')

        assert user.pk is not None
        assert user.username.startswith('guest_')
        assert user.email == 'new@example.com'
        assert user.first_name == 'Jane'
        assert user.last_name == 'Doe'
        assert not user.has_usable_password()

    def test_reuses_existing_guest_same_email(self):
        """Second call for the same email returns the existing guest user."""
        from accounts.services.account_creation_service import AccountCreationService

        user1 = AccountCreationService.create_guest_user('reuse@example.com', 'First', 'User')
        user2 = AccountCreationService.create_guest_user('reuse@example.com')

        assert user1.pk == user2.pk

    def test_case_insensitive_dedup(self):
        """Deduplication is case-insensitive."""
        from accounts.services.account_creation_service import AccountCreationService

        user1 = AccountCreationService.create_guest_user('Case@Example.COM')
        user2 = AccountCreationService.create_guest_user('case@example.com')

        assert user1.pk == user2.pk

    def test_updates_empty_name_on_reuse(self):
        """When reusing a guest, empty name fields are filled in."""
        from accounts.services.account_creation_service import AccountCreationService

        user1 = AccountCreationService.create_guest_user('fill@example.com')
        assert user1.first_name == ''

        user2 = AccountCreationService.create_guest_user('fill@example.com', 'Jane', 'Doe')
        user2.refresh_from_db()

        assert user2.pk == user1.pk
        assert user2.first_name == 'Jane'
        assert user2.last_name == 'Doe'

    def test_does_not_overwrite_existing_name(self):
        """When reusing a guest, existing non-empty names are preserved."""
        from accounts.services.account_creation_service import AccountCreationService

        user1 = AccountCreationService.create_guest_user('keep@example.com', 'Original', 'Name')

        user2 = AccountCreationService.create_guest_user('keep@example.com', 'New', 'Name')
        user2.refresh_from_db()

        assert user2.pk == user1.pk
        assert user2.first_name == 'Original'
        assert user2.last_name == 'Name'

    def test_does_not_reuse_registered_user(self):
        """A registered user with the same email is NOT reused as a guest."""
        from accounts.services.account_creation_service import AccountCreationService

        registered = UserFactory(email='registered@example.com', username='registered_user')

        guest = AccountCreationService.create_guest_user('registered@example.com')

        assert guest.pk != registered.pk
        assert guest.username.startswith('guest_')

    def test_picks_most_recent_guest(self):
        """When multiple guests exist for an email, the most recent is returned."""
        from accounts.services.account_creation_service import AccountCreationService

        old = _make_guest('multi@example.com', 'Old', 'Guest')
        new = _make_guest('multi@example.com', 'New', 'Guest')

        result = AccountCreationService.create_guest_user('multi@example.com')
        assert result.pk == new.pk


# ============================================================
# 3. AccountCreationService — merge_guest_users
# ============================================================

class TestMergeGuestUsers:

    def test_merges_orders_to_canonical(self):
        """Orders from duplicates are reassigned to the canonical user."""
        from accounts.services.account_creation_service import AccountCreationService

        canonical = _make_guest('merge@example.com')
        dup1 = _make_guest('merge@example.com')
        dup2 = _make_guest('merge@example.com')

        OrderFactory(user=canonical)
        OrderFactory(user=dup1)
        OrderFactory(user=dup2)
        OrderFactory(user=dup2)

        stats = AccountCreationService.merge_guest_users(canonical, [dup1, dup2])

        assert stats['orders_moved'] == 3
        assert stats['users_deleted'] == 2
        assert canonical.orders.count() == 4

    def test_merges_addresses_to_canonical(self):
        """Addresses from duplicates are reassigned to the canonical user."""
        from accounts.services.account_creation_service import AccountCreationService

        canonical = _make_guest('addr@example.com')
        dup = _make_guest('addr@example.com')

        AddressFactory(user=dup)
        AddressFactory(user=dup)

        stats = AccountCreationService.merge_guest_users(canonical, [dup])

        assert stats['addresses_moved'] == 2
        assert canonical.addresses.count() == 2

    def test_deletes_duplicate_users(self):
        """Duplicate users are deleted after merge."""
        from accounts.services.account_creation_service import AccountCreationService

        canonical = _make_guest('del@example.com')
        dup = _make_guest('del@example.com')
        dup_pk = dup.pk

        AccountCreationService.merge_guest_users(canonical, [dup])

        assert not User.objects.filter(pk=dup_pk).exists()

    def test_deletes_duplicate_profile_and_preferences(self):
        """OneToOne records (profile, communication_preferences) on duplicates are cleaned up."""
        from accounts.services.account_creation_service import AccountCreationService
        from accounts.models import CustomerProfile, CommunicationPreference

        canonical = _make_guest('cleanup@example.com')
        dup = _make_guest('cleanup@example.com')

        CustomerProfile.objects.create(user=dup)
        CommunicationPreference.objects.create(user=dup)

        stats = AccountCreationService.merge_guest_users(canonical, [dup])

        assert stats['users_deleted'] == 1
        assert not CustomerProfile.objects.filter(user_id=dup.pk).exists()

    def test_skips_canonical_in_duplicates_list(self):
        """If canonical appears in the duplicates list, it is not deleted."""
        from accounts.services.account_creation_service import AccountCreationService

        canonical = _make_guest('self@example.com')
        dup = _make_guest('self@example.com')

        stats = AccountCreationService.merge_guest_users(canonical, [canonical, dup])

        assert stats['users_deleted'] == 1
        assert User.objects.filter(pk=canonical.pk).exists()

    def test_empty_duplicates_list(self):
        """merge_guest_users with empty duplicates list does nothing."""
        from accounts.services.account_creation_service import AccountCreationService

        canonical = _make_guest('empty@example.com')
        stats = AccountCreationService.merge_guest_users(canonical, [])

        assert stats == {'orders_moved': 0, 'addresses_moved': 0, 'users_deleted': 0}


# ============================================================
# 4. AccountCreationService — merge_all_guests_for_email
# ============================================================

class TestMergeAllGuestsForEmail:

    def test_merges_all_duplicates(self):
        """All guest users for an email are merged into the most recent."""
        from accounts.services.account_creation_service import AccountCreationService

        g1 = _make_guest('all@example.com')
        g2 = _make_guest('all@example.com')
        g3 = _make_guest('all@example.com')
        OrderFactory(user=g1)
        OrderFactory(user=g2)

        canonical, stats = AccountCreationService.merge_all_guests_for_email('all@example.com')

        assert canonical.pk == g3.pk  # most recent
        assert stats['users_deleted'] == 2
        assert stats['orders_moved'] == 2

    def test_single_guest_no_merge(self):
        """When only one guest exists, nothing is merged."""
        from accounts.services.account_creation_service import AccountCreationService

        g = _make_guest('single@example.com')
        canonical, stats = AccountCreationService.merge_all_guests_for_email('single@example.com')

        assert canonical.pk == g.pk
        assert stats['users_deleted'] == 0

    def test_no_guests_returns_none(self):
        """When no guests exist for the email, None is returned."""
        from accounts.services.account_creation_service import AccountCreationService

        canonical, stats = AccountCreationService.merge_all_guests_for_email('nobody@example.com')

        assert canonical is None
        assert stats['users_deleted'] == 0

    def test_case_insensitive_email_match(self):
        """merge_all_guests_for_email matches emails case-insensitively."""
        from accounts.services.account_creation_service import AccountCreationService

        g1 = _make_guest('Case@Example.COM')
        g2 = _make_guest('case@example.com')

        canonical, stats = AccountCreationService.merge_all_guests_for_email('CASE@EXAMPLE.COM')

        assert canonical is not None
        assert stats['users_deleted'] == 1


# ============================================================
# 5. AccountCreationService — convert_guest_to_full_account
# ============================================================

class TestConvertGuestToFullAccount:

    def test_successful_conversion(self):
        """Guest user is converted with a proper username and usable password."""
        from accounts.services.account_creation_service import AccountCreationService

        guest = _make_guest('convert@example.com', 'Jane', 'Doe')

        success, message = AccountCreationService.convert_guest_to_full_account(
            user=guest,
            password='securepass123',
            send_confirmation_email=False,
        )

        guest.refresh_from_db()

        assert success is True
        assert not guest.username.startswith('guest_')
        assert guest.username == 'convert'  # derived from email
        assert guest.has_usable_password()
        assert guest.check_password('securepass123')

    def test_username_collision_appends_counter(self):
        """If the email-based username is taken, a counter is appended."""
        from accounts.services.account_creation_service import AccountCreationService

        # Create a registered user that occupies the 'taken' username
        UserFactory(username='taken', email='other@example.com')

        guest = _make_guest('taken@example.com')

        success, _ = AccountCreationService.convert_guest_to_full_account(
            user=guest, password='pass12345678', send_confirmation_email=False,
        )

        guest.refresh_from_db()
        assert success is True
        assert guest.username == 'taken1'

    def test_non_guest_user_rejected(self):
        """Conversion fails for non-guest users."""
        from accounts.services.account_creation_service import AccountCreationService

        regular = UserFactory(username='regular', email='regular@example.com')

        success, message = AccountCreationService.convert_guest_to_full_account(
            user=regular, password='pass12345678', send_confirmation_email=False,
        )

        assert success is False

    def test_merges_duplicates_before_conversion(self):
        """Conversion merges other guest users with the same email first."""
        from accounts.services.account_creation_service import AccountCreationService

        g1 = _make_guest('premerge@example.com')
        g2 = _make_guest('premerge@example.com')
        OrderFactory(user=g1)
        OrderFactory(user=g2)

        # Convert the most recent one
        success, _ = AccountCreationService.convert_guest_to_full_account(
            user=g2, password='pass12345678', send_confirmation_email=False,
        )

        g2.refresh_from_db()
        assert success is True
        assert g2.orders.count() == 2
        assert not User.objects.filter(pk=g1.pk).exists()


# ============================================================
# 6. AccountCreationService — create_account_during_checkout
# ============================================================

class TestCreateAccountDuringCheckout:

    def test_creates_fresh_account_when_no_guest(self):
        """A fresh account is created when no guest exists."""
        from accounts.services.account_creation_service import AccountCreationService

        success, message, user = AccountCreationService.create_account_during_checkout(
            email='fresh@example.com',
            password='strongpass123',
            first_name='Fresh',
            last_name='User',
            send_confirmation=False,
        )

        assert success is True
        assert user is not None
        assert user.email == 'fresh@example.com'
        assert not user.username.startswith('guest_')
        assert user.has_usable_password()

    def test_converts_existing_guest(self):
        """If a guest exists with the same email, it is converted instead of creating a new user."""
        from accounts.services.account_creation_service import AccountCreationService

        guest = _make_guest('existing@example.com', 'Guest', 'User')
        OrderFactory(user=guest)

        success, message, user = AccountCreationService.create_account_during_checkout(
            email='existing@example.com',
            password='strongpass123',
            first_name='Real',
            last_name='Name',
            send_confirmation=False,
        )

        assert success is True
        assert user.pk == guest.pk  # Same user, converted
        user.refresh_from_db()
        assert not user.username.startswith('guest_')
        assert user.first_name == 'Real'
        assert user.orders.count() == 1

    def test_rejects_duplicate_registered_email(self):
        """Fails if a registered (non-guest) user already has that email."""
        from accounts.services.account_creation_service import AccountCreationService

        UserFactory(email='taken@example.com', username='taken_user')

        success, message, user = AccountCreationService.create_account_during_checkout(
            email='taken@example.com',
            password='strongpass123',
            send_confirmation=False,
        )

        assert success is False
        assert user is None

    def test_excludes_guests_from_conflict_check(self):
        """Guest users with same email do NOT block account creation."""
        from accounts.services.account_creation_service import AccountCreationService

        _make_guest('guest_ok@example.com')

        success, _, user = AccountCreationService.create_account_during_checkout(
            email='guest_ok@example.com',
            password='strongpass123',
            send_confirmation=False,
        )

        # Should succeed by converting the guest
        assert success is True
        assert user is not None


# ============================================================
# 7. Views — activate_guest_account
# ============================================================

class TestActivateGuestAccountView:

    def test_get_shows_activation_form(self, django_site, guest_view_settings):
        """GET with valid token shows the activation form."""
        guest = _make_guest('activate@example.com')
        uid, token = _make_uid_token(guest)

        client = Client()
        url = reverse('accounts:activate_guest_account', kwargs={'uidb64': uid, 'token': token})
        response = client.get(url)

        assert response.status_code == 200
        assert b'activate@example.com' in response.content

    def test_post_converts_and_logs_in(self, django_site, guest_view_settings):
        """POST with valid passwords converts the guest and logs them in."""
        guest = _make_guest('activate2@example.com')
        uid, token = _make_uid_token(guest)

        client = Client()
        url = reverse('accounts:activate_guest_account', kwargs={'uidb64': uid, 'token': token})
        response = client.post(url, {
            'password': 'securepass123',
            'password_confirm': 'securepass123',
        })

        guest.refresh_from_db()
        assert response.status_code == 302  # Redirect to dashboard
        assert not guest.username.startswith('guest_')
        assert guest.has_usable_password()

    def test_post_password_mismatch(self, django_site, guest_view_settings):
        """POST with mismatched passwords re-renders form with error."""
        guest = _make_guest('mismatch@example.com')
        uid, token = _make_uid_token(guest)

        client = Client()
        url = reverse('accounts:activate_guest_account', kwargs={'uidb64': uid, 'token': token})
        response = client.post(url, {
            'password': 'password123',
            'password_confirm': 'different123',
        })

        assert response.status_code == 200  # Re-render
        msgs = list(get_messages(response.wsgi_request))
        assert any('do not match' in str(m).lower() for m in msgs)

    def test_post_password_too_short(self, django_site, guest_view_settings):
        """POST with short password re-renders form with error."""
        guest = _make_guest('short@example.com')
        uid, token = _make_uid_token(guest)

        client = Client()
        url = reverse('accounts:activate_guest_account', kwargs={'uidb64': uid, 'token': token})
        response = client.post(url, {
            'password': 'short',
            'password_confirm': 'short',
        })

        assert response.status_code == 200
        msgs = list(get_messages(response.wsgi_request))
        assert any('8 characters' in str(m) for m in msgs)

    @patch('accounts.views.redirect')
    def test_invalid_token_redirects(self, mock_redirect, django_site, guest_view_settings):
        """Invalid token triggers redirect to homepage."""
        from django.http import HttpResponseRedirect
        mock_redirect.return_value = HttpResponseRedirect('/')

        guest = _make_guest('badtoken@example.com')
        uid = urlsafe_base64_encode(force_bytes(guest.pk))

        client = Client()
        url = reverse('accounts:activate_guest_account', kwargs={
            'uidb64': uid, 'token': 'invalid-token',
        })
        response = client.get(url)

        assert response.status_code == 302
        mock_redirect.assert_called_with('catalog:home')

    def test_non_guest_user_rejected(self, django_site, guest_view_settings):
        """Activation link for a non-guest user redirects to dashboard."""
        regular = UserFactory(username='nong', email='nong@example.com')
        uid, token = _make_uid_token(regular)

        client = Client()
        url = reverse('accounts:activate_guest_account', kwargs={'uidb64': uid, 'token': token})
        response = client.get(url, follow=True)

        # The view redirects to 'accounts:dashboard' which requires login,
        # so we end up at the login page.
        assert response.status_code == 200

    @patch('accounts.views.redirect')
    def test_nonexistent_user_redirects(self, mock_redirect, django_site, guest_view_settings):
        """Token for a nonexistent user ID triggers redirect to homepage."""
        from django.http import HttpResponseRedirect
        mock_redirect.return_value = HttpResponseRedirect('/')

        uid = urlsafe_base64_encode(force_bytes(999999))

        client = Client()
        url = reverse('accounts:activate_guest_account', kwargs={
            'uidb64': uid, 'token': 'does-not-matter',
        })
        response = client.get(url)

        assert response.status_code == 302
        mock_redirect.assert_called_with('catalog:home')


# ============================================================
# 8. Views — guest_order_lookup
# ============================================================

class TestGuestOrderLookupView:

    def test_get_renders_form(self, django_site, guest_view_settings):
        """GET shows the email entry form."""
        client = Client()
        url = reverse('accounts:guest_order_lookup')
        response = client.get(url)

        assert response.status_code == 200

    @patch('email_system.services.email_sender.EmailSendingService')
    def test_post_with_matching_guest_sends_email(self, mock_email_service, django_site, guest_view_settings):
        """POST with an email that has guest orders sends a magic link email."""
        guest = _make_guest('lookup@example.com')
        OrderFactory(user=guest)

        # Reset mock after order creation (the order confirmation signal also
        # calls EmailSendingService, which would pollute our assertion).
        mock_email_service.reset_mock()

        client = Client()
        url = reverse('accounts:guest_order_lookup')
        response = client.post(url, {'email': 'lookup@example.com'})

        assert response.status_code == 200
        mock_email_service.send_template_email.assert_called_once()
        call_kwargs = mock_email_service.send_template_email.call_args[1]
        assert call_kwargs['to_email'] == 'lookup@example.com'

    def test_post_with_unknown_email_still_shows_success(self, django_site, guest_view_settings):
        """POST with an unknown email still shows success (prevents enumeration)."""
        client = Client()
        url = reverse('accounts:guest_order_lookup')
        response = client.post(url, {'email': 'nobody@example.com'})

        assert response.status_code == 200
        msgs = list(get_messages(response.wsgi_request))
        assert len(msgs) == 1  # Should have exactly one success message

    def test_post_empty_email_shows_error(self, django_site, guest_view_settings):
        """POST with empty email shows an error."""
        client = Client()
        url = reverse('accounts:guest_order_lookup')
        response = client.post(url, {'email': ''})

        assert response.status_code == 200
        msgs = list(get_messages(response.wsgi_request))
        assert any('email' in str(m).lower() for m in msgs)

    @patch('email_system.services.email_sender.EmailSendingService')
    def test_post_guest_without_orders_does_not_send(self, mock_email_service, django_site, guest_view_settings):
        """POST for a guest with no orders does NOT send an email (no orders to look up)."""
        _make_guest('noorders@example.com')

        client = Client()
        url = reverse('accounts:guest_order_lookup')
        response = client.post(url, {'email': 'noorders@example.com'})

        assert response.status_code == 200
        mock_email_service.send_template_email.assert_not_called()


# ============================================================
# 9. Views — guest_orders_view
# ============================================================

class TestGuestOrdersView:

    def test_get_shows_orders(self, django_site, guest_view_settings):
        """GET with valid token shows the guest's orders."""
        guest = _make_guest('orders@example.com')
        OrderFactory(user=guest, order_number='ORD-001')
        OrderFactory(user=guest, order_number='ORD-002')
        uid, token = _make_uid_token(guest)

        client = Client()
        url = reverse('accounts:guest_orders_view', kwargs={'uidb64': uid, 'token': token})
        response = client.get(url)

        assert response.status_code == 200
        assert b'ORD-001' in response.content
        assert b'ORD-002' in response.content

    def test_context_includes_order_count(self, django_site, guest_view_settings):
        """Response context includes the order count."""
        guest = _make_guest('ctx@example.com')
        OrderFactory(user=guest)
        OrderFactory(user=guest)
        uid, token = _make_uid_token(guest)

        client = Client()
        url = reverse('accounts:guest_orders_view', kwargs={'uidb64': uid, 'token': token})
        response = client.get(url)

        assert response.context['order_count'] == 2

    def test_post_converts_guest_account(self, django_site, guest_view_settings):
        """POST with valid passwords converts guest to full account."""
        guest = _make_guest('convert_view@example.com')
        OrderFactory(user=guest)
        uid, token = _make_uid_token(guest)

        client = Client()
        url = reverse('accounts:guest_orders_view', kwargs={'uidb64': uid, 'token': token})
        response = client.post(url, {
            'password': 'strongpass123',
            'password_confirm': 'strongpass123',
        })

        guest.refresh_from_db()
        assert response.status_code == 302  # Redirect to dashboard
        assert not guest.username.startswith('guest_')

    def test_post_password_too_short(self, django_site, guest_view_settings):
        """POST with short password shows error."""
        guest = _make_guest('short_view@example.com')
        uid, token = _make_uid_token(guest)

        client = Client()
        url = reverse('accounts:guest_orders_view', kwargs={'uidb64': uid, 'token': token})
        response = client.post(url, {
            'password': 'short',
            'password_confirm': 'short',
        })

        assert response.status_code == 200
        msgs = list(get_messages(response.wsgi_request))
        assert any('8 characters' in str(m) for m in msgs)

    def test_post_password_mismatch(self, django_site, guest_view_settings):
        """POST with mismatched passwords shows error."""
        guest = _make_guest('mismatch_view@example.com')
        uid, token = _make_uid_token(guest)

        client = Client()
        url = reverse('accounts:guest_orders_view', kwargs={'uidb64': uid, 'token': token})
        response = client.post(url, {
            'password': 'password123',
            'password_confirm': 'different123',
        })

        assert response.status_code == 200
        msgs = list(get_messages(response.wsgi_request))
        assert any('do not match' in str(m).lower() for m in msgs)

    def test_invalid_token_redirects_to_lookup(self, django_site, guest_view_settings):
        """Invalid token redirects to the guest order lookup page."""
        guest = _make_guest('badtoken_view@example.com')
        uid = urlsafe_base64_encode(force_bytes(guest.pk))

        client = Client()
        url = reverse('accounts:guest_orders_view', kwargs={
            'uidb64': uid, 'token': 'bad-token',
        })
        response = client.get(url)

        assert response.status_code == 302
        assert 'guest-orders' in response.url  # Redirect to lookup

    def test_registered_user_redirects_to_login(self, django_site, guest_view_settings):
        """If user is already registered (not guest), redirect to login."""
        registered = UserFactory(username='alreadyreg', email='alreadyreg@example.com')
        uid, token = _make_uid_token(registered)

        client = Client()
        url = reverse('accounts:guest_orders_view', kwargs={'uidb64': uid, 'token': token})
        response = client.get(url)

        assert response.status_code == 302
        # Should redirect to login page (allauth's account_login)

    def test_post_empty_password_shows_error(self, django_site, guest_view_settings):
        """POST with empty password shows error."""
        guest = _make_guest('empty_pw@example.com')
        uid, token = _make_uid_token(guest)

        client = Client()
        url = reverse('accounts:guest_orders_view', kwargs={'uidb64': uid, 'token': token})
        response = client.post(url, {
            'password': '',
            'password_confirm': '',
        })

        assert response.status_code == 200
        msgs = list(get_messages(response.wsgi_request))
        assert any('password' in str(m).lower() for m in msgs)


# ============================================================
# 10. Signal — Order confirmation email includes activation URL for guests
# ============================================================

class TestOrderConfirmationSignal:

    @patch('email_system.services.email_sender.EmailSendingService')
    def test_guest_order_includes_activation_url(self, mock_email_service, django_site, site_settings):
        """Order confirmation for a guest order includes activation_url in context."""
        from orders.models import Order

        guest = _make_guest('signal@example.com')

        # Create order directly to trigger signal
        # We need to patch to avoid actual email sending failures
        order = OrderFactory(user=guest, email='signal@example.com')

        # Check that the signal handler was called
        assert mock_email_service.send_template_email.called

        call_kwargs = mock_email_service.send_template_email.call_args[1]
        context = call_kwargs['context']

        assert context.get('is_guest_order') is True
        assert 'activation_url' in context
        assert 'activate-guest' in context['activation_url']

    @patch('email_system.services.email_sender.EmailSendingService')
    def test_registered_order_no_activation_url(self, mock_email_service, django_site, site_settings):
        """Order confirmation for a registered user does NOT include activation_url."""
        registered = UserFactory(username='siguser', email='siguser@example.com')

        order = OrderFactory(user=registered, email='siguser@example.com')

        assert mock_email_service.send_template_email.called

        call_kwargs = mock_email_service.send_template_email.call_args[1]
        context = call_kwargs['context']

        assert 'is_guest_order' not in context
        assert 'activation_url' not in context


# ============================================================
# 11. Admin — AccountTypeFilter
# ============================================================

class TestAccountTypeFilter:

    @staticmethod
    def _make_filter_params(key, value):
        """Build a params dict compatible with Django's SimpleListFilter.

        SimpleListFilter.__init__ calls ``params.pop(key)`` then indexes
        the result with ``[-1]``.  When params comes from a ``QueryDict``
        the popped value is a **list**, so ``[-1]`` picks the last item.
        We replicate that here with plain dicts containing list values.
        """
        return {key: [value]}

    def test_guest_filter(self):
        """AccountTypeFilter 'guest' returns only guest profiles."""
        from customers.admin import AccountTypeFilter
        from accounts.models import CustomerProfile

        guest = _make_guest('filter_g@example.com')
        registered = UserFactory(username='filter_reg', email='filter_reg@example.com')

        CustomerProfile.objects.create(user=guest)
        CustomerProfile.objects.create(user=registered)

        params = self._make_filter_params('account_type', 'guest')
        f = AccountTypeFilter(None, params, CustomerProfile, None)
        qs = f.queryset(None, CustomerProfile.objects.all())

        usernames = list(qs.values_list('user__username', flat=True))
        assert guest.username in usernames
        assert 'filter_reg' not in usernames

    def test_registered_filter(self):
        """AccountTypeFilter 'registered' excludes guest profiles."""
        from customers.admin import AccountTypeFilter
        from accounts.models import CustomerProfile

        guest = _make_guest('filter2_g@example.com')
        registered = UserFactory(username='filter2_reg', email='filter2_reg@example.com')

        CustomerProfile.objects.create(user=guest)
        CustomerProfile.objects.create(user=registered)

        params = self._make_filter_params('account_type', 'registered')
        f = AccountTypeFilter(None, params, CustomerProfile, None)
        qs = f.queryset(None, CustomerProfile.objects.all())

        usernames = list(qs.values_list('user__username', flat=True))
        assert 'filter2_reg' in usernames
        assert guest.username not in usernames

    def test_no_filter(self):
        """AccountTypeFilter with no value returns all profiles."""
        from customers.admin import AccountTypeFilter
        from accounts.models import CustomerProfile

        guest = _make_guest('all_g@example.com')
        registered = UserFactory(username='all_reg', email='all_reg@example.com')

        CustomerProfile.objects.create(user=guest)
        CustomerProfile.objects.create(user=registered)

        f = AccountTypeFilter(None, {}, CustomerProfile, None)
        qs = f.queryset(None, CustomerProfile.objects.all())

        assert qs.count() >= 2


# ============================================================
# 12. Admin — account_type_display
# ============================================================

class TestAccountTypeDisplay:

    def test_guest_badge(self):
        """account_type_display shows Guest badge for guest users."""
        from customers.admin import EnhancedCustomerProfileAdmin
        from accounts.models import CustomerProfile

        guest = _make_guest('badge_g@example.com')
        profile = CustomerProfile.objects.create(user=guest)

        admin_instance = EnhancedCustomerProfileAdmin(CustomerProfile, None)
        html = admin_instance.account_type_display(profile)

        assert 'Guest' in str(html)
        assert 'ffc107' in str(html)  # Yellow background

    def test_registered_badge(self):
        """account_type_display shows Registered badge for registered users."""
        from customers.admin import EnhancedCustomerProfileAdmin
        from accounts.models import CustomerProfile

        registered = UserFactory(username='badge_reg', email='badge_reg@example.com')
        profile = CustomerProfile.objects.create(user=registered)

        admin_instance = EnhancedCustomerProfileAdmin(CustomerProfile, None)
        html = admin_instance.account_type_display(profile)

        assert 'Registered' in str(html)
        assert '28a745' in str(html)  # Green background


# ============================================================
# 13. Admin — send_activation_invitations bulk action
# ============================================================

class TestSendActivationInvitations:

    @patch('email_system.services.email_sender.EmailSendingService')
    def test_sends_to_guest_users(self, mock_email_service, django_site):
        """Bulk action sends invitations to guest users with email."""
        from customers.admin import EnhancedCustomerProfileAdmin
        from accounts.models import CustomerProfile

        guest = _make_guest('invite@example.com')
        profile = CustomerProfile.objects.create(user=guest)

        admin_instance = EnhancedCustomerProfileAdmin(CustomerProfile, None)

        mock_request = MagicMock()
        mock_request.LANGUAGE_CODE = 'en'
        mock_request._messages = MagicMock()

        admin_instance.send_activation_invitations(
            mock_request, CustomerProfile.objects.filter(pk=profile.pk)
        )

        mock_email_service.send_template_email.assert_called_once()
        call_kwargs = mock_email_service.send_template_email.call_args[1]
        assert call_kwargs['to_email'] == 'invite@example.com'
        assert 'activate-guest' in call_kwargs['context']['activation_url']

    @patch('email_system.services.email_sender.EmailSendingService')
    def test_skips_registered_users(self, mock_email_service, django_site):
        """Bulk action skips registered (non-guest) users."""
        from customers.admin import EnhancedCustomerProfileAdmin
        from accounts.models import CustomerProfile

        registered = UserFactory(username='skip_reg', email='skip_reg@example.com')
        profile = CustomerProfile.objects.create(user=registered)

        admin_instance = EnhancedCustomerProfileAdmin(CustomerProfile, None)

        mock_request = MagicMock()
        mock_request.LANGUAGE_CODE = 'en'
        mock_request._messages = MagicMock()

        admin_instance.send_activation_invitations(
            mock_request, CustomerProfile.objects.filter(pk=profile.pk)
        )

        mock_email_service.send_template_email.assert_not_called()

    @patch('email_system.services.email_sender.EmailSendingService')
    def test_skips_guests_without_email(self, mock_email_service, django_site):
        """Bulk action skips guest users that have no email."""
        from customers.admin import EnhancedCustomerProfileAdmin
        from accounts.models import CustomerProfile

        guest = _make_guest('')
        profile = CustomerProfile.objects.create(user=guest)

        admin_instance = EnhancedCustomerProfileAdmin(CustomerProfile, None)

        mock_request = MagicMock()
        mock_request.LANGUAGE_CODE = 'en'
        mock_request._messages = MagicMock()

        admin_instance.send_activation_invitations(
            mock_request, CustomerProfile.objects.filter(pk=profile.pk)
        )

        mock_email_service.send_template_email.assert_not_called()

    @patch('email_system.services.email_sender.EmailSendingService')
    def test_mixed_queryset(self, mock_email_service, django_site):
        """Bulk action correctly counts sent and skipped in mixed queryset."""
        from customers.admin import EnhancedCustomerProfileAdmin
        from accounts.models import CustomerProfile

        guest1 = _make_guest('mix1@example.com')
        guest2 = _make_guest('mix2@example.com')
        registered = UserFactory(username='mix_reg', email='mix_reg@example.com')

        p1 = CustomerProfile.objects.create(user=guest1)
        p2 = CustomerProfile.objects.create(user=guest2)
        p3 = CustomerProfile.objects.create(user=registered)

        admin_instance = EnhancedCustomerProfileAdmin(CustomerProfile, None)

        mock_request = MagicMock()
        mock_request.LANGUAGE_CODE = 'en'
        mock_request._messages = MagicMock()

        admin_instance.send_activation_invitations(
            mock_request, CustomerProfile.objects.filter(pk__in=[p1.pk, p2.pk, p3.pk])
        )

        assert mock_email_service.send_template_email.call_count == 2


# ============================================================
# 14. Management Command — merge_duplicate_guests
# ============================================================

class TestMergeDuplicateGuestsCommand:

    def test_dry_run_reports_but_no_changes(self):
        """Default dry-run shows what would happen without deleting anything."""
        from django.core.management import call_command
        from io import StringIO

        g1 = _make_guest('cmd@example.com')
        g2 = _make_guest('cmd@example.com')
        OrderFactory(user=g1)

        out = StringIO()
        call_command('merge_duplicate_guests', stdout=out)

        output = out.getvalue()
        assert 'DRY RUN' in output
        assert 'cmd@example.com' in output
        # Both users should still exist
        assert User.objects.filter(pk=g1.pk).exists()
        assert User.objects.filter(pk=g2.pk).exists()

    def test_execute_actually_merges(self):
        """--execute flag actually deletes duplicate users."""
        from django.core.management import call_command
        from io import StringIO

        g1 = _make_guest('exec@example.com')
        g2 = _make_guest('exec@example.com')
        g3 = _make_guest('exec@example.com')
        OrderFactory(user=g1)
        OrderFactory(user=g2)

        out = StringIO()
        call_command('merge_duplicate_guests', '--execute', stdout=out)

        output = out.getvalue()
        assert 'Done' in output

        # Only one guest user should remain (the most recent: g3)
        remaining = User.objects.filter(
            email__iexact='exec@example.com',
            username__startswith='guest_'
        )
        assert remaining.count() == 1
        assert remaining.first().pk == g3.pk
        # All orders consolidated
        assert remaining.first().orders.count() == 2

    def test_email_filter(self):
        """--email flag restricts merge to that email only."""
        from django.core.management import call_command
        from io import StringIO

        # Two duplicate groups
        g1 = _make_guest('target@example.com')
        g2 = _make_guest('target@example.com')
        g3 = _make_guest('other@example.com')
        g4 = _make_guest('other@example.com')

        out = StringIO()
        call_command(
            'merge_duplicate_guests', '--execute', '--email=target@example.com',
            stdout=out,
        )

        # Target group merged
        assert User.objects.filter(
            email__iexact='target@example.com', username__startswith='guest_'
        ).count() == 1

        # Other group untouched
        assert User.objects.filter(
            email__iexact='other@example.com', username__startswith='guest_'
        ).count() == 2

    def test_no_duplicates_found(self):
        """Command reports no duplicates when none exist."""
        from django.core.management import call_command
        from io import StringIO

        _make_guest('unique@example.com')

        out = StringIO()
        call_command('merge_duplicate_guests', stdout=out)

        output = out.getvalue()
        assert 'No duplicate guest users found' in output


# ============================================================
# 15. Dashboard — unread_reply_count for messages badge
# ============================================================

class TestDashboardUnreadReplyCount:

    def test_dashboard_includes_unread_reply_count(self, customer_client, customer_user, site_settings):
        """Dashboard context includes unread_reply_count for the messages badge."""
        from admin_api.models import CustomerMessage

        CustomerMessage.objects.create(
            user=customer_user,
            name='Test',
            email=customer_user.email,
            subject='Replied msg',
            message='Hello',
            message_type='general',
            status='replied',
            reply_text='Thanks!',
        )

        url = reverse('accounts:dashboard')
        response = customer_client.get(url)

        assert response.status_code == 200
        assert response.context['unread_reply_count'] == 1

    def test_dashboard_no_replies_count_zero(self, customer_client, customer_user, site_settings):
        """Dashboard shows 0 unread replies when none exist."""
        url = reverse('accounts:dashboard')
        response = customer_client.get(url)

        assert response.status_code == 200
        assert response.context['unread_reply_count'] == 0


# ============================================================
# 16. Security — guest views without login requirement
# ============================================================

class TestGuestViewSecurity:

    def test_activate_guest_accessible_without_login(self, django_site, guest_view_settings):
        """activate_guest_account does NOT require @login_required (it's for guests)."""
        guest = _make_guest('nosec@example.com')
        uid, token = _make_uid_token(guest)

        client = Client()
        url = reverse('accounts:activate_guest_account', kwargs={'uidb64': uid, 'token': token})
        response = client.get(url)

        # Should NOT redirect to login
        assert response.status_code == 200

    def test_guest_order_lookup_accessible_without_login(self, django_site, guest_view_settings):
        """guest_order_lookup does NOT require @login_required."""
        client = Client()
        url = reverse('accounts:guest_order_lookup')
        response = client.get(url)

        assert response.status_code == 200

    def test_guest_orders_view_accessible_without_login(self, django_site, guest_view_settings):
        """guest_orders_view does NOT require @login_required (token-authenticated)."""
        guest = _make_guest('noauth@example.com')
        uid, token = _make_uid_token(guest)

        client = Client()
        url = reverse('accounts:guest_orders_view', kwargs={'uidb64': uid, 'token': token})
        response = client.get(url)

        assert response.status_code == 200


# ============================================================
# 17. Edge cases
# ============================================================

class TestEdgeCases:

    def test_convert_guest_with_no_email(self):
        """Converting a guest that has no email still works."""
        from accounts.services.account_creation_service import AccountCreationService

        guest = _make_guest('')
        success, _ = AccountCreationService.convert_guest_to_full_account(
            user=guest, password='pass12345678', send_confirmation_email=False,
        )

        guest.refresh_from_db()
        assert success is True
        assert not guest.username.startswith('guest_')

    def test_whitespace_only_email_normalized_to_empty(self):
        """Whitespace-only email normalizes to empty string."""
        from accounts.services.account_creation_service import AccountCreationService
        assert AccountCreationService._normalize_email('   ') == ''

    def test_create_guest_with_special_chars_in_email(self):
        """Guest creation works with valid special characters in email."""
        from accounts.services.account_creation_service import AccountCreationService

        user = AccountCreationService.create_guest_user('user+tag@example.com')
        assert user.email == 'user+tag@example.com'
        assert user.username.startswith('guest_')
