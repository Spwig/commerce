"""
SMS System Views.

Provides views for the SMS provider setup wizard and provider browsing.
"""

import json
import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View

from providers_common.utils import load_manifest_translations
from sms_system.models import SMSProviderAccount
from sms_system.providers.registry import SMSProviderRegistry
from sms_system.services.provider_service import SMSProviderService

logger = logging.getLogger(__name__)


class WizardSessionMixin:
    """Mixin for managing wizard session data."""

    SESSION_KEY = "sms_wizard_data"

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
class WizardStep1View(WizardSessionMixin, View):
    """
    Step 1: Select SMS Provider.

    Displays available SMS providers from the component registry.
    """

    template_name = "admin/sms_system/wizard/step1_select.html"

    def get(self, request):
        # Clear any previous wizard data
        self.clear_wizard_data()

        # Auto-skip if provider pre-selected from browse page
        provider_key = request.GET.get("provider", "")
        if provider_key and SMSProviderRegistry.is_provider_installed(provider_key):
            self.update_wizard_data(provider_key=provider_key)
            return redirect("sms_system:wizard_step2")

        # Get installed providers
        providers = SMSProviderRegistry.list_providers()

        # Group by capability
        sms_providers = [p for p in providers if p.get("capabilities", {}).get("sms", False)]
        whatsapp_providers = [
            p for p in providers if p.get("capabilities", {}).get("whatsapp", False)
        ]

        return render(
            request,
            self.template_name,
            {
                "title": _("Select SMS Provider"),
                "step": 1,
                "providers": providers,
                "sms_providers": sms_providers,
                "whatsapp_providers": whatsapp_providers,
            },
        )

    def post(self, request):
        provider_key = request.POST.get("provider_key")

        if not provider_key:
            messages.error(request, _("Please select a provider"))
            return redirect("sms_system:wizard_step1")

        # Verify provider exists
        if not SMSProviderRegistry.is_provider_installed(provider_key):
            messages.error(request, _("Selected provider is not available"))
            return redirect("sms_system:wizard_step1")

        # Store in session
        self.update_wizard_data(provider_key=provider_key)

        return redirect("sms_system:wizard_step2")


@method_decorator(staff_member_required, name="dispatch")
class WizardStep2View(WizardSessionMixin, View):
    """
    Step 2: Setup Instructions.

    Shows provider-specific setup instructions.
    """

    template_name = "admin/sms_system/wizard/step2_instructions.html"

    def get(self, request):
        wizard_data = self.get_wizard_data()
        provider_key = wizard_data.get("provider_key")

        if not provider_key:
            return redirect("sms_system:wizard_step1")

        # Get provider info
        provider_info = SMSProviderRegistry.get_provider_info(provider_key)
        if not provider_info:
            messages.error(request, _("Provider not found"))
            return redirect("sms_system:wizard_step1")

        # Get setup instructions
        instructions_html = SMSProviderService.get_setup_instructions(provider_key)

        # Load manifest translations for i18n
        try:
            component_path = SMSProviderService.get_component_path(provider_key)
            manifest_translations = load_manifest_translations(component_path)
        except Exception:
            manifest_translations = None

        return render(
            request,
            self.template_name,
            {
                "title": _("Setup Instructions"),
                "step": 2,
                "provider": provider_info,
                "instructions_html": instructions_html,
                "manifest_translations": manifest_translations,
            },
        )

    def post(self, request):
        # Just move to next step
        return redirect("sms_system:wizard_step3")


