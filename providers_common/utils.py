"""
Provider Common Utilities
=========================
Shared utilities for provider i18n translation support and credential validation.

Third-party providers include translations in their manifest.json.
These utilities load and apply translations for setup wizards and browse pages.

The validate_credential_fields() function provides shared validation for all
provider wizard views, enforcing manifest-defined constraints (required, max_length,
boolean type handling) without requiring JavaScript.
"""

import json
from pathlib import Path

from django.utils.translation import gettext as _


def load_manifest_translations(component_path: Path) -> dict | None:
    """
    Load the translations section from a component's manifest.json.

    Returns a dict suitable for passing to Django's ``json_script``
    template filter, or None if no translations exist. Includes the
    manifest's default_language so the client JS knows the base
    content language.

    Args:
        component_path: Path to the component directory containing manifest.json

    Returns:
        dict of translations (with default_language key), or None
    """
    manifest_file = component_path / "manifest.json"
    if not manifest_file.exists():
        return None

    try:
        with open(manifest_file, encoding="utf-8") as f:
            manifest = json.load(f)

        translations = manifest.get("translations")
        if translations and isinstance(translations, dict):
            # Include default_language so JS knows the base content language.
            # Defaults to 'en' if not specified (backward compatibility).
            default_language = manifest.get("default_language", "en")
            translations_copy = dict(translations)
            translations_copy["default_language"] = default_language
            return translations_copy
    except (OSError, json.JSONDecodeError):
        pass

    return None


def get_translated_provider_fields(manifest: dict, lang: str) -> dict:
    """
    Get translated name/description from a manifest for browse pages.

    Returns a dict with 'name' and 'description' translated into the
    requested language if available. Falls back to the manifest's
    top-level name/description (which are in the developer's default language).

    Fallback chain:
        1. Requested lang translation → use it
        2. No match → content stays in default_language (no blank content)

    Args:
        manifest: The full manifest dict (or subset with name, description,
                  translations, default_language keys)
        lang: The requested language code (e.g., 'es', 'fr')

    Returns:
        dict with 'name' and 'description' keys
    """
    translations = manifest.get("translations", {})
    default_language = manifest.get("default_language", "en")

    result = {
        "name": manifest.get("name", ""),
        "description": manifest.get("description", ""),
    }

    # If admin language matches default, base content is already correct
    if lang == default_language:
        return result

    # Try requested language
    lang_t = translations.get(lang, {})
    if lang_t:
        if lang_t.get("meta.name"):
            result["name"] = lang_t["meta.name"]
        if lang_t.get("meta.description"):
            result["description"] = lang_t["meta.description"]

    # If no match, content stays in default_language (no blank fallback)
    return result


