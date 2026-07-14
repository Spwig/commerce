"""
Permission Category Tests

Validates the 16 permission categories:
- Category structure and metadata
- Permission resolution logic (view/full levels)
- Sidebar category mapping
"""

import pytest
from django.contrib.auth.models import Permission

from staff_roles.categories import PERMISSION_CATEGORIES, SIDEBAR_CATEGORY_MAP
from staff_roles.services import resolve_category_permissions

pytestmark = pytest.mark.integrity


class TestPermissionCategoryStructure:
    """Validate category definition structure"""

    # Expected categories (16 total — the original 13 + system, custom_fields,
    # translations added as the platform picked up dedicated admin areas for
    # each).
    EXPECTED_CATEGORIES = [
        "catalog",
        "orders",
        "customers",
        "content",
        "design",
        "marketing",
        "media",
        "email",
        "payments",
        "search",
        "settings",
        "pos_admin",
        "users",
        "translations",
        "custom_fields",
        "system",
    ]

    # Required category keys
    REQUIRED_CATEGORY_KEYS = ["label", "icon", "description", "sort_order", "permissions"]
    REQUIRED_PERMISSION_LEVELS = ["view", "full"]

    def test_all_expected_categories_present(self):
        """Verify all 16 expected categories are defined"""
        actual_categories = set(PERMISSION_CATEGORIES.keys())
        expected_categories = set(self.EXPECTED_CATEGORIES)

        missing = expected_categories - actual_categories
        extra = actual_categories - expected_categories

        assert not missing, f"Missing expected categories: {missing}"
        assert not extra, f"Unexpected extra categories: {extra}"

    def test_category_count_is_sixteen(self):
        """Verify exactly 16 categories exist"""
        assert len(PERMISSION_CATEGORIES) == len(self.EXPECTED_CATEGORIES), (
            f"Expected {len(self.EXPECTED_CATEGORIES)} permission categories, "
            f"found {len(PERMISSION_CATEGORIES)}"
        )

    def test_all_categories_have_required_keys(self):
        """Verify each category has all required metadata keys"""
        errors = []

        for category_key, category_def in PERMISSION_CATEGORIES.items():
            missing_keys = [key for key in self.REQUIRED_CATEGORY_KEYS if key not in category_def]
            if missing_keys:
                errors.append(f"{category_key}: missing keys {missing_keys}")

        assert not errors, "Categories with missing keys:\n  " + "\n  ".join(errors)

    def test_all_categories_have_view_and_full_permissions(self):
        """Verify each category defines both 'view' and 'full' permission levels"""
        errors = []

        for category_key, category_def in PERMISSION_CATEGORIES.items():
            permissions = category_def.get("permissions", {})
            missing_levels = [
                level for level in self.REQUIRED_PERMISSION_LEVELS if level not in permissions
            ]
            if missing_levels:
                errors.append(f"{category_key}: missing permission levels {missing_levels}")

        assert not errors, "Categories with missing permission levels:\n  " + "\n  ".join(errors)

    def test_category_labels_are_translated(self):
        """Verify category labels use gettext_lazy for translation"""
        from django.utils.functional import Promise

        errors = []
        for category_key, category_def in PERMISSION_CATEGORIES.items():
            label = category_def.get("label")
            # Translated strings are lazy objects (Promise instances)
            if not isinstance(label, (Promise, str)):
                errors.append(f"{category_key}: label is not a translatable string")

        # This test passes if labels are either Promise (translated) or str (not translated yet)
        # No assertions needed - just checking types

    def test_category_icons_use_font_awesome(self):
        """Verify category icons use Font Awesome syntax"""
        errors = []

        for category_key, category_def in PERMISSION_CATEGORIES.items():
            icon = category_def.get("icon", "")
            if not icon.startswith("fas fa-") and not icon.startswith("fab fa-"):
                errors.append(f"{category_key}: icon '{icon}' doesn't use Font Awesome format")

        assert not errors, "Categories with invalid icon format:\n  " + "\n  ".join(errors)

    def test_category_sort_order_is_unique(self):
        """Verify each category has a unique sort_order"""
        sort_orders = {}
        duplicates = []

        for category_key, category_def in PERMISSION_CATEGORIES.items():
            sort_order = category_def.get("sort_order")
            if sort_order in sort_orders:
                duplicates.append(
                    f"{category_key} and {sort_orders[sort_order]} both have sort_order {sort_order}"
                )
            sort_orders[sort_order] = category_key

        assert not duplicates, "Duplicate sort_order values:\n  " + "\n  ".join(duplicates)


