"""
Email System Views

Handles OAuth flows for email provider connections.
"""
import logging
import secrets
from typing import Optional

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from email_system.models import EmailAccount
from email_system.utils.encryption import encrypt_credentials
from email_system.providers.registry import ProviderRegistry

logger = logging.getLogger(__name__)


@staff_member_required
@require_http_methods(["GET", "POST"])
def oauth_initiate(request: HttpRequest, provider_key: str) -> HttpResponse:
    """
    Initiate OAuth flow for email provider.

    Step 1 of OAuth authorization code flow:
    - Loads provider
    - Gets OAuth configuration from request (client_id, client_secret)
    - Generates authorization URL
    - Redirects user to provider's authorization page

    Args:
        request: HTTP request
        provider_key: Provider identifier (e.g., 'gmail_api')

    Query params (for POST):
        client_id: OAuth client ID from provider
        client_secret: OAuth client secret from provider

    Returns:
        Redirect to provider's OAuth authorization page
    """
    try:
        # Get provider class
        provider_class = ProviderRegistry.get_provider(provider_key)
        if not provider_class:
            messages.error(request, _("Email provider '%(provider)s' not found") % {'provider': provider_key})
            return redirect('admin:email_system_emailaccount_changelist')

        # Check if provider supports OAuth
        if not hasattr(provider_class, 'create_oauth_handler'):
            messages.error(request, _("Provider '%(provider)s' does not support OAuth") % {'provider': provider_key})
            return redirect('admin:email_system_emailaccount_changelist')

        # Get OAuth credentials from POST or session
        if request.method == 'POST':
            client_id = request.POST.get('client_id')
            client_secret = request.POST.get('client_secret')

            if not client_id or not client_secret:
                messages.error(request, _("Client ID and Client Secret are required"))
                return redirect('admin:email_system_emailaccount_changelist')

            # Store in session for callback
            request.session['oauth_client_id'] = client_id
            request.session['oauth_client_secret'] = client_secret
        else:
            # For GET, check if credentials are in session
            client_id = request.session.get('oauth_client_id')
            client_secret = request.session.get('oauth_client_secret')

            if not client_id or not client_secret:
                messages.error(request, _("OAuth credentials not found. Please start the connection process again."))
                return redirect('admin:email_system_emailaccount_changelist')

        # Store provider key in session
        request.session['oauth_provider_key'] = provider_key

        # Build redirect URI
        redirect_uri = request.build_absolute_uri(
            reverse('email_system:oauth_callback', kwargs={'provider_key': provider_key})
        )

        # Create OAuth handler
        oauth_handler = provider_class.create_oauth_handler(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri
        )

        # Generate state token for CSRF protection
        state = secrets.token_urlsafe(32)
        request.session['oauth_state'] = state
        request.session['oauth_redirect_uri'] = redirect_uri

        # Get authorization URL
        auth_result = oauth_handler.get_authorization_url(state=state)

        logger.info(f"Initiating OAuth flow for {provider_key}")

        # Redirect to provider's authorization page
        return redirect(auth_result['authorization_url'])

    except Exception as e:
        logger.error(f"Error initiating OAuth flow for {provider_key}: {e}", exc_info=True)
        messages.error(request, _("Failed to initiate OAuth flow: %(error)s") % {'error': str(e)})
        return redirect('admin:email_system_emailaccount_changelist')


