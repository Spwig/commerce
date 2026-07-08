"""
Management command to notify hosted subscribers to update their payment method.

Use when switching to a new payment provider account (e.g., new Airwallex account).
Sends each active subscriber an email asking them to update their card details
via the self-service account page.

Usage:
    python manage.py notify_payment_update --dry-run     # Preview only
    python manage.py notify_payment_update               # Send emails
    python manage.py notify_payment_update --status suspended  # Only suspended
"""
import logging
from django.core.management.base import BaseCommand
from django.utils import timezone

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Email hosted subscribers asking them to update their payment method'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run', action='store_true',
            help='Preview which subscribers would be emailed without sending',
        )
        parser.add_argument(
            '--status', type=str, default='active,past_due',
            help='Comma-separated subscription statuses to include (default: active,past_due)',
        )

    def handle(self, *args, **options):
        from license_checkout.models import HostedSubscription
        from license_checkout.services import _send_hosting_email

        dry_run = options['dry_run']
        statuses = [s.strip() for s in options['status'].split(',')]

        subscriptions = HostedSubscription.objects.filter(
            status__in=statuses,
        ).select_related('hosted_plan')

        total = subscriptions.count()
        self.stdout.write(f'Found {total} subscriptions with status in {statuses}')

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN — no emails will be sent'))

        sent = 0
        for sub in subscriptions:
            self.stdout.write(f'  {sub.store_slug} ({sub.email}) — {sub.hosted_plan.name} [{sub.status}]')

            if not dry_run:
                try:
                    _send_hosting_email(
                        to_email=sub.email,
                        template_type='hosted_payment_failed',
                        context={
                            'store_name': sub.store_name,
                            'plan_name': sub.hosted_plan.name,
                            'amount': str(sub.billing_amount),
                            'currency': 'EUR',
                            'retry_info': (
                                'We are updating our payment systems and need you to '
                                're-enter your card details to ensure uninterrupted service'
                            ),
                        },
                        label='payment update notification (provider switch)',
                    )
                    sent += 1
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'  Failed to send to {sub.email}: {e}'))

        if dry_run:
            self.stdout.write(self.style.SUCCESS(f'Would send {total} emails'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Sent {sent}/{total} emails'))
