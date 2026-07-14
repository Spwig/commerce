"""
Management command to fix the PlanPricingTier schema by removing old price fields.
"""

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Remove old price fields from PlanPricingTier table"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Fixing PlanPricingTier schema..."))

        with connection.cursor() as cursor:
            # Drop old price columns (all possible formats)
            columns_to_drop = [
                "price",
                "price_per_unit",
                "price_amount",
                "price_currency",
                "price_per_unit_amount",
                "price_per_unit_currency",
            ]

            for column in columns_to_drop:
                try:
                    cursor.execute(f"""
                        ALTER TABLE subscriptions_planpricingtier
                        DROP COLUMN IF EXISTS {column} CASCADE;
                    """)
                    self.stdout.write(self.style.SUCCESS(f"  ✓ Dropped column: {column}"))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"  ! Column {column}: {e}"))

        self.stdout.write(self.style.SUCCESS("\n✅ Schema fixed successfully!"))
