"""
Admin views for Custom Fields management page.

Provides a centralized interface for merchants to create, edit,
and manage custom field definitions across all supported models.
Includes recycle bin for deleted groups and fields.
"""

import json

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods, require_POST

from .models import (
    SUPPORTED_MODELS,
    CustomFieldDefinition,
    CustomFieldGroup,
)


def _is_ajax(request):
    """Check if request is an AJAX request."""
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


def _ajax_required(view_func):
    """Decorator to require AJAX requests for API endpoints."""

    def wrapper(request, *args, **kwargs):
        if not _is_ajax(request):
            return JsonResponse({"error": "Invalid request"}, status=400)
        return view_func(request, *args, **kwargs)

    wrapper.__name__ = view_func.__name__
    wrapper.__doc__ = view_func.__doc__
    return wrapper


@staff_member_required
def management_view(request):
    """
    Main custom fields management page.

    Displays all field definitions grouped by model with tabs.
    Supports CRUD operations via AJAX.
    """
    # Build model tabs with their content types
    model_tabs = []
    for model_ref in SUPPORTED_MODELS:
        app_label, model_name = model_ref.split(".")
        try:
            ct = ContentType.objects.get(app_label=app_label, model=model_name)
            model_class = ct.model_class()
            if model_class:
                groups = (
                    CustomFieldGroup.objects.filter(content_type=ct, is_active=True)
                    .prefetch_related("fields")
                    .order_by("sort_order")
                )

                model_tabs.append(
                    {
                        "id": model_ref.replace(".", "_"),
                        "content_type_id": ct.pk,
                        "label": model_class._meta.verbose_name_plural.title(),
                        "app_label": app_label,
                        "model_name": model_name,
                        "groups": groups,
                        "field_count": CustomFieldDefinition.objects.filter(
                            content_type=ct, is_active=True
                        ).count(),
                    }
                )
        except ContentType.DoesNotExist:
            pass

    # Count deleted items for recycle bin badge
    deleted_count = (
        CustomFieldGroup.all_objects.filter(is_deleted=True).count()
        + CustomFieldDefinition.all_objects.filter(is_deleted=True).count()
    )

    field_type_choices = CustomFieldDefinition.FIELD_TYPES

    context = {
        "title": _("Custom Fields"),
        "model_tabs": model_tabs,
        "field_type_choices": field_type_choices,
        "deleted_count": deleted_count,
        "has_permission": True,
        "site_title": "Spwig",
        "site_header": "Spwig",
    }
    return render(request, "admin/custom_fields/management.html", context)


@staff_member_required
def recycle_bin_view(request):
    """
    Recycle bin page showing deleted custom field groups and definitions.
    """
    deleted_groups = (
        CustomFieldGroup.all_objects.filter(is_deleted=True)
        .select_related("content_type")
        .order_by("-deleted_at")
    )

    deleted_fields = (
        CustomFieldDefinition.all_objects.filter(is_deleted=True)
        .select_related("group", "content_type")
        .order_by("-deleted_at")
    )

    context = {
        "title": _("Custom Fields - Recycle Bin"),
        "deleted_groups": deleted_groups,
        "deleted_fields": deleted_fields,
        "has_permission": True,
        "site_title": "Spwig",
        "site_header": "Spwig",
    }
    return render(request, "admin/custom_fields/recycle_bin.html", context)


