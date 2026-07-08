"""
Management command to initialize OAuth provider settings
"""
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from accounts.models import OAuthProviderSettings


class Command(BaseCommand):
    help = 'Initialize OAuth provider settings with default values'

    def handle(self, *args, **options):
        """Create default OAuth provider settings"""

        providers = [
            {
                'provider': 'google',
                'display_name': 'Google',
                'button_order': 1,
                'enabled': False,
            },
            {
                'provider': 'apple',
                'display_name': 'Apple',
                'button_order': 2,
                'enabled': False,
            },
            {
                'provider': 'microsoft',
                'display_name': 'Microsoft',
                'button_order': 3,
                'enabled': False,
            },
        ]

        created_count = 0
        updated_count = 0

        for provider_data in providers:
            provider_obj, created = OAuthProviderSettings.objects.get_or_create(
                provider=provider_data['provider'],
                defaults=provider_data
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created OAuth provider: {provider_obj.get_provider_display()}'
                    )
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'○ Provider already exists: {provider_obj.get_provider_display()}'
                    )
                )

        # Ensure default site exists
        site, site_created = Site.objects.get_or_create(
            pk=1,
            defaults={
                'domain': 'example.com',
                'name': 'My Shop'
            }
        )

        if site_created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Created default site: {site.domain}'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    '⚠ Remember to update the site domain in Django admin (Sites section)'
                )
            )

        self.stdout.write('\n')
        self.stdout.write(
            self.style.SUCCESS(
                f'✓ OAuth provider initialization complete!'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'  - Created: {created_count} providers'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'  - Existing: {updated_count} providers'
            )
        )
        self.stdout.write('\n')
        self.stdout.write(
            self.style.WARNING(
                'Next steps:'
            )
        )
        self.stdout.write(
            '  1. Configure OAuth credentials in Django admin → Social Applications'
        )
        self.stdout.write(
            '  2. Enable providers in Django admin → OAuth Provider Settings'
        )
        self.stdout.write(
            '  3. Update site domain in Django admin → Sites'
        )