@method_decorator(staff_member_required, name="dispatch")
class WizardStep3View(WizardSessionMixin, View):
    """
    Step 3: Enter Credentials.

    Dynamic form based on provider's credential schema.
    """

    template_name = "admin/sms_system/wizard/step3_credentials.html"

    def get(self, request):
        wizard_data = self.get_wizard_data()
        provider_key = wizard_data.get("provider_key")

        if not provider_key:
            return redirect("sms_system:wizard_step1")

        # Get provider info and credential schema
        provider_info = SMSProviderRegistry.get_provider_info(provider_key)
        credential_schema = SMSProviderService.get_credential_schema(provider_key)

        if not provider_info:
            messages.error(request, _("Provider not found"))
            return redirect("sms_system:wizard_step1")

        # Build form fields from schema
        form_fields = SMSProviderService.build_credential_form_fields(provider_key)

        return render(
            request,
            self.template_name,
            {
                "title": _("Enter Credentials"),
                "step": 3,
                "provider": provider_info,
                "credential_schema": credential_schema,
                "form_fields": form_fields,
            },
        )

    def post(self, request):
        wizard_data = self.get_wizard_data()
        provider_key = wizard_data.get("provider_key")

        if not provider_key:
            return redirect("sms_system:wizard_step1")

        # Get credential schema
        credential_schema = SMSProviderService.get_credential_schema(provider_key)
        if not credential_schema:
            messages.error(request, _("Unable to get credential schema"))
            return redirect("sms_system:wizard_step3")

        # Extract credentials from POST data
        properties = credential_schema.get("properties", {})
        required_fields = credential_schema.get("required", [])
        credentials = {}

        for field_name in properties:
            value = request.POST.get(field_name, "").strip()
            if value:
                credentials[field_name] = value

        # Validate required fields
        missing = [f for f in required_fields if not credentials.get(f)]
        if missing:
            messages.error(
                request, _("Missing required fields: %(fields)s") % {"fields": ", ".join(missing)}
            )
            return redirect("sms_system:wizard_step3")

        # Get display name
        display_name = request.POST.get("display_name", "").strip()
        if not display_name:
            provider_info = SMSProviderRegistry.get_provider_info(provider_key)
            display_name = (
                provider_info.get("name", provider_key) if provider_info else provider_key
            )

        # Store credentials in session (temporarily)
        self.update_wizard_data(
            credentials=credentials,
            display_name=display_name,
        )

        return redirect("sms_system:wizard_step4")


@method_decorator(staff_member_required, name="dispatch")
class WizardStep4View(WizardSessionMixin, View):
    """
    Step 4: Test Connection & Configure Defaults.

    Tests the provider connection and allows setting as default.
    """

    template_name = "admin/sms_system/wizard/step4_test.html"

    def get(self, request):
        wizard_data = self.get_wizard_data()
        provider_key = wizard_data.get("provider_key")
        credentials = wizard_data.get("credentials")
        display_name = wizard_data.get("display_name")

        if not all([provider_key, credentials]):
            return redirect("sms_system:wizard_step1")

        # Get provider info
        provider_info = SMSProviderRegistry.get_provider_info(provider_key)

        # Test connection
        test_result = SMSProviderService.test_connection(provider_key, credentials)

        # Store test result
        self.update_wizard_data(test_result=test_result)

        return render(
            request,
            self.template_name,
            {
                "title": _("Test Connection"),
                "step": 4,
                "provider": provider_info,
                "display_name": display_name,
                "test_result": test_result,
            },
        )

    def post(self, request):
        wizard_data = self.get_wizard_data()
        provider_key = wizard_data.get("provider_key")
        credentials = wizard_data.get("credentials")
        display_name = wizard_data.get("display_name")
        test_result = wizard_data.get("test_result", {})

        if not all([provider_key, credentials]):
            return redirect("sms_system:wizard_step1")

        # Check if connection test passed
        if not test_result.get("success", False):
            # Allow saving anyway with user confirmation
            if not request.POST.get("save_anyway"):
                messages.warning(
                    request, _("Connection test failed. Check your credentials and try again.")
                )
                return redirect("sms_system:wizard_step4")

        # Get default settings
        is_default_sms = request.POST.get("is_default_sms") == "on"
        is_default_whatsapp = request.POST.get("is_default_whatsapp") == "on"

        try:
            # Create account
            account = SMSProviderAccount(
                provider_key=provider_key,
                display_name=display_name,
                is_default_sms=is_default_sms,
                is_default_whatsapp=is_default_whatsapp,
                is_active=True,
                connection_status="success" if test_result.get("success") else "failed",
            )
            account.set_credentials(credentials)
            account.save()

            # Store account ID for completion page
            self.update_wizard_data(account_id=account.pk)

            messages.success(request, _("SMS provider account created successfully!"))
            return redirect("sms_system:wizard_complete")

        except Exception as e:
            logger.error(f"Failed to create SMS provider account: {e}")
            messages.error(request, _("Failed to create account: %(error)s") % {"error": str(e)})
            return redirect("sms_system:wizard_step4")


