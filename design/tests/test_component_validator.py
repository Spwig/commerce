"""
Tests for ComponentValidator - Multi-stage validation pipeline.

Tests cover:
- Package extraction and security checks
- Manifest validation (structure, required fields, versioning)
- Template validation (syntax, security, dangerous tags)
- Asset validation (file sizes, budgets)
- Security validation (XSS, SQL injection, path traversal)
- Permission validation (capabilities, tier restrictions)
"""

import json
import zipfile
from io import BytesIO
from pathlib import Path

import pytest
from django.core.files.base import ContentFile

from design.component_validator import ComponentValidator, validate_component
from design.models import ComponentStore


@pytest.fixture
def create_component_package():
    """Factory to create component packages with custom content."""

    def _create_package(manifest=None, template=None, assets=None):
        """
        Create a component package ZIP file.

        Args:
            manifest: Dict for manifest.json (or None for default)
            template: String for template.html (or None for default)
            assets: Dict of {filename: content} for assets (or None for no assets)

        Returns:
            BytesIO containing ZIP file content
        """
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            # Add manifest
            manifest_data = manifest or {
                "component_type": "test_component",
                "display_name": "Test Component",
                "version": "1.0.0",
                "author": "Test Author",
                "description": "Test component package",
            }
            zf.writestr("manifest.json", json.dumps(manifest_data, indent=2))

            # Add template
            template_content = template or "<div>{{ content }}</div>"
            zf.writestr("template.html", template_content)

            # Add assets if provided
            if assets:
                for filename, content in assets.items():
                    zf.writestr(f"assets/{filename}", content)

        zip_buffer.seek(0)
        return zip_buffer

    return _create_package


@pytest.fixture
def valid_component(db, create_component_package):
    """Create a component with valid package."""
    component = ComponentStore.objects.create(
        component_type="test_component",
        display_name="Test Component",
        version="1.0.0",
        author="Test Author",
        description="Valid test component",
        review_status="pending",
        render_mode="server",
        script_budget_kb=100,
        capabilities=["basic"],
        allowed_tiers=["A", "B", "C"],
    )

    # Create valid package
    package = create_component_package()
    component.package_file.save("test_component.zip", ContentFile(package.read()), save=True)

    return component


@pytest.mark.django_db
class TestPackageExtraction:
    """Test component package extraction and security checks."""

    def test_extract_valid_package(self, valid_component):
        """Test extracting a valid component package."""
        validator = ComponentValidator(valid_component)

        success = validator._extract_package()

        assert success is True
        assert validator.temp_dir is not None
        assert Path(validator.temp_dir).exists()

    def test_extract_package_without_file(self, db):
        """Test extraction fails when component has no package file."""
        component = ComponentStore.objects.create(
            component_type="no_package",
            display_name="No Package",
            version="1.0.0",
            author="Test",
            description="Component without package",
            review_status="pending",
        )

        validator = ComponentValidator(component)
        success = validator._extract_package()

        assert success is False
        assert any("no package file" in err.lower() for err in validator.errors)

    def test_detect_path_traversal_in_zip(self, db, create_component_package):
        """Test that path traversal attempts in ZIP are detected."""
        component = ComponentStore.objects.create(
            component_type="malicious",
            display_name="Malicious Component",
            version="1.0.0",
            author="Test",
            description="Component with path traversal",
            review_status="pending",
        )

        # Create malicious ZIP with path traversal
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            zf.writestr("../../../etc/passwd", "malicious content")
            zf.writestr("manifest.json", "{}")

        zip_buffer.seek(0)
        component.package_file.save("malicious.zip", ContentFile(zip_buffer.read()), save=True)

        validator = ComponentValidator(component)
        success = validator._extract_package()

        assert success is False
        assert any("invalid path" in err.lower() for err in validator.errors)

    def test_detect_absolute_paths_in_zip(self, db):
        """Test that absolute paths in ZIP are detected."""
        component = ComponentStore.objects.create(
            component_type="malicious2",
            display_name="Malicious Component 2",
            version="1.0.0",
            author="Test",
            description="Component with absolute path",
            review_status="pending",
        )

        # Create malicious ZIP with absolute path
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            zf.writestr("/tmp/malicious", "malicious content")
            zf.writestr("manifest.json", "{}")

        zip_buffer.seek(0)
        component.package_file.save("malicious2.zip", ContentFile(zip_buffer.read()), save=True)

        validator = ComponentValidator(component)
        success = validator._extract_package()

        assert success is False
        assert any("invalid path" in err.lower() for err in validator.errors)


