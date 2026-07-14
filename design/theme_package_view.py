"""
Theme Packaging View
Allows theme developers to package themes directly from the admin interface.
"""

import logging
from pathlib import Path

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .theme_packager import ThemePackager

logger = logging.getLogger(__name__)


@staff_member_required
def theme_package_view(request):
    """
    Main view for theme packaging interface.
    Displays form to select theme and validate/package it.
    """
    context = {
        "title": "Theme Packager",
        "available_themes": get_available_themes(),
    }
    return render(request, "admin/design/theme/theme_package.html", context)


@staff_member_required
@require_POST
def validate_theme_ajax(request):
    """
    AJAX endpoint to validate a theme before packaging.
    Returns validation results with errors and warnings.
    """
    theme_path = request.POST.get("theme_path")

    if not theme_path:
        return JsonResponse({"success": False, "error": "Theme path is required"}, status=400)

    try:
        # Resolve path
        theme_path = Path(theme_path)

        if not theme_path.is_absolute():
            # Try to resolve relative to themes directory
            themes_base = Path(settings.BASE_DIR) / "themes"
            theme_path = themes_base / theme_path

        if not theme_path.exists():
            return JsonResponse(
                {"success": False, "error": f"Theme directory not found: {theme_path}"}, status=404
            )

        # Initialize packager and validate
        packager = ThemePackager(theme_path)
        is_valid, errors, warnings = packager.validate()

        # Get validation report
        report = packager.get_validation_report()

        return JsonResponse(
            {
                "success": True,
                "is_valid": is_valid,
                "errors": errors,
                "warnings": warnings,
                "report": report,
                "theme_info": {
                    "name": packager.manifest.get("name", "Unknown"),
                    "display_name": packager.manifest.get("display_name", "Unknown"),
                    "version": packager.manifest.get("version", "0.0.0"),
                    "author": packager.manifest.get("author", "Unknown"),
                    "description": packager.manifest.get("description", ""),
                }
                if packager.manifest
                else None,
            }
        )

    except Exception as e:
        logger.error(f"Failed to validate theme at {theme_path}: {e}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
@require_POST
def package_theme_ajax(request):
    """
    AJAX endpoint to create a theme package.
    Returns download information for the created package.
    """
    theme_path = request.POST.get("theme_path")

    if not theme_path:
        return JsonResponse({"success": False, "error": "Theme path is required"}, status=400)

    try:
        # Resolve path
        theme_path = Path(theme_path)

        if not theme_path.is_absolute():
            # Try to resolve relative to themes directory
            themes_base = Path(settings.BASE_DIR) / "themes"
            theme_path = themes_base / theme_path

        if not theme_path.exists():
            return JsonResponse(
                {"success": False, "error": f"Theme directory not found: {theme_path}"}, status=404
            )

        # Initialize packager
        packager = ThemePackager(theme_path)

        # Validate first
        is_valid, errors, warnings = packager.validate()

        if not is_valid:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Theme validation failed",
                    "errors": errors,
                    "warnings": warnings,
                },
                status=400,
            )

        # Create package directory
        package_dir = Path(settings.MEDIA_ROOT) / "theme_packages"
        package_dir.mkdir(parents=True, exist_ok=True)

        # Generate package filename
        theme_name = packager.manifest.get("name", "theme")
        theme_version = packager.manifest.get("version", "1.0.0")
        package_filename = f"{theme_name}-{theme_version}.zip"
        output_path = package_dir / package_filename

        # Create package
        package_info = packager.package(output_path)

        # Get download URL
        download_url = f"{settings.MEDIA_URL}theme_packages/{package_filename}"

        return JsonResponse(
            {
                "success": True,
                "package_info": package_info,
                "download_url": download_url,
                "package_filename": package_filename,
            }
        )

    except Exception as e:
        logger.error(f"Failed to package theme at {theme_path}: {e}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


def get_available_themes():
    """
    Get list of available theme directories from the themes folder.
    Returns list of theme info dictionaries.
    """
    themes = []
    themes_base = Path(settings.BASE_DIR) / "themes"

    if not themes_base.exists():
        return themes

    # Scan themes directory
    for theme_dir in themes_base.iterdir():
        if not theme_dir.is_dir() or theme_dir.name.startswith("."):
            continue

        # Look for versioned directories (e.g., themes/modern-shop/v1.0.0/)
        for version_dir in theme_dir.iterdir():
            if not version_dir.is_dir() or not version_dir.name.startswith("v"):
                continue

            manifest_path = version_dir / "manifest.json"
            if manifest_path.exists():
                try:
                    import json

                    with open(manifest_path) as f:
                        manifest = json.load(f)

                    themes.append(
                        {
                            "path": str(version_dir.relative_to(settings.BASE_DIR)),
                            "absolute_path": str(version_dir),
                            "name": manifest.get("name", theme_dir.name),
                            "display_name": manifest.get("display_name", theme_dir.name),
                            "version": manifest.get("version", version_dir.name[1:]),
                            "author": manifest.get("author", "Unknown"),
                            "description": manifest.get("description", ""),
                        }
                    )
                except Exception as e:
                    logger.debug(f"Failed to read manifest for {version_dir}: {e}")
                    continue

    return sorted(themes, key=lambda t: t["display_name"])
