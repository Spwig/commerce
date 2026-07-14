"""
Tests for ComponentPackager - Component packaging utilities.

Tests cover:
- Directory structure validation
- Manifest validation and generation
- ZIP package creation
- Package statistics calculation
- File exclusion patterns
"""

import json
import zipfile
from pathlib import Path

import pytest

from design.component_packager import ComponentPackager, package_component


@pytest.fixture
def temp_component_dir(tmp_path):
    """Create a temporary component directory with valid structure."""
    component_dir = tmp_path / "test_component"
    component_dir.mkdir()

    # Create manifest
    manifest = {
        "component_type": "test_component",
        "display_name": "Test Component",
        "version": "1.0.0",
        "author": "Test Author",
        "description": "Test component for packaging",
    }
    (component_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))

    # Create template
    (component_dir / "template.html").write_text("<div>{{ content }}</div>")

    # Create assets directory
    assets_dir = component_dir / "assets"
    assets_dir.mkdir()
    (assets_dir / "style.css").write_text("body { color: red; }")
    (assets_dir / "script.js").write_text('console.log("test");')

    return component_dir


@pytest.fixture
def minimal_component_dir(tmp_path):
    """Create minimal component directory (only required files)."""
    component_dir = tmp_path / "minimal_component"
    component_dir.mkdir()

    manifest = {
        "component_type": "minimal",
        "display_name": "Minimal",
        "version": "1.0.0",
        "author": "Test",
    }
    (component_dir / "manifest.json").write_text(json.dumps(manifest))
    (component_dir / "template.html").write_text("<div>Minimal</div>")

    return component_dir


class TestComponentPackagerInitialization:
    """Test ComponentPackager initialization."""

    def test_init_with_path_object(self, temp_component_dir):
        """Test initialization with Path object."""
        packager = ComponentPackager(temp_component_dir)

        assert packager.component_dir == temp_component_dir
        assert packager.manifest == {}
        assert packager.errors == []
        assert packager.warnings == []

    def test_init_with_string_path(self, temp_component_dir):
        """Test initialization with string path."""
        packager = ComponentPackager(str(temp_component_dir))

        assert packager.component_dir == temp_component_dir
        assert isinstance(packager.component_dir, Path)


class TestStructureValidation:
    """Test component directory structure validation."""

    def test_validate_valid_structure(self, temp_component_dir):
        """Test validation of valid component structure."""
        packager = ComponentPackager(temp_component_dir)

        is_valid, errors, warnings = packager.validate_structure()

        assert is_valid is True
        assert len(errors) == 0

    def test_validate_nonexistent_directory(self, tmp_path):
        """Test validation fails for nonexistent directory."""
        nonexistent_dir = tmp_path / "nonexistent"
        packager = ComponentPackager(nonexistent_dir)

        is_valid, errors, warnings = packager.validate_structure()

        assert is_valid is False
        assert any("does not exist" in err.lower() for err in errors)

    def test_validate_file_instead_of_directory(self, tmp_path):
        """Test validation fails when path is a file, not directory."""
        file_path = tmp_path / "file.txt"
        file_path.write_text("not a directory")

        packager = ComponentPackager(file_path)
        is_valid, errors, warnings = packager.validate_structure()

        assert is_valid is False
        assert any("not a directory" in err.lower() for err in errors)

    def test_validate_missing_manifest(self, tmp_path):
        """Test validation fails when manifest.json is missing."""
        component_dir = tmp_path / "no_manifest"
        component_dir.mkdir()
        (component_dir / "template.html").write_text("<div>Test</div>")

        packager = ComponentPackager(component_dir)
        is_valid, errors, warnings = packager.validate_structure()

        assert is_valid is False
        assert any("manifest.json" in err for err in errors)

    def test_validate_missing_template(self, tmp_path):
        """Test validation fails when template.html is missing."""
        component_dir = tmp_path / "no_template"
        component_dir.mkdir()

        manifest = {
            "component_type": "test",
            "display_name": "Test",
            "version": "1.0.0",
            "author": "Test",
        }
        (component_dir / "manifest.json").write_text(json.dumps(manifest))

        packager = ComponentPackager(component_dir)
        is_valid, errors, warnings = packager.validate_structure()

        assert is_valid is False
        assert any("template.html" in err for err in errors)

    def test_validate_invalid_json_in_manifest(self, tmp_path):
        """Test validation fails with invalid JSON in manifest."""
        component_dir = tmp_path / "invalid_json"
        component_dir.mkdir()

        (component_dir / "manifest.json").write_text("{invalid json}")
        (component_dir / "template.html").write_text("<div>Test</div>")

        packager = ComponentPackager(component_dir)
        is_valid, errors, warnings = packager.validate_structure()

        assert is_valid is False
        assert any("invalid json" in err.lower() for err in errors)

    def test_validate_missing_required_manifest_fields(self, tmp_path):
        """Test validation fails when manifest is missing required fields."""
        component_dir = tmp_path / "incomplete_manifest"
        component_dir.mkdir()

        # Missing version and author
        manifest = {"component_type": "test", "display_name": "Test"}
        (component_dir / "manifest.json").write_text(json.dumps(manifest))
        (component_dir / "template.html").write_text("<div>Test</div>")

        packager = ComponentPackager(component_dir)
        is_valid, errors, warnings = packager.validate_structure()

        assert is_valid is False
        # Should have errors for missing version and author
        field_errors = [err for err in errors if "missing required field" in err.lower()]
        assert len(field_errors) >= 2

    def test_warn_missing_assets_directory(self, minimal_component_dir):
        """Test warning when assets directory is missing."""
        packager = ComponentPackager(minimal_component_dir)

        is_valid, errors, warnings = packager.validate_structure()

        assert is_valid is True
        assert any("no assets directory" in warn.lower() for warn in warnings)

    def test_warn_missing_locales_directory(self, minimal_component_dir):
        """Test warning when locales directory is missing."""
        packager = ComponentPackager(minimal_component_dir)

        is_valid, errors, warnings = packager.validate_structure()

        assert is_valid is True
        assert any("no locales directory" in warn.lower() for warn in warnings)

    def test_warn_invalid_version_format(self, tmp_path):
        """Test warning for non-semantic versioning."""
        component_dir = tmp_path / "bad_version"
        component_dir.mkdir()

        manifest = {
            "component_type": "test",
            "display_name": "Test",
            "version": "v1.0",  # Invalid: should be 1.0.0
            "author": "Test",
        }
        (component_dir / "manifest.json").write_text(json.dumps(manifest))
        (component_dir / "template.html").write_text("<div>Test</div>")

        packager = ComponentPackager(component_dir)
        is_valid, errors, warnings = packager.validate_structure()

        assert any("semantic versioning" in warn.lower() for warn in warnings)


