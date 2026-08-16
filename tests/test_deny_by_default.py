"""Direction B — deny-by-default staff access + the add-staff role picker.

- A staff user with no role (and not a superuser) can't access the admin and is
  read-only. Superusers are always exempt (single-owner stores unaffected).
- The add-staff form requires a password and at least one role, and assigns the
  role on create so a new staff member is never locked out.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.sessions.backends.db import SessionStore
from django.core.cache import cache
from django.http import HttpResponse
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from staff_roles.models import StaffRole
from staff_roles.services import (
    can_access_admin,
    invalidate_user_cache,
    is_effectively_read_only,
)

User = get_user_model()


def make_role(name, *, admin_access, categories=None):
    group = Group.objects.create(name=name)
    return StaffRole.objects.create(
        group=group,
        display_name=name.title(),
        can_access_admin=admin_access,
        permission_categories=categories or {},
    )


def _ensure_site_settings():
    """Currency middleware needs a valid SiteSettings(pk=1) on every request."""
    from django.contrib.sites.models import Site

    from core.models import SiteSettings

    Site.objects.update_or_create(pk=1, defaults={"domain": "localhost", "name": "Test Site"})
    SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            "admin_email": "admin@example.com",
            "default_currency": "USD",
            "enable_multi_warehouse": False,
        },
    )


class DenyByDefaultTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_superuser_is_exempt(self):
        su = User.objects.create_superuser("su", "su@t.co", "pw")
        self.assertTrue(can_access_admin(su))
        self.assertFalse(is_effectively_read_only(su))

    def test_roleless_staff_is_denied_and_readonly(self):
        u = User.objects.create_user("s1", "s1@t.co", "pw", is_staff=True)
        self.assertFalse(can_access_admin(u), "role-less staff must be denied admin")
        self.assertTrue(is_effectively_read_only(u), "role-less staff must be read-only")

    def test_role_with_admin_and_full_grants_access(self):
        role = make_role("manager", admin_access=True, categories={"orders": "full"})
        u = User.objects.create_user("s2", "s2@t.co", "pw", is_staff=True)
        u.groups.add(role.group)
        invalidate_user_cache(u)
        self.assertTrue(can_access_admin(u))
        self.assertFalse(is_effectively_read_only(u))

    def test_pos_only_role_denied_admin_and_readonly(self):
        role = make_role("cashier", admin_access=False, categories={})
        u = User.objects.create_user("s3", "s3@t.co", "pw", is_staff=True)
        u.groups.add(role.group)
        invalidate_user_cache(u)
        self.assertFalse(can_access_admin(u))
        self.assertTrue(is_effectively_read_only(u))


@override_settings(ALLOWED_HOSTS=["testserver", "localhost"])
class AddStaffFormTests(TestCase):
    def setUp(self):
        cache.clear()
        _ensure_site_settings()
        self.superuser = User.objects.create_superuser("owner", "owner@t.co", "pw")
        self.client.force_login(self.superuser)
        self.role = make_role("manager", admin_access=True, categories={"orders": "full"})
        self.add_url = reverse("admin:accounts_staffmember_add")

    def _post(self, **overrides):
        data = {
            "email": "new@t.co",
            "first_name": "New",
            "last_name": "Staff",
            "username": "newstaff",
            "password1": "Str0ng!passw0rd",
            "password2": "Str0ng!passw0rd",
            "roles": [self.role.pk],
        }
        data.update(overrides)
        return self.client.post(self.add_url, data)

    def test_role_is_required(self):
        resp = self._post(roles=[])
        self.assertEqual(resp.status_code, 200)  # re-render with errors
        self.assertFalse(User.objects.filter(username="newstaff").exists())

    def test_password_mismatch_rejected(self):
        resp = self._post(password2="different")
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(User.objects.filter(username="newstaff").exists())

    def test_valid_create_sets_password_role_and_grants_access(self):
        resp = self._post()
        self.assertEqual(
            resp.status_code, 302, getattr(resp, "context", None) and resp.context["errors"]
        )
        u = User.objects.get(username="newstaff")
        self.assertTrue(u.is_staff)
        self.assertTrue(u.check_password("Str0ng!passw0rd"))
        self.assertIn(self.role.group, u.groups.all())
        invalidate_user_cache(u)
        self.assertTrue(can_access_admin(u), "newly created + roled staff should reach the admin")


class AdminAccessDenyMiddlewareTests(TestCase):
    """The deny path must redirect, not 500.

    AdminAccessMiddleware runs before MessageMiddleware, so request._messages
    isn't set up when it denies access — using the messages framework directly
    there raises MessageFailure. Regression for that (the deny path builds its
    own message storage instead).
    """

    def setUp(self):
        cache.clear()

    def test_roleless_staff_is_redirected_without_messagefailure(self):
        from core.middleware.admin_access import AdminAccessMiddleware

        user = User.objects.create_user("s5", "s5@t.co", "pw", is_staff=True)
        request = RequestFactory().get("/en/admin/catalog/product/")
        request.user = user
        request.session = SessionStore()  # no request._messages — the bug condition

        middleware = AdminAccessMiddleware(lambda r: HttpResponse("should not reach the view"))
        response = middleware(request)  # must not raise MessageFailure

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")
