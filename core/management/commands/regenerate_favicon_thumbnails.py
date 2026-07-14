from django.core.management.base import BaseCommand

from core.models import SiteSettings
from media_library.management.commands.regenerate_media import Command as RegenerateCommand


class Command(BaseCommand):
    help = "Regenerate thumbnails specifically for SiteSettings favicon images"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force regeneration even if thumbnails exist",
        )

    def handle(self, *args, **options):
        # Get all SiteSettings instances with favicon
        settings_list = SiteSettings.objects.exclude(favicon__isnull=True)

        if not settings_list.exists():
            self.stdout.write(self.style.WARNING("No favicon configured in SiteSettings"))
            return

        # Get all unique favicon MediaAsset IDs
        favicon_ids = [str(s.favicon.id) for s in settings_list if s.favicon]

        if not favicon_ids:
            self.stdout.write(self.style.WARNING("No favicon assets found"))
            return

        self.stdout.write(f"Found {len(favicon_ids)} favicon(s) to process")

        # Use existing regenerate_media command with specific asset IDs
        regenerate_cmd = RegenerateCommand()
        regenerate_cmd.stdout = self.stdout
        regenerate_cmd.style = self.style

        regenerate_cmd.handle(
            thumbnails_only=True,
            asset_ids=favicon_ids,
            batch_size=10,
            force=options["force"],
            webp_only=False,
        )

        self.stdout.write(self.style.SUCCESS("✅ Favicon thumbnail regeneration complete!"))
