"""
Payout Provider Connection Wizard Views

Multi-step wizard for connecting payout providers (PayPal, Airwallex, etc.)
Pattern follows exchange_rates/views/wizard.py architecture.
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
from django.urls import reverse
from pathlib import Path
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)

from component_updates.integration_paths import INTEGRATIONS_DIR
from component_updates.models import ComponentRegistry
from payout_providers.models import PayoutProviderAccount
from payout_providers.loader import PayoutProviderLoader
from payment_providers.utils.encryption import encrypt_credentials
from providers_common.utils import load_manifest_translations, validate_credential_fields


def load_provider_manifest(provider_path: Path) -> dict:
    """Load manifest.json from provider directory"""
    manifest_file = provider_path / 'manifest.json'
    if manifest_file.exists():
        with open(manifest_file, 'r') as f:
            return json.load(f)
    return None


class WizardSessionMixin:
    """Mixin for managing wizard session data"""

    SESSION_KEY = 'payout_provider_wizard_data'

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


@method_decorator(staff_member_required, name='dispatch')
class ProviderWizardStep1View(WizardSessionMixin, View):
    """
    Step 1: Select Provider
    Displays available payout providers from ComponentRegistry
    """

    template_name = 'admin/payout_providers/wizard/step1_select.html'

    def get(self, request):
        """Display provider selection"""
        # Clear any existing wizard data when starting fresh
        self.clear_wizard_data()

        # Auto-skip if provider pre-selected from browse page
        provider_slug = request.GET.get('provider')
        if provider_slug:
            try:
                component = ComponentRegistry.objects.get(
                    slug=provider_slug, component_type='payout_provider'
                )
                self.update_wizard_data(
                    component_id=component.id,
                    component_name=component.name,
                    component_slug=component.slug,
                )
                return redirect('payout_providers:wizard_step2')
            except ComponentRegistry.DoesNotExist:
                pass  # Fall through to normal step 1

        # Get all payout provider components
        providers = ComponentRegistry.objects.filter(
            component_type='payout_provider'
        ).order_by('name')

        # Load manifests for each provider
        provider_data = []
        for component in providers:
            try:
                # Load from component directory using the actual version
                version = component.current_version or 'v1.0.0'
                if not version.startswith('v'):
                    version = f'v{version}'

                provider_dir = INTEGRATIONS_DIR / 'payout_provider' / component.slug / version

                if provider_dir.exists():
                    manifest = load_provider_manifest(provider_dir)
                    if manifest:
                        # Get logo URL
                        logo_file = manifest.get('logo', {})
                        if isinstance(logo_file, dict):
                            logo_filename = logo_file.get('file', '')
                        else:
                            logo_filename = logo_file if logo_file else ''

                        logo_url = ''
                        if logo_filename:
                            logo_path = provider_dir / logo_filename
                            if logo_path.exists():
                                logo_url = static(f'payout_provider/{component.slug}/current/{logo_filename}')

                        component.thumbnail_url = logo_url

                        provider_data.append({
                            'component': component,
                            'manifest': manifest,
                            'capabilities': manifest.get('capabilities', {}),
                            'supported_methods': manifest.get('supported_methods', []),
                            'supported_currencies': manifest.get('supported_currencies', []),
                        })
            except Exception as e:
                print(f"Could not load manifest for {component.name}: {e}")

        context = {
            'title': _('Connect Payout Provider - Select Provider'),
            'providers': provider_data,
            'step': 1,
            'total_steps': 4,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle provider selection"""
        component_id = request.POST.get('component_id')

        if not component_id:
            messages.error(request, _('Please select a provider.'))
            return redirect('payout_providers:wizard_step1')

        try:
            component = ComponentRegistry.objects.get(id=component_id, component_type='payout_provider')
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _('Invalid provider selected.'))
            return redirect('payout_providers:wizard_step1')

        # Store selected component in session
        self.update_wizard_data(
            component_id=component_id,
            component_name=component.name,
            component_slug=component.slug,
        )

        return redirect('payout_providers:wizard_step2')


