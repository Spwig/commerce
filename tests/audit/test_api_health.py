"""
API Endpoint Health Tests

Uses Django test client (no browser needed) to verify API endpoints
exist and don't crash. Fast tests suitable for CI.
"""
import pytest

pytestmark = [pytest.mark.django_db, pytest.mark.site_health]


class TestHealthEndpoints:
    """Health check endpoints must always return 200."""

    @pytest.mark.parametrize("path,label", [
        ("/health/", "Basic health"),
        ("/health/live/", "Liveness probe"),
        ("/health/ready/", "Readiness probe"),
    ])
    def test_health_endpoint_returns_200(self, client, site_settings, django_site, path, label):
        resp = client.get(path)
        assert resp.status_code == 200, f"{label} returned {resp.status_code}"

    def test_detailed_health_requires_auth(self, client, site_settings, django_site):
        """Detailed health check should not be publicly accessible."""
        resp = client.get("/health/detailed/")
        # Should require auth (302 redirect or 403)
        assert resp.status_code in (302, 403), (
            f"Detailed health is publicly accessible (status {resp.status_code})"
        )

    def test_detailed_health_works_for_admin(self, admin_client, site_settings, django_site):
        """Detailed health check should work for admin users."""
        resp = admin_client.get("/health/detailed/")
        assert resp.status_code == 200, (
            f"Detailed health returned {resp.status_code} for admin"
        )


class TestPublicAPIEndpoints:
    """Public API endpoints should exist and not crash."""

    @pytest.mark.parametrize("path,label", [
        ("/api/store/info/", "Store info"),
        ("/api/catalog/products/", "Catalog products"),
        ("/api/blog/posts/", "Blog posts"),
        ("/api/currencies/active/", "Active currencies"),
    ])
    def test_public_api_no_500(self, client, site_settings, django_site, path, label):
        """Public API endpoints should never return 500."""
        resp = client.get(path)
        assert resp.status_code != 500, f"{label} returned 500 (server error)"
        assert resp.status_code != 404, f"{label} returned 404 (endpoint missing)"


class TestAuthenticatedAPIEndpoints:
    """Authenticated API endpoints should not crash."""

    @pytest.fixture
    def admin_client(self, admin_user, client):
        """Django test client logged in as admin."""
        client.force_login(admin_user)
        return client

    @pytest.fixture
    def customer_client(self, customer_user, client):
        """Django test client logged in as customer."""
        client.force_login(customer_user)
        return client

    def test_translation_health(self, admin_client, site_settings):
        resp = admin_client.get("/api/translation/health/")
        assert resp.status_code == 200, f"Translation health returned {resp.status_code}"

    def test_cart_api_no_500(self, customer_client, site_settings):
        resp = customer_client.get("/api/cart/")
        assert resp.status_code != 500, f"Cart API returned 500"

    def test_checkout_api_no_500(self, customer_client, site_settings):
        resp = customer_client.get("/api/checkout/")
        assert resp.status_code != 500, f"Checkout API returned 500"
