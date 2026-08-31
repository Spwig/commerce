"""Seed Campaign Studio starter audiences from the store's own app data.

Creates ready-made dynamic segments (VIP, lapsing, loyalty, affiliate, ...) from
the customer, loyalty and affiliate intelligence the platform already computes.
Idempotent — re-running only adds missing starters, and never resurrects one the
merchant has removed. See ``email_marketing.services.starter_segments``.
"""

from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

from email_marketing.services.starter_segments import seed_starter_segments


class Command(BaseCommand):
    help = "Create ready-made starter audiences from the store's data (idempotent)."

    def handle(self, *args, **options):
        site = Site.objects.get(pk=1)
        result = seed_starter_segments(site)
        created, skipped = result["created"], result["skipped"]
        for name in created:
            self.stdout.write(self.style.SUCCESS(f"  + {name}"))
        for name in skipped:
            self.stdout.write(f"  = {name} (already exists)")
        self.stdout.write(
            self.style.SUCCESS(f"Done: {len(created)} created, {len(skipped)} skipped.")
        )
