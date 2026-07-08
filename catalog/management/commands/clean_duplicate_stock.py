"""
Management command to find and clean up duplicate StockItem records.

Duplicate stock items can cause "get() returned more than one StockItem" errors.
This command identifies duplicates and helps clean them up safely.
"""
from django.core.management.base import BaseCommand
from django.db.models import Count
from catalog.models import StockItem, Product


class Command(BaseCommand):
    help = 'Find and optionally clean up duplicate StockItem records'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Actually fix the duplicates (keeps the first record, deletes others)',
        )

    def handle(self, *args, **options):
        fix_mode = options['fix']

        if fix_mode:
            self.stdout.write(self.style.WARNING('FIX MODE - Will delete duplicate records'))
        else:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))

        self.stdout.write('')

        # Find duplicate stock items (same product, warehouse, variant combination)
        from django.db.models import Q

        # Group by product, warehouse, and variant to find duplicates
        duplicates = StockItem.objects.values(
            'product_id', 'warehouse_id', 'variant_id'
        ).annotate(
            count=Count('id')
        ).filter(count__gt=1)

        if not duplicates:
            self.stdout.write(self.style.SUCCESS('No duplicate StockItem records found!'))
            return

        self.stdout.write(self.style.WARNING(f'Found {duplicates.count()} sets of duplicate records:\n'))

        total_deleted = 0

        for dup in duplicates:
            product_id = dup['product_id']
            warehouse_id = dup['warehouse_id']
            variant_id = dup['variant_id']
            count = dup['count']

            # Get all stock items with this combination
            stock_items = StockItem.objects.filter(
                product_id=product_id,
                warehouse_id=warehouse_id,
                variant_id=variant_id
            ).order_by('id')

            product = Product.objects.get(id=product_id)
            variant_info = f" (Variant ID: {variant_id})" if variant_id else " (Parent Product)"

            self.stdout.write(
                f'Product: {product.name} (ID: {product_id}){variant_info}, '
                f'Warehouse ID: {warehouse_id} - {count} duplicates'
            )

            for i, stock_item in enumerate(stock_items):
                if i == 0:
                    # Keep the first one
                    self.stdout.write(
                        f'  ✓ KEEP:   ID={stock_item.id}, On Hand={stock_item.on_hand}, '
                        f'Allocated={stock_item.allocated}, Low Stock={stock_item.low_stock_threshold}'
                    )
                else:
                    # Delete the rest
                    self.stdout.write(
                        self.style.WARNING(
                            f'  ✗ DELETE: ID={stock_item.id}, On Hand={stock_item.on_hand}, '
                            f'Allocated={stock_item.allocated}, Low Stock={stock_item.low_stock_threshold}'
                        )
                    )
                    if fix_mode:
                        stock_item.delete()
                        total_deleted += 1

            self.stdout.write('')

        if fix_mode:
            self.stdout.write(
                self.style.SUCCESS(f'Deleted {total_deleted} duplicate StockItem records')
            )
        else:
            self.stdout.write('')
            self.stdout.write(
                self.style.WARNING(
                    f'DRY RUN - Would delete {duplicates.count() * (count - 1)} records. '
                    'Run with --fix to actually delete them.'
                )
            )
