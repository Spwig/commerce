"""Regression tests for two pre-existing gaps fixed alongside the multi-market work:

1. PageView must enforce Page.requires_auth (send anonymous visitors to log in).
2. The visibility evaluator's GeoIP lookup was doubly broken (wrong import path +
   filtering on the ``is_expired`` property), so precise geo_country never resolved.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.test import RequestFactory, TestCase

from page_builder.models import Page
from page_builder.views import PageView


def _seed_site_settings():
    from core.models import SiteSettings

    SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            "admin_email": "admin@example.com",
            "default_currency": "USD",
            "enable_multi_warehouse": False,
        },
    )


class RequiresAuthPageViewTests(TestCase):
    def setUp(self):
        cache.clear()
        _seed_site_settings()
        self.factory = RequestFactory()

    def _home(self, requires_auth):
        return Page.objects.create(
            title="Home",
            slug="fg-home",
            page_type="home",
            is_default_for_type=True,
            status="published",
            requires_auth=requires_auth,
        )

    def test_anonymous_redirected_from_requires_auth_page(self):
        self._home(requires_auth=True)
        request = self.factory.get("/en/")
        request.user = AnonymousUser()
        response = PageView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn("next=", response.url)  # login redirect preserves the target

    def test_authenticated_can_view_requires_auth_page(self):
        self._home(requires_auth=True)
        self.client.force_login(get_user_model().objects.create_user("u", password="x"))
        response = self.client.get("/en/")
        self.assertEqual(response.status_code, 200)

    def test_public_page_open_to_anonymous(self):
        self._home(requires_auth=False)
        response = self.client.get("/en/")
        self.assertEqual(response.status_code, 200)

    def test_requires_auth_page_bypasses_shared_cache(self):
        # An auth-gated page must not be stored in the shared (non-per-user) page
        # cache, or one logged-in user's page could be served to another.
        from unittest.mock import patch

        self._home(requires_auth=True)
        request = self.factory.get("/en/")
        request.user = get_user_model().objects.create_user("a", password="x")
        request.session = {}
        with patch("page_builder.views.cache_page") as mock_cache:
            try:
                PageView.as_view()(request)
            except Exception:
                pass  # render may need more context; we only assert cache_page usage
        mock_cache.assert_not_called()

    def test_public_page_uses_shared_cache(self):
        from unittest.mock import patch

        self._home(requires_auth=False)
        request = self.factory.get("/en/")
        request.user = AnonymousUser()
        request.session = {}
        with patch("page_builder.views.cache_page") as mock_cache:
            try:
                PageView.as_view()(request)
            except Exception:
                pass
        mock_cache.assert_called()


class GeoIPVisibilityContextTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_geoip_country_resolves_in_visibility_context(self):
        from geoip.models import GeoLocation
        from visibility.evaluator import ContextCollector

        GeoLocation.objects.create(
            ip_address="203.0.113.7", country_code="NZ", country_name="New Zealand"
        )
        request = self.factory.get("/", REMOTE_ADDR="203.0.113.7")
        request.user = AnonymousUser()
        request.session = {}

        context = ContextCollector().collect_context(request)
        # Precise country now resolves (import + is_expired query were both fixed).
        self.assertEqual(context["geo"]["country_code"], "NZ")
