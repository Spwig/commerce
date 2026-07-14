"""
Management command to generate DKIM keys for the built-in SMTP server.

Usage:
    ./manage.py generate_dkim_keys --domain example.com
    ./manage.py generate_dkim_keys --domain example.com --selector mail2
    ./manage.py generate_dkim_keys --account-id 1
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from email_system.models import EmailAccount
from email_system.smtp_server.dkim_handler import DKIMHandler


class Command(BaseCommand):
    help = "Generate DKIM keys for email sending domain"

    def add_arguments(self, parser):
        parser.add_argument(
            "--domain", type=str, help="Domain to generate DKIM keys for (e.g., example.com)"
        )
        parser.add_argument(
            "--selector", type=str, default="mail", help="DKIM selector (default: mail)"
        )
        parser.add_argument("--account-id", type=int, help="EmailAccount ID to associate keys with")
        parser.add_argument(
            "--force", action="store_true", help="Force regenerate keys even if they already exist"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        domain = options.get("domain")
        selector = options.get("selector") or "mail"
        account_id = options.get("account_id")
        force = options.get("force", False)

        # Get EmailAccount if specified
        account = None
        if account_id:
            try:
                account = EmailAccount.objects.get(pk=account_id)
                # Extract domain from account if not provided
                if not domain and account.from_email and "@" in account.from_email:
                    domain = account.from_email.split("@")[1]
                    self.stdout.write(f"Using domain from account: {domain}")

            except EmailAccount.DoesNotExist:
                raise CommandError(f"EmailAccount with ID {account_id} does not exist")

        if not domain:
            raise CommandError("Either --domain or --account-id with valid from_email is required")

        # Initialize DKIM handler
        handler = DKIMHandler(domain=domain, selector=selector)

        # Check if keys already exist
        if not force:
            existing_private = handler.get_private_key(account)
            existing_public = handler.get_public_key(account)

            if existing_private and existing_public:
                self.stdout.write(
                    self.style.WARNING(
                        f"\nDKIM keys already exist for {selector}._domainkey.{domain}"
                    )
                )
                self.stdout.write("Use --force to regenerate")
                return

        # Generate new keys
        self.stdout.write(f"\nGenerating DKIM keys for {selector}._domainkey.{domain}...")

        private_key, public_key = handler.generate_key_pair()

        # Store keys
        handler.store_keys(private_key, public_key, account)

        self.stdout.write(self.style.SUCCESS("\n✓ DKIM keys generated successfully!\n"))

        # Display DNS record
        dns_record = handler.get_dns_record(account)
        dns_hostname = f"{selector}._domainkey.{domain}"

        self.stdout.write(self.style.WARNING("=" * 80))
        self.stdout.write(self.style.WARNING("DNS Configuration Required"))
        self.stdout.write(self.style.WARNING("=" * 80))
        self.stdout.write("\nAdd the following TXT record to your DNS:\n")
        self.stdout.write(self.style.SUCCESS(f"Hostname: {dns_hostname}"))
        self.stdout.write(self.style.SUCCESS("Type: TXT"))
        self.stdout.write(self.style.SUCCESS(f"Value: {dns_record}\n"))

        self.stdout.write(self.style.WARNING("=" * 80))
        self.stdout.write("\nNote: DNS propagation can take 15 minutes to 48 hours")
        self.stdout.write("You can verify propagation with:")
        self.stdout.write(self.style.SUCCESS(f"  dig TXT {dns_hostname}"))
        self.stdout.write(self.style.SUCCESS(f"  nslookup -type=TXT {dns_hostname}\n"))

        if account:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Keys stored in EmailAccount: {account.name} (ID: {account.pk})"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "Keys generated but not associated with an EmailAccount\n"
                    "Consider creating a built-in SMTP EmailAccount to store these keys"
                )
            )
