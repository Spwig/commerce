"""
Staff & Role Serializers for Admin API

Serializers for staff member management, role CRUD, and permission listing.
"""

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


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

    def _get_roles(self, obj):
        """Return the user's StaffRole objects without a per-user role query.

        Resolution order, each avoiding an N+1 when serializing a page of
        staff members:

        1. A page-level bulk role map supplied by the view via the
           ``roles_by_user`` context (built with
           ``staff_roles.services.get_roles_for_users``).
        2. A ``groups__staff_role`` prefetch on the object, reused directly.
        3. The cached ``get_user_roles`` lookup, for callers that pass an
           unprefetched user (e.g. ``staff_update``).
        """
        roles_by_user = self.context.get("roles_by_user")
        if roles_by_user is not None:
            return roles_by_user.get(obj.pk, [])

        prefetched = getattr(obj, "_prefetched_objects_cache", None)
        if prefetched is not None and "groups" in prefetched:
            roles = [group.staff_role for group in obj.groups.all() if hasattr(group, "staff_role")]
            # Preserve StaffRole.Meta.ordering (sort_order, display_name); the
            # prefetched groups come back in the Group relation's order.
            roles.sort(key=lambda role: (role.sort_order, role.display_name))
            return roles

        if not hasattr(obj, "_cached_staff_roles"):
            from staff_roles.services import get_user_roles

            obj._cached_staff_roles = list(get_user_roles(obj))
        return obj._cached_staff_roles

    def get_groups(self, obj):
        roles = self._get_roles(obj)
        return [{"id": role.id, "name": role.display_name} for role in roles]

    def get_permissions_summary(self, obj):
        roles = self._get_roles(obj)
        modules = set()
        total = 0
        for role in roles:
            for category_key, level in role.permission_categories.items():
                if level in ("view", "full"):
                    modules.add(category_key)
                    total += 1
        return {
            "total_permissions": total,
            "modules": sorted(modules),
        }


class StaffMemberDetailSerializer(StaffMemberListSerializer):
    """Serializer for staff member detail view (includes full permissions)."""

    permissions = serializers.SerializerMethodField()

    def get_permissions(self, obj):
        if obj.is_superuser:
            from staff_roles.categories import PERMISSION_CATEGORIES

            return dict.fromkeys(PERMISSION_CATEGORIES, "full")
        from staff_roles.services import get_user_roles

        merged = {}
        for role in get_user_roles(obj):
            for category_key, level in role.permission_categories.items():
                current = merged.get(category_key, "none")
                if level == "full" or (level == "view" and current == "none"):
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
        help_text=_("List of StaffRole IDs to assign"),
    )


class StaffUpdateSerializer(serializers.Serializer):
    """Serializer for updating a staff member."""

    group_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text=_("Replace all role assignments"),
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
        # Prefer the ``member_count_annotated`` annotation set by the role-list
        # queryset so serializing a page of roles issues no per-role COUNT
        # queries; fall back to ``member_count`` for callers that pass an
        # unannotated role.
        annotated = getattr(obj, "member_count_annotated", None)
        if annotated is not None:
            return annotated
        return obj.member_count

    def get_permissions(self, obj):
        return obj.permission_categories


class RoleCreateSerializer(serializers.Serializer):
    """Serializer for creating a custom role."""

    name = serializers.CharField(required=True, max_length=100)
    description = serializers.CharField(required=False, default="", allow_blank=True)
    permissions = serializers.DictField(
        required=True,
        help_text=_('Permission categories dict: {"catalog": "full", "orders": "view"}'),
    )

    def validate_permissions(self, value):
        from staff_roles.categories import PERMISSION_CATEGORIES

        valid_keys = set(PERMISSION_CATEGORIES.keys())
        valid_levels = {"none", "view", "full"}
        for key, level in value.items():
            if key not in valid_keys:
                raise serializers.ValidationError(
                    f"Unknown permission category: {key}. Valid: {sorted(valid_keys)}"
                )
            if not isinstance(level, str) or level not in valid_levels:
                raise serializers.ValidationError(
                    f"Invalid access level '{level}' for {key}. Valid: {sorted(valid_levels)}"
                )
        return value


class RoleUpdateSerializer(serializers.Serializer):
    """Serializer for updating a custom role."""

    name = serializers.CharField(required=False, max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
    permissions = serializers.DictField(
        required=False, help_text=_("Full replacement of permission categories")
    )

    def validate_permissions(self, value):
        from staff_roles.categories import PERMISSION_CATEGORIES

        valid_keys = set(PERMISSION_CATEGORIES.keys())
        valid_levels = {"none", "view", "full"}
        for key, level in value.items():
            if key not in valid_keys:
                raise serializers.ValidationError(
                    f"Unknown permission category: {key}. Valid: {sorted(valid_keys)}"
                )
            if not isinstance(level, str) or level not in valid_levels:
                raise serializers.ValidationError(
                    f"Invalid access level '{level}' for {key}. Valid: {sorted(valid_levels)}"
                )
        return value