@method_decorator(staff_member_required, name='dispatch')
class ProviderWizardStep2View(WizardSessionMixin, View):
    """
    Step 2: Setup Instructions
    Shows provider-specific setup instructions from setup_instructions.html
    """

    template_name = 'admin/payout_providers/wizard/step2_setup.html'

    def get(self, request):
        """Display setup instructions"""
        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get('component_id')

        if not component_id:
            messages.warning(request, _('Please select a provider first.'))
            return redirect('payout_providers:wizard_step1')

        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Get component path using the actual version
            version = component.current_version or 'v1.0.0'
            if not version.startswith('v'):
                version = f'v{version}'

            component_path = INTEGRATIONS_DIR / 'payout_provider' / component.slug / version
            instructions_file = component_path / 'setup_instructions.html'

            has_instructions = False
            instructions_html = ''

            if instructions_file.exists():
                from django.utils.safestring import mark_safe
                from django.template import Template, Context

                # Read the setup instructions HTML file
                with open(instructions_file, 'r', encoding='utf-8') as f:
                    instructions_content = f.read()

                # Build webhook URL for template context
                webhook_url = request.build_absolute_uri(
                    reverse(f'payout_webhooks:webhook_{component.slug}')
                ) if component.slug in ['paypal', 'airwallex'] else ''

                # Render it as a Django template to support template variables
                template = Template(instructions_content)
                context = Context({
                    'component': component,
                    'webhook_url': webhook_url,
                })
                instructions_html = mark_safe(template.render(context))
                has_instructions = True
            else:
                messages.warning(
                    request,
                    _('Setup instructions not found for %(provider)s. Please contact support.') % {'provider': component.name}
                )

        except Exception as e:
            messages.error(request, _('Error loading provider: %(error)s') % {'error': str(e)})
            return redirect('payout_providers:wizard_step1')

        # Load manifest translations for i18n
        try:
            manifest_translations = load_manifest_translations(component_path)
        except Exception:
            manifest_translations = None

        context = {
            'title': _('Connect Payout Provider - Setup Instructions'),
            'component': component,
            'instructions_html': instructions_html,
            'has_instructions': has_instructions,
            'step': 2,
            'total_steps': 4,
            'manifest_translations': manifest_translations,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle continue to credentials"""
        return redirect('payout_providers:wizard_step3')


@method_decorator(staff_member_required, name='dispatch')
class ProviderWizardStep3View(WizardSessionMixin, View):
    """
    Step 3: Enter Credentials
    Dynamic form based on provider's credential schema
    """

    template_name = 'admin/payout_providers/wizard/step3_credentials.html'

    def get(self, request):
        """Display credentials form"""
        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get('component_id')

        if not component_id:
            messages.warning(request, _('Please select a provider first.'))
            return redirect('payout_providers:wizard_step1')

        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Get component path using the actual version
            version = component.current_version or 'v1.0.0'
            if not version.startswith('v'):
                version = f'v{version}'

            component_path = INTEGRATIONS_DIR / 'payout_provider' / component.slug / version
            manifest = load_provider_manifest(component_path) if component_path.exists() else None

            if not manifest:
                messages.error(request, _('Could not load provider configuration.'))
                return redirect('payout_providers:wizard_step1')

            credential_schema = manifest.get('credential_schema', {})
            signup_url = manifest.get('signup_url', '')

        except Exception as e:
            messages.error(request, _('Error loading provider: %(error)s') % {'error': str(e)})
            return redirect('payout_providers:wizard_step1')

        context = {
            'title': _('Connect Payout Provider - Enter Credentials'),
            'component': component,
            'credential_schema': credential_schema,
            'signup_url': signup_url,
            'step': 3,
            'total_steps': 4,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle credentials submission"""
        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get('component_id')

        if not component_id:
            return redirect('payout_providers:wizard_step1')

        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Get component path using the actual version
            version = component.current_version or 'v1.0.0'
            if not version.startswith('v'):
                version = f'v{version}'

            component_path = INTEGRATIONS_DIR / 'payout_provider' / component.slug / version
            manifest = load_provider_manifest(component_path) if component_path.exists() else None
            credential_schema = manifest.get('credential_schema', {}) if manifest else {}
        except Exception:
            messages.error(request, _('Error loading provider configuration.'))
            return redirect('payout_providers:wizard_step1')

        # Validate and collect credentials from POST data
        all_fields, errors = validate_credential_fields(credential_schema, request.POST)

        # Separate sensitive credentials from non-sensitive settings
        credentials = {}
        settings_data = {}
        for field_name, field_config in credential_schema.items():
            value = all_fields.get(field_name)
            if value is None or (isinstance(value, str) and not value):
                continue
            if field_config.get('sensitive', False):
                credentials[field_name] = value
            else:
                settings_data[field_name] = value

        if errors:
            for error in errors:
                messages.error(request, error)
            return self.get(request)

        # Get optional provider name from form
        provider_name = request.POST.get('provider_name', '').strip()

        # Store in session
        self.update_wizard_data(
            credentials=credentials,
            settings=settings_data,
            provider_name=provider_name
        )

        return redirect('payout_providers:wizard_step4')


@method_decorator(staff_member_required, name='dispatch')
class ProviderWizardStep4View(WizardSessionMixin, View):
    """
    Step 4: Test Connection & Save
    Tests the provider connection with entered credentials and saves if successful
    """

    template_name = 'admin/payout_providers/wizard/step4_test.html'

    def get(self, request):
        """Display test connection page"""
        wizard_data = self.get_wizard_data()

        if not wizard_data.get('component_id') or not wizard_data.get('credentials'):
            messages.warning(request, _('Please complete previous steps first.'))
            return redirect('payout_providers:wizard_step1')

        component_id = wizard_data.get('component_id')

        try:
            component = ComponentRegistry.objects.get(id=component_id)
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _('Provider not found.'))
            return redirect('payout_providers:wizard_step1')

        context = {
            'title': _('Connect Payout Provider - Test Connection'),
            'component': component,
            'step': 4,
            'total_steps': 4,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Perform connection test and save if successful"""
        action = request.POST.get('action', 'test')

        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get('component_id')
        component_slug = wizard_data.get('component_slug')
        credentials = wizard_data.get('credentials', {})
        settings_data = wizard_data.get('settings', {})
        provider_name = wizard_data.get('provider_name', '')

        if not component_id or not credentials:
            return JsonResponse({'success': False, 'error': 'Missing data'}, status=400)

        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Get provider class from loader
            provider_class = PayoutProviderLoader.get_provider(component_slug)

            if not provider_class:
                return JsonResponse({
                    'success': False,
                    'error': _('Provider implementation not found.')
                }, status=404)

            # Merge credentials and settings for provider config
            config = {**credentials, **settings_data}

            if action == 'test':
                # Test connection only
                try:
                    provider = provider_class(config)
                    test_result = provider.test_connection()

                    # Store test result in session
                    self.update_wizard_data(
                        connection_test_passed=test_result.get('success', False),
                        connection_test_message=test_result.get('message', ''),
                    )

                    return JsonResponse(test_result)
                except Exception:
                    logger.exception('Error testing payout provider connection')
                    return JsonResponse({
                        'success': False,
                        'error': _('An unexpected error occurred during connection test.')
                    }, status=500)

            elif action == 'save':
                # Save provider account
                try:
                    # Create provider instance to test first
                    provider = provider_class(config)
                    test_result = provider.test_connection()

                    if not test_result.get('success'):
                        return JsonResponse({
                            'success': False,
                            'error': test_result.get('message', _('Connection test failed'))
                        }, status=400)

                    # Encrypt credentials
                    encrypted_credentials = encrypt_credentials(credentials)

                    # Check if this is the first provider of this type
                    is_first_provider = not PayoutProviderAccount.objects.filter(
                        provider_type=component_slug,
                        is_active=True
                    ).exists()

                    # Get supported methods from manifest
                    version = component.current_version or 'v1.0.0'
                    if not version.startswith('v'):
                        version = f'v{version}'
                    component_path = INTEGRATIONS_DIR / 'payout_provider' / component.slug / version
                    manifest = load_provider_manifest(component_path) if component_path.exists() else {}
                    supported_methods = manifest.get('supported_methods', [])

                    # Create provider account
                    with transaction.atomic():
                        provider_account = PayoutProviderAccount.objects.create(
                            provider_type=component_slug,
                            component=component,
                            name=provider_name or component.name,
                            credentials_encrypted=encrypted_credentials,
                            settings=settings_data,
                            supported_methods=supported_methods,
                            is_active=True,
                            is_default=is_first_provider,
                            connection_status='connected',
                        )

                    # Clear wizard data
                    self.clear_wizard_data()

                    return JsonResponse({
                        'success': True,
                        'message': _('Provider connected successfully!'),
                        'redirect_url': reverse(
                            'admin:payout_providers_payoutprovideraccount_change',
                            args=[provider_account.id]
                        )
                    })

                except Exception:
                    logger.exception('Error saving payout provider account')
                    return JsonResponse({
                        'success': False,
                        'error': _('An unexpected error occurred while saving.')
                    }, status=500)

            else:
                return JsonResponse({'success': False, 'error': _('Invalid action')}, status=400)

        except Exception:
            logger.exception('Unexpected error in payout wizard step 4')
            return JsonResponse({
                'success': False,
                'error': _('An unexpected error occurred.')
            }, status=500)
