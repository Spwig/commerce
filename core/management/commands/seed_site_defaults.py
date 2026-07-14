from core.management.commands._seed_base import SeedCommand


class Command(SeedCommand):
    seed_name = "site_defaults"
    seed_version = 1
    help = "Ensure Django Site ID=1 exists (required for single-tenant architecture)"

    def seed(self) -> int:
        from django.contrib.sites.models import Site

        _, created = Site.objects.get_or_create(
            pk=1,
            defaults={
                "domain": "example.com",
                "name": "My E-commerce Store",
            },
        )
        return 1 if created else 0
