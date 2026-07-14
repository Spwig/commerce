"""
Storefront Page Health Tests

Uses Playwright to visit customer-facing pages and assert
they load without errors.
"""

import pytest

from tests.audit.engine import visit_page_browser

pytestmark = [pytest.mark.django_db, pytest.mark.e2e, pytest.mark.site_health, pytest.mark.slow]


class TestStorefrontPublicPages:
    """Pages accessible without authentication."""

    @pytest.mark.parametrize(
        "path,label",
        [
            ("/en/", "Home"),
            ("/en/products/", "Products listing"),
            ("/en/cart/", "Cart"),
            ("/en/blog/", "Blog listing"),
            ("/en/search/?q=test", "Search results"),
        ],
    )
    def test_public_page_returns_200(self, page, site_settings, path, label):
        base = page._live_server_url
        result = visit_page_browser(page, path, label, base, "storefront")
        assert result.status_code == 200, f"{label} returned {result.status_code}" + (
            f" — Django: {result.django_error}" if result.django_error else ""
        )

    @pytest.mark.parametrize(
        "path,label",
        [
            ("/en/", "Home"),
            ("/en/products/", "Products listing"),
            ("/en/cart/", "Cart"),
            ("/en/blog/", "Blog listing"),
        ],
    )
    def test_public_page_no_console_errors(self, page, site_settings, path, label):
        base = page._live_server_url
        result = visit_page_browser(page, path, label, base, "storefront")
        assert not result.console_errors, f"{label} has console errors: {result.console_errors[:3]}"


class TestStorefrontDataPages:
    """Pages that require test data to render properly."""

    def test_category_page(self, page, site_settings, audit_storefront_data):
        base = page._live_server_url
        slug = audit_storefront_data["category"].slug
        result = visit_page_browser(
            page,
            f"/en/category/{slug}/",
            "Category page",
            base,
            "storefront",
        )
        assert result.status_code == 200, f"Category page returned {result.status_code}"
        assert not result.console_errors, f"Console errors: {result.console_errors[:3]}"

    def test_product_page(self, page, site_settings, audit_storefront_data):
        base = page._live_server_url
        slug = audit_storefront_data["product"].slug
        result = visit_page_browser(
            page,
            f"/en/product/{slug}/",
            "Product page",
            base,
            "storefront",
        )
        assert result.status_code == 200, f"Product page returned {result.status_code}"
        assert not result.console_errors, f"Console errors: {result.console_errors[:3]}"


class TestStorefrontAuthenticatedPages:
    """Pages that require customer login."""

    @pytest.mark.parametrize(
        "path,label",
        [
            ("/en/account/dashboard/", "Account dashboard"),
            ("/en/account/addresses/", "Address list"),
            ("/en/account/profile/", "Profile"),
        ],
    )
    def test_authenticated_page_returns_200(self, authenticated_page, site_settings, path, label):
        base = authenticated_page._live_server_url
        result = visit_page_browser(
            authenticated_page,
            path,
            label,
            base,
            "storefront",
        )
        # Account pages should return 200 (or redirect to login which is also 200)
        assert result.status_code == 200, f"{label} returned {result.status_code}"
