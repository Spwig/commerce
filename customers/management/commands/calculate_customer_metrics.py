"""
Management command to calculate customer metrics for all users
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Q
from customers.models import CustomerMetrics, CustomerSegment

User = get_user_model()


class Command(BaseCommand):
    help = 'Calculate customer metrics and segments for all users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-id',
            type=int,
            help='Calculate metrics for a specific user ID',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recalculation even if metrics already exist',
        )
        parser.add_argument(
            '--show-segments',
            action='store_true',
            help='Display segment distribution after calculation',
        )

    def handle(self, *args, **options):
        user_id = options.get('user_id')
        force = options.get('force', False)
        show_segments = options.get('show_segments', False)

        # Get users to process
        if user_id:
            users = User.objects.filter(id=user_id)
            if not users.exists():
                self.stdout.write(self.style.ERROR(f'User with ID {user_id} not found'))
                return
        else:
            # Get all authenticated users, exclude guest users
            users = User.objects.filter(
                Q(username__isnull=False) & ~Q(username__startswith='guest_')
            )

        total_users = users.count()
        self.stdout.write(self.style.SUCCESS(f'\nCalculating metrics for {total_users} users...\n'))

        # Track statistics
        calculated_count = 0
        skipped_count = 0
        error_count = 0
        segment_distribution = {}

        # Process each user
        for index, user in enumerate(users, 1):
            try:
                # Skip if metrics already exist and not forcing
                if not force and hasattr(user, 'customer_metrics'):
                    skipped_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'[{index}/{total_users}] Skipped {user.username} (metrics exist)')
                    )
                    continue

                # Calculate metrics
                metrics = CustomerMetrics.calculate_for_user(user)

                if metrics:
                    calculated_count += 1

                    # Determine segment
                    segment = CustomerSegment.determine_segment_for_user(user)
                    segment_name = segment.display_name if segment else 'Unassigned'

                    # Track segment distribution
                    if segment_name not in segment_distribution:
                        segment_distribution[segment_name] = 0
                    segment_distribution[segment_name] += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f'[{index}/{total_users}] ✓ {user.username} - '
                            f'${metrics.total_spent.amount:.2f} spent, '
                            f'{metrics.completed_orders} orders - '
                            f'Segment: {segment_name}'
                        )
                    )
                else:
                    skipped_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'[{index}/{total_users}] - {user.username} (no orders)')
                    )

            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'[{index}/{total_users}] ✗ Error processing {user.username}: {str(e)}')
                )

        # Display summary
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS('\nCalculation Summary:'))
        self.stdout.write(f'  Total users processed: {total_users}')
        self.stdout.write(self.style.SUCCESS(f'  ✓ Calculated: {calculated_count}'))
        self.stdout.write(self.style.WARNING(f'  - Skipped: {skipped_count}'))
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'  ✗ Errors: {error_count}'))

        # Display segment distribution if requested
        if show_segments and segment_distribution:
            self.stdout.write('\n' + self.style.SUCCESS('Segment Distribution:'))
            for segment_name, count in sorted(segment_distribution.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / calculated_count * 100) if calculated_count > 0 else 0
                self.stdout.write(f'  {segment_name}: {count} ({percentage:.1f}%)')

        self.stdout.write('\n' + '=' * 70 + '\n')

        # Display available segments
        active_segments = CustomerSegment.objects.filter(is_active=True).count()
        self.stdout.write(
            self.style.SUCCESS(f'\n{active_segments} active customer segments available in the system.\n')
        )