@staff_member_required
@require_http_methods(["GET"])
def oauth_callback(request: HttpRequest, provider_key: str) -> HttpResponse:
    """
    Handle OAuth callback from email provider.

    Step 2 of OAuth authorization code flow:
    - Receives authorization code from provider
    - Exchanges code for access/refresh tokens
    - Creates EmailAccount with encrypted credentials

    Args:
        request: HTTP request with authorization code
        provider_key: Provider identifier (e.g., 'gmail_api')

    Query params:
        code: Authorization code from provider
        state: CSRF protection token

    Returns:
        Redirect to EmailAccount admin with success/error message
    """
    try:
        # Validate state for CSRF protection
        state = request.GET.get('state')
        expected_state = request.session.get('oauth_state')

        if not state or state != expected_state:
            logger.warning(f"OAuth state mismatch for {provider_key}")
            messages.error(request, _("Invalid OAuth state. Please try again."))
            return redirect('admin:email_system_emailaccount_changelist')

        # Check for error from provider
        error = request.GET.get('error')
        if error:
            error_description = request.GET.get('error_description', error)
            logger.warning(f"OAuth error from provider {provider_key}: {error_description}")
            messages.error(request, _("OAuth authorization failed: %(error)s") % {'error': error_description})
            return redirect('admin:email_system_emailaccount_changelist')

        # Get authorization code
        code = request.GET.get('code')
        if not code:
            messages.error(request, _("Authorization code not received"))
            return redirect('admin:email_system_emailaccount_changelist')

        # Get stored OAuth credentials from session
        client_id = request.session.get('oauth_client_id')
        client_secret = request.session.get('oauth_client_secret')
        redirect_uri = request.session.get('oauth_redirect_uri')
        stored_provider_key = request.session.get('oauth_provider_key')

        if not all([client_id, client_secret, redirect_uri, stored_provider_key]):
            messages.error(request, _("OAuth session expired. Please start the connection process again."))
            return redirect('admin:email_system_emailaccount_changelist')

        # Verify provider key matches
        if stored_provider_key != provider_key:
            messages.error(request, _("Provider mismatch. Please try again."))
            return redirect('admin:email_system_emailaccount_changelist')

        # Get provider class
        provider_class = ProviderRegistry.get_provider(provider_key)
        if not provider_class:
            messages.error(request, _("Email provider not found"))
            return redirect('admin:email_system_emailaccount_changelist')

        # Create OAuth handler
        oauth_handler = provider_class.create_oauth_handler(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri
        )

        # Exchange code for tokens
        logger.info(f"Exchanging authorization code for tokens: {provider_key}")
        credentials = oauth_handler.exchange_code_for_tokens(code)

        # Check if called from wizard
        wizard_session_key = 'email_wizard_data'
        wizard_data = request.session.get(wizard_session_key)

        if wizard_data and wizard_data.get('component_slug') == provider_key:
            # WIZARD FLOW: Store credentials and redirect to Step 3
            logger.info(f"OAuth callback from wizard - storing credentials and continuing wizard")

            wizard_data['credentials'] = credentials
            wizard_data['credentials_configured'] = True
            request.session[wizard_session_key] = wizard_data
            request.session.modified = True

            # Clear OAuth-specific session keys
            for key in ['oauth_state', 'oauth_client_id', 'oauth_client_secret',
                        'oauth_redirect_uri', 'oauth_provider_key']:
                request.session.pop(key, None)

            messages.success(request, _("Successfully authorized %(provider)s. Continue configuring your account.") % {
                'provider': provider_class.provider_name
            })

            return redirect('email_system:wizard_step3')

        # STANDALONE FLOW: Continue with existing account creation logic
        # Test connection with credentials
        logger.info(f"Testing provider connection: {provider_key}")
        provider_instance = provider_class(credentials=credentials)
        health_result = provider_instance.healthcheck()

        if not health_result.get('success'):
            error_msg = health_result.get('message', 'Connection test failed')
            messages.error(request, _("Connection test failed: %(error)s") % {'error': error_msg})
            return redirect('admin:email_system_emailaccount_changelist')

        # Get email address from health check if available
        email_address = health_result.get('details', {}).get('email_address', '')

        # Get current site
        site = get_current_site(request)

        # Get component registry entry
        from component_updates.models import ComponentRegistry
        component = ComponentRegistry.objects.filter(
            component_type='email_provider',
            slug=provider_key
        ).first()

        if not component:
            messages.error(request, _("Email provider component not found in registry"))
            return redirect('admin:email_system_emailaccount_changelist')

        # Create EmailAccount
        account = EmailAccount.objects.create(
            site=site,
            component=component,
            from_email=email_address or f'noreply@{site.domain}',
            from_name=site.name,
            credentials=encrypt_credentials(credentials),
            connection_status='connected',
            is_active=True,
            created_by=request.user
        )

        # Clear OAuth session data
        for key in ['oauth_state', 'oauth_client_id', 'oauth_client_secret',
                    'oauth_redirect_uri', 'oauth_provider_key']:
            request.session.pop(key, None)

        logger.info(f"Successfully created email account {account.id} for {provider_key}")
        messages.success(
            request,
            _("Successfully connected %(provider)s account: %(email)s") % {
                'provider': provider_class.provider_name,
                'email': account.from_email
            }
        )

        # Redirect to the created account's change page
        return redirect('admin:email_system_emailaccount_change', account.id)

    except ValueError as e:
        logger.error(f"OAuth validation error for {provider_key}: {e}")

        # Check if from wizard
        wizard_data = request.session.get('email_wizard_data')
        if wizard_data and wizard_data.get('component_slug') == provider_key:
            messages.error(request, _(
                "OAuth validation failed: %(error)s. Please check your Client ID and Client Secret and try again."
            ) % {'error': str(e)})
            return redirect('email_system:wizard_step2')

        # Standalone flow error handling
        messages.error(request, _("OAuth validation failed: %(error)s") % {'error': str(e)})
        return redirect('admin:email_system_emailaccount_changelist')

    except Exception as e:
        logger.error(f"Error in OAuth callback for {provider_key}: {e}", exc_info=True)

        # Check if from wizard
        wizard_data = request.session.get('email_wizard_data')
        if wizard_data and wizard_data.get('component_slug') == provider_key:
            messages.error(request, _(
                "OAuth authorization failed: %(error)s. Please check your Client ID and Client Secret and try again."
            ) % {'error': str(e)})
            return redirect('email_system:wizard_step2')

        # Standalone flow error handling
        messages.error(request, _("Failed to complete OAuth flow: %(error)s") % {'error': str(e)})
        return redirect('admin:email_system_emailaccount_changelist')