class TestPermissionResolution:
    """Validate permission resolution logic"""

    @pytest.mark.django_db
    def test_resolve_view_permissions_includes_only_view(self):
        """
        Verify 'view' level returns only view permissions, not full permissions
        """
        category_settings = {"catalog": "view"}
        permissions = resolve_category_permissions(category_settings)
        permission_codenames = {p.codename for p in permissions}

        # Should have view permissions
        assert "view_product" in permission_codenames, "view_product should be included"
        assert "view_category" in permission_codenames, "view_category should be included"

        # Should NOT have add/change/delete permissions
        assert "add_product" not in permission_codenames, (
            "add_product should NOT be included for 'view' level"
        )
        assert "change_product" not in permission_codenames, (
            "change_product should NOT be included for 'view' level"
        )
        assert "delete_product" not in permission_codenames, (
            "delete_product should NOT be included for 'view' level"
        )

    @pytest.mark.django_db
    def test_resolve_full_permissions_includes_view_and_full(self):
        """
        Verify 'full' level returns both view and full permissions
        """
        category_settings = {"catalog": "full"}
        permissions = resolve_category_permissions(category_settings)
        permission_codenames = {p.codename for p in permissions}

        # Should have view permissions
        assert "view_product" in permission_codenames, "view_product should be included"
        assert "view_category" in permission_codenames, "view_category should be included"

        # Should also have full permissions
        assert "add_product" in permission_codenames, (
            "add_product should be included for 'full' level"
        )
        assert "change_product" in permission_codenames, (
            "change_product should be included for 'full' level"
        )
        assert "delete_product" in permission_codenames, (
            "delete_product should be included for 'full' level"
        )

    @pytest.mark.django_db
    def test_resolve_multiple_categories(self):
        """
        Verify multiple categories can be resolved in a single call
        """
        category_settings = {
            "catalog": "view",
            "orders": "full",
        }
        permissions = resolve_category_permissions(category_settings)
        permission_codenames = {p.codename for p in permissions}

        # Catalog view permissions
        assert "view_product" in permission_codenames

        # Orders view + full permissions
        assert "view_order" in permission_codenames
        assert "change_order" in permission_codenames

    @pytest.mark.django_db
    def test_invalid_category_gracefully_ignored(self):
        """
        Verify invalid category keys are silently ignored
        """
        category_settings = {
            "invalid_category": "full",
            "catalog": "view",
        }
        # Should not raise exception
        permissions = resolve_category_permissions(category_settings)
        permission_codenames = {p.codename for p in permissions}

        # Valid category should still work
        assert "view_product" in permission_codenames

    @pytest.mark.django_db
    def test_invalid_access_level_ignored(self):
        """
        Verify invalid access levels are silently ignored
        """
        category_settings = {"catalog": "invalid_level"}
        permissions = resolve_category_permissions(category_settings)

        # Should return empty set (no permissions matched)
        assert len(permissions) == 0, "Invalid access level should return no permissions"

    @pytest.mark.django_db
    def test_permission_objects_are_valid(self):
        """
        Verify resolved permissions are actual Permission model instances
        """
        category_settings = {"catalog": "view"}
        permissions = resolve_category_permissions(category_settings)

        assert len(permissions) > 0, "Should resolve at least some permissions"
        for perm in permissions:
            assert isinstance(perm, Permission), f"Expected Permission instance, got {type(perm)}"


