"""
Detect breaking changes between schema versions

Breaking changes include:
- Field removal
- Field type change
- Required field addition
- Enum value removal

Non-breaking changes include:
- Field addition (optional)
- Enum value addition
- Making required field optional
"""
from typing import Dict, Any, List
from enum import Enum


class ChangeType(Enum):
    """Type of API change"""
    BREAKING = "breaking"
    NON_BREAKING = "non_breaking"
    UNKNOWN = "unknown"


class SchemaChange:
    """Represents a detected schema change"""

    def __init__(
        self,
        change_type: ChangeType,
        field_path: str,
        description: str,
        old_value: Any = None,
        new_value: Any = None
    ):
        self.change_type = change_type
        self.field_path = field_path
        self.description = description
        self.old_value = old_value
        self.new_value = new_value

    def __repr__(self):
        return f"<SchemaChange {self.change_type.value}: {self.field_path} - {self.description}>"


class BreakingChangeReport:
    """Report of breaking changes detected"""

    def __init__(self):
        self.breaking_changes: List[SchemaChange] = []
        self.non_breaking_changes: List[SchemaChange] = []

    @property
    def has_breaking_changes(self) -> bool:
        """Check if any breaking changes were detected"""
        return len(self.breaking_changes) > 0

    def add_breaking(self, change: SchemaChange):
        """Add a breaking change"""
        self.breaking_changes.append(change)

    def add_non_breaking(self, change: SchemaChange):
        """Add a non-breaking change"""
        self.non_breaking_changes.append(change)


def detect_breaking_changes(
    old_schema: Dict[str, Any],
    new_schema: Dict[str, Any],
    path: str = ""
) -> BreakingChangeReport:
    """
    Compare two schemas and detect breaking changes

    Args:
        old_schema: Previous schema baseline
        new_schema: Current schema
        path: Current field path (for nested objects)

    Returns:
        BreakingChangeReport with categorized changes
    """
    report = BreakingChangeReport()

    old_props = old_schema.get('properties', {})
    new_props = new_schema.get('properties', {})

    old_required = set(old_schema.get('required', []))
    new_required = set(new_schema.get('required', []))

    # Check for removed fields (BREAKING)
    for field in old_props:
        if field not in new_props:
            field_path = f"{path}.{field}" if path else field
            report.add_breaking(SchemaChange(
                change_type=ChangeType.BREAKING,
                field_path=field_path,
                description="Field removed from API response",
                old_value=old_props[field],
                new_value=None
            ))

    # Check for added fields
    for field in new_props:
        if field not in old_props:
            field_path = f"{path}.{field}" if path else field

            # Adding required field is BREAKING (client must provide it in requests)
            if field in new_required:
                report.add_breaking(SchemaChange(
                    change_type=ChangeType.BREAKING,
                    field_path=field_path,
                    description="New required field added",
                    old_value=None,
                    new_value=new_props[field]
                ))
            else:
                # Adding optional field is NON-BREAKING
                report.add_non_breaking(SchemaChange(
                    change_type=ChangeType.NON_BREAKING,
                    field_path=field_path,
                    description="New optional field added",
                    old_value=None,
                    new_value=new_props[field]
                ))

    # Check for type changes (BREAKING)
    for field in old_props:
        if field not in new_props:
            continue

        field_path = f"{path}.{field}" if path else field

        old_type = old_props[field].get('type')
        new_type = new_props[field].get('type')

        if old_type != new_type:
            report.add_breaking(SchemaChange(
                change_type=ChangeType.BREAKING,
                field_path=field_path,
                description=f"Field type changed from {old_type} to {new_type}",
                old_value=old_type,
                new_value=new_type
            ))
            continue  # Don't check nested if type changed

        # Check enum value changes
        old_enum = set(old_props[field].get('enum', []))
        new_enum = set(new_props[field].get('enum', []))

        if old_enum or new_enum:
            removed_values = old_enum - new_enum
            added_values = new_enum - old_enum

            if removed_values:
                # Removing enum values is BREAKING
                report.add_breaking(SchemaChange(
                    change_type=ChangeType.BREAKING,
                    field_path=field_path,
                    description=f"Enum values removed: {removed_values}",
                    old_value=list(old_enum),
                    new_value=list(new_enum)
                ))

            if added_values:
                # Adding enum values is NON-BREAKING
                report.add_non_breaking(SchemaChange(
                    change_type=ChangeType.NON_BREAKING,
                    field_path=field_path,
                    description=f"Enum values added: {added_values}",
                    old_value=list(old_enum),
                    new_value=list(new_enum)
                ))

        # Check nested objects recursively
        if old_type == 'object' and new_type == 'object':
            nested_report = detect_breaking_changes(
                old_props[field],
                new_props[field],
                path=field_path
            )
            report.breaking_changes.extend(nested_report.breaking_changes)
            report.non_breaking_changes.extend(nested_report.non_breaking_changes)

        # Check array item schemas
        elif old_type == 'array' and new_type == 'array':
            old_items = old_props[field].get('items', {})
            new_items = new_props[field].get('items', {})

            if old_items.get('type') == 'object' and new_items.get('type') == 'object':
                nested_report = detect_breaking_changes(
                    old_items,
                    new_items,
                    path=f"{field_path}[]"
                )
                report.breaking_changes.extend(nested_report.breaking_changes)
                report.non_breaking_changes.extend(nested_report.non_breaking_changes)

    # Check for required field changes
    # Making optional field required = BREAKING
    newly_required = new_required - old_required
    for field in newly_required:
        if field in old_props:  # Field existed but wasn't required
            field_path = f"{path}.{field}" if path else field
            report.add_breaking(SchemaChange(
                change_type=ChangeType.BREAKING,
                field_path=field_path,
                description="Optional field changed to required",
                old_value="optional",
                new_value="required"
            ))

    # Making required field optional = NON-BREAKING
    no_longer_required = old_required - new_required
    for field in no_longer_required:
        if field in new_props:  # Field still exists but isn't required
            field_path = f"{path}.{field}" if path else field
            report.add_non_breaking(SchemaChange(
                change_type=ChangeType.NON_BREAKING,
                field_path=field_path,
                description="Required field changed to optional",
                old_value="required",
                new_value="optional"
            ))

    return report
