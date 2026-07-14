"""
POS Permission Tests

Validates the 13 POS permission flags:
- Flag structure and metadata
- Boolean vs integer type handling
- Default values and constraints
"""

import pytest

from staff_roles.pos_permissions import POS_PERMISSION_FLAGS, POS_PERMISSION_GROUPS

pytestmark = pytest.mark.integrity


class TestPOSPermissionStructure:
    """Validate POS permission flag definitions"""

    # Expected POS permissions
    EXPECTED_POS_PERMISSIONS = [
        "pos_access",
        "pos_discount_manual",
        "pos_discount_max_percent",
        "pos_price_override",
        "pos_refund",
        "pos_void",
        "pos_gift_card_issue",
        "pos_gift_card_balance",
        "pos_cash_management",
        "pos_open_drawer",
        "pos_close_shift",
        "pos_view_reports",
        "pos_stock_adjustment",
    ]

    # Required flag definition keys
    REQUIRED_FLAG_KEYS = ["label", "description", "type", "default", "group"]

    def test_all_expected_flags_present(self):
        """Verify all 13 expected POS permission flags are defined"""
        actual_flags = set(POS_PERMISSION_FLAGS.keys())
        expected_flags = set(self.EXPECTED_POS_PERMISSIONS)

        missing = expected_flags - actual_flags
        extra = actual_flags - expected_flags

        assert not missing, f"Missing expected POS permissions: {missing}"
        assert not extra, f"Unexpected extra POS permissions: {extra}"

    def test_flag_count_is_thirteen(self):
        """Verify exactly 13 POS permission flags exist"""
        assert len(POS_PERMISSION_FLAGS) == 13, (
            f"Expected 13 POS permission flags, found {len(POS_PERMISSION_FLAGS)}"
        )

    def test_all_flags_have_required_keys(self):
        """Verify each flag has all required metadata keys"""
        errors = []

        for flag_key, flag_def in POS_PERMISSION_FLAGS.items():
            missing_keys = [key for key in self.REQUIRED_FLAG_KEYS if key not in flag_def]
            if missing_keys:
                errors.append(f"{flag_key}: missing keys {missing_keys}")

        assert not errors, "POS permissions with missing keys:\n  " + "\n  ".join(errors)

    def test_flag_types_are_valid(self):
        """Verify all flags use either 'bool' or 'integer' type"""
        errors = []
        valid_types = ["bool", "integer"]

        for flag_key, flag_def in POS_PERMISSION_FLAGS.items():
            flag_type = flag_def.get("type")
            if flag_type not in valid_types:
                errors.append(
                    f"{flag_key}: invalid type '{flag_type}' (must be 'bool' or 'integer')"
                )

        assert not errors, "POS permissions with invalid types:\n  " + "\n  ".join(errors)

    def test_boolean_flags_have_boolean_defaults(self):
        """Verify boolean flags have boolean default values"""
        errors = []

        for flag_key, flag_def in POS_PERMISSION_FLAGS.items():
            if flag_def.get("type") == "bool":
                default = flag_def.get("default")
                if not isinstance(default, bool):
                    errors.append(f"{flag_key}: boolean flag has non-boolean default '{default}'")

        assert not errors, "Boolean flags with invalid defaults:\n  " + "\n  ".join(errors)

    def test_integer_flags_have_integer_defaults(self):
        """Verify integer flags have integer default values"""
        errors = []

        for flag_key, flag_def in POS_PERMISSION_FLAGS.items():
            if flag_def.get("type") == "integer":
                default = flag_def.get("default")
                if not isinstance(default, int):
                    errors.append(f"{flag_key}: integer flag has non-integer default '{default}'")

        assert not errors, "Integer flags with invalid defaults:\n  " + "\n  ".join(errors)

    def test_integer_flags_have_min_max_constraints(self):
        """Verify integer flags define min and max values"""
        errors = []

        for flag_key, flag_def in POS_PERMISSION_FLAGS.items():
            if flag_def.get("type") == "integer":
                if "min" not in flag_def:
                    errors.append(f"{flag_key}: missing 'min' constraint")
                if "max" not in flag_def:
                    errors.append(f"{flag_key}: missing 'max' constraint")

                # Verify min <= default <= max
                if "min" in flag_def and "max" in flag_def:
                    min_val = flag_def["min"]
                    max_val = flag_def["max"]
                    default = flag_def.get("default")

                    if not (min_val <= default <= max_val):
                        errors.append(
                            f"{flag_key}: default {default} not in range [{min_val}, {max_val}]"
                        )

        assert not errors, "Integer flags with missing or invalid constraints:\n  " + "\n  ".join(
            errors
        )

    def test_all_flags_assigned_to_groups(self):
        """Verify all flags are assigned to defined permission groups"""
        errors = []
        valid_groups = set(POS_PERMISSION_GROUPS.keys())

        for flag_key, flag_def in POS_PERMISSION_FLAGS.items():
            group = flag_def.get("group")
            if group not in valid_groups:
                errors.append(f"{flag_key}: invalid group '{group}' (valid: {valid_groups})")

        assert not errors, "POS permissions with invalid group assignments:\n  " + "\n  ".join(
            errors
        )


