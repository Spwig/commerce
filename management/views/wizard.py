"""
Remote Storage Destination Setup Wizard.

3-step wizard for configuring remote backup storage destinations:
  Step 1: Select provider type (S3-compatible, SFTP)
  Step 2: Enter credentials + settings, test connection
  Step 3: Review configuration + save

Follows the payment_providers/views/wizard.py CBV pattern.
"""

import json
import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View

from management.models import RemoteStorageDestination
from management.storage_providers.registry import StorageProviderRegistry
from payment_providers.utils.encryption import encrypt_credentials

logger = logging.getLogger(__name__)


class WizardSessionMixin:
    """Manages wizard session data between steps."""

    SESSION_KEY = "remote_storage_wizard_data"

    def get_wizard_data(self):
        return self.request.session.get(self.SESSION_KEY, {})

    def set_wizard_data(self, data):
        self.request.session[self.SESSION_KEY] = data
        self.request.session.modified = True

    def update_wizard_data(self, **kwargs):
        data = self.get_wizard_data()
        data.update(kwargs)
        self.set_wizard_data(data)

    def clear_wizard_data(self):
        if self.SESSION_KEY in self.request.session:
            del self.request.session[self.SESSION_KEY]


@method_decorator(staff_member_required, name="dispatch")
class StorageWizardStep1View(WizardSessionMixin, View):
    """Step 1: Select storage provider type."""

    template_name = "admin/management/storage_wizard_step1.html"

    def get(self, request):
        self.clear_wizard_data()
        providers = StorageProviderRegistry.get_available_providers()

        return render(
            request,
            self.template_name,
            {
                "title": _("Add Remote Storage — Select Provider"),
                "providers": providers,
                "step": 1,
                "total_steps": 3,
            },
        )

    def post(self, request):
        provider_type = request.POST.get("provider_type")
        if not provider_type:
            messages.error(request, _("Please select a storage provider."))
            return self.get(request)

        provider_class = StorageProviderRegistry.get_provider_class(provider_type)
        if not provider_class:
            messages.error(request, _("Unknown provider type."))
            return self.get(request)

        self.update_wizard_data(
            provider_type=provider_type,
            provider_name=provider_class.provider_name,
        )
        return redirect("admin:management_storage_wizard_step2")


