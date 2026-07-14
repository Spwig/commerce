"""
Role Merging Logic Tests

Validates role permission merging when a user has multiple roles:
- OR logic for boolean POS permissions (any role grants → granted)
- MAX logic for integer POS permissions (take highest value)
- Django permission resolution from multiple groups
- Cache invalidation
"""

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from staff_roles.models import StaffRole
from staff_roles.services import (
    _get_merged_pos_permissions,
    can_access_admin,
    can_access_pos,
    get_pos_permission,
    get_user_pos_permissions_summary,
    invalidate_user_cache,
)

User = get_user_model()


pytestmark = [pytest.mark.django_db, pytest.mark.integrity]


@pytest.fixture
def test_user():
    """Create a test user"""
    user = User.objects.create_user(
        username="test_staff",
        email="test@example.com",
        password="testpass123",
        is_staff=True,
    )
    return user


@pytest.fixture
def role_cashier(test_user):
    """Create a cashier role with basic POS permissions"""
    group = Group.objects.create(name="Cashier")
    role = StaffRole.objects.create(
        group=group,
        display_name="Cashier",
        is_predefined=True,
        can_access_pos=True,
        pos_permissions={
            "pos_access": True,
            "pos_gift_card_balance": True,
            "pos_discount_manual": False,
            "pos_discount_max_percent": 5,  # Can discount up to 5%
            "pos_refund": False,
        },
    )
    test_user.groups.add(group)
    return role


@pytest.fixture
def role_supervisor(test_user):
    """Create a supervisor role with elevated POS permissions"""
    group = Group.objects.create(name="Supervisor")
    role = StaffRole.objects.create(
        group=group,
        display_name="Supervisor",
        is_predefined=True,
        can_access_pos=True,
        can_access_admin=True,
        pos_permissions={
            "pos_access": True,
            "pos_discount_manual": True,  # CAN apply manual discounts
            "pos_discount_max_percent": 20,  # Can discount up to 20%
            "pos_refund": True,  # CAN process refunds
            "pos_close_shift": True,
        },
    )
    test_user.groups.add(group)
    return role


class TestBooleanORLogic:
    """Validate OR logic for boolean POS permissions"""

    def test_single_role_boolean_permission(self, test_user, role_cashier):
        """
        Verify single role's boolean permissions are returned correctly
        """
        # Cashier has pos_access=True
        assert get_pos_permission(test_user, "pos_access") is True

        # Cashier has pos_refund=False
        assert get_pos_permission(test_user, "pos_refund") is False

    def test_multiple_roles_or_logic_grants_permission(
        self, test_user, role_cashier, role_supervisor
    ):
        """
        Verify OR logic: if ANY role grants boolean permission, it's granted
        """
        # Cashier: pos_refund=False, Supervisor: pos_refund=True
        # Result should be True (OR logic)
        assert get_pos_permission(test_user, "pos_refund") is True

        # Both have pos_access=True
        assert get_pos_permission(test_user, "pos_access") is True

    def test_multiple_roles_all_false_results_false(self, test_user):
        """
        Verify OR logic: if ALL roles deny permission, it's denied
        """
        # Create two roles both denying pos_refund
        group1 = Group.objects.create(name="Role1")
        role1 = StaffRole.objects.create(
            group=group1, display_name="Role 1", pos_permissions={"pos_refund": False}
        )
        test_user.groups.add(group1)

        group2 = Group.objects.create(name="Role2")
        role2 = StaffRole.objects.create(
            group=group2, display_name="Role 2", pos_permissions={"pos_refund": False}
        )
        test_user.groups.add(group2)

        # Both deny → result is False
        assert get_pos_permission(test_user, "pos_refund") is False

    def test_explicit_false_overrides_missing_key(self, test_user):
        """
        Verify that explicit False is different from missing key
        """
        group1 = Group.objects.create(name="RoleWithoutKey")
        role1 = StaffRole.objects.create(
            group=group1,
            display_name="Role Without Key",
            pos_permissions={},  # pos_refund not defined
        )
        test_user.groups.add(group1)

        group2 = Group.objects.create(name="RoleWithTrue")
        role2 = StaffRole.objects.create(
            group=group2, display_name="Role With True", pos_permissions={"pos_refund": True}
        )
        test_user.groups.add(group2)

        # One role grants → should be True
        assert get_pos_permission(test_user, "pos_refund") is True


