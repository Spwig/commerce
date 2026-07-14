"""
Type-specific validation for custom field values.

Each field type has a validator that checks the value against
the field definition's validation_config.
"""

import re
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, validate_email
from django.utils.translation import gettext_lazy as _


def validate_custom_field_value(field_def, value):
    """
    Validate a value against a custom field definition.

    Args:
        field_def: CustomFieldDefinition instance
        value: The value to validate

    Returns:
        The cleaned/coerced value

    Raises:
        ValidationError if the value is invalid
    """
    field_type = field_def.field_type
    config = field_def.validation_config or {}

    # Handle required fields
    if field_def.is_required and (value is None or value == "" or value == []):
        raise ValidationError(_("%(field)s is required."), params={"field": field_def.name})

    # Allow empty values for non-required fields
    if value is None or value == "" or value == []:
        return value

    # Dispatch to type-specific validator
    validator = VALIDATORS.get(field_type)
    if validator:
        return validator(field_def, value, config)

    return value


def _validate_text(field_def, value, config):
    """Validate text/textarea field."""
    value = str(value)
    min_length = config.get("min_length")
    max_length = config.get("max_length")
    regex = config.get("regex")

    if min_length is not None and len(value) < min_length:
        raise ValidationError(
            _("%(field)s must be at least %(min)d characters."),
            params={"field": field_def.name, "min": min_length},
        )
    if max_length is not None and len(value) > max_length:
        raise ValidationError(
            _("%(field)s must be at most %(max)d characters."),
            params={"field": field_def.name, "max": max_length},
        )
    if regex and not re.match(regex, value):
        raise ValidationError(
            _("%(field)s does not match the required pattern."),
            params={"field": field_def.name},
        )
    return value


def _validate_number(field_def, value, config):
    """Validate integer number field."""
    try:
        value = int(value)
    except (ValueError, TypeError):
        raise ValidationError(
            _("%(field)s must be a whole number."), params={"field": field_def.name}
        )

    min_val = config.get("min")
    max_val = config.get("max")
    if min_val is not None and value < min_val:
        raise ValidationError(
            _("%(field)s must be at least %(min)s."),
            params={"field": field_def.name, "min": min_val},
        )
    if max_val is not None and value > max_val:
        raise ValidationError(
            _("%(field)s must be at most %(max)s."),
            params={"field": field_def.name, "max": max_val},
        )
    return value


def _validate_decimal(field_def, value, config):
    """Validate decimal number field."""
    try:
        value = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        raise ValidationError(
            _("%(field)s must be a valid decimal number."), params={"field": field_def.name}
        )

    min_val = config.get("min")
    max_val = config.get("max")
    decimal_places = config.get("decimal_places", 2)
    if min_val is not None and value < Decimal(str(min_val)):
        raise ValidationError(
            _("%(field)s must be at least %(min)s."),
            params={"field": field_def.name, "min": min_val},
        )
    if max_val is not None and value > Decimal(str(max_val)):
        raise ValidationError(
            _("%(field)s must be at most %(max)s."),
            params={"field": field_def.name, "max": max_val},
        )
    # Round to configured decimal places
    return float(round(value, decimal_places))


def _validate_boolean(field_def, value, config):
    """Validate boolean field."""
    if isinstance(value, str):
        value = value.lower() in ("true", "1", "yes", "on")
    return bool(value)


def _validate_date(field_def, value, config):
    """Validate date field."""
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str):
        try:
            date.fromisoformat(value)
            return value
        except ValueError:
            pass
    raise ValidationError(
        _("%(field)s must be a valid date (YYYY-MM-DD)."), params={"field": field_def.name}
    )


def _validate_datetime(field_def, value, config):
    """Validate datetime field."""
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, str):
        try:
            datetime.fromisoformat(value)
            return value
        except ValueError:
            pass
    raise ValidationError(
        _("%(field)s must be a valid date and time."), params={"field": field_def.name}
    )


def _validate_url(field_def, value, config):
    """Validate URL field."""
    value = str(value)
    url_validator = URLValidator()
    try:
        url_validator(value)
    except ValidationError:
        raise ValidationError(_("%(field)s must be a valid URL."), params={"field": field_def.name})
    return value


def _validate_email(field_def, value, config):
    """Validate email field."""
    value = str(value)
    try:
        validate_email(value)
    except ValidationError:
        raise ValidationError(
            _("%(field)s must be a valid email address."), params={"field": field_def.name}
        )
    return value


def _validate_select(field_def, value, config):
    """Validate single-select dropdown field."""
    choices = config.get("choices", [])
    valid_values = [c.get("value") for c in choices]
    if value not in valid_values:
        raise ValidationError(
            _('%(field)s: "%(value)s" is not a valid choice.'),
            params={"field": field_def.name, "value": value},
        )
    return value


def _validate_multiselect(field_def, value, config):
    """Validate multi-select dropdown field."""
    if isinstance(value, str):
        value = [v.strip() for v in value.split(",") if v.strip()]
    if not isinstance(value, list):
        raise ValidationError(
            _("%(field)s must be a list of values."), params={"field": field_def.name}
        )
    choices = config.get("choices", [])
    valid_values = [c.get("value") for c in choices]
    for v in value:
        if v not in valid_values:
            raise ValidationError(
                _('%(field)s: "%(value)s" is not a valid choice.'),
                params={"field": field_def.name, "value": v},
            )
    return value


def _validate_color(field_def, value, config):
    """Validate color field (hex format)."""
    value = str(value)
    if not re.match(r"^#[0-9a-fA-F]{6}$", value):
        raise ValidationError(
            _("%(field)s must be a valid hex color (e.g., #FF0000)."),
            params={"field": field_def.name},
        )
    return value


# Map field types to validators
VALIDATORS = {
    "text": _validate_text,
    "textarea": _validate_text,
    "number": _validate_number,
    "decimal": _validate_decimal,
    "boolean": _validate_boolean,
    "date": _validate_date,
    "datetime": _validate_datetime,
    "url": _validate_url,
    "email": _validate_email,
    "select": _validate_select,
    "multiselect": _validate_multiselect,
    "color": _validate_color,
}
