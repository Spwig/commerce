"""
Provider Browse View
Displays available email providers for installation
"""

import json
from pathlib import Path

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.views import View

from component_updates.models import ComponentRegistry
from providers_common.utils import get_translated_provider_fields


@method_decorator(staff_member_required, name="dispatch")
class ProviderBrowseView(View):
    """
    Browse email providers.

    Displays:
    - Locally installed providers from components directory
    - Installation status for each provider
    """

    template_name = "email_system/providers/browse.html"

    def _get_local_manifest(self, slug):
        """
        Read the local manifest.json for an installed provider.

        Returns the parsed manifest dict, or {} if not found.
        """
        try:
            from component_updates.integration_paths import INTEGRATIONS_DIR

            manifest_path = INTEGRATIONS_DIR / "email_provider" / slug / "current" / "manifest.json"
            if manifest_path.exists():
                with open(manifest_path) as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def _get_builtin_provider_data(self):
        """
        Get provider data for the built-in SMTP provider.

        Returns:
            Dict with provider information
        """
        try:
            # Load manifest from builtin provider
            manifest_path = (
                Path(settings.BASE_DIR) / "email_system" / "providers" / "builtin" / "manifest.json"
            )
            with open(manifest_path) as f:
                manifest = json.load(f)

            # Build logo path for built-in provider
            from django.templatetags.static import static

            logo_path = "email_system/providers/builtin/logo.svg"

            # Built-in provider is always "installed" and always version 1.0.0
            return {
                "slug": "builtin_smtp",
                "name": manifest.get("name", "Built-in SMTP Server"),
                "description": manifest.get("description", ""),
                "version": manifest.get("version", "1.0.0"),
                "thumbnail_url": static(logo_path)
                if Path(settings.BASE_DIR / "email_system" / "static" / logo_path).exists()
                else "",
                "homepage_url": "",
                "documentation_url": "",
                "capabilities": manifest.get("capabilities", {}),
                "setup": manifest.get("setup_requirements", {}),
                "is_installed": True,  # Always installed
                "is_builtin": True,  # Flag to identify built-in provider
                "current_version": manifest.get("version", "1.0.0"),
                "latest_version": manifest.get("version", "1.0.0"),
                "has_update": False,  # Built-in providers update with platform
            }
        except Exception as e:
            print(f"Could not load built-in provider manifest: {e}")
            return None

    def get(self, request):
        """Display provider browse page"""
        # Get filter parameters
        has_transactional = request.GET.get("transactional")
        has_marketing = request.GET.get("marketing")
        has_webhooks = request.GET.get("webhooks")

        # Try to fetch available providers from update server
        available_from_server = []
        has_update_server = False

        try:
            from component_updates.services import UpdateManager

            update_manager = UpdateManager()
            available_from_server = update_manager.list_available_components(
                component_type="email_provider"
            )
            has_update_server = True
        except Exception as e:
            # If update server fails, we'll fall back to locally installed providers
            print(f"Could not fetch from update server: {e}")

        # Get installed providers for version comparison
        installed_db = {
            p.slug: p.current_version
            for p in ComponentRegistry.objects.filter(component_type="email_provider")
        }

        # Get current admin language for manifest-based i18n
        lang = get_language() or "en"

        # Process providers from update server
        all_providers = []

        # Add built-in SMTP provider first (always available, always installed)
        builtin_provider = self._get_builtin_provider_data()
        if builtin_provider:
            # Apply capability filters
            capabilities = builtin_provider.get("capabilities", {})
            include_builtin = True

            if has_transactional and not capabilities.get("transactional"):
                include_builtin = False
            if has_marketing and not capabilities.get("marketing"):
                include_builtin = False
            if has_webhooks and not capabilities.get("webhooks"):
                include_builtin = False

            if include_builtin:
                all_providers.append(builtin_provider)

        # Add external providers from update server
        for provider in available_from_server:
            slug = provider.get("slug")
            latest_version = provider.get("current_version") or provider.get("version")
            manifest = provider.get("manifest", {})

            # Check if installed and compare versions
            is_installed = slug in installed_db
            current_version = installed_db.get(slug, "")
            has_update = False

            # For installed providers, supplement with local manifest data
            # (update server API doesn't include manifest/capabilities/setup)
            if is_installed:
                local_manifest = self._get_local_manifest(slug)
                if local_manifest:
                    # Local manifest fills in fields the server API omits
                    if not manifest:
                        manifest = local_manifest
                    else:
                        # Merge: local fills gaps in server data
                        for key in (
                            "capabilities",
                            "setup_wizard",
                            "description",
                            "name",
                            "translations",
                            "default_language",
                            "homepage_url",
                            "documentation_url",
                            "api_docs_url",
                        ):
                            if key not in manifest or not manifest[key]:
                                if key in local_manifest and local_manifest[key]:
                                    manifest[key] = local_manifest[key]

            # Get capabilities
            capabilities = provider.get("capabilities") or manifest.get("capabilities", {})

            # Apply capability filters
            if has_transactional and not capabilities.get("transactional"):
                continue
            if has_marketing and not capabilities.get("marketing"):
                continue
            if has_webhooks and not capabilities.get("webhooks"):
                continue

            if is_installed and current_version and latest_version:
                try:
                    from packaging import version

                    has_update = version.parse(latest_version) > version.parse(current_version)
                except Exception:
                    has_update = False

            # Get setup info from manifest
            setup_info = manifest.get("setup_wizard", manifest.get("setup", {}))

            # Translate name/description from manifest translations
            translated = get_translated_provider_fields(manifest, lang)

            # Build logo URL for installed providers from local files
            thumbnail_url = provider.get("thumbnail_url", "")
            if not thumbnail_url and is_installed and manifest.get("logo"):
                try:
                    from django.templatetags.static import static

                    from component_updates.integration_paths import INTEGRATIONS_DIR

                    logo_file = manifest["logo"]
                    logo_path = INTEGRATIONS_DIR / "email_provider" / slug / "current" / logo_file
                    if logo_path.exists():
                        thumbnail_url = static(f"email_provider/{slug}/current/{logo_file}")
                except Exception:
                    pass

            provider_data = {
                "slug": slug,
                "name": translated["name"] or provider.get("name", ""),
                "description": translated["description"] or provider.get("description", ""),
                "version": latest_version,
                "thumbnail_url": thumbnail_url,
                "homepage_url": provider.get("homepage_url", "")
                or manifest.get("homepage_url", ""),
                "documentation_url": provider.get("documentation_url")
                or manifest.get("documentation_url", "")
                or manifest.get("api_docs_url", ""),
                "capabilities": capabilities,
                "setup": setup_info,
                "is_installed": is_installed,
                "current_version": current_version,
                "latest_version": latest_version,
                "has_update": has_update,
                "translations": manifest.get("translations", {}),
                "default_language": manifest.get("default_language", "en"),
            }

            all_providers.append(provider_data)

        # Add installed providers not returned by update server (offline fallback)
        server_slugs = {p.get("slug") for p in available_from_server}
        for slug, current_version in installed_db.items():
            if slug in server_slugs:
                continue  # Already processed above

            manifest = self._get_local_manifest(slug)
            if not manifest:
                continue

            capabilities = manifest.get("capabilities", {})

            # Apply capability filters
            if has_transactional and not capabilities.get("transactional"):
                continue
            if has_marketing and not capabilities.get("marketing"):
                continue
            if has_webhooks and not capabilities.get("webhooks"):
                continue

            setup_info = manifest.get("setup_wizard", manifest.get("setup", {}))
            translated = get_translated_provider_fields(manifest, lang)

            # Build logo URL
            thumbnail_url = ""
            if manifest.get("logo"):
                try:
                    from django.templatetags.static import static

                    from component_updates.integration_paths import INTEGRATIONS_DIR

                    logo_file = manifest["logo"]
                    logo_path = INTEGRATIONS_DIR / "email_provider" / slug / "current" / logo_file
                    if logo_path.exists():
                        thumbnail_url = static(f"email_provider/{slug}/current/{logo_file}")
                except Exception:
                    pass

            provider_data = {
                "slug": slug,
                "name": translated["name"] or manifest.get("name", slug),
                "description": translated["description"] or manifest.get("description", ""),
                "version": current_version,
                "thumbnail_url": thumbnail_url,
                "homepage_url": manifest.get("homepage_url", ""),
                "documentation_url": manifest.get("documentation_url", "")
                or manifest.get("api_docs_url", ""),
                "capabilities": capabilities,
                "setup": setup_info,
                "is_installed": True,
                "current_version": current_version,
                "latest_version": current_version,
                "has_update": False,
                "translations": manifest.get("translations", {}),
                "default_language": manifest.get("default_language", "en"),
            }
            all_providers.append(provider_data)

        # Count providers
        total_count = len(all_providers)
        transactional_count = sum(
            1 for p in all_providers if p["capabilities"].get("transactional")
        )
        marketing_count = sum(1 for p in all_providers if p["capabilities"].get("marketing"))
        webhooks_count = sum(1 for p in all_providers if p["capabilities"].get("webhooks"))

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
                "configure_url": "/admin/email_system/emailaccount/",
            }
            providers_for_modal.append(modal_data)

        context = {
            "title": _("Browse Email Providers"),
            "providers": all_providers,
            "providers_json": providers_for_modal,
            "total_count": total_count,
            "transactional_count": transactional_count,
            "marketing_count": marketing_count,
            "webhooks_count": webhooks_count,
            "has_transactional": has_transactional,
            "has_marketing": has_marketing,
            "has_webhooks": has_webhooks,
            "has_update_server": has_update_server,
        }

        return render(request, self.template_name, context)


