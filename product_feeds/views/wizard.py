"""
Installation wizard views for product feed providers.
Pattern follows exchange_rates/views/wizard.py architecture.
"""

import json
from pathlib import Path

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View

from component_updates.integration_paths import INTEGRATIONS_DIR
from component_updates.models import ComponentRegistry
from product_feeds.models import FeedProviderAccount
from product_feeds.providers.registry import ProviderRegistry
from product_feeds.utils.encryption import encrypt_credentials
from providers_common.utils import load_manifest_translations


def load_provider_manifest(provider_path: Path) -> dict:
    """Load manifest.json from provider directory"""
    manifest_file = provider_path / "manifest.json"
    if manifest_file.exists():
        with open(manifest_file) as f:
            return json.load(f)
    return None


class WizardSessionMixin:
    """Mixin for managing wizard session data"""

    SESSION_KEY = "product_feed_wizard"

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
class ProviderBrowseView(View):
    """
    Browse product feed providers.

    Displays:
    - Providers available from update server
    - Locally installed providers from components directory
    - Installation status for each provider
    """

    template_name = "admin/product_feeds/providers/browse.html"

    def get(self, request):
        """Display provider browse page"""
        # Get filter parameters
        has_push_feed = request.GET.get("push_feed")
        has_hosted_feed = request.GET.get("hosted_feed")
        has_api_sync = request.GET.get("api_sync")

        # Try to fetch available providers from update server
        available_from_server = []
        has_update_server = False

        try:
            from component_updates.services import UpdateManager

            update_manager = UpdateManager()
            available_from_server = update_manager.list_available_components(
                component_type="product_feed_provider"
            )
            has_update_server = True
        except Exception as e:
            # If update server fails, we'll fall back to locally installed providers
            print(f"Could not fetch from update server: {e}")

        # Get installed providers for version comparison
        installed_db = {
            p.slug: p.current_version
            for p in ComponentRegistry.objects.filter(component_type="product_feed_provider")
        }

        # Process providers from update server
        all_providers = []

        for provider in available_from_server:
            slug = provider.get("slug")
            latest_version = provider.get("current_version") or provider.get("version")
            manifest = provider.get("manifest", {})

            # Get capabilities
            capabilities = provider.get("capabilities") or manifest.get("capabilities", {})

            # Apply capability filters
            if has_push_feed and not capabilities.get("push_feed"):
                continue
            if has_hosted_feed and not capabilities.get("hosted_feed"):
                continue
            if has_api_sync and not capabilities.get("api_sync"):
                continue

            # Check if installed and compare versions
            is_installed = slug in installed_db
            current_version = installed_db.get(slug, "")
            has_update = False

            if is_installed and current_version and latest_version:
                try:
                    from packaging import version

                    has_update = version.parse(latest_version) > version.parse(current_version)
                except Exception:
                    has_update = False

            provider_data = {
                "slug": slug,
                "name": provider.get("name", ""),
                "description": provider.get("description", ""),
                "version": latest_version,
                "thumbnail_url": provider.get("thumbnail_url", ""),
                "homepage_url": provider.get("homepage_url", ""),
                "documentation_url": provider.get("documentation_url")
                or manifest.get("documentation_url", ""),
                "capabilities": capabilities,
                "feed_formats": manifest.get("feed_formats", []),
                "category": manifest.get("category", ""),
                "is_installed": is_installed,
                "current_version": current_version,
                "latest_version": latest_version,
                "has_update": has_update,
            }

            all_providers.append(provider_data)

        # Count providers
        total_count = len(all_providers)
        push_feed_count = sum(1 for p in all_providers if p["capabilities"].get("push_feed"))
        hosted_feed_count = sum(1 for p in all_providers if p["capabilities"].get("hosted_feed"))
        api_sync_count = sum(1 for p in all_providers if p["capabilities"].get("api_sync"))

        # Prepare provider data for modal (with all manifest data)
        providers_for_modal = []
        for provider_data in all_providers:
            modal_data = {
                "slug": provider_data["slug"],
                "name": provider_data["name"],
                "description": provider_data["description"],
                "thumbnail_url": provider_data["thumbnail_url"],
                "homepage_url": provider_data.get("homepage_url", ""),
                "documentation_url": provider_data.get("documentation_url", ""),
                "capabilities": provider_data["capabilities"],
                "feed_formats": provider_data.get("feed_formats", []),
                "category": provider_data.get("category", ""),
                "is_installed": provider_data["is_installed"],
                "current_version": provider_data.get("current_version", ""),
                "latest_version": provider_data.get("latest_version", ""),
                "has_update": provider_data.get("has_update", False),
                "configure_url": "/admin/product_feeds/feedprovideraccount/",
            }
            providers_for_modal.append(modal_data)

        context = {
            "title": _("Browse Product Feed Providers"),
            "providers": all_providers,
            "providers_json": providers_for_modal,
            "total_count": total_count,
            "push_feed_count": push_feed_count,
            "hosted_feed_count": hosted_feed_count,
            "api_sync_count": api_sync_count,
            "has_push_feed": has_push_feed,
            "has_hosted_feed": has_hosted_feed,
            "has_api_sync": has_api_sync,
            "has_update_server": has_update_server,
        }

        return render(request, self.template_name, context)


