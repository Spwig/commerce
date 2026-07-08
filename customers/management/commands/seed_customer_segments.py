from decimal import Decimal

from core.management.commands._seed_base import SeedCommand


class Command(SeedCommand):
    seed_name = 'customer_segments'
    seed_version = 1
    help = 'Seed default customer segments (VIP, High Value, etc.)'

    SEGMENTS = [
        {
            'name': 'vip',
            'display_name': 'VIP Customer',
            'description': 'High-value customers with frequent purchases and significant lifetime spending.',
            'min_total_spent': Decimal('5000'),
            'min_total_spent_currency': 'USD',
            'min_orders': 10,
            'max_days_since_last_purchase': 90,
            'color': '#FFD700',
            'priority': 100,
        },
        {
            'name': 'high_value',
            'display_name': 'High Value',
            'description': 'Customers with significant spending but moderate purchase frequency.',
            'min_total_spent': Decimal('2000'),
            'min_total_spent_currency': 'USD',
            'max_total_spent': Decimal('4999'),
            'max_total_spent_currency': 'USD',
            'min_orders': 5,
            'max_days_since_last_purchase': 120,
            'color': '#9B59B6',
            'priority': 90,
        },
        {
            'name': 'frequent_buyer',
            'display_name': 'Frequent Buyer',
            'description': 'Regular customers with consistent purchase patterns.',
            'min_orders': 8,
            'max_days_since_last_purchase': 60,
            'color': '#3498DB',
            'priority': 85,
        },
        {
            'name': 'regular',
            'display_name': 'Regular Customer',
            'description': 'Established customers with moderate spending and purchase frequency.',
            'min_total_spent': Decimal('500'),
            'min_total_spent_currency': 'USD',
            'max_total_spent': Decimal('1999'),
            'max_total_spent_currency': 'USD',
            'min_orders': 3,
            'max_orders': 7,
            'max_days_since_last_purchase': 90,
            'color': '#2ECC71',
            'priority': 70,
        },
        {
            'name': 'new',
            'display_name': 'New Customer',
            'description': 'Recently acquired customers. Focus on onboarding and building initial loyalty.',
            'max_orders': 2,
            'max_days_since_last_purchase': 30,
            'color': '#1ABC9C',
            'priority': 60,
        },
        {
            'name': 'at_risk',
            'display_name': 'At Risk',
            'description': 'Previously active customers who haven\'t purchased recently.',
            'min_orders': 2,
            'min_days_since_last_purchase': 91,
            'max_days_since_last_purchase': 180,
            'color': '#F39C12',
            'priority': 50,
        },
        {
            'name': 'inactive',
            'display_name': 'Inactive',
            'description': 'Customers with no recent activity.',
            'min_days_since_last_purchase': 181,
            'color': '#95A5A6',
            'priority': 40,
        },
        {
            'name': 'bargain_hunter',
            'display_name': 'Bargain Hunter',
            'description': 'Price-sensitive customers who primarily purchase during sales.',
            'max_total_spent': Decimal('499'),
            'max_total_spent_currency': 'USD',
            'min_orders': 2,
            'max_days_since_last_purchase': 120,
            'color': '#E67E22',
            'priority': 30,
        },
    ]

    def seed(self) -> int:
        from customers.models import CustomerSegment

        count = 0
        for data in self.SEGMENTS:
            _, created = CustomerSegment.objects.get_or_create(
                name=data['name'],
                defaults=data,
            )
            if created:
                count += 1
        return count
