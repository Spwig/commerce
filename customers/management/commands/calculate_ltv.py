"""
Management command to calculate customer LTV
Usage:
    python manage.py calculate_ltv [options]
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.utils import timezone

from customers.models import CustomerMetrics, LTVSettings
from customers.services.cohort_service import CohortService
from customers.services.probabilistic_ltv_service import ProbabilisticLTVService
from customers.tasks import calculate_all_customer_ltv_task, calculate_customer_ltv_task

User = get_user_model()


class Command(BaseCommand):
    help = 'Calculate customer lifetime value using configured method'

    def add_arguments(self, parser):
        parser.add_argument(
            '--method',
            type=str,
            choices=['simple', 'cohort', 'probabilistic'],
            help='Force specific calculation method (overrides settings)',
        )

        parser.add_argument(
            '--user',
            type=int,
            help='Calculate LTV for specific user ID',
        )

        parser.add_argument(
            '--all',
            action='store_true',
            help='Calculate LTV for all customers',
        )

        parser.add_argument(
            '--async',
            action='store_true',
            dest='use_async',
            help='Run calculation asynchronously via Celery',
        )

        parser.add_argument(
            '--check-quality',
            action='store_true',
            help='Check data quality for probabilistic methods',
        )

        parser.add_argument(
            '--rebuild-cohorts',
            action='store_true',
            help='Rebuild all cohorts and recalculate metrics',
        )

    def handle(self, *args, **options):
        # Get settings
        settings = LTVSettings.get_settings()
        method = options.get('method') or settings.calculation_method

        # Check data quality
        if options['check_quality']:
            return self.check_data_quality()

        # Rebuild cohorts
        if options['rebuild_cohorts']:
            return self.rebuild_cohorts()

        # Single user calculation
        if options['user']:
            return self.calculate_single_user(options['user'], method, options['use_async'])

        # All customers calculation
        if options['all']:
            return self.calculate_all_customers(method, options['use_async'])

        # No action specified
        raise CommandError(
            'Please specify either --user <id>, --all, --check-quality, or --rebuild-cohorts'
        )

    def calculate_single_user(self, user_id, method, use_async):
        """Calculate LTV for a single user"""
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise CommandError(f'User with ID {user_id} not found')

        self.stdout.write(f'Calculating LTV for user {user_id} using {method} method...')

        if use_async:
            # Queue Celery task
            task = calculate_customer_ltv_task.delay(user_id)
            self.stdout.write(
                self.style.SUCCESS(f'✓ Task queued: {task.id}')
            )
        else:
            # Calculate synchronously
            start_time = timezone.now()

            if method == 'simple':
                CustomerMetrics.calculate_for_user(user)
                self.stdout.write(
                    self.style.SUCCESS(f'✓ LTV calculated using simple RFM method')
                )

            elif method == 'cohort':
                metrics = CustomerMetrics.calculate_for_user(user)
                if metrics and metrics.cohort_month:
                    # Ensure cohort exists
                    CohortService.build_all_cohorts()
                    CohortService.update_customer_cohort_ltv()
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ LTV calculated using cohort method')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING('⚠ Customer has no cohort data, using simple method')
                    )
                    CustomerMetrics.calculate_for_user(user)

            elif method == 'probabilistic':
                service = ProbabilisticLTVService()

                # Check data quality first
                quality = ProbabilisticLTVService.check_data_quality()
                if not quality['can_use_probabilistic']:
                    self.stdout.write(
                        self.style.WARNING(
                            f'⚠ Insufficient data quality ({quality["recommendation"]}), '
                            f'using simple method'
                        )
                    )
                    CustomerMetrics.calculate_for_user(user)
                else:
                    # Fit models
                    self.stdout.write('Fitting probabilistic models...')
                    fit_result = service.fit_models()

                    if not fit_result['success']:
                        raise CommandError(f'Model fitting failed: {fit_result.get("error")}')

                    self.stdout.write(f'  Models fitted on {fit_result["customers_used"]} customers')

                    # Predict for user
                    prediction = service.predict_customer_ltv(user)

                    if prediction['success']:
                        from djmoney.money import Money
                        metrics = CustomerMetrics.objects.get(user=user)
                        default_currency = ProbabilisticLTVService.get_default_currency()

                        metrics.lifetime_value = Money(prediction['ltv'], default_currency)
                        metrics.probability_alive = prediction['probability_alive']
                        metrics.predicted_purchases_12m = prediction['predicted_purchases']
                        metrics.ltv_confidence_score = prediction['confidence']
                        metrics.ltv_calculation_method = 'probabilistic'
                        metrics.ltv_last_calculated = timezone.now()
                        metrics.save()

                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✓ LTV calculated: ${prediction["ltv"]:.2f} '
                                f'(P(alive): {prediction["probability_alive"]:.2%}, '
                                f'Confidence: {prediction["confidence"]:.2f})'
                            )
                        )
                    else:
                        raise CommandError(f'Prediction failed: {prediction.get("error")}')

            duration = (timezone.now() - start_time).total_seconds()
            self.stdout.write(f'Completed in {duration:.2f} seconds')

            # Display results
            metrics = CustomerMetrics.objects.get(user=user)
            self.stdout.write('')
            self.stdout.write('Results:')
            self.stdout.write(f'  LTV: {metrics.lifetime_value}')
            self.stdout.write(f'  Total Spent: {metrics.total_spent}')
            self.stdout.write(f'  Completed Orders: {metrics.completed_orders}')
            self.stdout.write(f'  Confidence: {metrics.ltv_confidence_score:.2%}')

    def calculate_all_customers(self, method, use_async):
        """Calculate LTV for all customers"""
        customer_count = CustomerMetrics.objects.filter(completed_orders__gte=1).count()

        self.stdout.write(
            f'Calculating LTV for {customer_count} customers using {method} method...'
        )

        if use_async:
            # Queue Celery task
            task = calculate_all_customer_ltv_task.delay()
            self.stdout.write(
                self.style.SUCCESS(f'✓ Task queued: {task.id}')
            )
            self.stdout.write('Use celery logs to monitor progress')
        else:
            # Calculate synchronously
            start_time = timezone.now()

            if method == 'simple':
                customers_updated = 0
                customers = User.objects.filter(is_active=True).exclude(
                    username__startswith='guest_'
                )

                for i, user in enumerate(customers, 1):
                    try:
                        CustomerMetrics.calculate_for_user(user)
                        customers_updated += 1

                        if i % 100 == 0:
                            self.stdout.write(f'  Processed {i}/{customer_count} customers...')
                    except Exception as e:
                        self.stdout.write(
                            self.style.WARNING(f'  Error for user {user.id}: {str(e)}')
                        )

                self.stdout.write(
                    self.style.SUCCESS(f'✓ Updated {customers_updated} customers')
                )

            elif method == 'cohort':
                self.stdout.write('Step 1: Building cohorts...')
                cohort_result = CohortService.build_all_cohorts()
                self.stdout.write(
                    f'  Created: {cohort_result["cohorts_created"]}, '
                    f'Updated: {cohort_result["cohorts_updated"]}'
                )

                self.stdout.write('Step 2: Calculating cohort metrics...')
                metrics_result = CohortService.calculate_cohort_metrics()
                self.stdout.write(
                    f'  Metrics created: {metrics_result["metrics_created"]}, '
                    f'Updated: {metrics_result["metrics_updated"]}'
                )

                self.stdout.write('Step 3: Updating customer LTV...')
                update_result = CohortService.update_customer_cohort_ltv()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Updated {update_result["customers_updated"]} customers'
                    )
                )

            elif method == 'probabilistic':
                # Check data quality
                quality = ProbabilisticLTVService.check_data_quality()
                self.stdout.write(
                    f'Data Quality: {quality["repeat_customers"]} repeat customers, '
                    f'{quality["data_span_days"]} days of history'
                )

                if not quality['can_use_probabilistic']:
                    raise CommandError(
                        f'Insufficient data quality ({quality["recommendation"]}). '
                        f'Need at least {quality["min_threshold"]} repeat customers and 180 days of history.'
                    )

                service = ProbabilisticLTVService()
                result = service.update_all_customer_ltv()

                if result['success']:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ Updated {result["customers_updated"]} customers, '
                            f'Failed: {result["customers_failed"]}'
                        )
                    )
                else:
                    raise CommandError(f'Calculation failed: {result.get("error")}')

            duration = (timezone.now() - start_time).total_seconds()
            self.stdout.write(f'Completed in {duration:.2f} seconds')

            # Update settings
            settings = LTVSettings.get_settings()
            settings.last_calculation_run = timezone.now()
            settings.save()

    def check_data_quality(self):
        """Check data quality for probabilistic methods"""
        self.stdout.write('Checking data quality for probabilistic LTV calculation...')

        quality = ProbabilisticLTVService.check_data_quality()

        self.stdout.write('')
        self.stdout.write('Data Quality Report:')
        self.stdout.write(f'  Total customers: {quality["total_customers"]}')
        self.stdout.write(f'  Repeat customers: {quality["repeat_customers"]}')
        self.stdout.write(f'  Data span: {quality["data_span_days"]} days')
        self.stdout.write(f'  Quality score: {quality["quality_score"]:.2%}')
        self.stdout.write('')

        if quality['can_use_probabilistic']:
            self.stdout.write(
                self.style.SUCCESS('✓ Data quality is sufficient for probabilistic methods')
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'⚠ Data quality is insufficient: {quality["recommendation"]}'
                )
            )
            self.stdout.write(
                f'  Need at least {quality["min_threshold"]} repeat customers and 180 days of history'
            )

    def rebuild_cohorts(self):
        """Rebuild all cohorts"""
        self.stdout.write('Rebuilding customer cohorts...')
        start_time = timezone.now()

        self.stdout.write('Step 1: Building cohorts...')
        cohort_result = CohortService.build_all_cohorts()
        self.stdout.write(
            f'  Created: {cohort_result["cohorts_created"]}, '
            f'Updated: {cohort_result["cohorts_updated"]}, '
            f'Customers assigned: {cohort_result["customers_assigned"]}'
        )

        self.stdout.write('Step 2: Calculating cohort metrics...')
        metrics_result = CohortService.calculate_cohort_metrics()
        self.stdout.write(
            f'  Metrics created: {metrics_result["metrics_created"]}, '
            f'Updated: {metrics_result["metrics_updated"]}'
        )

        duration = (timezone.now() - start_time).total_seconds()
        self.stdout.write(
            self.style.SUCCESS(f'✓ Cohorts rebuilt in {duration:.2f} seconds')
        )