@method_decorator(staff_member_required, name="dispatch")
class WizardStep1View(WizardSessionMixin, View):
    """
    Step 1: Select Provider
    Displays available product feed providers from ComponentRegistry
    """

    template_name = "admin/product_feeds/wizard/step1_select.html"

    def get(self, request):
        """Display provider selection"""
        # Clear any existing wizard data when starting fresh
        self.clear_wizard_data()

        # Auto-skip if provider pre-selected from browse page
        provider_slug = request.GET.get("provider")
        if provider_slug:
            try:
                component = ComponentRegistry.objects.get(
                    slug=provider_slug, component_type="product_feed_provider"
                )
                self.update_wizard_data(
                    component_id=component.id,
                    component_name=component.name,
                    component_slug=component.slug,
                )
                return redirect("product_feeds:wizard_step2")
            except ComponentRegistry.DoesNotExist:
                pass  # Fall through to normal step 1

        # Get all product feed provider components
        providers = ComponentRegistry.objects.filter(
            component_type="product_feed_provider"
        ).order_by("name")

        # Load manifests for each provider
        provider_data = []
        for component in providers:
            try:
                # Load from component directory using the actual version
                version = component.current_version or "v1.0.0"
                if not version.startswith("v"):
                    version = f"v{version}"

                provider_dir = INTEGRATIONS_DIR / "product_feed_provider" / component.slug / version

                if provider_dir.exists():
                    manifest = load_provider_manifest(provider_dir)
                    if manifest:
                        # Get logo URL
                        logo_file = manifest.get("logo", {})
                        if isinstance(logo_file, dict):
                            logo_filename = logo_file.get("file", "")
                        else:
                            logo_filename = logo_file if logo_file else ""

                        logo_url = ""
                        if logo_filename:
                            logo_path = provider_dir / logo_filename
                            if logo_path.exists():
                                logo_url = static(
                                    f"product_feed_provider/{component.slug}/current/{logo_filename}"
                                )

                        # Set thumbnail_url on component object
                        component.thumbnail_url = logo_url

                        provider_data.append(
                            {
                                "component": component,
                                "manifest": manifest,
                                "capabilities": manifest.get("capabilities", {}),
                                "feed_formats": manifest.get("feed_formats", []),
                            }
                        )
            except Exception as e:
                # Log but don't fail if manifest can't be loaded
                print(f"Could not load manifest for {component.name}: {e}")

        context = {
            "title": _("Connect Product Feed Provider - Select Provider"),
            "providers": provider_data,
            "step": 1,
            "total_steps": 4,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle provider selection"""
        component_id = request.POST.get("component_id")

        if not component_id:
            messages.error(request, _("Please select a provider."))
            return redirect("product_feeds:wizard_step1")

        try:
            component = ComponentRegistry.objects.get(
                id=component_id, component_type="product_feed_provider"
            )
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _("Invalid provider selected."))
            return redirect("product_feeds:wizard_step1")

        # Store selected component in session
        self.update_wizard_data(
            component_id=component_id,
            component_name=component.name,
            component_slug=component.slug,
        )

        return redirect("product_feeds:wizard_step2")


@method_decorator(staff_member_required, name="dispatch")
class WizardStep2View(WizardSessionMixin, View):
    """
    Step 2: Setup Instructions
    Shows provider-specific setup instructions from setup_instructions.html
    """

    template_name = "admin/product_feeds/wizard/step2_setup.html"

    def get(self, request):
        """Display setup instructions"""
        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get("component_id")

        if not component_id:
            messages.warning(request, _("Please select a provider first."))
            return redirect("product_feeds:wizard_step1")

        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Get component path using the actual version
            version = component.current_version or "v1.0.0"
            if not version.startswith("v"):
                version = f"v{version}"

            component_path = INTEGRATIONS_DIR / "product_feed_provider" / component.slug / version
            instructions_file = component_path / "setup_instructions.html"

            has_instructions = False
            instructions_html = ""

            if instructions_file.exists():
                from django.template import Context, Template
                from django.utils.safestring import mark_safe

                # Read the setup instructions HTML file
                with open(instructions_file, encoding="utf-8") as f:
                    instructions_content = f.read()

                # Render it as a Django template to support {% trans %} tags
                template = Template(instructions_content)
                context = Context({"component": component})
                instructions_html = mark_safe(template.render(context))
                has_instructions = True
            else:
                messages.warning(
                    request,
                    _("Setup instructions not found for %(provider)s. Please contact support.")
                    % {"provider": component.name},
                )

        except Exception as e:
            messages.error(request, _("Error loading provider: %(error)s") % {"error": str(e)})
            return redirect("product_feeds:wizard_step1")

        # Load manifest translations for i18n
        try:
            manifest_translations = load_manifest_translations(component_path)
        except Exception:
            manifest_translations = None

        context = {
            "title": _("Connect Product Feed Provider - Setup Instructions"),
            "component": component,
            "instructions_html": instructions_html,
            "has_instructions": has_instructions,
            "step": 2,
            "total_steps": 4,
            "manifest_translations": manifest_translations,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle continue to configuration"""
        return redirect("product_feeds:wizard_step3")


@method_decorator(staff_member_required, name="dispatch")
class WizardStep3View(WizardSessionMixin, View):
    """
    Step 3: Configure Feed Settings
    Dynamic form based on provider's credential schema + feed settings
    """

    template_name = "admin/product_feeds/wizard/step3_config.html"

    def get(self, request):
        """Display configuration form"""
        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get("component_id")

        if not component_id:
            messages.warning(request, _("Please select a provider first."))
            return redirect("product_feeds:wizard_step1")

        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Get component path using the actual version
            version = component.current_version or "v1.0.0"
            if not version.startswith("v"):
                version = f"v{version}"

            component_path = INTEGRATIONS_DIR / "product_feed_provider" / component.slug / version
            manifest = load_provider_manifest(component_path) if component_path.exists() else None

            if not manifest:
                messages.error(request, _("Could not load provider configuration."))
                return redirect("product_feeds:wizard_step1")

            credential_schema = manifest.get("credential_schema", {})
            signup_url = manifest.get("signup_url", "")
            feed_formats = manifest.get("feed_formats", ["xml", "csv", "json"])
            default_format = manifest.get("default_format", "xml")

            # Build feed format choices
            format_labels = {
                "xml": "XML (Google RSS)",
                "csv": "CSV (Comma-Separated)",
                "json": "JSON",
            }
            feed_format_choices = [
                (fmt, format_labels.get(fmt, fmt.upper())) for fmt in feed_formats
            ]

        except Exception as e:
            messages.error(request, _("Error loading provider: %(error)s") % {"error": str(e)})
            return redirect("product_feeds:wizard_step1")

        context = {
            "title": _("Connect Product Feed Provider - Configure Feed"),
            "component": component,
            "credential_schema": credential_schema,
            "signup_url": signup_url,
            "feed_formats": feed_format_choices,
            "default_format": default_format,
            "step": 3,
            "total_steps": 4,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle configuration submission"""
        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get("component_id")

        if not component_id:
            return redirect("product_feeds:wizard_step1")

        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Get component path using the actual version
            version = component.current_version or "v1.0.0"
            if not version.startswith("v"):
                version = f"v{version}"

            component_path = INTEGRATIONS_DIR / "product_feed_provider" / component.slug / version
            manifest = load_provider_manifest(component_path) if component_path.exists() else None
            credential_schema = manifest.get("credential_schema", {}) if manifest else {}
        except Exception:
            messages.error(request, _("Error loading provider configuration."))
            return redirect("product_feeds:wizard_step1")

        # Collect credentials from POST data
        credentials = {}
        errors = []

        for field_name, field_config in credential_schema.items():
            value = request.POST.get(field_name, "").strip()

            # Check required fields
            if field_config.get("required", False) and not value:
                errors.append(
                    _("%(field)s is required.") % {"field": field_config.get("label", field_name)}
                )
            elif value:  # Only add non-empty values
                credentials[field_name] = value

        # Get account name
        account_name = request.POST.get("account_name", "").strip()
        if not account_name:
            errors.append(_("Feed Name is required."))

        if errors:
            for error in errors:
                messages.error(request, error)
            return self.get(request)

        # Get feed configuration
        feed_config = {
            "sync_interval": request.POST.get("sync_interval", "daily"),
            "feed_format": request.POST.get("feed_format", "xml"),
            "is_active": request.POST.get("is_active") == "on",
        }

        # Store in session
        self.update_wizard_data(
            credentials=credentials,
            account_name=account_name,
            feed_config=feed_config,
        )

        return redirect("product_feeds:wizard_step4")


@method_decorator(staff_member_required, name="dispatch")
class WizardStep4View(WizardSessionMixin, View):
    """
    Step 4: Test Connection & Save
    Tests the provider connection with entered credentials and saves if successful
    """

    template_name = "admin/product_feeds/wizard/step4_test.html"

    def get(self, request):
        """Display test connection page"""
        wizard_data = self.get_wizard_data()

        if not wizard_data.get("component_id") or not wizard_data.get("credentials"):
            messages.warning(request, _("Please complete previous steps first."))
            return redirect("product_feeds:wizard_step1")

        component_id = wizard_data.get("component_id")

        try:
            component = ComponentRegistry.objects.get(id=component_id)
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _("Provider not found."))
            return redirect("product_feeds:wizard_step1")

        context = {
            "title": _("Connect Product Feed Provider - Test Connection"),
            "component": component,
            "step": 4,
            "total_steps": 4,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Perform connection test and save if successful"""
        action = request.POST.get("action", "test")

        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get("component_id")
        component_slug = wizard_data.get("component_slug")
        credentials = wizard_data.get("credentials", {})
        account_name = wizard_data.get("account_name", "")
        feed_config = wizard_data.get("feed_config", {})

        if not component_id or not credentials:
            return JsonResponse({"success": False, "error": "Missing data"}, status=400)

        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Get provider class from registry
            provider_class = ProviderRegistry.get_provider(component_slug)

            if not provider_class:
                return JsonResponse(
                    {"success": False, "error": _("Provider implementation not found.")}, status=404
                )

            if action == "test":
                # Test connection only
                try:
                    provider = provider_class(credentials=credentials)
                    test_result = provider.test_connection()

                    # Add preview data if test succeeded
                    if test_result.get("success"):
                        # Get product count for preview
                        from catalog.models import Product

                        product_count = Product.objects.filter(is_active=True).count()
                        from catalog.models import Category

                        category_count = Category.objects.filter(is_active=True).count()

                        test_result["preview"] = {
                            "product_count": product_count,
                            "category_count": category_count,
                            "format": feed_config.get("feed_format", "XML").upper(),
                        }

                    # Store test result in session
                    self.update_wizard_data(
                        connection_test_passed=test_result.get("success", False),
                        connection_test_message=test_result.get("message", ""),
                        connection_test_details=test_result.get("details", {}),
                    )

                    return JsonResponse(test_result)
                except Exception as e:
                    return JsonResponse({"success": False, "error": str(e)}, status=500)

            elif action == "save":
                # Save provider account
                try:
                    # Get site from Django sites framework
                    from django.contrib.sites.models import Site

                    site = Site.objects.get_current()
                    if not site:
                        return JsonResponse(
                            {"success": False, "error": _("Site not configured.")}, status=400
                        )

                    # Create provider instance to test first
                    provider = provider_class(credentials=credentials)
                    test_result = provider.test_connection()

                    if not test_result.get("success"):
                        return JsonResponse(
                            {
                                "success": False,
                                "error": test_result.get("message", _("Connection test failed")),
                            },
                            status=400,
                        )

                    # Encrypt credentials
                    encrypted_credentials = encrypt_credentials(credentials)

                    # Check if this is the first provider
                    is_first_provider = not FeedProviderAccount.objects.exists()

                    # Create provider account
                    with transaction.atomic():
                        provider_account = FeedProviderAccount.objects.create(
                            site=site,
                            component=component,
                            name=account_name or component.name,
                            credentials=encrypted_credentials,
                            config=feed_config,
                            is_active=feed_config.get("is_active", True),
                            is_primary=is_first_provider,  # Auto-set first provider as primary
                            sync_status="pending",
                        )

                    # Clear wizard data
                    self.clear_wizard_data()

                    return JsonResponse(
                        {
                            "success": True,
                            "message": _("Product feed provider connected successfully!"),
                            "redirect_url": reverse(
                                "admin:product_feeds_feedprovideraccount_change",
                                args=[provider_account.id],
                            ),
                        }
                    )

                except Exception as e:
                    return JsonResponse({"success": False, "error": str(e)}, status=500)

            else:
                return JsonResponse({"success": False, "error": "Invalid action"}, status=400)

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)


# Admin AJAX endpoints for card actions


@staff_member_required
def sync_feed_ajax(request, account_id):
    """AJAX endpoint to trigger feed sync"""
    get_object_or_404(FeedProviderAccount, id=account_id)

    try:
        from product_feeds.tasks import sync_feed

        sync_feed.delay(account_id)

        return JsonResponse({"success": True, "message": _("Feed sync started")})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@staff_member_required
def download_feed(request, account_id):
    """Download the latest generated feed"""
    from django.http import HttpResponse

    account = get_object_or_404(FeedProviderAccount, id=account_id)

    # Get latest feed
    feed = account.feeds.order_by("-generated_at").first()
    if not feed:
        return JsonResponse({"success": False, "message": _("No feed available")}, status=404)

    # Get content
    content = feed.get_content()

    # Create response with appropriate content type
    response = HttpResponse(content, content_type=feed.get_content_type())
    response["Content-Disposition"] = (
        f'attachment; filename="{account.component.slug}_feed.{feed.feed_format}"'
    )

    # Track download
    feed.increment_download()

    return response


@staff_member_required
def test_connection_ajax(request, account_id):
    """AJAX endpoint to test provider connection"""
    account = get_object_or_404(FeedProviderAccount, id=account_id)

    try:
        provider = account.get_provider_instance()
        result = provider.test_connection()

        return JsonResponse(
            {
                "success": result.get("success", False),
                "message": result.get("message", ""),
                "details": result.get("details", {}),
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@staff_member_required
def toggle_account_ajax(request, account_id):
    """AJAX endpoint to toggle account active status"""
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "POST required"}, status=405)

    account = get_object_or_404(FeedProviderAccount, id=account_id)

    try:
        data = json.loads(request.body)
        is_active = data.get("is_active", not account.is_active)
    except (json.JSONDecodeError, TypeError):
        is_active = not account.is_active

    account.is_active = is_active
    account.save(update_fields=["is_active", "updated_at"])

    status_text = _("enabled") if is_active else _("disabled")
    return JsonResponse(
        {
            "success": True,
            "message": f"{account.name} {status_text}",
            "is_active": account.is_active,
        }
    )


@staff_member_required
def set_primary_ajax(request, account_id):
    """AJAX endpoint to set account as primary"""
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "POST required"}, status=405)

    account = get_object_or_404(FeedProviderAccount, id=account_id)

    # Unset other primary accounts for this site
    FeedProviderAccount.objects.filter(site=account.site, is_primary=True).exclude(
        id=account.id
    ).update(is_primary=False)

    account.is_primary = True
    account.save(update_fields=["is_primary", "updated_at"])

    return JsonResponse(
        {"success": True, "message": f"{account.name} set as primary", "is_primary": True}
    )


