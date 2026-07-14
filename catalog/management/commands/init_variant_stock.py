"""
Management command to initialize stock items for product variants.

This creates StockItem records for all variants in all warehouses,
ensuring stock management UI appears correctly in the admin.
"""

from django.core.management.base import BaseCommand

from catalog.models import ProductVariant, StockItem, Warehouse


class Command(BaseCommand):
    help = "Initialize stock items for all product variants"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be created without actually creating records",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN MODE - No changes will be made"))

        # Get all warehouses
        warehouses = Warehouse.objects.all()
        warehouse_count = warehouses.count()

        if warehouse_count == 0:
            self.stdout.write(
                self.style.ERROR("No warehouses found! Please create at least one warehouse first.")
            )
            return

        self.stdout.write(f"Found {warehouse_count} warehouse(s)")

        # Get all variants
        variants = ProductVariant.objects.all()
        variant_count = variants.count()

        if variant_count == 0:
            self.stdout.write(self.style.WARNING("No product variants found."))
            return

        self.stdout.write(f"Found {variant_count} variant(s)")
        self.stdout.write("")

        created_count = 0
        skipped_count = 0

        for variant in variants:
            self.stdout.write(f"Processing: {variant.name} (SKU: {variant.sku})")

            for warehouse in warehouses:
                # Check if stock item already exists
                stock_item = StockItem.objects.filter(
                    product=variant.product, variant=variant, warehouse=warehouse
                ).first()

                if stock_item:
                    self.stdout.write(f"  ✓ Already exists for {warehouse.code}")
                    skipped_count += 1
                else:
                    if not dry_run:
                        stock_item = StockItem.objects.create(
                            product=variant.product,
                            variant=variant,
                            warehouse=warehouse,
                            on_hand=0,
                            allocated=0,
                            low_stock_threshold=0,
                        )
                        self.stdout.write(
                            self.style.SUCCESS(f"  ✓ Created stock item for {warehouse.code}")
                        )
                    else:
                        self.stdout.write(
                            self.style.SUCCESS(f"  → Would create stock item for {warehouse.code}")
                        )
                    created_count += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Summary:"))
        self.stdout.write(f"  - Created: {created_count}")
        self.stdout.write(f"  - Skipped (already exist): {skipped_count}")

        if dry_run:
            self.stdout.write("")
            self.stdout.write(
                self.style.WARNING("DRY RUN - Run without --dry-run to actually create records")
            )
