"""
Tests for Theme Packager

Tests theme packaging functionality including validation and ZIP package creation.
"""

import json
import zipfile
from pathlib import Path

import pytest

from design.theme_packager import ThemePackager, ThemePackagingError


@pytest.fixture
def temp_theme_dir(tmp_path):
    """Create temporary theme directory structure."""
    theme_dir = tmp_path / "test_theme"
    theme_dir.mkdir()
    return theme_dir


@pytest.fixture
def valid_theme_manifest():
    """Valid theme manifest data."""
    return {
        "name": "test-theme",
        "version": "1.0.0",
        "display_name": "Test Theme",
        "description": "A test theme for unit testing the packaging system",
        "author": "Spwig",
        "license": "Proprietary",
        "bundled_components": [
            {"type": "header", "name": "mega_menu", "path": "components/headers/mega_menu"},
            {"type": "footer", "name": "footer_links", "path": "components/footers/footer_links"},
        ],
        "page_schemas": {"home": "page_schemas/home.json", "product": "page_schemas/product.json"},
        "design_tokens": "theme/tokens.json",
        "preview_image": "preview.png",
        "screenshots": ["screenshot1.png", "screenshot2.png"],
        "categories": ["general"],
        "tags": ["modern", "responsive"],
    }


@pytest.fixture
def create_valid_theme(temp_theme_dir, valid_theme_manifest):
    """Create a complete valid theme directory structure."""

    def _create_theme(manifest_data=None):
        if manifest_data is None:
            manifest_data = valid_theme_manifest

        # Create manifest
        with open(temp_theme_dir / "manifest.json", "w") as f:
            json.dump(manifest_data, f, indent=2)

        # Create bundled components
        for component in manifest_data.get("bundled_components", []):
            comp_dir = temp_theme_dir / component["path"]
            comp_dir.mkdir(parents=True, exist_ok=True)

            # Create component manifest
            comp_manifest = {
                "name": component["name"],
                "version": "1.0.0",
                "display_name": component["name"].replace("_", " ").title(),
                "description": f"Test {component['type']} component",
                "author": "Spwig",
                "tier_compatibility": ["B", "C"],
                "regions": [component["type"]],
                "category": component["type"],
            }
            with open(comp_dir / "manifest.json", "w") as f:
                json.dump(comp_manifest, f, indent=2)

            # Create component template
            with open(comp_dir / "template.html", "w") as f:
                f.write(f"<div class='{component['name']}'></div>")

            # Create component schema
            comp_schema = {"type": "object", "properties": {"title": {"type": "string"}}}
            with open(comp_dir / "schema.json", "w") as f:
                json.dump(comp_schema, f, indent=2)

        # Create page schemas
        if "page_schemas" in manifest_data:
            for page_type, schema_path in manifest_data["page_schemas"].items():
                schema_file = temp_theme_dir / schema_path
                schema_file.parent.mkdir(parents=True, exist_ok=True)
                page_schema = {"page_type": page_type, "regions": ["header", "content", "footer"]}
                with open(schema_file, "w") as f:
                    json.dump(page_schema, f, indent=2)

        # Create design tokens
        if "design_tokens" in manifest_data:
            tokens_file = temp_theme_dir / manifest_data["design_tokens"]
            tokens_file.parent.mkdir(parents=True, exist_ok=True)
            tokens = {"colors": {"primary": "#007bff", "secondary": "#6c757d"}}
            with open(tokens_file, "w") as f:
                json.dump(tokens, f, indent=2)

        # Create preview image (1KB dummy file)
        if "preview_image" in manifest_data:
            preview_file = temp_theme_dir / manifest_data["preview_image"]
            with open(preview_file, "wb") as f:
                f.write(b"PNG_DUMMY_DATA" * 100)  # ~1.4KB

        # Create screenshots
        if "screenshots" in manifest_data:
            for screenshot in manifest_data["screenshots"]:
                screenshot_file = temp_theme_dir / screenshot
                with open(screenshot_file, "wb") as f:
                    f.write(b"PNG_DUMMY_DATA" * 100)  # ~1.4KB each

        return temp_theme_dir

    return _create_theme


