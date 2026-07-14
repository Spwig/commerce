"""
Installation wizard views for social connector providers.
Implements OAuth 2.0 flow for connecting social media accounts.
"""

import logging
import secrets
from pathlib import Path

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.sites.models import Site
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View

from blog.models import SocialConnectorAccount
from component_updates.models import ComponentRegistry
from providers_common.utils import load_manifest_translations

logger = logging.getLogger(__name__)


class WizardSessionMixin:
    """Mixin for managing wizard session data"""

    SESSION_KEY = "social_connector_wizard"

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


def get_oauth_redirect_uri(request):
    """Build the OAuth callback URI"""
    return request.build_absolute_uri(reverse("blog_admin:oauth_callback"))


@method_decorator(staff_member_required, name="dispatch")
class ProviderBrowseView(View):
    """
    Browse social connector providers.

    Displays:
    - Providers available from update server
    - Locally installed providers from components directory
    - Installation status for each provider
    """

    template_name = "admin/blog/social_connectors/providers/browse.html"

    def get(self, request):
        """Display provider browse page"""
        # Try to fetch available providers from update server
        available_from_server = []
        has_update_server = False

        try:
            from component_updates.services import UpdateManager

            update_manager = UpdateManager()
            available_from_server = update_manager.list_available_components(
                component_type="social_connector_provider"
            )
            has_update_server = True
        except Exception as e:
            print(f"Could not fetch from update server: {e}")

        # Get installed providers for version comparison
        installed_db = {
            p.slug: p.current_version
            for p in ComponentRegistry.objects.filter(component_type="social_connector_provider")
        }

        # Process providers from update server
        all_providers = []

        for provider in available_from_server:
            slug = provider.get("slug")
            latest_version = provider.get("current_version") or provider.get("version")
            manifest = provider.get("manifest", {})

            # Get capabilities
            capabilities = provider.get("capabilities") or manifest.get("capabilities", {})

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
                or manifest.get("api_docs_url", ""),
                "capabilities": capabilities,
                "character_limit": manifest.get("character_limit"),
                "is_installed": is_installed,
                "current_version": current_version,
                "latest_version": latest_version,
                "has_update": has_update,
            }

            all_providers.append(provider_data)

        # Prepare provider data for modal
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
                "character_limit": provider_data.get("character_limit"),
                "is_installed": provider_data["is_installed"],
                "current_version": provider_data.get("current_version", ""),
                "latest_version": provider_data.get("latest_version", ""),
                "has_update": provider_data.get("has_update", False),
            }
            providers_for_modal.append(modal_data)

        context = {
            "title": _("Browse Social Connector Providers"),
            "providers": all_providers,
            "providers_json": providers_for_modal,
            "total_count": len(all_providers),
            "has_update_server": has_update_server,
        }

        return render(request, self.template_name, context)


