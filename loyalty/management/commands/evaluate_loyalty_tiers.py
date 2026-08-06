"""
Management command to evaluate loyalty tiers for all members.

This command should be run periodically (e.g., daily via cron) to ensure
all members have the correct tier based on their current metrics.
"""

import argparse

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from loyalty.models import LoyaltyMember
from loyalty.services.tiering_service import TieringService


def positive_int(value):
    """Argparse type that accepts only strictly positive integers."""
    ivalue = int(value)
    if ivalue < 1:
        raise argparse.ArgumentTypeError("--limit must be a positive integer")
    return ivalue


class Command(BaseCommand):
    help = "Evaluate and update loyalty tiers for all active members"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=positive_int,
            default=None,
            help="Limit number of members to process (for testing)",
        )

        parser.add_argument(
            "--dry-run", action="store_true", help="Run without making any changes (preview only)"
        )

    def handle(self, *args, **options):
        limit = options.get("limit")
        dry_run = options.get("dry_run")

        self.stdout.write(
            self.style.SUCCESS(f"Starting loyalty tier evaluation at {timezone.now()}")
        )

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN MODE - No changes will be saved"))

        if limit is not None:
            self.stdout.write(f"Processing limit: {limit} members")

        # Initialize tiering service
        tiering_service = TieringService()

        try:
            # Run batch evaluation
            if dry_run:
                stats = self._evaluate_dry_run(tiering_service, limit)
            else:
                stats = tiering_service.batch_evaluate_all_members(limit=limit)

            # Display results
            self.stdout.write("\n" + "=" * 60)
            self.stdout.write(self.style.SUCCESS("Tier Evaluation Complete"))
            self.stdout.write("=" * 60)
            self.stdout.write(f"Total Processed: {stats['total_processed']}")
            self.stdout.write(self.style.SUCCESS(f"Promotions: {stats['promotions']}"))
            self.stdout.write(self.style.WARNING(f"Demotions: {stats['demotions']}"))
            self.stdout.write(f"No Change: {stats['no_change']}")

            if stats["errors"] > 0:
                self.stdout.write(self.style.ERROR(f"Errors: {stats['errors']}"))

            self.stdout.write("=" * 60)

            # Exit code based on errors
            if stats["errors"] > 0:
                raise CommandError(f"Completed with {stats['errors']} error(s)")

        except CommandError:
            # Intentional command errors (e.g. errors > 0) must surface unchanged.
            raise
        except Exception as e:
            raise CommandError(f"Tier evaluation failed: {str(e)}")

    def _evaluate_dry_run(self, tiering_service, limit):
        """Preview tier changes without persisting updates or sending notifications."""
        members = LoyaltyMember.objects.filter(is_active=True)

        if limit is not None:
            members = members[:limit]

        stats = {
            "total_processed": 0,
            "promotions": 0,
            "demotions": 0,
            "no_change": 0,
            "errors": 0,
        }

        for member in members:
            try:
                current_tier = member.current_tier
                eligible_tier = tiering_service.calculate_eligible_tier(member)

                stats["total_processed"] += 1

                if current_tier == eligible_tier:
                    stats["no_change"] += 1
                elif eligible_tier and (not current_tier or eligible_tier.rank < current_tier.rank):
                    stats["promotions"] += 1
                elif current_tier and (not eligible_tier or eligible_tier.rank > current_tier.rank):
                    # A real run defers demotion while a grace period applies, so
                    # the preview must too — otherwise members with an active or
                    # newly applicable grace period are miscounted as demotions.
                    if tiering_service.is_within_grace_period(member, current_tier):
                        stats["no_change"] += 1
                    else:
                        stats["demotions"] += 1
                else:
                    stats["no_change"] += 1

            except Exception as e:
                stats["errors"] += 1
                self.stderr.write(f"Error evaluating tier for member {member.id}: {e}")

        return stats
