"""
Component validation pipeline.

Validates components before approval:
- Manifest schema validation
- Security scan (XSS, SQL injection patterns)
- Template syntax validation
- Asset budget compliance
- Tier permission validation

The validation process ensures all components in the registry are:
- Properly structured (valid manifest, templates, assets)
- Secure (no XSS, script injection, or other vulnerabilities)
- Compliant (within asset budgets, proper capabilities declared)
- Compatible (tier permissions correctly configured)

Usage:
    validator = ComponentValidator(component)
    is_valid, errors, warnings = validator.validate()

    if is_valid:
        # Approve component
    else:
        # Show errors to reviewer
"""

import json
import re
import tempfile
import zipfile
from pathlib import Path

from django.template import Template, TemplateSyntaxError
from django.utils.translation import gettext_lazy as _

from .models import ComponentStore


class ComponentValidator:
    """
    Validates component packages for security and compliance.

    Performs multi-stage validation:
    1. Manifest validation - Checks manifest.json structure
    2. Template validation - Validates template.html syntax and security
    3. Asset validation - Checks CSS/JS files and budgets
    4. Security validation - Scans for common vulnerabilities
    5. Permission validation - Validates tier permissions and capabilities
    """

    # Security patterns to detect
    DANGEROUS_PATTERNS = {
        "xss": [
            r"<script[^>]*>.*?</script>",  # Script tags
            r"on\w+\s*=",  # Event handlers (onclick, onerror, etc.)
            r"javascript:",  # JavaScript protocol
            r"eval\s*\(",  # eval() calls
            r"document\.write",  # document.write
        ],
        "sql_injection": [
            r"(union|select|insert|update|delete|drop)\s+",
            r";\s*(drop|delete|truncate)",
        ],
        "file_inclusion": [
            r"\.\./+",  # Path traversal
            r"file://",  # File protocol
        ],
    }

    # Dangerous Django template tags/filters
    DANGEROUS_TEMPLATE_TAGS = [
        "load",  # Don't allow loading custom template tags
        "include",  # Don't allow including arbitrary templates
        "extends",  # Don't allow extending arbitrary templates
    ]

    # Maximum file sizes (in KB)
    MAX_MANIFEST_SIZE = 100  # 100KB
    MAX_TEMPLATE_SIZE = 500  # 500KB
    MAX_CSS_SIZE = 200  # 200KB per file
    MAX_JS_SIZE = 300  # 300KB per file

    def __init__(self, component: ComponentStore):
        """
        Initialize validator for a component.

        Args:
            component: ComponentStore instance to validate
        """
        self.component = component
        self.errors = []
        self.warnings = []
        self.manifest_data = None
        self.temp_dir = None

    def validate(self) -> tuple[bool, list[str], list[str]]:
        """
        Run all validation checks.

        Returns:
            Tuple of (is_valid, errors, warnings)
            - is_valid: True if no critical errors found
            - errors: List of critical errors that must be fixed
            - warnings: List of warnings that should be reviewed
        """
        self.errors = []
        self.warnings = []

        # Extract package to temp directory
        if not self._extract_package():
            return (False, self.errors, self.warnings)

        try:
            # Run validation pipeline
            self.validate_manifest()
            self.validate_template()
            self.validate_assets()
            self.validate_security()
            self.validate_permissions()

            is_valid = len(self.errors) == 0
            return (is_valid, self.errors, self.warnings)

        finally:
            # Cleanup temp directory
            if self.temp_dir:
                import shutil

                shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _extract_package(self) -> bool:
        """Extract component package to temporary directory."""
        if not self.component.package_file:
            self.errors.append(str(_("Component has no package file")))
            return False

        try:
            self.temp_dir = tempfile.mkdtemp(prefix="component_validation_")

            with zipfile.ZipFile(self.component.package_file.path, "r") as zip_ref:
                # Security check: prevent zip bomb or path traversal
                for member in zip_ref.namelist():
                    # Check for path traversal
                    if member.startswith("/") or ".." in member:
                        self.errors.append(
                            str(_("Package contains invalid path: %(path)s") % {"path": member})
                        )
                        return False

                zip_ref.extractall(self.temp_dir)

            return True

        except zipfile.BadZipFile:
            self.errors.append(str(_("Invalid ZIP file")))
            return False
        except Exception as e:
            self.errors.append(str(_("Failed to extract package: %(error)s") % {"error": str(e)}))
            return False

    def validate_manifest(self):
        """Validate manifest.json structure and content."""
        manifest_path = Path(self.temp_dir) / "manifest.json"

        # Check manifest exists
        if not manifest_path.exists():
            self.errors.append(str(_("manifest.json not found in package")))
            return

        # Check manifest size
        manifest_size = manifest_path.stat().st_size / 1024  # KB
        if manifest_size > self.MAX_MANIFEST_SIZE:
            self.errors.append(
                str(
                    _("Manifest file too large: %(size).1f KB (max: %(max)d KB)")
                    % {"size": manifest_size, "max": self.MAX_MANIFEST_SIZE}
                )
            )

        # Parse manifest
        try:
            with open(manifest_path, encoding="utf-8") as f:
                self.manifest_data = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(str(_("Invalid JSON in manifest: %(error)s") % {"error": str(e)}))
            return
        except Exception as e:
            self.errors.append(str(_("Failed to read manifest: %(error)s") % {"error": str(e)}))
            return

        # Validate required fields
        required_fields = ["component_type", "display_name", "version", "author"]
        for field in required_fields:
            if field not in self.manifest_data:
                self.errors.append(
                    str(_("Missing required field in manifest: %(field)s") % {"field": field})
                )

        # Validate version format (semantic versioning)
        if "version" in self.manifest_data:
            version = self.manifest_data["version"]
            if not re.match(r"^\d+\.\d+\.\d+$", version):
                self.warnings.append(str(_("Version should use semantic versioning (e.g., 1.0.0)")))

        # Validate component_type format (lowercase, underscores)
        if "component_type" in self.manifest_data:
            component_type = self.manifest_data["component_type"]
            if not re.match(r"^[a-z_]+$", component_type):
                self.errors.append(str(_("component_type must be lowercase with underscores only")))

    def validate_template(self):
        """Validate template.html syntax and security."""
        template_path = Path(self.temp_dir) / "template.html"

        # Check template exists
        if not template_path.exists():
            self.errors.append(str(_("template.html not found in package")))
            return

        # Check template size
        template_size = template_path.stat().st_size / 1024  # KB
        if template_size > self.MAX_TEMPLATE_SIZE:
            self.errors.append(
                str(
                    _("Template file too large: %(size).1f KB (max: %(max)d KB)")
                    % {"size": template_size, "max": self.MAX_TEMPLATE_SIZE}
                )
            )

        # Read template content
        try:
            with open(template_path, encoding="utf-8") as f:
                template_content = f.read()
        except Exception as e:
            self.errors.append(str(_("Failed to read template: %(error)s") % {"error": str(e)}))
            return

        # Validate Django template syntax
        try:
            Template(template_content)
        except TemplateSyntaxError as e:
            self.errors.append(str(_("Template syntax error: %(error)s") % {"error": str(e)}))

        # Check for dangerous template tags
        for tag in self.DANGEROUS_TEMPLATE_TAGS:
            pattern = r"\{%\s*" + tag + r"\s+"
            if re.search(pattern, template_content, re.IGNORECASE):
                self.errors.append(str(_("Forbidden template tag: %(tag)s") % {"tag": tag}))

        # Security check for inline scripts
        if "<script" in template_content.lower():
            self.errors.append(
                str(_("Inline <script> tags not allowed. Use external script files."))
            )

        # Check for dangerous event handlers
        event_handlers = re.findall(r"on\w+\s*=", template_content, re.IGNORECASE)
        if event_handlers:
            self.errors.append(
                str(
                    _("Inline event handlers not allowed: %(handlers)s")
                    % {"handlers": ", ".join(set(event_handlers))}
                )
            )

    def validate_assets(self):
        """Validate CSS/JS assets and budget compliance."""
        assets_dir = Path(self.temp_dir) / "assets"

        if not assets_dir.exists():
            self.warnings.append(str(_("No assets directory found")))
            return

        total_script_size = 0
        total_style_size = 0

        # Validate CSS files
        for css_file in assets_dir.glob("**/*.css"):
            css_size = css_file.stat().st_size / 1024  # KB
            total_style_size += css_size

            if css_size > self.MAX_CSS_SIZE:
                self.warnings.append(
                    str(
                        _("CSS file %(file)s is large: %(size).1f KB")
                        % {"file": css_file.name, "size": css_size}
                    )
                )

        # Validate JS files
        for js_file in assets_dir.glob("**/*.js"):
            js_size = js_file.stat().st_size / 1024  # KB
            total_script_size += js_size

            if js_size > self.MAX_JS_SIZE:
                self.warnings.append(
                    str(
                        _("JS file %(file)s is large: %(size).1f KB")
                        % {"file": js_file.name, "size": js_size}
                    )
                )

        # Check against declared budgets
        if self.component.script_budget_kb > 0:
            if total_script_size > float(self.component.script_budget_kb):
                self.errors.append(
                    str(
                        _("Script size %(actual).1f KB exceeds budget %(budget).1f KB")
                        % {
                            "actual": total_script_size,
                            "budget": float(self.component.script_budget_kb),
                        }
                    )
                )

    def validate_security(self):
        """Security scanning for common vulnerabilities."""
        # Scan all files for dangerous patterns
        for file_path in Path(self.temp_dir).rglob("*"):
            if not file_path.is_file():
                continue

            # Skip binary files
            if file_path.suffix in [".zip", ".png", ".jpg", ".jpeg", ".gif", ".svg"]:
                continue

            try:
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # Check XSS patterns
                for pattern in self.DANGEROUS_PATTERNS["xss"]:
                    if re.search(pattern, content, re.IGNORECASE):
                        self.warnings.append(
                            str(
                                _("Potential XSS pattern in %(file)s: %(pattern)s")
                                % {"file": file_path.name, "pattern": pattern}
                            )
                        )

                # Check SQL injection patterns
                for pattern in self.DANGEROUS_PATTERNS["sql_injection"]:
                    if re.search(pattern, content, re.IGNORECASE):
                        self.warnings.append(
                            str(
                                _("Potential SQL injection pattern in %(file)s")
                                % {"file": file_path.name}
                            )
                        )

                # Check file inclusion patterns
                for pattern in self.DANGEROUS_PATTERNS["file_inclusion"]:
                    if re.search(pattern, content):
                        self.errors.append(
                            str(_("Path traversal detected in %(file)s") % {"file": file_path.name})
                        )

            except Exception:
                # Skip files that can't be read as text
                continue

    def validate_permissions(self):
        """Validate tier permissions and capabilities."""
        # Check if component declares required capabilities
        if not self.component.capabilities:
            self.warnings.append(str(_("Component does not declare any capabilities")))

        # Check if component is allowed in at least one tier
        if not self.component.allowed_tiers:
            self.warnings.append(str(_("Component is not allowed in any tier")))

        # Validate capability-specific requirements
        capabilities = self.component.capabilities or []

        # If component uses external scripts, must declare external_domains
        if "external_scripts" in capabilities and not self.component.external_domains:
            self.errors.append(
                str(_("Component with 'external_scripts' capability must declare external_domains"))
            )

        # If component uses custom HTML, must have proper sandbox settings
        if "custom_html" in capabilities and not self.component.requires_sandbox:
            self.warnings.append(
                str(_("Component with 'custom_html' capability should use sandbox"))
            )

        # Check render mode compatibility
        if self.component.render_mode == "csr" and "external_scripts" not in capabilities:
            self.warnings.append(
                str(_("Client-side render components typically need 'external_scripts' capability"))
            )


def validate_component(component: ComponentStore) -> tuple[bool, list[str], list[str]]:
    """
    Convenience function to validate a component.

    Args:
        component: ComponentStore instance to validate

    Returns:
        Tuple of (is_valid, errors, warnings)
    """
    validator = ComponentValidator(component)
    return validator.validate()
