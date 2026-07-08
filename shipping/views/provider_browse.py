"""
Provider Browse View
Displays available shipping providers from update server for installation
"""
import json

from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.translation import gettext as _, get_language
from django.http import JsonResponse
from django_countries import countries
from packaging import version

from shipping.services import ProviderService
from component_updates.models import ComponentRegistry
from providers_common.utils import get_translated_provider_fields


@method_decorator(staff_member_required, name='dispatch')
class ProviderBrowseView(View):
    """
    Browse and install shipping providers from update server.

    Displays:
    - Providers available on update server (to install)
    - Locally installed providers (to configure)
    - Installation status for each provider
    """

    template_name = 'admin/shipping/providers/browse.html'

    def get(self, request):
        """Display provider browse page"""
        provider_service = ProviderService()

        # Get selected country filter
        selected_country = request.GET.get('country', '')

        # Try to get available providers from update server
        try:
            available_providers = provider_service.fetch_available_providers()
        except Exception as e:
            messages.warning(
                request,
                _('Could not fetch providers from update server. Showing installed providers only.')
            )
            available_providers = []

        # Get installed providers for version comparison
        installed_db = {p.slug: p.current_version for p in ComponentRegistry.objects.filter(component_type='shipping_provider')}

        # Get current admin language for manifest-based i18n
        lang = get_language() or 'en'

        # Process providers and add update info
        all_providers = []
        all_countries = set()

        for provider in available_providers:
            slug = provider.get('slug')
            latest_version = provider.get('current_version') or provider.get('version')
            manifest = provider.get('manifest', {})
            supported_countries = manifest.get('supported_countries', [])

            # Collect all countries
            all_countries.update(supported_countries)

            # Apply country filter if selected
            if selected_country and selected_country not in supported_countries:
                continue

            # Check if installed and compare versions
            is_installed = slug in installed_db
            current_version = installed_db.get(slug, '')
            has_update = False

            if is_installed and current_version and latest_version:
                has_update = self._compare_versions(current_version, latest_version)

            # Flatten provider data for template
            # Try to get capabilities from root level first (for simplified manifest format),
            # then fall back to nested manifest object
            capabilities = provider.get('capabilities') or manifest.get('capabilities', {})
            setup = provider.get('setup') or manifest.get('setup', {})
            documentation_url = provider.get('documentation_url') or manifest.get('documentation_url', '')

            # Translate name/description from manifest translations
            translated = get_translated_provider_fields(manifest, lang)

            provider_data = {
                'slug': slug,
                'name': translated['name'] or provider.get('name', ''),
                'description': translated['description'] or provider.get('description', ''),
                'version': latest_version,
                'thumbnail_url': provider.get('thumbnail_url', ''),
                'homepage_url': provider.get('homepage_url', ''),
                'documentation_url': documentation_url,
                'capabilities': capabilities,
                'setup': setup,
                'is_installed': is_installed,
                'current_version': current_version,
                'latest_version': latest_version,
                'has_update': has_update,
            }

            all_providers.append(provider_data)

        # Convert country codes to names for dropdown
        country_choices = [
            {'code': code, 'name': countries.name(code)}
            for code in sorted(all_countries)
            if code  # Filter out empty codes
        ]

        # Count installed providers
        installed_count = sum(1 for p in all_providers if p['is_installed'])

        # Prepare provider data for modal (with all manifest data)
        providers_for_modal = []
        for provider in available_providers:
            manifest = provider.get('manifest', {})
            slug = provider.get('slug')
            latest_version = provider.get('current_version') or provider.get('version')
            is_installed = slug in installed_db
            current_version = installed_db.get(slug, '')
            has_update = False

            if is_installed and current_version and latest_version:
                has_update = self._compare_versions(current_version, latest_version)

            capabilities = provider.get('capabilities') or manifest.get('capabilities', {})

            # Translate name/description for modal display
            modal_translated = get_translated_provider_fields(manifest, lang)

            modal_data = {
                'slug': slug,
                'name': modal_translated['name'] or provider.get('name', ''),
                'description': modal_translated['description'] or provider.get('description', ''),
                'thumbnail_url': provider.get('thumbnail_url', ''),
                'homepage_url': provider.get('homepage_url', ''),
                'documentation_url': provider.get('documentation_url') or manifest.get('documentation_url', ''),
                'capabilities': capabilities,
                'regions': manifest.get('regions', {}),
                'compliance': manifest.get('compliance', {}),
                'pricing_info': manifest.get('pricing_info', {}),
                'translations': dict(manifest.get('translations', {}), default_language=manifest.get('default_language', 'en')),
                'is_installed': is_installed,
                'current_version': current_version,
                'latest_version': latest_version,
                'has_update': has_update,
                'configure_url': '/admin/shipping/providers/',
            }
            providers_for_modal.append(modal_data)

        context = {
            'title': _('Browse Shipping Providers'),
            'providers': all_providers,
            'providers_json': providers_for_modal,
            'all_countries': country_choices,
            'selected_country': selected_country,
            'selected_country_name': countries.name(selected_country) if selected_country else '',
            'installed_count': installed_count,
            'has_update_server': len(available_providers) > 0,
        }

        return render(request, self.template_name, context)

    def _compare_versions(self, current: str, latest: str) -> bool:
        """Compare semantic versions (e.g., '1.0.0' vs '1.1.0')"""
        try:
            return version.parse(latest) > version.parse(current)
        except Exception:
            return False


