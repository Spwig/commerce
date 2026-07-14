"""
Theme Packager

Packages themes with bundled components into distributable ZIP files.
Follows the same pattern as existing provider packaging (exchange_rates, shipping, etc.)
"""

import hashlib
import json
import logging
import shutil
import zipfile
from pathlib import Path
from typing import Any

try:
    import jsonschema
    from jsonschema import SchemaError, ValidationError, validate
except ImportError:
    jsonschema = None
    validate = None
    ValidationError = None
    SchemaError = None

from design.component_schema_validator import ComponentSchemaValidator

logger = logging.getLogger(__name__)


class ThemePackagingError(Exception):
    """Raised when theme packaging fails."""

    pass


class ThemePackager:
    """
    Packages theme directories with bundled components into ZIP files.

    Usage:
        packager = ThemePackager(theme_dir='/path/to/theme/')
        packager.validate()
        package_info = packager.package(output_path='/tmp/theme.zip')
    """

    REQUIRED_FILES = [
        "manifest.json",
    ]

    def __init__(self, theme_dir: Path):
        """
        Initialize theme packager.

        Args:
            theme_dir: Path to theme directory containing manifest.json
        """
        self.theme_dir = Path(theme_dir)
        self.manifest = None
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.component_validator = ComponentSchemaValidator()

        # Load theme manifest schema
        schema_path = Path(__file__).parent / "theme_manifest_schema.json"
        with open(schema_path, encoding="utf-8") as f:
            self.theme_schema = json.load(f)

    def validate(self) -> tuple[bool, list[str], list[str]]:
        """
        Validate complete theme package.

        Returns:
            Tuple of (is_valid, error_list, warning_list)
        """
        self.errors = []
        self.warnings = []

        # 1. Check directory exists
        if not self.theme_dir.exists():
            self.errors.append(f"Theme directory does not exist: {self.theme_dir}")
            return False, self.errors, self.warnings

        if not self.theme_dir.is_dir():
            self.errors.append(f"Path is not a directory: {self.theme_dir}")
            return False, self.errors, self.warnings

        # 2. Check required files
        manifest_path = self.theme_dir / "manifest.json"
        if not manifest_path.exists():
            self.errors.append("Required file missing: manifest.json")
            return False, self.errors, self.warnings

        # 3. Load and validate manifest
        try:
            self.manifest = self._load_manifest(manifest_path)
        except Exception as e:
            self.errors.append(f"Failed to load manifest: {e}")
            return False, self.errors, self.warnings

        if not self._validate_manifest_schema():
            return False, self.errors, self.warnings

        # 4. Validate bundled components (if any)
        if "bundled_components" in self.manifest:
            if not self._validate_bundled_components():
                return False, self.errors, self.warnings

        # 5. Validate page schemas (if declared)
        if "page_schemas" in self.manifest and not self._validate_page_schemas():
            return False, self.errors, self.warnings

        # 6. Validate design tokens (if declared)
        if "design_tokens" in self.manifest and not self._validate_design_tokens():
            return False, self.errors, self.warnings

        # 7. Validate preview image (if declared)
        if "preview_image" in self.manifest and not self._validate_preview_image():
            return False, self.errors, self.warnings

        # 8. Validate screenshots (if declared)
        if "screenshots" in self.manifest and not self._validate_screenshots():
            return False, self.errors, self.warnings

        return len(self.errors) == 0, self.errors, self.warnings

    def package(self, output_path: Path) -> dict[str, Any]:
        """
        Create ZIP package from theme directory.

        Args:
            output_path: Path for output ZIP file

        Returns:
            Package metadata dictionary

        Raises:
            ThemePackagingError: If packaging fails
        """
        output_path = Path(output_path)

        # Ensure theme is validated first
        if self.manifest is None:
            is_valid, errors, warnings = self.validate()
            if not is_valid:
                raise ThemePackagingError(f"Theme validation failed: {'; '.join(errors)}")

        # Create temporary build directory
        build_dir = output_path.parent / f"build_{self.manifest['name']}"
        if build_dir.exists():
            shutil.rmtree(build_dir)
        build_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Copy theme directory to build directory
            self._copy_to_build_dir(build_dir)

            # Clean build directory
            self._clean_build_dir(build_dir)

            # Calculate package metadata
            metadata = self._calculate_metadata(build_dir)

            # Update manifest with metadata
            self._update_manifest_with_metadata(build_dir, metadata)

            # Create ZIP package
            self._create_zip(build_dir, output_path)

            # Calculate package checksum
            package_checksum = self._calculate_file_checksum(output_path)

            # Create checksum file
            checksum_path = Path(str(output_path) + ".sha256")
            with open(checksum_path, "w") as f:
                f.write(f"{package_checksum}  {output_path.name}\n")

            # Return package info
            package_info = {
                "theme_name": self.manifest["name"],
                "version": self.manifest["version"],
                "package_file": str(output_path),
                "checksum_file": str(checksum_path),
                "package_size": output_path.stat().st_size,
                "package_checksum": package_checksum,
                "content_checksum": metadata["checksum"],
                "file_count": metadata["file_count"],
                "total_size": metadata["total_size"],
                "bundled_components": len(self.manifest.get("bundled_components", [])),
            }

            logger.info(
                f"Theme package created: {self.manifest['name']} v{self.manifest['version']}"
            )

            return package_info

        finally:
            # Cleanup build directory
            if build_dir.exists():
                shutil.rmtree(build_dir)

    def _load_manifest(self, manifest_path: Path) -> dict[str, Any]:
        """Load and parse manifest.json."""
        try:
            with open(manifest_path, encoding="utf-8") as f:
                manifest = json.load(f)
            return manifest

        except json.JSONDecodeError as e:
            raise ThemePackagingError(f"Invalid JSON in manifest: {e}")

    def _validate_manifest_schema(self) -> bool:
        """Validate manifest against JSON schema."""
        if jsonschema is None:
            logger.warning("jsonschema library not installed - skipping manifest schema validation")
            return True

        try:
            validate(instance=self.manifest, schema=self.theme_schema)
            return True

        except ValidationError as e:
            self.errors.append(f"Manifest schema validation failed: {e.message}")
            return False

        except SchemaError as e:
            self.errors.append(f"Invalid theme manifest schema: {e.message}")
            return False

    def _validate_bundled_components(self) -> bool:
        """Validate all bundled components."""
        all_valid = True

        for component_ref in self.manifest["bundled_components"]:
            component_path = self.theme_dir / component_ref["path"]

            if not component_path.exists():
                self.errors.append(f"Bundled component not found: {component_ref['path']}")
                all_valid = False
                continue

            # Validate component using ComponentSchemaValidator
            is_valid, errors = self.component_validator.validate_component(component_path)

            if not is_valid:
                self.errors.append(f"Component validation failed for {component_ref['name']}:")
                self.errors.extend([f"  - {err}" for err in errors])
                all_valid = False

        return all_valid

    def _validate_page_schemas(self) -> bool:
        """Validate page schema files exist."""
        all_valid = True

        for page_type, schema_path in self.manifest["page_schemas"].items():
            full_path = self.theme_dir / schema_path

            if not full_path.exists():
                self.errors.append(f"Page schema not found: {schema_path} (for {page_type})")
                all_valid = False
                continue

            # Validate it's valid JSON
            try:
                with open(full_path, encoding="utf-8") as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                self.errors.append(f"Invalid JSON in page schema {schema_path}: {e}")
                all_valid = False

        return all_valid

    def _validate_design_tokens(self) -> bool:
        """Validate design tokens file exists and is valid JSON."""
        tokens_path = self.theme_dir / self.manifest["design_tokens"]

        if not tokens_path.exists():
            self.errors.append(f"Design tokens file not found: {self.manifest['design_tokens']}")
            return False

        # Validate it's valid JSON
        try:
            with open(tokens_path, encoding="utf-8") as f:
                json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in design tokens: {e}")
            return False

        return True

    def _validate_preview_image(self) -> bool:
        """Validate preview image exists."""
        preview_path = self.theme_dir / self.manifest["preview_image"]

        if not preview_path.exists():
            self.errors.append(f"Preview image not found: {self.manifest['preview_image']}")
            return False

        # Check file size (max 5MB like component previews)
        max_size = 5 * 1024 * 1024  # 5 MB
        if preview_path.stat().st_size > max_size:
            self.errors.append(
                f"Preview image too large (max 5MB): {self.manifest['preview_image']}"
            )
            return False

        return True

    def _validate_screenshots(self) -> bool:
        """Validate screenshot files exist."""
        all_valid = True

        for screenshot in self.manifest["screenshots"]:
            # Support both string format and dict format {"file": "...", "title": "..."}
            screenshot_file = screenshot["file"] if isinstance(screenshot, dict) else screenshot
            screenshot_path = self.theme_dir / screenshot_file

            if not screenshot_path.exists():
                self.errors.append(f"Screenshot not found: {screenshot_file}")
                all_valid = False
                continue

            # Check file size (max 5MB each)
            max_size = 5 * 1024 * 1024  # 5 MB
            if screenshot_path.stat().st_size > max_size:
                self.warnings.append(f"Screenshot is large (>5MB): {screenshot_file}")

        return all_valid

    def _copy_to_build_dir(self, build_dir: Path):
        """Copy theme directory to build directory."""
        # Copy all files and directories
        shutil.copytree(
            self.theme_dir,
            build_dir,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns(
                "__pycache__",
                "*.pyc",
                ".DS_Store",
                ".git",
                ".gitignore",
                "node_modules",
                ".env",
                "*.log",
            ),
        )

    def _clean_build_dir(self, build_dir: Path):
        """Clean build directory of unwanted files."""
        # Remove Python cache files
        for pyc_file in build_dir.rglob("*.pyc"):
            pyc_file.unlink()

        for pycache_dir in build_dir.rglob("__pycache__"):
            shutil.rmtree(pycache_dir)

        # Remove .DS_Store files (macOS)
        for ds_file in build_dir.rglob(".DS_Store"):
            ds_file.unlink()

    def _calculate_metadata(self, build_dir: Path) -> dict[str, Any]:
        """Calculate package metadata (file count, size, checksum)."""
        file_count = 0
        total_size = 0
        file_hashes = []

        # Collect all files (excluding manifest.json for checksum calculation)
        for file_path in sorted(build_dir.rglob("*")):
            if file_path.is_file():
                file_count += 1
                total_size += file_path.stat().st_size

                # Don't include manifest.json in checksum (will be updated)
                if file_path.name != "manifest.json":
                    file_hash = self._calculate_file_checksum(file_path)
                    file_hashes.append(file_hash)

        # Calculate overall checksum from sorted file hashes
        combined_hash = hashlib.sha256()
        for file_hash in sorted(file_hashes):
            combined_hash.update(file_hash.encode("utf-8"))

        checksum = combined_hash.hexdigest()

        return {
            "file_count": file_count,
            "total_size": total_size,
            "checksum": f"sha256:{checksum}",
        }

    def _calculate_file_checksum(self, file_path: Path) -> str:
        """Calculate SHA256 checksum of a file."""
        sha256_hash = hashlib.sha256()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)

        return sha256_hash.hexdigest()

    def _update_manifest_with_metadata(self, build_dir: Path, metadata: dict[str, Any]):
        """Update manifest.json with package metadata."""
        manifest_path = build_dir / "manifest.json"

        with open(manifest_path, encoding="utf-8") as f:
            manifest = json.load(f)

        # Add metadata
        manifest["total_size_bytes"] = metadata["total_size"]
        manifest["file_count"] = metadata["file_count"]
        manifest["checksum"] = metadata["checksum"]

        # Write updated manifest
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

    def _create_zip(self, build_dir: Path, output_path: Path):
        """Create ZIP package with files at root (not in subdirectory)."""
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in build_dir.rglob("*"):
                if file_path.is_file():
                    # Archive path is relative to build_dir (files at root)
                    archive_path = file_path.relative_to(build_dir)
                    zf.write(file_path, archive_path)

        logger.info(f"Created ZIP package: {output_path}")

    def get_validation_report(self) -> str:
        """
        Generate human-readable validation report.

        Returns:
            Formatted validation report string
        """
        report = []

        if self.manifest:
            report.append(f"Theme: {self.manifest.get('display_name', 'Unknown')}")
            report.append(f"Name: {self.manifest.get('name', 'Unknown')}")
            report.append(f"Version: {self.manifest.get('version', 'Unknown')}")
            report.append("")

        if self.errors:
            report.append(f"❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                report.append(f"  - {error}")
            report.append("")

        if self.warnings:
            report.append(f"⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                report.append(f"  - {warning}")
            report.append("")

        if not self.errors and not self.warnings:
            report.append("✅ Validation passed with no errors or warnings")

        return "\n".join(report)