@method_decorator(staff_member_required, name="dispatch")
class WizardStep1View(WizardSessionMixin, View):
    """
    Step 1: Select Provider
    Displays available social connector providers from ComponentRegistry
    """

    template_name = "admin/blog/social_connectors/wizard/step1_select.html"

    def get(self, request):
        """Display provider selection page"""
        # Clear any previous wizard data
        self.clear_wizard_data()

        # Auto-skip if provider pre-selected from browse page
        provider_slug = request.GET.get("provider")
        if provider_slug:
            try:
                component = ComponentRegistry.objects.get(
                    slug=provider_slug, component_type="social_connector_provider"
                )
                self.update_wizard_data(
                    component_id=str(component.id),
                    provider_key=component.slug,
                    provider_name=component.name,
                )
                return redirect("blog_admin:wizard_step2")
            except ComponentRegistry.DoesNotExist:
                pass  # Fall through to normal step 1

        # Get installed social connector providers
        installed_components = ComponentRegistry.objects.filter(
            component_type="social_connector_provider",
        ).order_by("name")

        providers = []
        for component in installed_components:
            manifest = component.get_manifest() or {}
            providers.append(
                {
                    "component": component,
                    "capabilities": manifest.get("capabilities", {}),
                    "character_limit": manifest.get("character_limit"),
                }
            )

        context = {
            "title": _("Connect Social Account"),
            "step": 1,
            "providers": providers,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle provider selection"""
        component_id = request.POST.get("component_id")

        if not component_id:
            messages.error(request, _("Please select a provider."))
            return redirect("blog_admin:wizard_step1")

        try:
            component = ComponentRegistry.objects.get(id=component_id)
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _("Invalid provider selected."))
            return redirect("blog_admin:wizard_step1")

        # Save to session
        self.update_wizard_data(
            component_id=str(component.id),
            provider_key=component.slug,
            provider_name=component.name,
        )

        return redirect("blog_admin:wizard_step2")


@method_decorator(staff_member_required, name="dispatch")
class WizardStep2View(WizardSessionMixin, View):
    """
    Step 2: Setup Instructions
    Shows OAuth setup instructions and initiates OAuth flow on POST
    """

    template_name = "admin/blog/social_connectors/wizard/step2_setup.html"

    def get(self, request):
        """Display setup instructions"""
        wizard_data = self.get_wizard_data()

        if not wizard_data.get("component_id"):
            messages.error(request, _("Please select a provider first."))
            return redirect("blog_admin:wizard_step1")

        try:
            component = ComponentRegistry.objects.get(id=wizard_data["component_id"])
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _("Provider not found."))
            return redirect("blog_admin:wizard_step1")

        manifest = component.get_manifest() or {}
        oauth_config = manifest.get("oauth_config", {})

        # Check for setup instructions HTML file
        setup_instructions = None
        if component.installed_path:
            instructions_file = Path(component.installed_path) / "setup_instructions.html"
            if instructions_file.exists():
                with open(instructions_file) as f:
                    setup_instructions = f.read()
                    # Replace placeholder with actual redirect URI
                    redirect_uri = get_oauth_redirect_uri(request)
                    setup_instructions = setup_instructions.replace("{redirect_uri}", redirect_uri)

        # Check if this provider uses OAuth
        uses_oauth = bool(oauth_config.get("authorize_url"))

        # Load manifest translations for i18n
        manifest_translations = None
        try:
            if component.installed_path:
                manifest_translations = load_manifest_translations(Path(component.installed_path))
        except Exception:
            manifest_translations = None

        context = {
            "title": _("Setup Instructions"),
            "step": 2,
            "component": component,
            "manifest": manifest,
            "oauth_config": oauth_config,
            "setup_instructions": setup_instructions,
            "wizard_data": wizard_data,
            "uses_oauth": uses_oauth,
            "redirect_uri": get_oauth_redirect_uri(request),
            "manifest_translations": manifest_translations,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Initiate OAuth flow or continue to manual configuration"""
        wizard_data = self.get_wizard_data()

        if not wizard_data.get("component_id"):
            return redirect("blog_admin:wizard_step1")

        try:
            component = ComponentRegistry.objects.get(id=wizard_data["component_id"])
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _("Provider not found."))
            return redirect("blog_admin:wizard_step1")

        manifest = component.get_manifest() or {}
        oauth_config = manifest.get("oauth_config", {})

        # Check if this provider uses OAuth
        if oauth_config.get("authorize_url"):
            # Build OAuth authorization URL
            state = secrets.token_urlsafe(32)
            self.update_wizard_data(oauth_state=state)

            # Get OAuth configuration
            authorize_url = oauth_config["authorize_url"]
            client_id = self._get_oauth_client_id(component.slug)
            redirect_uri = get_oauth_redirect_uri(request)
            scope = " ".join(oauth_config.get("scope", []))

            # Build authorization URL with parameters
            params = {
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "state": state,
                "response_type": oauth_config.get("response_type", "code"),
            }

            if scope:
                params["scope"] = scope

            # Provider-specific parameters
            if component.slug == "facebook_page":
                # Facebook requires config_id for business logins or display parameter
                params["display"] = "popup"
            elif component.slug == "linkedin_company":
                # LinkedIn uses different parameter names
                params["scope"] = scope.replace(" ", "%20")

            # Build URL with query parameters
            auth_url = f"{authorize_url}?"
            auth_url += "&".join(f"{k}={v}" for k, v in params.items())

            logger.info(f"Redirecting to OAuth: {auth_url[:100]}...")
            return HttpResponseRedirect(auth_url)
        else:
            # No OAuth, go to manual configuration
            return redirect("blog_admin:wizard_step3")

    def _get_oauth_client_id(self, provider_slug):
        """Get OAuth client ID from settings"""
        # Map provider slugs to setting names
        setting_map = {
            "facebook_page": "FACEBOOK_APP_ID",
            "instagram_business": "FACEBOOK_APP_ID",  # Uses Facebook OAuth
            "twitter": "TWITTER_CLIENT_ID",
            "linkedin_company": "LINKEDIN_CLIENT_ID",
            "google_merchant": "GOOGLE_CLIENT_ID",
        }
        setting_name = setting_map.get(provider_slug)
        if setting_name:
            return getattr(settings, setting_name, "")
        return ""


