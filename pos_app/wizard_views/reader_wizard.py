"""
Card Reader Registration Wizard Views

3-step wizard for pairing card readers with terminal providers:
1. Select provider & method (Register New or Discover Existing)
2. Register (code entry) or Discover (fetch from API)
3. Assign to terminal & save
"""

import logging
import uuid

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View

from pos_app.models import POSTerminal, POSTerminalProvider, POSTerminalReader

logger = logging.getLogger(__name__)


class ReaderWizardSessionMixin:
    """Mixin for managing reader wizard session data."""

    SESSION_KEY = "reader_wizard_data"

    def get_wizard_data(self):
        """Get wizard data from session."""
        return self.request.session.get(self.SESSION_KEY, {})

    def set_wizard_data(self, data):
        """Set wizard data in session."""
        self.request.session[self.SESSION_KEY] = data
        self.request.session.modified = True

    def update_wizard_data(self, **kwargs):
        """Update wizard data with new values."""
        data = self.get_wizard_data()
        data.update(kwargs)
        self.set_wizard_data(data)

    def clear_wizard_data(self):
        """Clear wizard data from session."""
        if self.SESSION_KEY in self.request.session:
            del self.request.session[self.SESSION_KEY]


@method_decorator(staff_member_required, name="dispatch")
class ReaderWizardStep1View(ReaderWizardSessionMixin, View):
    """
    Step 1: Select Provider & Method

    Choose which terminal provider to register with and how:
    - Register New Device: Enter registration code from device screen
    - Discover Existing: Fetch readers already registered with provider
    """

    template_name = "admin/pos_app/wizard/reader_step1_select.html"

    def get(self, request):
        """Display provider and method selection."""
        # Clear any existing wizard data when starting fresh
        self.clear_wizard_data()

        # Get active terminal providers
        providers = (
            POSTerminalProvider.objects.filter(is_active=True)
            .select_related("component")
            .order_by("display_name")
        )

        if not providers.exists():
            messages.warning(
                request, _("No active terminal providers found. Please configure a provider first.")
            )
            return redirect("admin:pos_app_posterminalprovider_changelist")

        context = {
            "title": _("Add Card Reader - Select Provider"),
            "providers": providers,
            "step": 1,
            "total_steps": 3,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle provider and method selection."""
        provider_id = request.POST.get("provider_id")
        method = request.POST.get("method")

        if not provider_id or not method:
            messages.error(request, _("Please select a provider and method."))
            return redirect("pos_admin:reader_wizard_step1")

        try:
            provider = POSTerminalProvider.objects.get(id=provider_id, is_active=True)
        except POSTerminalProvider.DoesNotExist:
            messages.error(request, _("Invalid provider selected."))
            return redirect("pos_admin:reader_wizard_step1")

        # Store selection in session
        self.update_wizard_data(
            provider_id=str(provider_id),
            provider_name=provider.display_name,
            provider_key=provider.provider_key,
            method=method,
        )

        # Manual provider skips to step 3
        if provider.provider_key == "manual":
            return redirect("pos_admin:reader_wizard_step3")

        return redirect("pos_admin:reader_wizard_step2")


@method_decorator(staff_member_required, name="dispatch")
class ReaderWizardStep2View(ReaderWizardSessionMixin, View):
    """
    Step 2: Register or Discover

    For 'register' mode: Enter registration code from device
    For 'discover' mode: Fetch and select from available readers
    """

    template_name = "admin/pos_app/wizard/reader_step2_register.html"

    def get(self, request):
        """Display registration code input or discovery results."""
        wizard_data = self.get_wizard_data()
        provider_id = wizard_data.get("provider_id")
        method = wizard_data.get("method")

        if not provider_id:
            messages.warning(request, _("Please select a provider first."))
            return redirect("pos_admin:reader_wizard_step1")

        try:
            provider = POSTerminalProvider.objects.get(id=provider_id)
        except POSTerminalProvider.DoesNotExist:
            messages.error(request, _("Provider not found."))
            return redirect("pos_admin:reader_wizard_step1")

        # For discover mode, fetch available readers
        available_readers = []
        discover_error = None

        if method == "discover":
            try:
                instance = provider.get_provider_instance()
                result = instance.list_readers()

                if result.get("success"):
                    # Filter out readers already registered locally
                    existing_ids = set(
                        POSTerminalReader.objects.filter(provider=provider).values_list(
                            "provider_reader_id", flat=True
                        )
                    )
                    available_readers = [
                        r for r in result.get("readers", []) if r["id"] not in existing_ids
                    ]
                else:
                    discover_error = result.get("message", _("Failed to fetch readers."))
            except Exception as e:
                logger.error(f"Error discovering readers: {e}")
                discover_error = str(e)

        context = {
            "title": _("Add Card Reader - %(method)s")
            % {"method": _("Register New") if method == "register" else _("Discover Existing")},
            "provider": provider,
            "method": method,
            "available_readers": available_readers,
            "discover_error": discover_error,
            "step": 2,
            "total_steps": 3,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle reader registration or discovery selection."""
        wizard_data = self.get_wizard_data()
        provider_id = wizard_data.get("provider_id")
        method = wizard_data.get("method")

        if not provider_id:
            return redirect("pos_admin:reader_wizard_step1")

        try:
            provider = POSTerminalProvider.objects.get(id=provider_id)
        except POSTerminalProvider.DoesNotExist:
            messages.error(request, _("Provider not found."))
            return redirect("pos_admin:reader_wizard_step1")

        if method == "register":
            # Get registration code and label from form
            registration_code = request.POST.get("registration_code", "").strip()
            reader_label = request.POST.get("reader_label", "").strip()

            if not registration_code:
                messages.error(request, _("Registration code is required."))
                return self.get(request)

            if not reader_label:
                reader_label = _("Reader %(date)s") % {
                    "date": timezone.now().strftime("%Y%m%d-%H%M")
                }

            # For AJAX requests, register immediately and return JSON
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return self._register_reader_ajax(
                    request, provider, registration_code, reader_label
                )

            # Non-AJAX: Register and continue to step 3
            try:
                instance = provider.get_provider_instance()
                result = instance.register_reader(registration_code, reader_label)

                if result.get("success"):
                    # Create the reader in database
                    reader = POSTerminalReader.objects.create(
                        provider=provider,
                        provider_reader_id=result["reader_id"],
                        reader_label=result.get("label", reader_label),
                        reader_type=result.get("type", ""),
                        serial_number=result.get("serial_number", ""),
                        status="online",
                        last_seen_at=timezone.now(),
                    )

                    self.update_wizard_data(
                        reader_id=str(reader.id),
                        reader_label=reader.reader_label,
                        reader_type=reader.reader_type,
                    )

                    return redirect("pos_admin:reader_wizard_step3")
                else:
                    messages.error(
                        request,
                        _("Registration failed: %(error)s") % {"error": result.get("message", "")},
                    )
                    return self.get(request)

            except Exception as e:
                logger.error(f"Reader registration error: {e}")
                messages.error(request, _("Registration error: %(error)s") % {"error": str(e)})
                return self.get(request)

        elif method == "discover":
            # Handle discovery selection
            selected_ids = request.POST.getlist("selected_readers")

            if not selected_ids:
                messages.error(request, _("Please select at least one reader."))
                return self.get(request)

            # Fetch reader details from provider
            try:
                instance = provider.get_provider_instance()
                result = instance.list_readers()

                if not result.get("success"):
                    messages.error(request, _("Failed to fetch reader details."))
                    return self.get(request)

                # Create readers for each selected ID
                readers_created = []
                for reader_data in result.get("readers", []):
                    if reader_data["id"] in selected_ids:
                        reader, created = POSTerminalReader.objects.update_or_create(
                            provider=provider,
                            provider_reader_id=reader_data["id"],
                            defaults={
                                "reader_label": reader_data.get("label", ""),
                                "reader_type": reader_data.get("type", ""),
                                "serial_number": reader_data.get("serial_number", ""),
                                "ip_address": reader_data.get("ip_address"),
                                "status": "online"
                                if reader_data.get("status") == "online"
                                else "offline",
                                "last_seen_at": timezone.now(),
                            },
                        )
                        readers_created.append(reader)

                if len(readers_created) == 1:
                    # Single reader - continue to step 3 for assignment
                    self.update_wizard_data(
                        reader_id=str(readers_created[0].id),
                        reader_label=readers_created[0].reader_label,
                        reader_type=readers_created[0].reader_type,
                    )
                    return redirect("pos_admin:reader_wizard_step3")
                else:
                    # Multiple readers - skip step 3 and show success
                    self.clear_wizard_data()
                    messages.success(
                        request,
                        _("Successfully imported %(count)d readers.")
                        % {"count": len(readers_created)},
                    )
                    return redirect("admin:pos_app_posterminalreader_changelist")

            except Exception as e:
                logger.error(f"Discovery import error: {e}")
                messages.error(request, _("Import error: %(error)s") % {"error": str(e)})
                return self.get(request)

        return redirect("pos_admin:reader_wizard_step1")

    def _register_reader_ajax(self, request, provider, registration_code, reader_label):
        """Handle AJAX reader registration."""
        try:
            instance = provider.get_provider_instance()
            result = instance.register_reader(registration_code, reader_label)

            if result.get("success"):
                # Create the reader in database
                reader = POSTerminalReader.objects.create(
                    provider=provider,
                    provider_reader_id=result["reader_id"],
                    reader_label=result.get("label", reader_label),
                    reader_type=result.get("type", ""),
                    serial_number=result.get("serial_number", ""),
                    status="online",
                    last_seen_at=timezone.now(),
                )

                self.update_wizard_data(
                    reader_id=str(reader.id),
                    reader_label=reader.reader_label,
                    reader_type=reader.reader_type,
                )

                return JsonResponse(
                    {
                        "success": True,
                        "reader": {
                            "id": str(reader.id),
                            "label": reader.reader_label,
                            "type": reader.reader_type,
                            "serial_number": reader.serial_number,
                        },
                        "redirect_url": str(request.build_absolute_uri("/").rstrip("/"))
                        + "/en/admin/pos/reader/wizard/step3/",
                    }
                )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "error": result.get("message", _("Registration failed.")),
                    }
                )

        except Exception as e:
            logger.error(f"AJAX reader registration error: {e}")
            return JsonResponse(
                {
                    "success": False,
                    "error": str(e),
                },
                status=500,
            )


