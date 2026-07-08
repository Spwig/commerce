"""
Management command to release held emails.

Usage:
    python manage.py release_held_emails          # Release only (transition held -> queued)
    python manage.py release_held_emails --send    # Release and immediately send
    python manage.py release_held_emails --dry-run # Show count without making changes
"""
from django.core.management.base import BaseCommand

from email_system.models import EmailOutbox
from email_system.services.email_sender import EmailSendingService


class Command(BaseCommand):
    help = 'Release all held emails (transition from held to queued and optionally send them)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--send',
            action='store_true',
            help='Immediately attempt delivery after releasing',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be released without making changes',
        )

    def handle(self, *args, **options):
        held_count = EmailOutbox.objects.filter(status='held').count()

        if held_count == 0:
            self.stdout.write(self.style.SUCCESS('No held emails to release.'))
            return

        if options['dry_run']:
            self.stdout.write(f'Would release {held_count} held email(s).')
            return

        result = EmailSendingService.release_held_emails(send_now=options['send'])

        self.stdout.write(self.style.SUCCESS(
            f"Released {result['released']} email(s)."
        ))
        if options['send']:
            self.stdout.write(self.style.SUCCESS(
                f"Sent: {result['sent']}, Failed: {result['failed']}"
            ))