class TestThemePackagerInitialization:
    """Tests for ThemePackager initialization."""

    def test_packager_initialization(self, temp_theme_dir):
        """Test ThemePackager initializes correctly."""
        packager = ThemePackager(temp_theme_dir)
        assert packager.theme_dir == temp_theme_dir
        assert packager.manifest is None
        assert packager.errors == []
        assert packager.warnings == []

    def test_packager_loads_schema(self, temp_theme_dir):
        """Test ThemePackager loads theme manifest schema."""
        packager = ThemePackager(temp_theme_dir)
        assert packager.theme_schema is not None
        assert isinstance(packager.theme_schema, dict)
        assert packager.theme_schema.get("title") == "Theme Package Manifest Schema"


class TestThemeValidation:
    """Tests for theme validation."""

    def test_valid_theme_passes_validation(self, create_valid_theme):
        """Test valid theme passes all validation checks."""
        theme_dir = create_valid_theme()
        packager = ThemePackager(theme_dir)

        is_valid, errors, warnings = packager.validate()

        assert is_valid is True
        assert len(errors) == 0
        assert packager.manifest is not None

    def test_missing_directory_fails(self, tmp_path):
        """Test validation fails for non-existent directory."""
        non_existent = tmp_path / "does_not_exist"
        packager = ThemePackager(non_existent)

        is_valid, errors, warnings = packager.validate()

        assert is_valid is False
        assert any("does not exist" in err for err in errors)

    def test_path_not_directory_fails(self, tmp_path):
        """Test validation fails when path is not a directory."""
        file_path = tmp_path / "not_a_dir.txt"
        file_path.write_text("test")
        packager = ThemePackager(file_path)

        is_valid, errors, warnings = packager.validate()

        assert is_valid is False
        assert any("not a directory" in err for err in errors)

    def test_missing_manifest_fails(self, temp_theme_dir):
        """Test validation fails when manifest.json is missing."""
        packager = ThemePackager(temp_theme_dir)

        is_valid, errors, warnings = packager.validate()

        assert is_valid is False
        assert any("manifest.json" in err for err in errors)

    def test_invalid_manifest_json_fails(self, temp_theme_dir):
        """Test validation fails for invalid JSON in manifest."""
        # Create invalid JSON
        with open(temp_theme_dir / "manifest.json", "w") as f:
            f.write("{invalid json")

        packager = ThemePackager(temp_theme_dir)
        is_valid, errors, warnings = packager.validate()

        assert is_valid is False
        assert any("JSON" in err or "manifest" in err for err in errors)


class TestManifestValidation:
    """Tests for theme manifest validation."""

    def test_valid_manifest_passes(self, create_valid_theme):
        """Test valid manifest passes schema validation."""
        theme_dir = create_valid_theme()
        packager = ThemePackager(theme_dir)

        is_valid, errors, warnings = packager.validate()

        assert is_valid is True
        assert packager.manifest["name"] == "test-theme"
        assert packager.manifest["version"] == "1.0.0"

    def test_missing_required_field_fails(self, create_valid_theme, valid_theme_manifest):
        """Test validation fails when required field is missing."""
        # Remove required field
        manifest = valid_theme_manifest.copy()
        del manifest["name"]

        theme_dir = create_valid_theme(manifest)
        packager = ThemePackager(theme_dir)

        is_valid, errors, warnings = packager.validate()

        assert is_valid is False
        assert any("name" in err.lower() for err in errors)

    # Removed test_invalid_name_format_fails: the theme_manifest_schema.json
    # only constrains "name" by minLength/maxLength (schema declares it as a
    # "Human-readable theme name"), so "Invalid Name With Spaces" is valid.
    # The test previously assumed a slug-only pattern that the schema does
    # not enforce, and there is no separate pattern check in ThemePackager.

    def test_invalid_version_format_fails(self, create_valid_theme, valid_theme_manifest):
        """Test validation fails for invalid version format."""
        manifest = valid_theme_manifest.copy()
        manifest["version"] = "1.0"  # Missing patch version

        theme_dir = create_valid_theme(manifest)
        packager = ThemePackager(theme_dir)

        is_valid, errors, warnings = packager.validate()

        assert is_valid is False

    def test_invalid_license_fails(self, create_valid_theme, valid_theme_manifest):
        """Test validation fails for invalid license value."""
        manifest = valid_theme_manifest.copy()
        manifest["license"] = "InvalidLicense"

        theme_dir = create_valid_theme(manifest)
        packager = ThemePackager(theme_dir)

        is_valid, errors, warnings = packager.validate()

        assert is_valid is False


