"""
Unified Theme Management Views
Elegant Themes-style interface for managing theme packages
"""

import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from component_updates.models import ComponentRegistry

from .theme_update_service import ThemeUpdateService
from .theme_version_manager import ThemeVersionManager

logger = logging.getLogger(__name__)


@staff_member_required
def unified_theme_management_view(request):
    """
    Unified view showing all theme information:
    - Installed theme packages (from ComponentRegistry) - always shown, not paginated
    - Available themes (from update server) - paginated
    - Active theme indicator
    - Elegant Themes-style layout with tall thumbnails
    - Automatically checks for updates on page load
    """
    filter_type = request.GET.get("filter", "all")  # all, installed, available
    search_query = request.GET.get("q", "")
    try:
        page = max(1, int(request.GET.get("page", 1)))
    except (ValueError, TypeError):
        page = 1
    page_size = 24

    context = {
        "title": _("Theme Management"),
        "filter_type": filter_type,
        "search_query": search_query,
        "themes": [],
    }

    # Get active theme info
    active_theme = ThemeVersionManager.get_active_theme()
    active_slug = active_theme["slug"] if active_theme else None

    # Note: We no longer sync on every page load. With 2000+ themes on the
    # update server, fetching the full list takes several seconds.
    # Merchants can use the "Check for Updates" button to sync manually.

    # Get installed theme packages from ComponentRegistry
    installed_themes = ComponentRegistry.objects.filter(component_type="theme").order_by("name")

    if search_query:
        installed_themes = installed_themes.filter(
            Q(name__icontains=search_query) | Q(slug__icontains=search_query)
        )

    # Build installed theme data
    themes_data = []
    installed_slugs = set()

    # Bulk-prefetch Theme instances and bundled component counts to avoid N+1 queries
    from django.db.models import Count

    from .theme_models import Theme

    theme_slug_list = list(installed_themes.values_list("slug", flat=True))
    installed_slugs = set(theme_slug_list)

    # Single query: get all Theme instances with bundled component counts
    theme_instances = {
        t.slug: t
        for t in Theme.objects.filter(slug__in=theme_slug_list).annotate(
            bundled_count=Count("bundled_components")
        )
    }

    for theme_pkg in installed_themes:
        # Only include installed themes in the list on page 1
        # to avoid repeating them on every paginated page
        if page > 1 and filter_type != "installed":
            continue

        # Get version info from ThemeVersionManager
        current_version = ThemeVersionManager.get_current_version(theme_pkg.slug)
        available_versions = ThemeVersionManager.get_theme_versions(theme_pkg.slug)

        # Get bundled component count from prefetched data
        theme_instance = theme_instances.get(theme_pkg.slug)
        bundled_component_count = (
            getattr(theme_instance, "bundled_count", 0) if theme_instance else 0
        )

        theme_data = {
            "id": theme_pkg.id,
            "slug": theme_pkg.slug,
            "name": theme_pkg.name,
            "description": theme_pkg.description or "",
            "current_version": current_version or theme_pkg.current_version,
            "latest_version": theme_pkg.latest_version,
            "has_update": theme_pkg.latest_version
            and theme_pkg.current_version != theme_pkg.latest_version,
            "is_installed": True,
            "is_active": theme_pkg.slug == active_slug,
            "last_checked": theme_pkg.last_checked,
            "locked": theme_pkg.locked,
            "available_versions": available_versions,
            # Author and visual assets
            "author_name": theme_pkg.author or theme_pkg.author_details.get("name", "Unknown"),
            "author_details": theme_pkg.author_details,
            "thumbnail_url": theme_pkg.thumbnail_url,
            "preview_images": theme_pkg.preview_images,
            "preview_videos": theme_pkg.preview_videos,
            # Bundled components (full info loaded on demand via detail modal)
            "bundled_components": [],
            "bundled_component_count": bundled_component_count,
            # Pricing (installed themes are already purchased/free)
            "pricing_model": "free",
            "price_eur": "0.00",
        }
        themes_data.append(theme_data)

    installed_count = len(installed_slugs)

    # Get available themes from update server (paginated)
    available_count = 0
    total_pages = 1
    server_page_data = None

    if filter_type != "installed":
        try:
            server_page_data = ThemeUpdateService.get_available_themes_paginated(
                page=page, page_size=page_size, search=search_query
            )
            available_themes_list = server_page_data.get("results", [])
            available_count = server_page_data.get("count", 0)
            total_pages = server_page_data.get("total_pages", 1)

            # Process available (not installed) themes from this page
            for theme in available_themes_list:
                slug = theme.get("slug")
                if slug not in installed_slugs:
                    author_details = theme.get("author_details", {})
                    author_name = theme.get("author_name", author_details.get("name", "Unknown"))

                    theme_data = {
                        "slug": slug,
                        "name": theme.get("name", slug),
                        "description": theme.get("description", ""),
                        "current_version": None,
                        "latest_version": theme.get("current_version", "1.0.0"),
                        "has_update": False,
                        "is_installed": False,
                        "is_active": False,
                        "last_checked": None,
                        "locked": False,
                        "available_versions": [],
                        # Author and visual assets
                        "author_name": author_name,
                        "author_details": author_details,
                        "thumbnail_url": theme.get("thumbnail_url", ""),
                        "preview_images": theme.get("preview_images", []),
                        "preview_videos": theme.get("preview_videos", []),
                        # Pricing
                        "pricing_model": theme.get("pricing_model", "free"),
                        "price_eur": theme.get("price_eur", "0.00"),
                    }
                    themes_data.append(theme_data)

        except Exception as e:
            messages.error(
                request, _("Failed to fetch available themes: %(error)s") % {"error": str(e)}
            )

    # Apply filtering (installed themes only - available already filtered by server)
    if filter_type == "installed":
        themes_data = [t for t in themes_data if t["is_installed"]]
    elif filter_type == "available":
        themes_data = [t for t in themes_data if not t["is_installed"]]

    all_count = installed_count + available_count

    context["themes"] = themes_data
    context["active_theme"] = active_theme
    context["all_count"] = all_count
    context["installed_count"] = installed_count
    context["available_count"] = available_count

    # Pagination context
    context["page"] = page
    context["total_pages"] = total_pages
    context["has_next"] = page < total_pages
    context["has_previous"] = page > 1

    return render(request, "admin/design/theme/unified_management.html", context)


