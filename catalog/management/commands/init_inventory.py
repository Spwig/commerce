"""
Management command to initialize multi-location inventory structure

Creates default SalesRegion and Warehouse for merchants who need to set up
the multi-location inventory system.

Usage:
    ./manage.py init_inventory --country US --currency USD --address "123 Main St" --city "New York" --postal-code "10001"
    ./manage.py init_inventory --country NZ --currency NZD --address "10 Queen St" --city "Auckland" --postal-code "1010"
"""
from django.core.management.base import BaseCommand, CommandError
from catalog.models import SalesRegion, Warehouse
from django.utils.translation import gettext as _


class Command(BaseCommand):
    help = 'Initialize default multi-location inventory structure (SalesRegion and Warehouse)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--country',
            type=str,
            required=True,
            help='Two-letter country code (e.g., US, NZ, SG)'
        )
        parser.add_argument(
            '--currency',
            type=str,
            required=True,
            help='Three-letter currency code (e.g., USD, NZD, SGD)'
        )
        parser.add_argument(
            '--address',
            type=str,
            required=True,
            help='Warehouse address line 1'
        )
        parser.add_argument(
            '--city',
            type=str,
            required=True,
            help='City'
        )
        parser.add_argument(
            '--postal-code',
            type=str,
            required=True,
            help='Postal/ZIP code'
        )
        parser.add_argument(
            '--state',
            type=str,
            default='',
            help='State or province (optional)'
        )
        parser.add_argument(
            '--region-name',
            type=str,
            help='Custom region name (optional, defaults to "Default Region")'
        )
        parser.add_argument(
            '--region-code',
            type=str,
            default='DEFAULT',
            help='Custom region code (optional, defaults to "DEFAULT")'
        )
        parser.add_argument(
            '--warehouse-name',
            type=str,
            help='Custom warehouse name (optional, defaults to "Main Warehouse")'
        )
        parser.add_argument(
            '--warehouse-code',
            type=str,
            default='MAIN-WH',
            help='Custom warehouse code (optional, defaults to "MAIN-WH")'
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Contact email for warehouse'
        )
        parser.add_argument(
            '--phone',
            type=str,
            help='Contact phone for warehouse'
        )

    def handle(self, *args, **options):
        country = options['country'].upper()
        currency = options['currency'].upper()
        address = options['address']
        city = options['city']
        postal_code = options['postal_code']
        state = options.get('state', '')
        region_name = options.get('region_name') or _('Default Region')
        region_code = options['region_code']
        warehouse_name = options.get('warehouse_name') or _('Main Warehouse')
        warehouse_code = options['warehouse_code']
        email = options.get('email', '')
        phone = options.get('phone', '')

        # Validate inputs
        if len(country) != 2:
            raise CommandError('Country code must be exactly 2 characters (e.g., US, NZ)')

        if len(currency) != 3:
            raise CommandError('Currency code must be exactly 3 characters (e.g., USD, NZD)')

        # Create or update SalesRegion
        region, region_created = SalesRegion.objects.get_or_create(
            code=region_code,
            defaults={
                'name': region_name,
                'countries': [country],
                'default_currency': currency,
                'is_active': True,
                'priority': 100
            }
        )

        if region_created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Created SalesRegion: {region.name} ({region.code})'
                )
            )
        else:
            # Update existing region to include this country if not already present
            if country not in region.countries:
                region.countries.append(country)
                region.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Updated SalesRegion "{region.name}" to include country: {country}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'⚠ SalesRegion "{region.name}" already exists and includes {country}'
                    )
                )

        # Create or update Warehouse
        warehouse, warehouse_created = Warehouse.objects.get_or_create(
            code=warehouse_code,
            defaults={
                'name': warehouse_name,
                'region': region,
                'address_line1': address,
                'address_line2': '',
                'city': city,
                'state_province': state,
                'postal_code': postal_code,
                'country': country,
                'is_active': True,
                'fulfillment_priority': 100,
                'stock_buffer_percentage': 10,
                'contact_email': email,
                'contact_phone': phone
            }
        )

        if warehouse_created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Created Warehouse: {warehouse.name} ({warehouse.code})'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'⚠ Warehouse "{warehouse.name}" already exists'
                )
            )

        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('Inventory Structure Summary:'))
        self.stdout.write(f'\nSalesRegion:')
        self.stdout.write(f'  Name: {region.name}')
        self.stdout.write(f'  Code: {region.code}')
        self.stdout.write(f'  Countries: {", ".join(region.countries)}')
        self.stdout.write(f'  Currency: {region.default_currency}')
        self.stdout.write(f'  Priority: {region.priority}')
        self.stdout.write(f'\nWarehouse:')
        self.stdout.write(f'  Name: {warehouse.name}')
        self.stdout.write(f'  Code: {warehouse.code}')
        self.stdout.write(f'  Address: {warehouse.address_line1}, {warehouse.city}')
        self.stdout.write(f'  Region: {warehouse.region.name}')
        self.stdout.write(f'  Priority: {warehouse.fulfillment_priority}')

        # Next steps
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('✓ Inventory structure is ready!'))
        self.stdout.write('\nNext steps:')
        self.stdout.write('  1. Add stock for your products using Django admin')
        self.stdout.write('  2. Or import stock from CSV: ./manage.py import_stock --input stock.csv')
        self.stdout.write('  3. Products will now show stock availability by region')
