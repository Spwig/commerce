import json

from django.contrib import admin
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.urls import path, reverse
from django.utils.html import format_html, format_html_join
from django.utils.translation import gettext_lazy as _

from staff_roles.categories import PERMISSION_CATEGORIES
from staff_roles.models import StaffRole
from staff_roles.pos_permissions import POS_PERMISSION_FLAGS, POS_PERMISSION_GROUPS

# Unregister default Group admin - we replace it with StaffRole admin
try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass


def _is_ajax(request):
    """Check if request is an AJAX request."""
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


@admin.register(StaffRole)
class StaffRoleAdmin(admin.ModelAdmin):
    list_display = [
        "display_name_with_icon",
        "description_short",
        "access_badges",
        "member_count_display",
        "is_predefined_badge",
    ]
    list_display_links = ["display_name_with_icon"]
    ordering = ["sort_order", "display_name"]

    # We use a custom change form, so exclude most fields
    exclude = ["group", "permission_categories", "pos_permissions"]

    change_list_template = "admin/staff_roles/staffrole/change_list.html"
    change_form_template = "admin/staff_roles/staffrole/change_form.html"

    class Media:
        css = {
            "all": ["staff_roles/css/role_management.css"],
        }
        js = ["staff_roles/js/role_editor.js"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:pk>/clone/",
                self.admin_site.admin_view(self.clone_role_view),
                name="staff_roles_staffrole_clone",
            ),
            path(
                "<int:pk>/members/",
                self.admin_site.admin_view(self.members_api_view),
                name="staff_roles_staffrole_members",
            ),
            path(
                "<int:pk>/add-member/",
                self.admin_site.admin_view(self.add_member_view),
                name="staff_roles_staffrole_add_member",
            ),
            path(
                "<int:pk>/remove-member/",
                self.admin_site.admin_view(self.remove_member_view),
                name="staff_roles_staffrole_remove_member",
            ),
        ]
        return custom_urls + urls

    def display_name_with_icon(self, obj):
        return format_html(
            '<span class="role-icon-name"><i class="{}"></i> {}</span>', obj.icon, obj.display_name
        )

    display_name_with_icon.short_description = _("Role")
    display_name_with_icon.admin_order_field = "display_name"

    def description_short(self, obj):
        desc = obj.description or ""
        if len(desc) > 80:
            desc = desc[:77] + "..."
        return format_html('<span class="role-text-quiet">{}</span>', desc)

    description_short.short_description = _("Description")

    def access_badges(self, obj):
        badges = []
        if obj.can_access_admin:
            badges.append(
                ("role-access-badge role-access-badge--admin", "fas fa-desktop", str(_("Admin")))
            )
        if obj.can_access_pos:
            badges.append(
                ("role-access-badge role-access-badge--pos", "fas fa-cash-register", str(_("POS")))
            )
        if badges:
            return format_html_join(
                " ",
                '<span class="{}"><i class="{}"></i> {}</span>',
                badges,
            )
        return format_html('<span class="role-text-quiet">{}</span>', "\u2014")

    access_badges.short_description = _("Access")

    def member_count_display(self, obj):
        count = getattr(obj, "members_total", obj.member_count)
        if count == 0:
            return format_html('<span class="role-text-quiet">0</span>')
        return format_html(
            '<a href="{}?groups__id__exact={}" class="role-text-bold">{}</a>',
            reverse("admin:auth_user_changelist"),
            obj.group_id,
            count,
        )

    member_count_display.short_description = _("Members")

    def is_predefined_badge(self, obj):
        if obj.is_predefined:
            return format_html(
                '<span class="role-predefined-badge"><i class="fas fa-lock"></i> {}</span>',
                _("System"),
            )
        return ""

    is_predefined_badge.short_description = _("Type")

    def has_delete_permission(self, request, obj=None):
        if obj and obj.is_predefined:
            return False
        return super().has_delete_permission(request, obj)

    def get_changeform_initial_data(self, request):
        return {
            "icon": "fas fa-user",
            "color": "primary",
            "can_access_admin": True,
        }

    def save_model(self, request, obj, form, change):
        # Create or get the underlying Group
        if not change:
            # New role - create the Group
            group_name = f"role_{obj.display_name.lower().replace(' ', '_')}"
            group, _ = Group.objects.get_or_create(name=group_name)
            obj.group = group

        # Parse permission categories from POST data
        permission_categories = {}
        for cat_key in PERMISSION_CATEGORIES:
            level = request.POST.get(f"cat_{cat_key}", "none")
            if level in ("view", "full"):
                permission_categories[cat_key] = level
        obj.permission_categories = permission_categories

        # Parse POS permissions from POST data
        pos_permissions = {}
        for flag_key, flag_def in POS_PERMISSION_FLAGS.items():
            if flag_def.get("type") == "integer":
                try:
                    pos_permissions[flag_key] = int(request.POST.get(f"pos_{flag_key}", 0))
                except (ValueError, TypeError):
                    pos_permissions[flag_key] = 0
            else:
                pos_permissions[flag_key] = request.POST.get(f"pos_{flag_key}") == "on"
        obj.pos_permissions = pos_permissions

        super().save_model(request, obj, form, change)

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}

        # Build category data for template
        categories = []
        for key, cat in sorted(PERMISSION_CATEGORIES.items(), key=lambda x: x[1]["sort_order"]):
            categories.append(
                {
                    "key": key,
                    "label": str(cat["label"]),
                    "icon": cat["icon"],
                    "description": str(cat["description"]),
                }
            )
        extra_context["permission_categories"] = categories
        extra_context["permission_categories_json"] = json.dumps(categories)

        # Build POS permission data
        pos_flags = []
        for key, flag in POS_PERMISSION_FLAGS.items():
            pos_flags.append(
                {
                    "key": key,
                    "label": str(flag["label"]),
                    "description": str(flag["description"]),
                    "type": flag.get("type", "bool"),
                    "default": flag.get("default", False),
                    "group": flag.get("group", "general"),
                    "min": flag.get("min", 0),
                    "max": flag.get("max", 100),
                }
            )
        extra_context["pos_flags"] = pos_flags
        extra_context["pos_flags_json"] = json.dumps(pos_flags)

        pos_groups = []
        for key, grp in POS_PERMISSION_GROUPS.items():
            pos_groups.append(
                {
                    "key": key,
                    "label": str(grp["label"]),
                    "icon": grp["icon"],
                }
            )
        extra_context["pos_groups"] = pos_groups

        # Current values for existing role (passed as dicts for json_script filter)
        if object_id:
            try:
                role = StaffRole.objects.get(pk=object_id)
                extra_context["current_categories"] = role.permission_categories or {}
                extra_context["current_pos_permissions"] = role.pos_permissions or {}
                extra_context["role_members"] = role.get_members().select_related()
            except StaffRole.DoesNotExist:
                extra_context["current_categories"] = {}
                extra_context["current_pos_permissions"] = {}
        else:
            extra_context["current_categories"] = {}
            extra_context["current_pos_permissions"] = {}

        # Available staff users for member assignment
        from django.contrib.auth import get_user_model

        User = get_user_model()
        extra_context["available_staff"] = User.objects.filter(
            is_staff=True, is_active=True
        ).order_by("first_name", "last_name", "username")

        return super().changeform_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        from django.db.models import Count

        qs = super().get_queryset(request)
        return qs.annotate(members_total=Count("group__user"))

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["title"] = _("Staff Roles")
        return super().changelist_view(request, extra_context)

    def clone_role_view(self, request, pk):
        """Clone an existing role. Requires POST to prevent CSRF via GET."""
        if request.method != "POST":
            return JsonResponse({"error": "POST required"}, status=405)

        if not self.has_add_permission(request):
            return JsonResponse({"error": "Permission denied"}, status=403)

        try:
            source = StaffRole.objects.get(pk=pk)
        except StaffRole.DoesNotExist:
            from django.http import Http404

            raise Http404

        # Create new group
        base_name = f"{source.display_name} (Copy)"
        group_name = f"role_{base_name.lower().replace(' ', '_')}"
        group = Group.objects.create(name=group_name)

        # Clone the role
        new_role = StaffRole.objects.create(
            group=group,
            display_name=base_name,
            description=source.description,
            icon=source.icon,
            color=source.color,
            is_predefined=False,
            permission_categories=source.permission_categories,
            pos_permissions=source.pos_permissions,
            can_access_admin=source.can_access_admin,
            can_access_pos=source.can_access_pos,
            sort_order=source.sort_order + 1,
        )

        from django.contrib import messages

        messages.success(request, _('Role "%(name)s" cloned successfully.') % {"name": base_name})
        from django.shortcuts import redirect

        return redirect(reverse("admin:staff_roles_staffrole_change", args=[new_role.pk]))

    def members_api_view(self, request, pk):
        """Get members of a role as JSON."""
        if not _is_ajax(request):
            return JsonResponse({"error": "Invalid request"}, status=400)

        try:
            role = StaffRole.objects.get(pk=pk)
        except StaffRole.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        members = []
        for user in role.get_members():
            members.append(
                {
                    "id": user.id,
                    "username": user.username,
                    "full_name": user.get_full_name(),
                    "email": user.email,
                }
            )
        return JsonResponse({"members": members})

    def add_member_view(self, request, pk):
        """Add a user to a role."""
        if request.method != "POST":
            return JsonResponse({"error": "POST required"}, status=405)

        if not _is_ajax(request):
            return JsonResponse({"error": "Invalid request"}, status=400)

        if not self.has_change_permission(request):
            return JsonResponse({"error": "Permission denied"}, status=403)

        try:
            role = StaffRole.objects.get(pk=pk)
        except StaffRole.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        user_id = request.POST.get("user_id")
        if not user_id:
            return JsonResponse({"error": "user_id required"}, status=400)

        from django.contrib.auth import get_user_model

        User = get_user_model()
        try:
            user = User.objects.get(pk=user_id, is_staff=True)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        role.group.user_set.add(user)

        # Invalidate cache
        from staff_roles.services import invalidate_user_cache

        invalidate_user_cache(user)

        return JsonResponse({"success": True})

    def remove_member_view(self, request, pk):
        """Remove a user from a role."""
        if request.method != "POST":
            return JsonResponse({"error": "POST required"}, status=405)

        if not _is_ajax(request):
            return JsonResponse({"error": "Invalid request"}, status=400)

        if not self.has_change_permission(request):
            return JsonResponse({"error": "Permission denied"}, status=403)

        try:
            role = StaffRole.objects.get(pk=pk)
        except StaffRole.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        user_id = request.POST.get("user_id")
        if not user_id:
            return JsonResponse({"error": "user_id required"}, status=400)

        from django.contrib.auth import get_user_model

        User = get_user_model()
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        role.group.user_set.remove(user)

        # Invalidate cache
        from staff_roles.services import invalidate_user_cache

        invalidate_user_cache(user)

        return JsonResponse({"success": True})
