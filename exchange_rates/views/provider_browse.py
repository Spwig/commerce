"""
Provider Browse View
Displays available exchange rate providers for installation
"""

import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.views import View
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)

from component_updates.models import ComponentRegistry
from providers_common.utils import get_translated_provider_fields


@method_decorator(staff_member_required, name="dispatch")
class ProviderBrowseView(View):
    """
    Browse exchange rate providers.

    Displays:
    - Locally installed providers from components directory
    - Installation status for each provider
    """

    template_name = "admin/exchange_rates/providers/browse.html"

    def get(self, request):
        """Display provider browse page"""
        # Get filter parameter
        has_live_rates = request.GET.get("live_rates")
        has_historical = request.GET.get("historical")
        has_crypto = request.GET.get("crypto")

        # Try to fetch available providers from update server
        available_from_server = []
        has_update_server = False

        try:
            from component_updates.services import UpdateManager

            update_manager = UpdateManager()
            available_from_server = update_manager.list_available_components(
                component_type="exchange_rate_provider"
            )
            has_update_server = True
        except Exception as e:
            # If update server fails, we'll fall back to locally installed providers
            logger.warning("Could not fetch from update server: %s", e)

        # Get installed providers for version comparison
        installed_db = {
            p.slug: p.current_version
            for p in ComponentRegistry.objects.filter(component_type="exchange_rate_provider")
        }

        # Get current admin language for manifest-based i18n
        lang = get_language() or "en"

        # Process providers from update server
        all_providers = []

        for provider in available_from_server:
            slug = provider.get("slug")
            latest_version = provider.get("current_version") or provider.get("version")
            manifest = provider.get("manifest", {})

            # Get capabilities
            capabilities = provider.get("capabilities") or manifest.get("capabilities", {})

            # Apply capability filters
            if has_live_rates and not capabilities.get("live_rates"):
                continue
            if has_historical and not capabilities.get("historical"):
                continue
            if has_crypto and not capabilities.get("crypto"):
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

            # Translate name/description from manifest translations
            translated = get_translated_provider_fields(manifest, lang)

            provider_data = {
                "slug": slug,
                "name": translated["name"] or provider.get("name", ""),
                "description": translated["description"] or provider.get("description", ""),
                "version": latest_version,
                "thumbnail_url": provider.get("thumbnail_url", ""),
                "homepage_url": provider.get("homepage_url", ""),
                "documentation_url": provider.get("documentation_url")
                or manifest.get("documentation_url", ""),
                "capabilities": capabilities,
                "rate_limits": manifest.get("rate_limits", {}),
                "supported_currencies": manifest.get("supported_currencies", []),
                "pricing": manifest.get("pricing", {}),
                "is_installed": is_installed,
                "current_version": current_version,
                "latest_version": latest_version,
                "has_update": has_update,
                "translations": manifest.get("translations", {}),
                "default_language": manifest.get("default_language", "en"),
            }

            all_providers.append(provider_data)

        # Count providers
        total_count = len(all_providers)
        live_count = sum(1 for p in all_providers if p["capabilities"].get("live_rates"))
        historical_count = sum(1 for p in all_providers if p["capabilities"].get("historical"))
        crypto_count = sum(1 for p in all_providers if p["capabilities"].get("crypto"))

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
                "regions": provider_data.get("regions", {}),
                "compliance": provider_data.get("compliance", {}),
                "pricing_info": provider_data.get("pricing_info", {}),
                "translations": dict(
                    provider_data.get("translations", {}),
                    default_language=provider_data.get("default_language", "en"),
                ),
                "is_installed": provider_data["is_installed"],
                "current_version": provider_data.get("current_version", ""),
                "latest_version": provider_data.get("latest_version", ""),
                "has_update": provider_data.get("has_update", False),
                "configure_url": "/admin/exchange_rates/provideraccount/",
            }
            providers_for_modal.append(modal_data)

        context = {
            "title": _("Browse Exchange Rate Providers"),
            "providers": all_providers,
            "providers_json": providers_for_modal,
            "total_count": total_count,
            "live_count": live_count,
            "historical_count": historical_count,
            "crypto_count": crypto_count,
            "has_live_rates": has_live_rates,
            "has_historical": has_historical,
            "has_crypto": has_crypto,
            "has_update_server": has_update_server,
        }

        return render(request, self.template_name, context)


@staff_member_required
@require_POST
def install_provider_ajax(request, provider_slug):
    """
    AJAX endpoint to install a provider from update server.

    POST to install provider from update server.
    Returns JSON with success status and redirect URL.
    """

    # Check if already installed
    try:
        component = ComponentRegistry.objects.get(
            slug=provider_slug, component_type="exchange_rate_provider"
        )

        # Provider is already installed, redirect to wizard to configure
        from django.urls import reverse

        return JsonResponse(
            {
                "success": True,
                "already_installed": True,
                "message": _("Provider is already installed. Configure it now."),
                "redirect_url": reverse("exchange_rates:wizard_step1"),
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
            component_type="exchange_rate_provider"
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
                component_type="exchange_rate_provider",
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
                from component_updates.integration_paths import INTEGRATIONS_DIR

                provider_base_dir = INTEGRATIONS_DIR / "exchange_rate_provider" / provider_slug
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
                from exchange_rates.providers.registry import ProviderRegistry

                ProviderRegistry.reload_providers()
            except Exception as e:
                # Don't fail the installation if symlink creation fails, just log it
                logger.warning("Could not create symlink for %s: %s", provider_slug, e)

        return JsonResponse(
            {
                "success": True,
                "message": _('Provider "%(name)s" installed successfully! Configure it now.')
                % {"name": provider_name},
                "redirect_url": reverse("exchange_rates:wizard_step1"),
            }
        )

    except Exception as e:
        logger.error("Error installing provider %s: %s", provider_slug, e, exc_info=True)
        return JsonResponse(
            {"success": False, "error": _("An unexpected error occurred during installation.")},
            status=500,
        )


@staff_member_required
@require_POST
def update_provider_ajax(request, provider_slug):
    """
    Update an existing provider to the latest version
    """
    from django.db import transaction
    from django.urls import reverse

    try:
        # Get the existing component
        try:
            component = ComponentRegistry.objects.get(
                slug=provider_slug, component_type="exchange_rate_provider"
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
                component_type="exchange_rate_provider"
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
                    "redirect_url": reverse("exchange_rates:provider_browse"),
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
                from component_updates.integration_paths import INTEGRATIONS_DIR

                provider_base_dir = INTEGRATIONS_DIR / "exchange_rate_provider" / provider_slug
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
                from exchange_rates.providers.registry import ProviderRegistry

                ProviderRegistry.reload_providers()
            except Exception as e:
                # Don't fail the update if symlink creation fails, just log it
                logger.warning("Could not update symlink for %s: %s", provider_slug, e)

            # Update component version
            component.current_version = latest_version
            component.save()

        return JsonResponse(
            {
                "success": True,
                "message": _('Provider "%(name)s" updated successfully to v%(version)s!')
                % {"name": provider_name, "version": latest_version},
                "redirect_url": reverse("exchange_rates:provider_browse"),
            }
        )

    except Exception as e:
        logger.error("Error updating provider %s: %s", provider_slug, e, exc_info=True)
        return JsonResponse(
            {"success": False, "error": _("An unexpected error occurred during the update.")},
            status=500,
        )
