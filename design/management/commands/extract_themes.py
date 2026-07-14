"""
Management command to extract all theme packages to static directories
"""

from django.conf import settings
from django.core.management.base import BaseCommand

from design.theme_models import Theme


class Command(BaseCommand):
    help = "Extracts all theme packages to web-accessible static directories"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force re-extraction even if already extracted",
        )
        parser.add_argument(
            "--theme",
            type=str,
            help="Extract specific theme by slug",
        )

    def handle(self, *args, **options):
        force = options["force"]
        theme_slug = options.get("theme")

        # Get themes to extract
        if theme_slug:
            themes = Theme.objects.filter(slug=theme_slug, is_active=True)
            if not themes.exists():
                self.stdout.write(self.style.ERROR(f"Theme '{theme_slug}' not found"))
                return
        else:
            themes = Theme.objects.filter(is_active=True)

        if not themes.exists():
            self.stdout.write(self.style.WARNING("No active themes found"))
            return

        self.stdout.write(f"\nExtracting {themes.count()} theme(s)...\n")

        extracted_count = 0
        skipped_count = 0
        failed_count = 0

        for theme in themes:
            # Skip if already extracted (unless force flag is set)
            if theme.extracted_path and not force:
                self.stdout.write(
                    self.style.WARNING(f"⊘ Skipped: {theme.name} (already extracted)")
                )
                skipped_count += 1
                continue

            # Extract theme
            self.stdout.write(f"⏳ Extracting: {theme.name} ({theme.slug})...")

            success = theme.extract_theme()

            if success:
                extracted_count += 1
                css_url = theme.get_extracted_css_url()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Extracted: {theme.name}\n"
                        f"  Path: {theme.extracted_path}\n"
                        f"  CSS URL: {css_url}"
                    )
                )
            else:
                failed_count += 1
                self.stdout.write(self.style.ERROR(f"✗ Failed: {theme.name}"))

        # Summary
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS(f"✓ Extracted: {extracted_count}"))
        if skipped_count > 0:
            self.stdout.write(self.style.WARNING(f"⊘ Skipped: {skipped_count}"))
        if failed_count > 0:
            self.stdout.write(self.style.ERROR(f"✗ Failed: {failed_count}"))
        self.stdout.write("=" * 50 + "\n")

        # Show STATIC_ROOT info
        if settings.STATIC_ROOT:
            self.stdout.write(f"\nℹ️  Themes extracted to: {settings.STATIC_ROOT}/themes/")
        else:
            self.stdout.write(
                f"\nℹ️  Themes extracted to: {settings.MEDIA_ROOT}/static_themes/themes/\n"
                f"⚠️  STATIC_ROOT not configured - using media fallback"
            )
