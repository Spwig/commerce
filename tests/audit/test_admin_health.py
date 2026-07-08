"""
Admin Page Health Tests

Uses Playwright to visit every admin sidebar page and assert
no HTTP errors, console errors, or missing resources.
"""
import pytest

from tests.audit.admin_audit import run_admin_audit

pytestmark = [pytest.mark.django_db, pytest.mark.e2e, pytest.mark.site_health, pytest.mark.slow]


class TestAdminPageHealth:
    """Every admin page should load cleanly."""

    @pytest.fixture(autouse=True)
    def _run_audit(self, admin_authenticated_page, site_settings):
        """Run the admin audit once and share results across tests."""
        base_url = admin_authenticated_page._live_server_url
        self.report = run_admin_audit(
            admin_authenticated_page, base_url, verbose=False,
        )

    def test_all_admin_pages_return_200(self):
        """Every admin sidebar page returns HTTP 200."""
        errors = self.report.http_errors
        assert not errors, (
            f"{len(errors)} admin pages returned HTTP errors:\n"
            + "\n".join(f"  [{r.status_code}] {r.label}: {r.url}" for r in errors)
        )

    def test_no_admin_console_errors(self):
        """No JavaScript console errors on admin pages."""
        pages = self.report.error_pages
        assert not pages, (
            f"{len(pages)} admin pages have console errors:\n"
            + "\n".join(
                f"  {r.label}: {r.console_errors[:3]}" for r in pages
            )
        )

    def test_no_admin_404_resources(self):
        """No missing sub-resources (CSS, JS, images) on admin pages."""
        pages = self.report.failed_request_pages
        assert not pages, (
            f"{len(pages)} admin pages have missing resources:\n"
            + "\n".join(
                f"  {r.label}: {r.failed_requests[:3]}" for r in pages
            )
        )

    def test_no_slow_admin_pages(self):
        """No admin page takes longer than 5 seconds to load."""
        slow = [r for r in self.report.results if r.load_time_ms > 5000]
        assert not slow, (
            f"{len(slow)} admin pages are slow:\n"
            + "\n".join(
                f"  {r.load_time_ms}ms {r.label}: {r.url}" for r in slow
            )
        )

    def test_no_navigation_failures(self):
        """No admin pages fail to load entirely."""
        failures = self.report.exception_pages
        assert not failures, (
            f"{len(failures)} admin pages failed to load:\n"
            + "\n".join(
                f"  {r.label}: {r.exception}" for r in failures
            )
        )
