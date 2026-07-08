"""
Email Provider Setup Wizard Views
Multi-step wizard for connecting email provider components

Pattern follows exchange_rates/views/wizard.py
Design follows .claude_code/email/admin_email_setup_flows.md
"""
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.db import transaction
from django.templatetags.static import static
from pathlib import Path
from django.conf import settings
import json
import logging

from component_updates.integration_paths import INTEGRATIONS_DIR
from component_updates.models import ComponentRegistry
from email_system.models import EmailAccount
from email_system.providers.registry import ProviderRegistry
from email_system.utils.encryption import encrypt_credentials
from django.contrib.sites.models import Site
from core.models import SiteSettings
from urllib.parse import urlparse
from providers_common.utils import load_manifest_translations, validate_credential_fields

logger = logging.getLogger(__name__)


def load_provider_manifest(provider_path: Path) -> dict:
    """Load manifest.json from provider directory"""
    manifest_file = provider_path / 'manifest.json'
    if manifest_file.exists():
        with open(manifest_file, 'r') as f:
            return json.load(f)
    return None


class WizardSessionMixin:
    """Mixin for managing wizard session data"""

    SESSION_KEY = 'email_wizard_data'

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

    def _verify_smtp_server_listening(self):
        """
        Verify SMTP server is actually listening on port 2525.
        Returns True if server is listening, False otherwise.
        """
        import socket

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('127.0.0.1', 2525))
            sock.close()
            return result == 0
        except Exception:
            return False

    def _ensure_smtp_server_running(self, request):
        """
        Ensure the built-in SMTP server is running.
        Automatically starts it if not running.
        """
        import socket
        import subprocess
        import time

        # Check if server is already running
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', 2525))
            sock.close()

            if result == 0:
                # Server already running
                logger.info("Built-in SMTP server is already running")
                return True

        except Exception as e:
            logger.warning(f"Error checking SMTP server status: {e}")

        # Server not running, try to start it
        logger.info("Starting built-in SMTP server...")

        # Try supervisor first (Docker/production environment)
        try:
            result = subprocess.run(
                ['supervisorctl', 'start', 'smtp-server'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                messages.info(request, _('✓ Started built-in SMTP server'))
                time.sleep(3)  # Give server time to fully start

                # Verify server is actually listening
                if self._verify_smtp_server_listening():
                    logger.info("Built-in SMTP server started via supervisor and verified listening")
                    return True
                else:
                    logger.warning("SMTP server started but not yet listening on port 2525")
                    messages.warning(request, _('SMTP server started but may need more time to initialize'))
                    return True  # Still return True since supervisor started it
            else:
                logger.warning(f"Supervisor start failed: {result.stderr}")

        except FileNotFoundError:
            logger.debug("supervisorctl not found, trying direct start")
        except subprocess.TimeoutExpired:
            logger.warning("supervisorctl start timed out")
        except Exception as e:
            logger.warning(f"Error starting via supervisor: {e}")

        # Try starting directly in background (development environment)
        try:
            import os
            import sys

            # Get paths
            manage_py = os.path.join(settings.BASE_DIR, 'manage.py')
            venv_python = sys.executable

            # Start in background with nohup
            subprocess.Popen(
                [venv_python, manage_py, 'start_smtp_server'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True  # Detach from parent process
            )

            messages.info(request, _('✓ Started built-in SMTP server in background'))
            time.sleep(4)  # Give server more time to start

            # Verify server is actually listening
            if self._verify_smtp_server_listening():
                logger.info("Built-in SMTP server started in background and verified listening")
                return True
            else:
                logger.warning("SMTP server started but not yet listening on port 2525")
                messages.warning(request, _('SMTP server started but may need more time. If test fails, wait a moment and try again.'))
                return True  # Still return True since we started it

        except Exception as e:
            logger.error(f"Failed to start SMTP server: {e}", exc_info=True)
            messages.warning(
                request,
                _('Could not start SMTP server automatically. You may need to start it manually.')
            )
            return False


@method_decorator(staff_member_required, name='dispatch')
class ProviderWizardStep1View(WizardSessionMixin, View):
    """
    Step 1: Select Email Provider
    Displays available email providers from ComponentRegistry
    """

    template_name = 'admin/email_system/wizard/step1_select.html'

    def _load_builtin_provider(self):
        """
        Load the built-in SMTP provider for display in wizard.

        Returns:
            List with built-in provider data
        """
        try:
            # Load manifest from builtin provider
            builtin_dir = Path(settings.BASE_DIR) / 'email_system' / 'providers' / 'builtin'
            manifest_path = builtin_dir / 'manifest.json'

            with open(manifest_path, 'r') as f:
                manifest = json.load(f)

            # Create a pseudo-component object for the built-in provider
            # This mimics ComponentRegistry but isn't saved to database
            class BuiltinComponent:
                id = 'builtin_smtp'
                slug = 'builtin_smtp'
                name = manifest.get('name', 'Built-in SMTP Server')
                description = manifest.get('description', '')
                component_type = 'email_provider'
                current_version = manifest.get('version', '1.0.0')
                is_builtin = True

                # Logo URL
                logo_file = manifest.get('logo', 'logo.svg')
                logo_url = static(f'email_system/providers/builtin/{logo_file}')
                thumbnail_url = logo_url

            return [{
                'component': BuiltinComponent(),
                'manifest': manifest,
                'capabilities': manifest.get('capabilities', {}),
                'requires_oauth': False,  # Built-in provider doesn't use OAuth
                'is_builtin': True,
            }]

        except Exception as e:
            print(f"Could not load built-in provider: {e}")
            return []

    def _load_spwig_hosted_provider(self):
        """
        Load the Spwig Hosted Mail provider for display in wizard.

        Only shown on Spwig-hosted installations.

        Returns:
            List with Spwig hosted provider data
        """
        try:
            hosted_dir = Path(settings.BASE_DIR) / 'email_system' / 'providers' / 'spwig_hosted'
            manifest_path = hosted_dir / 'manifest.json'

            with open(manifest_path, 'r') as f:
                manifest = json.load(f)

            class SpwigHostedComponent:
                id = 'spwig_hosted_mail'
                slug = 'spwig_hosted_mail'
                name = manifest.get('name', 'Spwig Email')
                description = manifest.get('description', '')
                component_type = 'email_provider'
                current_version = manifest.get('version', '1.0.0')
                is_builtin = True

                logo_file = manifest.get('logo', 'logo.svg')
                logo_url = static(f'email_system/providers/spwig_hosted/{logo_file}')
                thumbnail_url = logo_url

            return [{
                'component': SpwigHostedComponent(),
                'manifest': manifest,
                'capabilities': manifest.get('capabilities', {}),
                'requires_oauth': False,
                'is_builtin': True,
            }]

        except Exception as e:
            print(f"Could not load Spwig hosted provider: {e}")
            return []

    def get(self, request):
        """Display provider selection"""
        # Clear any existing wizard data when starting fresh
        self.clear_wizard_data()

        # Auto-skip if provider pre-selected from browse page
        provider_slug = request.GET.get('provider')
        if provider_slug:
            if provider_slug == 'builtin_smtp':
                # Block built-in SMTP for Spwig-hosted installations
                from core.license import get_license_manager
                if get_license_manager().is_spwig_hosted():
                    messages.error(request, _('Built-in SMTP is not available for Spwig-hosted installations.'))
                    return redirect('email_system:wizard_step1')
                # Handle built-in SMTP provider
                builtin_dir = Path(settings.BASE_DIR) / 'email_system' / 'providers' / 'builtin'
                manifest_path = builtin_dir / 'manifest.json'
                if manifest_path.exists():
                    with open(manifest_path, 'r') as f:
                        manifest = json.load(f)
                    self.update_wizard_data(
                        component_id='builtin_smtp',
                        component_name=manifest.get('name', 'Built-in SMTP Server'),
                        component_slug='builtin_smtp',
                        is_builtin=True,
                    )
                    return redirect('email_system:wizard_step2')
            elif provider_slug == 'spwig_hosted_mail':
                # Spwig Hosted Mail — only available on hosted installations
                from core.license import get_license_manager
                if not get_license_manager().is_spwig_hosted():
                    messages.error(request, _('Spwig Email is only available for Spwig-hosted installations.'))
                    return redirect('email_system:wizard_step1')
                hosted_dir = Path(settings.BASE_DIR) / 'email_system' / 'providers' / 'spwig_hosted'
                manifest_path = hosted_dir / 'manifest.json'
                if manifest_path.exists():
                    with open(manifest_path, 'r') as f:
                        manifest = json.load(f)
                    self.update_wizard_data(
                        component_id='spwig_hosted_mail',
                        component_name=manifest.get('name', 'Spwig Email'),
                        component_slug='spwig_hosted_mail',
                        is_builtin=True,
                    )
                    return redirect('email_system:wizard_step2')
            else:
                # Handle external providers from ComponentRegistry
                try:
                    component = ComponentRegistry.objects.get(
                        slug=provider_slug, component_type='email_provider'
                    )
                    self.update_wizard_data(
                        component_id=component.id,
                        component_name=component.name,
                        component_slug=component.slug,
                        is_builtin=False,
                    )
                    return redirect('email_system:wizard_step2')
                except ComponentRegistry.DoesNotExist:
                    pass  # Fall through to normal step 1

        # Load manifests for each provider
        provider_data = []

        from core.license import get_license_manager
        is_hosted = get_license_manager().is_spwig_hosted()

        if is_hosted:
            # Hosted: show Spwig Email first (default provider)
            provider_data.extend(self._load_spwig_hosted_provider())
        else:
            # Self-hosted: show built-in SMTP provider first
            provider_data.extend(self._load_builtin_provider())

        # Get all email provider components from ComponentRegistry
        providers = ComponentRegistry.objects.filter(
            component_type='email_provider'
        ).order_by('name')

        # Load external providers
        for component in providers:
            try:
                # Load from component directory using the actual version
                # Expected: components_data/integrations/email_providers/{slug}/v{version}/
                from component_updates.integration_paths import INTEGRATIONS_DIR
                version = component.current_version or 'v1.0.0'
                if not version.startswith('v'):
                    version = f'v{version}'

                provider_dir = INTEGRATIONS_DIR / 'email_provider' / component.slug / version

                if provider_dir.exists():
                    manifest = load_provider_manifest(provider_dir)
                    if manifest:
                        # Get logo URL - handle both dict and string formats
                        logo_raw = manifest.get('logo', '')
                        logo_filename = ''
                        if isinstance(logo_raw, dict):
                            logo_filename = logo_raw.get('file', '')
                        elif logo_raw:
                            logo_filename = logo_raw
                        logo_url = ''

                        if logo_filename:
                            logo_path = provider_dir / logo_filename
                            if logo_path.exists():
                                logo_url = static(f'email_provider/{component.slug}/current/{logo_filename}')

                        # Set thumbnail_url on component object
                        component.thumbnail_url = logo_url

                        provider_data.append({
                            'component': component,
                            'manifest': manifest,
                            'capabilities': manifest.get('capabilities', {}),
                            'requires_oauth': manifest.get('capabilities', {}).get('oauth', False),
                        })
            except Exception as e:
                # Log but don't fail if manifest can't be loaded
                print(f"Could not load manifest for {component.name}: {e}")

        context = {
            'title': _('Email Provider Setup - Select Provider'),
            'providers': provider_data,
            'step': 1,
            'total_steps': 6,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle provider selection"""
        component_id = request.POST.get('component_id')

        if not component_id:
            messages.error(request, _('Please select a provider.'))
            return redirect('email_system:wizard_step1')

        # Handle built-in provider (special case - not in ComponentRegistry)
        if component_id == 'builtin_smtp':
            from core.license import get_license_manager
            if get_license_manager().is_spwig_hosted():
                messages.error(request, _('Built-in SMTP is not available for Spwig-hosted installations.'))
                return redirect('email_system:wizard_step1')
            # Load built-in manifest
            builtin_dir = Path(settings.BASE_DIR) / 'email_system' / 'providers' / 'builtin'
            manifest_path = builtin_dir / 'manifest.json'
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)

            # Store built-in provider in session
            self.update_wizard_data(
                component_id='builtin_smtp',
                component_name=manifest.get('name', 'Built-in SMTP Server'),
                component_slug='builtin_smtp',
                is_builtin=True,
            )

            # Skip to step 2
            return redirect('email_system:wizard_step2')

        # Handle Spwig Hosted Mail provider (hosted installations only)
        if component_id == 'spwig_hosted_mail':
            from core.license import get_license_manager
            if not get_license_manager().is_spwig_hosted():
                messages.error(request, _('Spwig Email is only available for Spwig-hosted installations.'))
                return redirect('email_system:wizard_step1')
            hosted_dir = Path(settings.BASE_DIR) / 'email_system' / 'providers' / 'spwig_hosted'
            manifest_path = hosted_dir / 'manifest.json'
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)

            self.update_wizard_data(
                component_id='spwig_hosted_mail',
                component_name=manifest.get('name', 'Spwig Email'),
                component_slug='spwig_hosted_mail',
                is_builtin=True,
            )
            return redirect('email_system:wizard_step2')

        # Handle external providers from ComponentRegistry
        try:
            component = ComponentRegistry.objects.get(id=component_id, component_type='email_provider')
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _('Invalid provider selected.'))
            return redirect('email_system:wizard_step1')

        # Store selected component in session
        self.update_wizard_data(
            component_id=component_id,
            component_name=component.name,
            component_slug=component.slug,
            is_builtin=False,
        )

        return redirect('email_system:wizard_step2')


@method_decorator(staff_member_required, name='dispatch')
class ProviderWizardStep2View(WizardSessionMixin, View):
    """
    Step 2: Configure Credentials
    Shows setup instructions and credential input form
    Handles both OAuth and API key/password flows
    """

    template_name = 'admin/email_system/wizard/step2_configure.html'

    def get(self, request):
        """Display credentials configuration"""
        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get('component_id')
        is_builtin = wizard_data.get('is_builtin', False)

        if not component_id:
            messages.warning(request, _('Please select a provider first.'))
            return redirect('email_system:wizard_step1')

        # Handle built-in SMTP provider
        if component_id == 'builtin_smtp':
            builtin_dir = Path(settings.BASE_DIR) / 'email_system' / 'providers' / 'builtin'
            manifest_path = builtin_dir / 'manifest.json'

            with open(manifest_path, 'r') as f:
                manifest = json.load(f)

            # Load setup instructions
            instructions_file = builtin_dir / 'setup_instructions.html'
            has_instructions = False
            instructions_html = ''

            if instructions_file.exists():
                from django.utils.safestring import mark_safe
                from django.template import Template, Context
                from django.contrib.sites.models import Site

                with open(instructions_file, 'r', encoding='utf-8') as f:
                    instructions_content = f.read()

                template = Template(instructions_content)
                site = Site.objects.get_current()
                context = Context({
                    'component_slug': 'builtin_smtp',
                    'domain': site.domain,
                })
                instructions_html = mark_safe(template.render(context))
                has_instructions = True

            # Create pseudo-component object for template
            class BuiltinComponent:
                name = 'Spwig SMTP Server'
                slug = 'builtin_smtp'

            # Load manifest translations for i18n
            try:
                manifest_translations = load_manifest_translations(builtin_dir)
            except Exception:
                manifest_translations = None

            context = {
                'title': _('Email Provider Setup - Configure Built-in SMTP'),
                'component': BuiltinComponent(),
                'component_name': manifest.get('name', 'Built-in SMTP Server'),
                'component_slug': 'builtin_smtp',
                'manifest': manifest,
                'capabilities': manifest.get('capabilities', {}),
                'credential_schema': manifest.get('credential_schema', []),
                'requires_oauth': False,
                'has_instructions': has_instructions,
                'instructions_html': instructions_html,
                'is_builtin': True,
                'step': 2,
                'total_steps': 6,
                'manifest_translations': manifest_translations,
            }

            return render(request, self.template_name, context)

        # Handle Spwig Hosted Mail provider — credentials are pre-populated
        # and read-only, so we auto-skip Step 2 and go straight to Step 3
        if component_id == 'spwig_hosted_mail':
            self.update_wizard_data(credentials_configured=True)
            return redirect('email_system:wizard_step3')

        # Handle external providers from ComponentRegistry
        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Get component path
            version = component.current_version or 'v1.0.0'
            if not version.startswith('v'):
                version = f'v{version}'

            component_path = INTEGRATIONS_DIR / 'email_provider' / component.slug / version

            # Load manifest for credential schema
            manifest = load_provider_manifest(component_path)
            if not manifest:
                messages.error(request, _('Could not load provider configuration.'))
                return redirect('email_system:wizard_step1')

            # Load setup instructions
            instructions_file = component_path / 'setup_instructions.html'
            has_instructions = False
            instructions_html = ''

            if instructions_file.exists():
                from django.utils.safestring import mark_safe
                from django.template import Template, Context

                with open(instructions_file, 'r', encoding='utf-8') as f:
                    instructions_content = f.read()

                template = Template(instructions_content)
                context = Context({'component': component})
                instructions_html = mark_safe(template.render(context))
                has_instructions = True

            credential_schema = manifest.get('credential_schema', {})
            requires_oauth = manifest.get('capabilities', {}).get('oauth', False)

        except Exception as e:
            messages.error(request, _('Error loading provider: %(error)s') % {'error': str(e)})
            return redirect('email_system:wizard_step1')

        # Enrich credential_schema with stored values for back-navigation
        stored_credentials = wizard_data.get('credentials', {})
        if stored_credentials and credential_schema:
            for field_name, field_config in credential_schema.items():
                if field_name in stored_credentials:
                    field_config['stored_value'] = stored_credentials[field_name]
                    field_config['has_stored_value'] = True

        # Load manifest translations for i18n
        try:
            manifest_translations = load_manifest_translations(component_path)
        except Exception:
            manifest_translations = None

        context = {
            'title': _('Email Provider Setup - Configure Credentials'),
            'component': component,
            'instructions_html': instructions_html,
            'has_instructions': has_instructions,
            'credential_schema': credential_schema,
            'requires_oauth': requires_oauth,
            'wizard_data': wizard_data,
            'step': 2,
            'total_steps': 6,
            'manifest_translations': manifest_translations,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle credentials submission"""
        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get('component_id')
        component_slug = wizard_data.get('component_slug')
        is_builtin = wizard_data.get('is_builtin', False)

        if not component_id:
            messages.warning(request, _('Please select a provider first.'))
            return redirect('email_system:wizard_step1')

        # Handle built-in SMTP provider (no OAuth)
        if component_id == 'builtin_smtp':
            account_name = request.POST.get('account_name', '')
            self.update_wizard_data(
                account_name=account_name,
                credentials_configured=True,
            )
            return redirect('email_system:wizard_step3')

        # Spwig Hosted Mail — credentials are pre-populated, skip to Step 3
        if component_id == 'spwig_hosted_mail':
            self.update_wizard_data(credentials_configured=True)
            return redirect('email_system:wizard_step3')

        # Get component and check if OAuth required
        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Get component path and manifest
            version = component.current_version or 'v1.0.0'
            if not version.startswith('v'):
                version = f'v{version}'

            component_path = INTEGRATIONS_DIR / 'email_provider' / component.slug / version
            manifest = load_provider_manifest(component_path)

            if not manifest:
                messages.error(request, _('Could not load provider configuration.'))
                return redirect('email_system:wizard_step1')

            requires_oauth = manifest.get('capabilities', {}).get('oauth', False)

            if requires_oauth:
                # OAuth provider - get credentials from form
                client_id = request.POST.get('client_id', '').strip()
                client_secret = request.POST.get('client_secret', '').strip()

                if not client_id or not client_secret:
                    messages.error(request, _('Client ID and Client Secret are required for OAuth authentication.'))
                    return redirect('email_system:wizard_step2')

                # Store OAuth credentials in wizard session
                self.update_wizard_data(
                    oauth_client_id=client_id,
                    oauth_client_secret=client_secret,
                )

                logger.info(f"OAuth credentials stored for {component_slug}, initiating OAuth flow")

                # Redirect to OAuth initiate
                return redirect('email_system:oauth_initiate', provider_key=component_slug)
            else:
                # Non-OAuth provider - collect credentials from manifest schema
                account_name = request.POST.get('account_name', '')
                credential_schema = manifest.get('credential_schema', {})

                if credential_schema:
                    credentials, errors = validate_credential_fields(credential_schema, request.POST)

                    if errors:
                        for error in errors:
                            messages.error(request, error)
                        return redirect('email_system:wizard_step2')

                    self.update_wizard_data(
                        account_name=account_name,
                        credentials=credentials,
                        credentials_configured=True,
                    )
                else:
                    self.update_wizard_data(
                        account_name=account_name,
                        credentials_configured=True,
                    )

                return redirect('email_system:wizard_step3')

        except ComponentRegistry.DoesNotExist:
            messages.error(request, _('Invalid provider selected.'))
            return redirect('email_system:wizard_step1')
        except Exception as e:
            logger.error(f"Error in wizard step 2 POST: {e}", exc_info=True)
            messages.error(request, _('Error processing credentials: %(error)s') % {'error': str(e)})
            return redirect('email_system:wizard_step2')


@method_decorator(staff_member_required, name='dispatch')
class ProviderWizardStep3View(WizardSessionMixin, View):
    """
    Step 3: Sender Configuration
    Configure From/Reply-To email addresses
    """

    template_name = 'admin/email_system/wizard/step3_sender.html'

    def get(self, request):
        """Display sender configuration form"""
        wizard_data = self.get_wizard_data()

        if not wizard_data.get('component_id'):
            messages.warning(request, _('Please start from step 1.'))
            return redirect('email_system:wizard_step1')

        context = {
            'title': _('Email Provider Setup - Sender Details'),
            'step': 3,
            'total_steps': 6,
            'wizard_data': wizard_data,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle sender configuration"""
        from_email = request.POST.get('from_email', '').strip()
        from_name = request.POST.get('from_name', '').strip()
        reply_to = request.POST.get('reply_to', '').strip()

        if not from_email:
            messages.error(request, _('From email is required.'))
            return self.get(request)

        if not from_name:
            messages.error(request, _('From name is required.'))
            return self.get(request)

        # Validate email format
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError

        try:
            validate_email(from_email)
            if reply_to:
                validate_email(reply_to)
        except ValidationError:
            messages.error(request, _('Invalid email address format.'))
            return self.get(request)

        # Get wizard data to check if this is built-in provider
        wizard_data = self.get_wizard_data()
        is_builtin = wizard_data.get('is_builtin', False)
        component_id = wizard_data.get('component_id')

        # For built-in SMTP provider: automatically generate DKIM keys
        # (spwig_hosted_mail does NOT need local DKIM generation — the gateway handles it)
        if component_id == 'builtin_smtp':
            from email_system.utils.domain import extract_domain
            from email_system.smtp_server.dkim_handler import DKIMHandler

            try:
                # Extract domain from email
                domain = extract_domain(from_email)

                # Generate DKIM keys automatically
                dkim_handler = DKIMHandler(domain=domain, selector='mail')
                logger.info(f"Automatically generating DKIM keys for domain: {domain}")

                # Generate key pair
                private_key, public_key = dkim_handler.generate_key_pair()

                # Store in wizard session for later use
                self.update_wizard_data(
                    from_email=from_email,
                    from_name=from_name,
                    reply_to=reply_to,
                    dkim_domain=domain,
                    dkim_selector='mail',
                    dkim_private_key=private_key.decode('utf-8'),
                    dkim_public_key=public_key.decode('utf-8'),
                    dkim_auto_generated=True,
                )

                messages.success(request, _('✓ DKIM keys generated automatically for %(domain)s') % {'domain': domain})

                # Start SMTP server if not already running
                self._ensure_smtp_server_running(request)

            except Exception as e:
                logger.error(f"Failed to auto-generate DKIM keys: {e}", exc_info=True)
                messages.warning(request, _('Could not auto-generate DKIM keys. You may need to generate them manually later.'))

                # Continue anyway - keys can be generated later
                # Still try to start SMTP server
                self._ensure_smtp_server_running(request)
                self.update_wizard_data(
                    from_email=from_email,
                    from_name=from_name,
                    reply_to=reply_to,
                )
        else:
            # External providers don't need DKIM generation
            self.update_wizard_data(
                from_email=from_email,
                from_name=from_name,
                reply_to=reply_to,
            )

        return redirect('email_system:wizard_step4')


@method_decorator(staff_member_required, name='dispatch')
class ProviderWizardStep4View(WizardSessionMixin, View):
    """
    Step 4: DNS Configuration & Validation
    Shows DNS requirements from provider, validates SPF/DKIM/DMARC
    Allows skipping with warning if DNS not propagated
    """

    template_name = 'admin/email_system/wizard/step4_dns.html'

    def get(self, request):
        """Display DNS configuration with live validation"""
        wizard_data = self.get_wizard_data()

        if not wizard_data.get('from_email'):
            messages.warning(request, _('Please complete sender configuration first.'))
            return redirect('email_system:wizard_step3')

        try:
            from pathlib import Path
            from django.conf import settings
            from email_system.utils.domain import extract_domain, validate_domain
            from email_system.services.dns_assistant import DNSAssistant
            from email_system.models import EmailDNSCheck
            import json

            component_id = wizard_data.get('component_id')
            is_builtin = wizard_data.get('is_builtin', False)

            # Extract domain from from_email
            from_email = wizard_data.get('from_email')
            extracted_domain = extract_domain(from_email)

            # Get domain override from POST or session
            domain = wizard_data.get('dns_domain', extracted_domain)

            # Spwig Hosted Mail — gateway handles all DNS/DKIM, skip DNS step
            if component_id == 'spwig_hosted_mail':
                context = {
                    'title': _('Email Provider Setup - DNS Configuration'),
                    'component_name': 'Spwig Email',
                    'component_slug': 'spwig_hosted_mail',
                    'domain': domain,
                    'from_email': from_email,
                    'has_dns_template': False,
                    'dns_requirements_html': '',
                    'dns_check_results': None,
                    'is_builtin': True,
                    'is_spwig_hosted': True,
                    'step': 4,
                    'total_steps': 6,
                }
                return render(request, self.template_name, context)

            # Handle built-in SMTP provider
            if component_id == 'builtin_smtp':
                builtin_dir = Path(settings.BASE_DIR) / 'email_system' / 'providers' / 'builtin'
                manifest_path = builtin_dir / 'manifest.json'

                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)

                dns_requirements = manifest.get('dns_requirements', {})

                # Load DNS requirements template
                dns_requirements_file = builtin_dir / 'dns_requirements.html'
                has_dns_template = False
                dns_requirements_html = ''

                if dns_requirements_file.exists():
                    from django.utils.safestring import mark_safe
                    from django.template import Template, Context
                    from email_system.smtp_server.dkim_handler import DKIMHandler
                    import socket

                    # Get external (public) IP address for DNS records
                    from email_system.utils.domain import get_external_ip, is_private_ip
                    server_ip = get_external_ip()

                    # Fallback to internal IP detection if external detection fails
                    # (for local development/testing environments)
                    if not server_ip:
                        try:
                            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            s.connect(("8.8.8.8", 80))
                            server_ip = s.getsockname()[0]
                            s.close()

                            # Warn if detected IP is private
                            if server_ip and is_private_ip(server_ip):
                                logger.warning(f"Detected private IP {server_ip} - DNS records may not work for external email delivery")
                        except Exception:
                            server_ip = None

                    # Extract MX hostname from site URL for MX record recommendations
                    # This ensures MX points to the actual server (e.g., shop.spwig.com)
                    # rather than the email domain (e.g., spwig.com)
                    mx_hostname = domain  # Default to email domain
                    try:
                        site_settings = SiteSettings.objects.first()
                        if site_settings and site_settings.site_url:
                            parsed_url = urlparse(site_settings.site_url)
                            # Extract hostname, remove port if present
                            mx_hostname = parsed_url.netloc.split(':')[0] if parsed_url.netloc else domain
                            logger.info(f"Using MX hostname from site URL: {mx_hostname}")
                    except Exception as e:
                        logger.warning(f"Could not extract hostname from site URL, using domain: {e}")

                    # Generate DKIM keys automatically
                    dkim_selector = dns_requirements.get('dkim_selector', 'mail')
                    dkim_handler = DKIMHandler(domain=domain, selector=dkim_selector)
                    dkim_dns_hostname = f"{dkim_selector}._domainkey.{domain}"

                    # Auto-generate DKIM keys if they don't exist
                    # Check if keys already exist in session or generate new ones
                    dkim_keys = wizard_data.get('dkim_keys')
                    if not dkim_keys:
                        logger.info(f"Auto-generating DKIM keys for domain: {domain}")
                        private_key, public_key = dkim_handler.generate_key_pair()

                        # Store keys in wizard session for later use in Step 6
                        wizard_data['dkim_keys'] = {
                            'private_key': private_key.decode('utf-8'),
                            'public_key': public_key.decode('utf-8'),
                            'selector': dkim_selector
                        }
                        request.session['email_wizard_data'] = wizard_data

                        # Convert public key to DNS record format
                        public_key_str = public_key.decode('utf-8')
                        dkim_keys_exist = True
                    else:
                        # Keys already generated, use existing
                        public_key_str = dkim_keys['public_key']
                        dkim_keys_exist = True

                    # Extract base64 portion of public key for DNS record
                    lines = public_key_str.split('\n')
                    key_data = ''.join([
                        line for line in lines
                        if line and not line.startswith('-----')
                    ])
                    dkim_dns_record = f"v=DKIM1; k=rsa; p={key_data}"

                    # Run DNS validation and fetch existing records
                    # Clear cache to ensure fresh validation results
                    DNSAssistant.clear_cache(domain)

                    dns_assistant = DNSAssistant(domain=domain, dkim_selector=dkim_selector, server_ip=server_ip, mx_hostname=mx_hostname)
                    dns_results = dns_assistant.check_all()

                    # Merge existing SPF record with our requirements
                    spf_recommendation = dns_assistant.merge_spf_record()

                    # Merge existing DMARC record to ensure proper alignment
                    # Preserves existing reporting addresses but ensures aspf=r and adkim=r
                    dmarc_recommendation = dns_assistant.merge_dmarc_record()

                    # Detect DNS provider for smart instructions
                    dns_provider_info = dns_assistant.detect_dns_provider()

                    with open(dns_requirements_file, 'r', encoding='utf-8') as f:
                        dns_template_content = f.read()

                    template = Template(dns_template_content)
                    context_data = Context({
                        'domain': domain,
                        'from_email': from_email,
                        'account_name': wizard_data.get('account_name', ''),
                        'server_ip': server_ip,
                        'mx_hostname': mx_hostname,
                        'dkim_selector': dkim_selector,
                        'dkim_dns_hostname': dkim_dns_hostname,
                        'dkim_dns_record': dkim_dns_record,
                        'dkim_keys_exist': dkim_keys_exist,  # Now True - keys auto-generated
                        'spf_recommendation': spf_recommendation,
                        'dmarc_recommendation': dmarc_recommendation,
                        'dns_results': dns_results,
                        # DNS provider auto-detection
                        'dns_provider': dns_provider_info.get('provider', 'unknown'),
                        'dns_provider_display': dns_provider_info.get('provider_display', 'Other'),
                        'dns_nameservers': dns_provider_info.get('nameservers', []),
                        'dns_confidence': dns_provider_info.get('confidence', 'unknown'),
                    })
                    dns_requirements_html = mark_safe(template.render(context_data))
                    has_dns_template = True

                # Perform DNS validation
                dns_check_results = dns_results if has_dns_template else None

                # Note: We don't create EmailDNSCheck record yet since EmailAccount doesn't exist
                # This will be done when account is created in Step 6

                context = {
                    'title': _('Email Provider Setup - DNS Configuration'),
                    'component_name': manifest.get('name', 'Built-in SMTP Server'),
                    'component_slug': 'builtin_smtp',
                    'manifest': manifest,
                    'dns_requirements': dns_requirements,
                    'domain': domain,
                    'from_email': from_email,
                    'has_dns_template': has_dns_template,
                    'dns_requirements_html': dns_requirements_html,
                    'dns_check_results': dns_check_results,
                    'is_builtin': True,
                    'step': 4,
                    'total_steps': 6,
                }

                return render(request, self.template_name, context)

            # Handle external providers from ComponentRegistry
            component = ComponentRegistry.objects.get(id=component_id)

            # Get component path and load manifest
            version = component.current_version or 'v1.0.0'
            if not version.startswith('v'):
                version = f'v{version}'

            component_path = INTEGRATIONS_DIR / 'email_provider' / component.slug / version

            # Load manifest for DNS requirements
            manifest = load_provider_manifest(component_path)
            if not manifest:
                messages.error(request, _('Could not load provider configuration.'))
                return redirect('email_system:wizard_step3')

            dns_requirements = manifest.get('dns_requirements', {})

            # Load DNS requirements template
            dns_requirements_file = component_path / 'dns_requirements.html'
            has_dns_template = False
            dns_requirements_html = ''

            if dns_requirements_file.exists():
                from django.utils.safestring import mark_safe
                from django.template import Template, Context

                with open(dns_requirements_file, 'r', encoding='utf-8') as f:
                    dns_template_content = f.read()

                template = Template(dns_template_content)
                context_data = Context({
                    'domain': domain,
                    'from_email': from_email,
                    'account_name': wizard_data.get('account_name', ''),
                    'component': component
                })
                dns_requirements_html = mark_safe(template.render(context_data))
                has_dns_template = True

            # Perform DNS validation if domain is valid
            dns_check_results = None
            dns_check_record = None

            if domain and validate_domain(domain):
                # Clear cache for fresh validation
                DNSAssistant.clear_cache(domain)

                # Get DKIM selector and SPF include from manifest
                dkim_selector = dns_requirements.get('dkim_selector')
                spf_include = dns_requirements.get('spf_include', '')
                # Normalize spf_include - strip 'include:' prefix if present
                if spf_include and spf_include.startswith('include:'):
                    spf_include = spf_include[len('include:'):]

                # For SMTP provider: look up provider-specific DNS profile
                # based on the configured SMTP host
                if component.slug == 'smtp':
                    smtp_host = wizard_data.get('credentials', {}).get('host', '').lower().strip()
                    profiles = dns_requirements.get('provider_dns_profiles', {})

                    if smtp_host and profiles:
                        # Try exact match first
                        profile = profiles.get(smtp_host)
                        if not profile:
                            # Try substring match (for Amazon SES regional hosts etc.)
                            for host_pattern, prof in profiles.items():
                                if prof.get('host_match') == 'contains' and host_pattern in smtp_host:
                                    profile = prof
                                    break
                        if profile:
                            dkim_selector = profile.get('dkim_selector') or dkim_selector
                            spf_include = profile.get('spf_include') or spf_include

                # Run DNS validation with provider context
                dns_assistant = DNSAssistant(
                    domain=domain,
                    dkim_selector=dkim_selector,
                    spf_include=spf_include if spf_include else None,
                )
                dns_check_results = dns_assistant.check_all()

                # Note: We don't create EmailDNSCheck record yet since EmailAccount doesn't exist
                # This will be done when account is created in Step 6

            # Check if shop domain differs from email domain
            from django.contrib.sites.models import Site
            current_site = Site.objects.get_current()
            site_domain = current_site.domain.lower().replace('www.', '')
            email_domain_differs = False

            if domain and site_domain and domain != site_domain:
                email_domain_differs = True

            context = {
                'title': _('Email Provider Setup - DNS Configuration'),
                'step': 4,
                'total_steps': 6,
                'wizard_data': wizard_data,
                'component': component,
                'domain': domain,
                'extracted_domain': extracted_domain,
                'from_email': from_email,
                'has_dns_template': has_dns_template,
                'dns_requirements_html': dns_requirements_html,
                'dns_requirements': dns_requirements,
                'dns_check_results': dns_check_results,
                'email_domain_differs': email_domain_differs,
                'site_domain': site_domain,
            }

            return render(request, self.template_name, context)

        except Exception as e:
            messages.error(request, _('Error loading DNS configuration: %(error)s') % {'error': str(e)})
            return redirect('email_system:wizard_step3')

    def post(self, request):
        """Handle DNS configuration - allow domain override and skip"""
        action = request.POST.get('action', 'next')

        # Handle domain override
        if action == 'update_domain':
            new_domain = request.POST.get('domain', '').strip()

            from email_system.utils.domain import validate_domain

            if new_domain and validate_domain(new_domain):
                self.update_wizard_data(dns_domain=new_domain)
                messages.success(request, _('Domain updated. DNS validation refreshed.'))
            else:
                messages.error(request, _('Invalid domain format.'))

            return redirect('email_system:wizard_step4')

        # Handle skip with warning
        elif action == 'skip':
            wizard_data = self.get_wizard_data()
            dns_check_results = request.POST.get('dns_status')

            if dns_check_results and dns_check_results != 'pass':
                messages.warning(
                    request,
                    _('DNS validation incomplete. Your emails may be flagged as spam until DNS records are properly configured.')
                )

            self.update_wizard_data(dns_skipped=True)
            return redirect('email_system:wizard_step5')

        # Normal next (DNS validated or user accepts risk)
        else:
            return redirect('email_system:wizard_step5')


@method_decorator(staff_member_required, name='dispatch')
class ProviderWizardStep5View(WizardSessionMixin, View):
    """
    Step 5: Test Send
    Send a test email to verify configuration
    """

    template_name = 'admin/email_system/wizard/step5_test.html'

    def get(self, request):
        """Display test send form"""
        wizard_data = self.get_wizard_data()

        if not wizard_data.get('from_email'):
            messages.warning(request, _('Please complete previous steps first.'))
            return redirect('email_system:wizard_step1')

        context = {
            'title': _('Email Provider Setup - Test Send'),
            'step': 5,
            'total_steps': 6,
            'wizard_data': wizard_data,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle test send"""
        test_recipient = request.POST.get('test_recipient', '').strip()

        if not test_recipient:
            messages.error(request, _('Please enter a test recipient email.'))
            return self.get(request)

        # Validate email format
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        try:
            validate_email(test_recipient)
        except ValidationError:
            messages.error(request, _('Please enter a valid email address.'))
            return self.get(request)

        wizard_data = self.get_wizard_data()

        try:
            # Get provider information
            is_builtin = wizard_data.get('is_builtin', False)

            # For built-in SMTP provider, ensure SMTP server and Postfix are running
            if component_id == 'builtin_smtp':
                # Check if SMTP server is running
                if not self._ensure_smtp_server_running(request):
                    messages.error(
                        request,
                        _('Built-in SMTP server could not be started. Please check the logs.')
                    )
                    return self.get(request)

                # Verify Postfix is running (Docker/production environments)
                try:
                    import subprocess
                    result = subprocess.run(
                        ['supervisorctl', 'status', 'postfix'],
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    if 'RUNNING' not in result.stdout:
                        messages.error(
                            request,
                            _('⚠ Postfix mail server is not running. Email delivery will fail.')
                        )
                        messages.info(
                            request,
                            _('For Docker: Check container logs. For development: Run "sudo postfix start"')
                        )
                        return self.get(request)
                except (FileNotFoundError, subprocess.TimeoutExpired):
                    # Not in Docker/supervisor environment - skip check
                    logger.debug("Supervisor not available, skipping Postfix status check")
                except Exception as e:
                    logger.warning(f"Could not check Postfix status: {e}")

            component_id = wizard_data.get('component_id')
            if component_id == 'builtin_smtp':
                provider_key = 'builtin_smtp'
            elif component_id == 'spwig_hosted_mail':
                provider_key = 'spwig_hosted_mail'
            else:
                component = ComponentRegistry.objects.get(id=wizard_data['component_id'])
                provider_key = component.slug

            # Get the provider class
            ProviderClass = ProviderRegistry.get_provider(provider_key)
            if not ProviderClass:
                raise Exception(_('Provider not found: %(key)s') % {'key': provider_key})

            # Prepare credentials from wizard data
            credentials = wizard_data.get('credentials', {})

            # For Spwig Hosted Mail, load credentials from existing EmailAccount
            # (injected by provisioning system)
            if provider_key == 'spwig_hosted_mail':
                from email_system.utils.encryption import decrypt_credentials
                try:
                    existing_account = EmailAccount.objects.filter(
                        provider_key='spwig_hosted_mail', is_active=True,
                    ).first()
                    if existing_account and existing_account.credentials:
                        credentials = decrypt_credentials(existing_account.credentials)
                    else:
                        messages.error(
                            request,
                            _('Spwig Email credentials have not been provisioned yet. Please contact support.')
                        )
                        return self.get(request)
                except Exception as e:
                    logger.error("Failed to load spwig_hosted_mail credentials: %s", e)
                    messages.error(request, _('Could not load email credentials.'))
                    return self.get(request)

            # For OAuth providers, ensure we have the tokens
            if wizard_data.get('requires_oauth') and not credentials.get('access_token'):
                messages.error(request, _('OAuth authentication not completed. Please go back to Step 2.'))
                return redirect('email_system:wizard_step2')

            # Initialize provider
            provider = ProviderClass(credentials=credentials, config={})

            # Build test message
            subject = _('Test Email from %(name)s') % {'name': wizard_data.get('from_name', 'Spwig')}

            html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{subject}</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
        <h1 style="color: #0066cc; margin: 0 0 10px 0;">✓ Email Test Successful!</h1>
        <p style="margin: 0; color: #666;">Your email provider is configured correctly.</p>
    </div>

    <div style="background-color: #fff; padding: 20px; border: 1px solid #dee2e6; border-radius: 5px;">
        <h2 style="color: #333; margin: 0 0 15px 0;">Configuration Details:</h2>

        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="padding: 8px 0; color: #666; font-weight: bold;">Provider:</td>
                <td style="padding: 8px 0;">{provider.provider_name}</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; color: #666; font-weight: bold;">From Email:</td>
                <td style="padding: 8px 0;">{wizard_data.get('from_email', 'N/A')}</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; color: #666; font-weight: bold;">From Name:</td>
                <td style="padding: 8px 0;">{wizard_data.get('from_name', 'N/A')}</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; color: #666; font-weight: bold;">Reply-To:</td>
                <td style="padding: 8px 0;">{wizard_data.get('reply_to', 'N/A')}</td>
            </tr>
        </table>
    </div>

    <div style="margin-top: 20px; padding: 15px; background-color: #e7f3ff; border-left: 4px solid #0066cc; border-radius: 3px;">
        <p style="margin: 0; font-size: 14px;">
            <strong>Next Steps:</strong><br>
            1. Check that this email arrived in your inbox<br>
            2. Verify it's not in spam<br>
            3. Check the email headers for SPF/DKIM/DMARC authentication<br>
            4. Complete the wizard to save your configuration
        </p>
    </div>

    <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #dee2e6; text-align: center; color: #999; font-size: 12px;">
        <p>This is an automated test message from Spwig Email System Setup Wizard</p>
    </div>
</body>
</html>
"""

            text_body = f"""
Email Test Successful!
{'=' * 50}

Your email provider is configured correctly.

Configuration Details:
- Provider: {provider.provider_name}
- From Email: {wizard_data.get('from_email', 'N/A')}
- From Name: {wizard_data.get('from_name', 'N/A')}
- Reply-To: {wizard_data.get('reply_to', 'N/A')}

Next Steps:
1. Check that this email arrived in your inbox
2. Verify it's not in spam
3. Check the email headers for SPF/DKIM/DMARC authentication
4. Complete the wizard to save your configuration

---
This is an automated test message from Spwig Email System Setup Wizard
"""

            message = {
                'message_id': f'test-{wizard_data.get("component_id", "smtp")}',
                'to': [test_recipient],
                'subject': subject,
                'html': html_body,
                'text': text_body,
                'from_email': wizard_data.get('from_email'),
                'from_name': wizard_data.get('from_name'),
                'reply_to': wizard_data.get('reply_to') if wizard_data.get('reply_to') else None,
                'cc': [],
                'bcc': [],
                'headers': {},
                'return_path': wizard_data.get('from_email', ''),
                'attachments': [],
                'inline_images': [],
                'tags': [],
                'metadata': {},
            }

            # Send the test email
            logger.info(f"Sending test email to {test_recipient} via {provider_key}")
            result = provider.send(message)

            if result.get('accepted'):
                messages.success(
                    request,
                    _('✓ Test email sent successfully to %(email)s! Check your inbox.') % {'email': test_recipient}
                )

                if result.get('provider_message_id'):
                    messages.info(
                        request,
                        _('Message ID: %(id)s') % {'id': result['provider_message_id']}
                    )

                self.update_wizard_data(
                    test_sent=True,
                    test_recipient=test_recipient,
                    test_message_id=result.get('provider_message_id'),
                )

                return redirect('email_system:wizard_step6')
            else:
                error_msg = result.get('error', _('Unknown error'))
                messages.error(
                    request,
                    _('Failed to send test email: %(error)s') % {'error': error_msg}
                )
                return self.get(request)

        except Exception as e:
            logger.exception(f"Error sending test email: {e}")
            messages.error(
                request,
                _('Error sending test email: %(error)s') % {'error': str(e)}
            )
            return self.get(request)


@method_decorator(staff_member_required, name='dispatch')
class ProviderWizardStep6View(WizardSessionMixin, View):
    """
    Step 6: Complete
    Save the email account and finish wizard
    """

    template_name = 'admin/email_system/wizard/step6_complete.html'

    def get(self, request):
        """Display completion summary"""
        wizard_data = self.get_wizard_data()

        if not wizard_data.get('from_email'):
            messages.warning(request, _('Please complete all previous steps.'))
            return redirect('email_system:wizard_step1')

        try:
            component_id = wizard_data.get('component_id')

            # For built-in providers, create pseudo-component for template display
            if component_id == 'builtin_smtp':
                builtin_dir = Path(settings.BASE_DIR) / 'email_system' / 'providers' / 'builtin'
                manifest_path = builtin_dir / 'manifest.json'

                with open(manifest_path, 'r') as f:
                    import json
                    manifest = json.load(f)

                class BuiltinComponent:
                    id = 'builtin_smtp'
                    slug = 'builtin_smtp'
                    name = manifest.get('name', 'Built-in SMTP Server')
                    is_builtin = True

                component = BuiltinComponent()

            elif component_id == 'spwig_hosted_mail':
                class SpwigHostedComponent:
                    id = 'spwig_hosted_mail'
                    slug = 'spwig_hosted_mail'
                    name = 'Spwig Email'
                    is_builtin = True

                component = SpwigHostedComponent()
            else:
                component = ComponentRegistry.objects.get(id=wizard_data['component_id'])

            context = {
                'title': _('Email Provider Setup - Complete'),
                'step': 6,
                'total_steps': 6,
                'wizard_data': wizard_data,
                'component': component,
                'is_builtin': is_builtin,
            }

            return render(request, self.template_name, context)

        except Exception as e:
            messages.error(request, _('Error: %(error)s') % {'error': str(e)})
            return redirect('email_system:wizard_step1')

    def post(self, request):
        """Save email account and complete wizard"""
        wizard_data = self.get_wizard_data()
        make_default = request.POST.get('make_default') == 'on'

        try:
            with transaction.atomic():
                site = Site.objects.get_current()
                is_builtin = wizard_data.get('is_builtin', False)

                component_id = wizard_data.get('component_id')

                # Prepare credentials based on provider type
                if component_id == 'builtin_smtp':
                    # For built-in SMTP: store DKIM keys and local SMTP settings
                    dkim_keys = wizard_data.get('dkim_keys', {})
                    dkim_private_key = dkim_keys.get('private_key') or wizard_data.get('dkim_private_key', '')
                    dkim_public_key = dkim_keys.get('public_key') or wizard_data.get('dkim_public_key', '')
                    dkim_selector = dkim_keys.get('selector') or wizard_data.get('dkim_selector', 'mail')

                    credentials = {
                        'smtp_host': '127.0.0.1',
                        'smtp_port': 2525,
                        'smtp_use_tls': False,
                        'dkim_domain': wizard_data.get('dkim_domain', ''),
                        'dkim_selector': dkim_selector,
                        'dkim_private_key': dkim_private_key,
                        'dkim_public_key': dkim_public_key,
                    }

                    provider_key = 'builtin_smtp'
                    component = None
                    account_name = wizard_data.get('account_name', 'Spwig SMTP Server')

                elif component_id == 'spwig_hosted_mail':
                    # For Spwig Hosted Mail: credentials are pre-provisioned.
                    # Load from existing account or use what provisioning injected.
                    from email_system.utils.encryption import decrypt_credentials
                    existing = EmailAccount.objects.filter(
                        provider_key='spwig_hosted_mail',
                    ).first()
                    if existing and existing.credentials:
                        credentials = decrypt_credentials(existing.credentials)
                    else:
                        credentials = wizard_data.get('credentials', {})

                    provider_key = 'spwig_hosted_mail'
                    component = None
                    account_name = wizard_data.get('account_name', 'Spwig Email')

                else:
                    # For external providers: credentials are provider-specific
                    component = ComponentRegistry.objects.get(id=wizard_data['component_id'])
                    provider_key = component.slug
                    account_name = wizard_data.get('account_name', component.name)

                    # Get credentials from wizard session (OAuth or non-OAuth)
                    credentials_data = wizard_data.get('credentials')

                    if credentials_data:
                        logger.info(f"Using credentials from wizard session for {provider_key}")
                        credentials = credentials_data
                    else:
                        logger.warning(f"No credentials found in wizard session for {provider_key}")
                        credentials = {}

                # Create email account
                account = EmailAccount.objects.create(
                    site=site,
                    component=component,
                    provider_key=provider_key,
                    name=account_name,
                    from_email=wizard_data['from_email'],
                    from_name=wizard_data['from_name'],
                    reply_to=wizard_data.get('reply_to', ''),
                    is_default=make_default,
                    is_active=True,
                    connection_status='unknown',
                    credentials=encrypt_credentials(credentials),
                    dns_domain=wizard_data.get('dkim_domain', ''),
                    created_by=request.user,
                )

                # For built-in SMTP provider: automatically start SMTP server
                if component_id == 'builtin_smtp':
                    try:
                        import subprocess

                        # Try to start SMTP server via supervisor (Docker environment)
                        result = subprocess.run(
                            ['supervisorctl', 'start', 'smtp-server'],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )

                        if result.returncode == 0:
                            logger.info(f"Built-in SMTP server started for account {account.id}")
                            messages.success(
                                request,
                                _('✓ Email account "%(name)s" created successfully!') % {'name': account.name}
                            )
                            messages.success(
                                request,
                                _('✓ Built-in SMTP server is running and ready to send emails.')
                            )
                        else:
                            # Supervisor not available or server already running
                            logger.info(f"Built-in SMTP server configured for account {account.id} (may already be running)")
                            messages.success(
                                request,
                                _('✓ Email account "%(name)s" created successfully!') % {'name': account.name}
                            )
                            messages.info(
                                request,
                                _('The SMTP server should already be running. If emails don\'t send, please contact your system administrator.')
                            )

                    except FileNotFoundError:
                        # Not in Docker/supervisor environment - server should have been started in Step 3
                        logger.info(f"Built-in SMTP server configured for account {account.id} (supervisor not available, should be running from Step 3)")
                        messages.success(
                            request,
                            _('✓ Email account "%(name)s" created successfully!') % {'name': account.name}
                        )
                        messages.info(
                            request,
                            _('Your email system is configured and ready to use.')
                        )

                    except subprocess.TimeoutExpired:
                        logger.warning(f"Timeout starting SMTP server for account {account.id}")
                        messages.success(
                            request,
                            _('✓ Email account "%(name)s" created successfully!') % {'name': account.name}
                        )
                        messages.info(
                            request,
                            _('Email system configured. If you experience issues sending emails, please contact your system administrator.')
                        )

                    except Exception as e:
                        logger.error(f"Error starting SMTP server for account {account.id}: {e}")
                        messages.success(
                            request,
                            _('✓ Email account "%(name)s" created successfully!') % {'name': account.name}
                        )
                        messages.info(
                            request,
                            _('Your email account is configured. The SMTP server should be running from the previous setup steps.')
                        )
                else:
                    messages.success(
                        request,
                        _('Email account "%(name)s" created successfully!') % {'name': account.name}
                    )

                # Clear wizard data
                self.clear_wizard_data()

                # Redirect to email accounts list
                return redirect('admin:email_system_emailaccount_changelist')

        except Exception as e:
            logger.error(f"Error creating email account: {e}", exc_info=True)
            messages.error(request, _('Error creating account: %(error)s') % {'error': str(e)})
            return self.get(request)
