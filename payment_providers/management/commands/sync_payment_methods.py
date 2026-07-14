"""
Management command to sync payment methods from provider APIs.

Usage:
    python manage.py sync_payment_methods              # Sync all providers
    python manage.py sync_payment_methods --provider=airwallex  # Sync specific provider
    python manage.py sync_payment_methods --account=<uuid>      # Sync specific account
"""

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import gettext as _

from payment_providers.models import PaymentProviderAccount


class Command(BaseCommand):
    help = _("Sync payment methods from payment provider APIs")

    def add_arguments(self, parser):
        parser.add_argument(
            "--provider",
            type=str,
            help="Sync only accounts for specified provider slug (e.g., airwallex)",
        )
        parser.add_argument(
            "--account",
            type=str,
            help="Sync specific account by UUID",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force sync even if recently synced",
        )

    def handle(self, *args, **options):
        provider_slug = options.get("provider")
        account_uuid = options.get("account")
        options.get("force", False)
        # `BaseCommand` doesn't make verbosity a self attribute on Django
        # 4.x+; keep a local instead so `--verbosity 2` still works.
        verbosity = int(options.get("verbosity", 1))

        # Build queryset
        queryset = PaymentProviderAccount.objects.filter(is_active=True)

        if account_uuid:
            # Sync specific account
            try:
                queryset = queryset.filter(id=account_uuid)
                if not queryset.exists():
                    raise CommandError(f"Account with UUID {account_uuid} not found")
            except ValueError:
                raise CommandError(f"Invalid UUID: {account_uuid}")
        elif provider_slug:
            # Sync all accounts for specific provider
            queryset = queryset.filter(component__slug=provider_slug)
            if not queryset.exists():
                raise CommandError(f"No active accounts found for provider: {provider_slug}")

        accounts_count = queryset.count()

        if accounts_count == 0:
            self.stdout.write(
                self.style.WARNING("No active payment provider accounts found to sync")
            )
            return

        self.stdout.write(f"\nSyncing payment methods for {accounts_count} account(s)...\n")

        success_count = 0
        error_count = 0

        for account in queryset:
            provider_name = account.component.name
            self.stdout.write(f"\n[{account.id}] {provider_name}:")

            # Check if provider supports payment method sync
            try:
                provider_instance = account.get_provider_instance()
                if not hasattr(provider_instance, "get_payment_method_types"):
                    self.stdout.write(
                        self.style.WARNING(
                            f"  ⊗ Provider {provider_name} does not support payment method synchronization"
                        )
                    )
                    continue
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ Failed to load provider: {str(e)}"))
                error_count += 1
                continue

            # Sync payment methods
            try:
                result = account.sync_payment_methods()

                if result["success"]:
                    methods_data = result.get("methods", {})
                    total_countries = len(methods_data)
                    total_methods = sum(len(methods) for methods in methods_data.values())

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  ✓ Synced {total_methods} payment methods across {total_countries} countries"
                        )
                    )

                    # Show sample of synced data
                    if verbosity >= 2:
                        for country_code, methods in list(methods_data.items())[:3]:
                            methods_str = ", ".join(methods)
                            self.stdout.write(f"    • {country_code}: {methods_str}")
                        if total_countries > 3:
                            self.stdout.write(f"    ... and {total_countries - 3} more countries")

                    success_count += 1
                else:
                    error_msg = result.get("message", "Unknown error")
                    self.stdout.write(self.style.ERROR(f"  ✗ Sync failed: {error_msg}"))
                    error_count += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ Unexpected error: {str(e)}"))
                error_count += 1

        # Summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS(f"✓ Successfully synced: {success_count}"))
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f"✗ Failed: {error_count}"))
        self.stdout.write("=" * 60 + "\n")
