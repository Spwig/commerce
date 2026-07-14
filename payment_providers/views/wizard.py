"""
Provider Connection Wizard Views
Multi-step wizard for connecting payment API providers
"""

import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View

logger = logging.getLogger(__name__)

from component_updates.integration_paths import INTEGRATIONS_DIR
from component_updates.models import ComponentRegistry
from payment_providers.models import PaymentProviderAccount
from payment_providers.providers.loader import load_provider_manifest
from payment_providers.providers.registry import ProviderRegistry
from payment_providers.utils.encryption import encrypt_credentials
from providers_common.utils import load_manifest_translations, validate_dual_environment_credentials


class WizardSessionMixin:
    """Mixin for managing wizard session data"""

    SESSION_KEY = "payment_provider_wizard_data"

    def get_wizard_data(self):
        """Get wizard data from session"""
        return self.request.session.get(self.SESSION_KEY, {})

    def set_wizard_data(self, data):
        """Set wizard data in session"""
        self.request.session[self.SESSION_KEY] = data
        self.request.session.modified = True

    def update_wizard_data(self, **kwargs):
        """Update wizard data with new values"""
        data = self.get_wizard_data()
        data.update(kwargs)
        self.set_wizard_data(data)

    def clear_wizard_data(self):
        """Clear wizard data from session"""
        if self.SESSION_KEY in self.request.session:
            del self.request.session[self.SESSION_KEY]