@staff_member_required
@require_POST
def activate_theme_ajax(request, slug):
    """
    AJAX endpoint to activate a specific theme version.
    Deactivates all other themes automatically.
    """
    version = request.POST.get("version")

    if not version:
        return JsonResponse(
            {"success": False, "error": "Version parameter is required"}, status=400
        )

    result = ThemeVersionManager.activate_theme_version(slug, version)

    if result["success"]:
        messages.success(request, result["message"])

    return JsonResponse(result)


@staff_member_required
@require_POST
def rollback_theme_ajax(request, slug):
    """
    AJAX endpoint to rollback a theme to previous version.
    """
    to_version = request.POST.get("to_version")

    result = ThemeVersionManager.rollback_theme(slug, to_version)

    if result["success"]:
        messages.success(request, result["message"])
    else:
        messages.error(request, result.get("error", "Rollback failed"))

    return JsonResponse(result)


@staff_member_required
@require_POST
def install_theme_ajax(request, slug):
    """
    AJAX endpoint to trigger theme installation from update server.
    This integrates with UpdateManager for both fresh installs and updates.
    """
    from component_updates.services import UpdateManager

    try:
        manager = UpdateManager()

        # Get theme registry entry
        theme_pkg = ComponentRegistry.objects.filter(component_type="theme", slug=slug).first()

        if not theme_pkg:
            # Theme not in registry yet - fetch from update server and create registry entry
            logger.info(f"Theme {slug} not in registry, fetching from update server...")

            # Get theme info from update server
            theme_info = ThemeUpdateService.get_theme_info(slug)

            if not theme_info:
                return JsonResponse(
                    {"success": False, "error": f"Theme {slug} not found on update server"},
                    status=404,
                )

            # Create registry entry for the new theme
            theme_pkg = ComponentRegistry.objects.create(
                component_type="theme",
                slug=slug,
                name=theme_info.get("name", slug),
                description=theme_info.get("description", ""),
                current_version="0.0.0",  # Not installed yet
                latest_version=theme_info.get("current_version", "1.0.0"),
                update_available=True,
                author=theme_info.get("author_name", "Unknown"),
                author_details=theme_info.get("author_details", {}),
                thumbnail_url=theme_info.get("thumbnail_url", ""),
                preview_images=theme_info.get("preview_images", []),
                locked=False,
            )
            logger.info(f"Created registry entry for {slug}")

        # Install/update the theme
        logger.info(
            f"Installing theme {slug} v{theme_pkg.latest_version or theme_pkg.current_version}"
        )
        success = manager.install_update(theme_pkg)

        if success:
            messages.success(request, f"Theme {slug} installed successfully")
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "Installation failed"})

    except Exception as e:
        logger.error(f"Failed to install theme {slug}: {e}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
@require_POST
def uninstall_theme_ajax(request, slug):
    """
    AJAX endpoint to uninstall a theme.
    Cannot uninstall active theme.
    """
    # Defense-in-depth guard (also checked in ThemeVersionManager)
    active_theme = ThemeVersionManager.get_active_theme()
    if active_theme and active_theme["slug"] == slug:
        return JsonResponse(
            {
                "success": False,
                "error": _("Cannot uninstall the active theme. Switch to a different theme first."),
            },
            status=400,
        )

    version = request.POST.get("version")  # Optional - if None, removes entire theme

    result = ThemeVersionManager.uninstall_theme(slug, version)

    if result["success"]:
        messages.success(request, result["message"])
    else:
        messages.error(request, result.get("error", "Uninstall failed"))

    return JsonResponse(result)


@staff_member_required
@require_POST
def check_theme_updates_ajax(request):
    """
    AJAX endpoint to check for theme updates from update server.
    Forces a fresh fetch by clearing the cache first.
    """
    try:
        ThemeUpdateService.clear_cache()
        updated_count = ThemeUpdateService.sync_installed_theme_metadata()

        messages.success(request, f"Checked {updated_count} themes for updates")

        return JsonResponse({"success": True, "updated_count": updated_count})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
def get_theme_detail_ajax(request, slug):
    """
    AJAX endpoint to get full details for a theme (for the details modal).
    Combines data from ComponentRegistry (installed) and update server (available).
    """
    try:
        active_theme = ThemeVersionManager.get_active_theme()
        active_slug = active_theme["slug"] if active_theme else None

        # Try installed theme first (richer data)
        theme_pkg = ComponentRegistry.objects.filter(component_type="theme", slug=slug).first()

        # Get bundled components if theme is installed locally
        bundled_components = []
        if theme_pkg:
            from .theme_models import Theme

            theme_instance = Theme.objects.filter(slug=slug).first()
            if theme_instance:
                bundled_components = theme_instance.get_bundled_component_info()

        # Also fetch from update server for latest info
        server_info = ThemeUpdateService.get_theme_info(slug)

        if not theme_pkg and not server_info:
            return JsonResponse({"success": False, "error": f"Theme {slug} not found"}, status=404)

        # Build response, preferring installed data but enriching with server data
        data = {
            "success": True,
            "slug": slug,
            "name": (theme_pkg.name if theme_pkg else None)
            or (server_info or {}).get("name", slug),
            "description": (theme_pkg.description if theme_pkg else None)
            or (server_info or {}).get("description", ""),
            "is_installed": theme_pkg is not None,
            "is_active": slug == active_slug,
            "current_version": theme_pkg.current_version if theme_pkg else None,
            "latest_version": (
                (theme_pkg.latest_version if theme_pkg else None)
                or (server_info or {}).get("current_version")
            ),
            "has_update": (
                theme_pkg.latest_version and theme_pkg.current_version != theme_pkg.latest_version
            )
            if theme_pkg
            else False,
            # Author
            "author_name": (
                (theme_pkg.author if theme_pkg else None)
                or (server_info or {}).get("author_name", "Unknown")
            ),
            "author_details": (
                (theme_pkg.author_details if theme_pkg else None)
                or (server_info or {}).get("author_details", {})
            ),
            # Visual assets
            "thumbnail_url": (
                (theme_pkg.thumbnail_url if theme_pkg else None)
                or (server_info or {}).get("thumbnail_url", "")
            ),
            "preview_images": (
                (theme_pkg.preview_images if theme_pkg else None)
                or (server_info or {}).get("preview_images", [])
            ),
            "preview_videos": (
                (theme_pkg.preview_videos if theme_pkg else None)
                or (server_info or {}).get("preview_videos", [])
            ),
            # Components
            "bundled_components": bundled_components,
            "bundled_component_count": len(bundled_components),
            # Pricing
            "pricing_model": (server_info or {}).get("pricing_model", "free"),
            "price_eur": (server_info or {}).get("price_eur", "0.00"),
            # Manifest extras (from server)
            "manifest": (server_info or {}).get("manifest", {}),
        }

        return JsonResponse(data)

    except Exception as e:
        logger.error(f"Failed to get theme detail for {slug}: {e}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)
