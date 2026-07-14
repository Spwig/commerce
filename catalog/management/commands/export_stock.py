"""
Management command to export stock data to CSV

Usage:
    ./manage.py export_stock --output stock_export.csv
    ./manage.py export_stock --warehouse MAIN-WH --output warehouse_stock.csv
    ./manage.py export_stock --region DEFAULT --output regional_stock.csv
"""

import csv

from django.core.management.base import BaseCommand, CommandError

from catalog.models import SalesRegion, StockItem, Warehouse


class Command(BaseCommand):
    help = "Export inventory stock data to CSV"

    def add_arguments(self, parser):
        parser.add_argument("--output", type=str, required=True, help="Output CSV file path")
        parser.add_argument("--warehouse", type=str, help="Filter by warehouse code (optional)")
        parser.add_argument("--region", type=str, help="Filter by region code (optional)")
        parser.add_argument(
            "--sku", type=str, help="Filter by product SKU pattern (supports * wildcard, optional)"
        )

    def handle(self, *args, **options):
        output_file = options["output"]
        warehouse_code = options.get("warehouse")
        region_code = options.get("region")
        sku_pattern = options.get("sku")

        # Build queryset
        queryset = StockItem.objects.select_related(
            "product", "warehouse", "warehouse__region"
        ).order_by("warehouse__code", "product__sku")

        # Apply filters
        if warehouse_code:
            try:
                warehouse = Warehouse.objects.get(code=warehouse_code)
                queryset = queryset.filter(warehouse=warehouse)
                self.stdout.write(f"Filtering by warehouse: {warehouse.name}")
            except Warehouse.DoesNotExist:
                raise CommandError(f'Warehouse with code "{warehouse_code}" does not exist')

        if region_code:
            try:
                region = SalesRegion.objects.get(code=region_code)
                queryset = queryset.filter(warehouse__region=region)
                self.stdout.write(f"Filtering by region: {region.name}")
            except SalesRegion.DoesNotExist:
                raise CommandError(f'Region with code "{region_code}" does not exist')

        if sku_pattern:
            # Convert wildcard pattern to Django query
            if "*" in sku_pattern:
                django_pattern = sku_pattern.replace("*", "%")
                queryset = queryset.filter(product__sku__ilike=django_pattern)
            else:
                queryset = queryset.filter(product__sku=sku_pattern)
            self.stdout.write(f"Filtering by SKU pattern: {sku_pattern}")

        # Export to CSV
        try:
            with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)

                # Write header
                writer.writerow(
                    [
                        "Product SKU",
                        "Product Name",
                        "Warehouse Code",
                        "Warehouse Name",
                        "Region Code",
                        "Region Name",
                        "On Hand",
                        "Allocated",
                        "Available",
                        "Low Stock Threshold",
                        "Status",
                    ]
                )

                # Write data
                count = 0
                for stock_item in queryset:
                    available = stock_item.available
                    threshold = (
                        stock_item.low_stock_threshold or stock_item.product.low_stock_threshold
                    )

                    # Determine status
                    if available <= 0:
                        status = "OUT_OF_STOCK"
                    elif threshold > 0 and available <= threshold:
                        status = "LOW_STOCK"
                    else:
                        status = "IN_STOCK"

                    writer.writerow(
                        [
                            stock_item.product.sku,
                            stock_item.product.name,
                            stock_item.warehouse.code,
                            stock_item.warehouse.name,
                            stock_item.warehouse.region.code if stock_item.warehouse.region else "",
                            stock_item.warehouse.region.name if stock_item.warehouse.region else "",
                            stock_item.on_hand,
                            stock_item.allocated,
                            available,
                            threshold,
                            status,
                        ]
                    )
                    count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully exported {count} stock items to {output_file}"
                    )
                )

        except OSError as e:
            raise CommandError(f"Error writing to file: {e}")