@method_decorator(staff_member_required, name="dispatch")
class ProviderWizardStep1View(WizardSessionMixin, View):
    """
    Step 1: Select Provider
    Displays available payment providers from ComponentRegistry
    """

    template_name = "admin/payment_providers/wizard/step1_select.html"

    def get(self, request):
        """Display provider selection"""
        # Clear any existing wizard data when starting fresh
        self.clear_wizard_data()

        # Auto-skip if provider pre-selected from browse page
        provider_slug = request.GET.get("provider")
        if provider_slug:
            try:
                component = ComponentRegistry.objects.get(
                    slug=provider_slug, component_type="payment_provider"
                )
                self.update_wizard_data(
                    component_id=component.id,
                    component_name=component.name,
                    component_slug=component.slug,
                )
                return redirect("payment_providers:wizard_step2")
            except ComponentRegistry.DoesNotExist:
                pass  # Fall through to normal step 1

        # Get all payment provider components
        components = ComponentRegistry.objects.filter(component_type="payment_provider").order_by(
            "name"
        )

        # Split into healthy providers (registry + files present + manifest
        # loads) and broken providers (registry row exists but the on-disk
        # package is missing or unreadable). Broken ones get surfaced in the
        # template so the admin can repair them, instead of silently
        # disappearing from the list — which is what used to happen when a
        # Docker volume reset emptied components_data/.
        from component_updates.integration_paths import INTEGRATIONS_DIR

        provider_data = []
        broken_providers = []

        for component in components:
            provider_dir = INTEGRATIONS_DIR / "payment_provider" / component.slug / "current"
            broken_reason = None

            if not provider_dir.exists():
                broken_reason = _("Provider files missing on disk")
            else:
                try:
                    manifest = load_provider_manifest(provider_dir)
                except Exception as exc:
                    logger.warning(
                        "Could not load manifest for payment_provider '%s' at %s: %s",
                        component.slug,
                        provider_dir,
                        exc,
                    )
                    broken_reason = _("Provider manifest could not be loaded")
                    manifest = None

                if manifest:
                    provider_data.append(
                        {
                            "component": component,
                            "manifest": manifest,
                            "capabilities": manifest.get("capabilities", {}),
                        }
                    )
                elif not broken_reason:
                    broken_reason = _("Provider manifest is empty or invalid")

            if broken_reason:
                logger.warning(
                    "Hiding payment_provider '%s' from wizard: %s",
                    component.slug,
                    broken_reason,
                )
                broken_providers.append(
                    {
                        "component": component,
                        "reason": broken_reason,
                        "expected_dir": str(provider_dir),
                    }
                )

        context = {
            "title": _("Connect Payment Provider - Select Provider"),
            "providers": provider_data,
            "broken_providers": broken_providers,
            "step": 1,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle provider selection"""
        component_id = request.POST.get("component_id")

        if not component_id:
            messages.error(request, _("Please select a provider."))
            return redirect("payment_providers:wizard_step1")

        try:
            component = ComponentRegistry.objects.get(
                id=component_id, component_type="payment_provider"
            )
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _("Invalid provider selected."))
            return redirect("payment_providers:wizard_step1")

        # Store selected component in session
        self.update_wizard_data(
            component_id=component_id,
            component_name=component.name,
            component_slug=component.slug,
        )

        return redirect("payment_providers:wizard_step2")


@method_decorator(staff_member_required, name="dispatch")
class ProviderWizardStep2View(WizardSessionMixin, View):
    """
    Step 2: Setup Instructions
    Shows provider-specific setup instructions from setup_instructions.html
    """

    template_name = "admin/payment_providers/wizard/step2_setup.html"

    def get(self, request):
        """Display setup instructions"""
        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get("component_id")

        if not component_id:
            messages.warning(request, _("Please select a provider first."))
            return redirect("payment_providers:wizard_step1")

        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Get component path
            component_path = INTEGRATIONS_DIR / "payment_provider" / component.slug / "current"
            instructions_file = component_path / "setup_instructions.html"

            setup_instructions = ""
            if instructions_file.exists():
                # Read the setup instructions HTML file
                from django.template import Context, Template
                from django.utils.safestring import mark_safe

                with open(instructions_file, encoding="utf-8") as f:
                    instructions_content = f.read()

                # Render it as a Django template to support {% trans %} tags
                template = Template(instructions_content)
                context = Context({"provider": {"component": component}})
                setup_instructions = mark_safe(template.render(context))

            # Load manifest for signup URL
            manifest = load_provider_manifest(component_path) if component_path.exists() else None
            signup_url = manifest.get("signup_url", "") if manifest else ""

        except Exception as e:
            messages.error(request, _("Error loading provider: %(error)s") % {"error": str(e)})
            return redirect("payment_providers:wizard_step1")

        # Load manifest translations for i18n
        try:
            manifest_translations = load_manifest_translations(component_path)
        except Exception:
            manifest_translations = None

        context = {
            "title": _("Connect Payment Provider - Setup Instructions"),
            "provider": {"component": component, "signup_url": signup_url},
            "setup_instructions": setup_instructions,
            "component_id": component_id,
            "step": 2,
            "manifest_translations": manifest_translations,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle continue to credentials"""
        return redirect("payment_providers:wizard_step3")


@method_decorator(staff_member_required, name="dispatch")
class ProviderWizardStep3View(WizardSessionMixin, View):
    """
    Step 3: Enter Credentials
    Dynamic form based on provider's credential schema
    """

    template_name = "admin/payment_providers/wizard/step3_credentials.html"

    def get(self, request):
        """Display credentials form"""
        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get("component_id")

        if not component_id:
            messages.warning(request, _("Please select a provider first."))
            return redirect("payment_providers:wizard_step1")

        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Get component path and load manifest
            component_path = INTEGRATIONS_DIR / "payment_provider" / component.slug / "current"
            manifest = load_provider_manifest(component_path) if component_path.exists() else None

            if not manifest:
                messages.error(request, _("Could not load provider configuration."))
                return redirect("payment_providers:wizard_step1")

            credential_schema = manifest.get("credential_schema", {})

        except Exception as e:
            messages.error(request, _("Error loading provider: %(error)s") % {"error": str(e)})
            return redirect("payment_providers:wizard_step1")

        # Pre-populate with saved credentials if navigating back
        saved_credentials = wizard_data.get("credentials", {})
        saved_display_name = wizard_data.get("display_name", "")
        saved_checkout_mode = wizard_data.get("checkout_mode", "hosted")

        # Inject saved values into credential_schema for template rendering
        for field_name, field_config in credential_schema.items():
            if field_name in saved_credentials:
                field_config["saved_value"] = saved_credentials[field_name]

        context = {
            "title": _("Connect Payment Provider - Enter Credentials"),
            "provider": {"component": component},
            "credential_schema": credential_schema,
            "component_id": component_id,
            "step": 3,
            "saved_credentials": saved_credentials,
            "saved_display_name": saved_display_name,
            "saved_checkout_mode": saved_checkout_mode,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle credentials submission"""
        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get("component_id")

        if not component_id:
            return redirect("payment_providers:wizard_step1")

        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Get component path and load manifest
            component_path = INTEGRATIONS_DIR / "payment_provider" / component.slug / "current"
            manifest = load_provider_manifest(component_path) if component_path.exists() else None
            credential_schema = manifest.get("credential_schema", {}) if manifest else {}
        except Exception:
            messages.error(request, _("Error loading provider configuration."))
            return redirect("payment_providers:wizard_step1")

        # Validate and collect credentials from POST data
        # Use dual-environment validation for payment providers (supports test + live credentials)
        credentials, errors = validate_dual_environment_credentials(credential_schema, request.POST)

        # Get basic configuration
        display_name = request.POST.get("display_name", "").strip()
        checkout_mode = request.POST.get("checkout_mode", "hosted")

        if not display_name:
            errors.append(_("Display name is required."))

        if errors:
            for error in errors:
                messages.error(request, error)
            return self.get(request)

        # Store credentials and config in session
        self.update_wizard_data(
            credentials=credentials,
            display_name=display_name,
            checkout_mode=checkout_mode,
        )

        return redirect("payment_providers:wizard_step4")


@method_decorator(staff_member_required, name="dispatch")
class ProviderWizardStep4View(WizardSessionMixin, View):
    """
    Step 4: Test Connection
    Tests the provider connection with entered credentials
    """

    template_name = "admin/payment_providers/wizard/step4_test.html"

    def get(self, request):
        """Display test connection page"""
        wizard_data = self.get_wizard_data()

        if not wizard_data.get("component_id") or not wizard_data.get("credentials"):
            messages.warning(request, _("Please complete previous steps first."))
            return redirect("payment_providers:wizard_step1")

        # Handle retry - clear previous test result to re-run
        if request.GET.get("retry"):
            self.update_wizard_data(test_result=None, connection_test_passed=False)
            return redirect("payment_providers:wizard_step4")

        component_id = wizard_data.get("component_id")

        try:
            component = ComponentRegistry.objects.get(id=component_id)
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _("Provider not found."))
            return redirect("payment_providers:wizard_step1")

        context = {
            "title": _("Connect Payment Provider - Test Connection"),
            "provider": {"component": component},
            "component_id": component_id,
            "step": 4,
            "test_result": wizard_data.get("test_result"),
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Perform connection test"""
        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get("component_id")
        credentials = wizard_data.get("credentials", {})

        if not component_id or not credentials:
            return JsonResponse({"success": False, "error": "Missing data"}, status=400)

        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Get provider class from registry
            provider_class = ProviderRegistry.get_provider(component.slug)

            if not provider_class:
                test_result = {
                    "success": False,
                    "error_message": _("Provider implementation not found."),
                }
            else:
                # Create temporary provider instance
                provider = provider_class(credentials=credentials)

                # Test connection
                test_result = provider.test_connection()

                # Normalize keys for template (providers return 'message'/'details',
                # template expects 'error_message'/'error_details')
                if not test_result.get("success"):
                    if "message" in test_result and "error_message" not in test_result:
                        test_result["error_message"] = test_result["message"]
                    if "details" in test_result and "error_details" not in test_result:
                        details = test_result["details"]
                        if isinstance(details, dict):
                            test_result["error_details"] = "\n".join(
                                f"{k}: {v}" for k, v in details.items()
                            )
                        else:
                            test_result["error_details"] = str(details)

            # Store test result in session
            self.update_wizard_data(
                test_result=test_result,
                connection_test_passed=test_result.get("success", False),
            )

            # For AJAX requests, return JSON
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(test_result)

            # For regular POST, redirect back to show results
            return redirect("payment_providers:wizard_step4")

        except Exception as e:
            test_result = {
                "success": False,
                "error_message": str(e),
            }
            self.update_wizard_data(test_result=test_result)

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(test_result, status=500)

            return redirect("payment_providers:wizard_step4")


@method_decorator(staff_member_required, name="dispatch")
class ProviderWizardStep5View(WizardSessionMixin, View):
    """
    Step 5: Configure & Save
    Final configuration and save provider account
    """

    template_name = "admin/payment_providers/wizard/step5_configure.html"

    def get(self, request):
        """Display configuration form"""
        wizard_data = self.get_wizard_data()

        # Verify all required data is present
        if not all(
            [
                wizard_data.get("component_id"),
                wizard_data.get("credentials"),
                wizard_data.get("connection_test_passed"),
            ]
        ):
            messages.warning(request, _("Please complete all previous steps."))
            return redirect("payment_providers:wizard_step1")

        component_id = wizard_data.get("component_id")

        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Load manifest for settings schema
            component_path = INTEGRATIONS_DIR / "payment_provider" / component.slug / "current"
            manifest = load_provider_manifest(component_path) if component_path.exists() else None
            settings_schema = manifest.get("settings_schema", {}) if manifest else {}

            # Generate webhook URL
            webhook_url = request.build_absolute_uri(f"/webhooks/payments/{component.slug}/")

        except ComponentRegistry.DoesNotExist:
            messages.error(request, _("Provider not found."))
            return redirect("payment_providers:wizard_step1")

        context = {
            "title": _("Connect Payment Provider - Configure"),
            "provider": {"component": component},
            "component_id": component_id,
            "settings_schema": settings_schema,
            "webhook_url": webhook_url,
            "form": {
                "is_active": wizard_data.get("is_active", True),
                "is_default": wizard_data.get("is_default", False),
                "sort_order": wizard_data.get("sort_order", 0),
            },
            "step": 5,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Save provider account"""
        wizard_data = self.get_wizard_data()

        # Get configuration from POST
        is_active = request.POST.get("is_active") == "on"
        is_default = request.POST.get("is_default") == "on"
        sort_order = int(request.POST.get("sort_order", 0))

        # Load settings_schema to check field types
        settings_schema = {}
        try:
            component = ComponentRegistry.objects.get(id=wizard_data["component_id"])
            component_path = INTEGRATIONS_DIR / "payment_provider" / component.slug / "current"
            manifest = load_provider_manifest(component_path) if component_path.exists() else None
            settings_schema = manifest.get("settings_schema", {}) if manifest else {}
        except Exception:
            pass  # Will use empty schema, settings will be collected as strings

        # Collect advanced settings
        settings = {}
        for key in request.POST:
            if key.startswith("setting_"):
                setting_name = key.replace("setting_", "")

                # Check if this is a multiselect field
                setting_config = settings_schema.get(setting_name, {})
                if setting_config.get("type") == "multiselect":
                    settings[setting_name] = request.POST.getlist(key)
                else:
                    settings[setting_name] = request.POST.get(key)

        try:
            from django.utils import timezone

            component = ComponentRegistry.objects.get(id=wizard_data["component_id"])
            credentials = wizard_data["credentials"]
            display_name = wizard_data["display_name"]
            checkout_mode = wizard_data["checkout_mode"]

            # Encrypt credentials before storing
            credentials_encrypted = encrypt_credentials(credentials)

            # If setting as default, remove default from others
            if is_default:
                PaymentProviderAccount.objects.filter(is_default=True).update(is_default=False)

            # Create provider account
            provider_account = PaymentProviderAccount.objects.create(
                component=component,
                user=request.user,
                display_name=display_name,
                credentials_encrypted=credentials_encrypted,
                settings=settings,
                checkout_mode=checkout_mode,
                is_active=is_active,
                is_default=is_default,
                sort_order=sort_order,
                connection_status="connected",
                last_tested_at=timezone.now(),
            )

            messages.success(
                request,
                _('Payment provider "%(name)s" connected successfully!') % {"name": display_name},
            )

            # Immediately sync the provider's available payment methods so the
            # account is usable from checkout on the very next request. Without
            # this, the provider's `available_payment_methods` and
            # `enabled_payment_methods` stay empty (`method_sync_status=pending`)
            # and `PaymentMethodFilter` silently drops the provider from the
            # checkout list — the storefront then renders the
            # "Loading payment options…" state forever with nothing to show.
            #
            # Failures here are non-fatal: the wizard completes either way, the
            # merchant just gets a warning so they know to retry the sync from
            # the provider admin (or `manage.py sync_payment_methods`).
            sync_result = None
            try:
                if hasattr(provider_account, "sync_payment_methods"):
                    sync_result = provider_account.sync_payment_methods()
            except Exception as sync_exc:  # noqa: BLE001 — wide on purpose; we never let this raise.
                sync_result = {"success": False, "message": str(sync_exc)}

            if sync_result and not sync_result.get("success"):
                messages.warning(
                    request,
                    _(
                        "Provider was saved but payment methods could not be "
                        "auto-synced (%(error)s). The provider will not appear at "
                        'checkout until methods are synced — try the "Sync methods" '
                        "action on the provider list."
                    )
                    % {"error": sync_result.get("message", "unknown error")},
                )

            # Clear wizard session data
            self.clear_wizard_data()

            # Redirect to provider list
            return redirect("admin:payment_providers_paymentprovideraccount_changelist")

        except Exception as e:
            messages.error(request, _("Error saving provider: %(error)s") % {"error": str(e)})
            return self.get(request)
