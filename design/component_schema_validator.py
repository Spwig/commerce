"""
Component Schema Validator

Validates component packages against the manifest schema and checks directory structure.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

try:
    import jsonschema
    from jsonschema import validate, ValidationError, SchemaError
except ImportError:
    jsonschema = None
    validate = None
    ValidationError = None
    SchemaError = None


logger = logging.getLogger(__name__)


class ComponentValidationError(Exception):
    """Raised when component validation fails."""
    pass


class ComponentSchemaValidator:
    """
    Validates component packages against manifest schema and file structure.

    Usage:
        validator = ComponentSchemaValidator()
        is_valid, errors = validator.validate_component('/path/to/component/')

        if not is_valid:
            for error in errors:
                print(f"Error: {error}")
    """

    REQUIRED_FILES = [
        'manifest.json',
        'template.html',
        'schema.json',
    ]

    OPTIONAL_FILES = [
        'preview.png',
        'preview.jpg',
        'preview.jpeg',
        'preview.webp',
    ]

    def __init__(self, schema_path: Optional[Path] = None):
        """
        Initialize validator with manifest schema.

        Args:
            schema_path: Path to manifest schema JSON file.
                        If None, uses default schema in design app.
        """
        if schema_path is None:
            # Default to schema in design app
            schema_path = Path(__file__).parent / 'component_manifest_schema.json'

        self.schema_path = Path(schema_path)
        self.manifest_schema = self._load_schema()
        self.errors: List[str] = []

    def _load_schema(self) -> Dict[str, Any]:
        """Load and parse the manifest JSON schema."""
        try:
            with open(self.schema_path, 'r', encoding='utf-8') as f:
                schema = json.load(f)

            logger.info(f"Loaded manifest schema from {self.schema_path}")
            return schema

        except FileNotFoundError:
            raise ComponentValidationError(
                f"Manifest schema not found at {self.schema_path}"
            )
        except json.JSONDecodeError as e:
            raise ComponentValidationError(
                f"Invalid JSON in manifest schema: {e}"
            )

    def validate_component(
        self,
        component_dir: Path
    ) -> Tuple[bool, List[str]]:
        """
        Validate complete component package.

        Args:
            component_dir: Path to component directory

        Returns:
            Tuple of (is_valid, error_list)
        """
        self.errors = []
        component_dir = Path(component_dir)

        # 1. Check directory exists
        if not component_dir.exists():
            self.errors.append(f"Component directory does not exist: {component_dir}")
            return False, self.errors

        if not component_dir.is_dir():
            self.errors.append(f"Path is not a directory: {component_dir}")
            return False, self.errors

        # 2. Check required files
        manifest_path = component_dir / 'manifest.json'
        if not self._validate_required_files(component_dir):
            return False, self.errors

        # 3. Load and validate manifest
        try:
            manifest = self._load_manifest(manifest_path)
        except Exception as e:
            self.errors.append(f"Failed to load manifest: {e}")
            return False, self.errors

        if not self._validate_manifest_schema(manifest):
            return False, self.errors

        # 4. Validate template file
        if not self._validate_template(component_dir / 'template.html'):
            return False, self.errors

        # 5. Validate props schema file
        schema_path = component_dir / 'schema.json'
        if not self._validate_props_schema(schema_path, manifest):
            return False, self.errors

        # 6. Validate assets if declared
        if 'assets' in manifest:
            if not self._validate_assets(component_dir, manifest['assets']):
                return False, self.errors

        # 7. Validate locales if declared
        if 'locales' in manifest:
            if not self._validate_locales(component_dir, manifest['locales']):
                return False, self.errors

        # 8. Validate preview image if declared
        if 'preview' in manifest:
            if not self._validate_preview(component_dir, manifest['preview']):
                return False, self.errors

        # 9. Validate dependencies format
        if 'dependencies' in manifest:
            if not self._validate_dependencies(manifest['dependencies']):
                return False, self.errors

        return len(self.errors) == 0, self.errors

    def _validate_required_files(self, component_dir: Path) -> bool:
        """Check that all required files exist."""
        for filename in self.REQUIRED_FILES:
            file_path = component_dir / filename
            if not file_path.exists():
                self.errors.append(f"Required file missing: {filename}")
                return False

        return True

    def _load_manifest(self, manifest_path: Path) -> Dict[str, Any]:
        """Load and parse manifest.json."""
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            return manifest

        except json.JSONDecodeError as e:
            raise ComponentValidationError(f"Invalid JSON in manifest: {e}")

    def _validate_manifest_schema(self, manifest: Dict[str, Any]) -> bool:
        """Validate manifest against JSON schema."""
        if jsonschema is None:
            logger.warning(
                "jsonschema library not installed - skipping schema validation"
            )
            return True

        try:
            validate(instance=manifest, schema=self.manifest_schema)
            return True

        except ValidationError as e:
            self.errors.append(f"Manifest schema validation failed: {e.message}")
            return False

        except SchemaError as e:
            self.errors.append(f"Invalid manifest schema: {e.message}")
            return False

    def _validate_template(self, template_path: Path) -> bool:
        """Validate template.html file."""
        if not template_path.exists():
            self.errors.append("Template file (template.html) does not exist")
            return False

        # Check file is not empty
        if template_path.stat().st_size == 0:
            self.errors.append("Template file is empty")
            return False

        # Check it's valid UTF-8
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                f.read()
        except UnicodeDecodeError:
            self.errors.append("Template file is not valid UTF-8")
            return False

        return True

    def _validate_props_schema(
        self,
        schema_path: Path,
        manifest: Dict[str, Any]
    ) -> bool:
        """Validate props schema file."""
        if not schema_path.exists():
            self.errors.append("Props schema file (schema.json) does not exist")
            return False

        # Load and validate it's valid JSON
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                props_schema = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Props schema is not valid JSON: {e}")
            return False

        # Check it matches the props_schema in manifest (if present)
        if 'props_schema' in manifest:
            if props_schema != manifest['props_schema']:
                self.errors.append(
                    "Props schema in schema.json does not match manifest.props_schema"
                )
                return False

        # Validate it's a valid JSON Schema
        if jsonschema is None:
            logger.warning(
                "jsonschema library not installed - skipping props schema validation"
            )
            return True

        try:
            # Check it's a valid JSON Schema by creating a validator
            jsonschema.Draft7Validator.check_schema(props_schema)
        except SchemaError as e:
            self.errors.append(f"Props schema is not a valid JSON Schema: {e.message}")
            return False

        return True

    def _validate_assets(
        self,
        component_dir: Path,
        assets: Dict[str, List[str]]
    ) -> bool:
        """Validate declared asset files exist."""
        for asset_type, asset_paths in assets.items():
            if asset_type not in ['css', 'js', 'images']:
                self.errors.append(f"Unknown asset type: {asset_type}")
                return False

            for asset_path in asset_paths:
                full_path = component_dir / asset_path
                if not full_path.exists():
                    self.errors.append(f"Asset file does not exist: {asset_path}")
                    return False

                if not full_path.is_file():
                    self.errors.append(f"Asset path is not a file: {asset_path}")
                    return False

        return True

    def _validate_locales(
        self,
        component_dir: Path,
        locales: List[str]
    ) -> bool:
        """Validate locale files exist for declared locales."""
        locales_dir = component_dir / 'locales'

        if not locales_dir.exists():
            self.errors.append("Locales declared but locales/ directory does not exist")
            return False

        for locale in locales:
            locale_file = locales_dir / f"{locale}.json"
            if not locale_file.exists():
                self.errors.append(f"Locale file does not exist: locales/{locale}.json")
                return False

            # Validate it's valid JSON
            try:
                with open(locale_file, 'r', encoding='utf-8') as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                self.errors.append(f"Locale file {locale}.json is not valid JSON: {e}")
                return False

        return True

    def _validate_preview(self, component_dir: Path, preview_filename: str) -> bool:
        """Validate preview image file exists."""
        preview_path = component_dir / preview_filename

        if not preview_path.exists():
            self.errors.append(f"Preview image does not exist: {preview_filename}")
            return False

        if not preview_path.is_file():
            self.errors.append(f"Preview path is not a file: {preview_filename}")
            return False

        # Check file size is reasonable (not too large)
        max_size = 5 * 1024 * 1024  # 5 MB
        if preview_path.stat().st_size > max_size:
            self.errors.append(
                f"Preview image is too large (max 5MB): {preview_filename}"
            )
            return False

        return True

    def _validate_dependencies(self, dependencies: List[Dict[str, str]]) -> bool:
        """Validate dependency format."""
        for dep in dependencies:
            # Check version constraints are valid
            min_ver = dep.get('min_version')
            max_ver = dep.get('max_version')

            if min_ver and max_ver:
                # Compare versions
                if self._compare_versions(min_ver, max_ver) > 0:
                    self.errors.append(
                        f"Dependency {dep['name']}: min_version ({min_ver}) "
                        f"is greater than max_version ({max_ver})"
                    )
                    return False

        return True

    def _compare_versions(self, v1: str, v2: str) -> int:
        """
        Compare two semantic versions.

        Returns:
            -1 if v1 < v2
             0 if v1 == v2
             1 if v1 > v2
        """
        parts1 = [int(x) for x in v1.split('.')]
        parts2 = [int(x) for x in v2.split('.')]

        for p1, p2 in zip(parts1, parts2):
            if p1 < p2:
                return -1
            elif p1 > p2:
                return 1

        return 0

    def validate_manifest_only(self, manifest: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate just the manifest JSON against the schema.

        Useful for validating manifest before packaging.

        Args:
            manifest: Manifest dictionary

        Returns:
            Tuple of (is_valid, error_list)
        """
        self.errors = []

        if not self._validate_manifest_schema(manifest):
            return False, self.errors

        if 'dependencies' in manifest:
            if not self._validate_dependencies(manifest['dependencies']):
                return False, self.errors

        return True, self.errors