class TestBundledComponentValidation:
    """Tests for bundled component validation."""

    def test_valid_components_pass(self, create_valid_theme):
        """Test validation passes for valid bundled components."""
        theme_dir = create_valid_theme()
        packager = ThemePackager(theme_dir)

        is_valid, errors, warnings = packager.validate()

        assert is_valid is True

    def test_missing_component_fails(self, create_valid_theme, valid_theme_manifest):
        """Test validation fails when bundled component is missing."""
        manifest = valid_theme_manifest.copy()
        # Add component that doesn't exist
        manifest["bundled_components"].append(
            {"type": "section", "name": "missing_component", "path": "components/sections/missing"}
        )

        theme_dir = create_valid_theme(manifest)
        packager = ThemePackager(theme_dir)

        is_valid, errors, warnings = packager.validate()

        assert is_valid is False
        assert any("missing_component" in err or "not found" in err for err in errors)

    def test_invalid_component_fails(self, create_valid_theme, valid_theme_manifest):
        """Test validation fails for invalid component structure."""
        theme_dir = create_valid_theme()

        # Remove component's manifest.json to make it invalid
        comp_dir = theme_dir / "components/headers/mega_menu"
        (comp_dir / "manifest.json").unlink()

        packager = ThemePackager(theme_dir)
        is_valid, errors, warnings = packager.validate()

        assert is_valid is False


class TestPageSchemaValidation:
    """Tests for page schema validation."""

    def test_valid_page_schemas_pass(self, create_valid_theme):
        """Test validation passes for valid page schemas."""
        theme_dir = create_valid_theme()
        packager = ThemePackager(theme_dir)

        is_valid, errors, warnings = packager.validate()

        assert is_valid is True

    def test_missing_page_schema_fails(self, create_valid_theme, valid_theme_manifest):
        """Test validation fails when page schema file is missing."""
        theme_dir = create_valid_theme()

        # Remove one page schema
        (theme_dir / "page_schemas/home.json").unlink()

        packager = ThemePackager(theme_dir)
        is_valid, errors, warnings = packager.validate()

        assert is_valid is False
        assert any("home" in err.lower() for err in errors)

    def test_invalid_page_schema_json_fails(self, create_valid_theme):
        """Test validation fails for invalid JSON in page schema."""
        theme_dir = create_valid_theme()

        # Write invalid JSON to page schema
        with open(theme_dir / "page_schemas/home.json", "w") as f:
            f.write("{invalid json")

        packager = ThemePackager(theme_dir)
        is_valid, errors, warnings = packager.validate()

        assert is_valid is False


class TestDesignTokensValidation:
    """Tests for design tokens validation."""

    def test_valid_design_tokens_pass(self, create_valid_theme):
        """Test validation passes for valid design tokens."""
        theme_dir = create_valid_theme()
        packager = ThemePackager(theme_dir)

        is_valid, errors, warnings = packager.validate()

        assert is_valid is True

    def test_missing_design_tokens_fails(self, create_valid_theme):
        """Test validation fails when design tokens file is missing."""
        theme_dir = create_valid_theme()

        # Remove design tokens file
        (theme_dir / "theme/tokens.json").unlink()

        packager = ThemePackager(theme_dir)
        is_valid, errors, warnings = packager.validate()

        assert is_valid is False
        assert any("tokens" in err.lower() for err in errors)

    def test_invalid_design_tokens_json_fails(self, create_valid_theme):
        """Test validation fails for invalid JSON in design tokens."""
        theme_dir = create_valid_theme()

        # Write invalid JSON
        with open(theme_dir / "theme/tokens.json", "w") as f:
            f.write("{invalid json")

        packager = ThemePackager(theme_dir)
        is_valid, errors, warnings = packager.validate()

        assert is_valid is False


