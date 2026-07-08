"""
Provider Connection Wizard Views
Multi-step wizard for connecting shipping API providers
"""
import json
import logging

from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.translation import gettext as _
from django.http import JsonResponse

logger = logging.getLogger(__name__)

from component_updates.models import ComponentRegistry
from shipping.models import ProviderAccount
from shipping.providers.registry import ProviderRegistry
from shipping.providers.loader import load_provider_manifest
from shipping.utils.encryption import encrypt_credentials
from providers_common.utils import load_manifest_translations, validate_credential_fields


class WizardSessionMixin:
    """Mixin for managing wizard session data"""

    SESSION_KEY = 'provider_wizard_data'

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
    Displays available shipping providers from ComponentRegistry
    """

    template_name = 'admin/shipping/wizard/step1_select.html'

    def get(self, request):
        """Display provider selection"""
        from pathlib import Path
        from django.conf import settings

        # Clear any existing wizard data when starting fresh
        self.clear_wizard_data()

        # Auto-skip if provider pre-selected from browse page
        provider_slug = request.GET.get('provider')
        if provider_slug:
            try:
                component = ComponentRegistry.objects.get(
                    slug=provider_slug, component_type='shipping_provider'
                )
                self.update_wizard_data(
                    component_id=component.id,
                    component_name=component.name,
                )
                return redirect('shipping:wizard_step2')
            except ComponentRegistry.DoesNotExist:
                pass  # Fall through to normal step 1

        # Get all shipping provider components
        providers = ComponentRegistry.objects.filter(
            component_type='shipping_provider'
        ).order_by('name')

        # Load manifests for each provider
        provider_data = []
        for component in providers:
            try:
                # Load from component directory
                # Expected: components_data/integrations/shipping_provider/{slug}/current/
                from component_updates.integration_paths import INTEGRATIONS_DIR
                provider_dir = INTEGRATIONS_DIR / 'shipping_provider' / component.slug / 'current'

                if provider_dir.exists():
                    manifest = load_provider_manifest(provider_dir)
                    if manifest:
                        provider_data.append({
                            'component': component,
                            'manifest': manifest,
                            'capabilities': manifest.get('capabilities', {}),
                        })
                else:
                    logger.warning("Component directory not found for %s: %s", component.name, provider_dir)
            except Exception as e:
                # Log but don't fail if manifest can't be loaded
                logger.error("Could not load manifest for %s: %s", component.name, e)

        context = {
            'title': _('Connect Shipping Provider - Select Provider'),
            'providers': provider_data,
            'step': 1,
            'total_steps': 5,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle provider selection"""
        component_id = request.POST.get('component_id')

        if not component_id:
            messages.error(request, _('Please select a provider.'))
            return redirect('shipping:wizard_step1')

        try:
            component = ComponentRegistry.objects.get(id=component_id, component_type='shipping_provider')
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _('Invalid provider selected.'))
            return redirect('shipping:wizard_step1')

        # Store selected component in session
        self.update_wizard_data(
            component_id=component_id,
            component_name=component.name,
        )

        return redirect('shipping:wizard_step2')