class TestIntegerMAXLogic:
    """Validate MAX logic for integer POS permissions"""

    def test_single_role_integer_permission(self, test_user, role_cashier):
        """
        Verify single role's integer permissions are returned correctly
        """
        # Cashier has pos_discount_max_percent=5
        assert get_pos_permission(test_user, "pos_discount_max_percent") == 5

    def test_multiple_roles_max_logic_takes_highest(self, test_user, role_cashier, role_supervisor):
        """
        Verify MAX logic: take the highest value across all roles
        """
        # Cashier: 5%, Supervisor: 20%
        # Result should be 20% (MAX logic)
        assert get_pos_permission(test_user, "pos_discount_max_percent") == 20

    def test_three_roles_max_logic(self, test_user):
        """
        Verify MAX logic works with more than 2 roles
        """
        # Create three roles with different discount limits
        for i, percent in enumerate([10, 25, 15]):
            group = Group.objects.create(name=f"Role{i}")
            role = StaffRole.objects.create(
                group=group,
                display_name=f"Role {i}",
                pos_permissions={"pos_discount_max_percent": percent},
            )
            test_user.groups.add(group)

        # Should take max: 25
        assert get_pos_permission(test_user, "pos_discount_max_percent") == 25

    def test_integer_permission_with_zero_values(self, test_user):
        """
        Verify MAX logic handles zero values correctly
        """
        group1 = Group.objects.create(name="NoDiscount")
        role1 = StaffRole.objects.create(
            group=group1,
            display_name="No Discount",
            pos_permissions={"pos_discount_max_percent": 0},
        )
        test_user.groups.add(group1)

        group2 = Group.objects.create(name="SomeDiscount")
        role2 = StaffRole.objects.create(
            group=group2,
            display_name="Some Discount",
            pos_permissions={"pos_discount_max_percent": 10},
        )
        test_user.groups.add(group2)

        # max(0, 10) = 10
        assert get_pos_permission(test_user, "pos_discount_max_percent") == 10


class TestSuperuserPermissions:
    """Validate superuser always has all permissions"""

    def test_superuser_has_all_boolean_permissions(self, test_user):
        """Verify superuser gets True for all boolean POS permissions"""
        test_user.is_superuser = True
        test_user.save()

        # No roles assigned, but superuser should have all permissions
        assert get_pos_permission(test_user, "pos_access") is True
        assert get_pos_permission(test_user, "pos_refund") is True
        assert get_pos_permission(test_user, "pos_void") is True
        assert get_pos_permission(test_user, "pos_close_shift") is True

    def test_superuser_gets_max_integer_permissions(self, test_user):
        """Verify superuser gets maximum value for integer POS permissions"""
        test_user.is_superuser = True
        test_user.save()

        # Should get 100 (the max from POS_PERMISSION_FLAGS)
        assert get_pos_permission(test_user, "pos_discount_max_percent") == 100

    def test_superuser_summary_includes_all_permissions(self, test_user):
        """Verify permissions summary for superuser includes all flags"""
        test_user.is_superuser = True
        test_user.save()

        summary = get_user_pos_permissions_summary(test_user)

        # Should have all POS permission flags
        from staff_roles.pos_permissions import POS_PERMISSION_FLAGS

        for flag_key in POS_PERMISSION_FLAGS:
            assert flag_key in summary, f"Superuser summary missing {flag_key}"


class TestPermissionCaching:
    """Validate permission caching and invalidation"""

    def test_permissions_are_cached(self, test_user, role_cashier):
        """Verify permissions are cached after first access"""
        # First access
        result1 = get_pos_permission(test_user, "pos_access")

        # Modify role permissions directly (bypassing cache)
        role_cashier.pos_permissions["pos_access"] = False
        role_cashier.save()

        # Second access should return cached value (still True)
        result2 = get_pos_permission(test_user, "pos_access")
        assert result2 is True, "Cache should still return old value"

    def test_cache_invalidation_updates_permissions(self, test_user, role_cashier):
        """Verify cache invalidation causes permissions to be re-evaluated"""
        # First access
        result1 = get_pos_permission(test_user, "pos_access")
        assert result1 is True

        # Modify role permissions
        role_cashier.pos_permissions["pos_access"] = False
        role_cashier.save()

        # Invalidate cache
        invalidate_user_cache(test_user)

        # Now should get new value
        result2 = get_pos_permission(test_user, "pos_access")
        assert result2 is False, "After cache invalidation, should get updated value"

    def test_merged_permissions_cached(self, test_user, role_cashier, role_supervisor):
        """Verify _get_merged_pos_permissions uses cache"""
        # First call
        perms1 = _get_merged_pos_permissions(test_user)

        # Second call should be identical (from cache)
        perms2 = _get_merged_pos_permissions(test_user)

        assert perms1 == perms2