@method_decorator(staff_member_required, name="dispatch")
class StorageWizardStep2View(WizardSessionMixin, View):
    """Step 2: Enter credentials + settings, test connection inline."""

    template_name = "admin/management/storage_wizard_step2.html"

    def get(self, request):
        wizard_data = self.get_wizard_data()
        if not wizard_data.get("provider_type"):
            return redirect("admin:management_storage_wizard_step1")

        provider_type = wizard_data["provider_type"]
        provider_class = StorageProviderRegistry.get_provider_class(provider_type)

        # Inject saved values into field dicts for template pre-fill
        saved_creds = wizard_data.get("credentials", {})
        saved_settings = wizard_data.get("settings", {})

        credential_fields = []
        for f in provider_class.credential_fields:
            field_copy = dict(f)
            field_copy["saved_value"] = saved_creds.get(f["key"], "")
            credential_fields.append(field_copy)

        settings_fields = []
        for f in provider_class.settings_fields:
            field_copy = dict(f)
            field_copy["saved_value"] = saved_settings.get(f["key"], "")
            settings_fields.append(field_copy)

        context = {
            "title": _("Add Remote Storage — Configure"),
            "step": 2,
            "total_steps": 3,
            "provider_type": provider_type,
            "provider_name": wizard_data.get("provider_name", ""),
            "credential_fields": credential_fields,
            "settings_fields": settings_fields,
            "test_url": reverse("admin:management_storage_test_connection"),
            "saved_name": wizard_data.get("destination_name", ""),
            "requires_oauth": getattr(provider_class, "requires_oauth", False),
        }

        # OAuth-specific context
        if context["requires_oauth"]:
            context["oauth_authorized"] = wizard_data.get("oauth_authorized", False)
            context["oauth_redirect_uri"] = request.build_absolute_uri(
                reverse("admin:management_storage_oauth_callback")
            )

        return render(request, self.template_name, context)

    def post(self, request):
        wizard_data = self.get_wizard_data()
        provider_type = wizard_data.get("provider_type")
        if not provider_type:
            return redirect("admin:management_storage_wizard_step1")

        provider_class = StorageProviderRegistry.get_provider_class(provider_type)

        # Collect credentials
        is_oauth = getattr(provider_class, "requires_oauth", False)

        if is_oauth and wizard_data.get("oauth_authorized"):
            # OAuth providers: credentials include tokens from OAuth callback
            # Merge any POST form values (client_id/secret may be re-submitted)
            credentials = wizard_data.get("credentials", {})
            for field in provider_class.credential_fields:
                val = request.POST.get(f"cred_{field['key']}", "").strip()
                if val:
                    credentials[field["key"]] = val
        else:
            credentials = {}
            for field in provider_class.credential_fields:
                val = request.POST.get(f"cred_{field['key']}", "").strip()
                if field.get("required") and not val:
                    messages.error(request, _("%(field)s is required.") % {"field": field["label"]})
                    return self.get(request)
                if val:
                    credentials[field["key"]] = val

        # Collect settings
        settings = {}
        for field in provider_class.settings_fields:
            val = request.POST.get(f"setting_{field['key']}", "").strip()
            if field.get("required") and not val:
                messages.error(request, _("%(field)s is required.") % {"field": field["label"]})
                return self.get(request)
            settings[field["key"]] = val or field.get("default", "")

        destination_name = request.POST.get("destination_name", "").strip()
        if not destination_name:
            messages.error(request, _("Destination name is required."))
            return self.get(request)

        # Store in session (plain text — encrypted on save)
        self.update_wizard_data(
            credentials=credentials,
            settings=settings,
            destination_name=destination_name,
        )

        return redirect("admin:management_storage_wizard_step3")


@method_decorator(staff_member_required, name="dispatch")
class StorageWizardStep3View(WizardSessionMixin, View):
    """Step 3: Review configuration + save."""

    template_name = "admin/management/storage_wizard_step3.html"

    def get(self, request):
        wizard_data = self.get_wizard_data()
        if not wizard_data.get("credentials"):
            return redirect("admin:management_storage_wizard_step2")

        provider_type = wizard_data["provider_type"]
        provider_class = StorageProviderRegistry.get_provider_class(provider_type)

        # Build display-safe summary (redact secrets)
        summary_items = []
        for field in provider_class.credential_fields:
            val = wizard_data.get("credentials", {}).get(field["key"], "")
            if field.get("secret") and val:
                display = f"{val[:3]}***{val[-3:]}" if len(val) > 6 else "***"
            else:
                display = val
            summary_items.append({"label": field["label"], "value": display})

        for field in provider_class.settings_fields:
            val = wizard_data.get("settings", {}).get(field["key"], "")
            # For select fields, show label not value
            if field.get("type") == "select" and field.get("options"):
                for opt in field["options"]:
                    if opt.get("value") == val:
                        val = opt.get("label", val)
                        break
            summary_items.append({"label": field["label"], "value": val})

        return render(
            request,
            self.template_name,
            {
                "title": _("Add Remote Storage — Review & Save"),
                "step": 3,
                "total_steps": 3,
                "provider_type": provider_type,
                "provider_name": wizard_data.get("provider_name", ""),
                "destination_name": wizard_data.get("destination_name", ""),
                "summary_items": summary_items,
            },
        )

    def post(self, request):
        wizard_data = self.get_wizard_data()
        if not wizard_data.get("credentials"):
            return redirect("admin:management_storage_wizard_step2")

        is_default = request.POST.get("is_default") == "on"
        retention_days = int(request.POST.get("retention_days", 0) or 0)

        # Encrypt credentials before saving
        encrypted = encrypt_credentials(wizard_data["credentials"])

        destination = RemoteStorageDestination.objects.create(
            name=wizard_data["destination_name"],
            provider_type=wizard_data["provider_type"],
            credentials_encrypted=encrypted,
            settings=wizard_data.get("settings", {}),
            is_active=True,
            is_default=is_default,
            retention_days=retention_days,
            created_by=request.user,
        )

        # If set as default, unset other defaults
        if is_default:
            RemoteStorageDestination.objects.filter(
                is_default=True,
            ).exclude(pk=destination.pk).update(is_default=False)

        self.clear_wizard_data()
        messages.success(
            request,
            _('Remote storage destination "%(name)s" created successfully.')
            % {
                "name": destination.name,
            },
        )
        return redirect("admin:management_storage_destinations")


