"""
Component Package Validation Service
Validates uploaded component ZIP packages before submission.
Supports per-type validation with a dispatch pattern.
"""

import json
import re
import zipfile
import logging

logger = logging.getLogger(__name__)

SEMVER_REGEX = re.compile(
    r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)'
    r'(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)'
    r'(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?'
    r'(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
)

REQUIRED_MANIFEST_FIELDS = ['name', 'version', 'display_name', 'author']
MAX_PACKAGE_SIZE = 50 * 1024 * 1024  # 50 MB

# Patterns that indicate potentially malicious content
SUSPICIOUS_PATTERNS = [
    r'eval\s*\(',
    r'Function\s*\(',
    r'document\.write\s*\(',
    r'<script[^>]*src\s*=\s*["\']https?://',  # External script loading
]


def _new_result():
    """Create a fresh validation result dict."""
    return {
        'valid': False,
        'errors': [],
        'warnings': [],
        'manifest': {},
    }


def _validate_common(package_file):
    """
    Common validation shared by all component types:
    - File size check
    - ZIP integrity
    - Zip bomb detection
    - manifest.json parsing
    - Required manifest fields
    - SemVer version check
    - Suspicious JS pattern scan
    - Platform version compatibility warning

    Returns (result_dict, zipfile.ZipFile_or_None, names_list, manifest_dict, prefix_str).
    If result has errors, zf/names/manifest/prefix may be None.
    """
    result = _new_result()

    # Check file size
    if hasattr(package_file, 'size') and package_file.size > MAX_PACKAGE_SIZE:
        result['errors'].append(
            f'Package too large ({package_file.size / 1024 / 1024:.1f} MB). '
            f'Maximum size is {MAX_PACKAGE_SIZE / 1024 / 1024:.0f} MB.'
        )
        return result, None, None, None, None

    # Check ZIP integrity
    try:
        package_file.seek(0)
        if not zipfile.is_zipfile(package_file):
            result['errors'].append('File is not a valid ZIP archive.')
            return result, None, None, None, None
        package_file.seek(0)
    except Exception as e:
        result['errors'].append(f'Error reading file: {str(e)}')
        return result, None, None, None, None

    try:
        zf = zipfile.ZipFile(package_file, 'r')

        # Check for zip bombs
        total_uncompressed = sum(info.file_size for info in zf.infolist())
        if total_uncompressed > MAX_PACKAGE_SIZE * 10:
            result['errors'].append('Package uncompressed size exceeds limit.')
            zf.close()
            return result, None, None, None, None

        names = zf.namelist()

        # Find manifest.json (could be at root or inside a subdirectory)
        manifest_path = None
        prefix = ''
        for name in names:
            # Check common locations: root, theme/, widget/, etc.
            parts = name.split('/')
            if parts[-1] == 'manifest.json' and len(parts) <= 2:
                manifest_path = name
                prefix = parts[0] + '/' if len(parts) == 2 else ''
                break

        if not manifest_path:
            result['errors'].append(
                'manifest.json not found. Expected at package root or one level deep.'
            )
            zf.close()
            return result, None, None, None, None

        # Parse manifest
        try:
            manifest_content = zf.read(manifest_path).decode('utf-8')
            manifest = json.loads(manifest_content)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            result['errors'].append(f'Invalid manifest.json: {str(e)}')
            zf.close()
            return result, None, None, None, None

        # Validate required manifest fields
        for field in REQUIRED_MANIFEST_FIELDS:
            if field not in manifest:
                result['errors'].append(f'Missing required manifest field: {field}')

        if result['errors']:
            zf.close()
            return result, None, None, None, None

        # Validate version is SemVer
        version = manifest.get('version', '')
        if not SEMVER_REGEX.match(version):
            result['errors'].append(
                f'Invalid version "{version}". Must be valid semantic versioning (e.g., 1.0.0).'
            )

        # Scan for suspicious patterns in JS files
        for name in names:
            if name.endswith('.js'):
                try:
                    js_content = zf.read(name).decode('utf-8', errors='replace')
                    for pattern in SUSPICIOUS_PATTERNS:
                        if re.search(pattern, js_content):
                            result['warnings'].append(
                                f'Suspicious pattern found in {name}: {pattern}'
                            )
                except Exception:
                    pass

        # Check platform version compatibility
        min_platform = manifest.get('min_platform_version')
        if not min_platform:
            engine = manifest.get('engine', {})
            min_platform = engine.get('min') if isinstance(engine, dict) else None
        if not min_platform:
            result['warnings'].append(
                'No minimum platform version specified. '
                'Consider adding min_platform_version to manifest.'
            )

        return result, zf, names, manifest, prefix

    except zipfile.BadZipFile:
        result['errors'].append('Corrupted ZIP file.')
        return result, None, None, None, None
    except Exception as e:
        logger.exception('Error during common package validation')
        result['errors'].append(f'Unexpected error during validation: {str(e)}')
        return result, None, None, None, None


def _validate_theme_specific(zf, names, manifest, prefix, result):
    """Theme-specific validation: CSS files and tokens.json."""
    manifest_path = f'{prefix}manifest.json' if prefix else 'manifest.json'

    # Check for required CSS files
    has_css = any(
        n.endswith('.css') and (n.startswith(f'{prefix}css/') or '/css/' in n)
        for n in names
    )
    if not has_css:
        result['errors'].append('No CSS files found in the package. Themes must include CSS.')

    # Check for tokens.json
    has_tokens = any(
        n.endswith('tokens.json') and n != manifest_path
        for n in names
    )
    if not has_tokens:
        result['warnings'].append('No tokens.json found. Theme may not support design token customization.')

    # Validate tokens.json if present
    for name in names:
        if name.endswith('tokens.json') and name != manifest_path:
            try:
                tokens_content = zf.read(name).decode('utf-8')
                json.loads(tokens_content)
            except (json.JSONDecodeError, UnicodeDecodeError):
                result['errors'].append(f'Invalid JSON in {name}')


def validate_theme(package_file):
    """Validate a theme ZIP package (common + theme-specific checks)."""
    result, zf, names, manifest, prefix = _validate_common(package_file)

    if zf is None:
        package_file.seek(0)
        return result

    try:
        _validate_theme_specific(zf, names, manifest, prefix, result)

        if not result['errors']:
            result['valid'] = True
            result['manifest'] = manifest
    finally:
        zf.close()

    package_file.seek(0)
    return result


def validate_generic(package_file):
    """Validate any component ZIP package (common checks only)."""
    result, zf, names, manifest, prefix = _validate_common(package_file)

    if zf is None:
        package_file.seek(0)
        return result

    try:
        if not result['errors']:
            result['valid'] = True
            result['manifest'] = manifest
    finally:
        zf.close()

    package_file.seek(0)
    return result


# Validator dispatch — add type-specific validators here as needed
VALIDATORS = {
    'theme': validate_theme,
}


def validate_package(package_file, component_type='theme'):
    """
    Validate a component package using the appropriate validator for its type.
    Falls back to generic validation for unknown types.
    """
    validator_fn = VALIDATORS.get(component_type, validate_generic)
    return validator_fn(package_file)