@method_decorator(staff_member_required, name='dispatch')
class ProviderWizardStep2View(WizardSessionMixin, View):
    """
    Step 2: Setup Instructions
    Shows provider-specific setup instructions from setup_instructions.html
    """

    template_name = 'admin/shipping/wizard/step2_setup.html'

    def get(self, request):
        """Display setup instructions"""
        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get('component_id')

        if not component_id:
            messages.warning(request, _('Please select a provider first.'))
            return redirect('shipping:wizard_step1')

        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Get the component path using ProviderService
            from shipping.services import ProviderService
            from django.utils.safestring import mark_safe
            from django.template import Template, Context

            component_path = ProviderService.get_component_path(component.slug)
            instructions_file = component_path / 'setup_instructions.html'

            has_instructions = False
            instructions_html = ''

            if instructions_file.exists():
                # Read the setup instructions HTML file
                with open(instructions_file, 'r', encoding='utf-8') as f:
                    instructions_content = f.read()

                # Render it as a Django template to support {% trans %} tags
                template = Template(instructions_content)
                context = Context({'component': component})
                instructions_html = mark_safe(template.render(context))
                has_instructions = True
            else:
                messages.warning(
                    request,
                    _('Setup instructions not found for %(provider)s. Please contact support.') % {'provider': component.name}
                )

        except Exception as e:
            messages.error(request, _('Error loading provider: %(error)s') % {'error': str(e)})
            return redirect('shipping:wizard_step1')

        # Load manifest translations for i18n
        try:
            manifest_translations = load_manifest_translations(component_path)
        except Exception:
            manifest_translations = None

        context = {
            'title': _('Connect Shipping Provider - Setup Instructions'),
            'component': component,
            'instructions_html': instructions_html,
            'has_instructions': has_instructions,
            'step': 2,
            'total_steps': 5,
            'manifest_translations': manifest_translations,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle continue to credentials"""
        # Just continue to next step - no form data to process
        return redirect('shipping:wizard_step3')


@method_decorator(staff_member_required, name='dispatch')
class ProviderWizardStep3View(WizardSessionMixin, View):
    """
    Step 3: Enter Credentials
    Dynamic form based on provider's credential schema
    """

    template_name = 'admin/shipping/wizard/step3_credentials.html'

    def get(self, request):
        """Display credentials form"""
        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get('component_id')

        if not component_id:
            messages.warning(request, _('Please select a provider first.'))
            return redirect('shipping:wizard_step1')

        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Get the component path using ProviderService
            from shipping.services import ProviderService
            component_path = ProviderService.get_component_path(component.slug)
            manifest = load_provider_manifest(component_path) if component_path.exists() else None

            if not manifest:
                messages.error(request, _('Could not load provider configuration.'))
                return redirect('shipping:wizard_step1')

            credential_schema = manifest.get('credential_schema', {})
            signup_url = manifest.get('signup_url', '')

        except Exception as e:
            messages.error(request, _('Error loading provider: %(error)s') % {'error': str(e)})
            return redirect('shipping:wizard_step1')

        context = {
            'title': _('Connect Shipping Provider - Enter Credentials'),
            'component': component,
            'credential_schema': credential_schema,
            'signup_url': signup_url,
            'step': 3,
            'total_steps': 5,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle credentials submission"""
        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get('component_id')

        if not component_id:
            return redirect('shipping:wizard_step1')

        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Get the component path using ProviderService
            from shipping.services import ProviderService
            component_path = ProviderService.get_component_path(component.slug)
            manifest = load_provider_manifest(component_path) if component_path.exists() else None
            credential_schema = manifest.get('credential_schema', {}) if manifest else {}
        except Exception:
            messages.error(request, _('Error loading provider configuration.'))
            return redirect('shipping:wizard_step1')

        # Validate and collect credentials from POST data
        credentials, errors = validate_credential_fields(credential_schema, request.POST)

        if errors:
            for error in errors:
                messages.error(request, error)
            return self.get(request)

        # Store credentials in session (will be encrypted when saved)
        self.update_wizard_data(credentials=credentials)

        return redirect('shipping:wizard_step4')


@method_decorator(staff_member_required, name='dispatch')
class ProviderWizardStep4View(WizardSessionMixin, View):
    """
    Step 4: Test Connection
    Tests the provider connection with entered credentials
    """

    template_name = 'admin/shipping/wizard/step4_test.html'

    def get(self, request):
        """Display test connection page"""
        wizard_data = self.get_wizard_data()

        if not wizard_data.get('component_id') or not wizard_data.get('credentials'):
            messages.warning(request, _('Please complete previous steps first.'))
            return redirect('shipping:wizard_step1')

        component_id = wizard_data.get('component_id')

        try:
            component = ComponentRegistry.objects.get(id=component_id)
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _('Provider not found.'))
            return redirect('shipping:wizard_step1')

        context = {
            'title': _('Connect Shipping Provider - Test Connection'),
            'component': component,
            'step': 4,
            'total_steps': 5,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Perform connection test"""
        wizard_data = self.get_wizard_data()
        component_id = wizard_data.get('component_id')
        credentials = wizard_data.get('credentials', {})

        if not component_id or not credentials:
            return JsonResponse({'success': False, 'error': 'Missing data'}, status=400)

        try:
            component = ComponentRegistry.objects.get(id=component_id)

            # Get provider class from registry
            provider_class = ProviderRegistry.get_provider(component.slug)

            if not provider_class:
                return JsonResponse({
                    'success': False,
                    'error': _('Provider implementation not found.')
                }, status=404)

            # Create temporary provider instance
            provider = provider_class(credentials=credentials)

            # Test connection
            test_result = provider.test_connection()

            # Store test result in session
            self.update_wizard_data(
                connection_test_passed=test_result.get('success', False),
                connection_test_message=test_result.get('message', ''),
            )

            return JsonResponse(test_result)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


@method_decorator(staff_member_required, name='dispatch')
class ProviderWizardStep5View(WizardSessionMixin, View):
    """
    Step 5: Configure & Save
    Final configuration and save provider account
    """

    template_name = 'admin/shipping/wizard/step5_configure.html'

    def get(self, request):
        """Display configuration form"""
        wizard_data = self.get_wizard_data()

        # Verify all required data is present
        if not all([
            wizard_data.get('component_id'),
            wizard_data.get('credentials'),
            wizard_data.get('connection_test_passed'),
        ]):
            messages.warning(request, _('Please complete all previous steps.'))
            return redirect('shipping:wizard_step1')

        component_id = wizard_data.get('component_id')

        try:
            component = ComponentRegistry.objects.get(id=component_id)
        except ComponentRegistry.DoesNotExist:
            messages.error(request, _('Provider not found.'))
            return redirect('shipping:wizard_step1')

        context = {
            'title': _('Connect Shipping Provider - Configure'),
            'component': component,
            'step': 5,
            'total_steps': 5,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Save provider account"""
        wizard_data = self.get_wizard_data()

        display_name = request.POST.get('display_name', '').strip()
        is_default = request.POST.get('is_default') == 'on'

        if not display_name:
            messages.error(request, _('Display name is required.'))
            return self.get(request)

        try:
            from django.utils import timezone

            component = ComponentRegistry.objects.get(id=wizard_data['component_id'])
            credentials = wizard_data['credentials']

            # Encrypt credentials before storing
            credentials_encrypted = encrypt_credentials(credentials)

            # Create provider account
            provider_account = ProviderAccount.objects.create(
                component=component,
                user=request.user,
                display_name=display_name,
                credentials_encrypted=credentials_encrypted,
                is_active=True,
                is_default=is_default,
                connection_status='connected',
                last_tested_at=timezone.now(),  # Set connection health timestamp
            )

            messages.success(
                request,
                _('Provider "%(name)s" connected successfully!') % {'name': display_name}
            )

            # Clear wizard session data
            self.clear_wizard_data()

            # Redirect to provider list
            return redirect('admin:shipping_provideraccount_changelist')

        except Exception as e:
            messages.error(request, _('Error saving provider: %(error)s') % {'error': str(e)})
            return self.get(request)