@method_decorator(staff_member_required, name="dispatch")
class ReaderWizardStep3View(ReaderWizardSessionMixin, View):
    """
    Step 3: Assign to Terminal & Save

    Optionally assign the reader to a terminal and complete setup.
    """

    template_name = "admin/pos_app/wizard/reader_step3_assign.html"

    def get(self, request):
        """Display assignment form."""
        wizard_data = self.get_wizard_data()
        provider_id = wizard_data.get("provider_id")

        if not provider_id:
            messages.warning(request, _("Please select a provider first."))
            return redirect("pos_admin:reader_wizard_step1")

        try:
            provider = POSTerminalProvider.objects.get(id=provider_id)
        except POSTerminalProvider.DoesNotExist:
            messages.error(request, _("Provider not found."))
            return redirect("pos_admin:reader_wizard_step1")

        # Get reader if already registered (from step 2)
        reader_id = wizard_data.get("reader_id")
        reader = None
        if reader_id:
            try:
                reader = POSTerminalReader.objects.get(id=reader_id)
            except POSTerminalReader.DoesNotExist:
                pass

        # Get available terminals (those without a card reader assigned)
        terminals = (
            POSTerminal.objects.filter(is_active=True)
            .select_related("card_reader", "warehouse")
            .order_by("name")
        )

        context = {
            "title": _("Add Card Reader - Assign to Terminal"),
            "provider": provider,
            "reader": reader,
            "terminals": terminals,
            "step": 3,
            "total_steps": 3,
            "is_manual": provider.provider_key == "manual",
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle terminal assignment and save."""
        wizard_data = self.get_wizard_data()
        provider_id = wizard_data.get("provider_id")

        if not provider_id:
            return redirect("pos_admin:reader_wizard_step1")

        try:
            provider = POSTerminalProvider.objects.get(id=provider_id)
        except POSTerminalProvider.DoesNotExist:
            messages.error(request, _("Provider not found."))
            return redirect("pos_admin:reader_wizard_step1")

        # Get or create reader
        reader_id = wizard_data.get("reader_id")

        if reader_id:
            # Reader already exists (from step 2)
            try:
                reader = POSTerminalReader.objects.get(id=reader_id)
            except POSTerminalReader.DoesNotExist:
                messages.error(request, _("Reader not found."))
                return redirect("pos_admin:reader_wizard_step1")
        else:
            # Manual provider - create reader here
            reader_label = request.POST.get("reader_label", "").strip()
            if not reader_label:
                reader_label = _("Manual Reader %(date)s") % {
                    "date": timezone.now().strftime("%Y%m%d-%H%M")
                }

            reader = POSTerminalReader.objects.create(
                provider=provider,
                provider_reader_id=f"manual_{uuid.uuid4().hex[:8]}",
                reader_label=reader_label,
                reader_type="manual",
                status="online",
                last_seen_at=timezone.now(),
            )

        # Update label if provided
        new_label = request.POST.get("reader_label", "").strip()
        if new_label and new_label != reader.reader_label:
            reader.reader_label = new_label
            reader.save(update_fields=["reader_label"])

        # Handle terminal assignment
        terminal_id = request.POST.get("terminal_id")
        if terminal_id:
            try:
                terminal = POSTerminal.objects.get(id=terminal_id)

                # Remove any existing reader assignment
                POSTerminalReader.objects.filter(terminal=terminal).update(terminal=None)

                # Assign this reader
                reader.terminal = terminal
                reader.save(update_fields=["terminal"])

            except POSTerminal.DoesNotExist:
                messages.warning(request, _("Selected terminal not found."))

        # Clear wizard data
        self.clear_wizard_data()

        # Check for "add another" option
        add_another = request.POST.get("add_another")
        if add_another:
            messages.success(
                request,
                _('Reader "%(name)s" has been added. Add another reader below.')
                % {"name": reader.reader_label},
            )
            return redirect("pos_admin:reader_wizard_step1")

        messages.success(
            request,
            _('Reader "%(name)s" has been added successfully.') % {"name": reader.reader_label},
        )

        return redirect("admin:pos_app_posterminalreader_changelist")
