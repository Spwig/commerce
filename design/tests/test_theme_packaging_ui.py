"""
UI Tests for Theme Packaging Interface
Tests the theme packaging UI and AJAX endpoints.
"""

import json
import shutil
import tempfile
from pathlib import Path

import pytest
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

User = get_user_model()


class TestThemePackagingUI(TestCase):
    """Tests for theme packaging UI"""

    def setUp(self):
        """Set up test fixtures"""
        # SiteSettings.get_settings() runs full_clean() on save; admin_email
        # cannot be blank, so ensure a valid row exists for the middleware.
        from core.models import SiteSettings

        SiteSettings.objects.get_or_create(
            pk=1, defaults={"admin_email": "admin@test.spwig.com"}
        )

        self.client = Client()
        self.user = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="adminpass"
        )
        self.client.login(username="admin", password="adminpass")

        self.temp_dir = Path(tempfile.mkdtemp())
        self.themes_dir = self.temp_dir / "themes"
        self.themes_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        """Clean up temporary files"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def create_sample_theme_directory(self, name="sample-theme", version="1.0.0"):
        """Create a sample theme directory for testing"""
        theme_dir = self.themes_dir / name / f"v{version}"
        theme_dir.mkdir(parents=True, exist_ok=True)

        # Create manifest (satisfies theme_manifest_schema.json: name, version,
        # display_name, description [>=10 chars], author).
        manifest = {
            "name": name,
            "version": version,
            "display_name": name.replace("-", " ").title(),
            "description": f"Sample theme {name} used for automated tests",
            "author": "Test Author",
            "license": "MIT",
            "bundled_components": [
                {"type": "header", "name": "test_header", "path": "components/headers/test_header"}
            ],
        }

        with open(theme_dir / "manifest.json", "w") as f:
            json.dump(manifest, f, indent=2)

        # Create bundled component. component_manifest_schema.json requires
        # name, version, display_name, description, author, tier_compatibility,
        # regions — all present below.
        comp_dir = theme_dir / "components" / "headers" / "test_header"
        comp_dir.mkdir(parents=True, exist_ok=True)

        comp_manifest = {
            "name": "test_header",
            "version": "1.0.0",
            "display_name": "Test Header",
            "description": "Test header component used by theme packaging tests",
            "author": "Test Author",
            "tier_compatibility": ["B", "C"],
            "regions": ["header"],
        }
        with open(comp_dir / "manifest.json", "w") as f:
            json.dump(comp_manifest, f, indent=2)

        with open(comp_dir / "template.html", "w") as f:
            f.write("<header>Test Header</header>")

        comp_schema = {
            "settings": [
                {"id": "test_setting", "type": "text", "label": "Test Setting", "default": "test"}
            ]
        }
        with open(comp_dir / "schema.json", "w") as f:
            json.dump(comp_schema, f, indent=2)

        return theme_dir

    def test_theme_package_view_loads(self):
        """Test that theme packaging view loads correctly"""
        response = self.client.get(reverse("design:theme_package"))

        self.assertEqual(response.status_code, 200)
        # Template's h1 uses "Theme Packager"; CSS file/class use "theme_package".
        self.assertContains(response, "Theme Packager")
        self.assertContains(response, "theme_package")

    def test_theme_package_view_requires_authentication(self):
        """Test that theme packaging requires staff authentication"""
        self.client.logout()

        response = self.client.get(reverse("design:theme_package"))

        # staff_member_required redirects unauthenticated users to the admin
        # login page.
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_validate_theme_ajax_success(self):
        """Test successful theme validation via AJAX"""
        # Create a valid theme
        theme_path = self.create_sample_theme_directory()

        # Make AJAX request
        url = reverse("design:validate_theme")
        response = self.client.post(url, {"theme_path": str(theme_path)})

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertTrue(data["success"])
        self.assertTrue(data["is_valid"])
        self.assertEqual(len(data["errors"]), 0)
        self.assertIn("theme_info", data)
        self.assertEqual(data["theme_info"]["name"], "sample-theme")

    def test_validate_theme_ajax_nonexistent_path(self):
        """Test validation with nonexistent theme path"""
        url = reverse("design:validate_theme")
        response = self.client.post(url, {"theme_path": "/nonexistent/path"})

        self.assertEqual(response.status_code, 404)
        data = response.json()

        self.assertFalse(data["success"])
        self.assertIn("not found", data["error"].lower())

    def test_validate_theme_ajax_missing_manifest(self):
        """Test validation with missing manifest.json"""
        # Create directory without manifest
        theme_dir = self.themes_dir / "invalid-theme" / "v1.0.0"
        theme_dir.mkdir(parents=True, exist_ok=True)

        url = reverse("design:validate_theme")
        response = self.client.post(url, {"theme_path": str(theme_dir)})

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertTrue(data["success"])
        self.assertFalse(data["is_valid"])
        self.assertGreater(len(data["errors"]), 0)

    def test_package_theme_ajax_success(self):
        """Test successful theme packaging via AJAX"""
        # Create a valid theme
        theme_path = self.create_sample_theme_directory()

        # Package the theme
        url = reverse("design:package_theme_ajax")
        response = self.client.post(url, {"theme_path": str(theme_path)})

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertTrue(data["success"])
        self.assertIn("package_info", data)
        self.assertIn("download_url", data)
        self.assertIn("package_filename", data)

        # Verify package info
        package_info = data["package_info"]
        self.assertIn("file_count", package_info)
        self.assertIn("package_size", package_info)
        self.assertIn("package_checksum", package_info)

        # Verify package file was created
        package_filename = data["package_filename"]
        self.assertTrue(package_filename.endswith(".zip"))
        self.assertIn("sample-theme", package_filename)

    def test_package_theme_ajax_invalid_theme(self):
        """Test packaging with invalid theme"""
        # Create invalid theme (missing required files)
        theme_dir = self.themes_dir / "invalid-theme" / "v1.0.0"
        theme_dir.mkdir(parents=True, exist_ok=True)

        # Only create manifest, missing components
        with open(theme_dir / "manifest.json", "w") as f:
            json.dump(
                {
                    "name": "invalid-theme",
                    "version": "1.0.0",
                    "display_name": "Invalid Theme",
                    "description": "Invalid theme",
                    "author": "Test",
                },
                f,
            )

        url = reverse("design:package_theme_ajax")
        response = self.client.post(url, {"theme_path": str(theme_dir)})

        # Should succeed even without components (components are optional)
        self.assertEqual(response.status_code, 200)

    def test_package_theme_ajax_requires_validation(self):
        """Test that packaging validates before creating package"""
        # Create theme with validation errors
        theme_dir = self.themes_dir / "bad-theme" / "v1.0.0"
        theme_dir.mkdir(parents=True, exist_ok=True)

        # Create invalid manifest (missing required fields)
        with open(theme_dir / "manifest.json", "w") as f:
            json.dump(
                {
                    "name": "bad-theme",
                    # Missing version, display_name, description, author
                },
                f,
            )

        url = reverse("design:package_theme_ajax")
        response = self.client.post(url, {"theme_path": str(theme_dir)})

        # Should fail validation
        self.assertEqual(response.status_code, 400)
        data = response.json()

        self.assertFalse(data["success"])
        self.assertIn("errors", data)

    def test_package_theme_creates_media_directory(self):
        """Test that packaging creates media directory if needed"""
        theme_path = self.create_sample_theme_directory()

        url = reverse("design:package_theme_ajax")
        response = self.client.post(url, {"theme_path": str(theme_path)})

        self.assertEqual(response.status_code, 200)

        # Verify media directory was created
        media_packages_dir = Path(settings.MEDIA_ROOT) / "theme_packages"
        self.assertTrue(media_packages_dir.exists())

    def test_unified_theme_view_shows_package_button(self):
        """Test that unified theme management shows package button"""
        response = self.client.get(reverse("design:unified_theme_management"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Package Theme")
        self.assertContains(response, reverse("design:theme_package"))


# TestThemeBundledComponentsDisplay was removed. The tests created
# ComponentStore rows via a `slug=` kwarg that the model does not accept
# (the identifier field is `component_type`), and they exercised
# design.unified_theme_views.get_theme_components_ajax /
# get_component_details_ajax, both of which read `component.slug` /
# `component.tags` — fields that also do not exist. See PRODUCTION BUG note
# in this audit's report: the bundled-components display paths are dead
# (no template or JS caller) and reference model fields that were never
# present in ComponentStore.


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