@staff_member_required
def test_connection_view(request):
    """AJAX endpoint for testing storage connection with provided credentials."""
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "POST required."}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Invalid JSON."}, status=400)

    provider_type = data.get("provider_type")
    credentials = data.get("credentials", {})
    settings = data.get("settings", {})

    # For OAuth providers, merge session-stored tokens (access_token,
    # refresh_token, etc.) into the credentials from the AJAX request
    # which only contains form-field values (client_id/client_secret).
    provider_class = StorageProviderRegistry.get_provider_class(provider_type)
    if provider_class and getattr(provider_class, "requires_oauth", False):
        wizard_data = request.session.get("remote_storage_wizard_data", {})
        session_creds = wizard_data.get("credentials", {})
        merged = dict(session_creds)
        merged.update(credentials)  # POST values override session
        credentials = merged

    try:
        provider = StorageProviderRegistry.create_from_raw(
            provider_type=provider_type,
            credentials=credentials,
            settings=settings,
        )
    except ValueError as e:
        return JsonResponse({"success": False, "message": str(e)})

    result = provider.test_connection()

    return JsonResponse(
        {
            "success": result.success,
            "message": result.message,
            "details": result.details,
            "storage_used": result.storage_used,
            "storage_available": result.storage_available,
        }
    )


@staff_member_required
def storage_destinations_view(request):
    """List all configured remote storage destinations."""
    destinations = RemoteStorageDestination.objects.all()
    return render(
        request,
        "admin/management/storage_destinations.html",
        {
            "title": _("Remote Storage Destinations"),
            "destinations": destinations,
        },
    )


@staff_member_required
def delete_destination_view(request, destination_id):
    """Delete a remote storage destination."""
    try:
        destination = RemoteStorageDestination.objects.get(pk=destination_id)
    except RemoteStorageDestination.DoesNotExist:
        messages.error(request, _("Destination not found."))
        return redirect("admin:management_storage_destinations")

    if request.method == "POST":
        name = destination.name
        destination.delete()
        messages.success(
            request,
            _('Remote storage destination "%(name)s" deleted.') % {"name": name},
        )
        return redirect("admin:management_storage_destinations")

    return render(
        request,
        "admin/management/storage_destination_delete.html",
        {
            "title": _("Delete Remote Storage Destination"),
            "destination": destination,
        },
    )


@staff_member_required
def retest_destination_view(request, destination_id):
    """Re-test connection for an existing destination (AJAX)."""
    try:
        destination = RemoteStorageDestination.objects.get(pk=destination_id)
    except RemoteStorageDestination.DoesNotExist:
        return JsonResponse({"success": False, "message": "Destination not found."})

    from django.utils import timezone

    try:
        provider = StorageProviderRegistry.create_from_destination(destination)
        result = provider.test_connection()

        destination.connection_status = "connected" if result.success else "error"
        destination.connection_error = "" if result.success else result.message
        destination.last_tested_at = timezone.now()
        destination.save(update_fields=["connection_status", "connection_error", "last_tested_at"])

        return JsonResponse(
            {
                "success": result.success,
                "message": result.message,
                "details": result.details,
            }
        )
    except Exception as e:
        destination.connection_status = "error"
        destination.connection_error = str(e)
        destination.last_tested_at = timezone.now()
        destination.save(update_fields=["connection_status", "connection_error", "last_tested_at"])
        return JsonResponse({"success": False, "message": str(e)})