@staff_member_required
@require_http_methods(["POST"])
def test_connection(request: HttpRequest, account_id: str) -> JsonResponse:
    """
    Test email account connection.

    Args:
        request: HTTP request
        account_id: EmailAccount UUID

    Returns:
        JSON response with connection test results
    """
    try:
        account = get_object_or_404(EmailAccount, id=account_id)

        # Get provider instance
        provider = account.get_provider_instance()

        # Run health check
        result = provider.healthcheck()

        # Update connection status
        if result.get('success'):
            account.connection_status = 'connected'
            account.last_connection_check = timezone.now()
        else:
            account.connection_status = 'error'
            account.connection_error = result.get('message', 'Connection test failed')

        account.save()

        return JsonResponse(result)

    except Exception as e:
        logger.error(f"Error testing connection for account {account_id}: {e}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': str(e),
            'details': {}
        }, status=500)


@staff_member_required
@require_http_methods(["GET"])
def oauth_setup_form(request: HttpRequest, provider_key: str) -> HttpResponse:
    """
    Display OAuth setup form for provider.

    DEPRECATED: This standalone OAuth form is deprecated in favor of the
    multi-step wizard flow. OAuth providers should use the wizard which
    integrates OAuth into Step 2. This view is kept for backward compatibility
    but will be removed in a future version.

    Shows form to collect OAuth client credentials before initiating OAuth flow.

    Args:
        request: HTTP request
        provider_key: Provider identifier (e.g., 'gmail_api')

    Returns:
        Rendered OAuth setup form
    """
    try:
        # Get provider class
        provider_class = ProviderRegistry.get_provider(provider_key)
        if not provider_class:
            messages.error(request, _("Email provider not found"))
            return redirect('admin:email_system_emailaccount_changelist')

        # Get current site
        site = get_current_site(request)

        # Build redirect URI for display
        redirect_uri = request.build_absolute_uri(
            reverse('email_system:oauth_callback', kwargs={'provider_key': provider_key})
        )

        context = {
            'provider_key': provider_key,
            'provider_name': provider_class.provider_name,
            'redirect_uri': redirect_uri,
            'site': site,
        }

        return render(request, 'email_system/oauth_setup.html', context)

    except Exception as e:
        logger.error(f"Error showing OAuth setup form for {provider_key}: {e}", exc_info=True)
        messages.error(request, _("Failed to load OAuth setup form: %(error)s") % {'error': str(e)})
        return redirect('admin:email_system_emailaccount_changelist')