class TestPreviewImageValidation:
    """Tests for preview image validation."""

    def test_valid_preview_passes(self, create_valid_theme):
        """Test validation passes for valid preview image."""
        theme_dir = create_valid_theme()
        packager = ThemePackager(theme_dir)

        is_valid, errors, warnings = packager.validate()

        assert is_valid is True

    def test_missing_preview_fails(self, create_valid_theme):
        """Test validation fails when preview image is missing."""
        theme_dir = create_valid_theme()

        # Remove preview image
        (theme_dir / "preview.png").unlink()

        packager = ThemePackager(theme_dir)
        is_valid, errors, warnings = packager.validate()

        assert is_valid is False
        assert any("preview" in err.lower() for err in errors)

    def test_oversized_preview_fails(self, create_valid_theme):
        """Test validation fails when preview image exceeds size limit."""
        theme_dir = create_valid_theme()

        # Create oversized preview (>5MB)
        with open(theme_dir / "preview.png", "wb") as f:
            f.write(b"X" * (6 * 1024 * 1024))  # 6MB

        packager = ThemePackager(theme_dir)
        is_valid, errors, warnings = packager.validate()

        assert is_valid is False
        assert any(
            "preview" in err.lower() and ("large" in err.lower() or "5mb" in err.lower())
            for err in errors
        )


class TestScreenshotsValidation:
    """Tests for screenshots validation."""

    def test_valid_screenshots_pass(self, create_valid_theme):
        """Test validation passes for valid screenshots."""
        theme_dir = create_valid_theme()
        packager = ThemePackager(theme_dir)

        is_valid, errors, warnings = packager.validate()

        assert is_valid is True

    def test_missing_screenshot_fails(self, create_valid_theme):
        """Test validation fails when screenshot is missing."""
        theme_dir = create_valid_theme()

        # Remove one screenshot
        (theme_dir / "screenshot1.png").unlink()

        packager = ThemePackager(theme_dir)
        is_valid, errors, warnings = packager.validate()

        assert is_valid is False
        assert any("screenshot1" in err.lower() for err in errors)

    def test_oversized_screenshot_warns(self, create_valid_theme):
        """Test validation warns when screenshot is oversized."""
        theme_dir = create_valid_theme()

        # Create oversized screenshot (>5MB)
        with open(theme_dir / "screenshot1.png", "wb") as f:
            f.write(b"X" * (6 * 1024 * 1024))  # 6MB

        packager = ThemePackager(theme_dir)
        is_valid, errors, warnings = packager.validate()

        # Should still be valid but with warning
        assert is_valid is True
        assert any("screenshot" in warn.lower() for warn in warnings)


