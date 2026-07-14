"""
Schema generation utilities

Generates JSON Schemas from DRF serializers and API responses
"""

from typing import Any

from rest_framework import serializers


def generate_serializer_schema(serializer_class: type[serializers.Serializer]) -> dict[str, Any]:
    """
    Generate JSON Schema from DRF serializer

    This is a simplified schema generator. For production use, consider using
    drf-spectacular's schema generation capabilities.

    Args:
        serializer_class: DRF Serializer class

    Returns:
        Dict containing JSON Schema representation
    """
    serializer_instance = serializer_class()
    component_name = serializer_class.__name__

    properties = {}
    required = []

    for field_name, field in serializer_instance.fields.items():
        # Determine JSON Schema type from field type
        field_schema = _get_field_schema(field)
        properties[field_name] = field_schema

        # Mark as required if field is required
        if field.required and not field.read_only:
            required.append(field_name)

    return {
        "type": "object",
        "component_name": component_name,
        "properties": properties,
        "required": required,
        "description": serializer_class.__doc__ or "",
    }


def _get_field_schema(field: serializers.Field) -> dict[str, Any]:
    """
    Get JSON Schema for a DRF field

    Args:
        field: DRF Field instance

    Returns:
        JSON Schema dict for the field
    """
    schema = {}

    # Map DRF field types to JSON Schema types
    if isinstance(field, serializers.BooleanField):
        schema["type"] = "boolean"
    elif isinstance(field, serializers.IntegerField):
        schema["type"] = "integer"
    elif isinstance(field, (serializers.FloatField, serializers.DecimalField)):
        schema["type"] = "number"
    elif isinstance(field, serializers.CharField):
        schema["type"] = "string"
        if hasattr(field, "max_length") and field.max_length:
            schema["maxLength"] = field.max_length
    elif isinstance(field, serializers.EmailField):
        schema["type"] = "string"
        schema["format"] = "email"
    elif isinstance(field, serializers.URLField):
        schema["type"] = "string"
        schema["format"] = "uri"
    elif isinstance(field, serializers.DateTimeField):
        schema["type"] = "string"
        schema["format"] = "date-time"
    elif isinstance(field, serializers.DateField):
        schema["type"] = "string"
        schema["format"] = "date"
    elif isinstance(field, (serializers.ListField, serializers.ListSerializer)):
        schema["type"] = "array"
        # Try to get item schema
        if hasattr(field, "child"):
            schema["items"] = _get_field_schema(field.child)
        else:
            schema["items"] = {}
    elif isinstance(field, (serializers.DictField, serializers.JSONField)):
        schema["type"] = "object"
    elif isinstance(field, serializers.Serializer):
        # Nested serializer
        nested_schema = generate_serializer_schema(type(field))
        schema = nested_schema
    elif isinstance(field, serializers.ChoiceField):
        # Enum field
        schema["type"] = "string"
        schema["enum"] = [choice for choice, _ in field.choices.items()]
    else:
        # Default to string for unknown types
        schema["type"] = "string"

    # Add description if available
    if field.help_text:
        schema["description"] = field.help_text

    return schema