@method_decorator(staff_member_required, name="dispatch")
class WizardCompleteView(WizardSessionMixin, View):
    """
    Wizard Completion Page.

    Shows success message and next steps.
    """

    template_name = "admin/sms_system/wizard/complete.html"

    def get(self, request):
        wizard_data = self.get_wizard_data()
        account_id = wizard_data.get("account_id")

        account = None
        if account_id:
            try:
                account = SMSProviderAccount.objects.get(pk=account_id)
            except SMSProviderAccount.DoesNotExist:
                pass

        # Clear wizard data
        self.clear_wizard_data()

        return render(
            request,
            self.template_name,
            {
                "title": _("Setup Complete"),
                "step": 5,
                "account": account,
            },
        )


@method_decorator(staff_member_required, name="dispatch")
class ProviderBrowseView(View):
    """
    Provider Browse View.

    Lists installed and available SMS providers with filtering,
    update detection, and modal support.
    """

    template_name = "admin/sms_system/provider_browse.html"

    def get(self, request):
        from django.utils.translation import get_language

        # Get filter parameters
        has_sms = request.GET.get("sms")
        has_whatsapp = request.GET.get("whatsapp")
        has_mms = request.GET.get("mms")

        # Get current admin language for manifest i18n
        lang = get_language() or "en"

        # Get providers organized for display
        browse_data = SMSProviderService.get_providers_for_browse(lang=lang)

        installed_providers = browse_data.get("installed", [])
        available_providers = browse_data.get("available", [])

        # Apply capability filters
        if has_sms or has_whatsapp or has_mms:

            def matches_filters(provider):
                caps = provider.get("capabilities", {})
                if has_sms and not caps.get("sms"):
                    return False
                if has_whatsapp and not caps.get("whatsapp"):
                    return False
                return not (has_mms and not caps.get("mms"))

            installed_providers = [p for p in installed_providers if matches_filters(p)]
            available_providers = [p for p in available_providers if matches_filters(p)]

        # Count capabilities
        all_providers = installed_providers + available_providers
        sms_count = sum(1 for p in all_providers if p.get("capabilities", {}).get("sms"))
        whatsapp_count = sum(1 for p in all_providers if p.get("capabilities", {}).get("whatsapp"))
        mms_count = sum(1 for p in all_providers if p.get("capabilities", {}).get("mms"))

        return render(
            request,
            self.template_name,
            {
                "title": _("SMS Providers"),
                "installed_providers": installed_providers,
                "available_providers": available_providers,
                "has_update_server": browse_data.get("has_update_server", False),
                "providers_json": browse_data.get("providers_json", []),
                "has_sms": has_sms,
                "has_whatsapp": has_whatsapp,
                "has_mms": has_mms,
                "sms_count": sms_count,
                "whatsapp_count": whatsapp_count,
                "mms_count": mms_count,
            },
        )