@method_decorator(staff_member_required, name="dispatch")
class OAuthCallbackView(WizardSessionMixin, View):
    """
    OAuth callback handler.
    Receives authorization code and exchanges for access token.
    """

    def get(self, request):
        """Handle OAuth callback"""
        wizard_data = self.get_wizard_data()

        # Verify state parameter
        state = request.GET.get("state")
        expected_state = wizard_data.get("oauth_state")

        if not state or state != expected_state:
            messages.error(request, _("OAuth state mismatch. Please try again."))
            return redirect("blog_admin:wizard_step1")

        # Check for errors
        error = request.GET.get("error")
        if error:
            error_description = request.GET.get("error_description", error)
            messages.error(request, _("OAuth error: {error}").format(error=error_description))
            return redirect("blog_admin:wizard_step2")

        # Get authorization code
        code = request.GET.get("code")
        if not code:
            messages.error(request, _("No authorization code received."))
            return redirect("blog_admin:wizard_step2")

        # Get component
        try:
            component = ComponentRegistry.objects.get(id=wizard_data["component_id"])
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _("Provider not found."))
            return redirect("blog_admin:wizard_step1")

        manifest = component.get_manifest() or {}
        oauth_config = manifest.get("oauth_config", {})

        # Exchange code for access token
        try:
            token_data = self._exchange_code_for_token(
                component.slug, oauth_config, code, get_oauth_redirect_uri(request)
            )

            if not token_data.get("access_token"):
                messages.error(request, _("Failed to obtain access token."))
                return redirect("blog_admin:wizard_step2")

            # Store token data
            self.update_wizard_data(
                oauth_tokens=token_data,
                oauth_completed=True,
            )

            # Check if provider requires account selection (from manifest)
            account_selection = manifest.get("account_selection", {})
            if account_selection.get("required"):
                return redirect("blog_admin:wizard_select_account")
            else:
                # Go directly to configuration
                return redirect("blog_admin:wizard_step3")

        except Exception as e:
            logger.exception(f"OAuth token exchange failed: {e}")
            messages.error(request, _("Failed to complete OAuth: {error}").format(error=str(e)))
            return redirect("blog_admin:wizard_step2")

    def _exchange_code_for_token(self, provider_slug, oauth_config, code, redirect_uri):
        """Exchange authorization code for access token"""
        token_url = oauth_config["token_url"]
        client_id = self._get_oauth_client_id(provider_slug)
        client_secret = self._get_oauth_client_secret(provider_slug)

        if provider_slug in ["facebook_page", "instagram_business"]:
            # Facebook/Instagram token exchange
            params = {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "code": code,
            }
            response = requests.get(token_url, params=params, timeout=30)
            response.raise_for_status()
            token_data = response.json()

            # Exchange for long-lived token
            if token_data.get("access_token"):
                long_lived = self._get_long_lived_facebook_token(
                    token_data["access_token"], client_id, client_secret
                )
                if long_lived:
                    token_data["access_token"] = long_lived.get(
                        "access_token", token_data["access_token"]
                    )
                    token_data["expires_in"] = long_lived.get("expires_in")

            return token_data

        elif provider_slug == "twitter":
            # Twitter OAuth 2.0
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "client_id": client_id,
                "code_verifier": "challenge",  # PKCE
            }
            response = requests.post(
                token_url, data=data, auth=(client_id, client_secret), timeout=30
            )
            response.raise_for_status()
            return response.json()

        elif provider_slug == "linkedin_company":
            # LinkedIn OAuth 2.0
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "client_id": client_id,
                "client_secret": client_secret,
            }
            response = requests.post(token_url, data=data, timeout=30)
            response.raise_for_status()
            return response.json()

        else:
            # Generic OAuth 2.0
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "client_id": client_id,
                "client_secret": client_secret,
            }
            response = requests.post(token_url, data=data, timeout=30)
            response.raise_for_status()
            return response.json()

    def _get_long_lived_facebook_token(self, short_lived_token, client_id, client_secret):
        """Exchange short-lived Facebook token for long-lived token"""
        try:
            url = "https://graph.facebook.com/v18.0/oauth/access_token"
            params = {
                "grant_type": "fb_exchange_token",
                "client_id": client_id,
                "client_secret": client_secret,
                "fb_exchange_token": short_lived_token,
            }
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.warning(f"Failed to get long-lived token: {e}")
            return None

    def _get_oauth_client_id(self, provider_slug):
        """Get OAuth client ID from settings"""
        setting_map = {
            "facebook_page": "FACEBOOK_APP_ID",
            "instagram_business": "FACEBOOK_APP_ID",
            "twitter": "TWITTER_CLIENT_ID",
            "linkedin_company": "LINKEDIN_CLIENT_ID",
            "google_merchant": "GOOGLE_CLIENT_ID",
        }
        setting_name = setting_map.get(provider_slug)
        if setting_name:
            return getattr(settings, setting_name, "")
        return ""

    def _get_oauth_client_secret(self, provider_slug):
        """Get OAuth client secret from settings"""
        setting_map = {
            "facebook_page": "FACEBOOK_APP_SECRET",
            "instagram_business": "FACEBOOK_APP_SECRET",
            "twitter": "TWITTER_CLIENT_SECRET",
            "linkedin_company": "LINKEDIN_CLIENT_SECRET",
            "google_merchant": "GOOGLE_CLIENT_SECRET",
        }
        setting_name = setting_map.get(provider_slug)
        if setting_name:
            return getattr(settings, setting_name, "")
        return ""


