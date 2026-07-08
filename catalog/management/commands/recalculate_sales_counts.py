from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Sum

from catalog.models import Product
from orders.models import OrderItem


class Command(BaseCommand):
    help = 'Recalculate Product.sales_count from historical paid orders'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        # Aggregate quantities from paid, non-test orders, top-level items only
        aggregated = (
            OrderItem.objects
            .filter(
                order__payment_status='paid',
                order__is_test_order=False,
                parent_bundle__isnull=True,
            )
            .values('product_id')
            .annotate(total_sold=Sum('quantity'))
            .order_by('-total_sold')
        )

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - No changes will be made\n'))
            total_units = 0
            for row in aggregated:
                try:
                    product = Product.objects.get(pk=row['product_id'])
                    name = product.name
                except Product.DoesNotExist:
                    name = f"[deleted product {row['product_id']}]"
                self.stdout.write(f"  {name}: {row['total_sold']} units")
                total_units += row['total_sold']
            self.stdout.write(f"\nTotal: {aggregated.count()} products, {total_units} units")
            return

        # Atomic reset + apply to prevent a window of zero counts
        with transaction.atomic():
            Product.objects.all().update(sales_count=0)

            updated = 0
            total_units = 0
            for row in aggregated:
                Product.objects.filter(pk=row['product_id']).update(
                    sales_count=row['total_sold']
                )
                updated += 1
                total_units += row['total_sold']

        self.stdout.write(self.style.SUCCESS(
            f'Updated sales_count for {updated} products ({total_units} total units sold)'
        ))
