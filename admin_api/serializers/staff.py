"""
Staff & Role Serializers for Admin API

Serializers for staff member management, role CRUD, and permission listing.
"""
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class StaffMemberListSerializer(serializers.Serializer):
    """Serializer for staff member in list view."""
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_owner = serializers.SerializerMethodField()
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    groups = serializers.SerializerMethodField()
    permissions_summary = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        return obj.is_superuser

    def get_groups(self, obj):
        from staff_roles.services import get_user_roles
        roles = get_user_roles(obj)
        return [{'id': role.id, 'name': role.display_name} for role in roles]

    def get_permissions_summary(self, obj):
        from staff_roles.services import get_user_roles
        roles = get_user_roles(obj)
        modules = set()
        total = 0
        for role in roles:
            for category_key, level in role.permission_categories.items():
                if level in ('view', 'full'):
                    modules.add(category_key)
                    total += 1
        return {
            'total_permissions': total,
            'modules': sorted(modules),
        }


class StaffMemberDetailSerializer(StaffMemberListSerializer):
    """Serializer for staff member detail view (includes full permissions)."""
    permissions = serializers.SerializerMethodField()

    def get_permissions(self, obj):
        if obj.is_superuser:
            from staff_roles.categories import PERMISSION_CATEGORIES
            return {key: 'full' for key in PERMISSION_CATEGORIES}
        from staff_roles.services import get_user_roles
        merged = {}
        for role in get_user_roles(obj):
            for category_key, level in role.permission_categories.items():
                current = merged.get(category_key, 'none')
                if level == 'full' or (level == 'view' and current == 'none'):
                    merged[category_key] = level
        return merged


class StaffInviteSerializer(serializers.Serializer):
    """Serializer for staff invitation request."""
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150)
    group_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        min_length=1,
        help_text=_('List of StaffRole IDs to assign')
    )


class StaffUpdateSerializer(serializers.Serializer):
    """Serializer for updating a staff member."""
    group_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text=_('Replace all role assignments')
    )
    is_active = serializers.BooleanField(required=False)
    first_name = serializers.CharField(required=False, max_length=150)
    last_name = serializers.CharField(required=False, max_length=150)


class StaffRoleListSerializer(serializers.Serializer):
    """Serializer for role in list view."""
    id = serializers.IntegerField(read_only=True)
    name = serializers.SerializerMethodField()
    is_built_in = serializers.SerializerMethodField()
    staff_count = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    description = serializers.CharField(read_only=True)

    def get_name(self, obj):
        return obj.display_name

    def get_is_built_in(self, obj):
        return obj.is_predefined

    def get_staff_count(self, obj):
        return obj.member_count

    def get_permissions(self, obj):
        return obj.permission_categories


class RoleCreateSerializer(serializers.Serializer):
    """Serializer for creating a custom role."""
    name = serializers.CharField(required=True, max_length=100)
    description = serializers.CharField(required=False, default='', allow_blank=True)
    permissions = serializers.DictField(
        required=True,
        help_text=_('Permission categories dict: {"catalog": "full", "orders": "view"}')
    )

    def validate_permissions(self, value):
        from staff_roles.categories import PERMISSION_CATEGORIES
        valid_keys = set(PERMISSION_CATEGORIES.keys())
        valid_levels = {'none', 'view', 'full'}
        for key, level in value.items():
            if key not in valid_keys:
                raise serializers.ValidationError(
                    f"Unknown permission category: {key}. Valid: {sorted(valid_keys)}"
                )
            if level not in valid_levels:
                raise serializers.ValidationError(
                    f"Invalid access level '{level}' for {key}. Valid: {sorted(valid_levels)}"
                )
        return value


class RoleUpdateSerializer(serializers.Serializer):
    """Serializer for updating a custom role."""
    name = serializers.CharField(required=False, max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
    permissions = serializers.DictField(
        required=False,
        help_text=_('Full replacement of permission categories')
    )

    def validate_permissions(self, value):
        from staff_roles.categories import PERMISSION_CATEGORIES
        valid_keys = set(PERMISSION_CATEGORIES.keys())
        valid_levels = {'none', 'view', 'full'}
        for key, level in value.items():
            if key not in valid_keys:
                raise serializers.ValidationError(
                    f"Unknown permission category: {key}. Valid: {sorted(valid_keys)}"
                )
            if level not in valid_levels:
                raise serializers.ValidationError(
                    f"Invalid access level '{level}' for {key}. Valid: {sorted(valid_levels)}"
                )
        return value
