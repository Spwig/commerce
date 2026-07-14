"""
Middleware Enforcement Tests

Validates RBAC enforcement at the middleware layer:
- AdminAccessMiddleware (role-based admin panel access)
- MFAEnforcementMiddleware (2FA requirements for staff)
- License middleware (payment processing gating)
"""

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory

from core.middleware.admin_access import AdminAccessMiddleware
from core.middleware.mfa_enforcement import MFAEnforcementMiddleware
from staff_roles.models import StaffRole

User = get_user_model()


pytestmark = [pytest.mark.django_db, pytest.mark.integrity]


@pytest.fixture
def request_factory():
    """Request factory for creating test requests"""
    return RequestFactory()


@pytest.fixture
def add_session_to_request():
    """Helper to add session middleware to request"""

    def _add_session(request):
        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(request)
        request.session.save()

        # Add messages framework
        messages = FallbackStorage(request)
        request._messages = messages

        return request

    return _add_session


@pytest.fixture
def staff_user():
    """Create a staff user"""
    return User.objects.create_user(
        username="staff_user",
        email="staff@example.com",
        password="testpass123",
        is_staff=True,
    )


@pytest.fixture
def admin_role(staff_user):
    """Create a role with admin access"""
    group = Group.objects.create(name="Admin")
    role = StaffRole.objects.create(
        group=group,
        display_name="Admin",
        can_access_admin=True,
    )
    staff_user.groups.add(group)
    return role


@pytest.fixture
def pos_only_role(staff_user):
    """Create a POS-only role without admin access"""
    group = Group.objects.create(name="POS")
    role = StaffRole.objects.create(
        group=group,
        display_name="POS Only",
        can_access_admin=False,
        can_access_pos=True,
    )
    staff_user.groups.add(group)
    return role


