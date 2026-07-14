"""
License Provider Connection Wizard Views
Multi-step wizard for connecting to external license management providers
"""

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View

from catalog.models import LicenseProvider
from catalog.providers.registry import LicenseProviderRegistry
from providers_common.utils import load_manifest_translations, validate_credential_fields


class WizardSessionMixin:
    """Mixin for managing wizard session data"""

    SESSION_KEY = "license_provider_wizard_data"

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
    Step 1: Select Provider Type
    Displays available license provider types
    """

    template_name = "admin/catalog/licenseprovider/wizard/step1_select.html"

    def get(self, request):
        """Display provider selection"""
        # Clear any existing wizard data when starting fresh
        self.clear_wizard_data()

        # Get all available providers from registry
        LicenseProviderRegistry.discover_providers()
        available_providers = LicenseProviderRegistry.list_providers()

        context = {
            "title": _("Connect License Provider - Select Provider"),
            "providers": available_providers,
            "step": 1,
            "total_steps": 4,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle provider selection"""
        provider_key = request.POST.get("provider_key")

        if not provider_key:
            messages.error(request, _("Please select a provider."))
            return redirect("catalog_admin:license_provider_wizard_step1")

        # Validate provider exists
        provider_class = LicenseProviderRegistry.get_provider(provider_key)
        if not provider_class:
            messages.error(request, _("Invalid provider selected."))
            return redirect("catalog_admin:license_provider_wizard_step1")

        # Store selected provider in session
        self.update_wizard_data(
            provider_key=provider_key,
            provider_name=provider_class.provider_name,
        )

        return redirect("catalog_admin:license_provider_wizard_step2")


