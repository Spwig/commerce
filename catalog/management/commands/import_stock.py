"""
Management command to import stock data from CSV

CSV Format:
    Product SKU, Warehouse Code, On Hand, [Low Stock Threshold]

Usage:
    ./manage.py import_stock --input stock_data.csv
    ./manage.py import_stock --input stock_data.csv --mode update (default)
    ./manage.py import_stock --input stock_data.csv --mode replace
    ./manage.py import_stock --input stock_data.csv --dry-run
"""

import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from catalog.models import Product, StockItem, StockMovement, Warehouse

User = get_user_model()


class Command(BaseCommand):
    help = "Import inventory stock data from CSV"

    def add_arguments(self, parser):
        parser.add_argument("--input", type=str, required=True, help="Input CSV file path")
        parser.add_argument(
            "--mode",
            type=str,
            choices=["update", "replace"],
            default="update",
            help="Import mode: update (add to existing) or replace (overwrite existing)",
        )
        parser.add_argument(
            "--dry-run", action="store_true", help="Preview changes without applying them"
        )
        parser.add_argument(
            "--create-missing",
            action="store_true",
            help="Create StockItems that don't exist (default: skip)",
        )

    def handle(self, *args, **options):
        input_file = options["input"]
        mode = options["mode"]
        dry_run = options["dry_run"]
        create_missing = options["create_missing"]

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN MODE - No changes will be saved"))

        # Read CSV file
        try:
            with open(input_file, encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)

                # Validate CSV headers
                required_fields = ["Product SKU", "Warehouse Code", "On Hand"]
                for field in required_fields:
                    if field not in reader.fieldnames:
                        raise CommandError(f"CSV missing required field: {field}")

                rows = list(reader)

        except OSError as e:
            raise CommandError(f"Error reading file: {e}")

        # Process rows
        stats = {"created": 0, "updated": 0, "skipped": 0, "errors": 0}

        with transaction.atomic():
            for i, row in enumerate(rows, 1):
                try:
                    result = self._process_row(row, mode, create_missing, dry_run)
                    stats[result] += 1

                except Exception as e:
                    stats["errors"] += 1
                    self.stdout.write(self.style.ERROR(f"Row {i}: Error - {str(e)}"))

            # Report results
            self.stdout.write("\n" + "=" * 50)
            self.stdout.write(self.style.SUCCESS("Import Summary:"))
            self.stdout.write(f"  Created: {stats['created']}")
            self.stdout.write(f"  Updated: {stats['updated']}")
            self.stdout.write(f"  Skipped: {stats['skipped']}")
            self.stdout.write(f"  Errors:  {stats['errors']}")

            if dry_run:
                self.stdout.write(self.style.WARNING("\nDRY RUN - Rolling back transaction"))
                raise CommandError("Dry run completed (transaction rolled back)")
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"\n✓ Successfully imported {stats['created'] + stats['updated']} stock items"
                    )
                )

    def _process_row(self, row, mode, create_missing, dry_run):
        """
        Process a single CSV row.

        Returns:
            str: Result status ('created', 'updated', 'skipped')
        """
        sku = row["Product SKU"].strip()
        warehouse_code = row["Warehouse Code"].strip()
        on_hand = int(row["On Hand"])
        low_stock_threshold = int(row.get("Low Stock Threshold", 0))

        # Validate product exists
        try:
            product = Product.objects.get(sku=sku)
        except Product.DoesNotExist:
            raise ValueError(f'Product with SKU "{sku}" not found')

        # Validate warehouse exists
        try:
            warehouse = Warehouse.objects.get(code=warehouse_code)
        except Warehouse.DoesNotExist:
            raise ValueError(f'Warehouse with code "{warehouse_code}" not found')

        # Check if StockItem exists
        try:
            stock_item = StockItem.objects.get(product=product, warehouse=warehouse)
            existed = True
        except StockItem.DoesNotExist:
            if not create_missing:
                self.stdout.write(
                    self.style.WARNING(
                        f"  Skipped: {sku} @ {warehouse_code} (use --create-missing to create)"
                    )
                )
                return "skipped"
            stock_item = StockItem(product=product, warehouse=warehouse)
            existed = False

        # Store old values for stock movement
        old_on_hand = stock_item.on_hand if existed else 0

        # Update values
        if mode == "replace":
            stock_item.on_hand = on_hand
        else:  # mode == 'update'
            stock_item.on_hand += on_hand

        if low_stock_threshold > 0:
            stock_item.low_stock_threshold = low_stock_threshold

        # Save (unless dry run)
        if not dry_run:
            stock_item.save()

            # Record stock movement if quantity changed
            if stock_item.on_hand != old_on_hand:
                StockMovement.objects.create(
                    stock_item=stock_item,
                    movement_type="adjustment",
                    quantity=stock_item.on_hand - old_on_hand,
                    previous_quantity=old_on_hand,
                    new_quantity=stock_item.on_hand,
                    reason=f"CSV import ({mode} mode)",
                )

        # Log result
        if existed:
            self.stdout.write(
                self.style.SUCCESS(
                    f"  Updated: {sku} @ {warehouse_code} - "
                    f"On Hand: {old_on_hand} → {stock_item.on_hand}"
                )
            )
            return "updated"
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"  Created: {sku} @ {warehouse_code} - On Hand: {stock_item.on_hand}"
                )
            )
            return "created"