@staff_member_required
def delete_account_ajax(request, account_id):
    """AJAX endpoint to delete account"""
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "POST required"}, status=405)

    account = get_object_or_404(FeedProviderAccount, id=account_id)
    account_name = account.name

    try:
        account.delete()
        return JsonResponse({"success": True, "message": f"{account_name} deleted successfully"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@staff_member_required
def bulk_action_ajax(request):
    """AJAX endpoint for bulk actions on accounts"""
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "POST required"}, status=405)

    try:
        data = json.loads(request.body)
        action = data.get("action")
        provider_ids = data.get("provider_ids", [])
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

    if not action or not provider_ids:
        return JsonResponse(
            {"success": False, "message": "Missing action or provider_ids"}, status=400
        )

    accounts = FeedProviderAccount.objects.filter(id__in=provider_ids)
    count = accounts.count()

    if action == "enable":
        accounts.update(is_active=True)
        message = f"{count} feed(s) enabled"
    elif action == "disable":
        accounts.update(is_active=False)
        message = f"{count} feed(s) disabled"
    elif action == "set_primary":
        if count == 1:
            account = accounts.first()
            FeedProviderAccount.objects.filter(site=account.site, is_primary=True).exclude(
                id=account.id
            ).update(is_primary=False)
            account.is_primary = True
            account.save(update_fields=["is_primary"])
            message = f"{account.name} set as primary"
        else:
            return JsonResponse(
                {"success": False, "message": "Can only set one primary"}, status=400
            )
    elif action == "sync_feeds":
        from product_feeds.tasks import sync_feed

        for account in accounts:
            sync_feed.delay(account.id)
        message = f"Sync started for {count} feed(s)"
    elif action == "delete":
        list(accounts.values_list("name", flat=True))
        accounts.delete()
        message = f"Deleted {count} feed(s)"
    else:
        return JsonResponse({"success": False, "message": f"Unknown action: {action}"}, status=400)

    return JsonResponse({"success": True, "message": message})