@method_decorator(staff_member_required, name="dispatch")
class TestConnectionView(View):
    """
    AJAX endpoint for testing provider connection.
    """

    def post(self, request):
        try:
            data = json.loads(request.body)
            provider_key = data.get("provider_key")
            credentials = data.get("credentials", {})

            if not provider_key:
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Provider key is required",
                    }
                )

            result = SMSProviderService.test_connection(provider_key, credentials)
            return JsonResponse(result)

        except json.JSONDecodeError:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Invalid JSON data",
                }
            )
        except Exception as e:
            logger.error(f"Error testing connection: {e}")
            return JsonResponse(
                {
                    "success": False,
                    "error": str(e),
                }
            )


@method_decorator(staff_member_required, name="dispatch")
class SetupInstructionsView(View):
    """
    AJAX endpoint for fetching setup instructions.
    """

    def get(self, request, provider_key):
        instructions = SMSProviderService.get_setup_instructions(provider_key)

        if instructions:
            return JsonResponse(
                {
                    "success": True,
                    "html": instructions,
                }
            )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Instructions not found",
                }
            )


@staff_member_required
def install_provider_ajax(request, provider_slug):
    """
    AJAX endpoint to install an SMS provider from the update server.

    POST to install provider. Returns JSON with success status and redirect URL.
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)

    from component_updates.models import ComponentRegistry

    # Check if already installed
    try:
        component = ComponentRegistry.objects.get(slug=provider_slug, component_type="sms_provider")
        from django.urls import reverse

        return JsonResponse(
            {
                "success": True,
                "already_installed": True,
                "message": _("Provider is already installed. Configure it now."),
                "redirect_url": reverse("sms_system:wizard_step1"),
            }
        )
    except ComponentRegistry.DoesNotExist:
        pass

    # Install provider from update server
    try:
        from django.urls import reverse

        from component_updates.services import UpdateManager

        update_manager = UpdateManager()
        available_providers = update_manager.list_available_components(
            component_type="sms_provider"
        )

        # Find the requested provider
        provider_info = None
        for provider in available_providers:
            if provider.get("slug") == provider_slug:
                provider_info = provider
                break

        if not provider_info:
            return JsonResponse(
                {
                    "success": False,
                    "error": _("Provider not found on update server."),
                },
                status=404,
            )

        latest_version = provider_info.get("current_version") or provider_info.get("version")
        provider_name = provider_info.get("name", provider_slug)
        provider_description = provider_info.get("description", "")

        if not latest_version:
            return JsonResponse(
                {
                    "success": False,
                    "error": _("Could not determine provider version."),
                },
                status=400,
            )

        from django.db import transaction

        with transaction.atomic():
            component = ComponentRegistry.objects.create(
                slug=provider_slug,
                name=provider_name,
                description=provider_description,
                component_type="sms_provider",
                current_version=latest_version,
            )

            try:
                package_path = update_manager.download_component(component, latest_version)
            except Exception as e:
                component.delete()
                return JsonResponse(
                    {
                        "success": False,
                        "error": _("Failed to download provider: %(error)s") % {"error": str(e)},
                    },
                    status=500,
                )

            try:
                update_manager._install_package(component, package_path, latest_version)
            except Exception as e:
                component.delete()
                return JsonResponse(
                    {
                        "success": False,
                        "error": _("Failed to install provider: %(error)s") % {"error": str(e)},
                    },
                    status=500,
                )

            # Create 'current' symlink
            try:
                from component_updates.integration_paths import INTEGRATIONS_DIR

                provider_base_dir = INTEGRATIONS_DIR / "sms_provider" / provider_slug
                current_link = provider_base_dir / "current"
                version_dir = (
                    f"v{latest_version}" if not latest_version.startswith("v") else latest_version
                )

                if current_link.exists() or current_link.is_symlink():
                    current_link.unlink()

                current_link.symlink_to(version_dir)

                # Reload providers
                SMSProviderService.reload_providers()
            except Exception as e:
                logger.warning(f"Could not create symlink for {provider_slug}: {e}")

        return JsonResponse(
            {
                "success": True,
                "message": _('Provider "%(name)s" installed successfully! Configure it now.')
                % {"name": provider_name},
                "redirect_url": reverse("sms_system:wizard_step1"),
            }
        )

    except Exception as e:
        logger.error(f"Error installing SMS provider {provider_slug}: {e}")
        return JsonResponse(
            {
                "success": False,
                "error": str(e),
            },
            status=500,
        )


@staff_member_required
def update_provider_ajax(request, provider_slug):
    """
    AJAX endpoint to update an SMS provider to the latest version.
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)

    from django.db import transaction
    from django.urls import reverse

    from component_updates.models import ComponentRegistry

    try:
        try:
            component = ComponentRegistry.objects.get(
                slug=provider_slug, component_type="sms_provider"
            )
        except ComponentRegistry.DoesNotExist:
            return JsonResponse(
                {
                    "success": False,
                    "error": _("Provider not installed."),
                },
                status=404,
            )

        from component_updates.services import UpdateManager

        update_manager = UpdateManager()

        try:
            available_from_server = update_manager.list_available_components(
                component_type="sms_provider"
            )
        except Exception as e:
            return JsonResponse(
                {
                    "success": False,
                    "error": _("Could not connect to update server: %(error)s") % {"error": str(e)},
                },
                status=500,
            )

        provider_info = None
        for provider in available_from_server:
            if provider.get("slug") == provider_slug:
                provider_info = provider
                break

        if not provider_info:
            return JsonResponse(
                {
                    "success": False,
                    "error": _("Provider not found on update server."),
                },
                status=404,
            )

        latest_version = provider_info.get("current_version") or provider_info.get("version")
        provider_name = provider_info.get("name", provider_slug)

        if not latest_version:
            return JsonResponse(
                {
                    "success": False,
                    "error": _("Could not determine latest version."),
                },
                status=400,
            )

        current_version = component.current_version
        if current_version == latest_version:
            return JsonResponse(
                {
                    "success": True,
                    "message": _('Provider "%(name)s" is already up to date (v%(version)s).')
                    % {
                        "name": provider_name,
                        "version": latest_version,
                    },
                    "redirect_url": reverse("sms_system:provider_browse"),
                }
            )

        with transaction.atomic():
            try:
                package_path = update_manager.download_component(component, latest_version)
            except Exception as e:
                return JsonResponse(
                    {
                        "success": False,
                        "error": _("Failed to download update: %(error)s") % {"error": str(e)},
                    },
                    status=500,
                )

            try:
                update_manager._install_package(component, package_path, latest_version)
            except Exception as e:
                return JsonResponse(
                    {
                        "success": False,
                        "error": _("Failed to install update: %(error)s") % {"error": str(e)},
                    },
                    status=500,
                )

            # Update 'current' symlink
            try:
                from component_updates.integration_paths import INTEGRATIONS_DIR

                provider_base_dir = INTEGRATIONS_DIR / "sms_provider" / provider_slug
                current_link = provider_base_dir / "current"
                version_dir = (
                    f"v{latest_version}" if not latest_version.startswith("v") else latest_version
                )

                if current_link.exists() or current_link.is_symlink():
                    current_link.unlink()

                current_link.symlink_to(version_dir)

                SMSProviderService.reload_providers()
            except Exception as e:
                logger.warning(f"Could not update symlink for {provider_slug}: {e}")

            component.current_version = latest_version
            component.save()

        return JsonResponse(
            {
                "success": True,
                "message": _('Provider "%(name)s" updated successfully to v%(version)s!')
                % {
                    "name": provider_name,
                    "version": latest_version,
                },
                "redirect_url": reverse("sms_system:provider_browse"),
            }
        )

    except Exception as e:
        logger.error(f"Error updating SMS provider {provider_slug}: {e}")
        return JsonResponse(
            {
                "success": False,
                "error": str(e),
            },
            status=500,
        )
