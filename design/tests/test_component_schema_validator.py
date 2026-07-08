"""
Tests for Component Schema Validator

Tests validation of component packages against manifest schema and directory structure.
"""

import json
import pytest
from pathlib import Path
from design.component_schema_validator import (
    ComponentSchemaValidator,
    ComponentValidationError,
)


@pytest.fixture
def temp_component_dir(tmp_path):
    """Create a temporary component directory for testing."""
    component_dir = tmp_path / "test_component"
    component_dir.mkdir()
    return component_dir


@pytest.fixture
def valid_manifest():
    """Return a valid component manifest."""
    return {
        "name": "test_banner",
        "version": "1.0.0",
        "display_name": "Test Banner",
        "description": "A test banner component for validation testing purposes only.",
        "author": "Spwig",
        "tier_compatibility": ["B", "C"],
        "regions": ["hero", "header"],
        "props_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string"
                },
                "subtitle": {
                    "type": "string"
                }
            },
            "required": ["title"]
        },
        "category": "hero",
        "license": "Proprietary"
    }


@pytest.fixture
def valid_props_schema():
    """Return a valid props JSON schema."""
    return {
        "type": "object",
        "properties": {
            "title": {
                "type": "string"
            },
            "subtitle": {
                "type": "string"
            }
        },
        "required": ["title"]
    }


@pytest.fixture
def valid_component(temp_component_dir, valid_manifest, valid_props_schema):
    """Create a valid component directory structure."""
    # Write manifest
    manifest_path = temp_component_dir / "manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(valid_manifest, f, indent=2)

    # Write template
    template_path = temp_component_dir / "template.html"
    template_path.write_text(
        "<div class='banner'><h1>{{ title }}</h1></div>",
        encoding='utf-8'
    )

    # Write schema
    schema_path = temp_component_dir / "schema.json"
    with open(schema_path, 'w', encoding='utf-8') as f:
        json.dump(valid_props_schema, f, indent=2)

    return temp_component_dir


class TestComponentSchemaValidator:
    """Test ComponentSchemaValidator class."""

    def test_validator_initialization(self):
        """Test validator initializes correctly."""
        validator = ComponentSchemaValidator()

        assert validator.manifest_schema is not None
        assert isinstance(validator.manifest_schema, dict)
        assert validator.errors == []

    def test_validator_with_custom_schema_path(self, tmp_path):
        """Test validator with custom schema path."""
        # Create custom schema file
        custom_schema_path = tmp_path / "custom_schema.json"
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object"
        }
        with open(custom_schema_path, 'w', encoding='utf-8') as f:
            json.dump(schema, f)

        validator = ComponentSchemaValidator(schema_path=custom_schema_path)
        assert validator.manifest_schema == schema

    def test_validator_invalid_schema_path(self):
        """Test validator with non-existent schema path."""
        with pytest.raises(ComponentValidationError):
            ComponentSchemaValidator(schema_path=Path("/nonexistent/schema.json"))

    def test_valid_component_passes_validation(self, valid_component):
        """Test that a valid component passes all validation."""
        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_component(valid_component)

        assert is_valid is True
        assert errors == []

    def test_missing_directory_fails(self):
        """Test that non-existent directory fails validation."""
        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_component(Path("/nonexistent/path"))

        assert is_valid is False
        assert len(errors) == 1
        assert "does not exist" in errors[0]

    def test_path_not_directory_fails(self, tmp_path):
        """Test that file path instead of directory fails."""
        file_path = tmp_path / "file.txt"
        file_path.write_text("test")

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_component(file_path)

        assert is_valid is False
        assert "not a directory" in errors[0]

    def test_missing_manifest_fails(self, temp_component_dir):
        """Test that missing manifest.json fails validation."""
        # Create template and schema but not manifest
        (temp_component_dir / "template.html").write_text("<div>Test</div>")
        (temp_component_dir / "schema.json").write_text("{}")

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_component(temp_component_dir)

        assert is_valid is False
        assert any("manifest.json" in error for error in errors)

    def test_missing_template_fails(self, temp_component_dir, valid_manifest, valid_props_schema):
        """Test that missing template.html fails validation."""
        # Create manifest and schema but not template
        (temp_component_dir / "manifest.json").write_text(json.dumps(valid_manifest))
        (temp_component_dir / "schema.json").write_text(json.dumps(valid_props_schema))

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_component(temp_component_dir)

        assert is_valid is False
        assert any("template.html" in error for error in errors)

    def test_missing_schema_fails(self, temp_component_dir, valid_manifest):
        """Test that missing schema.json fails validation."""
        # Create manifest and template but not schema
        (temp_component_dir / "manifest.json").write_text(json.dumps(valid_manifest))
        (temp_component_dir / "template.html").write_text("<div>Test</div>")

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_component(temp_component_dir)

        assert is_valid is False
        assert any("schema.json" in error for error in errors)

    def test_invalid_manifest_json_fails(self, temp_component_dir):
        """Test that invalid JSON in manifest fails validation."""
        # Create all required files but manifest has invalid JSON
        (temp_component_dir / "manifest.json").write_text("{ invalid json }")
        (temp_component_dir / "template.html").write_text("<div>Test</div>")
        (temp_component_dir / "schema.json").write_text("{}")

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_component(temp_component_dir)

        assert is_valid is False
        assert any("Invalid JSON" in error for error in errors)

    def test_empty_template_fails(self, temp_component_dir, valid_manifest, valid_props_schema):
        """Test that empty template file fails validation."""
        (temp_component_dir / "manifest.json").write_text(json.dumps(valid_manifest))
        (temp_component_dir / "template.html").write_text("")
        (temp_component_dir / "schema.json").write_text(json.dumps(valid_props_schema))

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_component(temp_component_dir)

        assert is_valid is False
        assert any("empty" in error.lower() for error in errors)

    def test_invalid_props_schema_json_fails(self, temp_component_dir, valid_manifest):
        """Test that invalid JSON in schema.json fails validation."""
        (temp_component_dir / "manifest.json").write_text(json.dumps(valid_manifest))
        (temp_component_dir / "template.html").write_text("<div>Test</div>")
        (temp_component_dir / "schema.json").write_text("{ invalid }")

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_component(temp_component_dir)

        assert is_valid is False
        assert any("not valid JSON" in error for error in errors)


