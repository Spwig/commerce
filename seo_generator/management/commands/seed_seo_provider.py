from core.management.commands._seed_base import SeedCommand


class Command(SeedCommand):
    seed_name = "seo_provider"
    seed_version = 1
    help = "Create built-in deterministic SEO provider"

    def seed(self) -> int:
        from seo_generator.models import SEOProviderAccount

        _, created = SEOProviderAccount.objects.get_or_create(
            site_id=1,
            provider_key="deterministic",
            defaults={
                "name": "Built-in Generator",
                "is_active": True,
                "is_primary": True,
            },
        )
        return 1 if created else 0