@staff_member_required
def install_provider_ajax(request, provider_slug):
    """
    AJAX endpoint to install a provider from update server.

    POST to install provider from update server.
    Returns JSON with success status and redirect URL.
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)

    # Check if already installed
    try:
        component = ComponentRegistry.objects.get(
            slug=provider_slug, component_type="product_feed_provider"
        )

        # Provider is already installed, redirect to wizard to configure
        from django.urls import reverse

        return JsonResponse(
            {
                "success": True,
                "already_installed": True,
                "message": _("Provider is already installed. Configure it now."),
                "redirect_url": reverse("product_feeds:wizard_step1"),
            }
        )
    except ComponentRegistry.DoesNotExist:
        pass  # Not installed, proceed with installation

    # Install provider from update server
    try:
        from django.urls import reverse

        from component_updates.services import UpdateManager

        update_manager = UpdateManager()

        # Get available providers from update server
        available_providers = update_manager.list_available_components(
            component_type="product_feed_provider"
        )

        # Find the requested provider
        provider_info = None
        for provider in available_providers:
            if provider.get("slug") == provider_slug:
                provider_info = provider
                break

        if not provider_info:
            return JsonResponse(
                {"success": False, "error": _("Provider not found on update server.")}, status=404
            )

        # Get the latest version
        latest_version = provider_info.get("current_version") or provider_info.get("version")
        provider_name = provider_info.get("name", provider_slug)
        provider_description = provider_info.get("description", "")

        if not latest_version:
            return JsonResponse(
                {"success": False, "error": _("Could not determine provider version.")}, status=400
            )

        # Create ComponentRegistry entry
        from django.db import transaction

        with transaction.atomic():
            # Create the component registry entry
            component = ComponentRegistry.objects.create(
                slug=provider_slug,
                name=provider_name,
                description=provider_description,
                component_type="product_feed_provider",
                current_version=latest_version,
            )

            # Download the package
            try:
                package_path = update_manager.download_component(component, latest_version)
            except Exception as e:
                component.delete()  # Rollback component creation
                return JsonResponse(
                    {
                        "success": False,
                        "error": _("Failed to download provider: %(error)s") % {"error": str(e)},
                    },
                    status=500,
                )

            # Install the package
            try:
                update_manager._install_package(component, package_path, latest_version)
            except Exception as e:
                component.delete()  # Rollback component creation
                return JsonResponse(
                    {
                        "success": False,
                        "error": _("Failed to install provider: %(error)s") % {"error": str(e)},
                    },
                    status=500,
                )

            # Create 'current' symlink to the installed version
            try:
                provider_base_dir = INTEGRATIONS_DIR / "product_feed_provider" / provider_slug
                current_link = provider_base_dir / "current"
                version_dir = (
                    f"v{latest_version}" if not latest_version.startswith("v") else latest_version
                )

                # Remove existing symlink if it exists
                if current_link.exists() or current_link.is_symlink():
                    current_link.unlink()

                # Create new symlink
                current_link.symlink_to(version_dir)

                # Reload providers to make the new provider available
                ProviderRegistry.reload_providers()
            except Exception as e:
                # Don't fail the installation if symlink creation fails, just log it
                print(f"Warning: Could not create symlink for {provider_slug}: {e}")

        return JsonResponse(
            {
                "success": True,
                "message": _('Provider "%(name)s" installed successfully! Configure it now.')
                % {"name": provider_name},
                "redirect_url": reverse("product_feeds:wizard_step1"),
            }
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
def update_provider_ajax(request, provider_slug):
    """
    Update an existing provider to the latest version
    """
    from django.db import transaction
    from django.urls import reverse

    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)

    try:
        # Get the existing component
        try:
            component = ComponentRegistry.objects.get(
                slug=provider_slug, component_type="product_feed_provider"
            )
        except ComponentRegistry.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": _("Provider not installed.")}, status=404
            )

        # Get update server info
        from component_updates.services import UpdateManager

        update_manager = UpdateManager()

        try:
            available_from_server = update_manager.list_available_components(
                component_type="product_feed_provider"
            )
        except Exception as e:
            return JsonResponse(
                {
                    "success": False,
                    "error": _("Could not connect to update server: %(error)s") % {"error": str(e)},
                },
                status=500,
            )

        # Find this provider on update server
        provider_info = None
        for provider in available_from_server:
            if provider.get("slug") == provider_slug:
                provider_info = provider
                break

        if not provider_info:
            return JsonResponse(
                {"success": False, "error": _("Provider not found on update server.")}, status=404
            )

        # Get the latest version
        latest_version = provider_info.get("current_version") or provider_info.get("version")
        provider_name = provider_info.get("name", provider_slug)

        if not latest_version:
            return JsonResponse(
                {"success": False, "error": _("Could not determine latest version.")}, status=400
            )

        # Check if already up to date
        current_version = component.current_version
        if current_version == latest_version:
            return JsonResponse(
                {
                    "success": True,
                    "message": _('Provider "%(name)s" is already up to date (v%(version)s).')
                    % {"name": provider_name, "version": latest_version},
                    "redirect_url": reverse("product_feeds:provider_browse"),
                }
            )

        # Download and install the update
        with transaction.atomic():
            # Download the package
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

            # Install the package
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

            # Update the 'current' symlink to point to the new version
            try:
                provider_base_dir = INTEGRATIONS_DIR / "product_feed_provider" / provider_slug
                current_link = provider_base_dir / "current"
                version_dir = (
                    f"v{latest_version}" if not latest_version.startswith("v") else latest_version
                )

                # Remove existing symlink if it exists
                if current_link.exists() or current_link.is_symlink():
                    current_link.unlink()

                # Create new symlink
                current_link.symlink_to(version_dir)

                # Reload providers to make the updated provider available
                ProviderRegistry.reload_providers()
            except Exception as e:
                # Don't fail the update if symlink creation fails, just log it
                print(f"Warning: Could not update symlink for {provider_slug}: {e}")

            # Update component version
            component.current_version = latest_version
            component.save()

        return JsonResponse(
            {
                "success": True,
                "message": _('Provider "%(name)s" updated successfully to v%(version)s!')
                % {"name": provider_name, "version": latest_version},
                "redirect_url": reverse("product_feeds:provider_browse"),
            }
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
def filter_sync_logs(request):
    """
    AJAX endpoint for filtering sync logs.
    Returns filtered log list as HTML with count.
    """
    from django.db.models import Q
    from django.template.loader import render_to_string

    from product_feeds.models import FeedSyncLog

    # Ensure this is an AJAX request
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Get filter parameters
    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()
    sync_type = request.GET.get("sync_type", "").strip()
    account = request.GET.get("account", "").strip()

    # Build query with select_related for performance
    logs = FeedSyncLog.objects.select_related("account")

    # Apply search filter
    if search:
        logs = logs.filter(Q(account__name__icontains=search) | Q(error_message__icontains=search))

    # Apply status filter
    if status:
        logs = logs.filter(status=status)

    # Apply sync_type filter
    if sync_type:
        logs = logs.filter(sync_type=sync_type)

    # Apply account filter
    if account:
        logs = logs.filter(account_id=account)

    # Order by most recent
    logs = logs.order_by("-started_at")

    # Check if there are running syncs
    has_running = logs.filter(status="running").exists()

    # Render partial template
    html = render_to_string(
        "admin/product_feeds/feedsynclog/partials/log_cards.html",
        {"logs": logs, "request": request},
    )

    return JsonResponse({"html": html, "count": logs.count(), "has_running": has_running})