class TestManifestGeneration:
    """Test manifest generation."""

    def test_generate_manifest_with_required_fields(self):
        """Test generating manifest with only required fields."""
        packager = ComponentPackager(Path("/tmp"))

        manifest = packager.generate_manifest(
            component_type="test_component",
            display_name="Test Component",
            version="1.0.0",
            author="Test Author",
        )

        assert manifest["component_type"] == "test_component"
        assert manifest["display_name"] == "Test Component"
        assert manifest["version"] == "1.0.0"
        assert manifest["author"] == "Test Author"
        assert "created_at" in manifest

    def test_generate_manifest_with_optional_fields(self):
        """Test generating manifest with optional fields."""
        packager = ComponentPackager(Path("/tmp"))

        manifest = packager.generate_manifest(
            component_type="test",
            display_name="Test",
            version="1.0.0",
            author="Test",
            description="Test description",
            capabilities=["basic", "external_scripts"],
            allowed_tiers=["A", "B"],
            render_mode="csr",
            external_domains=["example.com"],
            script_budget_kb=100,
            requires_sandbox=True,
        )

        assert manifest["description"] == "Test description"
        assert manifest["capabilities"] == ["basic", "external_scripts"]
        assert manifest["allowed_tiers"] == ["A", "B"]
        assert manifest["render_mode"] == "csr"
        assert manifest["external_domains"] == ["example.com"]
        assert manifest["script_budget_kb"] == 100
        assert manifest["requires_sandbox"] is True

    def test_generate_manifest_missing_required_field(self):
        """Test that generate_manifest raises error when required field is missing."""
        packager = ComponentPackager(Path("/tmp"))

        with pytest.raises(ValueError, match="Missing required field"):
            packager.generate_manifest(
                component_type="test",
                display_name="Test",
                version="1.0.0",
                # Missing author
            )

    def test_generate_manifest_sets_defaults(self):
        """Test that generate_manifest sets default values for optional fields."""
        packager = ComponentPackager(Path("/tmp"))

        manifest = packager.generate_manifest(
            component_type="test",
            display_name="Test",
            version="1.0.0",
            author="Test",
        )

        # Check defaults
        assert manifest["description"] == ""
        assert manifest["capabilities"] == []
        assert manifest["allowed_tiers"] == ["A", "B", "C"]
        assert manifest["render_mode"] == "ssr"
        assert manifest["external_domains"] == []
        assert manifest["script_budget_kb"] == 0
        assert manifest["requires_sandbox"] is False