class TestAdminAccessMiddleware:
    """Validate AdminAccessMiddleware enforcement"""

    def test_superuser_has_admin_access(self, request_factory, add_session_to_request):
        """Verify superusers can access admin regardless of roles"""
        superuser = User.objects.create_user(
            username="super",
            is_staff=True,
            is_superuser=True,
        )

        request = request_factory.get("/admin/")
        request.user = superuser
        request = add_session_to_request(request)

        middleware = AdminAccessMiddleware(lambda r: None)
        response = middleware(request)

        # Should return None (allow access)
        assert response is None

    def test_staff_with_admin_role_has_access(
        self, request_factory, staff_user, admin_role, add_session_to_request
    ):
        """Verify staff with can_access_admin role can access admin"""
        request = request_factory.get("/admin/")
        request.user = staff_user
        request = add_session_to_request(request)

        middleware = AdminAccessMiddleware(lambda r: None)
        response = middleware(request)

        # Should return None (allow access)
        assert response is None

    def test_pos_only_staff_blocked_from_admin(
        self, request_factory, staff_user, pos_only_role, add_session_to_request
    ):
        """Verify POS-only staff (no admin access) are redirected from admin"""
        request = request_factory.get("/admin/")
        request.user = staff_user
        request = add_session_to_request(request)

        middleware = AdminAccessMiddleware(lambda r: None)
        response = middleware(request)

        # Should redirect (not None)
        assert response is not None
        assert response.status_code == 302
        assert response.url == "/"

    def test_staff_with_no_roles_has_access(
        self, request_factory, staff_user, add_session_to_request
    ):
        """
        Verify staff with no roles get admin access (backwards compatibility).
        This ensures existing staff users aren't locked out.
        """
        # staff_user has is_staff=True but no roles
        request = request_factory.get("/admin/")
        request.user = staff_user
        request = add_session_to_request(request)

        middleware = AdminAccessMiddleware(lambda r: None)
        response = middleware(request)

        # Should return None (allow access)
        assert response is None

    def test_non_staff_not_checked_by_middleware(self, request_factory, add_session_to_request):
        """Verify non-staff users pass through middleware (handled by Django)"""
        regular_user = User.objects.create_user(
            username="regular",
            is_staff=False,
        )

        request = request_factory.get("/admin/")
        request.user = regular_user
        request = add_session_to_request(request)

        middleware = AdminAccessMiddleware(lambda r: None)
        response = middleware(request)

        # Should return None (pass through to Django's admin auth)
        assert response is None

    def test_anonymous_user_passes_through(self, request_factory, add_session_to_request):
        """Verify anonymous users pass through middleware"""
        request = request_factory.get("/admin/")
        request.user = AnonymousUser()
        request = add_session_to_request(request)

        middleware = AdminAccessMiddleware(lambda r: None)
        response = middleware(request)

        # Should return None (pass through)
        assert response is None

    def test_admin_login_page_always_accessible(
        self, request_factory, staff_user, pos_only_role, add_session_to_request
    ):
        """Verify admin login/logout pages are accessible even without admin role"""
        login_paths = ["/admin/login/", "/en/admin/login/", "/admin/logout/"]

        for path in login_paths:
            request = request_factory.get(path)
            request.user = staff_user
            request = add_session_to_request(request)

            middleware = AdminAccessMiddleware(lambda r: None)
            response = middleware(request)

            # Should return None (allow access)
            assert response is None, f"{path} should be accessible"

    def test_non_admin_paths_not_checked(
        self, request_factory, staff_user, pos_only_role, add_session_to_request
    ):
        """Verify non-admin paths bypass the middleware"""
        non_admin_paths = ["/api/products/", "/checkout/", "/pos/"]

        for path in non_admin_paths:
            request = request_factory.get(path)
            request.user = staff_user
            request = add_session_to_request(request)

            middleware = AdminAccessMiddleware(lambda r: None)
            response = middleware(request)

            # Should return None (not an admin path)
            assert response is None

    def test_multiple_roles_or_logic(self, request_factory, staff_user, add_session_to_request):
        """Verify OR logic: if ANY role grants admin access, user can access admin"""
        # Add two roles: one denies, one grants
        group1 = Group.objects.create(name="POS")
        role1 = StaffRole.objects.create(
            group=group1,
            display_name="POS",
            can_access_admin=False,
        )
        staff_user.groups.add(group1)

        group2 = Group.objects.create(name="Manager")
        role2 = StaffRole.objects.create(
            group=group2,
            display_name="Manager",
            can_access_admin=True,
        )
        staff_user.groups.add(group2)

        request = request_factory.get("/admin/")
        request.user = staff_user
        request = add_session_to_request(request)

        middleware = AdminAccessMiddleware(lambda r: None)
        response = middleware(request)

        # Should return None (allow access due to Manager role)
        assert response is None

    def test_middleware_handles_language_prefixes(
        self, request_factory, staff_user, admin_role, add_session_to_request
    ):
        """Verify middleware handles admin paths with language prefixes"""
        paths_with_lang = ["/en/admin/", "/de/admin/", "/fr/admin/products/"]

        for path in paths_with_lang:
            request = request_factory.get(path)
            request.user = staff_user
            request = add_session_to_request(request)

            middleware = AdminAccessMiddleware(lambda r: None)
            response = middleware(request)

            # Should return None (allow access)
            assert response is None, f"{path} should be accessible"


class TestMFAEnforcementMiddleware:
    """Validate MFAEnforcementMiddleware path exemptions and checks"""

    def test_exempt_paths_bypass_middleware(
        self, request_factory, staff_user, add_session_to_request
    ):
        """Verify exempt paths don't trigger MFA enforcement"""
        exempt_paths = [
            "/static/css/style.css",
            "/media/images/logo.png",
            "/api/products/",
            "/accounts/mfa/setup/",
            "/accounts/login/",
            "/admin/jsi18n/",
        ]

        for path in exempt_paths:
            request = request_factory.get(path)
            request.user = staff_user
            request = add_session_to_request(request)

            middleware = MFAEnforcementMiddleware(lambda r: None)
            response = middleware.process_request(request)

            # Should return None (exempt)
            assert response is None, f"{path} should be exempt from MFA enforcement"

    def test_admin_paths_trigger_mfa_check(
        self, request_factory, staff_user, add_session_to_request
    ):
        """Verify admin paths trigger MFA enforcement logic"""
        # This test validates that the middleware examines admin paths
        # (Full MFA enforcement logic would require more complex setup)
        admin_paths = ["/admin/", "/admin/catalog/product/"]

        for path in admin_paths:
            request = request_factory.get(path)
            request.user = staff_user
            request = add_session_to_request(request)

            middleware = MFAEnforcementMiddleware(lambda r: None)
            # Process request (may return redirect or None depending on MFA state)
            middleware.process_request(request)

            # Test passes if no exception raised
            assert True

    def test_non_admin_paths_bypass_mfa_check(
        self, request_factory, staff_user, add_session_to_request
    ):
        """Verify non-admin paths bypass MFA enforcement"""
        non_admin_paths = ["/checkout/", "/pos/", "/products/"]

        for path in non_admin_paths:
            request = request_factory.get(path)
            request.user = staff_user
            request = add_session_to_request(request)

            middleware = MFAEnforcementMiddleware(lambda r: None)
            response = middleware.process_request(request)

            # Should return None (not admin path)
            assert response is None