@pytest.mark.django_db
class TestManifestValidation:
    """Test manifest.json validation."""

    def test_validate_missing_manifest(self, db, create_component_package):
        """Test validation fails when manifest.json is missing."""
        component = ComponentStore.objects.create(
            component_type="no_manifest",
            display_name="No Manifest",
            version="1.0.0",
            author="Test",
            description="Component without manifest",
            review_status="pending",
        )

        # Create package without manifest
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            zf.writestr("template.html", "<div>Test</div>")

        zip_buffer.seek(0)
        component.package_file.save("no_manifest.zip", ContentFile(zip_buffer.read()), save=True)

        validator = ComponentValidator(component)
        is_valid, errors, warnings = validator.validate()

        assert is_valid is False
        assert any("manifest.json not found" in err.lower() for err in errors)

    def test_validate_invalid_json_manifest(self, db):
        """Test validation fails with invalid JSON in manifest."""
        component = ComponentStore.objects.create(
            component_type="invalid_json",
            display_name="Invalid JSON",
            version="1.0.0",
            author="Test",
            description="Component with invalid JSON",
            review_status="pending",
        )

        # Create package with invalid JSON
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            zf.writestr("manifest.json", "{invalid json}")
            zf.writestr("template.html", "<div>Test</div>")

        zip_buffer.seek(0)
        component.package_file.save("invalid_json.zip", ContentFile(zip_buffer.read()), save=True)

        validator = ComponentValidator(component)
        is_valid, errors, warnings = validator.validate()

        assert is_valid is False
        assert any("invalid json" in err.lower() for err in errors)

    def test_validate_missing_required_fields(self, db, create_component_package):
        """Test validation fails when required fields are missing."""
        component = ComponentStore.objects.create(
            component_type="missing_fields",
            display_name="Missing Fields",
            version="1.0.0",
            author="Test",
            description="Component with incomplete manifest",
            review_status="pending",
        )

        # Create package with incomplete manifest
        package = create_component_package(manifest={"component_type": "test"})
        component.package_file.save("missing_fields.zip", ContentFile(package.read()), save=True)

        validator = ComponentValidator(component)
        is_valid, errors, warnings = validator.validate()

        assert is_valid is False
        # Should have errors for missing display_name, version, author
        missing_field_errors = [err for err in errors if "missing required field" in err.lower()]
        assert len(missing_field_errors) >= 3

    def test_validate_semantic_versioning(self, valid_component, create_component_package):
        """Test that non-semantic versioning triggers warning."""
        package = create_component_package(
            manifest={
                "component_type": "test_component",
                "display_name": "Test",
                "version": "v1.0",  # Invalid: should be 1.0.0
                "author": "Test",
            }
        )
        valid_component.package_file.save("bad_version.zip", ContentFile(package.read()), save=True)

        validator = ComponentValidator(valid_component)
        is_valid, errors, warnings = validator.validate()

        # Should have warning about semantic versioning
        assert any("semantic versioning" in warn.lower() for warn in warnings)

    def test_validate_component_type_format(self, valid_component, create_component_package):
        """Test that invalid component_type format triggers error."""
        package = create_component_package(
            manifest={
                "component_type": "Invalid-Component",  # Invalid: should be lowercase_underscore
                "display_name": "Test",
                "version": "1.0.0",
                "author": "Test",
            }
        )
        valid_component.package_file.save("bad_type.zip", ContentFile(package.read()), save=True)

        validator = ComponentValidator(valid_component)
        is_valid, errors, warnings = validator.validate()

        assert is_valid is False
        assert any("lowercase with underscores" in err.lower() for err in errors)

    def test_validate_large_manifest(self, valid_component):
        """Test that oversized manifest triggers error."""
        # Create manifest > 100KB
        large_manifest = {
            "component_type": "test",
            "display_name": "Test",
            "version": "1.0.0",
            "author": "Test",
            "description": "X" * 120000,  # >100KB
        }

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            zf.writestr("manifest.json", json.dumps(large_manifest))
            zf.writestr("template.html", "<div>Test</div>")

        zip_buffer.seek(0)
        valid_component.package_file.save(
            "large_manifest.zip", ContentFile(zip_buffer.read()), save=True
        )

        validator = ComponentValidator(valid_component)
        is_valid, errors, warnings = validator.validate()

        assert is_valid is False
        assert any("too large" in err.lower() for err in errors)


