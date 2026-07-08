"""
Contract validation using schema matching

Validates API response data against JSON Schema definitions
"""
from typing import Dict, Any, List
from decimal import Decimal


class SchemaValidationResult:
    """Result of schema validation"""

    def __init__(self):
        self.is_valid: bool = True
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def add_error(self, error: str):
        """Add an error and mark as invalid"""
        self.errors.append(error)
        self.is_valid = False

    def add_warning(self, warning: str):
        """Add a warning (doesn't affect validity)"""
        self.warnings.append(warning)


def validate_response_against_schema(
    response_data: Dict[str, Any],
    schema: Dict[str, Any],
    path: str = ""
) -> SchemaValidationResult:
    """
    Validate API response data against JSON Schema

    Args:
        response_data: Actual API response
        schema: Expected JSON Schema
        path: Current field path (for nested validation)

    Returns:
        SchemaValidationResult with validation outcome
    """
    result = SchemaValidationResult()

    # Validate required fields
    required_fields = schema.get('required', [])
    for field in required_fields:
        if field not in response_data:
            result.add_error(f"{path}.{field}: Required field missing" if path else f"{field}: Required field missing")

    # Validate field types and values
    properties = schema.get('properties', {})
    for field, field_schema in properties.items():
        field_path = f"{path}.{field}" if path else field

        if field not in response_data:
            # Field not in response - only error if required
            continue

        actual_value = response_data[field]
        expected_type = field_schema.get('type')

        # Validate type
        if not _validate_type(actual_value, expected_type):
            result.add_error(
                f"{field_path}: Incorrect type. "
                f"Expected: {expected_type}, Got: {_get_type_name(actual_value)}"
            )
            continue  # Skip further validation if type is wrong

        # Validate nested objects recursively
        if expected_type == 'object' and isinstance(actual_value, dict):
            nested_result = validate_response_against_schema(
                actual_value,
                field_schema,
                path=field_path
            )
            result.errors.extend(nested_result.errors)
            result.warnings.extend(nested_result.warnings)
            if not nested_result.is_valid:
                result.is_valid = False

        # Validate arrays
        elif expected_type == 'array' and isinstance(actual_value, list):
            item_schema = field_schema.get('items', {})
            if item_schema.get('type') == 'object':
                for idx, item in enumerate(actual_value):
                    if isinstance(item, dict):
                        item_result = validate_response_against_schema(
                            item,
                            item_schema,
                            path=f"{field_path}[{idx}]"
                        )
                        result.errors.extend(item_result.errors)
                        result.warnings.extend(item_result.warnings)
                        if not item_result.is_valid:
                            result.is_valid = False

        # Validate enum values
        enum_values = field_schema.get('enum')
        if enum_values and actual_value not in enum_values:
            result.add_error(
                f"{field_path}: Value '{actual_value}' not in allowed enum values: {enum_values}"
            )

    # Check for unexpected fields (warning only, not error)
    for field in response_data:
        if field not in properties:
            field_path = f"{path}.{field}" if path else field
            result.add_warning(f"{field_path}: Unexpected field in response")

    return result


def _validate_type(value: Any, expected_type: str) -> bool:
    """
    Check if value matches expected JSON Schema type

    Args:
        value: The value to check
        expected_type: JSON Schema type string

    Returns:
        True if value matches expected type
    """
    type_map = {
        'string': str,
        'integer': int,
        'number': (int, float, Decimal),
        'boolean': bool,
        'array': list,
        'object': dict,
        'null': type(None)
    }

    expected_python_type = type_map.get(expected_type)
    if expected_python_type is None:
        # Unknown type, allow it (don't fail validation for unknown types)
        return True

    return isinstance(value, expected_python_type)


def _get_type_name(value: Any) -> str:
    """
    Get JSON Schema type name for a Python value

    Args:
        value: Python value

    Returns:
        JSON Schema type name
    """
    if isinstance(value, bool):
        return 'boolean'
    elif isinstance(value, int):
        return 'integer'
    elif isinstance(value, (float, Decimal)):
        return 'number'
    elif isinstance(value, str):
        return 'string'
    elif isinstance(value, list):
        return 'array'
    elif isinstance(value, dict):
        return 'object'
    elif value is None:
        return 'null'
    else:
        return type(value).__name__


def extract_response_schema(response_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract schema structure from actual API response

    Generates a JSON Schema representation of the response data structure.

    Args:
        response_data: API response to analyze

    Returns:
        Dict describing the response structure in JSON Schema format
    """
    def build_schema(data):
        if isinstance(data, dict):
            properties = {}
            required = []

            for key, value in data.items():
                properties[key] = build_schema(value)
                # All present fields are considered required in the baseline
                required.append(key)

            return {
                "type": "object",
                "properties": properties,
                "required": required
            }
        elif isinstance(data, list):
            if len(data) > 0:
                # Use first item as schema template
                return {
                    "type": "array",
                    "items": build_schema(data[0])
                }
            return {
                "type": "array",
                "items": {}
            }
        else:
            # Primitive type
            return {"type": _get_type_name(data)}

    return build_schema(response_data)
