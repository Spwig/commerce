"""
Tests for the POS license middleware.

Verifies that /api/pos/ endpoints are gated behind a valid POS license,
while non-POS paths remain unaffected.
"""

import pytest

from tests.helpers import assert_pos_error

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.pos]


class TestPOSLicenseMiddleware:
    """POSLicenseMiddleware gates /api/pos/ behind a valid license."""

    def test_valid_license_allows_request(self, pos_client):
        """With a valid license (autouse fixture), POS endpoints are reachable."""
        response = pos_client.get("/api/pos/auth/me/")
        # Should not be 403 - the middleware lets the request through.
        # The actual status depends on auth/endpoint logic, but it must not
        # be a license-gated 403.
        assert response.status_code != 403

    def test_invalid_license_blocks_pos_api(self, anon_client, monkeypatch):
        """An invalid license returns 403 for /api/pos/ endpoints."""
        monkeypatch.setattr("pos_app.license.pos_license_is_valid", lambda: False)

        response = anon_client.get("/api/pos/auth/me/")
        assert_pos_error(response, "POS_LICENSE_REQUIRED", http_status=403)

    def test_invalid_license_error_format(self, anon_client, monkeypatch):
        """The 403 response has the exact POS error envelope structure."""
        monkeypatch.setattr("pos_app.license.pos_license_is_valid", lambda: False)

        response = anon_client.get("/api/pos/catalog/products/")
        data = response.json()

        assert data["success"] is False
        assert "error" in data
        assert data["error"]["code"] == "POS_LICENSE_REQUIRED"
        assert isinstance(data["error"]["message"], str)
        assert len(data["error"]["message"]) > 0

    def test_non_pos_api_unaffected(self, anon_client, monkeypatch):
        """Non-POS API paths are not blocked even when the license is invalid."""
        monkeypatch.setattr("pos_app.license.pos_license_is_valid", lambda: False)

        response = anon_client.get("/api/cart/mini/")
        # Must not be a license-gated 403.  Whatever status the cart API
        # returns (200, 401, etc.) it should never be the POS license error.
        assert response.status_code != 403 or (
            response.status_code == 403
            and response.json().get("error", {}).get("code") != "POS_LICENSE_REQUIRED"
        )

    def test_pos_static_paths_unaffected(self, anon_client, monkeypatch):
        """/pos/ and /pos/assets/ are not gated by the license middleware."""
        monkeypatch.setattr("pos_app.license.pos_license_is_valid", lambda: False)

        for path in ["/pos/", "/pos/assets/"]:
            response = anon_client.get(path)
            # These paths serve the SPA shell / static assets, not the API.
            # They must never receive the POS license 403 JSON error.
            if response.status_code == 403:
                data = response.json() if response["content-type"] == "application/json" else {}
                assert data.get("error", {}).get("code") != "POS_LICENSE_REQUIRED", (
                    f"Path {path} was incorrectly blocked by POS license middleware"
                )
