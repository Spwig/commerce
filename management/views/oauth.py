"""
OAuth views for storage provider authorization.

Handles the OAuth 2.0 authorization code flow for Google Drive, Dropbox,
and other OAuth-based storage providers. Integrates with the storage
setup wizard via session data.
"""

import logging
import secrets

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _

from management.storage_providers.registry import StorageProviderRegistry

logger = logging.getLogger(__name__)

WIZARD_SESSION_KEY = "remote_storage_wizard_data"


@staff_member_required
def storage_oauth_initiate(request):
    """
    Initiate OAuth flow for a storage provider.

    Reads the provider_type from the wizard session, collects client
    credentials from POST, and redirects to the provider's authorization page.
    """
    if request.method != "POST":
        messages.error(request, _("Invalid request method."))
        return redirect("admin:management_storage_wizard_step2")

    # Get provider type from wizard session
    wizard_data = request.session.get(WIZARD_SESSION_KEY, {})
    provider_type = wizard_data.get("provider_type")
    if not provider_type:
        messages.error(request, _("No provider selected. Please start the wizard again."))
        return redirect("admin:management_storage_wizard_step1")

    provider_class = StorageProviderRegistry.get_provider_class(provider_type)
    if not provider_class or not provider_class.requires_oauth:
        messages.error(request, _("Provider does not support OAuth."))
        return redirect("admin:management_storage_wizard_step2")

    # Collect client credentials from POST
    # Google Drive uses client_id/client_secret, Dropbox uses app_key/app_secret
    credentials = {}
    for field in provider_class.credential_fields:
        val = request.POST.get(f"cred_{field['key']}", "").strip()
        if field.get("required") and not val:
            messages.error(
                request,
                _("%(field)s is required.") % {"field": field["label"]},
            )
            return redirect("admin:management_storage_wizard_step2")
        if val:
            credentials[field["key"]] = val

    # Store credentials in wizard session for the callback
    wizard_data["credentials"] = credentials
    request.session[WIZARD_SESSION_KEY] = wizard_data
    request.session.modified = True

    # Build redirect URI for the OAuth callback
    redirect_uri = request.build_absolute_uri(reverse("admin:management_storage_oauth_callback"))

    try:
        # Get the first credential field values for OAuth handler
        # Google: client_id, client_secret  |  Dropbox: app_key, app_secret
        field_keys = [f["key"] for f in provider_class.credential_fields]
        oauth_handler = provider_class.create_oauth_handler(
            client_id=credentials.get(field_keys[0], ""),
            client_secret=credentials.get(field_keys[1], ""),
            redirect_uri=redirect_uri,
        )

        # Generate state token for CSRF protection
        state = secrets.token_urlsafe(32)
        request.session["storage_oauth_state"] = state
        request.session["storage_oauth_redirect_uri"] = redirect_uri

        # Get authorization URL
        auth_result = oauth_handler.get_authorization_url(state=state)

        logger.info("Initiating storage OAuth flow for %s", provider_type)
        return redirect(auth_result["authorization_url"])

    except Exception as e:
        logger.error("Error initiating storage OAuth for %s: %s", provider_type, e)
        messages.error(
            request,
            _("Failed to start authorization: %(error)s") % {"error": str(e)},
        )
        return redirect("admin:management_storage_wizard_step2")


@staff_member_required
def storage_oauth_callback(request):
    """
    Handle OAuth callback from storage provider.

    Validates the state token, exchanges the authorization code for tokens,
    stores them in the wizard session, and redirects back to Step 2.
    """
    # Validate state token
    state = request.GET.get("state")
    expected_state = request.session.get("storage_oauth_state")

    if not state or state != expected_state:
        logger.warning("Storage OAuth state mismatch")
        messages.error(request, _("Invalid OAuth state. Please try again."))
        return redirect("admin:management_storage_wizard_step2")

    # Check for error from provider
    error = request.GET.get("error")
    if error:
        error_description = request.GET.get("error_description", error)
        logger.warning("Storage OAuth error: %s", error_description)
        messages.error(
            request,
            _("Authorization failed: %(error)s") % {"error": error_description},
        )
        return redirect("admin:management_storage_wizard_step2")

    # Get authorization code
    code = request.GET.get("code")
    if not code:
        messages.error(request, _("Authorization code not received."))
        return redirect("admin:management_storage_wizard_step2")

    # Get wizard data
    wizard_data = request.session.get(WIZARD_SESSION_KEY, {})
    provider_type = wizard_data.get("provider_type")
    credentials = wizard_data.get("credentials", {})

    if not provider_type or not credentials:
        messages.error(request, _("Session expired. Please start the wizard again."))
        return redirect("admin:management_storage_wizard_step1")

    provider_class = StorageProviderRegistry.get_provider_class(provider_type)
    if not provider_class:
        messages.error(request, _("Unknown provider."))
        return redirect("admin:management_storage_wizard_step1")

    redirect_uri = request.session.get("storage_oauth_redirect_uri", "")

    try:
        # Create OAuth handler with stored credentials
        field_keys = [f["key"] for f in provider_class.credential_fields]
        oauth_handler = provider_class.create_oauth_handler(
            client_id=credentials.get(field_keys[0], ""),
            client_secret=credentials.get(field_keys[1], ""),
            redirect_uri=redirect_uri,
        )

        # Exchange code for tokens
        tokens = oauth_handler.exchange_code_for_tokens(code)

        # Merge tokens into credentials
        credentials.update(tokens)
        wizard_data["credentials"] = credentials
        wizard_data["oauth_authorized"] = True
        request.session[WIZARD_SESSION_KEY] = wizard_data
        request.session.modified = True

        # Clean up OAuth session keys
        request.session.pop("storage_oauth_state", None)
        request.session.pop("storage_oauth_redirect_uri", None)

        logger.info("Storage OAuth completed for %s", provider_type)
        messages.success(
            request,
            _("Successfully authorized with %(provider)s.")
            % {"provider": provider_class.provider_name},
        )

    except Exception as e:
        logger.error("Storage OAuth callback error for %s: %s", provider_type, e)
        messages.error(
            request,
            _("Authorization failed: %(error)s") % {"error": str(e)},
        )

    return redirect("admin:management_storage_wizard_step2")