@staff_member_required
def install_provider_ajax(request, provider_slug):
    """
    AJAX endpoint to install a provider.

    POST to install provider from update server.
    Returns JSON with success status and redirect URL.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    # Check if already installed
    if ComponentRegistry.objects.filter(slug=provider_slug, component_type='shipping_provider').exists():
        from django.urls import reverse
        return JsonResponse({
            'success': True,
            'already_installed': True,
            'message': _('Provider is already installed'),
            'redirect_url': reverse('shipping:wizard_step1'),
        })

    # Install provider using UpdateManager (following email_system pattern)
    try:
        from component_updates.services import UpdateManager
        from django.db import transaction
        from pathlib import Path
        from django.conf import settings
        import os

        update_manager = UpdateManager()

        # Get available providers from update server
        available_providers = update_manager.list_available_components(component_type='shipping_provider')

        # Find the requested provider
        provider_info = None
        for provider in available_providers:
            if provider.get('slug') == provider_slug:
                provider_info = provider
                break

        if not provider_info:
            return JsonResponse({
                'success': False,
                'error': _('Provider not found on update server.')
            }, status=404)

        # Get the latest version
        latest_version = provider_info.get('current_version') or provider_info.get('version')
        provider_name = provider_info.get('name', provider_slug)
        provider_description = provider_info.get('description', '')

        if not latest_version:
            return JsonResponse({
                'success': False,
                'error': _('Could not determine provider version.')
            }, status=400)

        # Create ComponentRegistry entry and install
        with transaction.atomic():
            # Create the component registry entry
            component = ComponentRegistry.objects.create(
                slug=provider_slug,
                name=provider_name,
                description=provider_description,
                component_type='shipping_provider',
                current_version=latest_version
            )

            # Download the package
            try:
                package_path = update_manager.download_component(component, latest_version)
            except Exception as e:
                component.delete()  # Rollback component creation
                return JsonResponse({
                    'success': False,
                    'error': _('Failed to download provider: %(error)s') % {'error': str(e)}
                }, status=500)

            # Install the package
            try:
                update_manager._install_package(component, package_path, latest_version)
            except Exception as e:
                component.delete()  # Rollback component creation
                return JsonResponse({
                    'success': False,
                    'error': _('Failed to install provider: %(error)s') % {'error': str(e)}
                }, status=500)

            # Create 'current' symlink to the installed version
            try:
                from component_updates.integration_paths import INTEGRATIONS_DIR
                provider_base_dir = INTEGRATIONS_DIR / 'shipping_provider' / provider_slug
                current_link = provider_base_dir / 'current'
                version_dir = f'v{latest_version}' if not latest_version.startswith('v') else latest_version

                # Remove existing symlink if it exists
                if current_link.exists() or current_link.is_symlink():
                    current_link.unlink()

                # Create new symlink
                current_link.symlink_to(version_dir)

                # Reload providers to make the new provider available
                from shipping.providers.registry import ProviderRegistry
                ProviderRegistry.reload_providers()
            except Exception as e:
                # Log warning but don't fail - symlink is optional
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Failed to create symlink for {provider_slug}: {e}")

        from django.urls import reverse
        return JsonResponse({
            'success': True,
            'message': _('Provider %(name)s installed successfully') % {'name': provider_name},
            'redirect_url': reverse('shipping:wizard_step1'),
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': _('Installation failed: %(error)s') % {'error': str(e)}
        }, status=500)


@staff_member_required
def update_provider_ajax(request, provider_slug):
    """
    AJAX endpoint to update a provider.

    POST to update provider from update server to latest version.
    Returns JSON with success status and new version.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    try:
        from component_updates.services import UpdateManager

        update_manager = UpdateManager()

        # Check if provider is installed
        try:
            component = ComponentRegistry.objects.get(slug=provider_slug, component_type='shipping_provider')
        except ComponentRegistry.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': _('Provider not installed')
            }, status=404)

        # Get latest version from update server
        available = update_manager.list_available_components(component_type='shipping_provider')
        latest_version = None
        for item in available:
            if item.get('slug') == provider_slug:
                latest_version = item.get('current_version')
                break

        if not latest_version:
            return JsonResponse({
                'success': False,
                'error': _('Could not find latest version on update server')
            }, status=404)

        # Use UpdateManager to install the update (pass the component object and version)
        success = update_manager.install_update(component=component, version=latest_version)

        if success:
            # Get new version
            component.refresh_from_db()
            return JsonResponse({
                'success': True,
                'message': _('Provider updated successfully to v%(version)s') % {'version': component.current_version},
                'new_version': component.current_version,
            })
        else:
            return JsonResponse({
                'success': False,
                'error': _('Update failed')
            }, status=400)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