def validate_credential_fields(credential_schema, post_data):
    """
    Validate and clean credential fields from POST data against a manifest's credential_schema.

    Handles:
    - Required field validation
    - max_length / min_length validation
    - Boolean type conversion (checkbox 'on' / absent -> True / False)
    - Multiselect type conversion (list of values with option validation)

    Args:
        credential_schema: dict from manifest's 'credential_schema' key.
            Each field_name maps to a config dict with keys like:
            type, label, title, required, max_length, min_length, default, options, etc.
        post_data: request.POST QueryDict

    Returns:
        tuple of (cleaned_credentials: dict, errors: list[str])
    """
    credentials = {}
    errors = []

    for field_name, field_config in credential_schema.items():
        field_type = field_config.get("type", "text")
        # Support both 'label' and 'title' (manifests vary by provider type)
        field_label = field_config.get("label") or field_config.get("title", field_name)

        # Boolean fields: checkbox sends 'on' when checked, absent when unchecked
        if field_type == "boolean":
            credentials[field_name] = post_data.get(field_name) == "on"
            continue

        # Multiselect fields: select multiple returns a list
        if field_type == "multiselect":
            value = post_data.getlist(field_name)

            # Required validation
            if field_config.get("required", False) and not value:
                errors.append(_("%(field)s is required.") % {"field": field_label})
                credentials[field_name] = value
                continue

            # Validate choices if options are defined
            allowed_values = [opt["value"] for opt in field_config.get("options", [])]
            if allowed_values:
                invalid = [v for v in value if v not in allowed_values]
                if invalid:
                    errors.append(
                        _("%(field)s contains invalid selection: %(values)s")
                        % {"field": field_label, "values": ", ".join(invalid)}
                    )

            credentials[field_name] = value
            continue

        # Number/integer fields: validate and convert to int
        if field_type == "number":
            raw_value = post_data.get(field_name, "").strip()

            if field_config.get("required", False) and not raw_value:
                errors.append(_("%(field)s is required.") % {"field": field_label})
                credentials[field_name] = field_config.get("default")
                continue

            if not raw_value:
                credentials[field_name] = field_config.get("default")
                continue

            try:
                int_value = int(raw_value)
            except (ValueError, TypeError):
                errors.append(_("%(field)s must be a valid number.") % {"field": field_label})
                credentials[field_name] = raw_value
                continue

            minimum = field_config.get("minimum")
            maximum = field_config.get("maximum")
            if minimum is not None and int_value < minimum:
                errors.append(
                    _("%(field)s must be at least %(min)d.")
                    % {"field": field_label, "min": minimum}
                )
            if maximum is not None and int_value > maximum:
                errors.append(
                    _("%(field)s must be at most %(max)d.") % {"field": field_label, "max": maximum}
                )

            credentials[field_name] = int_value
            continue

        # All other field types: get as string
        value = post_data.get(field_name, "").strip()

        # Required validation
        if field_config.get("required", False) and not value:
            errors.append(_("%(field)s is required.") % {"field": field_label})
            credentials[field_name] = value
            continue

        # max_length validation
        max_length = field_config.get("max_length")
        try:
            max_val = int(max_length) if max_length else None
        except (ValueError, TypeError):
            max_val = None
        if max_val is not None and value and len(value) > max_val:
            errors.append(
                _("%(field)s must be at most %(max)d characters.")
                % {"field": field_label, "max": max_val}
            )

        # min_length validation
        min_length = field_config.get("min_length")
        try:
            min_val = int(min_length) if min_length else None
        except (ValueError, TypeError):
            min_val = None
        if min_val is not None and value and len(value) < min_val:
            errors.append(
                _("%(field)s must be at least %(min)d characters.")
                % {"field": field_label, "min": min_val}
            )

        credentials[field_name] = value

    return credentials, errors


def validate_dual_environment_credentials(credential_schema, post_data):
    """
    Validate dual-environment credentials (test + live in single account).

    This function validates payment provider credentials that support both test
    and production environments in a single account. It ensures:
    - At least one complete credential set exists (test or live)
    - All required fields for the active environment are provided
    - Basic validation rules (type, length) are enforced

    The active environment is determined by the test_mode field. When test_mode=True,
    test credentials (test_* fields) are validated. When test_mode=False, live
    credentials (live_* fields) are validated.

    Args:
        credential_schema: dict from manifest's 'credential_schema' key.
            Should include test_mode boolean field and test_/live_ prefixed credential fields.
        post_data: request.POST QueryDict

    Returns:
        tuple of (cleaned_credentials: dict, errors: list[str])
    """
    # First, run basic validation for all fields (handles type conversion, etc.)
    credentials, basic_errors = validate_credential_fields(credential_schema, post_data)
    errors = list(basic_errors)

    # Determine active environment
    test_mode = credentials.get("test_mode", True)
    active_prefix = "test_" if test_mode else "live_"
    mode_name = "test" if test_mode else "production"

    # Find all required fields for the active environment
    active_required_fields = []
    for field_name, field_config in credential_schema.items():
        # Skip test_mode itself and fields from other environment
        if field_name == "test_mode":
            continue
        if not field_name.startswith(active_prefix):
            continue
        if field_config.get("required", False):
            active_required_fields.append(field_name)

    # Validate that all required fields for active environment are provided
    for field_name in active_required_fields:
        value = (
            credentials.get(field_name, "").strip()
            if isinstance(credentials.get(field_name), str)
            else credentials.get(field_name)
        )
        if not value:
            # Get field label for error message
            field_label = credential_schema[field_name].get("label") or credential_schema[
                field_name
            ].get("title", field_name)
            errors.append(
                _("%(field)s is required when in %(mode)s mode.")
                % {"field": field_label, "mode": mode_name}
            )

    return credentials, errors
