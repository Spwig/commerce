"""
Management command to bulk-update currency fields on existing records.

When a merchant changes their default currency in SiteSettings, existing records
retain their old currency (e.g. USD). This command updates all MoneyField currency
columns from one currency to another.

Usage:
    python manage.py fix_currency_defaults --dry-run
    python manage.py fix_currency_defaults --from-currency USD --to-currency SGD
    python manage.py fix_currency_defaults --from-currency USD --to-currency SGD --app catalog
"""
import logging

from django.apps import apps
from django.core.management.base import BaseCommand
from djmoney.models.fields import MoneyField as DjMoneyField

logger = logging.getLogger(__name__)

SKIP_APP_LABELS = {'license_checkout'}


class Command(BaseCommand):
    help = 'Bulk-update MoneyField currency columns from one currency to another'

    def add_arguments(self, parser):
        parser.add_argument(
            '--from-currency',
            type=str,
            help='Source currency code to replace (e.g. USD)',
        )
        parser.add_argument(
            '--to-currency',
            type=str,
            help='Target currency code (e.g. SGD). Defaults to SiteSettings.default_currency',
        )
        parser.add_argument(
            '--app',
            type=str,
            help='Limit to a specific app label (e.g. catalog, orders)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without making changes',
        )

    def handle(self, *args, **options):
        from_currency = options['from_currency']
        to_currency = options['to_currency']
        dry_run = options['dry_run']
        app_filter = options['app']

        if not to_currency:
            from core.utils import get_default_currency
            to_currency = get_default_currency()
            self.stdout.write(f"Using SiteSettings default currency: {to_currency}")

        if not from_currency:
            if not dry_run:
                self.stderr.write(self.style.ERROR(
                    'You must specify --from-currency or use --dry-run to scan all records'
                ))
                return
            self.stdout.write("Scanning all currency fields (dry run)...\n")

        if from_currency and from_currency == to_currency:
            self.stdout.write(self.style.WARNING(
                f'Source and target currencies are the same ({from_currency}). Nothing to do.'
            ))
            return

        total_affected = 0

        for model in apps.get_models():
            if model._meta.app_label in SKIP_APP_LABELS:
                continue
            if app_filter and model._meta.app_label != app_filter:
                continue

            currency_fields = []
            for field in model._meta.get_fields():
                if isinstance(field, DjMoneyField) and hasattr(field, '_currency_field'):
                    if field.default_currency is None:
                        continue  # Skip multi-currency fields
                    currency_fields.append(field._currency_field.name)

            if not currency_fields:
                continue

            for currency_field_name in currency_fields:
                if from_currency:
                    count = model.objects.filter(
                        **{currency_field_name: from_currency}
                    ).count()
                else:
                    # Dry run without --from-currency: show distribution
                    from django.db.models import Count
                    distribution = (
                        model.objects
                        .values(currency_field_name)
                        .annotate(count=Count('pk'))
                        .order_by('-count')
                    )
                    for entry in distribution:
                        curr = entry[currency_field_name]
                        cnt = entry['count']
                        if curr != to_currency and cnt > 0:
                            label = f"{model._meta.app_label}.{model._meta.model_name}"
                            self.stdout.write(
                                f"  {label}.{currency_field_name}: "
                                f"{cnt} records with {curr} (target: {to_currency})"
                            )
                            total_affected += cnt
                    continue

                if count == 0:
                    continue

                label = f"{model._meta.app_label}.{model._meta.model_name}"

                if dry_run:
                    self.stdout.write(
                        f"  {label}.{currency_field_name}: "
                        f"{count} records {from_currency} -> {to_currency}"
                    )
                    total_affected += count
                else:
                    updated = model.objects.filter(
                        **{currency_field_name: from_currency}
                    ).update(**{currency_field_name: to_currency})
                    self.stdout.write(self.style.SUCCESS(
                        f"  {label}.{currency_field_name}: "
                        f"updated {updated} records {from_currency} -> {to_currency}"
                    ))
                    total_affected += updated

        if dry_run:
            self.stdout.write(f"\nTotal records that would be affected: {total_affected}")
        else:
            self.stdout.write(self.style.SUCCESS(
                f"\nTotal records updated: {total_affected}"
            ))
