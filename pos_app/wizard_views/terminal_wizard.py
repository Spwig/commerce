"""
Terminal Provider Connection Wizard Views

Multi-step wizard for connecting POS terminal payment providers (e.g., Stripe Terminal).
5-step flow: Select → Setup Instructions → Credentials → Test → Configure
"""
import json
import logging
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.templatetags.static import static
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View

from component_updates.integration_paths import INTEGRATIONS_DIR
from component_updates.models import ComponentRegistry
from payment_providers.utils.encryption import encrypt_credentials
from pos_app.models import POSTerminalProvider
from pos_app.terminal_providers import TerminalProviderRegistry
from providers_common.utils import load_manifest_translations

logger = logging.getLogger(__name__)


def load_terminal_manifest(component_dir: Path) -> dict:
    """Load and parse manifest.json from a terminal provider component directory."""
    manifest_path = component_dir / 'manifest.json'
    if not manifest_path.exists():
        return {}
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Failed to load manifest from {manifest_path}: {e}")
        return {}


class WizardSessionMixin:
    """Mixin for managing wizard session data."""

    SESSION_KEY = 'terminal_provider_wizard_data'

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


@method_decorator(staff_member_required, name='dispatch')
class TerminalWizardStep1View(WizardSessionMixin, View):
    """
    Step 1: Select Provider

    Displays available terminal providers:
    - Component-based providers from ComponentRegistry (e.g., Stripe Terminal)
    - Built-in manual provider for standalone terminals
    """

    template_name = 'admin/pos_app/wizard/step1_select.html'

    def get(self, request):
        """Display provider selection."""
        # Clear any existing wizard data when starting fresh
        self.clear_wizard_data()

        # Get all terminal provider components
        components = ComponentRegistry.objects.filter(
            component_type='terminal_provider'
        ).order_by('name')

        # Load manifests for each provider
        provider_data = []
        for component in components:
            try:
                provider_dir = INTEGRATIONS_DIR / 'terminal_provider' / component.slug / 'current'

                if provider_dir.exists():
                    manifest = load_terminal_manifest(provider_dir)
                    if manifest:
                        # Compute logo URL if logo is specified
                        logo_url = None
                        logo_raw = manifest.get('logo')
                        if isinstance(logo_raw, dict):
                            logo_file = logo_raw.get('file', '')
                        else:
                            logo_file = logo_raw if logo_raw else ''
                            if logo_file:
                                # Static path: terminal_providers/{slug}/current/{logo_file}
                                logo_url = static(
                                    f'terminal_providers/{component.slug}/current/{logo_file}'
                                )

                        provider_data.append({
                            'component': component,
                            'manifest': manifest,
                            'logo_url': logo_url,
                            'capabilities': manifest.get('capabilities', {}),
                            'supported_readers': manifest.get('supported_readers', []),
                            'is_builtin': False,
                        })
            except Exception as e:
                logger.warning(f"Could not load manifest for {component.slug}: {e}")

        # Add built-in manual provider
        provider_data.append({
            'component': None,
            'manifest': {
                'name': 'Manual Entry',
                'slug': 'manual',
                'description': _('For standalone terminals that process cards independently. '
                                 'Card details are entered manually after each transaction.'),
                'logo': None,
            },
            'capabilities': {'payment_methods': ['manual']},
            'supported_readers': [],
            'is_builtin': True,
        })

        context = {
            'title': _('Connect Terminal Provider - Select Provider'),
            'providers': provider_data,
            'step': 1,
            'total_steps': 5,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle provider selection."""
        provider_type = request.POST.get('provider_type')

        if not provider_type:
            messages.error(request, _('Please select a provider.'))
            return redirect('pos_admin:wizard_step1')

        if provider_type == 'manual':
            # Manual provider - skip to step 5 (no credentials needed)
            self.update_wizard_data(
                provider_type='manual',
                is_builtin=True,
                connection_test_passed=True,  # Manual doesn't need testing
            )
            return redirect('pos_admin:wizard_step5')

        # Component-based provider
        component_id = request.POST.get('component_id')

        if not component_id:
            messages.error(request, _('Invalid provider selected.'))
            return redirect('pos_admin:wizard_step1')

        try:
            component = ComponentRegistry.objects.get(
                id=component_id, component_type='terminal_provider'
            )
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _('Invalid provider selected.'))
            return redirect('pos_admin:wizard_step1')

        # Store selected component in session
        self.update_wizard_data(
            provider_type='component',
            component_id=str(component_id),
            component_name=component.name,
            component_slug=component.slug,
            is_builtin=False,
        )

        return redirect('pos_admin:wizard_step2')


@method_decorator(staff_member_required, name='dispatch')
class TerminalWizardStep2View(WizardSessionMixin, View):
    """
    Step 2: Setup Instructions

    Shows provider-specific setup instructions from setup_instructions.html.
    """

    template_name = 'admin/pos_app/wizard/step2_setup.html'

    def get(self, request):
        """Display setup instructions."""
        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get('component_id')

        if not component_id:
            messages.warning(request, _('Please select a provider first.'))
            return redirect('pos_admin:wizard_step1')

        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Get component path
            component_path = INTEGRATIONS_DIR / 'terminal_provider' / component.slug / 'current'
            instructions_file = component_path / 'setup_instructions.html'

            setup_instructions = ''
            if instructions_file.exists():
                from django.utils.safestring import mark_safe
                from django.template import Template, Context

                with open(instructions_file, 'r', encoding='utf-8') as f:
                    instructions_content = f.read()

                # Render as Django template to support {% trans %} tags
                template = Template(instructions_content)
                context = Context({'provider': {'component': component}})
                setup_instructions = mark_safe(template.render(context))

            # Load manifest for signup URL
            manifest = load_terminal_manifest(component_path)
            signup_url = manifest.get('signup_url', '')

        except Exception as e:
            logger.error(f"Error loading provider setup: {e}")
            messages.error(request, _('Error loading provider: %(error)s') % {'error': str(e)})
            return redirect('pos_admin:wizard_step1')

        # Load manifest translations for i18n
        try:
            manifest_translations = load_manifest_translations(component_path)
        except Exception:
            manifest_translations = None

        context = {
            'title': _('Connect Terminal Provider - Setup Instructions'),
            'provider': {'component': component, 'signup_url': signup_url},
            'setup_instructions': setup_instructions,
            'step': 2,
            'total_steps': 5,
            'manifest_translations': manifest_translations,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Continue to credentials step."""
        return redirect('pos_admin:wizard_step3')


@method_decorator(staff_member_required, name='dispatch')
class TerminalWizardStep3View(WizardSessionMixin, View):
    """
    Step 3: Enter Credentials

    Dynamic form based on provider's credential_schema from manifest.
    """

    template_name = 'admin/pos_app/wizard/step3_credentials.html'

    def get(self, request):
        """Display credentials form."""
        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get('component_id')

        if not component_id:
            messages.warning(request, _('Please select a provider first.'))
            return redirect('pos_admin:wizard_step1')

        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Get component path and load manifest
            component_path = INTEGRATIONS_DIR / 'terminal_provider' / component.slug / 'current'
            manifest = load_terminal_manifest(component_path)

            if not manifest:
                messages.error(request, _('Could not load provider configuration.'))
                return redirect('pos_admin:wizard_step1')

            credential_schema = manifest.get('credential_schema', {})

        except Exception as e:
            logger.error(f"Error loading credentials form: {e}")
            messages.error(request, _('Error loading provider: %(error)s') % {'error': str(e)})
            return redirect('pos_admin:wizard_step1')

        context = {
            'title': _('Connect Terminal Provider - Enter Credentials'),
            'provider': {'component': component},
            'credential_schema': credential_schema,
            'step': 3,
            'total_steps': 5,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle credentials submission."""
        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get('component_id')

        if not component_id:
            return redirect('pos_admin:wizard_step1')

        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Load manifest for credential schema
            component_path = INTEGRATIONS_DIR / 'terminal_provider' / component.slug / 'current'
            manifest = load_terminal_manifest(component_path)
            credential_schema = manifest.get('credential_schema', {})
        except Exception:
            messages.error(request, _('Error loading provider configuration.'))
            return redirect('pos_admin:wizard_step1')

        # Collect credentials from POST data
        credentials = {}
        errors = []

        for field_name, field_config in credential_schema.items():
            value = request.POST.get(field_name, '').strip()

            # Check required fields
            if field_config.get('required', False) and not value:
                errors.append(
                    _('%(field)s is required.') % {'field': field_config.get('label', field_name)}
                )
            else:
                credentials[field_name] = value

        # Get display name
        display_name = request.POST.get('display_name', '').strip()
        if not display_name:
            display_name = manifest.get('name', component.name)

        if errors:
            for error in errors:
                messages.error(request, error)
            return self.get(request)

        # Store credentials in session
        self.update_wizard_data(
            credentials=credentials,
            display_name=display_name,
        )

        return redirect('pos_admin:wizard_step4')


@method_decorator(staff_member_required, name='dispatch')
class TerminalWizardStep4View(WizardSessionMixin, View):
    """
    Step 4: Test Connection

    Tests the provider connection with entered credentials.
    """

    template_name = 'admin/pos_app/wizard/step4_test.html'

    def get(self, request):
        """Display test connection page."""
        wizard_data = self.get_wizard_data()

        if not wizard_data.get('component_id') or not wizard_data.get('credentials'):
            messages.warning(request, _('Please complete previous steps first.'))
            return redirect('pos_admin:wizard_step1')

        component_id = wizard_data.get('component_id')

        try:
            component = ComponentRegistry.objects.get(id=component_id)
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _('Provider not found.'))
            return redirect('pos_admin:wizard_step1')

        context = {
            'title': _('Connect Terminal Provider - Test Connection'),
            'provider': {'component': component},
            'step': 4,
            'total_steps': 5,
            'test_result': wizard_data.get('test_result'),
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Perform connection test."""
        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get('component_id')
        credentials = wizard_data.get('credentials', {})

        if not component_id or not credentials:
            return JsonResponse({'success': False, 'error': 'Missing data'}, status=400)

        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Get provider class from registry
            provider_class = TerminalProviderRegistry.get_provider(component.slug)

            if not provider_class:
                test_result = {
                    'success': False,
                    'message': _('Provider implementation not found.'),
                }
            else:
                # Create temporary provider instance
                provider = provider_class(credentials=credentials)

                # Test connection
                test_result = provider.test_connection()

            # Store test result in session
            self.update_wizard_data(
                test_result=test_result,
                connection_test_passed=test_result.get('success', False),
            )

            # For AJAX requests, return JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(test_result)

            # For regular POST, redirect back to show results
            return redirect('pos_admin:wizard_step4')

        except Exception as e:
            logger.error(f"Connection test error: {e}")
            test_result = {
                'success': False,
                'message': str(e),
            }
            self.update_wizard_data(test_result=test_result)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(test_result, status=500)

            return redirect('pos_admin:wizard_step4')


@method_decorator(staff_member_required, name='dispatch')
class TerminalWizardStep5View(WizardSessionMixin, View):
    """
    Step 5: Configure & Save

    Final configuration and save terminal provider account.
    """

    template_name = 'admin/pos_app/wizard/step5_configure.html'

    def get(self, request):
        """Display configuration form."""
        wizard_data = self.get_wizard_data()
        is_builtin = wizard_data.get('is_builtin', False)

        # Verify required data
        if is_builtin:
            # Manual provider - just need provider_type
            if wizard_data.get('provider_type') != 'manual':
                messages.warning(request, _('Please select a provider first.'))
                return redirect('pos_admin:wizard_step1')

            context = {
                'title': _('Configure Terminal Provider - Manual Entry'),
                'provider': {
                    'component': None,
                    'name': 'Manual Entry',
                    'slug': 'manual',
                },
                'is_builtin': True,
                'step': 5,
                'total_steps': 5,
                'settings_schema': {},
            }
        else:
            # Component-based provider
            if not all([
                wizard_data.get('component_id'),
                wizard_data.get('credentials'),
                wizard_data.get('connection_test_passed'),
            ]):
                messages.warning(request, _('Please complete all previous steps.'))
                return redirect('pos_admin:wizard_step1')

            component_id = wizard_data.get('component_id')

            try:
                component = ComponentRegistry.objects.get(id=component_id)

                # Load manifest for settings schema
                component_path = INTEGRATIONS_DIR / 'terminal_provider' / component.slug / 'current'
                manifest = load_terminal_manifest(component_path)
                settings_schema = manifest.get('settings_schema', {})

            except Exception as e:
                logger.error(f"Error loading configuration: {e}")
                messages.error(request, _('Error loading provider configuration.'))
                return redirect('pos_admin:wizard_step1')

            context = {
                'title': _('Configure Terminal Provider - %(name)s') % {'name': component.name},
                'provider': {'component': component, 'name': component.name},
                'settings_schema': settings_schema,
                'display_name': wizard_data.get('display_name', component.name),
                'is_builtin': False,
                'step': 5,
                'total_steps': 5,
            }

        return render(request, self.template_name, context)

    def post(self, request):
        """Save the terminal provider configuration."""
        wizard_data = self.get_wizard_data()
        is_builtin = wizard_data.get('is_builtin', False)

        try:
            if is_builtin:
                # Create manual provider
                provider = POSTerminalProvider.objects.create(
                    provider_key='manual',
                    display_name=request.POST.get('display_name', 'Manual Entry'),
                    component=None,
                    credentials_encrypted={},
                    provider_settings={},
                    is_active=True,
                    connection_status='connected',  # Manual is always "connected"
                )
            else:
                # Create component-based provider
                component_id = wizard_data.get('component_id')
                component = ComponentRegistry.objects.get(id=component_id)

                credentials = wizard_data.get('credentials', {})
                encrypted_credentials = encrypt_credentials(credentials)

                # Collect provider settings from POST
                component_path = INTEGRATIONS_DIR / 'terminal_provider' / component.slug / 'current'
                manifest = load_terminal_manifest(component_path)
                settings_schema = manifest.get('settings_schema', {})

                provider_settings = {}
                for field_name, field_config in settings_schema.items():
                    value = request.POST.get(field_name, '')
                    if field_config.get('type') == 'boolean':
                        value = field_name in request.POST
                    provider_settings[field_name] = value

                display_name = request.POST.get(
                    'display_name',
                    wizard_data.get('display_name', component.name)
                )

                provider = POSTerminalProvider.objects.create(
                    provider_key=manifest.get('provider_key', component.slug),
                    display_name=display_name,
                    component=component,
                    credentials_encrypted=encrypted_credentials,
                    provider_settings=provider_settings,
                    is_active=True,
                    connection_status='connected',
                )

            # Clear wizard session data
            self.clear_wizard_data()

            messages.success(
                request,
                _('Terminal provider "%(name)s" has been connected successfully.') % {
                    'name': provider.display_name
                }
            )

            return redirect('admin:pos_app_posterminalprovider_changelist')

        except Exception as e:
            logger.error(f"Error saving terminal provider: {e}")
            messages.error(request, _('Error saving provider: %(error)s') % {'error': str(e)})
            return self.get(request)