@pytest.mark.django_db
class TestTemplateValidation:
    """Test template.html validation."""

    def test_validate_missing_template(self, db, create_component_package):
        """Test validation fails when template.html is missing."""
        component = ComponentStore.objects.create(
            component_type="no_template",
            display_name="No Template",
            version="1.0.0",
            author="Test",
            description="Component without template",
            review_status="pending",
        )

        # Create package without template
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            zf.writestr(
                "manifest.json",
                json.dumps(
                    {
                        "component_type": "test",
                        "display_name": "Test",
                        "version": "1.0.0",
                        "author": "Test",
                    }
                ),
            )

        zip_buffer.seek(0)
        component.package_file.save("no_template.zip", ContentFile(zip_buffer.read()), save=True)

        validator = ComponentValidator(component)
        is_valid, errors, warnings = validator.validate()

        assert is_valid is False
        assert any("template.html not found" in err.lower() for err in errors)

    def test_validate_template_syntax_error(self, valid_component, create_component_package):
        """Test validation fails with invalid Django template syntax."""
        package = create_component_package(template="<div>{% invalid_tag %}</div>")
        valid_component.package_file.save(
            "syntax_error.zip", ContentFile(package.read()), save=True
        )

        validator = ComponentValidator(valid_component)
        is_valid, errors, warnings = validator.validate()

        assert is_valid is False
        assert any("syntax error" in err.lower() for err in errors)

    def test_detect_dangerous_load_tag(self, valid_component, create_component_package):
        """Test that {% load %} tag is forbidden."""
        package = create_component_package(template="{% load custom_tags %}<div>Test</div>")
        valid_component.package_file.save("load_tag.zip", ContentFile(package.read()), save=True)

        validator = ComponentValidator(valid_component)
        is_valid, errors, warnings = validator.validate()

        assert is_valid is False
        assert any(
            "forbidden template tag" in err.lower() and "load" in err.lower() for err in errors
        )

    def test_detect_dangerous_include_tag(self, valid_component, create_component_package):
        """Test that {% include %} tag is forbidden."""
        package = create_component_package(template='{% include "malicious.html" %}')
        valid_component.package_file.save("include_tag.zip", ContentFile(package.read()), save=True)

        validator = ComponentValidator(valid_component)
        is_valid, errors, warnings = validator.validate()

        assert is_valid is False
        assert any(
            "forbidden template tag" in err.lower() and "include" in err.lower() for err in errors
        )

    def test_detect_inline_script_tags(self, valid_component, create_component_package):
        """Test that inline <script> tags are forbidden."""
        package = create_component_package(template='<div><script>alert("XSS")</script></div>')
        valid_component.package_file.save(
            "inline_script.zip", ContentFile(package.read()), save=True
        )

        validator = ComponentValidator(valid_component)
        is_valid, errors, warnings = validator.validate()

        assert is_valid is False
        assert any("inline <script> tags not allowed" in err.lower() for err in errors)

    def test_detect_inline_event_handlers(self, valid_component, create_component_package):
        """Test that inline event handlers are forbidden."""
        package = create_component_package(template="<div onclick=\"alert('XSS')\">Click me</div>")
        valid_component.package_file.save(
            "event_handler.zip", ContentFile(package.read()), save=True
        )

        validator = ComponentValidator(valid_component)
        is_valid, errors, warnings = validator.validate()

        assert is_valid is False
        assert any("inline event handlers not allowed" in err.lower() for err in errors)