class TestPackageCreation:
    """Test ZIP package creation."""

    def test_package_creates_zip_file(self, temp_component_dir, tmp_path):
        """Test that package() creates a ZIP file."""
        output_dir = tmp_path / "output"
        packager = ComponentPackager(temp_component_dir)

        package_path = packager.package(output_dir=output_dir)

        assert package_path.exists()
        assert package_path.suffix == ".zip"
        assert zipfile.is_zipfile(package_path)

    def test_package_filename_format(self, temp_component_dir, tmp_path):
        """Test that package filename uses component_type-version.zip format."""
        output_dir = tmp_path / "output"
        packager = ComponentPackager(temp_component_dir)

        package_path = packager.package(output_dir=output_dir)

        assert package_path.name == "test_component-1.0.0.zip"

    def test_package_contains_required_files(self, temp_component_dir, tmp_path):
        """Test that package contains manifest and template."""
        output_dir = tmp_path / "output"
        packager = ComponentPackager(temp_component_dir)

        package_path = packager.package(output_dir=output_dir)

        with zipfile.ZipFile(package_path, "r") as zf:
            file_list = zf.namelist()
            assert "manifest.json" in file_list
            assert "template.html" in file_list

    def test_package_contains_assets(self, temp_component_dir, tmp_path):
        """Test that package includes assets directory."""
        output_dir = tmp_path / "output"
        packager = ComponentPackager(temp_component_dir)

        package_path = packager.package(output_dir=output_dir)

        with zipfile.ZipFile(package_path, "r") as zf:
            file_list = zf.namelist()
            assert "assets/style.css" in file_list
            assert "assets/script.js" in file_list

    def test_package_excludes_patterns(self, tmp_path):
        """Test that package excludes files matching EXCLUDE_PATTERNS."""
        component_dir = tmp_path / "component_with_excludes"
        component_dir.mkdir()

        # Create valid component
        manifest = {
            "component_type": "test",
            "display_name": "Test",
            "version": "1.0.0",
            "author": "Test",
        }
        (component_dir / "manifest.json").write_text(json.dumps(manifest))
        (component_dir / "template.html").write_text("<div>Test</div>")

        # Create files that should be excluded
        (component_dir / "test.pyc").write_text("compiled python")
        (component_dir / ".DS_Store").write_text("mac metadata")
        (component_dir / "temp.tmp").write_text("temporary file")

        output_dir = tmp_path / "output"
        packager = ComponentPackager(component_dir)
        package_path = packager.package(output_dir=output_dir)

        with zipfile.ZipFile(package_path, "r") as zf:
            file_list = zf.namelist()
            # Excluded files should not be in package
            assert "test.pyc" not in file_list
            assert ".DS_Store" not in file_list
            assert "temp.tmp" not in file_list

    def test_package_fails_with_invalid_structure(self, tmp_path):
        """Test that package() raises error with invalid structure."""
        component_dir = tmp_path / "invalid"
        component_dir.mkdir()
        # Missing required files

        packager = ComponentPackager(component_dir)

        with pytest.raises(ValueError, match="validation failed"):
            packager.package()

    def test_package_default_output_dir(self, temp_component_dir):
        """Test that package() uses parent directory as default output."""
        packager = ComponentPackager(temp_component_dir)

        package_path = packager.package()

        # Should be in parent directory of component_dir
        assert package_path.parent == temp_component_dir.parent


class TestPackageStatistics:
    """Test package statistics calculation."""

    def test_calculate_basic_stats(self, temp_component_dir):
        """Test calculating package statistics."""
        packager = ComponentPackager(temp_component_dir)

        stats = packager.calculate_package_stats()

        assert stats["total_files"] >= 4  # manifest, template, 2 assets
        assert stats["total_size"] > 0
        assert stats["template_size"] > 0
        assert stats["manifest_size"] > 0
        assert stats["asset_count"] == 2
        assert stats["asset_size"] > 0

    def test_stats_include_kb_conversions(self, temp_component_dir):
        """Test that statistics include KB conversions."""
        packager = ComponentPackager(temp_component_dir)

        stats = packager.calculate_package_stats()

        assert "total_size_kb" in stats
        assert "asset_size_kb" in stats
        assert "template_size_kb" in stats
        assert "manifest_size_kb" in stats

        # KB values should be size divided by 1024
        assert stats["total_size_kb"] == stats["total_size"] / 1024

    def test_stats_for_minimal_component(self, minimal_component_dir):
        """Test statistics for minimal component (no assets)."""
        packager = ComponentPackager(minimal_component_dir)

        stats = packager.calculate_package_stats()

        assert stats["total_files"] == 2  # Only manifest and template
        assert stats["asset_count"] == 0
        assert stats["asset_size"] == 0


class TestConvenienceFunction:
    """Test package_component convenience function."""

    def test_package_component_success(self, temp_component_dir, tmp_path):
        """Test package_component() convenience function success case."""
        output_dir = tmp_path / "output"

        success, package_path, messages = package_component(
            str(temp_component_dir), output_dir=str(output_dir)
        )

        assert success is True
        assert package_path is not None
        assert package_path.exists()

    def test_package_component_failure(self, tmp_path):
        """Test package_component() convenience function failure case."""
        invalid_dir = tmp_path / "invalid"
        invalid_dir.mkdir()

        success, package_path, errors = package_component(str(invalid_dir))

        assert success is False
        assert package_path is None
        assert len(errors) > 0

    def test_package_component_returns_warnings(self, minimal_component_dir, tmp_path):
        """Test that package_component() returns warnings."""
        output_dir = tmp_path / "output"

        success, package_path, messages = package_component(
            str(minimal_component_dir), output_dir=str(output_dir)
        )

        assert success is True
        # Should have warnings about missing assets and locales
        assert len(messages) > 0