class TestManifestValidation:
    """Test manifest schema validation."""

    def test_valid_manifest_passes(self, valid_manifest):
        """Test that valid manifest passes schema validation."""
        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_manifest_only(valid_manifest)

        assert is_valid is True
        assert errors == []

    def test_missing_required_field_fails(self, valid_manifest):
        """Test that missing required field fails validation."""
        del valid_manifest['name']

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_manifest_only(valid_manifest)

        assert is_valid is False

    def test_invalid_name_format_fails(self, valid_manifest):
        """Test that invalid component name format fails."""
        valid_manifest['name'] = "Invalid-Name-With-Dashes"

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_manifest_only(valid_manifest)

        assert is_valid is False

    def test_invalid_version_format_fails(self, valid_manifest):
        """Test that invalid version format fails."""
        valid_manifest['version'] = "1.0"  # Should be x.y.z

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_manifest_only(valid_manifest)

        assert is_valid is False

    def test_invalid_tier_fails(self, valid_manifest):
        """Test that invalid tier value fails."""
        valid_manifest['tier_compatibility'] = ["A", "D"]  # D is invalid

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_manifest_only(valid_manifest)

        assert is_valid is False

    def test_empty_regions_fails(self, valid_manifest):
        """Test that empty regions array fails."""
        valid_manifest['regions'] = []

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_manifest_only(valid_manifest)

        assert is_valid is False

    def test_invalid_category_fails(self, valid_manifest):
        """Test that invalid category fails."""
        valid_manifest['category'] = "invalid_category"

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_manifest_only(valid_manifest)

        assert is_valid is False

    def test_valid_assets_passes(self, valid_manifest):
        """Test that valid assets declaration passes."""
        valid_manifest['assets'] = {
            'css': ['assets/style.css'],
            'js': ['assets/script.js'],
            'images': ['assets/icon.png']
        }

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_manifest_only(valid_manifest)

        assert is_valid is True

    def test_invalid_asset_path_fails(self, valid_manifest):
        """Test that asset path not in assets/ directory fails."""
        valid_manifest['assets'] = {
            'css': ['style.css']  # Should be assets/style.css
        }

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_manifest_only(valid_manifest)

        assert is_valid is False

    def test_valid_dependencies_passes(self, valid_manifest):
        """Test that valid dependencies pass."""
        valid_manifest['dependencies'] = [
            {
                'name': 'other_component',
                'min_version': '1.0.0',
                'max_version': '2.0.0'
            }
        ]

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_manifest_only(valid_manifest)

        assert is_valid is True

    def test_invalid_dependency_version_range_fails(self, valid_manifest):
        """Test that min_version > max_version fails."""
        valid_manifest['dependencies'] = [
            {
                'name': 'other_component',
                'min_version': '2.0.0',
                'max_version': '1.0.0'
            }
        ]

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_manifest_only(valid_manifest)

        assert is_valid is False
        assert any("min_version" in error and "max_version" in error for error in errors)


