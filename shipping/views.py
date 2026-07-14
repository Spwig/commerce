import json

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from .models import CarrierPreset


@staff_member_required
@require_POST
def toggle_carrier_active(request, carrier_id):
    """Toggle carrier active status via AJAX"""
    try:
        carrier = get_object_or_404(CarrierPreset, id=carrier_id)

        # Toggle active status
        carrier.is_active = not carrier.is_active
        carrier.save()

        return JsonResponse(
            {
                "success": True,
                "is_active": carrier.is_active,
                "message": _("Carrier {} successfully").format(
                    _("enabled") if carrier.is_active else _("disabled")
                ),
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)


@staff_member_required
@require_POST
def set_carrier_default(request, carrier_id):
    """Set carrier as default via AJAX"""
    try:
        carrier = get_object_or_404(CarrierPreset, id=carrier_id)

        # Remove default from all other carriers
        CarrierPreset.objects.all().update(is_default=False)

        # Set this carrier as default
        carrier.is_default = True
        carrier.save()

        return JsonResponse(
            {"success": True, "message": _('"{}" set as default carrier').format(carrier.name)}
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)


@staff_member_required
@require_POST
def delete_carrier(request, carrier_id):
    """Delete carrier via AJAX (custom carriers only)"""
    try:
        carrier = get_object_or_404(CarrierPreset, id=carrier_id)

        # Prevent deletion of system carriers
        if carrier.is_system:
            return JsonResponse(
                {"success": False, "message": _("System carriers cannot be deleted")}, status=403
            )

        carrier_name = carrier.name
        carrier.delete()

        return JsonResponse(
            {
                "success": True,
                "message": _('Carrier "{}" successfully deleted').format(carrier_name),
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)


@staff_member_required
@require_POST
def bulk_action(request):
    """Handle bulk actions on carriers via AJAX"""
    try:
        data = json.loads(request.body)
        action = data.get("action")
        carrier_ids = data.get("carrier_ids", [])

        if not action or not carrier_ids:
            return JsonResponse(
                {"success": False, "message": _("Invalid action or no carriers selected")},
                status=400,
            )

        carriers = CarrierPreset.objects.filter(id__in=carrier_ids)

        if action == "enable":
            carriers.update(is_active=True)
            message = _("{} carrier(s) enabled").format(carriers.count())

        elif action == "disable":
            carriers.update(is_active=False)
            message = _("{} carrier(s) disabled").format(carriers.count())

        elif action == "set_default":
            if carriers.count() != 1:
                return JsonResponse(
                    {
                        "success": False,
                        "message": _("Please select exactly one carrier to set as default"),
                    },
                    status=400,
                )

            # Remove default from all
            CarrierPreset.objects.all().update(is_default=False)

            # Set selected as default
            carrier = carriers.first()
            carrier.is_default = True
            carrier.save()

            message = _('"{}" set as default carrier').format(carrier.name)

        elif action == "delete":
            # Only delete custom carriers
            custom_carriers = carriers.filter(is_system=False)
            system_count = carriers.filter(is_system=True).count()

            deleted_count = custom_carriers.count()
            custom_carriers.delete()

            if system_count > 0:
                message = _("{} carrier(s) deleted ({} system carriers skipped)").format(
                    deleted_count, system_count
                )
            else:
                message = _("{} carrier(s) deleted").format(deleted_count)

        else:
            return JsonResponse(
                {"success": False, "message": _("Unknown action: {}").format(action)}, status=400
            )

        return JsonResponse({"success": True, "message": message})

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)
