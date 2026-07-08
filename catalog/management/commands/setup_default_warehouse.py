"""
Management command to set up default sales region and warehouse for merchants.
This command should be run after initial setup or when migrating from single-location to multi-location inventory.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from catalog.models import SalesRegion, Warehouse, Product, StockItem
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Create default sales region and warehouse, migrate existing product quantities to StockItem model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--region-name',
            type=str,
            default='Default Region',
            help='Name for the default sales region (default: "Default Region")',
        )
        parser.add_argument(
            '--region-code',
            type=str,
            default='DEFAULT',
            help='Code for the default sales region (default: "DEFAULT")',
        )
        parser.add_argument(
            '--warehouse-name',
            type=str,
            default='Main Warehouse',
            help='Name for the default warehouse (default: "Main Warehouse")',
        )
        parser.add_argument(
            '--warehouse-code',
            type=str,
            default='MAIN-WH',
            help='Code for the default warehouse (default: "MAIN-WH")',
        )
        parser.add_argument(
            '--currency',
            type=str,
            default='USD',
            help='Default currency code (default: "USD")',
        )
        parser.add_argument(
            '--country',
            type=str,
            default='US',
            help='Country code for warehouse (default: "US")',
        )
        parser.add_argument(
            '--skip-stock-migration',
            action='store_true',
            help='Skip migrating product quantities to stock items (only create region/warehouse)',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('='*60)
        self.stdout.write(self.style.SUCCESS('Setting up Multi-Location Inventory System'))
        self.stdout.write('='*60 + '\n')

        # Extract options
        region_name = options['region_name']
        region_code = options['region_code']
        warehouse_name = options['warehouse_name']
        warehouse_code = options['warehouse_code']
        currency = options['currency']
        country = options['country']
        skip_migration = options['skip_stock_migration']

        # Step 1: Create or get default sales region
        self.stdout.write('Step 1: Setting up default sales region...')
        region, created = SalesRegion.objects.get_or_create(
            code=region_code,
            defaults={
                'name': region_name,
                'countries': [country],
                'default_currency': currency,
                'is_active': True,
                'priority': 100,  # High priority for default region
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'  ✓ Created sales region: {region.name} ({region.code})'))
        else:
            self.stdout.write(self.style.WARNING(f'  ⚠ Sales region already exists: {region.name} ({region.code})'))

        # Step 2: Create or get default warehouse
        self.stdout.write('\nStep 2: Setting up default warehouse...')

        # Get site for address defaults
        site = Site.objects.get(pk=1)

        warehouse, created = Warehouse.objects.get_or_create(
            code=warehouse_code,
            defaults={
                'name': warehouse_name,
                'region': region,
                'address_line1': '123 Main Street',  # Placeholder - merchants should update
                'city': 'City',
                'postal_code': '00000',
                'country': country,
                'is_active': True,
                'fulfillment_priority': 100,  # High priority for default warehouse
                'stock_buffer_percentage': 10,  # 10% safety buffer
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'  ✓ Created warehouse: {warehouse.name} ({warehouse.code})'))
            self.stdout.write(self.style.WARNING(f'  ⚠ Please update the warehouse address in the admin interface'))
        else:
            self.stdout.write(self.style.WARNING(f'  ⚠ Warehouse already exists: {warehouse.name} ({warehouse.code})'))

        # Step 3: Migrate existing product quantities to StockItem model
        if not skip_migration:
            self.stdout.write('\nStep 3: Migrating product inventory to multi-location system...')

            # Get all products that track inventory
            products = Product.objects.all()
            total_products = products.count()

            if total_products == 0:
                self.stdout.write(self.style.WARNING('  ⚠ No products found'))
            else:
                migrated_count = 0
                skipped_count = 0

                for product in products:
                    # Check if stock item already exists for this product-warehouse combo
                    existing = StockItem.objects.filter(
                        product=product,
                        warehouse=warehouse
                    ).first()

                    if existing:
                        skipped_count += 1
                        continue

                    # Create stock item with on_hand = 0 (since Product.quantity field was removed)
                    # Merchants will need to adjust stock levels via the admin interface
                    StockItem.objects.create(
                        product=product,
                        warehouse=warehouse,
                        on_hand=0,
                        allocated=0,
                        low_stock_threshold=product.low_stock_threshold if hasattr(product, 'low_stock_threshold') else 5,
                    )
                    migrated_count += 1

                self.stdout.write(self.style.SUCCESS(f'  ✓ Created stock items: {migrated_count}'))
                if skipped_count > 0:
                    self.stdout.write(self.style.WARNING(f'  ⚠ Skipped (already exist): {skipped_count}'))

                self.stdout.write(self.style.WARNING('\n  ⚠ IMPORTANT: All products now have 0 stock at the warehouse.'))
                self.stdout.write(self.style.WARNING('  Please use the Stock Items admin to set actual stock levels.'))
        else:
            self.stdout.write('\nStep 3: Skipped stock migration (--skip-stock-migration flag)')

        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('✅ Setup Complete!'))
        self.stdout.write('='*60)
        self.stdout.write('\nNext Steps:')
        self.stdout.write('  1. Update warehouse address in: Admin → Catalog → Warehouses')
        self.stdout.write('  2. Set stock levels in: Admin → Catalog → Stock Items')
        self.stdout.write('  3. (Optional) Create additional regions/warehouses as needed')
        self.stdout.write('  4. (Optional) Configure product region visibility if needed')
        self.stdout.write('='*60 + '\n')