@pytest.mark.django_db
class TestAssetValidation:
    """Test asset file validation."""

    def test_validate_no_assets_warning(self, valid_component):
        """Test that missing assets directory triggers warning."""
        validator = ComponentValidator(valid_component)
        is_valid, errors, warnings = validator.validate()

        # Valid component has no assets, should warn
        assert any("no assets directory" in warn.lower() for warn in warnings)

    def test_validate_css_file_size(self, valid_component, create_component_package):
        """Test that oversized CSS files trigger warning."""
        # Create CSS file > 200KB
        # Each line is ~20 bytes, so 12000 lines = ~240KB
        large_css = "body { color: red; }\n" * 12000

        package = create_component_package(assets={"style.css": large_css})
        valid_component.package_file.save("large_css.zip", ContentFile(package.read()), save=True)

        validator = ComponentValidator(valid_component)
        is_valid, errors, warnings = validator.validate()

        # Should have warning about large CSS
        assert any("css file" in warn.lower() and "large" in warn.lower() for warn in warnings)

    def test_validate_js_file_size(self, valid_component, create_component_package):
        """Test that oversized JS files trigger warning."""
        # Create JS file > 300KB
        large_js = 'console.log("test");' * 20000

        package = create_component_package(assets={"script.js": large_js})
        valid_component.package_file.save("large_js.zip", ContentFile(package.read()), save=True)

        validator = ComponentValidator(valid_component)
        is_valid, errors, warnings = validator.validate()

        # Should have warning about large JS
        assert any("js file" in warn.lower() and "large" in warn.lower() for warn in warnings)

    def test_validate_script_budget_exceeded(self, valid_component, create_component_package):
        """Test that exceeding script budget triggers error."""
        # Set low budget
        valid_component.script_budget_kb = 10
        valid_component.save()

        # Create JS that exceeds budget
        large_js = 'console.log("test");' * 1000  # ~20KB

        package = create_component_package(assets={"script.js": large_js})
        valid_component.package_file.save(
            "budget_exceed.zip", ContentFile(package.read()), save=True
        )

        validator = ComponentValidator(valid_component)
        is_valid, errors, warnings = validator.validate()

        assert is_valid is False
        assert any("exceeds budget" in err.lower() for err in errors)


@pytest.mark.django_db
class TestSecurityValidation:
    """Test security scanning for vulnerabilities."""

    def test_detect_xss_patterns_in_assets(self, valid_component, create_component_package):
        """Test detection of XSS patterns in asset files."""
        malicious_js = "document.write(userInput);"

        package = create_component_package(assets={"malicious.js": malicious_js})
        valid_component.package_file.save("xss.zip", ContentFile(package.read()), save=True)

        validator = ComponentValidator(valid_component)
        is_valid, errors, warnings = validator.validate()

        # Should have warning about potential XSS
        assert any("xss" in warn.lower() for warn in warnings)

    def test_detect_eval_calls(self, valid_component, create_component_package):
        """Test detection of eval() calls."""
        malicious_js = "eval(userCode);"

        package = create_component_package(assets={"eval.js": malicious_js})
        valid_component.package_file.save("eval.zip", ContentFile(package.read()), save=True)

        validator = ComponentValidator(valid_component)
        is_valid, errors, warnings = validator.validate()

        # Should have warning about eval
        assert any("xss" in warn.lower() or "eval" in warn.lower() for warn in warnings)

    def test_detect_path_traversal_in_files(self, valid_component, create_component_package):
        """Test detection of path traversal patterns in files."""
        malicious_js = 'fetch("../../../etc/passwd");'

        package = create_component_package(assets={"traversal.js": malicious_js})
        valid_component.package_file.save("traversal.zip", ContentFile(package.read()), save=True)

        validator = ComponentValidator(valid_component)
        is_valid, errors, warnings = validator.validate()

        # Should have error about path traversal
        assert is_valid is False
        assert any("path traversal" in err.lower() for err in errors)


