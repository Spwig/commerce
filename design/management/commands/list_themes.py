"""
Management command to list installed themes
"""

from django.core.management.base import BaseCommand
from django.utils import timezone

from design.theme_models import Theme, ThemeBranding


class Command(BaseCommand):
    help = "List all installed themes"

    def add_arguments(self, parser):
        parser.add_argument("--active", action="store_true", help="Show only active themes")
        parser.add_argument("--verbose", action="store_true", help="Show detailed information")

    def handle(self, *args, **options):
        # Get themes
        themes = Theme.objects.all()

        if options["active"]:
            themes = themes.filter(is_active=True)

        if not themes.exists():
            self.stdout.write(self.style.WARNING("No themes installed"))
            return

        self.stdout.write(self.style.SUCCESS(f"\n{'=' * 60}"))
        self.stdout.write(self.style.SUCCESS("Installed Themes"))
        self.stdout.write(self.style.SUCCESS(f"{'=' * 60}\n"))

        for theme in themes:
            # Status indicators
            status = []
            if theme.is_active:
                status.append("✓ Active")
            if theme.is_default:
                status.append("★ Default")
            if theme.is_marketplace:
                status.append("◆ Marketplace")

            status_str = " | ".join(status) if status else "Inactive"

            # Basic info
            self.stdout.write(f"\n{theme.name} v{theme.version}")
            self.stdout.write(f"  Status: {status_str}")
            self.stdout.write(f"  Slug: {theme.slug}")

            if options["verbose"]:
                self.stdout.write(f"  Author: {theme.author}")
                if theme.author_email:
                    self.stdout.write(f"  Email: {theme.author_email}")
                self.stdout.write(f"  License: {theme.license}")
                self.stdout.write(
                    f"  Engine: {theme.engine_min_version} - {theme.engine_max_version or 'latest'}"
                )

                # Feature flags
                if theme.feature_flags:
                    self.stdout.write(f"  Features: {', '.join(theme.feature_flags)}")

                # Installation info
                if theme.installed_at:
                    days_ago = (timezone.now() - theme.installed_at).days
                    self.stdout.write(f"  Installed: {days_ago} days ago")

                # Assets count
                asset_count = theme.assets.count()
                if asset_count:
                    css_count = theme.assets.filter(asset_type="css").count()
                    js_count = theme.assets.filter(asset_type="js").count()
                    self.stdout.write(
                        f"  Assets: {asset_count} total ({css_count} CSS, {js_count} JS)"
                    )

                # Check if branding exists
                branding = ThemeBranding.objects.filter(theme=theme).first()
                if branding:
                    self.stdout.write(f"  Branding: Configured (hash: {branding.css_hash})")

        self.stdout.write(f"\n{'=' * 60}\n")
        self.stdout.write(f"Total: {themes.count()} theme(s)\n")