class TestPackageCreation:
    """Tests for theme package creation."""

    def test_package_creation(self, create_valid_theme, tmp_path):
        """Test theme package is created successfully."""
        theme_dir = create_valid_theme()
        packager = ThemePackager(theme_dir)

        output_path = tmp_path / "test-theme-1.0.0.zip"
        package_info = packager.package(output_path)

        assert output_path.exists()
        assert package_info["theme_name"] == "test-theme"
        assert package_info["version"] == "1.0.0"
        assert package_info["bundled_components"] == 2
        assert "package_checksum" in package_info
        assert "content_checksum" in package_info

    def test_package_creates_checksum_file(self, create_valid_theme, tmp_path):
        """Test package creation also creates checksum file."""
        theme_dir = create_valid_theme()
        packager = ThemePackager(theme_dir)

        output_path = tmp_path / "test-theme-1.0.0.zip"
        packager.package(output_path)

        checksum_file = Path(str(output_path) + ".sha256")
        assert checksum_file.exists()

        # Verify checksum file format
        content = checksum_file.read_text()
        assert "test-theme-1.0.0.zip" in content
        assert len(content.split()[0]) == 64  # SHA256 hash length

    def test_package_files_at_root(self, create_valid_theme, tmp_path):
        """Test package has files at root (not in subdirectory)."""
        theme_dir = create_valid_theme()
        packager = ThemePackager(theme_dir)

        output_path = tmp_path / "test-theme-1.0.0.zip"
        packager.package(output_path)

        with zipfile.ZipFile(output_path, "r") as zf:
            namelist = zf.namelist()
            # manifest.json should be at root
            assert "manifest.json" in namelist
            # Components should be under components/ (not theme-name/components/)
            assert any("components/headers/mega_menu/manifest.json" in name for name in namelist)

    def test_package_excludes_unwanted_files(self, create_valid_theme, tmp_path):
        """Test package excludes unwanted files (.pyc, __pycache__, .DS_Store, .git)."""
        theme_dir = create_valid_theme()

        # Add unwanted files
        (theme_dir / "test.pyc").write_bytes(b"compiled")
        (theme_dir / "__pycache__").mkdir()
        (theme_dir / "__pycache__" / "cache.pyc").write_bytes(b"cache")
        (theme_dir / ".DS_Store").write_bytes(b"macos")
        (theme_dir / ".gitignore").write_text("*.log")

        packager = ThemePackager(theme_dir)
        output_path = tmp_path / "test-theme-1.0.0.zip"
        packager.package(output_path)

        with zipfile.ZipFile(output_path, "r") as zf:
            namelist = zf.namelist()
            # Verify unwanted files are NOT in package
            assert not any(".pyc" in name for name in namelist)
            assert not any("__pycache__" in name for name in namelist)
            assert not any(".DS_Store" in name for name in namelist)
            assert not any(".gitignore" in name for name in namelist)

    def test_package_updates_manifest_metadata(self, create_valid_theme, tmp_path):
        """Test package updates manifest with metadata."""
        theme_dir = create_valid_theme()
        packager = ThemePackager(theme_dir)

        output_path = tmp_path / "test-theme-1.0.0.zip"
        packager.package(output_path)

        # Read manifest from package
        with zipfile.ZipFile(output_path, "r") as zf, zf.open("manifest.json") as f:
            manifest = json.load(f)

        # Verify metadata was added
        assert "total_size_bytes" in manifest
        assert "file_count" in manifest
        assert "checksum" in manifest
        assert manifest["checksum"].startswith("sha256:")

    def test_package_without_validation_fails(self, temp_theme_dir, tmp_path):
        """Test packaging without validation fails for invalid theme."""
        # Create invalid theme (missing manifest)
        packager = ThemePackager(temp_theme_dir)

        output_path = tmp_path / "test-theme-1.0.0.zip"

        with pytest.raises(ThemePackagingError) as exc_info:
            packager.package(output_path)

        assert "validation failed" in str(exc_info.value).lower()

    def test_package_cleans_up_build_directory(self, create_valid_theme, tmp_path):
        """Test package cleans up temporary build directory."""
        theme_dir = create_valid_theme()
        packager = ThemePackager(theme_dir)

        output_path = tmp_path / "test-theme-1.0.0.zip"
        package_info = packager.package(output_path)

        # Build directory should be cleaned up
        build_dir = output_path.parent / f"build_{packager.manifest['name']}"
        assert not build_dir.exists()


class TestValidationReport:
    """Tests for validation report generation."""

    def test_validation_report_for_valid_theme(self, create_valid_theme):
        """Test validation report for valid theme."""
        theme_dir = create_valid_theme()
        packager = ThemePackager(theme_dir)
        packager.validate()

        report = packager.get_validation_report()

        assert "Test Theme" in report
        assert "test-theme" in report
        assert "1.0.0" in report
        assert "✅" in report or "passed" in report.lower()

    def test_validation_report_shows_errors(self, temp_theme_dir):
        """Test validation report shows errors."""
        packager = ThemePackager(temp_theme_dir)
        packager.validate()

        report = packager.get_validation_report()

        assert "❌" in report or "error" in report.lower()
        assert "manifest.json" in report.lower()

    def test_validation_report_shows_warnings(self, create_valid_theme):
        """Test validation report shows warnings."""
        theme_dir = create_valid_theme()

        # Create oversized screenshot to trigger warning
        with open(theme_dir / "screenshot1.png", "wb") as f:
            f.write(b"X" * (6 * 1024 * 1024))  # 6MB

        packager = ThemePackager(theme_dir)
        packager.validate()

        report = packager.get_validation_report()

        assert "⚠️" in report or "warning" in report.lower()
