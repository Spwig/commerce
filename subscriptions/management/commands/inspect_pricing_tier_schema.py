"""
Management command to inspect PlanPricingTier database schema.
"""

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Inspect PlanPricingTier table schema"

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'subscriptions_planpricingtier'
                ORDER BY ordinal_position;
            """)

            self.stdout.write(self.style.SUCCESS("\nColumns in subscriptions_planpricingtier:"))
            self.stdout.write(self.style.SUCCESS("=" * 60))

            for row in cursor.fetchall():
                nullable = "NULL" if row[2] == "YES" else "NOT NULL"
                self.stdout.write(f"  {row[0]:<30} {row[1]:<20} {nullable}")