@staff_member_required
def install_provider_ajax(request, provider_slug):
    """
    AJAX endpoint to install a provider from update server.

    POST to install provider from update server.
    Returns JSON with success status and redirect URL.
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)

    # Check if already installed
    try:
        component = ComponentRegistry.objects.get(
            slug=provider_slug, component_type="email_provider"
        )

        # Provider is already installed, redirect to wizard
        from django.urls import reverse

        return JsonResponse(
            {
                "success": True,
                "already_installed": True,
                "message": _("Provider is already installed. Configure it now."),
                "redirect_url": reverse("email_system:wizard_step1"),
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
            component_type="email_provider"
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
                component_type="email_provider",
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

                provider_base_dir = INTEGRATIONS_DIR / "email_provider" / provider_slug
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
                from email_system.providers.registry import ProviderRegistry

                ProviderRegistry.reload_providers()
            except Exception as e:
                # Don't fail the installation if symlink creation fails, just log it
                print(f"Warning: Could not create symlink for {provider_slug}: {e}")

        return JsonResponse(
            {
                "success": True,
                "message": _('Provider "%(name)s" installed successfully! Configure it now.')
                % {"name": provider_name},
                "redirect_url": reverse("email_system:wizard_step1"),
            }
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
def update_provider_ajax(request, provider_slug):
    """
    Update an existing provider to the latest version
    """
    from django.db import transaction
    from django.urls import reverse

    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)

    try:
        # Get the existing component
        try:
            component = ComponentRegistry.objects.get(
                slug=provider_slug, component_type="email_provider"
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
                component_type="email_provider"
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
                    "redirect_url": reverse("email_system:provider_browse"),
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

                provider_base_dir = INTEGRATIONS_DIR / "email_provider" / provider_slug
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
                from email_system.providers.registry import ProviderRegistry

                ProviderRegistry.reload_providers()
            except Exception as e:
                # Don't fail the update if symlink creation fails, just log it
                print(f"Warning: Could not update symlink for {provider_slug}: {e}")

            # Update component version
            component.current_version = latest_version
            component.save()

        return JsonResponse(
            {
                "success": True,
                "message": _('Provider "%(name)s" updated successfully to v%(version)s!')
                % {"name": provider_name, "version": latest_version},
                "redirect_url": reverse("email_system:provider_browse"),
            }
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