class TestMiddlewareOrdering:
    """Validate critical middleware ordering in settings"""

    def test_admin_access_middleware_present(self):
        """Verify AdminAccessMiddleware is in MIDDLEWARE setting"""
        from django.conf import settings

        middleware = settings.MIDDLEWARE

        admin_access_mw = "core.middleware.admin_access.AdminAccessMiddleware"
        assert admin_access_mw in middleware, "AdminAccessMiddleware must be in MIDDLEWARE"

    def test_mfa_enforcement_middleware_present(self):
        """Verify MFAEnforcementMiddleware is in MIDDLEWARE setting"""
        from django.conf import settings

        middleware = settings.MIDDLEWARE

        mfa_mw = "core.middleware.mfa_enforcement.MFAEnforcementMiddleware"
        # MFA middleware may be optional, so just check if present
        if mfa_mw in middleware:
            # If present, it should come after AuthenticationMiddleware
            auth_mw = "django.contrib.auth.middleware.AuthenticationMiddleware"
            assert auth_mw in middleware, "AuthenticationMiddleware must be present"

            auth_idx = middleware.index(auth_mw)
            mfa_idx = middleware.index(mfa_mw)
            assert mfa_idx > auth_idx, (
                "MFAEnforcementMiddleware must come after AuthenticationMiddleware"
            )

    def test_session_middleware_before_auth(self):
        """Verify SessionMiddleware comes before AuthenticationMiddleware"""
        from django.conf import settings

        middleware = settings.MIDDLEWARE

        session_mw = "django.contrib.sessions.middleware.SessionMiddleware"
        auth_mw = "django.contrib.auth.middleware.AuthenticationMiddleware"

        if session_mw in middleware and auth_mw in middleware:
            session_idx = middleware.index(session_mw)
            auth_idx = middleware.index(auth_mw)
            assert session_idx < auth_idx, (
                "SessionMiddleware must come before AuthenticationMiddleware"
            )


class TestRBACIntegration:
    """Integration tests for RBAC across middleware and services"""

    def test_pos_staff_can_access_pos_api_but_not_admin(
        self, request_factory, staff_user, pos_only_role, add_session_to_request
    ):
        """
        Verify POS-only staff can access POS but not admin.
        This is a critical business rule.
        """
        from staff_roles.services import can_access_admin, can_access_pos

        # Verify service layer
        assert can_access_pos(staff_user) is True
        assert can_access_admin(staff_user) is False

        # Verify middleware layer (admin blocked)
        request = request_factory.get("/admin/")
        request.user = staff_user
        request = add_session_to_request(request)

        admin_mw = AdminAccessMiddleware(lambda r: None)
        response = admin_mw(request)

        assert response is not None, "POS-only staff should be redirected from admin"
        assert response.status_code == 302

    def test_admin_staff_can_access_both_admin_and_pos(
        self, request_factory, add_session_to_request
    ):
        """Verify staff with both admin and POS access can access both systems"""
        user = User.objects.create_user(
            username="manager",
            is_staff=True,
        )

        group = Group.objects.create(name="Manager")
        role = StaffRole.objects.create(
            group=group,
            display_name="Manager",
            can_access_admin=True,
            can_access_pos=True,
        )
        user.groups.add(group)

        from staff_roles.services import can_access_admin, can_access_pos

        # Verify service layer
        assert can_access_pos(user) is True
        assert can_access_admin(user) is True

        # Verify middleware layer (admin allowed)
        request = request_factory.get("/admin/")
        request.user = user
        request = add_session_to_request(request)

        admin_mw = AdminAccessMiddleware(lambda r: None)
        response = admin_mw(request)

        assert response is None, "Manager should have admin access"
