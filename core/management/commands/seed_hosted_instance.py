"""
Management command to seed initial configuration for a hosted Spwig instance.

Called during automated provisioning to configure a freshly deployed
hosted instance with the merchant's store name, domain, and defaults.

Usage:
    python manage.py seed_hosted_instance \
        --store-name "My Shop" \
        --domain shop.myspwig.com \
        --license-key ABC123

    # With provision data (from fleet script or cloud-init)
    python manage.py seed_hosted_instance \
        --store-name "Fashion Store" \
        --domain fashion.myspwig.com \
        --provision-data '{"email": {"gateway_host": "mail.myspwig.com", ...}}'

    # With individual email flags (manual provisioning)
    python manage.py seed_hosted_instance \
        --store-name "Fashion Store" \
        --domain fashion.myspwig.com \
        --email-auth-user fashion-store \
        --email-auth-token <token>
"""

import json

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Seed initial configuration for a hosted Spwig instance'

    def add_arguments(self, parser):
        parser.add_argument(
            '--store-name',
            required=True,
            help='Display name for the store',
        )
        parser.add_argument(
            '--domain',
            required=True,
            help='Primary domain for the store (e.g., shop.myspwig.com)',
        )
        parser.add_argument(
            '--license-key',
            default='',
            help='License key to pre-configure',
        )
        parser.add_argument(
            '--admin-email',
            default='',
            help='Admin contact email address',
        )
        parser.add_argument(
            '--default-language',
            default='en',
            help='Default language code (default: en)',
        )
        parser.add_argument(
            '--skip-wizard',
            action='store_true',
            help='Mark setup wizard as complete',
        )
        # Provision data (JSON blob from fleet script or cloud-init)
        parser.add_argument(
            '--provision-data',
            default='',
            help='JSON provisioning data (includes email section)',
        )
        # Individual email flags (fallback for manual provisioning)
        parser.add_argument(
            '--email-gateway-host',
            default='mail.myspwig.com',
            help='Mail gateway SMTP host (default: mail.myspwig.com)',
        )
        parser.add_argument(
            '--email-gateway-port',
            type=int,
            default=587,
            help='Mail gateway SMTP port (default: 587)',
        )
        parser.add_argument(
            '--email-auth-user',
            default='',
            help='SMTP auth username (merchant slug)',
        )
        parser.add_argument(
            '--email-auth-token',
            default='',
            help='SMTP auth token (from gateway API)',
        )
        parser.add_argument(
            '--email-from-address',
            default='',
            help='Default from email (default: noreply@myspwig.com)',
        )
        parser.add_argument(
            '--email-from-name',
            default='',
            help='Default from name (default: store name)',
        )

    def handle(self, *args, **options):
        store_name = options['store_name']
        domain = options['domain']
        license_key = options['license_key']
        admin_email = options['admin_email']
        default_language = options['default_language']
        skip_wizard = options['skip_wizard']

        site_url = f'https://{domain}'

        # 1. Update SiteSettings
        self._configure_site(store_name, site_url, admin_email)

        # 2. Create default staff roles
        self._create_default_roles()

        # 3. Mark setup wizard complete (if requested)
        if skip_wizard:
            self._complete_setup_wizard()

        # 4. Auto-accept license agreement
        self._accept_license()

        # 5. Enable default languages
        self._enable_languages(default_language)

        # 6. Set hosting-specific defaults
        self._set_hosted_defaults()

        # 7. Configure email account (Spwig hosted mail)
        self._configure_email(options, store_name, admin_email)

        self.stdout.write(self.style.SUCCESS(
            f'Hosted instance seeded: {store_name} ({domain})'
        ))

    def _configure_site(self, store_name, site_url, admin_email):
        """Configure SiteSettings with store details."""
        from core.models import SiteSettings

        settings, created = SiteSettings.objects.get_or_create(pk=1)
        # Use queryset update to bypass model validation
        update_fields = {
            'site_name': store_name,
            'site_url': site_url,
            'maintenance_mode': False,
        }
        if admin_email:
            update_fields['admin_email'] = admin_email

        SiteSettings.objects.filter(pk=1).update(**update_fields)
        action = 'Created' if created else 'Updated'
        self.stdout.write(f'  {action} SiteSettings: {store_name}')

    def _create_default_roles(self):
        """Create default staff roles if they don't exist."""
        from django.core.management import call_command
        try:
            call_command('create_default_roles', verbosity=0)
            self.stdout.write('  Created default staff roles')
        except Exception as e:
            self.stderr.write(self.style.WARNING(f'  Could not create roles: {e}'))

    def _complete_setup_wizard(self):
        """Mark setup wizard as fully complete."""
        from setup_wizard.models import SetupProgress

        progress, _ = SetupProgress.objects.get_or_create(pk=1)
        progress.admin_user_configured = True
        progress.site_info_completed = True
        progress.contact_info_completed = True
        progress.currency_locale_completed = True
        progress.payment_methods_configured = True
        progress.save()
        self.stdout.write('  Setup wizard marked complete')

    def _accept_license(self):
        """Auto-accept the license agreement."""
        from django.core.management import call_command
        try:
            call_command('accept_license', auto_accept=True, verbosity=0)
            self.stdout.write('  License agreement auto-accepted')
        except Exception as e:
            self.stderr.write(self.style.WARNING(f'  Could not accept license: {e}'))

    def _enable_languages(self, default_language):
        """Enable default set of frontend languages."""
        try:
            from translations.models import SiteLanguage

            target_codes = [
                'en', 'fr', 'es', 'ja', 'pt', 'th',
                'it', 'vi', 'de', 'ru', 'ar', 'hi',
                'id', 'ko', 'zh',
            ]
            SiteLanguage.objects.filter(code__in=target_codes).update(is_active=True)

            # Set default language
            default = SiteLanguage.objects.filter(code=default_language).first()
            if default:
                default.is_default = True
                default.save(update_fields=['is_default'])

            self.stdout.write(f'  Enabled {len(target_codes)} languages (default: {default_language})')
        except Exception as e:
            self.stderr.write(self.style.WARNING(f'  Could not enable languages: {e}'))

    def _set_hosted_defaults(self):
        """Apply hosting-specific defaults for hosted instances."""
        # Configure SSL as managed externally (Cloudflare origin cert)
        self._configure_ssl_hosted()
        self.stdout.write('  Applied hosted-mode defaults')

    def _configure_ssl_hosted(self):
        """Set DomainConfiguration for hosted instances behind Cloudflare."""
        try:
            from domain_ssl.models import DomainConfiguration
            config = DomainConfiguration.get_instance()
            config.ssl_mode = DomainConfiguration.SSLMode.MANAGED_EXTERNALLY
            config.cert_domain = '*.myspwig.com'
            config.cert_issuer = 'Cloudflare Origin CA'
            config.status = DomainConfiguration.Status.IDLE
            config.last_error = ''
            config.save(update_fields=[
                'ssl_mode', 'cert_domain', 'cert_issuer', 'status', 'last_error',
            ])
            self.stdout.write('  SSL configured as managed externally (Cloudflare)')
        except Exception as e:
            self.stderr.write(self.style.WARNING(f'  Could not configure SSL: {e}'))

    def _configure_email(self, options, store_name, admin_email):
        """Create the Spwig hosted email account with gateway credentials.

        Credentials are sourced from either:
        1. --provision-data JSON (preferred, from fleet script or cloud-init)
        2. Individual --email-* flags (manual provisioning fallback)

        If no credentials are provided, email setup is skipped.
        """
        email_config = self._extract_email_config(options, store_name)
        if not email_config:
            self.stderr.write(self.style.WARNING(
                '  No email credentials provided — skipping email setup. '
                'Use --provision-data or --email-auth-user/--email-auth-token.'
            ))
            return

        from django.contrib.sites.models import Site
        from email_system.models import EmailAccount

        site = Site.objects.get(pk=1)

        # Idempotent: update if already exists
        account, created = EmailAccount.objects.get_or_create(
            site=site,
            provider_key='spwig_hosted_mail',
            defaults={
                'name': 'Spwig Email',
                'from_email': email_config['from_email'],
                'from_name': email_config['from_name'],
                'reply_to': admin_email or '',
                'is_active': True,
                'is_default': True,
            },
        )

        if not created:
            # Update existing account with fresh credentials
            account.from_email = email_config['from_email']
            account.from_name = email_config['from_name']
            if admin_email:
                account.reply_to = admin_email
            account.is_active = True
            account.is_default = True

        # Set encrypted credentials
        account.set_credentials({
            'gateway_host': email_config['gateway_host'],
            'gateway_port': email_config['gateway_port'],
            'auth_user': email_config['auth_user'],
            'auth_token': email_config['auth_token'],
        })
        account.save()

        action = 'Created' if created else 'Updated'
        self.stdout.write(
            f'  {action} Spwig Email account '
            f'(user: {email_config["auth_user"]}, '
            f'gateway: {email_config["gateway_host"]})'
        )

    def _extract_email_config(self, options, store_name):
        """Extract email configuration from provision data or CLI flags.

        Returns dict with gateway_host, gateway_port, auth_user, auth_token,
        from_email, from_name — or None if no credentials available.
        """
        # Try provision-data JSON first
        provision_json = options.get('provision_data', '')
        if provision_json:
            try:
                provision_data = json.loads(provision_json)
                email_data = provision_data.get('email', {})
                if email_data.get('auth_user') and email_data.get('auth_token'):
                    return {
                        'gateway_host': email_data.get('gateway_host', 'mail.myspwig.com'),
                        'gateway_port': email_data.get('gateway_port', 587),
                        'auth_user': email_data['auth_user'],
                        'auth_token': email_data['auth_token'],
                        'from_email': email_data.get('default_from_email', 'noreply@myspwig.com'),
                        'from_name': email_data.get('default_from_name', store_name),
                    }
            except (json.JSONDecodeError, TypeError) as e:
                self.stderr.write(self.style.WARNING(
                    f'  Could not parse --provision-data: {e}'
                ))

        # Fall back to individual flags
        auth_user = options.get('email_auth_user', '')
        auth_token = options.get('email_auth_token', '')
        if auth_user and auth_token:
            return {
                'gateway_host': options.get('email_gateway_host', 'mail.myspwig.com'),
                'gateway_port': options.get('email_gateway_port', 587),
                'auth_user': auth_user,
                'auth_token': auth_token,
                'from_email': options.get('email_from_address', '') or 'noreply@myspwig.com',
                'from_name': options.get('email_from_name', '') or store_name,
            }

        return None