@method_decorator(staff_member_required, name="dispatch")
class WizardSelectAccountView(WizardSessionMixin, View):
    """
    Unified Account Selection View.
    Loads selection template from provider package and handles account selection.
    Supports Facebook Pages, LinkedIn Organizations, and other account types.
    """

    def get(self, request):
        """Display account selection using provider's template"""
        wizard_data = self.get_wizard_data()

        if not wizard_data.get("oauth_completed"):
            messages.error(request, _("Please complete OAuth first."))
            return redirect("blog_admin:wizard_step2")

        try:
            component = ComponentRegistry.objects.get(id=wizard_data["component_id"])
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _("Provider not found."))
            return redirect("blog_admin:wizard_step1")

        manifest = component.get_manifest() or {}
        account_selection = manifest.get("account_selection", {})

        if not account_selection.get("required"):
            # No account selection needed, go to config
            return redirect("blog_admin:wizard_step3")

        # Get accounts based on provider type
        access_token = wizard_data["oauth_tokens"].get("access_token")
        accounts = self._fetch_accounts(component.slug, access_token, account_selection)

        if not accounts:
            messages.warning(request, _("No accounts found. Please check your permissions."))

        # Load provider's selection template
        selection_template_content = self._load_provider_template(component, account_selection)

        context = {
            "title": _("Select Account"),
            "step": 3,
            "component": component,
            "manifest": manifest,
            "accounts": accounts,
            "wizard_data": wizard_data,
            "account_selection": account_selection,
            "selection_template_content": selection_template_content,
        }

        return render(request, "admin/blog/social_connectors/wizard/select_account.html", context)

    def post(self, request):
        """Handle account selection"""
        wizard_data = self.get_wizard_data()
        account_id = request.POST.get("account_id")

        if not account_id:
            messages.error(request, _("Please select an account."))
            return redirect("blog_admin:wizard_select_account")

        try:
            component = ComponentRegistry.objects.get(id=wizard_data["component_id"])
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _("Provider not found."))
            return redirect("blog_admin:wizard_step1")

        manifest = component.get_manifest() or {}
        account_selection = manifest.get("account_selection", {})

        # Get account details from hidden fields
        account_name = request.POST.get(f"account_name_{account_id}", "")
        account_token = request.POST.get(f"account_token_{account_id}", "")

        # Build credentials based on manifest config
        id_field = account_selection.get("id_field", "account_id")
        name_field = account_selection.get("name_field", "account_name")
        token_field = account_selection.get("token_field", "access_token")

        credentials = {
            token_field: account_token or wizard_data["oauth_tokens"].get("access_token"),
            id_field: account_id,
            name_field: account_name,
        }

        self.update_wizard_data(
            credentials=credentials,
            selected_account={
                "id": account_id,
                "name": account_name,
            },
        )

        return redirect("blog_admin:wizard_step3")

    def _load_provider_template(self, component, account_selection):
        """Load selection template from provider package"""
        template_file = account_selection.get("template", "select_account.html")

        if component.installed_path:
            template_path = Path(component.installed_path) / template_file
            if template_path.exists():
                with open(template_path) as f:
                    return f.read()

        return None

    def _fetch_accounts(self, provider_slug, access_token, account_selection):
        """Fetch accounts based on provider type"""
        if provider_slug in ["facebook_page", "instagram_business"]:
            return self._get_facebook_pages(access_token, account_selection)
        elif provider_slug == "linkedin_company":
            return self._get_linkedin_organizations(access_token)
        elif provider_slug == "twitter":
            # Twitter posts to user account directly, no selection needed
            return []
        else:
            # Generic account fetch using manifest config
            return self._get_generic_accounts(access_token, account_selection)

    def _get_facebook_pages(self, access_token, account_selection):
        """Get list of Facebook Pages the user manages"""
        try:
            api_endpoint = account_selection.get("api_endpoint", "/me/accounts")
            api_fields = account_selection.get(
                "api_fields", "id,name,category,picture{url},access_token"
            )

            url = f"https://graph.facebook.com/v18.0{api_endpoint}"
            params = {
                "access_token": access_token,
                "fields": api_fields,
            }
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except Exception as e:
            logger.exception(f"Failed to get Facebook pages: {e}")
            return []

    def _get_linkedin_organizations(self, access_token):
        """Get list of LinkedIn organizations the user can post to"""
        try:
            url = "https://api.linkedin.com/v2/organizationAcls"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "X-Restli-Protocol-Version": "2.0.0",
            }
            params = {
                "q": "roleAssignee",
                "role": "ADMINISTRATOR",
                "projection": "(elements*(organization~(id,localizedName,logoV2(original~:playableStreams))))",
            }
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            organizations = []
            for element in data.get("elements", []):
                org = element.get("organization~", {})
                organizations.append(
                    {
                        "id": org.get("id"),
                        "name": org.get("localizedName"),
                    }
                )
            return organizations
        except Exception as e:
            logger.exception(f"Failed to get LinkedIn organizations: {e}")
            return []

    def _get_generic_accounts(self, access_token, account_selection):
        """Generic account fetch for providers with custom API endpoints"""
        # This can be extended to support more providers
        return []