@method_decorator(staff_member_required, name="dispatch")
class ProviderWizardStep2View(WizardSessionMixin, View):
    """
    Step 2: Setup Instructions
    Shows provider-specific setup instructions
    """

    template_name = "admin/catalog/licenseprovider/wizard/step2_setup.html"

    def get(self, request):
        """Display setup instructions"""
        wizard_data = self.get_wizard_data()
        provider_key = wizard_data.get("provider_key")

        if not provider_key:
            messages.warning(request, _("Please select a provider first."))
            return redirect("catalog_admin:license_provider_wizard_step1")

        provider_class = LicenseProviderRegistry.get_provider(provider_key)
        if not provider_class:
            messages.error(request, _("Provider not found."))
            return redirect("catalog_admin:license_provider_wizard_step1")

        # Get setup instructions from provider
        setup_instructions = self._get_setup_instructions(provider_key)

        # Load manifest translations for i18n (only for component-based providers)
        manifest_translations = None
        try:
            if hasattr(provider_class, "_component_path") and provider_class._component_path:
                manifest_translations = load_manifest_translations(provider_class._component_path)
        except Exception:
            manifest_translations = None

        context = {
            "title": _("Connect License Provider - Setup Instructions"),
            "provider_name": provider_class.provider_name,
            "provider_key": provider_key,
            "instructions_html": setup_instructions,
            "step": 2,
            "total_steps": 4,
            "manifest_translations": manifest_translations,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle continue to credentials"""
        # Just continue to next step - no form data to process
        return redirect("catalog_admin:license_provider_wizard_step3")

    def _get_setup_instructions(self, provider_key):
        """Get HTML setup instructions for provider"""
        from django.utils.safestring import mark_safe

        # Get provider class to check if it's a component
        provider_class = LicenseProviderRegistry.get_provider(provider_key)

        # Try to load from component first
        if provider_class and hasattr(provider_class, "_component_path"):
            component_path = provider_class._component_path
            setup_file = component_path / "setup_instructions.html"

            if setup_file.exists():
                try:
                    with open(setup_file, encoding="utf-8") as f:
                        return mark_safe(f.read())
                except Exception as e:
                    # Log error and fall back to hardcoded instructions
                    import logging

                    logger = logging.getLogger(__name__)
                    logger.error(
                        f"Failed to load setup instructions from component {provider_key}: {e}"
                    )

        # Fallback to hardcoded instructions for built-in providers or if component file not found
        instructions = {
            "spwig_server": _("""
                <h3>Spwig Built-in License Server</h3>
                <p>Spwig's built-in license management server is fully-managed and requires no external setup!</p>
                <ol>
                    <li>In the next step, you'll enter your Spwig Built-in License Server credentials</li>
                    <li>If you don't have an account yet, sign up at: <a href="https://licenses.spwig.com" target="_blank">licenses.spwig.com</a></li>
                    <li>After signing up, you'll receive your Account ID and API Key</li>
                </ol>
                <div class="alert alert-info">
                    <strong>Recommended:</strong> The built-in license server provides the easiest integration with full feature support.
                </div>
            """),
            "keygen": _("""
                <h3>Keygen.sh Setup</h3>
                <ol>
                    <li>Sign up for a Keygen.sh account at <a href="https://keygen.sh" target="_blank">keygen.sh</a></li>
                    <li>Create a new product in your Keygen dashboard</li>
                    <li>Create a policy for your product (defines license terms)</li>
                    <li>Generate a Product API Token: Settings → Tokens → Create Product Token</li>
                    <li>Note your Account ID from the URL: app.keygen.sh/accounts/<strong>YOUR_ACCOUNT_ID</strong></li>
                </ol>
                <p>You'll need: <strong>Account ID</strong> and <strong>Product API Token</strong></p>
            """),
            "licensespring": _("""
                <h3>License Spring Setup</h3>
                <ol>
                    <li>Sign up for License Spring at <a href="https://licensespring.com" target="_blank">licensespring.com</a></li>
                    <li>Log in to your License Spring dashboard</li>
                    <li>Create a new product</li>
                    <li>Get your Management API Key from: Account Settings → API Keys</li>
                    <li>Get your Shared Key from: Products → Your Product → SDK</li>
                    <li>Note your Product Code</li>
                </ol>
                <p>You'll need: <strong>Management API Key</strong>, <strong>Shared Key</strong>, and <strong>Product Code</strong></p>
            """),
            "cryptlex": _("""
                <h3>Cryptlex Setup</h3>
                <ol>
                    <li>Sign up for Cryptlex at <a href="https://cryptlex.com" target="_blank">cryptlex.com</a></li>
                    <li>Log in to your Cryptlex dashboard</li>
                    <li>Create a new product</li>
                    <li>Generate a Personal Access Token: Profile → Access Tokens → Create Token</li>
                    <li>Note your Account ID and Product ID</li>
                </ol>
                <p>You'll need: <strong>Access Token</strong>, <strong>Product ID</strong>, and <strong>Account ID</strong></p>
            """),
            "custom": _("""
                <h3>Custom API Setup</h3>
                <p>This option allows you to integrate with your own license server.</p>
                <div class="alert alert-warning">
                    <strong>Requirements:</strong> Your license server must implement the required REST API endpoints.
                    <a href="/docs/custom-license-api/" target="_blank">View API specification</a>
                </div>
                <ol>
                    <li>Ensure your license server is accessible via HTTPS</li>
                    <li>Prepare your API base URL (e.g., https://licenses.yoursite.com/api)</li>
                    <li>Prepare your authentication credentials</li>
                    <li>Map your API endpoints to Spwig operations</li>
                </ol>
                <p>You'll need: <strong>API Base URL</strong> and <strong>Authentication Credentials</strong></p>
            """),
        }

        return mark_safe(instructions.get(provider_key, _("No setup instructions available.")))


@method_decorator(staff_member_required, name="dispatch")
class ProviderWizardStep3View(WizardSessionMixin, View):
    """
    Step 3: Enter Credentials
    Dynamic form based on provider's credential schema
    """

    template_name = "admin/catalog/licenseprovider/wizard/step3_credentials.html"

    def get(self, request):
        """Display credentials form"""
        wizard_data = self.get_wizard_data()
        provider_key = wizard_data.get("provider_key")

        if not provider_key:
            messages.warning(request, _("Please select a provider first."))
            return redirect("catalog_admin:license_provider_wizard_step1")

        provider_class = LicenseProviderRegistry.get_provider(provider_key)
        if not provider_class:
            messages.error(request, _("Provider not found."))
            return redirect("catalog_admin:license_provider_wizard_step1")

        # Get credential schema from provider
        # Create a temporary instance just to get schema
        temp_instance = provider_class(provider=None)
        credential_schema = temp_instance.credential_schema

        context = {
            "title": _("Connect License Provider - Enter Credentials"),
            "provider_name": provider_class.provider_name,
            "provider_key": provider_key,
            "credential_schema": credential_schema,
            "step": 3,
            "total_steps": 4,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle credentials submission"""
        wizard_data = self.get_wizard_data()
        provider_key = wizard_data.get("provider_key")

        if not provider_key:
            return redirect("catalog_admin:license_provider_wizard_step1")

        provider_class = LicenseProviderRegistry.get_provider(provider_key)
        if not provider_class:
            messages.error(request, _("Provider not found."))
            return redirect("catalog_admin:license_provider_wizard_step1")

        # Get credential schema
        temp_instance = provider_class(provider=None)
        credential_schema = temp_instance.credential_schema

        # Validate and collect credentials from POST data
        all_fields, errors = validate_credential_fields(credential_schema, request.POST)

        # Additional processing: JSON parsing and secret/config separation
        credentials = {}
        config = {}
        for field_name, field_config in credential_schema.items():
            value = all_fields.get(field_name)
            if value is None or (isinstance(value, str) and not value):
                continue

            # Parse JSON fields (like endpoint_mapping)
            if field_config.get("type") == "json" and isinstance(value, str):
                try:
                    import json

                    value = json.loads(value)
                except json.JSONDecodeError:
                    field_title = field_config.get("title", field_name)
                    errors.append(_("%(field)s must be valid JSON.") % {"field": field_title})
                    continue

            # Store in appropriate dict based on field type
            if field_config.get("secret", False):
                credentials[field_name] = value
            else:
                config[field_name] = value

        if errors:
            for error in errors:
                messages.error(request, error)
            return self.get(request)

        # Get optional provider name from form
        provider_name = request.POST.get("provider_name", "").strip()
        if not provider_name:
            provider_name = provider_class.provider_name

        # Store credentials and config in session
        self.update_wizard_data(credentials=credentials, config=config, provider_name=provider_name)

        return redirect("catalog_admin:license_provider_wizard_step4")


@method_decorator(staff_member_required, name="dispatch")
class ProviderWizardStep4View(WizardSessionMixin, View):
    """
    Step 4: Test Connection & Save
    Tests the provider connection with entered credentials and saves if successful
    """

    template_name = "admin/catalog/licenseprovider/wizard/step4_test.html"

    def get(self, request):
        """Display test connection page"""
        wizard_data = self.get_wizard_data()

        if not wizard_data.get("provider_key") or not wizard_data.get("credentials"):
            messages.warning(request, _("Please complete previous steps first."))
            return redirect("catalog_admin:license_provider_wizard_step1")

        provider_key = wizard_data.get("provider_key")
        provider_class = LicenseProviderRegistry.get_provider(provider_key)

        if not provider_class:
            messages.error(request, _("Provider not found."))
            return redirect("catalog_admin:license_provider_wizard_step1")

        context = {
            "title": _("Connect License Provider - Test Connection"),
            "provider_name": provider_class.provider_name,
            "provider_key": provider_key,
            "step": 4,
            "total_steps": 4,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Perform connection test and save if successful"""
        action = request.POST.get("action", "test")

        wizard_data = self.get_wizard_data()
        provider_key = wizard_data.get("provider_key")
        credentials = wizard_data.get("credentials", {})
        config = wizard_data.get("config", {})
        provider_name = wizard_data.get("provider_name", "")

        if not provider_key or not credentials:
            return JsonResponse({"success": False, "error": "Missing data"}, status=400)

        provider_class = LicenseProviderRegistry.get_provider(provider_key)
        if not provider_class:
            return JsonResponse({"success": False, "error": _("Provider not found.")}, status=404)

        if action == "test":
            # Test connection only
            try:
                # Merge all credentials into config for adapter
                temp_config = {**config, **credentials}

                # Create temporary LicenseProvider for testing
                temp_provider = LicenseProvider(
                    provider_type=provider_key,
                    name=provider_name,
                    api_key=credentials.get(
                        "api_key",
                        credentials.get(
                            "api_token",
                            credentials.get("access_token", credentials.get("auth_token", "")),
                        ),
                    ),
                    api_secret=credentials.get("api_secret", credentials.get("auth_secret", "")),
                    api_endpoint=config.get("api_endpoint", ""),
                    provider_config=temp_config,  # Pass merged config to the model field
                )

                # Instantiate adapter with temp provider
                adapter = provider_class(temp_provider)
                test_result = adapter.test_connection()

                # Store test result in session
                self.update_wizard_data(
                    connection_test_passed=test_result.get("success", False),
                    connection_test_message=test_result.get("message", ""),
                )

                return JsonResponse(test_result)
            except Exception as e:
                return JsonResponse({"success": False, "error": str(e)}, status=500)

        elif action == "save":
            # Save provider
            try:
                # Merge all credentials into config for adapter
                temp_config = {**config, **credentials}

                # Test connection first
                temp_provider = LicenseProvider(
                    provider_type=provider_key,
                    name=provider_name,
                    api_key=credentials.get(
                        "api_key",
                        credentials.get(
                            "api_token",
                            credentials.get("access_token", credentials.get("auth_token", "")),
                        ),
                    ),
                    api_secret=credentials.get("api_secret", credentials.get("auth_secret", "")),
                    api_endpoint=config.get("api_endpoint", ""),
                    provider_config=temp_config,
                )

                adapter = provider_class(temp_provider)
                test_result = adapter.test_connection()

                if not test_result.get("success"):
                    return JsonResponse(
                        {
                            "success": False,
                            "error": test_result.get("error", _("Connection test failed")),
                        },
                        status=400,
                    )

                # Create provider
                with transaction.atomic():
                    provider = LicenseProvider.objects.create(
                        provider_type=provider_key,
                        name=provider_name,
                        api_key=credentials.get(
                            "api_key",
                            credentials.get(
                                "api_token",
                                credentials.get("access_token", credentials.get("auth_token", "")),
                            ),
                        ),
                        api_secret=credentials.get(
                            "api_secret", credentials.get("auth_secret", "")
                        ),
                        api_endpoint=config.get("api_endpoint", ""),
                        webhook_secret="",  # Can be set later if needed
                        provider_config=temp_config,  # Merged config with all settings
                        is_active=True,
                        sync_on_order=True,  # Sync license to provider when order is placed
                        connection_status="connected",
                    )

                # Clear wizard data
                self.clear_wizard_data()

                return JsonResponse(
                    {
                        "success": True,
                        "message": _("Provider connected successfully!"),
                        "redirect_url": f"/admin/catalog/licenseprovider/{provider.id}/change/",
                    }
                )

            except Exception as e:
                return JsonResponse({"success": False, "error": str(e)}, status=500)

        else:
            return JsonResponse({"success": False, "error": "Invalid action"}, status=400)
