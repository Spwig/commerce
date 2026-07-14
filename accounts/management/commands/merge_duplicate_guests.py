"""
Management command to find and merge duplicate guest users.

Guest checkout previously created a new User for every order, even with the
same email. This command consolidates those duplicates so each email has a
single canonical guest user with all orders linked to it.

Usage:
    python manage.py merge_duplicate_guests              # Dry-run (default)
    python manage.py merge_duplicate_guests --execute     # Actually merge
    python manage.py merge_duplicate_guests --email foo@bar.com  # Single email
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models import Count

User = get_user_model()


class Command(BaseCommand):
    help = "Find and merge duplicate guest users (same email, multiple guest_ accounts)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--execute",
            action="store_true",
            default=False,
            help="Actually perform the merge. Without this flag, only shows what would happen.",
        )
        parser.add_argument(
            "--email",
            type=str,
            default=None,
            help="Merge duplicates for a specific email only.",
        )

    def handle(self, *args, **options):
        from accounts.services.account_creation_service import AccountCreationService

        execute = options["execute"]
        target_email = options["email"]

        if not execute:
            self.stdout.write(
                self.style.WARNING("DRY RUN — no changes will be made. Use --execute to apply.\n")
            )

        # Find emails with multiple guest users
        if target_email:
            normalized = target_email.lower().strip()
            guest_groups = (
                User.objects.filter(
                    username__startswith="guest_",
                    email__iexact=normalized,
                )
                .values("email")
                .annotate(count=Count("id"))
                .filter(count__gt=1)
            )
        else:
            guest_groups = (
                User.objects.filter(username__startswith="guest_")
                .values("email")
                .annotate(count=Count("id"))
                .filter(count__gt=1)
                .order_by("-count")
            )

        total_groups = guest_groups.count()
        if total_groups == 0:
            self.stdout.write(self.style.SUCCESS("No duplicate guest users found."))
            return

        self.stdout.write(f"Found {total_groups} email(s) with duplicate guest users:\n")

        total_stats = {"orders_moved": 0, "addresses_moved": 0, "users_deleted": 0}

        for group in guest_groups:
            email = group["email"]
            count = group["count"]

            guests = list(
                User.objects.filter(email__iexact=email, username__startswith="guest_").order_by(
                    "-date_joined"
                )
            )

            canonical = guests[0]
            duplicates = guests[1:]

            # Count orders per user for reporting
            order_counts = []
            for g in guests:
                oc = g.orders.count() if hasattr(g, "orders") else 0
                order_counts.append(f"{g.username}({oc} orders)")

            self.stdout.write(
                f"  {email}: {count} guests — keep {canonical.username}, "
                f"merge {len(duplicates)} duplicate(s)"
            )
            self.stdout.write(f"    Users: {', '.join(order_counts)}")

            if execute:
                stats = AccountCreationService.merge_guest_users(canonical, duplicates)
                total_stats["orders_moved"] += stats["orders_moved"]
                total_stats["addresses_moved"] += stats["addresses_moved"]
                total_stats["users_deleted"] += stats["users_deleted"]
                self.stdout.write(
                    self.style.SUCCESS(
                        f"    Merged: {stats['orders_moved']} orders, "
                        f"{stats['addresses_moved']} addresses, "
                        f"{stats['users_deleted']} users deleted"
                    )
                )

        self.stdout.write("")
        if execute:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Done. Totals: {total_stats['orders_moved']} orders moved, "
                    f"{total_stats['addresses_moved']} addresses moved, "
                    f"{total_stats['users_deleted']} duplicate users deleted."
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING("Dry run complete. Run with --execute to apply changes.")
            )
