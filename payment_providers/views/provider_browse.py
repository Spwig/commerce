"""
Payment Provider Browse View
Displays available payment providers from update server for installation
"""
import json

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.translation import gettext as _, get_language
from django.http import JsonResponse
from django_countries import countries
from packaging import version

from component_updates.models import ComponentRegistry
from component_updates.services import UpdateManager
from providers_common.utils import get_translated_provider_fields
from shipping.models import ShippingCountry


@method_decorator(staff_member_required, name='dispatch')
class ProviderBrowseView(View):
    """
    Browse and install payment providers from update server.

    Displays:
    - Providers available on update server (to install)
    - Locally installed providers (to configure)
    - Installation status for each provider
    - Providers filtered by merchant's default country
    """

    template_name = 'admin/payment_providers/providers/browse.html'

    def get(self, request):
        """Display provider browse page"""
        update_manager = UpdateManager()

        # Get selected country filter (defaults to merchant's default country on first visit only)
        from core.utils import get_default_country
        default_country = get_default_country()

        # Check if country filter was explicitly provided (including empty string for "All")
        if 'country' in request.GET:
            selected_country = request.GET.get('country', '')
        else:
            # First visit - use default country
            selected_country = default_country

        # Try to get available providers from update server
        try:
            available_providers = update_manager.list_available_components(component_type='payment_provider')
        except Exception as e:
            messages.warning(
                request,
                _('Could not fetch providers from update server. Showing installed providers only.')
            )
            available_providers = []

        # Get installed providers for version comparison
        installed_db = {
            p.slug: p.current_version
            for p in ComponentRegistry.objects.filter(component_type='payment_provider')
        }

        # Get current admin language for manifest-based i18n
        lang = get_language() or 'en'

        # Process providers and add update info
        all_providers = []
        all_countries = set()

        for provider in available_providers:
            slug = provider.get('slug')
            latest_version = provider.get('current_version') or provider.get('version')
            manifest = provider.get('manifest', {})

            # Get supported countries/regions from manifest
            regions = manifest.get('regions', {})
            supported = regions.get('supported', [])
            restricted = regions.get('restricted', [])

            # Normalize supported countries - handle both list of codes and special values
            supported_countries = []
            if isinstance(supported, list):
                for item in supported:
                    if item == 'global' or item == 'worldwide':
                        # Global provider - add all countries
                        supported_countries = [c.code for c in countries]
                        break
                    elif len(item) == 2:  # Country code
                        supported_countries.append(item)

            # Remove restricted countries
            if restricted:
                supported_countries = [c for c in supported_countries if c not in restricted]

            # Collect all countries
            all_countries.update(supported_countries)

            # Apply country filter if selected
            if selected_country and supported_countries and selected_country not in supported_countries:
                continue

            # Check if installed and compare versions
            is_installed = slug in installed_db
            current_version = installed_db.get(slug, '')
            has_update = False

            if is_installed and current_version and latest_version:
                has_update = self._compare_versions(current_version, latest_version)

            # Flatten provider data for template
            capabilities = provider.get('capabilities') or manifest.get('capabilities', {})
            pricing_info = manifest.get('pricing_info', {})

            # Translate name/description from manifest translations
            translated = get_translated_provider_fields(manifest, lang)

            provider_data = {
                'slug': slug,
                'name': translated['name'] or provider.get('name', ''),
                'description': translated['description'] or provider.get('description', ''),
                'version': latest_version,
                'thumbnail_url': provider.get('thumbnail_url', ''),
                'homepage_url': provider.get('homepage_url', ''),
                'documentation_url': provider.get('documentation_url') or manifest.get('documentation', ''),
                'capabilities': capabilities,
                'pricing_info': pricing_info,
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

        # Get merchant's shipping countries for regional availability display
        shipping_countries = ShippingCountry.objects.filter(
            site_id=1,  # Single-tenant - always site 1
            is_active=True
        ).values_list('country_code', flat=True)

        shipping_countries_list = list(shipping_countries)
        shipping_countries_data = [
            {'code': code, 'name': countries.name(code)}
            for code in shipping_countries_list
        ]

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

            # Translate name/description for modal display
            modal_translated = get_translated_provider_fields(manifest, lang)

            modal_data = {
                'slug': slug,
                'name': modal_translated['name'] or provider.get('name', ''),
                'description': modal_translated['description'] or provider.get('description', ''),
                'thumbnail_url': provider.get('thumbnail_url', ''),
                'homepage_url': provider.get('homepage_url', ''),
                'documentation_url': provider.get('documentation_url') or manifest.get('documentation', ''),
                'capabilities': provider.get('capabilities') or manifest.get('capabilities', {}),
                'regions': manifest.get('regions', {}),
                'compliance': manifest.get('compliance', {}),
                'pricing_info': manifest.get('pricing_info', {}),
                'translations': dict(manifest.get('translations', {}), default_language=manifest.get('default_language', 'en')),
                'is_installed': is_installed,
                'current_version': current_version,
                'latest_version': latest_version,
                'has_update': has_update,
                'configure_url': '/admin/payment_providers/paymentprovideraccount/',
            }
            providers_for_modal.append(modal_data)

        context = {
            'title': _('Browse Payment Providers'),
            'providers': all_providers,
            'providers_json': providers_for_modal,
            'shipping_countries': shipping_countries_data,
            'shipping_countries_json': shipping_countries_list,
            'all_countries': country_choices,
            'selected_country': selected_country,
            'selected_country_name': countries.name(selected_country) if selected_country else '',
            'default_country': default_country,
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
    AJAX endpoint to install a payment provider.

    POST to install provider from update server.
    Returns JSON with success status and redirect URL.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    # Check if already installed — registry entry AND files on disk both
    # have to be present. A registry row with missing files is a half-installed
    # state (e.g. the Docker named volume was wiped after install) and would
    # otherwise short-circuit installation here, hiding the provider from the
    # wizard with no obvious recovery path. Treat that case as not installed
    # and continue into the install path below, where the orphan row gets
    # deleted before re-downloading.
    existing = ComponentRegistry.objects.filter(
        slug=provider_slug, component_type='payment_provider'
    ).first()

    if existing:
        from component_updates.integration_paths import INTEGRATIONS_DIR
        provider_dir = INTEGRATIONS_DIR / 'payment_provider' / provider_slug / 'current'
        if provider_dir.exists():
            # Truly installed.
            from django.urls import reverse
            return JsonResponse({
                'success': True,
                'already_installed': True,
                'message': _('Provider is already installed'),
                'redirect_url': reverse('admin:payment_providers_paymentprovideraccount_changelist'),
            })
        # Orphan registry row — files are gone, self-heal by removing the row
        # and falling through to the normal install path.
        import logging
        logging.getLogger(__name__).warning(
            "Self-healing orphan registry row for payment_provider '%s' (no files at %s)",
            provider_slug, provider_dir,
        )
        existing.delete()

    # Install provider using UpdateManager
    try:
        from django.db import transaction
        from pathlib import Path
        from django.conf import settings

        update_manager = UpdateManager()

        # Get available providers from update server
        available_providers = update_manager.list_available_components(component_type='payment_provider')

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
                component_type='payment_provider',
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
                provider_base_dir = INTEGRATIONS_DIR / 'payment_provider' / provider_slug
                current_link = provider_base_dir / 'current'
                version_dir = f'v{latest_version}' if not latest_version.startswith('v') else latest_version

                # Remove existing symlink if it exists
                if current_link.exists() or current_link.is_symlink():
                    current_link.unlink()

                # Create new symlink
                current_link.symlink_to(version_dir)

                # Reload providers to make the new provider available
                from payment_providers.providers.registry import ProviderRegistry
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
            'redirect_url': reverse('admin:payment_providers_paymentprovideraccount_changelist'),
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': _('Installation failed: %(error)s') % {'error': str(e)}
        }, status=500)


@staff_member_required
def update_provider_ajax(request, provider_slug):
    """
    AJAX endpoint to update a payment provider.

    POST to update provider from update server to latest version.
    Returns JSON with success status and new version.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    try:
        update_manager = UpdateManager()

        # Check if provider is installed
        try:
            component = ComponentRegistry.objects.get(slug=provider_slug, component_type='payment_provider')
        except ComponentRegistry.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': _('Provider not installed')
            }, status=404)

        # Get latest version from update server
        available = update_manager.list_available_components(component_type='payment_provider')
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

        # Use UpdateManager to install the update
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