# Keep these as aliases for backward compatibility
WizardSelectPageView = WizardSelectAccountView
WizardSelectOrganizationView = WizardSelectAccountView


@method_decorator(staff_member_required, name="dispatch")
class WizardStep3View(WizardSessionMixin, View):
    """
    Step 3: Configure Account
    Enter account name (credentials are auto-populated from OAuth)
    """

    template_name = "admin/blog/social_connectors/wizard/step3_config.html"

    def get(self, request):
        """Display configuration form"""
        wizard_data = self.get_wizard_data()

        if not wizard_data.get("component_id"):
            messages.error(request, _("Please select a provider first."))
            return redirect("blog_admin:wizard_step1")

        try:
            component = ComponentRegistry.objects.get(id=wizard_data["component_id"])
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _("Provider not found."))
            return redirect("blog_admin:wizard_step1")

        manifest = component.get_manifest() or {}
        oauth_config = manifest.get("oauth_config", {})
        settings_schema = manifest.get("settings_schema", {})

        # Check if we have credentials from OAuth
        has_oauth_credentials = bool(wizard_data.get("credentials"))
        uses_oauth = bool(oauth_config.get("authorize_url"))

        # If OAuth provider but no credentials, redirect back
        if uses_oauth and not has_oauth_credentials:
            messages.error(request, _("Please complete the authorization flow first."))
            return redirect("blog_admin:wizard_step2")

        # Generate suggested account name
        suggested_name = ""
        if wizard_data.get("credentials"):
            creds = wizard_data["credentials"]
            suggested_name = (
                creds.get("page_name")
                or creds.get("organization_name")
                or creds.get("username")
                or ""
            )

        context = {
            "title": _("Configure Account"),
            "step": 4 if uses_oauth else 3,
            "component": component,
            "manifest": manifest,
            "settings_schema": settings_schema,
            "wizard_data": wizard_data,
            "has_oauth_credentials": has_oauth_credentials,
            "suggested_name": suggested_name,
            # Only show credential fields for non-OAuth providers
            "credential_schema": {}
            if has_oauth_credentials
            else manifest.get("credential_schema", {}),
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle configuration submission"""
        wizard_data = self.get_wizard_data()

        if not wizard_data.get("component_id"):
            return redirect("blog_admin:wizard_step1")

        try:
            component = ComponentRegistry.objects.get(id=wizard_data["component_id"])
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _("Provider not found."))
            return redirect("blog_admin:wizard_step1")

        # Get form data
        account_name = request.POST.get("account_name", "").strip()
        if not account_name:
            messages.error(request, _("Please enter an account name."))
            return redirect("blog_admin:wizard_step3")

        manifest = component.get_manifest() or {}

        # Get credentials - either from OAuth or form
        credentials = wizard_data.get("credentials", {})

        # If no OAuth credentials, collect from form
        if not credentials:
            credential_schema = manifest.get("credential_schema", {})
            for field_name, field_config in credential_schema.items():
                value = request.POST.get(field_name, "").strip()
                if field_config.get("required") and not value:
                    messages.error(request, _("Please fill in all required fields."))
                    return redirect("blog_admin:wizard_step3")
                if value:
                    credentials[field_name] = value

        # Collect settings
        settings_schema = manifest.get("settings_schema", {})
        account_settings = {}
        for field_name, field_config in settings_schema.items():
            if field_config.get("type") == "boolean":
                account_settings[field_name] = request.POST.get(field_name) == "on"
            else:
                value = request.POST.get(field_name, "").strip()
                if value:
                    account_settings[field_name] = value

        # Save to session for test step
        self.update_wizard_data(
            account_name=account_name,
            credentials=credentials,
            settings=account_settings,
        )

        return redirect("blog_admin:wizard_step4")


@method_decorator(staff_member_required, name="dispatch")
class WizardStep4View(WizardSessionMixin, View):
    """
    Step 4: Test & Save
    Test connection and save account
    """

    template_name = "admin/blog/social_connectors/wizard/step4_test.html"

    def get(self, request):
        """Display test page"""
        wizard_data = self.get_wizard_data()

        if not wizard_data.get("component_id"):
            messages.error(request, _("Please select a provider first."))
            return redirect("blog_admin:wizard_step1")

        if not wizard_data.get("credentials"):
            messages.error(request, _("Please configure credentials first."))
            return redirect("blog_admin:wizard_step3")

        try:
            component = ComponentRegistry.objects.get(id=wizard_data["component_id"])
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _("Provider not found."))
            return redirect("blog_admin:wizard_step1")

        manifest = component.get_manifest() or {}

        context = {
            "title": _("Test & Save"),
            "step": 5 if manifest.get("oauth_config", {}).get("authorize_url") else 4,
            "component": component,
            "manifest": manifest,
            "wizard_data": wizard_data,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Save the account"""
        wizard_data = self.get_wizard_data()

        if not wizard_data.get("component_id") or not wizard_data.get("credentials"):
            messages.error(request, _("Invalid wizard state."))
            return redirect("blog_admin:wizard_step1")

        try:
            component = ComponentRegistry.objects.get(id=wizard_data["component_id"])
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _("Provider not found."))
            return redirect("blog_admin:wizard_step1")

        # Encrypt credentials
        from email_system.utils.encryption import encrypt_credentials

        encrypted_credentials = encrypt_credentials(wizard_data["credentials"])

        # Create the account
        with transaction.atomic():
            account = SocialConnectorAccount.objects.create(
                site=Site.objects.get(pk=1),
                component=component,
                provider_key=component.slug,
                name=wizard_data["account_name"],
                platform_account_id=wizard_data["credentials"].get("page_id")
                or wizard_data["credentials"].get("user_id")
                or wizard_data["credentials"].get("organization_id")
                or wizard_data["credentials"].get("instagram_account_id")
                or "pending",
                platform_account_name=wizard_data["credentials"].get("page_name")
                or wizard_data["credentials"].get("username")
                or wizard_data["credentials"].get("organization_name")
                or wizard_data["credentials"].get("instagram_username")
                or "",
                credentials=encrypted_credentials,
                status="active",
                auto_share_enabled=True,
                post_template=wizard_data.get("settings", {}).get("post_template", ""),
                default_hashtags=wizard_data.get("settings", {}).get("default_hashtags", ""),
                connected_by=request.user,
            )

        # Clear wizard session
        self.clear_wizard_data()

        messages.success(
            request, _('Social account "{name}" connected successfully!').format(name=account.name)
        )

        return redirect("admin:blog_socialconnectoraccount_changelist")