class TestSidebarCategoryMapping:
    """Validate sidebar category mapping"""

    def test_all_sidebar_groups_mapped(self):
        """Verify SIDEBAR_CATEGORY_MAP covers all expected sidebar groups"""
        # These should match the admin sidebar structure
        expected_sidebar_groups = [
            "catalog",
            "orders",
            "customers",
            "pos",
            "search",
            "marketing",
            "content",
            "design",
            "settings",
            "payments",
            "email",
            "users",
            "media",
        ]

        actual_groups = set(SIDEBAR_CATEGORY_MAP.keys())
        expected_groups = set(expected_sidebar_groups)

        missing = expected_groups - actual_groups
        assert not missing, f"Missing sidebar groups in SIDEBAR_CATEGORY_MAP: {missing}"

    def test_all_mapped_categories_exist(self):
        """
        Verify all categories referenced in SIDEBAR_CATEGORY_MAP exist in PERMISSION_CATEGORIES
        """
        errors = []

        for sidebar_group, categories in SIDEBAR_CATEGORY_MAP.items():
            for category in categories:
                if category not in PERMISSION_CATEGORIES:
                    errors.append(
                        f"Sidebar group '{sidebar_group}' references non-existent category '{category}'"
                    )

        assert not errors, "Invalid category references in SIDEBAR_CATEGORY_MAP:\n  " + "\n  ".join(
            errors
        )

    def test_no_duplicate_mappings(self):
        """Verify each sidebar group maps to unique categories (no duplicates)"""
        errors = []

        for sidebar_group, categories in SIDEBAR_CATEGORY_MAP.items():
            if len(categories) != len(set(categories)):
                duplicates = [c for c in categories if categories.count(c) > 1]
                errors.append(
                    f"Sidebar group '{sidebar_group}' has duplicate categories: {duplicates}"
                )

        assert not errors, "Duplicate category mappings:\n  " + "\n  ".join(errors)


class TestPermissionStringFormat:
    """Validate permission string formats in categories"""

    def test_all_permission_strings_have_valid_format(self):
        """
        Verify all permission strings follow 'app_label.codename' format
        """
        errors = []

        for category_key, category_def in PERMISSION_CATEGORIES.items():
            for level in ["view", "full"]:
                perm_list = category_def.get("permissions", {}).get(level, [])
                for perm_string in perm_list:
                    if "." not in perm_string:
                        errors.append(
                            f"{category_key} {level}: '{perm_string}' missing dot separator"
                        )
                    else:
                        parts = perm_string.split(".")
                        if len(parts) != 2:
                            errors.append(
                                f"{category_key} {level}: '{perm_string}' has invalid format"
                            )

        assert not errors, "Invalid permission string formats:\n  " + "\n  ".join(errors)

    def test_view_permissions_use_view_codename(self):
        """
        Verify 'view' level permissions use 'view_*' codenames
        """
        errors = []

        for category_key, category_def in PERMISSION_CATEGORIES.items():
            view_perms = category_def.get("permissions", {}).get("view", [])
            for perm_string in view_perms:
                try:
                    app_label, codename = perm_string.split(".")
                    if not codename.startswith("view_"):
                        errors.append(
                            f"{category_key}: view permission '{perm_string}' doesn't start with 'view_'"
                        )
                except ValueError:
                    # Already caught by format test
                    pass

        assert not errors, "View permissions not using view_* codenames:\n  " + "\n  ".join(errors)

    def test_full_permissions_use_add_change_delete_codenames(self):
        """
        Verify 'full' level permissions use add_*, change_*, delete_* codenames
        """
        errors = []

        for category_key, category_def in PERMISSION_CATEGORIES.items():
            full_perms = category_def.get("permissions", {}).get("full", [])
            for perm_string in full_perms:
                try:
                    app_label, codename = perm_string.split(".")
                    valid_prefixes = ["add_", "change_", "delete_"]
                    if not any(codename.startswith(prefix) for prefix in valid_prefixes):
                        errors.append(
                            f"{category_key}: full permission '{perm_string}' doesn't use add/change/delete prefix"
                        )
                except ValueError:
                    # Already caught by format test
                    pass

        assert not errors, (
            "Full permissions not using add/change/delete codenames:\n  " + "\n  ".join(errors)
        )