class TestPOSPermissionGroups:
    """Validate POS permission group definitions"""

    EXPECTED_GROUPS = [
        "general",
        "sales",
        "refunds",
        "gift_cards",
        "cash",
        "reports",
        "inventory",
    ]

    def test_all_expected_groups_defined(self):
        """Verify all expected permission groups are defined"""
        actual_groups = set(POS_PERMISSION_GROUPS.keys())
        expected_groups = set(self.EXPECTED_GROUPS)

        missing = expected_groups - actual_groups
        assert not missing, f"Missing expected POS permission groups: {missing}"

    def test_groups_have_labels(self):
        """Verify all groups have labels defined"""
        errors = []

        for group_key, group_def in POS_PERMISSION_GROUPS.items():
            if "label" not in group_def:
                errors.append(f"{group_key}: missing 'label'")

        assert not errors, "POS permission groups missing labels:\n  " + "\n  ".join(errors)

    def test_groups_have_icons(self):
        """Verify all groups have Font Awesome icons"""
        errors = []

        for group_key, group_def in POS_PERMISSION_GROUPS.items():
            icon = group_def.get("icon", "")
            if not icon.startswith("fas fa-") and not icon.startswith("fab fa-"):
                errors.append(f"{group_key}: icon '{icon}' doesn't use Font Awesome format")

        assert not errors, "POS permission groups with invalid icons:\n  " + "\n  ".join(errors)

    def test_all_groups_have_at_least_one_permission(self):
        """Verify each group has at least one permission assigned to it"""
        group_counts = dict.fromkeys(POS_PERMISSION_GROUPS.keys(), 0)

        for flag_def in POS_PERMISSION_FLAGS.values():
            group = flag_def.get("group")
            if group in group_counts:
                group_counts[group] += 1

        empty_groups = [group for group, count in group_counts.items() if count == 0]

        assert not empty_groups, f"Permission groups with no permissions assigned: {empty_groups}"


class TestSpecificPOSPermissions:
    """Validate specific POS permission configurations"""

    def test_pos_access_is_boolean_defaulting_false(self):
        """Verify pos_access is a boolean flag defaulting to False"""
        flag = POS_PERMISSION_FLAGS["pos_access"]
        assert flag["type"] == "bool"
        assert flag["default"] is False

    def test_pos_discount_max_percent_is_integer_0_to_100(self):
        """Verify pos_discount_max_percent is integer with 0-100 range"""
        flag = POS_PERMISSION_FLAGS["pos_discount_max_percent"]
        assert flag["type"] == "integer"
        assert flag["min"] == 0
        assert flag["max"] == 100
        assert flag["default"] == 0

    def test_pos_gift_card_balance_defaults_true(self):
        """
        Verify pos_gift_card_balance defaults to True.
        This is the only POS permission that defaults to True (read-only operation).
        """
        flag = POS_PERMISSION_FLAGS["pos_gift_card_balance"]
        assert flag["type"] == "bool"
        assert flag["default"] is True

    def test_destructive_operations_default_false(self):
        """
        Verify destructive operations (refund, void, cash_management) default to False
        """
        destructive_flags = [
            "pos_refund",
            "pos_void",
            "pos_cash_management",
            "pos_open_drawer",
            "pos_close_shift",
        ]

        for flag_key in destructive_flags:
            flag = POS_PERMISSION_FLAGS[flag_key]
            assert flag["type"] == "bool", f"{flag_key} should be boolean"
            assert flag["default"] is False, f"{flag_key} should default to False"

    def test_discount_and_price_override_flags_exist(self):
        """
        Verify both manual discount and price override flags exist separately
        """
        assert "pos_discount_manual" in POS_PERMISSION_FLAGS
        assert "pos_price_override" in POS_PERMISSION_FLAGS

        # They should be separate permissions
        discount_flag = POS_PERMISSION_FLAGS["pos_discount_manual"]
        override_flag = POS_PERMISSION_FLAGS["pos_price_override"]

        assert discount_flag["type"] == "bool"
        assert override_flag["type"] == "bool"


class TestPOSPermissionNaming:
    """Validate POS permission naming conventions"""

    def test_all_permissions_start_with_pos_prefix(self):
        """Verify all POS permission keys start with 'pos_' prefix"""
        errors = []

        for flag_key in POS_PERMISSION_FLAGS:
            if not flag_key.startswith("pos_"):
                errors.append(f"{flag_key}: doesn't start with 'pos_' prefix")

        assert not errors, "POS permissions not following naming convention:\n  " + "\n  ".join(
            errors
        )

    def test_permission_keys_use_snake_case(self):
        """Verify all permission keys use snake_case"""
        import re

        snake_case_pattern = re.compile(r"^[a-z][a-z0-9_]*$")
        errors = []

        for flag_key in POS_PERMISSION_FLAGS:
            if not snake_case_pattern.match(flag_key):
                errors.append(f"{flag_key}: doesn't use snake_case")

        assert not errors, "POS permissions not using snake_case:\n  " + "\n  ".join(errors)
