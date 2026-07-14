"""
Admin AJAX views for carrier and provider account management
Handles quick actions and bulk operations
"""

import json
import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from shipping.models import CarrierPreset, ProviderAccount, ShippingPromotion, ShippingZone
from shipping.providers.registry import ProviderRegistry

logger = logging.getLogger(__name__)


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


# ============================================================================
# Provider Account AJAX Views
# ============================================================================


@staff_member_required
@require_POST
def toggle_provider_active(request, provider_id):
    """Toggle provider account active status via AJAX"""
    try:
        provider = get_object_or_404(ProviderAccount, id=provider_id)

        # Toggle active status
        provider.is_active = not provider.is_active
        provider.save()

        return JsonResponse(
            {
                "success": True,
                "is_active": provider.is_active,
                "message": _("Provider {} successfully").format(
                    _("enabled") if provider.is_active else _("disabled")
                ),
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)


@staff_member_required
@require_POST
def set_provider_default(request, provider_id):
    """Set provider account as default via AJAX"""
    try:
        provider = get_object_or_404(ProviderAccount, id=provider_id)

        # Remove default from all other providers
        ProviderAccount.objects.all().update(is_default=False)

        # Set this provider as default
        provider.is_default = True
        provider.save()

        return JsonResponse(
            {
                "success": True,
                "message": _('"{}" set as default provider').format(
                    provider.display_name or provider.component.name
                ),
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)


@staff_member_required
@require_POST
def test_provider_connection(request, provider_id):
    """Test provider connection via AJAX"""
    try:
        provider = get_object_or_404(ProviderAccount, id=provider_id)

        # Get provider class from registry
        provider_class = ProviderRegistry.get_provider(provider.component.slug)

        if not provider_class:
            return JsonResponse(
                {"success": False, "message": _("Provider implementation not found")}, status=404
            )

        # Decrypt credentials
        from shipping.utils.encryption import decrypt_credentials

        credentials = decrypt_credentials(provider.credentials_encrypted)

        # Create provider instance and test
        provider_instance = provider_class(credentials=credentials)
        test_result = provider_instance.test_connection()

        # Update provider account status
        if test_result.get("success"):
            provider.connection_status = "connected"
            provider.connection_error = None
            provider.save(update_fields=["connection_status", "connection_error", "last_tested_at"])
        else:
            provider.connection_status = "error"
            provider.connection_error = test_result.get("error", test_result.get("message"))
            provider.save(update_fields=["connection_status", "connection_error", "last_tested_at"])

        return JsonResponse(test_result)

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
@require_POST
def delete_provider(request, provider_id):
    """Delete provider account via AJAX"""
    try:
        provider = get_object_or_404(ProviderAccount, id=provider_id)

        provider_name = provider.display_name or provider.component.name
        provider.delete()

        return JsonResponse(
            {
                "success": True,
                "message": _('Provider "{}" successfully deleted').format(provider_name),
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)


@staff_member_required
@require_POST
def provider_bulk_action(request):
    """Handle bulk actions on provider accounts via AJAX"""
    try:
        data = json.loads(request.body)
        action = data.get("action")
        provider_ids = data.get("provider_ids", [])

        if not action or not provider_ids:
            return JsonResponse(
                {"success": False, "message": _("Invalid action or no providers selected")},
                status=400,
            )

        providers = ProviderAccount.objects.filter(id__in=provider_ids)

        if action == "enable":
            providers.update(is_active=True)
            message = _("{} provider(s) enabled").format(providers.count())

        elif action == "disable":
            providers.update(is_active=False)
            message = _("{} provider(s) disabled").format(providers.count())

        elif action == "set_default":
            if providers.count() != 1:
                return JsonResponse(
                    {
                        "success": False,
                        "message": _("Please select exactly one provider to set as default"),
                    },
                    status=400,
                )

            # Remove default from all
            ProviderAccount.objects.all().update(is_default=False)

            # Set selected as default
            provider = providers.first()
            provider.is_default = True
            provider.save()

            message = _('"{}" set as default provider').format(
                provider.display_name or provider.component.name
            )

        elif action == "test_connection":
            # Test connection for each provider
            success_count = 0
            error_count = 0

            for provider in providers:
                try:
                    provider_class = ProviderRegistry.get_provider(provider.component.slug)
                    if provider_class:
                        from shipping.utils.encryption import decrypt_credentials

                        credentials = decrypt_credentials(provider.credentials_encrypted)
                        provider_instance = provider_class(credentials=credentials)
                        test_result = provider_instance.test_connection()

                        if test_result.get("success"):
                            provider.connection_status = "connected"
                            provider.connection_error = None
                            success_count += 1
                        else:
                            provider.connection_status = "error"
                            provider.connection_error = test_result.get(
                                "error", test_result.get("message")
                            )
                            error_count += 1

                        provider.save(
                            update_fields=[
                                "connection_status",
                                "connection_error",
                                "last_tested_at",
                            ]
                        )
                except Exception:
                    error_count += 1

            if error_count > 0:
                message = _("{} provider(s) connected, {} failed").format(
                    success_count, error_count
                )
            else:
                message = _("{} provider(s) tested successfully").format(success_count)

        elif action == "delete":
            deleted_count = providers.count()
            providers.delete()
            message = _("{} provider(s) deleted").format(deleted_count)

        else:
            return JsonResponse(
                {"success": False, "message": _("Unknown action: {}").format(action)}, status=400
            )

        return JsonResponse({"success": True, "message": message})

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)


# ============================================================================
# Shipping Zone Bulk Actions
# ============================================================================


@staff_member_required
@require_POST
def zone_bulk_action(request):
    """Handle bulk actions on shipping zones via AJAX"""
    try:
        data = json.loads(request.body)
        action = data.get("action")
        zone_ids = data.get("zone_ids", [])

        if not action or not zone_ids:
            return JsonResponse(
                {"success": False, "message": _("Invalid action or no zones selected")}, status=400
            )

        zones = ShippingZone.objects.filter(id__in=zone_ids)
        count = zones.count()

        if action == "enable":
            zones.update(is_active=True)
            message = _("{} zone(s) enabled").format(count)

        elif action == "disable":
            zones.update(is_active=False)
            message = _("{} zone(s) disabled").format(count)

        elif action == "delete":
            zones.delete()
            message = _("{} zone(s) deleted").format(count)

        else:
            return JsonResponse({"success": False, "message": _("Unknown action")}, status=400)

        return JsonResponse({"success": True, "message": message})

    except Exception as e:
        logger.error("Shipping zone bulk action error: %s", e, exc_info=True)
        return JsonResponse(
            {"success": False, "message": _("An unexpected error occurred. Please try again.")},
            status=500,
        )


# ============================================================================
# Shipping Promotion Bulk Actions
# ============================================================================


@staff_member_required
@require_POST
def rule_bulk_action(request):
    """Handle bulk actions on shipping promotions via AJAX"""
    try:
        data = json.loads(request.body)
        action = data.get("action")
        rule_ids = data.get("rule_ids", [])

        if not action or not rule_ids:
            return JsonResponse(
                {"success": False, "message": _("Invalid action or no promotions selected")},
                status=400,
            )

        promotions = ShippingPromotion.objects.filter(id__in=rule_ids)
        count = promotions.count()

        if action == "enable":
            promotions.update(is_active=True)
            message = _("{} promotion(s) enabled").format(count)

        elif action == "disable":
            promotions.update(is_active=False)
            message = _("{} promotion(s) disabled").format(count)

        elif action == "delete":
            promotions.delete()
            message = _("{} promotion(s) deleted").format(count)

        else:
            return JsonResponse({"success": False, "message": _("Unknown action")}, status=400)

        return JsonResponse({"success": True, "message": message})

    except Exception as e:
        logger.error("Shipping rule bulk action error: %s", e, exc_info=True)
        return JsonResponse(
            {"success": False, "message": _("An unexpected error occurred. Please try again.")},
            status=500,
        )