class TestAssetValidation:
    """Test asset file validation."""

    def test_declared_assets_exist_passes(self, valid_component, valid_manifest):
        """Test that validation passes when declared assets exist."""
        # Add assets to manifest
        valid_manifest['assets'] = {
            'css': ['assets/style.css'],
            'js': ['assets/script.js']
        }

        # Create assets directory and files
        assets_dir = valid_component / "assets"
        assets_dir.mkdir()
        (assets_dir / "style.css").write_text(".banner { color: red; }")
        (assets_dir / "script.js").write_text("console.log('test');")

        # Update manifest file
        manifest_path = valid_component / "manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(valid_manifest, f)

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_component(valid_component)

        assert is_valid is True
        assert errors == []

    def test_missing_declared_asset_fails(self, valid_component, valid_manifest):
        """Test that validation fails when declared asset doesn't exist."""
        # Add assets to manifest but don't create files
        valid_manifest['assets'] = {
            'css': ['assets/missing.css']
        }

        # Update manifest file
        manifest_path = valid_component / "manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(valid_manifest, f)

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_component(valid_component)

        assert is_valid is False
        assert any("missing.css" in error for error in errors)


class TestLocaleValidation:
    """Test locale file validation."""

    def test_declared_locales_exist_passes(self, valid_component, valid_manifest):
        """Test that validation passes when declared locales exist."""
        # Add locales to manifest
        valid_manifest['locales'] = ['en', 'es']

        # Create locales directory and files
        locales_dir = valid_component / "locales"
        locales_dir.mkdir()
        (locales_dir / "en.json").write_text('{"title": "Title"}')
        (locales_dir / "es.json").write_text('{"title": "Título"}')

        # Update manifest file
        manifest_path = valid_component / "manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(valid_manifest, f)

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_component(valid_component)

        assert is_valid is True
        assert errors == []

    def test_missing_locale_file_fails(self, valid_component, valid_manifest):
        """Test that validation fails when declared locale file doesn't exist."""
        # Add locales to manifest but don't create files
        valid_manifest['locales'] = ['en', 'es']

        # Create locales directory but only one file
        locales_dir = valid_component / "locales"
        locales_dir.mkdir()
        (locales_dir / "en.json").write_text('{"title": "Title"}')

        # Update manifest file
        manifest_path = valid_component / "manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(valid_manifest, f)

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_component(valid_component)

        assert is_valid is False
        assert any("es.json" in error for error in errors)

    def test_invalid_locale_json_fails(self, valid_component, valid_manifest):
        """Test that invalid JSON in locale file fails."""
        valid_manifest['locales'] = ['en']

        # Create locales directory with invalid JSON
        locales_dir = valid_component / "locales"
        locales_dir.mkdir()
        (locales_dir / "en.json").write_text('{ invalid }')

        # Update manifest file
        manifest_path = valid_component / "manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(valid_manifest, f)

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_component(valid_component)

        assert is_valid is False
        assert any("not valid JSON" in error for error in errors)


class TestPreviewValidation:
    """Test preview image validation."""

    def test_declared_preview_exists_passes(self, valid_component, valid_manifest):
        """Test that validation passes when declared preview exists."""
        # Add preview to manifest
        valid_manifest['preview'] = 'preview.png'

        # Create preview file
        preview_path = valid_component / "preview.png"
        preview_path.write_bytes(b'\x89PNG\r\n\x1a\n')  # Minimal PNG header

        # Update manifest file
        manifest_path = valid_component / "manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(valid_manifest, f)

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_component(valid_component)

        assert is_valid is True
        assert errors == []

    def test_missing_declared_preview_fails(self, valid_component, valid_manifest):
        """Test that validation fails when declared preview doesn't exist."""
        # Add preview to manifest but don't create file
        valid_manifest['preview'] = 'preview.png'

        # Update manifest file
        manifest_path = valid_component / "manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(valid_manifest, f)

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_component(valid_component)

        assert is_valid is False
        assert any("preview.png" in error for error in errors)

    def test_oversized_preview_fails(self, valid_component, valid_manifest):
        """Test that oversized preview image fails validation."""
        valid_manifest['preview'] = 'preview.png'

        # Create oversized file (> 5MB)
        preview_path = valid_component / "preview.png"
        preview_path.write_bytes(b'\x00' * (6 * 1024 * 1024))  # 6 MB

        # Update manifest file
        manifest_path = valid_component / "manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(valid_manifest, f)

        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_component(valid_component)

        assert is_valid is False
        assert any("too large" in error for error in errors)


class TestVersionComparison:
    """Test semantic version comparison."""

    def test_version_comparison(self):
        """Test version comparison logic."""
        validator = ComponentSchemaValidator()

        # Test equal versions
        assert validator._compare_versions("1.0.0", "1.0.0") == 0

        # Test less than
        assert validator._compare_versions("1.0.0", "1.0.1") == -1
        assert validator._compare_versions("1.0.0", "1.1.0") == -1
        assert validator._compare_versions("1.0.0", "2.0.0") == -1

        # Test greater than
        assert validator._compare_versions("1.0.1", "1.0.0") == 1
        assert validator._compare_versions("1.1.0", "1.0.0") == 1
        assert validator._compare_versions("2.0.0", "1.0.0") == 1