class TestAdminAndPOSAccess:
    """Validate can_access_admin and can_access_pos functions"""

    def test_can_access_admin_with_explicit_permission(self, test_user, role_supervisor):
        """Verify can_access_admin returns True when role grants it"""
        # Supervisor has can_access_admin=True
        assert can_access_admin(test_user) is True

    def test_can_access_admin_denied_without_permission(self, test_user):
        """Verify can_access_admin returns False when no role grants it"""
        group = Group.objects.create(name="NoAdminAccess")
        role = StaffRole.objects.create(
            group=group,
            display_name="No Admin Access",
            can_access_admin=False,
        )
        test_user.groups.add(group)

        assert can_access_admin(test_user) is False

    def test_can_access_admin_or_logic(self, test_user):
        """Verify can_access_admin uses OR logic across roles"""
        # Role 1: denies admin access
        group1 = Group.objects.create(name="Role1")
        role1 = StaffRole.objects.create(
            group=group1,
            display_name="Role 1",
            can_access_admin=False,
        )
        test_user.groups.add(group1)

        # Role 2: grants admin access
        group2 = Group.objects.create(name="Role2")
        role2 = StaffRole.objects.create(
            group=group2,
            display_name="Role 2",
            can_access_admin=True,
        )
        test_user.groups.add(group2)

        # Should be True (OR logic)
        assert can_access_admin(test_user) is True

    def test_can_access_pos_with_explicit_permission(self, test_user, role_cashier):
        """Verify can_access_pos returns True when role grants it"""
        # Cashier has can_access_pos=True
        assert can_access_pos(test_user) is True

    def test_can_access_pos_denied_without_permission(self, test_user):
        """Verify can_access_pos returns False when no role grants it"""
        group = Group.objects.create(name="NoPOSAccess")
        role = StaffRole.objects.create(
            group=group,
            display_name="No POS Access",
            can_access_pos=False,
        )
        test_user.groups.add(group)

        assert can_access_pos(test_user) is False

    def test_superuser_can_access_both(self, test_user):
        """Verify superuser can access both admin and POS"""
        test_user.is_superuser = True
        test_user.save()

        assert can_access_admin(test_user) is True
        assert can_access_pos(test_user) is True

    def test_staff_with_no_roles_gets_admin_access(self, test_user):
        """
        Verify staff users with no roles get admin access (backwards compatibility)
        """
        test_user.is_staff = True
        test_user.save()

        # No roles assigned, but is_staff=True
        assert can_access_admin(test_user) is True


class TestDefaultPermissions:
    """Validate default permission values from POS_PERMISSION_FLAGS"""

    def test_undefined_permission_uses_default(self, test_user):
        """
        Verify permissions not defined in any role use flag default
        """
        group = Group.objects.create(name="MinimalRole")
        role = StaffRole.objects.create(
            group=group,
            display_name="Minimal Role",
            pos_permissions={},  # No permissions defined
        )
        test_user.groups.add(group)

        # pos_gift_card_balance defaults to True
        assert get_pos_permission(test_user, "pos_gift_card_balance") is True

        # pos_refund defaults to False
        assert get_pos_permission(test_user, "pos_refund") is False

        # pos_discount_max_percent defaults to 0
        assert get_pos_permission(test_user, "pos_discount_max_percent") == 0

    def test_partial_permission_set_uses_defaults_for_missing(self, test_user):
        """
        Verify roles with partial pos_permissions use defaults for missing keys
        """
        group = Group.objects.create(name="PartialRole")
        role = StaffRole.objects.create(
            group=group,
            display_name="Partial Role",
            pos_permissions={
                "pos_refund": True,  # Only this one defined
            },
        )
        test_user.groups.add(group)

        # Defined permission
        assert get_pos_permission(test_user, "pos_refund") is True

        # Undefined permissions should use defaults
        assert get_pos_permission(test_user, "pos_void") is False  # default False
        assert get_pos_permission(test_user, "pos_gift_card_balance") is True  # default True
