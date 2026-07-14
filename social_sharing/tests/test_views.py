"""
Social Sharing Admin View Tests
"""

from django.contrib.sites.models import Site
from django.test import TestCase

from social_sharing.tests.factories import (
    create_share_count,
    create_social_share,
    create_user,
    get_product_content_type,
)


def _ensure_site_and_settings():
    """Ensure Django Site and SiteSettings exist for middleware."""
    Site.objects.get_or_create(pk=1, defaults={"domain": "testserver", "name": "Test"})
    from core.models import SiteSettings

    if not SiteSettings.objects.filter(pk=1).exists():
        SiteSettings.objects.create(
            pk=1,
            site_name="Test Store",
            admin_email="test@test.spwig.com",
            default_currency="USD",
        )


class DashboardViewTest(TestCase):
    """Tests for the social sharing dashboard admin view."""

    def setUp(self):
        _ensure_site_and_settings()
        self.admin = create_user(email="admin@test.spwig.com", is_staff=True)
        self.client.login(username="admin@test.spwig.com", password="testpass123")

    def test_dashboard_requires_staff(self):
        self.client.logout()
        resp = self.client.get("/en/admin/social_sharing/dashboard/")
        self.assertNotEqual(resp.status_code, 200)

    def test_dashboard_accessible_by_staff(self):
        resp = self.client.get("/en/admin/social_sharing/dashboard/")
        self.assertEqual(resp.status_code, 200)

    def test_dashboard_context_has_kpi_data(self):
        create_social_share(platform="facebook")
        resp = self.client.get("/en/admin/social_sharing/dashboard/")
        self.assertIn("total_shares", resp.context)
        self.assertIn("shares_today", resp.context)
        self.assertIn("shares_trend_json", resp.context)
        self.assertIn("platform_distribution_json", resp.context)

    def test_dashboard_uses_json_script_safe_data(self):
        """Dashboard should use json_script instead of |safe for XSS prevention."""
        create_social_share(platform="facebook")
        resp = self.client.get("/en/admin/social_sharing/dashboard/")
        content = resp.content.decode()
        self.assertIn('id="shares-trend-data"', content)
        self.assertIn('id="platform-dist-data"', content)


class FilterSharesViewTest(TestCase):
    """Tests for AJAX share filtering view."""

    def setUp(self):
        _ensure_site_and_settings()
        self.admin = create_user(email="admin2@test.spwig.com", is_staff=True)
        self.client.login(username="admin2@test.spwig.com", password="testpass123")
        self.ct = get_product_content_type()

    def test_filter_shares_requires_staff(self):
        self.client.logout()
        resp = self.client.get("/en/admin/social_sharing/socialshare/filter/")
        self.assertNotEqual(resp.status_code, 200)

    def test_filter_shares_returns_json(self):
        create_social_share(platform="facebook", content_type=self.ct)
        resp = self.client.get(
            "/en/admin/social_sharing/socialshare/filter/", HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "application/json")

    def test_filter_by_platform(self):
        create_social_share(platform="facebook", content_type=self.ct, object_id=500)
        create_social_share(platform="twitter", content_type=self.ct, object_id=501)
        resp = self.client.get(
            "/en/admin/social_sharing/socialshare/filter/",
            {"platform": "facebook"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.status_code, 200)


class FilterShareCountsViewTest(TestCase):
    """Tests for AJAX share count filtering view."""

    def setUp(self):
        _ensure_site_and_settings()
        self.admin = create_user(email="admin3@test.spwig.com", is_staff=True)
        self.client.login(username="admin3@test.spwig.com", password="testpass123")
        self.ct = get_product_content_type()

    def test_filter_sharecounts_requires_staff(self):
        self.client.logout()
        resp = self.client.get("/en/admin/social_sharing/sharecount/filter/")
        self.assertNotEqual(resp.status_code, 200)

    def test_filter_sharecounts_returns_json(self):
        create_share_count(platform="facebook", content_type=self.ct, count=5, object_id=600)
        resp = self.client.get(
            "/en/admin/social_sharing/sharecount/filter/", HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "application/json")
