"""
Management command to regenerate theme CSS
"""

from django.core.cache import cache
from django.core.management.base import BaseCommand

from design.theme_models import ThemeBranding


class Command(BaseCommand):
    help = "Regenerate CSS for theme branding"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear-cache", action="store_true", help="Clear theme cache after regeneration"
        )

    def handle(self, *args, **options):
        self.stdout.write("Regenerating theme CSS...")

        try:
            # Get or create branding
            branding = ThemeBranding.objects.first()

            if not branding:
                self.stdout.write(
                    self.style.WARNING("No branding configuration found. Creating default...")
                )
                branding = ThemeBranding.objects.create()

            # Regenerate CSS
            old_hash = branding.css_hash
            css_content = branding.generate_css()
            new_hash = branding.css_hash

            self.stdout.write(self.style.SUCCESS("✓ CSS regenerated successfully"))

            # Display info
            self.stdout.write("\nCSS Information:")
            self.stdout.write(f"  Size: {len(css_content)} bytes")
            self.stdout.write(f"  Old hash: {old_hash or 'None'}")
            self.stdout.write(f"  New hash: {new_hash}")
            self.stdout.write(f"  URL: {branding.get_css_url()}")

            # Token counts
            token_counts = {
                "Colors": len(branding.color_tokens),
                "Typography": len(branding.typography_tokens),
                "Spacing": len(branding.spacing_tokens),
                "Borders": len(branding.border_tokens),
                "Shadows": len(branding.shadow_tokens),
                "Animations": len(branding.animation_tokens),
            }

            self.stdout.write("\nToken counts:")
            for token_type, count in token_counts.items():
                if count > 0:
                    self.stdout.write(f"  {token_type}: {count}")

            # Clear cache if requested
            if options["clear_cache"]:
                self.stdout.write("\nClearing theme cache...")
                cache.delete("active_theme")
                cache.delete("active_theme_context")
                cache.delete_pattern("theme_*")
                self.stdout.write(self.style.SUCCESS("✓ Cache cleared"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ Failed to regenerate CSS: {str(e)}"))
