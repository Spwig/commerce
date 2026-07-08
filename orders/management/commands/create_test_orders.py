"""
Management command to create test orders for analytics
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
from decimal import Decimal
import random
from orders.models import Order

User = get_user_model()


class Command(BaseCommand):
    help = 'Create test orders for analytics dashboard'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=30,
            help='Number of orders to create (default: 30)'
        )
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Spread orders over this many days (default: 30)'
        )

    def handle(self, *args, **options):
        count = options['count']
        days = options['days']

        self.stdout.write(f'Creating {count} test orders over {days} days...\n')

        # Get or create test users
        test_users = []
        for i in range(10):  # Create 10 test customers
            user, created = User.objects.get_or_create(
                username=f'test_customer_{i}',
                defaults={
                    'email': f'test.customer{i}@example.com',
                    'first_name': f'Test',
                    'last_name': f'Customer {i}',
                }
            )
            test_users.append(user)

        self.stdout.write(f'Using {len(test_users)} test customer accounts\n')

        # Order statuses
        statuses = [
            ('pending', 5),
            ('processing', 60),
            ('shipped', 20),
            ('delivered', 10),
            ('completed', 5),
        ]

        # Sales channels/sources
        sources = [
            ('web', 70),
            ('mobile', 20),
            ('social', 5),
            ('referral', 3),
            ('organic', 2),
        ]

        # Countries
        countries = ['US', 'GB', 'CA', 'DE', 'FR', 'AU', 'JP']

        created_count = 0
        now = timezone.now()

        for i in range(count):
            # Random timestamp within the date range
            days_ago = random.randint(0, days)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            timestamp = now - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)

            # Select status
            status = random.choices([s[0] for s in statuses], weights=[s[1] for s in statuses])[0]

            # Select source
            source = random.choices([s[0] for s in sources], weights=[s[1] for s in sources])[0]

            # Random amounts
            subtotal = Decimal(str(random.uniform(25.0, 500.0))).quantize(Decimal('0.01'))
            tax_rate = Decimal('0.10')  # 10% tax
            tax_amount = (subtotal * tax_rate).quantize(Decimal('0.01'))
            shipping_cost = Decimal(str(random.choice([0.0, 5.99, 9.99, 14.99]))).quantize(Decimal('0.01'))
            discount_amount = Decimal('0.00')

            # Occasionally add a discount
            if random.random() < 0.2:  # 20% of orders have a discount
                discount_amount = (subtotal * Decimal(str(random.uniform(0.05, 0.25)))).quantize(Decimal('0.01'))

            total_amount = (subtotal + tax_amount + shipping_cost - discount_amount).quantize(Decimal('0.01'))

            # Generate order number
            order_number = f'TEST-{now.year}{(i+1):05d}'

            # Random country
            country = random.choice(countries)

            # Select random user
            user = random.choice(test_users)
            email = user.email

            # Create order
            order = Order.objects.create(
                order_number=order_number,
                user=user,
                status=status,
                source=source,
                email=email,
                phone='+1234567890',
                # Shipping address
                shipping_name=f'Test Customer {i}',
                shipping_address1=f'{random.randint(100, 9999)} Main Street',
                shipping_address2=f'Apt {random.randint(1, 500)}' if random.random() < 0.3 else '',
                shipping_city='Test City',
                shipping_state='TS',
                shipping_postal_code='12345',
                shipping_country=country,
                # Billing same as shipping
                billing_same_as_shipping=True,
                # Amounts
                subtotal=subtotal,
                tax_amount=tax_amount,
                shipping_cost=shipping_cost,
                discount_amount=discount_amount,
                total_amount=total_amount,
                subtotal_currency='USD',
                tax_amount_currency='USD',
                shipping_cost_currency='USD',
                discount_amount_currency='USD',
                total_amount_currency='USD',
                # Timestamps
                created_at=timestamp,
                updated_at=timestamp,
            )

            # Set delivered date for delivered/completed orders
            if status in ['delivered', 'completed']:
                order.delivered_at = timestamp + timedelta(days=random.randint(3, 10))
                order.save()

            created_count += 1

            if (created_count % 10) == 0:
                self.stdout.write(f'  Created {created_count}/{count} orders...')

        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully created {created_count} test orders!'))

        # Calculate totals
        total_revenue = sum([
            Decimal(str(random.uniform(25.0, 500.0))) * Decimal('1.10')
            for _ in range(count)
        ])
        avg_order_value = total_revenue / count if count > 0 else 0

        self.stdout.write('\nOrder statistics:')
        self.stdout.write(f'  Total orders: {created_count}')
        self.stdout.write(f'  Status distribution:')
        for status, weight in statuses:
            self.stdout.write(f'    {status}: ~{weight}%')
        self.stdout.write(f'  Channel distribution:')
        for source, weight in sources:
            self.stdout.write(f'    {source}: ~{weight}%')
