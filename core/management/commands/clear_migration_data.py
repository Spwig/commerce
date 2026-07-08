"""
Management command to clear all migration-related data from the database.
This prepares the database for a fresh WooCommerce migration.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Clear all migration-related data (customers, products, orders, reviews, categories, coupons)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-confirm',
            action='store_true',
            help='Skip confirmation prompt',
        )

    def handle(self, *args, **options):
        # Import models here to avoid circular imports
        from catalog.models import Category, Product, ProductVariant, ProductImage, ProductReview
        from orders.models import Order, OrderItem, Address
        from cart.models import Cart, CartItem
        from vouchers.models import VoucherCode, VoucherUsage, AppliedVoucher, GiftCard
        from customers.models import CustomerMetrics, AbandonedCart, CustomerNote

        if not options['no_confirm']:
            self.stdout.write(self.style.WARNING(
                '\n⚠️  WARNING: This will delete ALL of the following data:\n'
                '   - Categories\n'
                '   - Products (and variants, images)\n'
                '   - Product Reviews\n'
                '   - Orders (and order items)\n'
                '   - Addresses\n'
                '   - Carts\n'
                '   - Vouchers (codes, usage, gift cards)\n'
                '   - Customer Metrics\n'
                '   - Abandoned Carts\n'
                '   - Customer Notes\n'
                '   - Guest users (username starting with "guest_")\n'
            ))
            confirm = input('\nAre you sure you want to continue? Type "yes" to confirm: ')
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.ERROR('Operation cancelled.'))
                return

        self.stdout.write(self.style.WARNING('\n🧹 Starting cleanup...\n'))

        try:
            with transaction.atomic():
                # Count items before deletion
                counts = {
                    'carts': Cart.objects.count(),
                    'cart_items': CartItem.objects.count(),
                    'abandoned_carts': AbandonedCart.objects.count(),
                    'order_items': OrderItem.objects.count(),
                    'orders': Order.objects.count(),
                    'reviews': ProductReview.objects.count(),
                    'product_images': ProductImage.objects.count(),
                    'product_variants': ProductVariant.objects.count(),
                    'products': Product.objects.count(),
                    'categories': Category.objects.count(),
                    'voucher_codes': VoucherCode.objects.count(),
                    'voucher_usage': VoucherUsage.objects.count(),
                    'applied_vouchers': AppliedVoucher.objects.count(),
                    'gift_cards': GiftCard.objects.count(),
                    'addresses': Address.objects.count(),
                    'customer_metrics': CustomerMetrics.objects.count(),
                    'customer_notes': CustomerNote.objects.count(),
                    'guest_users': User.objects.filter(username__startswith='guest_').count(),
                }

                # Delete in correct order to avoid foreign key constraints
                self.stdout.write('Deleting abandoned carts...')
                AbandonedCart.objects.all().delete()

                self.stdout.write('Deleting carts and cart items...')
                CartItem.objects.all().delete()
                Cart.objects.all().delete()

                self.stdout.write('Deleting orders and order items...')
                OrderItem.objects.all().delete()
                Order.objects.all().delete()

                self.stdout.write('Deleting product reviews...')
                ProductReview.objects.all().delete()

                self.stdout.write('Deleting product images...')
                ProductImage.objects.all().delete()

                self.stdout.write('Deleting product variants...')
                ProductVariant.objects.all().delete()

                self.stdout.write('Deleting products...')
                Product.objects.all().delete()

                self.stdout.write('Deleting categories...')
                Category.objects.all().delete()

                self.stdout.write('Deleting vouchers and gift cards...')
                AppliedVoucher.objects.all().delete()
                VoucherUsage.objects.all().delete()
                GiftCard.objects.all().delete()
                VoucherCode.objects.all().delete()

                self.stdout.write('Deleting addresses...')
                Address.objects.all().delete()

                self.stdout.write('Deleting customer metrics...')
                CustomerMetrics.objects.all().delete()

                self.stdout.write('Deleting customer notes...')
                CustomerNote.objects.all().delete()

                self.stdout.write('Deleting guest users...')
                User.objects.filter(username__startswith='guest_').delete()

                # Show summary
                self.stdout.write(self.style.SUCCESS('\n✅ Cleanup completed successfully!\n'))
                self.stdout.write(self.style.SUCCESS('Items deleted:'))
                for model, count in counts.items():
                    if count > 0:
                        self.stdout.write(f'   - {model}: {count}')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Error during cleanup: {e}'))
            raise
