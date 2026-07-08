"""
Component packaging utilities.

Creates properly structured component packages:
- Validates directory structure
- Generates or validates manifest.json
- Creates signed ZIP packages
- Prepares components for distribution

Component Directory Structure:
    my_component/
    ├── manifest.json          # Component metadata (required)
    ├── template.html          # Main template (required)
    ├── assets/                # Optional assets directory
    │   ├── style.css         # Component styles
    │   └── script.js         # Component JavaScript
    ├── locales/               # Optional translations
    │   ├── en.json           # English translations
    │   └── es.json           # Spanish translations
    └── README.md             # Optional documentation

Usage:
    packager = ComponentPackager('/path/to/my_component')
    if packager.validate_structure():
        package_path = packager.package()
        print(f"Package created: {package_path}")
"""

import json
import zipfile
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

from django.core.files import File
from django.utils.translation import gettext_lazy as _


class ComponentPackager:
    """
    Packages components for distribution.

    Handles validation, manifest generation, and ZIP packaging of
    component directories.
    """

    # Required files/directories
    REQUIRED_FILES = ['manifest.json', 'template.html']

    # Optional files/directories
    OPTIONAL_DIRS = ['assets', 'locales', 'docs']

    # Files to exclude from package
    EXCLUDE_PATTERNS = [
        '*.pyc',
        '__pycache__',
        '.git',
        '.DS_Store',
        'Thumbs.db',
        '*.tmp',
        '.env',
    ]

    def __init__(self, component_dir: Path):
        """
        Initialize packager for a component directory.

        Args:
            component_dir: Path to component directory
        """
        if isinstance(component_dir, str):
            component_dir = Path(component_dir)

        self.component_dir = component_dir
        self.manifest = {}
        self.errors = []
        self.warnings = []

    def validate_structure(self) -> Tuple[bool, List[str], List[str]]:
        """
        Validate component directory structure.

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []

        # Check directory exists
        if not self.component_dir.exists():
            self.errors.append(
                f"Directory does not exist: {self.component_dir}"
            )
            return (False, self.errors, self.warnings)

        if not self.component_dir.is_dir():
            self.errors.append(
                f"Path is not a directory: {self.component_dir}"
            )
            return (False, self.errors, self.warnings)

        # Check required files
        for required_file in self.REQUIRED_FILES:
            file_path = self.component_dir / required_file
            if not file_path.exists():
                self.errors.append(f"Missing required file: {required_file}")

        # Validate manifest if it exists
        manifest_path = self.component_dir / 'manifest.json'
        if manifest_path.exists():
            self._validate_manifest(manifest_path)

        # Check for assets directory
        assets_dir = self.component_dir / 'assets'
        if not assets_dir.exists():
            self.warnings.append("No assets directory found")

        # Check for locales
        locales_dir = self.component_dir / 'locales'
        if not locales_dir.exists():
            self.warnings.append("No locales directory found (no translations)")

        is_valid = len(self.errors) == 0
        return (is_valid, self.errors, self.warnings)

    def _validate_manifest(self, manifest_path: Path):
        """Validate manifest.json structure."""
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                self.manifest = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in manifest: {e}")
            return
        except Exception as e:
            self.errors.append(f"Failed to read manifest: {e}")
            return

        # Check required manifest fields
        required_fields = [
            'component_type',
            'display_name',
            'version',
            'author',
        ]

        for field in required_fields:
            if field not in self.manifest:
                self.errors.append(f"Missing required field in manifest: {field}")

        # Validate version format
        if 'version' in self.manifest:
            import re
            version = self.manifest['version']
            if not re.match(r'^\d+\.\d+\.\d+$', version):
                self.warnings.append(
                    "Version should use semantic versioning (e.g., 1.0.0)"
                )

    def generate_manifest(self, **kwargs) -> Dict:
        """
        Generate manifest.json from provided data.

        Args:
            **kwargs: Manifest fields

        Returns:
            Generated manifest dict

        Required kwargs:
            - component_type: str
            - display_name: str
            - version: str
            - author: str

        Optional kwargs:
            - description: str
            - capabilities: list
            - allowed_tiers: list
            - render_mode: str
            - external_domains: list
            - script_budget_kb: float
            - requires_sandbox: bool
        """
        required_fields = ['component_type', 'display_name', 'version', 'author']
        for field in required_fields:
            if field not in kwargs:
                raise ValueError(f"Missing required field: {field}")

        manifest = {
            'component_type': kwargs['component_type'],
            'display_name': kwargs['display_name'],
            'version': kwargs['version'],
            'author': kwargs['author'],
            'description': kwargs.get('description', ''),
            'capabilities': kwargs.get('capabilities', []),
            'allowed_tiers': kwargs.get('allowed_tiers', ['A', 'B', 'C']),
            'render_mode': kwargs.get('render_mode', 'ssr'),
            'external_domains': kwargs.get('external_domains', []),
            'script_budget_kb': kwargs.get('script_budget_kb', 0),
            'requires_sandbox': kwargs.get('requires_sandbox', False),
            'created_at': datetime.utcnow().isoformat(),
        }

        self.manifest = manifest
        return manifest

    def package(self, output_dir: Optional[Path] = None, sign: bool = False) -> Path:
        """
        Create component package ZIP.

        Args:
            output_dir: Directory to write package (default: component_dir parent)
            sign: Whether to sign the package (requires ComponentSigner)

        Returns:
            Path to created package ZIP file

        Raises:
            ValueError: If structure validation fails
        """
        # Validate structure first
        is_valid, errors, warnings = self.validate_structure()
        if not is_valid:
            raise ValueError(
                f"Component structure validation failed: {'; '.join(errors)}"
            )

        # Determine output location
        if output_dir is None:
            output_dir = self.component_dir.parent

        if isinstance(output_dir, str):
            output_dir = Path(output_dir)

        output_dir.mkdir(parents=True, exist_ok=True)

        # Create package filename from component_type and version
        component_type = self.manifest.get(
            'component_type',
            self.component_dir.name
        )
        version = self.manifest.get('version', '1.0.0')
        package_filename = f"{component_type}-{version}.zip"
        package_path = output_dir / package_filename

        # Create ZIP package
        with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            self._add_directory_to_zip(zip_file, self.component_dir)

        return package_path

    def _add_directory_to_zip(
        self,
        zip_file: zipfile.ZipFile,
        directory: Path,
        base_path: Optional[Path] = None
    ):
        """
        Recursively add directory contents to ZIP file.

        Args:
            zip_file: ZipFile instance
            directory: Directory to add
            base_path: Base path for relative paths in ZIP
        """
        if base_path is None:
            base_path = directory

        for item in directory.rglob('*'):
            # Skip excluded patterns
            if any(item.match(pattern) for pattern in self.EXCLUDE_PATTERNS):
                continue

            # Skip if it's a directory (directories are created automatically)
            if item.is_dir():
                continue

            # Calculate relative path
            relative_path = item.relative_to(base_path)

            # Add file to ZIP
            zip_file.write(item, arcname=str(relative_path))

    def calculate_package_stats(self) -> Dict:
        """
        Calculate package statistics.

        Returns:
            Dict with package statistics (file count, total size, etc.)
        """
        stats = {
            'total_files': 0,
            'total_size': 0,
            'asset_count': 0,
            'asset_size': 0,
            'template_size': 0,
            'manifest_size': 0,
        }

        for item in self.component_dir.rglob('*'):
            if item.is_file():
                stats['total_files'] += 1
                file_size = item.stat().st_size
                stats['total_size'] += file_size

                # Track specific file types
                if item.name == 'template.html':
                    stats['template_size'] = file_size
                elif item.name == 'manifest.json':
                    stats['manifest_size'] = file_size
                elif item.parent.name == 'assets':
                    stats['asset_count'] += 1
                    stats['asset_size'] += file_size

        # Convert to KB
        for key in ['total_size', 'asset_size', 'template_size', 'manifest_size']:
            stats[f'{key}_kb'] = stats[key] / 1024

        return stats


def package_component(
    component_dir: str,
    output_dir: Optional[str] = None
) -> Tuple[bool, Optional[Path], List[str]]:
    """
    Convenience function to package a component.

    Args:
        component_dir: Path to component directory
        output_dir: Directory to write package (optional)

    Returns:
        Tuple of (success, package_path, errors)
    """
    try:
        packager = ComponentPackager(component_dir)

        is_valid, errors, warnings = packager.validate_structure()
        if not is_valid:
            return (False, None, errors)

        package_path = packager.package(output_dir=output_dir)
        return (True, package_path, warnings)

    except Exception as e:
        return (False, None, [str(e)])