@pytest.mark.django_db
class TestPermissionValidation:
    """Test permission and capability validation."""

    def test_warn_no_capabilities(self, db, create_component_package):
        """Test warning when component declares no capabilities."""
        component = ComponentStore.objects.create(
            component_type="no_caps",
            display_name="No Capabilities",
            version="1.0.0",
            author="Test",
            description="Component without capabilities",
            review_status="pending",
            capabilities=[],
        )

        package = create_component_package()
        component.package_file.save("no_caps.zip", ContentFile(package.read()), save=True)

        validator = ComponentValidator(component)
        is_valid, errors, warnings = validator.validate()

        assert any("does not declare any capabilities" in warn.lower() for warn in warnings)

    def test_warn_no_allowed_tiers(self, db, create_component_package):
        """Test warning when component is not allowed in any tier."""
        component = ComponentStore.objects.create(
            component_type="no_tiers",
            display_name="No Tiers",
            version="1.0.0",
            author="Test",
            description="Component without tier permissions",
            review_status="pending",
            allowed_tiers=[],
        )

        package = create_component_package()
        component.package_file.save("no_tiers.zip", ContentFile(package.read()), save=True)

        validator = ComponentValidator(component)
        is_valid, errors, warnings = validator.validate()

        assert any("not allowed in any tier" in warn.lower() for warn in warnings)

    def test_external_scripts_requires_domains(self, db, create_component_package):
        """Test that external_scripts capability requires external_domains."""
        component = ComponentStore.objects.create(
            component_type="external_scripts",
            display_name="External Scripts",
            version="1.0.0",
            author="Test",
            description="Component with external scripts",
            review_status="pending",
            capabilities=["external_scripts"],
            external_domains=[],  # Missing required domains
        )

        package = create_component_package()
        component.package_file.save("external.zip", ContentFile(package.read()), save=True)

        validator = ComponentValidator(component)
        is_valid, errors, warnings = validator.validate()

        assert is_valid is False
        assert any(
            "external_scripts" in err.lower() and "external_domains" in err.lower()
            for err in errors
        )

    def test_custom_html_should_use_sandbox(self, db, create_component_package):
        """Test warning for custom_html without sandbox."""
        component = ComponentStore.objects.create(
            component_type="custom_html",
            display_name="Custom HTML",
            version="1.0.0",
            author="Test",
            description="Component with custom HTML",
            review_status="pending",
            capabilities=["custom_html"],
            requires_sandbox=False,  # Should use sandbox
        )

        package = create_component_package()
        component.package_file.save("custom.zip", ContentFile(package.read()), save=True)

        validator = ComponentValidator(component)
        is_valid, errors, warnings = validator.validate()

        assert any("custom_html" in warn.lower() and "sandbox" in warn.lower() for warn in warnings)


@pytest.mark.django_db
class TestConvenienceFunction:
    """Test convenience function for validation."""

    def test_validate_component_function(self, valid_component):
        """Test validate_component() convenience function."""
        is_valid, errors, warnings = validate_component(valid_component)

        # Valid component should pass
        assert (
            is_valid is True or len(errors) == 0 or all("warning" in str(e).lower() for e in errors)
        )
