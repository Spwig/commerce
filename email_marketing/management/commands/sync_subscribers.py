"""Populate Campaign Studio subscribers from existing customer accounts.

Creates one Subscriber per active, non-staff customer account (linked to the
User), so audiences/segments can target the real customer base. Idempotent —
re-running only adds missing rows. Consent is NOT set here: for a linked user,
``Subscriber.is_emailable`` defers to their CommunicationPreference at send time,
so marketing consent stays governed by the customer's own preferences.
"""

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

from email_marketing.models import Subscriber


class Command(BaseCommand):
    help = "Create Subscriber rows for existing customer accounts (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--include-staff",
            action="store_true",
            help="Also create subscribers for staff accounts (default: customers only).",
        )

    def handle(self, *args, **options):
        User = get_user_model()
        site = Site.objects.get(pk=1)

        users = User.objects.filter(is_active=True).exclude(email="")
        if not options["include_staff"]:
            users = users.filter(is_staff=False)

        # Emails already tracked (registered or anonymous) — skip to stay idempotent.
        existing = set(Subscriber.all_objects.filter(site=site).values_list("email", flat=True))

        created = 0
        for user in users.iterator():
            if user.email in existing:
                continue
            Subscriber.objects.create(
                site=site,
                email=user.email,
                user=user,
                source="order",
                language_code=getattr(user, "language", "") or "",
                status=Subscriber.STATUS_ACTIVE,
            )
            existing.add(user.email)
            created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Synced {created} new subscriber(s); "
                f"{Subscriber.objects.filter(site=site).count()} total."
            )
        )