@staff_member_required
@require_POST
@_ajax_required
def create_group(request):
    """Create a new custom field group via AJAX."""
    try:
        data = json.loads(request.body)
        ct = ContentType.objects.get(pk=data["content_type_id"])

        group = CustomFieldGroup.objects.create(
            name=data["name"],
            content_type=ct,
            show_on_storefront=data.get("show_on_storefront", False),
        )

        return JsonResponse(
            {
                "success": True,
                "group": {
                    "id": group.pk,
                    "name": group.name,
                    "slug": group.slug,
                    "sort_order": group.sort_order,
                    "show_on_storefront": group.show_on_storefront,
                },
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@staff_member_required
@require_POST
@_ajax_required
def update_group(request, group_id):
    """Update a custom field group via AJAX."""
    try:
        data = json.loads(request.body)
        group = CustomFieldGroup.objects.get(pk=group_id)

        if "name" in data:
            group.name = data["name"]
        if "sort_order" in data:
            group.sort_order = data["sort_order"]
        if "show_on_storefront" in data:
            group.show_on_storefront = data["show_on_storefront"]
        if "is_active" in data:
            group.is_active = data["is_active"]

        group.save()

        return JsonResponse({"success": True})
    except CustomFieldGroup.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Group not found")}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@staff_member_required
@require_POST
@_ajax_required
def delete_group(request, group_id):
    """Soft-delete a group via recycle bin (SoftDeleteModel)."""
    try:
        group = CustomFieldGroup.objects.get(pk=group_id)
        # Soft-delete the group using SoftDeleteModel
        group.delete(user=request.user)
        # Also soft-delete all fields in this group
        for field_def in group.fields.all():
            field_def.delete(user=request.user)
        return JsonResponse({"success": True})
    except CustomFieldGroup.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Group not found")}, status=404)


@staff_member_required
@require_POST
@_ajax_required
def create_field(request):
    """Create a new custom field definition via AJAX."""
    try:
        data = json.loads(request.body)
        group = CustomFieldGroup.objects.get(pk=data["group_id"])

        # Build validation config
        validation_config = data.get("validation_config", {})
        if not validation_config:
            # Legacy format: build from flat keys
            if data.get("field_type") in ("text", "textarea"):
                if data.get("max_length"):
                    validation_config["max_length"] = int(data["max_length"])
                if data.get("min_length"):
                    validation_config["min_length"] = int(data["min_length"])
                if data.get("regex"):
                    validation_config["regex"] = data["regex"]
            elif data.get("field_type") in ("number", "decimal"):
                if data.get("min") is not None and data.get("min") != "":
                    validation_config["min"] = float(data["min"])
                if data.get("max") is not None and data.get("max") != "":
                    validation_config["max"] = float(data["max"])
                if data.get("field_type") == "decimal" and data.get("decimal_places"):
                    validation_config["decimal_places"] = int(data["decimal_places"])
            elif data.get("field_type") in ("select", "multiselect"):
                if data.get("choices"):
                    validation_config["choices"] = data["choices"]

        # Parse default value
        default_value = data.get("default_value")
        if default_value == "":
            default_value = None

        field_def = CustomFieldDefinition.objects.create(
            group=group,
            content_type=group.content_type,
            name=data["name"],
            field_type=data["field_type"],
            help_text_value=data.get("help_text", ""),
            default_value=default_value,
            validation_config=validation_config,
            is_required=data.get("is_required", False),
            show_on_storefront=data.get("show_on_storefront", False),
            is_translatable=data.get("is_translatable", False),
        )

        return JsonResponse(
            {
                "success": True,
                "field": {
                    "id": field_def.pk,
                    "name": field_def.name,
                    "slug": field_def.slug,
                    "field_type": field_def.field_type,
                    "field_type_display": field_def.get_field_type_display(),
                    "is_required": field_def.is_required,
                    "show_on_storefront": field_def.show_on_storefront,
                    "is_translatable": field_def.is_translatable,
                    "help_text": field_def.help_text_value,
                },
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@staff_member_required
@require_POST
@_ajax_required
def update_field(request, field_id):
    """Update a custom field definition via AJAX."""
    try:
        data = json.loads(request.body)
        field_def = CustomFieldDefinition.objects.get(pk=field_id)

        if "name" in data:
            field_def.name = data["name"]
        if "help_text" in data:
            field_def.help_text_value = data["help_text"]
        if "is_required" in data:
            field_def.is_required = data["is_required"]
        if "show_on_storefront" in data:
            field_def.show_on_storefront = data["show_on_storefront"]
        if "is_translatable" in data:
            field_def.is_translatable = data["is_translatable"]
        if "sort_order" in data:
            field_def.sort_order = data["sort_order"]
        if "default_value" in data:
            field_def.default_value = data["default_value"] if data["default_value"] != "" else None
        if "is_active" in data:
            field_def.is_active = data["is_active"]

        # Update validation config
        if "validation_config" in data:
            field_def.validation_config = data["validation_config"]

        field_def.save()

        return JsonResponse({"success": True})
    except CustomFieldDefinition.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Field not found")}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@staff_member_required
@require_POST
@_ajax_required
def delete_field(request, field_id):
    """Soft-delete a field definition via recycle bin (SoftDeleteModel)."""
    try:
        field_def = CustomFieldDefinition.objects.get(pk=field_id)
        field_def.delete(user=request.user)
        return JsonResponse({"success": True})
    except CustomFieldDefinition.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Field not found")}, status=404)


@staff_member_required
@require_http_methods(["GET"])
@_ajax_required
def get_field_detail(request, field_id):
    """Get full details of a field definition for the edit modal."""
    try:
        field_def = CustomFieldDefinition.objects.select_related("group").get(pk=field_id)
        return JsonResponse(
            {
                "success": True,
                "field": {
                    "id": field_def.pk,
                    "name": field_def.name,
                    "slug": field_def.slug,
                    "field_type": field_def.field_type,
                    "field_type_display": field_def.get_field_type_display(),
                    "help_text": field_def.help_text_value,
                    "default_value": field_def.default_value,
                    "validation_config": field_def.validation_config,
                    "is_required": field_def.is_required,
                    "show_on_storefront": field_def.show_on_storefront,
                    "is_translatable": field_def.is_translatable,
                    "sort_order": field_def.sort_order,
                    "group_id": field_def.group_id,
                },
            }
        )
    except CustomFieldDefinition.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Field not found")}, status=404)


@staff_member_required
@require_POST
@_ajax_required
def reorder_fields(request):
    """Update sort order for multiple fields at once."""
    try:
        data = json.loads(request.body)
        for item in data.get("fields", []):
            CustomFieldDefinition.objects.filter(pk=item["id"]).update(
                sort_order=item["sort_order"]
            )
        # Invalidate cache
        if data.get("content_type_id"):
            ct = ContentType.objects.get(pk=data["content_type_id"])
            CustomFieldDefinition.invalidate_cache(ct)
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


# ═══════════════════════════════════════════
# Recycle Bin Actions
# ═══════════════════════════════════════════


@staff_member_required
@require_POST
@_ajax_required
def restore_group(request, group_id):
    """Restore a soft-deleted group from the recycle bin."""
    try:
        group = CustomFieldGroup.all_objects.get(pk=group_id, is_deleted=True)
        group.restore()
        # Also restore fields that were deleted with this group
        for field_def in CustomFieldDefinition.all_objects.filter(group=group, is_deleted=True):
            field_def.restore()
        # Invalidate cache
        CustomFieldDefinition.invalidate_cache(group.content_type)
        return JsonResponse({"success": True})
    except CustomFieldGroup.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Group not found")}, status=404)


@staff_member_required
@require_POST
@_ajax_required
def restore_field(request, field_id):
    """Restore a soft-deleted field from the recycle bin."""
    try:
        field_def = CustomFieldDefinition.all_objects.get(pk=field_id, is_deleted=True)
        field_def.restore()
        CustomFieldDefinition.invalidate_cache(field_def.content_type)
        return JsonResponse({"success": True})
    except CustomFieldDefinition.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Field not found")}, status=404)


@staff_member_required
@require_POST
@_ajax_required
def permanent_delete_group(request, group_id):
    """Permanently delete a group from the recycle bin."""
    try:
        group = CustomFieldGroup.all_objects.get(pk=group_id, is_deleted=True)
        ct = group.content_type
        # Permanently delete all fields in this group first
        for field_def in CustomFieldDefinition.all_objects.filter(group=group):
            field_def.hard_delete()
        group.hard_delete()
        CustomFieldDefinition.invalidate_cache(ct)
        return JsonResponse({"success": True})
    except CustomFieldGroup.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Group not found")}, status=404)


@staff_member_required
@require_POST
@_ajax_required
def permanent_delete_field(request, field_id):
    """Permanently delete a field from the recycle bin."""
    try:
        field_def = CustomFieldDefinition.all_objects.get(pk=field_id, is_deleted=True)
        ct = field_def.content_type
        field_def.hard_delete()
        CustomFieldDefinition.invalidate_cache(ct)
        return JsonResponse({"success": True})
    except CustomFieldDefinition.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Field not found")}, status=404)
