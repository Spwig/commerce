"""
Management command to test the shipping package packing algorithm.

Usage:
    python manage.py test_packing_algorithm

Creates sample packages and items, then demonstrates the packing algorithm.
"""

from django.core.management.base import BaseCommand
from decimal import Decimal
from shipping.models import ShippingPackage
from shipping.utils.packing import PackableItem, PackingAlgorithm


class Command(BaseCommand):
    help = 'Test the shipping package packing algorithm with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--optimize',
            type=str,
            default='cost',
            choices=['cost', 'volume', 'count'],
            help='Optimization strategy (default: cost)'
        )

    def handle(self, *args, **options):
        optimize_for = options['optimize']

        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write(self.style.SUCCESS('SHIPPING PACKAGE PACKING ALGORITHM TEST'))
        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write('')

        # Get or create sample packages
        packages = self._ensure_sample_packages()

        self.stdout.write(self.style.SUCCESS(f'\n📦 Available Shipping Packages ({len(packages)})'))
        self.stdout.write(self.style.SUCCESS('-' * 80))
        for pkg in packages:
            external_dims = pkg.get_external_dimensions()
            self.stdout.write(
                f'  • {pkg.name}:'
            )
            self.stdout.write(
                f'    Internal: {pkg.length}×{pkg.width}×{pkg.height}cm '
                f'(volume: {pkg.get_volume_liters():.2f}L)'
            )
            self.stdout.write(
                f'    External: {external_dims["length"]}×{external_dims["width"]}×{external_dims["height"]}cm '
                f'(wall: {pkg.wall_thickness}cm)'
            )
            self.stdout.write(
                f'    Max weight: {pkg.max_weight}kg, tare: {pkg.tare_weight}kg, priority: {pkg.priority}'
            )

        # Create sample items to pack
        sample_items = self._create_sample_items()

        self.stdout.write(self.style.SUCCESS(f'\n📋 Items to Pack ({len(sample_items)})'))
        self.stdout.write(self.style.SUCCESS('-' * 80))
        total_weight = Decimal('0')
        total_volume = Decimal('0')
        for item in sample_items:
            item_volume = item.get_volume()
            total_weight += item.weight * item.quantity
            total_volume += item_volume * item.quantity
            self.stdout.write(
                f'  • {item.name} (×{item.quantity}): '
                f'{item.length}×{item.width}×{item.height}cm, '
                f'{item.weight}kg, '
                f'{item_volume:.0f}cm³'
            )

        self.stdout.write('')
        self.stdout.write(f'  Total Weight: {total_weight}kg')
        self.stdout.write(f'  Total Volume: {total_volume:.0f}cm³ ({total_volume/1000:.2f}L)')

        # Run packing algorithm
        self.stdout.write(self.style.SUCCESS(f'\n🔧 Running Packing Algorithm'))
        self.stdout.write(self.style.SUCCESS(f'   Optimization Strategy: {optimize_for.upper()}'))
        self.stdout.write(self.style.SUCCESS('-' * 80))

        algorithm = PackingAlgorithm(list(packages))
        results = algorithm.pack_items(sample_items, optimize_for=optimize_for)

        if not results:
            self.stdout.write(self.style.ERROR('\n❌ No valid packing found!'))
            self.stdout.write(self.style.WARNING('Possible reasons:'))
            self.stdout.write('  • Items too large for available packages')
            self.stdout.write('  • Items too heavy for available packages')
            self.stdout.write('  • No active shipping packages defined')
            return

        # Display results
        self.stdout.write(self.style.SUCCESS(f'\n✅ Packing Complete'))
        self.stdout.write(self.style.SUCCESS('-' * 80))
        self.stdout.write(f'  Packages Required: {len(results)}')
        self.stdout.write('')

        total_cost = Decimal('0')
        total_weight_shipped = Decimal('0')

        for i, result in enumerate(results, 1):
            external_dims = result.package.get_external_dimensions()

            self.stdout.write(self.style.SUCCESS(f'\n  Package #{i}: {result.package.name}'))
            self.stdout.write(f'    Internal Dimensions: {result.package.length}×{result.package.width}×{result.package.height}cm (used for packing)')
            self.stdout.write(f'    External Dimensions: {external_dims["length"]}×{external_dims["width"]}×{external_dims["height"]}cm (sent to carriers)')
            self.stdout.write(f'    Items Packed: {len(result.items)}')

            # List items
            item_names = {}
            for item in result.items:
                item_names[item.name] = item_names.get(item.name, 0) + 1

            for name, count in item_names.items():
                self.stdout.write(f'      - {name} (×{count})')

            self.stdout.write(f'    Total Weight: {result.total_weight:.3f}kg (includes {result.package.tare_weight}kg package)')
            self.stdout.write(f'    Weight Utilization: {result.weight_utilization:.1f}% ({result.total_weight:.3f}kg / {result.package.max_weight}kg)')
            self.stdout.write(f'    Volume Utilization: {result.volume_utilization:.1f}%')

            if result.package.cost:
                self.stdout.write(f'    Package Cost: {result.package.cost}')
                total_cost += result.package.cost.amount

            total_weight_shipped += result.total_weight

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 80))
        self.stdout.write(self.style.SUCCESS('SUMMARY'))
        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write(f'  Total Packages: {len(results)}')
        self.stdout.write(f'  Total Weight (with packaging): {total_weight_shipped:.3f}kg')
        if total_cost > 0:
            self.stdout.write(f'  Total Package Cost: ${total_cost:.2f}')

        # Efficiency metrics
        items_packed = sum(len(r.items) for r in results)
        items_total = sum(item.quantity for item in sample_items)

        if items_packed == items_total:
            self.stdout.write(self.style.SUCCESS(f'  ✓ All {items_total} items successfully packed!'))
        else:
            self.stdout.write(self.style.WARNING(f'  ⚠ Only {items_packed} of {items_total} items packed'))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 80))

    def _ensure_sample_packages(self):
        """Create sample packages if none exist"""
        # Check if we already have packages
        existing = ShippingPackage.objects.filter(is_active=True)

        if existing.exists():
            return existing

        self.stdout.write(self.style.WARNING('No shipping packages found. Creating samples...'))

        # Create sample packages
        packages = [
            ShippingPackage(
                name='Small Envelope',
                length=Decimal('25'),
                width=Decimal('18'),
                height=Decimal('2'),
                max_weight=Decimal('0.5'),
                tare_weight=Decimal('0.05'),
                priority=10,
                is_active=True
            ),
            ShippingPackage(
                name='Medium Box',
                length=Decimal('30'),
                width=Decimal('20'),
                height=Decimal('15'),
                max_weight=Decimal('5.0'),
                tare_weight=Decimal('0.2'),
                priority=50,
                is_active=True
            ),
            ShippingPackage(
                name='Large Box',
                length=Decimal('50'),
                width=Decimal('40'),
                height=Decimal('30'),
                max_weight=Decimal('20.0'),
                tare_weight=Decimal('0.5'),
                priority=30,
                is_active=True
            ),
            ShippingPackage(
                name='Extra Large Box',
                length=Decimal('80'),
                width=Decimal('60'),
                height=Decimal('50'),
                max_weight=Decimal('50.0'),
                tare_weight=Decimal('1.0'),
                priority=10,
                is_active=True
            ),
        ]

        ShippingPackage.objects.bulk_create(packages)
        self.stdout.write(self.style.SUCCESS(f'Created {len(packages)} sample packages'))

        return ShippingPackage.objects.filter(is_active=True)

    def _create_sample_items(self):
        """Create sample items to pack"""
        return [
            PackableItem(
                id='book_1',
                name='Hardcover Book',
                length=Decimal('24'),
                width=Decimal('16'),
                height=Decimal('3'),
                weight=Decimal('0.8'),
                quantity=2
            ),
            PackableItem(
                id='tshirt_1',
                name='T-Shirt (folded)',
                length=Decimal('25'),
                width=Decimal('20'),
                height=Decimal('2'),
                weight=Decimal('0.2'),
                quantity=3
            ),
            PackableItem(
                id='mug_1',
                name='Coffee Mug',
                length=Decimal('12'),
                width=Decimal('10'),
                height=Decimal('10'),
                weight=Decimal('0.4'),
                quantity=2
            ),
            PackableItem(
                id='phone_case_1',
                name='Phone Case',
                length=Decimal('18'),
                width=Decimal('10'),
                height=Decimal('1'),
                weight=Decimal('0.1'),
                quantity=1
            ),
        ]