@staff_member_required
def install_provider_ajax(request, provider_slug):
    """Install a social connector provider from update server"""
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        from component_updates.services import UpdateManager

        update_manager = UpdateManager()

        # Install the provider
        result = update_manager.install_component(
            component_type="social_connector_provider", slug=provider_slug
        )

        if result.get("success"):
            return JsonResponse(
                {
                    "success": True,
                    "message": _("Provider installed successfully"),
                    "redirect_url": "/admin/blog/social-connectors/wizard/step1/",
                }
            )
        else:
            return JsonResponse(
                {"success": False, "error": result.get("error", _("Installation failed"))},
                status=400,
            )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
def update_provider_ajax(request, provider_slug):
    """Update a social connector provider from update server"""
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        from component_updates.services import UpdateManager

        update_manager = UpdateManager()

        # Update the provider
        result = update_manager.update_component(
            component_type="social_connector_provider", slug=provider_slug
        )

        if result.get("success"):
            return JsonResponse({"success": True, "message": _("Provider updated successfully")})
        else:
            return JsonResponse(
                {"success": False, "error": result.get("error", _("Update failed"))}, status=400
            )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
def test_connection_ajax(request, account_id):
    """Test connection for a social connector account"""
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        account = get_object_or_404(SocialConnectorAccount, id=account_id)

        # Load the provider class
        if not account.component or not account.component.installed_path:
            return JsonResponse(
                {"success": False, "error": _("Provider not properly installed")}, status=400
            )

        # Get credentials
        credentials = account.get_credentials()

        # Try to load and test the provider
        try:
            import importlib.util

            provider_path = Path(account.component.installed_path) / "provider.py"

            if not provider_path.exists():
                return JsonResponse(
                    {"success": False, "error": _("Provider module not found")}, status=400
                )

            spec = importlib.util.spec_from_file_location("provider", provider_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            manifest = account.component.get_manifest() or {}
            class_name = manifest.get("class_name")

            if not class_name or not hasattr(module, class_name):
                return JsonResponse(
                    {"success": False, "error": _("Provider class not found")}, status=400
                )

            provider_class = getattr(module, class_name)
            provider = provider_class(credentials)
            result = provider.test_connection()

            return JsonResponse(result)

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    except SocialConnectorAccount.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Account not found")}, status=404)


@staff_member_required
def delete_account_ajax(request, account_id):
    """Delete a social connector account"""
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        account = get_object_or_404(SocialConnectorAccount, id=account_id)
        account_name = account.name
        account.delete()

        return JsonResponse(
            {
                "success": True,
                "message": _('Account "{name}" deleted successfully').format(name=account_name),
            }
        )

    except SocialConnectorAccount.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Account not found")}, status=404)
