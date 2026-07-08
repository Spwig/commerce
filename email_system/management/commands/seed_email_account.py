from core.management.commands._seed_base import SeedCommand


class Command(SeedCommand):
    seed_name = 'email_account'
    seed_version = 1
    help = 'Create default built-in SMTP email account'

    def seed(self) -> int:
        from django.contrib.sites.models import Site
        from email_system.models import EmailAccount
        from email_system.utils.encryption import encrypt_credentials

        # Skip if any account already exists
        if EmailAccount.objects.exists():
            return 0

        site = Site.objects.get(pk=1)
        domain = site.domain
        default_email = f'noreply@{domain}'

        credentials = {'enabled': True, 'dkim_selector': 'mail'}

        EmailAccount.objects.create(
            site=site,
            name='Built-in SMTP Server',
            provider_key='builtin_smtp',
            from_email=default_email,
            from_name=f'{site.name} Store',
            reply_to=default_email,
            credentials=encrypt_credentials(credentials),
            is_active=True,
            is_default=True,
            connection_status='unconfigured',
            dns_validated=False,
        )
        return 1
